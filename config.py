import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY') or 'afb4ce6d6ca347ebad67c93a75780711'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///news_app.db'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/news_app.log')
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '60'))
    
    # News API settings
    NEWS_API_BASE_URL = 'https://newsapi.org/v2'
    DEFAULT_LANGUAGE = 'en'
    DEFAULT_PAGE_SIZE = 50
    MAX_PAGE_SIZE = 100
    
    # User profile settings
    USER_PROFILE_FILE = 'user_profile.json'
    DEFAULT_TOPIC_WEIGHT = 1.0
    RELATED_TOPIC_WEIGHT = 0.5
    LEARNING_RATE = 0.5
    
    # Related topics mapping
    RELATED_TOPICS = {
        "ai": ["artificial intelligence", "machine learning", "deep learning", "nlp", "neural networks"],
        "cricket": ["sports", "football", "ipl", "match", "cricket", "batsman", "bowler"],
        "tech": ["gadgets", "innovation", "startups", "technology", "software", "hardware"],
        "finance": ["stocks", "economy", "investment", "market", "trading", "cryptocurrency"],
        "politics": ["government", "elections", "policy", "parliament", "democracy"],
        "health": ["medical", "healthcare", "medicine", "hospital", "doctor"],
        "science": ["research", "discovery", "experiment", "scientific", "study"],
        "entertainment": ["movie", "music", "celebrity", "film", "actor", "actress"],
    }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False
    LOG_LEVEL = 'WARNING'

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True
    DATABASE_URL = 'sqlite:///:memory:'

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name: str = None) -> Config:
    """Get configuration based on environment"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    return config.get(config_name, config['default'])
