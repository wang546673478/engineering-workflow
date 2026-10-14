# Engineering Workflow Maintenance Flow

Status: `current with TASK-ISSUES-02 implementation in progress`

## Checker path and documentation flow

1. The checker reads manifest paths and normalizes `/` and `\\` separators at the safety boundary; foreign drive/UNC paths on POSIX, root escapes and link traversal fail before validation continues.
2. Baseline validation resolves literal documents and modules. Exclusion globs are validated as project-relative segment patterns, and matching directory subtrees are pruned before child links are inspected.
3. Change/commit validation compares Git paths against literal module/document coverage. Excluded paths are reported separately and are not coverage. A `when_paths` common parent shared by source scopes from at least two selected modules triggers all configured documentation updates, but does not make unrelated descendants covered.
4. The checker emits a JSON report whose `tool_version` comes from the package `VERSION` file; declared tests run only after manifest and scope checks pass.

## Persistent project adoption and recovery

1. The project chooses to adopt engineering-workflow. The agent reads existing project rules and selects the project's existing manifest, task and state locations.
2. Merge the managed block into repository-root `AGENTS.md`, preserving rules outside its markers. The installer can repeat this update. Record the skill source/revision and canonical state locations in project files.
3. For a project's selected agent, add a thin reference from its native instruction entry to `AGENTS.md` only when needed. Check the host's loading behavior; do not assume that every agent discovers every filename.
4. At task start, resume, handoff, incomplete context, agent change or scope change, reload project rules, the adopted skill source/revision, manifest, `workflow.active_task` (unless an explicit task ID is supplied), and recent progress/handoff before editing. Reconcile those records with the working tree; scope changes refresh skill review and impact analysis.
5. Keep plans, decisions, impact, progress, verification and handoff in the project's authoritative files. `AGENTS.md` remains the stable entry, rather than accumulating every task's history.
6. Review and verify the concrete adoption change. New protected-rule changes require their own final approval; a past task's approval cannot be reused. Missing skill access or unverified host integration is recorded explicitly.
7. CI consumes the manifest's active task pointer instead of copying a historical task ID into workflow files. Changing the active task is a governed manifest/state change and must be reviewed with its documentation impact.

This repository's current adoption work is [TASK-PERSISTENCE-01](../planning/persistence-task.md). Installer validation, final approval and publication remain pending in that record. The GitHub issue review in the same record is an audit only.

## Skill change path

1. Maintainer identifies a workflow, checker, adapter, documentation, or release change.
2. Applicable skills are reviewed and recorded in the active task `skill_review`.
3. The module map and impact record identify affected modules, contracts, database boundaries, and tests.
4. Code and the corresponding documentation are staged together.
5. Tests, compilation and independent skill structure validation produce a concrete result for human review. Explain the result and any choices in plain language.
6. The `commit` gate checks the index. Protected-rule edits remain blocked until the user reviews those edits; approval to implement is not approval of the finished rules. Exercise the approval path only in disposable test fixtures while review is pending.
7. After the reviewed change is committed, use `committed` locally or in the project's chosen CI. GitHub and GitHub Actions are optional for users of the skill; this repository opts in to Actions.

## Failure and recovery

| Trigger | Expected behavior | Recovery |
| --- | --- | --- |
| Missing manifest or baseline evidence | Baseline fails | Restore the missing control document and rerun baseline |
| Code change without declared documentation impact | Commit gate fails | Add the canonical gate and update the affected documents |
| Protected rule changed without human approval | Protected-rule gate fails | Show the exact change and its effect to the reviewer; after approval supply the short-lived external acknowledgement |
| Shallow or incomplete Git history | Submission check cannot establish prior rules; commands are not run | Obtain the missing history and rerun the check |
| Required test fails or is skipped | Handoff remains incomplete | Fix the failure or document a user-approved scope change |
| Remote adapter lacks driver/credentials | Adapter reports unsupported | Install the optional driver or use an offline snapshot |
| Managed guidance markers are malformed or a target leaves the project root | Installer rejects the target | Correct the selected target or conflicting block; preserve project-authored rules |
| Native instruction entry is not loaded by the selected host | Automatic persistence is unverified | Use the host's supported project-rule entry and verify that it follows the canonical file |
| Skill or task state cannot be read after resumption | Missing context remains explicit | Record the missing source and recover the authoritative project files before dependent work |

## Ownership

The repository maintainer owns semantic review. The installer owns only the marked guidance blocks and thin references. Project task files own current state. The checker owns mechanical evidence. The skill-creator validator owns skill package structure. The user performs final review before any push or release.

This repository's ordinary Actions path runs the submission gate before declared project checks. Protected-rule updates use a separate manual run for an exact reviewed SHA, after the repository owner configures a protected environment and required reviewers. The earlier setup and publication evidence is recorded in [the historical impact record](../planning/change-impact.md); that evidence does not verify this working tree or approve this task. Other projects can keep the entire review and verification flow local.
