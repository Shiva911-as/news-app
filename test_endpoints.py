#!/usr/bin/env python3
"""
Test the Flask API endpoints
"""

import requests
import json
import time

BASE_URL = "http://127.0.0.1:5000"

def test_endpoint(endpoint, description):
    """Test a single endpoint"""
    print(f"\n🔍 Testing {description}...")
    try:
        response = requests.get(f"{BASE_URL}{endpoint}", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success', True):  # Some endpoints don't have 'success' field
                print(f"✅ {description} - SUCCESS")
                if 'articles' in data:
                    print(f"   📰 Found {len(data['articles'])} articles")
                    if data['articles']:
                        print(f"   📝 First article: {data['articles'][0].get('title', 'No title')[:60]}...")
                elif 'recommendations' in data:
                    print(f"   🎯 Found {len(data['recommendations'])} recommendations")
                elif 'message' in data:
                    print(f"   💬 Message: {data['message']}")
                return True
            else:
                print(f"❌ {description} - API Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ {description} - HTTP {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {description} - Connection failed (is the server running?)")
        return False
    except Exception as e:
        print(f"❌ {description} - Error: {e}")
        return False

def main():
    """Test all endpoints"""
    print("🚀 Testing News App API Endpoints...")
    print(f"🌐 Base URL: {BASE_URL}")
    
    # Wait a moment for server to be ready
    time.sleep(2)
    
    endpoints = [
        ("/", "Root endpoint"),
        ("/api/news/trending", "Trending news"),
        ("/api/news/search?q=technology", "Search news"),
        ("/api/news/topic/sports", "Topic news"),
        ("/api/recommendations", "Recommendations"),
        ("/api/profile", "User profile"),
    ]
    
    results = []
    for endpoint, description in endpoints:
        success = test_endpoint(endpoint, description)
        results.append((description, success))
    
    # Summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY")
    print("="*50)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for description, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {description}")
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The news app is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the logs above for details.")

if __name__ == "__main__":
    main()
