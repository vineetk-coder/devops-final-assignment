# Exercise-03 — Scaling a Flask App on a Single Node using ReplicaSets

**Reference:** `Exercises/3-Minikube-Scaling-Flask-App-with-Replicasets.md`

## Use case
E-commerce flash sale (Big Billion Days / Prime Day): traffic spikes from 100 to 10,000
req/min. A ReplicaSet scales the Flask service out to many identical Pods and back down.

## Objective
- Understand ReplicaSets and Pods
- Scale the Flask app
- Observe pod distribution (and self-healing when a pod is deleted)

## Requirements
- Flask app with `/` (welcome), `/buy` (random item, `?user=` param, `served_by_pod`), `/health`
- Dockerfile: python:3.11-slim, flask + gunicorn on port 5000
- Build image (optionally push to Docker Hub)
- `minikube stop/delete`, then `minikube start --nodes=1`
- ReplicaSet `flashsale-rs` (3 replicas, readiness/liveness probes, resource requests/limits)
  + ClusterIP Service `flashsale-svc` (80 → 5000)
- Scale to 5, delete one pod, verify it is replaced, view `-o wide`
- Additional challenges: different image, Deployment instead of RS, `kubectl describe`

## Files
| File | Purpose |
|------|---------|
| `app.py` | Flash-sale Flask app |
| `Dockerfile` | gunicorn-based image |
| `k8s/flashsale-replicaset.yaml` | ReplicaSet + Service |
| `k8s/challenge-flashsale-deployment.yaml` | Challenge: Deployment version |
| `scripts/run.sh` | All steps end-to-end |
| `scripts/push-image.sh` | Optional Docker Hub push (uses `DOCKERHUB_USERNAME`) |
| `scripts/cleanup.sh` | Cleanup |
| `tests/test_exercise03.py` | Endpoint + manifest tests |

## How to run (working directory: `Exercise-03/`, Linux/WSL shell)
```bash
minikube stop && minikube delete
minikube start --nodes=1
kubectl get nodes
eval $(minikube docker-env)
docker build -t flashsale:1.0 .
kubectl apply -f k8s/flashsale-replicaset.yaml
kubectl get pods
kubectl get rs
kubectl scale rs flashsale-rs --replicas=5
kubectl get rs
kubectl get pods
kubectl delete pod <one-pod-name>
kubectl get pods
kubectl get pods -o wide
```
Shortcut: `bash scripts/run.sh`

## Expected output
```
replicaset.apps/flashsale-rs created
service/flashsale-svc created
NAME           DESIRED   CURRENT   READY
flashsale-rs   3         3         3
replicaset.apps/flashsale-rs scaled
flashsale-rs   5         5         5
```
After deleting a pod, a new one (young AGE) appears; total stays 5, all on node `minikube`.

### Optional: build and push to Docker Hub (reference step)
```bash
docker login                                       # interactive, never store the password
docker build -t <your-dockerhub-username>/flashsale:1.0 .
docker push <your-dockerhub-username>/flashsale:1.0
```
(or `DOCKERHUB_USERNAME=<you> bash scripts/push-image.sh`)

### Additional challenges (from the reference)
```bash
# 1. Use a different image: edit image: in k8s/flashsale-replicaset.yaml, e.g.
#    <your-dockerhub-username>/flashsale:1.0, then:
kubectl apply -f k8s/flashsale-replicaset.yaml
kubectl delete pods -l app=flashsale              # RS recreates pods with the new image

# 2. Deployment instead of ReplicaSet
kubectl delete rs flashsale-rs
kubectl apply -f k8s/challenge-flashsale-deployment.yaml
kubectl get deploy,rs,pods

# 3. Inspect with describe
kubectl describe rs flashsale-rs
kubectl describe pod <pod-name>
```
Tips: `kubectl get pods -o wide`, `kubectl logs <pod-name>`, `kubectl exec -it <pod-name> -- sh`.

## Testing
```bash
python -m unittest discover -s Exercise-03/tests -v     # from project root
```

## Q&A (from the reference)
1. Initial replicas: **3** 2. Pods after apply: **3**
3. Scale to 5 → 2 extra pods are created.
4. Delete one pod → a replacement is created automatically (stays at 5).
5. The controller continuously reconciles actual vs desired count.
6. Nodes: **1** 7. All 5 pods run on the single node.

## Assumptions / fixes to reference inconsistencies
| Reference | Implemented | Why |
|-----------|-------------|-----|
| Dockerfile `COPY ex3-flash-sale.py` but `CMD ... app:app` | File named `app.py` | gunicorn needs module `app`; otherwise the container crashes |
| Step 5 builds `flask-app` | Build `flashsale:1.0` | Manifest uses `image: flashsale:1.0` |
| Steps 6–11 use `flask-app-rs` | Use `flashsale-rs` | Name defined in the manifest |
| No `imagePullPolicy` | `IfNotPresent` (explicit) | Same as default for a tagged image; makes the local-image intent clear |
| Image built after apply | Image built before apply | Avoids `ErrImagePull` at start (pods would recover anyway) |
