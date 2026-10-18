#!/usr/bin/env bash
# Exercise-07: Install/start Jenkins using Docker.
# Port 8080 = web UI, 50000 = agent communication.
set -euo pipefail

if docker ps -a --format '{{.Names}}' | grep -qx jenkins; then
  echo "A container named 'jenkins' already exists; starting it."
  docker start jenkins
else
  docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts
fi

docker ps -a --filter name=jenkins
echo "Jenkins is starting. Open http://localhost:8080/ in ~30-60 seconds."
echo "Then run: bash scripts/get-initial-password.sh"
