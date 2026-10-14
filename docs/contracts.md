# Engineering Workflow Contracts

## Checker CLI

- Input: project root, manifest path, mode, task ID, and optional base or commit reference.
- Modes: `baseline`, `change`, `handoff`, `commit`, `committed`.
- Output: JSON containing `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, and `errors`.
- Exit codes: `0` required checks passed; `1` required validation failed; `2` configuration, environment, or unsupported capability error.
- Safety: no shell command composition; declared checks are opt-in through `--run-checks`.

## Database adapter snapshot

- Input: explicit adapter command and optional environment-provided connection URL.
- Output: database metadata inventory with provenance and snapshot hashes.
- Safety: no credentials, business rows, Redis keys, or Redis values in output.
- Unsupported behavior: unavailable optional driver, credentials, connection, or unsupported metadata scope is reported as unsupported.
