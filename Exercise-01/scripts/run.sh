#!/usr/bin/env bash
# Exercise-01: Hello Pod — runs the exact lab steps in order.
# Run from the Exercise-01 folder:  bash scripts/run.sh
set -euo pipefail

echo "Step 1: Start Minikube"
minikube start

echo "Step 2: Create the hello-k8s Pod (nginx = Zepto storefront)"
kubectl run hello-k8s --image=nginx --port=80

echo "Waiting for the Pod to become Ready..."
kubectl wait --for=condition=Ready pod/hello-k8s --timeout=120s

echo "Step 3: Verify the Pod is running"
kubectl get pods

echo "Step 4: Expose the Pod as a NodePort Service"
kubectl expose pod hello-k8s --type=NodePort --port=80

echo "Step 5: Open the app (prints URL; keep terminal open with docker driver)"
minikube service hello-k8s --url
