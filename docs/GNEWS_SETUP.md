# GNews API Integration Setup

## Overview

We've successfully integrated **GNews API** as the primary source for India-focused news content. GNews provides cleaner, more structured results with better signal-to-noise ratio compared to general-purpose news APIs.

## Key Benefits

✅ **India-Specific Content**: Filter by `country=in` for relevant Indian news  
✅ **Clean Results**: No unrelated global noise  
✅ **Better Quality**: Structured data from reliable sources  
✅ **Topic Targeting**: Search specific topics like "startups", "ISRO", "elections"  
✅ **Fallback System**: Automatic fallback to NewsAPI/NDTV if GNews fails  

## API Endpoints Enhanced

The following endpoints now use GNews as primary source:

- `/api/news/trending` - Indian headlines with GNews priority
- `/api/news/search` - Search with Indian context
- `/api/news/cricket` - Cricket news with Indian focus
- `/api/news/technology` - **NEW** Tech/startup news endpoint
- `/api/recommendations` - Enhanced recommendations with GNews data

## Environment Variables

### Required for Production

```bash
# GNews API Key (Already configured in config.py)
GNEWS_API_KEY=829b731da36e4ad541c16ad9ce12902a

# Optional: Enable/disable GNews (default: true)
GNEWS_ENABLED=true
```

**✅ API Key Status**: Already configured and ready to use!

### Existing Variables (Fallback)

```bash
# NewsAPI key (fallback source)
NEWS_API_KEY=your_newsapi_key_here

# NDTV API (community scraper - optional)
NDTV_API_ENABLED=true
NDTV_BASE_URL=https://ndtvnews-api.herokuapp.com
```

## Setup Instructions

### 1. Get GNews API Key

1. Visit [https://gnews.io/](https://gnews.io/)
2. Sign up for a free account
3. Get your API key from the dashboard
4. Free tier: 100 requests/day

### 2. Configure Environment

**Option A: Environment File (.env)**
```bash
# Add to your .env file
GNEWS_API_KEY=your_actual_api_key_here
GNEWS_ENABLED=true
```

**Option B: System Environment**
```bash
# Windows
set GNEWS_API_KEY=your_actual_api_key_here

# Linux/Mac
export GNEWS_API_KEY=your_actual_api_key_here
```

### 3. Test Integration

Run the test script to verify everything works:

```bash
python test_gnews_integration.py
```

Expected output:
```
🚀 GNews Integration Test Suite
==================================================
Environment: DevelopmentConfig
GNews enabled: True
GNews API key configured: Yes

🧪 Testing GNews Service...
✅ GNews API key configured

📰 Testing Indian headlines...
✅ Got 5 Indian headlines
   1. Latest Indian government policy updates...
   2. Technology sector growth in India...
```

## Usage Examples

### GNews API Endpoints

```bash
# Indian headlines
https://gnews.io/api/v4/top-headlines?lang=en&country=in&token=YOUR_API_KEY

# Search Indian startups
https://gnews.io/api/v4/search?q=startups&lang=en&country=in&token=YOUR_API_KEY

# Search ISRO news
https://gnews.io/api/v4/search?q=ISRO&lang=en&country=in&token=YOUR_API_KEY
```

### Application API Endpoints

```bash
# Get trending Indian news (GNews priority)
GET /api/news/trending?page_size=20

# Search with Indian context
GET /api/news/search?q=startups&page_size=15

# Cricket news with Indian focus
GET /api/news/cricket?page_size=10

# Technology/startup news (NEW)
GET /api/news/technology?page_size=15

# Enhanced recommendations
GET /api/recommendations
```

## Fallback System

The integration includes robust fallback mechanisms:

1. **GNews Primary**: Try GNews API first
2. **NewsAPI Fallback**: If GNews fails, use NewsAPI
3. **NDTV Augmentation**: Add NDTV content for diversity
4. **Static Fallback**: Use cached articles if all APIs fail

## Monitoring

Check logs for source information:

```
🚀 Using GNews API for comprehensive Indian news...
✅ GNews returned 25 high-quality Indian articles
🔗 Augmenting with 10 NDTV articles
```

Response includes source information:
```json
{
  "success": true,
  "articles": [...],
  "source": "gnews",
  "note": "Cricket news with Indian focus - GNews priority!"
}
```

## Rate Limits

- **GNews Free**: 100 requests/day
- **GNews Paid**: Up to 10,000+ requests/day
- **Automatic Rate Limiting**: Built-in 200ms delays between requests
- **Fallback on Limit**: Switches to NewsAPI if rate limit hit

## Quality Improvements

With GNews integration, you get:

✅ **Better Indian Focus**: Country-specific filtering at source  
✅ **Reduced Noise**: Less irrelevant global content  
✅ **Quality Sources**: Curated Indian news sources  
✅ **Structured Data**: Clean, consistent article format  
✅ **Topic Relevance**: Better matching for Indian topics  
✅ **Clean Processing**: Simplified, reliable article transformation  

## Troubleshooting

### GNews Not Working

1. **Check API Key**: Verify `GNEWS_API_KEY` is set correctly
2. **Check Rate Limits**: Free tier has 100 requests/day
3. **Check Logs**: Look for GNews error messages
4. **Test Manually**: Try GNews API directly in browser

### Fallback Issues

1. **NewsAPI Key**: Ensure `NEWS_API_KEY` is still valid
2. **NDTV Service**: Check if NDTV API is responding
3. **Network Issues**: Verify internet connectivity

### No Articles Returned

1. **Check Query**: Some searches may have no results
2. **Try Different Topics**: Test with "India", "cricket", "technology"
3. **Check Date Range**: Recent news may be limited

## Development Notes

- **Service Class**: `services/gnews_service.py`
- **Integration**: `services/news_service.py` (updated)
- **Config**: `config.py` (GNews settings added)
- **Tests**: `test_gnews_integration.py`

## Production Deployment

For production deployment:

1. **Get Paid GNews Plan**: For higher rate limits
2. **Set Environment Variables**: In your hosting platform
3. **Monitor Usage**: Track API usage and costs
4. **Enable Caching**: Consider Redis caching for frequently requested content

---

**Ready to go!** 🚀 Your news app now has high-quality, India-focused content with GNews integration.
