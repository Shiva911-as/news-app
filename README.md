# News App - Personalized News Recommendations

A production-ready news application with personalized recommendations, built with React frontend and Flask backend.

## Features

- **Personalized News Recommendations**: AI-powered article recommendations based on user interests
- **User Profile Management**: Set and manage your interests, view reading history
- **News Search**: Search for articles on any topic
- **Learning System**: The app learns from your reading preferences to improve recommendations
- **Modern UI**: Beautiful, responsive design with smooth animations
- **Real-time Updates**: Get the latest news from multiple categories

## Tech Stack

### Frontend
- **React 18** - Modern React with hooks and functional components
- **React Router** - Client-side routing
- **React Icons** - Beautiful icon library
- **React Hot Toast** - Toast notifications
- **Axios** - HTTP client for API calls
- **CSS3** - Modern styling with CSS Grid and Flexbox

### Backend
- **Flask** - Python web framework
- **News API** - External news data source
- **JSON** - Data storage (user profiles)
- **Python-dotenv** - Environment variable management

## Project Structure

```
News/
├── src/                    # React frontend
│   ├── components/         # Reusable components
│   ├── pages/             # Page components
│   ├── context/           # React context
│   ├── services/          # API services
│   └── ...
├── services/              # Flask backend services
├── models/                # Data models
├── utils/                 # Utility functions
├── config.py             # Configuration management
├── app.py                # Flask application
├── requirements.txt      # Python dependencies
├── package.json          # Node.js dependencies
└── README.md            # This file
```

## Installation & Setup

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- News API key (get from [newsapi.org](https://newsapi.org))

### Backend Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Set up environment variables**:
   Create a `.env` file in the root directory:
   ```env
   NEWS_API_KEY=your_news_api_key_here
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   ```

3. **Run the Flask backend**:
   ```bash
   python app.py
   ```
   The backend will run on `http://localhost:5000`

### Frontend Setup

1. **Install Node.js dependencies**:
   ```bash
   npm install
   ```

2. **Start the React development server**:
   ```bash
   npm start
   ```
   The frontend will run on `http://localhost:3000`

## Usage

1. **First Time Setup**:
   - Visit the app in your browser
   - Go to the Setup page to configure your interests
   - Add topics like "technology", "sports", "politics", etc.

2. **Getting Recommendations**:
   - The home page shows personalized news recommendations
   - Click "Read Article" to open articles in a new tab
   - The app learns from your reading preferences

3. **Searching News**:
   - Use the Search page to find articles on specific topics
   - Enter keywords and get relevant results

4. **Managing Profile**:
   - View your profile to see interests and reading history
   - Update interests anytime from the Setup page

## API Endpoints

### News Endpoints
- `GET /api/news/trending` - Get trending news
- `GET /api/news/search?q=query` - Search for articles
- `GET /api/news/topic/<topic>` - Get topic-specific news

### User Profile Endpoints
- `GET /api/profile` - Get user profile
- `POST /api/profile` - Update user interests
- `POST /api/profile/learn` - Learn from article reading
- `GET /api/recommendations` - Get personalized recommendations

## Production Deployment

### Backend Deployment
1. Set `FLASK_ENV=production` in environment variables
2. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Frontend Deployment
1. Build the production version:
   ```bash
   npm run build
   ```
2. Serve the `build` folder with a web server like Nginx

## Configuration

### Environment Variables
- `NEWS_API_KEY`: Your News API key
- `FLASK_ENV`: Environment (development/production)
- `SECRET_KEY`: Flask secret key
- `LOG_LEVEL`: Logging level (INFO/WARNING/ERROR)

### Customization
- Modify `config.py` to change app settings
- Update related topics in `RELATED_TOPICS` configuration
- Customize styling in CSS files

## Features in Detail

### Personalized Recommendations
- Uses machine learning to score articles based on user interests
- Learns from reading behavior to improve recommendations
- Supports related topics and synonyms

### User Profile System
- Persistent user profiles stored in JSON files
- Interest weighting system
- Reading history tracking
- Profile statistics and analytics

### News Integration
- Real-time news from News API
- Multiple news categories
- Article metadata (source, date, description)
- External article links

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support, please open an issue on GitHub or contact the development team.

---

**Note**: Make sure to replace `your_news_api_key_here` with your actual News API key from [newsapi.org](https://newsapi.org).
