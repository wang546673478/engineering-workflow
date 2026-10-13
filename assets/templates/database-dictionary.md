# Database Dictionary

Database/schema: `<name>`  
Adapter: `sqlite-metadata | mysql-metadata | postgresql-metadata | redis-metadata | manual`  
Migration baseline: `<version>`  
Last verified: `YYYY-MM-DD`

## Snapshot provenance

- Source reference (redacted host/schema identity, never credentials):
- Captured at (UTC):
- Query/adapter hash:
- Snapshot hash:
- Metadata boundary and unsupported details:

## Table: `<schema.table>`

- Purpose and owning module:
- Writers and readers:
- Lifecycle, retention, archive/delete policy:
- Transaction, lock, idempotency, and recovery rules:
- Primary/foreign keys, unique/check constraints, and indexes:
- Sensitivity and access scope:
- Migration, compatibility, and rollback:

| Field | Type/precision | Null/default | Meaning/unit/status | Source and writers | Readers | Mutable/snapshot | Constraints |
|---|---|---|---|---|---|---|---|
| `<name>` |  |  |  |  |  |  |  |

JSON field structure and consumers:

Code-only relationships (not foreign keys):

Unknown, unused, or reserved fields:

## Non-relational resource (Redis)

- Keyspace/resource name and owner:
- Metadata fields collected (`keys`, `expires`, `avg_ttl`, or project-approved equivalents):
- Explicitly not collected: keys, values, scans, payloads, and business data:
- Expiry, persistence, eviction, replication, and recovery rules:
