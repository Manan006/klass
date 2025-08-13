#!/bin/sh
echo "Running DB migration..."
poetry run python klass/manage.py migrate

echo "Collecting static files..."
poetry run python klass/manage.py collectstatic --noinput

echo "Starting Uvicorn..."
poetry run uvicorn klass.asgi:application --host 0.0.0.0 --port 6060 --app-dir klass
