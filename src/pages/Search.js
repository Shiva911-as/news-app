import React, { useState } from 'react';
import { useUser } from '../context/UserContext';
import { apiService } from '../services/apiService';
import ArticleCard from '../components/ArticleCard';
import toast from 'react-hot-toast';
import { FaSearch, FaTimes } from 'react-icons/fa';
import './Search.css';

const Search = () => {
  const { learnFromArticle } = useUser();
  const [query, setQuery] = useState('');
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [searched, setSearched] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    
    if (!query.trim()) {
      toast.error('Please enter a search term');
      return;
    }

    setLoading(true);
    setSearched(true);
    
    try {
      const response = await apiService.searchNews(query.trim());
      
      if (response.success) {
        setArticles(response.articles);
        if (response.articles.length === 0) {
          toast.info('No articles found for your search');
        }
      } else {
        toast.error('Failed to search for articles');
      }
    } catch (err) {
      toast.error('An error occurred while searching');
      console.error('Search error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleArticleRead = async (article) => {
    try {
      const result = await learnFromArticle(article);
      if (result.success) {
        toast.success('Learning from your reading preferences!');
      }
    } catch (err) {
      console.error('Error learning from article:', err);
    }
  };

  const clearSearch = () => {
    setQuery('');
    setArticles([]);
    setSearched(false);
  };

  return (
    <div className="container">
      <div className="search-container">
        <div className="search-header">
          <h1>Search News</h1>
          <p>Find articles on any topic that interests you</p>
        </div>

        <form onSubmit={handleSearch} className="search-form">
          <div className="search-input-group">
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search for news articles..."
              className="search-input"
              disabled={loading}
            />
            <button
              type="submit"
              className="search-btn"
              disabled={loading || !query.trim()}
            >
              {loading ? (
                <FaSearch className="spinning" />
              ) : (
                <FaSearch />
              )}
            </button>
            {searched && (
              <button
                type="button"
                className="clear-btn"
                onClick={clearSearch}
                disabled={loading}
              >
                <FaTimes />
              </button>
            )}
          </div>
        </form>

        {loading && (
          <div className="loading">
            <FaSearch className="loading-icon spinning" />
            <p>Searching for articles...</p>
          </div>
        )}

        {searched && !loading && (
          <div className="search-results">
            <div className="results-header">
              <h2>Search Results</h2>
              {articles.length > 0 && (
                <p>{articles.length} article{articles.length !== 1 ? 's' : ''} found for "{query}"</p>
              )}
            </div>

            {articles.length > 0 ? (
              <div className="articles-grid">
                {articles.map((article, index) => (
                  <ArticleCard
                    key={`${article.url}-${index}`}
                    article={article}
                    onRead={handleArticleRead}
                    showScore={false}
                  />
                ))}
              </div>
            ) : (
              <div className="no-results">
                <FaSearch />
                <h3>No articles found</h3>
                <p>Try searching with different keywords or check your spelling</p>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default Search;
