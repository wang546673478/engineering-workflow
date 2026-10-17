import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import collect_code_context as collector
import source_relations as relations


class RustReferencesTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix="rust-context-")
        cls.root = Path(cls.temp.name) / "source"
        cls.root.mkdir()
        files = {
            "Cargo.toml": '[workspace]\nmembers=["app","dep"]\n[workspace.dependencies]\nrenamed={path="dep",package="actual-dep"}\n',
            "app/Cargo.toml": '[package]\nname="app"\nversion="0.1.0"\n[dependencies]\nrenamed={workspace=true}\n',
            "dep/Cargo.toml": '[package]\nname="actual-dep"\nversion="0.1.0"\n',
            "dep/src/lib.rs": "pub mod item;\n",
            "dep/src/item.rs": "pub struct Thing;\n",
            "app/src/local.rs": "pub struct Thing; pub mod nested;\n",
            "app/src/local/nested.rs": "pub struct Other;\n",
            "app/src/alternate.rs": "pub struct Alternate;\n",
            "app/src/lib.rs": "\n".join(
                [
                    "// use crate::fake::False;",
                    'const EXAMPLE: &str = "use crate::fake::False;";',
                    "mod local;",
                    "use crate::local::{Thing, nested::Other};",
                    "use renamed::item::Thing as DepThing;",
                    '#[cfg(target_os="linux")]',
                    "use crate::local::Thing as Conditional;",
                    '#[path="alternate.rs"]',
                    "mod custom;",
                    "use external_package::Whatever;",
                ]
            )
            + "\n",
            "app/src/fake.rs": "pub struct False;\n",
        }
        for name, text in files.items():
            p = cls.root / name
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(text, encoding="utf-8")
        cls.result = collector.collect(cls.root, includes=["app/src/lib.rs"])
        cls.analysis = relations.analyze_result(cls.result)

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def test_expected_module_endpoints(self):
        refs = {
            (r["evidence"]["line"], r["to"])
            for r in self.analysis["references"]
            if r["status"] == "resolved"
        }
        self.assertEqual(
            refs,
            {
                (3, "app/src/local.rs"),
                (4, "app/src/local.rs"),
                (4, "app/src/local/nested.rs"),
                (5, "dep/src/item.rs"),
                (7, "app/src/local.rs"),
                (9, "app/src/alternate.rs"),
            },
        )

    def test_comments_strings_not_edges(self):
        self.assertFalse(
            any(r["to"] == "app/src/fake.rs" for r in self.analysis["references"])
        )

    def test_conditional_import_not_made_unconditional(self):
        ref = next(r for r in self.analysis["references"] if r["evidence"]["line"] == 7)
        self.assertTrue(ref["conditions"])
        self.assertIn("cfg", ref["conditions"][0])

    def test_external_references_remain_unresolved(self):
        ref = next(
            r
            for r in self.analysis["references"]
            if r["specifier"].startswith("external_package")
        )
        self.assertEqual(ref["status"], "rust_unresolved_or_external")

    def test_rust_graph_and_explicit_views(self):
        output = Path(self.temp.name) / "output"
        collector.write_result(self.result, output)
        status = relations.build_relation_outputs(
            self.result, output, views="all", analysis=self.analysis
        )
        self.assertTrue(status["validation"]["valid"])
        self.assertTrue((output / "references.mmd").exists())
        self.assertTrue((output / "relations.md").exists())
        graph = json.loads((output / "graph.json").read_text())
        self.assertTrue(any(edge["conditions"] for edge in graph["edges"]))
        self.assertIn("conditional rust_use", (output / "references.mmd").read_text())

    def test_summary_view_avoids_unrequested_table_and_diagram(self):
        output = Path(self.temp.name) / "summary"
        collector.write_result(self.result, output)
        relations.build_relation_outputs(self.result, output, analysis=self.analysis)
        self.assertTrue((output / "graph.json").exists())
        self.assertFalse((output / "relations.md").exists())
        self.assertFalse((output / "references.mmd").exists())

    def test_same_run_inventory_reuse_matches_fresh_collection(self):
        discovery = collector.collect(self.root)
        reused = collector.collect(
            self.root, includes=["app/src/lib.rs"], discovery=discovery
        )
        self.assertEqual(reused["pack"], self.result["pack"])
        self.assertEqual(
            reused["inventory"]["summary"]["file_bytes"],
            self.result["inventory"]["summary"]["file_bytes"],
        )

    def test_inventory_reuse_rejects_different_scan_scope(self):
        discovery = collector.collect(self.root)
        with self.assertRaises(ValueError):
            collector.collect(self.root, discovery=discovery, excludes=["app"])

    def test_multiline_crlf_rust_statement_keeps_valid_evidence(self):
        text = "use crate::local::{\r\n    Thing,\r\n};\r\n"
        digest = hashlib.sha256(text.encode()).hexdigest()
        evidence = {"path": "lib.rs", "line": 1, "end_line": 3,
                    "sha256": digest, "statement": text.rstrip("\r\n"),
                    "specifier": "crate::local::Thing"}
        record = {"to": "local.rs", "kind": "rust_use", "type_only": False,
                  "specifier": evidence["specifier"], "evidence": evidence}
        graph = {"nodes": [{"id": "a", "path": "lib.rs"}, {"id": "b", "path": "local.rs"}],
                 "edges": [{"from": "a", "to": "b", "target_path": "local.rs",
                            "relation": "rust_use", "type_only": False, "evidence": evidence}]}
        sources = {"lib.rs": {"sha256": digest, "text": text, "observed_references": [record]},
                   "local.rs": {"sha256": None, "text": ""}}
        self.assertTrue(relations.validate_graph(graph, sources)["valid"])


if __name__ == "__main__":
    unittest.main()
