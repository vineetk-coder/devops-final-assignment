# Exercise-10 — Multi-Node Kubernetes Cluster with Multiple Applications and ReplicaSets

**Reference:** `Exercises/10-Minikube-Multi-Node-Multi-App-Minikube-Deployment.md`

## Storyboard
E-commerce platform: **Product Catalog** (AppA, 2 replicas) and **Shopping Cart** (AppB,
3 replicas), each replica on a different node for high availability.

## Requirements
0. `minikube stop` / `minikube delete`
1a. `minikube start --nodes 3 -p devops-multinode --force`
1b. `minikube -p devops-multinode addons enable registry`
2–3. `product_catalog.py` (`GET /products`) and `shopping_cart.py` (`GET/POST /cart`), port 80
4. `Dockerfile.product`, `Dockerfile.shopping`; build `product-catalog:latest`, `shopping-cart:latest`
5. `minikube -p devops-multinode image load ...`; verify with `minikube ssh -- docker images`
6. Deployments with `podAntiAffinity` (required, `kubernetes.io/hostname`), `imagePullPolicy: Never`
7. NodePort Services
8. `kubectl get pods -o wide` → each replica on a different node
9. `minikube -p devops-multinode service <svc>` (each in its own terminal)
10. curl tests

## Files
| File | Purpose |
|------|---------|
| `product_catalog.py`, `shopping_cart.py` | The two apps |
| `Dockerfile.product`, `Dockerfile.shopping` | Images |
| `k8s/*_deployment.yaml`, `k8s/*_service.yaml` | Manifests |
| `scripts/run.sh` | Steps 0–8 |
| `scripts/curl_tests.sh` | Step 10 |
| `scripts/cleanup.sh` | Tear down |
| `tests/test_exercise10.py` | App + manifest tests |

## How to run (Linux/WSL; working directory: `Exercise-10/`)
> The reference keeps the YAML files next to the code (`kubectl apply -f product_catalog_deployment.yaml`).
> Here they are in `k8s/`, so the commands use `k8s/<file>`. The curl ports (`35855`, `38975`)
> are examples; use the URLs that `minikube service` prints for you.
```bash
minikube stop; minikube delete
minikube start --nodes 3 -p devops-multinode --force
minikube -p devops-multinode addons enable registry
docker build -t product-catalog:latest -f Dockerfile.product .
docker build -t shopping-cart:latest -f Dockerfile.shopping .
minikube -p devops-multinode image load product-catalog:latest
minikube -p devops-multinode image load shopping-cart:latest
minikube -p devops-multinode ssh -- docker images
kubectl apply -f k8s/product_catalog_deployment.yaml
kubectl apply -f k8s/shopping_cart_deployment.yaml
kubectl apply -f k8s/product_catalog_service.yaml
kubectl apply -f k8s/shopping_cart_service.yaml
kubectl get pods -o wide
minikube -p devops-multinode service product-catalog-service   # terminal 2
minikube -p devops-multinode service shopping-cart-service     # terminal 3
bash scripts/curl_tests.sh <product-url> <cart-url>
```
Shortcut for steps 0–8: `bash scripts/run.sh`

## Expected output
```
product-catalog-...-2jlnv  Running  devops-multinode-m02
product-catalog-...-7v556  Running  devops-multinode-m03
shopping-cart-...-7l4lx    Running  devops-multinode
shopping-cart-...-d48w2    Running  devops-multinode-m02
shopping-cart-...-hml9r    Running  devops-multinode-m03

curl <product-url>/products -> [{"id":1,"name":"Laptop","price":1200}, ...]
curl <cart-url>/cart        -> []
curl -X POST ... /cart      -> [{"id":1,"name":"Laptop","quantity":1}]
```

## Testing
```bash
python -m unittest discover -s Exercise-10/tests -v    # from project root
```

## Assumptions / changes
| Change | Reason |
|--------|--------|
| `shopping_cart_deployment.yaml` namespace `devops-exercise` → `default` | Namespace was never created (apply fails) and the Service is in `default`, so it would never reach the pods |
| `--force` kept | Reference uses it (only needed when running as root) |

> Each cart replica keeps its own in-memory cart, so a later `GET /cart` may hit a different
> pod and show a different cart — expected for this stateless lab.
