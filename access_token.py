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
    
    if not client_id or not client_secret:
        raise ValueError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in environment variables")
    
    return client_id, client_secret

client_id, client_secret = get_spotify_config()

URL = "https://accounts.spotify.com/api/token?grant_type=client_credentials"
encoded = base64.b64encode(f'{client_id}:{client_secret}'.encode())
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic ' + encoded.decode()
}

response = requests.request("POST", URL, headers=headers).json()

print(json.dumps(response, indent=4))