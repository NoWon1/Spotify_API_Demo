import json
import requests
import sys
import os

# Add parent directory to path to import utilities
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from spotify_utils import get_spotify_headers

url = ('https://api.spotify.com/v1/me/albums?'
       'ids=4aawyAB9vmqN3uQ7FjRGTy,1uyf3l2d4XYwiEqAb7t7fX')
      #4aawyAB9vmqN3uQ7FjRGTy is the ID of Pitbull's album Can't Stop Us Now
      #1uyf3l2d4XYwiEqAb7t7fX is the ID of Bruno Mars's album Doo-Wops And Hooligans
headers = get_spotify_headers()

response = requests.request("PUT", url, headers=headers,params={})
if response.status_code==200:
  print(response.status_code)
else:
  print(json.dumps(response.json(), indent=4))