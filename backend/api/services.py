import requests
from django.core.cache import cache
from django.conf import settings
from .models import SpotifyToken


class SpotifyAPIService:
    """Service class for Spotify Web API interactions"""
    
    BASE_URL = 'https://api.spotify.com/v1'
    
    def __init__(self, user):
        self.user = user
        self.access_token = self._get_access_token()
    
    def _get_access_token(self):
        """Get user's access token"""
        try:
            spotify_token = SpotifyToken.objects.get(user=self.user)
            return spotify_token.access_token
        except SpotifyToken.DoesNotExist:
            raise ValueError("User has no Spotify token")
    
    def _get_headers(self):
        """Get authorization headers"""
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def _make_request(self, method, endpoint, params=None, data=None, cache_key=None, cache_timeout=300):
        """Make authenticated request to Spotify API with caching"""
        if cache_key:
            cached_result = cache.get(cache_key)
            if cached_result:
                return cached_result
        
        url = f"{self.BASE_URL}{endpoint}"
        headers = self._get_headers()
        
        response = requests.request(method, url, headers=headers, params=params, json=data)
        
        if response.status_code == 401:
            # Token expired - for now just raise error, refresh will be handled later
            raise ValueError("Access token expired. Please re-authenticate.")
        
        if response.status_code >= 400:
            response.raise_for_status()
        
        result = response.json()
        
        if cache_key and response.status_code == 200:
            cache.set(cache_key, result, cache_timeout)
        
        return result
    
    # User Profile Methods
    def get_user_profile(self):
        """Get current user's profile"""
        return self._make_request('GET', '/me', cache_key=f'user_profile_{self.user.id}')
    
    def get_user_playlists(self, limit=20, offset=0):
        """Get user's playlists"""
        params = {'limit': limit, 'offset': offset}
        return self._make_request('GET', '/me/playlists', params=params)
    
    def get_user_top_tracks(self, time_range='medium_term', limit=20):
        """Get user's top tracks"""
        params = {'time_range': time_range, 'limit': limit}
        cache_key = f'user_top_tracks_{self.user.id}_{time_range}_{limit}'
        return self._make_request('GET', '/me/top/tracks', params=params, cache_key=cache_key)
    
    def get_user_top_artists(self, time_range='medium_term', limit=20):
        """Get user's top artists"""
        params = {'time_range': time_range, 'limit': limit}
        cache_key = f'user_top_artists_{self.user.id}_{time_range}_{limit}'
        return self._make_request('GET', '/me/top/artists', params=params, cache_key=cache_key)
    
    def get_recently_played(self, limit=20):
        """Get recently played tracks"""
        params = {'limit': limit}
        return self._make_request('GET', '/me/player/recently-played', params=params)
    
    # Browse Methods
    def get_featured_playlists(self, limit=20):
        """Get featured playlists"""
        params = {'limit': limit}
        cache_key = f'featured_playlists_{limit}'
        return self._make_request('GET', '/browse/featured-playlists', params=params, 
                                cache_key=cache_key, cache_timeout=1800)
    
    def get_new_releases(self, limit=20):
        """Get new album releases"""
        params = {'limit': limit}
        cache_key = f'new_releases_{limit}'
        return self._make_request('GET', '/browse/new-releases', params=params,
                                cache_key=cache_key, cache_timeout=1800)
    
    def get_categories(self, limit=20):
        """Get browse categories"""
        params = {'limit': limit}
        cache_key = f'categories_{limit}'
        return self._make_request('GET', '/browse/categories', params=params,
                                cache_key=cache_key, cache_timeout=3600)
    
    # Search Methods
    def search(self, query, search_type='track', limit=20, offset=0):
        """Search for tracks, artists, albums, or playlists"""
        params = {
            'q': query,
            'type': search_type,
            'limit': limit,
            'offset': offset
        }
        return self._make_request('GET', '/search', params=params)
    
    # Track Methods
    def get_track(self, track_id):
        """Get track details"""
        cache_key = f'track_{track_id}'
        return self._make_request('GET', f'/tracks/{track_id}', cache_key=cache_key)
    
    def get_track_audio_features(self, track_id):
        """Get audio features for a track"""
        cache_key = f'audio_features_{track_id}'
        return self._make_request('GET', f'/audio-features/{track_id}', cache_key=cache_key)
    
    def get_tracks_audio_features(self, track_ids):
        """Get audio features for multiple tracks"""
        params = {'ids': ','.join(track_ids)}
        return self._make_request('GET', '/audio-features', params=params)
    
    # Artist Methods
    def get_artist(self, artist_id):
        """Get artist details"""
        cache_key = f'artist_{artist_id}'
        return self._make_request('GET', f'/artists/{artist_id}', cache_key=cache_key)
    
    def get_artist_albums(self, artist_id, limit=20):
        """Get artist's albums"""
        params = {'limit': limit}
        cache_key = f'artist_albums_{artist_id}_{limit}'
        return self._make_request('GET', f'/artists/{artist_id}/albums', params=params, cache_key=cache_key)
    
    def get_artist_top_tracks(self, artist_id, market='US'):
        """Get artist's top tracks"""
        params = {'market': market}
        cache_key = f'artist_top_tracks_{artist_id}_{market}'
        return self._make_request('GET', f'/artists/{artist_id}/top-tracks', params=params, cache_key=cache_key)
    
    def get_related_artists(self, artist_id):
        """Get related artists"""
        cache_key = f'related_artists_{artist_id}'
        return self._make_request('GET', f'/artists/{artist_id}/related-artists', cache_key=cache_key)
    
    # Album Methods
    def get_album(self, album_id):
        """Get album details"""
        cache_key = f'album_{album_id}'
        return self._make_request('GET', f'/albums/{album_id}', cache_key=cache_key)
    
    def get_album_tracks(self, album_id, limit=20):
        """Get album tracks"""
        params = {'limit': limit}
        cache_key = f'album_tracks_{album_id}_{limit}'
        return self._make_request('GET', f'/albums/{album_id}/tracks', params=params, cache_key=cache_key)
    
    # Playlist Methods
    def get_playlist(self, playlist_id):
        """Get playlist details"""
        cache_key = f'playlist_{playlist_id}'
        return self._make_request('GET', f'/playlists/{playlist_id}', cache_key=cache_key)
    
    def get_playlist_tracks(self, playlist_id, limit=20, offset=0):
        """Get playlist tracks"""
        params = {'limit': limit, 'offset': offset}
        return self._make_request('GET', f'/playlists/{playlist_id}/tracks', params=params)
    
    def create_playlist(self, name, description='', public=True):
        """Create a new playlist"""
        data = {
            'name': name,
            'description': description,
            'public': public
        }
        user_profile = self.get_user_profile()
        user_id = user_profile['id']
        return self._make_request('POST', f'/users/{user_id}/playlists', data=data)
    
    def add_tracks_to_playlist(self, playlist_id, track_uris):
        """Add tracks to playlist"""
        data = {'uris': track_uris}
        return self._make_request('POST', f'/playlists/{playlist_id}/tracks', data=data)
    
    # Library Methods
    def get_saved_tracks(self, limit=20, offset=0):
        """Get user's saved tracks"""
        params = {'limit': limit, 'offset': offset}
        return self._make_request('GET', '/me/tracks', params=params)
    
    def save_tracks(self, track_ids):
        """Save tracks to user's library"""
        params = {'ids': ','.join(track_ids)}
        return self._make_request('PUT', '/me/tracks', params=params)
    
    def remove_saved_tracks(self, track_ids):
        """Remove tracks from user's library"""
        params = {'ids': ','.join(track_ids)}
        return self._make_request('DELETE', '/me/tracks', params=params)
    
    def check_saved_tracks(self, track_ids):
        """Check if tracks are saved in user's library"""
        params = {'ids': ','.join(track_ids)}
        return self._make_request('GET', '/me/tracks/contains', params=params)
