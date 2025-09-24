import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import toast from 'react-hot-toast';
import { FaCog, FaCheck } from 'react-icons/fa';
import './Setup.css';

const Setup = () => {
  const navigate = useNavigate();
  const { updateInterests } = useUser();
  const [interests, setInterests] = useState('');
  const [loading, setLoading] = useState(false);

  const suggestedTopics = [
    'technology', 'ai', 'machine learning', 'cricket', 'sports',
    'finance', 'politics', 'health', 'science', 'entertainment',
    'business', 'startups', 'cryptocurrency', 'climate change'
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!interests.trim()) {
      toast.error('Please enter at least one interest');
      return;
    }

    setLoading(true);
    
    try {
      const interestsList = interests
        .split(',')
        .map(interest => interest.trim())
        .filter(interest => interest.length > 0);

      const result = await updateInterests(interestsList);
      
      if (result.success) {
        toast.success('Profile updated successfully!');
        navigate('/');
      } else {
        toast.error(result.error || 'Failed to update profile');
      }
    } catch (err) {
      toast.error('An error occurred while updating your profile');
      console.error('Error updating interests:', err);
    } finally {
      setLoading(false);
    }
  };

  const addSuggestedTopic = (topic) => {
    const currentInterests = interests.split(',').map(i => i.trim()).filter(i => i);
    if (!currentInterests.includes(topic)) {
      const newInterests = [...currentInterests, topic].join(', ');
      setInterests(newInterests);
    }
  };

  return (
    <div className="container">
      <div className="setup-container">
        <div className="setup-header">
          <FaCog className="setup-icon" />
          <h1>Set Up Your Interests</h1>
          <p>Tell us what topics interest you to get personalized news recommendations</p>
        </div>

        <form onSubmit={handleSubmit} className="setup-form">
          <div className="form-group">
            <label htmlFor="interests">Your Interests</label>
            <textarea
              id="interests"
              value={interests}
              onChange={(e) => setInterests(e.target.value)}
              placeholder="Enter your interests separated by commas (e.g., technology, sports, politics)"
              rows="4"
              className="form-control"
              disabled={loading}
            />
            <small>Separate multiple interests with commas</small>
          </div>

          <div className="suggested-topics">
            <h3>Suggested Topics</h3>
            <p>Click on topics to add them to your interests:</p>
            <div className="topic-tags">
              {suggestedTopics.map((topic) => (
                <button
                  key={topic}
                  type="button"
                  className="topic-tag"
                  onClick={() => addSuggestedTopic(topic)}
                  disabled={loading}
                >
                  {topic}
                </button>
              ))}
            </div>
          </div>

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={() => navigate('/')}
              disabled={loading}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
            >
              {loading ? (
                <>
                  <FaCog className="spinning" />
                  Saving...
                </>
              ) : (
                <>
                  <FaCheck />
                  Save Interests
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default Setup;
