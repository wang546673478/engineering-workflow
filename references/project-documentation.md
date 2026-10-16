# Project Documentation Baseline

For first takeover of a documentation-incomplete project, establish a full baseline and obtain the user's review confirmation before the detailed feature interview, not merely before feature development. Follow the stages and exceptions in [SKILL.md](../SKILL.md). Inventory the actual applicable modules, entrypoints, contracts, all tables and all fields first. Work without frontend/backend/database marks those views not applicable with evidence. Reuse existing documents and link to one authoritative location for each fact. A documented baseline is not approval of a major implementation plan.

Present the whole-system structure, important end-to-end flows, coverage and unverified behavior in plain language before asking for review. Record baseline paths, source revision, semantic review and the user's confirmation in the Task. Creating headings or a list of gaps does not complete the baseline. Future feature decisions can remain unresolved in the target Spec while the current-system baseline is established; do not invent requirements to complete it. Mechanical checks do not establish semantic completeness or user confirmation.

## Autonomous discovery and bounded review

Bind discovery to the source revision and working-tree changes, applicable modules, validation environments and intended baseline scope. Follow entrypoints, consumers, migrations and tests through the whole system. The agent performs code and field-semantic review, reconciles contradictions and gathers runtime evidence; “manual review” means reasoning beyond the checker, not assigning technical investigation to the user.

Maintain one coverage view in the existing Task: accounted-for areas and evidence, remaining investigation, external unknowns, actual blockers and next action. Keep investigating and preparing necessary isolated environments after each saved batch or progress update. A list of remaining work is a continuation plan, not a reason to require another “continue”. End with a reviewable baseline or a concrete blocker that cannot be resolved within available tools, authority and evidence; continue independent work first. Ask only for missing decisions/access that investigation cannot supply.

A reviewable baseline accounts for every applicable entrypoint, consumer, table and field within its stated scope, with semantics and key end-to-end flows supported by source/test/runtime evidence. An unresolved field meaning or contradictory critical flow remains an investigation gap. Known implementation defects may be baseline facts; discovery does not authorize fixing every defect. Distinguish source coverage from runtime validation and external/production unknowns. Use controlled fixtures or sandboxes where appropriate and report their limits. External integration or certification is required only when the actual task or project rules require it; do not claim it from a local test.

Present the user with the system structure, key findings, covered scope, known defects, unverified boundaries and their effect on the next work. The user accepts that version's scope and limitations, rather than personally verifying every field or certifying correctness. Uncertainty that could invalidate the baseline's conclusions or dependent implementation remains blocking for that part; unrelated external unknowns are tracked with owners, effects and resumption conditions. Scope acceptance cannot turn an unsatisfied required check into pass.

## Inventory capability before gates

Before adopting a manifest, compare each proposed required inventory's provenance and scope with supported checker capabilities in [checker.md](checker.md). Manual sources always remain partial; this checker has no generic contract/route extractor. Do not create an impossible required-source gate by copying an example. New templates leave such inventories optional while database/contract documents and semantic coverage remain required. Make an inventory required only when its actual source has a supported, achievable verification path and the project has reviewed the gate.

In an existing project, keep required declarations and failures intact. An impossible gate is a tooling/acceptance conflict, not evidence that the user has failed to understand the source. Complete independent investigation, prepare a concrete supported-adapter or scoped acceptance proposal with its effect on coverage, and follow that project's control-change approval rules. Repeating the same tests, forging provenance, changing complete flags or silently dropping required items cannot resolve it.

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

For every changed route, type, table, field, event, permission, or dependency, update the affected views and cross-links. Baseline completion is bounded to the recorded revision, scope and evidence above; all applicable entrypoints, consumers, tables and fields must be accounted for with agent semantic review. Unknowns retain an owner, effects and follow-up task; documenting a gap does not verify it. If scope or a critical conclusion cannot be established, keep dependent feature work pending. Declare `task.documentation_impact` for path-based gates so module/call-chain changes require module map, flow, and contract updates, while migration/schema changes require database dictionary and flow updates. Use the checker for mechanical coverage and agent code review for field meaning and ownership.

The declaration is required for the checker to enforce the gate: it does not infer transitive module or database impact from source paths. A task that changes code under a broad module path must still list the expected connectivity and data-document updates, or record why each gate is not applicable with search evidence.

At the end of a module discussion, combine the requirements completeness check and user review as defined in requirements-interview.md; do not defer saving until that review. A path-based checker cannot detect chat decisions that were never recorded or establish that the user reviewed their meaning. Module review leaves the whole-system baseline and complete implementation proposal gates intact; later changes reopen only the affected parts and dependencies.

Keep architecture constraints and target decisions apart from the current module map. Normal leaf modules, migration tools and test helpers are deliberate isolation, not defects. Distinguish genuinely unreachable code from registered dynamic hooks, externally consumed interfaces, and existing but disconnected features.

## Continuous correction

The current baseline is maintained throughout testing, investigation and approved development. Its historical review remains tied to the version and evidence actually reviewed. A newly discovered documentation error triggers correction even when product source has not changed.

Immediately flag the affected claims and check source, confirmed requirements, migrations, tests and runtime evidence. Once established, correct the current authoritative views and follow the affected links through module ownership, contracts, dictionary, flow, inventories and Spec/Plan/Task. Record the old/new conclusion, discovery reason, source/worktree revision, evidence, affected scope and current next action in the existing task/history. Preserve contradictory or unverified evidence as open until reconciled; do not rewrite a failing implementation as the desired requirement or weaken a test to match it.

Factual documentation correction proceeds autonomously. If the correction changes a product decision or invalidates an approved plan's premise, notify the user, mark that approval as needing review for the affected scope, and pause only work dependent on the disputed premise. Reuse still-valid approvals elsewhere. Do not apply an old approval to corrected content silently. Revalidate affected conclusions and check citation/source freshness; a documentation-only correction does not require rerunning unrelated full suites unless project policy requires them. On recovery, load the current corrected view and its valid review evidence, not an obsolete snapshot presented as current.
