@echo off
echo 🎵 Setting up Spotify Demo - Modern Full-Stack Application
echo ==================================================

echo Checking prerequisites...

where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Python is required but not installed.
    exit /b 1
)

where node >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Node.js is required but not installed.
    exit /b 1
)

where npm >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ npm is required but not installed.
    exit /b 1
)

echo ✅ Prerequisites check passed

REM Create .env file if it doesn't exist
if not exist .env (
    echo Creating .env file from template...
    copy .env.example .env
    echo ⚠️  Please edit .env file with your Spotify credentials before continuing
    echo    Get your credentials from: https://developer.spotify.com/dashboard
    pause
)

REM Backend Setup
echo 🔧 Setting up Django backend...
cd backend

REM Create virtual environment
if not exist venv (
    echo Creating Python virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

REM Install dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Database setup
echo Setting up database...
python manage.py makemigrations
python manage.py migrate

REM Create superuser (optional)
echo Would you like to create a Django superuser? (y/n)
set /p create_superuser=
if "%create_superuser%"=="y" (
    python manage.py createsuperuser
)

cd ..

REM Frontend Setup
echo 🔧 Setting up Angular frontend...
cd frontend

REM Install dependencies
echo Installing Node.js dependencies...
call npm install

REM Build Angular app
echo Building Angular application...
call npm run build

cd ..

echo ✅ Setup complete!
echo.
echo 🚀 To start the application:
echo Backend:  cd backend ^&^& venv\Scripts\activate ^&^& python manage.py runserver
echo Frontend: cd frontend ^&^& npm start
echo.
echo 📱 Access the application:
echo Frontend: http://localhost:4200
echo Backend:  http://localhost:8000
echo Admin:    http://localhost:8000/admin
echo.
echo 🔒 Make sure to configure your Spotify app redirect URI to:
echo    http://localhost:4200/login

pause
