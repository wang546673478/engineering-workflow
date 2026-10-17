#!/usr/bin/env python3
"""Create a reviewable engineering-workflow manifest skeleton."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
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


def project_root(raw: str) -> Path:
    path = Path(raw).absolute().resolve()
    if not path.is_dir():
        raise ValueError("--root must be an existing directory")
    return path


def source_paths(root: Path) -> list[str]:
    found = [name for name in SOURCE_CANDIDATES if (root / name).is_dir()]
    return found or ["."]


def manifest(root: Path, profile: str, project_kind: str = "existing", implementation_paths=None,
             manifest_path: str = "engineering-manifest.json") -> dict:
    sources = source_paths(root)
    if project_kind == "greenfield":
        sources = implementation_paths or ["src", "tests"]
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
    # Every linked view is required in both profiles. Lite omits inventories
    # and uses an impact record; it does not silently waive linked documents.
    required = {ident for ident, _, _ in DOCS}
    documents = [{"id": ident, "path": path, "kind": kind, "required": ident in required} for ident, path, kind in DOCS]
    modules = []
    for path in sources:
        ident = "project" if path == "." else path.replace("/", "-")
        if ident == "workflow-docs":
            ident += "-source"
        modules.append({"id": ident, "source_paths": [path], "document": "MAP", "depends_on": [], "allowed_dependencies": []})
    governance_paths = list(dict.fromkeys(["docs", "planning", manifest_path]))
    modules.append({"id": "workflow-docs", "source_paths": governance_paths, "document": "MAP", "depends_on": [], "allowed_dependencies": []})
    if profile == "lite":
        inventories = []
        impact = {"implementation-progress": {"when_paths": sources, "document_ids": ["BASELINE", "IMPACT"]}}
    else:
        inventories = [
            {"id": "schema", "kind": "database", "path": "planning/database-inventory.json", "documentation": "planning/database-doc-mapping.json", "required": False},
            {"id": "routes", "kind": "contract", "path": "planning/contract-inventory.json", "documentation": "planning/contract-doc-mapping.json", "required": False},
        ]
        impact = {"module-connectivity": {"when_paths": sources, "document_ids": ["BASELINE", "MAP", "FLOW", "CONTRACT", "DB"]}}
    impact["workflow-records"] = {"when_paths": governance_paths, "document_ids": ["IMPACT"]}
    baseline = {"status": "planned", "origin": project_kind, "evidence": "planning/baseline-review.md", "document_ids": ["BASELINE", "MAP", "DB", "CONTRACT", "FLOW"], "source_revision": "record-before-review", "scope": "record reviewed modules and limits"}
    if project_kind == "greenfield":
        baseline.update({"reason": "record no-implementation evidence before selecting not_applicable", "implementation_paths": sources})
    return {
        "schema_version": 1,
        "workflow": {"active_baseline": "BASELINE", "active_spec": "SPEC", "active_plan": "PLAN", "active_task": "TASK-01"},
        "documents": documents,
        "requirements": [{"id": "REQ-BOOTSTRAP-01", "document": "SPEC", "index": "TRACE"}],
        "acceptance": [{"id": "AT-BOOTSTRAP-01", "document": "SPEC", "index": "TRACE"}],
        "modules": modules,
        "inventories": inventories,
        "checks": [{"id": "TEST", "command": ["python", "-m", "unittest", "discover", "-q"], "required": True, "timeout_seconds": 120}],
        "tasks": [{
            "id": "TASK-01", "requirement_ids": ["REQ-BOOTSTRAP-01"], "acceptance_ids": ["AT-BOOTSTRAP-01"],
            "module_ids": [item["id"] for item in modules], "depends_on": [], "status": "planned", "impact_document": "IMPACT",
            "required_checks": ["TEST"], "approval_required": True, "approval": {"status": "pending", "evidence": "planning/approval.md"},
            "artifact_links": {"baseline": "BASELINE", "spec": "SPEC", "plan": "PLAN", "task": "TASK", "traceability": "TRACE"},
            "skill_review": {"catalog_source": "record host catalog here", "scope": "record task deliverables here", "checked_at": datetime.now(timezone.utc).isoformat(), "candidates": [], "recheck": "record scope changes here"},
            "documentation_impact": impact,
        }],
        "baseline": baseline,
        "exclude_paths": [".git", "node_modules", "build", "dist", "work", "__pycache__"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="engineering-manifest.json")
    parser.add_argument("--profile", choices=("full", "lite"), default="full")
    parser.add_argument("--project-kind", choices=("existing", "greenfield"), default="existing",
                        help="greenfield records a no-implementation entry path, not an approved baseline")
    parser.add_argument("--implementation-path", action="append",
                        help="greenfield implementation scope, repeatable; defaults to src and tests")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
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
                        output.relative_to(root).as_posix())
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
