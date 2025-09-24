import React from 'react';

const ArticleSchema = ({ article, isMainArticle = false }) => {
  if (!article) return null;

  const schema = {
    "@context": "https://schema.org",
    "@type": "NewsArticle",
    "headline": article.title,
    "description": article.description || article.title,
    "image": article.urlToImage ? [article.urlToImage] : [],
    "datePublished": article.publishedAt,
    "dateModified": article.publishedAt,
    "author": {
      "@type": "Organization",
      "name": article.source?.name || "News Source"
    },
    "publisher": {
      "@type": "Organization",
      "name": article.source?.name || "News App",
      "logo": {
        "@type": "ImageObject",
        "url": "https://newsapp.com/logo.png"
      }
    },
    "mainEntityOfPage": {
      "@type": "WebPage",
      "@id": article.url
    },
    "url": article.url,
    "articleSection": "News",
    "keywords": article.title.split(' ').slice(0, 5).join(', '),
    "wordCount": article.description ? article.description.split(' ').length : 0,
    "isAccessibleForFree": true,
    "inLanguage": "en-US"
  };

  // Add AI summary if available
  if (article.aiSummary) {
    schema.abstract = article.aiSummary;
  }

  // Add trending information if available
  if (article.isTrending) {
    schema.about = {
      "@type": "Thing",
      "name": "Trending News",
      "description": "Currently trending news article"
    };
  }

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{
        __html: JSON.stringify(schema, null, 2)
      }}
    />
  );
};

export default ArticleSchema;
