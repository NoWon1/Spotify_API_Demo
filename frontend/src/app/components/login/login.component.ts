import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthService } from '../../services/auth.service';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'app-login',
  template: `
    <div class="login-container">
      <div class="login-card mat-elevation-4">
        <div class="login-header text-center">
          <mat-icon class="spotify-icon">music_note</mat-icon>
          <h1 class="spotify-green">Spotify Demo</h1>
          <p class="text-secondary">Modern Music Discovery Platform</p>
        </div>

        <div class="login-content" *ngIf="!isLoading">
          <div class="login-description text-center">
            <h2>Discover Your Music</h2>
            <p>
              Connect your Spotify account to explore personalized playlists, 
              discover new artists, and analyze your listening habits with our 
              modern web application.
            </p>
          </div>

          <div class="login-features">
            <div class="feature-item">
              <mat-icon>dashboard</mat-icon>
              <span>Personalized Dashboard</span>
            </div>
            <div class="feature-item">
              <mat-icon>search</mat-icon>
              <span>Advanced Search</span>
            </div>
            <div class="feature-item">
              <mat-icon>analytics</mat-icon>
              <span>Audio Analysis</span>
            </div>
            <div class="feature-item">
              <mat-icon>favorite</mat-icon>
              <span>Smart Recommendations</span>
            </div>
          </div>

          <div class="login-actions text-center">
            <button 
              mat-raised-button 
              color="primary" 
              class="spotify-login-btn"
              (click)="login()"
              [disabled]="isLoading">
              <mat-icon>login</mat-icon>
              Connect with Spotify
            </button>
            
            <p class="login-disclaimer text-secondary">
              By connecting, you agree to share your Spotify listening data 
              for the purpose of this demonstration.
            </p>
          </div>
        </div>

        <div class="login-loading text-center" *ngIf="isLoading">
          <mat-spinner></mat-spinner>
          <p class="text-secondary">Connecting to Spotify...</p>
        </div>
      </div>

      <div class="login-footer text-center">
        <p class="text-secondary">
          This is a demonstration application showcasing modern web technologies 
          with the Spotify Web API.
        </p>
      </div>
    </div>
  `,
  styles: [`
    .login-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      justify-content: center;
      align-items: center;
      background: linear-gradient(135deg, #191414 0%, #1db954 100%);
      padding: 20px;
    }

    .login-card {
      background: white;
      border-radius: 16px;
      padding: 40px;
      max-width: 500px;
      width: 100%;
      box-shadow: 0 8px 32px rgba(0,0,0,0.3);
    }

    .login-header {
      margin-bottom: 40px;
    }

    .spotify-icon {
      font-size: 48px;
      height: 48px;
      width: 48px;
      color: #1db954;
      margin-bottom: 16px;
    }

    .login-header h1 {
      margin: 0 0 8px 0;
      font-size: 32px;
      font-weight: 300;
    }

    .login-description h2 {
      color: #333;
      margin-bottom: 16px;
      font-weight: 400;
    }

    .login-description p {
      color: #666;
      line-height: 1.6;
      margin-bottom: 32px;
    }

    .login-features {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 16px;
      margin-bottom: 40px;
    }

    .feature-item {
      display: flex;
      align-items: center;
      gap: 8px;
      color: #666;
      font-size: 14px;
    }

    .feature-item mat-icon {
      color: #1db954;
      font-size: 20px;
      height: 20px;
      width: 20px;
    }

    .spotify-login-btn {
      background-color: #1db954 !important;
      color: white !important;
      padding: 12px 32px;
      font-size: 16px;
      font-weight: 500;
      border-radius: 25px;
      margin-bottom: 16px;
    }

    .spotify-login-btn:hover {
      background-color: #1ed760 !important;
      transform: translateY(-1px);
      box-shadow: 0 4px 12px rgba(29, 185, 84, 0.3);
    }

    .spotify-login-btn mat-icon {
      margin-right: 8px;
    }

    .login-disclaimer {
      font-size: 12px;
      line-height: 1.4;
      max-width: 300px;
      margin: 0 auto;
    }

    .login-loading {
      padding: 40px 0;
    }

    .login-loading mat-spinner {
      margin: 0 auto 16px auto;
    }

    .login-footer {
      margin-top: 32px;
      max-width: 400px;
    }

    .login-footer p {
      font-size: 12px;
      color: rgba(255,255,255,0.7);
    }

    @media (max-width: 600px) {
      .login-card {
        padding: 24px;
        margin: 16px;
      }

      .login-features {
        grid-template-columns: 1fr;
      }

      .spotify-icon {
        font-size: 40px;
        height: 40px;
        width: 40px;
      }

      .login-header h1 {
        font-size: 28px;
      }
    }
  `]
})
export class LoginComponent implements OnInit {
  isLoading = false;

  constructor(
    private authService: AuthService,
    private router: Router,
    private route: ActivatedRoute,
    private snackBar: MatSnackBar
  ) {}

  ngOnInit(): void {
    // Check if this is a callback from Spotify
    this.route.queryParams.subscribe(params => {
      if (params['code']) {
        this.handleSpotifyCallback(params['code'], params['state']);
      } else if (params['error']) {
        this.handleSpotifyError(params['error'], params['error_description']);
      }
    });

    // If already authenticated, redirect to dashboard
    if (this.authService.isAuthenticated()) {
      this.router.navigate(['/dashboard']);
    }
  }

  /**
   * Initiate Spotify login process
   */
  login(): void {
    this.isLoading = true;
    
    this.authService.getAuthUrl().subscribe({
      next: (response) => {
        // Redirect to Spotify authorization page
        window.location.href = response.auth_url;
      },
      error: (error) => {
        console.error('Failed to get auth URL:', error);
        this.isLoading = false;
        this.snackBar.open('Failed to connect to Spotify. Please try again.', 'Close', {
          duration: 5000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  /**
   * Handle Spotify OAuth callback
   */
  private handleSpotifyCallback(code: string, state?: string): void {
    this.isLoading = true;
    
    this.authService.handleCallback(code, state).subscribe({
      next: () => {
        this.snackBar.open('Successfully connected to Spotify!', 'Close', {
          duration: 3000,
          panelClass: ['success-snackbar']
        });
        this.router.navigate(['/dashboard']);
      },
      error: (error) => {
        console.error('Authentication failed:', error);
        this.isLoading = false;
        this.snackBar.open('Authentication failed. Please try again.', 'Close', {
          duration: 5000,
          panelClass: ['error-snackbar']
        });
      }
    });
  }

  /**
   * Handle Spotify OAuth error
   */
  private handleSpotifyError(error: string, description?: string): void {
    console.error('Spotify OAuth error:', error, description);
    
    let errorMessage = 'Authentication failed.';
    if (error === 'access_denied') {
      errorMessage = 'Access was denied. Please grant permission to continue.';
    }
    
    this.snackBar.open(errorMessage, 'Close', {
      duration: 5000,
      panelClass: ['error-snackbar']
    });
  }
}
