#!/usr/bin/env python3
"""Create a reviewable engineering-workflow manifest skeleton."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
from pathlib import Path
import sys


DOCS = [
    ("SPEC", "docs/spec.md", "spec"),
    ("MAP", "docs/module-map.md", "module-map"),
    ("DB", "docs/database.md", "database-dictionary"),
    ("CONTRACT", "docs/contracts.md", "contract"),
    ("FLOW", "docs/business-flow.md", "business-flow"),
    ("IMPACT", "planning/change-impact.md", "impact"),
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


def manifest(root: Path, profile: str) -> dict:
    sources = source_paths(root)
    required = {"SPEC", "MAP", "IMPACT"} if profile == "lite" else {ident for ident, _, _ in DOCS}
    documents = [{"id": ident, "path": path, "kind": kind, "required": ident in required} for ident, path, kind in DOCS]
    modules = []
    for index, path in enumerate(sources):
        ident = "project" if path == "." else path.replace("/", "-")
        modules.append({"id": ident, "source_paths": [path], "document": "MAP", "depends_on": [], "allowed_dependencies": []})
    if profile == "lite":
        inventories = []
        impact = {"implementation-only": {"when_paths": sources, "document_ids": ["IMPACT"]}}
    else:
        inventories = [
            {"id": "schema", "kind": "database", "path": "planning/database-inventory.json", "documentation": "planning/database-doc-mapping.json", "required": False},
            {"id": "routes", "kind": "contract", "path": "planning/contract-inventory.json", "documentation": "planning/contract-doc-mapping.json", "required": False},
        ]
        impact = {"module-connectivity": {"when_paths": sources, "document_ids": ["MAP", "FLOW", "CONTRACT"]}, "database": {"when_paths": ["migrations", "backend/db"], "document_ids": ["DB", "FLOW"]}}
    return {
        "schema_version": 1,
        "workflow": {"active_task": "TASK-01"},
        "documents": documents,
        "requirements": [{"id": "REQ-BOOTSTRAP-01", "document": "SPEC"}],
        "acceptance": [{"id": "AT-BOOTSTRAP-01", "document": "SPEC"}],
        "modules": modules,
        "inventories": inventories,
        "checks": [{"id": "TEST", "command": ["python", "-m", "unittest", "discover", "-q"], "required": True, "timeout_seconds": 120}],
        "tasks": [{
            "id": "TASK-01", "requirement_ids": ["REQ-BOOTSTRAP-01"], "acceptance_ids": ["AT-BOOTSTRAP-01"],
            "module_ids": [item["id"] for item in modules], "depends_on": [], "status": "planned", "impact_document": "IMPACT",
            "required_checks": ["TEST"], "approval_required": True, "approval": {"status": "pending", "evidence": "planning/approval.md"},
            "skill_review": {"catalog_source": "record host catalog here", "scope": "record task deliverables here", "checked_at": datetime.now(timezone.utc).isoformat(), "candidates": [], "recheck": "record scope changes here"},
            "documentation_impact": impact,
        }],
        "baseline": {"status": "planned", "evidence": "planning/baseline-review.md"},
        "exclude_paths": [".git", "node_modules", "build", "dist", "work", "__pycache__"],
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--output", default="engineering-manifest.json")
    parser.add_argument("--profile", choices=("full", "lite"), default="full")
    parser.add_argument("--force", action="store_true", help="replace an existing output file")
    args = parser.parse_args(argv)
    try:
        root = project_root(args.root)
        output = (root / args.output).resolve()
        if not output.is_relative_to(root):
            raise ValueError("--output must remain inside --root")
        if output.exists() and not args.force:
            raise ValueError("output exists; use --force only after reviewing it")
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(json.dumps(manifest(root, args.profile), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"created {output.relative_to(root).as_posix()} ({args.profile} profile)")
        print("complete the planned baseline, requirements, skill_review and approval before using handoff/commit gates")
        return 0
    except (OSError, ValueError) as exc:
        print(f"init_manifest: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
