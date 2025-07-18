import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers, print_json_response

url = 'https://api.spotify.com/v1/albums/1uyf3l2d4XYwiEqAb7t7fX'
      #1uyf3l2d4XYwiEqAb7t7fX is the ID of Bruno Mars's album Doo-Wops And Hooligans

headers = get_spotify_headers()
response = requests.request("GET", url, headers=headers)
print_json_response(response)