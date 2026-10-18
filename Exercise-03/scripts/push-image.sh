#!/usr/bin/env bash
# Exercise-03: optional — push the image to Docker Hub (reference "Build and push" step).
# Requires: `docker login` done interactively beforehand; DOCKERHUB_USERNAME set in your shell.
set -euo pipefail
: "${DOCKERHUB_USERNAME:?Set DOCKERHUB_USERNAME first (see ../.env.example)}"
docker build -t "${DOCKERHUB_USERNAME}/flashsale:1.0" .
docker push "${DOCKERHUB_USERNAME}/flashsale:1.0"
