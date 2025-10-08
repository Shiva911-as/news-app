import requests
import time
from typing import Dict, List, Optional, Any, Tuple
from utils.logger import logger
from config import get_config


class GNewsService:
    """GNews API Service for India-focused news with clean, structured results"""

    def __init__(self):
        self.config = get_config()
        self.api_key = self.config.GNEWS_API_KEY
        self.base_url = 'https://gnews.io/api/v4'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NewsApp/1.0 (India-focused)',
            'Accept': 'application/json'
        })
        self.last_request_time = 0
        self.min_request_interval = 0.2  # 200ms between requests
        self.rate_limit_reset_time = 0
        
        # India-specific search terms for better targeting
        self.indian_topics = {
            'politics': ['Modi', 'BJP', 'Congress', 'Parliament', 'Lok Sabha', 'Indian government'],
            'economy': ['RBI', 'Rupee', 'NSE', 'BSE', 'Indian economy', 'GDP India'],
            'technology': ['Indian startups', 'Bangalore tech', 'IT sector India', 'Digital India'],
            'sports': ['Indian cricket', 'IPL', 'India vs', 'cricket team India'],
            'regional': ['Delhi news', 'Mumbai news', 'Bangalore news', 'Chennai news'],
            'global': ['India international', 'India trade', 'India diplomacy']
        }
        
        # Quality Indian news sources (GNews format)
        self.preferred_sources = [
            'timesofindia.indiatimes.com',
            'thehindu.com',
            'hindustantimes.com',
            'indianexpress.com',
            'ndtv.com',
            'zeenews.india.com',
            'indiatoday.in',
            'news18.com',
            'firstpost.com',
            'thewire.in',
            'scroll.in',
            'livemint.com',
            'economictimes.indiatimes.com',
            'business-standard.com'
        ]

    def _rate_limit_check(self) -> bool:
        """Check rate limit and spacing between requests."""
        now = time.time()

        if now < self.rate_limit_reset_time:
            logger.warning("GNews rate limit active. Try after cooldown.")
            return False

        elapsed = now - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        self.last_request_time = time.time()
        return True

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Make API request to GNews API.

        Returns:
            success: True/False
            articles: List of articles or None
            error_message: Error string if failed
        """
        if not self.api_key:
            return False, None, "GNews API key not configured"

        if not self._rate_limit_check():
            return False, None, "Rate limit exceeded. Try again later."

        params['apikey'] = self.api_key
        url = f"{self.base_url}/{endpoint}"

        try:
            logger.info(f"Fetching from GNews endpoint: {endpoint}")
            response = self.session.get(url, params=params, timeout=5)

            if response.status_code == 429:
                logger.error("GNews API rate limit hit.")
                self.rate_limit_reset_time = time.time() + 300  # 5 min cooldown
                return False, None, "GNews API rate limit exceeded."

            if response.status_code == 403:
                logger.error("GNews API key invalid or expired.")
                return False, None, "GNews API key invalid."

            response.raise_for_status()
            data = response.json()

            if 'articles' not in data:
                logger.error(f"GNews API error: {data}")
                return False, None, "Invalid response from GNews API."

            # Transform GNews format to our standard format
            articles = self._transform_gnews_articles(data['articles'])
            return True, articles, None

        except requests.exceptions.Timeout:
            logger.exception("GNews request timed out.")
            return False, None, "Request timed out."

        except requests.exceptions.RequestException as e:
            logger.exception("GNews network error.")
            return False, None, str(e)
        except Exception as e:
            logger.exception(f"Unexpected GNews error: {e}")
            return False, None, str(e)

    def _transform_gnews_articles(self, gnews_articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Transform GNews article format to our standard format."""
        transformed = []
        
        for article in gnews_articles:
            try:
                # Transform to NewsAPI-compatible format
                transformed_article = {
                    'title': article.get('title', ''),
                    'description': article.get('description', ''),
                    'url': article.get('url', ''),
                    'urlToImage': article.get('image', ''),
                    'publishedAt': article.get('publishedAt', ''),
                    'content': article.get('content', ''),
                    'source': {
                        'id': None,
                        'name': article.get('source', {}).get('name', 'GNews')
                    }
                }
                
                # Add GNews-specific metadata
                transformed_article['gnews_source'] = True
                transformed_article['source_url'] = article.get('source', {}).get('url', '')
                
                transformed.append(transformed_article)
                
            except Exception as e:
                logger.warning(f"Error transforming GNews article: {e}")
                continue
        
        return transformed

    def get_indian_headlines(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get top headlines from India using GNews API."""
        params = {
            'lang': 'en',
            'country': 'in',
            'max': min(page_size, 100)  # GNews max is 100
        }
        
        return self._make_request('top-headlines', params)
    
    def get_category_headlines(self, category: str, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get category-specific headlines from India using GNews API."""
        params = {
            'category': category,
            'lang': 'en',
            'country': 'in',
            'max': min(page_size, 100)
        }
        
        return self._make_request('top-headlines', params)

    def search_indian_news(self, query: str, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Search for news with Indian context using GNews API."""
        params = {
            'q': query,
            'lang': 'en',
            'country': 'in',
            'max': min(page_size, 100)
        }
        
        return self._make_request('search', params)

    def get_topic_news(self, topic: str, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get news for specific topics with Indian focus."""
        # Enhance topic with Indian context
        if topic.lower() in self.indian_topics:
            # Use predefined Indian-focused search terms
            search_terms = self.indian_topics[topic.lower()]
            query = f"({' OR '.join(search_terms)})"
        else:
            # Add India context to any topic
            query = f"{topic} India"
        
        return self.search_indian_news(query, page_size)

    def get_cricket_news(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get cricket news with Indian focus."""
        cricket_queries = [
            'Indian cricket team',
            'IPL cricket India',
            'India vs cricket match',
            'Virat Kohli cricket',
            'cricket tournament India'
        ]
        
        all_articles = []
        for query in cricket_queries:
            success, articles, _ = self.search_indian_news(query, page_size // len(cricket_queries))
            if success and articles:
                # Mark as cricket category
                for article in articles:
                    article['category'] = 'cricket'
                all_articles.extend(articles)
        
        if all_articles:
            # Deduplicate by title
            seen = set()
            unique_articles = []
            for article in all_articles:
                title = article.get('title', '').strip().lower()
                if title and title not in seen:
                    seen.add(title)
                    unique_articles.append(article)
            
            return True, unique_articles[:page_size], None
        else:
            return False, None, "No cricket articles found"

    def get_startup_tech_news(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get startup and technology news focused on India."""
        tech_queries = [
            'Indian startups funding',
            'Bangalore tech companies',
            'India technology innovation',
            'Digital India initiatives',
            'Indian IT sector'
        ]
        
        all_articles = []
        for query in tech_queries:
            success, articles, _ = self.search_indian_news(query, page_size // len(tech_queries))
            if success and articles:
                # Mark as technology category
                for article in articles:
                    article['category'] = 'technology'
                all_articles.extend(articles)
        
        if all_articles:
            # Deduplicate and return
            seen = set()
            unique_articles = []
            for article in all_articles:
                title = article.get('title', '').strip().lower()
                if title and title not in seen:
                    seen.add(title)
                    unique_articles.append(article)
            
            return True, unique_articles[:page_size], None
        else:
            return False, None, "No tech articles found"

    def get_comprehensive_indian_news(self, page_size: int = 100) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get comprehensive Indian news from multiple categories."""
        try:
            all_articles = []
            
            # Get headlines first
            success, headlines, _ = self.get_indian_headlines(page_size // 3)
            if success and headlines:
                all_articles.extend(headlines)
            
            # Get cricket news (trending)
            success, cricket, _ = self.get_cricket_news(page_size // 4)
            if success and cricket:
                all_articles.extend(cricket)
            
            # Get tech news
            success, tech, _ = self.get_startup_tech_news(page_size // 4)
            if success and tech:
                all_articles.extend(tech)
            
            # Get politics news
            success, politics, _ = self.get_topic_news('politics', page_size // 6)
            if success and politics:
                all_articles.extend(politics)
            
            # Get economy news
            success, economy, _ = self.get_topic_news('economy', page_size // 6)
            if success and economy:
                all_articles.extend(economy)
            
            if all_articles:
                # Deduplicate by title
                seen = set()
                unique_articles = []
                for article in all_articles:
                    title = article.get('title', '').strip().lower()
                    if title and title not in seen:
                        seen.add(title)
                        unique_articles.append(article)
                
                logger.info(f"GNews comprehensive: {len(unique_articles)} unique articles")
                return True, unique_articles[:page_size], None
            else:
                return False, None, "No articles found from GNews"
                
        except Exception as e:
            logger.error(f"Error getting comprehensive Indian news: {e}")
            return False, None, str(e)

    def is_available(self) -> bool:
        """Check if GNews API is available and configured."""
        return bool(self.api_key)
