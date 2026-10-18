#!/usr/bin/env bash
# Exercise-06: run the monitoring stack manually (without Jenkins).
# Run from Exercise-06/delivery_monitoring:  bash ../scripts/run_stack.sh
# Linux/WSL (uses --network=host for Prometheus, as in the reference).
set -euo pipefail

pip3 install prometheus-client

echo "Starting metrics app in background (logs: delivery_metrics.log)"
nohup python3 delivery_metrics.py > delivery_metrics.log 2>&1 &
echo $! > delivery_metrics.pid
sleep 2
curl -s http://localhost:8000/metrics | grep -E '^(total|pending|on_the_way|average)_' || true

echo "Starting Prometheus (http://localhost:9090)"
docker rm -f prometheus >/dev/null 2>&1 || true
docker run -d --name prometheus --network=host \
  -v "$(pwd)/prometheus.yml:/etc/prometheus/prometheus.yml" \
  -v "$(pwd)/alert_rules.yml:/etc/prometheus/alert_rules.yml" \
  prom/prometheus

echo "Starting Grafana (http://localhost:3000)"
docker rm -f grafana >/dev/null 2>&1 || true
docker run -d --name grafana -p 3000:3000 grafana/grafana

ip addr show docker0 || true
echo "Add Prometheus data source in Grafana with URL http://<docker0-IP>:9090 (e.g. 172.17.0.1)"
