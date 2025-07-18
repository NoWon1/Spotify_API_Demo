web: gunicorn --pythonpath backend spotify_api.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A backend.spotify_api worker --loglevel=info
