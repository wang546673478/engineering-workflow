# Engineering Workflow Module Map

Status: `current`  
Last verified: `2026-10-14`

## Module: instructions

- Responsibility and owner: Agent workflow instructions, references, templates, and public usage guide; owned by this repository.
- Entrypoints/public interfaces: `SKILL.md`, `README.md`, `agents/openai.yaml`, referenced Markdown files, JSON templates, hook templates.
- Callers: Codex skill selection and engineering tasks using the skill.
- Direct dependencies and reason: The instructions route to references and templates.
- Dependents: `checker` uses manifest and task conventions defined here.
- Tables/fields read or written: None; database-adapter metadata is documented, not stored here.
- Current state: `implemented`
- Evidence: `SKILL.md`, references, templates, README.

## Module: checker

- Responsibility and owner: Validate project manifests, inventories, task gates, documentation impact, staged commits, and committed trees.
- Entrypoints/public interfaces: `scripts/check_project.py`; `baseline`, `change`, `handoff`, `commit`, and `committed` modes.
- Callers: Project hooks, CI, and maintainers.
- Direct dependencies and reason: Python standard library, manifest documents, and adapter metadata validators.
- Dependents: Project-specific hook and CI templates.
- Current state: `implemented`
- Evidence: `scripts/check_project.py`, `scripts/tests/test_checker.py`.
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

- Responsibility and owner: Public behavior regression tests for the checker and metadata adapters.
- Entrypoints/public interfaces: `scripts/tests/test_checker.py` through the declared unittest command.
- Callers: Maintainers and CI.
- Direct dependencies and reason: Checker and adapter public entrypoints.
- Dependents: None at runtime.
- Current state: `implemented`
- Evidence: `scripts/tests/test_checker.py`.

## Module: governance

- Responsibility: the self-maintenance manifest, review records, docs, ignore rules and optional GitHub workflow.
- Entrypoints: `engineering-manifest.json` and `.github/workflows/quality.yml`.
- Consumers: maintainers, the checker and CI runners. Local projects can run the same checks without GitHub.
- Review: changing the manifest, checker, rules or CI listed in `control_plane.protected_paths` blocks commit validation until a human has reviewed that concrete change.
- State: local implementation, awaiting final human review and remote CI execution.

## Dependency rules

Allowed direction: `checker -> adapters`; tests may exercise checker and adapters. Instructions define contracts and governance documents describe the system; neither is a runtime dependency.

Forbidden or risky dependencies: adapters must not read business rows; checker must not silently connect to remote databases; instructions must not override project rules.

Intentionally isolated modules: test fixtures and templates are maintained separately from runtime checker code.
