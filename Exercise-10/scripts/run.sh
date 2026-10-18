#!/usr/bin/env bash
# Exercise-10: 3-node Minikube cluster, 2 apps, pods spread across nodes.
# Run from the Exercise-10 folder:  bash scripts/run.sh
set -euo pipefail
P=devops-multinode

echo "Step 0: Clean up"
minikube stop || true
minikube delete || true

echo "Step 1a: Start a 3-node cluster (--force only needed when running as root)"
minikube start --nodes 3 -p "$P" --force

echo "Step 1b: Enable the registry addon"
minikube -p "$P" addons enable registry

echo "Step 4: Build images"
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .

echo "Step 5: Load images into all cluster nodes"
minikube -p "$P" image load product-catalog:latest
minikube -p "$P" image load shopping-cart:latest
minikube -p "$P" ssh -- docker images | grep -E 'product-catalog|shopping-cart'

echo "Step 6: Deploy"
kubectl apply -f k8s/product_catalog_deployment.yaml
kubectl apply -f k8s/shopping_cart_deployment.yaml

echo "Step 7: Expose"
kubectl apply -f k8s/product_catalog_service.yaml
kubectl apply -f k8s/shopping_cart_service.yaml

kubectl rollout status deployment/product-catalog --timeout=180s
kubectl rollout status deployment/shopping-cart --timeout=180s

echo "Step 8: Verify distribution (each replica on a different node)"
kubectl get nodes
kubectl get pods -o wide

echo "Step 9: Open each service in its own terminal:"
echo "  minikube -p $P service product-catalog-service"
echo "  minikube -p $P service shopping-cart-service"
