# Engineering Workflow Module Map

Status: `current`; active task and current evidence are selected by `workflow.active_task` in [the manifest](../engineering-manifest.json).
Persistence history: [TASK-PERSISTENCE-01](../planning/persistence-task.md)

## Module: instructions

- Responsibility and owner: Agent workflow instructions, references, templates, public usage guide and managed project-guidance installation; owned by this repository.
- Entrypoints/public interfaces: `SKILL.md`, `README.md`, `AGENTS.md`, `VERSION`, `CHANGELOG.md`, `LICENSE`, `agents/openai.yaml`, `scripts/install_agents_guidance.py`, `scripts/init_manifest.py`, referenced Markdown files, JSON templates, hook templates.
- Callers: Skill selection, feature-change discussions and engineering tasks using the skill, including follow-up answers in an adopted project's active task; maintainers explicitly invoke the installer for a project. Other agents can follow a thin native-entry reference to `AGENTS.md` when the host loads that entry.
- Direct dependencies and reason: The instructions route to references and templates; the installer renders the managed template and uses the Python standard library.
- Dependents: `checker` uses manifest and task conventions defined here; `tests` verifies the installer.
- Files read or written: The installer reads its template and project instruction files, then updates only its managed section in `AGENTS.md` and any explicitly selected thin adapter files. Plans and task state are maintained separately in project files. No database access.
- Current state: Skill guidance and the persistence installer are implemented. Version1.4.3 was published; its historical evidence remains in [TASK-CONTINUITY-01](../planning/continuous-requirements-task.md). The local1.4.4 candidate adds autonomous investigation and dynamic baseline maintenance; current scope and verification belong to [TASK-BASELINE-01](../planning/baseline-workflow-task.md).
- Evidence: `SKILL.md`, `AGENTS.md`, references, templates, `scripts/install_agents_guidance.py`, `scripts/init_manifest.py`, README.

## Module: checker

- Responsibility and owner: Validate project manifests, inventories, task gates, documentation impact, staged commits, and committed trees.
- Entrypoints/public interfaces: `scripts/check_project.py`; `baseline`, `change`, `handoff`, `commit`, and `committed` modes.
- Callers: Project hooks, CI, and maintainers.
- Direct dependencies and reason: Python standard library, manifest documents, and adapter metadata validators.
- Dependents: Project-specific hook and CI templates.
- Current state: `implemented`; #11-#13 path/version rules and #14-#16 process-safety/release-protection rules are tracked in `TASK-ISSUES-04`.
- Evidence: `scripts/check_project.py`, `scripts/tests/test_checker.py`, `references/checker.md`, `docs/contracts.md`.
- Protected-rule checks: commit modes read the previous manifest from Git and combine previous and proposed protected scopes. Approval comes from outside the submitted manifest; these checks do not authenticate a human or replace protected branch settings.
- Conversation boundary: the checker has no conversation-message input and validates only supplied files and declarations. Continuous requirement recording and module semantic review are agent/user responsibilities; this batch adds no checker behavior.

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
- Entrypoints/public interfaces: `scripts/tests/test_checker.py` and `scripts/tests/test_guidance.py` through the declared unittest command.
- Callers: Maintainers and CI.
- Direct dependencies and reason: Checker, adapter and installer public entrypoints.
- Dependents: None at runtime.
- Current state: Existing coverage is implemented; historical issue regression results remain in their task records, and fresh verification is recorded in the manifest-selected task.
- Evidence: `scripts/tests/test_checker.py`, `scripts/tests/test_guidance.py`.

## Module: governance

- Responsibility: the self-maintenance manifest, review records, docs, ignore rules, release metadata protection and optional GitHub workflow.
- Entrypoints: `engineering-manifest.json` (`workflow.active_task`), [the persistence task record](../planning/persistence-task.md) and `.github/workflows/quality.yml`.
- Consumers: maintainers, the checker and CI runners. Local projects can run the same checks without GitHub.
- Review: changing the manifest, checker, rules or CI listed in `control_plane.protected_paths` blocks commit validation until a human has reviewed that concrete change.
- State: The historical approved tasks remain intact. `TASK-ISSUES-02` and `TASK-ISSUES-03` are complete and published. CI consumes the manifest pointer instead of copying a historical task ID into workflow code. The repository owner chose to keep direct pushes; protected push checks happen after publication and are not a merge-prevention control.
- The governance workflow also owns automatic PR-review-linked protected checks: ordinary jobs receive no approval value, the fixed environment gates exact commits, and the aggregate `quality` check is intended for branch protection.
- Reviewed workflow diagnostics are owned by governance and are constrained to rule-valid, TEST-only failures; they do not change checker or test ownership.
- Diagnostic recovery is part of the governance workflow contract: a passing verbose rerun may recover a transient TEST result after rule validation, while checker failures remain blocking.
- Release metadata (`VERSION` and `CHANGELOG.md`) is within the protected review scope so a checker report cannot be re-labeled silently.

## Dependency rules

Allowed direction: `checker -> adapters`; tests may exercise checker, adapters and the installer in `instructions`. The installer reads the maintained guidance template. Project-specific state stays in the project, while governance documents describe this repository.

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

The managed AGENTS block and Task template carry these responsibilities into projects. The manifest example now matches init_manifest full: source inventories start optional pending capability review; database/contract documents remain required. The agent corrects current factual documents; the user reviews product decisions and invalidated implementation premises. No checker, adapter, runtime dependency, CI or module dependency changed. Existing manual/partial and required-gate semantics remain implemented as before.
