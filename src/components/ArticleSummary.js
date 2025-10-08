import React, { useState, useEffect, useCallback } from 'react';
import './ArticleSummary.css';

const ArticleSummary = ({ selectedArticle, onClose }) => {
  const [summary, setSummary] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);

  const generateSummary = useCallback(async (article) => {
    setIsGenerating(true);
    
    // Simulate AI summary generation (you can integrate with actual AI service)
    setTimeout(() => {
      const summaryText = generateAISummary(article);
      setSummary(summaryText);
      setIsGenerating(false);
    }, 1500);
  }, []);

  useEffect(() => {
    if (selectedArticle) {
      generateSummary(selectedArticle);
    }
  }, [selectedArticle, generateSummary]);

  const generateAISummary = (article) => {
    // Simple AI-like summary generation based on article content
    const title = article.title || '';
    const description = article.description || '';
    
    // Extract key points
    const keyPoints = [];
    
    if (title.toLowerCase().includes('india')) {
      keyPoints.push('🇮🇳 Indian context and relevance');
    }
    
    if (title.toLowerCase().includes('technology') || title.toLowerCase().includes('tech')) {
      keyPoints.push('💻 Technology sector impact');
    }
    
    if (title.toLowerCase().includes('business') || title.toLowerCase().includes('economy')) {
      keyPoints.push('💼 Business and economic implications');
    }
    
    if (title.toLowerCase().includes('cricket') || title.toLowerCase().includes('sports')) {
      keyPoints.push('🏏 Sports and entertainment news');
    }

    // Generate summary based on content length and key points
    let summaryText = `This article discusses ${title.toLowerCase()}. `;
    
    if (description && description.length > 50) {
      const sentences = description.split('.').filter(s => s.trim().length > 10);
      if (sentences.length > 0) {
        summaryText += sentences[0].trim() + '. ';
      }
    }
    
    if (keyPoints.length > 0) {
      summaryText += '\n\nKey highlights:\n' + keyPoints.join('\n');
    }
    
    return summaryText;
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'Recently';
    
    const date = new Date(dateString);
    const now = new Date();
    const diffTime = Math.abs(now - date);
    const diffHours = Math.ceil(diffTime / (1000 * 60 * 60));
    
    if (diffHours < 1) return 'Just now';
    if (diffHours < 24) return `${diffHours}h ago`;
    return date.toLocaleDateString();
  };

  if (!selectedArticle) {
    console.log('No article selected for summary');
    return (
      <div className="article-summary-panel">
        <div className="summary-placeholder">
          <div className="placeholder-icon">📰</div>
          <h3>Select an article</h3>
          <p>Click on any article to see AI-generated summary and insights</p>
        </div>
      </div>
    );
  }

  console.log('Rendering summary for article:', selectedArticle.title);

  return (
    <div className="article-summary-panel open">
      <div className="summary-header">
        <div className="summary-title-section">
          <span className="ai-badge">AI</span>
          <h3>Summary side peek</h3>
        </div>
        <button className="close-button" onClick={onClose} title="Close">
          ✕
        </button>
      </div>

      <div className="summary-content">
        <div className="article-header">
          <h4 className="selected-article-title">{selectedArticle.title}</h4>
        </div>

        <div className="article-details">
          <div className="detail-section">
            <h5 className="detail-label">Author & Source</h5>
            <p className="detail-value">{selectedArticle.source?.name || 'Unknown Source'}</p>
          </div>
          
          <div className="detail-section">
            <h5 className="detail-label">Published Date</h5>
            <p className="detail-value">{formatDate(selectedArticle.publishedAt)}</p>
          </div>
        </div>

        <div className="summary-section">
          <h5>📝 Summary</h5>
          {isGenerating ? (
            <div className="summary-loading">
              <div className="loading-spinner"></div>
              <p>Generating AI summary...</p>
            </div>
          ) : (
            <div className="summary-text">
              {summary.split('\n').map((line, index) => (
                <p key={index}>{line}</p>
              ))}
            </div>
          )}
        </div>

        <div className="summary-section">
          <h5>🔗 Quick Actions</h5>
          <div className="action-buttons">
            <button 
              className="action-button primary"
              onClick={() => {
                if (selectedArticle.url && selectedArticle.url !== '#' && selectedArticle.url.startsWith('http')) {
                  window.open(selectedArticle.url, '_blank', 'noopener,noreferrer');
                } else {
                  // Fallback: Search for the article title on Google
                  const searchQuery = encodeURIComponent(selectedArticle.title);
                  window.open(`https://www.google.com/search?q=${searchQuery}`, '_blank', 'noopener,noreferrer');
                }
              }}
            >
              Read Full Article
            </button>
            <button 
              className="action-button secondary"
              onClick={() => {
                const shareData = {
                  title: selectedArticle.title,
                  text: selectedArticle.description || selectedArticle.title,
                  url: window.location.href
                };
                if (navigator.share) {
                  navigator.share(shareData);
                } else {
                  // Fallback: Copy to clipboard
                  navigator.clipboard.writeText(`${selectedArticle.title}\n${selectedArticle.description || ''}`);
                  alert('Article details copied to clipboard!');
                }
              }}
            >
              Share
            </button>
          </div>
        </div>

        {selectedArticle.description && (
          <div className="summary-section">
            <h5>📄 Description</h5>
            <p className="article-description">{selectedArticle.description}</p>
          </div>
        )}

        <div className="summary-section">
          <h5>📊 Article Stats</h5>
          <div className="article-stats">
            <div className="stat-item">
              <span className="stat-label">Source</span>
              <span className="stat-value">{selectedArticle.source?.name || 'N/A'}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Published</span>
              <span className="stat-value">{formatDate(selectedArticle.publishedAt)}</span>
            </div>
            <div className="stat-item">
              <span className="stat-label">Type</span>
              <span className="stat-value">News Article</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ArticleSummary;
