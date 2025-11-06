web: gunicorn ip_tracking.wsgi:application --bind 0.0.0.0:$PORT
worker: celery -A ip_tracking worker -l info
beat: celery -A ip_tracking beat -l info

