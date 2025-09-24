import requests
import time
from typing import Dict, List, Optional, Any, Tuple
from utils.logger import logger
from config import get_config
from .fallback_data import get_fallback_articles, get_trending_fallback, search_fallback


class NewsService:
    """News Service with API and Fallback Support"""

    def __init__(self):
        self.config = get_config()
        self.api_key = self.config.NEWS_API_KEY
        self.base_url = self.config.NEWS_API_BASE_URL
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'NewsApp/1.0 (RealTime)'})
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 100ms
        self.rate_limit_reset_time = 0

    def _rate_limit_check(self) -> bool:
        """Check rate limit and spacing between requests."""
        now = time.time()

        if now < self.rate_limit_reset_time:
            logger.warning("Rate limit active. Try after cooldown.")
            return False

        elapsed = now - self.last_request_time
        if elapsed < self.min_request_interval:
            time.sleep(self.min_request_interval - elapsed)

        self.last_request_time = time.time()
        return True

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Make API request to News API (no fallback).

        Returns:
            success: True/False
            articles: List of articles or None
            error_message: Error string if failed
        """
        if not self._rate_limit_check():
            return False, None, "Rate limit exceeded. Try again later."

        params['apiKey'] = self.api_key
        url = f"{self.base_url}/{endpoint}"

        try:
            logger.info(f"Fetching from endpoint: {endpoint}")
            response = self.session.get(url, params=params, timeout=3)

            if response.status_code == 429:
                logger.error("API rate limit hit.")
                self.rate_limit_reset_time = time.time() + 60  # 1 min cooldown
                return False, None, "API rate limit exceeded."

            response.raise_for_status()
            data = response.json()

            if data.get('status') != 'ok' or 'articles' not in data:
                logger.error(f"API error: {data}")
                return False, None, "Invalid response from news API."

            return True, data['articles'], None

        except requests.exceptions.Timeout:
            logger.exception("Request timed out.")
            return False, None, "Request timed out."

        except requests.exceptions.RequestException as e:
            logger.exception("Network error.")
            return False, None, str(e)
        except Exception as e:
            logger.exception(f"Unexpected error: {e}")
            return False, None, str(e)

    def get_top_headlines(self, country: str = 'us', category: Optional[str] = None, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Get top headlines with fallback support.

        Returns:
            success, articles or None, error message or None
        """
        params = {
            'country': country,
            'pageSize': min(page_size, self.config.MAX_PAGE_SIZE)
        }
        if category:
            params['category'] = category

        success, articles, error = self._make_request('top-headlines', params)
        
        # If API fails, use fallback data
        if not success:
            logger.warning(f"API failed, using fallback data: {error}")
            fallback_articles = get_fallback_articles(page_size=page_size)
            return True, fallback_articles, None
        
        return success, articles, error

    def search_articles(self, query: str, from_date: Optional[str] = None, to_date: Optional[str] = None,
                        sort_by: str = 'publishedAt', page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Search articles by keyword with fallback support.
        """
        params = {
            'q': query,
            'language': self.config.DEFAULT_LANGUAGE,
            'sortBy': sort_by,
            'pageSize': min(page_size, self.config.MAX_PAGE_SIZE)
        }
        if from_date:
            params['from'] = from_date
        if to_date:
            params['to'] = to_date

        success, articles, error = self._make_request('everything', params)
        
        # If API fails, use fallback data
        if not success:
            logger.warning(f"API search failed, using fallback data: {error}")
            fallback_articles = search_fallback(query=query, page_size=page_size)
            return True, fallback_articles, None
        
        return success, articles, error

    def get_articles_by_topic(self, topic: str, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Get articles based on topic/interest.
        """
        return self.search_articles(query=topic, page_size=page_size)

    def get_trending_articles(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """
        Get trending articles with fallback support.
        """
        categories = ['general', 'technology', 'business', 'sports', 'entertainment']
        collected_articles = []
        api_failed = False

        for category in categories:
            success, articles, error = self.get_top_headlines(category=category, page_size=page_size // len(categories))
            if success and articles:
                # Check if this is fallback data (no real API success)
                if not any('example.com' in article.get('url', '') for article in articles[:1]):
                    collected_articles.extend(articles)
                else:
                    # This is fallback data, mark API as failed
                    api_failed = True
                    collected_articles.extend(articles)
            else:
                logger.warning(f"Skipped category '{category}' due to error: {error}")
                api_failed = True

        # If all API calls failed, use comprehensive fallback
        if not collected_articles or api_failed:
            logger.warning("Using fallback trending articles")
            fallback_articles = get_trending_fallback(page_size=page_size)
            return True, fallback_articles, None

        # Deduplicate by title
        seen = set()
        unique_articles = []
        for article in collected_articles:
            title = article.get('title', '').strip().lower()
            if title and title not in seen:
                seen.add(title)
                unique_articles.append(article)

        return True, unique_articles[:page_size], None
