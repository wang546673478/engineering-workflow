# Project Documentation Baseline

For first takeover of a documentation-incomplete project, establish and review a full baseline before feature development. Inventory the actual applicable modules, entrypoints, contracts, all tables and all fields first. Work without frontend/backend/database marks those views not applicable with evidence. Reuse existing documents and link to one authoritative location for each fact. A documented baseline is not approval of a major implementation plan.

## Required views

- **Spec:** goals, users, scope, business rules, permissions, constraints, requirements, and acceptance IDs.
- **Module map:** each module's responsibility, public entrypoints, callers, dependencies, data ownership, events, cache/config/background-worker dependencies, and isolated/dead-code candidates.
- **Frontend/backend contract:** page action, route/method, request and response fields, validation, auth, errors, loading/retry behavior, and UI state updates.
- **Database dictionary:** every table and field, type/precision, nullability/default, meaning/unit/status, constraints/indexes/foreign keys, writers/readers, lifecycle, sensitivity, snapshot/immutability, transaction/lock/idempotency and migration rules.
- **Business flow:** page -> endpoint -> use case -> table/field -> event/job/consumer, including success, failure, retry, recovery, and permission changes.
- **Plan/Task:** dependency-ordered milestones, affected artifacts, acceptance evidence, status, and handoff notes.

## Source versus goal

Label every statement as current implementation, simulated/partial, target design, or verified behavior. Cite source paths, migrations, schemas, tests, or runtime evidence. Do not describe a target interface as implemented merely because a page or type exists. Mark code as dead only after checking static references, dynamic registration, reflection, generated code, workers, external calls, and tests.

## Consistency gate

For every changed route, type, table, field, event, permission, or dependency, update the affected views and cross-links. The baseline is complete only when all applicable entrypoints, consumers, tables and fields are accounted for and semantic review is recorded. Unknowns remain open with an owner and follow-up task; they cannot be converted into “complete” by documenting the gap. If scope cannot be established, explain the missing evidence and keep feature work pending. Declare `task.documentation_impact` for path-based gates so module/call-chain changes require module map, flow, and contract updates, while migration/schema changes require database dictionary and flow updates. Use the checker to validate mechanical coverage; review field meaning and module ownership manually.

The declaration is required for the checker to enforce the gate: it does not infer transitive module or database impact from source paths. A task that changes code under a broad module path must still list the expected connectivity and data-document updates, or record why each gate is not applicable with search evidence.

Keep architecture constraints and target decisions apart from the current module map. Normal leaf modules, migration tools and test helpers are deliberate isolation, not defects. Distinguish genuinely unreachable code from registered dynamic hooks, externally consumed interfaces, and existing but disconnected features.
