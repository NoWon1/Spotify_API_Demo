import base64
import requests
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import User
from api.models import SpotifyToken, UserProfile


class SpotifyService:
    """Service class for Spotify API interactions"""
    
    BASE_URL = 'https://api.spotify.com/v1'
    AUTH_URL = 'https://accounts.spotify.com/api/token'
    AUTHORIZE_URL = 'https://accounts.spotify.com/authorize'
    
    @staticmethod
    def get_auth_url(state=None):
        """Generate Spotify authorization URL"""
        scope = 'user-read-private user-read-email playlist-read-private playlist-modify-public playlist-modify-private user-library-read user-library-modify user-top-read user-read-recently-played'
        
        params = {
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'response_type': 'code',
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
            'scope': scope,
            'show_dialog': 'true'
        }
        
        if state:
            params['state'] = state
            
        query_string = '&'.join([f'{k}={v}' for k, v in params.items()])
        return f'{SpotifyService.AUTHORIZE_URL}?{query_string}'
    
    @staticmethod
    def exchange_code_for_token(code):
        """Exchange authorization code for access token"""
        client_credentials = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': settings.SPOTIFY_REDIRECT_URI
        }
        
        response = requests.post(SpotifyService.AUTH_URL, headers=headers, data=data)
        return response.json()
    
    @staticmethod
    def refresh_access_token(refresh_token):
        """Refresh access token using refresh token"""
        client_credentials = f"{settings.SPOTIFY_CLIENT_ID}:{settings.SPOTIFY_CLIENT_SECRET}"
        encoded_credentials = base64.b64encode(client_credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token
        }
        
        response = requests.post(SpotifyService.AUTH_URL, headers=headers, data=data)
        return response.json()
    
    @staticmethod
    def get_user_profile(access_token):
        """Get Spotify user profile"""
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.get(f'{SpotifyService.BASE_URL}/me', headers=headers)
        return response.json()
    
    @staticmethod
    def save_user_token(user, token_data):
        """Save or update user's Spotify token"""
        spotify_token, created = SpotifyToken.objects.get_or_create(
            user=user,
            defaults={
                'access_token': token_data['access_token'],
                'refresh_token': token_data.get('refresh_token', ''),
                'token_type': token_data.get('token_type', 'Bearer'),
                'expires_in': token_data.get('expires_in', 3600),
                'scope': token_data.get('scope', '')
            }
        )
        
        if not created:
            spotify_token.access_token = token_data['access_token']
            if 'refresh_token' in token_data:
                spotify_token.refresh_token = token_data['refresh_token']
            spotify_token.expires_in = token_data.get('expires_in', 3600)
            spotify_token.scope = token_data.get('scope', '')
            spotify_token.save()
        
        return spotify_token
    
    @staticmethod
    def save_user_profile(user, profile_data):
        """Save or update user's Spotify profile"""
        profile, created = UserProfile.objects.get_or_create(
            user=user,
            defaults={
                'spotify_id': profile_data.get('id'),
                'display_name': profile_data.get('display_name'),
                'email': profile_data.get('email'),
                'country': profile_data.get('country'),
                'product': profile_data.get('product'),
                'followers': profile_data.get('followers', {}).get('total', 0),
                'profile_image_url': profile_data.get('images', [{}])[0].get('url') if profile_data.get('images') else None
            }
        )
        
        if not created:
            profile.spotify_id = profile_data.get('id')
            profile.display_name = profile_data.get('display_name')
            profile.email = profile_data.get('email')
            profile.country = profile_data.get('country')
            profile.product = profile_data.get('product')
            profile.followers = profile_data.get('followers', {}).get('total', 0)
            if profile_data.get('images'):
                profile.profile_image_url = profile_data.get('images', [{}])[0].get('url')
            profile.save()
        
        return profile
