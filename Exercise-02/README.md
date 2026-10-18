# Exercise-02 — Deploy a Flask app on Minikube using kubectl and YAML

**Reference:** `Exercises/2-Minikube-Kubectl-Flask.md`

## Objective
Use Minikube (single-node cluster) to deploy a Python Flask application with a Deployment,
then expose it with a NodePort Service.

## Requirements
1. `minikube start`
2. `app.py` — Flask app returning `Hello from Flask on Kubernetes!` on port **15000**
3. `Dockerfile` (python:3.8-slim, installs flask, runs `python app.py`)
4. Build the image with Minikube's Docker daemon (`eval $(minikube docker-env)`)
5. `flask-deployment.yaml` — Deployment, `image: flask-app:latest`, `imagePullPolicy: Never`
6–10. Apply, check deployments, pods, describe, logs
11–12. Check services; `curl 127.0.0.1:15000` fails (port not exposed externally)
13. Add a NodePort Service (`port: 15000`, `targetPort: 15000`) and access it via
    `minikube service flask-app-service --url`

## Prerequisites (from the reference)
- The Illustrated Children's Guide to Kubernetes: https://www.cncf.io/phippy/the-childrens-illustrated-guide-to-kubernetes/
- Video: https://www.youtube.com/watch?v=3I9PkvZ80BQ
- Install Minikube: https://minikube.sigs.k8s.io/docs/ (see Exercise-01 for OS commands)
- Watch: Origins of Kubernetes with Tim Hockin: https://www.youtube.com/watch?v=xSztxKexDXM
- Watch: Kubernetes in Its Second Decade (Tim Hockin): https://www.youtube.com/watch?v=WqeShpaztZY

## Minikube cheat sheet (frequently used commands)
```
# 1. Starting and Stopping Minikube
minikube start                            # Start Minikube with default settings
minikube start --kubernetes-version=v1.21.2  # Start with a specific Kubernetes version
minikube stop                             # Stop Minikube without deleting
minikube delete                           # Delete Minikube cluster

# 2. Checking Status and Information
minikube status                           # Check Minikube status
kubectl cluster-info                      # Display cluster information

# 3. Accessing Services
minikube service <service-name>           # Open specified service in browser
minikube service list                     # List URLs of all services
minikube tunnel                           # Create a network tunnel to access LoadBalancer services

# 4. Docker with Minikube
eval $(minikube docker-env)               # Use Minikube's Docker daemon
docker build -t my-image .                # Build image directly in Minikube
minikube image load my-image              # Load a local image into Minikube

# 5. Debugging and Logs
minikube logs                             # View Minikube logs
minikube dashboard                        # Open the Kubernetes dashboard
minikube ssh                              # SSH into the Minikube VM
```

## Files
| File | Purpose |
|------|---------|
| `app.py` | Flask app |
| `Dockerfile` | Container image definition |
| `k8s/flask-deployment-step5.yaml` | Step 5 manifest (Deployment only) |
| `k8s/flask-deployment.yaml` | Step 13 manifest (Deployment + Service) |
| `scripts/deploy.sh` / `scripts/cleanup.sh` | Automate deploy / cleanup |
| `tests/test_exercise02.py` | App + manifest tests |

## How to run (working directory: `Exercise-02/`, Linux/WSL shell)
```bash
minikube start
minikube docker-env
eval $(minikube docker-env)
docker build -t flask-app .

kubectl apply -f k8s/flask-deployment-step5.yaml   # Step 6
kubectl get deployments                            # Step 7
kubectl get pods -l app=flask-app                  # Step 8
kubectl describe deployment flask-app              # Step 9
kubectl logs <pod-name>                            # Step 10
kubectl get services                               # Step 11
curl http://127.0.0.1:15000                        # Step 12 -> fails (expected)

kubectl apply -f k8s/flask-deployment.yaml         # Step 13
minikube service flask-app-service --url
curl <URL printed above>                           # in a NEW terminal
```
Shortcut: `bash scripts/deploy.sh`

## Expected output
```
deployment.apps/flask-app unchanged
service/flask-app-service created
$ curl http://127.0.0.1:<port>
Hello from Flask on Kubernetes!
```

## Testing
```bash
python -m unittest discover -s Exercise-02/tests -v   # from project root
```

## Q&A (from the reference)
1. `minikube service flask-app-service --url` → gives the URL to reach the service.
2. It checks the service is running, generates a URL, prints it.
3. `targetPort` = port the container listens on.
4. `port` = exposed Service port; `targetPort` = container port.
5. Use `minikube service <service-name> --url`.
6. With the Docker driver on Linux the tunnel lives in that terminal.
7. `--url` avoids building the URL by hand.
8. `kubectl expose` or `kubectl apply -f <service.yaml>`.
9. Minikube runs a local single-node cluster for testing.
10. `kubectl` is the CLI used to deploy, scale and manage resources.

## Notes
- The Dockerfile copies only `app.py` (reference used `COPY . /app`) so tests/scripts are not
  baked into the image — behaviour is identical.
