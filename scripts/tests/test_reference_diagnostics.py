import builtins
import contextlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import collect_code_context as collector
import source_relations as relations


class ReferenceDiagnosticsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="reference-diagnostics-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / "source"
        (self.root / "src").mkdir(parents=True)
        for path, text in {
            "Cargo.toml": '[package]\nname="fixture"\nversion="0.1.0"\n',
            "src/lib.rs": "mod local;\n",
            "src/local.rs": "pub struct Thing;\n",
            "src/main.ts": 'import {x} from "./local";\n',
            "src/local.ts": "export const x=1;\n",
        }.items():
            (self.root / path).write_text(text, encoding="utf-8")

    @staticmethod
    def without_rust(name, *args, **kwargs):
        if name in {"tree_sitter", "tree_sitter_rust"}:
            raise ImportError("missing Rust parser fixture")
        return ReferenceDiagnosticsTests.original_import(name, *args, **kwargs)

    original_import = staticmethod(builtins.__import__)

    def test_missing_rust_is_actionable_in_cli_and_saved_summary(self):
        output = Path(self.temp.name) / "rust-output"
        stdout = io.StringIO()
        with patch("builtins.__import__", side_effect=self.without_rust), contextlib.redirect_stdout(stdout):
            code = collector.main(["--root", str(self.root), "--include", "src/lib.rs", "--relations", "--output", str(output)])
        status = json.loads(stdout.getvalue())["relations"]
        self.assertEqual(code, 0)  # Collection is usable independently of references.
        self.assertEqual(status["status"], "unsupported")
        self.assertEqual(status["unsupported"], [{"path": "src/lib.rs", "status": "rust_parser_unavailable"}])
        command = status["diagnostics"][0]["setup_commands"][0]
        self.assertEqual(command[:5], [sys.executable, "-m", "pip", "install", "-r"])
        self.assertEqual(Path(command[-1]).name, "reference-requirements.txt")
        self.assertEqual(status, json.loads((output / "relations-status.json").read_text()))
        self.assertIn("rust_parser_unavailable", (output / "relations-summary.txt").read_text())
        self.assertTrue((output / "reading-pack.txt").exists())

    def test_missing_node_has_runtime_and_script_disabled_setup_guidance(self):
        result = collector.collect(self.root, includes=["src/main.ts"])
        with patch.object(relations.shutil, "which", return_value=None):
            analysis = relations.analyze_result(result)
        diagnostics = relations.dependency_diagnostics(analysis)
        self.assertEqual(diagnostics[0]["status"], "node_runtime_missing")
        self.assertEqual(diagnostics[0]["setup_commands"][0][:4], ["npm", "ci", "--ignore-scripts", "--prefix"])

    def test_missing_typescript_does_not_execute_the_analyzer(self):
        result = collector.collect(self.root, includes=["src/main.ts"])
        original = Path.is_file
        parser = Path(relations.__file__).with_name("context-runtime") / "node_modules/typescript/lib/typescript.js"
        with patch.object(relations.shutil, "which", return_value="node"), patch.object(Path, "is_file", autospec=True, side_effect=lambda p: False if p == parser else original(p)), patch.object(relations.subprocess, "run") as run:
            analysis = relations.analyze_result(result)
        run.assert_not_called()
        diagnostic = relations.dependency_diagnostics(analysis)[0]
        self.assertEqual(diagnostic["status"], "js_parser_unavailable")
        self.assertEqual(Path(diagnostic["setup_commands"][0][-1]).name, "context-runtime")

    def test_analyzer_execution_failure_is_not_reported_as_a_missing_parser(self):
        result = collector.collect(self.root, includes=["src/main.ts"])
        original = Path.is_file
        parser = Path(relations.__file__).with_name("context-runtime") / "node_modules/typescript/lib/typescript.js"
        for response in (subprocess.CompletedProcess([], 1, "", "runtime failure"), subprocess.CompletedProcess([], 0, "invalid JSON", "")):
            with self.subTest(returncode=response.returncode), patch.object(relations.shutil, "which", return_value="node"), patch.object(Path, "is_file", autospec=True, side_effect=lambda p: True if p == parser else original(p)), patch.object(relations.subprocess, "run", return_value=response):
                analysis = relations.analyze_result(result)
            diagnostic = relations.dependency_diagnostics(analysis)[0]
            self.assertEqual(diagnostic["status"], "js_analysis_failed")
            self.assertEqual(diagnostic["setup_commands"], [])


if __name__ == "__main__":
    unittest.main()
