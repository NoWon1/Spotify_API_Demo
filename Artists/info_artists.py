url = ('https://api.spotify.com/v1/artists?'
       'ids=2CIMQHirSU0MQqyYHq0eOx,57dN52uHvrHOxijzpIgu3E,1vCWHaC5f2uS3yhpwWbIA6')
        #2CIMQHirSU0MQqyYHq0eOx is the ID of deadmau5
        #57dN52uHvrHOxijzpIgu3E is the ID of Ratatat
        #1vCWHaC5f2uS3yhpwWbIA6 is the ID of Avicii
        
headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQBZqLRUFX8KZLb31JPc63Eo01BhgFMvwDvGz80wZWIQMOE12C6BWC55LEln5bCf1wkP7cwK5EWOS5QjoKcXiHQ2csauX__f6ZQzebwR8bEsEMHFyALDonbyb-Yc27UGMyamFBNzL5U'
}

response = requests.request("GET", url, headers=headers)
print(json.dumps(response.json(), indent=4))