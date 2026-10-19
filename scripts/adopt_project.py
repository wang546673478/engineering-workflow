#!/usr/bin/env python3
"""Create a reviewable engineering-workflow adoption scaffold without overwriting project state."""
from __future__ import annotations

import argparse
from contextlib import redirect_stdout
from datetime import datetime, timezone
import io
import json
import os
from pathlib import Path
import sys
import tempfile

import check_project
import init_manifest
import install_agents_guidance


def bootstrap_check(root, manifest_path, data):
    """Inspect declarations with the bundled checker; never execute project commands."""
    stage = data.get("workflow", {}).get("stage")
    mode = "discovery" if stage in check_project.EARLY_WORKFLOW_STAGES else "baseline"
    output = io.StringIO()
    with redirect_stdout(output):
        code = check_project.main([
            "--root", str(root), "--manifest", str(manifest_path), "--mode", mode,
            "--task", data["workflow"]["active_task"],
        ])
    return {"exit_code": code, "checker_source": str(Path(check_project.__file__).resolve()),
            "report": json.loads(output.getvalue())}


def replace_manifest(path, data, original):
    """Keep the prior JSON intact if staging fails or another writer changed it."""
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", newline="\n",
                                         dir=path.parent, prefix=path.name + ".", delete=False) as output:
            temporary = Path(output.name)
            output.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
            output.flush()
            os.fsync(output.fileno())
        if path.read_bytes() != original:
            raise ValueError("manifest changed during adoption; concurrent update preserved")
        os.replace(temporary, path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def adoption_manifest(root, args, output):
    source_scopes = args.implementation_path or None
    data = init_manifest.manifest(
        root, args.profile, args.project_kind, source_scopes,
        output.relative_to(root).as_posix(), args.state_dir,
        args.skill_source, args.skill_version, args.checker_source,
        args.task_id, args.document,
    )
    data["adoption"].update(status="initialized_incomplete", checked_at=datetime.now(timezone.utc).astimezone().isoformat())
    return data


def legacy_implementation_scopes(manifest, args):
    if args.implementation_path:
        return list(dict.fromkeys(args.implementation_path))
    scopes = []
    for module in manifest.get("modules", []):
        if not isinstance(module, dict) or module.get("id") in {"governance", "workflow-docs", "test", "tests"}:
            continue
        for raw in module.get("source_paths", []):
            if not isinstance(raw, str) or not raw.strip() or raw in (".", "docs", "planning"):
                continue
            if raw.startswith(("docs/", "planning/")):
                continue
            scopes.append(raw)
    return list(dict.fromkeys(scopes))


def upgrade_legacy_manifest(root, manifest, args, manifest_path):
    tasks = manifest.get("tasks")
    documents = manifest.get("documents")
    if not isinstance(tasks, list) or not tasks or not isinstance(documents, list):
        raise ValueError("legacy manifest is incomplete; no lifecycle fields were written")
    workflow = manifest.setdefault("workflow", {})
    if not isinstance(workflow, dict):
        raise ValueError("legacy workflow is not an object; no lifecycle fields were written")
    active_task = workflow.get("active_task")
    if not isinstance(active_task, str) or not any(isinstance(task, dict) and task.get("id") == active_task for task in tasks):
        active_task = next((task.get("id") for task in tasks if isinstance(task, dict) and isinstance(task.get("id"), str)), None)
        if not active_task:
            raise ValueError("legacy manifest has no task to select; no lifecycle fields were written")
        workflow["active_task"] = active_task
    scopes = legacy_implementation_scopes(manifest, args)
    if not scopes:
        raise ValueError("could not infer implementation scopes; pass --implementation-path explicitly")
    normalized_scopes = []
    for raw in scopes:
        path = check_project.safe_path(root, raw, file_only=False)
        if path == root or check_project.has_glob_magic(raw):
            raise ValueError("implementation scopes must be literal non-root paths: " + raw)
        normalized_scopes.append(path.relative_to(root).as_posix())
    workflow.setdefault("stage", "takeover_discovery")
    workflow.setdefault("implementation_paths", list(dict.fromkeys(normalized_scopes)))
    workflow.setdefault("baseline_review", {"status": "pending", "source_revision": None, "evidence": None})
    workflow.setdefault("proposal_approval", {"status": "pending", "revision": None, "evidence": None})
    selected_task = next(task for task in tasks if isinstance(task, dict) and task.get("id") == active_task)
    selected_task.setdefault("implementation_authorization", {
        "status": "pending", "plan_revision": None,
        "evidence": f"{args.state_dir}/approval.md", "task_id": active_task,
    })
    adoption = manifest.setdefault("adoption", {})
    if not isinstance(adoption, dict):
        raise ValueError("legacy adoption record is not an object; no lifecycle fields were written")
    adoption.update({
        "status": "legacy_manifest_upgraded",
        "skill_source": args.skill_source,
        "skill_version": args.skill_version,
        "checker_source": args.checker_source,
        "manifest_path": manifest_path.relative_to(root).as_posix(),
        "state_dir": args.state_dir,
        "checked_at": datetime.now(timezone.utc).astimezone().isoformat(),
    })
    return manifest


def preflight_guidance(root, args, manifest_path):
    return install_agents_guidance.prepare_targets(
        root, manifest_path.relative_to(root).as_posix(), args.state_dir,
        f"{args.skill_source} (version {args.skill_version})", args.file)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", default="engineering-manifest.json")
    parser.add_argument("--state-dir", default="planning")
    parser.add_argument("--profile", choices=("full", "lite"), default="full")
    parser.add_argument("--project-kind", choices=("existing", "greenfield"), default="existing")
    parser.add_argument("--implementation-path", action="append", default=[])
    parser.add_argument("--document", action="append", default=[], metavar="ID=PATH")
    parser.add_argument("--task-id", default="TASK-01")
    parser.add_argument("--upgrade-legacy-manifest", action="store_true",
                        help="add lifecycle fields to an existing manifest without replacing its documents, checks, tasks, or history")
    parser.add_argument("--skill-source", required=True)
    parser.add_argument("--skill-version", required=True)
    parser.add_argument("--checker-source", default=str(Path(__file__).resolve().parent / "check_project.py"))
    parser.add_argument("--file", action="append", default=[])
    args = parser.parse_args(argv)
    manifest_created = False
    try:
        root = install_agents_guidance.project_root(args.root)
        manifest_path = install_agents_guidance.safe_relative(root, args.manifest)
        if manifest_path.suffix.lower() != ".json":
            raise ValueError("--manifest must be a .json file")
        if not args.skill_source.strip() or not args.skill_version.strip():
            raise ValueError("record the actual loaded skill source and version")
        init_manifest.parse_document_overrides(args.document)
        install_agents_guidance.safe_relative(root, args.state_dir)
        if manifest_path.exists():
            install_agents_guidance.validate_manifest(root, args.manifest)
            original = manifest_path.read_bytes()
            existing = json.loads(original.decode("utf-8-sig"))
            if isinstance(existing.get("workflow"), dict) and existing["workflow"].get("stage"):
                adoption = existing.get("adoption")
                if not isinstance(adoption, dict) or any(adoption.get(key) != value for key, value in (
                        ("skill_source", args.skill_source), ("skill_version", args.skill_version),
                        ("checker_source", args.checker_source), ("state_dir", args.state_dir))):
                    raise ValueError("existing lifecycle manifest provenance differs; review the skill upgrade explicitly; manifest preserved")
                with redirect_stdout(io.StringIO()):
                    result = install_agents_guidance.main([
                        "--root", str(root), "--manifest", args.manifest,
                        "--state-dir", args.state_dir,
                        "--skill", f"{args.skill_source} (version {args.skill_version})",
                        *[part for raw in args.file for part in ("--file", raw)],
                    ])
                if result:
                    return result
                print(json.dumps({"status": "lifecycle_manifest_reused", "manifest": args.manifest,
                                  "stage": existing["workflow"]["stage"],
                                  "bootstrap": bootstrap_check(root, manifest_path, existing)}, ensure_ascii=False))
                return 0
            if not args.upgrade_legacy_manifest:
                raise ValueError("legacy manifest preserved; review it, then rerun with --upgrade-legacy-manifest for an additive lifecycle migration")
            preflight_guidance(root, args, manifest_path)
            upgraded = upgrade_legacy_manifest(root, existing, args, manifest_path)
            replace_manifest(manifest_path, upgraded, original)
            with redirect_stdout(io.StringIO()):
                result = install_agents_guidance.main([
                    "--root", str(root), "--manifest", args.manifest,
                    "--state-dir", args.state_dir,
                    "--skill", f"{args.skill_source} (version {args.skill_version})",
                    *[part for raw in args.file for part in ("--file", raw)],
                ])
            if result:
                print("manifest lifecycle fields were added but guidance installation failed; preserve and inspect the update", file=sys.stderr)
                return result
            print(json.dumps({"status": "legacy_manifest_upgraded", "manifest": args.manifest,
                              "stage": upgraded["workflow"]["stage"], "active_task": upgraded["workflow"]["active_task"],
                              "implementation_paths": upgraded["workflow"]["implementation_paths"],
                              "bootstrap": bootstrap_check(root, manifest_path, upgraded)}, ensure_ascii=False, indent=2))
            return 0

        preflight_guidance(root, args, manifest_path)
        data = adoption_manifest(root, args, manifest_path)
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        with manifest_path.open("x", encoding="utf-8", newline="\n") as output:
            output.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
        manifest_created = True

        with redirect_stdout(io.StringIO()):
            result = install_agents_guidance.main([
                "--root", str(root), "--manifest", args.manifest,
                "--state-dir", args.state_dir,
                "--skill", f"{args.skill_source} (version {args.skill_version})",
                *[part for raw in args.file for part in ("--file", raw)],
            ])
        if result:
            print("manifest created but guidance installation failed; see the error above", file=sys.stderr)
            return result
        print(json.dumps({
            "status": "initialized_incomplete",
            "manifest": args.manifest,
            "stage": data["workflow"]["stage"],
            "baseline_status": data["baseline"]["status"],
            "active_task": data["workflow"]["active_task"],
            "skill_source": args.skill_source,
            "skill_version": args.skill_version,
            "bootstrap": bootstrap_check(root, manifest_path, data),
            "next_step": "map or create the linked factual documents, run check_project.py --mode discovery, and keep implementation authorization pending",
        }, ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError) as exc:
        print("adopt_project: " + str(exc), file=sys.stderr)
        if manifest_created:
            print("the newly created manifest was preserved; no existing project file was overwritten", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
