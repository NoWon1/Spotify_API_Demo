from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.conf import settings
import uuid

from .services import SpotifyService
from .serializers import UserProfileDetailSerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def get_auth_url(request):
    """Get Spotify authorization URL"""
    state = str(uuid.uuid4())
    request.session['oauth_state'] = state
    auth_url = SpotifyService.get_auth_url(state)
    
    return Response({
        'auth_url': auth_url,
        'state': state
    })


@api_view(['POST'])
@permission_classes([AllowAny])
def callback(request):
    """Handle Spotify OAuth callback"""
    code = request.data.get('code')
    state = request.data.get('state')
    
    # Verify state parameter
    session_state = request.session.get('oauth_state')
    if state != session_state:
        return Response({'error': 'Invalid state parameter'}, status=status.HTTP_400_BAD_REQUEST)
    
    if not code:
        return Response({'error': 'Authorization code not provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Exchange code for token
        token_data = SpotifyService.exchange_code_for_token(code)
        
        if 'error' in token_data:
            return Response({'error': token_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Get user profile from Spotify
        profile_data = SpotifyService.get_user_profile(token_data['access_token'])
        
        if 'error' in profile_data:
            return Response({'error': 'Failed to get user profile'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create or get user
        spotify_id = profile_data['id']
        email = profile_data.get('email', f"{spotify_id}@spotify.local")
        
        user, created = User.objects.get_or_create(
            username=spotify_id,
            defaults={
                'email': email,
                'first_name': profile_data.get('display_name', '').split()[0] if profile_data.get('display_name') else '',
                'last_name': ' '.join(profile_data.get('display_name', '').split()[1:]) if profile_data.get('display_name') else ''
            }
        )
        
        # Save tokens and profile
        SpotifyService.save_user_token(user, token_data)
        SpotifyService.save_user_profile(user, profile_data)
        
        # Create or get auth token
        auth_token, _ = Token.objects.get_or_create(user=user)
        
        # Login user
        login(request, user)
        
        # Clean up session
        if 'oauth_state' in request.session:
            del request.session['oauth_state']
        
        return Response({
            'token': auth_token.key,
            'user': UserProfileDetailSerializer(user).data,
            'message': 'Successfully authenticated with Spotify'
        })
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """Get current user profile"""
    serializer = UserProfileDetailSerializer(request.user)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token(request):
    """Refresh Spotify access token"""
    try:
        spotify_token = request.user.spotify_token
        token_data = SpotifyService.refresh_access_token(spotify_token.refresh_token)
        
        if 'error' in token_data:
            return Response({'error': token_data['error']}, status=status.HTTP_400_BAD_REQUEST)
        
        # Update token
        SpotifyService.save_user_token(request.user, token_data)
        
        return Response({'message': 'Token refreshed successfully'})
        
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Logout user"""
    logout(request)
    return Response({'message': 'Successfully logged out'})
