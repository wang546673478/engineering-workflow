import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPTS = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("install_agents_guidance", SCRIPTS / "install_agents_guidance.py")
guidance = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guidance)


class GuidanceTests(unittest.TestCase):
    def test_generic_workflow_contracts_are_documented(self):
        root = SCRIPTS.parent
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        requirements = (root / "references" / "requirements-interview.md").read_text(encoding="utf-8")
        source_context = (root / "references" / "source-context.md").read_text(encoding="utf-8")
        implementation = (root / "references" / "implementation-workflow.md").read_text(encoding="utf-8")

        for field in ("question_id", "status", "asked_at", "answer_ref", "scope", "resume_condition"):
            self.assertIn(field, requirements)
        self.assertIn("现成工具优先", skill)
        self.assertIn("精确全量分析", skill)
        self.assertIn("unknown/unsupported", source_context)
        self.assertIn("Environment contract and startup diagnostics", implementation)
        self.assertIn("Reports are never portable across worktrees", implementation)

    def test_defect_guidance_defaults_to_cause_correction_or_tracks_mitigation(self):
        root = SCRIPTS.parent
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        implementation = (root / "references" / "implementation-workflow.md").read_text(encoding="utf-8")
        defect = implementation.split("## Defect evidence within the existing task", 1)[1].split("## Isolated investigation environments", 1)[0]

        self.assertIn("只有恢复或强制诊断出的不变量的 guard 才算修复", skill)
        self.assertIn("仅隐藏症状的兜底须在明确延期根因修复时标为缓解", skill)
        self.assertIn("smallest complete correction that removes it", defect)
        self.assertIn("restores or enforces the violated invariant", defect)
        for mitigation_record in (
            "label containment as a mitigation",
            "why correction is deferred",
            "residual risk",
            "could mask",
            "owner or trigger for revisiting the cause",
            "validation that checks the mitigation",
        ):
            with self.subTest(mitigation_record=mitigation_record):
                self.assertIn(mitigation_record, defect)

    def test_task_check_sets_preserve_policy_and_exact_tree_receipts(self):
        root = SCRIPTS.parent
        skill = (root / "SKILL.md").read_text(encoding="utf-8")
        implementation = (root / "references" / "implementation-workflow.md").read_text(encoding="utf-8")
        feedback = implementation.split("### Feedback, verification and progress", 1)[1].split("\n## During editing", 1)[0]

        self.assertIn("按其实际影响确定适用检查集", skill)
        self.assertIn("At Task planning, choose its `required_checks` from the Task's actual impact", feedback)
        self.assertIn("Preserve every check the project requires for all Tasks", feedback)
        self.assertIn("instead of inheriting unrelated checks", feedback)
        self.assertIn("does not justify removing or weakening a declared check", feedback)
        self.assertIn("Do not rerun unaffected product suites unless the project policy requires them or their inputs changed", feedback)
        self.assertIn("earlier code or deployment reports remain evidence only for the exact tree they verified", feedback)
        self.assertIn("exact-tree `commit`/`committed` checks", feedback)

    def test_manifest_template_declares_logical_environment_contract(self):
        root = SCRIPTS.parent
        manifest = json.loads((root / "assets" / "templates" / "project-manifest.example.json").read_text(encoding="utf-8"))
        tool = manifest["environment"]["tools"][0]
        for key in ("tool_id", "version", "purpose", "locator", "identity_check", "cache_policy", "isolation", "status"):
            self.assertIn(key, tool)
        self.assertEqual(manifest["environment"]["evidence"], "planning/task-environment.json")

    def test_source_analysis_fixture_binds_precise_full_evidence(self):
        root = SCRIPTS.parent
        fixture = json.loads((root / "assets" / "templates" / "source-analysis-evidence.example.json").read_text(encoding="utf-8"))
        final = fixture["final_analysis"]
        preview = fixture["development_preview"]

        self.assertEqual(final["mode"], "precise-full")
        self.assertTrue(final["eligible_as_final_evidence"])
        self.assertTrue(fixture["adapter"]["deterministic"])
        self.assertFalse(fixture["adapter"]["model_required"])
        self.assertRegex(final["input_fingerprint"], r"^[0-9a-f]{64}$")
        self.assertEqual(final["input_fingerprint"], fixture["current_input_fingerprint"])
        self.assertTrue(final["supported_relations"])
        self.assertTrue(final["unknown_relations"])
        self.assertTrue(final["unsupported_relations"])
        self.assertTrue(fixture["scope"]["limitations"])
        self.assertEqual(preview["mode"], "incremental-preview")
        self.assertFalse(preview["eligible_as_final_evidence"])
        self.assertNotEqual(preview["input_fingerprint"], fixture["current_input_fingerprint"])

    def test_generic_plan_has_no_project_specific_source_or_business_definition(self):
        root = SCRIPTS.parent
        text = "\n".join(
            (root / "planning" / name).read_text(encoding="utf-8")
            for name in (
                "engineering-workflow-report-spec.md",
                "engineering-workflow-report-plan.md",
            )
        )
        for forbidden in ("PostgreSQL", ".review", "192.168.", "extract-contract-ast"):
            self.assertNotIn(forbidden, text)

    def write_manifest(self, root):
        (root / "engineering-manifest.json").write_text(json.dumps({
            "schema_version": 1,
            "workflow": {"active_task": "TASK-01"},
            "tasks": [{"id": "TASK-01"}],
        }), encoding="utf-8")

    def test_rejects_a_nonexistent_or_non_json_manifest_pointer(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs/tasks").mkdir(parents=True)
            (root / "docs/tasks/README.md").write_text("task index", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(SCRIPTS / "install_agents_guidance.py"),
                 "--root", tmp, "--manifest", "docs/tasks/README.md"],
                capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertFalse((root / "AGENTS.md").exists())

    def test_guidance_can_be_installed_before_manifest_without_claiming_complete_adoption(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            result = subprocess.run([sys.executable, str(SCRIPTS / "install_agents_guidance.py"), "--root", tmp], capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertFalse((root / "engineering-manifest.json").exists())
            self.assertIn("guidance_only_incomplete", result.stdout)

    def test_creates_and_updates_only_managed_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            path = root / "AGENTS.md"
            path.write_text("# Existing rules\n\nKeep this text.\n", encoding="utf-8")
            content = guidance.block("manifest.json", "planning", "engineering-workflow")
            self.assertTrue(guidance.update(path, content))
            first = path.read_text(encoding="utf-8")
            self.assertIn("Keep this text.", first)
            self.assertEqual(first.count(guidance.START), 1)
            self.assertFalse(guidance.update(path, content))
            path.write_text(first.replace("planning", "planning/workflow", 1), encoding="utf-8")
            self.assertTrue(guidance.update(path, content))
            updated = path.read_text(encoding="utf-8")
            self.assertEqual(updated.count(guidance.START), 1)
            self.assertIn("`planning` 或项目已有权威状态文件", updated)

    def test_cli_can_update_multiple_agent_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            self.write_manifest(root)
            command = [
                sys.executable,
                str(SCRIPTS / "install_agents_guidance.py"),
                "--root",
                str(root),
                "--file",
                "CLAUDE.md",
                "--file",
                ".github/copilot-instructions.md",
            ]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertTrue((root / "AGENTS.md").is_file())
            self.assertTrue((root / "CLAUDE.md").is_file())
            adapter = (root / ".github/copilot-instructions.md").read_text(encoding="utf-8")
            self.assertIn("(../AGENTS.md)", adapter)
            self.assertNotIn("engineering-manifest.json", adapter)
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(second.stdout, "")

    def test_rejects_path_escape(self):
        with tempfile.TemporaryDirectory() as tmp:
            result = subprocess.run(
                [
                    sys.executable,
                    str(SCRIPTS / "install_agents_guidance.py"),
                    "--root",
                    tmp,
                    "--file",
                    "../AGENTS.md",
                ],
                capture_output=True,
                text=True,
            )
            self.assertEqual(result.returncode, 2)
            self.assertFalse((Path(tmp) / "AGENTS.md").exists())

    def test_preserves_bytes_outside_block(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "AGENTS.md"
            before = b"\xef\xbb\xbf# Existing\r\n\r\n"
            after = b"\r\n\r\nKeep trailing spaces  \r\n"
            path.write_bytes(before + guidance.START.encode() + b"\r\nold\r\n" + guidance.END.encode() + after)
            guidance.update(path, guidance.block("manifest.json", "planning", "engineering-workflow"))
            self.assertTrue(path.read_bytes().startswith(before))
            self.assertTrue(path.read_bytes().endswith(after))

    def test_invalid_second_target_leaves_all_files_untouched(self):
        for invalid in (guidance.START, guidance.END + guidance.START, guidance.START * 2 + guidance.END, "## Engineering workflow\nmanual rules", "Example: `" + guidance.START + "` and `" + guidance.END + "` preserve me"):
            with self.subTest(invalid=invalid), tempfile.TemporaryDirectory() as tmp:
                root = Path(tmp)
                self.write_manifest(root)
                target = root / "CLAUDE.md"
                target.write_text(invalid, encoding="utf-8")
                result = guidance.main(["--root", tmp, "--file", "CLAUDE.md"])
                self.assertEqual(result, 2)
                self.assertEqual(target.read_text(encoding="utf-8"), invalid)
                self.assertFalse((root / "AGENTS.md").exists())

    def test_link_target_is_rejected(self):
        from unittest import mock
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            with mock.patch.object(guidance, "is_link", side_effect=lambda p: p == root / "AGENTS.md"):
                with self.assertRaises(ValueError):
                    guidance.safe_relative(root, "AGENTS.md")

    def test_windows_reparse_point_on_older_python_is_rejected(self):
        from types import SimpleNamespace
        from unittest import mock
        path = mock.Mock()
        path.is_symlink.return_value = False
        path.lstat.return_value = SimpleNamespace(st_file_attributes=0x400)
        self.assertTrue(guidance.is_link(path))
        path.lstat.return_value = SimpleNamespace(st_file_attributes=0)
        self.assertFalse(guidance.is_link(path))


if __name__ == "__main__":
    unittest.main()
