url = "https://api.spotify.com/v1/tracks/4rHZZAmHpZrA3iH5zx8frV"
      #11dFghVXANMlKmJXsNCbNl is the Spotify ID of the song Cut To The Feeling
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQADKKbdbp_eSqNYP95WoXgUgobcdK_6aV1a_oO9sXommIo1y-_JVoL6TDdpb3JcAw48ijY-RM0q2d4W6Y0ZOoUv0ZEG-MrHca2srXEuL0uL_XydFVNQvjNUD0-gfBENWiLluiZUrBM'
}

response = requests.request("GET", url, headers=headers)
print(json.dumps(response.json(), indent=4))