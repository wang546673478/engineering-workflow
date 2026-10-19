# Adoption Lifecycle Impact

Current task: [TASK-ADOPTION-LIFECYCLE-01](adoption-lifecycle-task.md).

Current semantic review: original-flow exceptions and core instructions have now been corrected under the user instruction to test, upload on success and update the local skill. Earlier parity-not-satisfied findings remain historical below. Fresh scenario/full/exact gates and dirty-install rehearsal must pass before delivery.

## Required synchronization

- Instructions: `SKILL.md`, `README.md`, `assets/templates/AGENTS.engineering.md`, `references/project-agents-clauses.md`, `references/checker.md`, `scripts/init_manifest.py`, `scripts/install_agents_guidance.py` and `scripts/adopt_project.py`.
- Checker and tests: `scripts/check_project.py`, `scripts/tests/test_adoption.py`, initializer/guidance/checker lifecycle regressions.
- Governance: `engineering-manifest.json`, `docs/spec.md`, `docs/plan.md`, `docs/module-map.md`, `docs/contracts.md`, `docs/business-flow.md`, `planning/baseline-review.md`, `planning/traceability.md`, `planning/skill-review.md`, version and CHANGELOG.

## Original defect and implemented behavior

Original 1.6.4 behavior is split: the guidance installer updates `AGENTS.md`, while the initializer and checker are separate commands. A prose task index can be supplied as the manifest pointer, and no stage or independent approval state is created by guidance installation.

The current 1.7.0 Unreleased implementation has one adoption entrypoint that creates a planned, provenance-bound manifest and managed guidance without overwriting existing project state. New manifests declare a takeover stage, implementation scopes, baseline/proposal/implementation approvals and skill/checker provenance. Discovery mode supports incomplete existing baselines; change/commit/handoff gates reject source changes until the declared stage and approvals permit implementation.

## Boundary

This is a workflow-tooling change. It does not migrate external projects, modify their source or data, authenticate a user, or prove semantic baseline completeness. Existing manifests without lifecycle fields remain compatible and require explicit migration before they receive the new stage gates.

## Control and dependency impact

The original required TEST command/120 seconds and existing compiler inputs/30 seconds remain; GUIDANCE-COMPILE additionally compiles adopt_project.py. No check is weakened. The instructions module now calls checker for read-only bootstrap, so its actual dependency/allowed dependency explicitly includes checker; checker still depends on adapters and has no instructions dependency. Version metadata and CHANGELOG move together to 1.7.0 Unreleased.

New lifecycle fields tighten declared stages and implementation authorization only for manifests that opt in; prior manifests retain their previous gates. This is compatibility, not evidence that an old project has the new protection. No control-plane approval variable, prior protected scope, hook or hosted CI setting is changed. Implementation authorization does not by itself authorize publishing or supply finished-control-file approval.

No tables, fields, indexes, migrations, business routes or metadata adapter read/write contracts change; database view remains applicable as the existing metadata-only boundary. Source/search evidence: diff restricted to workflow tools/tests/instructions/governance; extract_database.py and extract_sqlite.py remain unchanged. Cross-file write failures can leave a created scaffold; errors preserve it for inspection. Manifest replacement is atomic but not a general concurrent-writer lock.

Test-fixture performance: after 200 native Python3.11 tests passed diagnostically in 122.569 seconds, retain the 120-second required limit and all assertions while replacing repeated identical initial Git setup with full independent copies of a real committed seed. No shared objects/hardlinks, skipped tests, mocked Git or product gate change applies. Fresh full validation is required after this test infrastructure adjustment.

## Workflow parity findings (2026-10-19 23:04 +08:00)

The original phase sequence remains, but requiring a real JSON/active task before guidance maintenance, mandatory lifecycle/authorization declarations, complete-stage approved-current-baseline and stage-conditioned handoff are operational rule changes. The new blanket baseline-review gate also needs reconciliation with the original evidenced-empty-project exception. Existing valid baselines, small fixes and resumed applicable approvals require explicit rule mappings; legacy compatibility alone is not proof. Do not call this a workflow-preserving global fix until these affected rules and exceptions are reconciled. Current user request is explanation only; preserve implementation and test history, hold dependent delivery.

## Revision 02 original-flow correction

No new human review rounds: guidance-first remains, empty projects use evidenced baseline-review non-applicability, small fixes use established requirements/impact evidence instead of forced full proposal, valid past baseline reviews persist after factual revisions unless invalidated, the same explicit instruction may authorize proposal and implementation, and completion uses complete/approved. These are corrections to make declarations match original semantics, not exemptions from existing project controls. User now authorizes exact local submission/upload after checks and local-install update with WIP preservation; independent hosted required-reviewer approval is never fabricated.
