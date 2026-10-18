#!/usr/bin/env bash
# Exercise-04: Docker networking with Flask + MySQL + Redis on a user-defined bridge.
# Run from the Exercise-04 folder:  bash scripts/run.sh
set -euo pipefail

echo "Task 1: Create a bridge network"
docker network create --driver bridge my-bridge-net

echo "Task 2: Verify the network"
docker network ls

echo "Task 3: Inspect the network"
docker network inspect my-bridge-net

echo "Task 4: Build the Flask image"
docker build -t flask-api .

echo "Task 4: Launch the containers (-d = detached)"
# mysql:latest refuses to start without a root-password option. We use
# MYSQL_RANDOM_ROOT_PASSWORD so NO password is hard-coded anywhere.
docker run -d --name mysql --net=my-bridge-net -e MYSQL_RANDOM_ROOT_PASSWORD=yes mysql:latest
docker run -d --name redis --net=my-bridge-net redis:latest
docker run -d --name flask --net=my-bridge-net -p 5001:5001 flask-api

sleep 5
echo "Task 5: Test connectivity (container names resolve via Docker's embedded DNS)"
docker exec flask ping -c 2 mysql
docker exec flask ping -c 2 redis

echo "Bonus: call the API through the published port"
curl -s http://localhost:5001/about || echo "(curl not available or app still starting)"
echo
echo "Done. Run 'bash scripts/cleanup.sh' (Task 6) when finished."
