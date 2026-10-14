import copy
from contextlib import closing
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SCRIPTS))
def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / (name + ".py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
checker = load("check_project")
extractor = load("extract_sqlite")
database_extractor = load("extract_database")

class CheckerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        for path, content in {"docs/spec.md":"REQ-1 AT-1", "docs/module.md":"module", "docs/impact.md":"impact", "docs/baseline.md":"reviewed", "docs/approval.md":"approved", "src/app.py":"print('app')", "data.sql":"CREATE TABLE accounts(id integer);", "docs/db.md":"accounts id value"}.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        with closing(sqlite3.connect(self.root / "data.sqlite")) as con:
            con.execute("CREATE TABLE accounts(id INTEGER,value TEXT)")
            con.commit()
        self.source = {"kind":"database","provenance":{"type":"sqlite-metadata","scope":"main metadata","complete":True,"evidence":"fixture snapshot","source_files":[{"path":"data.sqlite","sha256":checker.file_hash(self.root/"data.sqlite")}]}, "items":[{"id":"accounts","fields":["id","value"]}]}
        self.mapping = {"kind":"database","items":[{"id":"accounts","document":"docs/db.md","fields":["id","value"]}]}
        self.manifest = {"schema_version":1,"documents":[{"id":i,"path":p,"kind":"spec" if i=="spec" else "other","required":True} for i,p in [("spec","docs/spec.md"),("module","docs/module.md"),("impact","docs/impact.md")]],"requirements":[{"id":"REQ-1","document":"spec"}],"acceptance":[{"id":"AT-1","document":"spec"}],"modules":[{"id":"core","source_paths":["src"],"document":"module","depends_on":[],"allowed_dependencies":[]}],"inventories":[{"id":"db","kind":"database","path":"inventory.json","documentation":"mapping.json","required":True}],"checks":[{"id":"unit","command":[sys.executable,"-c","print('ok')"],"required":True,"timeout_seconds":5}],"tasks":[{"id":"TASK-1","requirement_ids":["REQ-1"],"acceptance_ids":["AT-1"],"module_ids":["core"],"depends_on":[],"status":"complete","impact_document":"impact","required_checks":["unit"],"approval_required":True,"approval":{"status":"approved","evidence":"docs/approval.md"},"skill_review":{"catalog_source":"test fixture","scope":"test task","checked_at":"2026-10-13T00:00:00+08:00","candidates":[],"recheck":"none"}}],"baseline":{"status":"complete","evidence":"docs/baseline.md"},"exclude_paths":["manifest.json","inventory.json","mapping.json","data.sql","docs/spec.md","docs/baseline.md","docs/approval.md","docs/db.md"]}
        self.write()
        if shutil.which("git"):
            self.git("init")
            self.git("add", ".")
            self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "baseline")
    def git(self, *args):
        proc=subprocess.run(["git","-c","safe.directory="+str(self.root)]+list(args),cwd=self.root,capture_output=True)
        self.assertEqual(proc.returncode,0,proc.stderr)
    def tearDown(self):
        self.tmp.cleanup()
    def write(self):
        for name, data in (("manifest.json",self.manifest),("inventory.json",self.source),("mapping.json",self.mapping)):
            (self.root/name).write_text(json.dumps(data),encoding="utf-8")
    def cli(self,*extra):
        self.write()
        extra=list(extra)
        if "handoff" in extra and "--base" not in extra:
            extra.extend(["--base", "HEAD"])
        command=[sys.executable,str(SCRIPTS/"check_project.py"),"--root",str(self.root),"--manifest","manifest.json"]+list(extra)
        proc=subprocess.run(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True)
        return proc,json.loads(proc.stdout)
    def test_handoff_actual_success(self):
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,0, result)
        self.assertTrue(result["required_checks_satisfied"])
        self.assertNotIn("ok", json.dumps(result))
    def test_manifest_active_task_is_used_when_cli_task_is_omitted(self):
        self.manifest["workflow"] = {"active_task": "TASK-1"}
        proc,result=self.cli("--mode","handoff","--run-checks")
        self.assertEqual(proc.returncode,0, result)
        self.assertTrue(result["required_checks_satisfied"])

    def test_unknown_manifest_active_task_blocks_baseline(self):
        self.manifest["workflow"] = {"active_task": "TASK-MISSING"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("workflow.active_task", json.dumps(result))
    def test_check_runs_from_declared_working_directory(self):
        self.manifest["checks"][0]["working_directory"] = "src"
        self.manifest["checks"][0]["command"] = [
            sys.executable, "-c", "from pathlib import Path; Path('cwd-marker').write_text('ok')"
        ]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0, result)
        self.assertEqual((self.root / "src/cwd-marker").read_text(), "ok")
        check = next(item for item in result["checks"] if item["rule_id"] == "unit")
        self.assertEqual(check["evidence"]["working_directory"], "src")
    def test_check_working_directory_must_stay_in_project(self):
        self.manifest["checks"][0]["working_directory"] = "../outside"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,2)
        self.assertFalse(result["required_checks_satisfied"])
        self.assertIn("path escapes project root", json.dumps(result))
    def test_check_working_directory_rejects_link(self):
        link = self.root / "work-link"
        link.mkdir()
        self.manifest["checks"][0]["working_directory"] = "work-link"
        self.write()
        with mock.patch.object(Path, "is_symlink", autospec=True, side_effect=lambda path: path == link):
            with self.assertRaises(checker.ConfigError):
                checker.validate(self.root, self.manifest, "baseline", None)
    def test_skipped_required_command_blocks(self):
        proc,result=self.cli("--mode","handoff","--task","TASK-1")
        self.assertEqual(proc.returncode,1)
        self.assertFalse(result["required_checks_satisfied"])
        self.assertIn("skipped",[x["status"] for x in result["checks"]])
    def test_actual_failure_and_secret_output_not_exposed(self):
        self.manifest["checks"][0]["command"]=[sys.executable,"-c","print('secret-value');raise SystemExit(3)"]
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertNotIn("secret-value",json.dumps(result))
    def test_test_skip_summary_is_partial(self):
        self.manifest["checks"][0]["command"]=[sys.executable,"-c","print('OK (skipped=1)')"]
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("partial",[x["status"] for x in result["checks"]])
    def test_invalid_reference(self):
        self.manifest["tasks"][0]["module_ids"]=["ghost"]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertFalse(result["required_checks_satisfied"])
    def test_requirement_id_must_appear(self):
        (self.root/"docs/spec.md").write_text("different",encoding="utf-8")
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)

    def test_requirement_and_acceptance_can_use_independent_traceability_index(self):
        self.manifest["documents"].append({"id": "trace", "path": "docs/traceability.md", "kind": "traceability-index", "required": True})
        (self.root / "docs/traceability.md").write_text("REQ-1 -> AT-1\n", encoding="utf-8")
        self.manifest["requirements"][0]["index"] = "trace"
        self.manifest["acceptance"][0]["index"] = "trace"
        (self.root / "docs/spec.md").write_text("User requirements and acceptance narrative", encoding="utf-8")
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

    def test_traceability_anchor_is_checked_when_declared(self):
        self.manifest["requirements"][0]["anchor"] = "Requirements"
        (self.root / "docs/spec.md").write_text("# Requirements\nREQ-1\nAT-1", encoding="utf-8")
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
    def test_lost_field(self):
        self.mapping["items"][0]["fields"]=["id"]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("field coverage",json.dumps(result))
    def test_stale_metadata_hash(self):
        with closing(sqlite3.connect(self.root / "data.sqlite")) as con:
            con.execute("ALTER TABLE accounts ADD COLUMN newer TEXT")
            con.commit()
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("stale",json.dumps(result))
    def test_manual_claim_complete_is_still_partial(self):
        self.source["provenance"]["type"]="manual"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("partial",[x["status"] for x in result["checks"]])
    def test_unknown_extractor_is_unsupported(self):
        self.source["provenance"]["type"]="magical"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,2)
    def test_forged_sqlite_inventory_cannot_pass(self):
        self.source["items"][0]["fields"]=["id"]
        self.mapping["items"][0]["fields"]=["id"]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("differs",json.dumps(result))
    def test_approval_only_selected_task_gate(self):
        self.manifest["tasks"][0]["approval"]={"status":"pending"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0)
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
    def test_handoff_requires_skill_review(self):
        self.manifest["tasks"][0].pop("skill_review")
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("skill_review",json.dumps(result))
    def test_task_dependency_not_complete(self):
        previous=copy.deepcopy(self.manifest["tasks"][0]);previous["id"]="TASK-0";previous["status"]="planned";previous["depends_on"]=[]
        self.manifest["tasks"].append(previous);self.manifest["tasks"][0]["depends_on"]=["TASK-0"]
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
    def test_module_dependency_rules_and_cycles(self):
        self.manifest["modules"][0]["depends_on"]=["core"]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("cycle",json.dumps(result))
    def test_boolean_string_is_config_error(self):
        self.manifest["checks"][0]["required"]="false"
        proc,result=self.cli("--mode","baseline")
        self.assertEqual(proc.returncode,2)
    def test_command_string_and_empty_manifest_rejected(self):
        self.manifest["checks"][0]["command"]="echo ok"
        proc,result=self.cli("--mode","baseline")
        self.assertEqual(proc.returncode,2)
        self.manifest={}
        proc,result=self.cli("--mode","baseline")
        self.assertEqual(proc.returncode,2)
    def test_path_escape_rejected(self):
        self.manifest["documents"][0]["path"]="../outside.md"
        proc,result=self.cli("--mode","baseline")
        self.assertEqual(proc.returncode,2)
    def test_malformed_json(self):
        self.write();(self.root/"manifest.json").write_text("{",encoding="utf-8")
        proc=subprocess.run([sys.executable,str(SCRIPTS/"check_project.py"),"--root",str(self.root),"--manifest","manifest.json","--mode","baseline"],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2);self.assertFalse(json.loads(proc.stdout)["required_checks_satisfied"])
    def test_symlink_checked_before_resolve(self):
        target=self.root/"real.md";target.write_text("content")
        link=self.root/"link.md"
        try:link.symlink_to(target)
        except OSError:
            # Native symlink creation needs OS privilege; exercise the same path
            # decision using the filesystem predicate, without claiming native coverage.
            link.write_text("content")
            self.write()
            with mock.patch.object(Path,"is_symlink",autospec=True,side_effect=lambda p: p == link):
                with self.assertRaises(checker.ConfigError):checker.safe_path(self.root,"link.md")
        else:
            self.manifest["documents"][0]["path"]="link.md"
            proc,result=self.cli("--mode","baseline")
            self.assertEqual(proc.returncode,2)
    def test_module_walk_prunes_excluded_pnpm_links(self):
        excluded = self.root / "src/node_modules"
        excluded.mkdir(parents=True)
        link = excluded / "workspace-package"
        link.write_text("placeholder")
        self.manifest["exclude_paths"].append("src/node_modules")
        with mock.patch.object(Path, "is_symlink", autospec=True, side_effect=lambda path: path == link):
            proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0, result)
    def test_module_walk_rejects_unexcluded_link(self):
        link = self.root / "src/workspace-package"
        link.write_text("placeholder")
        self.write()
        with mock.patch.object(Path, "is_symlink", autospec=True, side_effect=lambda path: path == link):
            with self.assertRaises(checker.ConfigError):
                checker.validate(self.root, self.manifest, "baseline", None)
    def test_change_requires_git_and_task(self):
        if (self.root / ".git").exists():
            (self.root / ".git").rename(self.root / ".git-offline")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,2)
        self.assertIn("unsupported",[x["status"] for x in result["checks"]])
    @unittest.skipUnless(shutil.which("git"),"Git unavailable")
    def test_changed_untracked_deleted_and_excluded_paths(self):
        self.write()
        def git(*args):
            proc=subprocess.run(["git","-c","safe.directory="+str(self.root)]+list(args),cwd=self.root,capture_output=True)
            self.assertEqual(proc.returncode,0,proc.stderr)
        git("status","--porcelain")
        (self.root/"src/app.py").unlink();(self.root/"uncovered.txt").write_text("new");(self.root/"src/new.py").write_text("new")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("src/app.py",result["changed_paths"]);self.assertIn("uncovered.txt",result["changed_paths"])
        self.manifest["exclude_paths"].append("uncovered.txt")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,0,result)
    def test_broken_document_link(self):
        (self.root/"docs/module.md").write_text("[broken](missing.md)")
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
    def test_report_cannot_overwrite_manifest(self):
        self.write()
        before=(self.root/"manifest.json").read_bytes()
        proc,result=self.cli("--mode","baseline","--run-checks","--report","manifest.json")
        self.assertEqual(proc.returncode,2)
        self.assertEqual((self.root/"manifest.json").read_bytes(),before)
        self.assertFalse(result["required_checks_satisfied"])
    def test_report_new_file_and_escape(self):
        proc,result=self.cli("--mode","baseline","--run-checks","--report","report.json")
        self.assertEqual(proc.returncode,0)
        self.assertEqual(json.loads((self.root/"report.json").read_text()),result)
        proc,result=self.cli("--mode","baseline","--run-checks","--report","../escape.json")
        self.assertEqual(proc.returncode,2)
    def test_root_ancestor_symlink_predicate(self):
        ancestor=self.root.parent
        with mock.patch.object(Path,"is_symlink",autospec=True,side_effect=lambda p: p==ancestor):
            with self.assertRaises(checker.ConfigError):checker.safe_root(self.root)
    def test_in_root_parent_document_link_is_allowed(self):
        (self.root/"docs/module.md").write_text("[spec](../docs/spec.md)")
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0,result)
    def test_optional_but_referenced_document_missing_fails(self):
        self.manifest["documents"][0]["required"]=False
        (self.root/"docs/spec.md").unlink()
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1,result)
    def test_handoff_requires_base_and_change_scope(self):
        self.write()
        proc=subprocess.run([sys.executable,str(SCRIPTS/"check_project.py"),"--root",str(self.root),"--manifest","manifest.json","--mode","handoff","--task","TASK-1","--run-checks"],capture_output=True,text=True)
        self.assertEqual(proc.returncode,2)
        (self.root/"unknown.py").write_text("new")
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
    def test_git_base_cannot_be_command_option(self):
        for base in ("--cached","--output=attack.txt"):
            proc,result=self.cli("--mode","change","--task","TASK-1","--base="+base,"--run-checks")
            self.assertEqual(proc.returncode,2,result)
        self.assertFalse((self.root/"attack.txt").exists())
    @unittest.skipUnless(shutil.which("git"),"Git unavailable")
    def test_cross_module_rename_records_old_path(self):
        other=self.root/"other";other.mkdir();(other/"old.py").write_text("content")
        self.manifest["modules"].append({"id":"other","source_paths":["other"],"document":"module","depends_on":[],"allowed_dependencies":[]})
        self.write();self.git("add",".");self.git("-c","user.name=Test","-c","user.email=test@example.invalid","commit","-m","other")
        (other/"old.py").rename(self.root/"src/new.py")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,1,result)
        self.assertIn("other/old.py",result["changed_paths"])
    @unittest.skipUnless(shutil.which("git"),"Git unavailable")
    def test_absolute_source_scope_is_canonicalized(self):
        self.manifest["modules"][0]["source_paths"]=[str(self.root/"src")]
        (self.root/"src/app.py").write_text("changed")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,0,result)

    @unittest.skipUnless(shutil.which("git"),"Git unavailable")
    def test_documentation_impact_requires_and_allows_flow_document(self):
        flow = self.root / "docs/flow.md"
        flow.write_text("flow", encoding="utf-8")
        self.manifest["documents"].append({"id":"flow","path":"docs/flow.md","kind":"business-flow","required":True})
        self.manifest["tasks"][0]["documentation_impact"] = {
            "module-connectivity": {"when_paths":["src"],"document_ids":["flow"]}
        }
        self.manifest["exclude_paths"].append("manifest.json")
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "flow baseline")

        (self.root/"src/app.py").write_text("changed", encoding="utf-8")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,1,result)
        scope = next(check for check in result["checks"] if check["rule_id"] == "change-scope")
        self.assertTrue(any("requires document update" in gap for gap in scope["evidence"]["documentation_gaps"]))

        flow.write_text("updated flow", encoding="utf-8")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        self.assertEqual(proc.returncode,0,result)

    def test_documentation_impact_trigger_must_be_inside_module_or_document_scope(self):
        self.manifest["tasks"][0]["documentation_impact"] = {
            "module-connectivity": {"when_paths": ["unrelated"], "document_ids": ["module"]}
        }
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        self.assertIn("outside module/document scopes", json.dumps(result))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_commit_gate_requires_document_in_same_staged_index(self):
        flow = self.root / "docs/flow.md"
        flow.write_text("flow", encoding="utf-8")
        self.manifest["documents"].append({"id":"flow","path":"docs/flow.md","kind":"business-flow","required":True})
        self.manifest["tasks"][0]["documentation_impact"] = {
            "module-connectivity": {"when_paths":["src"],"document_ids":["flow"]}
        }
        self.manifest["exclude_paths"].append("manifest.json")
        self.write(); self.git("add", "."); self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "commit gate baseline")

        (self.root / "src/app.py").write_text("changed", encoding="utf-8")
        self.git("add", "src/app.py")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        scope = next(check for check in result["checks"] if check["rule_id"] == "commit-scope")
        self.assertTrue(any("requires document update" in gap for gap in scope["evidence"]["documentation_gaps"]))

        flow.write_text("updated flow", encoding="utf-8")
        self.git("add", "docs/flow.md")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
        self.assertEqual(result["mode"], "commit")

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_commit_gate_ignores_unstaged_document_update(self):
        flow = self.root / "docs/flow.md"
        flow.write_text("flow", encoding="utf-8")
        self.manifest["documents"].append({"id":"flow","path":"docs/flow.md","kind":"business-flow","required":True})
        self.manifest["tasks"][0]["documentation_impact"] = {
            "module-connectivity": {"when_paths":["src"],"document_ids":["flow"]}
        }
        self.manifest["exclude_paths"].append("manifest.json")
        self.write(); self.git("add", "."); self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "commit gate baseline")

        (self.root / "src/app.py").write_text("changed", encoding="utf-8")
        flow.write_text("updated but not staged", encoding="utf-8")
        self.git("add", "src/app.py")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_commit_paths_include_initial_commit_deletion_and_rename(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            def git(*args):
                proc = subprocess.run(["git", "-c", "safe.directory=" + str(root)] + list(args), cwd=root, capture_output=True)
                self.assertEqual(proc.returncode, 0, proc.stderr)
            git("init")
            (root / "old.md").write_text("old", encoding="utf-8")
            git("add", "old.md")
            self.assertEqual(checker.staged_git_paths(root), ["old.md"])
            git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "initial")
            (root / "old.md").rename(root / "new.md")
            git("add", "-A")
            self.assertEqual(checker.staged_git_paths(root), ["new.md", "old.md"])
            (root / "new.md").unlink()
            git("add", "-A")
            self.assertEqual(checker.staged_git_paths(root), ["old.md"])

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_commit_gate_reads_task_id_from_environment(self):
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}
        }
        self.write()
        self.git("add", "manifest.json")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "task gate baseline")
        (self.root / "src/app.py").write_text("environment task", encoding="utf-8")
        (self.root / "docs/impact.md").write_text("implementation-only evidence", encoding="utf-8")
        self.git("add", "src/app.py", "docs/impact.md")
        with mock.patch.dict(os.environ, {"ENGINEERING_TASK_ID": "TASK-1"}, clear=False):
            proc, result = self.cli("--mode", "commit", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_control_plane_changes_require_external_approval(self):
        self.manifest["control_plane"] = {
            "protected_paths": ["manifest.json"],
            "approval_env": "TEST_CONTROL_PLANE_APPROVED",
        }
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}
        }
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "control baseline")

        self.manifest["control_plane"]["protected_paths"].append("docs/approval.md")
        self.write()
        self.git("add", "manifest.json")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        control = next(check for check in result["checks"] if check["rule_id"] == "control-plane")
        self.assertEqual(control["status"], "fail")
        self.assertIn("manifest.json", control["evidence"]["changed_paths"])

        with mock.patch.dict(os.environ, {"TEST_CONTROL_PLANE_APPROVED": "1"}, clear=False):
            proc, result = self.cli("--mode", "commit", "--task", "TASK-1",
                                    "--allow-control-plane-change", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
        control = next(check for check in result["checks"] if check["rule_id"] == "control-plane")
        self.assertEqual(control["status"], "pass")

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_control_plane_committed_mode_uses_parent_manifest(self):
        self.manifest["control_plane"] = {
            "protected_paths": ["manifest.json"],
            "approval_env": "TEST_CONTROL_PLANE_APPROVED",
        }
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}
        }
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "control baseline")
        self.manifest.pop("control_plane")
        self.write()
        self.git("add", "manifest.json")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "control change")

        proc, result = self.cli("--mode", "committed", "--commit-ref", "HEAD", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        control = next(check for check in result["checks"] if check["rule_id"] == "control-plane")
        self.assertEqual(control["status"], "fail")
        self.assertIn("manifest.json", control["evidence"]["changed_paths"])

        with mock.patch.dict(os.environ, {"TEST_CONTROL_PLANE_APPROVED": "1"}, clear=False):
            proc, result = self.cli("--mode", "committed", "--commit-ref", "HEAD", "--task", "TASK-1",
                                    "--allow-control-plane-change", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_control_plane_approval_variable_cannot_be_changed_in_same_commit(self):
        self.manifest["control_plane"] = {
            "protected_paths": ["manifest.json"],
            "approval_env": "TEST_CONTROL_PLANE_APPROVED",
        }
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}
        }
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "control baseline")
        self.manifest["control_plane"]["approval_env"] = "ATTACKER_CHOSEN_APPROVAL"
        self.write()
        self.git("add", "manifest.json")
        with mock.patch.dict(os.environ, {
            "TEST_CONTROL_PLANE_APPROVED": "0",
            "ATTACKER_CHOSEN_APPROVAL": "1",
        }, clear=False):
            proc, result = self.cli("--mode", "commit", "--task", "TASK-1",
                                    "--allow-control-plane-change", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        control = next(check for check in result["checks"] if check["rule_id"] == "control-plane")
        self.assertEqual(control["evidence"]["approval_variable"], "TEST_CONTROL_PLANE_APPROVED")
        self.assertFalse(control["evidence"]["external_approval_present"])

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_control_plane_failure_does_not_execute_declared_commands(self):
        marker = self.root / "command-ran.txt"
        self.manifest["control_plane"] = {"protected_paths": ["manifest.json"], "approval_env": "TEST_CONTROL_PLANE_APPROVED"}
        self.manifest["tasks"][0]["documentation_impact"] = {"implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}}
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "open('command-ran.txt','w').write('ran')"]
        self.write(); self.git("add", "."); self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "safe command baseline")
        self.manifest["control_plane"]["protected_paths"].append("docs/approval.md")
        self.write(); self.git("add", "manifest.json")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        self.assertFalse(marker.exists())

    def prepare_command_marker(self):
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}
        }
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "open('command-ran.txt','w').write('ran')"]
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "marker baseline")

    def clone_shallow_fixture(self, destination):
        proc = subprocess.run(["git", "clone", "--depth", "1", self.root.as_uri(), str(destination)],
                              capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertTrue(checker.git_is_shallow(destination))

    def fixture_cli(self, root, mode, *extra):
        args = [sys.executable, str(SCRIPTS / "check_project.py"), "--root", str(root),
                "--manifest", "manifest.json", "--mode", mode, "--task", "TASK-1", "--run-checks"]
        if mode == "committed":
            args.extend(["--commit-ref", "HEAD"])
        proc = subprocess.run(args + list(extra), capture_output=True, text=True)
        return proc, json.loads(proc.stdout)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_scope_failure_blocks_declared_commands_in_both_commit_modes(self):
        self.prepare_command_marker()
        (self.root / "src/app.py").write_text("changed without documentation", encoding="utf-8")
        self.git("add", "src/app.py")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        self.assertFalse((self.root / "command-ran.txt").exists(), result)
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "missing documentation")
        proc, result = self.fixture_cli(self.root, "committed")
        self.assertEqual(proc.returncode, 1, result)
        self.assertFalse((self.root / "command-ran.txt").exists(), result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_commit_discovery_error_does_not_execute_declared_commands(self):
        self.prepare_command_marker()
        proc, result = self.fixture_cli(self.root, "committed", "--commit-ref", "missing-reference")
        self.assertEqual(proc.returncode, 2, result)
        self.assertFalse((self.root / "command-ran.txt").exists(), result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_unstaged_manifest_command_never_executes_in_both_commit_modes(self):
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]}
        }
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "gate baseline")
        (self.root / "src/app.py").write_text("documented change", encoding="utf-8")
        (self.root / "docs/impact.md").write_text("reviewed change", encoding="utf-8")
        self.git("add", "src/app.py", "docs/impact.md")
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "open('command-ran.txt','w').write('ran')"]
        self.write()
        proc, result = self.fixture_cli(self.root, "commit")
        self.assertEqual(proc.returncode, 1, result)
        self.assertFalse((self.root / "command-ran.txt").exists(), result)
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "documented change")
        proc, result = self.fixture_cli(self.root, "committed")
        self.assertEqual(proc.returncode, 1, result)
        self.assertFalse((self.root / "command-ran.txt").exists(), result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_shallow_clone_refuses_both_modes_without_running_commands(self):
        self.prepare_command_marker()
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp).resolve() / "shallow"
            self.clone_shallow_fixture(clone)
            for mode in ("committed", "commit"):
                with self.subTest(mode=mode):
                    proc, result = self.fixture_cli(clone, mode)
                    self.assertEqual(proc.returncode, 2, result)
                    self.assertIn("shallow", json.dumps(result).lower())
                    self.assertFalse((clone / "command-ran.txt").exists(), result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_missing_parent_object_is_not_treated_as_root_and_cannot_run_commands(self):
        self.assertIsNone(checker.git_parent(self.root, "HEAD"))
        self.prepare_command_marker()
        with tempfile.TemporaryDirectory() as tmp:
            clone = Path(tmp).resolve() / "missing-parent"
            self.clone_shallow_fixture(clone)
            # Remove only the fixture's shallow marker; the raw commit still
            # declares a parent object that this clone does not possess.
            (clone / ".git" / "shallow").unlink()
            self.assertFalse(checker.git_is_shallow(clone))
            with self.assertRaisesRegex(checker.ConfigError, "parent.*unavailable|missing.*parent"):
                checker.git_parent(clone, "HEAD")
            for mode in ("committed", "commit"):
                with self.subTest(mode=mode):
                    proc, result = self.fixture_cli(clone, mode)
                    self.assertEqual(proc.returncode, 2, result)
                    self.assertFalse((clone / "command-ran.txt").exists(), result)

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_commit_rejects_undeclared_source_change(self):
        (self.root / "src/app.py").write_text("changed", encoding="utf-8")
        self.git("add", "src/app.py")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        self.assertIn("documentation_impact", json.dumps(result))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_committed_mode_rechecks_same_commit_tree(self):
        flow = self.root / "docs/flow.md"
        flow.write_text("flow", encoding="utf-8")
        self.manifest["documents"].append({"id":"flow","path":"docs/flow.md","kind":"business-flow","required":True})
        self.manifest["tasks"][0]["documentation_impact"] = {
            "module-connectivity": {"when_paths":["src"],"document_ids":["flow"]}
        }
        self.write(); self.git("add", "."); self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "gate baseline")
        (self.root / "src/app.py").write_text("changed", encoding="utf-8")
        flow.write_text("updated flow", encoding="utf-8")
        self.git("add", "src/app.py", "docs/flow.md")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "documented change")
        proc, result = self.cli("--mode", "committed", "--commit-ref", "HEAD", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
        self.assertIn("src/app.py", result["changed_paths"])
        flow.write_text("unstaged", encoding="utf-8")
        proc, result = self.cli("--mode", "committed", "--commit-ref", "HEAD", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)

class SQLiteTests(unittest.TestCase):
    def test_real_extraction_roundtrip_database_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();db=root/"schema #1.sqlite"
            with closing(sqlite3.connect(db)) as con:
                con.execute('CREATE TABLE accounts(id INTEGER PRIMARY KEY,value TEXT, derived TEXT GENERATED ALWAYS AS (value) VIRTUAL)')
                con.execute("INSERT INTO accounts(value) VALUES ('private')")
                con.execute("CREATE VIEW names AS SELECT value FROM accounts")
                con.commit()
            before=db.read_bytes();data=extractor.extract(db)
            self.assertEqual(db.read_bytes(),before)
            by_id={item["id"]:item for item in data["items"]}
            self.assertEqual(by_id["accounts"]["fields"],["id","value","derived"])
            self.assertEqual(by_id["names"]["fields"],["value"])
            self.assertNotIn("private",json.dumps(data))
            (root/"db.md").write_text("schema")
            mapping={"kind":"database","items":[{"id":item["id"],"document":"db.md","fields":item["fields"]} for item in data["items"]]}
            (root/"source.json").write_text(json.dumps(data));(root/"map.json").write_text(json.dumps(mapping))
            result=checker.validate_inventory(root,"db",{"required":True,"kind":"database","path":"source.json","documentation":"map.json"})
            self.assertEqual(result["status"],"pass",result)
    def test_extractor_output_cannot_replace_database(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/"a.sqlite"
            with closing(sqlite3.connect(db)) as con:
                con.execute("CREATE TABLE t(id INTEGER)")
                con.commit()
            before=db.read_bytes()
            proc=subprocess.run([sys.executable,str(SCRIPTS/"extract_sqlite.py"),str(db),"--output",str(db)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,2);self.assertEqual(db.read_bytes(),before)

    def test_extractor_update_requires_generated_snapshot_and_replaces_atomically(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/"a.sqlite";target=Path(tmp)/"inventory.json"
            with closing(sqlite3.connect(db)) as con:
                con.execute("CREATE TABLE t(id INTEGER)")
                con.commit()
            first=subprocess.run([sys.executable,str(SCRIPTS/"extract_sqlite.py"),str(db),"--output",str(target)],capture_output=True,text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original=json.loads(target.read_text())
            updated=subprocess.run([sys.executable,str(SCRIPTS/"extract_sqlite.py"),str(db),"--output",str(target),"--update"],capture_output=True,text=True)
            self.assertEqual(updated.returncode, 0, updated.stderr)
            self.assertEqual(json.loads(target.read_text())["tool_version"], extractor.TOOL_VERSION)
            target.write_text(json.dumps({"kind":"database","items":[]}), encoding="utf-8")
            rejected=subprocess.run([sys.executable,str(SCRIPTS/"extract_sqlite.py"),str(db),"--output",str(target),"--update"],capture_output=True,text=True)
            self.assertEqual(rejected.returncode, 2)
            self.assertEqual(json.loads(target.read_text())["items"], [])

    def test_unified_database_extractor_update_rejects_handwritten_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/"a.sqlite";target=Path(tmp)/"inventory.json"
            with closing(sqlite3.connect(db)) as con:
                con.execute("CREATE TABLE t(id INTEGER)")
                con.commit()
            target.write_text(json.dumps({"kind":"database","items":[]}), encoding="utf-8")
            proc=subprocess.run([sys.executable,str(SCRIPTS/"extract_database.py"),"sqlite","--database",str(db),"--output",str(target),"--update"],capture_output=True,text=True)
            self.assertEqual(proc.returncode,2)
    def test_wal_rejected_without_side_effects(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/"a.sqlite"
            con=sqlite3.connect(db);con.execute("PRAGMA journal_mode=WAL");con.execute("CREATE TABLE t(id INTEGER)");con.commit()
            try:
                with self.assertRaises(ValueError):extractor.extract(db)
            finally:con.close()
    def test_output_never_overwrites_other_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            db=Path(tmp)/"a.sqlite";target=Path(tmp)/"notes.md";target.write_text("keep")
            with closing(sqlite3.connect(db)) as con:con.execute("CREATE TABLE t(id INTEGER)")
            proc=subprocess.run([sys.executable,str(SCRIPTS/"extract_sqlite.py"),str(db),"--output",str(target)],capture_output=True,text=True)
            self.assertEqual(proc.returncode,2);self.assertEqual(target.read_text(),"keep")

    def test_update_replaces_only_generated_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); db = root / "a.sqlite"; target = root / "inventory.json"
            with closing(sqlite3.connect(db)) as con:
                con.execute("CREATE TABLE t(id INTEGER)"); con.commit()
            first = subprocess.run([sys.executable, str(SCRIPTS / "extract_sqlite.py"), str(db), "--output", str(target)], capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = target.read_text()
            with closing(sqlite3.connect(db)) as con:
                con.execute("ALTER TABLE t ADD COLUMN name TEXT"); con.commit()
            updated = subprocess.run([sys.executable, str(SCRIPTS / "extract_sqlite.py"), str(db), "--output", str(target), "--update"], capture_output=True, text=True)
            self.assertEqual(updated.returncode, 0, updated.stderr)
            self.assertNotEqual(target.read_text(), original)
            self.assertEqual(json.loads(target.read_text())["tool_version"], extractor.TOOL_VERSION)

    def test_update_rejects_non_generated_snapshot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); db = root / "a.sqlite"; target = root / "notes.json"
            with closing(sqlite3.connect(db)) as con: con.execute("CREATE TABLE t(id INTEGER)")
            target.write_text(json.dumps({"kind": "database", "tool_version": "other"}))
            proc = subprocess.run([sys.executable, str(SCRIPTS / "extract_sqlite.py"), str(db), "--output", str(target), "--update"], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 2)
            self.assertIn("not generated", proc.stderr)

class DatabaseAdapterTests(unittest.TestCase):
    class Cursor:
        def __init__(self, responses):
            self.responses = iter(responses)
            self.queries = []
        def execute(self, query, params):
            self.queries.append((query, params))
        def fetchall(self):
            return next(self.responses)
        def close(self):
            pass

    class Connection:
        def __init__(self, responses):
            self.cursor_value = DatabaseAdapterTests.Cursor(responses)
        def cursor(self):
            return self.cursor_value
        def close(self):
            pass

    def test_mysql_metadata_adapter_reads_information_schema_only(self):
        connection = self.Connection([
            [("app", "accounts", "BASE TABLE")],
            [("app", "accounts", "id", "int", 1, "NO", None),
             ("app", "accounts", "status", "varchar", 2, "YES", "'new'")],
        ])
        snapshot = database_extractor.extract_mysql(connection, "app", "mysql://db.example/app")
        self.assertEqual(snapshot["provenance"]["type"], "mysql-metadata")
        self.assertEqual(snapshot["provenance"]["source_ref"], "mysql://db.example/app")
        self.assertEqual(snapshot["items"][0]["fields"], ["id", "status"])
        self.assertTrue(all("information_schema" in query.lower() for query, _ in connection.cursor_value.queries))

    def test_postgresql_metadata_adapter_filters_system_schemas(self):
        connection = self.Connection([
            [("public", "accounts", "BASE TABLE")],
            [("public", "accounts", "id", "integer", 1, "NO", None)],
        ])
        snapshot = database_extractor.extract_postgresql(connection, "public", "postgresql://db.example/app")
        self.assertEqual(snapshot["provenance"]["type"], "postgresql-metadata")
        self.assertEqual(snapshot["items"][0]["id"], "public.accounts")
        self.assertTrue(all("information_schema" in query.lower() for query, _ in connection.cursor_value.queries))

    def test_redis_adapter_uses_keyspace_info_without_scan_or_values(self):
        class Redis:
            def __init__(self):
                self.calls = []
            def info(self, section=None):
                self.calls.append(("info", section))
                return {"db0": {"keys": 3, "expires": 1, "avg_ttl": 20}}
            def scan(self, *args, **kwargs):
                raise AssertionError("SCAN must not be used")
            def get(self, *args, **kwargs):
                raise AssertionError("business values must not be read")
        redis = Redis()
        snapshot = database_extractor.extract_redis(redis, "redis://cache.example")
        self.assertEqual(snapshot["provenance"]["type"], "redis-metadata")
        self.assertEqual(snapshot["items"][0]["object_kind"], "keyspace")
        self.assertEqual(redis.calls, [("info", "keyspace")])

    def test_remote_snapshot_digest_is_verified_offline(self):
        items = [{"id": "db0", "fields": ["keys"]}]
        source = {
            "kind": "database",
            "provenance": {
                "type": "redis-metadata", "scope": "keyspace", "complete": True,
                "evidence": "fixture", "source_ref": "redis://cache.example",
                "captured_at": "2026-10-13T00:00:00+00:00",
                "query_sha256": hashlib.sha256(database_extractor.QUERY_HASHES["redis"].encode("utf-8")).hexdigest(),
                "snapshot_sha256": database_extractor.snapshot_digest(items),
                "source_files": [],
            },
            "items": items,
        }
        with tempfile.TemporaryDirectory() as tmp:
            # Match the CLI's canonical root: Windows TEMP may use an 8.3 alias.
            root = checker.safe_root(tmp)
            (root / "inventory.json").write_text(json.dumps(source), encoding="utf-8")
            (root / "mapping.json").write_text(json.dumps({"kind": "database", "items": [{"id": "db0", "document": "db.md", "fields": ["keys"]}]}), encoding="utf-8")
            (root / "db.md").write_text("db0 keys", encoding="utf-8")
            result = checker.validate_inventory(root, "remote", {"required": True, "kind": "database", "path": "inventory.json", "documentation": "mapping.json"})
        self.assertEqual(result["status"], "pass", result)

if __name__=="__main__":unittest.main()

