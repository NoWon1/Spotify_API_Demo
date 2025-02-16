URL = "https://accounts.spotify.com/api/token?grant_type=refresh_token&refresh_token=AQA4nVyZJOS3pvat7biOdO3IxaOX5_dxseYZt_bT3G9m2nU5QgZUdkcZcGie8K-zbMOF4c40TlQFLkGn5x2J6ZX6GDJyEQoyF-Xc3IPiGSeXBdbBkUSI3iyWxQAHWuCHBqw"
encoded = base64.b64encode('ac0aee299d4b478fbcfcaf4b4e1fb081:d3e4da947ecc4e2d99bec3955f2700bf')
headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': 'Basic '+encoded
}

response = requests.request("POST", URL, headers=headers).json()

print(json.dumps(response, indent=4))