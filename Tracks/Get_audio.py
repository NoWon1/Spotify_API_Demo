import json
import os
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

url = ('https://api.spotify.com/v1/audio-features?'
       'ids=11dFghVXANMlKmJXsNCbNl,7ouMYWpwJ422jRcDASZB7P,4VqPOruhp5EdPBeR92t6lQ')
       #11dFghVXANMlKmJXsNCbNl is the Spotify ID of the song Cut To The Feeling
       #7ouMYWpwJ422jRcDASZB7P is the Spotify ID of the song Knights of Cydonia
       #4VqPOruhp5EdPBeR92t6lQ is the Spotify ID of the song Uprising
       

headers = get_spotify_headers()

response = requests.request("GET", url, headers=headers)
print(json.dumps(response.json(), indent=4))