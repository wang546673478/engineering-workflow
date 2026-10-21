import json
import os
from pathlib import Path
import subprocess
import shutil
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
import check_project as checker
import init_manifest as initializer


class InitManifestTests(unittest.TestCase):
    def setUp(self):
        # Generated fixture manifests must not inherit the enclosing CI task.
        environment = mock.patch.dict(os.environ, {})
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("ENGINEERING_TASK_ID", None)
        os.environ.pop("ENGINEERING_CONTROL_PLANE_APPROVED", None)

    def test_generated_profiles_prune_dependencies_before_link_validation(self):
        for profile in ("lite", "full"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                (root / "packages/a/src").mkdir(parents=True)
                source = root / "packages/a/src/main.ts"
                source.write_text("export const x=1", encoding="utf-8")
                before = initializer.manifest(root, profile)
                links = []
                for folder in ("node_modules", "packages/a/node_modules", "apps/a/node_modules", "nested/deeper/app/node_modules"):
                    link = root / folder / "vitest"
                    link.parent.mkdir(parents=True)
                    link.write_text("link fixture", encoding="utf-8")
                    links.append(link)
                similar = root / "packages/a/node_modules_custom/owned.ts"
                similar.parent.mkdir()
                similar.write_text("authored source", encoding="utf-8")
                after = initializer.manifest(root, profile)
                self.assertEqual(before["exclude_paths"], after["exclude_paths"])
                excludes = checker.build_exclude_specs(root, after["exclude_paths"])
                original = checker.is_link
                with mock.patch.object(checker, "is_link", side_effect=lambda p: p in links or original(p)):
                    walked = list(checker.iter_module_paths(root, root, excludes))
                self.assertIn(source, walked)
                self.assertIn(similar, walked)
                self.assertTrue(all(link not in walked for link in links))
                unsafe = root / "packages/a/src/linked-source"
                unsafe.write_text("unexcluded link fixture", encoding="utf-8")
                with mock.patch.object(checker, "is_link", side_effect=lambda p: p == unsafe or original(p)):
                    with self.assertRaises(checker.ConfigError):
                        list(checker.iter_module_paths(root, root, excludes))

    def test_lite_profile_discovers_sources_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            command = [sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", tmp, "--profile", "lite"]
            result = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((root / "engineering-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["modules"][0]["source_paths"], ["backend"])
            self.assertTrue(next(doc for doc in data["documents"] if doc["id"] == "DB")["required"])
            self.assertEqual(data["workflow"]["active_baseline"], "BASELINE")
            self.assertEqual(data["workflow"]["active_spec"], "SPEC")
            self.assertEqual(data["workflow"]["active_plan"], "PLAN")
            self.assertEqual(data["tasks"][0]["artifact_links"]["task"], "TASK")
            again = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(again.returncode, 2)

    def test_output_escape_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run([sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", tmp, "--output", "../manifest.json"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)

    def test_greenfield_lifecycle_roundtrip(self):
        for profile in ("lite", "full"):
            with self.subTest(profile=profile), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp).resolve()
                result = subprocess.run([sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", str(root),
                                         "--profile", profile, "--project-kind", "greenfield"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                manifest_path = root / "engineering-manifest.json"
                data = json.loads(manifest_path.read_text(encoding="utf-8"))
                self.assertEqual(data["baseline"]["status"], "planned")
                self.assertEqual(data["baseline"]["implementation_paths"], ["src", "tests"])
                self.assertEqual(data["workflow"]["approval_policy"], {"record_contract": 1, "enforcement": "diagnostic", "sequence_enforcement": "diagnostic", "minimum_checker_version": "1.8.0"})
                self.assertFalse((root / "src").exists())
                # A real agent supplies evidence, documents and project checks.
                for doc in data["documents"]:
                    path = root / doc["path"]
                    path.parent.mkdir(parents=True, exist_ok=True)
                    path.write_text("REQ-BOOTSTRAP-01 AT-BOOTSTRAP-01\nNo implementation yet; target belongs in Plan.", encoding="utf-8")
                (root / "planning/approval.md").write_text("fixture approval record", encoding="utf-8")
                data["checks"][0]["command"] = [sys.executable, "-c", "print('fixture verification')"]
                command = [sys.executable, str(SCRIPTS / "check_project.py"), "--root", str(root),
                           "--manifest", "engineering-manifest.json", "--mode", "baseline", "--run-checks"]
                def check(expected):
                    manifest_path.write_text(json.dumps(data), encoding="utf-8")
                    proc = subprocess.run(command, capture_output=True, text=True)
                    report = json.loads(proc.stdout)
                    self.assertEqual(proc.returncode, expected, report)
                    return report
                check(1)  # Initialization never manufactures completion.
                data["baseline"].update(status="not_applicable", reason="Reviewed empty implementation scope",
                                        source_revision="empty-tree-2026-10-18", scope="src and tests; no prior implementation")
                report = check(0)
                lifecycle = next(item for item in report["checks"] if item["rule_id"] == "baseline-lifecycle")
                self.assertFalse(lifecycle["evidence"]["completion_ready"])
                (root / "src").mkdir()
                (root / "src/app.py").write_text("print('first implementation')", encoding="utf-8")
                check(1)
                data["baseline"]["status"] = "partial"
                check(0)
                data["tasks"][0]["status"] = "complete"
                check(1)
                (root / "tests").mkdir()
                data["baseline"]["status"] = "complete"
                check(0)
                if shutil.which("git"):
                    # Check a real developing tree: approval and documentation
                    # gates remain active while the baseline is provisional.
                    git_prefix = ["git", "-c", "safe.directory=" + str(root)]
                    def git(*args):
                        proc = subprocess.run(git_prefix + list(args), cwd=root, capture_output=True, text=True)
                        self.assertEqual(proc.returncode, 0, proc.stderr)
                    git("init")
                    git("add", ".")
                    git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "first slice")
                    data["tasks"][0]["status"] = "in_progress"
                    data["baseline"]["status"] = "partial"
                    change_command = command.copy()
                    change_command[change_command.index("baseline")] = "change"
                    change_command.extend(["--base", "HEAD"])
                    def change(expected):
                        manifest_path.write_text(json.dumps(data), encoding="utf-8")
                        proc = subprocess.run(change_command, capture_output=True, text=True)
                        report = json.loads(proc.stdout)
                        self.assertEqual(proc.returncode, expected, report)
                        return report
                    change(1)  # Implementation remains blocked in takeover discovery.
                    data["tasks"][0]["approval"] = {"status":"approved", "evidence":"planning/task.md"}
                    data["workflow"]["stage"] = "implementation"
                    data["workflow"]["baseline_review"] = {"status":"approved", "source_revision":data["baseline"]["source_revision"], "evidence":"planning/baseline-review.md"}
                    data["workflow"]["proposal_approval"] = {"status":"approved", "revision":"PLAN-01", "evidence":"planning/approval.md"}
                    data["tasks"][0]["implementation_authorization"] = {"status":"approved", "plan_revision":"PLAN-01", "evidence":"planning/approval.md", "task_id":"TASK-01"}
                    for doc in data["documents"]:
                        path = root / doc["path"]
                        path.write_text(path.read_text(encoding="utf-8") + "\nUpdated first-slice evidence.", encoding="utf-8")
                    (root / "src/app.py").write_text("print('updated implementation')", encoding="utf-8")
                    report = change(0)
                    self.assertEqual(next(item for item in report["checks"] if item["rule_id"] == "change-scope")["status"], "pass")
                    data["tasks"][0]["status"] = "complete"
                    data["baseline"].update(status="approved", source_revision="final-baseline-r1")
                    data["workflow"]["stage"] = "complete"
                    data["workflow"]["baseline_review"]["source_revision"] = "final-baseline-r1"
                    data["tasks"][0]["skill_review"].update(catalog_source="fixture skills", scope="first slice", recheck="none")
                    manifest_path.write_text(json.dumps(data), encoding="utf-8")
                    handoff_command = change_command.copy()
                    handoff_command[handoff_command.index("change")] = "handoff"
                    proc = subprocess.run(handoff_command, capture_output=True, text=True)
                    self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_existing_flat_sources_do_not_emit_root_or_unowned_triggers(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            (root / "main.py").write_text("print('flat project')", encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", str(root)], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr)
            path = root / "engineering-manifest.json"
            data = json.loads(path.read_text(encoding="utf-8"))
            for doc in data["documents"]:
                target = root / doc["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("REQ-BOOTSTRAP-01 AT-BOOTSTRAP-01", encoding="utf-8")
            data["baseline"]["status"] = "complete"
            data["checks"][0]["command"] = [sys.executable, "-c", "print('fixture')"]
            path.write_text(json.dumps(data), encoding="utf-8")
            proc = subprocess.run([sys.executable, str(SCRIPTS / "check_project.py"), "--root", str(root), "--manifest", "engineering-manifest.json", "--mode", "baseline", "--run-checks"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stdout)

    def test_greenfield_custom_scope_and_invalid_scopes(self):
        with tempfile.TemporaryDirectory() as tmp:
            command = [sys.executable, str(SCRIPTS / "init_manifest.py"), "--root", tmp, "--project-kind", "greenfield"]
            for raw in (".", "../outside", "src/*"):
                result = subprocess.run(command + ["--implementation-path", raw], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertFalse((Path(tmp) / "engineering-manifest.json").exists())
            result = subprocess.run(command + ["--implementation-path", "backend"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((Path(tmp) / "engineering-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["baseline"]["implementation_paths"], ["backend"])

    def test_approval_strict_mode_is_explicit(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            data = initializer.manifest(root, "lite", approval_enforcement="strict")
            self.assertEqual(data["workflow"]["approval_policy"]["enforcement"], "strict")


if __name__ == "__main__":
    unittest.main()
