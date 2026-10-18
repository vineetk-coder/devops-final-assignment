#!/usr/bin/env bash
# Exercise-02: remove the Deployment and Service
set -uo pipefail
kubectl delete -f k8s/flask-deployment.yaml --ignore-not-found
