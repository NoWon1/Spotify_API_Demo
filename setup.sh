#!/bin/bash

# Spotify Demo - Setup Script
# This script sets up the complete development environment

echo "🎵 Setting up Spotify Demo - Modern Full-Stack Application"
echo "=================================================="

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js is required but not installed."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    echo "❌ npm is required but not installed."
    exit 1
fi

echo "✅ Prerequisites check passed"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your Spotify credentials before continuing"
    echo "   Get your credentials from: https://developer.spotify.com/dashboard"
    read -p "Press Enter after you've configured your .env file..."
fi

# Backend Setup
echo "🔧 Setting up Django backend..."
cd backend

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate || venv\Scripts\activate

# Install dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Database setup
echo "Setting up database..."
python manage.py makemigrations
python manage.py migrate

# Create superuser (optional)
echo "Would you like to create a Django superuser? (y/n)"
read -r create_superuser
if [ "$create_superuser" = "y" ]; then
    python manage.py createsuperuser
fi

cd ..

# Frontend Setup
echo "🔧 Setting up Angular frontend..."
cd frontend

# Install dependencies
echo "Installing Node.js dependencies..."
npm install

# Build Angular app
echo "Building Angular application..."
npm run build

cd ..

echo "✅ Setup complete!"
echo ""
echo "🚀 To start the application:"
echo "Backend:  cd backend && source venv/bin/activate && python manage.py runserver"
echo "Frontend: cd frontend && npm start"
echo ""
echo "📱 Access the application:"
echo "Frontend: http://localhost:4200"
echo "Backend:  http://localhost:8000"
echo "Admin:    http://localhost:8000/admin"
echo ""
echo "🔒 Make sure to configure your Spotify app redirect URI to:"
echo "   http://localhost:4200/login"
