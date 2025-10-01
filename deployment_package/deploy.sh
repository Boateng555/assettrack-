#!/bin/bash
echo "Deploying Django AssetTrack..."

# Stop existing containers
docker stop $(docker ps -q) 2>/dev/null || true
docker rm $(docker ps -aq) 2>/dev/null || true

# Build and run the Django app
docker build -t assettrack-django .
docker run -d -p 80:80 --name assettrack-app assettrack-django

echo "Django AssetTrack is now running at http://172.191.203.103/"
