#!/bin/bash
echo "Starting Numerix..."
docker stop numerix_app 2>/dev/null
docker rm numerix_app 2>/dev/null
docker run -d -p 5000:5000 -v numerix_data:/app/instance --name numerix_app numerix

echo "Waiting for server to start..."
sleep 3

echo "Opening browser..."
xdg-open http://localhost:5000 2>/dev/null || open http://localhost:5000 2>/dev/null

echo "Numerix is running at http://localhost:5000"
echo "To stop: docker stop numerix_app && docker rm numerix_app"