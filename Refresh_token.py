import os
import base64
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_spotify_config():
    """Get Spotify configuration from environment variables"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    refresh_token = os.getenv('SPOTIFY_REFRESH_TOKEN')
    
    if not client_id or not client_secret or not refresh_token:
        raise ValueError("SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, and SPOTIFY_REFRESH_TOKEN must be set in environment variables")
    
    return client_id, client_secret, refresh_token

client_id, client_secret, refresh_token = get_spotify_config()

URL = f"https://accounts.spotify.com/api/token?grant_type=refresh_token&refresh_token={refresh_token}"
encoded = base64.b64encode(f'{client_id}:{client_secret}'.encode())
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic ' + encoded.decode()
}

response = requests.request("POST", URL, headers=headers).json()

print(json.dumps(response, indent=4))