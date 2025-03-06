# Spotify API Demo

## Features

- **Authentication with Spotify API**
  - Client Credentials flow
  - Authorization Code flow with refresh tokens
  
- **Music Exploration**
  - Browse featured playlists
  - Discover new album releases
  - Search for artists
  - View artist details and top tracks
  - Explore album tracks
  - View playlist content
  
- **Music Analysis**
  - Visualize audio features with interactive charts
  - Display track metrics (danceability, energy, etc.)
  
- **User Library Management**
  - Save/remove albums from user's library
  - Save/remove tracks from user's library
  
- **Playlist Management**
  - Create playlists
  - Add tracks to playlists
  - View user playlists

## Technologies Used

- **Backend**
  - Python 3.x
  - Django 4.0.x
  - Requests library for API calls
  
- **Frontend**
  - HTML/CSS
  - Bootstrap 3.4.1
  - JavaScript
  - Chart.js for data visualization
  - jQuery
  
- **APIs**
  - Spotify Web API

## Project Structure

```
Demo/
├── Albums/              # Album-related API examples
├── Artists/             # Artist-related API examples
├── Playlists/           # Playlist-related API examples
├── Search Spotify/      # Search-related API examples
├── Tracks/              # Track-related API examples
├── music_world/         # Main Django app
│   ├── templates/       # HTML templates
│   ├── views.py         # View controllers
│   └── urls.py          # URL routing
├── spotify_demo_app/    # Django project settings
└── templates/           # Global templates
```

## Installation and Setup

1. **Clone the repository**
   ```
   git clone https://github.com/yourusername/spotify-api-django.git
   cd spotify-api-django
   ```

2. **Set up a virtual environment (recommended)**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```
   pip install django requests
   ```

4. **Create a Spotify Developer account**
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
   - Create a new application to get your Client ID and Client Secret
   - Add a redirect URI (e.g., http://localhost:8000/callback)

5. **Update configuration**
   - Update the CLIENT_ID and CLIENT_SECRET in Authorization_code.py
   - Update the REDIRECT_URI if needed

6. **Run migrations**
   ```
   python manage.py migrate
   ```

7. **Start the development server**
   ```
   python manage.py runserver
   ```

8. **Access the application**
   - Open your web browser and navigate to http://localhost:8000

## Usage

1. **Home Page**
   - Displays featured playlists and new album releases
   - Search for artists using the sidebar search form

2. **Artist Page**
   - View artist information and top tracks
   - Listen to track previews
   - View audio analysis for each track

3. **Album Page**
   - Browse album tracks
   - Listen to track previews
   - Access audio analysis

4. **Playlist Page**
   - View playlist tracks
   - See artist information
   - Listen to track previews

5. **Audio Analysis**
   - Visualized audio features like danceability, energy, etc.
   - Bar chart representation of track characteristics

## API Reference

This application demonstrates various Spotify Web API endpoints:

- **Artist APIs**
  - Get artist information
  - Get artist's top tracks
  - Get artist's albums

- **Album APIs**
  - Get album details
  - Save albums to library
  - Get user's saved albums
  - Remove albums from library

- **Track APIs**
  - Get track details
  - Save tracks to library
  - Get audio features
  - Remove tracks from library

- **Playlist APIs**
  - Create playlists
  - Get playlist details
  - Add tracks to playlists
  - Get user's playlists

- **Search API**
  - Search for artists

For complete API documentation, visit [Spotify Web API Documentation](https://developer.spotify.com/documentation/web-api/).

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Acknowledgements

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Django Documentation](https://docs.djangoproject.com/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/3.4/)
- [Chart.js](https://www.chartjs.org/)
