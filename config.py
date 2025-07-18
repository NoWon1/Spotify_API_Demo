import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def get_spotify_config():
    """Get Spotify API configuration from environment variables"""
    return {
        'client_id': os.getenv('SPOTIFY_CLIENT_ID'),
        'client_secret': os.getenv('SPOTIFY_CLIENT_SECRET'),
        'redirect_uri': os.getenv('SPOTIFY_REDIRECT_URI'),
        'scope': os.getenv('SPOTIFY_SCOPE'),
        'access_token': os.getenv('SPOTIFY_ACCESS_TOKEN'),
        'refresh_token': os.getenv('SPOTIFY_REFRESH_TOKEN')
    }

def get_spotify_headers():
    """Get Authorization headers for Spotify API requests"""
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("SPOTIFY_ACCESS_TOKEN not found in environment variables")
    
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
