# DevOps Lab — Exercise Implementations

Implementations of the **10 exercises** in the reference `DevOps-Lab-main.zip`
(folder `Exercises/`). The ZIP is kept here unchanged, as read-only reference material.

| Folder | Exercise | Main tools |
|--------|----------|------------|
| [Exercise-01](Exercise-01/) | Kubernetes Getting Started: Hello Pod (nginx) | Minikube, kubectl |
| [Exercise-02](Exercise-02/) | Deploy a Flask app on Minikube with kubectl + YAML | Docker, Minikube |
| [Exercise-03](Exercise-03/) | Scaling a Flask app with ReplicaSets (flash sale) | Minikube, gunicorn |
| [Exercise-04](Exercise-04/) | Docker networking: Flask + MySQL + Redis | Docker bridge network |
| [Exercise-05](Exercise-05/) | Docker security with AppArmor + Docker SDK for Python | AppArmor, docker-py |
| [Exercise-06](Exercise-06/) | Real-time monitoring and alerting (quick commerce) | Prometheus, Grafana, Jenkins |
| [Exercise-07](Exercise-07/) | Introduction to CI and Jenkins installation | Jenkins (Docker) |
| [Exercise-08](Exercise-08/) | "Hello World" Jenkins freestyle job | Git, GitHub, Jenkins |
| [Exercise-09](Exercise-09/) | Jenkins multi-stage pipeline (Build/Test/Deploy) | Jenkinsfile, unittest, flake8 |
| [Exercise-10](Exercise-10/) | Multi-node Minikube, multiple apps, anti-affinity | Minikube (3 nodes) |

Every exercise folder has its own `README.md`. Each one covers the objective, requirements,
files, exact commands, expected output, testing steps, and any documented deviations from
the reference.

## Prerequisites
- Python 3.10+
- Docker
- Minikube + kubectl (Exercises 1–3 and 10)
- A Linux shell, such as WSL2 on Windows, for the `.sh` scripts and AppArmor

## Run the offline test suite (from this folder)
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate     Linux/macOS: source .venv/bin/activate
pip install -r requirements-dev.txt
python scripts/run_all_tests.py      # writes reports/test_results.md
```

## Configuration
No secrets are needed. `.env.example` lists the optional identifiers (Docker Hub and GitHub
usernames). If you use it, copy it to `.env`. Git ignores `.env`.

## Reports
- [PROJECT_REPORT.md](PROJECT_REPORT.md): full build, test and audit report
- [reports/test_results.md](reports/test_results.md): latest automated test output
