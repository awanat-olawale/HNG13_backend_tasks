#!/bin/bash
# start.sh — for Railway Django deployment

echo "Applying database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn server..."
gunicorn analyzer.wsgi:application --bind 0.0.0.0:$PORT
