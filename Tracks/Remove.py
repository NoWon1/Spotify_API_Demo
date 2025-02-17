url = 'https://api.spotify.com/v1/me/tracks'
data = {
         "ids":"3C0nOe05EIt1390bVABLyN"
       }
        #3C0nOe05EIt1390bVABLyN is the Spotify ID for the song On the Floor
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQCKBtFTWcfbGfxFH2M2GMVTg-OMIM5CO6blcFb5SB88Rgwz1Gtvwg8kKHTTbF6zpEJSLPk0If9_ehzXXBDh0CpQPyZboWrIQXqIC19VlrLIuDIaGrz7KkLzge0tPFEBYvu4jDKMDJApZ0adOwb9RKYxZRXV9HBm-lCHW6RyMf1yKmu-fry6E-q4YyNOmkm9COVTkLs2ehMjs1pJ1RyCTIx9LN7giWko6RwyfISdaOHdLNwgWklBFwDkMreKpma1vNtxxzVJFGwaAeJjzgIu-lrqTqb6TYLJKtqLO0hgCuPk9ERdNifT1GKsUQEn1SHTTxUdFg'
}

response = requests.request("DELETE", url, headers=headers,params=data)
if response.status_code==200:
    print(response.status_code)
else:
    print(json.dumps(response.json(), indent=4))