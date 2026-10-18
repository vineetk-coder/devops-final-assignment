#!/usr/bin/env bash
# Exercise-06: stop everything started by run_stack.sh or the Jenkins pipeline.
# Run from Exercise-06/delivery_monitoring:  bash ../scripts/cleanup.sh
set -uo pipefail
[ -f delivery_metrics.pid ] && kill "$(cat delivery_metrics.pid)" 2>/dev/null; rm -f delivery_metrics.pid
docker rm -f prometheus grafana delivery_metrics 2>/dev/null
echo "Stopped."
