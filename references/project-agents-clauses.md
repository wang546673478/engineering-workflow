# Project AGENTS Clauses

Adapt these clauses into each project's `AGENTS.md`; do not copy them blindly over existing project rules.

## Required process

- Before changing behavior, read the current Spec, architecture, module map, relevant contracts, database dictionary, business flow, Plan, Task, and progress.
- Replace these generic names with actual project links and check commands; retain existing higher-priority project constraints. Every edit task reads the global summary and then affected detail, not every unrelated field.
- For new projects or major changes, complete the one-question interview and obtain confirmation of the complete Spec/Plan/Task proposal before implementation.
- An already confirmed plan, including an explicit request to implement it, does not need repeated permission. On first takeover of an incomplete project, establish the full applicable documentation baseline before feature development.
- For small fixes, perform and record impact analysis before editing.
- At the start of every task, inspect the host's available skills catalog, plugin/tool registry, or project-provided skill inventory. Record a `skill_review` in the active Task with the catalog scope/source and timestamp, each relevant candidate's name/ID, source path or URI, visible version/release date, decision (`adopted`, `not-adopted`, or `unavailable`), reason, and evidence read. Record an explicit no-candidate or unavailable result when applicable; repeat after scope or catalog changes.
- Before asking the user to approve a material decision, explain the situation, the decision, the options, and their effects in plain language. Explain technical terms before using them, show the reviewable result first, and restate the user's decision in plain language after they answer. If the user is confused, rephrase instead of sending them straight to files or logs.
- Preserve the project's authoritative data and business-rule owners; extend existing modules before creating parallel behavior.

## Documentation and verification

- Every route, interface, table, field, event, permission, and dependency change updates the corresponding documentation and acceptance evidence.
- Every task that may affect module connectivity, cross-layer contracts, or schema/migrations declares the matching `documentation_impact` gates in the manifest; not-applicable decisions include search scope and evidence.
- Before each commit, run the staged `commit` gate; source code changes without a matching documentation-impact rule fail. Recheck each committed tree locally or in the project's chosen CI. GitHub and GitHub Actions are optional; absence of either is not a failed requirement.
- Explain protected-rule changes to the user before requesting final approval. An agent must not set the live project's external approval variable merely to obtain a passing gate. Approval paths may be exercised in disposable test fixtures; real approval must come from the human reviewer for the concrete change.
- A task cannot be marked complete until its `skill_review` is present, current for the final scope, and includes candidate paths plus versions/dates when the host exposes them. Skill guidance never overrides user decisions, repository rules, security constraints, or required documentation gates.
- Record current implementation separately from target design, and never claim unverified behavior.
- Run meaningful project checks and record results, including skips and residual risk.
- Maintain a project manifest with document/module/contract/schema inventories, active task and required checks; invoke the skill checker in baseline, change and handoff modes as applicable. Report unsatisfied required checks as incomplete, not passed. Keep unknowns open until reviewed; unsupported tooling does not establish full coverage.

## Design and safety

- Prefer high cohesion, directional dependencies, explicit interfaces, and low coupling.
- Document migrations, compatibility, rollback/recovery, and idempotency for persistent effects.
- Do not expose secrets in planning artifacts. Follow repository-specific license, security, database, and deployment rules.
