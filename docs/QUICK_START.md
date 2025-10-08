# 🚀 NewsHub Quick Start Guide

Get your professional news app with Google OAuth running in **5 minutes**!

## 📋 Prerequisites

- Python 3.7+ installed
- Node.js 14+ installed  
- Google account
- Internet connection

## ⚡ Quick Setup (5 Steps)

### 1️⃣ Install Dependencies
```bash
# Install Python packages
pip install -r requirements.txt

# Install Node packages (if needed)
npm install
```

### 2️⃣ Set Up Google OAuth
**Follow this guide:** `STEP_BY_STEP_GOOGLE_OAUTH.md`

**Quick version:**
1. Go to https://console.cloud.google.com/
2. Create new project: "NewsHub-Auth"
3. Enable Google+ API and Google Identity
4. Create OAuth 2.0 credentials
5. Copy Client ID and Secret

### 3️⃣ Configure Environment
```bash
# Copy example file
cp .env.example .env

# Edit .env with your credentials
GOOGLE_CLIENT_ID=your_client_id_here
GOOGLE_CLIENT_SECRET=your_client_secret_here
SECRET_KEY=generate_random_key_here
```

### 4️⃣ Start the Application
```bash
# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend  
npm start
```

### 5️⃣ Test Authentication
1. Open: http://localhost:3000/login
2. Click "Sign in with Google"
3. Select your Google account
4. Enjoy your professional news app! 🎉

## 🔧 What You Get

✅ **Professional Google OAuth** - Same quality as Gmail, YouTube
✅ **Modern News Interface** - Clean, responsive design
✅ **Indian News Focus** - GNews API integration
✅ **Bilingual Support** - English and Telugu
✅ **Smart Caching** - Fast loading, API efficient
✅ **Production Ready** - Security best practices

## 🆘 Need Help?

**Common Issues:**
- **Port conflicts:** Change ports in config if needed
- **API errors:** Check your .env file credentials
- **CORS issues:** Make sure both servers are running

**Detailed Help:** See `STEP_BY_STEP_GOOGLE_OAUTH.md`

## 🚀 Next Steps

1. **Customize Categories** - Edit sidebar categories
2. **Add News Sources** - Configure additional APIs
3. **Deploy to Production** - Follow production guide
4. **Add Features** - Bookmarks, notifications, etc.

**Happy coding!** 🎯
