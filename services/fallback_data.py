"""
Fallback data for when News API is not available
"""

from datetime import datetime, timedelta
import random

# Sample Indian-focused news articles for fallback
FALLBACK_ARTICLES = [
    {
        "title": "Breaking: PM Modi Announces Major Digital India Initiative",
        "description": "Prime Minister Narendra Modi unveiled a comprehensive digital transformation program aimed at making India a global technology leader.",
        "url": "https://timesofindia.indiatimes.com/india/digital-india",
        "urlToImage": "https://via.placeholder.com/400x200?text=Digital+India",
        "publishedAt": (datetime.now() - timedelta(hours=1)).isoformat(),
        "source": {"name": "Times of India"},
        "author": "Political Correspondent",
        "content": "This is a sample article about Digital India initiative..."
    },
    {
        "title": "Indian Cricket Team Wins Historic Series Against Australia",
        "description": "Team India secured a remarkable victory in the Test series, marking their best performance on Australian soil in decades.",
        "url": "https://www.espncricinfo.com/series/india-tour-of-australia",
        "urlToImage": "https://via.placeholder.com/400x200?text=Cricket+Victory",
        "publishedAt": (datetime.now() - timedelta(hours=3)).isoformat(),
        "source": {"name": "ESPN Cricinfo"},
        "author": "Cricket Correspondent",
        "content": "This is a sample article about India's cricket victory..."
    },
    {
        "title": "Sensex Hits All-Time High as Indian Economy Shows Strong Growth",
        "description": "The BSE Sensex reached a historic milestone crossing 75,000 points driven by robust performance in banking and IT sectors.",
        "url": "https://economictimes.indiatimes.com/markets/stocks/news",
        "urlToImage": "https://via.placeholder.com/400x200?text=Sensex+High",
        "publishedAt": (datetime.now() - timedelta(hours=5)).isoformat(),
        "source": {"name": "Economic Times"},
        "author": "Market Reporter",
        "content": "This is a sample article about Sensex reaching new heights..."
    },
    {
        "title": "ISRO Successfully Launches Chandrayaan-4 Mission to Moon",
        "description": "India's space agency achieved another milestone with the successful launch of its fourth lunar mission, showcasing indigenous technology.",
        "url": "https://www.ndtv.com/india-news/isro-chandrayaan-mission",
        "urlToImage": "https://via.placeholder.com/400x200?text=ISRO+Mission",
        "publishedAt": (datetime.now() - timedelta(hours=7)).isoformat(),
        "source": {"name": "NDTV"},
        "author": "Science Reporter",
        "content": "This is a sample article about ISRO's lunar mission..."
    },
    {
        "title": "Healthcare Innovation: New Treatment Shows Promise",
        "description": "Medical researchers have developed a new treatment approach that shows significant promise in clinical trials.",
        "url": "https://www.medicalnewstoday.com/articles/healthcare-innovation-india-2024",
        "urlToImage": "https://via.placeholder.com/400x200?text=Health+News",
        "publishedAt": (datetime.now() - timedelta(hours=10)).isoformat(),
        "source": {"name": "Medical Journal"},
        "author": "Health Reporter",
        "content": "This is a sample article about healthcare innovation..."
    },
    {
        "title": "Space Exploration: Mission to Mars Gets Green Light",
        "description": "Space agency announces approval for ambitious Mars exploration mission scheduled for next year.",
        "url": "https://www.space.com/india-mars-mission-2024-announcement",
        "urlToImage": "https://via.placeholder.com/400x200?text=Space+News",
        "publishedAt": (datetime.now() - timedelta(hours=12)).isoformat(),
        "source": {"name": "Space Today"},
        "author": "Space Correspondent",
        "content": "This is a sample article about Mars mission..."
    },
    {
        "title": "Entertainment: Blockbuster Movie Breaks Box Office Records",
        "description": "The latest superhero movie has shattered previous box office records in its opening weekend.",
        "url": "https://www.hollywoodreporter.com/movies/movie-news/blockbuster-box-office-records-2024",
        "urlToImage": "https://via.placeholder.com/400x200?text=Movie+News",
        "publishedAt": (datetime.now() - timedelta(hours=14)).isoformat(),
        "source": {"name": "Entertainment Weekly"},
        "author": "Film Critic",
        "content": "This is a sample article about blockbuster movie..."
    },
    {
        "title": "Education: Universities Embrace Digital Learning Revolution",
        "description": "Higher education institutions are rapidly adopting new digital technologies to enhance student learning experiences.",
        "url": "https://www.educationtimes.com/universities-digital-learning-revolution-2024",
        "urlToImage": "https://via.placeholder.com/400x200?text=Education+News",
        "publishedAt": (datetime.now() - timedelta(hours=16)).isoformat(),
        "source": {"name": "Education Today"},
        "author": "Education Reporter",
        "content": "This is a sample article about digital learning..."
    },
    {
        "title": "Technology: Quantum Computing Milestone Achieved",
        "description": "Scientists have achieved a significant breakthrough in quantum computing that could revolutionize data processing.",
        "url": "https://www.sciencedaily.com/releases/2024/10/quantum-computing-breakthrough.htm",
        "urlToImage": "https://via.placeholder.com/400x200?text=Quantum+News",
        "publishedAt": (datetime.now() - timedelta(hours=18)).isoformat(),
        "source": {"name": "Science Daily"},
        "author": "Science Writer",
        "content": "This is a sample article about quantum computing..."
    },
    {
        "title": "Business: Startup Unicorn Valued at $10 Billion",
        "description": "A rapidly growing startup has achieved unicorn status with a valuation exceeding $10 billion in latest funding round.",
        "url": "https://yourstory.com/2024/10/startup-unicorn-billion-valuation-funding",
        "urlToImage": "https://via.placeholder.com/400x200?text=Business+News",
        "publishedAt": (datetime.now() - timedelta(hours=20)).isoformat(),
        "author": "Business Reporter",
        "content": "This is a sample article about startup valuation..."
    }
]

def get_category_specific_articles(category: str, page_size: int = 20) -> list:
    """Get category-specific fallback articles"""
    
    # Generate recent timestamps
    now = datetime.now()
    recent_times = [
        (now - timedelta(hours=2)).isoformat() + 'Z',
        (now - timedelta(hours=5)).isoformat() + 'Z', 
        (now - timedelta(hours=8)).isoformat() + 'Z',
        (now - timedelta(hours=12)).isoformat() + 'Z',
        (now - timedelta(hours=18)).isoformat() + 'Z'
    ]
    
    category_articles = {
        'business': [
            {
                "title": "Indian Stock Market Hits New High as Sensex Crosses 75,000",
                "description": "The BSE Sensex reached a historic milestone today, crossing 75,000 points driven by strong performance in banking and IT sectors.",
                "source": {"name": "Economic Times"},
                "publishedAt": recent_times[0],
                "url": "https://economictimes.indiatimes.com/markets/stocks/news/sensex-hits-new-high/articleshow/104567890.cms",
                "author": "Market Reporter"
            },
            {
                "title": "RBI Announces New Digital Currency Pilot Program",
                "description": "Reserve Bank of India launches expanded digital rupee trials across major cities, targeting retail transactions.",
                "source": {"name": "Business Standard"},
                "publishedAt": recent_times[1],
                "url": "https://www.business-standard.com/economy/news/rbi-digital-currency-pilot-program-123456789.html",
                "author": "Banking Correspondent"
            },
            {
                "title": "Startup Funding in India Reaches $12 Billion in 2024",
                "description": "Indian startups raised record funding this year, with fintech and edtech leading the investment surge.",
                "source": {"name": "Mint"},
                "publishedAt": recent_times[2],
                "url": "https://www.livemint.com/companies/start-ups/startup-funding-india-2024-123456789.html",
                "author": "Startup Reporter"
            }
        ],
        'sports': [
            {
                "title": "India Defeats Australia by 6 Wickets in Melbourne Test",
                "description": "Virat Kohli's century leads India to a commanding victory in the Boxing Day Test at MCG.",
                "source": {"name": "Cricbuzz"},
                "publishedAt": recent_times[0],
                "url": "https://www.cricbuzz.com/cricket-news/123456/india-defeats-australia-melbourne-test",
                "author": "Cricket Reporter"
            },
            {
                "title": "IPL 2025 Auction: Mumbai Indians Acquire Star Players",
                "description": "Mumbai Indians make strategic picks in the IPL mega auction, focusing on young Indian talent.",
                "source": {"name": "ESPN Cricinfo"},
                "publishedAt": recent_times[1],
                "url": "https://www.espncricinfo.com/story/ipl-2025-auction-mumbai-indians-123456789",
                "author": "IPL Correspondent"
            },
            {
                "title": "Indian Football Team Qualifies for Asian Cup Finals",
                "description": "Blue Tigers secure their spot in the Asian Cup final after defeating South Korea 2-1.",
                "source": {"name": "Goal.com"},
                "publishedAt": recent_times[2],
                "url": "https://www.goal.com/en-in/news/india-football-asian-cup-finals-123456789",
                "author": "Football Reporter"
            }
        ],
        'entertainment': [
            {
                "title": "Shah Rukh Khan's New Film Breaks Box Office Records",
                "description": "The Bollywood superstar's latest release earns ₹100 crores in its opening weekend.",
                "source": {"name": "BollywoodHungama"},
                "publishedAt": recent_times[0],
                "url": "https://www.bollywoodhungama.com/news/bollywood/shah-rukh-khan-film-box-office-123456789",
                "author": "Entertainment Reporter"
            },
            {
                "title": "Netflix Announces 10 New Indian Original Series",
                "description": "Streaming giant reveals ambitious slate of regional content across multiple Indian languages.",
                "source": {"name": "Variety India"},
                "publishedAt": recent_times[1],
                "url": "https://variety.com/2024/tv/news/netflix-indian-original-series-123456789",
                "author": "Streaming Correspondent"
            },
            {
                "title": "Cannes Film Festival to Feature Indian Cinema Section",
                "description": "Prestigious film festival announces dedicated showcase for contemporary Indian filmmakers.",
                "source": {"name": "Film Companion"},
                "publishedAt": recent_times[2],
                "url": "https://www.filmcompanion.in/news/cannes-film-festival-indian-cinema-123456789",
                "author": "Film Critic"
            }
        ],
        'technology': [
            {
                "title": "Indian AI Startup Raises $50 Million Series B Funding",
                "description": "Bangalore-based artificial intelligence company secures major funding round from global investors.",
                "source": {"name": "TechCrunch India"},
                "publishedAt": recent_times[0],
                "url": "https://techcrunch.com/2024/10/06/indian-ai-startup-funding-series-b/",
                "author": "Tech Reporter"
            },
            {
                "title": "India Launches World's Largest 5G Network Rollout",
                "description": "Government announces nationwide 5G deployment covering 1000+ cities by end of 2025.",
                "source": {"name": "Gadgets360"},
                "publishedAt": recent_times[1],
                "url": "https://www.gadgets360.com/telecom/news/india-5g-network-rollout-2024-123456789",
                "author": "Telecom Correspondent"
            },
            {
                "title": "ISRO Successfully Launches Chandrayaan-4 Mission",
                "description": "Indian Space Research Organisation's lunar mission aims to establish permanent research station.",
                "source": {"name": "Space India"},
                "publishedAt": recent_times[2],
                "url": "https://www.isro.gov.in/chandrayaan-4-mission-launch-success",
                "author": "Space Reporter"
            }
        ],
        'politics': [
            {
                "title": "Parliament Passes Digital India Act 2025",
                "description": "New legislation aims to regulate digital platforms and protect user privacy rights.",
                "source": {"name": "The Hindu"},
                "publishedAt": recent_times[0],
                "url": "https://www.thehindu.com/news/national/parliament-digital-india-act-2025/article123456789.ece",
                "author": "Political Correspondent"
            },
            {
                "title": "PM Modi Announces New Infrastructure Development Plan",
                "description": "₹10 lakh crore investment approved for roads, rails, and digital infrastructure.",
                "source": {"name": "Times of India"},
                "publishedAt": recent_times[1],
                "url": "https://timesofindia.indiatimes.com/india/pm-modi-infrastructure-development-plan/articleshow/123456789.cms",
                "author": "Government Reporter"
            },
            {
                "title": "Election Commission Announces Assembly Poll Dates",
                "description": "Five state assemblies to go to polls in March 2025, EC announces detailed schedule.",
                "source": {"name": "Indian Express"},
                "publishedAt": recent_times[2],
                "url": "https://indianexpress.com/article/india/election-commission-assembly-poll-dates-2025-123456789/",
                "author": "Election Correspondent"
            }
        ]
    }
    
    articles = category_articles.get(category, [])
    return articles[:page_size]

def get_fallback_articles(page_size: int = 20, query: str = None) -> list:
    """
    Get fallback articles when API is not available
    
    Args:
        page_size: Number of articles to return
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
    """Get Indian trending articles fallback"""
    # Generate recent timestamps for trending content
    now = datetime.now()
    recent_times = [
        (now - timedelta(minutes=30)).isoformat() + 'Z',
        (now - timedelta(hours=1)).isoformat() + 'Z',
        (now - timedelta(hours=2)).isoformat() + 'Z',
        (now - timedelta(hours=4)).isoformat() + 'Z',
        (now - timedelta(hours=6)).isoformat() + 'Z'
    ]
    
    # Indian trending topics
    indian_trending = [
        {
            "title": "🔥 Breaking: India Wins Historic Cricket World Cup Final",
            "description": "Team India defeats Australia in a thrilling final match, bringing the World Cup home after years of anticipation.",
            "source": {"name": "ESPN Cricinfo"},
            "publishedAt": recent_times[0],
            "url": "https://www.espncricinfo.com/series/cricket-world-cup",
            "author": "Cricket Correspondent"
        },
        {
            "title": "🚀 ISRO Creates History with Successful Mars Mission Landing",
            "description": "India becomes the fourth country to successfully land on Mars, showcasing indigenous space technology capabilities.",
            "source": {"name": "NDTV"},
            "publishedAt": recent_times[1],
            "url": "https://www.ndtv.com/india-news/isro-mars-mission",
            "author": "Space Reporter"
        },
        {
            "title": "📈 Indian Startup Becomes Unicorn with $1 Billion Valuation",
            "description": "Bangalore-based fintech startup achieves unicorn status, marking another milestone for India's startup ecosystem.",
            "source": {"name": "Economic Times"},
            "publishedAt": recent_times[2],
            "url": "https://economictimes.indiatimes.com/tech/startups",
            "author": "Startup Reporter"
        },
        {
            "title": "🏛️ Parliament Passes Landmark Digital Privacy Bill",
            "description": "Lok Sabha approves comprehensive data protection legislation, strengthening digital rights for Indian citizens.",
            "source": {"name": "Times of India"},
            "publishedAt": recent_times[3],
            "url": "https://timesofindia.indiatimes.com/india/parliament-news",
            "author": "Political Correspondent"
        },
        {
            "title": "🎬 Bollywood Film Breaks Box Office Records Worldwide",
            "description": "Latest Indian blockbuster achieves unprecedented global success, earning ₹500 crores in opening weekend.",
            "source": {"name": "India Today"},
            "publishedAt": recent_times[4],
            "url": "https://www.indiatoday.in/movies/bollywood",
            "author": "Entertainment Reporter"
        }
    ]
    
    return indian_trending[:page_size]

def search_fallback(query: str, page_size: int = 20) -> list:
    """Search articles fallback"""
    return get_fallback_articles(page_size=page_size, query=query)
