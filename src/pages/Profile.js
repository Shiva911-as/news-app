import React, { useState } from 'react';
import { useUser } from '../context/UserContext';
import { Link } from 'react-router-dom';
import { FaUser, FaHeart, FaClock, FaTags, FaEdit, FaHistory } from 'react-icons/fa';
import './Profile.css';

const Profile = () => {
  const { user, loading } = useUser();
  const [activeTab, setActiveTab] = useState('overview');

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <FaUser className="loading-icon" />
          <p>Loading your profile...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return (
      <div className="container">
        <div className="no-profile">
          <FaUser />
          <h2>No Profile Found</h2>
          <p>Set up your profile to get started with personalized news</p>
          <Link to="/setup" className="btn btn-primary">
            Set Up Profile
          </Link>
        </div>
      </div>
    );
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  return (
    <div className="container">
      <div className="profile-container">
        <div className="profile-header">
          <div className="profile-avatar">
            <FaUser />
          </div>
          <div className="profile-info">
            <h1>Your Profile</h1>
            <p>User ID: {user.user_id}</p>
            <p>Last updated: {formatDate(user.last_updated)}</p>
          </div>
        </div>

        <div className="profile-tabs">
          <button
            className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <FaUser />
            Overview
          </button>
          <button
            className={`tab-btn ${activeTab === 'interests' ? 'active' : ''}`}
            onClick={() => setActiveTab('interests')}
          >
            <FaTags />
            Interests
          </button>
          <button
            className={`tab-btn ${activeTab === 'history' ? 'active' : ''}`}
            onClick={() => setActiveTab('history')}
          >
            <FaHistory />
            Reading History
          </button>
        </div>

        <div className="profile-content">
          {activeTab === 'overview' && (
            <div className="overview-tab">
              <div className="stats-grid">
                <div className="stat-card">
                  <FaTags className="stat-icon" />
                  <div className="stat-content">
                    <h3>{user.total_interests}</h3>
                    <p>Total Interests</p>
                  </div>
                </div>
                <div className="stat-card">
                  <FaHeart className="stat-icon" />
                  <div className="stat-content">
                    <h3>{user.articles_read}</h3>
                    <p>Articles Read</p>
                  </div>
                </div>
                <div className="stat-card">
                  <FaClock className="stat-icon" />
                  <div className="stat-content">
                    <h3>{formatDate(user.last_updated)}</h3>
                    <p>Last Updated</p>
                  </div>
                </div>
              </div>

              <div className="quick-actions">
                <h3>Quick Actions</h3>
                <div className="action-buttons">
                  <Link to="/setup" className="btn btn-primary">
                    <FaEdit />
                    Update Interests
                  </Link>
                  <Link to="/" className="btn btn-secondary">
                    <FaHeart />
                    View Recommendations
                  </Link>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'interests' && (
            <div className="interests-tab">
              <div className="interests-header">
                <h3>Your Interests</h3>
                <p>These topics influence your personalized news recommendations</p>
              </div>

              {user.top_interests && user.top_interests.length > 0 ? (
                <div className="interests-list">
                  {user.top_interests.map(([interest, weight], index) => (
                    <div key={interest} className="interest-item">
                      <div className="interest-info">
                        <span className="interest-name">{interest}</span>
                        <span className="interest-weight">Weight: {weight.toFixed(2)}</span>
                      </div>
                      <div className="interest-bar">
                        <div 
                          className="interest-progress" 
                          style={{ width: `${Math.min(weight * 20, 100)}%` }}
                        ></div>
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-interests">
                  <FaTags />
                  <h4>No interests set</h4>
                  <p>Set up your interests to get personalized recommendations</p>
                  <Link to="/setup" className="btn btn-primary">
                    Set Up Interests
                  </Link>
                </div>
              )}
            </div>
          )}

          {activeTab === 'history' && (
            <div className="history-tab">
              <div className="history-header">
                <h3>Reading History</h3>
                <p>Articles you've read recently</p>
              </div>

              {user.read_history && user.read_history.length > 0 ? (
                <div className="history-list">
                  {user.read_history.slice(0, 10).map((article, index) => (
                    <div key={index} className="history-item">
                      <div className="history-content">
                        <h4>{article.title}</h4>
                        <p className="history-meta">
                          Read on: {formatDate(article.read_at)}
                          {article.published_at && (
                            <span> • Published: {formatDate(article.published_at)}</span>
                          )}
                        </p>
                      </div>
                      {article.url && (
                        <a 
                          href={article.url} 
                          target="_blank" 
                          rel="noopener noreferrer"
                          className="btn btn-secondary"
                        >
                          Read Again
                        </a>
                      )}
                    </div>
                  ))}
                </div>
              ) : (
                <div className="no-history">
                  <FaHistory />
                  <h4>No reading history</h4>
                  <p>Start reading articles to build your history</p>
                  <Link to="/" className="btn btn-primary">
                    Browse News
                  </Link>
                </div>
              )}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Profile;
