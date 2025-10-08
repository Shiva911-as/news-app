/**
 * Professional Google OAuth Component
 * Matches Google's official design patterns and UX
 */

import React, { useState, useEffect, createContext, useContext } from 'react';
import './GoogleAuth.css';

// Auth Context for global state management
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [token, setToken] = useState(localStorage.getItem('auth_token'));

  useEffect(() => {
    // Check for token in URL (from OAuth callback)
    const urlParams = new URLSearchParams(window.location.search);
    const urlToken = urlParams.get('token');
    
    if (urlToken) {
      localStorage.setItem('auth_token', urlToken);
      setToken(urlToken);
      // Clean URL
      window.history.replaceState({}, document.title, window.location.pathname);
    }

    // Verify existing token
    if (token) {
      verifyToken(token);
    } else {
      setLoading(false);
    }
  }, [token]);

  const verifyToken = async (authToken) => {
    try {
      const response = await fetch('/auth/verify', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: authToken })
      });

      const data = await response.json();
      
      if (data.valid) {
        setUser(data.user);
      } else {
        localStorage.removeItem('auth_token');
        setToken(null);
      }
    } catch (error) {
      console.error('Token verification failed:', error);
      localStorage.removeItem('auth_token');
      setToken(null);
    } finally {
      setLoading(false);
    }
  };

  const login = () => {
    window.location.href = '/auth/login';
  };

  const logout = async () => {
    try {
      await fetch('/auth/logout', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem('auth_token');
      setToken(null);
      setUser(null);
    }
  };

  const value = {
    user,
    token,
    loading,
    login,
    logout,
    isAuthenticated: !!user
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

// Google Sign-In Button Component
export const GoogleSignInButton = ({ className = '', size = 'large' }) => {
  const { login } = useAuth();
  const [isHovered, setIsHovered] = useState(false);

  return (
    <button
      className={`google-signin-btn ${size} ${className}`}
      onClick={login}
      onMouseEnter={() => setIsHovered(true)}
      onMouseLeave={() => setIsHovered(false)}
    >
      <div className="google-signin-content">
        <svg className="google-icon" viewBox="0 0 24 24">
          <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
          <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
          <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
          <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
        </svg>
        <span className="google-signin-text">
          {size === 'large' ? 'Sign in with Google' : 'Google'}
        </span>
      </div>
    </button>
  );
};

// Account Chooser Component (like in your screenshots)
export const AccountChooser = ({ accounts = [], onSelectAccount, onUseAnotherAccount }) => {
  return (
    <div className="account-chooser">
      <div className="account-chooser-header">
        <div className="google-logo">
          <svg viewBox="0 0 24 24" className="google-logo-svg">
            <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
            <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
            <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
            <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
          </svg>
          <span>Sign in with Google</span>
        </div>
      </div>

      <div className="account-chooser-content">
        <h1 className="chooser-title">Choose an account</h1>
        <p className="chooser-subtitle">to continue to NewsHub</p>

        <div className="accounts-list">
          {accounts.map((account, index) => (
            <div 
              key={index}
              className="account-item"
              onClick={() => onSelectAccount(account)}
            >
              <div className="account-avatar">
                {account.picture ? (
                  <img src={account.picture} alt={account.name} />
                ) : (
                  <div className="avatar-placeholder">
                    {account.name?.charAt(0)?.toUpperCase() || account.email?.charAt(0)?.toUpperCase()}
                  </div>
                )}
              </div>
              <div className="account-info">
                <div className="account-name">{account.name}</div>
                <div className="account-email">{account.email}</div>
              </div>
            </div>
          ))}
        </div>

        <div className="use-another-account" onClick={onUseAnotherAccount}>
          <div className="add-account-icon">+</div>
          <span>Use another account</span>
        </div>
      </div>
    </div>
  );
};

// User Profile Component
export const UserProfile = ({ user, onLogout, compact = false }) => {
  const [showDropdown, setShowDropdown] = useState(false);

  if (compact) {
    return (
      <div className="user-profile-compact">
        <div 
          className="profile-avatar-compact"
          onClick={() => setShowDropdown(!showDropdown)}
        >
          {user.picture ? (
            <img src={user.picture} alt={user.name} />
          ) : (
            <div className="avatar-placeholder">
              {user.name?.charAt(0)?.toUpperCase()}
            </div>
          )}
        </div>
        
        {showDropdown && (
          <div className="profile-dropdown">
            <div className="dropdown-header">
              <div className="dropdown-avatar">
                {user.picture ? (
                  <img src={user.picture} alt={user.name} />
                ) : (
                  <div className="avatar-placeholder">
                    {user.name?.charAt(0)?.toUpperCase()}
                  </div>
                )}
              </div>
              <div className="dropdown-info">
                <div className="dropdown-name">{user.name}</div>
                <div className="dropdown-email">{user.email}</div>
              </div>
            </div>
            <div className="dropdown-divider"></div>
            <button className="dropdown-item" onClick={onLogout}>
              Sign out
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="user-profile">
      <div className="profile-header">
        <div className="profile-avatar">
          {user.picture ? (
            <img src={user.picture} alt={user.name} />
          ) : (
            <div className="avatar-placeholder">
              {user.name?.charAt(0)?.toUpperCase()}
            </div>
          )}
        </div>
        <div className="profile-info">
          <h2 className="profile-name">{user.name}</h2>
          <p className="profile-email">{user.email}</p>
        </div>
      </div>
      
      <div className="profile-actions">
        <button className="profile-btn secondary" onClick={onLogout}>
          Sign Out
        </button>
      </div>
    </div>
  );
};

// Loading Spinner Component
export const AuthLoadingSpinner = () => (
  <div className="auth-loading">
    <div className="loading-spinner"></div>
    <p>Authenticating...</p>
  </div>
);

// Protected Route Component
export const ProtectedRoute = ({ children, fallback }) => {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <AuthLoadingSpinner />;
  }

  if (!isAuthenticated) {
    return fallback || <GoogleSignInButton />;
  }

  return children;
};
