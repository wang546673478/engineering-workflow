# Self-Maintenance Specification

Status: `current`

This repository is the maintained source of the `engineering-workflow` Codex skill. The skill must remain useful to unfamiliar projects, continuous feature discussions, cross-layer changes, documentation impact gates, and verification work. The 1.4.3 source batch was uploaded on 2026-10-16; scope, local verification and publication evidence are recorded in [TASK-CONTINUITY-01](../planning/continuous-requirements-task.md). Hosted CI remains separate from that evidence.

## Requirements

- REQ-SELF-01: The repository maintains a traceable baseline for its own instructions, modules, contracts, business flow, database-adapter boundary, and verification checks.
- REQ-SELF-02: Changes to the skill are reviewed with applicable skills, tests, documentation-impact analysis, and Git commit evidence.
- REQ-SELF-03: Database adapters remain metadata-only, explicit, and safe to run without exposing credentials or business values.
- REQ-SELF-04: Explain review decisions in plain language, separate automated results from human approval, and allow local-only checks for projects without GitHub.
- REQ-SELF-05: Changing validation rules requires a separate human decision; deleting protected-path declarations or renaming approval variables in the same change must not silently allow it.
- REQ-PERSIST-01: Projects that adopt the workflow retain a stable, managed instruction block in repository-root `AGENTS.md`, with links or paths to authoritative task state and recovery guidance. The installer preserves project-authored text outside its own markers.
- REQ-PERSIST-02: Other agents use thin native-entry references to that same `AGENTS.md` and project state. Host loading behavior is explicitly verified per project; writing an instruction file alone does not prove the host loads it.
- REQ-PERSIST-03: The GitHub issue audit and this persistence change have a separate task, plan, impact, skill review, decisions, progress and verification record. Prior-task approval does not authorize the new protected changes.
- REQ-ISSUES-01: The checker handles excluded dependency trees and project-relative check working directories without weakening root and link safety.
- REQ-ISSUES-02: Requirement/acceptance traceability, inventory refreshes and first adoption provide explicit, reviewable workflows with backward-compatible defaults.
- REQ-ISSUES-03: Public guidance records the declaration-based verification boundary, package version/license/change history and a reviewable full/lite manifest bootstrap.
- REQ-ISSUES-04: CI task selection comes from the manifest active-task pointer or an explicit runtime input, never from a historical task ID copied into workflow code.
- REQ-ISSUES-05: Checker reports derive `tool_version` from the repository's canonical `VERSION` file.
- REQ-ISSUES-06: Manifest paths using either slash style behave consistently across hosts, while absolute paths from another platform, root escapes and links remain rejected.
- REQ-ISSUES-07: `exclude_paths` supports documented segment-aware glob patterns; `documentation_impact.when_paths` may use the strict common ancestor of source scopes from at least two selected modules without expanding changed-path coverage.
- REQ-ISSUES-08: The repository workflow routes protected-path changes through the fixed `engineering-control-review` environment automatically, runs ordinary checks for other changes, and exposes one aggregate quality result while retaining an exact-SHA manual fallback.
- REQ-ISSUES-09: The checker rejects NUL-containing declared command arguments as structured configuration errors before starting a subprocess.
- REQ-ISSUES-10: Declared checks capture output incrementally within a bounded per-check limit and fail safely when a command exceeds that limit.
- REQ-ISSUES-11: Release metadata used by the checker is included in the repository control-plane review scope.
- REQ-CONTINUITY-01: Record discussions of any feature addition, modification, deletion or behavior, permission, billing or data-relationship change. Follow-up answers in an adopted project's active task continue the same workflow without requiring another explicit skill invocation.
- REQ-CONTINUITY-02: Maintain one authoritative requirement record and current summary during discussion. Separate facts, candidates, confirmations and deferred topics; preserve deferred dependencies and recovery conditions, and keep requirement status distinct from implementation status.
- REQ-CONTINUITY-03: At module discussion completion, consolidate the module's requirements, changes, open/deferred items and connected impacts for user review. This does not add per-turn approval or replace first-takeover baseline review and complete implementation-proposal approval.
- REQ-CONTINUITY-04: Instructions, persistent entrypoints, templates and public documentation describe the same process and limits. The checker remains declaration-based, receives no conversation messages and cannot guarantee instruction execution or discover wholly unrecorded requirements.

## Acceptance

- AT-SELF-01: The active manifest and baseline documents pass the checker in baseline mode.
- AT-SELF-02: The test suite and Python compilation checks pass for the current source tree.
- AT-SELF-03: A self-maintenance change records skill applicability, affected modules, documentation gates, tests, and manual-review status.
- AT-SELF-04: Guidance accepts an empty business-database inventory when genuinely not applicable; CI remains optional for other projects.
- AT-SELF-05: CLI regression tests reject unapproved rule changes and exercise the approved path only in disposable fixture repositories.
- AT-PERSIST-01: Installer verification covers initial creation, repeat invocation, updating only its managed block, preservation of surrounding project rules, invalid markers and out-of-project targets.
- AT-PERSIST-02: The canonical block states when to reload project/skill/task files and where to record plans, decisions, progress and verification. Optional native agent files reference the canonical instructions, with no claim of universal automatic discovery.
- AT-PERSIST-03: [The persistence task](../planning/persistence-task.md) records issue #2–10 recommendations without claiming those issues are fixed; its manifest task remains separate from the historical approved task and records current verification and review status.
- AT-ISSUES-01: Checker regression tests cover excluded symlink trees, working directories, trace anchors/indexes and first-adoption diagnostics.
- AT-ISSUES-02: Extractors refuse unsafe overwrites by default and atomically update only their own versioned snapshots when explicitly requested.
- AT-ISSUES-03: Documentation and bootstrap templates explain `documentation_impact` semantics, verification limits, version metadata and the reviewable `lite`/`full` initialization path.
- AT-ISSUES-04: Checker tests cover manifest active-task fallback and reject an unknown active task; the repository workflow invokes the checker without a copied historical task ID.
- AT-ISSUES-05: Checker CLI reports the current value in `VERSION`; release metadata must agree with that canonical value.
- AT-ISSUES-06: A POSIX host resolves a manifest path such as `docs\\spec.md` to `docs/spec.md`, while Windows drive/UNC paths on POSIX and project-root escapes still fail.
- AT-ISSUES-07: Exclusion globs support `*`, `?`, character classes and complete-segment `**`, prune matching directory trees before link resolution, and never become change allowlists; a non-root `when_paths` ancestor covering source scopes from two or more selected modules is accepted and triggers the normal AND documentation gate.
- AT-ISSUES-08: A push or pull request first detects protected paths from the trusted base manifest plus fixed checker/manifest/workflow paths; protected changes wait for the fixed review environment before committed checks, unprotected changes run the normal matrix, and the aggregate quality job fails when the selected path is not successful. Manual exact-SHA review remains available.
- AT-ISSUES-09: A manifest command containing a NUL byte returns JSON configuration errors without a traceback or command side effect.
- AT-ISSUES-10: A check that emits more than its fixed output limit is terminated, reports a failed check with bounded evidence, and does not expose raw output.
- AT-ISSUES-11: `VERSION` and `CHANGELOG.md` are protected control-plane paths and a change to either requires external approval in commit/committed modes.
- AT-CONTINUITY-01: A follow-up feature answer without a skill mention updates the existing requirement/task record when it adds material information; a factual answer with no new change information does not create duplicate requirements.
- AT-CONTINUITY-02: Deferred topics retain their module, known conclusions, remaining question, impacts/dependencies and resumption condition. A confirmed requirement can remain unimplemented; a phase change refreshes current state while retaining its history.
- AT-CONTINUITY-03: A module review presents a concrete summary and records user wording, scope and document version. Discussion is saved continuously before that review, and only affected portions reopen after a later change.
- AT-CONTINUITY-04: Existing CLI/check commands and protection semantics remain intact; isolated conversation scenarios and manual review supplement structural checks without claiming host discovery or production reliability is proven.

## Persistence change status

The persistence implementation was verified and published as recorded in [TASK-PERSISTENCE-01](../planning/persistence-task.md). Current work is selected by `workflow.active_task` in the manifest; its task record owns current verification and review status. Historical approval applies only to its recorded scope.

## Publishing diagnostics

If an approved hosted verification fails its TEST check, the reviewed workflow may rerun this repository's fixture-only tests with visible diagnostics. It first verifies the saved report's control-plane, committed-scope and all other required prechecks. A rejected rule change never enables this diagnostic path.

## Scope and ownership

The skill instructions own the workflow rules and managed guidance template. The guidance installer updates the instruction block and optional thin references; the agent maintains requirements, current state and review evidence in the project's existing authoritative files. The checker owns mechanical manifest, impact, inventory, and Git gate validation. The adapter scripts own metadata extraction. Tests are the executable behavior evidence. User decisions and repository-specific rules remain higher priority than this skill.

## Non-goals

This baseline does not claim that the checker discovers every dynamic dependency, proves database business semantics, or replaces human review of its own design. Workflow text does not guarantee model compliance or host loading. Recording a requirement is not its confirmation, and requirement confirmation is not automatic implementation authorization.

## First-takeover stage requirement

REQ-STAGES-01 / AT-STAGES-01: First takeover without a valid global baseline completes discovery and user baseline review before detailed feature interviewing. Basic goal clarification is permitted; existing valid evidence, small fixes and projects without existing code retain their explicit exceptions. See [the stage-change record](../planning/takeover-stages-task.md).

## Version and changelog delivery requirements

REQ-VERSION-01 / AT-VERSION-01: Each substantive delivery batch follows the project's existing version policy, records authoritative sources and impact classification, and synchronizes applicable version consumers before delivery. The default three-part scheme distinguishes compatible fixes, compatible new capabilities and incompatible changes.

REQ-VERSION-02 / AT-VERSION-02: The Task records release impact and meaningful CHANGELOG/equivalent notes, separates unreleased content from actual publication, and documents any no-bump decision for progress/evidence-only changes. No automatic inference or new publication authority is implied. See [TASK-VERSION-01](../planning/version-policy-task.md).

Publication checkpoint: the 1.4.2 source batch was uploaded on 2026-10-15 after local commit/committed checks. Its changelog date is now based on that event; hosted CI and real-agent behavior remain unverified.
