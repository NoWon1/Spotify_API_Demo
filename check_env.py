#!/usr/bin/env python3
"""
Environment validation script for Spotify API project
Run this script to check if all required environment variables are properly configured
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_var(var_name, required=True):
    """Check if an environment variable is set"""
    value = os.getenv(var_name)
    if value:
        # Hide sensitive values in output
        if 'TOKEN' in var_name or 'SECRET' in var_name or 'KEY' in var_name:
            display_value = f"{'*' * (len(value) - 4)}{value[-4:]}" if len(value) > 4 else "****"
        else:
            display_value = value
        print(f"✅ {var_name}: {display_value}")
        return True
    else:
        status = "❌ MISSING (Required)" if required else "⚠️  MISSING (Optional)"
        print(f"{status} {var_name}")
        return not required

def main():
    print("🔐 Spotify API Environment Configuration Check")
    print("=" * 50)
    
    all_good = True
    
    # Required variables
    required_vars = [
        'SPOTIFY_CLIENT_ID',
        'SPOTIFY_CLIENT_SECRET',
    ]
    
    # Optional but recommended variables
    optional_vars = [
        'SPOTIFY_ACCESS_TOKEN',
        'SPOTIFY_REFRESH_TOKEN',
        'SPOTIFY_REDIRECT_URI',
        'SPOTIFY_SCOPE',
        'DJANGO_SECRET_KEY',
        'DJANGO_DEBUG',
        'DJANGO_ALLOWED_HOSTS'
    ]
    
    print("\n📋 Required Variables:")
    for var in required_vars:
        if not check_env_var(var, required=True):
            all_good = False
    
    print("\n📋 Optional Variables:")
    for var in optional_vars:
        check_env_var(var, required=False)
    
    print("\n" + "=" * 50)
    
    if all_good:
        print("🎉 All required environment variables are configured!")
        print("📖 You can now run the Spotify API scripts.")
        
        # Test importing the utility module
        try:
            from spotify_utils import get_spotify_headers
            print("✅ Utility modules are working correctly.")
        except Exception as e:
            print(f"⚠️  Warning: Could not import utilities - {e}")
            
    else:
        print("❌ Some required environment variables are missing.")
        print("📋 Please check your .env file and refer to SECURITY.md for setup instructions.")
    
    print("\n💡 Tips:")
    print("   - Copy .env.example to .env and fill in your credentials")
    print("   - Get your credentials from https://developer.spotify.com/dashboard/")
    print("   - Never commit .env files to version control")

if __name__ == "__main__":
    main()
