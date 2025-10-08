import os
from dotenv import load_dotenv
from typing import Dict, Any

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///news_app.db'
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/news_app.log')
    RATE_LIMIT_PER_MINUTE = int(os.environ.get('RATE_LIMIT_PER_MINUTE', '60'))
    
    # News API Configuration (PRIMARY SOURCE - RELIABLE & FREE)
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', '59c25ff5f05a4f6e8de956b222f24407')
    NEWS_API_BASE_URL = 'https://newsapi.org/v2'
    MAX_PAGE_SIZE = 100
    DEFAULT_LANGUAGE = 'en'
    
    # GNews API Configuration (Secondary - for when NewsAPI is exhausted)
    GNEWS_API_KEY = os.getenv('GNEWS_API_KEY', '4179c034edf4e40d665a3db70307410e')
    GNEWS_BASE_URL = 'https://gnews.io/api/v4'
    GNEWS_ENABLED = os.environ.get('GNEWS_ENABLED', 'true').lower() == 'true'
    
    # NDTV API Configuration
    NDTV_TIMEOUT = int(os.environ.get('NDTV_TIMEOUT', '8'))
    
    # User profile settings
    USER_PROFILE_FILE = 'user_profile.json'
    DEFAULT_TOPIC_WEIGHT = 1.0
    RELATED_TOPIC_WEIGHT = 0.5
    LEARNING_RATE = 0.5
    
    # Related topics mapping with Indian focus
    RELATED_TOPICS = {
        "indian_politics": ["modi", "bjp", "congress", "parliament", "lok sabha", "rajya sabha", "elections", "government", "policy", "democracy"],
        "indian_economy": ["rbi", "rupee", "nse", "bse", "sensex", "nifty", "gdp", "inflation", "budget", "finance minister"],
        "technology": ["artificial intelligence", "machine learning", "startups", "innovation", "software", "hardware", "it sector", "bangalore", "hyderabad"],
        "global_affairs": ["international", "diplomacy", "trade", "foreign policy", "china", "pakistan", "usa", "europe", "climate change"],
        "indian_regional": ["delhi", "mumbai", "bangalore", "chennai", "kolkata", "hyderabad", "pune", "state government", "regional news"],
        "science_research": ["isro", "space", "research", "discovery", "experiment", "scientific", "study", "innovation"],
        "health_policy": ["healthcare", "medicine", "hospital", "doctor", "public health", "covid", "vaccination"],
        "infrastructure": ["railways", "metro", "roads", "airports", "smart cities", "development", "urbanization"],
        "education": ["iit", "iim", "universities", "schools", "education policy", "skill development"],
        "defense": ["army", "navy", "air force", "border", "security", "defense deals", "military"],
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
