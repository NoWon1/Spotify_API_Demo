from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404

from .services import SpotifyAPIService
from .models import UserPlaylist, UserTrack, UserArtist, SearchHistory
from .serializers import (
    UserPlaylistSerializer, UserTrackSerializer, UserArtistSerializer,
    SearchHistorySerializer, SpotifyTrackSerializer, SpotifyArtistSerializer,
    SpotifyAlbumSerializer, SpotifyPlaylistSerializer, AudioFeaturesSerializer,
    SearchResultSerializer
)


# User Profile & Dashboard Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard(request):
    """Get user dashboard data"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        
        # Get user's top tracks, artists, and recent activity
        top_tracks = spotify_service.get_user_top_tracks(limit=10)
        top_artists = spotify_service.get_user_top_artists(limit=10)
        recently_played = spotify_service.get_recently_played(limit=10)
        featured_playlists = spotify_service.get_featured_playlists(limit=6)
        new_releases = spotify_service.get_new_releases(limit=6)
        
        return Response({
            'top_tracks': top_tracks,
            'top_artists': top_artists,
            'recently_played': recently_played,
            'featured_playlists': featured_playlists,
            'new_releases': new_releases
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_playlists(request):
    """Get user's playlists"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        
        playlists = spotify_service.get_user_playlists(limit=limit, offset=offset)
        return Response(playlists)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Search Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search(request):
    """Search for tracks, artists, albums, or playlists"""
    try:
        query = request.GET.get('q', '')
        search_type = request.GET.get('type', 'track')
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        
        if not query:
            return Response({'error': 'Query parameter is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        spotify_service = SpotifyAPIService(request.user)
        results = spotify_service.search(query, search_type, limit, offset)
        
        # Save search history
        SearchHistory.objects.create(
            user=request.user,
            query=query,
            search_type=search_type,
            result_count=results.get(f'{search_type}s', {}).get('total', 0)
        )
        
        return Response(results)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def search_history(request):
    """Get user's search history"""
    try:
        history = SearchHistory.objects.filter(user=request.user)[:20]
        serializer = SearchHistorySerializer(history, many=True)
        return Response(serializer.data)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Track Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_detail(request, track_id):
    """Get track details"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        track = spotify_service.get_track(track_id)
        return Response(track)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def track_audio_features(request, track_id):
    """Get track audio features"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        features = spotify_service.get_track_audio_features(track_id)
        return Response(features)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Artist Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def artist_detail(request, artist_id):
    """Get artist details"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        artist = spotify_service.get_artist(artist_id)
        return Response(artist)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def artist_albums(request, artist_id):
    """Get artist's albums"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        albums = spotify_service.get_artist_albums(artist_id, limit)
        return Response(albums)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def artist_top_tracks(request, artist_id):
    """Get artist's top tracks"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        market = request.GET.get('market', 'US')
        tracks = spotify_service.get_artist_top_tracks(artist_id, market)
        return Response(tracks)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def related_artists(request, artist_id):
    """Get related artists"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        artists = spotify_service.get_related_artists(artist_id)
        return Response(artists)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Album Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def album_detail(request, album_id):
    """Get album details"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        album = spotify_service.get_album(album_id)
        return Response(album)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def album_tracks(request, album_id):
    """Get album tracks"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        tracks = spotify_service.get_album_tracks(album_id, limit)
        return Response(tracks)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Playlist Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def playlist_detail(request, playlist_id):
    """Get playlist details"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        playlist = spotify_service.get_playlist(playlist_id)
        return Response(playlist)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def playlist_tracks(request, playlist_id):
    """Get playlist tracks"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        tracks = spotify_service.get_playlist_tracks(playlist_id, limit, offset)
        return Response(tracks)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_playlist(request):
    """Create a new playlist"""
    try:
        name = request.data.get('name')
        description = request.data.get('description', '')
        public = request.data.get('public', True)
        
        if not name:
            return Response({'error': 'Playlist name is required'}, status=status.HTTP_400_BAD_REQUEST)
        
        spotify_service = SpotifyAPIService(request.user)
        playlist = spotify_service.create_playlist(name, description, public)
        return Response(playlist)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Browse Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def featured_playlists(request):
    """Get featured playlists"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        playlists = spotify_service.get_featured_playlists(limit)
        return Response(playlists)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def new_releases(request):
    """Get new album releases"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        albums = spotify_service.get_new_releases(limit)
        return Response(albums)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def categories(request):
    """Get browse categories"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        categories = spotify_service.get_categories(limit)
        return Response(categories)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Library Views
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def saved_tracks(request):
    """Get user's saved tracks"""
    try:
        spotify_service = SpotifyAPIService(request.user)
        limit = int(request.GET.get('limit', 20))
        offset = int(request.GET.get('offset', 0))
        tracks = spotify_service.get_saved_tracks(limit, offset)
        return Response(tracks)
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_tracks(request):
    """Save tracks to user's library"""
    try:
        track_ids = request.data.get('track_ids', [])
        if not track_ids:
            return Response({'error': 'Track IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        spotify_service = SpotifyAPIService(request.user)
        result = spotify_service.save_tracks(track_ids)
        return Response({'message': 'Tracks saved successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_saved_tracks(request):
    """Remove tracks from user's library"""
    try:
        track_ids = request.data.get('track_ids', [])
        if not track_ids:
            return Response({'error': 'Track IDs are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        spotify_service = SpotifyAPIService(request.user)
        result = spotify_service.remove_saved_tracks(track_ids)
        return Response({'message': 'Tracks removed successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# User Favorites Management
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def favorite_tracks(request):
    """Get user's favorite tracks"""
    favorites = UserTrack.objects.filter(user=request.user)
    serializer = UserTrackSerializer(favorites, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_favorite_track(request):
    """Add track to favorites"""
    serializer = UserTrackSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_favorite_track(request, track_id):
    """Remove track from favorites"""
    try:
        track = UserTrack.objects.get(user=request.user, track_id=track_id)
        track.delete()
        return Response({'message': 'Track removed from favorites'})
    except UserTrack.DoesNotExist:
        return Response({'error': 'Track not found in favorites'}, status=status.HTTP_404_NOT_FOUND)
