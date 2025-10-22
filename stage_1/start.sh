#!/bin/bash
set -o errexit

pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
gunicorn string_analyzer.wsgi:application --bind 0.0.0.0:$PORT
