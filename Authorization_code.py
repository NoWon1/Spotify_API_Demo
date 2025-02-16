app = Flask(__name__)


#  Client Keys
CLIENT_ID = "ac0aee299d4b478fbcfcaf4b4e1fb081"
CLIENT_SECRET = "d3e4da947ecc4e2d99bec3955f2700bf"
# Encoding values for header
ENCODED_CLIENT_SECRET = base64.b64encode(b'ac0aee299d4b478fbcfcaf4b4e1fb081:d3e4da947ecc4e2d99bec3955f2700bf')
ENCODED_CLIENT_SECRET=ENCODED_CLIENT_SECRET.decode("utf-8")

# Spotify URLS
SPOTIFY_AUTH_URL = "https://accounts.spotify.com/authorize"
SPOTIFY_TOKEN_URL = "https://accounts.spotify.com/api/token"

# Server-side Parameters
REDIRECT_URI = "https://ed-6488463376777216.educative.run/callback"
SCOPE = "playlist-read-collaborative playlist-modify-public playlist-modify-private playlist-read-private user-library-read user-library-modify"
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

validation()