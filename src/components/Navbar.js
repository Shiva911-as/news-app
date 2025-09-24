import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { FaNewspaper, FaHome, FaCog, FaUser, FaSearch, FaBars, FaTimes, FaMoon, FaSun } from 'react-icons/fa';
import { useDarkMode } from '../context/DarkModeContext';
import './Navbar.css';

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const location = useLocation();
  const { isDarkMode, toggleDarkMode } = useDarkMode();

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  const closeMenu = () => {
    setIsMenuOpen(false);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-brand" onClick={closeMenu}>
          <FaNewspaper />
          News App
        </Link>

        <button className="navbar-toggle" onClick={toggleMenu}>
          {isMenuOpen ? <FaTimes /> : <FaBars />}
        </button>

        <ul className={`navbar-nav ${isMenuOpen ? 'active' : ''}`}>
          <li>
            <Link 
              to="/" 
              className={`nav-link ${isActive('/') ? 'active' : ''}`}
              onClick={closeMenu}
            >
              <FaHome />
              Home
            </Link>
          </li>
          <li>
            <Link 
              to="/search" 
              className={`nav-link ${isActive('/search') ? 'active' : ''}`}
              onClick={closeMenu}
            >
              <FaSearch />
              Search
            </Link>
          </li>
          <li>
            <Link 
              to="/profile" 
              className={`nav-link ${isActive('/profile') ? 'active' : ''}`}
              onClick={closeMenu}
            >
              <FaUser />
              Profile
            </Link>
          </li>
          <li>
            <Link 
              to="/setup" 
              className={`nav-link ${isActive('/setup') ? 'active' : ''}`}
              onClick={closeMenu}
            >
              <FaCog />
              Setup
            </Link>
          </li>
          <li>
            <button 
              className="nav-link dark-mode-toggle-btn"
              onClick={toggleDarkMode}
              aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
            >
              {isDarkMode ? <FaSun /> : <FaMoon />}
              {isDarkMode ? 'Light' : 'Dark'}
            </button>
          </li>
        </ul>
      </div>
    </nav>
  );
};

export default Navbar;
