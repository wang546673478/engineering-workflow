#!/usr/bin/env python3
"""Read-only manifest checks; declared commands run only with --run-checks."""
from __future__ import annotations
import argparse
from datetime import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import urlparse

VERSION = "1.3"
STATES = {"pass", "fail", "partial", "unsupported", "skipped", "error"}

class ConfigError(ValueError):
    pass

def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def is_link(path):
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())

def safe_root(raw):
    original = Path(raw).absolute()
    cursor = Path(original.anchor)
    for part in original.parts[1:]:
        cursor = cursor / part
        if is_link(cursor):
            raise ConfigError("root traverses a symlink or junction")
    if not original.is_dir():
        raise ConfigError("root must be an existing directory")
    return original.resolve()

def safe_path(root, raw, file_only=True):
    if not isinstance(raw, str) or not raw.strip() or "\x00" in raw:
        raise ConfigError("invalid path")
    given = Path(raw)
    candidate = given if given.is_absolute() else root / given
    try:
        relative = candidate.absolute().relative_to(root)
    except ValueError:
        raise ConfigError("path escapes project root: " + raw)
    cursor = root
    for part in relative.parts:
        if part == "..":
            cursor = cursor.parent
            try:
                cursor.relative_to(root)
            except ValueError:
                raise ConfigError("path escapes project root: " + raw)
            continue
        cursor = cursor / part
        if is_link(cursor):
            raise ConfigError("symlink path is not allowed: " + raw)
    resolved = candidate.resolve()
    try:
        resolved.relative_to(root)
    except ValueError:
        raise ConfigError("resolved path escapes project root: " + raw)
    if resolved.exists() and file_only and not resolved.is_file():
        raise ConfigError("expected file: " + raw)
    return resolved

def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise ConfigError("invalid JSON: " + str(path)) from exc

def array(value, name):
    if not isinstance(value, list):
        raise ConfigError(name + " must be an array")
    return value

def boolean(value, name):
    if not isinstance(value, bool):
        raise ConfigError(name + " must be boolean")
    return value

def identifier(value):
    if not isinstance(value, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_.-]*", value):
        raise ConfigError("invalid ID: " + repr(value))
    return value

def indexed(value, name):
    out = {}
    for item in array(value, name):
        if not isinstance(item, dict):
            raise ConfigError(name + " entries must be objects")
        ident = identifier(item.get("id"))
        if ident in out:
            raise ConfigError("duplicate ID in " + name + ": " + ident)
        out[ident] = item
    return out

def document_reference(docs, value):
    """Resolve a document ID, with a path fallback for older manifests."""
    if isinstance(value, str) and value in docs:
        return docs[value]
    if isinstance(value, str):
        for document in docs.values():
            if document.get("path") == value:
                return document
    return None

def anchor_present(text, anchor):
    """Recognize explicit HTML/Markdown anchors and heading slugs."""
    token = anchor.strip()
    if token.startswith("#"):
        token = token[1:]
    if not token:
        return False
    escaped = re.escape(token)
    if re.search(r"(?:id|name)=[\"']" + escaped + r"[\"']", text, re.IGNORECASE):
        return True
    if re.search(r"\{#" + escaped + r"\}", text, re.IGNORECASE):
        return True
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = match.group(1).strip()
        if heading.casefold() == token.casefold():
            return True
        slug = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"[-\s]+", "-", slug).strip("-").casefold()
        if slug == token.casefold():
            return True
    return False

def validate_trace_reference(root, docs, ident, entry, kind, faults):
    """Validate a requirement/acceptance document and optional index/anchor."""
    document = document_reference(docs, entry.get("document"))
    if document is None:
        faults.append(kind + " " + ident + " has unknown document")
        return
    path = safe_path(root, document["path"])
    if not path.is_file():
        faults.append(kind + " references a missing document: " + ident)
        return
    index_ref = entry.get("index")
    index_document = None
    if index_ref is not None:
        if not isinstance(index_ref, str) or not index_ref.strip():
            raise ConfigError(kind + ".index must be a non-empty document ID or path")
        index_document = document_reference(docs, index_ref)
        if index_document is None:
            faults.append(kind + " " + ident + " has unknown index document")
        else:
            index_path = safe_path(root, index_document["path"])
            if not index_path.is_file():
                faults.append(kind + " index references a missing document: " + ident)
            elif not re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(ident) + r"(?![A-Za-z0-9_.-])",
                               index_path.read_text(encoding="utf-8-sig")):
                faults.append(kind + " ID absent from index document: " + ident)
    anchor = entry.get("anchor")
    if anchor is not None:
        if not isinstance(anchor, str) or not anchor.strip():
            raise ConfigError(kind + ".anchor must be a non-empty anchor or heading")
        if not anchor_present(path.read_text(encoding="utf-8-sig"), anchor):
            faults.append(kind + " anchor absent from document: " + ident)
    elif index_document is None:
        if not re.search(r"(?<![A-Za-z0-9_.-])" + re.escape(ident) + r"(?![A-Za-z0-9_.-])",
                         path.read_text(encoding="utf-8-sig")):
            faults.append(kind + " ID absent from document: " + ident)

def cycle(graph):
    visiting, visited = set(), set()
    def visit(node):
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        if any(visit(dep) for dep in graph.get(node, []) if dep in graph):
            return True
        visiting.remove(node)
        visited.add(node)
        return False
    return any(visit(node) for node in graph)

def output_check(rule, status, scope, evidence, required=True, limitations=None):
    return {"rule_id": rule, "status": status, "required": required,
            "checked_scope": scope, "evidence": evidence, "limitations": limitations or []}

def relative_scope(root, raw):
    """Normalize a manifest path so it can be compared with Git paths."""
    path = safe_path(root, raw, file_only=False).relative_to(root).as_posix()
    return "" if path == "." else path

def lexical_path(root, raw):
    """Return an absolute path without resolving links for traversal pruning."""
    given = Path(raw)
    return Path(os.path.normpath(str((given if given.is_absolute() else root / given).absolute())))

def is_under(path, scope):
    """Whether path is scope itself or a descendant, without resolving links."""
    try:
        path.relative_to(scope)
        return True
    except ValueError:
        return False

def iter_module_paths(root, source, excluded):
    """Walk a module tree while pruning declared excluded subtrees.

    A lexical exclusion check must happen before ``safe_path`` so a pnpm link
    inside an excluded ``node_modules`` tree is never resolved or rejected.
    Links outside an exclusion remain subject to the normal root safety check.
    """
    stack = [source]
    while stack:
        current = stack.pop()
        if any(is_under(current, scope) for scope in excluded):
            continue
        try:
            children = list(current.iterdir())
        except OSError:
            raise
        for child in children:
            if any(is_under(child, scope) for scope in excluded):
                continue
            safe_path(root, str(child), file_only=False)
            yield child
            if child.is_dir():
                stack.append(child)

def control_plane_paths(root, manifest, manifest_path):
    """Return the current manifest's protected control-plane scopes."""
    paths = [manifest_path, "scripts/check_project.py"]
    control = manifest.get("control_plane", {})
    if control is not None:
        if not isinstance(control, dict):
            raise ConfigError("control_plane must be an object")
        declared = control.get("protected_paths", [])
        if not isinstance(declared, list) or not all(isinstance(item, str) and item.strip() for item in declared):
            raise ConfigError("control_plane.protected_paths must be an array of non-empty paths")
        paths.extend(declared)
        approval_env = control.get("approval_env", "ENGINEERING_CONTROL_PLANE_APPROVED")
        if not isinstance(approval_env, str) or not re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", approval_env):
            raise ConfigError("control_plane.approval_env must be a valid environment variable name")
    return sorted({relative_scope(root, path) for path in paths})

def git_revision(root, ref):
    if not isinstance(ref, str) or not ref or ref.startswith("-"):
        return None
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    proc = subprocess.run(prefix + ["rev-parse", "--verify", "--end-of-options", ref + "^{commit}"],
                          cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        return None
    oid = proc.stdout.decode("ascii", "replace").strip()
    return oid if re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", oid) else None

def git_parent(root, ref):
    oid = git_revision(root, ref)
    if not oid:
        raise ConfigError("Git commit is unavailable while inspecting its parent")
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    # Read the raw commit: rev-parse HEAD^ treats shallow boundaries and
    # missing parent objects like roots, which is unsafe for policy history.
    proc = subprocess.run(prefix + ["cat-file", "-p", oid],
                          cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        raise ConfigError("Git commit metadata is unavailable")
    headers = proc.stdout.split(b"\n\n", 1)[0].splitlines()
    parents = [line[7:].decode("ascii", "replace") for line in headers if line.startswith(b"parent ")]
    if not parents:
        return None
    if any(not re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", parent)
           or git_revision(root, parent) is None for parent in parents):
        raise ConfigError("Git parent object is unavailable; restore complete history before validation")
    return parents[0]

def git_is_shallow(root):
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    proc = subprocess.run(prefix + ["rev-parse", "--is-shallow-repository"], cwd=root,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        raise ConfigError("Git cannot determine whether this checkout is shallow")
    return proc.stdout.decode("ascii", "replace").strip().lower() == "true"

def manifest_from_git(root, revision, manifest_path):
    """Read a baseline manifest without trusting the working tree copy."""
    oid = git_revision(root, revision)
    if not oid:
        return None
    relative = relative_scope(root, manifest_path)
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    proc = subprocess.run(prefix + ["show", "--no-ext-diff", "--format=", oid + ":" + relative],
                          cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        return None
    try:
        return json.loads(proc.stdout.decode("utf-8-sig"))
    except (UnicodeError, json.JSONDecodeError):
        return None

def control_plane_check(root, manifest, manifest_path, mode, changed_paths, commit_ref=None, allow=False):
    """Block control-plane edits unless explicitly approved outside the repository."""
    if git_is_shallow(root):
        raise ConfigError("commit validation requires full Git history; shallow checkout is not supported")
    if mode == "commit" and git_revision(root, "HEAD"):
        git_parent(root, "HEAD")
    protected = set(control_plane_paths(root, manifest, manifest_path))
    baseline_ref = "HEAD" if mode == "commit" else git_parent(root, commit_ref) if commit_ref else None
    baseline = manifest_from_git(root, baseline_ref, manifest_path) if baseline_ref else None
    if isinstance(baseline, dict):
        protected.update(control_plane_paths(root, baseline, manifest_path))
    changed = sorted(path for path in changed_paths if any(covered(path, scope) for scope in protected))
    env_name = "ENGINEERING_CONTROL_PLANE_APPROVED"
    # The baseline setting is authoritative: a submitted manifest must not be
    # able to rename the approval variable to one already present in its runner.
    control = baseline.get("control_plane") if isinstance(baseline, dict) else None
    if isinstance(control, dict) and isinstance(control.get("approval_env"), str) and control["approval_env"].strip():
        env_name = control["approval_env"].strip()
    externally_approved = os.environ.get(env_name) == "1"
    approved = bool(changed) and allow and externally_approved
    gaps = []
    bootstrap = not isinstance(baseline, dict) and any(path == relative_scope(root, manifest_path) for path in changed_paths)
    if bootstrap:
        gaps.append("first adoption: new manifest/control-plane files require one-time manual review; inspect the generated baseline and rerun with --allow-control-plane-change plus the external approval variable")
    if changed and not approved:
        if not allow:
            gaps.append("control-plane files changed; rerun with --allow-control-plane-change after manual review")
        else:
            gaps.append("--allow-control-plane-change requires external approval variable " + env_name + "=1")
    evidence = {"protected_paths": sorted(protected), "changed_paths": changed, "first_adoption": bootstrap,
                "approval_variable": env_name, "external_approval_present": externally_approved}
    return output_check("control-plane", "fail" if gaps else "pass",
                        "baseline control-plane paths and submitted tree", evidence if not gaps else {**evidence, "gaps": gaps},
                        required=True,
                        limitations=["Control-plane approval is intentionally supplied outside the repository; review the manifest and checker changes separately."])

def validate(root, manifest, mode, task_id):
    if not isinstance(manifest, dict) or type(manifest.get("schema_version")) is not int or manifest["schema_version"] != 1:
        raise ConfigError("schema_version must be integer 1")
    for key in ("documents", "requirements", "acceptance", "modules", "inventories", "checks", "tasks", "baseline", "exclude_paths"):
        if key not in manifest:
            raise ConfigError("missing manifest key: " + key)
    docs = indexed(manifest["documents"], "documents")
    requirements = indexed(manifest["requirements"], "requirements")
    acceptance = indexed(manifest["acceptance"], "acceptance")
    modules = indexed(manifest["modules"], "modules")
    tasks = indexed(manifest["tasks"], "tasks")
    declared_checks = indexed(manifest["checks"], "checks")
    inventories = indexed(manifest["inventories"], "inventories")
    if not docs or not modules or not requirements or not acceptance or not tasks:
        raise ConfigError("documents, modules, requirements, acceptance and tasks cannot be empty")
    results, faults = [], []
    excluded = []
    for raw in array(manifest["exclude_paths"], "exclude_paths"):
        path = safe_path(root, raw, file_only=False)
        if path == root:
            raise ConfigError("exclude_paths cannot exclude project root")
        excluded.append(lexical_path(root, raw))
    def fault(msg):
        faults.append(msg)
    for ident, doc in docs.items():
        required = boolean(doc.get("required"), "document.required")
        path = safe_path(root, doc.get("path"))
        if not isinstance(doc.get("kind"), str) or not doc["kind"]:
            raise ConfigError("document.kind must be non-empty string")
        results.append(output_check("document:" + ident, "pass" if path.exists() else ("fail" if required else "skipped"),
                                    "document existence", doc["path"], required))
        if path.is_file() and path.suffix.lower() == ".md":
            for match in re.finditer(r"\[[^\]]*\]\(([^\s)]+)(?:\s+[^)]*)?\)", path.read_text(encoding="utf-8-sig")):
                target = match.group(1).strip("<>")
                if target.startswith(("#", "http://", "https://", "mailto:", "skill://", "app://", "codex://")):
                    continue
                target = target.split("#", 1)[0]
                if not target:
                    continue
                link = safe_path(root, str(path.parent / target), file_only=False)
                if not link.exists():
                    fault("broken local document reference: " + doc["path"] + " -> " + target)
    for name, entries in (("requirement", requirements), ("acceptance", acceptance)):
        for ident, item in entries.items():
            validate_trace_reference(root, docs, ident, item, name, faults)
    graph = {}
    for ident, module in modules.items():
        paths = array(module.get("source_paths"), "module.source_paths")
        if not paths:
            fault("module has no source paths: " + ident)
        for raw in paths:
            path = safe_path(root, raw, file_only=False)
            if not path.exists():
                fault("source missing: " + raw)
            if path.is_dir():
                for child in iter_module_paths(root, path, excluded):
                    # iter_module_paths performs the safety check before
                    # yielding, including for nested directories.
                    del child
        if module.get("document") not in docs:
            fault("module has unknown document: " + ident)
        elif not safe_path(root, docs[module["document"]]["path"]).is_file():
            fault("module references a missing document: " + ident)
        deps = array(module.get("depends_on"), "module.depends_on")
        allowed = array(module.get("allowed_dependencies"), "module.allowed_dependencies")
        graph[ident] = deps
        for dep in deps + allowed:
            if dep not in modules:
                fault("unknown dependency: " + str(dep))
        if not set(deps) <= set(allowed):
            fault("module dependencies violate allowlist: " + ident)
    if cycle(graph):
        fault("module dependency cycle")
    for ident, item in declared_checks.items():
        boolean(item.get("required"), "check.required")
        argv = item.get("command")
        if not isinstance(argv, list) or not argv or not all(isinstance(x, str) and x for x in argv):
            raise ConfigError("check command must be a non-empty argv array: " + ident)
        working_directory = item.get("working_directory", ".")
        if not isinstance(working_directory, str) or not working_directory.strip():
            raise ConfigError("check working_directory must be a non-empty path: " + ident)
        cwd = safe_path(root, working_directory, file_only=False)
        if not cwd.exists() or not cwd.is_dir():
            raise ConfigError("check working_directory must be an existing directory: " + ident)
        timeout = item.get("timeout_seconds")
        if type(timeout) not in (int, float) or not 0 < timeout <= 86400:
            raise ConfigError("invalid check timeout: " + ident)
    task_graph = {}
    for ident, task in tasks.items():
        for field, known in (("requirement_ids", requirements), ("acceptance_ids", acceptance), ("module_ids", modules), ("required_checks", declared_checks)):
            refs = array(task.get(field), "task." + field)
            for ref in refs:
                if ref not in known:
                    fault("task " + ident + " has unknown " + field + ": " + str(ref))
        if not task["requirement_ids"] or not task["acceptance_ids"] or not task["module_ids"]:
            fault("task trace is empty: " + ident)
        deps = array(task.get("depends_on"), "task.depends_on")
        task_graph[ident] = deps
        for dep in deps:
            if dep not in tasks:
                fault("task has unknown dependency: " + ident)
        if task.get("impact_document") not in docs:
            fault("task impact_document is unknown: " + ident)
        elif not safe_path(root, docs[task["impact_document"]]["path"]).is_file():
            fault("task references a missing impact document: " + ident)
        impact = task.get("documentation_impact", {})
        if impact is not None and not isinstance(impact, dict):
            raise ConfigError("task.documentation_impact must be an object")
        for kind, rule in (impact or {}).items():
            if not isinstance(kind, str) or not kind:
                raise ConfigError("documentation_impact kind must be a non-empty string")
            if not isinstance(rule, dict):
                raise ConfigError("documentation_impact entries must be objects")
            when_paths = rule.get("when_paths")
            if not isinstance(when_paths, list) or not when_paths or not all(isinstance(x, str) and x for x in when_paths):
                raise ConfigError("documentation_impact.when_paths must be a non-empty path array")
            document_ids = rule.get("document_ids")
            if not isinstance(document_ids, list) or not document_ids or not all(isinstance(x, str) and x for x in document_ids):
                raise ConfigError("documentation_impact.document_ids must be a non-empty array")
            for doc_id in document_ids:
                if doc_id not in docs:
                    raise ConfigError("documentation_impact references unknown document: " + doc_id)
            legal_trigger_scopes = [raw for module_id in task["module_ids"] if module_id in modules
                                    for raw in modules[module_id]["source_paths"]]
            legal_trigger_scopes.extend(docs[doc_id]["path"] for doc_id in document_ids)
            legal_trigger_scopes = [relative_scope(root, raw) for raw in legal_trigger_scopes]
            for raw in when_paths:
                normalized = relative_scope(root, raw)
                if not any(covered(normalized, allowed) for allowed in legal_trigger_scopes):
                    fault("documentation_impact.when_paths is outside module/document scopes: " + raw)
        boolean(task.get("approval_required"), "task.approval_required")
        if task.get("status") not in ("planned", "in_progress", "blocked", "complete"):
            raise ConfigError("invalid task status: " + ident)
    if cycle(task_graph):
        fault("task dependency cycle")
    baseline = manifest["baseline"]
    if not isinstance(baseline, dict):
        raise ConfigError("baseline must be an object")
    if baseline.get("status") not in ("complete", "approved"):
        fault("baseline not complete")
    evidence = safe_path(root, baseline.get("evidence"))
    if not evidence.is_file():
        fault("baseline evidence missing")
    results.append(output_check("manifest", "fail" if faults else "pass", "declared IDs, references, graph and baseline", faults or ["manifest validated"],
                                limitations=["Declared dependencies are not a discovered runtime graph; approval meaning and document semantics need review."]))
    for ident, entry in inventories.items():
        results.append(validate_inventory(root, ident, entry))
    if mode in ("change", "handoff", "commit", "committed"):
        if not task_id or task_id not in tasks:
            raise ConfigError("a known --task is required")
        task = tasks[task_id]
        gating = []
        if task["approval_required"]:
            approval = task.get("approval")
            if not isinstance(approval, dict) or approval.get("status") != "approved":
                gating.append("approval absent or not approved")
            else:
                path = safe_path(root, approval.get("evidence"))
                if not path.is_file():
                    gating.append("approval evidence missing")
        for dep in task["depends_on"]:
            if dep in tasks and tasks[dep]["status"] != "complete":
                gating.append("dependency not complete: " + dep)
        if mode == "handoff":
            if task["status"] != "complete":
                gating.append("handoff task status must be complete")
            if not task["required_checks"]:
                gating.append("handoff task needs required checks")
            review = task.get("skill_review")
            if not isinstance(review, dict):
                gating.append("handoff task skill_review is missing")
            else:
                for field in ("catalog_source", "scope", "checked_at", "recheck"):
                    if not isinstance(review.get(field), str) or not review[field].strip():
                        gating.append("skill_review missing " + field)
                candidates = review.get("candidates")
                if not isinstance(candidates, list):
                    gating.append("skill_review candidates must be an array")
                else:
                    for index, candidate in enumerate(candidates):
                        if not isinstance(candidate, dict):
                            gating.append("skill_review candidate is not an object: " + str(index))
                            continue
                        for field in ("id", "source", "version_or_release_date", "reason"):
                            if not isinstance(candidate.get(field), str) or not candidate[field].strip():
                                gating.append("skill_review candidate missing " + field + ": " + str(index))
                        if candidate.get("decision") not in ("adopted", "not-adopted", "unavailable"):
                            gating.append("skill_review candidate has invalid decision: " + str(index))
                        evidence = candidate.get("evidence")
                        if not isinstance(evidence, list) or not evidence or not all(isinstance(item, str) and item.strip() for item in evidence):
                            gating.append("skill_review candidate evidence is incomplete: " + str(index))
        if mode in ("commit", "committed") and not task.get("documentation_impact"):
            gating.append("commit task documentation_impact is missing; declare gates or record an explicit not-applicable decision")
        results.append(output_check("task-gate", "fail" if gating else "pass", "selected task approval/dependencies/status", gating or [task_id]))
    return results, docs, modules, tasks, declared_checks

def fields(items, label):
    out = {}
    for item in array(items, label):
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or not item["id"]:
            raise ConfigError(label + " item needs string ID")
        if item["id"] in out:
            raise ConfigError(label + " duplicate ID")
        names = array(item.get("fields"), label + ".fields")
        if not all(isinstance(x, str) and x for x in names) or len(set(names)) != len(names):
            raise ConfigError(label + " fields must be unique non-empty strings")
        out[item["id"]] = set(names)
    return out

def validate_inventory(root, ident, entry):
    required = boolean(entry.get("required"), "inventory.required")
    src_path = safe_path(root, entry.get("path"))
    map_path = safe_path(root, entry.get("documentation"))
    if not src_path.is_file() or not map_path.is_file():
        return output_check("inventory:" + ident, "error", "source and documentation inventories", "missing source or mapping file", required)
    src, mapping = read_json(src_path), read_json(map_path)
    if not isinstance(src, dict) or not isinstance(mapping, dict):
        raise ConfigError("inventories must be objects")
    if not entry.get("kind") or src.get("kind") != entry["kind"] or mapping.get("kind") != entry["kind"]:
        raise ConfigError("inventory kind mismatch: " + ident)
    source_items, doc_items = fields(src.get("items"), "source"), fields(mapping.get("items"), "mapping")
    problems = []
    for item in mapping["items"]:
        if not safe_path(root, item.get("document")).is_file():
            problems.append("mapping document missing: " + item["id"])
    if set(source_items) != set(doc_items):
        problems.append("item coverage mismatch: missing=" + str(sorted(set(source_items) - set(doc_items))) + " extra=" + str(sorted(set(doc_items) - set(source_items))))
    for item in set(source_items) & set(doc_items):
        if source_items[item] != doc_items[item]:
            problems.append("field coverage mismatch for " + item + ": missing=" + str(sorted(source_items[item] - doc_items[item])) + " extra=" + str(sorted(doc_items[item] - source_items[item])))
    provenance = src.get("provenance")
    if not isinstance(provenance, dict):
        raise ConfigError("inventory provenance required")
    boolean(provenance.get("complete"), "provenance.complete")
    if not isinstance(provenance.get("scope"), str) or not provenance["scope"] or not provenance.get("evidence"):
        raise ConfigError("inventory scope and evidence required")
    sources = array(provenance.get("source_files"), "provenance.source_files")
    for source in sources:
        if not isinstance(source, dict) or not isinstance(source.get("sha256"), str) or not re.fullmatch("[a-fA-F0-9]{64}", source["sha256"]):
            raise ConfigError("source_files requires path/sha256")
        path = safe_path(root, source.get("path"))
        if not path.is_file() or file_hash(path).lower() != source["sha256"].lower():
            problems.append("source metadata stale or missing: " + source["path"])
    if problems:
        status = "fail"
    elif provenance.get("type") == "manual" or not provenance["complete"]:
        status = "partial"
    elif provenance.get("type") == "sqlite-metadata" and entry["kind"] == "database" and len(sources) == 1:
        try:
            import extract_sqlite
            actual = extract_sqlite.extract(safe_path(root, sources[0]["path"]))
            if fields(actual["items"], "actual SQLite") != source_items:
                problems.append("SQLite metadata differs from declared source inventory")
                status = "fail"
            else:
                status = "pass"
        except (OSError, ValueError, __import__("sqlite3").Error):
            status = "unsupported"
            problems.append("SQLite source cannot be independently read as a checkpointed metadata snapshot")
    elif provenance.get("type") in {"mysql-metadata", "postgresql-metadata", "redis-metadata"} and entry["kind"] == "database":
        try:
            import extract_database
            adapter = provenance["type"].removesuffix("-metadata")
            expected = provenance.get("snapshot_sha256")
            actual = extract_database.snapshot_digest(src.get("items", []))
            if not isinstance(expected, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", expected):
                problems.append("metadata snapshot_sha256 is missing or malformed")
            elif actual.lower() != expected.lower():
                problems.append("metadata snapshot digest differs from declared snapshot")
            if not isinstance(provenance.get("source_ref"), str) or not provenance["source_ref"]:
                problems.append("metadata source_ref is missing")
            elif urlparse(provenance["source_ref"]).username or urlparse(provenance["source_ref"]).password:
                problems.append("metadata source_ref must not include credentials")
            try:
                captured = datetime.fromisoformat(provenance.get("captured_at", ""))
                if captured.tzinfo is None:
                    raise ValueError("timestamp has no timezone")
            except (TypeError, ValueError):
                problems.append("metadata captured_at is missing or invalid")
            expected_query = hashlib.sha256(extract_database.QUERY_HASHES[adapter].encode("utf-8")).hexdigest()
            if provenance.get("query_sha256") != expected_query:
                problems.append("metadata query_sha256 differs from supported adapter")
            status = "fail" if problems else "pass"
        except (OSError, ValueError, TypeError):
            status = "unsupported"
            problems.append("metadata snapshot cannot be independently validated")
    else:
        status = "unsupported"
    return output_check("inventory:" + ident, status, provenance["scope"], {"provenance": provenance, "coverage": problems or ["items and fields match"], "item_count": len(source_items)}, required,
                        ["Manual/unknown sources cannot prove full coverage. SQLite completeness covers the declared metadata scope only. Remote adapter snapshots prove internal integrity and declared metadata shape, not live database truth; field semantics and real usage require code review."])

def git_paths(root, base):
    if not isinstance(base, str) or not base or base.startswith("-"):
        raise ConfigError("Git base must be a commit reference, not an option")
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    revision = subprocess.run(prefix + ["rev-parse", "--verify", "--end-of-options", base + "^{commit}"], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
    oid = revision.stdout.decode("ascii", "replace").strip()
    if revision.returncode or not re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", oid):
        raise ConfigError("Git base cannot be resolved to a commit")
    paths = set()
    for argv in (["diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only", "-z", oid, "--"], ["ls-files", "--others", "--exclude-standard", "-z"]):
        proc = subprocess.run(prefix + argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
        if proc.returncode:
            raise ConfigError("Git cannot inspect requested base or working tree")
        paths.update(x.decode("utf-8", "surrogateescape").replace("\\", "/") for x in proc.stdout.split(b"\x00") if x)
    for path in paths:
        safe_path(root, path, file_only=False)
    return sorted(paths)

def staged_git_paths(root):
    """Return paths represented by the current index, including rename endpoints."""
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    head = subprocess.run(prefix + ["rev-parse", "--verify", "--end-of-options", "HEAD^{commit}"],
                          cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if head.returncode == 0:
        diff_args = ["diff", "--cached", "--no-ext-diff", "--no-textconv", "--find-renames", "--name-status", "-z", head.stdout.decode("ascii", "replace").strip(), "--"]
    else:
        diff_args = ["diff", "--cached", "--root", "--no-ext-diff", "--no-textconv", "--find-renames", "--name-status", "-z", "--"]
    proc = subprocess.run(prefix + diff_args, cwd=root, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        raise ConfigError("Git cannot inspect the staged index")
    fields = proc.stdout.split(b"\x00")
    paths = set()
    index = 0
    while index < len(fields):
        if not fields[index]:
            index += 1
            continue
        status = fields[index].decode("ascii", "replace")
        index += 1
        if status[:1] in ("R", "C"):
            if index + 1 >= len(fields):
                raise ConfigError("Git returned an incomplete rename record")
            old_path = fields[index].decode("utf-8", "surrogateescape").replace("\\", "/")
            new_path = fields[index + 1].decode("utf-8", "surrogateescape").replace("\\", "/")
            paths.update((old_path, new_path))
            index += 2
        else:
            if index >= len(fields):
                raise ConfigError("Git returned an incomplete staged-path record")
            path = fields[index].decode("utf-8", "surrogateescape").replace("\\", "/")
            paths.add(path)
            index += 1
    for path in paths:
        safe_path(root, path, file_only=False)
    return sorted(paths)

def unstaged_git_paths(root):
    """Return tracked and untracked paths not represented by the index."""
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    paths = set()
    for argv in (["diff", "--no-ext-diff", "--no-textconv", "--name-only", "-z", "--"],
                 ["ls-files", "--others", "--exclude-standard", "-z"]):
        proc = subprocess.run(prefix + argv, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
        if proc.returncode:
            raise ConfigError("Git cannot inspect unstaged paths")
        paths.update(x.decode("utf-8", "surrogateescape").replace("\\", "/") for x in proc.stdout.split(b"\x00") if x)
    for path in paths:
        safe_path(root, path, file_only=False)
    return sorted(paths)

def committed_git_paths(root, commit):
    """Return paths changed by a committed tree versus its first parent."""
    if git_is_shallow(root):
        raise ConfigError("committed mode requires a full Git history; shallow checkout cannot prove the parent")
    if not isinstance(commit, str) or not commit or commit.startswith("-"):
        raise ConfigError("Git commit must be a commit reference, not an option")
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    revision = subprocess.run(prefix + ["rev-parse", "--verify", "--end-of-options", commit + "^{commit}"], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
    oid = revision.stdout.decode("ascii", "replace").strip()
    if revision.returncode or not re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", oid):
        raise ConfigError("Git commit cannot be resolved")
    base = git_parent(root, oid)
    if base is None:
        args = ["diff-tree", "--root", "--no-commit-id", "-r", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only", "-z", oid, "--"]
    else:
        args = ["diff", "--no-ext-diff", "--no-textconv", "--no-renames", "--name-only", "-z", base, oid, "--"]
    proc = subprocess.run(prefix + args, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        raise ConfigError("Git cannot inspect committed tree")
    paths = {x.decode("utf-8", "surrogateescape").replace("\\", "/") for x in proc.stdout.split(b"\x00") if x}
    for path in paths:
        safe_path(root, path, file_only=False)
    return sorted(paths)

def covered(path, raw):
    normalized = raw.replace("\\", "/").rstrip("/")
    if normalized in ("", "."):
        return True
    if os.name == "nt":
        path, normalized = path.casefold(), normalized.casefold()
    return path == normalized or path.startswith(normalized + "/")

def change_check(root, manifest, docs, modules, tasks, task_id, base=None, paths=None, rule_id="change-scope", scope_label=None):
    if paths is None:
        paths = git_paths(root, base)
    selected = tasks[task_id]
    allowed = list(manifest["exclude_paths"])
    for ident in selected["module_ids"]:
        if ident in modules:
            allowed.extend(modules[ident]["source_paths"])
            doc = docs.get(modules[ident]["document"])
            if doc:
                allowed.append(doc["path"])
    if selected["impact_document"] in docs:
        allowed.append(docs[selected["impact_document"]]["path"])
    impact = selected.get("documentation_impact", {})
    if impact is not None and not isinstance(impact, dict):
        raise ConfigError("task.documentation_impact must be an object")
    for kind, rule in (impact or {}).items():
        if not isinstance(rule, dict):
            raise ConfigError("documentation_impact entries must be objects")
        if not isinstance(rule.get("when_paths"), list) or not rule["when_paths"] or not all(isinstance(x, str) and x for x in rule["when_paths"]):
            raise ConfigError("documentation_impact.when_paths must be a non-empty path array")
        if not isinstance(rule.get("document_ids"), list) or not rule["document_ids"]:
            raise ConfigError("documentation_impact.document_ids must be a non-empty array")
        for doc_id in rule["document_ids"]:
            if doc_id not in docs:
                raise ConfigError("documentation_impact references unknown document: " + str(doc_id))
            allowed.append(docs[doc_id]["path"])
    allowed = [relative_scope(root, raw) for raw in allowed]
    uncovered = [p for p in paths if not any(covered(p, raw) for raw in allowed)]
    exclude_scopes = [relative_scope(root, raw) for raw in manifest["exclude_paths"]]
    excluded = [p for p in paths if any(covered(p, raw) for raw in exclude_scopes)]
    documentation_gaps = []
    changed = [p for p in paths if not any(covered(p, raw) for raw in exclude_scopes)]
    document_scopes = {doc_id: relative_scope(root, doc["path"]) for doc_id, doc in docs.items()}
    changed_docs = {scope for scope in document_scopes.values() if any(covered(p, scope) for p in changed)}
    for kind, rule in (impact or {}).items():
        scopes = [relative_scope(root, raw) for raw in rule["when_paths"]]
        triggered = any(any(covered(p, scope) for scope in scopes) for p in changed)
        if triggered:
            for doc_id in rule["document_ids"]:
                if document_scopes[doc_id] not in changed_docs:
                    documentation_gaps.append(kind + " requires document update: " + docs[doc_id]["path"])
    if rule_id in ("commit-scope", "committed-scope"):
        source_scopes = [relative_scope(root, raw) for ident in selected["module_ids"] for raw in modules[ident]["source_paths"]]
        trigger_scopes = [relative_scope(root, raw) for rule in (impact or {}).values() for raw in rule["when_paths"]]
        document_paths = set(document_scopes.values())
        for path in changed:
            if path in document_paths or not any(covered(path, scope) for scope in source_scopes):
                continue
            if not any(covered(path, scope) for scope in trigger_scopes):
                documentation_gaps.append("source change has no documentation_impact rule: " + path)
    details = {"uncovered": uncovered, "excluded": excluded, "allowed": allowed, "documentation_gaps": documentation_gaps}
    status = "fail" if uncovered or documentation_gaps else "pass"
    scope = scope_label or ("Git staged index including deletions and rename endpoints" if base is None else "Git base diff including deletions, untracked paths and declared documentation impact")
    return paths, output_check(rule_id, status, scope, details,
                               limitations=["Explicit path coverage is not proof of undocumented transitive semantic impact; rules depend on the task's declared path scopes."])

def run_checks(root, checks, enabled, forced, blocked_reason=None):
    results = []
    for ident, check in checks.items():
        required = check["required"] or ident in forced
        if not enabled:
            results.append(output_check(ident, "skipped", "declared command", blocked_reason or "not run; use --run-checks", required))
            continue
        start = time.monotonic()
        try:
            cwd = safe_path(root, check.get("working_directory", "."), file_only=False)
            if not cwd.exists() or not cwd.is_dir():
                raise ConfigError("check working_directory must be an existing directory")
            proc = subprocess.run(check["command"], cwd=cwd, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                  timeout=check["timeout_seconds"], shell=False)
            evidence = {"command_sha256": hashlib.sha256(json.dumps(check["command"]).encode()).hexdigest(),
                        "working_directory": check.get("working_directory", "."),
                        "returncode": proc.returncode, "duration_seconds": round(time.monotonic()-start, 3),
                        "output_bytes": len(proc.stdout), "output_sha256": hashlib.sha256(proc.stdout).hexdigest()}
            status = "pass" if proc.returncode == 0 else "fail"
            if status == "pass" and re.search(rb"(?im)(?:skipped[=:]\s*[1-9]\d*|[1-9]\d*\s+skipped\b|#\s*SKIP\b)", proc.stdout):
                status = "partial"
                evidence["skip_marker_detected"] = True
            results.append(output_check(ident, status, "fresh invocation", evidence, required,
                                        ["Raw command output and argv are omitted to avoid leaking secrets. Common skip summaries are detected, but the absence of a marker cannot prove no checks were skipped."]))
        except subprocess.TimeoutExpired:
            results.append(output_check(ident, "fail", "fresh invocation", {"timeout_seconds": check["timeout_seconds"]}, required))
        except (ConfigError, OSError):
            results.append(output_check(ident, "unsupported", "fresh invocation", "declared executable unavailable", required))
    return results

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--mode", required=True, choices=("baseline", "change", "handoff", "commit", "committed"))
    parser.add_argument("--base")
    parser.add_argument("--commit-ref")
    parser.add_argument("--task")
    parser.add_argument("--run-checks", action="store_true")
    parser.add_argument("--allow-control-plane-change", action="store_true",
                        help="allow protected manifest/checker changes only with external approval")
    parser.add_argument("--report")
    args = parser.parse_args(argv)
    task_id = args.task or os.environ.get("ENGINEERING_TASK_ID")
    report = {"tool_version": VERSION, "mode": args.mode, "required_checks_satisfied": False, "checks": [], "summary": "", "changed_paths": [], "errors": []}
    # These modes must positively prove the submitted tree is safe to run;
    # exceptions and incomplete history leave command execution disabled.
    commands_allowed = args.mode not in ("commit", "committed")
    try:
        root = safe_root(args.root)
        manifest = read_json(safe_path(root, args.manifest))
        results, docs, modules, tasks, declared = validate(root, manifest, args.mode, task_id)
        report["checks"].extend(results)
        if args.mode in ("change", "handoff"):
            if not args.base:
                raise ConfigError("--base is required in change and handoff modes")
            try:
                report["changed_paths"], check = change_check(root, manifest, docs, modules, tasks, task_id, args.base)
                report["checks"].append(check)
            except (ConfigError, OSError, subprocess.TimeoutExpired):
                report["checks"].append(output_check("change-scope", "unsupported", "Git change discovery", "Git or requested base unavailable"))
        elif args.mode == "commit":
            try:
                report["changed_paths"], check = change_check(root, manifest, docs, modules, tasks, task_id,
                                                               paths=staged_git_paths(root), rule_id="commit-scope")
                control_check = control_plane_check(root, manifest, args.manifest, args.mode,
                                                    report["changed_paths"], allow=args.allow_control_plane_change)
                report["checks"].append(control_check)
                unstaged = unstaged_git_paths(root)
                if unstaged:
                    check["status"] = "fail"
                    check["evidence"]["unstaged_paths"] = unstaged
                    check["evidence"]["documentation_gaps"].append("worktree differs from staged index; stage or restore changes before commit validation")
                if not report["changed_paths"]:
                    check["status"] = "fail"
                    check["evidence"]["staged_paths"] = []
                    check["evidence"]["documentation_gaps"].append("no staged changes found")
                report["checks"].append(check)
                commands_allowed = all(item["status"] == "pass" for item in report["checks"] if item["required"])
            except (ConfigError, OSError, subprocess.TimeoutExpired) as exc:
                report["checks"].append(output_check("commit-scope", "unsupported", "Git staged index discovery", str(exc)))
        elif args.mode == "committed":
            try:
                if not args.commit_ref:
                    raise ConfigError("--commit-ref is required in committed mode")
                prefix = ["git", "-c", "safe.directory=" + str(root)]
                head = subprocess.run(prefix + ["rev-parse", "--verify", "HEAD^{commit}"], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
                target = subprocess.run(prefix + ["rev-parse", "--verify", "--end-of-options", args.commit_ref + "^{commit}"], cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
                if head.returncode or target.returncode or head.stdout.strip() != target.stdout.strip():
                    raise ConfigError("committed mode requires checkout at --commit-ref")
                report["changed_paths"], check = change_check(root, manifest, docs, modules, tasks, task_id,
                                                               paths=committed_git_paths(root, args.commit_ref), rule_id="committed-scope",
                                                               scope_label="checked-out commit tree versus first parent")
                control_check = control_plane_check(root, manifest, args.manifest, args.mode,
                                                    report["changed_paths"], commit_ref=args.commit_ref,
                                                    allow=args.allow_control_plane_change)
                report["checks"].append(control_check)
                unstaged = unstaged_git_paths(root)
                staged = staged_git_paths(root)
                if unstaged or staged:
                    check["status"] = "fail"
                    check["evidence"]["worktree_paths"] = unstaged
                    check["evidence"]["index_paths"] = staged
                    check["evidence"]["documentation_gaps"].append("checkout differs from committed tree")
                if not report["changed_paths"]:
                    check["status"] = "fail"
                    check["evidence"]["documentation_gaps"].append("commit has no changed paths")
                report["checks"].append(check)
                commands_allowed = all(item["status"] == "pass" for item in report["checks"] if item["required"])
            except (ConfigError, OSError, subprocess.TimeoutExpired) as exc:
                report["checks"].append(output_check("committed-scope", "unsupported", "committed tree discovery", str(exc)))
        forced = set(tasks[task_id]["required_checks"]) if task_id and task_id in tasks else set()
        reason = None if commands_allowed else "not run; submitted-tree validation did not pass"
        report["checks"].extend(run_checks(root, declared, args.run_checks and commands_allowed, forced, reason))
    except (ConfigError, OSError, UnicodeError, TypeError, KeyError) as exc:
        report["errors"].append(str(exc))
    required = [x for x in report["checks"] if x["required"]]
    report["required_checks_satisfied"] = bool(required) and not report["errors"] and all(x["status"] == "pass" for x in required)
    report["summary"] = "required checks satisfied" if report["required_checks_satisfied"] else "required checks not satisfied"
    if args.report:
        try:
            report_path = safe_path(safe_root(args.root), args.report)
            if report_path.exists():
                raise ConfigError("report output must be a new file; refusing overwrite")
            with report_path.open("x", encoding="utf-8") as output:
                output.write(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
        except (OSError, ConfigError) as exc:
            report["errors"].append(str(exc))
            report["required_checks_satisfied"] = False
            report["summary"] = "required checks not satisfied"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["required_checks_satisfied"]:
        return 0
    if report["errors"] or any(x["status"] in ("error", "unsupported") for x in required):
        return 2
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

