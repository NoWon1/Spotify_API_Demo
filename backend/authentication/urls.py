from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.get_auth_url, name='get_auth_url'),
    path('callback/', views.callback, name='spotify_callback'),
    path('profile/', views.user_profile, name='user_profile'),
    path('refresh/', views.refresh_token, name='refresh_token'),
    path('logout/', views.logout_view, name='logout'),
]
