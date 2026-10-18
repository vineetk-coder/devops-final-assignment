#!/usr/bin/env bash
# Exercise-03: remove ReplicaSet/Deployment and Service
set -uo pipefail
kubectl delete -f k8s/flashsale-replicaset.yaml --ignore-not-found
kubectl delete -f k8s/challenge-flashsale-deployment.yaml --ignore-not-found
