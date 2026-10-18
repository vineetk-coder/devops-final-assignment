# Exercise-01 — Kubernetes Getting Started: Hello Pod

**Reference:** `Exercises/1-Kubernetes-Getting-Started.md`

## Objective
As a DevOps engineer at Zepto, deploy the storefront web app (simulated with the `nginx`
image) on Kubernetes so it is always running, portable and can be scaled later.

## Requirements (from the reference)
- Minikube installed with Docker or a VM driver.
- Start a local cluster with Minikube.
- Create a Pod `hello-k8s` from the `nginx` image on port 80.
- Verify the Pod is running.
- Expose the Pod as a `NodePort` Service.
- Open it with `minikube service hello-k8s` → nginx welcome page.

## Pre-requisites: install Minikube (one-time setup)
You need **Docker** or a VM driver (VirtualBox, Hyper-V) installed.

Linux:
```bash
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```
macOS (Homebrew):
```bash
brew install minikube
```
Windows (PowerShell as Administrator):
```powershell
choco install minikube
```
WSL (inside the WSL terminal):
```bash
sudo apt-get update -y
sudo apt-get install -y curl apt-transport-https virtualbox virtualbox-ext-pack
curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube
```

## Files
| File | Purpose |
|------|---------|
| `scripts/run.sh` | The exact lab commands, in order |
| `scripts/cleanup.sh` | Deletes the Pod and Service |
| `k8s/hello-k8s.yaml` | Optional declarative (YAML) equivalent |
| `tests/test_exercise01.py` | Static checks (YAML valid, commands present) |

## How to run (working directory: `Exercise-01/`)
```bash
minikube start
kubectl run hello-k8s --image=nginx --port=80
kubectl get pods
kubectl expose pod hello-k8s --type=NodePort --port=80
minikube service hello-k8s
```
Or simply: `bash scripts/run.sh`

Declarative alternative (use instead of `kubectl run`/`expose`, not in addition):
```bash
kubectl apply -f k8s/hello-k8s.yaml
```

## Expected output
```
pod/hello-k8s created
NAME        READY   STATUS    RESTARTS   AGE
hello-k8s   1/1     Running   0          10s
service/hello-k8s exposed
```
The browser shows **"Welcome to nginx!"**.

## Testing
```bash
python -m unittest discover -s Exercise-01/tests -v     # from project root
curl $(minikube service hello-k8s --url)                # live check, needs cluster
```

## Cleanup
`bash scripts/cleanup.sh`

## Notes
- Installation commands (Linux / macOS / Windows `choco install minikube` / WSL) are in the
  reference file and are unchanged.
- With the Docker driver on Linux/WSL, `minikube service` must stay open in its terminal.
