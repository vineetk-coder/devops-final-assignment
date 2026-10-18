#!/usr/bin/env bash
# Exercise-02: build the image inside Minikube and deploy it.
# Run from the Exercise-02 folder:  bash scripts/deploy.sh
set -euo pipefail

minikube start

# Point the docker CLI at Minikube's Docker daemon, then build there
eval "$(minikube docker-env)"
docker build -t flask-app .

kubectl apply -f k8s/flask-deployment.yaml
kubectl rollout status deployment/flask-app --timeout=120s

kubectl get deployments
kubectl get pods -l app=flask-app
kubectl get services

echo "Getting the service URL (keep this terminal open with the docker driver)..."
minikube service flask-app-service --url
