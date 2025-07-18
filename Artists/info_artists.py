import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers, print_json_response

url = ('https://api.spotify.com/v1/artists?'
       'ids=2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6')
        #2CIMQHirSU0MQqyYHq0eOx is the ID of deadmau5
        #57dN52uHvrHOxijzpIgu3E is the ID of Ratatat
        #1vCWHaC5f2uS3yhpwWbIA6 is the ID of Avicii
        
headers = get_spotify_headers()
response = requests.request("GET", url, headers=headers)
print_json_response(response)