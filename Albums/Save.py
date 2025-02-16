url = ('https://api.spotify.com/v1/me/albums?'
       'ids=4aawyAB9vmqN3uQ7FjRGTy,1uyf3l2d4XYwiEqAb7t7fX')
      #4aawyAB9vmqN3uQ7FjRGTy is the ID of Pitbull's album Can't Stop Us Now
      #1uyf3l2d4XYwiEqAb7t7fX is the ID of Bruno Mars's album Doo-Wops And Hooligans
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQCKBtFTWcfbGfxFH2M2GMVTg-OMIM5CO6blcFb5SB88Rgwz1Gtvwg8kKHTTbF6zpEJSLPk0If9_ehzXXBDh0CpQPyZboWrIQXqIC19VlrLIuDIaGrz7KkLzge0tPFEBYvu4jDKMDJApZ0adOwb9RKYxZRXV9HBm-lCHW6RyMf1yKmu-fry6E-q4YyNOmkm9COVTkLs2ehMjs1pJ1RyCTIx9LN7giWko6RwyfISdaOHdLNwgWklBFwDkMreKpma1vNtxxzVJFGwaAeJjzgIu-lrqTqb6TYLJKtqLO0hgCuPk9ERdNifT1GKsUQEn1SHTTxUdFg'
}

response = requests.request("PUT", url, headers=headers,params={})
if response.status_code==200:
  print(response.status_code)
else:
  print(json.dumps(response.json(), indent=4))