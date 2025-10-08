import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { ArrowLeft } from 'lucide-react';
import { GoogleSignInButton, useAuth } from '../components/GoogleAuth';
import './Login.css';

const Login = () => {
  const navigate = useNavigate();
  const { isAuthenticated, loading } = useAuth();

  // Redirect if already authenticated
  useEffect(() => {
    if (!loading && isAuthenticated) {
      navigate('/');
    }
  }, [isAuthenticated, loading, navigate]);

  const handleBackToChat = () => {
    navigate('/');
  };

  return (
    <div className="login-container">
      <div className="login-background">
        <div className="login-grid"></div>
        <div className="login-gradient"></div>
      </div>
      
      <div className="login-content">
        <button className="back-button" onClick={handleBackToChat}>
          <ArrowLeft size={20} />
          <span>Back to Chat</span>
        </button>
        
        <div className="login-card">
          <div className="login-header">
            <h1 className="login-title">
              Welcome to <span className="brand-name">NewsHub</span>
            </h1>
            <p className="login-subtitle">
              Sign in to access personalized news and preferences
            </p>
          </div>
          
          <div className="login-form">
            <GoogleSignInButton size="large" className="professional-signin" />
          </div>
          
          <div className="login-footer">
            <p className="terms-text">
              By continuing, you agree to our{' '}
              <a href="#" className="terms-link">Terms of Service</a>{' '}
              and{' '}
              <a href="#" className="terms-link">Privacy Policy</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
