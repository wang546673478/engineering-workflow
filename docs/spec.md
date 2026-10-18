# Current specification: SPEC-SAFE-19-21-01

Confirmed by the 2026-10-19 user instruction adopting ASSESS-19-21-01 and requesting implementation, upload, replies and closure. Exact scope: [Task](../planning/issues-19-21-task.md). This batch preserves prior workflow/gate duties and freezes the following boundaries.

- REQ-SAFE-19 / AT-SAFE-19: Both commit modes bind input HEAD/index tree and reject persistent post-command HEAD/index/worktree or nonignored-file drift. Successful reports expose the validated tree/base; preserve user changes on failure. Boundary snapshots do not establish sandboxing or prevent later hook races.
- REQ-SAFE-20 / AT-SAFE-20: File/historical JSON parser limits and manifest root-type errors produce structured failures without executing declarations. Corrupt historical policy is distinct from absent policy; legitimate large shallow documents remain compatible.
- REQ-SAFE-21 / AT-SAFE-21: Owned ordinary process families/readers are cleaned on normal, timeout and catchable cancellation paths; signal handlers are restored and interruption never passes. Windows uses suspended creation plus Job assignment/resume. POSIX SIGKILL and the pre-assignment Windows startup window remain outside an absolute same-process cleanup promise.
- REQ-SAFE-DELIVERY / AT-SAFE-DELIVERY: Keep the original TEST/COMPILE/GUIDANCE-COMPILE and limits/review controls; publish verified 1.6.4 with linked facts/evidence, then factual replies and completed closure for #19/#20/#21. Hosted review/results remain independently bound to exact SHAs.

## Prior specifications and evidence

# Current specification: SPEC-UX-17-18-01

Confirmed on 2026-10-19 by the user's instruction to implement the reviewed recommendations, publish, reply to and close #17/#18. The exact statement and boundaries are in [Task](../planning/issues-17-18-task.md). This revision freezes only the compatible issue-fix batch; prior requirements/review scope below remain historical.

- REQ-UX-17 / AT-UX-17: Newly generated full/lite manifests explicitly exclude node_modules at any depth before link resolution, independent of dependency-install timing. Ordinary source, similar directory names and unexcluded link protections remain covered; existing manifests are not rewritten.
- REQ-UX-18 / AT-UX-18: Optional Rust/Node/TypeScript failures expose reasons, preparation guidance and unsupported scope in CLI/summaries while preserving core collection and valid partial references. Missing parsers, execution failure and successfully parsed zero-reference files remain distinct.
- REQ-UX-VERIFY / AT-UX-VERIFY: Full parser regressions require prepared pinned environments, fail early with guidance when unavailable, and do not use skip to satisfy required checks. Preserve checker/CI commands, limits and review duties; publish the tested change and factual issue replies/closure.

## Prior specifications and evidence

# Self-Maintenance Specification

Status: `current`

Current revision `SPEC-CONTEXT-03` (2026-10-18): user-authorized local source helpers and two-corpus optimization/publication, preserving the original workflow and requiring the original result of every declared check to remain authoritative. Diagnostic reruns may provide evidence but cannot replace a failed required check. The 1.6.2 correction is on `main` at `3fab75ba5d8e2663af811d2b7daee53c90fe6818`; exact-SHA Actions run `39115700117` passed its approved reviewed Ubuntu/Windows jobs and aggregate quality check. Exact authorization and scope are in [Task](../planning/source-context-task.md). Historical specifications and approvals below retain their own scope.

- REQ-CONTEXT-01 / AT-CONTEXT-01: Complete local inventory, compact full-source packs, explicit budgets/omissions and version-bound evidence.
- REQ-CONTEXT-02 / AT-CONTEXT-02: Optional syntax/config JS/TS and Rust module references; directions, source lines/hashes and unknown conditions preserved.
- REQ-CONTEXT-03 / AT-CONTEXT-03: Choose analysis/view invocation by actual task; derived summaries/tables/diagrams preserve the existing engineering phases and gates. In protected CI, automatic reviewed and manual-reviewed paths use the same rule: a diagnostic rerun never substitutes for the original required-check result.
- REQ-CONTEXT-04 / AT-CONTEXT-04: Compare four helper orders across Pi and Codex read-only corpora, prioritizing coverage/correctness before measurable cost.
- REQ-CONTEXT-05 / AT-CONTEXT-05: Synchronize versioned artifacts, exact local checks and authorized source publication; hosted CI evidence reported separately.

Historical linked-model revision: `SPEC-LINKED-02` (2026-10-18). This adds greenfield lifecycle and current-document reconciliation to the initial linked-model scope. Local implementation is authorized by the user's “那就开始完整的更改吧” and request to organize existing documents. Current technical design is [PLAN-LINKED-02](plan.md); actual progress is in the manifest-selected Task. The subsequent 2026-10-18 user instruction to upload the completed upgrade approves this batch for submission/publication; see the current Task for the exact wording and scope. Earlier release/approval statements below retain their original scope.

This repository is the maintained source of the `engineering-workflow` Codex skill. The skill must remain useful to unfamiliar projects, continuous feature discussions, cross-layer changes, documentation impact gates, and verification work. The 1.4.3 source batch was uploaded on 2026-10-16; scope, local verification and publication evidence are recorded in [TASK-CONTINUITY-01](../planning/continuous-requirements-task.md). Hosted CI remains separate from that evidence.

Previous published source: 1.4.4, uploaded on 2026-10-17. Autonomous investigation and continuous baseline correction, exact local commit verification and the source push are recorded in [TASK-BASELINE-01](../planning/baseline-workflow-task.md). Current published source: 1.5.0, uploaded on 2026-10-18 as `46d57a6cefd5cc80ae62e47099b782d4cb381504`. The linked-artifact/greenfield implementation, local exact-commit checks, scope and source-upload receipt are recorded in [TASK-LINKED-ARTIFACTS-01](../planning/linked-artifact-model-task.md); hosted CI has separate evidence.

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
- REQ-LINKED-01: Global Baseline, Spec, Technical Plan and Task form a versioned linked chain. Baseline describes the current system; Spec freezes the approved target boundary; Plan binds the change design to both revisions; Task binds execution to Plan items and acceptance evidence.
- REQ-LINKED-02: New project initialization and maintained examples expose active Baseline/Spec/Plan/Task pointers, Baseline document IDs and task artifact links. Existing manifests without optional linkage fields remain compatible.
- REQ-LINKED-03: Source, test or runtime discoveries correct the current Baseline and propagate affected impacts through Plan and Task; only an accepted change to user intent, scope, permissions or acceptance reopens Spec approval. Historical conclusions remain marked as superseded rather than silently erased.
- REQ-LINKED-04: A genuine no-implementation project records its empty starting state and constraints, puts target design in Plan, and evolves from evidenced not_applicable through partial implementation to a factual complete baseline before task completion/delivery. Existing code without documents still requires discovery; initialization must not manufacture completion or approvals.
- REQ-LINKED-05: After changing the workflow, compare and organize this repository's current authoritative documents against code and decisions, refresh effective content and linked execution steps, and preserve historical versions, reviews and release facts. Other adopted projects require their own scoped reconciliation.

## Acceptance

- REQ-BASELINE-01 / AT-BASELINE-01: Authorized discovery continues after saved batches and progress reports until a scoped, evidenced baseline is reviewable or a concrete blocker prevents further dependent work. Technical investigation belongs to the agent; independent work continues without repeated user prompts.
- REQ-BASELINE-02 / AT-BASELINE-02: Prepare necessary task-local runtimes, dependencies, database/cache instances and test data within existing authority. Record versions, migration/test results and cleanup; do not turn setup into permission for global settings or production changes.
- REQ-BASELINE-03 / AT-BASELINE-03: Bind review to the source/worktree revision, covered scope, facts, verified behavior, known defects and limits. Account for applicable modules, entrypoints, consumers, tables and fields with agent semantic evidence; critical unknowns remain blocking for affected conclusions/work. User scope acceptance is neither field-level verification nor production certification.
- REQ-BASELINE-04 / AT-BASELINE-04: Testing, runtime observation and source reading independently trigger factual baseline correction even without code edits. Verify contradictions, synchronize affected views and preserve old/new evidence and review history. Invalidated product decisions or plan premises reopen only affected review and dependent implementation; valid independent approvals remain usable.
- REQ-BASELINE-05 / AT-BASELINE-05: Check inventory provenance and supported capability before setting required gates. The manifest example matches the existing full initializer's optional source inventories, while database/contract documents and semantic coverage remain required. Existing required gates and manual/partial behavior cannot be silently changed; resolve conflicts through concrete project-reviewed proposals.

Validation for these requirements combines unchanged repository checks, template/initializer capability comparison and isolated observable discovery/correction scenarios. It does not claim host compliance or guaranteed future model behavior. Implementation authorization and completed-rule commit approval remain separate.

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
- AT-LINKED-01: A new manifest skeleton contains active Baseline/Spec/Plan/Task pointers, a Baseline document set, and task artifact links; the checker validates declared IDs and file existence.
- AT-LINKED-02: An existing manifest without optional linkage fields continues to pass its prior structural path, while unknown declared linkage IDs fail with a bounded configuration result.
- AT-LINKED-03: Public guidance, templates, references, self-maintenance Spec/Plan/Task and checker tests describe the same forward and return paths without claiming semantic approval or user understanding is mechanically proven.
- AT-LINKED-04: Disposable full/lite initialization scenarios exercise planned → evidenced not_applicable → first implementation → partial → complete. Existing-origin exemptions, missing evidence metadata, unsafe scopes, declared implementation hidden by exclusions and premature completion/handoff fail. Provisional success states explicitly do not claim delivery readiness.
- AT-LINKED-05: The current baseline, Spec, Plan, Task, views, traceability, templates and version metadata match final local behavior. A reconciliation record lists corrections, retained history and remaining limits; original reviews are not transferred to the new revision. Unchanged required repository checks pass for the final source.

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


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](../planning/source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](../planning/source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


Delivery receipt: all three REQ-UX / AT-UX boundaries were implemented in source 0040878 and locally verified with 170 tests; upload and both issue replies/closure were verified on 2026-10-19. Frozen targets above are unchanged; hosted verification is recorded separately.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.
