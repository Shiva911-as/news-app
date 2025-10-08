# Google OAuth Setup Guide

This guide will help you set up Google OAuth authentication for the NewsHub application.

## Prerequisites

- Google Cloud Console account
- NewsHub application running locally or deployed

## Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: `NewsHub Auth`
4. Click "Create"

## Step 2: Enable Google+ API

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search for "Google+ API"
3. Click on it and press "Enable"
4. Also enable "Google Identity" API

## Step 3: Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose "External" user type
3. Fill in the required information:
   - **App name**: NewsHub
   - **User support email**: Your email
   - **Developer contact information**: Your email
4. Add scopes:
   - `openid`
   - `email`
   - `profile`
5. Add test users (your email addresses)
6. Save and continue

## Step 4: Create OAuth 2.0 Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth 2.0 Client IDs"
3. Choose "Web application"
4. Configure:
   - **Name**: NewsHub Web Client
   - **Authorized JavaScript origins**: 
     - `http://localhost:3000` (for development)
     - `https://yourdomain.com` (for production)
   - **Authorized redirect URIs**:
     - `http://localhost:5000/auth/callback` (for development)
     - `https://yourdomain.com/auth/callback` (for production)
5. Click "Create"
6. Copy the **Client ID** and **Client Secret**

## Step 5: Environment Configuration

1. Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```

2. Update `.env` with your credentials:
   ```env
   # Google OAuth Configuration
   GOOGLE_CLIENT_ID=your_google_client_id_here
   GOOGLE_CLIENT_SECRET=your_google_client_secret_here
   
   # Flask Configuration
   SECRET_KEY=your_super_secret_key_here
   FLASK_ENV=development
   
   # Frontend URL (for OAuth redirects)
   FRONTEND_URL=http://localhost:3000
   ```

3. Generate a secure secret key:
   ```python
   import secrets
   print(secrets.token_hex(32))
   ```

## Step 6: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 7: Test the Setup

1. Start the Flask backend:
   ```bash
   python app.py
   ```

2. Start the React frontend:
   ```bash
   cd src
   npm start
   ```

3. Navigate to `http://localhost:3000/login`
4. Click "Sign in with Google"
5. Complete the OAuth flow

## Production Deployment

### Environment Variables

Set these environment variables in your production environment:

```env
GOOGLE_CLIENT_ID=your_production_client_id
GOOGLE_CLIENT_SECRET=your_production_client_secret
SECRET_KEY=your_production_secret_key
FRONTEND_URL=https://yourdomain.com
DATABASE_URL=postgresql://user:password@localhost/newsapp
REDIS_URL=redis://localhost:6379/0
```

### Security Considerations

1. **HTTPS Only**: Always use HTTPS in production
2. **Secure Cookies**: Set secure cookie flags
3. **CORS Configuration**: Restrict CORS to your domain
4. **Rate Limiting**: Implement rate limiting for auth endpoints
5. **Session Security**: Use Redis for session storage

### Domain Configuration

Update your Google OAuth settings for production:

1. Add your production domain to "Authorized JavaScript origins"
2. Add your production callback URL to "Authorized redirect URIs"
3. Update the OAuth consent screen with production URLs

## Troubleshooting

### Common Issues

1. **"redirect_uri_mismatch"**
   - Ensure your redirect URI exactly matches what's configured in Google Console
   - Check for trailing slashes and protocol (http vs https)

2. **"invalid_client"**
   - Verify your Client ID and Client Secret are correct
   - Check that the OAuth consent screen is properly configured

3. **"access_denied"**
   - User cancelled the OAuth flow
   - Check that your app is not in "Testing" mode for external users

4. **CORS Errors**
   - Ensure CORS is properly configured in Flask
   - Check that your frontend URL is whitelisted

### Debug Mode

Enable debug logging by setting:
```env
FLASK_ENV=development
```

This will provide detailed error messages in the console.

## Security Best Practices

1. **Never commit credentials** to version control
2. **Use environment variables** for all sensitive data
3. **Implement proper session management**
4. **Use HTTPS** in production
5. **Validate all user input**
6. **Implement rate limiting**
7. **Monitor authentication logs**

## Support

If you encounter issues:

1. Check the browser console for JavaScript errors
2. Check the Flask logs for backend errors
3. Verify your Google Cloud Console configuration
4. Test with a fresh incognito/private browser window

## Additional Resources

- [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Flask-Login Documentation](https://flask-login.readthedocs.io/)
- [Authlib Documentation](https://docs.authlib.org/)
