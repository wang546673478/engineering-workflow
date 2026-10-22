#!/usr/bin/env python3
"""Read-only manifest checks; declared commands run only with --run-checks."""
from __future__ import annotations
import argparse
from contextlib import contextmanager
import ctypes
from datetime import datetime, timezone
from fnmatch import fnmatchcase
import hashlib
import json
import os
from pathlib import Path, PureWindowsPath
import queue
import re
import signal
import subprocess
import sys
import threading
import time
from urllib.parse import urlparse

VERSION = (Path(__file__).resolve().parents[1] / "VERSION").read_text(encoding="utf-8-sig").strip()
MAX_CHECK_OUTPUT_BYTES = 8 * 1024 * 1024
OUTPUT_READ_CHUNK_BYTES = 64 * 1024
STATES = {"pass", "fail", "partial", "unsupported", "skipped", "error"}
GLOB_CHARS = frozenset("*?[")
WORKFLOW_STAGES = ("takeover_discovery", "baseline_review", "requirements_interview", "plan_confirmation", "implementation", "verification", "complete")
EARLY_WORKFLOW_STAGES = {"takeover_discovery", "baseline_review"}
IMPLEMENTATION_WORKFLOW_STAGES = {"implementation", "verification"}
WORKFLOW_APPROVALS = ("baseline_review", "proposal_approval")

class ConfigError(ValueError):
    pass

def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def is_link(path):
    return path.is_symlink() or bool(getattr(path, "is_junction", lambda: False)())

def _comparison_path(path):
    """Expand existing Win32 8.3 aliases without resolving link targets."""
    absolute = Path(path).absolute()
    if os.name != "nt" or not any(re.search(r"~[0-9]", part) for part in absolute.parts):
        return absolute
    try:
        get_long = ctypes.windll.kernel32.GetLongPathNameW
        get_long.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint)
        get_long.restype = ctypes.c_uint
        expanded = Path(absolute.anchor)
        for part in absolute.parts[1:]:
            candidate = expanded / part
            if candidate.exists():
                size = get_long(str(candidate), None, 0)
                if size:
                    buffer = ctypes.create_unicode_buffer(size + 1)
                    written = get_long(str(candidate), buffer, len(buffer))
                    if written and written < len(buffer):
                        candidate = Path(buffer.value)
            expanded = candidate
        return expanded
    except (AttributeError, OSError, ValueError):
        return absolute

def _relative_to_root(path, root):
    """Compare paths after resolving Windows long/short aliases consistently."""
    candidate = _comparison_path(path)
    canonical_root = _comparison_path(root)
    return candidate.relative_to(canonical_root)

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

def normalize_manifest_path(raw):
    if isinstance(raw, os.PathLike):
        raw = os.fspath(raw)
    if not isinstance(raw, str) or not raw.strip() or "\x00" in raw:
        raise ConfigError("invalid path")
    normalized = raw.replace("\\", "/")
    if os.name != "nt" and PureWindowsPath(normalized).drive:
        raise ConfigError("foreign absolute path: " + raw)
    return normalized

def safe_path(root, raw, file_only=True):
    normalized = normalize_manifest_path(raw)
    given = Path(normalized)
    candidate = given if given.is_absolute() else root / given
    raw_text = os.fspath(raw)
    try:
        relative = _relative_to_root(candidate, root)
    except ValueError:
        raise ConfigError("path escapes project root: " + raw_text)
    cursor = root
    for part in relative.parts:
        if part == "..":
            cursor = cursor.parent
            try:
                _relative_to_root(cursor, root)
            except ValueError:
                raise ConfigError("path escapes project root: " + raw_text)
            continue
        cursor = cursor / part
        if is_link(cursor):
            raise ConfigError("symlink path is not allowed: " + raw_text)
    resolved = candidate.resolve()
    try:
        _relative_to_root(resolved, root)
    except ValueError:
        raise ConfigError("resolved path escapes project root: " + raw_text)
    if resolved.exists() and file_only and not resolved.is_file():
        raise ConfigError("expected file: " + raw_text)
    return resolved

def has_glob_magic(raw):
    return any(char in raw for char in GLOB_CHARS)

def glob_segments_match(path, pattern):
    """Match slash-separated paths; ``**`` is the only multi-segment token."""
    path_parts = tuple(part for part in path.replace("\\", "/").split("/") if part)
    pattern_parts = tuple(pattern) if not isinstance(pattern, str) else tuple(pattern.replace("\\", "/").split("/"))
    if os.name == "nt":
        path_parts = tuple(part.casefold() for part in path_parts)
        pattern_parts = tuple(part.casefold() for part in pattern_parts)
    memo = {}
    def match(path_index, pattern_index):
        key = (path_index, pattern_index)
        if key in memo:
            return memo[key]
        if pattern_index == len(pattern_parts):
            result = path_index == len(path_parts)
        elif pattern_parts[pattern_index] == "**":
            result = match(path_index, pattern_index + 1) or (
                path_index < len(path_parts) and match(path_index + 1, pattern_index)
            )
        else:
            result = path_index < len(path_parts) and fnmatchcase(path_parts[path_index], pattern_parts[pattern_index]) and match(path_index + 1, pattern_index + 1)
        memo[key] = result
        return result
    return match(0, 0)

def build_exclude_specs(root, values):
    specs = []
    for raw in array(values, "exclude_paths"):
        normalized = normalize_manifest_path(raw)
        if has_glob_magic(normalized):
            parts = normalized.split("/")
            if normalized.startswith("/") or PureWindowsPath(normalized).drive:
                raise ConfigError("exclude glob must be project-relative: " + raw)
            if any(not part or part in (".", "..") for part in parts):
                raise ConfigError("exclude glob contains an unsafe path segment: " + raw)
            pattern = tuple(parts)
            if glob_segments_match("", pattern):
                raise ConfigError("exclude glob cannot exclude project root: " + raw)
            specs.append(("glob", pattern))
            continue
        path = safe_path(root, normalized, file_only=False)
        if path == root:
            raise ConfigError("exclude_paths cannot exclude project root")
        specs.append(("literal", lexical_path(root, normalized)))
    return specs

def lexical_relative(root, path):
    return _relative_to_root(path, root).as_posix()

def excluded_path(root, path, specs):
    if isinstance(path, Path):
        relative = lexical_relative(root, path)
    else:
        relative = normalize_manifest_path(path).lstrip("./")
    relative_parts = tuple(part for part in relative.split("/") if part)
    for kind, value in specs:
        if kind == "literal":
            candidate = root / Path(relative)
            if is_under(candidate, value):
                return True
        else:
            for index in range(1, len(relative_parts) + 1):
                if glob_segments_match("/".join(relative_parts[:index]), value):
                    return True
    return False

def parse_json(data, source, **decoder_options):
    try:
        if isinstance(data, bytes):
            data = data.decode("utf-8-sig")
        # CPython 3.14's C decoder may accept depths that older decoders
        # rejected. Preserve the interpreter recursion-budget boundary without
        # increasing it or introducing a different arbitrary input size limit.
        depth, quoted, escaped = 0, False, False
        for char in data:
            if quoted:
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == '"':
                    quoted = False
            elif char == '"':
                quoted = True
            elif char in "[{":
                depth += 1
                if depth >= sys.getrecursionlimit():
                    raise ValueError("JSON nesting exceeds the interpreter recursion budget")
            elif char in "]}":
                depth -= 1
        return json.loads(data, **decoder_options)
    except (ValueError, RecursionError) as exc:
        raise ConfigError("invalid JSON or parser limit exceeded: " + str(source)) from exc


def read_json(path):
    try:
        return parse_json(path.read_bytes(), path)
    except OSError as exc:
        raise ConfigError("cannot read JSON: " + str(path)) from exc

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


def _approval_section_text(text, section_id):
    """Return a stable heading section for approval snapshot hashing."""
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    identifier(section_id)
    begin = "<!-- engineering-review:" + section_id + " -->"
    end_marker = "<!-- /engineering-review:" + section_id + " -->"
    if begin in normalized or end_marker in normalized:
        if normalized.count(begin) != 1 or normalized.count(end_marker) != 1:
            raise ConfigError("approval subject markers must be unique and paired")
        start = normalized.index(begin) + len(begin)
        end = normalized.index(end_marker)
        if end <= start:
            raise ConfigError("approval subject markers are out of order")
        return normalized[start:end].strip() + "\n"
    token = section_id.strip().lstrip("#")
    lines = normalized.splitlines()
    matches = []
    for index, line in enumerate(lines):
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        heading = match.group(2).strip()
        slug = re.sub(r"[^\w\s-]", "", heading, flags=re.UNICODE)
        slug = re.sub(r"[-\s]+", "-", slug).strip("-").casefold()
        if heading.casefold() == token.casefold() or slug == token.casefold():
            matches.append((index, len(match.group(1))))
    if len(matches) > 1:
        raise ConfigError("approval subject heading is ambiguous")
    if not matches:
        return None
    start, level = matches[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        match = re.match(r"^\s{0,3}(#{1,6})\s+", lines[index])
        if match and len(match.group(1)) <= level:
            end = index
            break
    return "\n".join(lines[start:end]).strip() + "\n"


def approval_subject_hash(text, section_id):
    """Hash a normalized approval subject section for fixtures and evidence."""
    section = _approval_section_text(text, section_id)
    if section is None:
        raise ConfigError("approval subject section is missing: " + str(section_id))
    return hashlib.sha256(section.encode("utf-8")).hexdigest()


def _strict_json_object(text, source):
    duplicate = []

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                duplicate.append(key)
            result[key] = value
        return result

    def reject_constant(value):
        raise ValueError("non-finite JSON constant: " + value)

    try:
        value = parse_json(text, source, object_pairs_hook=pairs, parse_constant=reject_constant)
    except (ValueError, RecursionError) as exc:
        raise ConfigError("invalid approval JSON: " + str(source)) from exc
    if duplicate:
        raise ConfigError("duplicate approval JSON key in " + str(source) + ": " + duplicate[0])
    if not isinstance(value, dict):
        raise ConfigError("approval record must be a JSON object: " + str(source))
    return value


def approval_records(path):
    """Read uniquely named JSON approval blocks without executing content."""
    text = path.read_text(encoding="utf-8-sig")
    if path.suffix.lower() == ".json":
        data = _strict_json_object(text, path)
        values = data.get("records", [data])
        if not isinstance(values, list):
            raise ConfigError("approval records must be an array")
        records = {}
        for value in values:
            if not isinstance(value, dict):
                raise ConfigError("approval record must be an object")
            ident = identifier(value.get("id"))
            if ident in records:
                raise ConfigError("duplicate approval record ID: " + ident)
            records[ident] = value
        return records
    pattern = re.compile(
        r"<!--\s*engineering-approval:([A-Za-z][A-Za-z0-9_.-]*)\s*-->\s*"
        r"```json\s*\r?\n(.*?)\r?\n```", re.IGNORECASE | re.DOTALL)
    records = {}
    for match in pattern.finditer(text):
        ident = match.group(1)
        if ident in records:
            raise ConfigError("duplicate approval record ID: " + ident)
        record = _strict_json_object(match.group(2), path)
        if record.get("id") != ident:
            raise ConfigError("approval record ID does not match its block: " + ident)
        records[ident] = record
    markers = re.findall(r"<!--\s*engineering-approval:([A-Za-z][A-Za-z0-9_.-]*)\s*-->", text)
    if len(markers) != len(records):
        raise ConfigError("approval blocks must have unique IDs and valid JSON fences")
    return records


def resolve_approval_record(root, evidence, record_id, visited=()):
    """Resolve an explicit bounded reuse relation, retaining the original statement."""
    path = safe_path(root, evidence)
    key = (str(path), record_id)
    if key in visited or len(visited) >= 16:
        raise ConfigError("approval reuse cycle or depth limit")
    records = approval_records(path)
    if record_id not in records:
        raise ConfigError("approval evidence record is missing: " + str(record_id))
    record = records[record_id]
    if record.get("invalidated") is True:
        raise ConfigError("approval evidence was invalidated")
    reuse = record.get("reuse_of")
    if reuse is None:
        return record
    if not isinstance(reuse, dict) or not isinstance(reuse.get("reason"), str) or not reuse["reason"].strip():
        raise ConfigError("approval reuse_of requires a reference and reason")
    original = resolve_approval_record(root, reuse.get("evidence"), reuse.get("evidence_record_id"), visited + (key,))
    if original.get("status") != "approved":
        raise ConfigError("approval reuse source is not approved")
    new_ids, old_ids = record.get("requirement_ids"), original.get("requirement_ids")
    if not isinstance(new_ids, list) or not all(isinstance(x, str) for x in new_ids) or not isinstance(old_ids, list) or not all(isinstance(x, str) for x in old_ids) or not set(new_ids) <= set(old_ids):
        raise ConfigError("approval reuse cannot expand the approved requirements")
    new_acceptance, old_acceptance = record.get("acceptance_ids"), original.get("acceptance_ids")
    if not isinstance(new_acceptance, list) or not all(isinstance(x, str) for x in new_acceptance) or not isinstance(old_acceptance, list) or not all(isinstance(x, str) for x in old_acceptance) or not set(new_acceptance) <= set(old_acceptance):
        raise ConfigError("approval reuse cannot expand approved acceptance")
    for field in ("subject", "spec_basis"):
        if record.get(field, original.get(field)) != original.get(field):
            raise ConfigError("approval reuse cannot replace reviewed subjects")
    resolved = dict(original)
    resolved.update(record)
    for field in ("user_statement", "approved_at", "source"):
        if field in record and record[field] != original.get(field):
            raise ConfigError("approval reuse cannot invent a new " + field)
        resolved[field] = original.get(field)
    return resolved


def _approval_timestamp(value, now=None):
    if not isinstance(value, str) or not value.strip():
        return False
    try:
        parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    if parsed.tzinfo is None:
        return False
    return parsed <= (now or datetime.now(timezone.utc))


def _approval_semver(value):
    match = re.fullmatch(r"(\d+)\.(\d+)\.(\d+)(?:[-+].*)?", value) if isinstance(value, str) else None
    return tuple(int(match.group(index)) for index in range(1, 4)) if match else None


def _approval_subject_gaps(root, docs, subject, label):
    gaps = []
    if not isinstance(subject, dict):
        return [label + " subject is missing"]
    document = document_reference(docs, subject.get("document"))
    if document is None:
        return [label + " subject references unknown document"]
    try:
        path = safe_path(root, document["path"])
    except ConfigError as exc:
        return [label + " subject path is unsafe: " + str(exc)]
    section_id = subject.get("section_id")
    digest = subject.get("sha256")
    if not isinstance(subject.get("revision"), str) or not subject["revision"].strip():
        gaps.append(label + " subject revision is missing")
    if not isinstance(section_id, str) or not section_id.strip():
        gaps.append(label + " subject section_id is missing")
    if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
        gaps.append(label + " subject sha256 is invalid")
    if isinstance(section_id, str) and section_id.strip() and path.is_file():
        text = path.read_text(encoding="utf-8-sig")
        try:
            section = _approval_section_text(text, section_id)
        except ConfigError as exc:
            return gaps + [label + " " + str(exc)]
        if section is None:
            gaps.append(label + " subject section is missing")
        elif isinstance(digest, str) and re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            actual = hashlib.sha256(section.encode("utf-8")).hexdigest()
            if actual.casefold() != digest.casefold():
                gaps.append(label + " subject sha256 does not match")
    return gaps


def approval_contract_check(root, docs, workflow, selected_task, task_id):
    """Validate opt-in structured approval evidence while preserving legacy manifests."""
    policy = workflow.get("approval_policy") if isinstance(workflow, dict) else None
    if policy is None:
        declaration_scope = {}
        if isinstance(selected_task, dict):
            declaration_scope = {key: {"status": value.get("status"), "evidence": value.get("evidence")}
                                 for key in ("implementation_authorization", "spec_review", "plan_review", "approval")
                                 if isinstance((value := selected_task.get(key)), dict)}
        return output_check("approval-evidence", "partial", "legacy approval declarations",
                            {"status": "legacy_unverified", "reason": "no structured approval policy enabled", "declared_records": declaration_scope}, False,
                            limitations=["Legacy validation is preserved; a passing command result does not verify approval content or current scope."])
    if not isinstance(policy, dict):
        raise ConfigError("workflow.approval_policy must be an object")
    if type(policy.get("record_contract")) is not int or policy.get("record_contract") != 1:
        raise ConfigError("workflow.approval_policy.record_contract must be 1")
    enforcement = policy.get("enforcement", "diagnostic")
    if enforcement not in ("diagnostic", "strict"):
        raise ConfigError("workflow.approval_policy.enforcement must be diagnostic or strict")
    gaps = []
    if enforcement == "strict" and (not isinstance(workflow, dict) or "stage" not in workflow):
        gaps.append("strict approval policy requires workflow.stage")
    minimum_version = policy.get("minimum_checker_version", "1.8.0")
    current_version = _approval_semver(VERSION)
    required_version = _approval_semver(minimum_version)
    if required_version is None:
        raise ConfigError("workflow.approval_policy.minimum_checker_version must be semantic version")
    if enforcement == "strict" and (current_version is None or current_version < required_version):
        gaps.append("strict approval policy requires checker " + minimum_version + " or newer")
    records_to_check = []
    reviewed_records = {}
    if isinstance(workflow, dict):
        records_to_check.extend([
            ("baseline_review", workflow.get("baseline_review"), "baseline"),
            ("proposal_approval", workflow.get("proposal_approval"), "proposal"),
        ])
    if isinstance(selected_task, dict):
        records_to_check.append(("implementation_authorization", selected_task.get("implementation_authorization"), "implementation"))
        if selected_task.get("approval_required") is True:
            records_to_check.append(("task.approval", selected_task.get("approval"), "task"))
    for name, declaration, kind in records_to_check:
        if declaration is None or not isinstance(declaration, dict):
            gaps.append(name + " declaration is missing")
            continue
        status = declaration.get("status")
        if status == "pending":
            continue
        if status not in ("approved", "not_applicable"):
            gaps.append(name + " has invalid status")
            continue
        evidence = declaration.get("evidence")
        record_id = declaration.get("evidence_record_id")
        if not isinstance(evidence, str) or not evidence.strip():
            gaps.append(name + " evidence path is missing")
            continue
        if not isinstance(record_id, str) or not record_id.strip():
            gaps.append(name + " evidence_record_id is missing")
            continue
        try:
            path = safe_path(root, evidence)
        except ConfigError as exc:
            gaps.append(name + " evidence path is unsafe: " + str(exc))
            continue
        if not path.is_file():
            gaps.append(name + " evidence file does not exist")
            continue
        try:
            record = resolve_approval_record(root, evidence, record_id)
        except (ConfigError, OSError, UnicodeError) as exc:
            gaps.append(name + " evidence cannot be parsed: " + str(exc))
            continue
        if record.get("status") != status:
            gaps.append(name + " evidence status does not match declaration")
        reviewed_records[kind] = record
        for field in ("user_statement", "approved_at", "scope", "source"):
            if field in declaration and declaration[field] != record.get(field):
                gaps.append(name + " declaration " + field + " does not match evidence")
        if status == "not_applicable":
            if not isinstance(record.get("reason"), str) or not record["reason"].strip():
                gaps.append(name + " not_applicable evidence needs a reason")
            if kind == "proposal" and (not isinstance(selected_task, dict) or selected_task.get("workflow_kind") != "small_fix"):
                gaps.append(name + " not_applicable is only valid for an evidenced small_fix")
            if kind == "implementation":
                gaps.append(name + " implementation authorization cannot be not_applicable")
        statement = record.get("user_statement")
        if status == "approved" and (not isinstance(statement, str) or _approval_placeholder(statement)):
            gaps.append(name + " user_statement is missing or placeholder")
        if status == "approved" and not _approval_timestamp(record.get("approved_at")):
            gaps.append(name + " approved_at must be timezone-aware and not future")
        if status == "approved" and ("recorded_at" not in record or not _approval_timestamp(record.get("recorded_at"))):
            gaps.append(name + " recorded_at must be present, timezone-aware and not future")
        scope = record.get("scope")
        if not isinstance(scope, str) or _approval_placeholder(scope):
            gaps.append(name + " scope is missing or not reviewable")
        source = record.get("source")
        if status == "approved" and (not isinstance(source, dict) or source.get("kind") not in ("conversation", "manual") or not isinstance(source.get("reference"), str) or not source["reference"].strip()):
            gaps.append(name + " source must identify a conversation or manual reference")
        if kind in ("proposal", "implementation", "task"):
            if record.get("task_id") != task_id:
                gaps.append(name + " evidence task_id does not match selected task")
            batch_id = selected_task.get("batch_id") if isinstance(selected_task, dict) else None
            if not isinstance(batch_id, str) or not batch_id.strip():
                gaps.append(name + " selected task batch_id is missing")
            elif record.get("batch_id") != batch_id:
                gaps.append(name + " evidence batch_id does not match selected task")
            if declaration.get("batch_id") != record.get("batch_id"):
                gaps.append(name + " declaration batch_id does not match evidence")
            if not isinstance(record.get("batch_id"), str) or not record["batch_id"].strip():
                gaps.append(name + " evidence batch_id is missing")
            required_ids = set(selected_task.get("requirement_ids", [])) if isinstance(selected_task, dict) else set()
            actual_ids = record.get("requirement_ids")
            if not isinstance(actual_ids, list) or not actual_ids or not all(isinstance(item, str) for item in actual_ids) or set(actual_ids) != required_ids:
                gaps.append(name + " requirement_ids must exactly match the selected task scope")
            expected_acceptance = set(selected_task.get("acceptance_ids", []))
            actual_acceptance = record.get("acceptance_ids")
            if not isinstance(actual_acceptance, list) or not actual_acceptance or not all(isinstance(item, str) for item in actual_acceptance) or set(actual_acceptance) != expected_acceptance:
                gaps.append(name + " acceptance_ids must exactly match the selected task scope")
            gaps.extend(_approval_subject_gaps(root, docs, record.get("subject"), name))
            gaps.extend(_approval_subject_gaps(root, docs, record.get("spec_basis"), name + " spec_basis"))
            revisions = selected_task.get("artifact_revisions", {}) if isinstance(selected_task, dict) else {}
            active_revisions = workflow.get("active_revisions", {}) if isinstance(workflow, dict) else {}
            if not isinstance(revisions, dict) or not isinstance(active_revisions, dict):
                raise ConfigError("artifact_revisions and active_revisions must be objects")
            subject = record.get("subject") if isinstance(record.get("subject"), dict) else {}
            spec_basis = record.get("spec_basis") if isinstance(record.get("spec_basis"), dict) else {}
            plan_revision = revisions.get("plan") or active_revisions.get("plan")
            spec_revision = revisions.get("spec") or active_revisions.get("spec")
            basis = selected_task.get("review_basis_revision", {})
            if not isinstance(basis, dict):
                raise ConfigError("task.review_basis_revision must be an object")
            if basis and (not isinstance(basis.get("reason"), str) or not basis["reason"].strip()):
                gaps.append(name + " review_basis_revision requires an equivalence reason")
            if not plan_revision or subject.get("revision") != (basis.get("plan") if basis.get("reason") else None) and subject.get("revision") != plan_revision:
                gaps.append(name + " subject revision does not match the selected task Plan revision")
            if not spec_revision or spec_basis.get("revision") != (basis.get("spec") if basis.get("reason") else None) and spec_basis.get("revision") != spec_revision:
                gaps.append(name + " spec_basis revision does not match the selected task Spec revision")
            links = selected_task.get("artifact_links", {})
            for field, entry in (("plan", subject), ("spec", spec_basis)):
                expected_document = links.get(field) or workflow.get("active_" + field)
                if expected_document and entry.get("document") != expected_document:
                    gaps.append(name + " subject document does not match active " + field)
            if kind == "proposal":
                revision = declaration.get("revision")
                if subject.get("revision") != revision:
                    gaps.append(name + " subject revision does not match declaration")
            elif kind == "implementation":
                proposal = workflow.get("proposal_approval") if isinstance(workflow, dict) else None
                expected = proposal.get("revision") if isinstance(proposal, dict) else None
                if declaration.get("plan_revision") != expected or subject.get("revision") != expected:
                    gaps.append(name + " implementation plan revision does not match proposal")
            elif kind == "task":
                task_plan = selected_task.get("artifact_revisions", {}).get("plan")
                if task_plan and subject.get("revision") != task_plan:
                    gaps.append(name + " subject revision does not match selected task Plan")
        else:
            gaps.extend(_approval_subject_gaps(root, docs, record.get("subject"), name))
            if status == "approved" and (not isinstance(record.get("subject"), dict) or record["subject"].get("revision") != declaration.get("source_revision")):
                gaps.append(name + " source_revision does not match reviewed subject")
    proposal = reviewed_records.get("proposal")
    implementation = reviewed_records.get("implementation")
    if isinstance(proposal, dict) and isinstance(implementation, dict):
        for field in ("subject", "spec_basis"):
            if proposal.get(field) != implementation.get(field):
                gaps.append("implementation_authorization " + field + " does not match approved proposal content")
        declaration = selected_task.get("implementation_authorization", {})
        expected_id = workflow.get("proposal_approval", {}).get("evidence_record_id")
        if declaration.get("proposal_record_id") != expected_id:
            gaps.append("implementation_authorization proposal_record_id does not match approved proposal")
    if gaps:
        status = "partial" if enforcement == "diagnostic" else "fail"
        required = enforcement == "strict"
    else:
        status, required = "pass", enforcement == "strict"
    return output_check("approval-evidence", status, "structured approval records and reviewed subjects", gaps or ["approval records are structurally bound"], required,
                        limitations=["The checker validates declared structure, paths, hashes and bindings; it cannot authenticate a human, prove a user understood the scope, or certify semantic completeness."])


def _approval_placeholder(value):
    if not isinstance(value, str) or not value.strip():
        return True
    text = value.strip().casefold()
    return (text in {"pending", "all", "this batch", "tbd", "todo", "placeholder"}
            or bool(re.fullmatch(r"<[^>]+>", text))
            or any(token in text for token in ("replace me", "fill this", "insert here", "default-consent implementation")))


def approval_policy_history_check(root, manifest, manifest_path, mode, base=None, commit_ref=None, allow=False, submission_baseline=None):
    """Preserve previously enabled approval gates, including complete history checks."""
    if submission_baseline is not None and "manifest" in submission_baseline:
        # The control-plane check has already read this exact submission's
        # historical manifest. This dictionary is local to one CLI invocation;
        # it is never reused across commands, repositories or verification runs.
        previous = submission_baseline["manifest"]
    else:
        if mode == "change":
            ref = base
        elif mode in ("handoff", "commit"):
            ref = "HEAD" if git_revision(root, "HEAD") else None
        elif mode == "committed":
            ref = git_parent(root, commit_ref or "HEAD")
        else:
            return None
        if ref and not git_revision(root, ref):
            raise ConfigError("approval policy history revision is unavailable")
        previous = manifest_from_git(root, ref, manifest_path) if ref else None
    old_workflow = previous.get("workflow", {}) if isinstance(previous, dict) else {}
    new_workflow = manifest.get("workflow", {})
    old = old_workflow.get("approval_policy") if isinstance(old_workflow, dict) else None
    if old is None:
        return None
    new = new_workflow.get("approval_policy") if isinstance(new_workflow, dict) else None
    gaps = []
    if not isinstance(old, dict):
        raise ConfigError("historical approval_policy must be an object")
    if not isinstance(new, dict):
        gaps.append("enabled approval policy was removed")
    else:
        if old.get("record_contract") != new.get("record_contract"):
            gaps.append("approval record contract was replaced")
        if old.get("enforcement", "diagnostic") == "strict":
            if new.get("enforcement", "diagnostic") != "strict":
                gaps.append("strict approval policy was weakened")
            for field in ("stage", "implementation_paths"):
                if field not in new_workflow:
                    gaps.append("strict lifecycle field was removed: " + field)
            old_paths = old_workflow.get("implementation_paths", [])
            new_paths = new_workflow.get("implementation_paths", [])
            if isinstance(old_paths, list) and isinstance(new_paths, list):
                if not all(any(covered(relative_scope(root, old_path), relative_scope(root, new_path)) for new_path in new_paths) for old_path in old_paths):
                    gaps.append("strict implementation scopes were reduced")
        if old.get("sequence_enforcement") == "strict" and new.get("sequence_enforcement") != "strict":
            gaps.append("strict approval sequence policy was weakened")
    control = previous.get("control_plane", {}) if isinstance(previous, dict) else {}
    env_name = control.get("approval_env", "ENGINEERING_CONTROL_PLANE_APPROVED") if isinstance(control, dict) else "ENGINEERING_CONTROL_PLANE_APPROVED"
    approved = allow and os.environ.get(env_name) == "1"
    if not gaps:
        return output_check("approval-policy-history", "pass", "previously enabled approval policy", "policy retained", True)
    return output_check("approval-policy-history", "fail" if not approved else "pass",
                        "previously enabled approval policy", {"gaps": gaps, "external_change_approval": approved}, True,
                        limitations=["Policy weakening requires the existing one-run external control approval; this does not authenticate a human."])


def approval_sequence_check(workflow, task):
    """Compare declared event positions on one timeline; clocks alone never prove order."""
    policy = workflow.get("approval_policy") if isinstance(workflow, dict) else None
    if policy is None:
        return None
    enforcement = policy.get("sequence_enforcement", "diagnostic")
    if enforcement not in ("diagnostic", "strict"):
        raise ConfigError("sequence_enforcement must be diagnostic or strict")
    sequence = task.get("approval_sequence") if isinstance(task, dict) else None
    required = enforcement == "strict" and workflow.get("stage") in IMPLEMENTATION_WORKFLOW_STAGES | {"complete"}
    status, evidence = "partial", "ordered approval events were not supplied"
    if isinstance(sequence, dict):
        events = [sequence.get(key) for key in ("presented", "approved", "implementation")]
        valid = all(isinstance(event, dict) and isinstance(event.get("timeline_id"), str) and event["timeline_id"].strip()
                    and isinstance(event.get("reference"), str) and event["reference"].strip()
                    and type(event.get("position")) is int and event["position"] >= 0 for event in events)
        if valid and len({event["timeline_id"] for event in events}) == 1:
            status = "pass" if events[0]["position"] < events[1]["position"] < events[2]["position"] else "fail"
            evidence = {"timeline_id": events[0]["timeline_id"], "positions": [event["position"] for event in events]}
        else:
            evidence = "event references are incomplete or belong to different timelines"
    return output_check("approval-sequence", status, "declared presentation/approval/implementation order", evidence, required,
                        limitations=["Declared event order is not a trusted host receipt. File mtime, Git time and manually asserted order cannot authenticate approval."])


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


def workflow_lifecycle_gaps(root, workflow, baseline, selected_task, task_id, mode):
    """Validate explicit adoption-stage and approval state when a manifest opts in."""
    stage = workflow.get("stage")
    if stage not in WORKFLOW_STAGES:
        return ["workflow.stage must be one of: " + ", ".join(WORKFLOW_STAGES)]
    gaps = []
    authorization = selected_task.get("implementation_authorization") if isinstance(selected_task, dict) else None
    if not isinstance(authorization, dict) or authorization.get("status") not in ("pending", "approved"):
        gaps.append("selected task implementation_authorization must record pending or approved status")
    implementation_paths = workflow.get("implementation_paths")
    if not isinstance(implementation_paths, list) or not implementation_paths:
        gaps.append("workflow.implementation_paths must declare reviewed implementation scopes")
    else:
        for raw in implementation_paths:
            if has_glob_magic(normalize_manifest_path(raw)):
                gaps.append("workflow.implementation_paths must be literal paths: " + str(raw))
                continue
            try:
                if not relative_scope(root, raw):
                    gaps.append("workflow.implementation_paths cannot include project root")
            except (ConfigError, TypeError):
                gaps.append("workflow.implementation_paths contains an unsafe path: " + str(raw))

    approvals = {}
    for key in WORKFLOW_APPROVALS:
        record = workflow.get(key)
        if not isinstance(record, dict):
            gaps.append("workflow." + key + " approval record is missing")
            approvals[key] = None
            continue
        status = record.get("status")
        if status not in ("pending", "approved", "not_applicable"):
            gaps.append("workflow." + key + ".status must be pending, approved or evidenced not_applicable")
        if record.get("invalidated") is True:
            gaps.append("workflow." + key + " approval was invalidated; affected review must be reopened")
        evidence = record.get("evidence")
        if status in ("approved", "not_applicable"):
            if not isinstance(evidence, str) or not evidence.strip():
                gaps.append("workflow." + key + " approval evidence is missing")
            else:
                try:
                    if not safe_path(root, evidence).is_file():
                        gaps.append("workflow." + key + " approval evidence does not exist")
                except ConfigError:
                    gaps.append("workflow." + key + " approval evidence path is unsafe")
        approvals[key] = record

    baseline_status = baseline.get("status") if isinstance(baseline, dict) else None
    baseline_review = approvals.get("baseline_review")
    baseline_approved = isinstance(baseline_review, dict) and baseline_review.get("status") == "approved"
    if baseline_approved and (not isinstance(baseline_review.get("source_revision"), str)
                              or not baseline_review["source_revision"].strip()):
        gaps.append("baseline review approval must identify the reviewed source_revision")
    greenfield_progress = baseline.get("origin") == "greenfield" and baseline_status in ("not_applicable", "partial", "complete", "approved")
    baseline_exempt = isinstance(baseline_review, dict) and baseline_review.get("status") == "not_applicable"
    if baseline_exempt and (not greenfield_progress or not isinstance(baseline_review.get("reason"), str) or not baseline_review["reason"].strip()):
        gaps.append("baseline review not_applicable requires evidenced greenfield origin and reason")
    baseline_reviewable = baseline_status in ("complete", "approved") or greenfield_progress
    proposal = approvals.get("proposal_approval")
    proposal_exempt = isinstance(proposal, dict) and proposal.get("status") == "not_applicable"
    if proposal_exempt and (not isinstance(selected_task, dict) or selected_task.get("workflow_kind") != "small_fix"
                            or not isinstance(proposal.get("reason"), str) or not proposal["reason"].strip()):
        gaps.append("proposal not_applicable requires an evidenced small_fix under established requirements")
    if stage == "baseline_review" and not baseline_reviewable:
        gaps.append("baseline_review stage requires a complete factual baseline before user review")
    if stage in {"requirements_interview", "plan_confirmation", "implementation", "verification", "complete"}:
        if not (baseline_approved or (baseline_exempt and greenfield_progress)):
            gaps.append("later stages require valid baseline review or the evidenced greenfield exception")
        if stage in {"requirements_interview", "plan_confirmation"} and not baseline_reviewable:
            gaps.append("later stages require a complete factual baseline or evidenced greenfield start")
        # A factual revision is maintained throughout implementation. Reusing a
        # still-valid prior review does not require approving every new revision.
        # Mark invalidated reviews explicitly; a checker cannot infer semantics.
    if stage in IMPLEMENTATION_WORKFLOW_STAGES | {"complete"}:
        proposal = approvals.get("proposal_approval")
        if not isinstance(proposal, dict) or proposal.get("status") not in ("approved", "not_applicable"):
            gaps.append("implementation requires recorded Spec/Plan approval or evidenced small-fix scope")
        elif not isinstance(proposal.get("revision"), str) or not proposal["revision"].strip():
            gaps.append("proposal approval must identify the approved Spec/Plan revision")
        authorization = selected_task.get("implementation_authorization") if isinstance(selected_task, dict) else None
        if not isinstance(authorization, dict) or authorization.get("status") != "approved":
            gaps.append("implementation requires separate task implementation authorization")
        else:
            if not isinstance(authorization.get("evidence"), str) or not authorization["evidence"].strip():
                gaps.append("implementation authorization evidence is missing")
            else:
                try:
                    if not safe_path(root, authorization["evidence"]).is_file():
                        gaps.append("implementation authorization evidence does not exist")
                except ConfigError:
                    gaps.append("implementation authorization evidence path is unsafe")
            if task_id and authorization.get("task_id") != task_id:
                gaps.append("implementation authorization must name the selected task")
            proposal = approvals.get("proposal_approval")
            if isinstance(proposal, dict) and authorization.get("plan_revision") != proposal.get("revision"):
                gaps.append("implementation authorization must match the approved Spec/Plan revision")
    if stage == "complete":
        if baseline_status not in ("complete", "approved"):
            gaps.append("complete stage requires a complete or approved factual baseline")
        if not isinstance(selected_task, dict) or selected_task.get("status") != "complete":
            gaps.append("complete stage requires the selected task to be complete")
    if mode == "discovery" and stage not in EARLY_WORKFLOW_STAGES:
        gaps.append("discovery mode is only available during takeover_discovery or baseline_review")
    return gaps


def implementation_gate(root, manifest, paths, task_id):
    workflow = manifest.get("workflow")
    if not isinstance(workflow, dict) or "stage" not in workflow:
        return None
    scopes = workflow.get("implementation_paths", [])
    if not isinstance(scopes, list):
        return output_check("implementation-gate", "fail", "declared implementation scopes",
                            {"gaps": ["workflow.implementation_paths is not an array"]}, required=True)
    scopes = [relative_scope(root, scope) for scope in scopes]
    changed = [path for path in paths if any(covered(path, scope) for scope in scopes)]
    if not changed:
        return output_check("implementation-gate", "pass", "declared implementation scopes", [],
                            limitations=["Only workflow.implementation_paths are classified as implementation; review scope accuracy."])
    stage = workflow.get("stage")
    gaps = []
    if stage not in IMPLEMENTATION_WORKFLOW_STAGES | {"complete"}:
        gaps.append("implementation-scope changes are not allowed in stage " + str(stage))
    task = next((item for item in manifest.get("tasks", []) if isinstance(item, dict) and item.get("id") == task_id), None)
    authorization = task.get("implementation_authorization") if isinstance(task, dict) else None
    if not isinstance(authorization, dict) or authorization.get("status") != "approved":
        gaps.append("selected task has no separate implementation authorization")
    evidence = authorization.get("evidence") if isinstance(authorization, dict) else None
    if not isinstance(evidence, str) or not evidence.strip():
        gaps.append("implementation authorization evidence is missing")
    return output_check("implementation-gate", "fail" if gaps else "pass",
                        "changed paths under declared implementation scopes",
                        {"changed_implementation_paths": changed, "stage": stage, "gaps": gaps or ["implementation authorization recorded"]},
                        required=True,
                        limitations=["The checker enforces declared scopes and evidence references; it cannot authenticate a human approval or discover undeclared source paths."])

def relative_scope(root, raw):
    """Normalize a manifest path so it can be compared with Git paths."""
    path = _relative_to_root(safe_path(root, raw, file_only=False), root).as_posix()
    return "" if path == "." else path

def lexical_path(root, raw):
    """Return an absolute path without resolving links for traversal pruning."""
    given = Path(normalize_manifest_path(raw))
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
        if excluded_path(root, current, excluded):
            continue
        try:
            children = list(current.iterdir())
        except OSError:
            raise
        for child in children:
            if excluded_path(root, child, excluded):
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
    entry = subprocess.run(prefix + ["ls-tree", "-z", "--full-tree", oid, "--", ":(literal)" + relative],
                           cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                           stdin=subprocess.DEVNULL, timeout=30)
    if entry.returncode:
        raise ConfigError("Git historical manifest discovery is unavailable")
    if not entry.stdout:
        return None
    if entry.stdout.split(b"\t", 1)[0].split()[1:2] != [b"blob"]:
        raise ConfigError("historical manifest is not a file")
    proc = subprocess.run(prefix + ["show", "--no-ext-diff", "--format=", oid + ":" + relative],
                          cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        raise ConfigError("Git historical manifest content is unavailable")
    data = parse_json(proc.stdout, "Git manifest " + oid + ":" + relative)
    if not isinstance(data, dict):
        raise ConfigError("historical manifest must be a JSON object")
    return data

def control_plane_check(root, manifest, manifest_path, mode, changed_paths, commit_ref=None, allow=False, submission_baseline=None):
    """Block control-plane edits unless explicitly approved outside the repository."""
    if git_is_shallow(root):
        raise ConfigError("commit validation requires full Git history; shallow checkout is not supported")
    if mode == "commit" and git_revision(root, "HEAD"):
        git_parent(root, "HEAD")
    protected = set(control_plane_paths(root, manifest, manifest_path))
    baseline_ref = "HEAD" if mode == "commit" else git_parent(root, commit_ref) if commit_ref else None
    baseline = manifest_from_git(root, baseline_ref, manifest_path) if baseline_ref else None
    if submission_baseline is not None:
        submission_baseline["manifest"] = baseline
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
    workflow = manifest.get("workflow")
    if workflow is not None:
        if not isinstance(workflow, dict):
            raise ConfigError("workflow must be an object")
        active_task = workflow.get("active_task")
        if not isinstance(active_task, str) or not active_task.strip():
            raise ConfigError("workflow.active_task must be a non-empty task ID")
        if active_task not in tasks:
            faults.append("workflow.active_task references unknown task: " + active_task)
        for field in ("active_baseline", "active_spec", "active_plan"):
            reference = workflow.get(field)
            if reference is None:
                continue
            if not isinstance(reference, str) or not reference.strip():
                raise ConfigError("workflow." + field + " must be a non-empty document ID")
            if reference not in docs:
                faults.append("workflow." + field + " references unknown document: " + reference)
            elif not safe_path(root, docs[reference]["path"]).is_file():
                faults.append("workflow." + field + " references missing document: " + reference)
    excluded = build_exclude_specs(root, manifest["exclude_paths"])
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
            baseline_entry = manifest.get("baseline")
            planned_greenfield_path = (
                isinstance(baseline_entry, dict) and baseline_entry.get("origin") == "greenfield"
                and baseline_entry.get("status") in ("not_applicable", "partial")
                and isinstance(baseline_entry.get("implementation_paths"), list)
                and raw in baseline_entry["implementation_paths"])
            if not path.exists() and not planned_greenfield_path:
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
        if any("\x00" in arg for arg in argv):
            raise ConfigError("check command contains NUL byte: " + ident)
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
        artifact_links = task.get("artifact_links")
        if artifact_links is not None:
            if not isinstance(artifact_links, dict):
                raise ConfigError("task.artifact_links must be an object: " + ident)
            for link_name, document_id in artifact_links.items():
                if not isinstance(link_name, str) or not link_name.strip():
                    raise ConfigError("task.artifact_links keys must be non-empty strings: " + ident)
                if not isinstance(document_id, str) or not document_id.strip():
                    raise ConfigError("task.artifact_links values must be document IDs: " + ident)
                if document_id not in docs:
                    fault("task " + ident + " has unknown artifact link " + link_name + ": " + document_id)
                elif not safe_path(root, docs[document_id]["path"]).is_file():
                    fault("task " + ident + " artifact link points to missing document: " + document_id)
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
                if has_glob_magic(normalize_manifest_path(raw)):
                    raise ConfigError("documentation_impact.when_paths must be literal paths: " + raw)
                normalized = relative_scope(root, raw)
                common_parent = bool(normalized) and sum(
                    any(scope != normalized and covered(scope, normalized)
                        for scope in (relative_scope(root, source) for source in modules[module_id]["source_paths"]))
                    for module_id in task["module_ids"] if module_id in modules
                ) >= 2
                if not normalized:
                    fault("documentation_impact.when_paths cannot target project root: " + raw)
                elif not any(covered(normalized, allowed) for allowed in legal_trigger_scopes) and not common_parent:
                    fault("documentation_impact.when_paths is outside module/document scopes: " + raw)
        boolean(task.get("approval_required"), "task.approval_required")
        if task.get("status") not in ("planned", "in_progress", "blocked", "complete"):
            raise ConfigError("invalid task status: " + ident)
    if cycle(task_graph):
        fault("task dependency cycle")
    baseline = manifest["baseline"]
    if not isinstance(baseline, dict):
        raise ConfigError("baseline must be an object")
    baseline_status = baseline.get("status")
    provisional = baseline_status in ("not_applicable", "partial", "planned")
    workflow_stage = workflow.get("stage") if isinstance(workflow, dict) else None
    discovery_stage = mode == "discovery" and workflow_stage in EARLY_WORKFLOW_STAGES
    lifecycle_gaps = []
    if provisional:
        if baseline.get("origin") != "greenfield" and not (discovery_stage and baseline.get("origin") == "existing"):
            lifecycle_gaps.append("provisional baseline requires origin=greenfield; existing code needs discovery")
        if baseline_status == "planned" and not discovery_stage:
            lifecycle_gaps.append("planned baselines may only be checked in discovery mode")
        for field in ("reason", "source_revision", "scope"):
            if not isinstance(baseline.get(field), str) or not baseline[field].strip():
                lifecycle_gaps.append("provisional baseline missing " + field)
        implementation_paths = baseline.get("implementation_paths")
        if baseline.get("origin") == "greenfield" and (not isinstance(implementation_paths, list) or not implementation_paths):
            raise ConfigError("provisional baseline.implementation_paths must be a non-empty path array")
        for raw in implementation_paths or []:
            if has_glob_magic(normalize_manifest_path(raw)) or not relative_scope(root, raw):
                raise ConfigError("baseline.implementation_paths must be literal non-root paths")
            path = safe_path(root, raw, file_only=False)
            # Do not let exclude_paths hide implementation in the declared scope.
            if baseline_status == "not_applicable":
                files = [path] if path.is_file() else (
                    iter_module_paths(root, path, []) if path.is_dir() else [])
                if any(candidate.is_file() for candidate in files):
                    lifecycle_gaps.append("implementation exists; change baseline to partial or complete: " + raw)
        if mode == "handoff":
            lifecycle_gaps.append("handoff requires a complete or approved factual baseline")
        selected = tasks.get(task_id) if task_id else None
        if selected and selected.get("status") == "complete":
            lifecycle_gaps.append("completed task requires a complete or approved factual baseline")
    elif baseline_status not in ("complete", "approved"):
        fault("baseline not complete")
    if provisional or baseline.get("origin") == "greenfield" or discovery_stage:
        results.append(output_check(
            "baseline-lifecycle", "fail" if lifecycle_gaps else "pass",
            "declared baseline lifecycle",
            {"status": baseline_status, "completion_ready": baseline_status in ("complete", "approved"),
             "gaps": lifecycle_gaps}, required=True,
            limitations=["Provisional success permits ongoing work, not delivery. Only declared implementation paths are inspected; project origin and semantics require review."]))
    evidence = safe_path(root, baseline.get("evidence"))
    if not evidence.is_file():
        fault("baseline evidence missing")
    baseline_document_ids = baseline.get("document_ids")
    if baseline_document_ids is not None:
        if not isinstance(baseline_document_ids, list) or not baseline_document_ids or not all(isinstance(x, str) and x for x in baseline_document_ids):
            raise ConfigError("baseline.document_ids must be a non-empty document ID array")
        for document_id in baseline_document_ids:
            if document_id not in docs:
                fault("baseline references unknown document: " + document_id)
            elif not safe_path(root, docs[document_id]["path"]).is_file():
                fault("baseline references missing document: " + document_id)
    lifecycle_errors = workflow_lifecycle_gaps(root, workflow, baseline, tasks.get(task_id) if task_id else None, task_id, mode) if isinstance(workflow, dict) and "stage" in workflow else []
    if mode == "discovery" and not (isinstance(workflow, dict) and "stage" in workflow):
        lifecycle_errors.append("discovery mode requires an explicit workflow.stage; legacy manifests keep the compatibility path")
    if isinstance(workflow, dict) and "stage" in workflow:
        results.append(output_check(
            "workflow-lifecycle", "fail" if lifecycle_errors else "pass", "declared takeover stage and approval evidence",
            {"stage": workflow.get("stage"), "completion_ready": workflow.get("stage") == "complete" and baseline_status == "approved", "gaps": lifecycle_errors or ["lifecycle fields are consistent"]},
            required=True,
            limitations=["Approval records are declarations: the checker cannot authenticate a human or prove semantic completeness, user understanding, host loading, or undiscovered dependencies."]))
    else:
        results.append(output_check("workflow-lifecycle", "partial", "legacy manifest without stage lifecycle", "existing compatibility path retained", required=False,
                                    limitations=["This manifest does not receive automatic takeover-stage or implementation authorization gates until lifecycle fields are adopted."]))
    faults.extend(lifecycle_errors)
    approval_check = approval_contract_check(root, docs, workflow, tasks.get(task_id) if task_id else None, task_id) if isinstance(workflow, dict) else None
    if approval_check is not None:
        results.append(approval_check)
        sequence_check = approval_sequence_check(workflow, tasks.get(task_id) if task_id else None)
        if sequence_check is not None:
            results.append(sequence_check)
    results.append(output_check("manifest", "fail" if faults else "pass", "declared IDs, references, graph and baseline", faults or ["manifest validated"],
                                limitations=["Declared dependencies are not a discovered runtime graph; approval meaning and document semantics need review."]))
    for ident, entry in inventories.items():
        results.append(validate_inventory(root, ident, entry))
    if mode in ("change", "handoff", "commit", "committed"):
        if not task_id or task_id not in tasks:
            raise ConfigError("a known --task is required")
        task = tasks[task_id]
        gating = []
        approval_required_now = mode in ("handoff", "commit", "committed") or (
            mode == "change" and (workflow_stage is None or workflow_stage in IMPLEMENTATION_WORKFLOW_STAGES | {"complete"}))
        if task["approval_required"] and approval_required_now:
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
    path = path.replace("\\", "/").rstrip("/")
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
    exclude_specs = build_exclude_specs(root, manifest["exclude_paths"])
    allowed = []
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
    uncovered = [p for p in paths if not excluded_path(root, p, exclude_specs) and not any(covered(p, raw) for raw in allowed)]
    excluded = [p for p in paths if excluded_path(root, p, exclude_specs)]
    documentation_gaps = []
    changed = [p for p in paths if not excluded_path(root, p, exclude_specs)]
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

def verification_snapshot(root):
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    proc = subprocess.run(prefix + ["write-tree"], cwd=root, stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, stdin=subprocess.DEVNULL, timeout=30)
    tree = proc.stdout.decode("ascii", "replace").strip()
    if proc.returncode or not re.fullmatch(r"[a-fA-F0-9]{40}|[a-fA-F0-9]{64}", tree):
        raise ConfigError("Git cannot snapshot the index tree")
    return {"head": git_revision(root, "HEAD"), "tree": tree}


def verification_state_check(root, before):
    prefix = ["git", "-c", "safe.directory=" + str(root)]
    proc = subprocess.run(prefix + ["diff", "--cached", "--no-ext-diff", "--no-textconv", "--no-renames",
                                    "--name-only", "-z", before["tree"], "--"],
                          cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                          stdin=subprocess.DEVNULL, timeout=30)
    if proc.returncode:
        raise ConfigError("Git cannot inspect index drift after verification")
    index_paths = sorted(p.decode("utf-8", "surrogateescape") for p in proc.stdout.split(b"\0") if p)
    # A clean index diff already proves tree equality; compute a new OID only on drift.
    after = verification_snapshot(root) if index_paths else {"head": git_revision(root, "HEAD"), "tree": before["tree"]}
    dirty = unstaged_git_paths(root)
    drifted = before != after or bool(dirty)
    return output_check("verification-state", "fail" if drifted else "pass",
                        "HEAD, index tree and worktree after declared checks",
                        {"before": before, "after": after, "index_paths": index_paths,
                         "worktree_paths": dirty}, limitations=[
                            "Boundary snapshots detect persistent drift, not transient changes restored by hostile code, later hook races or sandbox escapes."
                        ])


class CheckCancelled(Exception):
    def __init__(self, signum):
        super().__init__("verification interrupted by signal " + str(signum))
        self.exit_code = 128 + signum


@contextmanager
def command_cancellation():
    previous = {}
    def cancel(signum, frame):
        raise CheckCancelled(signum)
    try:
        if threading.current_thread() is threading.main_thread():
            for name in ("SIGINT", "SIGTERM", "SIGBREAK"):
                signum = getattr(signal, name, None)
                if signum is not None:
                    previous[signum] = signal.getsignal(signum)
                    signal.signal(signum, cancel)
        yield
    finally:
        for signum, handler in previous.items():
            signal.signal(signum, handler)


class _WindowsProcessJob:
    """Own an ordinary Windows process family before its code can execute."""
    def __init__(self):
        import ctypes
        from ctypes import wintypes as w
        class Limits(ctypes.Structure):
            _fields_ = [("process_time", ctypes.c_longlong), ("job_time", ctypes.c_longlong),
                        ("flags", w.DWORD), ("minimum_working_set", ctypes.c_size_t),
                        ("maximum_working_set", ctypes.c_size_t), ("active_processes", w.DWORD),
                        ("affinity", ctypes.c_size_t), ("priority", w.DWORD), ("scheduling", w.DWORD)]
        class IO(ctypes.Structure):
            _fields_ = [(name, ctypes.c_ulonglong) for name in
                        ("read_ops", "write_ops", "other_ops", "read_bytes", "write_bytes", "other_bytes")]
        class ExtendedLimits(ctypes.Structure):
            _fields_ = [("basic", Limits), ("io", IO), ("process_memory", ctypes.c_size_t),
                        ("job_memory", ctypes.c_size_t), ("peak_process_memory", ctypes.c_size_t),
                        ("peak_job_memory", ctypes.c_size_t)]
        class ThreadEntry(ctypes.Structure):
            _fields_ = [("size", w.DWORD), ("usage", w.DWORD), ("thread_id", w.DWORD),
                        ("owner_pid", w.DWORD), ("base_priority", w.LONG),
                        ("delta_priority", w.LONG), ("flags", w.DWORD)]
        self.ctypes, self.thread_entry = ctypes, ThreadEntry
        self.kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        signatures = {
            "CreateJobObjectW": ([ctypes.c_void_p, w.LPCWSTR], w.HANDLE),
            "SetInformationJobObject": ([w.HANDLE, ctypes.c_int, ctypes.c_void_p, w.DWORD], w.BOOL),
            "AssignProcessToJobObject": ([w.HANDLE, w.HANDLE], w.BOOL),
            "OpenProcess": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "TerminateJobObject": ([w.HANDLE, w.UINT], w.BOOL),
            "CloseHandle": ([w.HANDLE], w.BOOL),
            "CreateToolhelp32Snapshot": ([w.DWORD, w.DWORD], w.HANDLE),
            "Thread32First": ([w.HANDLE, ctypes.POINTER(ThreadEntry)], w.BOOL),
            "Thread32Next": ([w.HANDLE, ctypes.POINTER(ThreadEntry)], w.BOOL),
            "OpenThread": ([w.DWORD, w.BOOL, w.DWORD], w.HANDLE),
            "ResumeThread": ([w.HANDLE], w.DWORD),
        }
        for name, (args, result) in signatures.items():
            function = getattr(self.kernel, name)
            function.argtypes, function.restype = args, result
        self.handle = self.kernel.CreateJobObjectW(None, None)
        if not self.handle:
            raise ctypes.WinError(ctypes.get_last_error())
        info = ExtendedLimits()
        info.basic.flags = 0x2000  # JOB_OBJECT_LIMIT_KILL_ON_JOB_CLOSE; handle is not inheritable.
        if not self.kernel.SetInformationJobObject(self.handle, 9, ctypes.byref(info), ctypes.sizeof(info)):
            error = ctypes.WinError(ctypes.get_last_error())
            self.close()
            raise error

    def attach_and_resume(self, pid):
        c, k = self.ctypes, self.kernel
        process = k.OpenProcess(0x0100 | 0x0001, False, pid)  # SET_QUOTA | TERMINATE
        if not process:
            raise c.WinError(c.get_last_error())
        try:
            if not k.AssignProcessToJobObject(self.handle, process):
                raise c.WinError(c.get_last_error())
        finally:
            k.CloseHandle(process)
        snapshot = k.CreateToolhelp32Snapshot(0x00000004, 0)  # TH32CS_SNAPTHREAD
        if snapshot == c.c_void_p(-1).value:
            raise c.WinError(c.get_last_error())
        resumed = 0
        try:
            entry = self.thread_entry()
            entry.size = c.sizeof(entry)
            present = k.Thread32First(snapshot, c.byref(entry))
            while present:
                if entry.owner_pid == pid:
                    thread = k.OpenThread(0x0002, False, entry.thread_id)  # SUSPEND_RESUME
                    if not thread:
                        raise c.WinError(c.get_last_error())
                    try:
                        if k.ResumeThread(thread) == 0xFFFFFFFF:
                            raise c.WinError(c.get_last_error())
                        resumed += 1
                    finally:
                        k.CloseHandle(thread)
                present = k.Thread32Next(snapshot, c.byref(entry))
        finally:
            k.CloseHandle(snapshot)
        if not resumed:
            raise OSError("cannot resume the owned Windows process")

    def terminate(self):
        if not self.kernel.TerminateJobObject(self.handle, 1):
            raise self.ctypes.WinError(self.ctypes.get_last_error())

    def close(self):
        if self.handle:
            self.kernel.CloseHandle(self.handle)
            self.handle = None


def run_declared_command(command, cwd, timeout_seconds):
    """Bound output and clean the owned process family on every exit path."""
    process = job = reader = None
    reader_started = False
    chunks = queue.Queue(maxsize=8)
    stop_reader = threading.Event()
    reader_finished = threading.Event()
    reader_failed = threading.Event()

    def read_output():
        try:
            while not stop_reader.is_set():
                chunk = process.stdout.read(OUTPUT_READ_CHUNK_BYTES)
                if not chunk:
                    break
                while not stop_reader.is_set():
                    try:
                        chunks.put(chunk, timeout=0.1)
                        break
                    except queue.Full:
                        continue
        except Exception:
            reader_failed.set()
        finally:
            reader_finished.set()

    start = time.monotonic()
    total_bytes = 0
    digest = hashlib.sha256()
    captured = bytearray()
    timed_out = False
    limit_exceeded = False
    cleanup_timed_out = False
    returncode = None

    def stop_process():
        nonlocal cleanup_timed_out
        stop_reader.set()
        if process is None:
            return
        try:
            if job is not None:
                job.terminate()
            else:
                os.killpg(process.pid, signal.SIGKILL)
        except ProcessLookupError:
            pass
        except OSError:
            cleanup_timed_out = True
        if job is not None and process.poll() is None:
            try:
                # Also covers a suspended child whose job assignment failed.
                process.kill()
            except OSError:
                if process.poll() is None:
                    cleanup_timed_out = True

    try:
        if os.name == "nt":
            job = _WindowsProcessJob()
            launch_options = {"creationflags": subprocess.CREATE_NEW_PROCESS_GROUP | 0x00000004}
        else:
            launch_options = {"start_new_session": True}
        process = subprocess.Popen(command, cwd=cwd, stdin=subprocess.DEVNULL,
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   shell=False, **launch_options)
        if job is not None:
            job.attach_and_resume(process.pid)
        reader = threading.Thread(target=read_output, name="engineering-check-output", daemon=True)
        reader.start()
        reader_started = True
        while not reader_finished.is_set() or not chunks.empty():
            remaining = timeout_seconds - (time.monotonic() - start)
            if remaining <= 0:
                timed_out = True
                break
            try:
                chunk = chunks.get(timeout=min(remaining, 0.1))
            except queue.Empty:
                continue
            total_bytes += len(chunk)
            digest.update(chunk)
            if len(captured) < MAX_CHECK_OUTPUT_BYTES:
                captured.extend(chunk[:MAX_CHECK_OUTPUT_BYTES - len(captured)])
            if total_bytes > MAX_CHECK_OUTPUT_BYTES:
                limit_exceeded = True
                break
        if timed_out or limit_exceeded or reader_failed.is_set():
            stop_process()
        try:
            wait_limit = 2 if timed_out or limit_exceeded or reader_failed.is_set() else max(0, timeout_seconds - (time.monotonic() - start))
            returncode = process.wait(timeout=wait_limit)
        except subprocess.TimeoutExpired:
            timed_out = True
            stop_process()
            try:
                returncode = process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                cleanup_timed_out = True
    finally:
        pending = sys.exc_info()[1]
        stop_process()
        if process is not None:
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                cleanup_timed_out = True
        if job is not None:
            job.close()
        if reader_started:
            reader.join(timeout=2)
        reader_stalled = reader_started and reader.is_alive()
        if process is not None and process.stdout is not None and not reader_stalled:
            process.stdout.close()
        if pending is not None:
            pending.cleanup_timed_out = cleanup_timed_out
            pending.reader_stalled = reader_stalled
    return {
        "returncode": returncode,
        "output": bytes(captured),
        "output_bytes": total_bytes,
        "output_sha256": digest.hexdigest(),
        "timed_out": timed_out,
        "output_limit_exceeded": limit_exceeded,
        "reader_failed": reader_failed.is_set(),
        "reader_stalled": reader_stalled,
        "cleanup_timed_out": cleanup_timed_out,
    }


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
            result = run_declared_command(check["command"], cwd, check["timeout_seconds"])
            evidence = {"command_sha256": hashlib.sha256(json.dumps(check["command"]).encode()).hexdigest(),
                        "working_directory": check.get("working_directory", "."),
                        "returncode": result["returncode"], "duration_seconds": round(time.monotonic()-start, 3),
                        "output_bytes": result["output_bytes"], "output_sha256": result["output_sha256"],
                        "output_limit_bytes": MAX_CHECK_OUTPUT_BYTES,
                        "output_limit_exceeded": result["output_limit_exceeded"],
                        "timed_out": result["timed_out"],
                        "reader_failed": result["reader_failed"],
                        "reader_stalled": result["reader_stalled"],
                        "output_complete": not (result["timed_out"] or result["output_limit_exceeded"] or result["reader_failed"] or result["reader_stalled"]),
                        "cleanup_timed_out": result["cleanup_timed_out"]}
            status = "pass" if result["returncode"] == 0 and not result["timed_out"] and not result["output_limit_exceeded"] and not result["reader_failed"] and not result["reader_stalled"] and not result["cleanup_timed_out"] else "fail"
            if status == "pass" and re.search(rb"(?im)(?:skipped[=:]\s*[1-9]\d*|[1-9]\d*\s+skipped\b|#\s*SKIP\b)", result["output"]):
                status = "partial"
                evidence["skip_marker_detected"] = True
            results.append(output_check(ident, status, "fresh invocation", evidence, required,
                                        ["Raw command output and argv are omitted to avoid leaking secrets. Common skip summaries are detected, but the absence of a marker cannot prove no checks were skipped."]))
        except subprocess.TimeoutExpired:
            results.append(output_check(ident, "fail", "fresh invocation", {"timeout_seconds": check["timeout_seconds"]}, required))
        except (ConfigError, OSError, ValueError):
            results.append(output_check(ident, "unsupported", "fresh invocation", "declared executable unavailable", required))
    return results

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--mode", required=True, choices=("discovery", "baseline", "change", "handoff", "commit", "committed"))
    parser.add_argument("--base")
    parser.add_argument("--commit-ref")
    parser.add_argument("--task")
    parser.add_argument("--run-checks", action="store_true")
    parser.add_argument("--allow-control-plane-change", action="store_true",
                        help="allow protected manifest/checker changes only with external approval")
    parser.add_argument("--require-approval-contract", type=int, choices=(1,),
                        help="require approval contract capability 1; older checkers must reject this invocation")
    parser.add_argument("--report")
    args = parser.parse_args(argv)
    task_id = args.task or os.environ.get("ENGINEERING_TASK_ID")
    report = {"tool_version": VERSION, "mode": args.mode, "required_checks_satisfied": False, "checks": [], "summary": "", "changed_paths": [], "errors": [], "verified_tree": None, "verification_head": None}
    # These modes must positively prove the submitted tree is safe to run;
    # exceptions and incomplete history leave command execution disabled.
    commands_allowed = args.mode not in ("commit", "committed")
    snapshot = None
    cancelled_exit = None
    submission_baseline = {}
    try:
        root = safe_root(args.root)
        if args.mode in ("commit", "committed"):
            snapshot = verification_snapshot(root)
        manifest = read_json(safe_path(root, args.manifest))
        if not isinstance(manifest, dict):
            raise ConfigError("manifest must be a JSON object")
        if args.require_approval_contract is not None:
            capability = manifest.get("workflow", {}).get("approval_policy") if isinstance(manifest.get("workflow"), dict) else None
            if not isinstance(capability, dict) or capability.get("record_contract") != args.require_approval_contract:
                raise ConfigError("requested approval contract is not declared in this manifest")
        if task_id is None and isinstance(manifest.get("workflow"), dict):
            task_id = manifest["workflow"].get("active_task")
        results, docs, modules, tasks, declared = validate(root, manifest, args.mode, task_id)
        report["checks"].extend(results)
        if args.mode in ("change", "handoff"):
            if not args.base:
                raise ConfigError("--base is required in change and handoff modes")
            try:
                report["changed_paths"], check = change_check(root, manifest, docs, modules, tasks, task_id, args.base)
                report["checks"].append(check)
                gate = implementation_gate(root, manifest, report["changed_paths"], task_id)
                if gate is not None:
                    report["checks"].append(gate)
            except (ConfigError, OSError, subprocess.TimeoutExpired):
                report["checks"].append(output_check("change-scope", "unsupported", "Git change discovery", "Git or requested base unavailable"))
        elif args.mode == "commit":
            try:
                report["changed_paths"], check = change_check(root, manifest, docs, modules, tasks, task_id,
                                                               paths=staged_git_paths(root), rule_id="commit-scope")
                control_check = control_plane_check(root, manifest, args.manifest, args.mode,
                                                    report["changed_paths"], allow=args.allow_control_plane_change,
                                                    submission_baseline=submission_baseline)
                report["checks"].append(control_check)
                gate = implementation_gate(root, manifest, report["changed_paths"], task_id)
                if gate is not None:
                    report["checks"].append(gate)
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
                                                    allow=args.allow_control_plane_change,
                                                    submission_baseline=submission_baseline)
                report["checks"].append(control_check)
                gate = implementation_gate(root, manifest, report["changed_paths"], task_id)
                if gate is not None:
                    report["checks"].append(gate)
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
        if args.mode in ("change", "handoff", "commit", "committed") and relative_scope(root, args.manifest) in report["changed_paths"] and not any(
                item["required"] and item["status"] != "pass" for item in report["checks"]):
            try:
                history_check = approval_policy_history_check(root, manifest, args.manifest, args.mode, args.base, args.commit_ref,
                                                             args.allow_control_plane_change, submission_baseline)
                if history_check is not None:
                    report["checks"].append(history_check)
            except (ConfigError, OSError, subprocess.TimeoutExpired) as exc:
                report["checks"].append(output_check("approval-policy-history", "unsupported", "previously enabled approval policy", str(exc), True))
        if any(item["required"] and item["status"] != "pass" for item in report["checks"]
               if item["rule_id"] in ("approval-evidence", "approval-sequence", "approval-policy-history")):
            commands_allowed = False
        reason = None if commands_allowed else "not run; submitted-tree validation did not pass"
        with command_cancellation():
            report["checks"].extend(run_checks(root, declared, args.run_checks and commands_allowed, forced, reason))
    except (CheckCancelled, KeyboardInterrupt) as exc:
        cancelled_exit = exc.exit_code if isinstance(exc, CheckCancelled) else 130
        report["checks"].append(output_check("interrupted", "fail", "verification cancelled",
                                             {"exit_code": cancelled_exit,
                                              "cleanup_timed_out": getattr(exc, "cleanup_timed_out", False),
                                              "reader_stalled": getattr(exc, "reader_stalled", False)}))
    except (ConfigError, OSError, UnicodeError, TypeError, KeyError) as exc:
        report["errors"].append(str(exc))
    finally:
        if snapshot is not None:
            try:
                report["checks"].append(verification_state_check(root, snapshot))
            except (ConfigError, OSError, subprocess.TimeoutExpired) as exc:
                report["checks"].append(output_check("verification-state", "unsupported",
                                                     "post-check Git state discovery", str(exc)))
    required = [x for x in report["checks"] if x["required"]]
    report["required_checks_satisfied"] = bool(required) and not report["errors"] and all(x["status"] == "pass" for x in required)
    if report["required_checks_satisfied"] and snapshot is not None:
        report["verified_tree"] = snapshot["tree"]
        report["verification_head"] = snapshot["head"]
    if args.mode == "discovery" and report["required_checks_satisfied"]:
        report["summary"] = "discovery checks satisfied; this does not mean the Global Baseline is complete or approved"
    else:
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
            report["verified_tree"] = None
            report["verification_head"] = None
            report["summary"] = "required checks not satisfied"
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if cancelled_exit is not None:
        return cancelled_exit
    if report["required_checks_satisfied"]:
        return 0
    if report["errors"] or any(x["status"] in ("error", "unsupported") for x in required):
        return 2
    return 1

if __name__ == "__main__":
    raise SystemExit(main())

