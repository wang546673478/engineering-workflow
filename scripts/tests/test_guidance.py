import importlib.util
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
