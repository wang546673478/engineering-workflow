# Engineering Workflow Contracts

## Checker CLI

- Input: project root, manifest path, mode, task ID, and optional base or commit reference.
- Modes: `baseline`, `change`, `handoff`, `commit`, `committed`.
- Output: JSON containing `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, and `errors`.
- Exit codes: `0` required checks passed; `1` required validation failed; `2` configuration, environment, or unsupported capability error.
- Safety: no shell command composition; declared checks are opt-in through `--run-checks`.
- Protected-rule changes: `commit` and `committed` add a required `control-plane` result. Without human approval this check fails even if ordinary tests pass. The approved path requires both `--allow-control-plane-change` and the previous manifest's approval environment variable set to `1`; if not configured previously, the fixed default is `ENGINEERING_CONTROL_PLANE_APPROVED`.
- Protected scopes: union of old and new `control_plane.protected_paths`, plus the selected manifest and the conventional checker path. The proposed manifest cannot rename the approval variable to authorize itself.
- Approval boundary: a process variable is an operator acknowledgement, not proof of identity or a digital signature. Keep its lifetime to one verification run. A hosted repository still needs trusted reviewer/branch settings to resist modification of the checker itself.
- Hosting: GitHub Actions is optional. The same CLI can be run locally or by another CI system.

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

## Manifest bootstrap helper

- Entrypoint: `scripts/init_manifest.py`.
- Input: project root, output path, and `full` or `lite` profile.
- Behavior: discovers common source directories and writes a planned manifest skeleton without overwriting an existing output unless `--force` is explicit. The skeleton is not completion evidence until paths, requirements, skill review, baseline, approval and checks are reviewed.
- Current status: the new installer and these contracts require verification against the final working tree. Results, exact limitations and pending review are recorded in [TASK-PERSISTENCE-01](../planning/persistence-task.md); no success is implied by this documentation.
