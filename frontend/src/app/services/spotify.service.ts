import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';
import { AuthService } from './auth.service';

// Spotify API Interfaces
export interface SpotifyTrack {
  id: string;
  name: string;
  artists: SpotifyArtist[];
  album: SpotifyAlbum;
  duration_ms: number;
  external_urls: { spotify: string };
  preview_url: string | null;
  popularity: number;
  track_number: number;
  uri: string;
}

export interface SpotifyArtist {
  id: string;
  name: string;
  images: SpotifyImage[];
  genres: string[];
  popularity: number;
  followers: { total: number };
  external_urls: { spotify: string };
  uri: string;
}

export interface SpotifyAlbum {
  id: string;
  name: string;
  artists: SpotifyArtist[];
  images: SpotifyImage[];
  release_date: string;
  total_tracks: number;
  external_urls: { spotify: string };
  uri: string;
}

export interface SpotifyPlaylist {
  id: string;
  name: string;
  description: string;
  images: SpotifyImage[];
  owner: { id: string; display_name: string };
  tracks: { total: number };
  external_urls: { spotify: string };
  uri: string;
  public: boolean;
}

export interface SpotifyImage {
  url: string;
  height: number;
  width: number;
}

export interface AudioFeatures {
  id: string;
  acousticness: number;
  danceability: number;
  energy: number;
  instrumentalness: number;
  key: number;
  liveness: number;
  loudness: number;
  mode: number;
  speechiness: number;
  tempo: number;
  time_signature: number;
  valence: number;
}

export interface SearchResult {
  tracks?: { items: SpotifyTrack[]; total: number };
  artists?: { items: SpotifyArtist[]; total: number };
  albums?: { items: SpotifyAlbum[]; total: number };
  playlists?: { items: SpotifyPlaylist[]; total: number };
}

export interface DashboardData {
  top_tracks: SpotifyTrack[];
  top_artists: SpotifyArtist[];
  recently_played: SpotifyTrack[];
  featured_playlists: SpotifyPlaylist[];
  new_releases: SpotifyAlbum[];
}

@Injectable({
  providedIn: 'root'
})
export class SpotifyService {
  private readonly API_BASE_URL = 'http://localhost:8000/api';

  constructor(
    private http: HttpClient,
    private authService: AuthService
  ) {}

  /**
   * Get dashboard data with user's top content and recommendations
   */
  getDashboardData(): Observable<DashboardData> {
    return this.http.get<DashboardData>(`${this.API_BASE_URL}/dashboard/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Search for tracks, artists, albums, or playlists
   */
  search(query: string, type: string = 'track', limit: number = 20, offset: number = 0): Observable<SearchResult> {
    const params = new HttpParams()
      .set('q', query)
      .set('type', type)
      .set('limit', limit.toString())
      .set('offset', offset.toString());

    return this.http.get<SearchResult>(`${this.API_BASE_URL}/search/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get search history
   */
  getSearchHistory(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_BASE_URL}/search/history/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get track details
   */
  getTrack(trackId: string): Observable<SpotifyTrack> {
    return this.http.get<SpotifyTrack>(`${this.API_BASE_URL}/tracks/${trackId}/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get track audio features
   */
  getTrackAudioFeatures(trackId: string): Observable<AudioFeatures> {
    return this.http.get<AudioFeatures>(`${this.API_BASE_URL}/tracks/${trackId}/audio-features/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get artist details
   */
  getArtist(artistId: string): Observable<SpotifyArtist> {
    return this.http.get<SpotifyArtist>(`${this.API_BASE_URL}/artists/${artistId}/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get artist's albums
   */
  getArtistAlbums(artistId: string, limit: number = 20): Observable<{ items: SpotifyAlbum[] }> {
    const params = new HttpParams().set('limit', limit.toString());
    
    return this.http.get<{ items: SpotifyAlbum[] }>(`${this.API_BASE_URL}/artists/${artistId}/albums/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get artist's top tracks
   */
  getArtistTopTracks(artistId: string, market: string = 'US'): Observable<{ tracks: SpotifyTrack[] }> {
    const params = new HttpParams().set('market', market);
    
    return this.http.get<{ tracks: SpotifyTrack[] }>(`${this.API_BASE_URL}/artists/${artistId}/top-tracks/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get related artists
   */
  getRelatedArtists(artistId: string): Observable<{ artists: SpotifyArtist[] }> {
    return this.http.get<{ artists: SpotifyArtist[] }>(`${this.API_BASE_URL}/artists/${artistId}/related/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get album details
   */
  getAlbum(albumId: string): Observable<SpotifyAlbum> {
    return this.http.get<SpotifyAlbum>(`${this.API_BASE_URL}/albums/${albumId}/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get album tracks
   */
  getAlbumTracks(albumId: string, limit: number = 20): Observable<{ items: SpotifyTrack[] }> {
    const params = new HttpParams().set('limit', limit.toString());
    
    return this.http.get<{ items: SpotifyTrack[] }>(`${this.API_BASE_URL}/albums/${albumId}/tracks/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get playlist details
   */
  getPlaylist(playlistId: string): Observable<SpotifyPlaylist> {
    return this.http.get<SpotifyPlaylist>(`${this.API_BASE_URL}/playlists/${playlistId}/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get playlist tracks
   */
  getPlaylistTracks(playlistId: string, limit: number = 20, offset: number = 0): Observable<{ items: any[] }> {
    const params = new HttpParams()
      .set('limit', limit.toString())
      .set('offset', offset.toString());
    
    return this.http.get<{ items: any[] }>(`${this.API_BASE_URL}/playlists/${playlistId}/tracks/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Create a new playlist
   */
  createPlaylist(name: string, description: string = '', isPublic: boolean = true): Observable<SpotifyPlaylist> {
    const data = {
      name,
      description,
      public: isPublic
    };

    return this.http.post<SpotifyPlaylist>(`${this.API_BASE_URL}/playlists/create/`, data, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Get user's playlists
   */
  getUserPlaylists(limit: number = 20, offset: number = 0): Observable<{ items: SpotifyPlaylist[] }> {
    const params = new HttpParams()
      .set('limit', limit.toString())
      .set('offset', offset.toString());

    return this.http.get<{ items: SpotifyPlaylist[] }>(`${this.API_BASE_URL}/playlists/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get featured playlists
   */
  getFeaturedPlaylists(limit: number = 20): Observable<{ playlists: { items: SpotifyPlaylist[] } }> {
    const params = new HttpParams().set('limit', limit.toString());
    
    return this.http.get<{ playlists: { items: SpotifyPlaylist[] } }>(`${this.API_BASE_URL}/browse/featured-playlists/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get new album releases
   */
  getNewReleases(limit: number = 20): Observable<{ albums: { items: SpotifyAlbum[] } }> {
    const params = new HttpParams().set('limit', limit.toString());
    
    return this.http.get<{ albums: { items: SpotifyAlbum[] } }>(`${this.API_BASE_URL}/browse/new-releases/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get browse categories
   */
  getCategories(limit: number = 20): Observable<{ categories: { items: any[] } }> {
    const params = new HttpParams().set('limit', limit.toString());
    
    return this.http.get<{ categories: { items: any[] } }>(`${this.API_BASE_URL}/browse/categories/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Get user's saved tracks
   */
  getSavedTracks(limit: number = 20, offset: number = 0): Observable<{ items: any[] }> {
    const params = new HttpParams()
      .set('limit', limit.toString())
      .set('offset', offset.toString());

    return this.http.get<{ items: any[] }>(`${this.API_BASE_URL}/me/tracks/`, {
      headers: this.authService.getAuthHeaders(),
      params
    });
  }

  /**
   * Save tracks to user's library
   */
  saveTracks(trackIds: string[]): Observable<any> {
    return this.http.post(`${this.API_BASE_URL}/me/tracks/save/`, {
      track_ids: trackIds
    }, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Remove tracks from user's library
   */
  removeSavedTracks(trackIds: string[]): Observable<any> {
    return this.http.request('DELETE', `${this.API_BASE_URL}/me/tracks/remove/`, {
      headers: this.authService.getAuthHeaders(),
      body: { track_ids: trackIds }
    });
  }

  /**
   * Get user's favorite tracks (local database)
   */
  getFavoriteTracks(): Observable<any[]> {
    return this.http.get<any[]>(`${this.API_BASE_URL}/favorites/tracks/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Add track to favorites (local database)
   */
  addFavoriteTrack(track: any): Observable<any> {
    return this.http.post(`${this.API_BASE_URL}/favorites/tracks/add/`, track, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Remove track from favorites (local database)
   */
  removeFavoriteTrack(trackId: string): Observable<any> {
    return this.http.delete(`${this.API_BASE_URL}/favorites/tracks/${trackId}/remove/`, {
      headers: this.authService.getAuthHeaders()
    });
  }

  /**
   * Format duration from milliseconds to MM:SS
   */
  formatDuration(ms: number): string {
    const minutes = Math.floor(ms / 60000);
    const seconds = Math.floor((ms % 60000) / 1000);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  }

  /**
   * Format follower count with abbreviations
   */
  formatFollowers(count: number): string {
    if (count >= 1000000) {
      return `${(count / 1000000).toFixed(1)}M`;
    } else if (count >= 1000) {
      return `${(count / 1000).toFixed(1)}K`;
    }
    return count.toString();
  }

  /**
   * Get image URL with fallback
   */
  getImageUrl(images: SpotifyImage[], size: 'small' | 'medium' | 'large' = 'medium'): string {
    if (!images || images.length === 0) {
      return '/assets/images/placeholder.png';
    }

    const sizeIndex = {
      'small': images.length - 1,
      'medium': Math.floor(images.length / 2),
      'large': 0
    };

    const index = Math.max(0, Math.min(sizeIndex[size], images.length - 1));
    return images[index]?.url || '/assets/images/placeholder.png';
  }
}
