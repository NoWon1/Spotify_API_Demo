import { Component, OnInit } from '@angular/core';
import { AuthService } from './services/auth.service';

@Component({
  selector: 'app-root',
  template: `
    <div class="app-container bg-dark">
      <app-navigation *ngIf="authService.isAuthenticated()"></app-navigation>
      
      <main class="main-content" [class.with-nav]="authService.isAuthenticated()">
        <router-outlet></router-outlet>
      </main>
    </div>
  `,
  styles: [`
    .app-container {
      min-height: 100vh;
      display: flex;
      flex-direction: column;
    }
    
    .main-content {
      flex: 1;
      padding: 0;
      transition: margin-left 0.3s ease;
    }
    
    .main-content.with-nav {
      margin-left: 240px;
    }
    
    @media (max-width: 768px) {
      .main-content.with-nav {
        margin-left: 0;
      }
    }
  `]
})
export class AppComponent implements OnInit {
  title = 'Spotify Demo - Modern Music Discovery';

  constructor(public authService: AuthService) {}

  ngOnInit(): void {
    // Initialize authentication state
    this.authService.checkAuthStatus();
  }
}
