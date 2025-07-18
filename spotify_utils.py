"""
Shared utilities for Spotify API interactions
"""
import os
import json
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_spotify_headers():
    """Get Authorization headers for Spotify API requests"""
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("SPOTIFY_ACCESS_TOKEN not found in environment variables")
    
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }

def make_spotify_request(method, url, **kwargs):
    """Make a request to Spotify API with proper headers"""
    headers = get_spotify_headers()
    response = requests.request(method, url, headers=headers, **kwargs)
    return response

def print_json_response(response):
    """Print JSON response in a formatted way"""
    if response.status_code == 200:
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Error {response.status_code}:")
        try:
            print(json.dumps(response.json(), indent=4))
        except:
            print(response.text)
