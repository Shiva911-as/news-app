import React, { useState, useEffect, useCallback } from 'react';
import { useUser } from '../context/UserContext';
import { apiService } from '../services/apiService';
import ArticleBox from '../components/ArticleBox';
import toast from 'react-hot-toast';
import { FaSpinner, FaExclamationTriangle } from 'react-icons/fa';
import './Home.css';

const Home = ({ selectedCategory, onArticleSelect, selectedArticle }) => {
  const { learnFromArticle } = useUser();
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(true);

  // Load articles when category changes
  useEffect(() => {
    if (selectedCategory) {
      loadCategoryArticles();
    }
  }, [selectedCategory]); // eslint-disable-line react-hooks/exhaustive-deps

  const loadCategoryArticles = async () => {
    if (!selectedCategory) return;

    try {
      setLoading(true);
      setError(null);
      setPage(1);

      const response = await fetchCategoryData(selectedCategory);
      
      if (response.success) {
        setArticles(response.articles || []);
        setHasMore(response.has_more || false);
      } else {
        setError(response.error || 'Failed to load articles');
      }
    } catch (err) {
      setError('Failed to load articles');
      console.error('Error loading category articles:', err);
      toast.error('Failed to load articles');
    } finally {
      setLoading(false);
    }
  };

  const fetchCategoryData = async (category) => {
    const endpoint = category.endpoint;
    
    // Use the new category endpoint for all categories
    if (endpoint.includes('/api/news/category/')) {
      try {
        const response = await fetch(endpoint + '?page_size=8');
        const data = await response.json();
        
        if (data.status === 'success') {
          return {
            success: true,
            articles: data.articles || [],
            has_more: false
          };
        } else {
          return {
            success: false,
            error: data.message || 'Failed to fetch category news'
          };
        }
      } catch (error) {
        return {
          success: false,
          error: 'Network error: ' + error.message
        };
      }
    }
    
    // Fallback for any legacy endpoints
    return await apiService.getTrendingNews(8);
  };

  const loadMoreArticles = useCallback(async () => {
    if (loading || !hasMore || !selectedCategory) return;

    try {
      setLoading(true);
      const nextPage = page + 1;
      const response = await fetchCategoryData(selectedCategory);
      
      if (response.success) {
        setArticles(prev => [...prev, ...response.articles]);
        setPage(nextPage);
        setHasMore(response.has_more || false);
      }
    } catch (err) {
      console.error('Error loading more articles:', err);
      toast.error('Failed to load more articles');
    } finally {
      setLoading(false);
    }
  }, [loading, hasMore, selectedCategory, page]);

  const handleArticleClick = async (article) => {
    // Learn from article interaction
    try {
      await learnFromArticle(article);
    } catch (err) {
      console.error('Error learning from article:', err);
    }
    
    // Select article for summary panel
    onArticleSelect(article);
  };

  if (!selectedCategory) {
    return (
      <div className="home-container">
        <div className="welcome-message">
          <h2>Welcome to News</h2>
          <p>Select a category from the sidebar to start reading news</p>
        </div>
      </div>
    );
  }

  if (loading && articles.length === 0) {
    return (
      <div className="home-container">
        <div className="category-header">
          <h1>
            <span className="category-icon">{selectedCategory.icon}</span>
            {selectedCategory.name}
          </h1>
        </div>
        <div className="loading-state">
          <FaSpinner className="loading-spinner" />
          <p>Loading {selectedCategory.name.toLowerCase()} news...</p>
        </div>
        <div className="articles-grid-skeleton">
          {[...Array(8)].map((_, index) => (
            <div key={index} className="article-skeleton">
              <div className="skeleton-title"></div>
              <div className="skeleton-description"></div>
              <div className="skeleton-meta"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="home-container">
        <div className="category-header">
          <h1>
            <span className="category-icon">{selectedCategory.icon}</span>
            {selectedCategory.name}
          </h1>
        </div>
        <div className="error-state">
          <FaExclamationTriangle className="error-icon" />
          <h3>Failed to load articles</h3>
          <p>{error}</p>
          <button className="retry-button" onClick={loadCategoryArticles}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="home-container">
      <div className="category-header">
        <h1>
          {selectedCategory.icon && (
            <selectedCategory.icon className="category-header-icon" size={28} strokeWidth={1.5} />
          )}
          {selectedCategory.name}
        </h1>
        <p className="category-description">
          {selectedCategory.id === 'home' ? 
            `${articles.length} personalized recommendations` : 
            `${articles.length} articles available`
          }
        </p>
      </div>

      {articles.length > 0 ? (
        <>
          <div className="articles-grid">
            {articles.slice(0, 8).map((article, index) => (
              <ArticleBox
                key={`${article.url}-${index}`}
                article={article}
                onClick={() => handleArticleClick(article)}
                isSelected={selectedArticle?.url === article.url}
              />
            ))}
          </div>
          
          {hasMore && (
            <div className="load-more-section">
              <button 
                className="load-more-button"
                onClick={loadMoreArticles}
                disabled={loading}
              >
                {loading ? (
                  <>
                    <FaSpinner className="spinner" />
                    Loading more...
                  </>
                ) : (
                  'Load More Articles'
                )}
              </button>
            </div>
          )}
        </>
      ) : (
        <div className="no-articles">
          <h3>No articles found</h3>
          <p>Try selecting a different category or check back later</p>
        </div>
      )}
    </div>
  );
};

export default Home;
