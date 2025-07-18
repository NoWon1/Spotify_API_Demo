import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { DashboardComponent } from './components/dashboard/dashboard.component';
import { SearchComponent } from './components/search/search.component';
import { TrackDetailComponent } from './components/track-detail/track-detail.component';
import { ArtistDetailComponent } from './components/artist-detail/artist-detail.component';
import { AlbumDetailComponent } from './components/album-detail/album-detail.component';
import { PlaylistDetailComponent } from './components/playlist-detail/playlist-detail.component';
import { BrowseComponent } from './components/browse/browse.component';
import { LibraryComponent } from './components/library/library.component';
import { LoginComponent } from './components/login/login.component';

const routes: Routes = [
  { path: '', redirectTo: '/dashboard', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent },
  { path: 'search', component: SearchComponent },
  { path: 'browse', component: BrowseComponent },
  { path: 'library', component: LibraryComponent },
  { path: 'track/:id', component: TrackDetailComponent },
  { path: 'artist/:id', component: ArtistDetailComponent },
  { path: 'album/:id', component: AlbumDetailComponent },
  { path: 'playlist/:id', component: PlaylistDetailComponent },
  { path: '**', redirectTo: '/dashboard' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
