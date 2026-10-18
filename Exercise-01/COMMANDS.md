# Exercise 01 - Kubernetes Getting Started

All commands are run from inside the `Exercise-01/` folder unless noted.

## Prerequisites

Install `kubectl` and Minikube (see [README.md](README.md) for OS-specific install commands).

```bash
minikube version
kubectl version --client
```

## Start Minikube

```bash
minikube start
```

## Create the Pod

```bash
kubectl run hello-k8s --image=nginx --port=80
kubectl wait --for=condition=Ready pod/hello-k8s --timeout=120s
```

## Verify the Pod

```bash
kubectl get pods
```

## Expose the Pod as a NodePort Service

```bash
kubectl expose pod hello-k8s --type=NodePort --port=80
kubectl get services
```

## Access the Application

```bash
minikube service hello-k8s
# or print the URL only and test it
minikube service hello-k8s --url
curl $(minikube service hello-k8s --url)
```

## Declarative Alternative (manifest)

```bash
kubectl apply -f k8s/hello-k8s.yaml
```

## Automated Script

```bash
bash scripts/run.sh
```

## Run Tests (from the project root)

```bash
python -m unittest discover -s Exercise-01/tests -v
```

## Cleanup

```bash
bash scripts/cleanup.sh
# equivalent to:
kubectl delete service hello-k8s --ignore-not-found
kubectl delete pod hello-k8s --ignore-not-found
```
