import json
import os
from typing import Dict, List, Optional, Tuple
from datetime import datetime
from utils.logger import logger
from config import get_config

class UserProfile:
    """User profile management with learning capabilities"""
    
    def __init__(self, user_id: str = "default"):
        self.config = get_config()
        self.user_id = user_id
        self.profile_file = f"user_profiles/{user_id}_profile.json"
        self.interests: Dict[str, float] = {}
        self.read_history: List[Dict[str, any]] = []
        self.last_updated: Optional[str] = None
        
        self._load_profile()
        self._ensure_related_topics()
    
    def _load_profile(self) -> None:
        """Load user profile from file"""
        try:
            if os.path.exists(self.profile_file):
                with open(self.profile_file, 'r') as f:
                    data = json.load(f)
                    self.interests = data.get('interests', {})
                    self.read_history = data.get('read_history', [])
                    self.last_updated = data.get('last_updated')
                    logger.info(f"Loaded profile for user {self.user_id}")
            else:
                logger.info(f"Creating new profile for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error loading profile: {e}")
            self.interests = {}
            self.read_history = []
    
    def _save_profile(self) -> None:
        """Save user profile to file"""
        try:
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.profile_file), exist_ok=True)
            
            data = {
                'user_id': self.user_id,
                'interests': self.interests,
                'read_history': self.read_history[-100:],  # Keep last 100 articles
                'last_updated': datetime.now().isoformat()
            }
            
            with open(self.profile_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            self.last_updated = data['last_updated']
            logger.info(f"Saved profile for user {self.user_id}")
        except Exception as e:
            logger.error(f"Error saving profile: {e}")
    
    def _ensure_related_topics(self) -> None:
        """Ensure related topics are included in user profile"""
        for main_topic, related_topics in self.config.RELATED_TOPICS.items():
            # Add main topic if not present
            if main_topic not in self.interests:
                self.interests[main_topic] = 0.0
            
            # Add related topics if not present
            for topic in related_topics:
                if topic not in self.interests:
                    self.interests[topic] = 0.0
    
    def set_interests(self, topics: List[str]) -> None:
        """
        Set user interests
        
        Args:
            topics: List of topic strings
        """
        # Reset interests
        self.interests = {}
        
        # Add new interests
        for topic in topics:
            clean_topic = topic.strip().lower()
            if clean_topic:
                self.interests[clean_topic] = self.config.DEFAULT_TOPIC_WEIGHT
        
        # Ensure related topics are included
        self._ensure_related_topics()
        
        # Save profile
        self._save_profile()
        logger.info(f"Updated interests for user {self.user_id}: {list(self.interests.keys())}")
    
    def add_interest(self, topic: str, weight: float = None) -> None:
        """
        Add or update interest weight
        
        Args:
            topic: Topic to add/update
            weight: Weight for the topic (optional)
        """
        clean_topic = topic.strip().lower()
        if clean_topic:
            if weight is None:
                weight = self.config.DEFAULT_TOPIC_WEIGHT
            
            self.interests[clean_topic] = weight
            self._save_profile()
            logger.info(f"Added interest '{clean_topic}' with weight {weight}")
    
    def learn_from_article(self, article: Dict[str, any]) -> None:
        """
        Learn from user reading an article
        
        Args:
            article: Article data
        """
        title = (article.get('title') or "").lower()
        description = (article.get('description') or "").lower()
        content = f"{title} {description}"
        
        # Record reading history
        self.read_history.append({
            'title': article.get('title'),
            'url': article.get('url'),
            'published_at': article.get('publishedAt'),
            'read_at': datetime.now().isoformat()
        })
        
        # Update topic weights based on content
        for topic, related_topics in self.config.RELATED_TOPICS.items():
            if topic in content:
                # Increase weight for main topic
                self.interests[topic] = self.interests.get(topic, 0) + self.config.LEARNING_RATE
                
                # Increase weight for related topics
                for related_topic in related_topics:
                    if related_topic in content:
                        self.interests[related_topic] = self.interests.get(related_topic, 0) + self.config.LEARNING_RATE
        
        # Also check for any other topics in content
        for topic in self.interests:
            if topic in content and topic not in [t for topics in self.config.RELATED_TOPICS.values() for t in topics]:
                self.interests[topic] = self.interests.get(topic, 0) + self.config.LEARNING_RATE
        
        self._save_profile()
        logger.info(f"Learned from article: {article.get('title', 'Unknown')}")
    
    def get_top_interests(self, limit: int = 10) -> List[Tuple[str, float]]:
        """
        Get top interests by weight
        
        Args:
            limit: Maximum number of interests to return
            
        Returns:
            List of (topic, weight) tuples sorted by weight
        """
        sorted_interests = sorted(
            self.interests.items(), 
            key=lambda x: x[1], 
            reverse=True
        )
        return sorted_interests[:limit]
    
    def score_article(self, article: Dict[str, any]) -> float:
        """
        Enhanced scoring for articles based on user interests and quality
        
        Args:
            article: Article data
            
        Returns:
            Relevance score
        """
        title = (article.get('title') or "").lower()
        description = (article.get('description') or "").lower()
        source_name = (article.get('source', {}).get('name') or "").lower()
        content = f"{title} {description}"
        
        score = 0.0
        
        # Base scoring from user interests
        for topic, weight in self.interests.items():
            if topic in content:
                score += weight
        
        # Boost for Indian context (since user is based in India)
        indian_indicators = ['india', 'indian', 'delhi', 'mumbai', 'bangalore', 'modi', 'rupee', 'parliament']
        indian_matches = sum(1 for indicator in indian_indicators if indicator in content)
        score += indian_matches * 0.5
        
        # Boost for technology and global affairs (user preferences)
        tech_global_keywords = ['technology', 'ai', 'startup', 'innovation', 'global', 'international', 'climate', 'economy']
        tech_matches = sum(1 for keyword in tech_global_keywords if keyword in content)
        score += tech_matches * 0.4
        
        # Penalize entertainment/celebrity content
        entertainment_keywords = ['celebrity', 'bollywood', 'gossip', 'viral', 'scandal']
        entertainment_matches = sum(1 for keyword in entertainment_keywords if keyword in content)
        score -= entertainment_matches * 1.0
        
        # Boost for quality sources
        quality_sources = ['times', 'hindu', 'economic', 'mint', 'wire', 'scroll', 'firstpost']
        if any(source in source_name for source in quality_sources):
            score += 1.0
        
        return max(0.0, score)
    
    def get_recommendations(self, articles: List[Dict[str, any]], limit: int = 10) -> List[Tuple[float, Dict[str, any]]]:
        """
        Get personalized article recommendations
        
        Args:
            articles: List of articles to score
            limit: Maximum number of recommendations
            
        Returns:
            List of (score, article) tuples sorted by score
        """
        scored_articles = []
        
        for article in articles:
            score = self.score_article(article)
            if score > 0:
                scored_articles.append((score, article))
        
        # Sort by score (highest first)
        scored_articles.sort(key=lambda x: x[0], reverse=True)
        
        return scored_articles[:limit]
    
    def get_profile_summary(self) -> Dict[str, any]:
        """
        Get profile summary
        
        Returns:
            Profile summary dictionary
        """
        return {
            'user_id': self.user_id,
            'total_interests': len(self.interests),
            'top_interests': self.get_top_interests(5),
            'articles_read': len(self.read_history),
            'last_updated': self.last_updated
        }
    
    def initialize_indian_user_preferences(self) -> None:
        """Initialize profile with Indian-focused interests for new users."""
        if not self.interests or len(self.interests) == 0:
            # Set default Indian-focused interests
            default_interests = {
                'indian_politics': 2.0,
                'indian_economy': 2.0,
                'technology': 2.5,
                'global_affairs': 2.0,
                'indian_regional': 1.5,
                'science_research': 1.5,
                'infrastructure': 1.0,
                'education': 1.0
            }
            
            self.interests.update(default_interests)
            self._ensure_related_topics()
            self._save_profile()
            logger.info(f"Initialized Indian user preferences for {self.user_id}")
    
    def get_indian_focused_recommendations(self, articles: List[Dict[str, any]], limit: int = 10) -> List[Tuple[float, Dict[str, any]]]:
        """
        Get recommendations with enhanced Indian focus and quality filtering.
        
        Args:
            articles: List of articles to score
            limit: Maximum number of recommendations
            
        Returns:
            List of (score, article) tuples sorted by relevance
        """
        # Ensure user has Indian preferences
        self.initialize_indian_user_preferences()
        
        scored_articles = []
        seen_titles = set()
        
        for article in articles:
            # Skip duplicates
            title = (article.get('title') or '').strip().lower()
            if title in seen_titles or not title:
                continue
            seen_titles.add(title)
            
            # Skip articles without proper content
            if not article.get('description'):
                continue
            
            score = self.score_article(article)
            
            # Only include articles with meaningful scores
            if score > 0.5:
                scored_articles.append((score, article))
        
        # Sort by score (highest first)
        scored_articles.sort(key=lambda x: x[0], reverse=True)
        
        logger.info(f"Generated {len(scored_articles)} Indian-focused recommendations from {len(articles)} articles")
        return scored_articles[:limit]
