URL = "https://accounts.spotify.com/api/token?grant_type=client_credentials"
encoded = base64.b64encode('ac0aee299d4b478fbcfcaf4b4e1fb081:d3e4da947ecc4e2d99bec3955f2700bf')
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic '+encoded
}

response = requests.request("POST", URL, headers=headers).json()

print(json.dumps(response, indent=4))

validation()