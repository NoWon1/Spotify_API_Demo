from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import SpotifyToken, UserProfile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'spotify_id', 'display_name', 'email', 'country', 
            'followers', 'profile_image'
        ]


class SpotifyTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpotifyToken
        fields = ['token_type', 'expires_in', 'scope', 'created_at', 'updated_at']


class UserProfileDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    profile = UserProfileSerializer(read_only=True)
    spotify_token = SpotifyTokenSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['user', 'profile', 'spotify_token']
        
    def to_representation(self, instance):
        data = {
            'user': UserSerializer(instance).data,
            'profile': UserProfileSerializer(instance.profile).data if hasattr(instance, 'profile') else None,
            'spotify_token': SpotifyTokenSerializer(instance.spotify_token).data if hasattr(instance, 'spotify_token') else None
        }
        return data
