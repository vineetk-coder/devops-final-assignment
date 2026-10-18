#!/usr/bin/env bash
# Exercise-03: Scale the flash-sale app with a ReplicaSet on a single node.
# Run from the Exercise-03 folder:  bash scripts/run.sh
set -euo pipefail

echo "Step 1: Clean up any previous cluster"
minikube stop || true
minikube delete || true

echo "Step 2: Start Minikube with a single node"
minikube start --nodes=1
kubectl get nodes

echo "Build the image inside Minikube's Docker daemon (so pods can use it)"
eval "$(minikube docker-env)"
docker build -t flashsale:1.0 .

echo "Steps 3-4: Apply the ReplicaSet + Service"
kubectl apply -f k8s/flashsale-replicaset.yaml
sleep 15

echo "Step 6: Verify pods and ReplicaSet (expect 3)"
kubectl get pods
kubectl get rs

echo "Step 7: Scale to 5 replicas"
kubectl scale rs flashsale-rs --replicas=5
sleep 15

echo "Steps 8-9: Verify (expect 5)"
kubectl get rs
kubectl get pods

echo "Step 10: Delete one pod — the ReplicaSet will replace it"
POD=$(kubectl get pods -l app=flashsale -o jsonpath='{.items[0].metadata.name}')
kubectl delete pod "$POD"
sleep 10

echo "Step 11: Verify pods again (still 5) and distribution across nodes"
kubectl get pods
kubectl get pods -o wide

echo "Load distribution demo: call /buy 5 times through the Service"
kubectl run curl-test --rm -i --restart=Never --image=curlimages/curl -- \
  sh -c 'for i in 1 2 3 4 5; do curl -s http://flashsale-svc/buy?user=$i; echo; done'
