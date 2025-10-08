import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Home as HomeIcon } from 'lucide-react';
import './App.css';

// Simple News App Component
function SimpleNewsApp() {
  const [articles, setArticles] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('home');
  const [loading, setLoading] = useState(false);

  const categories = [
    { id: 'home', name: 'Home' },
    { id: 'business', name: 'Business' },
    { id: 'sports', name: 'Sports' },
    { id: 'technology', name: 'Technology' },
    { id: 'politics', name: 'Politics' },
    { id: 'entertainment', name: 'Entertainment' }
  ];

  const loadNews = async (category) => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:5000/api/news/category/${category}?page_size=8`);
      const data = await response.json();
      
      if (data.status === 'success') {
        setArticles(data.articles || []);
      } else {
        setArticles([]);
      }
    } catch (error) {
      console.error('Error loading news:', error);
      setArticles([]);
    }
    setLoading(false);
  };

  useEffect(() => {
    loadNews(selectedCategory);
  }, [selectedCategory]);

  return (
    <div style={{ 
      minHeight: '100vh', 
      background: '#0f0f0f', 
      color: '#ffffff',
      fontFamily: 'Arial, sans-serif'
    }}>
      {/* Header */}
      <header style={{ 
        background: '#1a1a1a', 
        padding: '15px 20px', 
        borderBottom: '1px solid #333',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between'
      }}>
        <h1 style={{ margin: 0, color: '#3b82f6' }}>📰 NewsHub</h1>
        <div style={{ fontSize: '14px', color: '#888' }}>
          Real-time Indian News
        </div>
      </header>

      <div style={{ display: 'flex' }}>
        {/* Sidebar */}
        <nav style={{ 
          width: '240px', 
          background: '#1a1a1a', 
          minHeight: 'calc(100vh - 60px)',
          padding: '20px 0',
          borderRight: '1px solid #333'
        }}>
          <div style={{ padding: '0 20px', marginBottom: '20px' }}>
            <h3 style={{ margin: 0, color: '#888', fontSize: '14px' }}>CATEGORIES</h3>
          </div>
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => setSelectedCategory(category.id)}
              style={{
                width: '100%',
                padding: '12px 20px',
                background: selectedCategory === category.id ? '#3b82f6' : 'transparent',
                color: selectedCategory === category.id ? '#ffffff' : '#cccccc',
                border: 'none',
                textAlign: 'left',
                cursor: 'pointer',
                fontSize: '14px',
                transition: 'all 0.2s'
              }}
            >
              {category.name}
            </button>
          ))}
        </nav>

        {/* Main Content */}
        <main style={{ 
          flex: 1, 
          padding: '30px',
          maxWidth: 'calc(100vw - 240px)'
        }}>
          <div style={{ marginBottom: '30px' }}>
            <h2 style={{ margin: 0, textTransform: 'capitalize' }}>
              {categories.find(c => c.id === selectedCategory)?.name} News
            </h2>
            <p style={{ color: '#888', margin: '5px 0 0 0' }}>
              {loading ? 'Loading...' : `${articles.length} articles available`}
            </p>
          </div>

          {loading ? (
            <div style={{ textAlign: 'center', padding: '50px' }}>
              <div style={{ color: '#3b82f6', fontSize: '18px' }}>Loading news...</div>
            </div>
          ) : (
            <div style={{ 
              display: 'grid', 
              gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
              gap: '20px'
            }}>
              {articles.map((article, index) => (
                <div key={index} style={{
                  background: '#1a1a1a',
                  border: '1px solid #333',
                  borderRadius: '8px',
                  padding: '20px',
                  cursor: 'pointer',
                  transition: 'all 0.2s'
                }}
                onMouseOver={(e) => e.target.style.borderColor = '#3b82f6'}
                onMouseOut={(e) => e.target.style.borderColor = '#333'}
                onClick={() => window.open(article.url, '_blank')}
                >
                  <h3 style={{ 
                    margin: '0 0 10px 0', 
                    fontSize: '16px',
                    lineHeight: '1.4',
                    color: '#ffffff'
                  }}>
                    {article.title}
                  </h3>
                  <p style={{ 
                    color: '#cccccc', 
                    fontSize: '14px',
                    lineHeight: '1.5',
                    margin: '0 0 15px 0'
                  }}>
                    {article.description}
                  </p>
                  <div style={{ 
                    display: 'flex', 
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    fontSize: '12px',
                    color: '#888'
                  }}>
                    <span>{article.source?.name}</span>
                    <span>Click to read →</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {!loading && articles.length === 0 && (
            <div style={{ 
              textAlign: 'center', 
              padding: '50px',
              color: '#888'
            }}>
              No articles available for this category.
            </div>
          )}
        </main>
      </div>
    </div>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/*" element={<SimpleNewsApp />} />
    </Routes>
  );
}

export default App;
