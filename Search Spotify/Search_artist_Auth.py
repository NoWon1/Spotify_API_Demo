url = ('https://api.spotify.com/v1/search?'
       'q=jake&'
       'type=artist')

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQAikugrf9DkApJZEMVXpPYHkcLtlhLg4GMPCkpcMp9ehR0VszJwMokBikJRc7VZmrSxB1X0Jhe50eZhK_Mv0CtYA8H9YzISxViecbqi8nlOTTUmqLbUff33MYk26ARcUPXNpTc5DVbx4n9H5as7yXLpzTyyr8GeRJUH4zpEKfi1m6vPh8cs1hu8BiLUKl3rsGSs__iKQn58iC9K88m-6jMfYgB5Tc9nJjbBDWGRR94ku0zy7U2Pn5Cw3r8o225ny4lXTJTgsyizMcuuWntxbTngHkWPnF1kNxqE3fOA2bs1YxxjiPDceA1W7u6iBO0VcRME2Q'
}

response = requests.request("GET", url, headers=headers)
print(json.dumps(response.json(), indent=4))