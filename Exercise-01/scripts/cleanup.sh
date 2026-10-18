#!/usr/bin/env bash
# Exercise-01: remove the resources created by run.sh
set -uo pipefail
kubectl delete service hello-k8s --ignore-not-found
kubectl delete pod hello-k8s --ignore-not-found
echo "Cleanup done. (Optional) stop the cluster with: minikube stop"
