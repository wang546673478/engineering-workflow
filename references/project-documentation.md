# Project Documentation Baseline

For first takeover of a documentation-incomplete project, establish a full baseline and obtain the user's review confirmation before the detailed feature interview, not merely before feature development. Follow the stages and exceptions in [SKILL.md](../SKILL.md). Inventory the actual applicable modules, entrypoints, contracts, all tables and all fields first. Work without frontend/backend/database marks those views not applicable with evidence. Reuse existing documents and link to one authoritative location for each fact. A documented baseline is not approval of a major implementation plan.

Present the whole-system structure, important end-to-end flows, coverage and unverified behavior in plain language before asking for review. Record baseline paths, source revision, semantic review and the user's confirmation in the Task. Creating headings or a list of gaps does not complete the baseline. Future feature decisions can remain unresolved in the target Spec while the current-system baseline is established; do not invent requirements to complete it. Mechanical checks do not establish semantic completeness or user confirmation.

## Required views

- **Spec:** goals, users, scope, business rules, permissions, constraints, requirements and acceptance IDs, with current requirement state, candidate/confirmed decisions and deferred questions.
- **Module map:** each module's responsibility, public entrypoints, callers, dependencies, data ownership, events, cache/config/background-worker dependencies, and isolated/dead-code candidates.
- **Frontend/backend contract:** page action, route/method, request and response fields, validation, auth, errors, loading/retry behavior, and UI state updates.
- **Database dictionary:** every table and field, type/precision, nullability/default, meaning/unit/status, constraints/indexes/foreign keys, writers/readers, lifecycle, sensitivity, snapshot/immutability, transaction/lock/idempotency and migration rules.
- **Business flow:** page -> endpoint -> use case -> table/field -> event/job/consumer, including success, failure, retry, recovery, and permission changes.
- **Plan/Task:** dependency-ordered milestones, affected artifacts, acceptance evidence, requirement and implementation states tracked separately, implementation authorization, current next action and handoff notes.

## Source versus goal

Label every statement as current implementation, simulated/partial, target design, or verified behavior. Cite source paths, migrations, schemas, tests, or runtime evidence. Do not describe a target interface as implemented merely because a page or type exists. Mark code as dead only after checking static references, dynamic registration, reflection, generated code, workers, external calls, and tests.

Functional change discussions update the existing target requirements and current task state continuously, following [requirements-interview.md](requirements-interview.md). Separate facts, candidates, confirmed decisions and deferred discussion; link deferred conclusions, questions, effects/dependencies and resumption conditions. Preserve the current-system baseline as source evidence rather than rewriting it as the agreed target. Refresh current summaries when decisions change and retain superseded history with clear labels.

## Consistency gate

For every changed route, type, table, field, event, permission, or dependency, update the affected views and cross-links. The baseline is complete only when all applicable entrypoints, consumers, tables and fields are accounted for and semantic review is recorded. Unknowns remain open with an owner and follow-up task; they cannot be converted into “complete” by documenting the gap. If scope cannot be established, explain the missing evidence and keep feature work pending. Declare `task.documentation_impact` for path-based gates so module/call-chain changes require module map, flow, and contract updates, while migration/schema changes require database dictionary and flow updates. Use the checker to validate mechanical coverage; review field meaning and module ownership manually.

The declaration is required for the checker to enforce the gate: it does not infer transitive module or database impact from source paths. A task that changes code under a broad module path must still list the expected connectivity and data-document updates, or record why each gate is not applicable with search evidence.

At the end of a module discussion, combine the requirements completeness check and user review as defined in requirements-interview.md; do not defer saving until that review. A path-based checker cannot detect chat decisions that were never recorded or establish that the user reviewed their meaning. Module review leaves the whole-system baseline and complete implementation proposal gates intact; later changes reopen only the affected parts and dependencies.

Keep architecture constraints and target decisions apart from the current module map. Normal leaf modules, migration tools and test helpers are deliberate isolation, not defects. Distinguish genuinely unreachable code from registered dynamic hooks, externally consumed interfaces, and existing but disconnected features.
