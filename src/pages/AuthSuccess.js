/**
 * OAuth Success Page - Handles post-authentication flow
 */

import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../components/GoogleAuth';
import './AuthSuccess.css';

const AuthSuccess = () => {
  const navigate = useNavigate();
  const { user, loading } = useAuth();

  useEffect(() => {
    // Redirect to home after successful authentication
    if (!loading && user) {
      setTimeout(() => {
        navigate('/');
      }, 2000);
    }
  }, [user, loading, navigate]);

  if (loading) {
    return (
      <div className="auth-success-page">
        <div className="auth-success-content">
          <div className="loading-spinner"></div>
          <h2>Authenticating...</h2>
          <p>Please wait while we sign you in.</p>
        </div>
      </div>
    );
  }

  if (user) {
    return (
      <div className="auth-success-page">
        <div className="auth-success-content">
          <div className="success-icon">✓</div>
          <h2>Welcome, {user.given_name || user.name}!</h2>
          <p>You have been successfully signed in.</p>
          <p className="redirect-message">Redirecting to NewsHub...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="auth-success-page">
      <div className="auth-success-content">
        <div className="error-icon">⚠</div>
        <h2>Authentication Failed</h2>
        <p>There was an issue signing you in. Please try again.</p>
        <button 
          className="retry-button"
          onClick={() => navigate('/login')}
        >
          Try Again
        </button>
      </div>
    </div>
  );
};

export default AuthSuccess;
