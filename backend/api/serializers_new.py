from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    UserProfile, SpotifyToken, UserPlaylist, UserTrack, 
    UserArtist, UserAlbum, SearchHistory, UserRecommendation, ListeningHistory
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 'user', 'spotify_id', 'display_name', 'email', 
            'country', 'profile_image', 'followers', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class SpotifyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyToken
        fields = [
            'id', 'user', 'token_type', 'expires_in', 'scope', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']
        # Exclude sensitive token fields from serialization


class UserPlaylistSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPlaylist
        fields = [
            'id', 'playlist_id', 'name', 'description', 'image_url',
            'total_tracks', 'owner_name', 'owner_id', 'public', 
            'collaborative', 'followers', 'external_urls', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserTrackSerializer(serializers.ModelSerializer):
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = UserTrack
        fields = [
            'id', 'track_id', 'name', 'artist_name', 'artist_id',
            'album_name', 'album_id', 'image_url', 'duration_ms',
            'duration_formatted', 'popularity', 'preview_url', 'explicit',
            'external_urls', 'audio_features', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'duration_formatted']

    def get_duration_formatted(self, obj):
        """Convert duration from milliseconds to MM:SS format"""
        if obj.duration_ms:
            minutes = obj.duration_ms // 60000
            seconds = (obj.duration_ms % 60000) // 1000
            return f"{minutes}:{seconds:02d}"
        return "0:00"

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserArtistSerializer(serializers.ModelSerializer):
    followers_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = UserArtist
        fields = [
            'id', 'artist_id', 'name', 'image_url', 'followers',
            'followers_formatted', 'popularity', 'genres', 
            'external_urls', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'followers_formatted']

    def get_followers_formatted(self, obj):
        """Format followers count in a human-readable way"""
        if obj.followers >= 1000000:
            return f"{obj.followers / 1000000:.1f}M"
        elif obj.followers >= 1000:
            return f"{obj.followers / 1000:.1f}K"
        return str(obj.followers)

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserAlbumSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAlbum
        fields = [
            'id', 'album_id', 'name', 'artist_name', 'artist_id',
            'image_url', 'total_tracks', 'release_date', 'album_type',
            'external_urls', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = [
            'id', 'query', 'search_type', 'result_count', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class UserRecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRecommendation
        fields = [
            'id', 'item_type', 'item_id', 'item_name', 'score',
            'reason', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at']


class ListeningHistorySerializer(serializers.ModelSerializer):
    duration_formatted = serializers.SerializerMethodField()
    
    class Meta:
        model = ListeningHistory
        fields = [
            'id', 'track_id', 'track_name', 'artist_name', 'played_at',
            'duration_played', 'duration_formatted', 'context_type', 
            'context_id', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'created_at', 'duration_formatted']

    def get_duration_formatted(self, obj):
        """Convert duration from milliseconds to MM:SS format"""
        if obj.duration_played:
            minutes = obj.duration_played // 60000
            seconds = (obj.duration_played % 60000) // 1000
            return f"{minutes}:{seconds:02d}"
        return "0:00"

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


# Spotify API response serializers (for external data)
class SpotifyArtistSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    genres = serializers.ListField(child=serializers.CharField(), required=False)
    popularity = serializers.IntegerField(required=False)
    followers = serializers.DictField(required=False)
    images = serializers.ListField(required=False)
    external_urls = serializers.DictField(required=False)


class SpotifyTrackSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    artists = SpotifyArtistSerializer(many=True)
    album = serializers.DictField(required=False)
    duration_ms = serializers.IntegerField()
    explicit = serializers.BooleanField(required=False)
    popularity = serializers.IntegerField(required=False)
    preview_url = serializers.URLField(required=False, allow_null=True)
    external_urls = serializers.DictField(required=False)


class SpotifyAlbumSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    artists = SpotifyArtistSerializer(many=True)
    album_type = serializers.CharField(required=False)
    total_tracks = serializers.IntegerField(required=False)
    release_date = serializers.CharField(required=False)
    images = serializers.ListField(required=False)
    external_urls = serializers.DictField(required=False)


class SpotifyPlaylistSerializer(serializers.Serializer):
    id = serializers.CharField()
    name = serializers.CharField()
    description = serializers.CharField(required=False, allow_null=True)
    owner = serializers.DictField(required=False)
    public = serializers.BooleanField(required=False)
    collaborative = serializers.BooleanField(required=False)
    tracks = serializers.DictField(required=False)
    images = serializers.ListField(required=False)
    external_urls = serializers.DictField(required=False)
    followers = serializers.DictField(required=False)


class AudioFeaturesSerializer(serializers.Serializer):
    danceability = serializers.FloatField()
    energy = serializers.FloatField()
    key = serializers.IntegerField()
    loudness = serializers.FloatField()
    mode = serializers.IntegerField()
    speechiness = serializers.FloatField()
    acousticness = serializers.FloatField()
    instrumentalness = serializers.FloatField()
    liveness = serializers.FloatField()
    valence = serializers.FloatField()
    tempo = serializers.FloatField()
    time_signature = serializers.IntegerField()
