# Security Configuration Guide

## ⚠️ IMPORTANT: Setting Up Environment Variables

Your Spotify API keys have been secured using environment variables. Follow these steps to set up your project:

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Create Environment File

1. Copy `.env.example` to `.env`:
   ```bash
   copy .env.example .env
   ```

2. Open `.env` file and replace the placeholder values with your actual Spotify credentials:

```env
# Spotify App Credentials (Get these from https://developer.spotify.com/dashboard/)
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here

# OAuth Configuration  
SPOTIFY_REDIRECT_URI=https://your-domain.com/callback
SPOTIFY_SCOPE=playlist-read-collaborative playlist-modify-public playlist-modify-private playlist-read-private user-library-read user-library-modify

# Access Tokens (these expire - you'll need to refresh them)
SPOTIFY_ACCESS_TOKEN=your_actual_access_token_here
SPOTIFY_REFRESH_TOKEN=your_actual_refresh_token_here

# Django Configuration
DJANGO_SECRET_KEY=your_actual_django_secret_key_here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,your-domain.com
```

### 3. Getting Your Spotify Credentials

1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Copy your Client ID and Client Secret
4. Set your redirect URI in the app settings
5. Use the Authorization flow scripts to get access and refresh tokens

### 4. Important Security Notes

- **Never commit `.env` files to version control**
- The `.gitignore` file has been configured to exclude sensitive files
- All hardcoded tokens have been removed from the source code
- Use environment variables for all API keys and secrets

### 5. Running the Application

After setting up your `.env` file:

```bash
# For Django application
python manage.py runserver

# For individual API scripts
python "Tracks/Get_audio.py"
```

### 6. Token Management

- Access tokens expire after 1 hour
- Use `Refresh_token.py` to get new access tokens
- Update the `SPOTIFY_ACCESS_TOKEN` in your `.env` file when needed

### Files Modified for Security

All the following files have been updated to use environment variables:

**Core Files:**
- `config.py` - Central configuration
- `spotify_utils.py` - Shared utilities
- `Authorization_code.py` - OAuth flow
- `access_token.py` - Client credentials flow
- `Refresh_token.py` - Token refresh

**Django App:**
- `music_world/views.py` - Web application views
- `spotify_demo_app/settings.py` - Django settings

**API Examples:**
- All files in `Tracks/` directory
- All files in `Artists/` directory  
- All files in `Albums/` directory
- All files in `Playlists/` directory
- All files in `Search Spotify/` directory

### Emergency Security Checklist

If you accidentally committed sensitive data:

1. **Revoke compromised keys immediately** in Spotify Developer Dashboard
2. Generate new Client ID and Client Secret
3. Update your `.env` file with new credentials
4. Consider git history cleanup if keys were committed

### Support

- Check the main `README.md` for application documentation
- Refer to [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/)
- Ensure all environment variables are properly set before running scripts
