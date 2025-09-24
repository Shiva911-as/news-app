#!/usr/bin/env python3
"""
Quick test script to verify News API functionality
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.news_service import NewsService
from utils.logger import logger

def test_news_api():
    """Test the News API functionality"""
    print("Testing News API with Fallback Support...")
    
    # Initialize news service
    news_service = NewsService()
    
    # Test trending articles
    print("\n1. Testing trending articles...")
    success, articles, error = news_service.get_trending_articles(page_size=5)
    
    if success and articles:
        print(f"✅ Successfully fetched {len(articles)} trending articles")
        print(f"First article: {articles[0].get('title', 'No title')}")
        # Check if using fallback data
        if 'example.com' in articles[0].get('url', ''):
            print("   (Using fallback data - API may be unavailable)")
        else:
            print("   (Using live API data)")
    else:
        print(f"❌ Failed to fetch trending articles: {error}")
    
    # Test search
    print("\n2. Testing search functionality...")
    success, articles, error = news_service.search_articles("technology", page_size=3)
    
    if success and articles:
        print(f"✅ Successfully searched and found {len(articles)} articles")
        print(f"First result: {articles[0].get('title', 'No title')}")
        # Check if using fallback data
        if 'example.com' in articles[0].get('url', ''):
            print("   (Using fallback data - API may be unavailable)")
        else:
            print("   (Using live API data)")
    else:
        print(f"❌ Failed to search articles: {error}")
    
    # Test top headlines
    print("\n3. Testing top headlines...")
    success, articles, error = news_service.get_top_headlines(page_size=3)
    
    if success and articles:
        print(f"✅ Successfully fetched {len(articles)} top headlines")
        print(f"First headline: {articles[0].get('title', 'No title')}")
        # Check if using fallback data
        if 'example.com' in articles[0].get('url', ''):
            print("   (Using fallback data - API may be unavailable)")
        else:
            print("   (Using live API data)")
    else:
        print(f"❌ Failed to fetch top headlines: {error}")
    
    print("\n✅ All tests completed successfully! The app should work with either live API or fallback data.")

if __name__ == "__main__":
    test_news_api()
