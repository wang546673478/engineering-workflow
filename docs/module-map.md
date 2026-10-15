# Engineering Workflow Module Map

Status: `current with TASK-ISSUES-03 complete`
Persistence task: [TASK-PERSISTENCE-01](../planning/persistence-task.md)

## Module: instructions

- Responsibility and owner: Agent workflow instructions, references, templates, public usage guide and managed project-guidance installation; owned by this repository.
- Entrypoints/public interfaces: `SKILL.md`, `README.md`, `AGENTS.md`, `VERSION`, `CHANGELOG.md`, `LICENSE`, `agents/openai.yaml`, `scripts/install_agents_guidance.py`, `scripts/init_manifest.py`, referenced Markdown files, JSON templates, hook templates.
- Callers: Skill selection and engineering tasks using the skill; maintainers explicitly invoke the installer for a project. Other agents can follow a thin native-entry reference to `AGENTS.md` when the host loads that entry.
- Direct dependencies and reason: The instructions route to references and templates; the installer renders the managed template and uses the Python standard library.
- Dependents: `checker` uses manifest and task conventions defined here; `tests` verifies the installer.
- Files read or written: The installer reads its template and project instruction files, then updates only its managed section in `AGENTS.md` and any explicitly selected thin adapter files. Plans and task state are maintained separately in project files. No database access.
- Current state: Existing skill guidance is implemented; the new persistence installer and its exact behavior await the verification recorded in the active task.
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
- Current state: Existing coverage is implemented; issue #11-#13 regression results are recorded in the active task as they run.
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
