# Project AGENTS Clauses

Adapt these clauses into each project's `AGENTS.md`; do not copy them blindly over existing project rules. Use the managed block in [AGENTS.engineering.md](../assets/templates/AGENTS.engineering.md) so later skill updates can replace only their own section.

## Persistent adoption

- Adoption is a one-time project change: merge the managed block into the repository-root `AGENTS.md`, then record the skill source and fixed revision in the project manifest or canonical workflow state. Keep the active task, progress, decisions, impact analysis, verification and handoff in files under the manifest-declared state directory (normally `planning/`).
- Keep shared guidance in `AGENTS.md`. If the active agent uses another native instruction entry, add only a thin pointer with a correct relative link. Check that host's actual file format, loading scope and any required frontmatter; a generic Markdown file does not establish automatic loading. Specify a file, not a rules directory. Use portable recovery triggers: start, resume, handoff, incomplete context and scope change.
- On start, resume, handoff, context compression/incomplete context or scope change, locate and reread the adopted skill's actual `SKILL.md` and applicable references using the recorded source/revision, together with project rules, the manifest, active task, recent progress/handoff and affected documents. If no source is recorded, locate it through the host catalog and record it; if unavailable, record that limitation. A scope or deliverable change requires a fresh `skill_review` and impact analysis.
- Follow-up answers in an enabled task continue the workflow without another explicit skill invocation. Apply the continuous-record and module-review rules in [requirements-interview.md](requirements-interview.md) whenever functional changes are discussed, not only once coding begins.
- Keep the adoption change reviewable and idempotent. Preserve user-written rules outside the managed markers, do not create agent-specific permissions, and do not treat the presence of the block as approval to send messages, deploy, change global settings or bypass project rules.

## Required process

- Before changing behavior, read the current Spec, architecture, module map, relevant contracts, database dictionary, business flow, Plan, Task, and progress.
- Replace these generic names with actual project links and check commands; retain existing higher-priority project constraints. Every edit task reads the global summary and then affected detail, not every unrelated field.
- For new projects or major changes, complete the one-question interview and obtain confirmation of the complete Spec/Plan/Task proposal before implementation.
- An already confirmed plan, including an explicit request to implement it, does not need repeated permission. First takeover of existing code without a valid baseline follows the stages in SKILL.md: global discovery, user baseline review, detailed feature interview, proposal approval, implementation. Basic goal clarification may orient discovery but must not turn into continuous feature questioning. Record the current stage, baseline source/version and transition evidence in the Task; reuse valid prior evidence and retain the small-fix/new-project exceptions.
- For small fixes, perform and record impact analysis before editing.
- At the start of every task, inspect the host's available skills catalog, plugin/tool registry, or project-provided skill inventory. Record a `skill_review` in the active Task with the catalog scope/source and timestamp, each relevant candidate's name/ID, source path or URI, visible version/release date, decision (`adopted`, `not-adopted`, or `unavailable`), reason, and evidence read. Record an explicit no-candidate or unavailable result when applicable; repeat after scope or catalog changes.
- Before asking the user to approve a material decision, explain the situation, the decision, the options, and their effects in plain language. Explain technical terms before using them, show the reviewable result first, and restate the user's decision in plain language after they answer. If the user is confused, rephrase instead of sending them straight to files or logs.
- Save new functional requirements, candidates, decisions and deferred discussion in existing authoritative records during discussion. Refresh current state and next action, distinguish facts/candidates/confirmed/deferred content, and keep requirement state separate from implementation state and authorization. Deferred items retain conclusions, questions, effects/dependencies and resumption conditions; revisit them before dependent work. Report save failures honestly.
- When a module discussion concludes, combine the completeness check with user review of its requirements, changes, open/deferred items and related effects. Record the user's statement, date, scope and document version. Do not add per-answer concentrated checks or approvals, or postpone saving until module review. Keep the whole-system baseline and complete proposal approval gates; later changes reopen only affected parts.
- Preserve the project's authoritative data and business-rule owners; extend existing modules before creating parallel behavior.

## Documentation and verification

- Every route, interface, table, field, event, permission, and dependency change updates the corresponding documentation and acceptance evidence.
- Every task that may affect module connectivity, cross-layer contracts, or schema/migrations declares the matching `documentation_impact` gates in the manifest; not-applicable decisions include search scope and evidence.
- Before each commit, run the staged `commit` gate; source code changes without a matching documentation-impact rule fail. Recheck each committed tree locally or in the project's chosen CI. GitHub and GitHub Actions are optional; absence of either is not a failed requirement.
- Explain protected-rule changes to the user before requesting final approval. An agent must not set the live project's external approval variable merely to obtain a passing gate. Approval paths may be exercised in disposable test fixtures; real approval must come from the human reviewer for the concrete change.
- A task cannot be marked complete until its `skill_review` is present, current for the final scope, and includes candidate paths plus versions/dates when the host exposes them. Skill guidance never overrides user decisions, repository rules, security constraints, or required documentation gates.
- Record current implementation separately from target design, and never claim unverified behavior.
- Before delivering substantive changes, follow the version/changelog policy in SKILL.md and implementation-workflow.md; record release impact, the authoritative version source, old/target version, synchronization paths, change notes and actual release status in the Task. Apply project-specific versioning first; a metadata-only progress/verification receipt need not consume another version. Updating a version does not grant publication permissions.
- Run meaningful project checks and record results, including skips and residual risk.
- Maintain a project manifest with document/module/contract/schema inventories, active task and required checks; invoke the skill checker in baseline, change and handoff modes as applicable. Report unsatisfied required checks as incomplete, not passed. Keep unknowns open until reviewed; unsupported tooling does not establish full coverage.
- Keep the active task in the manifest's `workflow.active_task` (or an equivalent project state pointer). CI and reusable templates should consume that pointer or an explicit runtime task ID; they must not hard-code a historical task ID.

## Design and safety

- Prefer high cohesion, directional dependencies, explicit interfaces, and low coupling.
- Document migrations, compatibility, rollback/recovery, and idempotency for persistent effects.
- Do not expose secrets in planning artifacts. Follow repository-specific license, security, database, and deployment rules.
