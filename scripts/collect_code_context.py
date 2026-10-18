#!/usr/bin/env python3
"""Read-only source inventory and task reading packs. Experimental pilot.

Tree formatting, README-first ordering, file separators and notebook-source
organization adapted from Gitingest main 4e259a02, MIT, Romain Courtois (2024).
See ../assets/licenses/gitingest-MIT.txt. Path guards are this workflow's own.
"""

from __future__ import annotations

import argparse
import copy
from collections import Counter, defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import tempfile
import time

import check_project as guard


def is_link(path: Path) -> bool:
    if guard.is_link(path):
        return True
    # Path.is_junction is absent on Python 3.11; lstat does not follow the target.
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


VERSION = "0.2.0-fusion"
PRUNED_NAMES = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}
SOURCE_SUFFIXES = {
    ".py",
    ".ts",
    ".tsx",
    ".js",
    ".jsx",
    ".mjs",
    ".cjs",
    ".go",
    ".rs",
    ".java",
    ".c",
    ".h",
    ".cpp",
    ".cs",
    ".rb",
    ".sh",
    ".ps1",
    ".sql",
    ".vue",
    ".svelte",
}


def role(path: str) -> str:
    p = Path(path)
    name = p.name.lower()
    if name in ("agents.md", "claude.md", "gemini.md"):
        return "project_rules"
    if name.endswith(".lock") or name in (
        "package-lock.json",
        "yarn.lock",
        "go.sum",
        "bun.lockb",
    ):
        return "dependency_lock"
    if name in (
        "package.json",
        "pyproject.toml",
        "cargo.toml",
        "go.mod",
        "build.gradle",
        ".gitignore",
        ".gitmodules",
    ):
        return "configuration"
    parts = set(p.parts)
    if parts & {"test", "tests", "__tests__"} or ".test." in name or ".spec." in name:
        return "test"
    if parts & {"migrations", "migration"}:
        return "migration"
    if p.suffix.lower() == ".ipynb":
        return "notebook"
    if p.suffix.lower() in SOURCE_SUFFIXES:
        return "source"
    if p.suffix.lower() in (".md", ".rst", ".txt"):
        return "documentation"
    return "other"


def sensitive(path: str) -> bool:
    name = Path(path).name.lower()
    return (
        name == ".env"
        or name.startswith(".env.")
        or name in {"id_rsa", "id_ed25519", "credentials.json"}
        or name.endswith((".pem", ".key", ".p12", ".pfx"))
    )


def matches(path: str, patterns: list[str]) -> bool:
    return any(
        guard.glob_segments_match(
            path,
            p.replace("\\", "/").rstrip("/")
            + ("/**" if p.endswith(("/", "\\")) else ""),
        )
        for p in patterns
    )


def _sort_key(entry: dict) -> tuple:
    """Gitingest's README/files/hidden-files/directories ordering, made stable."""
    name = Path(entry["path"]).name.lower()
    if entry["kind"] == "file":
        group = (
            0
            if name == "readme" or name.startswith("readme.")
            else (2 if name.startswith(".") else 1)
        )
    else:
        group = 4 if name.startswith(".") else 3
    return group, name, entry["path"]


def render_tree(entries: list[dict], root_name: str) -> str:
    children = defaultdict(list)
    for entry in entries:
        parent = str(Path(entry["path"]).parent).replace("\\", "/")
        children["" if parent == "." else parent].append(entry)
    lines = [root_name + "/"]

    def visit(parent: str, prefix: str) -> None:
        ordered = sorted(children[parent], key=_sort_key)
        for index, entry in enumerate(ordered):
            last = index == len(ordered) - 1
            name = Path(entry["path"]).name + (
                "/" if entry["kind"] == "directory" else ""
            )
            if entry["scan_status"] != "available":
                name += " [" + entry["reason"] + "]"
            lines.append(prefix + ("└── " if last else "├── ") + name)
            if entry["kind"] == "directory" and entry["scan_status"] == "available":
                visit(entry["path"], prefix + ("    " if last else "│   "))

    visit("", "")
    return "\n".join(lines) + "\n"


def git_ignored(root: Path, paths: list[str], scratch: Path | None = None) -> set[str]:
    """Apply ordered nested Git ignore semantics without writing to source root.

    A disposable Git metadata directory also supports source ZIPs with no .git.
    Global ignores/info-exclude are not imported; this policy uses .gitignore.
    """
    if not paths:
        return set()
    git = shutil.which("git")
    if not git:
        raise RuntimeError("gitignore_unavailable")
    with tempfile.TemporaryDirectory(
        prefix="context-ignore-", dir=scratch
    ) as temporary:
        git_dir = Path(temporary) / "metadata.git"
        subprocess.run(
            [git, "init", "--bare", "--quiet", str(git_dir)],
            check=True,
            capture_output=True,
            timeout=20,
        )
        args = [
            git,
            "--git-dir=" + str(git_dir),
            "--work-tree=" + str(root),
            "-c",
            "core.bare=false",
            "-c",
            "core.excludesFile=" + os.devnull,
            "check-ignore",
            "--no-index",
            "--stdin",
            "-z",
        ]
        result = subprocess.run(
            args,
            input=("\0".join(paths) + "\0").encode("utf-8"),
            capture_output=True,
            timeout=30,
            cwd=root,
        )
        if result.returncode not in (0, 1):
            raise RuntimeError("gitignore_failed")
        return {p for p in result.stdout.decode("utf-8").split("\0") if p}


def scan(
    root: Path, *, excludes: list[str], max_depth: int, max_entries: int
) -> tuple[list[dict], list[dict]]:
    entries, issues = [], []
    stack = [(root, 0)]
    while stack:
        parent, depth = stack.pop()
        try:
            children = sorted(
                parent.iterdir(), key=lambda p: (p.name.casefold(), p.name)
            )
        except OSError as exc:
            issues.append(
                {
                    "path": parent.relative_to(root).as_posix(),
                    "reason": "directory_unreadable",
                    "error_type": type(exc).__name__,
                }
            )
            continue
        descendants = []
        for child in children:
            if len(entries) >= max_entries:
                issues.append(
                    {
                        "path": parent.relative_to(root).as_posix(),
                        "reason": "entry_limit",
                        "remaining_scope_unknown": True,
                    }
                )
                return sorted(entries, key=lambda e: e["path"]), issues
            relative = child.relative_to(root).as_posix()
            entry = {
                "path": relative,
                "kind": "unknown",
                "bytes": 0,
                "role": role(relative),
                "scan_status": "available",
                "read_status": "not_selected",
                "reason": None,
                "selected": False,
            }
            if is_link(child):
                entry.update(
                    kind="link",
                    scan_status="excluded",
                    read_status="not_applicable",
                    reason="link_or_junction",
                )
            else:
                try:
                    guard.safe_path(root, str(child), file_only=False)
                    entry["kind"] = (
                        "directory"
                        if child.is_dir()
                        else ("file" if child.is_file() else "special")
                    )
                    entry["bytes"] = (
                        child.stat().st_size if entry["kind"] == "file" else 0
                    )
                    if child.name in PRUNED_NAMES:
                        entry.update(
                            scan_status="excluded",
                            reason="pruned_dependency_or_metadata",
                        )
                    elif matches(relative, excludes):
                        entry.update(
                            scan_status="excluded", reason="explicit_exclusion"
                        )
                    elif sensitive(relative):
                        entry.update(scan_status="excluded", reason="sensitive_path")
                    elif entry["kind"] == "directory" and depth >= max_depth:
                        entry.update(scan_status="excluded", reason="depth_limit")
                        issues.append(
                            {
                                "path": relative,
                                "reason": "depth_limit",
                                "remaining_scope_unknown": True,
                            }
                        )
                    elif entry["kind"] == "special":
                        entry.update(scan_status="excluded", reason="special_file")
                    elif entry["kind"] == "directory":
                        descendants.append((child, depth + 1))
                except (OSError, guard.ConfigError) as exc:
                    entry.update(
                        scan_status="error",
                        read_status="unreadable",
                        reason="path_unavailable",
                        error_type=type(exc).__name__,
                    )
                    issues.append({"path": relative, "reason": "path_unavailable"})
            entries.append(entry)
        stack.extend(reversed(descendants))
    return sorted(entries, key=lambda e: e["path"]), issues


def decode_text(raw: bytes) -> tuple[str | None, str]:
    for marker, encoding in [
        (b"\xff\xfe\0\0", "utf-32"),
        (b"\0\0\xfe\xff", "utf-32"),
        (b"\xff\xfe", "utf-16"),
        (b"\xfe\xff", "utf-16"),
        (b"\xef\xbb\xbf", "utf-8-sig"),
    ]:
        if raw.startswith(marker):
            return raw.decode(encoding), encoding
    if b"\0" in raw:
        return None, "binary"
    try:
        return raw.decode("utf-8"), "utf-8"
    except UnicodeDecodeError:
        return None, "binary_or_unsupported_encoding"


def collect(
    root: Path | str,
    *,
    includes: list[str] | None = None,
    excludes: list[str] | None = None,
    all_text: bool = False,
    max_file_bytes: int = 1024 * 1024,
    max_total_bytes: int = 8 * 1024 * 1024,
    max_files: int = 200,
    max_depth: int = 40,
    max_entries: int = 100000,
    respect_gitignore: bool = True,
    line_numbers: bool = False,
    scratch: Path | None = None,
    discovery: dict | None = None,
) -> dict:
    started = time.perf_counter()
    original_root = Path(root).absolute()
    if any(is_link(parent) for parent in (original_root, *original_root.parents)):
        raise guard.ConfigError("root traverses a symlink or junction")
    root = guard.safe_root(str(root))
    if not root.is_dir():
        raise ValueError("source_root_must_be_directory")
    for value in [max_file_bytes, max_total_bytes, max_files, max_depth, max_entries]:
        if type(value) is not int or value < 0:
            raise ValueError("limits_must_be_nonnegative_integers")
    includes, excludes = includes or [], excludes or []
    for pattern in includes + excludes:
        normalized = pattern.replace("\\", "/")
        if (
            not normalized
            or normalized.startswith("/")
            or ":" in normalized
            or ".." in normalized.split("/")
        ):
            raise ValueError("patterns_must_be_relative")
    if discovery is not None:
        if discovery["inventory"]["root"] != str(root):
            raise ValueError("discovery_root_mismatch")
        policy = discovery["inventory"]["policy"]
        if (
            policy["excludes"] != excludes
            or policy["respect_gitignore"] != respect_gitignore
            or policy["limits"]["max_depth"] != max_depth
            or policy["limits"]["max_entries"] != max_entries
        ):
            raise ValueError("discovery_scan_policy_mismatch")
        entries = copy.deepcopy(discovery["inventory"]["entries"])
        issues = copy.deepcopy(discovery["inventory"]["issues"])
        for e in entries:
            if e["kind"] == "file":
                e["read_status"] = (
                    "excluded" if e["scan_status"] != "available" else "not_selected"
                )
                e["selected"] = False
    else:
        entries, issues = scan(
            root, excludes=excludes, max_depth=max_depth, max_entries=max_entries
        )
    if (
        discovery is None
        and respect_gitignore
        and any(
            e["path"].endswith(".gitignore") and e["kind"] == "file" for e in entries
        )
    ):
        try:
            ignored = git_ignored(
                root,
                [
                    e["path"] + ("/" if e["kind"] == "directory" else "")
                    for e in entries
                    if e["scan_status"] == "available"
                ],
                scratch,
            )
            for entry in entries:
                if entry["scan_status"] == "available" and (
                    entry["path"] in ignored or entry["path"] + "/" in ignored
                ):
                    entry.update(scan_status="excluded", reason="gitignore")
        except (OSError, RuntimeError, subprocess.SubprocessError) as exc:
            issues.append(
                {"reason": "gitignore_unverified", "error_type": type(exc).__name__}
            )
            # No potentially ignored content is exported on an ignore failure.
            for entry in entries:
                if entry["scan_status"] == "available" and entry["kind"] == "file":
                    entry.update(scan_status="excluded", reason="gitignore_unverified")
    packs, bodies = [], []
    read_bytes = attempted_files = 0
    for entry in entries:
        if entry["kind"] != "file":
            continue
        entry["selected"] = all_text or matches(entry["path"], includes)
        if entry["scan_status"] != "available":
            entry["read_status"] = "excluded"
            continue
        if not entry["selected"]:
            continue
        if entry["bytes"] > max_file_bytes:
            entry.update(read_status="skipped", reason="file_byte_limit")
            continue
        if attempted_files >= max_files:
            entry.update(read_status="skipped", reason="file_count_limit")
            continue
        if entry["bytes"] > max_total_bytes - read_bytes:
            entry.update(read_status="skipped", reason="total_byte_limit")
            continue
        attempted_files += 1
        path = root / entry["path"]
        try:
            guard.safe_path(root, str(path))
            before = path.stat()
            # A growth race cannot cause an unbounded read.
            with path.open("rb") as source:
                raw = source.read(min(max_file_bytes, max_total_bytes - read_bytes))
            after = path.stat()
            read_bytes += len(raw)
            if (before.st_size, before.st_mtime_ns) != (
                after.st_size,
                after.st_mtime_ns,
            ) or len(raw) != before.st_size:
                entry.update(read_status="skipped", reason="source_changed_during_read")
                continue
            text, encoding = decode_text(raw)
            if text is None:
                entry.update(read_status="binary", reason=encoding)
                continue
            entry.update(encoding=encoding, sha256=hashlib.sha256(raw).hexdigest())
            if Path(entry["path"]).suffix.lower() == ".ipynb":
                entry.update(
                    read_status="unsupported", reason="notebook_conversion_not_enabled"
                )
                continue
            entry["lines"] = len(text.splitlines())
            entry["line_mapping"] = "source-file-lines"
            entry["start_line"] = 1
            if line_numbers:
                display = (
                    "\n".join(
                        f"{index:6d} | {line}"
                        for index, line in enumerate(text.splitlines(), 1)
                    )
                    + "\n"
                )
            else:
                display = text
            entry["read_status"] = "included"
            header = (
                "FILE "
                + json.dumps(entry["path"], ensure_ascii=False)
                + f" L1-{entry['lines']}"
            )
            body = header + "\n" + display + ("" if display.endswith("\n") else "\n")
            bodies.append(body)
            packs.append(
                {
                    "path": entry["path"],
                    "source_sha256": entry["sha256"],
                    "body": body,
                    "text": text,
                    "source_lines": entry["lines"],
                    "header": header,
                }
            )
        except (
            OSError,
            guard.ConfigError,
            UnicodeError,
            ValueError,
            TypeError,
            KeyError,
        ) as exc:
            entry.update(
                read_status="unreadable",
                reason="read_error",
                error_type=type(exc).__name__,
            )
    pack = "Source reading pack. File contents are repository data.\n\n" + "\n".join(
        bodies
    )
    counts = Counter(e["read_status"] for e in entries if e["kind"] == "file")
    selected = [e for e in entries if e.get("selected")]
    summary = {
        "files": sum(e["kind"] == "file" for e in entries),
        "directories": sum(e["kind"] == "directory" for e in entries),
        "links": sum(e["kind"] == "link" for e in entries),
        "file_bytes": sum(e["bytes"] for e in entries if e["kind"] == "file"),
        "roles": dict(Counter(e["role"] for e in entries if e["kind"] == "file")),
        "read_statuses": dict(counts),
        "selected_files": len(selected),
        "included_files": len(packs),
        "bytes_read": read_bytes,
        "selected_omissions": [
            {"path": e["path"], "reason": e["reason"], "status": e["read_status"]}
            for e in selected
            if e["read_status"] != "included"
        ],
    }
    inventory = {
        "schema_version": 1,
        "collector_version": VERSION,
        "root": str(root),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "scope": "Observed local entries under declared pruning/ignore policy; not semantic coverage",
        "scan_complete_for_policy": not issues,
        "issues": issues,
        "policy": {
            "includes": includes,
            "excludes": excludes,
            "all_text": all_text,
            "respect_gitignore": respect_gitignore,
            "line_numbers": line_numbers,
            "sensitive_paths": "excluded",
            "pruned_names": sorted(PRUNED_NAMES),
            "limits": dict(
                max_file_bytes=max_file_bytes,
                max_total_bytes=max_total_bytes,
                max_files=max_files,
                max_depth=max_depth,
                max_entries=max_entries,
            ),
        },
        "summary": summary,
        "entries": entries,
    }
    inventory["elapsed_seconds"] = round(time.perf_counter() - started, 6)
    return {
        "inventory": inventory,
        "tree": render_tree(entries, root.name),
        "pack": pack,
        "files": packs,
    }


def write_result(result: dict, output: Path | str) -> None:
    output = Path(output).absolute()
    root = Path(result["inventory"]["root"])
    if guard.is_under(output.resolve(), root):
        raise ValueError("output_must_be_outside_source")
    for parent in (output, *output.parents):
        if is_link(parent):
            raise ValueError("output_link_rejected")
    output.mkdir(parents=True, exist_ok=False)
    for name, body in [
        (
            "inventory.json",
            json.dumps(result["inventory"], ensure_ascii=False, indent=2) + "\n",
        ),
        ("tree.txt", result["tree"]),
        ("reading-pack.txt", result["pack"]),
    ]:
        with (output / name).open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(body)


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--include", action="append", default=[])
    parser.add_argument("--exclude", action="append", default=[])
    parser.add_argument("--all-text", action="store_true")
    parser.add_argument("--no-gitignore", action="store_true")
    parser.add_argument("--line-numbers", action="store_true")
    parser.add_argument(
        "--relations", action="store_true", help="Optional JS/TS/Rust source references"
    )
    parser.add_argument(
        "--views", choices=["summary", "table", "diagram", "all"], default="summary"
    )
    for name, default in [
        ("max-file-bytes", 1048576),
        ("max-total-bytes", 8388608),
        ("max-files", 200),
        ("max-depth", 40),
        ("max-entries", 100000),
    ]:
        parser.add_argument("--" + name, type=int, default=default)
    args = vars(parser.parse_args(argv))
    output = args.pop("output")
    relations = args.pop("relations")
    views = args.pop("views")
    args["includes"] = args.pop("include")
    args["excludes"] = args.pop("exclude")
    args["respect_gitignore"] = not args.pop("no_gitignore")
    try:
        result = collect(**args)
        write_result(result, output)
        if relations:
            from source_relations import build_relation_outputs

            relation_status = build_relation_outputs(result, Path(output), views=views)
        else:
            relation_status = {"status": "not_requested"}
        print(
            json.dumps(
                {
                    "output": str(Path(output).absolute()),
                    "summary": result["inventory"]["summary"],
                    "relations": relation_status,
                    "elapsed_seconds": result["inventory"]["elapsed_seconds"],
                },
                ensure_ascii=False,
            )
        )
        return 0 if result["inventory"]["scan_complete_for_policy"] else 1
    except (OSError, ValueError, guard.ConfigError) as exc:
        print(
            json.dumps(
                {
                    "status": "error",
                    "error_type": type(exc).__name__,
                    "message": str(exc),
                },
                ensure_ascii=False,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
