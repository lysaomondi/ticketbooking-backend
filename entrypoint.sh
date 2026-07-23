#!/bin/sh
set -e

echo "Applying migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Creating superuser if not exists..."
python manage.py createsuperuser --noinput --email "$DJANGO_SUPERUSER_EMAIL" || true

echo "Starting server..."
exec gunicorn config.wsgi:application --bind 0.0.0.0:$PORT
