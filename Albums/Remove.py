import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers

url = ('https://api.spotify.com/v1/me/albums')
data={"ids":"4aawyAB9vmqN3uQ7FjRGTy"}
      #4aawyAB9vmqN3uQ7FjRGTy is the ID of Pitbull's album Can't Stop Us Now
headers = get_spotify_headers()

response = requests.request("DELETE", url, headers=headers,params=data)
if response.status_code==200:
  print(response.status_code)
else:
  print(json.dumps(response.json(), indent=4))