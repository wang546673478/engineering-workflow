#!/usr/bin/env python3
"""Extract main-schema SQLite metadata read-only; never read business rows."""
from __future__ import annotations
import argparse
from contextlib import closing
import hashlib
import json
from pathlib import Path
import sqlite3
import sys

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def regular_path(path):
    original = path.absolute()
    cursor = Path(original.anchor)
    for component in original.parts[1:]:
        cursor = cursor / component
        if cursor.is_symlink() or bool(getattr(cursor, "is_junction", lambda: False)()):
            raise ValueError("symlink paths are not allowed")
    return original.resolve()

def extract(path):
    resolved = regular_path(Path(path))
    if not resolved.is_file():
        raise ValueError("database must exist")
    sources = [resolved]
    wal = resolved.with_name(resolved.name + "-wal")
    if wal.exists():
        sources.append(wal)
    before = {str(p): digest(p) for p in sources}
    items = []
    # immutable disallows sidecar writes for ordinary snapshots. Active WAL is
    # outside this extractor's supported scope rather than silently ignored.
    if wal.exists():
        raise ValueError("active WAL database unsupported; use an explicit checkpointed schema snapshot")
    uri = resolved.as_uri() + "?mode=ro&immutable=1"
    with closing(sqlite3.connect(uri, uri=True)) as db:
        db.execute("PRAGMA query_only=ON")
        for name, kind in db.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view') AND substr(name,1,7) != 'sqlite_' ORDER BY name"):
            quoted = '"' + name.replace('"', '""') + '"'
            rows = db.execute("PRAGMA main.table_xinfo(" + quoted + ")").fetchall()
            details = [{"name": row[1], "type": row[2], "not_null": bool(row[3]), "default": row[4], "primary_key": row[5], "hidden": row[6]} for row in rows]
            items.append({"id": name, "object_kind": kind, "fields": [x["name"] for x in details], "field_details": details})
    if any(digest(p) != before[str(p)] for p in sources):
        raise ValueError("database changed during extraction")
    return {"kind": "database", "provenance": {"type": "sqlite-metadata", "scope": "main schema tables/views and table_xinfo fields in a checkpointed SQLite file",
            "complete": True, "evidence": "read-only main schema extraction; no business rows", "source_files": [{"path": str(p), "sha256": before[str(p)]} for p in sources]}, "items": items}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("database")
    parser.add_argument("--output")
    args = parser.parse_args(argv)
    try:
        path = regular_path(Path(args.database))
        data = extract(path)
        payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if args.output:
            out = regular_path(Path(args.output))
            if out == path or out in (path.with_name(path.name + "-wal"), path.with_name(path.name + "-shm")):
                raise ValueError("output must not replace database or sidecars")
            if out.exists():
                raise ValueError("output must be a new file; refusing overwrite")
            with out.open("x", encoding="utf-8") as output:
                output.write(payload)
        else:
            sys.stdout.write(payload)
        return 0
    except (OSError, sqlite3.Error, ValueError) as exc:
        sys.stderr.write("extract_sqlite: " + str(exc) + "\n")
        return 2

if __name__ == "__main__":
    raise SystemExit(main())

