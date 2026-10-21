#!/usr/bin/env python3
"""Create a reviewable engineering-workflow manifest skeleton."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import sys


DOCS = [
    ("BASELINE", "planning/baseline-review.md", "baseline"),
    ("SPEC", "docs/spec.md", "spec"),
    ("PLAN", "docs/plan.md", "technical-plan"),
    ("TASK", "planning/task.md", "task"),
    ("MAP", "docs/module-map.md", "module-map"),
    ("DB", "docs/database.md", "database-dictionary"),
    ("CONTRACT", "docs/contracts.md", "contract"),
    ("FLOW", "docs/business-flow.md", "business-flow"),
    ("IMPACT", "planning/change-impact.md", "impact"),
    ("TRACE", "planning/traceability.md", "traceability-index"),
]
SOURCE_CANDIDATES = ("src", "app", "backend", "frontend", "server", "client", "packages", "lib", "tests")
DOCUMENT_IDS = {item[0] for item in DOCS}


def project_root(raw: str) -> Path:
    path = Path(raw).absolute().resolve()
    if not path.is_dir():
        raise ValueError("--root must be an existing directory")
    return path


def source_paths(root: Path) -> list[str]:
    found = [name for name in SOURCE_CANDIDATES if (root / name).is_dir()]
    return found or ["."]


def parse_document_overrides(values):
    overrides = {}
    for raw in values or []:
        if "=" not in raw:
            raise ValueError("--document must use ID=project-relative-path")
        ident, path = raw.split("=", 1)
        if ident not in DOCUMENT_IDS or not path.strip():
            raise ValueError("--document has an unknown ID or empty path: " + raw)
        candidate = Path(path.replace("\\", "/"))
        if candidate.is_absolute() or ".." in candidate.parts or any(char in path for char in "\r\n\x00"):
            raise ValueError("--document path must remain project-relative: " + raw)
        if ident in overrides:
            raise ValueError("duplicate --document override: " + ident)
        overrides[ident] = candidate.as_posix()
    return overrides


def manifest(root: Path, profile: str, project_kind: str = "existing", implementation_paths=None,
             manifest_path: str = "engineering-manifest.json", state_dir: str = "planning",
             skill_source: str = "record actual skill source and version", skill_version: str = "not provided",
             checker_source: str = "scripts/check_project.py", task_id: str = "TASK-01",
             document_overrides=None, approval_enforcement="diagnostic") -> dict:
    # Direct library callers can supply Windows short-name or lexical aliases,
    # just like the CLI. Compare scopes against the same canonical root.
    root = project_root(root)
    if approval_enforcement not in ("diagnostic", "strict"):
        raise ValueError("approval enforcement must be diagnostic or strict")
    if not state_dir.strip() or Path(state_dir).is_absolute() or Path(state_dir) == Path(".") or ".." in Path(state_dir).parts:
        raise ValueError("--state-dir must be a project-relative path")
    state_dir = Path(state_dir.replace("\\", "/")).as_posix().strip("/") or "."
    overrides = parse_document_overrides(document_overrides)
    state_documents = {"BASELINE": "baseline-review.md", "TASK": "task.md", "IMPACT": "change-impact.md", "TRACE": "traceability.md"}
    docs = [(ident, overrides.get(ident, f"{state_dir}/{state_documents[ident]}" if ident in state_documents and state_dir != "." else (state_documents[ident] if ident in state_documents else path)), kind)
            for ident, path, kind in DOCS]
    sources = implementation_paths or (["src", "tests"] if project_kind == "greenfield" else source_paths(root))
    # A root scope cannot be used as a documentation-impact trigger. Fall back
    # to the actual top-level files/directories for an existing flat project.
    if sources == ["."]:
        sources = sorted(path.name for path in root.iterdir()
                         if path.name not in {".git", "docs", "planning", "work", "node_modules", "__pycache__"})
    sources = list(dict.fromkeys(sources))
    if not sources:
        raise ValueError("no source paths found; use --project-kind greenfield for a project without implementation")
    for raw in sources:
        path = root / raw
        if not path.resolve().is_relative_to(root):
            raise ValueError("implementation paths must remain inside --root")
        if path.resolve() == root or raw in (".", "") or any(char in raw for char in "*?[") or ".." in Path(raw).parts:
            raise ValueError("implementation paths must be literal non-root paths")
    if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", task_id):
        raise ValueError("--task-id must be a valid manifest identifier")
    implementation_scopes = list(implementation_paths or [path for path in sources if Path(path).name.casefold() not in {"test", "tests", "docs", "planning"}])
    if not implementation_scopes:
        implementation_scopes = list(sources)
    # Every linked view is required in both profiles. Lite omits inventories
    # and uses an impact record; it does not silently waive linked documents.
    required = {ident for ident, _, _ in DOCS}
    documents = [{"id": ident, "path": path, "kind": kind, "required": ident in required} for ident, path, kind in docs]
    modules = []
    for path in sources:
        ident = "project" if path == "." else path.replace("/", "-")
        if ident == "workflow-docs":
            ident += "-source"
        modules.append({"id": ident, "source_paths": [path], "document": "MAP", "depends_on": [], "allowed_dependencies": []})
    governance_paths = list(dict.fromkeys(["docs", state_dir, manifest_path]))
    modules.append({"id": "workflow-docs", "source_paths": governance_paths, "document": "MAP", "depends_on": [], "allowed_dependencies": []})
    if profile == "lite":
        inventories = []
        impact = {"implementation-progress": {"when_paths": sources, "document_ids": ["BASELINE", "IMPACT"]}}
    else:
        inventories = [
            {"id": "schema", "kind": "database", "path": f"{state_dir}/database-inventory.json", "documentation": f"{state_dir}/database-doc-mapping.json", "required": False},
            {"id": "routes", "kind": "contract", "path": f"{state_dir}/contract-inventory.json", "documentation": f"{state_dir}/contract-doc-mapping.json", "required": False},
        ]
        impact = {"module-connectivity": {"when_paths": sources, "document_ids": ["BASELINE", "MAP", "FLOW", "CONTRACT", "DB"]}}
    impact["workflow-records"] = {"when_paths": governance_paths, "document_ids": ["IMPACT"]}
    baseline = {"status": "planned", "origin": project_kind, "evidence": next(item["path"] for item in documents if item["id"] == "BASELINE"), "document_ids": ["BASELINE", "MAP", "DB", "CONTRACT", "FLOW"], "source_revision": "record-before-review", "scope": "record reviewed modules and limits"}
    if project_kind == "greenfield":
        baseline.update({"reason": "record no-implementation evidence before selecting not_applicable", "implementation_paths": sources})
    else:
        baseline.update({"reason": "existing code requires global discovery; no baseline completion or approval is inferred"})
    return {
        "schema_version": 1,
        "workflow": {
            "active_baseline": "BASELINE", "active_spec": "SPEC", "active_plan": "PLAN", "active_task": task_id,
            "stage": "takeover_discovery", "implementation_paths": implementation_scopes,
            "baseline_review": {"status": "pending", "source_revision": None, "evidence": None},
            "proposal_approval": {"status": "pending", "revision": None, "evidence": None},
            "approval_policy": {"record_contract": 1, "enforcement": approval_enforcement,
                                "sequence_enforcement": "diagnostic", "minimum_checker_version": "1.8.0"},
        },
        "adoption": {
            "status": "initialized_incomplete", "skill_source": skill_source, "skill_version": skill_version,
            "checker_source": checker_source,
            "manifest_path": manifest_path, "state_dir": state_dir,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        },
        "documents": documents,
        "requirements": [{"id": "REQ-BOOTSTRAP-01", "document": "SPEC", "index": "TRACE"}],
        "acceptance": [{"id": "AT-BOOTSTRAP-01", "document": "SPEC", "index": "TRACE"}],
        "modules": modules,
        "inventories": inventories,
        "checks": [{"id": "TEST", "command": ["python", "-m", "unittest", "discover", "-q"], "required": True, "timeout_seconds": 120}],
        "tasks": [{
            "id": task_id, "batch_id": task_id + "-BATCH-01", "requirement_ids": ["REQ-BOOTSTRAP-01"], "acceptance_ids": ["AT-BOOTSTRAP-01"],
            "module_ids": [item["id"] for item in modules], "depends_on": [], "status": "planned", "impact_document": "IMPACT",
            "required_checks": ["TEST"], "approval_required": True, "approval": {"status": "pending", "evidence": f"{state_dir}/approval.md"},
            "implementation_authorization": {"status": "pending", "plan_revision": None, "evidence": f"{state_dir}/approval.md", "task_id": task_id},
            "artifact_links": {"baseline": "BASELINE", "spec": "SPEC", "plan": "PLAN", "task": "TASK", "traceability": "TRACE"},
            "skill_review": {"catalog_source": "record host catalog here", "scope": "record task deliverables here", "checked_at": datetime.now(timezone.utc).isoformat(), "candidates": [], "recheck": "record scope changes here"},
            "documentation_impact": impact,
        }],
        "baseline": baseline,
        "exclude_paths": [".git", "**/node_modules", "build", "dist", "work", "__pycache__"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", "--manifest", dest="output", default="engineering-manifest.json")
    parser.add_argument("--state-dir", default="planning")
    parser.add_argument("--skill-source", default="record actual skill source and version")
    parser.add_argument("--skill-version", default="not provided")
    parser.add_argument("--checker-source", default="scripts/check_project.py")
    parser.add_argument("--task-id", default="TASK-01")
    parser.add_argument("--document", action="append", default=[], help="override a linked document path as ID=path")
    parser.add_argument("--profile", choices=("full", "lite"), default="full")
    parser.add_argument("--project-kind", choices=("existing", "greenfield"), default="existing",
                        help="greenfield records a no-implementation entry path, not an approved baseline")
    parser.add_argument("--implementation-path", action="append",
                        help="greenfield implementation scope, repeatable; defaults to src and tests")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    parser.add_argument("--approval-enforcement", choices=("diagnostic", "strict"), default="diagnostic",
                        help="structured approval checks default to nonblocking diagnostics; strict must be explicit")
    args = parser.parse_args(argv)
    try:
        root = project_root(args.root)
        if args.implementation_path and args.project_kind != "greenfield":
            raise ValueError("--implementation-path requires --project-kind greenfield")
        output = (root / args.output).resolve()
        if not output.is_relative_to(root):
            raise ValueError("--output must remain inside --root")
        if output.exists() and not args.force:
            raise ValueError("output exists; use --force only after reviewing it")
        data = manifest(root, args.profile, args.project_kind, args.implementation_path,
                        output.relative_to(root).as_posix(), args.state_dir,
                        args.skill_source, args.skill_version, args.checker_source, args.task_id, args.document, args.approval_enforcement)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"created {output.relative_to(root).as_posix()} ({args.profile} profile)")
        print("review source scopes, create linked documents and replace the test command with the project's authoritative checks")
        print("baseline remains planned: investigate existing code or record greenfield evidence; delivery requires a factual complete baseline")
        return 0
    except (OSError, ValueError) as exc:
        print(f"init_manifest: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
