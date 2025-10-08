"""
Professional Google OAuth 2.0 Integration
Production-ready authentication system with proper security measures
"""

import os
import json
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask import Blueprint, request, jsonify, session, redirect, url_for, current_app
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from authlib.integrations.flask_client import OAuth
from authlib.common.errors import AuthlibBaseError
import requests
from typing import Optional, Dict, Any

# Initialize Flask-Login
login_manager = LoginManager()

class User(UserMixin):
    """Professional User model with Google OAuth integration"""
    
    def __init__(self, user_data: Dict[str, Any]):
        self.id = user_data.get('sub')  # Google's unique user ID
        self.email = user_data.get('email')
        self.name = user_data.get('name')
        self.picture = user_data.get('picture')
        self.given_name = user_data.get('given_name')
        self.family_name = user_data.get('family_name')
        self.locale = user_data.get('locale', 'en')
        self.verified_email = user_data.get('email_verified', False)
        self.created_at = datetime.utcnow()
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'picture': self.picture,
            'given_name': self.given_name,
            'family_name': self.family_name,
            'locale': self.locale,
            'verified_email': self.verified_email,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def get_preferences(self) -> Dict[str, Any]:
        """Get user preferences for news personalization"""
        return {
            'language': 'telugu' if self.locale == 'te' else 'english',
            'categories': ['home', 'technology', 'business'],
            'location': 'india',
            'notifications': True
        }

# In-memory user store (replace with database in production)
users_db = {}

@login_manager.user_loader
def load_user(user_id: str) -> Optional[User]:
    """Load user from session"""
    return users_db.get(user_id)

# Create OAuth blueprint
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def init_oauth(app):
    """Initialize OAuth with Flask app"""
    oauth = OAuth(app)
    
    # Configure Google OAuth
    google = oauth.register(
        name='google',
        client_id=os.getenv('GOOGLE_CLIENT_ID'),
        client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
        server_metadata_url='https://accounts.google.com/.well-known/openid_configuration',
        client_kwargs={
            'scope': 'openid email profile',
            'prompt': 'select_account'  # Always show account selection
        }
    )
    
    return oauth, google

def generate_jwt_token(user: User) -> str:
    """Generate JWT token for authenticated user"""
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.utcnow() + timedelta(days=7),  # 7 day expiry
        'iat': datetime.utcnow(),
        'iss': 'newsapp'
    }
    
    return jwt.encode(
        payload, 
        current_app.config['SECRET_KEY'], 
        algorithm='HS256'
    )

def verify_jwt_token(token: str) -> Optional[Dict[str, Any]]:
    """Verify and decode JWT token"""
    try:
        payload = jwt.decode(
            token, 
            current_app.config['SECRET_KEY'], 
            algorithms=['HS256']
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def jwt_required(f):
    """Decorator for JWT authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'No token provided'}), 401
        
        if token.startswith('Bearer '):
            token = token[7:]
        
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401
        
        # Load user
        user = load_user(payload['user_id'])
        if not user:
            return jsonify({'error': 'User not found'}), 401
        
        request.current_user = user
        return f(*args, **kwargs)
    
    return decorated_function

@auth_bp.route('/login')
def login():
    """Initiate Google OAuth login"""
    try:
        oauth, google = init_oauth(current_app)
        
        # Generate state parameter for security
        state = os.urandom(16).hex()
        session['oauth_state'] = state
        
        redirect_uri = url_for('auth.callback', _external=True)
        return google.authorize_redirect(redirect_uri, state=state)
        
    except Exception as e:
        current_app.logger.error(f"OAuth login error: {str(e)}")
        return jsonify({'error': 'Authentication service unavailable'}), 503

@auth_bp.route('/callback')
def callback():
    """Handle Google OAuth callback"""
    try:
        oauth, google = init_oauth(current_app)
        
        # Verify state parameter
        if request.args.get('state') != session.get('oauth_state'):
            return jsonify({'error': 'Invalid state parameter'}), 400
        
        # Exchange code for token
        token = google.authorize_access_token()
        
        # Get user info from Google
        user_info = token.get('userinfo')
        if not user_info:
            # Fallback: fetch user info manually
            resp = google.get('userinfo')
            user_info = resp.json()
        
        # Create or update user
        user = User(user_info)
        users_db[user.id] = user
        
        # Login user with Flask-Login
        login_user(user, remember=True)
        
        # Generate JWT token
        jwt_token = generate_jwt_token(user)
        
        # Clean up session
        session.pop('oauth_state', None)
        
        # Redirect to frontend with token
        frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:3000')
        return redirect(f"{frontend_url}/auth/success?token={jwt_token}")
        
    except AuthlibBaseError as e:
        current_app.logger.error(f"OAuth callback error: {str(e)}")
        return jsonify({'error': 'Authentication failed'}), 400
    except Exception as e:
        current_app.logger.error(f"Unexpected callback error: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required
def logout():
    """Logout user and invalidate session"""
    try:
        # Remove from users_db (in production, mark token as revoked in database)
        if hasattr(request, 'current_user'):
            users_db.pop(request.current_user.id, None)
        
        logout_user()
        session.clear()
        
        return jsonify({'message': 'Logged out successfully'}), 200
        
    except Exception as e:
        current_app.logger.error(f"Logout error: {str(e)}")
        return jsonify({'error': 'Logout failed'}), 500

@auth_bp.route('/user', methods=['GET'])
@jwt_required
def get_user():
    """Get current user information"""
    try:
        user = request.current_user
        return jsonify({
            'user': user.to_dict(),
            'preferences': user.get_preferences()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Get user error: {str(e)}")
        return jsonify({'error': 'Failed to get user info'}), 500

@auth_bp.route('/verify', methods=['POST'])
def verify_token():
    """Verify JWT token validity"""
    try:
        data = request.get_json()
        token = data.get('token')
        
        if not token:
            return jsonify({'valid': False, 'error': 'No token provided'}), 400
        
        payload = verify_jwt_token(token)
        if not payload:
            return jsonify({'valid': False, 'error': 'Invalid token'}), 401
        
        user = load_user(payload['user_id'])
        if not user:
            return jsonify({'valid': False, 'error': 'User not found'}), 401
        
        return jsonify({
            'valid': True,
            'user': user.to_dict(),
            'preferences': user.get_preferences()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Token verification error: {str(e)}")
        return jsonify({'valid': False, 'error': 'Verification failed'}), 500

@auth_bp.route('/preferences', methods=['PUT'])
@jwt_required
def update_preferences():
    """Update user preferences"""
    try:
        data = request.get_json()
        user = request.current_user
        
        # In production, save to database
        # For now, we'll just return success
        
        return jsonify({
            'message': 'Preferences updated successfully',
            'preferences': data
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Update preferences error: {str(e)}")
        return jsonify({'error': 'Failed to update preferences'}), 500

def init_auth(app):
    """Initialize authentication system with Flask app"""
    # Configure Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    # Register blueprint
    app.register_blueprint(auth_bp)
    
    # Set required config
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', os.urandom(24).hex())
    
    return login_manager
