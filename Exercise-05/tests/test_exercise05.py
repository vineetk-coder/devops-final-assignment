"""Offline tests for Exercise-05 (no Docker/AppArmor needed)."""
import pathlib
import re
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-05/
sys.path.insert(0, str(ROOT))

from app import app  # noqa: E402


class TestApp(unittest.TestCase):
    def test_home(self):
        resp = app.test_client().get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertIn("secure Flask application", resp.data.decode())


class TestProfile(unittest.TestCase):
    def setUp(self):
        self.text = (ROOT / "apparmor" / "my-apparmor-profile").read_text()

    def test_profile_name_matches_docker_option(self):
        self.assertRegex(self.text, r"profile\s+my-apparmor-profile\b")

    def test_required_rules_present(self):
        for rule in ("deny /etc/** r,", "deny /var/** rw,", "network inet stream,",
                     "/app/** rwk,", "deny /bin/** rmix,", "deny /usr/bin/** rmix,",
                     "capability net_bind_service,", "deny capability sys_admin,"):
            self.assertIn(rule, self.text)

    def test_braces_balanced(self):
        body = re.sub(r"#.*", "", self.text)
        self.assertEqual(body.count("{"), body.count("}"))


class TestScripts(unittest.TestCase):
    def test_scripts_compile(self):
        for f in ("apply_apparmor.py", "test_restricted_actions.py"):
            # in-memory compile: validates syntax without writing .pyc files
            compile((ROOT / f).read_text(encoding="utf-8"), f, "exec")

    def test_scripts_use_profile(self):
        for f in ("apply_apparmor.py", "test_restricted_actions.py"):
            self.assertIn('security_opt=["apparmor=my-apparmor-profile"]', (ROOT / f).read_text())


if __name__ == "__main__":
    unittest.main()
