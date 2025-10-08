# Step-by-Step Google OAuth Setup Guide

This guide will walk you through **exactly** how to set up Google OAuth for your NewsHub application. Follow each step carefully.

## 🚀 Step 1: Access Google Cloud Console

1. **Open your browser** and go to: https://console.cloud.google.com/
2. **Sign in** with your Google account (use the same account you want to manage the app)
3. **Accept** any terms of service if prompted

## 📁 Step 2: Create a New Project

1. **Click** on the project dropdown at the top (it might say "Select a project")
2. **Click** "NEW PROJECT" button
3. **Enter Project Details:**
   - Project name: `NewsHub-Auth`
   - Organization: Leave as default
   - Location: Leave as default
4. **Click** "CREATE"
5. **Wait** for the project to be created (30-60 seconds)
6. **Select** your new project from the dropdown

## 🔧 Step 3: Enable Required APIs

### Enable Google+ API:
1. **Go to:** https://console.cloud.google.com/apis/library
2. **Search for:** "Google+ API"
3. **Click** on "Google+ API" from results
4. **Click** "ENABLE" button
5. **Wait** for it to enable

### Enable Google Identity Services:
1. **Search for:** "Google Identity"
2. **Click** on "Google Identity" from results  
3. **Click** "ENABLE" button

## 🛡️ Step 4: Configure OAuth Consent Screen

1. **Go to:** https://console.cloud.google.com/apis/credentials/consent
2. **If you see "Google Auth Platform not configured yet":**
   - **Click** the blue "Get started" button
   - This will take you to the OAuth consent screen setup
3. **Choose** "External" user type (this allows anyone with a Google account to sign in)
4. **Click** "CREATE"

### Fill App Information:
- **App name:** `NewsHub`
- **User support email:** Your email address
- **App logo:** Skip for now
- **App domain:** Leave empty for now
- **Developer contact information:** Your email address
4. **Click** "SAVE AND CONTINUE"

### Scopes Section:
5. **Click** "ADD OR REMOVE SCOPES"
6. **Select these scopes:**
   - `../auth/userinfo.email`
   - `../auth/userinfo.profile`  
   - `openid`
7. **Click** "UPDATE"
8. **Click** "SAVE AND CONTINUE"

### Test Users:
9. **Click** "ADD USERS"
10. **Add your email address**
11. **Click** "SAVE AND CONTINUE"
12. **Click** "BACK TO DASHBOARD"

## 🔑 Step 5: Create OAuth 2.0 Credentials

1. **Go to:** https://console.cloud.google.com/apis/credentials
2. **Click** "CREATE CREDENTIALS" → "OAuth 2.0 Client IDs"

### Configure Web Application:
3. **Application type:** Web application
4. **Name:** `NewsHub Web Client`

### Authorized JavaScript Origins:
5. **Click** "ADD URI" under "Authorized JavaScript origins"
6. **Add:** `http://localhost:3000`
7. **Add:** `http://localhost:5000` (click ADD URI again)

### Authorized Redirect URIs:
8. **Click** "ADD URI" under "Authorized redirect URIs"  
9. **Add:** `http://localhost:5000/auth/callback`

10. **Click** "CREATE"

### Save Your Credentials:
11. **Copy** the "Client ID" (starts with numbers, ends with .googleusercontent.com)
12. **Copy** the "Client Secret" (random string)
13. **Click** "OK"

## 📝 Step 6: Configure Your Application

### Create Environment File:
1. **Open** your NewsHub project folder
2. **Copy** `.env.example` to `.env`
3. **Edit** `.env` file:

```env
# Google OAuth Configuration  
GOOGLE_CLIENT_ID=paste_your_client_id_here
GOOGLE_CLIENT_SECRET=paste_your_client_secret_here

# Flask Configuration
SECRET_KEY=your_random_secret_key_here
FLASK_ENV=development

# Frontend URL
FRONTEND_URL=http://localhost:3000

# Other APIs (if you have them)
NEWS_API_KEY=your_news_api_key
GNEWS_API_KEY=your_gnews_api_key
```

### Generate Secret Key:
4. **Open** Python terminal and run:
```python
import secrets
print(secrets.token_hex(32))
```
5. **Copy** the output and paste as SECRET_KEY in .env

## 🧪 Step 7: Test Your Setup

### Start Backend:
1. **Open** terminal in your project folder
2. **Run:** `python app.py`
3. **Verify** you see: "Starting Smart Cached News App"

### Start Frontend:
4. **Open** new terminal
5. **Run:** `npm start` (or `cd src && npm start`)
6. **Browser** should open to http://localhost:3000

### Test Authentication:
7. **Go to:** http://localhost:3000/login
8. **Click** "Sign in with Google"
9. **You should see** Google's account selection screen
10. **Select** your account
11. **Grant** permissions
12. **You should be** redirected back to NewsHub

## 🔧 Troubleshooting Common Issues

### "redirect_uri_mismatch" Error:
- **Check** that your redirect URI is exactly: `http://localhost:5000/auth/callback`
- **No trailing slash**
- **Correct port number**

### "invalid_client" Error:
- **Double-check** your Client ID and Client Secret in .env
- **Make sure** no extra spaces or quotes

### "This app isn't verified" Warning:
- **Click** "Advanced"
- **Click** "Go to NewsHub (unsafe)" 
- **This is normal** for development

### CORS Errors:
- **Make sure** both frontend (3000) and backend (5000) are running
- **Check** that CORS is enabled in Flask

## 🌐 Production Setup (Later)

When you're ready to deploy:

### Update Google Console:
1. **Add production domains** to Authorized JavaScript origins
2. **Add production callback** to Authorized redirect URIs
3. **Update OAuth consent screen** with production info

### Update Environment:
```env
GOOGLE_CLIENT_ID=same_as_development
GOOGLE_CLIENT_SECRET=same_as_development  
FRONTEND_URL=https://yourdomain.com
SECRET_KEY=new_production_secret
```

## 📞 Need Help?

### Check These First:
1. **Browser Console** (F12) for JavaScript errors
2. **Terminal** where you ran `python app.py` for backend errors
3. **Make sure** both servers are running (ports 3000 and 5000)

### Still Stuck?
- **Try incognito/private** browser window
- **Clear browser cache** and cookies
- **Double-check** all URLs have correct ports
- **Verify** .env file has no syntax errors

## ✅ Success Checklist

- [ ] Google Cloud project created
- [ ] APIs enabled (Google+ and Google Identity)  
- [ ] OAuth consent screen configured
- [ ] OAuth 2.0 credentials created
- [ ] .env file configured with credentials
- [ ] Backend running on port 5000
- [ ] Frontend running on port 3000
- [ ] Can click "Sign in with Google"
- [ ] Google account selection appears
- [ ] Successfully redirected back to app

**Congratulations!** 🎉 You now have professional Google OAuth authentication working in your NewsHub application!
