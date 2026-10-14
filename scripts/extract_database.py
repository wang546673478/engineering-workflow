#!/usr/bin/env python3
"""Extract database metadata without reading business values.

The remote adapters use optional drivers and are only invoked explicitly. The
output is a portable metadata snapshot that the project checker can validate
offline. Connection strings are read from an environment variable and never
written to the snapshot.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
from urllib.parse import urlparse, unquote

TOOL_VERSION = "1.0"


QUERIES = {
    "mysql": (
        "SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_SCHEMA = %s ORDER BY TABLE_SCHEMA, TABLE_NAME",
        "SELECT TABLE_SCHEMA, TABLE_NAME, COLUMN_NAME, DATA_TYPE, ORDINAL_POSITION, IS_NULLABLE, COLUMN_DEFAULT FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_SCHEMA = %s ORDER BY TABLE_SCHEMA, TABLE_NAME, ORDINAL_POSITION",
    ),
    "postgresql": (
        "SELECT table_schema, table_name, table_type FROM information_schema.tables WHERE table_schema = COALESCE(%s, table_schema) AND table_schema NOT IN ('pg_catalog', 'information_schema') ORDER BY table_schema, table_name",
        "SELECT table_schema, table_name, column_name, data_type, ordinal_position, is_nullable, column_default FROM information_schema.columns WHERE table_schema = COALESCE(%s, table_schema) AND table_schema NOT IN ('pg_catalog', 'information_schema') ORDER BY table_schema, table_name, ordinal_position",
    ),
    "redis": ("INFO keyspace",),
}
QUERY_HASHES = {adapter: "\n".join(queries) for adapter, queries in QUERIES.items()}


class AdapterError(ValueError):
    pass


def canonical_items(items):
    return json.dumps(items, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def snapshot_digest(items):
    return hashlib.sha256(canonical_items(items).encode("utf-8")).hexdigest()


def _row(row, index, name):
    if isinstance(row, dict):
        return row[name]
    return row[index]


def _group_relational(table_rows, column_rows):
    tables = {}
    for row in table_rows:
        schema = str(_row(row, 0, "table_schema"))
        name = str(_row(row, 1, "table_name"))
        kind = str(_row(row, 2, "table_type")).lower()
        object_kind = "view" if "view" in kind else "table"
        ident = schema + "." + name
        tables[ident] = {"id": ident, "object_kind": object_kind, "fields": [], "field_details": []}
    for row in column_rows:
        schema = str(_row(row, 0, "table_schema"))
        table = str(_row(row, 1, "table_name"))
        ident = schema + "." + table
        if ident not in tables:
            continue
        detail = {
            "name": str(_row(row, 2, "column_name")),
            "type": str(_row(row, 3, "data_type")),
            "ordinal": int(_row(row, 4, "ordinal_position")),
            "nullable": str(_row(row, 5, "is_nullable")).upper() == "YES",
            "default": _row(row, 6, "column_default"),
        }
        tables[ident]["fields"].append(detail["name"])
        tables[ident]["field_details"].append(detail)
    return [tables[key] for key in sorted(tables)]


def _snapshot(adapter, scope, items, source_ref, query_hash):
    if adapter not in QUERY_HASHES:
        raise AdapterError("unknown adapter: " + adapter)
    safe_source = source_ref or "environment-provided connection"
    parsed = urlparse(safe_source)
    if parsed.scheme and parsed.hostname:
        safe_source = parsed.scheme + "://" + parsed.hostname
        if parsed.path and parsed.path != "/":
            safe_source += parsed.path
    return {
        "kind": "database",
        "tool_version": TOOL_VERSION,
        "provenance": {
            "type": adapter + "-metadata",
            "scope": scope,
            "complete": True,
            "evidence": "explicit read-only metadata extraction; no business values",
            "source_ref": safe_source,
            "captured_at": datetime.now(timezone.utc).isoformat(),
            "query_sha256": hashlib.sha256(query_hash.encode("utf-8")).hexdigest(),
            "snapshot_sha256": snapshot_digest(items),
            "source_files": [],
        },
        "items": items,
    }


def extract_mysql(connection, schema=None, source_ref=None):
    if not schema:
        raise AdapterError("MySQL schema is required")
    cursor = connection.cursor()
    try:
        table_query, column_query = QUERIES["mysql"]
        cursor.execute(table_query, (schema,))
        tables = cursor.fetchall()
        cursor.execute(column_query, (schema,))
        columns = cursor.fetchall()
    finally:
        cursor.close()
    return _snapshot("mysql", "MySQL information_schema tables and columns visible to this role in schema " + schema, _group_relational(tables, columns), source_ref or schema, QUERY_HASHES["mysql"])


def extract_postgresql(connection, schema=None, source_ref=None):
    cursor = connection.cursor()
    try:
        table_query, column_query = QUERIES["postgresql"]
        cursor.execute(table_query, (schema,))
        tables = cursor.fetchall()
        cursor.execute(column_query, (schema,))
        columns = cursor.fetchall()
    finally:
        cursor.close()
    return _snapshot("postgresql", "PostgreSQL information_schema tables and columns visible to this role; schema=" + (schema or "non-system schemas"), _group_relational(tables, columns), source_ref or schema, QUERY_HASHES["postgresql"])


def extract_redis(connection, source_ref=None):
    info = connection.info(section="keyspace")
    items = []
    for key in sorted(info):
        if not str(key).startswith("db"):
            continue
        values = info[key] if isinstance(info[key], dict) else {}
        details = []
        for field in ("keys", "expires", "avg_ttl"):
            if field in values:
                details.append({"name": field, "type": "integer", "value": values[field]})
        items.append({"id": "redis:" + str(key), "object_kind": "keyspace", "fields": [x["name"] for x in details], "field_details": details})
    return _snapshot("redis", "Redis connected-node INFO keyspace counters; no SCAN and no key/value reads; not a cluster-wide schema", items, source_ref, QUERY_HASHES["redis"])


def _connect(adapter, url):
    if not url:
        raise AdapterError("connection URL is missing")
    try:
        if adapter == "mysql":
            parsed = urlparse(url)
            if parsed.scheme != "mysql" or not parsed.hostname or parsed.query:
                raise AdapterError("MySQL requires mysql:// URL without unsupported query options")
            options = dict(host=parsed.hostname, port=parsed.port or 3306,
                           user=unquote(parsed.username or ""), password=unquote(parsed.password or ""),
                           database=unquote((parsed.path or "/").lstrip("/")) or None)
            try:
                import mysql.connector as driver
                return driver.connect(**options, connection_timeout=10)
            except ModuleNotFoundError:
                import pymysql as driver
                return driver.connect(**options, connect_timeout=10, read_timeout=30)
        if adapter == "postgresql":
            try:
                import psycopg as driver
            except ModuleNotFoundError:
                import psycopg2 as driver
            return driver.connect(url, connect_timeout=10)
        if adapter == "redis":
            import redis
            return redis.Redis.from_url(url, decode_responses=True, socket_connect_timeout=10, socket_timeout=30)
    except AdapterError:
        raise
    except ModuleNotFoundError as exc:
        raise AdapterError("optional driver is unavailable for " + adapter) from exc
    except Exception as exc:
        raise AdapterError("database connection failed for " + adapter) from exc
    raise AdapterError("unknown adapter: " + adapter)


def extract(adapter, connection, schema=None, source_ref=None):
    if adapter == "mysql":
        return extract_mysql(connection, schema, source_ref)
    if adapter == "postgresql":
        return extract_postgresql(connection, schema, source_ref)
    if adapter == "redis":
        return extract_redis(connection, source_ref)
    raise AdapterError("unknown adapter: " + adapter)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("adapter", choices=("sqlite", "mysql", "postgresql", "redis"))
    parser.add_argument("--url-env", default="ENGINEERING_DATABASE_URL")
    parser.add_argument("--database")
    parser.add_argument("--schema")
    parser.add_argument("--output", required=True)
    parser.add_argument("--update", action="store_true", help="atomically replace an existing snapshot produced by this tool")
    args = parser.parse_args(argv)
    connection = None
    try:
        if args.adapter == "sqlite":
            if not args.database:
                raise AdapterError("--database is required for SQLite")
            import extract_sqlite
            data = extract_sqlite.extract(args.database)
            url = None
        else:
            url = os.environ.get(args.url_env)
            connection = _connect(args.adapter, url)
            schema = args.schema
            if args.adapter == "mysql" and not schema and url:
                schema = unquote(urlparse(url).path.lstrip("/"))
            data = extract(args.adapter, connection, schema, url)
        import extract_sqlite
        output = extract_sqlite.regular_path(Path(args.output))
        if args.adapter == "sqlite":
            source = extract_sqlite.regular_path(Path(args.database))
            if output in (source, source.with_name(source.name + "-wal"), source.with_name(source.name + "-shm")):
                raise AdapterError("output must not replace database or sidecars")
        payload = json.dumps(data, ensure_ascii=False, indent=2) + "\n"
        if output.exists() and not args.update:
            raise AdapterError("output must be a new file; refusing overwrite (use --update for a generated snapshot)")
        if args.update:
            if not output.exists():
                raise AdapterError("--update requires an existing generated snapshot")
            try:
                existing = json.loads(output.read_text(encoding="utf-8-sig"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                raise AdapterError("--update target is not valid JSON") from exc
            if existing.get("tool_version") != TOOL_VERSION or existing.get("kind") != "database":
                raise AdapterError("--update target was not generated by this tool")
            fd, temporary = tempfile.mkstemp(prefix=output.name + ".", suffix=".tmp", dir=str(output.parent))
            try:
                with os.fdopen(fd, "w", encoding="utf-8") as handle:
                    handle.write(payload)
                    handle.flush()
                    os.fsync(handle.fileno())
                os.replace(temporary, output)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        else:
            with output.open("x", encoding="utf-8") as handle:
                handle.write(payload)
        return 0
    except (OSError, AdapterError, ValueError, sqlite3.Error) as exc:
        sys.stderr.write("extract_database: " + str(exc) + "\n")
        return 2
    except Exception:
        sys.stderr.write("extract_database: metadata extraction failed; check driver, permissions and schema\n")
        return 2
    finally:
        if connection is not None and hasattr(connection, "close"):
            try:
                connection.close()
            except Exception:
                pass


if __name__ == "__main__":
    raise SystemExit(main())
