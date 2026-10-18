"""Static checks for Exercise-01 (no cluster required)."""
import pathlib
import unittest

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-01/


class TestExercise01(unittest.TestCase):
    def test_manifest_is_valid(self):
        docs = list(yaml.safe_load_all((ROOT / "k8s" / "hello-k8s.yaml").read_text()))
        kinds = {d["kind"]: d for d in docs}
        self.assertEqual(kinds["Pod"]["spec"]["containers"][0]["image"], "nginx")
        self.assertEqual(kinds["Pod"]["spec"]["containers"][0]["ports"][0]["containerPort"], 80)
        self.assertEqual(kinds["Service"]["spec"]["type"], "NodePort")
        # Service selector must match the Pod labels
        self.assertEqual(kinds["Service"]["spec"]["selector"], kinds["Pod"]["metadata"]["labels"])

    def test_script_contains_lab_commands(self):
        script = (ROOT / "scripts" / "run.sh").read_text()
        for cmd in ("minikube start",
                    "kubectl run hello-k8s --image=nginx --port=80",
                    "kubectl get pods",
                    "kubectl expose pod hello-k8s --type=NodePort --port=80",
                    "minikube service hello-k8s"):
            self.assertIn(cmd, script)


if __name__ == "__main__":
    unittest.main()
