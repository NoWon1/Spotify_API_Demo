from django.urls import path
from . import views

urlpatterns = [
    # Dashboard & User Profile
    path('dashboard/', views.dashboard, name='dashboard'),
    path('playlists/', views.user_playlists, name='user_playlists'),
    
    # Search
    path('search/', views.search, name='search'),
    path('search/history/', views.search_history, name='search_history'),
    
    # Tracks
    path('tracks/<str:track_id>/', views.track_detail, name='track_detail'),
    path('tracks/<str:track_id>/audio-features/', views.track_audio_features, name='track_audio_features'),
    
    # Artists
    path('artists/<str:artist_id>/', views.artist_detail, name='artist_detail'),
    path('artists/<str:artist_id>/albums/', views.artist_albums, name='artist_albums'),
    path('artists/<str:artist_id>/top-tracks/', views.artist_top_tracks, name='artist_top_tracks'),
    path('artists/<str:artist_id>/related/', views.related_artists, name='related_artists'),
    
    # Albums
    path('albums/<str:album_id>/', views.album_detail, name='album_detail'),
    path('albums/<str:album_id>/tracks/', views.album_tracks, name='album_tracks'),
    
    # Playlists
    path('playlists/<str:playlist_id>/', views.playlist_detail, name='playlist_detail'),
    path('playlists/<str:playlist_id>/tracks/', views.playlist_tracks, name='playlist_tracks'),
    path('playlists/create/', views.create_playlist, name='create_playlist'),
    
    # Browse
    path('browse/featured-playlists/', views.featured_playlists, name='featured_playlists'),
    path('browse/new-releases/', views.new_releases, name='new_releases'),
    path('browse/categories/', views.categories, name='categories'),
    
    # Library
    path('me/tracks/', views.saved_tracks, name='saved_tracks'),
    path('me/tracks/save/', views.save_tracks, name='save_tracks'),
    path('me/tracks/remove/', views.remove_saved_tracks, name='remove_saved_tracks'),
    
    # User Favorites (Local Database)
    path('favorites/tracks/', views.favorite_tracks, name='favorite_tracks'),
    path('favorites/tracks/add/', views.add_favorite_track, name='add_favorite_track'),
    path('favorites/tracks/<str:track_id>/remove/', views.remove_favorite_track, name='remove_favorite_track'),
]
