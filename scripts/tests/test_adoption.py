import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock


SCRIPTS = Path(__file__).resolve().parents[1]
ADOPT = SCRIPTS / "adopt_project.py"
INIT = SCRIPTS / "init_manifest.py"
sys.path.insert(0, str(SCRIPTS))
import adopt_project
import init_manifest


class AdoptionTests(unittest.TestCase):
    def setUp(self):
        environment = mock.patch.dict(os.environ, {})
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("ENGINEERING_TASK_ID", None)
        os.environ.pop("ENGINEERING_CONTROL_PLANE_APPROVED", None)

    def command(self, root, *extra):
        return subprocess.run(
            [sys.executable, str(ADOPT), "--root", str(root), "--profile", "lite",
             "--skill-source", "C:/skills/engineering-workflow/SKILL.md",
             "--skill-version", "1.6.4", *extra], capture_output=True, text=True)

    def test_complete_adoption_creates_a_real_manifest_and_incomplete_discovery_entry(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            source = root / "backend/app.py"
            source.write_text("print('preserve source')", encoding="utf-8")
            result = self.command(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((root / "engineering-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["workflow"]["stage"], "takeover_discovery")
            self.assertEqual(data["workflow"]["active_task"], "TASK-01")
            self.assertEqual(data["baseline"]["status"], "planned")
            self.assertEqual(data["adoption"]["status"], "initialized_incomplete")
            self.assertEqual(data["adoption"]["skill_version"], "1.6.4")
            self.assertEqual(data["tasks"][0]["implementation_authorization"]["status"], "pending")
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertIn("engineering-manifest.json", (root / "AGENTS.md").read_text(encoding="utf-8"))
            self.assertEqual(source.read_text(encoding="utf-8"), "print('preserve source')")
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "initialized_incomplete")
            self.assertEqual(report["bootstrap"]["report"]["mode"], "discovery")
            self.assertFalse(report["bootstrap"]["report"]["required_checks_satisfied"])
            self.assertTrue(report["bootstrap"]["report"]["checks"])

    def test_existing_manifest_is_never_overwritten(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            result = subprocess.run([sys.executable, str(INIT), "--root", str(root), "--profile", "lite"], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            manifest = root / "engineering-manifest.json"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["workflow"] = {key: value for key, value in data["workflow"].items() if key.startswith("active_")}
            manifest.write_text(json.dumps(data), encoding="utf-8")
            original = manifest.read_bytes()
            result = self.command(root)
            self.assertEqual(result.returncode, 2)
            self.assertIn("legacy manifest preserved", result.stderr)
            self.assertEqual(manifest.read_bytes(), original)
            self.assertFalse((root / "AGENTS.md").exists())

    def test_same_lifecycle_manifest_is_reused_without_rewriting_its_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            first = self.command(root)
            self.assertEqual(first.returncode, 0, first.stderr)
            manifest = root / "engineering-manifest.json"
            data = json.loads(manifest.read_text(encoding="utf-8"))
            data["checks"][0]["command"] = [sys.executable, "-c", "from pathlib import Path; Path('must-not-run').touch()"]
            manifest.write_text(json.dumps(data), encoding="utf-8")
            original = manifest.read_bytes()
            result = self.command(root)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(result.stdout)["status"], "lifecycle_manifest_reused")
            self.assertEqual(manifest.read_bytes(), original)
            self.assertFalse((root / "must-not-run").exists())

    def legacy_manifest(self, root):
        (root / "backend").mkdir()
        data = init_manifest.manifest(root, "lite")
        data["workflow"] = {key: value for key, value in data["workflow"].items() if key.startswith("active_")}
        data.pop("adoption")
        data["tasks"][0].pop("implementation_authorization")
        data["history"] = [{"review": "preserve prior scope"}]
        path = root / "engineering-manifest.json"
        path.write_text(json.dumps(data), encoding="utf-8")
        return path, data

    def test_explicit_legacy_upgrade_preserves_existing_policy_documents_and_history(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, original = self.legacy_manifest(root)
            result = self.command(root, "--upgrade-legacy-manifest")
            self.assertEqual(result.returncode, 0, result.stderr)
            upgraded = json.loads(path.read_text(encoding="utf-8"))
            for key in ("documents", "checks", "requirements", "acceptance", "modules", "inventories", "baseline", "history"):
                self.assertEqual(upgraded[key], original[key], key)
            self.assertEqual(upgraded["tasks"][0]["approval"], original["tasks"][0]["approval"])
            self.assertEqual(upgraded["workflow"]["baseline_review"]["status"], "pending")
            self.assertEqual(upgraded["workflow"]["proposal_approval"]["status"], "pending")
            self.assertEqual(upgraded["tasks"][0]["implementation_authorization"]["status"], "pending")
            self.assertEqual(json.loads(result.stdout)["bootstrap"]["report"]["mode"], "discovery")

    def test_failed_legacy_replacement_leaves_original_bytes_and_guidance_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path, _ = self.legacy_manifest(root)
            original = path.read_bytes()
            with mock.patch.object(adopt_project.os, "replace", side_effect=OSError("fixture replacement denied")):
                code = adopt_project.main([
                    "--root", str(root), "--upgrade-legacy-manifest",
                    "--skill-source", str(SCRIPTS.parent / "SKILL.md"), "--skill-version", "1.7.0"])
            self.assertEqual(code, 2)
            self.assertEqual(path.read_bytes(), original)
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertEqual(sorted(p.name for p in root.iterdir()), ["backend", "engineering-manifest.json"])

    def test_invalid_adoption_targets_and_document_overrides_write_nothing(self):
        for options in (("--file", "engineering-manifest.json"),
                        ("--state-dir", "../outside"),
                        ("--document", "UNKNOWN=docs/spec.md"),
                        ("--document", "SPEC=docs/a.md", "--document", "SPEC=docs/b.md")):
            with self.subTest(options=options), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                (root / "backend").mkdir()
                result = self.command(root, *options)
                self.assertEqual(result.returncode, 2, result.stdout)
                self.assertEqual([p.name for p in root.iterdir()], ["backend"])

    def test_existing_documents_and_task_can_be_mapped_without_creating_duplicates(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "backend").mkdir()
            (root / "docs/tasks").mkdir(parents=True)
            for path in ("docs/SPEC.md", "docs/PLAN.md", "docs/tasks/current.md"):
                (root / path).write_text("existing authority", encoding="utf-8")
            result = self.command(root, "--state-dir", "project-state", "--task-id", "TASK-PI-01",
                                  "--document", "SPEC=docs/SPEC.md", "--document", "PLAN=docs/PLAN.md",
                                  "--document", "TASK=docs/tasks/current.md")
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads((root / "engineering-manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(data["workflow"]["active_task"], "TASK-PI-01")
            self.assertEqual(data["documents"][1]["path"], "docs/SPEC.md")
            self.assertEqual(data["documents"][2]["path"], "docs/PLAN.md")
            self.assertEqual(data["documents"][3]["path"], "docs/tasks/current.md")
            self.assertEqual(data["documents"][0]["path"], "project-state/baseline-review.md")
            self.assertEqual((root / "docs/SPEC.md").read_text(encoding="utf-8"), "existing authority")

    def test_prose_cannot_be_used_as_manifest_path(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/tasks").mkdir(parents=True)
            (root / "docs/tasks/README.md").write_text("task list", encoding="utf-8")
            result = self.command(root, "--manifest", "docs/tasks/README.md")
            self.assertEqual(result.returncode, 2)
            self.assertFalse((root / "AGENTS.md").exists())
            self.assertEqual((root / "docs/tasks/README.md").read_text(encoding="utf-8"), "task list")


if __name__ == "__main__":
    unittest.main()
