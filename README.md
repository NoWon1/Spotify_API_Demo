# Spotify API Demo - Full Stack Application

A modern full-stack web application demonstrating Spotify Web API integration with Django REST Framework backend and Angular frontend.

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js 18+
- Spotify Developer Account

###  Setup Instructions

#### 1. Clone and Setup Environment
```bash
# Navigate to project directory
cd "c:\Users\adity\OneDrive\Desktop\Coding\APIs\Spotify\Demo"

# Copy environment file
copy .env.example .env
```

#### 2. Configure Spotify API Credentials
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard/)
2. Create a new application
3. Copy your credentials to `.env` file:

```env
# Spotify App Credentials
SPOTIFY_CLIENT_ID=your_actual_client_id_here
SPOTIFY_CLIENT_SECRET=your_actual_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:4200/callback

# Django Configuration
DJANGO_SECRET_KEY=your_django_secret_key_here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

#### 3. Backend Setup (Django)
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
# Install dependencies (already done)
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Start Django server
python manage.py runserver 8000
```

#### 4. Frontend Setup (Angular)
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (already done)
npm install

# Start Angular development server
npm start
```

###  Access the Application

- **Frontend**: http://localhost:4200
- **Backend API**: http://localhost:8000
- **Django Admin**: http://localhost:8000/admin

##  Architecture

### Backend (Django REST Framework)
- **API Endpoints**: `/api/` - User authentication, Spotify integration
- **Authentication**: JWT tokens with Spotify OAuth
- **Models**: User profiles, Spotify tokens, analytics
- **Services**: Spotify API wrapper, token management

### Frontend (Angular + Material Design)
- **Components**: Dashboard, Search, Playlists, Profile
- **Services**: HTTP client, authentication, Spotify integration
- **Routing**: Protected routes with auth guards
- **UI**: Material Design with responsive layout

## Project Structure

```
Demo/
├── backend/                    # Django REST Framework
│   ├── api/                   # Core API application
│   ├── authentication/       # User authentication
│   ├── spotify_api/          # Django settings
│   └── requirements.txt      # Python dependencies
├── frontend/                  # Angular application
│   ├── src/app/              # Angular components & services
│   ├── package.json          # Node.js dependencies
│   └── angular.json          # Angular configuration
├── .env.example              # Environment template
├── .gitignore               # Git ignore rules
└── SECURITY.md              # Security setup guide
```

## Security Features

-  Environment variables for all sensitive data
-  No hardcoded API keys or secrets
-  JWT token authentication
-  CORS configuration for cross-origin requests
-  Secure Spotify OAuth flow

##  Features

### Dashboard
- Personalized user statistics
- Top tracks and artists
- New releases and featured playlists
- Recent listening activity

### Search
- Real-time search across Spotify catalog
- Filter by tracks, artists, albums, playlists
- Responsive results with rich metadata

### Audio Analysis
- Track audio features visualization
- Audio analysis integration
- Recommendations based on preferences

### Profile Management
- User profile with Spotify data
- Listening history and statistics
- Account preferences

##  Development Commands

### Backend
```bash
# Run Django development server
python manage.py runserver

# Create superuser
python manage.py createsuperuser

# Make migrations
python manage.py makemigrations

# Run tests
python manage.py test
```

### Frontend
```bash
# Development server
npm start

# Build for production
npm run build:prod

# Run tests
npm test

# Run linting
npm run lint
```

##  API Endpoints

### Authentication
- `POST /api/auth/spotify/` - Initiate Spotify OAuth
- `POST /api/auth/callback/` - Handle OAuth callback
- `POST /api/auth/refresh/` - Refresh access token

### Spotify Integration
- `GET /api/user/profile/` - Get user profile
- `GET /api/search/` - Search Spotify catalog
- `GET /api/tracks/top/` - Get user's top tracks
- `GET /api/artists/top/` - Get user's top artists
- `GET /api/playlists/` - Get user's playlists

##  Troubleshooting

### Common Issues

1. **Django Server Won't Start**
   - Ensure virtual environment is activated
   - Check if all dependencies are installed: `pip install -r requirements.txt`

2. **Angular Build Errors**
   - Delete `node_modules` and run `npm install`
   - Clear npm cache: `npm cache clean --force`

3. **Spotify API Errors**
   - Verify credentials in `.env` file
   - Check redirect URI matches Spotify app settings
   - Ensure tokens haven't expired

### Environment Issues
- Make sure `.env` file exists and has correct values
- Verify Python virtual environment is activated
- Check Node.js version compatibility (18+)

##  Next Steps

1. Set up production environment
2. Configure SSL certificates
3. Set up continuous deployment
4. Add more Spotify API features
5. Implement real-time updates

##  Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit pull request

##  License

This project is for demonstration purposes. Spotify API usage subject to [Spotify Developer Terms](https://developer.spotify.com/terms/).
