import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers, print_json_response

url = 'https://api.spotify.com/v1/playlists/11k95A0KyCM8B0rQIw2am0'

headers = get_spotify_headers()
response = requests.request("GET", url, headers=headers)
print_json_response(response)