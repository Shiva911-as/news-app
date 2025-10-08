import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { 
  Home, 
  TrendingUp, 
  MapPin, 
  Briefcase, 
  Building2, 
  Trophy, 
  Laptop, 
  Rocket, 
  Film, 
  Globe,
  LogIn
} from 'lucide-react';
import './Sidebar.css';

const Sidebar = ({ onCategorySelect, selectedCategory, isOpen = true }) => {
  const [language, setLanguage] = useState('English');
  const navigate = useNavigate();

  const categories = [
    { id: 'home', name: 'Home', icon: Home, endpoint: '/api/news/category/home' },
    { id: 'business', name: 'Business', icon: Briefcase, endpoint: '/api/news/category/business' },
    { id: 'politics', name: 'Politics', icon: Building2, endpoint: '/api/news/category/politics' },
    { id: 'sports', name: 'Sports', icon: Trophy, endpoint: '/api/news/category/sports' },
    { id: 'technology', name: 'Technology', icon: Laptop, endpoint: '/api/news/category/technology' },
    { id: 'startups', name: 'Startups', icon: Rocket, endpoint: '/api/news/category/startups' },
    { id: 'entertainment', name: 'Entertainment', icon: Film, endpoint: '/api/news/category/entertainment' },
    { id: 'mobile', name: 'Mobile', icon: TrendingUp, endpoint: '/api/news/category/mobile' },
    { id: 'international', name: 'International', icon: Globe, endpoint: '/api/news/category/international' },
    { id: 'automobile', name: 'Automobile', icon: MapPin, endpoint: '/api/news/category/automobile' },
    { id: 'miscellaneous', name: 'Miscellaneous', icon: TrendingUp, endpoint: '/api/news/category/miscellaneous' }
  ];


  const handleCategoryClick = (category) => {
    onCategorySelect(category);
    // Update URL without full navigation to maintain state
    window.history.pushState({}, '', `/?category=${category.id}`);
  };

  return (
    <div className={`sidebar ${isOpen ? 'sidebar-open' : 'sidebar-closed'}`}>
      {isOpen && (
        <>
          <div className="sidebar-header">
            <h2 className="sidebar-title">News</h2>
            <div className="language-toggle">
              <button 
                className={`language-btn ${language === 'English' ? 'active' : ''}`}
                onClick={() => setLanguage('English')}
              >
                English
              </button>
              <button 
                className={`language-btn ${language === 'Telugu' ? 'active' : ''}`}
                onClick={() => setLanguage('Telugu')}
              >
                Telugu
              </button>
            </div>
          </div>
          
          <nav className="sidebar-nav">
            <ul className="category-list">
              {categories.map((category) => (
                <li key={category.id} className="category-item">
                  <button
                    className={`category-button ${selectedCategory?.id === category.id ? 'active' : ''}`}
                    onClick={() => handleCategoryClick(category)}
                    title={category.name}
                    data-category={category.id}
                  >
                    <category.icon className="category-icon" size={20} strokeWidth={1.5} />
                    <span className="category-name">{category.name}</span>
                  </button>
                </li>
              ))}
            </ul>
            
            <div className="sidebar-footer">
              <button
                className="login-button"
                onClick={() => navigate('/login')}
                title="Login"
              >
                <LogIn className="login-icon" size={20} strokeWidth={1.5} />
                <span className="login-text">Login</span>
              </button>
            </div>
          </nav>
        </>
      )}
    </div>
  );
};

export default Sidebar;
