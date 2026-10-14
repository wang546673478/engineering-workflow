# Engineering Workflow Maintenance Flow

Status: `current`

## Skill change path

1. Maintainer identifies a workflow, checker, adapter, documentation, or release change.
2. Applicable skills are reviewed and recorded in the active task `skill_review`.
3. The module map and impact record identify affected modules, contracts, database boundaries, and tests.
4. Code and the corresponding documentation are staged together.
5. The `commit` gate checks the index; CI uses `committed` against the generated commit tree.
6. Tests, compilation, and independent skill validation run before manual review.

## Failure and recovery

| Trigger | Expected behavior | Recovery |
| --- | --- | --- |
| Missing manifest or baseline evidence | Baseline fails | Restore the missing control document and rerun baseline |
| Code change without declared documentation impact | Commit gate fails | Add the canonical gate and update the affected documents |
| Required test fails or is skipped | Handoff remains incomplete | Fix the failure or document a user-approved scope change |
| Remote adapter lacks driver/credentials | Adapter reports unsupported | Install the optional driver or use an offline snapshot |

## Ownership

The repository maintainer owns semantic review. The checker owns mechanical evidence. The skill-creator validator owns skill package structure. The user performs final review before any push or release.
