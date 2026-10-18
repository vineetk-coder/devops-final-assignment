#!/usr/bin/env bash
# Exercise-09: simulate the Jenkins pipeline stages locally (Linux/WSL/Git Bash).
# Run from Exercise-09/python-flask-app:  bash ../scripts/simulate_pipeline.sh
set -euo pipefail
WORKSPACE="$(pwd)"
DEPLOY_DIR="$WORKSPACE/python-app-deploy"

echo "== Build =="
python3 -m venv venv
if [ -f venv/bin/activate ]; then . venv/bin/activate; else . venv/Scripts/activate; fi
pip install -q -r requirements.txt flake8

echo "== Code Quality =="
flake8 . --exclude=venv,python-app-deploy --max-line-length=120

echo "== Test =="
python -m unittest discover -s .

echo "== Deploy =="
mkdir -p "$DEPLOY_DIR"
cp app.py "$DEPLOY_DIR/"

echo "== Run Application =="
nohup python "$DEPLOY_DIR/app.py" > "$DEPLOY_DIR/app.log" 2>&1 &
echo $! > "$DEPLOY_DIR/app.pid"

echo "== Test Application =="
python test_app.py

kill "$(cat "$DEPLOY_DIR/app.pid")" 2>/dev/null || true
echo "Pipeline completed successfully!"
