# Engineering Workflow Maintenance Flow

Status: `current`

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

## Ownership

The repository maintainer owns semantic review. The checker owns mechanical evidence. The skill-creator validator owns skill package structure. The user performs final review before any push or release.

This repository's ordinary Actions path runs the submission gate before declared project checks. Protected-rule updates use a separate manual run for an exact reviewed SHA, after the repository owner configures a protected environment and required reviewers. That hosted configuration has not been applied during this local task. Other projects can keep the entire review and verification flow local.
