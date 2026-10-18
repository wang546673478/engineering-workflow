import os
from pathlib import Path
import subprocess
import sys
import unittest


FINALIZER = (
    Path(__file__).resolve().parents[2]
    / ".github"
    / "scripts"
    / "finalize_reviewed_quality.py"
)


class ReviewedWorkflowFinalizerTests(unittest.TestCase):
    def run_finalizer(self, checker, diagnostic):
        env = os.environ.copy()
        env["CHECK_OUTCOME"] = checker
        env["DIAGNOSE_OUTCOME"] = diagnostic
        return subprocess.run(
            [sys.executable, str(FINALIZER)],
            capture_output=True,
            text=True,
            env=env,
            check=False,
        )

    def test_diagnostic_success_does_not_recover_failed_required_check(self):
        result = self.run_finalizer("failure", "success")

        self.assertEqual(result.returncode, 1)
        self.assertIn("does not replace the required check", result.stderr)

    def test_failed_required_check_stays_failed_when_diagnostic_fails(self):
        result = self.run_finalizer("failure", "failure")

        self.assertEqual(result.returncode, 1)
        self.assertIn("see the diagnostic step", result.stderr)

    def test_successful_required_check_passes_when_diagnostic_is_skipped(self):
        result = self.run_finalizer("success", "skipped")

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stderr, "")


if __name__ == "__main__":
    unittest.main()
