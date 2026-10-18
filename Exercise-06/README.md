# Exercise-06 — Real-Time Operations Monitoring and Alerting (Grafana)

**Reference:** `Exercises/6-Grafana-Realtime-Monitoring-of-Quick-Commerce-App.md`

## Objective
As a DevOps engineer at ZAPPTTO (quick-commerce delivery), build monitoring that simulates
delivery metrics (Python), scrapes them (Prometheus), visualises them (Grafana), raises
alerts, and automates the stack with a Jenkins pipeline.

## Requirements
- Tools: Docker, Python ≥ 3.10, Jenkins, Prometheus, Grafana; `pip3 install prometheus-client`
- Directory `delivery_monitoring/` with `delivery_metrics.py`, `prometheus.yml`,
  `alert_rules.yml`, `Jenkinsfile`
- Metrics: `total_deliveries`, `pending_deliveries`, `on_the_way_deliveries` (Gauges),
  `average_delivery_time` (Summary), served on `:8000/metrics`, updated every second
- Prometheus scrapes itself + `172.17.0.1:8000`; loads `alert_rules.yml`
- Alerts: `HighPendingDeliveries` (`> 10` for 15s, warning) and
  `HighAverageDeliveryTime` (avg `> 30`, critical)
- Grafana on :3000, Prometheus data source, dashboard with 4 panels
- Jenkins (Docker) pipeline: Pre-check Docker → Setup Workspace → Build Image → Run App →
  Run Prometheus & Grafana
- Step 6: raise pending range to 50–100 and verify alerts

## Files
| File | Purpose |
|------|---------|
| `delivery_monitoring/delivery_metrics.py` | Metrics simulator |
| `delivery_monitoring/prometheus.yml` | Scrape config |
| `delivery_monitoring/alert_rules.yml` | Alert rules |
| `delivery_monitoring/Jenkinsfile` | Pipeline |
| `delivery_monitoring/Dockerfile` + `requirements.txt` | Image used by the pipeline's build stage |
| `delivery_monitoring/grafana-dashboard.json` | Importable dashboard (4 panels) |
| `scripts/run_stack.sh` / `scripts/cleanup.sh` | Manual run / stop |
| `tests/test_exercise06.py` | Runs the app and validates configs |

## How to run manually (Linux/WSL; working directory: `Exercise-06/delivery_monitoring/`)
```bash
pip3 install prometheus-client
python3 delivery_metrics.py            # terminal 1
curl http://localhost:8000/metrics     # terminal 2

docker run -d --name prometheus --network=host \
  -v ./prometheus.yml:/etc/prometheus/prometheus.yml \
  -v ./alert_rules.yml:/etc/prometheus/alert_rules.yml prom/prometheus
docker run -d --name grafana -p 3000:3000 grafana/grafana
ip addr show docker0                   # note the IP, e.g. 172.17.0.1
```
Or: `bash ../scripts/run_stack.sh`

- Prometheus: http://localhost:9090 → Status → Targets (both UP), Alerts tab.
- Grafana: http://localhost:3000 → log in with Grafana's built-in first-login account (see the
  reference; Grafana forces/offers a password change — choose your own) → Connections →
  Data sources → Prometheus → URL `http://172.17.0.1:9090` → Save & Test.
- Dashboards → New → Import → upload `grafana-dashboard.json` (or build the 4 panels by hand:
  `total_deliveries`, `pending_deliveries`, `on_the_way_deliveries`,
  `average_delivery_time_sum / average_delivery_time_count`).

### Step 6 — simulate alerts
```bash
SIMULATE_ALERTS=1 python3 delivery_metrics.py   # pending in 50–100
docker restart prometheus
```
(Equivalent to editing the line to `random.randint(50, 100)` as the reference describes.)

### Jenkins pipeline
```bash
mkdir delivery_monitoring          # already provided in this repo
docker ps -a | grep prom           # verify Prometheus is up
docker ps -a | grep jenkins        # Step 5a: check for an existing Jenkins
docker rm <container-id>           # remove an exited/old Jenkins instance if needed
docker run -d -p 8080:8080 -p 50000:50000 --name jenkins -v jenkins_home:/var/jenkins_home jenkins/jenkins:lts
docker exec -it jenkins bash
  cat /var/jenkins_home/secrets/initialAdminPassword
  exit
```
(The reference also shows the shorter form without a volume:
`docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts`.)
New Item → Pipeline → either *Pipeline script* (paste `Jenkinsfile`, set parameter
`SOURCE_DIR` accordingly) or *Pipeline script from SCM* pointing at your repo with script path
`Exercise-06/delivery_monitoring/Jenkinsfile`.

> The Jenkins container needs a Docker CLI and access to a Docker daemon (e.g. a custom
> image with docker-cli plus `-v /var/run/docker.sock:/var/run/docker.sock`). Otherwise the
> *Pre-check Docker* stage fails with the clear message built into the pipeline.

## Expected outputs
1. `/metrics` shows the 4 delivery metrics + Python process metrics.
2. Prometheus graphs for `total_deliveries`, `pending_deliveries`, `average_delivery_time`.
3. Grafana dashboard with live panels.
4. Jenkins console: all stages green, `Finished: SUCCESS`.
5. Prometheus Alerts: `HighPendingDeliveries` firing (pending > 10 almost always).

## Testing
```bash
python -m unittest discover -s Exercise-06/tests -v   # from project root
```

## Assumptions / changes
| Change | Reason |
|--------|--------|
| Jenkinsfile `localSourcePath` = relative `SOURCE_DIR` parameter | No absolute paths allowed; files come from the SCM checkout |
| Added `Dockerfile` + `requirements.txt` | The pipeline's `docker build` needs a Dockerfile; reference did not supply one |
| `docker rm -f ... || true` before `docker run` in pipeline | Pipeline can be re-run without name conflicts |
| `SIMULATE_ALERTS` / `METRICS_PORT` env vars | Step 6 without editing code; port override for tests. Defaults match the reference |
| File named `alert_rules.yml` | The reference tree says `alerts_rules.yml` but every command uses `alert_rules.yml` |
| Bind mounts in the Jenkins stage use `$WORKSPACE` | Kept as in reference; if Jenkins runs in Docker using the host socket, the path must exist on the host (mount the workspace at the same path) |
