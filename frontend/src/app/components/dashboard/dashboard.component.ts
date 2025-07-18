import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { SpotifyService, DashboardData, SpotifyTrack, SpotifyArtist, SpotifyAlbum, SpotifyPlaylist } from '../../services/spotify.service';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-dashboard',
  template: `
    <div class="dashboard-container container">
      <!-- Welcome Header -->
      <div class="dashboard-header fade-in">
        <h1 class="text-primary">
          Welcome back, {{ getCurrentUserName() }}!
        </h1>
        <p class="text-secondary">
          Discover your personalized music experience
        </p>
      </div>

      <!-- Loading State -->
      <div class="loading-spinner" *ngIf="isLoading">
        <mat-spinner></mat-spinner>
        <p class="text-secondary">Loading your music data...</p>
      </div>

      <!-- Dashboard Content -->
      <div class="dashboard-content" *ngIf="!isLoading && dashboardData">
        
        <!-- Quick Stats -->
        <div class="stats-section fade-in">
          <div class="stats-grid">
            <div class="stat-card mat-elevation-2">
              <mat-icon class="stat-icon">library_music</mat-icon>
              <div class="stat-info">
                <span class="stat-number">{{ dashboardData.top_tracks?.length || 0 }}</span>
                <span class="stat-label">Top Tracks</span>
              </div>
            </div>
            <div class="stat-card mat-elevation-2">
              <mat-icon class="stat-icon">person</mat-icon>
              <div class="stat-info">
                <span class="stat-number">{{ dashboardData.top_artists?.length || 0 }}</span>
                <span class="stat-label">Top Artists</span>
              </div>
            </div>
            <div class="stat-card mat-elevation-2">
              <mat-icon class="stat-icon">album</mat-icon>
              <div class="stat-info">
                <span class="stat-number">{{ dashboardData.new_releases?.length || 0 }}</span>
                <span class="stat-label">New Releases</span>
              </div>
            </div>
            <div class="stat-card mat-elevation-2">
              <mat-icon class="stat-icon">playlist_play</mat-icon>
              <div class="stat-info">
                <span class="stat-number">{{ dashboardData.featured_playlists?.length || 0 }}</span>
                <span class="stat-label">Featured Playlists</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Top Tracks Section -->
        <div class="section fade-in" *ngIf="dashboardData.top_tracks?.length">
          <div class="section-header">
            <h2 class="text-primary">Your Top Tracks</h2>
            <button mat-button class="view-all-btn" (click)="viewAllTracks()">
              View All
              <mat-icon>arrow_forward</mat-icon>
            </button>
          </div>
          <div class="tracks-grid">
            <div 
              class="track-card mat-elevation-2"
              *ngFor="let track of dashboardData.top_tracks.slice(0, 6)"
              (click)="goToTrack(track.id)">
              <img 
                [src]="spotifyService.getImageUrl(track.album?.images || [], 'medium')" 
                [alt]="track.name"
                class="track-image">
              <div class="track-info">
                <span class="track-name text-primary">{{ track.name }}</span>
                <span class="track-artist text-secondary">{{ getArtistNames(track.artists) }}</span>
                <span class="track-duration text-secondary">
                  {{ spotifyService.formatDuration(track.duration_ms) }}
                </span>
              </div>
              <button mat-icon-button class="play-btn" (click)="$event.stopPropagation(); playTrack(track)">
                <mat-icon>play_arrow</mat-icon>
              </button>
            </div>
          </div>
        </div>

        <!-- Top Artists Section -->
        <div class="section fade-in" *ngIf="dashboardData.top_artists?.length">
          <div class="section-header">
            <h2 class="text-primary">Your Top Artists</h2>
            <button mat-button class="view-all-btn" (click)="viewAllArtists()">
              View All
              <mat-icon>arrow_forward</mat-icon>
            </button>
          </div>
          <div class="artists-grid">
            <div 
              class="artist-card mat-elevation-2"
              *ngFor="let artist of dashboardData.top_artists.slice(0, 6)"
              (click)="goToArtist(artist.id)">
              <img 
                [src]="spotifyService.getImageUrl(artist.images, 'medium')" 
                [alt]="artist.name"
                class="artist-image">
              <div class="artist-info">
                <span class="artist-name text-primary">{{ artist.name }}</span>
                <span class="artist-followers text-secondary">
                  {{ spotifyService.formatFollowers(artist.followers?.total || 0) }} followers
                </span>
                <div class="artist-genres">
                  <mat-chip 
                    *ngFor="let genre of artist.genres?.slice(0, 2)"
                    class="genre-chip">
                    {{ genre }}
                  </mat-chip>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Recently Played Section -->
        <div class="section fade-in" *ngIf="dashboardData.recently_played?.length">
          <div class="section-header">
            <h2 class="text-primary">Recently Played</h2>
          </div>
          <div class="recent-tracks">
            <div 
              class="recent-track-item"
              *ngFor="let track of dashboardData.recently_played.slice(0, 8)"
              (click)="goToTrack(track.id)">
              <img 
                [src]="spotifyService.getImageUrl(track.album?.images || [], 'small')" 
                [alt]="track.name"
                class="recent-track-image">
              <div class="recent-track-info">
                <span class="track-name text-primary">{{ track.name }}</span>
                <span class="track-artist text-secondary">{{ getArtistNames(track.artists) }}</span>
              </div>
              <span class="track-duration text-secondary">
                {{ spotifyService.formatDuration(track.duration_ms) }}
              </span>
            </div>
          </div>
        </div>

        <!-- New Releases Section -->
        <div class="section fade-in" *ngIf="dashboardData.new_releases?.length">
          <div class="section-header">
            <h2 class="text-primary">New Releases</h2>
            <button mat-button class="view-all-btn" (click)="viewBrowse()">
              View All
              <mat-icon>arrow_forward</mat-icon>
            </button>
          </div>
          <div class="albums-grid">
            <div 
              class="album-card mat-elevation-2"
              *ngFor="let album of dashboardData.new_releases.slice(0, 6)"
              (click)="goToAlbum(album.id)">
              <img 
                [src]="spotifyService.getImageUrl(album.images, 'medium')" 
                [alt]="album.name"
                class="album-image">
              <div class="album-info">
                <span class="album-name text-primary">{{ album.name }}</span>
                <span class="album-artist text-secondary">{{ getArtistNames(album.artists) }}</span>
                <span class="album-year text-secondary">{{ getYear(album.release_date) }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Featured Playlists Section -->
        <div class="section fade-in" *ngIf="dashboardData.featured_playlists?.length">
          <div class="section-header">
            <h2 class="text-primary">Featured Playlists</h2>
            <button mat-button class="view-all-btn" (click)="viewBrowse()">
              View All
              <mat-icon>arrow_forward</mat-icon>
            </button>
          </div>
          <div class="playlists-grid">
            <div 
              class="playlist-card mat-elevation-2"
              *ngFor="let playlist of dashboardData.featured_playlists.slice(0, 6)"
              (click)="goToPlaylist(playlist.id)">
              <img 
                [src]="spotifyService.getImageUrl(playlist.images, 'medium')" 
                [alt]="playlist.name"
                class="playlist-image">
              <div class="playlist-info">
                <span class="playlist-name text-primary">{{ playlist.name }}</span>
                <span class="playlist-description text-secondary">{{ playlist.description }}</span>
                <span class="playlist-tracks text-secondary">{{ playlist.tracks?.total }} tracks</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Error State -->
      <div class="error-state text-center" *ngIf="!isLoading && !dashboardData">
        <mat-icon class="error-icon">error_outline</mat-icon>
        <h3 class="text-primary">Unable to load dashboard</h3>
        <p class="text-secondary">Please check your connection and try again.</p>
        <button mat-raised-button color="primary" (click)="loadDashboard()">
          Retry
        </button>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 24px;
      max-width: 1400px;
    }

    .dashboard-header {
      margin-bottom: 32px;
      text-align: center;
    }

    .dashboard-header h1 {
      font-size: 32px;
      font-weight: 300;
      margin-bottom: 8px;
    }

    .dashboard-header p {
      font-size: 16px;
    }

    .stats-section {
      margin-bottom: 40px;
    }

    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .stat-card {
      background: var(--background-light);
      padding: 20px;
      border-radius: 12px;
      display: flex;
      align-items: center;
      gap: 16px;
      transition: transform 0.2s ease;
    }

    .stat-card:hover {
      transform: translateY(-2px);
    }

    .stat-icon {
      font-size: 32px;
      height: 32px;
      width: 32px;
      color: var(--spotify-green);
    }

    .stat-info {
      display: flex;
      flex-direction: column;
    }

    .stat-number {
      font-size: 24px;
      font-weight: 600;
      color: var(--text-primary);
    }

    .stat-label {
      font-size: 12px;
      color: var(--text-secondary);
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    .section {
      margin-bottom: 40px;
    }

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
    }

    .section-header h2 {
      font-size: 24px;
      font-weight: 400;
      margin: 0;
    }

    .view-all-btn {
      color: var(--spotify-green) !important;
    }

    .view-all-btn mat-icon {
      margin-left: 4px;
      font-size: 18px;
      height: 18px;
      width: 18px;
    }

    /* Track Cards */
    .tracks-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 16px;
    }

    .track-card {
      background: var(--background-light);
      border-radius: 8px;
      padding: 16px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
      position: relative;
    }

    .track-card:hover {
      transform: translateY(-2px);
      background: rgba(255,255,255,0.1);
    }

    .track-image {
      width: 60px;
      height: 60px;
      border-radius: 6px;
      object-fit: cover;
    }

    .track-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 4px;
      min-width: 0;
    }

    .track-name {
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .track-artist, .track-duration {
      font-size: 14px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .play-btn {
      opacity: 0;
      transition: opacity 0.2s ease;
      color: var(--spotify-green) !important;
    }

    .track-card:hover .play-btn {
      opacity: 1;
    }

    /* Artist Cards */
    .artists-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .artist-card {
      background: var(--background-light);
      border-radius: 8px;
      padding: 16px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .artist-card:hover {
      transform: translateY(-2px);
      background: rgba(255,255,255,0.1);
    }

    .artist-image {
      width: 120px;
      height: 120px;
      border-radius: 50%;
      object-fit: cover;
      margin-bottom: 12px;
    }

    .artist-name {
      font-weight: 500;
      font-size: 16px;
      display: block;
      margin-bottom: 4px;
    }

    .artist-followers {
      font-size: 14px;
      display: block;
      margin-bottom: 8px;
    }

    .artist-genres {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      justify-content: center;
    }

    .genre-chip {
      font-size: 10px !important;
      height: 20px !important;
      background: rgba(29,185,84,0.2) !important;
      color: var(--spotify-green) !important;
    }

    /* Recent Tracks */
    .recent-tracks {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .recent-track-item {
      background: var(--background-light);
      border-radius: 6px;
      padding: 12px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }

    .recent-track-item:hover {
      background: rgba(255,255,255,0.1);
    }

    .recent-track-image {
      width: 40px;
      height: 40px;
      border-radius: 4px;
      object-fit: cover;
    }

    .recent-track-info {
      flex: 1;
      min-width: 0;
    }

    .recent-track-info .track-name {
      font-size: 14px;
      font-weight: 500;
    }

    .recent-track-info .track-artist {
      font-size: 12px;
    }

    /* Album Cards */
    .albums-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .album-card {
      background: var(--background-light);
      border-radius: 8px;
      padding: 16px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .album-card:hover {
      transform: translateY(-2px);
      background: rgba(255,255,255,0.1);
    }

    .album-image {
      width: 150px;
      height: 150px;
      border-radius: 6px;
      object-fit: cover;
      margin-bottom: 12px;
    }

    .album-name {
      font-weight: 500;
      font-size: 14px;
      display: block;
      margin-bottom: 4px;
    }

    .album-artist, .album-year {
      font-size: 12px;
      display: block;
      margin-bottom: 2px;
    }

    /* Playlist Cards */
    .playlists-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .playlist-card {
      background: var(--background-light);
      border-radius: 8px;
      padding: 16px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .playlist-card:hover {
      transform: translateY(-2px);
      background: rgba(255,255,255,0.1);
    }

    .playlist-image {
      width: 150px;
      height: 150px;
      border-radius: 6px;
      object-fit: cover;
      margin-bottom: 12px;
    }

    .playlist-name {
      font-weight: 500;
      font-size: 14px;
      display: block;
      margin-bottom: 4px;
    }

    .playlist-description {
      font-size: 12px;
      display: block;
      margin-bottom: 4px;
      opacity: 0.8;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    .playlist-tracks {
      font-size: 12px;
      display: block;
    }

    .error-state {
      padding: 40px;
    }

    .error-icon {
      font-size: 48px;
      height: 48px;
      width: 48px;
      color: var(--text-secondary);
      margin-bottom: 16px;
    }

    @media (max-width: 768px) {
      .dashboard-container {
        padding: 16px;
      }

      .section-header {
        flex-direction: column;
        align-items: flex-start;
        gap: 8px;
      }

      .stats-grid {
        grid-template-columns: 1fr 1fr;
        gap: 12px;
      }

      .stat-card {
        padding: 16px;
      }

      .tracks-grid,
      .artists-grid,
      .albums-grid,
      .playlists-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
      }

      .artist-image,
      .album-image,
      .playlist-image {
        width: 100px;
        height: 100px;
      }
    }
  `]
})
export class DashboardComponent implements OnInit {
  dashboardData: DashboardData | null = null;
  isLoading = false;

  constructor(
    public spotifyService: SpotifyService,
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.loadDashboard();
  }

  /**
   * Load dashboard data
   */
  loadDashboard(): void {
    this.isLoading = true;
    
    this.spotifyService.getDashboardData().subscribe({
      next: (data) => {
        this.dashboardData = data;
        this.isLoading = false;
      },
      error: (error) => {
        console.error('Failed to load dashboard:', error);
        this.isLoading = false;
        this.snackBar.open('Failed to load dashboard data', 'Close', {
          duration: 5000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  /**
   * Get current user name
   */
  getCurrentUserName(): string {
    const user = this.authService.getCurrentUser();
    return user?.display_name || 'Music Lover';
  }

  /**
   * Get artist names as comma-separated string
   */
  getArtistNames(artists: SpotifyArtist[]): string {
    return artists?.map(artist => artist.name).join(', ') || 'Unknown Artist';
  }

  /**
   * Get year from date string
   */
  getYear(dateString: string): string {
    return new Date(dateString).getFullYear().toString();
  }

  /**
   * Navigate to track detail
   */
  goToTrack(trackId: string): void {
    this.router.navigate(['/track', trackId]);
  }

  /**
   * Navigate to artist detail
   */
  goToArtist(artistId: string): void {
    this.router.navigate(['/artist', artistId]);
  }

  /**
   * Navigate to album detail
   */
  goToAlbum(albumId: string): void {
    this.router.navigate(['/album', albumId]);
  }

  /**
   * Navigate to playlist detail
   */
  goToPlaylist(playlistId: string): void {
    this.router.navigate(['/playlist', playlistId]);
  }

  /**
   * Play track (placeholder)
   */
  playTrack(track: SpotifyTrack): void {
    if (track.preview_url) {
      // In a real app, this would play the preview
      this.snackBar.open(`Playing preview of "${track.name}"`, 'Close', {
        duration: 3000
      });
    } else {
      this.snackBar.open('No preview available for this track', 'Close', {
        duration: 3000
      });
    }
  }

  /**
   * View all tracks
   */
  viewAllTracks(): void {
    this.router.navigate(['/library'], { queryParams: { section: 'tracks' } });
  }

  /**
   * View all artists
   */
  viewAllArtists(): void {
    this.router.navigate(['/library'], { queryParams: { section: 'artists' } });
  }

  /**
   * View browse page
   */
  viewBrowse(): void {
    this.router.navigate(['/browse']);
  }
}
