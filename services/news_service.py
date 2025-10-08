import requests
import time
import re
from typing import Dict, List, Optional, Any, Tuple
from utils.logger import logger
from config import get_config
from .fallback_data import get_fallback_articles, get_trending_fallback, search_fallback
from .ndtv_client import NDTVClient
from .gnews_service import GNewsService


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
        
        # Primary GNews service for India-focused content
        try:
            self.gnews_service = GNewsService()
            if self.gnews_service.is_available():
                logger.info("GNews API initialized successfully - Primary source for Indian news")
            else:
                logger.warning("GNews API key not configured - falling back to NewsAPI")
                self.gnews_service = None
        except Exception as e:
            logger.warning(f"Failed to initialize GNews service: {e}")
            self.gnews_service = None
        
        # Optional NDTV client (community scraper API)
        try:
            self.ndtv_client = NDTVClient()
        except Exception as e:
            logger.warning(f"Failed to initialize NDTVClient: {e}")
            self.ndtv_client = None
        
        # Quality filters
        self.clickbait_patterns = [
            r'\b(shocking|unbelievable|amazing|incredible|stunning)\b',
            r'\b(you won\'t believe|this will|must see|viral)\b',
            r'\b(celebrities?|bollywood|gossip|scandal)\b',
            r'\b(top \d+|\d+ things|\d+ ways)\b',
            r'[!]{2,}|[?]{2,}',
            r'\b(click here|watch now|see more)\b'
        ]
        
        # Preferred Indian sources
        self.indian_sources = [
            'the-times-of-india', 'the-hindu', 'hindustan-times', 'indian-express',
            'ndtv', 'zee-news', 'india-today', 'news18', 'firstpost', 'the-wire-india',
            'scroll-in', 'livemint', 'economic-times', 'business-standard'
        ]
        
        # Quality keywords for Indian context
        self.quality_keywords = [
            'government', 'policy', 'economy', 'technology', 'innovation', 'research',
            'parliament', 'supreme court', 'rbi', 'ministry', 'infrastructure',
            'education', 'healthcare', 'agriculture', 'defence', 'diplomacy'
        ]

    def get_ndtv_category(self, category: Optional[str] = None, page_size: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Fetch NDTV category if NDTV API is enabled."""
        if not self.ndtv_client or not getattr(self.ndtv_client, 'enabled', False):
            return False, None, 'NDTV disabled'
        try:
            success, items, error = self.ndtv_client.fetch_category(category=category or 'latest', limit=page_size)
            if success and items:
                # Apply our quality filter lightly (no location penalty)
                filtered = self._filter_and_prioritize_articles(items, location='india')
                return True, filtered[:page_size], None
            return success, items, error
        except Exception as e:
            logger.warning(f"NDTV category fetch failed: {e}")
            return False, None, str(e)
    
    def get_ndtv_comprehensive(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Fetch comprehensive NDTV news from all endpoints (general, sports, cities)."""
        if not self.ndtv_client or not getattr(self.ndtv_client, 'enabled', False):
            return False, None, 'NDTV disabled'
        try:
            success, items, error = self.ndtv_client.fetch_comprehensive_news(limit=page_size)
            if success and items:
                # Apply our quality filter
                filtered = self._filter_and_prioritize_articles(items, location='india')
                return True, filtered[:page_size], None
            return success, items, error
        except Exception as e:
            logger.warning(f"NDTV comprehensive fetch failed: {e}")
            return False, None, str(e)
    
    def get_ndtv_sports(self, sports: List[str] = None, page_size: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Fetch NDTV sports news including cricket updates."""
        if not self.ndtv_client or not getattr(self.ndtv_client, 'enabled', False):
            return False, None, 'NDTV disabled'
        try:
            success, items, error = self.ndtv_client.fetch_sports_news(sports=sports or ['cricket', 'football'], limit=page_size)
            if success and items:
                # Apply our quality filter
                filtered = self._filter_and_prioritize_articles(items, location='india')
                return True, filtered[:page_size], None
            return success, items, error
        except Exception as e:
            logger.warning(f"NDTV sports fetch failed: {e}")
            return False, None, str(e)
    
    def get_real_cricket_news(self, page_size: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get real cricket news from NewsAPI with Indian focus."""
        try:
            # Search for cricket news with Indian context
            cricket_queries = [
                'India cricket team',
                'IPL cricket',
                'Indian cricket players',
                'cricket India match',
                'Virat Kohli cricket',
                'cricket tournament India'
            ]
            
            all_cricket_articles = []
            
            for query in cricket_queries:
                success, articles, _ = self.search_articles(
                    query=query, 
                    page_size=page_size//len(cricket_queries)
                )
                if success and articles:
                    # Filter for cricket-specific content
                    cricket_articles = []
                    for article in articles:
                        title = (article.get('title') or '').lower()
                        desc = (article.get('description') or '').lower()
                        content = f"{title} {desc}"
                        
                        # Check if it's really about cricket
                        cricket_keywords = ['cricket', 'ipl', 'test match', 'odi', 't20', 'wicket', 'batting', 'bowling', 'runs', 'over']
                        if any(keyword in content for keyword in cricket_keywords):
                            # Mark as cricket category
                            article['category'] = 'cricket'
                            cricket_articles.append(article)
                    
                    all_cricket_articles.extend(cricket_articles)
            
            if all_cricket_articles:
                # Deduplicate by title
                seen = set()
                unique_articles = []
                for article in all_cricket_articles:
                    title = article.get('title', '').strip().lower()
                    if title and title not in seen:
                        seen.add(title)
                        unique_articles.append(article)
                
                # Apply quality filtering with cricket boost
                filtered = self._filter_and_prioritize_articles(unique_articles, location='india')
                logger.info(f"Found {len(filtered)} real cricket articles")
                return True, filtered[:page_size], None
            else:
                return False, None, "No cricket articles found"
                
        except Exception as e:
            logger.error(f"Error fetching real cricket news: {e}")
            return False, None, str(e)
    
    def get_real_sports_news(self, page_size: int = 30) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get real sports news from NewsAPI with focus on Indian sports."""
        try:
            # Search for various sports with Indian context
            sports_queries = [
                'India cricket team match',
                'Indian football league',
                'India Olympics sports',
                'Indian badminton tennis',
                'IPL cricket 2024',
                'India vs cricket match'
            ]
            
            all_sports_articles = []
            
            for query in sports_queries:
                success, articles, _ = self.search_articles(
                    query=query, 
                    page_size=page_size//len(sports_queries)
                )
                if success and articles:
                    # Filter and categorize sports content
                    for article in articles:
                        title = (article.get('title') or '').lower()
                        desc = (article.get('description') or '').lower()
                        content = f"{title} {desc}"
                        
                        # Determine sport category
                        if any(word in content for word in ['cricket', 'ipl', 'test match', 'odi', 't20']):
                            article['category'] = 'cricket'
                        elif any(word in content for word in ['football', 'soccer', 'fifa']):
                            article['category'] = 'football'
                        elif any(word in content for word in ['badminton', 'tennis', 'olympics']):
                            article['category'] = 'other_sports'
                        else:
                            article['category'] = 'sports'
                        
                        all_sports_articles.append(article)
            
            if all_sports_articles:
                # Deduplicate and filter
                seen = set()
                unique_articles = []
                for article in all_sports_articles:
                    title = article.get('title', '').strip().lower()
                    if title and title not in seen:
                        seen.add(title)
                        unique_articles.append(article)
                
                filtered = self._filter_and_prioritize_articles(unique_articles, location='india')
                logger.info(f"Found {len(filtered)} real sports articles")
                return True, filtered[:page_size], None
            else:
                return False, None, "No sports articles found"
                
        except Exception as e:
            logger.error(f"Error fetching real sports news: {e}")
            return False, None, str(e)

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
        
        # Apply quality filtering for better recommendations
        if articles and country == 'in':  # Indian news gets special filtering
            filtered_articles = self._filter_and_prioritize_articles(articles, location='india')
            return True, filtered_articles, None
        
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
        
        # Apply quality filtering for search results
        if articles:
            filtered_articles = self._filter_and_prioritize_articles(articles, location='india')
            return True, filtered_articles, None
        
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

        # Apply quality filtering and Indian focus
        filtered_articles = self._filter_and_prioritize_articles(unique_articles, location='india')
        
        return True, filtered_articles[:page_size], None
    
    def _calculate_quality_score(self, article: Dict[str, Any]) -> float:
        """Calculate quality score for an article based on content analysis."""
        title = (article.get('title') or '').lower()
        description = (article.get('description') or '').lower()
        source_name = (article.get('source', {}).get('name') or '').lower()
        content = f"{title} {description}"
        
        score = 5.0  # Base score
        
        # Penalize clickbait patterns
        for pattern in self.clickbait_patterns:
            if re.search(pattern, content, re.IGNORECASE):
                score -= 2.0
                logger.debug(f"Clickbait pattern found in: {title[:50]}...")
        
        # Boost quality keywords
        quality_matches = sum(1 for keyword in self.quality_keywords if keyword in content)
        score += quality_matches * 0.5
        
        # Boost Indian sources
        source_id = article.get('source', {}).get('id', '')
        if source_id in self.indian_sources or any(indian_src in source_name for indian_src in ['times', 'hindu', 'ndtv', 'zee', 'india']):
            score += 2.0
        
        # Penalize entertainment/celebrity content
        entertainment_keywords = ['celebrity', 'bollywood', 'actor', 'actress', 'film', 'movie', 'gossip', 'viral', 'meme']
        entertainment_matches = sum(1 for keyword in entertainment_keywords if keyword in content)
        if entertainment_matches > 2:
            score -= 3.0
        
        # Boost Indian context keywords
        indian_keywords = ['india', 'indian', 'delhi', 'mumbai', 'bangalore', 'chennai', 'kolkata', 'hyderabad', 'pune', 'modi', 'bjp', 'congress', 'rupee', 'nse', 'bse']
        indian_matches = sum(1 for keyword in indian_keywords if keyword in content)
        score += indian_matches * 0.3
        
        # Boost technology and global affairs
        tech_global_keywords = ['technology', 'ai', 'artificial intelligence', 'startup', 'innovation', 'global', 'international', 'trade', 'economy', 'climate', 'environment']
        tech_matches = sum(1 for keyword in tech_global_keywords if keyword in content)
        score += tech_matches * 0.4
        
        # MAJOR BOOST for cricket and sports content (trending now!)
        cricket_keywords = ['cricket', 'ipl', 'test match', 'odi', 't20', 'wicket', 'batting', 'bowling', 'runs', 'over', 'virat kohli', 'rohit sharma', 'ms dhoni', 'indian cricket']
        cricket_matches = sum(1 for keyword in cricket_keywords if keyword in content)
        if cricket_matches > 0:
            score += 3.0  # Big boost for cricket content
            logger.debug(f"Cricket content boosted: {title[:50]}...")
        
        # Boost other Indian sports
        sports_keywords = ['football', 'badminton', 'tennis', 'hockey', 'olympics', 'asian games', 'commonwealth games']
        sports_matches = sum(1 for keyword in sports_keywords if keyword in content)
        if sports_matches > 0:
            score += 1.5  # Good boost for other sports
        
        # Extra boost if it's categorized as cricket/sports
        category = article.get('category', '').lower()
        if category == 'cricket':
            score += 2.0
        elif category in ['sports', 'football', 'other_sports']:
            score += 1.0
        
        return max(0.0, score)
    
    def _is_recent_article(self, article: Dict[str, Any], hours_threshold: int = 48) -> bool:
        """Check if article is recent (within threshold hours)."""
        try:
            from datetime import datetime, timezone
            published_at = article.get('publishedAt')
            if not published_at:
                return False
            
            # Parse the published date
            pub_date = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
            now = datetime.now(timezone.utc)
            
            # Check if within threshold
            time_diff = (now - pub_date).total_seconds() / 3600  # Convert to hours
            return time_diff <= hours_threshold
        except Exception as e:
            logger.warning(f"Error parsing date for article: {e}")
            return True  # Default to including the article
    
    def _filter_and_prioritize_articles(self, articles: List[Dict[str, Any]], location: str = 'india') -> List[Dict[str, Any]]:
        """Filter and prioritize articles based on quality and relevance."""
        if not articles:
            return articles
        
        # Calculate scores and filter
        scored_articles = []
        for article in articles:
            # Skip articles without title or description
            if not article.get('title') or not article.get('description'):
                continue
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(article)
            
            # Only include articles with decent quality score
            if quality_score >= 3.0:
                # Add recency boost
                if self._is_recent_article(article, 24):  # Within 24 hours
                    quality_score += 1.0
                elif self._is_recent_article(article, 48):  # Within 48 hours
                    quality_score += 0.5
                
                scored_articles.append((quality_score, article))
        
        # Sort by score (highest first)
        scored_articles.sort(key=lambda x: x[0], reverse=True)
        
        # Return articles without scores
        filtered_articles = [article for score, article in scored_articles]
        
        logger.info(f"Filtered {len(articles)} articles down to {len(filtered_articles)} quality articles")
        return filtered_articles
    
    def get_indian_recommendations(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get high-quality Indian news recommendations with GNews as primary source."""
        try:
            # PRIORITY 1: Try GNews comprehensive Indian news (best quality, India-focused)
            if self.gnews_service and self.gnews_service.is_available():
                logger.info("🚀 Using GNews API for comprehensive Indian news...")
                success, gnews_articles, error = self.gnews_service.get_comprehensive_indian_news(page_size=page_size)
                
                if success and gnews_articles:
                    logger.info(f"✅ GNews returned {len(gnews_articles)} high-quality Indian articles")
                    # Apply our quality filtering on top of GNews results
                    filtered_articles = self._filter_and_prioritize_articles(gnews_articles, location='india')
                    
                    # Augment with NDTV if we have room and NDTV is available
                    if len(filtered_articles) < page_size and self.ndtv_client:
                        try:
                            remaining_slots = page_size - len(filtered_articles)
                            ok_ndtv, ndtv_items, _ = self.get_ndtv_comprehensive(page_size=remaining_slots)
                            if ok_ndtv and ndtv_items:
                                logger.info(f"🔗 Augmenting with {len(ndtv_items)} NDTV articles")
                                # Merge and deduplicate
                                merged = list(filtered_articles)
                                merged.extend(ndtv_items)
                                seen = set()
                                unique_articles = []
                                for article in merged:
                                    title = article.get('title', '').strip().lower()
                                    if title and title not in seen:
                                        seen.add(title)
                                        unique_articles.append(article)
                                filtered_articles = unique_articles
                        except Exception as e:
                            logger.warning(f"NDTV augmentation failed: {e}")
                    
                    return True, filtered_articles[:page_size], None
                else:
                    logger.warning(f"GNews failed: {error}, falling back to legacy sources")
            
            # FALLBACK: Use legacy NewsAPI + NDTV approach
            logger.info("📰 Falling back to NewsAPI + NDTV approach...")
            all_articles = []
            
            # Get real cricket news (trending now!)
            logger.info("Fetching trending cricket news...")
            cricket_success, cricket_articles, _ = self.get_real_cricket_news(page_size=max(15, page_size//3))
            if cricket_success and cricket_articles:
                logger.info(f"✅ Found {len(cricket_articles)} cricket articles")
                all_articles.extend(cricket_articles)
            
            # Get other real sports news
            sports_success, sports_articles, _ = self.get_real_sports_news(page_size=max(10, page_size//4))
            if sports_success and sports_articles:
                logger.info(f"✅ Found {len(sports_articles)} sports articles")
                all_articles.extend(sports_articles)
            
            # Get Indian headlines
            success, indian_articles, error = self.get_top_headlines(country='in', page_size=page_size//2)
            
            if not success or not indian_articles:
                logger.warning("Failed to get Indian headlines, falling back to search")
                # Fallback to searching for Indian topics
                indian_topics = ['India government', 'Indian technology', 'Indian economy', 'Indian policy']
                
                for topic in indian_topics:
                    success, articles, _ = self.search_articles(query=topic, page_size=page_size//len(indian_topics)//2)
                    if success and articles:
                        all_articles.extend(articles)
                
                if all_articles:
                    # Deduplicate
                    seen = set()
                    unique_articles = []
                    for article in all_articles:
                        title = article.get('title', '').strip().lower()
                        if title and title not in seen:
                            seen.add(title)
                            unique_articles.append(article)
                    
                    # Try augment with NDTV even in fallback
                    try:
                        ok_ndtv, ndtv_items, _ = self.get_ndtv_category('india', page_size=max(10, page_size//3))
                    except Exception:
                        ok_ndtv, ndtv_items = False, None
                    if ok_ndtv and ndtv_items:
                        unique_articles.extend(ndtv_items)
                        # Deduplicate again
                        seen = set()
                        deduped = []
                        for a in unique_articles:
                            t = (a.get('title') or '').strip().lower()
                            if t and t not in seen:
                                seen.add(t)
                                deduped.append(a)
                        unique_articles = deduped
                    
                    filtered_articles = self._filter_and_prioritize_articles(unique_articles, location='india')
                    return True, filtered_articles[:page_size], None
                else:
                    return False, None, "Unable to fetch Indian news"
            
            # If we did get Indian headlines, try merging comprehensive NDTV to improve diversity and include sports/cricket
            merged = list(indian_articles)
            try:
                # Use comprehensive NDTV to get general, sports (cricket!), and city news
                ok_ndtv, ndtv_items, _ = self.get_ndtv_comprehensive(page_size=max(15, page_size//2))
            except Exception:
                ok_ndtv, ndtv_items = False, None
            if ok_ndtv and ndtv_items:
                logger.info(f"Adding {len(ndtv_items)} comprehensive NDTV articles (includes cricket & city news)")
                merged.extend(ndtv_items)
                # Deduplicate by title
                seen = set()
                unique_articles = []
                for article in merged:
                    title = article.get('title', '').strip().lower()
                    if title and title not in seen:
                        seen.add(title)
                        unique_articles.append(article)
                merged = unique_articles
            
            # Apply quality filter one more time and cap size
            final_articles = self._filter_and_prioritize_articles(merged, location='india')
            return True, final_articles[:page_size], None
            
        except Exception as e:
            logger.error(f"Error getting Indian recommendations: {e}")
            return False, None, str(e)

    def get_gnews_headlines(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get Indian headlines using GNews API as primary source."""
        if self.gnews_service and self.gnews_service.is_available():
            logger.info("🚀 Fetching Indian headlines from GNews...")
            success, articles, error = self.gnews_service.get_indian_headlines(page_size=page_size)
            
            if success and articles:
                # Apply our quality filtering
                filtered_articles = self._filter_and_prioritize_articles(articles, location='india')
                logger.info(f"✅ GNews headlines: {len(filtered_articles)} quality articles")
                return True, filtered_articles, None
            else:
                logger.warning(f"GNews headlines failed: {error}")
        
        # Fallback to NewsAPI
        logger.info("📰 Falling back to NewsAPI for headlines...")
        return self.get_top_headlines(country='in', page_size=page_size)

    def get_gnews_cricket_news(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get cricket news using GNews API as primary source."""
        if self.gnews_service and self.gnews_service.is_available():
            logger.info("🏏 Fetching cricket news from GNews...")
            success, articles, error = self.gnews_service.get_cricket_news(page_size=page_size)
            
            if success and articles:
                # Apply our quality filtering with cricket boost
                filtered_articles = self._filter_and_prioritize_articles(articles, location='india')
                logger.info(f"✅ GNews cricket: {len(filtered_articles)} quality articles")
                return True, filtered_articles, None
            else:
                logger.warning(f"GNews cricket failed: {error}")
        
        # Fallback to NewsAPI cricket search
        logger.info("📰 Falling back to NewsAPI for cricket...")
        return self.get_real_cricket_news(page_size=page_size)

    def get_gnews_tech_news(self, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Get technology/startup news using GNews API as primary source."""
        if self.gnews_service and self.gnews_service.is_available():
            logger.info("💻 Fetching tech/startup news from GNews...")
            success, articles, error = self.gnews_service.get_startup_tech_news(page_size=page_size)
            
            if success and articles:
                # Apply our quality filtering with tech boost
                filtered_articles = self._filter_and_prioritize_articles(articles, location='india')
                logger.info(f"✅ GNews tech: {len(filtered_articles)} quality articles")
                return True, filtered_articles, None
            else:
                logger.warning(f"GNews tech failed: {error}")
        
        # Fallback to NewsAPI search
        logger.info("📰 Falling back to NewsAPI for tech news...")
        return self.search_articles(query="Indian technology startups", page_size=page_size)

    def search_gnews_articles(self, query: str, page_size: int = 50) -> Tuple[bool, Optional[List[Dict[str, Any]]], Optional[str]]:
        """Search articles using GNews API as primary source."""
        if self.gnews_service and self.gnews_service.is_available():
            logger.info(f"🔍 Searching GNews for: {query}")
            success, articles, error = self.gnews_service.search_indian_news(query, page_size=page_size)
            
            if success and articles:
                # Apply our quality filtering
                filtered_articles = self._filter_and_prioritize_articles(articles, location='india')
                logger.info(f"✅ GNews search: {len(filtered_articles)} quality articles")
                return True, filtered_articles, None
            else:
                logger.warning(f"GNews search failed: {error}")
        
        # Fallback to NewsAPI search
        logger.info("📰 Falling back to NewsAPI for search...")
        return self.search_articles(query=query, page_size=page_size)
