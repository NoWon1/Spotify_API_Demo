import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService, User } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-navigation',
  template: `
    <mat-sidenav-container class="sidenav-container bg-dark">
      <mat-sidenav
        #drawer
        class="sidenav bg-dark"
        fixedInViewport
        [attr.role]="'navigation'"
        [mode]="'side'"
        [opened]="true">
        
        <!-- Navigation Header -->
        <div class="nav-header">
          <div class="nav-logo">
            <mat-icon class="spotify-green">music_note</mat-icon>
            <span class="nav-title text-primary">Spotify Demo</span>
          </div>
          
          <div class="user-info" *ngIf="currentUser">
            <div class="user-avatar">
              <img 
                [src]="getUserAvatar()" 
                [alt]="currentUser.display_name"
                onerror="this.src='/assets/images/default-avatar.png'">
            </div>
            <div class="user-details">
              <span class="user-name text-primary">{{ currentUser.display_name }}</span>
              <span class="user-followers text-secondary">
                {{ formatFollowers(currentUser.followers?.total || 0) }} followers
              </span>
            </div>
          </div>
        </div>

        <!-- Navigation Menu -->
        <mat-nav-list class="nav-menu">
          <mat-list-item 
            routerLink="/dashboard" 
            routerLinkActive="active"
            class="nav-item">
            <mat-icon matListIcon>dashboard</mat-icon>
            <span matLine class="text-primary">Dashboard</span>
          </mat-list-item>

          <mat-list-item 
            routerLink="/search" 
            routerLinkActive="active"
            class="nav-item">
            <mat-icon matListIcon>search</mat-icon>
            <span matLine class="text-primary">Search</span>
          </mat-list-item>

          <mat-list-item 
            routerLink="/browse" 
            routerLinkActive="active"
            class="nav-item">
            <mat-icon matListIcon>explore</mat-icon>
            <span matLine class="text-primary">Browse</span>
          </mat-list-item>

          <mat-list-item 
            routerLink="/library" 
            routerLinkActive="active"
            class="nav-item">
            <mat-icon matListIcon>library_music</mat-icon>
            <span matLine class="text-primary">Your Library</span>
          </mat-list-item>

          <mat-divider class="nav-divider"></mat-divider>

          <!-- Quick Actions -->
          <div class="nav-section-title text-secondary">Quick Actions</div>
          
          <mat-list-item class="nav-item action-item" (click)="createPlaylist()">
            <mat-icon matListIcon>add</mat-icon>
            <span matLine class="text-primary">Create Playlist</span>
          </mat-list-item>

          <mat-list-item class="nav-item action-item" (click)="viewFavorites()">
            <mat-icon matListIcon>favorite</mat-icon>
            <span matLine class="text-primary">Liked Songs</span>
          </mat-list-item>

          <mat-divider class="nav-divider"></mat-divider>

          <!-- Recently Played -->
          <div class="nav-section-title text-secondary">Recently Played</div>
          
          <div class="recent-tracks" *ngIf="recentTracks.length > 0">
            <div 
              class="recent-track-item" 
              *ngFor="let track of recentTracks.slice(0, 3)"
              (click)="goToTrack(track.id)">
              <img 
                [src]="getTrackImage(track)" 
                [alt]="track.name"
                class="recent-track-image">
              <div class="recent-track-info">
                <span class="track-name text-primary">{{ track.name }}</span>
                <span class="track-artist text-secondary">{{ getArtistNames(track.artists) }}</span>
              </div>
            </div>
          </div>
        </mat-nav-list>

        <!-- Navigation Footer -->
        <div class="nav-footer">
          <button 
            mat-button 
            class="logout-btn"
            (click)="logout()"
            [disabled]="isLoggingOut">
            <mat-icon>logout</mat-icon>
            <span *ngIf="!isLoggingOut">Logout</span>
            <span *ngIf="isLoggingOut">Logging out...</span>
          </button>
        </div>
      </mat-sidenav>

      <mat-sidenav-content class="sidenav-content">
        <!-- Mobile Header -->
        <mat-toolbar class="mobile-header" *ngIf="isMobile">
          <button
            type="button"
            aria-label="Toggle sidenav"
            mat-icon-button
            (click)="drawer.toggle()">
            <mat-icon aria-label="Side nav toggle icon">menu</mat-icon>
          </button>
          <span class="nav-title">Spotify Demo</span>
        </mat-toolbar>

        <!-- Content will be projected here -->
        <ng-content></ng-content>
      </mat-sidenav-content>
    </mat-sidenav-container>
  `,
  styles: [`
    .sidenav-container {
      height: 100vh;
    }

    .sidenav {
      width: 240px;
      background-color: #191414 !important;
      border-right: 1px solid #282828;
    }

    .nav-header {
      padding: 20px 16px;
      border-bottom: 1px solid #282828;
    }

    .nav-logo {
      display: flex;
      align-items: center;
      gap: 8px;
      margin-bottom: 20px;
    }

    .nav-logo mat-icon {
      font-size: 24px;
      height: 24px;
      width: 24px;
    }

    .nav-title {
      font-size: 18px;
      font-weight: 500;
    }

    .user-info {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .user-avatar {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      overflow: hidden;
      background: #282828;
    }

    .user-avatar img {
      width: 100%;
      height: 100%;
      object-fit: cover;
    }

    .user-details {
      display: flex;
      flex-direction: column;
      flex: 1;
      min-width: 0;
    }

    .user-name {
      font-weight: 500;
      font-size: 14px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .user-followers {
      font-size: 12px;
    }

    .nav-menu {
      padding: 8px 0;
      flex: 1;
      overflow-y: auto;
    }

    .nav-item {
      height: 48px !important;
      margin: 2px 8px;
      border-radius: 8px;
      transition: background-color 0.2s ease;
      cursor: pointer;
    }

    .nav-item:hover {
      background-color: rgba(255,255,255,0.1) !important;
    }

    .nav-item.active {
      background-color: rgba(29,185,84,0.2) !important;
    }

    .nav-item.active .text-primary {
      color: #1db954 !important;
    }

    .nav-item.active mat-icon {
      color: #1db954 !important;
    }

    .nav-item mat-icon {
      color: #b3b3b3;
      transition: color 0.2s ease;
    }

    .action-item:hover mat-icon {
      color: #1db954 !important;
    }

    .nav-divider {
      background-color: #282828;
      margin: 16px 16px;
    }

    .nav-section-title {
      font-size: 12px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 1px;
      padding: 0 24px 8px 24px;
      margin-top: 8px;
    }

    .recent-tracks {
      padding: 0 8px;
    }

    .recent-track-item {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 8px;
      border-radius: 4px;
      cursor: pointer;
      transition: background-color 0.2s ease;
    }

    .recent-track-item:hover {
      background-color: rgba(255,255,255,0.1);
    }

    .recent-track-image {
      width: 32px;
      height: 32px;
      border-radius: 4px;
      object-fit: cover;
    }

    .recent-track-info {
      display: flex;
      flex-direction: column;
      flex: 1;
      min-width: 0;
    }

    .track-name {
      font-size: 12px;
      font-weight: 500;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .track-artist {
      font-size: 11px;
      white-space: nowrap;
      overflow: hidden;
      text-overflow: ellipsis;
    }

    .nav-footer {
      padding: 16px;
      border-top: 1px solid #282828;
    }

    .logout-btn {
      width: 100%;
      color: #b3b3b3 !important;
      justify-content: flex-start;
      text-transform: none;
      font-size: 14px;
    }

    .logout-btn:hover {
      background-color: rgba(255,255,255,0.1) !important;
      color: #ffffff !important;
    }

    .logout-btn mat-icon {
      margin-right: 8px;
    }

    .mobile-header {
      background-color: #191414 !important;
      display: none;
    }

    .sidenav-content {
      background-color: #121212;
    }

    @media (max-width: 768px) {
      .sidenav {
        width: 280px;
      }

      .mobile-header {
        display: flex !important;
      }

      .nav-header {
        padding-top: 0;
      }
    }
  `]
})
export class NavigationComponent implements OnInit {
  currentUser: User | null = null;
  recentTracks: any[] = [];
  isLoggingOut = false;
  isMobile = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Subscribe to user data
    this.authService.user$.subscribe(user => {
      this.currentUser = user;
    });

    // Load recent tracks (this would be implemented in a real app)
    this.loadRecentTracks();

    // Check if mobile
    this.checkIfMobile();
    window.addEventListener('resize', () => this.checkIfMobile());
  }

  /**
   * Get user avatar URL with fallback
   */
  getUserAvatar(): string {
    if (this.currentUser?.images && this.currentUser.images.length > 0) {
      return this.currentUser.images[0].url;
    }
    return '/assets/images/default-avatar.png';
  }

  /**
   * Format follower count
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
   * Get track image URL
   */
  getTrackImage(track: any): string {
    if (track.album?.images && track.album.images.length > 0) {
      return track.album.images[track.album.images.length - 1].url;
    }
    return '/assets/images/placeholder.png';
  }

  /**
   * Get artist names as comma-separated string
   */
  getArtistNames(artists: any[]): string {
    return artists?.map(artist => artist.name).join(', ') || 'Unknown Artist';
  }

  /**
   * Navigate to track detail
   */
  goToTrack(trackId: string): void {
    this.router.navigate(['/track', trackId]);
  }

  /**
   * Create new playlist
   */
  createPlaylist(): void {
    // This would open a dialog to create a playlist
    this.snackBar.open('Create playlist feature coming soon!', 'Close', {
      duration: 3000
    });
  }

  /**
   * View favorites
   */
  viewFavorites(): void {
    this.router.navigate(['/library'], { queryParams: { section: 'favorites' } });
  }

  /**
   * Logout user
   */
  logout(): void {
    this.isLoggingOut = true;
    
    this.authService.logout().subscribe({
      next: () => {
        this.router.navigate(['/login']);
        this.snackBar.open('Successfully logged out', 'Close', {
          duration: 3000
        });
      },
      error: (error) => {
        console.error('Logout failed:', error);
        this.isLoggingOut = false;
        // Still redirect to login even if logout API fails
        this.router.navigate(['/login']);
      },
      complete: () => {
        this.isLoggingOut = false;
      }
    });
  }

  /**
   * Load recent tracks (placeholder)
   */
  private loadRecentTracks(): void {
    // In a real implementation, this would fetch recent tracks from Spotify
    this.recentTracks = [];
  }

  /**
   * Check if device is mobile
   */
  private checkIfMobile(): void {
    this.isMobile = window.innerWidth <= 768;
  }
}
