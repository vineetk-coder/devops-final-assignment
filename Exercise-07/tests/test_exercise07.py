"""Static checks for Exercise-07."""
import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parent.parent  # Exercise-07/


class TestExercise07(unittest.TestCase):
    def test_start_script(self):
        s = (ROOT / "scripts" / "start-jenkins.sh").read_text()
        self.assertIn("docker run -d --name jenkins -p 8080:8080 -p 50000:50000 jenkins/jenkins:lts", s)

    def test_password_script_reads_from_container(self):
        s = (ROOT / "scripts" / "get-initial-password.sh").read_text()
        self.assertIn("/var/jenkins_home/secrets/initialAdminPassword", s)

    def test_readme_covers_ci_concepts(self):
        r = (ROOT / "README.md").read_text()
        for topic in ("Continuous Integration", "GitLab CI/CD", "CircleCI", "Travis CI", "Bamboo",
                      "TeamCity", "Azure DevOps", "GitHub Actions", "Spinnaker", "Buildkite", "Drone",
                      "Job/Project", "Pipeline", "Plugins", "Nodes"):
            self.assertIn(topic, r)


if __name__ == "__main__":
    unittest.main()
