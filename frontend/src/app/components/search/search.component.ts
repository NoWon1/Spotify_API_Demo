import { Component, OnInit } from '@angular/core';
import { FormControl } from '@angular/forms';
import { Router } from '@angular/router';
import { debounceTime, distinctUntilChanged, switchMap, catchError } from 'rxjs/operators';
import { of } from 'rxjs';
import { SpotifyService, SearchResult } from '../../services/spotify.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-search',
  template: `
    <div class="search-container container">
      <!-- Search Header -->
      <div class="search-header">
        <h1 class="text-primary">Search</h1>
        <p class="text-secondary">Find your favorite music, artists, albums, and playlists</p>
      </div>

      <!-- Search Bar -->
      <div class="search-bar-container">
        <mat-form-field class="search-bar" appearance="outline">
          <mat-label>Search for music...</mat-label>
          <input 
            matInput 
            [formControl]="searchControl"
            placeholder="Try 'Bohemian Rhapsody' or 'Queen'"
            autocomplete="off">
          <mat-icon matSuffix>search</mat-icon>
        </mat-form-field>

        <!-- Search Type Tabs -->
        <mat-tab-group 
          [(selectedIndex)]="selectedTabIndex" 
          (selectedTabChange)="onTabChange($event)"
          class="search-tabs">
          <mat-tab label="All"></mat-tab>
          <mat-tab label="Tracks"></mat-tab>
          <mat-tab label="Artists"></mat-tab>
          <mat-tab label="Albums"></mat-tab>
          <mat-tab label="Playlists"></mat-tab>
        </mat-tab-group>
      </div>

      <!-- Loading State -->
      <div class="loading-spinner" *ngIf="isSearching">
        <mat-spinner></mat-spinner>
        <p class="text-secondary">Searching...</p>
      </div>

      <!-- Search Results -->
      <div class="search-results" *ngIf="searchResults && !isSearching">
        
        <!-- Tracks Results -->
        <div class="results-section" *ngIf="searchResults.tracks?.items?.length">
          <h2 class="section-title text-primary">Tracks</h2>
          <div class="tracks-list">
            <div 
              class="track-item"
              *ngFor="let track of searchResults.tracks?.items?.slice(0, getResultLimit('tracks')) || []"
              (click)="goToTrack(track.id)">
              <img 
                [src]="spotifyService.getImageUrl(track.album?.images || [], 'small')" 
                [alt]="track.name"
                class="track-image">
              <div class="track-info">
                <span class="track-name text-primary">{{ track.name }}</span>
                <span class="track-artist text-secondary">{{ getArtistNames(track.artists) }}</span>
                <span class="track-album text-secondary">{{ track.album?.name }}</span>
              </div>
              <span class="track-duration text-secondary">
                {{ spotifyService.formatDuration(track.duration_ms) }}
              </span>
              <button 
                mat-icon-button 
                class="play-btn"
                (click)="$event.stopPropagation(); playTrack(track)">
                <mat-icon>play_arrow</mat-icon>
              </button>
            </div>
          </div>
          <button 
            *ngIf="searchResults.tracks?.items && (searchResults.tracks?.items?.length || 0) > getResultLimit('tracks')"
            mat-button 
            class="view-more-btn"
            (click)="viewMoreTracks()">
            View More Tracks
          </button>
        </div>

        <!-- Artists Results -->
        <div class="results-section" *ngIf="searchResults.artists?.items?.length">
          <h2 class="section-title text-primary">Artists</h2>
          <div class="artists-grid">
            <div 
              class="artist-card mat-elevation-2"
              *ngFor="let artist of searchResults.artists?.items?.slice(0, getResultLimit('artists')) || []"
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
                <div class="artist-genres" *ngIf="artist.genres?.length">
                  <mat-chip 
                    *ngFor="let genre of artist.genres.slice(0, 2)"
                    class="genre-chip">
                    {{ genre }}
                  </mat-chip>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Albums Results -->
        <div class="results-section" *ngIf="searchResults.albums?.items?.length">
          <h2 class="section-title text-primary">Albums</h2>
          <div class="albums-grid">
            <div 
              class="album-card mat-elevation-2"
              *ngFor="let album of searchResults.albums?.items?.slice(0, getResultLimit('albums')) || []"
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

        <!-- Playlists Results -->
        <div class="results-section" *ngIf="searchResults.playlists?.items?.length">
          <h2 class="section-title text-primary">Playlists</h2>
          <div class="playlists-grid">
            <div 
              class="playlist-card mat-elevation-2"
              *ngFor="let playlist of searchResults.playlists?.items?.slice(0, getResultLimit('playlists')) || []"
              (click)="goToPlaylist(playlist.id)">
              <img 
                [src]="spotifyService.getImageUrl(playlist.images, 'medium')" 
                [alt]="playlist.name"
                class="playlist-image">
              <div class="playlist-info">
                <span class="playlist-name text-primary">{{ playlist.name }}</span>
                <span class="playlist-owner text-secondary">By {{ playlist.owner?.display_name }}</span>
                <span class="playlist-tracks text-secondary">{{ playlist.tracks?.total }} tracks</span>
              </div>
            </div>
          </div>
        </div>

        <!-- No Results -->
        <div class="no-results text-center" *ngIf="hasSearched && !hasResults()">
          <mat-icon class="no-results-icon">search_off</mat-icon>
          <h3 class="text-primary">No results found</h3>
          <p class="text-secondary">
            Try different keywords or check your spelling
          </p>
        </div>
      </div>

      <!-- Search Suggestions -->
      <div class="search-suggestions" *ngIf="!hasSearched && !isSearching">
        <h2 class="section-title text-primary">Try searching for:</h2>
        <div class="suggestions-grid">
          <mat-chip 
            *ngFor="let suggestion of searchSuggestions"
            class="suggestion-chip"
            (click)="searchFor(suggestion)">
            {{ suggestion }}
          </mat-chip>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .search-container {
      padding: 24px;
      max-width: 1200px;
    }

    .search-header {
      text-align: center;
      margin-bottom: 32px;
    }

    .search-header h1 {
      font-size: 32px;
      font-weight: 300;
      margin-bottom: 8px;
    }

    .search-bar-container {
      margin-bottom: 32px;
    }

    .search-bar {
      width: 100%;
      max-width: 600px;
      margin: 0 auto 24px auto;
      display: block;
    }

    .search-tabs {
      max-width: 600px;
      margin: 0 auto;
    }

    .results-section {
      margin-bottom: 40px;
    }

    .section-title {
      font-size: 24px;
      font-weight: 400;
      margin-bottom: 20px;
    }

    /* Track Items */
    .tracks-list {
      display: flex;
      flex-direction: column;
      gap: 8px;
    }

    .track-item {
      background: var(--background-light);
      border-radius: 8px;
      padding: 12px;
      display: flex;
      align-items: center;
      gap: 12px;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .track-item:hover {
      background: rgba(255,255,255,0.1);
      transform: translateY(-1px);
    }

    .track-image {
      width: 48px;
      height: 48px;
      border-radius: 4px;
      object-fit: cover;
    }

    .track-info {
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 2px;
      min-width: 0;
    }

    .track-name {
      font-weight: 500;
      font-size: 14px;
    }

    .track-artist, .track-album {
      font-size: 12px;
    }

    .track-duration {
      font-size: 12px;
      margin-right: 8px;
    }

    .play-btn {
      opacity: 0;
      transition: opacity 0.2s ease;
      color: var(--spotify-green) !important;
    }

    .track-item:hover .play-btn {
      opacity: 1;
    }

    /* Grid Layouts */
    .artists-grid, .albums-grid, .playlists-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 16px;
    }

    .artist-card, .album-card, .playlist-card {
      background: var(--background-light);
      border-radius: 8px;
      padding: 16px;
      text-align: center;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .artist-card:hover, .album-card:hover, .playlist-card:hover {
      transform: translateY(-2px);
      background: rgba(255,255,255,0.1);
    }

    .artist-image, .album-image, .playlist-image {
      width: 150px;
      height: 150px;
      border-radius: 6px;
      object-fit: cover;
      margin-bottom: 12px;
    }

    .artist-image {
      border-radius: 50%;
    }

    .artist-name, .album-name, .playlist-name {
      font-weight: 500;
      font-size: 14px;
      display: block;
      margin-bottom: 4px;
    }

    .artist-followers, .album-artist, .album-year,
    .playlist-owner, .playlist-tracks {
      font-size: 12px;
      display: block;
      margin-bottom: 2px;
    }

    .artist-genres {
      display: flex;
      flex-wrap: wrap;
      gap: 4px;
      justify-content: center;
      margin-top: 8px;
    }

    .genre-chip {
      font-size: 10px !important;
      height: 20px !important;
      background: rgba(29,185,84,0.2) !important;
      color: var(--spotify-green) !important;
    }

    .view-more-btn {
      color: var(--spotify-green) !important;
      margin-top: 16px;
    }

    .no-results {
      padding: 40px;
    }

    .no-results-icon {
      font-size: 48px;
      height: 48px;
      width: 48px;
      color: var(--text-secondary);
      margin-bottom: 16px;
    }

    .search-suggestions {
      text-align: center;
    }

    .suggestions-grid {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      justify-content: center;
      margin-top: 20px;
    }

    .suggestion-chip {
      background: var(--background-light) !important;
      color: var(--text-primary) !important;
      cursor: pointer;
      transition: all 0.2s ease;
    }

    .suggestion-chip:hover {
      background: rgba(29,185,84,0.2) !important;
      color: var(--spotify-green) !important;
    }

    @media (max-width: 768px) {
      .search-container {
        padding: 16px;
      }

      .artists-grid, .albums-grid, .playlists-grid {
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 12px;
      }

      .artist-image, .album-image, .playlist-image {
        width: 100px;
        height: 100px;
      }

      .track-item {
        padding: 8px;
      }

      .track-image {
        width: 40px;
        height: 40px;
      }
    }
  `]
})
export class SearchComponent implements OnInit {
  searchControl = new FormControl('');
  searchResults: SearchResult | null = null;
  isSearching = false;
  hasSearched = false;
  selectedTabIndex = 0;

  searchTypes = ['track,artist,album,playlist', 'track', 'artist', 'album', 'playlist'];
  searchSuggestions = [
    'Bohemian Rhapsody', 'The Beatles', 'Taylor Swift', 'Ed Sheeran',
    'Billie Eilish', 'Drake', 'Imagine Dragons', 'Ariana Grande',
    'The Weeknd', 'Dua Lipa', 'Post Malone', 'Bad Bunny'
  ];

  constructor(
    public spotifyService: SpotifyService,
    private router: Router,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    this.setupSearchControl();
  }

  /**
   * Setup search control with debouncing
   */
  private setupSearchControl(): void {
    this.searchControl.valueChanges.pipe(
      debounceTime(300),
      distinctUntilChanged(),
      switchMap(query => {
        if (!query || query.trim().length < 2) {
          this.searchResults = null;
          this.hasSearched = false;
          return of(null);
        }

        this.isSearching = true;
        const searchType = this.searchTypes[this.selectedTabIndex];
        
        return this.spotifyService.search(query.trim(), searchType, 20).pipe(
          catchError(error => {
            console.error('Search failed:', error);
            this.snackBar.open('Search failed. Please try again.', 'Close', {
              duration: 3000,
              panelClass: ['error-snackbar']
            });
            return of(null);
          })
        );
      })
    ).subscribe(results => {
      this.searchResults = results;
      this.isSearching = false;
      this.hasSearched = true;
    });
  }

  /**
   * Handle tab change
   */
  onTabChange(event: any): void {
    this.selectedTabIndex = event.index;
    const currentQuery = this.searchControl.value;
    
    if (currentQuery && currentQuery.trim().length >= 2) {
      this.performSearch(currentQuery);
    }
  }

  /**
   * Perform search with current query
   */
  private performSearch(query: string): void {
    if (!query || query.trim().length < 2) return;

    this.isSearching = true;
    const searchType = this.searchTypes[this.selectedTabIndex];
    
    this.spotifyService.search(query.trim(), searchType, 20).subscribe({
      next: (results) => {
        this.searchResults = results;
        this.isSearching = false;
        this.hasSearched = true;
      },
      error: (error) => {
        console.error('Search failed:', error);
        this.isSearching = false;
        this.snackBar.open('Search failed. Please try again.', 'Close', {
          duration: 3000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  /**
   * Search for a specific term
   */
  searchFor(term: string): void {
    this.searchControl.setValue(term);
  }

  /**
   * Check if there are any results
   */
  hasResults(): boolean {
    if (!this.searchResults) return false;
    
    return !!(
      this.searchResults.tracks?.items?.length ||
      this.searchResults.artists?.items?.length ||
      this.searchResults.albums?.items?.length ||
      this.searchResults.playlists?.items?.length
    );
  }

  /**
   * Get result limit based on current tab
   */
  getResultLimit(type: string): number {
    if (this.selectedTabIndex === 0) { // All tab
      return type === 'tracks' ? 8 : 6;
    }
    return 20; // Specific type tab
  }

  /**
   * Get artist names as comma-separated string
   */
  getArtistNames(artists: any[]): string {
    return artists?.map(artist => artist.name).join(', ') || 'Unknown Artist';
  }

  /**
   * Get year from date string
   */
  getYear(dateString: string): string {
    return new Date(dateString).getFullYear().toString();
  }

  /**
   * Navigation methods
   */
  goToTrack(trackId: string): void {
    this.router.navigate(['/track', trackId]);
  }

  goToArtist(artistId: string): void {
    this.router.navigate(['/artist', artistId]);
  }

  goToAlbum(albumId: string): void {
    this.router.navigate(['/album', albumId]);
  }

  goToPlaylist(playlistId: string): void {
    this.router.navigate(['/playlist', playlistId]);
  }

  /**
   * Play track (placeholder)
   */
  playTrack(track: any): void {
    if (track.preview_url) {
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
   * View more tracks
   */
  viewMoreTracks(): void {
    this.selectedTabIndex = 1; // Switch to tracks tab
  }
}
