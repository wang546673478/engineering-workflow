#!/usr/bin/env python3
"""Merge project guidance into AGENTS.md and optional native-agent pointers."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import re
import stat
import sys

START = "<!-- engineering-workflow:start -->"
END = "<!-- engineering-workflow:end -->"
TEMPLATE = Path(__file__).resolve().parents[1] / "assets/templates/AGENTS.engineering.md"


def is_link(path):
    if path.is_symlink():
        return True
    try:
        attributes = getattr(path.lstat(), "st_file_attributes", 0)
    except FileNotFoundError:
        return False
    return bool(attributes & getattr(stat, "FILE_ATTRIBUTE_REPARSE_POINT", 0x400))


def project_root(raw):
    path = Path(raw).absolute()
    if any(is_link(parent) for parent in (path, *path.parents)):
        raise ValueError("project root traverses a symlink or junction")
    if not path.is_dir():
        raise ValueError("project root must be an existing directory")
    return path.resolve()


def safe_relative(root: Path, raw: str) -> Path:
    candidate = Path(raw)
    if not raw.strip() or candidate.is_absolute() or candidate.drive or ".." in candidate.parts or any(c in raw for c in "\r\n\x00"):
        raise ValueError(f"expected project-relative path: {raw!r}")
    path = root / candidate
    cursor = root
    for part in candidate.parts:
        cursor = cursor / part
        if is_link(cursor):
            raise ValueError(f"symlink or junction target is not allowed: {raw}")
    if not path.resolve().is_relative_to(root):
        raise ValueError(f"path escapes project root: {raw}")
    return path


def block(manifest: str, state_dir: str, skill: str) -> str:
    values = {"MANIFEST": manifest, "STATE_DIR": state_dir, "SKILL_SOURCE": skill}
    if any(not value.strip() or any(c in value for c in "\r\n\x00") or START in value or END in value for value in values.values()):
        raise ValueError("guidance parameters must be non-empty single-line values")
    return re.sub(r"\{\{(MANIFEST|STATE_DIR|SKILL_SOURCE)\}\}", lambda match: values[match[1]], TEMPLATE.read_text(encoding="utf-8")).rstrip("\r\n")


def adapter_block(path: Path, canonical: Path) -> str:
    relative = Path(os.path.relpath(canonical, path.parent)).as_posix()
    return "\n".join([
        START,
        "## Engineering Workflow",
        "",
        f"工程任务开始或恢复时，先读取并遵循 [项目工程规则]({relative}) 的 Engineering Workflow 段及其指向的 skill 和任务状态文件。",
        "本文件仅作入口；流程和进度以这些权威文件为准。",
        END,
    ])


def prepare(path: Path, content: str) -> bytes:
    if path.exists() and (not path.is_file() or path.stat().st_nlink > 1):
        raise ValueError(f"target must be a regular, unshared file: {path}")
    existing = path.read_bytes() if path.exists() else b""
    text = existing.decode("utf-8-sig")
    start, end = START.encode(), END.encode()
    newline = b"\r\n" if b"\r\n" in existing else b"\n"
    rendered = content.encode("utf-8").replace(b"\n", newline)
    if start in existing or end in existing:
        marker_text = existing.removeprefix(b"\xef\xbb\xbf")
        standalone = all(re.search(rb"(?m)^" + re.escape(marker) + rb"\r?$", marker_text) for marker in (start, end))
        if existing.count(start) != 1 or existing.count(end) != 1 or existing.index(start) >= existing.index(end) or not standalone:
            raise ValueError(f"invalid managed block markers: {path}")
        return existing[:existing.index(start)] + rendered + existing[existing.index(end) + len(end):]
    if re.search(r"(?im)^#{1,6}\s+engineering[ -]workflow\s*$", text):
        raise ValueError(f"existing unmarked workflow section needs manual merge: {path}")
    separator = b"" if not existing else (newline if existing.endswith(b"\n") else newline * 2)
    return existing + separator + rendered + newline


def update(path: Path, content: str) -> bool:
    updated = prepare(path, content)
    if path.exists() and path.read_bytes() == updated:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(updated)
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=".")
    parser.add_argument("--file", action="append", default=[], help="additional native instruction file; AGENTS.md is always included")
    parser.add_argument("--manifest", default="engineering-manifest.json")
    parser.add_argument("--state-dir", default="planning")
    parser.add_argument("--skill", default="从宿主 skills 清单定位 engineering-workflow/SKILL.md")
    args = parser.parse_args(argv)
    try:
        root = project_root(args.root)
        safe_relative(root, args.manifest)
        safe_relative(root, args.state_dir)
        canonical = root / "AGENTS.md"
        rendered = block(args.manifest, args.state_dir, args.skill)
        pending = {}
        for raw in ["AGENTS.md", *args.file]:
            path = safe_relative(root, raw)
            content = rendered if path == canonical else adapter_block(path, canonical)
            pending[path] = prepare(path, content)
        # Validate every target before writing any. OS write failures may leave
        # earlier files updated; report them and allow an idempotent rerun.
        for path, updated in pending.items():
            if path.exists() and path.read_bytes() == updated:
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(updated)
            print(path.relative_to(root).as_posix())
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
