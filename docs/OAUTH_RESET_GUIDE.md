# Complete OAuth Reset Guide

## Step 1: Delete Current OAuth Credentials
1. Go to: https://console.cloud.google.com/apis/credentials
2. Find your "NewsHub Web Client"
3. Click the trash/delete icon
4. Confirm deletion

## Step 2: Create New OAuth Credentials
1. Click "CREATE CREDENTIALS" → "OAuth 2.0 Client IDs"
2. Application type: **Web application**
3. Name: **NewsHub-Fresh**
4. Authorized JavaScript origins:
   - http://localhost:3000
   - http://localhost:5000
5. Authorized redirect URIs:
   - http://localhost:5000/auth/callback
6. Click "CREATE"

## Step 3: Update OAuth Consent Screen
1. Go to: https://console.cloud.google.com/apis/credentials/consent
2. Click "EDIT APP"
3. User Type: **External** (not Internal)
4. Publishing status: Click "PUBLISH APP"
5. Remove all test users (leave empty)
6. Save changes

## Step 4: Update Your .env File
Replace your current credentials with the new ones:
```
GOOGLE_CLIENT_ID=your_new_client_id_here
GOOGLE_CLIENT_SECRET=your_new_client_secret_here
```

## Step 5: Clear Browser Completely
1. Close ALL browser windows
2. Clear all browsing data (cookies, cache, everything)
3. Restart browser
4. Or try a different browser entirely

## Step 6: Test
1. Go to http://localhost:3000/login
2. Click "Sign in with Google"
3. You should now see your real Google accounts

## Why This Works:
- Fresh OAuth credentials without test restrictions
- Published app (not in testing mode)
- No cached test user data
- External user type allows any Google account
