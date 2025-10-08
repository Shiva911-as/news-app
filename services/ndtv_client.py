import requests
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

from utils.logger import logger
from config import get_config


class NDTVClient:
    """
    Client for the NDTV scraping API (https://ndtvnews-api.herokuapp.com).
    Supports all three endpoints: /general, /cities, /sports
    Normalizes responses into our internal article schema used across the app.
    """

    def __init__(self) -> None:
        self.config = get_config()
        # Use the live Heroku API as default
        self.base_url: str = getattr(self.config, 'NDTV_BASE_URL', 'https://ndtvnews-api.herokuapp.com').rstrip('/')
        self.enabled: bool = getattr(self.config, 'NDTV_API_ENABLED', True)  # Enable by default
        self.timeout: int = int(getattr(self.config, 'NDTV_TIMEOUT', 10))  # Longer timeout for Heroku
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'NewsApp/1.0 (NDTVClient)'})

        if not self.enabled:
            logger.info("NDTVClient initialized but NDTV API is disabled.")
        else:
            logger.info(f"NDTVClient initialized with base URL: {self.base_url}")
            # Test API availability on initialization
            self._test_api_availability()

    def _test_api_availability(self) -> None:
        """Test if the NDTV API is available and working"""
        try:
            test_url = f"{self.base_url}/general"
            resp = self.session.get(test_url, timeout=5)
            if resp.status_code == 200:
                logger.info("✅ NDTV API is available and responding")
            else:
                logger.warning(f"⚠️ NDTV API returned status {resp.status_code}, falling back to mock data")
                self.enabled = False
        except Exception as e:
            logger.warning(f"⚠️ NDTV API not available ({e}), falling back to mock data")
            self.enabled = False

    def _get_mock_ndtv_data(self, category: str = 'india') -> List[Dict[str, Any]]:
        """Generate mock NDTV-style articles for testing when API is unavailable"""
        from datetime import datetime, timedelta
        import random
        
        mock_articles = {
            'india': [
                {
                    'headline': 'Government Announces New Digital India Initiative for Rural Areas',
                    'description': 'The central government has launched a comprehensive digital infrastructure program aimed at connecting remote villages across India with high-speed internet and digital services.',
                    'url': 'https://www.ndtv.com/india-news/government-digital-india-rural-mock-1',
                    'image_url': 'https://c.ndtvimg.com/2024-09/digital-india_650x400_61695123456.jpg',
                    'posted_date': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d')
                },
                {
                    'headline': 'Supreme Court Delivers Landmark Judgment on Environmental Protection',
                    'description': 'The apex court has issued new guidelines for industrial pollution control, emphasizing the need for sustainable development practices across all sectors.',
                    'url': 'https://www.ndtv.com/india-news/supreme-court-environment-mock-2',
                    'image_url': 'https://c.ndtvimg.com/2024-09/supreme-court_650x400_61695123457.jpg',
                    'posted_date': (datetime.now() - timedelta(hours=4)).strftime('%Y-%m-%d')
                }
            ],
            'cricket': [
                {
                    'headline': 'India Defeats Australia in Thrilling T20 Match, Kohli Scores Century',
                    'description': 'Virat Kohli\'s magnificent century helped India secure a 6-wicket victory over Australia in the second T20I at the Melbourne Cricket Ground.',
                    'url': 'https://sports.ndtv.com/cricket/india-australia-t20-kohli-century-mock-1',
                    'image_url': 'https://c.ndtvimg.com/2024-09/kohli-century_650x400_61695123458.jpg',
                    'posted_date': (datetime.now() - timedelta(hours=1)).strftime('%Y-%m-%d')
                },
                {
                    'headline': 'IPL 2024 Auction: Record Breaking Bids for Young Indian Talent',
                    'description': 'The IPL auction saw unprecedented bidding wars for emerging Indian cricketers, with several players fetching multi-crore deals.',
                    'url': 'https://sports.ndtv.com/cricket/ipl-auction-2024-mock-2',
                    'image_url': 'https://c.ndtvimg.com/2024-09/ipl-auction_650x400_61695123459.jpg',
                    'posted_date': (datetime.now() - timedelta(hours=3)).strftime('%Y-%m-%d')
                }
            ],
            'business': [
                {
                    'headline': 'Indian Startups Raise $2.5 Billion in Q3, Tech Sector Leads Growth',
                    'description': 'The Indian startup ecosystem continues its robust growth with significant funding rounds in fintech, edtech, and healthtech sectors.',
                    'url': 'https://www.ndtv.com/business/startup-funding-q3-mock-1',
                    'image_url': 'https://c.ndtvimg.com/2024-09/startup-funding_650x400_61695123460.jpg',
                    'posted_date': (datetime.now() - timedelta(hours=5)).strftime('%Y-%m-%d')
                }
            ]
        }
        
        return mock_articles.get(category, mock_articles['india'])

    def _parse_date(self, raw: Optional[str]) -> Optional[str]:
        if not raw:
            return None
        # Try common formats; fall back to current time if parse fails
        for fmt in [
            '%Y-%m-%dT%H:%M:%SZ',
            '%Y-%m-%dT%H:%M:%S.%fZ',
            '%a, %d %b %Y %H:%M:%S %Z',
            '%Y-%m-%d %H:%M:%S',
        ]:
            try:
                return datetime.strptime(raw, fmt).isoformat() + 'Z'
            except Exception:
                continue
        try:
            # As a last resort, some sources provide epoch
            if raw.isdigit():
                dt = datetime.utcfromtimestamp(int(raw))
                return dt.isoformat() + 'Z'
        except Exception:
            pass
        return None

    def _normalize_item(self, item: Dict[str, Any], category: str = None) -> Dict[str, Any]:
        # NDTV API uses 'headline' instead of 'title'
        title = item.get('headline') or item.get('title') or ''
        desc = item.get('description') or ''
        url = item.get('url') or ''
        image = item.get('image_url') or item.get('urlToImage')
        # NDTV API uses 'posted_date' in YYYY-MM-DD format
        posted_date = item.get('posted_date')
        published = None
        if posted_date:
            try:
                # Convert YYYY-MM-DD to ISO format
                dt = datetime.strptime(posted_date, '%Y-%m-%d')
                published = dt.isoformat() + 'Z'
            except Exception:
                published = None

        return {
            'source': {
                'id': 'ndtv',
                'name': 'NDTV',
            },
            'author': item.get('author') or 'NDTV',
            'title': title,
            'description': desc,
            'url': url,
            'urlToImage': image,
            'publishedAt': published,
            'content': desc,  # Use description as content
            'category': category or item.get('category') or 'general'
        }

    def fetch(self, path: str, params: Optional[Dict[str, Any]] = None) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        if not self.enabled:
            return False, None, 'NDTV API disabled'

        url = f"{self.base_url}{path}"
        try:
            resp = self.session.get(url, params=params or {}, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()

            # NDTV API returns: {"news": [{"category": "india", "articles": [...]}]}
            if not isinstance(data, dict) or 'news' not in data:
                logger.error(f"Invalid NDTV API response format: {data}")
                return False, None, 'Invalid NDTV API response format'

            all_articles = []
            for category_data in data['news']:
                if isinstance(category_data, dict) and 'articles' in category_data:
                    articles = category_data['articles']
                    category_name = category_data.get('category', 'general')
                    if isinstance(articles, list):
                        # Normalize each article with category info
                        for article in articles:
                            if isinstance(article, dict):
                                normalized_article = self._normalize_item(article, category_name)
                                all_articles.append(normalized_article)

            logger.info(f"NDTV API returned {len(all_articles)} articles from {url}")
            return True, all_articles, None
        except requests.exceptions.RequestException as e:
            logger.error(f"NDTV API request failed for {url}: {e}")
            return False, None, str(e)
        except Exception as e:
            logger.exception(f"Unexpected error while parsing NDTV response from {url}")
            return False, None, str(e)

    def fetch_general_news(self, categories: List[str] = None, limit: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetch general news from NDTV /general endpoint.
        Available categories: latest, india, world, science, business, entertainment, offbeat
        """
        if not categories:
            categories = ['latest', 'india']
        
        # Use /general endpoint with category parameter
        params = {
            'category': f'values({",".join(categories)})',
            'field': 'values(headline,description,url,image_url,posted_date)'
        }
        
        success, items, error = self.fetch('/general', params=params)
        if not success or not items:
            return success, items, error

        # Deduplicate by title and trim to limit
        return self._deduplicate_and_limit(items, limit)
    
    def fetch_sports_news(self, sports: List[str] = None, limit: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetch sports news from NDTV /sports endpoint.
        Available sports: cricket, football, tennis, formula-1, hockey, golf, badminton, chess, kabaddi, wrestling, nba, boxing
        """
        if not sports:
            sports = ['cricket', 'football']  # Default to popular sports
        
        params = {
            'sport': f'values({",".join(sports)})',
            'field': 'values(headline,description,url,image_url,posted_date)'
        }
        
        success, items, error = self.fetch('/sports', params=params)
        if not success or not items:
            return success, items, error

        return self._deduplicate_and_limit(items, limit)
    
    def fetch_city_news(self, cities: List[str] = None, limit: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetch city-specific news from NDTV /cities endpoint.
        Available cities: delhi, mumbai, chennai, bangalore, hyderabad, pune, kolkata, etc.
        """
        if not cities:
            cities = ['delhi', 'mumbai', 'bangalore']  # Default to major cities
        
        params = {
            'city': f'values({",".join(cities)})',
            'field': 'values(headline,description,url,image_url,posted_date)'
        }
        
        success, items, error = self.fetch('/cities', params=params)
        if not success or not items:
            return success, items, error

        return self._deduplicate_and_limit(items, limit)
    
    def _deduplicate_and_limit(self, items: List[Dict[str, Any]], limit: int) -> Tuple[bool, List[Dict[str, Any]], None]:
        """Remove duplicates by title and limit results"""
        seen = set()
        unique: List[Dict[str, Any]] = []
        for a in items:
            t = (a.get('title') or '').strip().lower()
            if t and t not in seen:
                seen.add(t)
                unique.append(a)
                if len(unique) >= limit:
                    break
        
        return True, unique, None
    
    def fetch_category(self, category: Optional[str] = None, limit: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Legacy method for backward compatibility. 
        Maps categories to appropriate endpoint calls.
        """
        category = (category or 'latest').lower()
        
        # Route to appropriate endpoint based on category
        if category in ['cricket', 'football', 'tennis', 'sports']:
            if category == 'sports':
                return self.fetch_sports_news(['cricket', 'football', 'tennis'], limit)
            else:
                return self.fetch_sports_news([category], limit)
        elif category in ['delhi', 'mumbai', 'chennai', 'bangalore', 'hyderabad', 'pune', 'kolkata']:
            return self.fetch_city_news([category], limit)
        else:
            # Map to general categories
            category_map = {
                'latest': ['latest'],
                'general': ['latest'], 
                'india': ['india'],
                'national': ['india'],
                'world': ['world'],
                'business': ['business'],
                'economy': ['business'],
                'science': ['science'],
                'entertainment': ['entertainment'],
                'offbeat': ['offbeat'],
                'technology': ['science'],  # NDTV doesn't have tech, use science
                'tech': ['science']
            }
            
            categories = category_map.get(category, ['latest'])
            return self.fetch_general_news(categories, limit)
    
    def fetch_comprehensive_news(self, limit: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Fetch a comprehensive mix of news from all NDTV endpoints.
        This gives you the most diverse content including cricket updates!
        Falls back to mock data if API is unavailable.
        """
        if not self.enabled:
            # Use mock data when API is unavailable
            logger.info("Using mock NDTV data (API unavailable)")
            all_articles = []
            
            # Add mock articles from different categories
            for category in ['india', 'cricket', 'business']:
                mock_data = self._get_mock_ndtv_data(category)
                for item in mock_data:
                    normalized = self._normalize_item(item, category)
                    all_articles.append(normalized)
            
            return self._deduplicate_and_limit(all_articles, limit)
        
        # Try real API calls
        all_articles = []
        
        # Fetch general news (India focus)
        success, general_articles, _ = self.fetch_general_news(['latest', 'india', 'world'], limit//3)
        if success and general_articles:
            all_articles.extend(general_articles)
        
        # Fetch sports news (including cricket!)
        success, sports_articles, _ = self.fetch_sports_news(['cricket', 'football', 'tennis'], limit//3)
        if success and sports_articles:
            all_articles.extend(sports_articles)
        
        # Fetch city news
        success, city_articles, _ = self.fetch_city_news(['delhi', 'mumbai', 'bangalore'], limit//3)
        if success and city_articles:
            all_articles.extend(city_articles)
        
        # If no articles from API, fall back to mock data
        if not all_articles:
            logger.warning("API calls failed, using mock NDTV data")
            for category in ['india', 'cricket', 'business']:
                mock_data = self._get_mock_ndtv_data(category)
                for item in mock_data:
                    normalized = self._normalize_item(item, category)
                    all_articles.append(normalized)
        
        # Final deduplication and limit
        return self._deduplicate_and_limit(all_articles, limit)
