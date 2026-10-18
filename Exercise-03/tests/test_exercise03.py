"""Tests for Exercise-03: flash-sale endpoints + ReplicaSet manifest."""
import pathlib
import socket
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-03/
sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


class TestFlashSaleApp(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_homepage(self):
        data = self.client.get("/").get_json()
        self.assertEqual(data["message"], "Welcome to Big Sale!")
        self.assertEqual(data["pod"], socket.gethostname())

    def test_buy_with_user(self):
        data = self.client.get("/buy?user=123").get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["user"], "123")
        self.assertIn(data["item"], ["Smartphone", "Shoes", "Headphones", "Laptop"])
        self.assertIn("served_by_pod", data)

    def test_buy_random_user(self):
        self.assertTrue(self.client.get("/buy").get_json()["user"].startswith("user"))

    def test_health(self):
        resp = self.client.get("/health")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json()["status"], "healthy")


class TestManifests(unittest.TestCase):
    def test_replicaset(self):
        docs = {d["kind"]: d for d in yaml.safe_load_all(
            (ROOT / "k8s" / "flashsale-replicaset.yaml").read_text())}
        rs = docs["ReplicaSet"]
        self.assertEqual(rs["metadata"]["name"], "flashsale-rs")
        self.assertEqual(rs["spec"]["replicas"], 3)
        c = rs["spec"]["template"]["spec"]["containers"][0]
        self.assertEqual(c["image"], "flashsale:1.0")
        self.assertEqual(c["readinessProbe"]["httpGet"]["path"], "/health")
        self.assertEqual(c["livenessProbe"]["httpGet"]["path"], "/health")
        svc = docs["Service"]["spec"]
        self.assertEqual((svc["ports"][0]["port"], svc["ports"][0]["targetPort"]), (80, 5000))
        self.assertEqual(svc["selector"], rs["spec"]["selector"]["matchLabels"])

    def test_dockerfile_module_matches_file(self):
        df = (ROOT / "Dockerfile").read_text()
        self.assertIn("COPY app.py", df)
        self.assertIn('"app:app"', df)

    def test_challenge_deployment(self):
        d = yaml.safe_load((ROOT / "k8s" / "challenge-flashsale-deployment.yaml").read_text())
        self.assertEqual(d["kind"], "Deployment")


if __name__ == "__main__":
    unittest.main()
