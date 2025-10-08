import React from 'react';
import './ArticleBox.css';

const ArticleBox = ({ article, onClick, isSelected = false }) => {

  const truncateTitle = (title, maxLength = 100) => {
    if (!title) return 'Untitled Article';
    if (title.length <= maxLength) return title;
    return title.substring(0, maxLength) + '...';
  };

  const handleClick = () => {
    console.log('Article clicked:', article.title);
    if (onClick) {
      onClick(article);
    }
  };

  return (
    <div 
      className={`modern-article-card ${isSelected ? 'selected' : ''}`}
      onClick={handleClick}
    >
      <div className="card-header">
        <h3 className="card-title">
          {truncateTitle(article.title)}
        </h3>
      </div>
      
      <div className="card-content">
        <div className="card-meta">
          <span className="card-source">
            {article.source?.name || 'Kara Swisher'}
          </span>
          <span className="card-type">Article</span>
        </div>
      </div>
    </div>
  );
};

export default ArticleBox;
