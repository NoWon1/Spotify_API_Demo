from django.urls import path 
from .import views
app_name = 'music_world'
urlpatterns = [
    path('', views.home, name='home'), 
    path('playlist/<str:id>/', views.playlist, name='playlist'),
    path('artist/<str:id>/', views.artist, name='artist'),
    path('sartist/', views.sartist, name='sartist'),
    path('audio/<str:id>/', views.audio, name='audio'),
    path('album/<str:id>/', views.album, name='album'),
    ]