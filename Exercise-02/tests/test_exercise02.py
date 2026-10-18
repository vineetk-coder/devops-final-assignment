"""Tests for Exercise-02: Flask app behaviour + Kubernetes manifests."""
import pathlib
import sys
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-02/
sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


class TestFlaskApp(unittest.TestCase):
    def test_home(self):
        resp = app.test_client().get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.data.decode(), "Hello from Flask on Kubernetes!")


class TestManifests(unittest.TestCase):
    def load(self, name):
        return {d["kind"]: d for d in yaml.safe_load_all((ROOT / "k8s" / name).read_text())}

    def test_step5_has_only_deployment(self):
        docs = self.load("flask-deployment-step5.yaml")
        self.assertEqual(set(docs), {"Deployment"})

    def test_final_manifest(self):
        docs = self.load("flask-deployment.yaml")
        c = docs["Deployment"]["spec"]["template"]["spec"]["containers"][0]
        self.assertEqual(c["image"], "flask-app:latest")
        self.assertEqual(c["imagePullPolicy"], "Never")
        self.assertEqual(c["ports"][0]["containerPort"], 15000)
        svc = docs["Service"]["spec"]
        self.assertEqual(svc["type"], "NodePort")
        self.assertEqual(svc["ports"][0]["port"], 15000)
        self.assertEqual(svc["ports"][0]["targetPort"], 15000)
        self.assertEqual(svc["selector"], docs["Deployment"]["spec"]["selector"]["matchLabels"])


if __name__ == "__main__":
    unittest.main()
