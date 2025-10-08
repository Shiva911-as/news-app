# 📱 NEWS APP - USER GUIDE

## 🚀 **Getting Started**

### 1. Launch the Application
```bash
# Terminal 1: Start Backend
python app.py

# Terminal 2: Start Frontend  
npm start
```

### 2. Open in Browser
- **URL**: `http://localhost:3000`
- **Best Experience**: Chrome, Firefox, Safari, Edge

## 🎯 **Key Features**

### 📰 **Browse News by Category**
- **Click any category** in the left sidebar
- **Categories available**:
  - 🏠 **Home**: Personalized recommendations
  - 🔥 **Trending**: Top trending news
  - 🇮🇳 **India**: Indian headlines
  - 💼 **Business**: Economy & market news
  - 🏛️ **Politics**: Government & policy news
  - ⚽ **Sports**: Cricket & sports news
  - 💻 **Technology**: Tech & startup news
  - 🎬 **Entertainment**: Bollywood & cinema
  - 🚀 **Startups**: Startup ecosystem news

### 🌐 **Language Support**
- **Toggle Languages**: Click [English | Telugu] in sidebar
- **Complete Translation**: All UI elements switch
- **Telugu Content**: News articles in Telugu script
- **Smart Translation**: Key terms automatically translated

### 🔊 **Text-to-Speech**
- **Article Cards**: Click small speaker icon (🔊) 
- **Article Details**: Click large speaker icon in header
- **Language Support**: English and Telugu voices
- **Controls**: Click again to stop reading

### 🧠 **Smart Recommendations**
- **Learns Your Interests**: Tracks what you click and read
- **Improves Over Time**: More clicks = better recommendations
- **Home Feed**: Shows personalized content based on your behavior
- **Anonymous**: No registration required

## 🎨 **Using the Interface**

### Sidebar Navigation
- **Categories**: Click to browse different news sections
- **Language Toggle**: Switch between English/Telugu
- **Collapsible**: Responsive design adapts to screen size

### Article Grid
- **Responsive Layout**: 4×2 on desktop, adapts on mobile
- **Article Cards**: Click any card to read full article
- **Speaker Icons**: Click to listen to article
- **Hover Effects**: Cards lift when you hover over them

### Article Details Panel
- **Opens on Right**: Slides in when you click an article
- **Full Content**: Title, description, source, author, date
- **Audio Reading**: Speaker icon to read aloud
- **Close**: Click X or click outside to close

## 🎯 **How Recommendations Work**

### Your First Visit
- **Default Content**: Shows general Indian news
- **Start Clicking**: Click articles that interest you
- **System Learns**: Tracks your preferences automatically

### After Using the App
- **Day 1**: Click 3 tech articles → Home shows more tech news
- **Day 7**: Click 15 tech, 5 sports → Home prioritizes tech heavily
- **Ongoing**: Recommendations get smarter with every interaction

### Scoring System
```
Your Interest Score = Clicks × 1.0 + Reading Time × 0.1

Example:
- Technology: 10 clicks + 45s avg reading = 10.0 + 4.5 = 14.5
- Sports: 3 clicks + 20s avg reading = 3.0 + 2.0 = 5.0
→ Home feed shows 3:1 ratio of tech to sports articles
```

## 🔧 **Troubleshooting**

### No Articles Loading
1. **Check Internet**: Ensure stable connection
2. **Refresh Browser**: Hard refresh (Ctrl+F5)
3. **Try Different Category**: Some categories may have limited content
4. **Check Console**: Open F12 → Console for error messages

### Text-to-Speech Not Working
1. **Browser Support**: Use Chrome, Firefox, Safari, or Edge
2. **Permissions**: Allow audio permissions if prompted
3. **Volume**: Check system and browser volume settings
4. **Language**: Some browsers have limited Telugu voice support

### Recommendations Not Personal
1. **Use the App More**: Click and read articles regularly
2. **Vary Your Interests**: Try different categories
3. **Reading Time**: Spend time reading articles (not just clicking)
4. **Clear Data**: Clear browser data if needed to reset

### Language Toggle Issues
1. **Refresh Page**: Hard refresh after language change
2. **Clear Cache**: Clear browser cache and cookies
3. **Check Network**: Ensure API calls are working

## 📊 **Understanding Your Data**

### What We Track
- **Article Clicks**: Which articles you click on
- **Reading Time**: How long you spend reading
- **Category Preferences**: Which sections you visit most
- **Anonymous ID**: Stored in browser (no personal info)

### What We Don't Track
- **Personal Information**: No names, emails, or personal data
- **Browsing History**: Only news app interactions
- **Location**: No GPS or location tracking
- **Device Info**: No device fingerprinting

### Data Control
- **Anonymous**: All data tied to random user ID
- **Local Storage**: User ID stored in your browser only
- **Reset Anytime**: Clear browser data to start fresh
- **No Registration**: No accounts or sign-ups required

## 🎉 **Pro Tips**

### Get Better Recommendations
1. **Read Articles**: Don't just click, spend time reading
2. **Explore Categories**: Try different sections occasionally
3. **Use Regularly**: Daily usage improves recommendations
4. **Mix Interests**: Click on variety of topics you like

### Best User Experience
1. **Use Desktop**: Best experience on larger screens
2. **Good Internet**: Stable connection for smooth loading
3. **Modern Browser**: Chrome/Firefox for all features
4. **Audio**: Use headphones for text-to-speech

### Discover More Content
1. **Try Telugu**: Switch language to see translated content
2. **Listen to News**: Use text-to-speech while multitasking
3. **Check Home Daily**: Personalized feed updates constantly
4. **Explore All Categories**: Each has unique, relevant content

## 🆘 **Need Help?**

### Common Questions
- **Q**: Why do I see the same articles?
- **A**: Try different categories or clear browser data to reset

- **Q**: Can I use this offline?
- **A**: No, requires internet for live news content

- **Q**: Is my data private?
- **A**: Yes, completely anonymous with no personal info stored

- **Q**: How do I reset my recommendations?
- **A**: Clear browser data or use incognito/private mode

### Technical Support
- Check `FINAL_SYSTEM_STATUS.md` for system status
- Run `python comprehensive_test.py` to test backend
- Check browser console (F12) for error messages
- Ensure both frontend and backend servers are running

---

## 🎯 **Enjoy Your Personalized News Experience!**

The more you use the app, the smarter it gets at showing you relevant Indian news content. Happy reading! 📰✨
