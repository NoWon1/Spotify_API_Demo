import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers

url = ('https://api.spotify.com/v1/playlists/11k95A0KyCM8B0rQIw2am0/tracks')

data={
       'uris':'spotify:track:4iV5W9uYEdYUVa79Axb7Rh,spotify:track:1301WleyT98MSxVHPZCA6M'
}

headers = get_spotify_headers()
response = requests.request("POST", url, headers=headers, params=data)
print(json.dumps(response.json(), indent=4))