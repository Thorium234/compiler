#!/bin/bash
# Campus Code Lab Startup Script

echo "=== Campus Code Lab Initializer ==="

if ! command -v docker-compose &> /dev/null
then
    echo "[!] docker-compose could not be found. Please install Docker and docker-compose to run Campus Code Lab."
    exit 1
fi

echo "[1] Pulling required Docker images..."
docker pull python:3.10-alpine

echo "[2] Starting up containers in detached mode..."
docker-compose up --build -d

echo "[2] Performing database migrations..."
docker-compose exec -T web python manage.py migrate

echo ""
echo "✅ Configuration Complete!"
echo "🚀 Application is running at http://localhost:8000"
echo "To create the initial lecturer superuser, execute: docker-compose exec web python manage.py createsuperuser"
