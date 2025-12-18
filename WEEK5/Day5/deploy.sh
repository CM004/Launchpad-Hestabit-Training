#!/bin/bash

echo "Stopping old containers..."
docker compose -f docker-compose.prod.yaml down

echo "Building images..."
docker compose -f docker-compose.prod.yaml build --no-cache

echo "Starting containers..."
docker compose -f docker-compose.prod.yaml up -d

echo "Deployment complete!"
docker ps
