#!/usr/bin/env bash
# Exercise-10: delete apps and the multi-node cluster
set -uo pipefail
kubectl delete -f k8s/ --ignore-not-found
minikube stop -p devops-multinode
minikube delete -p devops-multinode
