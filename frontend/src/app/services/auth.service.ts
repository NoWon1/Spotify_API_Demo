import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import { Observable, BehaviorSubject, throwError } from 'rxjs';
import { map, catchError } from 'rxjs/operators';

export interface User {
  id: string;
  display_name: string;
  email: string;
  images: Array<{ url: string }>;
  followers: { total: number };
}

export interface AuthTokens {
  access_token: string;
  refresh_token: string;
  expires_in: number;
}

@Injectable({
  providedIn: 'root'
})
export class AuthService {
  private readonly API_BASE_URL = 'http://localhost:8000/api';
  private isAuthenticatedSubject = new BehaviorSubject<boolean>(false);
  private userSubject = new BehaviorSubject<User | null>(null);

  public isAuthenticated$ = this.isAuthenticatedSubject.asObservable();
  public user$ = this.userSubject.asObservable();

  constructor(private http: HttpClient) {
    this.checkAuthStatus();
  }

  /**
   * Check if user is authenticated by verifying token existence and validity
   */
  checkAuthStatus(): void {
    const token = this.getAccessToken();
    if (token) {
      this.validateToken().subscribe(
        (isValid) => {
          this.isAuthenticatedSubject.next(isValid);
          if (isValid) {
            this.loadUserProfile();
          }
        },
        () => this.isAuthenticatedSubject.next(false)
      );
    } else {
      this.isAuthenticatedSubject.next(false);
    }
  }

  /**
   * Get Spotify authorization URL
   */
  getAuthUrl(): Observable<{ auth_url: string }> {
    return this.http.get<{ auth_url: string }>(`${this.API_BASE_URL}/auth/login/`);
  }

  /**
   * Handle OAuth callback and exchange code for tokens
   */
  handleCallback(code: string, state?: string): Observable<AuthTokens> {
    const params = new HttpParams()
      .set('code', code)
      .set('state', state || '');

    return this.http.get<AuthTokens>(`${this.API_BASE_URL}/auth/callback/`, { params })
      .pipe(
        map(tokens => {
          this.setTokens(tokens);
          this.isAuthenticatedSubject.next(true);
          this.loadUserProfile();
          return tokens;
        }),
        catchError(error => {
          console.error('Authentication failed:', error);
          return throwError(() => error);
        })
      );
  }

  /**
   * Refresh access token using refresh token
   */
  refreshToken(): Observable<AuthTokens> {
    const refreshToken = this.getRefreshToken();
    if (!refreshToken) {
      return throwError(() => new Error('No refresh token available'));
    }

    return this.http.post<AuthTokens>(`${this.API_BASE_URL}/auth/refresh/`, {
      refresh_token: refreshToken
    }).pipe(
      map(tokens => {
        this.setTokens(tokens);
        return tokens;
      }),
      catchError(error => {
        this.logout();
        return throwError(() => error);
      })
    );
  }

  /**
   * Load current user profile
   */
  loadUserProfile(): void {
    this.http.get<User>(`${this.API_BASE_URL}/auth/profile/`)
      .subscribe(
        user => this.userSubject.next(user),
        error => console.error('Failed to load user profile:', error)
      );
  }

  /**
   * Logout user and clear tokens
   */
  logout(): Observable<any> {
    return this.http.post(`${this.API_BASE_URL}/auth/logout/`, {})
      .pipe(
        map(() => {
          this.clearTokens();
          this.isAuthenticatedSubject.next(false);
          this.userSubject.next(null);
        }),
        catchError(error => {
          // Even if logout fails on server, clear local tokens
          this.clearTokens();
          this.isAuthenticatedSubject.next(false);
          this.userSubject.next(null);
          return throwError(() => error);
        })
      );
  }

  /**
   * Check if user is currently authenticated
   */
  isAuthenticated(): boolean {
    return this.isAuthenticatedSubject.value;
  }

  /**
   * Get current user
   */
  getCurrentUser(): User | null {
    return this.userSubject.value;
  }

  /**
   * Get access token from localStorage
   */
  getAccessToken(): string | null {
    return localStorage.getItem('spotify_access_token');
  }

  /**
   * Get refresh token from localStorage
   */
  getRefreshToken(): string | null {
    return localStorage.getItem('spotify_refresh_token');
  }

  /**
   * Get HTTP headers with authorization
   */
  getAuthHeaders(): HttpHeaders {
    const token = this.getAccessToken();
    if (!token) {
      throw new Error('No access token available');
    }
    
    return new HttpHeaders({
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    });
  }

  /**
   * Validate current access token
   */
  private validateToken(): Observable<boolean> {
    const token = this.getAccessToken();
    if (!token) {
      return throwError(() => new Error('No token to validate'));
    }

    return this.http.get(`${this.API_BASE_URL}/auth/profile/`)
      .pipe(
        map(() => true),
        catchError(() => {
          // Token is invalid, try to refresh
          return this.refreshToken().pipe(
            map(() => true),
            catchError(() => {
              this.clearTokens();
              return throwError(() => new Error('Token validation failed'));
            })
          );
        })
      );
  }

  /**
   * Store tokens in localStorage
   */
  private setTokens(tokens: AuthTokens): void {
    localStorage.setItem('spotify_access_token', tokens.access_token);
    if (tokens.refresh_token) {
      localStorage.setItem('spotify_refresh_token', tokens.refresh_token);
    }
    
    // Set token expiration time
    const expirationTime = new Date().getTime() + (tokens.expires_in * 1000);
    localStorage.setItem('spotify_token_expiration', expirationTime.toString());
  }

  /**
   * Clear tokens from localStorage
   */
  private clearTokens(): void {
    localStorage.removeItem('spotify_access_token');
    localStorage.removeItem('spotify_refresh_token');
    localStorage.removeItem('spotify_token_expiration');
  }

  /**
   * Check if token is expired
   */
  private isTokenExpired(): boolean {
    const expiration = localStorage.getItem('spotify_token_expiration');
    if (!expiration) {
      return true;
    }
    
    return new Date().getTime() > parseInt(expiration);
  }
}
