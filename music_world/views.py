from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
import requests
from django.views.generic import TemplateView

headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer BQDkTqkJlSK1IOFbMmO_aUrKqRA-57V3NikvIkt9K2lHJKXZ9HVop3HKOJEwYbd3YybxKdS9g0hU6F389vigqoc_ELSFXinRsXUwq__foNElZsQ61xuKcEfT75KRjhKXe9tyr1nYC5A'
}
def home(request):
    data = requests.get("https://api.spotify.com/v1/browse/featured-playlists?limit=3", headers=headers)
    data1 = requests.get("https://api.spotify.com/v1/browse/new-releases?limit=3", headers=headers)
    status_code=data.status_code
    data=data.json()
    data1=data1.json()
    if status_code==200:
        data=data['playlists']['items']
        data1=data1['albums']['items']
        return render(request, 'music_world/home.html', {
            "data": data,"data1":data1})
    else:
        return render(request, 'music_world/error.html', {
            "data": data,"message":data['error']['message']})

def playlist(request,id):
    data = requests.get(f'https://api.spotify.com/v1/playlists/{id}', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        return render(request, 'music_world/playlist.html', {"data":data})
    else:
        return render(request, 'music_world/error.html', {
            "data": data,"message":data['error']['message']})

def album(request,id):
    data = requests.get(f'https://api.spotify.com/v1/albums/{id}', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        return render(request, 'music_world/album.html', {"data":data})
    else:
        return render(request, 'music_world/error.html', {
        "data": data,"message":data['error']['message']})

def sartist(request):
    symbol = request.GET.get("search")
    data = requests.get(f'https://api.spotify.com/v1/search?q={symbol}&type=artist', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        return render(request, 'music_world/sartist.html', {"data":data['artists']['items']})
    else:
        return render(request, 'music_world/error.html', {
        "data": data,"message":data['error']['message']})

def artist(request,id):
    data = requests.get(f'https://api.spotify.com/v1/artists/{id}/top-tracks?market=US', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        image=data['tracks'][0]['album']['images'][0]['url']
        return render(request, 'music_world/artist.html', {"data":data['tracks'],"image":image})
    else:
            return render(request, 'music_world/error.html', {
            "data": data,"message":data['error']['message']}) 

def audio(request,id):
    data = requests.get(f'https://api.spotify.com/v1/audio-features/{id}', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        context={
            "danceability":data['danceability'],
            "energy":data['energy'],
            "loudness":data['loudness'],
            "speechiness":data['speechiness'],
            "acousticness":data['acousticness'],
            "instrumentalness":data['instrumentalness'],
            "liveness":data['liveness'],
            "valence":data['valence'],
            "tempo":data['tempo']
        }
        return render(request, 'music_world/audio.html', context)
    else:
            return render(request, 'music_world/error.html', {
            "data": data,"message":data['error']['message']}) 