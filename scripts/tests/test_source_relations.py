import copy, json
from pathlib import Path
import subprocess, sys, tempfile, unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import collect_code_context as collector
import source_relations as relations


class RelationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temporary = tempfile.TemporaryDirectory(prefix="fusion-reference-")
        cls.addClassCleanup(cls.temporary.cleanup)
        cls.base = Path(cls.temporary.name)
        cls.root = cls.base / "source"
        cls.root.mkdir()
        files = {
            "tsconfig.json": json.dumps(
                {
                    "compilerOptions": {
                        "moduleResolution": "Bundler",
                        "module": "ESNext",
                        "baseUrl": ".",
                        "paths": {
                            "@alias/*": ["src/*"],
                            "@work/core": ["packages/core/src/index.ts"],
                        },
                    }
                }
            ),
            "package.json": json.dumps({"name": "fixture", "type": "module"}),
            "packages/core/package.json": json.dumps(
                {"name": "@work/core", "exports": {".": "./src/index.ts"}}
            ),
            "packages/core/src/index.ts": "export const core = 42;",
            "src/local.ts": "export const local = 1; export type Kind = string;",
            "src/fake.ts": "export const fake = 0;",
            "src/main.ts": "\n".join(
                [
                    '// import { fake } from "./fake";',
                    'const example = `import { fake } from "./fake";`;',
                    'import { local } from "./local";',
                    'import type { Kind } from "./local";',
                    'import { local as aliased } from "@alias/local";',
                    'import { core } from "@work/core";',
                    'export { local } from "./local";',
                    'const later = import("./local");',
                    'const name = "./local"; import(name);',
                    'type Local = import("./local").Kind;',
                    'const loaded = require("./local");',
                    'import { missing } from "./missing";',
                    'import { readFile } from "node:fs";',
                    'import { external } from "outside-package";',
                ]
            )
            + "\n",
            "src/outside.ts": 'import { secret } from "../../outside";\n',
            "README.md": "fixture",
        }
        for name, text in files.items():
            p = cls.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        cls.result = collector.collect(
            cls.root, includes=["src/main.ts", "src/outside.ts"]
        )
        cls.output = cls.base / "output"
        collector.write_result(cls.result, cls.output)
        cls.status = relations.build_relation_outputs(
            cls.result, cls.output, views="all"
        )
        cls.analysis = json.loads((cls.output / "references.json").read_text())
        cls.graph = json.loads((cls.output / "graph.json").read_text())
        if not cls.analysis["files"]:
            raise RuntimeError("Required JS/TS regression environment is unavailable.\n" + relations.diagnostic_text(cls.status["diagnostics"]))
        cls.sources = {
            e["path"]: {"sha256": None, "text": "", "observed_references": []}
            for e in cls.result["inventory"]["entries"]
            if e["kind"] == "file"
        }
        for f in cls.result["files"]:
            cls.sources[f["path"]].update(sha256=f["source_sha256"], text=f["text"])
        for ref in cls.analysis["references"]:
            if ref["status"] == "resolved":
                cls.sources[ref["from"]]["observed_references"].append(ref)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def test_fixture_exact_local_reference_truth(self):
        expected = {
            (3, "src/local.ts", "import", False),
            (4, "src/local.ts", "import", True),
            (5, "src/local.ts", "import", False),
            (6, "packages/core/src/index.ts", "import", False),
            (7, "src/local.ts", "reexport", False),
            (8, "src/local.ts", "dynamic_import_literal", False),
            (10, "src/local.ts", "import_type", True),
            (11, "src/local.ts", "require_literal_syntax", False),
        }
        actual = {
            (r["evidence"]["line"], r["to"], r["kind"], r["type_only"])
            for r in self.analysis["references"]
            if r["status"] == "resolved"
        }
        self.assertEqual(actual, expected)

    def test_comment_and_string_imports_do_not_become_edges(self):
        self.assertFalse(
            any(r["to"] == "src/fake.ts" for r in self.analysis["references"])
        )

    def test_dynamic_variable_is_unknown(self):
        self.assertTrue(
            any(
                r["line"] == 9 and r["status"] == "dynamic_specifier_unknown"
                for r in self.analysis["unknown"]
            )
        )

    def test_unresolved_and_external_are_explicit(self):
        statuses = {r["specifier"]: r["status"] for r in self.analysis["references"]}
        self.assertEqual(statuses["./missing"], "local_unresolved")
        self.assertEqual(statuses["outside-package"], "external_or_unresolved")
        self.assertEqual(statuses["node:fs"], "builtin")

    def test_root_escape_never_resolves_outside_inventory(self):
        refs = [r for r in self.analysis["references"] if r["from"] == "src/outside.ts"]
        self.assertEqual(refs[0]["status"], "local_unresolved")

    def test_evidence_has_real_line_and_source_hash(self):
        ref = next(
            r for r in self.analysis["references"] if r["specifier"] == "@work/core"
        )
        self.assertEqual(ref["evidence"]["line"], 6)
        self.assertEqual(
            ref["evidence"]["sha256"], self.sources["src/main.ts"]["sha256"]
        )

    def test_generated_graph_is_valid_and_deterministic(self):
        self.assertTrue(relations.validate_graph(self.graph, self.sources)["valid"])
        again = relations.graph_from_references(self.analysis, self.sources)
        self.assertEqual(
            relations.compile_mermaid(self.graph), relations.compile_mermaid(again)
        )

    def test_direction_cannot_be_reversed_with_same_evidence(self):
        graph = copy.deepcopy(self.graph)
        edge = graph["edges"][0]
        edge["from"], edge["to"] = edge["to"], edge["from"]
        self.assertFalse(relations.validate_graph(graph, self.sources)["valid"])

    def test_unsupported_business_label_is_rejected(self):
        graph = copy.deepcopy(self.graph)
        graph["edges"][0]["relation"] = "charges customer"
        self.assertIn(
            "unsupported_semantic_claim",
            relations.validate_graph(graph, self.sources)["issues"],
        )

    def test_bad_hash_bad_line_duplicate_id_rejected(self):
        for mutation in ["hash", "line", "id"]:
            graph = copy.deepcopy(self.graph)
            if mutation == "hash":
                graph["edges"][0]["evidence"]["sha256"] = "0" * 64
            elif mutation == "line":
                graph["edges"][0]["evidence"]["line"] = 999999
            else:
                graph["nodes"].append(graph["nodes"][0])
            with self.subTest(mutation=mutation):
                self.assertFalse(relations.validate_graph(graph, self.sources)["valid"])

    def test_types_are_visually_distinct_and_sources_are_clickable_in_table(self):
        self.assertIn("type import", relations.compile_mermaid(self.graph))
        self.assertIn(
            "src/main.ts:6", relations.relation_markdown(self.graph, self.root)
        )
        self.assertIn("semantics_unreviewed", self.graph["edges"][0]["status"])

    def test_compiler_escapes_source_labels(self):
        graph = copy.deepcopy(self.graph)
        graph["nodes"][0]["label"] = '"<script>#`[x]|'
        output = relations.compile_mermaid(graph)
        self.assertNotIn("<script>", output)
        self.assertIn("&lt;script&gt;", output)

    def test_cli_integrates_collection_and_reference_views(self):
        output = self.base / "cli"
        proc = subprocess.run(
            [
                sys.executable,
                str(Path(collector.__file__)),
                "--root",
                str(self.root),
                "--include",
                "src/main.ts",
                "--relations",
                "--views",
                "all",
                "--output",
                str(output),
            ],
            capture_output=True,
            text=True,
            encoding="utf-8",
        )
        self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
        self.assertTrue((output / "references.mmd").exists())
        self.assertTrue((output / "reading-pack.txt").exists())
        self.assertNotIn(
            "token_count", json.loads((output / "inventory.json").read_text())
        )

    def test_package_summary_keeps_all_underlying_evidence(self):
        package_graph = relations.package_graph(
            self.graph, ["packages/core/package.json"]
        )
        self.assertEqual(
            package_graph["nodes"], []
        )  # Caller is outside package: no guessed package edge.

    def test_missing_optional_node_does_not_break_collector_outputs(self):
        output = self.base / "without-node"
        collector.write_result(self.result, output)
        with patch.object(relations.shutil, "which", return_value=None):
            status = relations.build_relation_outputs(self.result, output)
        self.assertEqual(status["status"], "unsupported")
        self.assertTrue((output / "reading-pack.txt").exists())

    def test_partial_language_support_keeps_valid_javascript_edges(self):
        output = self.base / "partial-language"
        result = copy.deepcopy(self.result)
        rust = {"references": [], "unknown": [], "unsupported": [{"path": "src/lib.rs", "status": "rust_parser_unavailable"}], "files": [], "configuration": []}
        result["files"].append({"path": "src/lib.rs", "text": "mod local;", "source_sha256": "fixture"})
        with patch("rust_references.analyze_rust", return_value=rust):
            analysis = relations.analyze_result(result)
        collector.write_result(self.result, output)
        status = relations.build_relation_outputs(self.result, output, analysis=analysis)
        self.assertGreater(status["summary"]["resolved"], 0)
        self.assertEqual(status["unsupported"], rust["unsupported"])
        self.assertEqual(status["diagnostics"][0]["status"], "rust_parser_unavailable")
        self.assertIn("coverage is incomplete", (output / "relations-summary.txt").read_text())
        self.assertTrue(json.loads((output / "graph.json").read_text())["edges"])


if __name__ == "__main__":
    unittest.main()
