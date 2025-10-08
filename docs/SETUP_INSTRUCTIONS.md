# News App - Setup Instructions

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
1. Double-click `start_app.bat` to start both backend and frontend servers
2. Open your browser and go to `http://localhost:3000`

### Option 2: Manual Setup

#### Start Backend (Flask API)
```bash
python app.py
```
- Backend will run on `http://localhost:5000`

#### Start Frontend (React App)
```bash
npm start
```
- Frontend will run on `http://localhost:3000`

## 📋 Prerequisites

Make sure you have installed:
- **Node.js** (v14 or higher)
- **Python** (v3.7 or higher)
- **npm** (comes with Node.js)

## 🔧 Installation

### Frontend Dependencies
```bash
npm install
```

### Backend Dependencies
```bash
pip install -r requirements.txt
```

## 🌟 Features

- ✅ **Dark Mode Toggle** - Switch between light and dark themes
- ✅ **SEO Optimized** - Rich meta tags and structured data
- ✅ **Image Optimization** - Lazy loading and responsive images
- ✅ **Modern UI** - Built with Tailwind CSS
- ✅ **Responsive Design** - Works on all devices
- ✅ **AI-Powered** - Personalized news recommendations

## 🎯 Usage

1. **Home Page**: View personalized news recommendations
2. **Search**: Search for specific news topics
3. **Profile**: Manage your interests and preferences
4. **Setup**: Configure your news preferences

## 🐛 Troubleshooting

### "Failed to load news" Error
- Make sure the Flask backend is running on port 5000
- Check that all Python dependencies are installed
- Verify the backend API is accessible at `http://localhost:5000`

### Frontend Not Loading
- Make sure Node.js and npm are installed
- Run `npm install` to install dependencies
- Check that port 3000 is not being used by another application

### Dark Mode Not Working
- Clear browser cache and refresh the page
- Check browser console for any JavaScript errors

## 📱 Browser Support

- Chrome (recommended)
- Firefox
- Safari
- Edge

## 🔗 API Endpoints

- `GET /api/news/trending` - Get trending news
- `GET /api/news/search?q=query` - Search news
- `GET /api/recommendations` - Get personalized recommendations
- `GET /api/profile` - Get user profile
- `POST /api/profile` - Update user profile

## 📞 Support

If you encounter any issues, check the browser console for error messages and ensure both servers are running properly.
