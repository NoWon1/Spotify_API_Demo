url = ('https://api.spotify.com/v1/search?'
       'q=metallica&'
       'type=artist')

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQBZqLRUFX8KZLb31JPc63Eo01BhgFMvwDvGz80wZWIQMOE12C6BWC55LEln5bCf1wkP7cwK5EWOS5QjoKcXiHQ2csauX__f6ZQzebwR8bEsEMHFyALDonbyb-Yc27UGMyamFBNzL5U'
}

response = requests.request("GET", url, headers=headers)
print(json.dumps(response.json(), indent=4))