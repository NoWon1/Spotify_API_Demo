import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers

url = 'https://api.spotify.com/v1/users/v3b60nrswk4600pu20n0fpvwn/playlists'

data={
    'name': 'Educative playlist',
    'description': 'Playlist created using the Spotify API'
}

headers = get_spotify_headers()
response = requests.request("POST", url, headers=headers, data=json.dumps(data))
print(json.dumps(response.json(), indent=4))

data={
    'name': 'Educative playlist',
    'description': 'Playlist created using the Spotify API'
}

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQCKBtFTWcfbGfxFH2M2GMVTg-OMIM5CO6blcFb5SB88Rgwz1Gtvwg8kKHTTbF6zpEJSLPk0If9_ehzXXBDh0CpQPyZboWrIQXqIC19VlrLIuDIaGrz7KkLzge0tPFEBYvu4jDKMDJApZ0adOwb9RKYxZRXV9HBm-lCHW6RyMf1yKmu-fry6E-q4YyNOmkm9COVTkLs2ehMjs1pJ1RyCTIx9LN7giWko6RwyfISdaOHdLNwgWklBFwDkMreKpma1vNtxxzVJFGwaAeJjzgIu-lrqTqb6TYLJKtqLO0hgCuPk9ERdNifT1GKsUQEn1SHTTxUdFg'
}

response = requests.request("POST", url, headers=headers, data=json.dumps(data))
print(json.dumps(response.json(), indent=4))