# Implementation Workflow

## Before editing

Restore the current stage and its transition evidence from the authoritative Task. First takeover without a valid baseline follows [SKILL.md](../SKILL.md): global discovery, user baseline review, detailed feature interview, complete proposal approval, implementation. Do not defer the baseline until coding begins or mistake baseline confirmation for implementation approval. Reuse applicable existing evidence and follow the stated small-fix/new-project exceptions.

Read project instructions and the current Spec, module map, relevant frontend/backend contract, database dictionary, business flow, Plan, and Task. Search for existing implementations and public callers. Write an impact record with requirement IDs, owners, affected modules/routes/tables/fields, permission and financial effects, compatibility, migration, recovery, tests, and docs.

At the start of every task, inspect the host's available skills catalog, plugin/tool registry, or project-provided skill inventory. Filter candidates against the task's actual deliverables, read each applicable `SKILL.md` and relevant linked guidance, and record the review in the Task `skill_review` field. Each candidate record includes its name or ID, source path/URI, visible version or release date (or `not provided`), review timestamp, decision (`adopted`, `not-adopted`, or `unavailable`), and a concrete fit/conflict reason. Record the catalog scope and evidence when no candidate applies or the host cannot expose a catalog. Repeat the review when task scope, deliverables, or available skills change; do not silently substitute a remembered skill version.

Read global architecture, module-map summary, active plan/task and recent progress at the start of each edit task. Load only relevant detailed contracts, dictionary sections and upstream rules after that. If no baseline exists on first takeover, document and review it before feature work. Small approved changes do not repeat the full interview. Record documents and versions reviewed as an audit trail, not proof that a script can verify comprehension.

## During editing

Keep each capability in one cohesive owner. Depend on stable interfaces instead of internal details; avoid circular dependencies and duplicate validation, pricing, authorization, or persistence rules. Preserve transaction boundaries and exact-once identities where side effects matter. Add a new abstraction only when its boundary removes real coupling and its owner is explicit.

Use real variability or a concrete coordination problem to justify interfaces and adapters; do not add a layer for every function. A same-purpose replacement names the old entrypoint and when it is disabled or removed. Preserve project money units, precision, tenant authorization and durable side-effect identities; take their values from the project rather than this skill.

## Change and migration control

For data or contract changes, document forward migration, existing-data behavior, compatibility window, rollback or recovery, and cleanup of the old path. Update consumers in the same task unless a compatibility plan states otherwise. Treat route, response, schema, permission, and event changes as cross-layer changes even when the diff is small.

Before editing, set `task.documentation_impact` for every task that can change module or call-chain connectivity, a frontend/backend contract, or a schema/migration. Use the standard gates for module-connectivity (`module map`, `business flow`, affected `contract`) and database (`database dictionary`, `business flow`); include inventory/mapping documents when the project manifest declares them. If analysis proves a gate is not applicable, record the search scope and evidence in the impact document.

Do not treat a skill recommendation as approval to change scope or bypass project rules. User decisions, repository instructions, security constraints, and required review gates remain authoritative. An adopted skill supplies process or tooling guidance only; record conflicts and the final resolution in `skill_review`.

Reopen only the newly changed product decision when the user changes confirmed scope or acceptance. Present an updated complete proposal for a major change. Ordinary implementation choices inside an approved task proceed without another permission question. Approval records cite the user's statement and exact scope; never fabricate a human approval.

## Recovery and handoff

On start, resume, handoff, incomplete context or agent change, reread the project rules, manifest, active task, recent progress or handoff, adopted skill source/revision and the unfinished documentation before making edits. Inspect the working tree and current task status, then continue from the recorded state. Do not repeat completed work or discard unrelated changes. A handoff must name the current state, next action, blockers, changed files and exact verification still required. A scope, deliverable or technology change requires a fresh `skill_review` and impact analysis.

Bind test evidence to the source version/worktree and relevant environment. Old reports become historical when affected source changes; do not claim a fresh pass. When a test expectation conflicts with implementation, reconcile both with confirmed requirements before updating it; never weaken an assertion only to get green results.

## Completion evidence

Run the project's declared checks and relevant focused tests. Record actual commands/results and distinguish passed, failed, partial, skipped, unsupported, and unverified behavior. Update Spec/Plan/Task, module/contracts/database/flow docs, and progress before marking done. Declare and satisfy documentation-impact gates: module or cross-layer connectivity changes must update the module map, business flow, and affected contract; migration/schema changes must update the database dictionary and business flow. Re-run impact checks after late changes.

Before marking a task complete, verify that its `skill_review` is present and complete, including the catalog source/time, candidate paths and versions/dates, decisions, reasons, and any recheck triggered by scope changes. A missing or stale skill review leaves the task incomplete even when code and tests pass.

Use [checker.md](checker.md) for the manifest and CLI. Optional inventories marked not applicable still need a reason. Required checks skipped, unsupported or failed do not qualify for completion; ask for changed acceptance scope only if the task genuinely cannot progress. CI can invoke read-only checks. `--run-checks` runs the explicit trusted project commands; inspect commands and authorization before enabling it. Scripts cannot prove the quality of a requirements interview or field descriptions.
