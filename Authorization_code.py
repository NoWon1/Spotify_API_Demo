import os
import base64
import requests
from flask import Flask, redirect, request, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

def get_spotify_config():
    """Get Spotify configuration from environment variables"""
    client_id = os.getenv('SPOTIFY_CLIENT_ID')
    client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
    
    if not client_id or not client_secret:
        raise ValueError("SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET must be set in environment variables")
    
    return {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': os.getenv('SPOTIFY_REDIRECT_URI', 'https://ed-6488463376777216.educative.run/callback'),
        'scope': os.getenv('SPOTIFY_SCOPE', 'playlist-read-collaborative playlist-modify-public playlist-modify-private playlist-read-private user-library-read user-library-modify')
    }

#  Client Keys
config = get_spotify_config()
CLIENT_ID = config['client_id']
CLIENT_SECRET = config['client_secret']
# Encoding values for header
ENCODED_CLIENT_SECRET = base64.b64encode(f'{CLIENT_ID}:{CLIENT_SECRET}'.encode()).decode("utf-8")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Server-side Parameters
REDIRECT_URI = config['redirect_uri']
SCOPE = config['scope']
RESPONSE_TYPE = "code"
GRANT_TYPE = 'authorization_code'

@app.route("/")
def index():
    authorize_url = 'https://accounts.spotify.com/en/authorize?response_type={}&client_id={}&redirect_uri={}&scope={}&show_dialog=TRUE'.format(RESPONSE_TYPE,CLIENT_ID,REDIRECT_URI,SCOPE)
    response = redirect(authorize_url)
    return response


@app.route("/callback")
def callback():
    token_url = 'https://accounts.spotify.com/api/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': 'Basic '+'{}'.format(ENCODED_CLIENT_SECRET)
        }
    body = {'code': request.args.get('code'), 'redirect_uri': REDIRECT_URI, 
            'grant_type': GRANT_TYPE}
    post_response = requests.post(token_url,headers=headers,data=body)
    return render_template('home.html',token=post_response.json())


if __name__ == '__main__':
    app.run(debug=True)