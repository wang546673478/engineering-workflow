# Engineering Workflow Contracts

## Checker CLI

- Input: project root, manifest path, mode, task ID, and optional base or commit reference.
- Modes: `baseline`, `change`, `handoff`, `commit`, `committed`.
- Output: JSON containing `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, and `errors`.
- `tool_version` is read from the repository-root `VERSION` file beside the checker package.
- Exit codes: `0` required checks passed; `1` a declared check or validation requirement failed (including an output limit); `2` malformed configuration, unavailable environment, or unsupported capability before a check can run.
- Safety: no shell command composition; declared checks are opt-in through `--run-checks`; command arguments containing NUL are rejected before process creation.
- Output limits: each check has a fixed 8 MiB output bound. Output is read incrementally, over-limit commands are terminated, and reports contain only observed byte counts, hashes and limit status; interrupted output is marked incomplete.
- Protected-rule changes: `commit` and `committed` add a required `control-plane` result. Without human approval this check fails even if ordinary tests pass. The approved path requires both `--allow-control-plane-change` and the previous manifest's approval environment variable set to `1`; if not configured previously, the fixed default is `ENGINEERING_CONTROL_PLANE_APPROVED`.
- Protected scopes: union of old and new `control_plane.protected_paths`, plus the selected manifest and the conventional checker path. This repository also protects `VERSION` and `CHANGELOG.md`; the proposed manifest cannot rename the approval variable to authorize itself.
- Approval boundary: a process variable is an operator acknowledgement, not proof of identity or a digital signature. Keep its lifetime to one verification run. A hosted repository still needs trusted reviewer/branch settings to resist modification of the checker itself.
- Hosting: GitHub Actions is optional. The same CLI can be run locally or by another CI system.
- Hosted review: ordinary PR/fork jobs never receive the control-plane approval value. A protected environment may run the committed check only after a reviewer-approved same-repository PR review is tied to the current exact commit; fork PRs remain subject to branch protection and a maintainer-controlled fallback. Manual exact-SHA dispatch remains a fallback. A single aggregate quality result should be the required branch-protection check.
- Hosted reports: a verbose test diagnostic may run only after control-plane and committed-scope checks pass and the declared TEST check alone fails. If that diagnostic rerun passes, the workflow may recover a transient TEST failure; it cannot bypass or convert a failed rule/scope gate into success.

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
