import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers

url = ('https://api.spotify.com/v1/me/tracks?'
        'ids=4rHZZAmHpZrA3iH5zx8frV,3C0nOe05EIt1390bVABLyN')
        #4rHZZAmHpZrA3iH5zx8frV is the Spotify ID for the song Mirrors
        #3C0nOe05EIt1390bVABLyN is the Spotify ID for the song On the Floor
headers = get_spotify_headers()

response = requests.request("PUT", url, headers=headers,params={})
if response.status_code==200:
    print(response.status_code)
else:
    print(json.dumps(response.json(), indent=4))