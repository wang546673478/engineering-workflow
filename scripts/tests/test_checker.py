import copy
from contextlib import closing, redirect_stdout
import ctypes
import hashlib
import importlib.util
import io
import json
import os
import re
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
        # Fixture projects own their task/approval inputs, even inside a CI gate.
        environment = mock.patch.dict(os.environ, {})
        environment.start()
        self.addCleanup(environment.stop)
        os.environ.pop("ENGINEERING_TASK_ID", None)
        os.environ.pop("ENGINEERING_CONTROL_PLANE_APPROVED", None)
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name).resolve()
        for path, content in {"docs/spec.md":"REQ-1 AT-1", "docs/module.md":"module", "docs/impact.md":"impact", "docs/baseline.md":"reviewed", "docs/approval.md":"approved", "src/app.py":"print('app')", "data.sql":"CREATE TABLE accounts(id integer);", "docs/db.md":"accounts id value"}.items():
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
        # The execution marker is a deliberate generated artifact, not source drift.
        (self.root / ".gitignore").write_text("command-ran.txt\n", encoding="utf-8")
        with closing(sqlite3.connect(self.root / "data.sqlite")) as con:
            con.execute("CREATE TABLE accounts(id INTEGER,value TEXT)")
            con.commit()
        self.source = {"kind":"database","provenance":{"type":"sqlite-metadata","scope":"main metadata","complete":True,"evidence":"fixture snapshot","source_files":[{"path":"data.sqlite","sha256":checker.file_hash(self.root/"data.sqlite")}]}, "items":[{"id":"accounts","fields":["id","value"]}]}
        self.mapping = {"kind":"database","items":[{"id":"accounts","document":"docs/db.md","fields":["id","value"]}]}
        self.manifest = {"schema_version":1,"documents":[{"id":i,"path":p,"kind":"spec" if i=="spec" else "other","required":True} for i,p in [("spec","docs/spec.md"),("module","docs/module.md"),("impact","docs/impact.md")]],"requirements":[{"id":"REQ-1","document":"spec"}],"acceptance":[{"id":"AT-1","document":"spec"}],"modules":[{"id":"core","source_paths":["src"],"document":"module","depends_on":[],"allowed_dependencies":[]}],"inventories":[{"id":"db","kind":"database","path":"inventory.json","documentation":"mapping.json","required":True}],"checks":[{"id":"unit","command":[sys.executable,"-c","print('ok')"],"required":True,"timeout_seconds":5}],"tasks":[{"id":"TASK-1","requirement_ids":["REQ-1"],"acceptance_ids":["AT-1"],"module_ids":["core"],"depends_on":[],"status":"complete","impact_document":"impact","required_checks":["unit"],"approval_required":True,"approval":{"status":"approved","evidence":"docs/approval.md"},"skill_review":{"catalog_source":"test fixture","scope":"test task","checked_at":"2026-10-13T00:00:00+08:00","candidates":[],"recheck":"none"}}],"baseline":{"status":"complete","evidence":"docs/baseline.md"},"exclude_paths":["manifest.json","inventory.json","mapping.json","data.sql","docs/spec.md","docs/baseline.md","docs/approval.md","docs/db.md"]}
        self.write()
        if shutil.which("git"):
            # Each fixture has the same initial bytes. Copy a real committed
            # seed's complete .git directory, never shared worktree metadata
            # or hardlinks, so later commits/config/object deletions are private.
            seed = getattr(CheckerTests, "_repository_seed", None)
            if seed is None:
                self.git("init")
                self.git("add", ".")
                self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "baseline")
                seed = tempfile.TemporaryDirectory(prefix="checker-git-seed-")
                shutil.copytree(self.root / ".git", Path(seed.name) / ".git")
                CheckerTests._repository_seed = seed
            else:
                shutil.copytree(Path(seed.name) / ".git", self.root / ".git")
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

    def test_discovery_mode_allows_an_existing_incomplete_baseline_without_claiming_completion(self):
        self.manifest["workflow"] = {
            "active_task": "TASK-1", "stage": "takeover_discovery", "implementation_paths": ["src"],
            "baseline_review": {"status": "pending", "evidence": None},
            "proposal_approval": {"status": "pending", "evidence": None},
        }
        self.manifest["baseline"].update(status="partial", origin="existing", reason="Discovery is in progress",
                                          source_revision="fixture-head", scope="src", implementation_paths=["src"])
        self.manifest["tasks"][0]["status"] = "in_progress"
        self.manifest["tasks"][0]["implementation_authorization"] = {"status": "pending", "task_id": "TASK-1"}
        proc, result = self.cli("--mode", "discovery", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
        lifecycle = next(item for item in result["checks"] if item["rule_id"] == "workflow-lifecycle")
        self.assertFalse(lifecycle["evidence"]["completion_ready"])
        self.assertEqual(lifecycle["evidence"]["stage"], "takeover_discovery")

    def test_implementation_scope_changes_are_blocked_before_separate_approvals(self):
        self.manifest["workflow"] = {
            "active_task": "TASK-1", "stage": "plan_confirmation", "implementation_paths": ["src"],
            "baseline_review": {"status": "approved", "source_revision": "baseline-r1", "evidence": "docs/approval.md"},
            "proposal_approval": {"status": "pending", "evidence": None},
        }
        self.manifest["baseline"].update(status="approved", source_revision="baseline-r1")
        self.manifest["tasks"][0]["status"] = "in_progress"
        self.manifest["tasks"][0]["implementation_authorization"] = {"status": "pending", "evidence": None, "task_id": "TASK-1"}
        (self.root / "src/app.py").write_text("print('changed implementation')", encoding="utf-8")
        proc, result = self.cli("--mode", "change", "--task", "TASK-1", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        gate = next(item for item in result["checks"] if item["rule_id"] == "implementation-gate")
        self.assertEqual(gate["status"], "fail")
        self.assertIn("implementation", json.dumps(gate["evidence"]))

    def test_implementation_scope_changes_pass_only_after_all_lifecycle_approvals(self):
        self.manifest["workflow"] = {
            "active_task": "TASK-1", "stage": "implementation", "implementation_paths": ["src"],
            "baseline_review": {"status": "approved", "source_revision": "baseline-r1", "evidence": "docs/approval.md"},
            "proposal_approval": {"status": "approved", "revision": "plan-r1", "evidence": "docs/approval.md"},
        }
        self.manifest["baseline"].update(status="approved", source_revision="baseline-r1")
        self.manifest["tasks"][0]["status"] = "in_progress"
        self.manifest["tasks"][0]["implementation_authorization"] = {"status": "approved", "plan_revision": "plan-r1", "evidence": "docs/approval.md", "task_id": "TASK-1"}
        (self.root / "src/app.py").write_text("print('approved implementation')", encoding="utf-8")
        proc, result = self.cli("--mode", "change", "--task", "TASK-1", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
        gate = next(item for item in result["checks"] if item["rule_id"] == "implementation-gate")
        self.assertEqual(gate["status"], "pass")

    def lifecycle_fixture(self):
        self.manifest["workflow"] = {
            "active_task": "TASK-1", "stage": "implementation", "implementation_paths": ["src"],
            "baseline_review": {"status": "approved", "source_revision": "baseline-r1", "evidence": "docs/approval.md"},
            "proposal_approval": {"status": "approved", "revision": "plan-r1", "evidence": "docs/approval.md"},
        }
        self.manifest["baseline"].update(status="approved", source_revision="baseline-r1")
        self.manifest["tasks"][0]["status"] = "in_progress"
        self.manifest["tasks"][0]["implementation_authorization"] = {
            "status": "approved", "plan_revision": "plan-r1", "evidence": "docs/approval.md", "task_id": "TASK-1"}

    def approval_contract_fixture(self, enforcement="strict"):
        self.lifecycle_fixture()
        (self.root / "docs/spec.md").write_text("# Approval scope\nREQ-1 AT-1\n", encoding="utf-8")
        subject_sha = hashlib.sha256(b"# Approval scope\nREQ-1 AT-1\n").hexdigest()
        records = {
            "BASELINE-APPROVAL": {
                "id": "BASELINE-APPROVAL", "status": "approved",
                "user_statement": "我已审阅当前基线范围和限制。",
                "approved_at": "2026-10-20T10:00:00+08:00", "recorded_at": "2026-10-20T10:00:01+08:00",
                "scope": "Review the listed project modules, public contracts and documented validation limits.", "source": {"kind": "conversation", "reference": "fixture-message-1"},
                "subject": {"document": "spec", "revision": "baseline-r1", "section_id": "Approval-Scope", "sha256": subject_sha},
            },
            "PROPOSAL-APPROVAL": {
                "id": "PROPOSAL-APPROVAL", "status": "approved",
                "user_statement": "按这个完整方案实施。",
                "approved_at": "2026-10-20T10:01:00+08:00", "recorded_at": "2026-10-20T10:01:01+08:00",
                "scope": "Implement the reviewed TASK-1 Plan for REQ-1, including its stated behavior and acceptance. No additional requirements or permission changes are included.", "source": {"kind": "conversation", "reference": "fixture-message-2"},
                "task_id": "TASK-1", "batch_id": "batch-r1", "requirement_ids": ["REQ-1"],
                "acceptance_ids": ["AT-1"],
                "subject": {"document": "spec", "revision": "plan-r1", "section_id": "Approval-Scope", "sha256": subject_sha},
                "spec_basis": {"document": "spec", "revision": "spec-r1", "section_id": "Approval-Scope", "sha256": subject_sha},
            },
            "IMPLEMENTATION-APPROVAL": {
                "id": "IMPLEMENTATION-APPROVAL", "status": "approved",
                "user_statement": "按这个完整方案实施。",
                "approved_at": "2026-10-20T10:01:00+08:00", "recorded_at": "2026-10-20T10:01:01+08:00",
                "scope": "Implement the reviewed TASK-1 Plan for REQ-1, including its stated behavior and acceptance. No additional requirements or permission changes are included.", "source": {"kind": "conversation", "reference": "fixture-message-2"},
                "task_id": "TASK-1", "batch_id": "batch-r1", "requirement_ids": ["REQ-1"],
                "acceptance_ids": ["AT-1"],
                "subject": {"document": "spec", "revision": "plan-r1", "section_id": "Approval-Scope", "sha256": subject_sha},
                "spec_basis": {"document": "spec", "revision": "spec-r1", "section_id": "Approval-Scope", "sha256": subject_sha},
            },
        }
        blocks = []
        for record in records.values():
            blocks.append("<!-- engineering-approval:%s -->\n```json\n%s\n```" % (record["id"], json.dumps(record, ensure_ascii=False, indent=2)))
        (self.root / "docs/approval.md").write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
        self.manifest["workflow"]["approval_policy"] = {"record_contract": 1, "enforcement": enforcement}
        self.manifest["workflow"]["approval_policy"]["minimum_checker_version"] = checker.VERSION
        self.manifest["workflow"]["baseline_review"].update(evidence="docs/approval.md", evidence_record_id="BASELINE-APPROVAL")
        self.manifest["workflow"]["proposal_approval"].update(evidence="docs/approval.md", evidence_record_id="PROPOSAL-APPROVAL", batch_id="batch-r1")
        self.manifest["tasks"][0].update(batch_id="batch-r1", artifact_revisions={"plan": "plan-r1", "spec": "spec-r1"})
        self.manifest["tasks"][0]["approval_required"] = False
        self.manifest["tasks"][0]["implementation_authorization"].update(
            evidence="docs/approval.md", evidence_record_id="IMPLEMENTATION-APPROVAL", batch_id="batch-r1", proposal_record_id="PROPOSAL-APPROVAL")

    def approval_cli(self, *extra):
        """Exercise the public CLI entrypoint without another interpreter for static contracts."""
        self.write()
        output = io.StringIO()
        with redirect_stdout(output):
            code = checker.main(["--root", str(self.root), "--manifest", "manifest.json", *extra])
        return subprocess.CompletedProcess([], code), json.loads(output.getvalue())

    def test_strict_approval_contract_accepts_bound_records(self):
        self.approval_contract_fixture()
        proc, report = self.cli("--mode", "change", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        contract = next(item for item in report["checks"] if item["rule_id"] == "approval-evidence")
        self.assertEqual(contract["status"], "pass")
        self.assertTrue(contract["required"])

    def test_strict_approval_contract_rejects_empty_or_placeholder_evidence(self):
        self.approval_contract_fixture()
        (self.root / "docs/approval.md").write_text("approved\n", encoding="utf-8")
        proc, report = self.approval_cli("--mode", "change", "--base", "HEAD")
        self.assertEqual(proc.returncode, 1, report)
        contract = next(item for item in report["checks"] if item["rule_id"] == "approval-evidence")
        self.assertEqual(contract["status"], "fail")
        self.assertTrue(contract["required"])

    def test_strict_approval_contract_rejects_plan_scope_drift(self):
        self.approval_contract_fixture()
        self.manifest["workflow"]["proposal_approval"]["revision"] = "plan-r2"
        proc, report = self.approval_cli("--mode", "change", "--base", "HEAD")
        self.assertEqual(proc.returncode, 1, report)
        self.assertIn("revision", json.dumps(next(item for item in report["checks"] if item["rule_id"] == "approval-evidence")))

    def test_diagnostic_approval_contract_reports_partial_without_blocking(self):
        self.approval_contract_fixture("diagnostic")
        (self.root / "docs/approval.md").write_text("approved\n", encoding="utf-8")
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        contract = next(item for item in report["checks"] if item["rule_id"] == "approval-evidence")
        self.assertEqual(contract["status"], "partial")
        self.assertFalse(contract["required"])

    def test_legacy_manifest_without_policy_keeps_existing_approval_behavior(self):
        self.lifecycle_fixture()
        self.manifest["workflow"].pop("approval_policy", None)
        proc, report = self.cli("--mode", "change", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        contract = next(item for item in report["checks"] if item["rule_id"] == "approval-evidence")
        self.assertEqual(contract["status"], "partial")
        self.assertFalse(contract["required"])

    def test_contract_rejects_stale_current_plan_and_does_not_run_commands(self):
        self.approval_contract_fixture()
        self.manifest["tasks"][0]["artifact_revisions"]["plan"] = "plan-r2"
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "open('command-ran.txt','w').write('ran')"]
        proc, report = self.cli("--mode", "change", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 1, report)
        self.assertFalse((self.root / "command-ran.txt").exists())
        self.assertIn("selected task Plan", str(next(c for c in report["checks"] if c["rule_id"] == "approval-evidence")))

    def test_contract_rejects_future_time_duplicate_blocks_and_snapshot_changes(self):
        for mutation in ("future", "duplicate", "snapshot", "spec_revision", "batch"):
            with self.subTest(mutation=mutation):
                self.approval_contract_fixture()
                path = self.root / "docs/approval.md"
                text = path.read_text(encoding="utf-8")
                if mutation == "future":
                    path.write_text(text.replace("2026-10-20", "2099-01-01"), encoding="utf-8")
                elif mutation == "duplicate":
                    path.write_text(text + text, encoding="utf-8")
                elif mutation == "snapshot":
                    (self.root / "docs/spec.md").write_text("# Approval scope\nREQ-1 AT-1 changed permission\n", encoding="utf-8")
                elif mutation == "spec_revision":
                    self.manifest["tasks"][0]["artifact_revisions"]["spec"] = "spec-r2"
                else:
                    self.manifest["tasks"][0]["batch_id"] = "new-batch"
                proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
                self.assertEqual(proc.returncode, 1, report)
                self.assertEqual(next(c for c in report["checks"] if c["rule_id"] == "approval-evidence")["status"], "fail")

    def test_contract_policy_removal_is_not_a_legacy_escape(self):
        self.approval_contract_fixture()
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "strict approval basis")
        self.manifest["workflow"].pop("approval_policy")
        self.write()
        proc, report = self.cli("--mode", "change", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 1, report)
        self.assertEqual(next(c for c in report["checks"] if c["rule_id"] == "approval-policy-history")["status"], "fail")

    def test_contract_sequence_is_optional_unless_explicitly_required(self):
        self.approval_contract_fixture()
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        sequence = next(c for c in report["checks"] if c["rule_id"] == "approval-sequence")
        self.assertEqual(sequence["status"], "partial")
        self.assertFalse(sequence["required"])
        self.manifest["workflow"]["approval_policy"]["sequence_enforcement"] = "strict"
        self.manifest["tasks"][0]["approval_sequence"] = {
            key: {"timeline_id": "fixture-chat", "position": position, "reference": "fixture-message-" + str(position)}
            for key, position in (("presented", 1), ("approved", 2), ("implementation", 3))}
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        self.manifest["tasks"][0]["approval_sequence"]["approved"]["position"] = 4
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, report)

    def test_contract_can_read_json_records_and_normalize_crlf(self):
        self.approval_contract_fixture()
        evidence = self.root / "docs/approval.md"
        records = [json.loads(part) for part in re.findall(r"```json\n(.*?)\n```", evidence.read_text(encoding="utf-8"), re.DOTALL)]
        (self.root / "docs/approval.json").write_text(json.dumps({"records": records}), encoding="utf-8")
        for record in (self.manifest["workflow"]["baseline_review"], self.manifest["workflow"]["proposal_approval"], self.manifest["tasks"][0]["implementation_authorization"]):
            record["evidence"] = "docs/approval.json"
        (self.root / "docs/spec.md").write_bytes(b"# Approval scope\r\nREQ-1 AT-1\r\n")
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)

    def test_contract_approved_scope_can_be_reused_without_new_user_statement(self):
        self.approval_contract_fixture()
        path = self.root / "docs/approval.md"
        text = path.read_text(encoding="utf-8")
        for kind, original in (("proposal_approval", "PROPOSAL-APPROVAL"), ("implementation_authorization", "IMPLEMENTATION-APPROVAL")):
            ident = original + "-REUSE"
            reuse = {"id": ident, "status": "approved", "task_id": "TASK-1", "batch_id": "batch-r2", "scope": "same approved requirement scope", "requirement_ids": ["REQ-1"], "acceptance_ids": ["AT-1"],
                     "reuse_of": {"evidence": "docs/approval.md", "evidence_record_id": original, "reason": "same accepted scope"}}
            text += "\n<!-- engineering-approval:%s -->\n```json\n%s\n```\n" % (ident, json.dumps(reuse))
            declaration = self.manifest["workflow"][kind] if kind == "proposal_approval" else self.manifest["tasks"][0][kind]
            declaration.update(evidence_record_id=ident, batch_id="batch-r2")
        self.manifest["tasks"][0]["batch_id"] = "batch-r2"
        self.manifest["tasks"][0]["implementation_authorization"]["proposal_record_id"] = "PROPOSAL-APPROVAL-REUSE"
        path.write_text(text, encoding="utf-8")
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)

    def test_strict_contract_accepts_evidenced_small_fix_not_applicable(self):
        self.approval_contract_fixture()
        task = self.manifest["tasks"][0]
        task["workflow_kind"] = "small_fix"
        declaration = self.manifest["workflow"]["proposal_approval"]
        declaration.update(status="not_applicable", revision="plan-r1", reason="Existing confirmed requirement; correction scope only.")
        path = self.root / "docs/approval.md"
        records = checker.approval_records(path)
        record = records["PROPOSAL-APPROVAL"]
        record.update(status="not_applicable", reason="Existing confirmed requirement; this correction does not change scope.",
                      scope="Existing confirmed requirement REQ-1 only.")
        record.pop("user_statement", None); record.pop("approved_at", None); record.pop("recorded_at", None); record.pop("source", None)
        baseline = records["BASELINE-APPROVAL"]; implementation = records["IMPLEMENTATION-APPROVAL"]
        rendered=[]
        for ident, value in (("BASELINE-APPROVAL", baseline), ("PROPOSAL-APPROVAL", record), ("IMPLEMENTATION-APPROVAL", implementation)):
            rendered.append("<!-- engineering-approval:%s -->\n```json\n%s\n```" % (ident, json.dumps(value, ensure_ascii=False, indent=2)))
        path.write_text("\n\n".join(rendered), encoding="utf-8")
        self.manifest["workflow"]["proposal_approval"]["status"] = "not_applicable"
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        declaration["status"] = "approved"
        task["workflow_kind"] = "major_change"
        proc, report = self.approval_cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, report)

    def test_contract_rejects_unsafe_records_and_preserves_incomplete_state(self):
        for mutation in ("path", "duplicate_key", "wrong_type", "invalidated", "capability"):
            with self.subTest(mutation=mutation):
                self.approval_contract_fixture()
                if mutation == "path":
                    self.manifest["workflow"]["proposal_approval"]["evidence"] = "../outside.json"
                elif mutation == "duplicate_key":
                    path=self.root/"docs/approval.md"
                    path.write_text(path.read_text(encoding="utf-8").replace('"status": "approved"','"status": "approved", "status": "approved"'),encoding="utf-8")
                elif mutation == "wrong_type":
                    path=self.root/"docs/approval.md"
                    path.write_text(path.read_text(encoding="utf-8").replace('"requirement_ids": [\n    "REQ-1"\n  ]','"requirement_ids": [{}]'),encoding="utf-8")
                elif mutation == "invalidated":
                    path=self.root/"docs/approval.md"
                    path.write_text(path.read_text(encoding="utf-8").replace('"status": "approved"','"status": "approved", "invalidated": true'),encoding="utf-8")
                else:
                    self.manifest["workflow"]["approval_policy"]["minimum_checker_version"] = "999.0.0"
                proc,report=self.approval_cli("--mode","change","--base","HEAD","--run-checks")
                self.assertNotEqual(proc.returncode,0,report)
                self.assertFalse(report["required_checks_satisfied"])

    def test_contract_bound_snapshots_and_capability_in_both_commit_modes(self):
        self.approval_contract_fixture()
        task=self.manifest["tasks"][0]
        task["documentation_impact"]={"implementation-only":{"when_paths":["src"],"document_ids":["impact"]}}
        self.write();self.git("add",".");self.git("-c","user.name=Test","-c","user.email=test@example.invalid","commit","-m","approved contract")
        (self.root/"src/app.py").write_text("print('bounded implementation')",encoding="utf-8")
        (self.root/"docs/impact.md").write_text("bounded change review",encoding="utf-8")
        self.git("add",".")
        proc,report=self.cli("--mode","commit","--run-checks","--require-approval-contract","1")
        self.assertEqual(proc.returncode,0,report)
        self.git("-c","user.name=Test","-c","user.email=test@example.invalid","commit","-m","bounded implementation")
        proc,report=self.cli("--mode","committed","--commit-ref","HEAD","--run-checks","--require-approval-contract","1")
        self.assertEqual(proc.returncode,0,report)
        self.assertIsNotNone(report["verified_tree"])
        (self.root/"docs/approval.md").write_text("approved",encoding="utf-8")
        proc,report=self.cli("--mode","committed","--commit-ref","HEAD","--run-checks","--require-approval-contract","1")
        self.assertEqual(proc.returncode,1,report)

    def test_lifecycle_rejects_missing_approval_and_revision_or_task_mismatches(self):
        self.lifecycle_fixture()
        original = copy.deepcopy(self.manifest)
        cases = [
            ("baseline missing", lambda: self.manifest["workflow"]["baseline_review"].update(status="pending")),
            ("proposal missing", lambda: self.manifest["workflow"]["proposal_approval"].update(status="pending")),
            ("authorization missing", lambda: self.manifest["tasks"][0].pop("implementation_authorization")),
            ("wrong task", lambda: self.manifest["tasks"][0]["implementation_authorization"].update(task_id="TASK-OTHER")),
            ("wrong plan", lambda: self.manifest["tasks"][0]["implementation_authorization"].update(plan_revision="stale-plan")),
            ("missing evidence", lambda: self.manifest["workflow"]["proposal_approval"].update(evidence="docs/missing.md")),
            ("partial existing baseline", lambda: self.manifest["baseline"].update(status="partial", origin="existing", reason="unfinished", scope="src")),
            ("invalidated reviewed baseline", lambda: self.manifest["workflow"]["baseline_review"].update(invalidated=True)),
        ]
        for label, mutation in cases:
            with self.subTest(label=label):
                self.manifest = copy.deepcopy(original)
                mutation()
                proc, report = self.cli("--mode", "baseline")
                self.assertEqual(proc.returncode, 1, report)
                self.assertFalse(report["required_checks_satisfied"])
                self.assertTrue(any(c["required"] and c["status"] == "fail" for c in report["checks"]))

    def test_both_commit_modes_block_implementation_before_authorization_without_running_commands(self):
        self.lifecycle_fixture()
        self.manifest["workflow"]["stage"] = "plan_confirmation"
        self.manifest["tasks"][0]["implementation_authorization"]["status"] = "pending"
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "from pathlib import Path; Path('command-ran.txt').touch()"]
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "declared lifecycle")
        (self.root / "src/app.py").write_text("print('unapproved implementation')", encoding="utf-8")
        self.git("add", "src/app.py")
        for mode in ("commit", "committed"):
            with self.subTest(mode=mode):
                if mode == "committed":
                    self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "fixture unapproved code")
                extra = ["--commit-ref", "HEAD"] if mode == "committed" else []
                proc, report = self.cli("--mode", mode, "--run-checks", *extra)
                self.assertEqual(proc.returncode, 1, report)
                gate = next(c for c in report["checks"] if c["rule_id"] == "implementation-gate")
                self.assertEqual(gate["status"], "fail")
                self.assertFalse((self.root / "command-ran.txt").exists())

    def test_absolute_implementation_scope_is_also_blocked_during_discovery(self):
        self.lifecycle_fixture()
        self.manifest["workflow"].update(stage="takeover_discovery", implementation_paths=[str(self.root / "src")])
        (self.root / "src/app.py").write_text("print('changed')", encoding="utf-8")
        proc, report = self.cli("--mode", "change", "--base", "HEAD")
        self.assertEqual(proc.returncode, 1, report)
        self.assertEqual(next(c for c in report["checks"] if c["rule_id"] == "implementation-gate")["status"], "fail")

    def test_handoff_accepts_completed_implementation_without_an_extra_stage(self):
        self.lifecycle_fixture()
        self.manifest["tasks"][0]["status"] = "complete"
        proc, report = self.cli("--mode", "handoff", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        self.assertEqual(next(c for c in report["checks"] if c["rule_id"] == "workflow-lifecycle")["status"], "pass")

    def test_greenfield_interview_and_implementation_do_not_require_a_fictitious_baseline_approval(self):
        self.lifecycle_fixture()
        (self.root / "src/app.py").unlink()
        self.manifest["baseline"].update(status="not_applicable", origin="greenfield", reason="Empty implementation inspected",
                                           scope="src", implementation_paths=["src"])
        self.manifest["workflow"]["baseline_review"] = {"status": "not_applicable", "reason": "No preexisting system to review", "evidence": "docs/baseline.md"}
        self.manifest["workflow"]["stage"] = "requirements_interview"
        self.manifest["workflow"]["proposal_approval"]["status"] = "pending"
        self.manifest["tasks"][0]["implementation_authorization"]["status"] = "pending"
        proc, report = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        self.manifest["workflow"]["stage"] = "implementation"
        self.manifest["workflow"]["proposal_approval"]["status"] = "approved"
        self.manifest["tasks"][0]["implementation_authorization"]["status"] = "approved"
        proc, report = self.cli("--mode", "change", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)

    def test_known_small_fix_uses_established_scope_and_one_existing_instruction(self):
        self.lifecycle_fixture()
        task = self.manifest["tasks"][0]
        task["workflow_kind"] = "small_fix"
        self.manifest["workflow"]["proposal_approval"] = {"status": "not_applicable", "revision": "fix-scope-r1",
            "reason": "Known defect under existing accepted requirements; minimal impact recorded", "evidence": "docs/approval.md"}
        task["implementation_authorization"].update(plan_revision="fix-scope-r1", evidence="docs/approval.md")
        (self.root / "src/app.py").write_text("print('bounded fix')", encoding="utf-8")
        proc, report = self.cli("--mode", "change", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        self.assertEqual(task["approval"]["evidence"], task["implementation_authorization"]["evidence"])
        task["workflow_kind"] = "major_change"
        proc, report = self.cli("--mode", "change", "--base", "HEAD")
        self.assertEqual(proc.returncode, 1, report)
        self.assertIn("small_fix", str(next(c for c in report["checks"] if c["rule_id"] == "workflow-lifecycle")))

    def test_resumption_reuses_valid_review_after_factual_baseline_refresh(self):
        self.lifecycle_fixture()
        self.manifest["workflow"]["stage"] = "requirements_interview"
        self.manifest["baseline"]["source_revision"] = "updated-factual-baseline-r2"
        proc, report = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        self.assertEqual(self.manifest["workflow"]["baseline_review"]["source_revision"], "baseline-r1")
        self.manifest["workflow"]["baseline_review"]["invalidated"] = True
        proc, report = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, report)

    def test_completed_greenfield_delivery_accepts_complete_factual_baseline(self):
        self.lifecycle_fixture()
        self.manifest["baseline"].update(status="complete", origin="greenfield", source_revision="delivered-slice-r2")
        self.manifest["workflow"]["stage"] = "complete"
        self.manifest["workflow"]["baseline_review"] = {"status": "not_applicable", "reason": "Original empty start; implemented facts now complete", "evidence": "docs/baseline.md"}
        self.manifest["tasks"][0]["status"] = "complete"
        proc, report = self.cli("--mode", "handoff", "--run-checks")
        self.assertEqual(proc.returncode, 0, report)
        self.manifest["baseline"]["origin"] = "existing"
        proc, report = self.cli("--mode", "handoff", "--run-checks")
        self.assertEqual(proc.returncode, 1, report)

    def test_unknown_manifest_active_task_blocks_baseline(self):
        self.manifest["workflow"] = {"active_task": "TASK-MISSING"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("workflow.active_task", json.dumps(result))

    def test_linked_artifact_pointers_and_task_links_pass(self):
        (self.root / "docs/plan.md").write_text("plan", encoding="utf-8")
        (self.root / "docs/task.md").write_text("task", encoding="utf-8")
        (self.root / "docs/trace.md").write_text("REQ-1 AT-1", encoding="utf-8")
        self.manifest["documents"].extend([
            {"id": "baseline", "path": "docs/baseline.md", "kind": "baseline", "required": True},
            {"id": "plan", "path": "docs/plan.md", "kind": "technical-plan", "required": True},
            {"id": "task", "path": "docs/task.md", "kind": "task", "required": True},
            {"id": "trace", "path": "docs/trace.md", "kind": "traceability-index", "required": True},
        ])
        self.manifest["workflow"] = {"active_baseline": "baseline", "active_spec": "spec", "active_plan": "plan", "active_task": "TASK-1"}
        self.manifest["baseline"]["document_ids"] = ["baseline", "module"]
        self.manifest["tasks"][0]["artifact_links"] = {"baseline": "baseline", "spec": "spec", "plan": "plan", "task": "task", "traceability": "trace"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0, result)
        self.assertTrue(result["required_checks_satisfied"])

    def test_unknown_linked_artifact_document_blocks_baseline(self):
        self.manifest["tasks"][0]["artifact_links"] = {"plan": "PLAN-MISSING"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("artifact link", json.dumps(result))

    def test_provisional_baseline_cannot_exempt_existing_project(self):
        for status in ("not_applicable", "partial"):
            with self.subTest(status=status):
                self.manifest["baseline"].update(status=status, origin="existing", reason="missing docs",
                                                 source_revision="fixture", scope="src", implementation_paths=["src"])
                proc,result=self.cli("--mode","baseline","--run-checks")
                self.assertEqual(proc.returncode,1, result)
                self.assertIn("origin=greenfield", json.dumps(result))

    def test_greenfield_no_implementation_claim_checks_files_despite_exclusion(self):
        self.manifest["baseline"].update(status="not_applicable", origin="greenfield", reason="new project",
                                         source_revision="fixture", scope="src", implementation_paths=["src"])
        self.manifest["exclude_paths"].append("src")
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1, result)
        self.assertIn("implementation exists", json.dumps(result))

    def test_greenfield_partial_blocks_handoff_and_completed_task(self):
        self.manifest["workflow"] = {"active_task": "TASK-1"}
        self.manifest["baseline"].update(status="partial", origin="greenfield", reason="first slice in progress",
                                         source_revision="fixture", scope="src", implementation_paths=["src"])
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1, result)
        self.assertIn("completed task", json.dumps(result))
        self.manifest["tasks"][0]["status"] = "in_progress"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0, result)
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1, result)
        self.assertIn("handoff requires", json.dumps(result))

    def test_provisional_baseline_requires_reason_revision_scope_and_safe_paths(self):
        self.manifest["tasks"][0]["status"] = "in_progress"
        self.manifest["baseline"].update(status="partial", origin="greenfield", implementation_paths=["src"])
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1, result)
        self.assertIn("missing reason", json.dumps(result))
        for paths in ([], ["."], ["../outside"], ["src/*"]):
            with self.subTest(paths=paths):
                self.manifest["baseline"]["implementation_paths"] = paths
                proc,result=self.cli("--mode","baseline","--run-checks")
                self.assertEqual(proc.returncode,2, result)

    def test_active_artifact_missing_optional_file_is_rejected(self):
        self.manifest["documents"].append({"id":"plan", "path":"docs/missing-plan.md", "kind":"technical-plan", "required":False})
        self.manifest["workflow"] = {"active_task":"TASK-1", "active_plan":"plan"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1, result)
        self.assertIn("active_plan references missing", json.dumps(result))

    def test_report_uses_repository_version_file(self):
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)
        self.assertEqual(result["tool_version"], (SCRIPTS.parent / "VERSION").read_text(encoding="utf-8").strip())

    def test_manifest_backslash_paths_are_portable(self):
        self.manifest["documents"][0]["path"] = "docs\\spec.md"
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

    if os.name == "nt":
        def test_safe_path_accepts_existing_short_alias_inside_project(self):
            root = self.root / "project root with spaces"
            target = root / "docs" / "spec.md"
            target.parent.mkdir(parents=True)
            target.write_text("spec", encoding="utf-8")
            buffer = ctypes.create_unicode_buffer(32768)
            get_short = ctypes.windll.kernel32.GetShortPathNameW
            get_short.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint)
            get_short.restype = ctypes.c_uint
            written = get_short(str(root), buffer, len(buffer))
            self.assertGreater(written, 0)
            alias = Path(buffer.value)
            if alias == root:
                self.skipTest("This volume does not generate a short-path alias for the fixture")

            self.assertEqual(checker.safe_path(root, alias / "docs" / "spec.md"), target.resolve())
            with self.assertRaisesRegex(checker.ConfigError, "path escapes project root"):
                checker.safe_path(root, alias.parent / "outside.txt")

        def test_relative_to_root_accepts_extended_and_short_source_path(self):
            root = checker.safe_root(self.root)
            source = root / "source with spaces" / "module.ts"
            source.parent.mkdir(parents=True)
            source.write_text("export const value = 1;", encoding="utf-8")
            extended = Path(chr(92) + chr(92) + "?" + chr(92) + str(source))
            self.assertEqual(checker._relative_to_root(extended, root), Path("source with spaces") / "module.ts")

    def test_foreign_drive_and_unc_paths_are_rejected(self):
        for raw in ("C:/outside/spec.md", "//server/share/spec.md"):
            with self.subTest(raw=raw):
                with self.assertRaises(checker.ConfigError):
                    checker.safe_path(self.root, raw)
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

    def test_nul_in_declared_command_is_structured_configuration_error(self):
        self.manifest["checks"][0]["command"] = [
            sys.executable, "-c", "open('nul-marker.txt','w').write('ran')", "bad\x00arg"
        ]
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 2, result)
        self.assertEqual(proc.stderr, "")
        self.assertIn("NUL", json.dumps(result))
        self.assertNotIn("Traceback", proc.stdout)
        self.assertFalse((self.root / "nul-marker.txt").exists())

    def test_check_output_over_limit_is_terminated_without_raw_output(self):
        limit = checker.MAX_CHECK_OUTPUT_BYTES
        self.manifest["checks"][0]["command"] = [
            sys.executable, "-c",
            "import sys; chunk='x'*65536; [sys.stdout.write(chunk) or sys.stdout.flush() for _ in iter(int, 1)]"
        ]
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        check = next(item for item in result["checks"] if item["rule_id"] == "unit")
        self.assertEqual(check["status"], "fail")
        self.assertTrue(check["evidence"]["output_limit_exceeded"])
        self.assertEqual(check["evidence"]["output_limit_bytes"], limit)
        self.assertGreater(check["evidence"]["output_bytes"], limit)
        self.assertNotIn("xxxxxxxx", json.dumps(result))

    def test_stderr_is_bounded_with_stdout_capture(self):
        limit = checker.MAX_CHECK_OUTPUT_BYTES
        self.manifest["checks"][0]["command"] = [
            sys.executable, "-c",
            "import sys; chunk='e'*65536; [sys.stderr.write(chunk) or sys.stderr.flush() for _ in iter(int, 1)]"
        ]
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        check = next(item for item in result["checks"] if item["rule_id"] == "unit")
        self.assertEqual(check["status"], "fail")
        self.assertTrue(check["evidence"]["output_limit_exceeded"])
        self.assertGreater(check["evidence"]["output_bytes"], limit)
        self.assertNotIn("eeeeeeee", json.dumps(result))

    def test_check_timeout_is_structured_and_does_not_traceback(self):
        self.manifest["checks"][0]["timeout_seconds"] = 0.2
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "import time; time.sleep(2)"]
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        check = next(item for item in result["checks"] if item["rule_id"] == "unit")
        self.assertEqual(check["status"], "fail")
        self.assertTrue(check["evidence"]["timed_out"])
        self.assertNotIn("Traceback", proc.stdout)
    def test_test_skip_summary_is_partial(self):
        self.manifest["checks"][0]["command"]=[sys.executable,"-c","print('OK (skipped=1)')"]
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("partial",[x["status"] for x in result["checks"]])

    def test_repository_manifest_protects_release_metadata(self):
        manifest = json.loads((SCRIPTS.parent / "engineering-manifest.json").read_text(encoding="utf-8"))
        protected = manifest["control_plane"]["protected_paths"]
        self.assertIn("VERSION", protected)
        self.assertIn("CHANGELOG.md", protected)
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
    def test_manual_inventory_can_pass_with_declared_scope_limitation(self):
        self.source["provenance"]["type"]="manual"
        self.source["provenance"]["evidence"]="docs/db.md"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0,result)
        inventory=next(x for x in result["checks"] if x["rule_id"]=="inventory:db")
        self.assertEqual(inventory["status"],"pass")
        self.assertIn("does not prove there are no omissions",inventory["limitations"][0])
    def test_manual_inventory_without_locatable_source_cannot_pass(self):
        self.source["provenance"]["type"]="manual"
        self.source["provenance"]["source_files"]=[]
        self.source["provenance"]["evidence"]="missing/evidence.md"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1,result)
        inventory=next(x for x in result["checks"] if x["rule_id"]=="inventory:db")
        self.assertEqual(inventory["status"],"fail")
        self.assertIn("evidence path",json.dumps(inventory))
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
    def test_after_dependency_never_blocks_started_task(self):
        previous=copy.deepcopy(self.manifest["tasks"][0]);previous["id"]="TASK-0";previous["status"]="planned";previous["depends_on"]=[]
        self.manifest["tasks"].append(previous)
        self.manifest["tasks"][0]["after"]=["TASK-0"]
        proc,result=self.cli("--mode","handoff","--task","TASK-1","--run-checks")
        gate=next(item for item in result["checks"] if item["rule_id"]=="task-gate")
        self.assertEqual(gate["status"],"pass")
    def test_read_only_task_does_not_require_implementation_approval(self):
        self.manifest["workflow"]={"stage":"implementation","active_task":"TASK-1"}
        self.manifest["tasks"][0]["implementation_task"]=False
        self.manifest["tasks"][0]["approval"]={"status":"pending"}
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        gate=next(item for item in result["checks"] if item["rule_id"]=="task-gate")
        self.assertEqual(gate["status"],"pass")
    def test_read_only_discovery_task_in_global_implementation_stage_is_not_gated(self):
        self.manifest["workflow"]={
            "active_task":"TASK-1","stage":"implementation","implementation_paths":["src"],
            "baseline_review":{"status":"pending","evidence":None},
            "proposal_approval":{"status":"pending","evidence":None},
        }
        self.manifest["baseline"].update(status="partial",origin="existing",reason="diagnosis",source_revision="fixture",scope="src",implementation_paths=["src"])
        self.manifest["tasks"][0]["implementation_task"]=False
        self.manifest["tasks"][0]["implementation_authorization"]={"status":"pending","task_id":"TASK-1"}
        self.manifest["tasks"][0]["approval_required"]=False
        self.manifest["tasks"][0]["status"]="in_progress"
        self.write()
        results,_,_,_,_=checker.validate(self.root,self.manifest,"change","TASK-1")
        life=next(x for x in results if x["rule_id"]=="workflow-lifecycle")
        self.assertEqual(life["status"],"pass")
    def test_temporary_untracked_file_is_reported_but_nonblocking(self):
        (self.root/"src"/"preview.tmp").write_text("temporary",encoding="utf-8")
        paths,check=checker.change_check(self.root,self.manifest,{d["id"]:d for d in self.manifest["documents"]},{m["id"]:m for m in self.manifest["modules"]},{t["id"]:t for t in self.manifest["tasks"]},"TASK-1",paths=["src/preview.tmp"])
        self.assertEqual(check["status"],"pass")
        self.assertEqual(check["evidence"]["temporary_nonblocking"],["src/preview.tmp"])
    def test_change_scope_automatically_upscales_declared_hotfix(self):
        self.manifest["tasks"][0]["scale"]="hotfix"
        self.manifest["tasks"][0]["module_ids"]=["core"]
        (self.root/"other").mkdir()
        self.manifest["modules"].append({"id":"web","source_paths":["other"],"document":"module","depends_on":[],"allowed_dependencies":[]})
        paths,check=checker.change_check(self.root,self.manifest,{d["id"]:d for d in self.manifest["documents"]},{m["id"]:m for m in self.manifest["modules"]},{t["id"]:t for t in self.manifest["tasks"]},"TASK-1",paths=["src/app.py","other/app.ts"])
        self.assertEqual(check["evidence"]["task_scale"]["declared"],"hotfix")
        self.assertEqual(check["evidence"]["task_scale"]["effective"],"feature")
        self.assertTrue(check["evidence"]["task_scale"]["inference_reasons"])
    def test_cross_module_auto_upscale_keeps_feature_applies_to_gate(self):
        self.manifest["workflow"]={"active_task":"TASK-1","policy_version":"delta-v1"}
        self.manifest["tasks"][0].update(scale="hotfix",required_checks=[])
        self.manifest["checks"][0]["required"]=False
        self.manifest["checks"][0]["applies_to"]=["feature","takeover"]
        (self.root/"other").mkdir(exist_ok=True)
        (self.root/"other/app.ts").write_text("export const x = 1",encoding="utf-8")
        self.manifest["modules"].append({"id":"web","source_paths":["other"],"document":"module","depends_on":[],"allowed_dependencies":[]})
        self.write()
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        scope=next(x for x in result["checks"] if x["rule_id"]=="change-scope")
        check=next(x for x in result["checks"] if x["rule_id"]=="unit")
        self.assertEqual(scope["evidence"]["task_scale"]["effective"],"feature")
        self.assertEqual(check["status"],"pass")
    def test_new_task_fields_require_declared_scale_and_compatibility(self):
        self.manifest["workflow"]={"policy_version":"delta-v1","active_task":"TASK-1"}
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,1)
        self.assertIn("scale",json.dumps(result))
        self.manifest["tasks"][0]["scale"]="minor"
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0,result)
    def test_check_applies_to_skips_only_nonapplicable_nonforced_gate(self):
        self.manifest["workflow"]={"active_task":"TASK-1","policy_version":"delta-v1"}
        task=self.manifest["tasks"][0];task["scale"]="hotfix"
        task["required_checks"]=[]
        self.manifest["checks"][0]["required"]=False
        self.manifest["checks"][0]["applies_to"]=["feature","takeover"]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0,result)
        check=next(x for x in result["checks"] if x["rule_id"]=="unit")
        self.assertEqual(check["status"],"skipped")
        self.assertFalse(check["required"])
        task["required_checks"]=["unit"]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0,result)
        check=next(x for x in result["checks"] if x["rule_id"]=="unit")
        self.assertEqual(check["status"],"pass")
        self.manifest["checks"][0]["required"]=True
        task["required_checks"]=[]
        proc,result=self.cli("--mode","baseline","--run-checks")
        self.assertEqual(proc.returncode,0,result)
        check=next(x for x in result["checks"] if x["rule_id"]=="unit")
        self.assertEqual(check["status"],"pass")
    def test_structured_artifact_dependency_blocks_only_missing_consumer_artifact(self):
        source=copy.deepcopy(self.manifest["tasks"][0]);source.update(id="TASK-0",status="planned",module_ids=["core"],depends_on=[])
        self.manifest["tasks"].append(source)
        consumer=self.manifest["tasks"][0]
        consumer.update(scale="feature",depends_on=[{"task_id":"TASK-0","artifact_path":"src/schema.sql"}])
        self.manifest["workflow"]={"policy_version":"delta-v1","active_task":"TASK-1"}
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        gate=next(x for x in result["checks"] if x["rule_id"]=="task-gate")
        self.assertEqual(gate["status"],"fail")
        (self.root/"src/schema.sql").write_text("CREATE TABLE x(id int);",encoding="utf-8")
        proc,result=self.cli("--mode","change","--task","TASK-1","--base","HEAD","--run-checks")
        gate=next(x for x in result["checks"] if x["rule_id"]=="task-gate")
        self.assertEqual(gate["status"],"pass")
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

    def test_glob_exclusion_prunes_nested_dependency_links(self):
        excluded = self.root / "src/packages/a/node_modules"
        excluded.mkdir(parents=True)
        link = excluded / "workspace-package"
        link.write_text("placeholder")
        self.manifest["exclude_paths"].append("**/node_modules")
        with mock.patch.object(Path, "is_symlink", autospec=True, side_effect=lambda path: path == link):
            proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

    def test_glob_root_exclusion_is_rejected(self):
        self.manifest["exclude_paths"].append("**")
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 2)
        self.assertIn("project root", json.dumps(result))

    def test_glob_segments_do_not_cross_directories(self):
        self.assertTrue(checker.glob_segments_match("src/a/node_modules", ("src", "*", "node_modules")))
        self.assertFalse(checker.glob_segments_match("src/a/b/node_modules", ("src", "*", "node_modules")))
        self.assertTrue(checker.glob_segments_match("src/a/b/node_modules", ("**", "node_modules")))

    def test_common_parent_for_two_modules_is_valid_trigger_scope(self):
        for path in ("packages/api/api.py", "packages/web/web.py"):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("content", encoding="utf-8")
        self.manifest["modules"][0]["source_paths"] = ["packages/api"]
        self.manifest["modules"].append({"id": "web", "source_paths": ["packages/web"], "document": "module", "depends_on": [], "allowed_dependencies": []})
        self.manifest["tasks"][0]["module_ids"] = ["core", "web"]
        self.manifest["tasks"][0]["documentation_impact"] = {"module-connectivity": {"when_paths": ["packages"], "document_ids": ["impact"]}}
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

    def test_common_parent_for_one_module_is_rejected(self):
        self.manifest["modules"][0]["source_paths"] = ["packages/api"]
        (self.root / "packages/api").mkdir(parents=True, exist_ok=True)
        self.manifest["tasks"][0]["documentation_impact"] = {"module-connectivity": {"when_paths": ["packages"], "document_ids": ["impact"]}}
        proc, result = self.cli("--mode", "baseline", "--run-checks")
        self.assertEqual(proc.returncode, 1)
        self.assertIn("outside module/document scopes", json.dumps(result))

    def test_documentation_trigger_glob_and_project_root_are_rejected(self):
        for when_path in ("src/*", "."):
            with self.subTest(when_path=when_path):
                self.manifest["tasks"][0]["documentation_impact"] = {"module-connectivity": {"when_paths": [when_path], "document_ids": ["impact"]}}
                proc, result = self.cli("--mode", "baseline", "--run-checks")
                self.assertIn(proc.returncode, (1, 2))
                self.assertIn("when_paths", json.dumps(result))

    @unittest.skipUnless(shutil.which("git"), "Git unavailable")
    def test_common_parent_trigger_does_not_expand_change_coverage(self):
        for path in ("packages/api/api.py", "packages/web/web.py"):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text("content", encoding="utf-8")
        self.manifest["modules"][0]["source_paths"] = ["packages/api"]
        self.manifest["modules"].append({"id": "web", "source_paths": ["packages/web"], "document": "module", "depends_on": [], "allowed_dependencies": []})
        self.manifest["tasks"][0]["module_ids"] = ["core", "web"]
        self.manifest["tasks"][0]["documentation_impact"] = {"module-connectivity": {"when_paths": ["packages"], "document_ids": ["impact"]}}
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "two module baseline")
        (self.root / "packages/other").mkdir(parents=True, exist_ok=True)
        (self.root / "packages/other/other.py").write_text("changed", encoding="utf-8")
        proc, result = self.cli("--mode", "change", "--task", "TASK-1", "--base", "HEAD", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        scope = next(item for item in result["checks"] if item["rule_id"] == "change-scope")
        self.assertIn("packages/other/other.py", scope["evidence"]["uncovered"])
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
        scope=next(item for item in result["checks"] if item["rule_id"]=="change-scope")
        self.assertTrue(scope["evidence"]["findings"])
        self.assertIn("action",scope["evidence"]["findings"][0])
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
    def test_current_report_replaces_only_the_exact_work_slot(self):
        report=checker.write_report(self.root,"work/TASK-1-baseline-current.json",{"version":1},"TASK-1","baseline")
        self.assertEqual(json.loads(report.read_text(encoding="utf-8")),{"version":1})
        checker.write_report(self.root,"work/TASK-1-baseline-current.json",{"version":2},"TASK-1","baseline")
        self.assertEqual(json.loads(report.read_text(encoding="utf-8")),{"version":2})
        rerun=self.root/"work/TASK-1-baseline-rerun2.json"
        checker.write_report(self.root,"work/TASK-1-baseline-rerun2.json",{"version":3},"TASK-1","baseline")
        self.assertEqual(json.loads(rerun.read_text(encoding="utf-8")),{"version":3})
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
    def test_release_metadata_control_plane_paths_require_approval(self):
        self.manifest["control_plane"] = {
            "protected_paths": ["manifest.json", "VERSION", "CHANGELOG.md"],
            "approval_env": "TEST_CONTROL_PLANE_APPROVED",
        }
        self.manifest["tasks"][0]["documentation_impact"] = {
            "implementation-only": {"when_paths": ["src"], "document_ids": ["impact"]},
            "release-metadata": {"when_paths": ["VERSION", "CHANGELOG.md"], "document_ids": ["impact"]},
        }
        self.manifest["modules"][0]["source_paths"].extend(["VERSION", "CHANGELOG.md"])
        (self.root / "VERSION").write_text("1.0.0\n", encoding="utf-8")
        (self.root / "CHANGELOG.md").write_text("initial\n", encoding="utf-8")
        self.manifest["checks"][0]["command"] = [sys.executable, "-c", "open('command-ran.txt','w').write('ran')"]
        self.write()
        self.git("add", ".")
        self.git("-c", "user.name=Test", "-c", "user.email=test@example.invalid", "commit", "-m", "release baseline")

        (self.root / "VERSION").write_text("1.1.0\n", encoding="utf-8")
        (self.root / "docs/impact.md").write_text("release metadata reviewed\n", encoding="utf-8")
        self.git("add", "VERSION", "docs/impact.md")
        proc, result = self.cli("--mode", "commit", "--task", "TASK-1", "--run-checks")
        self.assertEqual(proc.returncode, 1, result)
        control = next(check for check in result["checks"] if check["rule_id"] == "control-plane")
        self.assertEqual(control["status"], "fail")
        self.assertIn("VERSION", control["evidence"]["changed_paths"])
        self.assertFalse((self.root / "command-ran.txt").exists())

        with mock.patch.dict(os.environ, {"TEST_CONTROL_PLANE_APPROVED": "1"}, clear=False):
            proc, result = self.cli("--mode", "commit", "--task", "TASK-1",
                                    "--allow-control-plane-change", "--run-checks")
        self.assertEqual(proc.returncode, 0, result)

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

