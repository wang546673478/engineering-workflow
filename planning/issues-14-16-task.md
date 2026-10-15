# TASK-ISSUES-04: Checker process safety and release metadata protection

Updated: `2026-10-15` Asia/Shanghai  
Status: `in_progress`  
Base commit: `24c0d7f`  
Requirements: `REQ-ISSUES-09`-`REQ-ISSUES-11`  
Acceptance: `AT-ISSUES-09`-`AT-ISSUES-11`

This is the current task record for the three new open GitHub issues. Earlier task approvals remain historical and do not authorize this protected checker and manifest change.

## User request and remote audit

The user asked to inspect the three new GitHub issues and determine how to change the repository. The public GitHub API confirmed that issues #14, #15 and #16 are open; issues #1-#13 are closed. No issue state or remote comment is changed by this task unless separately authorized.

| Issue | Finding | Planned behavior |
| --- | --- | --- |
| [#14: null byte in check argv](https://github.com/wang546673478/engineering-workflow/issues/14) | `subprocess.run` can raise `ValueError` before the current exception boundary and emit a traceback | Reject NUL-containing command arguments during manifest validation and return the normal JSON configuration error without executing a command. |
| [#15: unbounded check stdout](https://github.com/wang546673478/engineering-workflow/issues/15) | `stdout=PIPE` buffers the entire command output in memory | Read output incrementally, enforce a fixed 8 MiB per-check capture bound, terminate an over-limit command, and report a failed check with byte count/hash evidence but no raw output. |
| [#16: release metadata outside control plane](https://github.com/wang546673478/engineering-workflow/issues/16) | `VERSION` and `CHANGELOG.md` are documentation/source paths but are not in this repository's protected path list | Add both files to `control_plane.protected_paths`; release metadata changes require the same external review as checker/manifest changes. |

## Decisions

- A NUL byte is a malformed command declaration, so validation fails with exit code 2 and structured JSON. No shell or subprocess is reached.
- Output limits are safety bounds, not test assertions. Existing manifests remain compatible through the fixed 8 MiB bound. Exceeding the bound is a required-check failure, with the child terminated and no output copied into the report.
- The checker records a digest and byte count for the bytes observed, plus whether the limit was exceeded. Interrupted output is marked incomplete. It never includes command arguments or command output in JSON evidence.
- `VERSION` and `CHANGELOG.md` are protected in this repository's manifest. The existing baseline-manifest union and hosted detection will protect both old and new declarations on future changes.

## Skill review

Catalog source: Codex Skills catalog available in this session. Checked: `2026-10-15T00:00:00+08:00` Asia/Shanghai. Scope covers Python subprocess safety, bounded output, manifest control-plane protection, documentation and regression tests.

| Skill | Source | Decision | Reason |
| --- | --- | --- | --- |
| `engineering-workflow` | `C:/Users/54667/.codex/skills/engineering-workflow/SKILL.md` | adopted | Explicit user request; governs task state, impact analysis, protected changes and verification. |
| `tdd` | `C:/Users/54667/.agents/skills/tdd/SKILL.md` | adopted | Public checker behavior needs incremental CLI regression tests. |
| `skill-creator` | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md` | not-adopted | No skill package structure or metadata changes. |
| `planning-with-files` | `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md` | not-adopted | Existing manifest and this task file are the authoritative state. |

The skill review must be rechecked before the protected commit and after any change to the output-limit or control-plane design.

## Impact analysis

- Modules: `checker`, `tests`, `instructions`, `governance`.
- Call path: manifest command validation -> bounded subprocess execution -> JSON check evidence; manifest control-plane paths -> commit/committed review and hosted protected-path detection.
- Contracts: malformed command declarations now fail before execution; check results gain output-limit evidence while the manifest schema remains unchanged.
- Database: not applicable. No adapter, inventory, business table, field, migration or persistence behavior changes.
- Compatibility: existing small outputs and exit/skip semantics remain unchanged. A command that legitimately emits more than 8 MiB must reduce its output or split the check.
- Recovery: an over-limit process is terminated and the check fails; rerunning after reducing output is the recovery path. No generated report is overwritten.
- Control plane: `engineering-manifest.json`, `scripts/check_project.py`, checker guidance and release metadata are protected. The new task approval remains pending until the user reviews the concrete diff.

## Plan and acceptance

1. Add a CLI regression for NUL-containing argv and implement validation before subprocess creation.
2. Add a CLI regression for over-limit output and implement bounded incremental capture with timeout/termination handling.
3. Update the fixed output-limit guidance, protect `VERSION` and `CHANGELOG.md`, and add control-plane regression coverage.
4. Update spec, module map, business flow, contract, README, and this task record; run declared checks and change-scope validation.

Acceptance requires: structured no-traceback rejection for NUL argv; bounded output with a failed over-limit check and no raw output leakage; protected release metadata; focused and full tests; Python compilation; baseline/change checks; and a fresh human review for the protected manifest/checker change.

## Progress and verification

- Remote audit complete: #14-#16 open, no comments, #1-#13 closed; read-only public API access was sufficient and the supplied PAT was not stored.
- Planning and impact record created before implementation. Checker, regression tests, manifest protection and affected docs are implemented.
- Required checks: `TEST`, `COMPILE`, `GUIDANCE-COMPILE`. Local verification is complete for the current worktree.
- Focused checks for #14-#16 pass, and the full suite passes: `python -m unittest discover -s scripts/tests -q` (95 tests).
- Baseline with declared checks passes: `python scripts/check_project.py --root . --manifest engineering-manifest.json --mode baseline --run-checks`; TEST, COMPILE and GUIDANCE-COMPILE pass. Optional database/contracts inventories remain partial by design.
- Direct Python compilation and `git diff --check` pass. Change-scope against `24c0d7f` passes with the approved task gate.
- Human approval: on 2026-10-15 the user stated “我已经审阅了文档的变更,同意这样做”, approving the exact #14-#16 implementation, tests, documentation and release-metadata protection described in this file. This authorizes the local commit gate and commit; it does not authorize pushing, issue replies or issue closure.
- Approval status: approved for local commit; push and issue communication remain pending separate authorization.
- Local commit `1ba0b21` passed the protected `commit` gate with external approval. Its exact tree passed `committed` verification with TEST (95 tests), COMPILE and GUIDANCE-COMPILE; optional database/contracts inventories remain partial by design.

## Handoff

Current checkout is `24c0d7f`, clean before this task. After implementation, record focused/full test results, baseline/change/commit gate results, the reviewed diff, and the user's separate approval before any commit or publication.
