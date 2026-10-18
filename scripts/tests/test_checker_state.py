import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import test_checker as support

SCRIPTS = support.SCRIPTS


class CheckerStateTests(unittest.TestCase):
    def fixture(self):
        workspace = SCRIPTS.parent / "work" / "checker-state-tests"
        workspace.mkdir(parents=True, exist_ok=True)
        factory = tempfile.TemporaryDirectory
        fixture = support.CheckerTests("test_invalid_reference")
        with patch("test_checker.tempfile.TemporaryDirectory", side_effect=lambda *a, **kw: factory(*a, dir=workspace, **kw)):
            fixture.setUp()
        self.addCleanup(fixture.doCleanups)
        self.addCleanup(fixture.tearDown)
        return fixture

    def prepare(self, mode, code):
        f = self.fixture()
        f.manifest["tasks"][0]["documentation_impact"] = {"implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}}
        f.manifest["checks"][0]["command"] = [sys.executable, "-c", code]
        f.write(); f.git("add", ".")
        f.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "check configuration")
        (f.root / "src/app.py").write_text("REVIEWED = True\n", encoding="utf-8")
        (f.root / "docs/impact.md").write_text("reviewed impact", encoding="utf-8")
        f.git("add", "src/app.py", "docs/impact.md")
        if mode == "committed":
            f.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "reviewed source")
        return f

    def test_both_modes_reject_index_and_worktree_drift_without_restoring_files(self):
        for mode in ("commit", "committed"):
            for stage in (False, True):
                with self.subTest(mode=mode, stage=stage):
                    code = "from pathlib import Path; import subprocess; Path('src/app.py').write_text('CHANGED = True\\n');"
                    if stage:
                        code += "subprocess.run(['git','add','src/app.py'],check=True);"
                    f = self.prepare(mode, code)
                    proc, report = f.fixture_cli(f.root, mode)
                    self.assertEqual(proc.returncode, 1, report)
                    state = next(c for c in report["checks"] if c["rule_id"] == "verification-state")
                    self.assertEqual(state["status"], "fail")
                    self.assertIsNone(report["verified_tree"])
                    self.assertIn("CHANGED", (f.root / "src/app.py").read_text())
                    self.assertIn("src/app.py", state["evidence"]["index_paths" if stage else "worktree_paths"])

    def test_head_change_is_rejected_even_when_index_tree_is_unchanged(self):
        code = "import subprocess; subprocess.run(['git','-c','user.name=Test','-c','user.email=test@example.invalid','commit','--allow-empty','-m','check changed HEAD'],check=True)"
        f = self.prepare("commit", code)
        proc, report = f.fixture_cli(f.root, "commit")
        state = next(c for c in report["checks"] if c["rule_id"] == "verification-state")
        self.assertEqual(proc.returncode, 1, report)
        self.assertEqual(state["evidence"]["before"]["tree"], state["evidence"]["after"]["tree"])
        self.assertNotEqual(state["evidence"]["before"]["head"], state["evidence"]["after"]["head"])

    def test_nonignored_new_files_fail_but_generated_ignored_outputs_succeed(self):
        for filename, expected in (("unexpected.txt", 1), ("command-ran.txt", 0)):
            with self.subTest(filename=filename):
                f = self.prepare("commit", f"from pathlib import Path; Path({filename!r}).write_text('generated')")
                proc, report = f.fixture_cli(f.root, "commit")
                self.assertEqual(proc.returncode, expected, report)
                if expected == 0:
                    tree = subprocess.check_output(["git", "write-tree"], cwd=f.root, text=True).strip()
                    self.assertEqual(report["verified_tree"], tree)
                    f.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "verified source")
                    self.assertEqual(tree, subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=f.root, text=True).strip())

    def test_real_precommit_template_binds_the_tree_that_git_commits(self):
        f = self.prepare("commit", "print('hook fixture')")
        hook = f.root / ".git/hooks/pre-commit"
        hook.write_bytes((SCRIPTS.parent / "assets/templates/pre-commit.engineering").read_bytes().replace(b"\r\n", b"\n"))
        hook.chmod(0o755)
        expected = subprocess.check_output(["git", "write-tree"], cwd=f.root, text=True).strip()
        env = {**os.environ, "PYTHON": Path(sys.executable).as_posix(),
               "ENGINEERING_PROJECT_ROOT": f.root.as_posix(), "ENGINEERING_MANIFEST": "manifest.json",
               "ENGINEERING_WORKFLOW_SKILL_DIR": SCRIPTS.parent.as_posix(), "ENGINEERING_TASK_ID": "TASK-1"}
        proc = subprocess.run(["git", "-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "verified by real hook"], cwd=f.root, env=env, capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertIn(expected, proc.stdout + proc.stderr)
        self.assertEqual(expected, subprocess.check_output(["git", "rev-parse", "HEAD^{tree}"], cwd=f.root, text=True).strip())

    def raw_json_cli(self, f, content):
        (f.root / "manifest.json").write_text(content, encoding="utf-8")
        proc = subprocess.run([sys.executable, str(SCRIPTS / "check_project.py"), "--root", str(f.root), "--manifest", "manifest.json", "--mode", "baseline", "--run-checks"], capture_output=True, text=True)
        self.assertNotIn("Traceback", proc.stderr)
        return proc, json.loads(proc.stdout)

    def test_json_limits_and_root_types_are_structured_and_do_not_run_commands(self):
        f = self.fixture()
        f.manifest["checks"][0]["command"] = [sys.executable, "-c", "open('command-ran.txt','w').write('ran')"]
        base = json.dumps(f.manifest)[:-1] + ',"extra":'
        inputs = ["[]", "null", base + '{"a":' * 10000 + '{}' + '}' * 10000 + '}',
                  base + '[' * 10000 + '0' + ']' * 10000 + '}']
        digit_limit = getattr(sys, "get_int_max_str_digits", lambda: 0)()
        if digit_limit:
            inputs.append(base + '9' * (digit_limit + 1) + '}')
        for content in inputs:
            with self.subTest(prefix=content[:20]):
                proc, report = self.raw_json_cli(f, content)
                self.assertEqual(proc.returncode, 2, report)
                self.assertFalse(report["required_checks_satisfied"])
                self.assertTrue(report["errors"])
                self.assertFalse((f.root / "command-ran.txt").exists())

    def test_large_shallow_manifest_retains_existing_compatibility(self):
        f = self.fixture()
        f.manifest["extra"] = "x" * (1024 * 1024 + 1)
        proc, report = self.raw_json_cli(f, json.dumps(f.manifest))
        self.assertEqual(proc.returncode, 0, report)

    def test_corrupt_git_manifest_cannot_be_treated_as_missing_policy(self):
        for bad in ('{"a":' * 10000 + '{}' + '}' * 10000, "[]"):
            with self.subTest(root=bad[:10]):
                f = self.prepare("commit", "open('command-ran.txt','w').write('ran')")
                (f.root / "manifest.json").write_text(bad, encoding="utf-8")
                f.git("add", "manifest.json")
                f.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "corrupt historical policy")
                f.write()
                f.git("add", "manifest.json")
                proc, report = f.fixture_cli(f.root, "commit")
                self.assertEqual(proc.returncode, 2, report)
                self.assertFalse((f.root / "command-ran.txt").exists())
                self.assertFalse(report["required_checks_satisfied"])
                self.assertTrue("historical manifest" in json.dumps(report) or "invalid JSON" in json.dumps(report))

    def test_unreadable_historical_blob_is_not_first_adoption(self):
        f = self.fixture()
        original = support.checker.subprocess.run
        def unreadable(argv, **kwargs):
            if "show" in argv:
                return subprocess.CompletedProcess(argv, 1, b"", b"unavailable blob fixture")
            return original(argv, **kwargs)
        with patch.object(support.checker.subprocess, "run", side_effect=unreadable):
            with self.assertRaises(support.checker.ConfigError):
                support.checker.manifest_from_git(f.root, "HEAD", "manifest.json")


if __name__ == "__main__":
    unittest.main()
