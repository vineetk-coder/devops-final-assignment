"""Checks for Exercise-09: runs the app's unit test and validates the Jenkinsfile."""
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-09/
APP = ROOT / "python-flask-app"


class TestExercise09(unittest.TestCase):
    def test_unittest_discover_passes(self):
        # Same command as the pipeline's Test stage
        r = subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "."],
                           cwd=APP, capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("Hello, Jenkins Multi-Stage Pipeline!", r.stdout + r.stderr)
        self.assertIn("OK", r.stderr)

    def test_jenkinsfile_stages(self):
        jf = (APP / "Jenkinsfile").read_text()
        for stage in ("Build", "Test", "Deploy", "Run Application", "Test Application"):
            self.assertIn(f"stage('{stage}')", jf)
        self.assertIn("python3 -m unittest discover -s .", jf)
        self.assertIn("python-app-deploy", jf)
        self.assertIn("Pipeline completed successfully!", jf)
        self.assertEqual(jf.count("{"), jf.count("}"))

    def test_requirements(self):
        self.assertIn("flask==2.1.2", (APP / "requirements.txt").read_text())


if __name__ == "__main__":
    unittest.main()
