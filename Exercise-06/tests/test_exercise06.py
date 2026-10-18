"""Tests for Exercise-06: runs the metrics app for real and checks /metrics + configs."""
import json
import os
import pathlib
import socket
import subprocess
import sys
import time
import unittest
import urllib.request

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-06/
APP_DIR = ROOT / "delivery_monitoring"


def free_port():
    with socket.socket() as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


def scrape(port, retries=20):
    for _ in range(retries):
        try:
            return urllib.request.urlopen(f"http://127.0.0.1:{port}/metrics", timeout=2).read().decode()
        except OSError:
            time.sleep(0.5)
    raise RuntimeError("metrics endpoint did not come up")


def metric(text, name):
    for line in text.splitlines():
        if line.startswith(name + " "):
            return float(line.split()[1])
    raise KeyError(name)


class RunningApp:
    def __init__(self, simulate_alerts=False):
        self.port = free_port()
        env = dict(os.environ, METRICS_PORT=str(self.port),
                   SIMULATE_ALERTS="1" if simulate_alerts else "0")
        self.proc = subprocess.Popen([sys.executable, "delivery_metrics.py"], cwd=APP_DIR, env=env,
                                     stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

    def __enter__(self):
        time.sleep(2.5)  # let at least two simulation cycles run
        return self

    def __exit__(self, *exc):
        self.proc.terminate()
        self.proc.wait(timeout=10)


class TestMetricsApp(unittest.TestCase):
    def test_metrics_endpoint_normal_mode(self):
        with RunningApp() as app:
            text = scrape(app.port)
        for name in ("total_deliveries", "pending_deliveries", "on_the_way_deliveries",
                     "average_delivery_time_sum", "average_delivery_time_count"):
            self.assertIn(name, text)
        self.assertTrue(10 <= metric(text, "pending_deliveries") <= 20)
        self.assertTrue(5 <= metric(text, "on_the_way_deliveries") <= 20)
        self.assertGreater(metric(text, "average_delivery_time_count"), 0)
        avg = metric(text, "average_delivery_time_sum") / metric(text, "average_delivery_time_count")
        self.assertTrue(15 <= avg <= 45)

    def test_simulate_alerts_mode(self):
        with RunningApp(simulate_alerts=True) as app:
            text = scrape(app.port)
        self.assertTrue(50 <= metric(text, "pending_deliveries") <= 100)


class TestConfigs(unittest.TestCase):
    def test_prometheus_yml(self):
        cfg = yaml.safe_load((APP_DIR / "prometheus.yml").read_text())
        jobs = {j["job_name"]: j for j in cfg["scrape_configs"]}
        self.assertIn("prometheus", jobs)
        self.assertEqual(jobs["delivery_service"]["static_configs"][0]["targets"], ["172.17.0.1:8000"])
        self.assertEqual(cfg["rule_files"], ["/etc/prometheus/alert_rules.yml"])

    def test_alert_rules(self):
        cfg = yaml.safe_load((APP_DIR / "alert_rules.yml").read_text())
        rules = {r["alert"]: r for r in cfg["groups"][0]["rules"]}
        self.assertEqual(rules["HighPendingDeliveries"]["expr"], "pending_deliveries > 10")
        self.assertEqual(rules["HighPendingDeliveries"]["for"], "15s")
        self.assertIn("average_delivery_time_sum / average_delivery_time_count",
                      rules["HighAverageDeliveryTime"]["expr"])
        self.assertEqual(rules["HighAverageDeliveryTime"]["labels"]["severity"], "critical")

    def test_dashboard_has_four_panels(self):
        dash = json.loads((APP_DIR / "grafana-dashboard.json").read_text())
        exprs = [p["targets"][0]["expr"] for p in dash["panels"]]
        self.assertEqual(exprs, ["total_deliveries", "pending_deliveries", "on_the_way_deliveries",
                                 "average_delivery_time_sum / average_delivery_time_count"])

    def test_jenkinsfile(self):
        jf = (APP_DIR / "Jenkinsfile").read_text()
        for stage in ("Pre-check Docker", "Setup Workspace", "Build Docker Image",
                      "Run Application", "Run Prometheus & Grafana"):
            self.assertIn(f"stage('{stage}')", jf)
        self.assertNotIn("/path/to/your/local/files'", jf.split("pipeline {", 1)[1])
        self.assertEqual(jf.count("{"), jf.count("}"))


if __name__ == "__main__":
    unittest.main()
