from flask import Flask, request, jsonify, session
from flask_cors import CORS
import os
import time
from datetime import datetime
from typing import Dict, List, Any

from config import get_config
from services.cached_news_service import CachedNewsService
from models.user_profile import UserProfile
from utils.logger import logger
from user_tracking import UserTracker
# from auth.google_oauth import init_auth, auth_bp  # Temporarily disabled until dependencies are installed

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(get_config())
CORS(app, supports_credentials=True)

# Initialize authentication
# login_manager = init_auth(app)  # Temporarily disabled until dependencies are installed

# Initialize services
cached_news_service = CachedNewsService()
user_tracker = UserTracker()

@app.route('/')
def index():
    return jsonify({
        'message': 'News App API is running - REAL-TIME MODE',
        'status': 'success'
    })

@app.route('/api/news/trending')
def api_trending_news():
    """Smart cached trending news"""
    try:
        page_size = request.args.get('page_size', 8, type=int)
        logger.info("🚀 Smart cached trending news...")
        
        success, articles, error = cached_news_service.get_cached_category_news('home', page_size)
        
        if success and articles:
            logger.info(f"✅ Trending: {len(articles)} articles from smart cache")
            return jsonify({
                'status': 'success',
                'articles': articles,
                'source': 'smart_cache',
                'timestamp': time.time(),
                'cached': True
            })
        else:
            logger.error(f"Smart cache failed: {error}")
            return jsonify({
                'status': 'error',
                'message': error or 'Failed to fetch trending news',
                'articles': []
            }), 500
            
    except Exception as e:
        logger.error(f"Trending API error: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@app.route('/api/news/sports')
def api_sports_news():
    """Sports news with smart caching"""
    try:
        page_size = request.args.get('page_size', 8, type=int)
        success, articles, error = cached_news_service.get_cached_category_news('sports', page_size)
        
        if success and articles:
            logger.info(f"✅ Sports: {len(articles)} articles from smart cache")
            return jsonify({
                'success': True,
                'articles': articles,
                'source': 'smart_cache',
                'category': 'sports'
            })
        else:
            return jsonify({
                'success': False,
                'error': error,
                'articles': []
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/news/search')
def api_search_news():
    """Search news (bypasses cache as results are query-specific)"""
    try:
        query = request.args.get('q', '')
        page_size = request.args.get('page_size', 8, type=int)
        
        if not query:
            return jsonify({'success': False, 'error': 'Query required'}), 400
        
        success, articles, error = cached_news_service.search_articles(query, page_size)
        
        if success and articles:
            return jsonify({
                'success': True,
                'articles': articles,
                'query': query,
                'cached': False  # Search results are not cached
            })
        else:
            return jsonify({
                'success': False,
                'error': error or 'Search failed',
                'articles': []
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/recommendations')
def api_recommendations():
    """REAL-TIME recommendations"""
    try:
        # Use trending as recommendations for now
        success, articles, error = news_service.get_top_headlines(country='in', page_size=15)
        if success and articles:
            recommendations = [{'score': 5.0, 'article': article} for article in articles]
            return jsonify({
                'success': True,
                'recommendations': recommendations,
                'source': 'newsapi_realtime'
            })
        
        # Fallback
        from services.fallback_data import get_trending_fallback
        articles = get_trending_fallback(15)
        recommendations = [{'score': 3.0, 'article': article} for article in articles]
        return jsonify({
            'success': True,
            'recommendations': recommendations,
            'source': 'fallback_static'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/news/indian')
def api_indian_news():
    """REAL-TIME Indian news"""
    try:
        page_size = request.args.get('page_size', 20, type=int)
        logger.info("🇮🇳 NewsAPI ONLY - real-time Indian news...")
        
        # Use search for Indian news (more reliable)
        success, articles, error = news_service.search_articles('India news current affairs', page_size=page_size)
        if success and articles:
            logger.info(f"✅ NewsAPI Indian: {len(articles)} articles")
            return jsonify({
                'success': True,
                'articles': articles,
                'source': 'newsapi_realtime',
                'timestamp': time.time()
            })
        
        # Fallback
        from services.fallback_data import get_trending_fallback
        articles = get_trending_fallback(page_size)
        return jsonify({
            'success': True,
            'articles': articles,
            'source': 'fallback_static'
        })
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# SMART CACHING ENDPOINTS - All 11 categories
@app.route('/api/news/category/<category>')
def api_category_news(category):
    """Generic category endpoint with smart caching"""
    try:
        page_size = request.args.get('page_size', 8, type=int)
        
        # Validate category
        valid_categories = [
            'home', 'business', 'politics', 'sports', 'technology', 
            'startups', 'entertainment', 'mobile', 'international', 
            'automobile', 'miscellaneous'
        ]
        
        if category not in valid_categories:
            return jsonify({
                'status': 'error',
                'message': f'Invalid category. Valid categories: {valid_categories}'
            }), 400
        
        success, articles, error = cached_news_service.get_cached_category_news(category, page_size)
        
        if success and articles:
            logger.info(f"✅ {category.title()}: {len(articles)} articles from smart cache")
            return jsonify({
                'status': 'success',
                'articles': articles,
                'category': category,
                'cached': True,
                'count': len(articles)
            })
        else:
            logger.error(f"Smart cache failed for {category}: {error}")
            return jsonify({
                'status': 'error',
                'message': error or f'Failed to fetch {category} news',
                'articles': []
            }), 500
            
    except Exception as e:
        logger.error(f"Error in category {category}: {e}")
        return jsonify({
            'status': 'error',
            'message': str(e),
            'articles': []
        }), 500

# Update existing endpoints to use smart caching
@app.route('/api/news/business')
def api_business_news():
    """Business news with smart caching"""
    try:
        page_size = request.args.get('page_size', 8, type=int)
        success, articles, error = cached_news_service.get_cached_category_news('business', page_size)
        
        if success and articles:
            return jsonify({
                'success': True,
                'articles': articles,
                'source': 'smart_cache',
                'category': 'business'
            })
        else:
            return jsonify({
                'success': False,
                'error': error,
                'articles': []
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/news/politics')
def api_politics_news():
    """Politics news with smart caching"""
    try:
        page_size = request.args.get('page_size', 8, type=int)
        success, articles, error = cached_news_service.get_cached_category_news('politics', page_size)
        
        if success and articles:
            return jsonify({
                'success': True,
                'articles': articles,
                'source': 'smart_cache',
                'category': 'politics'
            })
        else:
            return jsonify({
                'success': False,
                'error': error,
                'articles': []
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/news/technology')
def api_technology_news():
    """Technology news with smart caching"""
    try:
        page_size = request.args.get('page_size', 8, type=int)
        success, articles, error = cached_news_service.get_cached_category_news('technology', page_size)
        
        if success and articles:
            return jsonify({
                'success': True,
                'articles': articles,
                'source': 'smart_cache',
                'category': 'technology'
            })
        else:
            return jsonify({
                'success': False,
                'error': error,
                'articles': []
            }), 500
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

# Cache management endpoints
@app.route('/api/cache/refresh', methods=['POST'])
def api_cache_refresh():
    """Force refresh cache (for manual refresh button)"""
    try:
        success = cached_news_service.force_refresh_cache()
        
        if success:
            return jsonify({
                'status': 'success',
                'message': 'Cache refreshed successfully',
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({
                'status': 'error',
                'message': 'Failed to refresh cache'
            }), 500
            
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    logger.info("Starting Smart Cached News App")
    app.run(debug=True, host='0.0.0.0', port=5000)
