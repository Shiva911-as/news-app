import React, { createContext, useContext, useState, useEffect } from 'react';
import { apiService } from '../services/apiService';

const UserContext = createContext();

export const useUser = () => {
  const context = useContext(UserContext);
  if (!context) {
    throw new Error('useUser must be used within a UserProvider');
  }
  return context;
};

export const UserProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    loadUserProfile();
  }, []);

  const loadUserProfile = async () => {
    try {
      setLoading(true);
      const response = await apiService.getProfile();
      if (response.success) {
        setUser(response.profile);
      }
    } catch (err) {
      setError('Failed to load user profile');
      console.error('Error loading user profile:', err);
    } finally {
      setLoading(false);
    }
  };

  const updateInterests = async (interests) => {
    try {
      const response = await apiService.updateProfile({ interests });
      if (response.success) {
        setUser(response.profile);
        return { success: true };
      }
    } catch (err) {
      setError('Failed to update interests');
      console.error('Error updating interests:', err);
      return { success: false, error: err.message };
    }
  };

  const learnFromArticle = async (article) => {
    try {
      const response = await apiService.learnFromArticle(article);
      if (response.success) {
        // Reload user profile to get updated interests
        await loadUserProfile();
        return { success: true };
      }
    } catch (err) {
      console.error('Error learning from article:', err);
      return { success: false, error: err.message };
    }
  };

  const value = {
    user,
    loading,
    error,
    updateInterests,
    learnFromArticle,
    loadUserProfile,
  };

  return (
    <UserContext.Provider value={value}>
      {children}
    </UserContext.Provider>
  );
};
