# TASK-ISSUES-02: GitHub issues #11-#13

Updated: `2026-10-15` Asia/Shanghai  
Status: `in_progress`  
Base commit: `5b8babf`  
Requirements: `REQ-ISSUES-05`-`REQ-ISSUES-07`  
Acceptance: `AT-ISSUES-05`-`AT-ISSUES-07`

This is the active task record for implementing the three open GitHub issues audited in [the prior issue record](persistence-task.md). The prior task and its approvals remain historical and do not authorize this protected checker/manifest change.

## User request

On 2026-10-15 the user directed: “先处理 #11、#12,然后#13 的 glob 和公共目录规则”. This authorized local implementation of all three issue scopes, documentation and verification. The later user instruction “是不是可以上传GitHub了并且回应issuse了?” authorizes committing, pushing and posting factual replies for this exact implementation scope after the protected checks pass. It does not authorize unrelated changes or issue closure.

## Decisions

- #11: `VERSION` is the single source for the checker report version. Load it relative to the installed checker file, not the process working directory.
- #12: Treat backslash as a portable path separator at the safety boundary. Reject Windows drive-qualified and UNC paths when running on POSIX; continue rejecting out-of-root paths and symlink/junction traversal.
- #13 exclusion grammar: `exclude_paths` supports POSIX-style `*`, `?`, character classes, and `**` only as a complete path segment. `*`, `?`, and character classes match within one segment; `**` matches zero or more complete segments. A matched directory excludes its descendants. Patterns are project-relative; exact literal paths may remain absolute if they resolve inside the project. Root-matching patterns, absolute glob patterns, and `.`/`..` glob segments are invalid. Exclusions never add paths to the allowed-change scopes.
- #13 impact triggers: `when_paths` remain literal paths. In addition to a path inside a selected source/document scope, a strict non-root parent of source paths for at least two distinct selected modules is valid. It triggers the configured documentation requirements for changed descendants but does not expand the allowed-change paths. `document_ids` keeps its existing AND behavior.

These are implementation defaults chosen to fulfill the user's requested glob/common-directory rules while keeping the existing safety boundaries. No schema version change is needed because the existing string path fields gain documented matching semantics.

## Skill review

Catalog source: Codex Skills catalog available in this session. Scope: Python checker behavior, path portability, glob matching, manifest/documentation updates and regression tests. Checked: `2026-10-15T01:36:22+08:00`.

| Skill | Source | Version/date | Decision | Reason and evidence |
| --- | --- | --- | --- | --- |
| `engineering-workflow` | repository `SKILL.md` at this checkout | 1.4.0; base `5b8babf` | adopted | User explicitly requested this workflow; read `SKILL.md`, `references/checker.md`, `references/project-agents-clauses.md`, `references/implementation-workflow.md`, `references/project-documentation.md` and `references/requirements-interview.md`. |
| `tdd` | `C:/Users/54667/.agents/skills/tdd/SKILL.md` | not provided | adopted | Checker behavior requires public CLI regression coverage; read `SKILL.md`, `tests.md` and `mocking.md`. |
| `skill-creator` | `C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md` | not provided | not-adopted | This task changes checker guidance references, not skill structure, metadata or package assets; no package validator is needed. |
| `planning-with-files` | `C:/Users/54667/.agents/skills/planning-with-files/SKILL.md` | not provided | not-adopted | The manifest and this task record already hold plan, decisions, progress and evidence; a second planning system would duplicate state. |

Recheck: scope includes #13 after the prior audit and the release-safety fix removing the stale workflow task default. `tdd` remains adopted for the full checker work; the `.github` control-plane impact is now included. No new technology category was introduced.

## Impact analysis

- Modules: `checker`, `tests`, `instructions`, and `governance`.
- Call path: manifest path inputs -> `safe_path`/scope normalization -> baseline validation and Git change checking -> checker JSON report. Exclusion patterns also affect module-tree traversal before symlink resolution. Impact triggers feed change/commit documentation gates but not changed-path allowlists.
- Documents: update spec requirements/acceptance, module map, business flow, checker contract, checker reference, README usage, this task record and manifest.
- Database: not applicable. No adapter, inventory format, database field, migration or business data behavior changes; checker scope is path validation and documentation gates.
- Compatibility: `VERSION` remains `1.4.0`; prior exact exclusion paths remain valid. New glob patterns require explicit opt-in. Existing literal `when_paths` retain their behavior; only qualifying common ancestors become valid. Root, external, drive/UNC, traversal and link protections remain.
- Control plane: `engineering-manifest.json` and `scripts/check_project.py` are protected. Final human review is required before any commit gate can approve this change. No approval signal will be set during implementation.

## Plan and acceptance scenarios

1. Add one observable regression at a time, run it red, implement the smallest behavior, and run it green.
2. Fix #11 and verify a CLI report reads the canonical `VERSION` value.
3. Fix #12 and verify Windows separators resolve on POSIX while external drive/UNC and traversal inputs fail.
4. Implement #13 glob matching, excluded-tree pruning and common-parent validation/triggering, with regression tests for root and nested dependency trees, path-segment behavior, symlinks, two-module parents, unrelated/single-module parents, and unchanged coverage gates.
5. Update all affected docs and manifest impact rules; run the full declared tests, Python compilation, baseline checker, and diff checks.

Required checks: `TEST`, `COMPILE`. Also run `GUIDANCE-COMPILE` as declared repository-wide baseline verification. Verification status remains pending until executed on the final tree.

## Progress and handoff

- Initial source verification: at base commit `5b8babf`, `scripts/check_project.py` contains `VERSION = "1.3"`, and the baseline report emits `tool_version: "1.3"` while `VERSION` says `1.4.0`.
- The GitHub issue list and bodies confirmed #11-#13 open as of 2026-10-15. Source inspection confirmed the reported code paths.
- Implemented: checker version loading from `VERSION`; portable slash normalization and foreign-drive/UNC rejection; segment-aware exclusion glob matching and pre-link pruning; literal common-parent documentation triggers for two or more selected modules; root/glob trigger rejection and coverage separation.
- Regression coverage: focused tests pass, then full `python -m unittest discover -s scripts/tests -q` passes with 89 tests. The checker baseline run passes with `tool_version: "1.4.0"`; required TEST, COMPILE and GUIDANCE-COMPILE checks pass, with optional database/contracts inventories remaining partial by design. `python scripts/check_project.py --root . --manifest engineering-manifest.json --mode change --base 5b8babf --task TASK-ISSUES-02 --run-checks` reports TEST, COMPILE, GUIDANCE-COMPILE and change-scope pass; only the expected task-gate fails because approval is pending. These are local working-tree results, not committed-tree or hosted-CI evidence.
- Release follow-up: removed the stale `TASK-ISSUES-01` default from the manual reviewed-rules workflow; the task ID must now be supplied explicitly, while push/PR checks continue to consume `workflow.active_task`.
- Human approval: on 2026-10-15 the user answered “批准提交、推送并回复 #11–#13” for the exact TASK-ISSUES-02 scope described above. This approves commit, push and factual replies only; it does not authorize closing issues or altering unrelated files.
- Remaining: stage the reviewed tree, run the approved protected commit gate, commit, run the committed-tree gate, push `main`, then post issue replies and record the resulting commit/URLs. The task remains `in_progress` until those actions and verifications finish.
