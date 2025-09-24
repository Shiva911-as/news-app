import React, { useState } from 'react';
import { FaExternalLinkAlt, FaClock, FaStar, FaBookmark, FaRegBookmark, FaShare, FaHeart, FaRegHeart } from 'react-icons/fa';
import ArticleSchema from './ArticleSchema';
import OptimizedImage from './OptimizedImage';
import './ArticleCard.css';

const ArticleCard = ({ article, score, onRead, showScore = true, variant = 'default', isTrending = false, trendingRank = null }) => {
  const [isBookmarked, setIsBookmarked] = useState(false);
  const [isLiked, setIsLiked] = useState(false);

  const handleRead = () => {
    if (onRead) {
      onRead(article);
    }
    if (article.url) {
      window.open(article.url, '_blank', 'noopener,noreferrer');
    }
  };

  const handleBookmark = (e) => {
    e.stopPropagation();
    setIsBookmarked(!isBookmarked);
  };

  const handleLike = (e) => {
    e.stopPropagation();
    setIsLiked(!isLiked);
  };

  const handleShare = (e) => {
    e.stopPropagation();
    if (navigator.share) {
      navigator.share({
        title: article.title,
        text: article.description,
        url: article.url
      });
    } else {
      // Fallback to copying URL to clipboard
      navigator.clipboard.writeText(article.url);
      // You could add a toast notification here
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Unknown';
    const date = new Date(dateString);
    const now = new Date();
    const diffInHours = Math.floor((now - date) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return 'Just now';
    if (diffInHours < 24) return `${diffInHours}h ago`;
    if (diffInHours < 48) return 'Yesterday';
    return date.toLocaleDateString();
  };

  const truncateText = (text, maxLength = 150) => {
    if (!text) return '';
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
  };

  const getImageUrl = () => {
    if (article.urlToImage) return article.urlToImage;
    // Fallback to a placeholder service
    return `https://picsum.photos/120/80?random=${Math.random()}`;
  };

  const getAISummary = () => {
    // Placeholder AI summary - in a real app, this would come from your AI service
    const summaries = [
      "AI Analysis: This article discusses key developments in technology that could impact the industry significantly.",
      "AI Summary: Recent findings suggest important changes in market trends and consumer behavior patterns.",
      "AI Insight: This piece highlights critical information about current events and their potential implications.",
      "AI Overview: The article presents data-driven insights into emerging trends and future predictions.",
      "AI Brief: Key takeaways include important updates on policy changes and their expected outcomes."
    ];
    return summaries[Math.floor(Math.random() * summaries.length)];
  };

  return (
    <>
      <ArticleSchema article={article} isMainArticle={variant === 'featured'} />
      <article className={`article-card article-card--${variant} fade-in bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-600 rounded-xl shadow-md dark:shadow-gray-900/30 hover:shadow-lg dark:hover:shadow-gray-900/50 transition-all duration-300 hover:-translate-y-1 mb-8`}>
      {/* Thumbnail Image */}
      <div className="article-thumbnail flex-shrink-0 w-32 h-20 md:w-40 md:h-24">
        <div className="thumbnail-wrapper relative w-full h-full rounded-lg overflow-hidden bg-gray-100 dark:bg-gray-700">
          <OptimizedImage
            src={getImageUrl()}
            alt={article.title}
            width={variant === 'featured' ? 160 : variant === 'compact' ? 100 : 120}
            height={variant === 'featured' ? 100 : variant === 'compact' ? 70 : 80}
            className="w-full h-full hover:scale-105 transition-transform duration-300"
            priority={variant === 'featured'}
            quality={85}
          />
          {isTrending && trendingRank && (
            <div className="trending-badge absolute top-2 right-2 bg-gradient-to-r from-orange-500 to-red-500 text-white px-2 py-1 rounded-md text-xs font-bold flex items-center gap-1 shadow-lg animate-pulse">
              <span className="trending-icon">🔥</span>
              <span className="trending-rank">#{trendingRank}</span>
            </div>
          )}
          {showScore && score && !isTrending && (
            <div className="score-badge absolute top-2 right-2 bg-gradient-to-r from-blue-500 to-purple-500 text-white px-2 py-1 rounded-md text-xs font-semibold flex items-center gap-1 shadow-lg">
              <FaStar className="w-3 h-3" />
              {score.toFixed(1)}
            </div>
          )}
        </div>
      </div>

      {/* Article Content */}
      <div className="article-content flex-1 flex flex-col gap-2 min-w-0">
        <div className="article-meta-top flex justify-between items-center gap-2 mb-3">
          {article.source?.name && (
            <span className="article-source font-bold text-blue-600 dark:text-blue-400 text-sm uppercase tracking-wide">
              {article.source.name}
            </span>
          )}
          {article.publishedAt && (
            <span className="article-date text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1 font-medium">
              <FaClock className="w-3 h-3" />
              {formatDate(article.publishedAt)}
            </span>
          )}
        </div>

        <h3 className="article-title text-xl md:text-2xl font-bold text-gray-900 dark:text-white leading-tight line-clamp-2 mb-4">
          {article.title}
        </h3>
        
        {/* AI Summary */}
        <div className="ai-summary bg-gray-50 dark:bg-gray-700 rounded-lg p-4 border-l-4 border-blue-500 my-3">
          <div className="ai-summary-header mb-2">
            <span className="ai-label text-sm font-bold text-blue-600 dark:text-blue-400 uppercase tracking-wide">
              🤖 AI Summary
            </span>
          </div>
          <p className="ai-summary-text text-base text-gray-700 dark:text-gray-300 leading-relaxed line-clamp-2">
            {getAISummary()}
          </p>
        </div>
        
        {article.description && (
          <p className="article-description text-base text-gray-600 dark:text-gray-400 leading-relaxed line-clamp-2 flex-1 mb-4">
            {truncateText(article.description, variant === 'compact' ? 80 : 120)}
          </p>
        )}
        
        <div className="article-actions flex gap-3 mt-auto pt-4">
          <button 
            className={`w-10 h-10 border-none rounded-lg flex items-center justify-center cursor-pointer transition-all duration-300 text-sm relative overflow-hidden ${
              isBookmarked 
                ? 'bg-blue-500 text-white shadow-lg' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 hover:bg-blue-500 hover:text-white hover:scale-110'
            }`}
            onClick={handleBookmark}
            aria-label={isBookmarked ? 'Remove from saved' : 'Save article'}
          >
            {isBookmarked ? <FaBookmark className="w-4 h-4" /> : <FaRegBookmark className="w-4 h-4" />}
          </button>
          
          <button 
            className={`w-10 h-10 border-none rounded-lg flex items-center justify-center cursor-pointer transition-all duration-300 text-sm relative overflow-hidden ${
              isLiked 
                ? 'bg-blue-500 text-white shadow-lg' 
                : 'bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 hover:bg-blue-500 hover:text-white hover:scale-110'
            }`}
            onClick={handleLike}
            aria-label={isLiked ? 'Unlike article' : 'Like article'}
          >
            {isLiked ? <FaHeart className="w-4 h-4" /> : <FaRegHeart className="w-4 h-4" />}
          </button>
          
          <button 
            className="w-10 h-10 border-none rounded-lg flex items-center justify-center cursor-pointer transition-all duration-300 text-sm relative overflow-hidden bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-400 border border-gray-200 dark:border-gray-600 hover:bg-blue-500 hover:text-white hover:scale-110"
            onClick={handleShare}
            aria-label="Share article"
          >
            <FaShare className="w-4 h-4" />
          </button>
          
          <button 
            className="w-10 h-10 border-none rounded-lg flex items-center justify-center cursor-pointer transition-all duration-300 text-sm relative overflow-hidden bg-blue-500 text-white shadow-lg ml-auto hover:scale-110 hover:shadow-xl hover:bg-blue-600"
            onClick={handleRead}
            aria-label="Read full article"
          >
            <FaExternalLinkAlt className="w-4 h-4" />
          </button>
        </div>
      </div>
      </article>
    </>
  );
};

export default ArticleCard;
