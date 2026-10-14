# Engineering Workflow Contracts

## Checker CLI

- Input: project root, manifest path, mode, task ID, and optional base or commit reference.
- Modes: `baseline`, `change`, `handoff`, `commit`, `committed`.
- Output: JSON containing `tool_version`, `mode`, `required_checks_satisfied`, `checks`, `summary`, `changed_paths`, and `errors`.
- `tool_version` is read from the repository-root `VERSION` file beside the checker package.
- Exit codes: `0` required checks passed; `1` required validation failed; `2` configuration, environment, or unsupported capability error.
- Safety: no shell command composition; declared checks are opt-in through `--run-checks`.
- Protected-rule changes: `commit` and `committed` add a required `control-plane` result. Without human approval this check fails even if ordinary tests pass. The approved path requires both `--allow-control-plane-change` and the previous manifest's approval environment variable set to `1`; if not configured previously, the fixed default is `ENGINEERING_CONTROL_PLANE_APPROVED`.
- Protected scopes: union of old and new `control_plane.protected_paths`, plus the selected manifest and the conventional checker path. The proposed manifest cannot rename the approval variable to authorize itself.
- Approval boundary: a process variable is an operator acknowledgement, not proof of identity or a digital signature. Keep its lifetime to one verification run. A hosted repository still needs trusted reviewer/branch settings to resist modification of the checker itself.
- Hosting: GitHub Actions is optional. The same CLI can be run locally or by another CI system.
- Hosted review: ordinary PR/fork jobs never receive the control-plane approval value. A protected environment may run the committed check only after a reviewer-approved same-repository PR review is tied to the current exact commit; fork PRs remain subject to branch protection and a maintainer-controlled fallback. Manual exact-SHA dispatch remains a fallback. A single aggregate quality result should be the required branch-protection check.

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
- An explicit CLI `--task` takes precedence, followed by `ENGINEERING_TASK_ID`; when neither is supplied, checker commit/committed/handoff modes use `workflow.active_task`.
- Reusable CI must consume this pointer or provide an explicit runtime task ID. Historical task IDs must not be hard-coded into workflow files.

## Manifest bootstrap helper

- Entrypoint: `scripts/init_manifest.py`.
- Input: project root, output path, and `full` or `lite` profile.
- Behavior: discovers common source directories and writes a planned manifest skeleton without overwriting an existing output unless `--force` is explicit. The skeleton is not completion evidence until paths, requirements, skill review, baseline, approval and checks are reviewed.
- Current status: the new installer and these contracts require verification against the final working tree. Results, exact limitations and pending review are recorded in [TASK-PERSISTENCE-01](../planning/persistence-task.md); no success is implied by this documentation.
