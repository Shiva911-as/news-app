import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth tokens here if needed
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error) => {
    console.error('API Error:', error);
    if (error.response) {
      throw new Error(error.response.data.error || 'API request failed');
    } else if (error.request) {
      throw new Error('Network error - please check your connection');
    } else {
      throw new Error('An unexpected error occurred');
    }
  }
);

export const apiService = {
  // News endpoints
  getTrendingNews: async (pageSize = 20, page = 1) => {
    return api.get(`/api/news/trending?page_size=${pageSize}&page=${page}`);
  },

  searchNews: async (query, pageSize = 20) => {
    return api.get(`/api/news/search?q=${encodeURIComponent(query)}&page_size=${pageSize}`);
  },

  getTopicNews: async (topic, pageSize = 20) => {
    return api.get(`/api/news/topic/${encodeURIComponent(topic)}?page_size=${pageSize}`);
  },

  // User profile endpoints
  getProfile: async () => {
    return api.get('/api/profile');
  },

  updateProfile: async (data) => {
    return api.post('/api/profile', data);
  },

  learnFromArticle: async (article) => {
    return api.post('/api/profile/learn', { article });
  },

  // Recommendations endpoint
  getRecommendations: async () => {
    return api.get('/api/recommendations');
  },

  // Indian news endpoint
  getIndianNews: async (pageSize = 20) => {
    return api.get(`/api/news/indian?page_size=${pageSize}`);
  },

  // Sports news endpoints
  getSportsNews: async (pageSize = 20) => {
    return api.get(`/api/news/sports?page_size=${pageSize}`);
  },

  getCricketNews: async (pageSize = 20) => {
    return api.get(`/api/news/cricket?page_size=${pageSize}`);
  },

  // Technology news endpoint
  getTechnologyNews: async (pageSize = 20) => {
    return api.get(`/api/news/technology?page_size=${pageSize}`);
  },
};
