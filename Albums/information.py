url = 'https://api.spotify.com/v1/albums/1uyf3l2d4XYwiEqAb7t7fX'
      #1uyf3l2d4XYwiEqAb7t7fX is the ID of Bruno Mars's album Doo-Wops And Hooligans

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQADKKbdbp_eSqNYP95WoXgUgobcdK_6aV1a_oO9sXommIo1y-_JVoL6TDdpb3JcAw48ijY-RM0q2d4W6Y0ZOoUv0ZEG-MrHca2srXEuL0uL_XydFVNQvjNUD0-gfBENWiLluiZUrBM'
}

response = requests.request("GET", url, headers=headers)
print(json.dumps(response.json(), indent=4))