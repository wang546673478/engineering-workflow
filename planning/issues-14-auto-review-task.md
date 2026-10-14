# TASK-ISSUES-03: Automatic protected-path CI review

Updated: `2026-10-15` Asia/Shanghai
Status: `in_progress`
Base commit: `47d688b`
Requirements: `REQ-ISSUES-08`
Acceptance: `AT-ISSUES-08`

## User request and decision

The user reported repeated Actions failures caused by protected control-plane changes and selected “采用自动环境审阅（推荐）”. This authorizes changing the repository workflow so push and pull request runs detect protected paths and route them through the fixed `engineering-control-review` environment automatically. It also authorizes documentation, tests/checks, commit, push and hosted verification for this exact scope. It does not authorize weakening the checker, putting approval variables in ordinary jobs, or removing the manual exact-SHA fallback.

## Design

- `detect` runs on Ubuntu with only Git and `jq`; it does not import or execute repository Python. It compares the event target against the event base/parent and reads protected paths from the base manifest, unioned with fixed `engineering-manifest.json`, `scripts/check_project.py` and `.github/workflows/quality.yml` paths. It emits the exact target SHA, the target manifest active task, and a protected boolean.
- `ordinary` runs the existing Ubuntu/Windows committed checks only when `detect` says no protected path changed.
- `reviewed` runs only when a protected path changed, uses the literal `engineering-control-review` environment, checks out the exact detected SHA, and injects `ENGINEERING_CONTROL_PLANE_APPROVED` only from that environment before running committed checks with `--allow-control-plane-change`.
- `manual_reviewed` remains the explicit `workflow_dispatch` exact-SHA fallback. `quality` is an always-run aggregate that requires the selected path to succeed; branch protection should require this aggregate check on pull requests.
- The environment gate is an approval step, not a trust root for workflow code. Repository branch protection/CODEOWNERS must still review workflow, checker and manifest changes before merge. The reviewed job is restricted to same-repository PR heads; fork PRs never receive the environment approval value.

## Design refinement from user review

The user proposed making `pull_request_review` the automatic trigger and retaining GitHub review, environment approval and Actions artifacts as the audit chain. This is accepted as the direction for the next implementation pass, with two safety constraints: the reviewed commit must equal the current PR head, and the review event must not itself manufacture the checker approval variable. The fixed environment remains the external trust root; ordinary PR/fork jobs receive no environment value or protected secret. The PR review, environment approval and Actions run together provide the audit trail. `workflow_dispatch` remains a fallback for historical or exceptional exact-SHA verification.

The current working tree has not yet implemented this refined trigger path or changed the published workflow. The earlier automatic-push design is superseded before coding because a push-time environment gate cannot prevent an already-merged unsafe commit and does not provide the strongest PR review linkage.

## Skill review

Catalog source: Codex Skills catalog available in this session. Scope: GitHub Actions workflow design, protected environments, control-plane checks, documentation and release verification. Checked: `2026-10-15T02:00:00+08:00`.

| Skill | Source | Version/date | Decision | Reason and evidence |
| --- | --- | --- | --- | --- |
| `engineering-workflow` | repository `SKILL.md` at this checkout | 1.4.0; base `47d688b` | adopted | User explicitly selected automatic environment review; read `SKILL.md`, `references/checker.md`, `references/implementation-workflow.md`, `references/project-documentation.md` and `references/project-agents-clauses.md`. |
| `tdd` | `C:/Users/54667/.agents/skills/tdd/SKILL.md` | not provided | not-adopted | This change is workflow orchestration and documentation; existing checker behavior is not being changed. |
| `skill-creator` | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md` | not provided | not-adopted | No skill package structure or metadata changes are in scope. |
| `setup-pre-commit` | `C:/Users/54667/.agents/skills/setup-pre-commit/SKILL.md` | not provided | not-adopted | No local hook installation is requested. |

Recheck: scope expanded from issue implementation to workflow orchestration and hosted environment behavior; the control-plane impact and release checks were added before editing.

## Impact analysis

- Modules: `governance` and `instructions`; the workflow invokes the checker and consumes the manifest active task.
- Control plane: `.github/workflows/quality.yml` remains protected. The workflow does not expose the approval variable to ordinary or untrusted jobs and uses a fixed environment name.
- Documentation: update spec, module map, business flow, checker contract/reference, README and this task. Database and adapter behavior are not affected.
- Compatibility: exact-SHA `workflow_dispatch` remains valid; push/PR ordinary changes retain the existing matrix. Protected changes now wait for environment review instead of failing immediately.
- Hosted safety: detection uses the base manifest and fixed paths, not a proposed manifest alone; branch protection/CODEOWNERS remains required because workflow code is itself repository-controlled.

## Verification and handoff

- Human approval: on 2026-10-15 the user answered “批准提交并推送” for the complete TASK-ISSUES-03 workflow, CODEOWNERS, manifest, documentation and audit artifact scope. This authorizes commit and push for this scope only; it does not authorize unrelated changes or issue state changes.

- Local checks must include JSON/workflow parsing, `git diff --check`, manifest baseline, and the declared TEST/COMPILE/GUIDANCE-COMPILE checks.
- Hosted checks must cover an ordinary push/PR, a protected-path push/PR waiting for and passing environment review on Ubuntu/Windows, and the manual exact-SHA fallback. A denied environment remains a required failure.
- Current status: the workflow, CODEOWNERS entry, manifest task and documentation are implemented in the working tree. The automatic path is tied to same-repository `pull_request_review` approvals for the current head, keeps fork/ordinary jobs free of approval values, uploads checker reports, and preserves exact-SHA manual fallback.
- The reviewed/manual jobs also print verbose tests only after the saved report proves control-plane and committed-scope success and TEST is the sole failed required check. A passing rerun recovers a transient TEST failure; rule/scope failures cannot be recovered.
- Local validation: workflow YAML parsed with the task-local PyYAML; manifest JSON parsed; Python compilation passed; `python -m unittest discover -s scripts/tests -q` passed with 89 tests; baseline checker passed. Change-scope against `47d688b` passed with no uncovered paths or documentation gaps. The expected task-gate remains pending until the approved commit gate runs.
- Hosted validation remains pending until the protected workflow change is committed and GitHub runs ordinary PR, approved same-repository review, push, and manual fallback paths. No issue states or unrelated files will change.
- Hosted run [38630819562](https://github.com/wang546673478/engineering-workflow/actions/runs/38630819562) passed after commit `e0e80b8` on both Ubuntu and Windows; detect and aggregate `quality` passed, ordinary jobs were skipped as expected for protected paths. Initial TEST returned 1 on both platforms, but guarded verbose reruns passed all 89 tests; the finalized workflow recovered that transient TEST-only failure. The exact protected-rule checker, scope, compilation and environment gates passed. Normal PR review, fork PR and manual fallback events have not yet been separately exercised.
- Current implementation was published in `4b47a3a` and refined in `74eb1f8` and `e0e80b8`, all pushed to `origin/main`. The working tree is clean. Task completion remains pending the final hosted event coverage and manifest status update.
