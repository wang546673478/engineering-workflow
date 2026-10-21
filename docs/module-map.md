# Engineering Workflow Module Map

同批技术保持性修正：提交校验在单次main内复用control-plane已读取的历史manifest，避免重复Git查询；缓存不跨验证运行。静态合同用例经同一公开CLI入口减少解释器启动，原安全断言、测试/超时/同步边界保持。新源码门槛结果见Issue23 Task/evidence。

源上传回执（2026-10-21）：实现9723921已通过原提交门槛并核对origin/main；本次仅同步发布事实，运行合同与技术范围不变。详见当前Issue23 Task/evidence。

## Issue 23 current implementation / 1.8.0

The existing checker owns structured approval parsing, stable section digests, task/batch/REQ/AT and current Spec/Plan bindings, reuse/sequence validation and historical policy comparison. init_manifest emits diagnostic policy; adopt_project previews/applies explicit migration without manufacturing approvals. Existing hooks optionally pass the capability flag. Instructions remain the semantic authority; no new runtime dependency or product database exists. Tests exercise actual CLI/Git and migration boundaries. [Task](../planning/issue-23-task.md) owns current verification.


## Issue 23 current factual supplement

Existing checker lifecycle/file gates and legacy compatibility are unchanged. The scoped audit found approval-content/current-batch gaps; governance links the candidate solution without adding a runtime dependency or implementation. [Plan](../planning/issue-23-plan.md), [facts B23-01..07](../planning/baseline-review.md), [Task](../planning/issue-23-task.md).

Status: `current`; active task and current evidence are selected by `workflow.active_task` in [the manifest](../engineering-manifest.json).
Persistence history: [TASK-PERSISTENCE-01](../planning/persistence-task.md)

## Module: instructions

- Issue 22 current guidance (1.7.2): implementation-workflow owns defect evidence, baseline-linked-artifacts owns delivery discrepancy classification and routing, requirements-interview owns optional EARS/Given–When–Then examples. SKILL/README route to these original owners; the two existing templates offer optional prompts. Task/impact/Spec remain project-owned records. No new module, executable dependency or automatic migration is added; current evidence is in [Task](../planning/issue-22-task.md).

- Responsibility and owner: Agent workflow instructions, references, templates, public usage guide and managed project-guidance installation; owned by this repository.
- Entrypoints/public interfaces: `SKILL.md`, `README.md`, `AGENTS.md`, `VERSION`, `CHANGELOG.md`, `LICENSE`, `agents/openai.yaml`, `scripts/install_agents_guidance.py`, `scripts/init_manifest.py`, `scripts/adopt_project.py`, referenced Markdown files, JSON templates, hook templates.
- Callers: Skill selection, feature-change discussions and engineering tasks using the skill, including follow-up answers in an adopted project's active task; maintainers explicitly invoke the installer for a project. Other agents can follow a thin native-entry reference to `AGENTS.md` when the host loads that entry.
- Direct dependencies and reason: The instructions route to references and templates; the installer renders the managed template, and adoption calls the bundled checker for read-only diagnostics.
- Dependents: `checker` uses manifest and task conventions defined here; `tests` verifies the installer.
- Files read or written: The installer reads its template and project instruction files, then updates only its managed section in `AGENTS.md` and any explicitly selected thin adapter files. Plans and task state are maintained separately in project files. No database access.
- Current state: Skill guidance and the persistence installer are implemented. The 1.5.0 linked-artifact implementation adds an explicit Baseline → Spec → Plan → Task chain, revision pointers, and evidence-driven Baseline correction; current scope and verification belong to [TASK-LINKED-ARTIFACTS-01](../planning/linked-artifact-model-task.md).
- Evidence: `SKILL.md`, `AGENTS.md`, references, templates, `scripts/install_agents_guidance.py`, `scripts/init_manifest.py`, README.
- Current greenfield entry: init_manifest explicitly selects existing/greenfield, declares future implementation scopes without creating them, and emits a planned skeleton. Both profiles require linked view files; full/lite differ in inventories and impact gates. Existing-document reconciliation refreshes authority and links while retaining original review history.

## Module: checker

- Responsibility and owner: Validate project manifests, inventories, task gates, documentation impact, staged commits, and committed trees.
- Entrypoints/public interfaces: `scripts/check_project.py`; `discovery`, `baseline`, `change`, `handoff`, `commit`, and `committed` modes.
- Callers: Project hooks, CI, and maintainers.
- Direct dependencies and reason: Python standard library, manifest documents, and adapter metadata validators.
- Dependents: Project-specific hook and CI templates.
- Current state: `implemented`; #11-#13 path/version rules and #14-#16 process-safety/release-protection rules are tracked in `TASK-ISSUES-04`. The linked-artifact change adds optional validation for active Baseline/Spec/Plan pointers, Baseline document IDs and Task artifact links while preserving old manifests.
- Evidence: `scripts/check_project.py`, `scripts/tests/test_checker.py`, `references/checker.md`, `docs/contracts.md`.
- Current lifecycle behavior: origin=greenfield provisional states require metadata/scopes; declared files invalidate not_applicable even if excluded, and completion/handoff reject provisional baselines. These are required structural checks, not automatic proof of project origin or semantic/revision agreement.
- Protected-rule checks: commit modes read the previous manifest from Git and combine previous and proposed protected scopes. Approval comes from outside the submitted manifest; these checks do not authenticate a human or replace protected branch settings.
- Conversation boundary: the checker has no conversation-message input and validates only supplied files and declarations. Continuous requirement recording and semantic review remain agent/user responsibilities; the 1.5.0 implementation adds optional linked references and explicit provisional lifecycle checks.

## Module: adapters

- Responsibility and owner: Read-only metadata snapshots for SQLite, MySQL, PostgreSQL, and Redis.
- Entrypoints/public interfaces: `scripts/extract_sqlite.py`, `scripts/extract_database.py`.
- Callers: Explicit maintainer commands and offline inventory validation.
- Direct dependencies and reason: SQLite standard library; optional remote database drivers.
- Dependents: Checker inventory validation and database inventory documentation.
- Current state: `implemented` with declared metadata limits.
- Evidence: adapter scripts, tests, and `docs/database.md`.

## Module: tests

- Responsibility and owner: Public behavior regression tests for the checker, metadata adapters and managed-guidance installer.
- Entrypoints/public interfaces: `scripts/tests/test_checker.py`, `scripts/tests/test_guidance.py` and `scripts/tests/test_init.py` through the declared unittest command; init fixtures exercise the full/lite empty-project-to-factual-baseline transition.
- Callers: Maintainers and CI.
- Direct dependencies and reason: Checker, adapter and installer public entrypoints.
- Dependents: None at runtime.
- Current state: Existing coverage is implemented; historical issue regression results remain in their task records, and fresh verification is recorded in the manifest-selected task.
- Evidence: `scripts/tests/test_checker.py`, `scripts/tests/test_guidance.py`.

## Module: governance

- Responsibility: the self-maintenance manifest, review records, docs, ignore rules, release metadata protection and optional GitHub workflow.
- Entrypoints: `engineering-manifest.json` (`workflow.active_task`), [the persistence task record](../planning/persistence-task.md), `.github/workflows/quality.yml` and `.github/scripts/finalize_reviewed_quality.py`.
- Consumers: maintainers, the checker and CI runners. Local projects can run the same checks without GitHub.
- Review: changing the manifest, checker, rules or CI listed in `control_plane.protected_paths` blocks commit validation until a human has reviewed that concrete change.
- State: The historical approved tasks remain intact. `TASK-ISSUES-02` and `TASK-ISSUES-03` are complete and published. CI consumes the manifest pointer instead of copying a historical task ID into workflow code. The repository owner chose to keep direct pushes; protected push checks happen after publication and are not a merge-prevention control.
- The governance workflow also owns automatic PR-review-linked protected checks: ordinary jobs receive no approval value, the fixed environment gates exact commits, and the aggregate `quality` check is intended for branch protection.
- Reviewed workflow diagnostics are owned by governance and are constrained to rule-valid, TEST-only failures; they do not change checker or test ownership.
- Diagnostic reruns are owned by governance and run only after the report proves rule/scope validation passed with TEST alone failing. They provide verbose failure context and never replace the original required checker result; any original checker failure blocks the reviewed and aggregate jobs.
- Source commit `82b3c8531a9a9867dd77756444a2bcbc922aa2c8` and receipt commits passed local commit and committed checks. Implementation SHA `3fab75ba5d8e2663af811d2b7daee53c90fe6818` passed the exact-SHA protected Ubuntu/Windows review and aggregate quality run `39115700117`; both checker artifacts were uploaded.
- Release metadata (`VERSION` and `CHANGELOG.md`) is within the protected review scope so a checker report cannot be re-labeled silently.

## Dependency rules

Allowed direction: `instructions -> checker -> adapters` for read-only adoption diagnostics; tests may exercise checker, adapters and the installer in `instructions`. The installer reads the maintained guidance template. Project-specific state stays in the project, while governance documents describe this repository.

Forbidden or risky dependencies: adapters must not read business rows; checker must not silently connect to remote databases; instructions must not override project rules.

Other-agent references do not duplicate the canonical workflow. Their presence does not guarantee automatic loading by a host; the project's selected agent and rule-file configuration determine that behavior.

Intentionally isolated modules: test fixtures and templates are maintained separately from runtime checker code.

## First-takeover stage ownership

SKILL.md owns the stage sequence; requirements-interview and project-documentation define the interview/baseline boundary; implementation-workflow restores the stage; project-agents-clauses and the Spec/Plan/Task template carry state and evidence into projects. The checker does not infer semantic completeness or enforce conversational transitions. See [TASK-STAGES-01](../planning/takeover-stages-task.md).

## Continuous discussion ownership

SKILL.md owns applicability and continuity; AGENTS and its managed template provide the persistent project entry. Requirements-interview owns ongoing recording and module-review timing; project-documentation defines authoritative requirement/current-state views; implementation-workflow restores the latest state and dependent deferred topics. The Task and decision templates carry separate requirement/implementation states and review evidence. The agent maintains those project files; the user reviews a module's meaning, scope and omissions after its discussion converges. Module review retains the existing baseline and full implementation-proposal boundaries. Host discovery and model compliance are outside the installer and checker contracts.

The 1.4.3 source publication occurred on 2026-10-16 and is recorded in TASK-CONTINUITY-01. Its date/status receipt changes no module responsibilities or dependencies and does not require another version.

## Version policy ownership

SKILL.md owns the delivery obligation; implementation-workflow defines batch, compatibility, source synchronization and changelog rules; the Task template and project clauses persist release impact. VERSION remains this repository's canonical version, reflected in skill metadata, README and existing agent metadata. The checker reads VERSION and protects release files but does not infer a version bump or changelog completeness. See [TASK-VERSION-01](../planning/version-policy-task.md).

The 1.4.2 source publication is recorded in that task. The date/status receipt changes no module responsibilities or dependencies and does not require a new version.

## Baseline investigation and correction ownership

SKILL.md owns the autonomous investigation loop and stopping conditions. Project-documentation owns revision/scope coverage, agent semantic review, user scope acceptance, capability preflight and correction history. Implementation-workflow owns authorized local environment setup, teardown, evidence freshness and dependent-work recovery. Requirements-interview keeps factual investigation separate from missing user decisions.

The managed AGENTS block and linked-artifact Task template carry these responsibilities into projects. The manifest example and initializer expose Baseline/Spec/Plan/Task pointers, while source inventories stay optional pending capability review and database/contract documents remain required. The agent corrects current factual documents; the user reviews product decisions and invalidated implementation premises. Existing manual/partial and required-gate semantics remain implemented as before.

The 1.4.4 source was uploaded on 2026-10-17, as recorded in TASK-BASELINE-01. The current 1.5.0 linked-artifact candidate is recorded in TASK-LINKED-ARTIFACTS-01 and remains Unreleased; its scope changes the guidance/template/checker linkage, not adapters or product runtime dependencies.

Publication: the 1.5.0 module implementation was uploaded on 2026-10-18 as `46d57a6cefd5cc80ae62e47099b782d4cb381504`; exact local commit checks are in the active Task, while hosted CI is tracked separately.


## Module: source-context

Owns local inventory, full-text packing, read limits/statuses, optional JS/TS/Rust module reference adapters and validated derived graph/text/table. Entrypoints scripts/collect_code_context.py and source_relations.py; depends on checker safe-root/path/glob helpers without modifying its rules. Rust uses optional pinned tree-sitter parsers, JS/TS optional pinned TypeScript. Data stays in caller-chosen local outputs; no business database/model calls. Scope/evidence: [Task](../planning/source-context-task.md), [guide](../references/source-context.md).


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](../planning/source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](../planning/source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


## Issue #17/#18 ownership (1.6.3)

instructions owns the new explicit initializer default and verification setup documentation; checker continues consuming explicit manifest excludes without hidden pruning or required-test policy changes. source-context owns grouped dependency diagnostics derived from existing unsupported records and the additive CLI/status/text output. tests owns required parser setup failures and missing/mixed/zero-reference regressions. governance owns versioned evidence, active task and publication/issue receipts. No new cross-module dependency or business database is introduced.

Current scope, source and validation: [TASK-ISSUES-17-18](../planning/issues-17-18-task.md).


Publication receipt: the 1.6.3 source-context/instructions/test changes are on main at 0040878; fresh 170-test local gates passed. The receipt introduces no module, entrypoint or dependency changes.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.


## 1.6.4 checker ownership

checker retains JSON/file/history policy, Git input/result binding, CLI cancellation handlers and native Windows job/POSIX group ownership in the existing protected check_project.py. tests owns real Git/hook, invalid-input and native lifecycle regressions; governance/instructions own reports, limits, version and publication records. No critical helper is moved outside the protected checker. ctypes/kernel32 is Windows-only standard-library/native support; no new package dependency or business database is introduced.

Scope and evidence: [TASK-ISSUES-19-21](../planning/issues-19-21-task.md).


Published implementation5f9b3e1d54a0709241fb5f11173e13ce00af3ffd passed local184-test staged/exact-commit gates and original Windows/Ubuntu reports in approved run39157028881; source upload and #19/#20/#21 replies/completed closure were verified on 2026-10-19. Receipt-only updates do not change implementation, targets, limits or prior approval scope.

## Complete adoption and declared stage gates (1.7.0)

The instructions module owns `adopt_project.py`, the initializer, shared guidance-target preflight and `references/adoption-lifecycle.md`. Adoption imports the bundled checker for a read-only bootstrap diagnostic; the checker does not import adoption or execute its helpers. This adds instructions → checker → adapters as allowed dependencies, with no reverse edge. The command creates a planned manifest and managed guidance, maps existing document paths, and records actual skill/checker provenance. Explicit legacy upgrades preserve policy/documents/history and use a same-directory atomic replacement; reruns preserve lifecycle state.

The checker maps original workflow stages, evidenced greenfield/small-fix exceptions, valid prior-review reuse, proposal/task authorization and implementation scopes without adding review rounds. Complete/approved delivery and guidance-first adoption remain available. Existing manifests without stage retain compatibility and explicitly lack these new gates. Tests exercise real CLI scaffolds, failure preservation, stage/revision/task mismatches, absolute scopes and refusal to execute commands in blocked commit modes. Runtime database adapters and application data are unaffected. Current boundaries and evidence: [Task](../planning/adoption-lifecycle-task.md).

Publication receipt (2026-10-19): implementation c15b94397314b8e84b3ee94877267f8245c3351c passed original local staged/exact-commit gates with 205 tests and the unchanged 120-second limit, was uploaded to main, and was installed as 1.7.0 with prior local work preserved. GitHub run39277812120 has a verified human environment approval but original platform reports are still pending; no hosted pass is claimed. This receipt changes evidence/status only, not source behavior or acceptance.

1.7.1 correction: normalize initializer library roots through the same existing project_root function as the CLI; hosted Windows exposed short-name aliases. Scope checks and the original workflow remain unchanged; 1.7.0 Ubuntu success/Windows failure are historical, and fresh local/exact/hosted checks are required.
