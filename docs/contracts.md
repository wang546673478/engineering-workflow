# Engineering Workflow Contracts

## Issue 23 current approval/report contract / 1.8.0

Optional record_contract=1 keeps schema_version=1; enforcement defaults diagnostic and strict is explicit. Existing stages, original required checks, process limits, Git state and document-impact rules remain. approval-evidence validates record structure, safe references, reviewed section hashes, selected task batch/REQ/AT and Plan/Spec revision. The current implementation also checks old task.approval_required. approval-sequence is diagnostic unless separately strict; history guards reject silent policy weakening. Legacy content coverage remains nonrequired partial. Explicit migration previews proposed data before atomic apply. Capability flag prevents accidental execution with old checker. [Field contract](../references/checker.md#结构化批准证据合同), [Task](../planning/issue-23-task.md).


## Issue 22 guidance compatibility

The 1.7.2 guidance clarifies existing defect records and delivery checks, with optional EARS/Given–When–Then examples. It uses existing Task/Issue/impact/Spec records and IDs, preserving old formats and valid approvals. A sentence, template or structural check is not evidence of business correctness. It adds no CLI, schema field, stage, verdict protocol, approval round or required report; required checks retain their failure/skip/unsupported meanings. The command, installer, adapter, Git-state and control-plane contracts below are unchanged. Source-audit deferral is this maintenance task's user decision, not a new exception granted to other projects.

## Checker CLI


- Input: project root, manifest path, mode, task ID, and optional base or commit reference.
- Modes: `discovery`, `baseline`, `change`, `handoff`, `commit`, `committed`.
- Output: JSON containing `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, `errors`, and nullable `verified_tree`/`verification_head`.
- `tool_version` is read from the repository-root `VERSION` file beside the checker package.
- Exit codes: `0` required checks passed; `1` a declared check or validation requirement failed (including an output limit); `2` malformed configuration, unavailable environment, or unsupported capability before a check can run.
- Safety: no shell command composition; declared checks are opt-in through `--run-checks`; command arguments containing NUL are rejected before process creation.
- Output limits: each check has a fixed 8 MiB output bound. Output is read incrementally, over-limit commands are terminated, and reports contain only observed byte counts, hashes and limit status; interrupted output is marked incomplete.
- Protected-rule changes: `commit` and `committed` add a required `control-plane` result. Without human approval this check fails even if ordinary tests pass. The approved path requires both `--allow-control-plane-change` and the previous manifest's approval environment variable set to `1`; if not configured previously, the fixed default is `ENGINEERING_CONTROL_PLANE_APPROVED`.
- Protected scopes: union of old and new `control_plane.protected_paths`, plus the selected manifest and the conventional checker path. This repository also protects `VERSION` and `CHANGELOG.md`; the proposed manifest cannot rename the approval variable to authorize itself.
- Approval boundary: a process variable is an operator acknowledgement, not proof of identity or a digital signature. Keep its lifetime to one verification run. A hosted repository still needs trusted reviewer/branch settings to resist modification of the checker itself.
- Hosting: GitHub Actions is optional. The same CLI can be run locally or by another CI system.
- Hosted review: ordinary PR/fork jobs never receive the control-plane approval value. A protected environment may run the committed check only after a reviewer-approved same-repository PR review is tied to the current exact commit; fork PRs remain subject to branch protection and a maintainer-controlled fallback. Manual exact-SHA dispatch remains a fallback. A single aggregate quality result should be the required branch-protection check. Each protected push is reviewed against its exact SHA; approval of an earlier run does not approve later commits. On source SHA `3fab75ba5d8e2663af811d2b7daee53c90fe6818`, both reviewed platform jobs and aggregate quality passed after exact-SHA approval.
- Hosted reports: a verbose test diagnostic may run only after control-plane and committed-scope checks pass and the declared TEST check alone fails. Automatic reviewed and manual-reviewed paths call `.github/scripts/finalize_reviewed_quality.py`; it exits successfully only when the original committed checker invocation succeeded. A successful diagnostic rerun provides debugging evidence but never changes a failed required check to success. The aggregate quality result therefore remains failed whenever the original checker fails.

### Manifest path rules

- Manifest paths accept `/` or `\\` separators. On POSIX, foreign Windows drive and UNC paths are rejected; project-root escapes and symlink/junction traversal remain rejected on every host.
- `exclude_paths` may contain project-relative segment-aware globs: `*`, `?`, character classes and `**` as a complete segment. Single-segment wildcards do not cross `/`; `**` matches zero or more segments. A matching directory and its descendants are pruned before link resolution. Root-matching, absolute and traversal glob patterns are rejected. Exclusions are reported and never grant change coverage.
- `documentation_impact.when_paths` remains literal. It may name a source/document scope or a strict non-root parent containing source paths from at least two distinct selected modules. Such a parent triggers its document gate but is not added to the allowed source coverage. `document_ids` remains an AND requirement.

## Database adapter snapshot

- Input: explicit adapter command and optional environment-provided connection URL.
- Output: database metadata inventory with provenance and snapshot hashes.
- Safety: no credentials, business rows, Redis keys, or Redis values in output.
- Unsupported behavior: unavailable optional driver, credentials, connection, or unsupported metadata scope is reported as unsupported.

## Persistent agent guidance installer

- Entrypoint: [install_agents_guidance.py](../scripts/install_agents_guidance.py). The maintained canonical block is [AGENTS.engineering.md](../assets/templates/AGENTS.engineering.md).
- Input: a project root, canonical manifest/state locations and optional agent instruction-file paths; the canonical project entry is `AGENTS.md`. Consult the CLI help for its current options.
- Behavior contract: create or replace the marked `engineering-workflow:start/end` section while preserving project-authored content outside it. Repeating an unchanged invocation is idempotent.
- Cross-agent contract: optional native instruction files contain thin references to canonical `AGENTS.md` and project state, rather than a second full workflow. The selected host determines native-entry discovery and loading; creating a file does not prove host integration.
- State contract: the stable block locates authoritative project files and names start/resume/handoff/incomplete-context/agent-change/scope-change recovery triggers. The installer does not infer completed tasks, approve work or reconstruct missing project state from chat.
- Safety contract: selected targets remain inside the project root; invalid or duplicate markers are rejected. The installer must not confer permissions or replace unrelated project instructions.

## Active task selection

- `engineering-manifest.json` may declare `workflow.active_task`.
- New manifests may also declare `workflow.active_baseline`, `workflow.active_spec` and `workflow.active_plan`; the checker validates those document IDs when present.
- An explicit CLI `--task` takes precedence, followed by `ENGINEERING_TASK_ID`; when neither is supplied, checker commit/committed/handoff modes use `workflow.active_task`.
- Reusable CI must consume this pointer or provide an explicit runtime task ID. Historical task IDs must not be hard-coded into workflow files.

## Linked artifact selection and traceability

- A project may declare `BASELINE`, `SPEC`, `PLAN`, `TASK` and `TRACE` documents in the manifest. `baseline.document_ids` identifies the current Baseline views; a task's optional `artifact_links` identifies the Baseline, Spec, Plan, Task and traceability files used by that task.
- The checker validates declared document IDs and file existence. It does not decide whether a Spec is semantically approved, whether a Plan is technically sufficient, or whether a user understood a decision.
- Existing manifests without these optional pointers remain compatible. New skeletons and examples include the linked pointers so a new project starts with an explicit Baseline → Spec → Plan → Task chain.

### Greenfield baseline lifecycle

- Existing projects retain complete/approved baseline requirements. Only origin=greenfield permits temporary not_applicable/partial states, with nonempty reason, source_revision, scope, evidence and literal non-root implementation_paths.
- Declared implementation locations may be absent while provisional. A not_applicable claim fails if files exist inside those locations, independently of exclusions. Undeclared implementation locations and origin truth require agent review.
- The required baseline-lifecycle result reports completion_ready=false for provisional work. Other task approval, impact, command and control-plane gates remain effective. Handoff and the selected task's complete status require a factual complete/approved baseline.
- Code, contracts and database structures become current facts only as implemented and evidenced; targets remain in Plan. Current artifact revisions are recorded in the Spec/Plan/Task and traceability; the checker does not automatically validate their semantic/revision agreement.

## Manifest bootstrap helper

- Entrypoint: `scripts/init_manifest.py`.
- Input: project root, output path, `full` or `lite` profile, --project-kind existing/greenfield (default existing), and repeatable greenfield --implementation-path (default src/tests).
- Behavior: discovers common source directories and writes a planned manifest skeleton without overwriting an existing output unless `--force` is explicit. The skeleton is not completion evidence until paths, requirements, skill review, baseline, approval and checks are reviewed.
- Capability defaults: the full initializer and maintained manifest example leave source inventories optional; Baseline, Spec, Plan, Task and applicable database/contract documents remain required. Agents review actual source/adapter capabilities before making an inventory required. Existing project manifests remain compatible; new skeletons include explicit artifact links.
- Current status: the helper is implemented. Historical adoption evidence is in [TASK-PERSISTENCE-01](../planning/persistence-task.md); the manifest-selected task owns fresh verification, limitations and pending review for current work.
- Both profiles require every linked view file; lite omits inventories and requires current baseline plus an impact record for implementation changes. Full conservatively triggers baseline/map/contract/database/flow updates; reviewers specialize actual paths. Root triggers and invented migration scopes are not emitted. Source discovery remains a candidate scaffold, not a full architecture audit.
- The helper creates only the planned manifest; it does not create source directories, documents, real project checks, completed baselines or approvals. Evidence-based transitions are maintained by the agent.

## First-takeover process contract

Before detailed feature interviewing, first takeover without a valid baseline requires global discovery and user baseline confirmation. Project Tasks record the stage, baseline paths/source revision, coverage, gaps, transition evidence and next action. Baseline confirmation is distinct from proposal approval. Existing valid evidence and explicit scope exceptions are reusable. New manifests expose the linked artifact pointers; older manifests continue through the compatibility path.

## Continuous requirement process contract

- Scope: feature-change discussions and their follow-up answers in the active task of an adopted project. Material new information updates the existing authoritative requirement and Task records during discussion; repeated facts need no duplicate entry or explicit skill invocation.
- State: facts, candidate ideas, confirmed decisions and deferred topics remain distinguishable. Requirement status and implementation status are separate process records, not new checker schema fields. Refresh the current phase, scope, next action and dependencies when they change; retain historical statements as history.
- Deferred topics: preserve the module, existing conclusion, unanswered question, impact/dependencies and resumption condition. Revisit before dependent design or implementation; deferral neither cancels the topic nor resolves a blocking uncertainty.
- Review: when a module discussion converges, consolidate its requirements, changes, unresolved/deferred items and linked impacts for user review. Save the user's wording, scope and document version. Save discussion continuously beforehand; do not introduce per-turn concentrated gates or repeated approval. Requirement confirmation does not itself authorize implementation, and existing baseline/full-proposal approval rules remain in force.
- Evidence boundary: briefly identify updated records and remaining unknowns; a failed write cannot be reported as saved. The checker has no conversation-message input or new semantic checks. Installer output and instruction text do not guarantee host loading, model compliance or completeness. Current scope and validation are recorded in [TASK-CONTINUITY-01](../planning/continuous-requirements-task.md).

The 1.4.3 source batch was uploaded on 2026-10-16 after local commit/committed checks. Publication receipts do not change the CLI, manifest schema or process contract; hosted CI is not established by a successful source push.

## Version and changelog process contract

Tasks record release impact: project policy and version source, bump/exemption reason, old/target version and classification, affected packages/synchronization paths, change notes, checks and actual publication status. Version and changelog checks are human/agent workflow obligations; the manifest schema and checker do not gain new automatic release validation. This repository uses a candidate-version / Unreleased heading before publication, then the actual date. The metadata update grants no commit/tag/push/Release/deployment authority.

For 1.4.2, the source push occurred on 2026-10-15 and is recorded in TASK-VERSION-01; the dated changelog is a publication receipt, with version and CLI contracts unchanged.

## Autonomous and continuously corrected baseline contract

- Investigation continues after saving or reporting a batch. The agent prepares necessary authorized local isolated environments and performs code/semantic verification; a reviewable evidenced scope or concrete unresolved blocker is the stopping boundary, with independent work continuing.
- Baseline acceptance records the actual source/worktree revision, scope, findings, known defects and limits. It does not assert production correctness, replace required checks or authorize product implementation.
- Testing/source/runtime findings trigger baseline correction even without a code change. Verify before asserting new facts, synchronize affected documents, retain old/new evidence and historical review, and notify/reopen only invalidated decisions or implementation premises.
- Manual inventories remain partial and cannot satisfy a declared required gate. Capability conflicts in existing projects need a concrete reviewed adjustment or supported source path; no automatic provenance relabeling, required-item removal or approval transfer is introduced.
- These are agent process obligations recorded in project Task files. The checker adds optional mechanical validation for linked artifact pointers; it does not infer semantic completeness. The 1.4.4 source publication and exact local verification are tracked by TASK-BASELINE-01; the published 1.5.0 implementation and its new fields are tracked by TASK-LINKED-ARTIFACTS-01. Existing command modes and adapter contracts remain compatible.

Publication receipt: the contracts documented here were uploaded with 1.5.0 on 2026-10-18 (`46d57a6cefd5cc80ae62e47099b782d4cb381504`). This receipt does not change CLI behavior or establish hosted CI success.


## Source helper CLI and evidence

[Guide](../references/source-context.md) describes --include/limits, --relations and --views summary/table/diagram/all. Core collection does not require parsers. Optional references report supported/read scope, unresolved/conditional/unsupported facts, never business approval. JSON evidence remains complete regardless of view choice; output is outside source and refuses overwrite. Existing checker modes/contracts unchanged. [Task](../planning/source-context-task.md).


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](../planning/source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](../planning/source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


## Issue #17/#18 compatible contract changes (1.6.3)

Both initializer profiles generate **/node_modules explicitly; existing manifests are not migrated. Relation status and CLI relations objects add unsupported per-file records and grouped diagnostics (status, files, message, setup_commands argv), retaining existing status/summary/validation fields and enums. Summary text flags incomplete selected-source coverage and renders setup hints. js_analysis_failed denotes failure executing an installed analyzer and carries no missing-parser installation recommendation. Partial results retain valid edges. Core collection exit codes remain based on inventory scan policy; graph validation is not parser coverage. Full regression environments need both pinned parsers; skips remain partial under the unchanged checker.

Current scope, source and validation: [TASK-ISSUES-17-18](../planning/issues-17-18-task.md).


Publication receipt: source 0040878 implements the additive diagnostics and explicit-default contracts above; original local gates passed and #17/#18 were replied to/closed on 2026-10-19. The receipt changes no CLI or checker contract.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.


## 1.6.4 checker state and lifecycle

Both submitted-tree modes snapshot input HEAD/index tree before validation and require post-command verification-state to pass. Persistent HEAD/index/worktree and nonignored-file drift fails; successful reports expose verified_tree and the input verification_head. Ignored generated artifacts remain allowed. These are boundary observations before report output, not atomic commit or malicious-code isolation.

File/historical JSON parser limits and non-object manifest roots fail structurally; missing historical paths differ from corrupt/unavailable content. CLI cancellation produces a failed interrupted result and nonzero 128+signal exit (KeyboardInterrupt130); handlers are restored. Owned ordinary process families/readers are cleaned in finally. POSIX uses process groups; Windows suspended children enter a kill-on-close job before resume, with setup failures refusing command execution. POSIX SIGKILL and pre-assignment hard-kill windows remain limits. No original check, limit or review duty is relaxed.

Current source/evidence: [TASK-ISSUES-19-21](../planning/issues-19-21-task.md). Earlier investigation remains in the linked assessment as historical facts.


Published implementation5f9b3e1d54a0709241fb5f11173e13ce00af3ffd passed local184-test staged/exact-commit gates and original Windows/Ubuntu reports in approved run39157028881; source upload and #19/#20/#21 replies/completed closure were verified on 2026-10-19. Receipt-only updates do not change implementation, targets, limits or prior approval scope.

## Complete adoption and original-workflow mapping (1.7.0)

Adoption creates an initialized_incomplete scaffold, managed entry and actual bundled bootstrap report without executing project commands. Outer exit 0 describes scaffold writing, not completion. Existing documents and policy remain; explicit legacy migration adds declarations without replacing evidence or approvals. Guidance-only installation remains available before a manifest and reports incomplete adoption; an existing manifest argument must reference real schema-version-1 JSON, never Markdown.

Declared stages record the original current phase, not new mandatory user review rounds. Evidenced greenfield baseline-review and established small-fix proposal exceptions are accepted; mismarked exceptions fail. Prior valid reviews retain their reviewed revision when factual views evolve; invalidated records fail. Proposal and implementation authorization may share one explicit user instruction while retaining separate meanings, task and revision bindings. Completion/handoff accepts complete or approved factual baselines with original task/validation requirements; no extra handoff stage or blanket reapproval applies.

Change and both submit modes reject unauthorized implementation-scope paths; submit failures never execute project commands. Legacy manifests retain their original path until explicit migration. Exact schema and limits: [adoption-lifecycle](../references/adoption-lifecycle.md). These checks do not authenticate review meaning, semantic completeness, dynamic dependencies or undeclared scopes.

Publication receipt (2026-10-19): implementation c15b94397314b8e84b3ee94877267f8245c3351c passed original local staged/exact-commit gates with 205 tests and the unchanged 120-second limit, was uploaded to main, and was installed as 1.7.0 with prior local work preserved. GitHub run39277812120 has a verified human environment approval but original platform reports are still pending; no hosted pass is claimed. This receipt changes evidence/status only, not source behavior or acceptance.

1.7.1 correction: normalize initializer library roots through the same existing project_root function as the CLI; hosted Windows exposed short-name aliases. Scope checks and the original workflow remain unchanged; 1.7.0 Ubuntu success/Windows failure are historical, and fresh local/exact/hosted checks are required.
