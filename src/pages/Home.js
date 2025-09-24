import React, { useState, useEffect, useCallback } from 'react';
import { useUser } from '../context/UserContext';
import { apiService } from '../services/apiService';
import ArticleCard from '../components/ArticleCard';
import UserProfileCard from '../components/UserProfileCard';
import toast from 'react-hot-toast';
import { FaNewspaper, FaUserCog, FaFire, FaSpinner } from 'react-icons/fa';
import './Home.css';

const Home = () => {
  const { user, learnFromArticle } = useUser();
  const [recommendations, setRecommendations] = useState([]);
  const [trendingNews, setTrendingNews] = useState([]);
  const [loading, setLoading] = useState(true);
  const [trendingLoading, setTrendingLoading] = useState(false);
  const [error, setError] = useState(null);
  const [trendingPage, setTrendingPage] = useState(1);
  const [hasMoreTrending, setHasMoreTrending] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);

      // Load both recommendations and trending news
      const [recResponse, trendingResponse] = await Promise.all([
        apiService.getRecommendations(),
        apiService.getTrendingNews(10)
      ]);

      if (recResponse.success) {
        setRecommendations(recResponse.recommendations);
      }

      if (trendingResponse.success) {
        setTrendingNews(trendingResponse.articles);
        setTrendingPage(1);
        setHasMoreTrending(trendingResponse.has_more || false);
      }
    } catch (err) {
      setError('Failed to load news');
      console.error('Error loading data:', err);
      toast.error('Failed to load news');
    } finally {
      setLoading(false);
    }
  };

  const loadMoreTrending = useCallback(async () => {
    if (trendingLoading || !hasMoreTrending) return;

    try {
      setTrendingLoading(true);
      const nextPage = trendingPage + 1;
      const response = await apiService.getTrendingNews(10, nextPage);
      
      if (response.success) {
        setTrendingNews(prev => [...prev, ...response.articles]);
        setTrendingPage(nextPage);
        setHasMoreTrending(response.has_more || false);
      }
    } catch (err) {
      console.error('Error loading more trending news:', err);
      toast.error('Failed to load more trending news');
    } finally {
      setTrendingLoading(false);
    }
  }, [trendingLoading, hasMoreTrending, trendingPage]);

  const handleArticleRead = async (article) => {
    try {
      const result = await learnFromArticle(article);
      if (result.success) {
        toast.success('Learning from your reading preferences!');
        // Reload recommendations after learning
        setTimeout(loadData, 1000);
      }
    } catch (err) {
      console.error('Error learning from article:', err);
    }
  };

  if (loading) {
    return (
      <div className="container">
        <div className="loading">
          <FaNewspaper className="loading-icon" />
          <p>Loading your personalized news...</p>
        </div>
        <div className="loading-skeleton">
          {[...Array(6)].map((_, index) => (
            <div key={index} className="skeleton-card">
              <div className="skeleton skeleton-image"></div>
              <div className="skeleton skeleton-title"></div>
              <div className="skeleton skeleton-description"></div>
              <div className="skeleton skeleton-description"></div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="container">
        <div className="error">
          <p>{error}</p>
          <button className="btn btn-primary" onClick={loadData}>
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="home-grid">
        <div className="main-content">
          {/* User Profile Card */}
          <UserProfileCard user={user} />

          {/* Personalized Recommendations */}
          <section className="news-section">
            <div className="section-header">
              <h2>
                <FaNewspaper />
                Your Personalized News
              </h2>
              <p>Articles tailored to your interests</p>
            </div>

            {recommendations.length > 0 ? (
              <div className="articles-grid articles-grid--featured">
                {recommendations.map((rec, index) => (
                  <ArticleCard
                    key={`${rec.article.url}-${index}`}
                    article={rec.article}
                    score={rec.score}
                    onRead={handleArticleRead}
                    variant={index === 0 ? 'featured' : 'default'}
                  />
                ))}
              </div>
            ) : (
              <div className="no-recommendations">
                <FaUserCog />
                <h3>No personalized recommendations yet</h3>
                <p>Set up your interests to get personalized news recommendations</p>
                <a href="/setup" className="btn btn-primary">
                  Set Up Interests
                </a>
              </div>
            )}
          </section>

          {/* Trending News */}
          <section className="news-section trending-section">
            <div className="section-header">
              <h2>
                <FaFire />
                Trending News
              </h2>
              <p>What's happening around the world right now</p>
            </div>

            {trendingNews.length > 0 ? (
              <>
                <div className="articles-grid articles-grid--trending">
                  {trendingNews.map((article, index) => (
                    <div key={`${article.url}-${index}`} className="trending-article-wrapper">
                      <ArticleCard
                        article={article}
                        onRead={handleArticleRead}
                        showScore={false}
                        variant="default"
                        isTrending={true}
                        trendingRank={index + 1}
                      />
                    </div>
                  ))}
                </div>
                
                {hasMoreTrending && (
                  <div className="load-more-container">
                    <button 
                      className="btn btn-secondary load-more-btn"
                      onClick={loadMoreTrending}
                      disabled={trendingLoading}
                    >
                      {trendingLoading ? (
                        <>
                          <FaSpinner className="spinner" />
                          Loading more...
                        </>
                      ) : (
                        'Load More Trending News'
                      )}
                    </button>
                  </div>
                )}
              </>
            ) : (
              <p>No trending news available</p>
            )}
          </section>
        </div>
      </div>
    </div>
  );
};

export default Home;
