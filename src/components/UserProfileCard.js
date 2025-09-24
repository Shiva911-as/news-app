import React, { useEffect, useRef, useState } from 'react';
import { FaUser, FaHeart, FaClock, FaTags, FaRocket, FaChartBar } from 'react-icons/fa';
import './UserProfileCard.css';

// Lightweight animated counter without external deps
const CountUp = ({ value = 0, duration = 1000, format = (n) => n.toString() }) => {
  const [display, setDisplay] = useState(0);
  const startRef = useRef(null);
  const fromRef = useRef(0);
  const valueRef = useRef(value);

  useEffect(() => {
    valueRef.current = value;
    fromRef.current = display;
    startRef.current = null;

    const step = (timestamp) => {
      if (!startRef.current) startRef.current = timestamp;
      const progress = Math.min((timestamp - startRef.current) / duration, 1);
      const current = fromRef.current + (valueRef.current - fromRef.current) * progress;
      setDisplay(current);
      if (progress < 1) requestAnimationFrame(step);
    };

    const raf = requestAnimationFrame(step);
    return () => cancelAnimationFrame(raf);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [value, duration]);

  return <span>{format(Math.round(display))}</span>;
};

const UserProfileCard = ({ user }) => {
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const getGreetingEmoji = () => {
    const hour = new Date().getHours();
    if (hour < 12) return '☀️';
    if (hour < 17) return '🌤️';
    return '🌙';
  };

  const getUserName = () => {
    // For now, we'll use a default name. In a real app, this would come from user data
    return 'Alex';
  };

  const getCurrentDate = () => {
    const now = new Date();
    return now.toLocaleDateString('en-US', { 
      weekday: 'long', 
      year: 'numeric', 
      month: 'long', 
      day: 'numeric' 
    });
  };

  if (!user) {
    return (
      <div className="profile-card">
        <div className="profile-header">
          <div className="profile-avatar">
            <FaUser />
          </div>
        <div className="profile-info">
          <h2 className="profile-greeting">
            {getGreeting()}, {getUserName()} {getGreetingEmoji()}
          </h2>
          <p className="profile-date">{getCurrentDate()}</p>
          <p className="profile-subtitle">Set up your interests to get personalized news recommendations</p>
        </div>
        </div>
        <div className="profile-actions">
          <a href="/setup" className="btn btn-primary discover-btn">
            <FaRocket />
            Discover New Topics
          </a>
        </div>
      </div>
    );
  }

  const formatDate = (dateString) => {
    if (!dateString) return 'Never';
    const date = new Date(dateString);
    return date.toLocaleDateString();
  };

  const getTopInterests = () => {
    if (!user.top_interests || user.top_interests.length === 0) return [];
    return user.top_interests.slice(0, 3);
  };

  const topInterests = getTopInterests();

  return (
    <div className="profile-card">
      <div className="profile-header">
        <div className="profile-avatar">
          <FaUser />
        </div>
        <div className="profile-info">
          <h2 className="profile-greeting">
            {getGreeting()}, {getUserName()} {getGreetingEmoji()}
          </h2>
          <p className="profile-date">{getCurrentDate()}</p>
          <p className="profile-subtitle">Here's your personalized news digest</p>
        </div>
      </div>

      {topInterests.length > 0 && (
        <div className="interests-section">
          <div className="interests-header">
            <FaChartBar className="interests-icon" />
            <h3>Your Top Interests</h3>
          </div>
          <div className="interests-chart">
            {topInterests.map(([interest, weight], index) => (
              <div key={interest} className="interest-item">
                <div className="interest-info">
                  <span className="interest-name">{interest}</span>
                  <span className="interest-weight">{Math.round(weight * 100)}%</span>
                </div>
                <div className="interest-bar">
                  <div 
                    className="interest-bar-fill" 
                    style={{ width: `${Math.min(weight * 100, 100)}%` }}
                  ></div>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="profile-stats">
        <div className="stat-item">
          <div className="stat-icon">
            <FaTags />
          </div>
          <div className="stat-content">
            <span className="stat-value">
              <CountUp value={user.total_interests || 0} />
            </span>
            <span className="stat-label">Interests</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <FaHeart />
          </div>
          <div className="stat-content">
            <span className="stat-value">
              <CountUp value={user.articles_read || 0} />
            </span>
            <span className="stat-label">Articles Read</span>
          </div>
        </div>
        <div className="stat-item">
          <div className="stat-icon">
            <FaClock />
          </div>
          <div className="stat-content">
            <span className="stat-value">{formatDate(user.last_updated)}</span>
            <span className="stat-label">Last Updated</span>
          </div>
        </div>
      </div>

      <div className="profile-actions">
        <a href="/profile" className="btn btn-secondary">
          View Full Profile
        </a>
        <a href="/setup" className="btn btn-primary discover-btn">
          <FaRocket />
          Discover New Topics
        </a>
      </div>
    </div>
  );
};

export default UserProfileCard;
