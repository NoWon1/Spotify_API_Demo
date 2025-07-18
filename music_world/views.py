from django.shortcuts import render
from django.http.response import JsonResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
import json
import requests
from django.views.generic import TemplateView
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_spotify_headers():
    """Get Authorization headers for Spotify API requests"""
    access_token = os.getenv('SPOTIFY_ACCESS_TOKEN')
    if not access_token:
        raise ValueError("SPOTIFY_ACCESS_TOKEN not found in environment variables")
    
    return {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
def home(request):
    headers = get_spotify_headers()
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
    headers = get_spotify_headers()
    data = requests.get(f'https://api.spotify.com/v1/playlists/{id}', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        return render(request, 'music_world/playlist.html', {"data":data})
    else:
        return render(request, 'music_world/error.html', {
            "data": data,"message":data['error']['message']})

def album(request,id):
    headers = get_spotify_headers()
    data = requests.get(f'https://api.spotify.com/v1/albums/{id}', headers=headers)
    status_code=data.status_code
    data=data.json()
    if status_code==200:
        return render(request, 'music_world/album.html', {"data":data})
    else:
        return render(request, 'music_world/error.html', {
        "data": data,"message":data['error']['message']})

def sartist(request):
    headers = get_spotify_headers()
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
    headers = get_spotify_headers()
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
    headers = get_spotify_headers()
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