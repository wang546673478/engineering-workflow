# Engineering Workflow Database Boundary

Status: `current`  
Last verified: `2026-10-14`

Current reconciliation: `2026-10-18`, BASELINE-LINKED-02. Source comparison confirms no adapter or business-schema change in this batch; the original review remains historical. Greenfield projects document proposed schemas in Plan and add only implemented/evidenced structures to their factual dictionary; an unused database view records its reason. The adapter boundary below is retained, not re-certified by this documentation check.

This skill repository has no application database. Its database-facing module is the metadata adapter boundary.

The user accepted an empty business-database inventory on 2026-10-14. It is optional because no business schema exists here, not because adapter limitations have been waived. The adapter description below remains maintained. This change does not connect to or modify any database.

## Adapter inventory

| Adapter | Reads | Does not read | Completeness |
| --- | --- | --- | --- |
| SQLite | Schema tables, views, and fields from a checkpointed file | Business rows and active WAL state | Metadata scope only |
| MySQL | Visible `INFORMATION_SCHEMA` tables and columns | Business rows and credentials in snapshots | Metadata scope only |
| PostgreSQL | Visible `information_schema` tables and columns | Business rows and credentials in snapshots | Metadata scope only |
| Redis | Connected-node `INFO keyspace` counters | `SCAN`, keys, values, and payloads | Keyspace metadata only |

## Ownership and limitations

The adapter scripts own extraction. The checker owns offline snapshot consistency. Indexes, foreign keys, triggers, comments, migrations, cluster-wide Redis state, and field business semantics require additional project evidence or an explicitly recorded partial scope.

## Investigation setup boundary

The 1.4.4 guidance assigns necessary authorized local database/cache preparation and tests to the investigating agent, including task-owned isolation and cleanup evidence. This is separate from the metadata adapters: their commands still require explicit invocation and retain the same reads and exclusions. No adapter, schema or runtime dependency changes in this batch. A manual dictionary/source inventory remains partial mechanically; the agent performs semantic review and corrects factual errors discovered later. Existing required gates remain in force.
