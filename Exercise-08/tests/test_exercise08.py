"""Tests for Exercise-08: hello-world.sh content and (if bash exists) its output."""
import pathlib
import shutil
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-08/
SCRIPT = ROOT / "hello-world.sh"


def find_bash():
    # On Windows prefer Git-for-Windows bash, found relative to git.exe (<Git>/cmd/git.exe)
    git = shutil.which("git")
    if git:
        candidate = pathlib.Path(git).resolve().parent.parent / "bin" / "bash.exe"
        if candidate.exists():
            return str(candidate)
    return shutil.which("bash")


class TestHelloWorld(unittest.TestCase):
    def test_content(self):
        raw = SCRIPT.read_bytes()
        self.assertNotIn(b"\r\n", raw, "must use LF line endings for bash/Jenkins")
        self.assertTrue(raw.startswith(b"#!/bin/bash\n"))
        self.assertIn(b'echo "Hello, Jenkins!"', raw)

    def test_output(self):
        bash = find_bash()
        if not bash:
            self.skipTest("bash not available")
        out = subprocess.run([bash, "hello-world.sh"], cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(out.returncode, 0)
        self.assertEqual(out.stdout.strip(), "Hello, Jenkins!")


if __name__ == "__main__":
    unittest.main()
