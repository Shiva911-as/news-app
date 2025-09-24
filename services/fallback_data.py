"""
Fallback data for when News API is not available
"""

from datetime import datetime, timedelta
import random

# Sample news articles for fallback
FALLBACK_ARTICLES = [
    {
        "title": "Breaking: Major Tech Company Announces Revolutionary AI Breakthrough",
        "description": "A leading technology company has unveiled a groundbreaking artificial intelligence system that promises to transform various industries.",
        "url": "https://example.com/tech-ai-breakthrough",
        "urlToImage": "https://via.placeholder.com/400x200?text=AI+News",
        "publishedAt": (datetime.now() - timedelta(hours=2)).isoformat(),
        "source": {"name": "Tech News Daily"},
        "author": "Tech Reporter",
        "content": "This is a sample article about AI breakthrough..."
    },
    {
        "title": "Global Climate Summit Reaches Historic Agreement",
        "description": "World leaders have reached a consensus on new climate policies that could significantly impact global warming efforts.",
        "url": "https://example.com/climate-summit",
        "urlToImage": "https://via.placeholder.com/400x200?text=Climate+News",
        "publishedAt": (datetime.now() - timedelta(hours=4)).isoformat(),
        "source": {"name": "Environmental Times"},
        "author": "Climate Correspondent",
        "content": "This is a sample article about climate agreement..."
    },
    {
        "title": "Sports: Championship Finals Set for This Weekend",
        "description": "The most anticipated sporting event of the year is scheduled for this weekend with record-breaking ticket sales.",
        "url": "https://example.com/sports-championship",
        "urlToImage": "https://via.placeholder.com/400x200?text=Sports+News",
        "publishedAt": (datetime.now() - timedelta(hours=6)).isoformat(),
        "source": {"name": "Sports Central"},
        "author": "Sports Writer",
        "content": "This is a sample article about sports championship..."
    },
    {
        "title": "Economic Markets Show Strong Recovery Signs",
        "description": "Financial analysts report positive trends in global markets as economic indicators point to sustained growth.",
        "url": "https://example.com/market-recovery",
        "urlToImage": "https://via.placeholder.com/400x200?text=Finance+News",
        "publishedAt": (datetime.now() - timedelta(hours=8)).isoformat(),
        "source": {"name": "Financial Tribune"},
        "author": "Market Analyst",
        "content": "This is a sample article about market recovery..."
    },
    {
        "title": "Healthcare Innovation: New Treatment Shows Promise",
        "description": "Medical researchers have developed a new treatment approach that shows significant promise in clinical trials.",
        "url": "https://example.com/healthcare-innovation",
        "urlToImage": "https://via.placeholder.com/400x200?text=Health+News",
        "publishedAt": (datetime.now() - timedelta(hours=10)).isoformat(),
        "source": {"name": "Medical Journal"},
        "author": "Health Reporter",
        "content": "This is a sample article about healthcare innovation..."
    },
    {
        "title": "Space Exploration: Mission to Mars Gets Green Light",
        "description": "Space agency announces approval for ambitious Mars exploration mission scheduled for next year.",
        "url": "https://example.com/mars-mission",
        "urlToImage": "https://via.placeholder.com/400x200?text=Space+News",
        "publishedAt": (datetime.now() - timedelta(hours=12)).isoformat(),
        "source": {"name": "Space Today"},
        "author": "Space Correspondent",
        "content": "This is a sample article about Mars mission..."
    },
    {
        "title": "Entertainment: Blockbuster Movie Breaks Box Office Records",
        "description": "The latest superhero movie has shattered previous box office records in its opening weekend.",
        "url": "https://example.com/blockbuster-movie",
        "urlToImage": "https://via.placeholder.com/400x200?text=Movie+News",
        "publishedAt": (datetime.now() - timedelta(hours=14)).isoformat(),
        "source": {"name": "Entertainment Weekly"},
        "author": "Film Critic",
        "content": "This is a sample article about blockbuster movie..."
    },
    {
        "title": "Education: Universities Embrace Digital Learning Revolution",
        "description": "Higher education institutions are rapidly adopting new digital technologies to enhance student learning experiences.",
        "url": "https://example.com/digital-learning",
        "urlToImage": "https://via.placeholder.com/400x200?text=Education+News",
        "publishedAt": (datetime.now() - timedelta(hours=16)).isoformat(),
        "source": {"name": "Education Today"},
        "author": "Education Reporter",
        "content": "This is a sample article about digital learning..."
    },
    {
        "title": "Technology: Quantum Computing Milestone Achieved",
        "description": "Scientists have achieved a significant breakthrough in quantum computing that could revolutionize data processing.",
        "url": "https://example.com/quantum-computing",
        "urlToImage": "https://via.placeholder.com/400x200?text=Quantum+News",
        "publishedAt": (datetime.now() - timedelta(hours=18)).isoformat(),
        "source": {"name": "Science Daily"},
        "author": "Science Writer",
        "content": "This is a sample article about quantum computing..."
    },
    {
        "title": "Business: Startup Unicorn Valued at $10 Billion",
        "description": "A rapidly growing startup has achieved unicorn status with a valuation exceeding $10 billion in latest funding round.",
        "url": "https://example.com/startup-unicorn",
        "urlToImage": "https://via.placeholder.com/400x200?text=Business+News",
        "publishedAt": (datetime.now() - timedelta(hours=20)).isoformat(),
        "source": {"name": "Business Insider"},
        "author": "Business Reporter",
        "content": "This is a sample article about startup valuation..."
    }
]

def get_fallback_articles(page_size: int = 20, category: str = None, query: str = None) -> list:
    """
    Get fallback articles when API is not available
    
    Args:
        page_size: Number of articles to return
        category: Filter by category (optional)
        query: Search query (optional)
    
    Returns:
        List of articles
    """
    articles = FALLBACK_ARTICLES.copy()
    
    # Filter by query if provided
    if query:
        query_lower = query.lower()
        articles = [
            article for article in articles
            if query_lower in article['title'].lower() or 
               query_lower in article['description'].lower()
        ]
    
    # Shuffle for variety
    random.shuffle(articles)
    
    # Return requested number of articles
    return articles[:page_size]

def get_trending_fallback(page_size: int = 20) -> list:
    """Get trending articles fallback"""
    return get_fallback_articles(page_size=page_size)

def search_fallback(query: str, page_size: int = 20) -> list:
    """Search articles fallback"""
    return get_fallback_articles(page_size=page_size, query=query)
