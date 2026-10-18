"""Tests for Exercise-04: REST API + Dockerfile/script checks."""
import pathlib
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-04/
sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


class TestAboutApi(unittest.TestCase):
    def test_about(self):
        resp = app.test_client().get("/about")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.get_json(), {
            "name": "Simple REST API",
            "version": "1.0",
            "description": "This is a simple REST API built with Flask.",
        })


class TestDockerAssets(unittest.TestCase):
    def test_dockerfile(self):
        df = (ROOT / "Dockerfile").read_text()
        for s in ("FROM python:3.9-slim", "EXPOSE 5001", "iputils-ping", 'CMD ["python", "app.py"]'):
            self.assertIn(s, df)

    def test_script_has_all_tasks(self):
        s = (ROOT / "scripts" / "run.sh").read_text()
        for cmd in ("docker network create --driver bridge my-bridge-net",
                    "docker network ls", "docker network inspect my-bridge-net",
                    "docker build -t flask-api .",
                    "--name mysql --net=my-bridge-net", "--name redis --net=my-bridge-net",
                    "--name flask --net=my-bridge-net -p 5001:5001 flask-api",
                    "ping -c 2 mysql", "ping -c 2 redis"):
            self.assertIn(cmd, s)
        self.assertNotIn("MYSQL_ROOT_PASSWORD=", s)  # no hard-coded password

    def test_cleanup(self):
        s = (ROOT / "scripts" / "cleanup.sh").read_text()
        self.assertIn("docker network rm my-bridge-net", s)


if __name__ == "__main__":
    unittest.main()
