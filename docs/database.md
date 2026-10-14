# Engineering Workflow Database Boundary

Status: `current`  
Last verified: `2026-10-14`

This skill repository has no application database. Its database-facing module is the metadata adapter boundary.

## Adapter inventory

| Adapter | Reads | Does not read | Completeness |
| --- | --- | --- | --- |
| SQLite | Schema tables, views, and fields from a checkpointed file | Business rows and active WAL state | Metadata scope only |
| MySQL | Visible `INFORMATION_SCHEMA` tables and columns | Business rows and credentials in snapshots | Metadata scope only |
| PostgreSQL | Visible `information_schema` tables and columns | Business rows and credentials in snapshots | Metadata scope only |
| Redis | Connected-node `INFO keyspace` counters | `SCAN`, keys, values, and payloads | Keyspace metadata only |

## Ownership and limitations

The adapter scripts own extraction. The checker owns offline snapshot consistency. Indexes, foreign keys, triggers, comments, migrations, cluster-wide Redis state, and field business semantics require additional project evidence or an explicitly recorded partial scope.
