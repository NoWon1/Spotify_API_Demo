from django.db import models
from django.contrib.auth.models import User
import json


class UserProfile(models.Model):
    """Extended user profile with Spotify data"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    spotify_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    display_name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    country = models.CharField(max_length=10, blank=True)
    profile_image = models.URLField(blank=True)
    followers = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.display_name}"


class SpotifyToken(models.Model):
    """Store Spotify OAuth tokens for users"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='spotify_token')
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_type = models.CharField(max_length=50, default='Bearer')
    expires_in = models.IntegerField()
    scope = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Token for {self.user.username}"


class UserPlaylist(models.Model):
    """Store user's favorite playlists"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_playlists')
    playlist_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    total_tracks = models.IntegerField(default=0)
    owner_name = models.CharField(max_length=100, blank=True)
    owner_id = models.CharField(max_length=100, blank=True)
    public = models.BooleanField(default=True)
    collaborative = models.BooleanField(default=False)
    followers = models.IntegerField(default=0)
    external_urls = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_playlists'
        unique_together = ['user', 'playlist_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class UserTrack(models.Model):
    """Store user's favorite tracks"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_tracks')
    track_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    artist_id = models.CharField(max_length=100, blank=True)
    album_name = models.CharField(max_length=200)
    album_id = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    duration_ms = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    preview_url = models.URLField(blank=True, null=True)
    explicit = models.BooleanField(default=False)
    external_urls = models.JSONField(default=dict)
    audio_features = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_tracks'
        unique_together = ['user', 'track_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name} by {self.artist_name}"


class UserArtist(models.Model):
    """Store user's favorite artists"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_artists')
    artist_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    image_url = models.URLField(blank=True)
    followers = models.IntegerField(default=0)
    popularity = models.IntegerField(default=0)
    genres = models.JSONField(default=list)
    external_urls = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_artists'
        unique_together = ['user', 'artist_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name}"


class UserAlbum(models.Model):
    """Store user's favorite albums"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_albums')
    album_id = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    artist_id = models.CharField(max_length=100, blank=True)
    image_url = models.URLField(blank=True)
    total_tracks = models.IntegerField(default=0)
    release_date = models.CharField(max_length=20, blank=True)
    album_type = models.CharField(max_length=50, blank=True)
    external_urls = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_albums'
        unique_together = ['user', 'album_id']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.name} by {self.artist_name}"


class SearchHistory(models.Model):
    """Store user's search history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='search_history')
    query = models.CharField(max_length=200)
    search_type = models.CharField(max_length=20)  # track, artist, album, playlist
    result_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'search_history'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} searched '{self.query}' in {self.search_type}"


class UserRecommendation(models.Model):
    """Store personalized recommendations for users"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    item_type = models.CharField(max_length=20)  # track, artist, album, playlist
    item_id = models.CharField(max_length=100)
    item_name = models.CharField(max_length=200)
    score = models.FloatField(default=0.0)
    reason = models.CharField(max_length=500, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user_recommendations'
        ordering = ['-score', '-created_at']

    def __str__(self):
        return f"Recommendation for {self.user.username}: {self.item_name}"


class ListeningHistory(models.Model):
    """Track user's listening patterns"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='listening_history')
    track_id = models.CharField(max_length=100)
    track_name = models.CharField(max_length=200)
    artist_name = models.CharField(max_length=200)
    played_at = models.DateTimeField()
    duration_played = models.IntegerField(default=0)  # in milliseconds
    context_type = models.CharField(max_length=50, blank=True)  # playlist, album, etc.
    context_id = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'listening_history'
        ordering = ['-played_at']

    def __str__(self):
        return f"{self.user.username} played {self.track_name} at {self.played_at}"
