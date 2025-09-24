from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
from datetime import datetime
from typing import Dict, List, Any

from config import get_config
from services.news_service import NewsService
from models.user_profile import UserProfile
from utils.logger import logger

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(get_config())
CORS(app)

# Initialize services
news_service = NewsService()

@app.route('/')
def index():
    """API endpoint for React app"""
    return jsonify({
        'message': 'News App API is running',
        'status': 'success'
    })

@app.route('/api/news/trending')
def api_trending_news():
    """API endpoint for trending news"""
    try:
        page_size = request.args.get('page_size', 20, type=int)
        page = request.args.get('page', 1, type=int)
        
        # Calculate offset for pagination
        offset = (page - 1) * page_size
        
        success, articles, error = news_service.get_trending_articles(page_size=page_size + offset)
        
        if success and articles:
            # Apply pagination
            paginated_articles = articles[offset:offset + page_size]
            
            return jsonify({
                'success': True,
                'articles': paginated_articles,
                'count': len(paginated_articles),
                'page': page,
                'page_size': page_size,
                'has_more': len(articles) > offset + page_size
            })
        else:
            error_msg = error or 'Unable to fetch trending news'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500
    
    except Exception as e:
        logger.error(f"Error in trending news API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/news/search')
def api_search_news():
    """API endpoint for searching news"""
    try:
        query = request.args.get('q', '')
        page_size = request.args.get('page_size', 20, type=int)
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Query parameter is required'
            }), 400
        
        success, articles, error = news_service.search_articles(query, page_size=page_size)
        
        if success and articles:
            return jsonify({
                'success': True,
                'articles': articles,
                'count': len(articles),
                'query': query
            })
        else:
            error_msg = error or 'No articles found for the query'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 404
    
    except Exception as e:
        logger.error(f"Error in search news API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/news/topic/<topic>')
def api_topic_news(topic):
    """API endpoint for topic-specific news"""
    try:
        page_size = request.args.get('page_size', 20, type=int)
        success, articles, error = news_service.get_articles_by_topic(topic, page_size=page_size)
        
        if success and articles:
            return jsonify({
                'success': True,
                'articles': articles,
                'count': len(articles),
                'topic': topic
            })
        else:
            error_msg = error or f'No articles found for topic: {topic}'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 404
    
    except Exception as e:
        logger.error(f"Error in topic news API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/profile', methods=['GET', 'POST'])
def api_profile():
    """API endpoint for user profile management"""
    try:
        user_id = session.get('user_id', 'default')
        user_profile = UserProfile(user_id)
        
        if request.method == 'GET':
            return jsonify({
                'success': True,
                'profile': user_profile.get_profile_summary()
            })
        
        elif request.method == 'POST':
            data = request.get_json()
            
            if 'interests' in data:
                user_profile.set_interests(data['interests'])
                return jsonify({
                    'success': True,
                    'message': 'Profile updated successfully',
                    'profile': user_profile.get_profile_summary()
                })
            else:
                return jsonify({
                    'success': False,
                    'error': 'Interests field is required'
                }), 400
    
    except Exception as e:
        logger.error(f"Error in profile API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/profile/learn', methods=['POST'])
def api_learn_from_article():
    """API endpoint for learning from article reading"""
    try:
        user_id = session.get('user_id', 'default')
        user_profile = UserProfile(user_id)
        
        data = request.get_json()
        
        if 'article' not in data:
            return jsonify({
                'success': False,
                'error': 'Article data is required'
            }), 400
        
        user_profile.learn_from_article(data['article'])
        
        return jsonify({
            'success': True,
            'message': 'Learned from article successfully'
        })
    
    except Exception as e:
        logger.error(f"Error in learn API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/recommendations')
def api_recommendations():
    """API endpoint for personalized recommendations"""
    try:
        user_id = session.get('user_id', 'default')
        user_profile = UserProfile(user_id)
        
        # Get trending articles for recommendations
        success, articles, error = news_service.get_trending_articles(page_size=50)
        
        if success and articles:
            recommendations = user_profile.get_recommendations(articles, limit=10)
            
            return jsonify({
                'success': True,
                'recommendations': [
                    {
                        'score': score,
                        'article': article
                    } for score, article in recommendations
                ],
                'count': len(recommendations)
            })
        else:
            error_msg = error or 'Unable to fetch recommendations'
            return jsonify({
                'success': False,
                'error': error_msg
            }), 500
    
    except Exception as e:
        logger.error(f"Error in recommendations API: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/setup', methods=['GET', 'POST'])
def setup():
    """Setup endpoint for React app"""
    return jsonify({
        'message': 'Setup endpoint - use React frontend',
        'status': 'success'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    logger.error(f"Internal server error: {error}")
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Ensure logs directory exists
    os.makedirs('logs', exist_ok=True)
    os.makedirs('user_profiles', exist_ok=True)
    
    logger.info("Starting News App")
    app.run(debug=app.config.get('DEBUG', False), host='0.0.0.0', port=5000)
