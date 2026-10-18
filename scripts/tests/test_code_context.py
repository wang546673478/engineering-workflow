"""Behavioral checks for the isolated collector's externally useful contract."""

import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import collect_code_context as collector


class ContextCollectorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="context-pilot-test-")
        self.base = Path(self.temp.name)
        self.root = self.base / "source"
        self.root.mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, data):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data if isinstance(data, bytes) else data.encode("utf-8"))
        return path

    def collect(self, **kwargs):
        return collector.collect(self.root, **kwargs)

    def entries(self, result):
        return {e["path"]: e for e in result["inventory"]["entries"]}

    def test_inventory_does_not_read_content_without_selection(self):
        self.write("src/app.ts", "const sentinel = 42;")
        self.write("test/app.test.ts", "test-content")
        result = self.collect()
        self.assertEqual(result["inventory"]["summary"]["files"], 2)
        self.assertEqual(result["inventory"]["summary"]["bytes_read"], 0)
        self.assertNotIn("sentinel", result["pack"])
        self.assertTrue(
            all(
                e["read_status"] == "not_selected"
                for e in self.entries(result).values()
                if e["kind"] == "file"
            )
        )

    def test_lock_build_and_rules_files_remain_available(self):
        names = [
            "package-lock.json",
            "Cargo.lock",
            "build.gradle",
            ".gitmodules",
            "AGENTS.md",
        ]
        for name in names:
            self.write(name, "source-content")
        result = self.collect(all_text=True)
        self.assertEqual(result["inventory"]["summary"]["included_files"], len(names))
        self.assertEqual(self.entries(result)["Cargo.lock"]["role"], "dependency_lock")

    def test_task_selection_keeps_source_lines_and_hash(self):
        self.write("src/app.ts", "first\nsecond\n")
        self.write("src/other.ts", "SHOULD_NOT_READ")
        result = self.collect(includes=["src/app.ts"], line_numbers=True)
        self.assertIn("     1 | first\n     2 | second\n", result["pack"])
        self.assertIn('FILE "src/app.ts"', result["pack"])
        self.assertNotIn("SHOULD_NOT_READ", result["pack"])
        self.assertEqual(len(self.entries(result)["src/app.ts"]["sha256"]), 64)

    def test_glob_double_star_selects_root_and_nested(self):
        self.write("root.ts", "root")
        self.write("deep/child.ts", "child")
        self.write("deep/no.txt", "no")
        self.assertEqual(
            self.collect(includes=["**/*.ts"])["inventory"]["summary"][
                "included_files"
            ],
            2,
        )

    def test_literal_spaces_unicode_and_commas_are_not_split(self):
        self.write("src/中文 file,a.ts", "正常内容")
        result = self.collect(includes=["src/中文 file,a.ts"])
        self.assertEqual(result["inventory"]["summary"]["included_files"], 1)
        self.assertIn("正常内容", result["pack"])

    def test_directory_prefix_selection(self):
        self.write("src/deep/a.ts", "a")
        self.write("test/b.ts", "b")
        result = self.collect(includes=["src/"])
        self.assertEqual(result["inventory"]["summary"]["included_files"], 1)

    def test_explicit_excluded_subtree_is_recorded(self):
        self.write("vendor/a.ts", "NEVER_READ")
        self.write("src/a.ts", "READ")
        result = self.collect(all_text=True, excludes=["vendor"])
        self.assertEqual(self.entries(result)["vendor"]["reason"], "explicit_exclusion")
        self.assertNotIn("NEVER_READ", result["pack"])

    def test_dependency_tree_is_pruned_with_a_reason(self):
        self.write("node_modules/library/file.ts", "NEVER_READ")
        result = self.collect(all_text=True)
        self.assertEqual(
            self.entries(result)["node_modules"]["reason"],
            "pruned_dependency_or_metadata",
        )
        self.assertNotIn("node_modules/library/file.ts", self.entries(result))

    def test_gitignore_negation_preserves_order(self):
        self.write(".gitignore", "*.log\n!important.log\n")
        self.write("important.log", "KEEP")
        self.write("other.log", "OMIT")
        result = self.collect(all_text=True)
        self.assertIn("KEEP", result["pack"])
        self.assertEqual(self.entries(result)["other.log"]["reason"], "gitignore")

    def test_nested_gitignore_applies_to_deeper_descendants(self):
        self.write("sub/.gitignore", "*.private\n")
        self.write("sub/deep/file.private", "OMIT")
        self.write("root.private", "KEEP")
        result = self.collect(all_text=True)
        self.assertEqual(
            self.entries(result)["sub/deep/file.private"]["reason"], "gitignore"
        )
        self.assertIn("KEEP", result["pack"])

    def test_root_anchored_gitignore_does_not_match_nested_name(self):
        self.write(".gitignore", "/root-only.txt\n")
        self.write("root-only.txt", "OMIT")
        self.write("deep/root-only.txt", "KEEP")
        result = self.collect(all_text=True)
        self.assertEqual(self.entries(result)["root-only.txt"]["reason"], "gitignore")
        self.assertEqual(
            self.entries(result)["deep/root-only.txt"]["read_status"], "included"
        )

    def test_gitignore_failure_never_silently_exports_uncertain_files(self):
        self.write(".gitignore", "private.txt\n")
        self.write("private.txt", "SENTINEL")
        with patch.object(
            collector, "git_ignored", side_effect=RuntimeError("unavailable")
        ):
            result = self.collect(all_text=True)
        self.assertFalse(result["inventory"]["scan_complete_for_policy"])
        self.assertNotIn("SENTINEL", result["pack"])
        self.assertEqual(
            self.entries(result)["private.txt"]["reason"], "gitignore_unverified"
        )

    def test_sensitive_filename_is_omitted_even_when_explicitly_selected(self):
        self.write(".env.production", "SYNTHETIC_SECRET")
        self.write("id_rsa", "SYNTHETIC_KEY")
        result = self.collect(includes=[".env.production", "id_rsa"])
        self.assertEqual(result["inventory"]["summary"]["included_files"], 0)
        self.assertEqual(len(result["inventory"]["summary"]["selected_omissions"]), 2)
        self.assertNotIn("SYNTHETIC", result["pack"])

    def test_multibyte_utf8_at_1024_boundary_is_not_binary(self):
        self.write("text.txt", "a" * 1023 + "汉字")
        result = self.collect(includes=["text.txt"])
        self.assertIn("汉字", result["pack"])
        self.assertEqual(self.entries(result)["text.txt"]["read_status"], "included")

    def test_utf16_and_utf32_bom_are_decoded(self):
        self.write("utf16.txt", "中文".encode("utf-16"))
        self.write("utf32.txt", "文字".encode("utf-32"))
        result = self.collect(all_text=True)
        self.assertIn("中文", result["pack"])
        self.assertIn("文字", result["pack"])

    def test_binary_and_empty_files_have_distinct_status(self):
        self.write("empty.txt", "")
        self.write("blob.dat", b"\x00\xff")
        result = self.collect(all_text=True)
        self.assertEqual(self.entries(result)["empty.txt"]["read_status"], "included")
        self.assertEqual(self.entries(result)["blob.dat"]["read_status"], "binary")

    def test_direct_file_selection_obeys_file_limit(self):
        self.write("large.ts", "x" * 30)
        result = self.collect(includes=["large.ts"], max_file_bytes=10)
        self.assertEqual(self.entries(result)["large.ts"]["reason"], "file_byte_limit")
        self.assertEqual(result["inventory"]["summary"]["bytes_read"], 0)

    def test_total_budget_records_selected_omissions(self):
        self.write("a.ts", "12345")
        self.write("b.ts", "67890")
        result = self.collect(all_text=True, max_total_bytes=7)
        self.assertEqual(result["inventory"]["summary"]["bytes_read"], 5)
        self.assertEqual(self.entries(result)["b.ts"]["reason"], "total_byte_limit")

    def test_file_count_budget(self):
        self.write("a.ts", "a")
        self.write("b.ts", "b")
        result = self.collect(all_text=True, max_files=1)
        self.assertEqual(result["inventory"]["summary"]["included_files"], 1)
        self.assertEqual(self.entries(result)["b.ts"]["reason"], "file_count_limit")

    def test_depth_limit_does_not_claim_complete_scope(self):
        self.write("deep/child/a.ts", "a")
        result = self.collect(all_text=True, max_depth=1)
        self.assertFalse(result["inventory"]["scan_complete_for_policy"])
        self.assertEqual(self.entries(result)["deep/child"]["reason"], "depth_limit")

    def test_inventory_entry_limit_is_explicit(self):
        for name in ["a.ts", "b.ts", "c.ts"]:
            self.write(name, "x")
        result = self.collect(max_entries=1)
        self.assertEqual(len(result["inventory"]["entries"]), 1)
        self.assertEqual(result["inventory"]["issues"][0]["reason"], "entry_limit")

    def test_read_failure_is_recorded_and_not_exported(self):
        # The collector canonicalizes roots; Windows temp paths can be 8.3 aliases.
        target = self.write("blocked.ts", "SHOULD_NOT_EXPORT").resolve()
        original = Path.open

        def opened(path, *args, **kwargs):
            if path == target and args and args[0] == "rb":
                raise PermissionError("synthetic")
            return original(path, *args, **kwargs)

        with patch.object(Path, "open", new=opened):
            result = self.collect(all_text=True)
        self.assertEqual(
            self.entries(result)["blocked.ts"]["read_status"], "unreadable"
        )
        self.assertNotIn("SHOULD_NOT_EXPORT", result["pack"])

    def test_file_growing_after_inventory_cannot_exceed_read_budget(self):
        target = self.write("growing.ts", "old")
        original = collector.scan

        def scanned(*args, **kwargs):
            result = original(*args, **kwargs)
            target.write_text("new-content-is-larger", encoding="utf-8")
            return result

        with patch.object(collector, "scan", new=scanned):
            result = self.collect(all_text=True, max_total_bytes=5)
        self.assertLessEqual(result["inventory"]["summary"]["bytes_read"], 5)
        self.assertEqual(
            self.entries(result)["growing.ts"]["reason"], "source_changed_during_read"
        )
        self.assertEqual(result["inventory"]["summary"]["included_files"], 0)

    def test_junction_outside_source_is_not_followed(self):
        outside = self.base / "outside"
        outside.mkdir()
        (outside / "secret.txt").write_text("OUTSIDE_SENTINEL")
        junction = self.root / "linked"
        if os.name == "nt":

            def quote(p):
                return "'" + str(p).replace("'", "''") + "'"

            result = subprocess.run(
                [
                    "powershell",
                    "-NoProfile",
                    "-Command",
                    "New-Item -ItemType Junction -Path "
                    + quote(junction)
                    + " -Target "
                    + quote(outside)
                    + " | Out-Null",
                ],
                capture_output=True,
            )
            self.assertEqual(result.returncode, 0)
        else:
            junction.symlink_to(outside, target_is_directory=True)
        result = self.collect(all_text=True)
        self.assertEqual(self.entries(result)["linked"]["reason"], "link_or_junction")
        self.assertNotIn("OUTSIDE_SENTINEL", result["pack"])

    def test_reparse_directory_without_junction_api_is_not_followed(self):
        self.write("linked/secret.txt", "DO_NOT_FOLLOW")
        target = (self.root / "linked").resolve()
        original = Path.lstat

        def lstat(path, *args, **kwargs):
            if path == target:
                return SimpleNamespace(st_file_attributes=0x400)
            return original(path, *args, **kwargs)

        with patch.object(collector.guard, "is_link", return_value=False), patch.object(
            Path, "lstat", new=lstat
        ):
            result = self.collect(all_text=True)
        self.assertEqual(self.entries(result)["linked"]["reason"], "link_or_junction")
        self.assertNotIn("linked/secret.txt", self.entries(result))
        self.assertNotIn("DO_NOT_FOLLOW", result["pack"])

    def test_reparse_source_root_without_junction_api_is_rejected(self):
        original = Path.lstat

        def lstat(path, *args, **kwargs):
            if path == self.root:
                return SimpleNamespace(st_file_attributes=0x400)
            return original(path, *args, **kwargs)

        with patch.object(collector.guard, "is_link", return_value=False), patch.object(
            Path, "lstat", new=lstat
        ):
            with self.assertRaises(collector.guard.ConfigError):
                self.collect()

    def test_notebook_conversion_is_not_part_of_fusion(self):
        self.write("demo.ipynb", json.dumps({"cells": [{"source": "print(42)"}]}))
        result = self.collect(all_text=True)
        self.assertEqual(
            self.entries(result)["demo.ipynb"]["read_status"], "unsupported"
        )
        self.assertEqual(
            self.entries(result)["demo.ipynb"]["reason"],
            "notebook_conversion_not_enabled",
        )
        self.assertNotIn("print(42)", result["pack"])

    def test_compact_pack_preserves_full_text_and_source_range(self):
        text = "line one\n中文 line two\n\nline four"
        self.write("app.ts", text)
        result = self.collect(includes=["app.ts"])
        self.assertEqual(result["files"][0]["text"], text)
        self.assertIn('FILE "app.ts" L1-4\n' + text, result["pack"])
        self.assertNotIn("     1 |", result["pack"])
        self.assertNotIn("token_count", result["inventory"])

    def test_output_must_be_new_and_outside_source(self):
        result = self.collect()
        with self.assertRaises(ValueError):
            collector.write_result(result, self.root / "output")
        self.assertFalse((self.root / "output").exists())
        output = self.base / "output"
        collector.write_result(result, output)
        with self.assertRaises(FileExistsError):
            collector.write_result(result, output)

    def test_invalid_limits_and_path_patterns_fail_before_read(self):
        for options in [
            {"max_file_bytes": -1},
            {"includes": ["../outside"]},
            {"includes": ["C:/outside"]},
        ]:
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.collect(**options)

    def test_cli_produces_parseable_inventory_and_reading_pack(self):
        self.write("app.ts", "const value = 42;")
        output = self.base / "cli-output"
        proc = subprocess.run(
            [
                sys.executable,
                str(Path(collector.__file__)),
                "--root",
                str(self.root),
                "--include",
                "app.ts",
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        inventory = json.loads((output / "inventory.json").read_text(encoding="utf-8"))
        self.assertEqual(inventory["summary"]["included_files"], 1)
        self.assertIn(
            "const value = 42;",
            (output / "reading-pack.txt").read_text(encoding="utf-8"),
        )


if __name__ == "__main__":
    unittest.main()
