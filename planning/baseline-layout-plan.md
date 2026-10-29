# PLAN-BASELINE-LAYOUT-01 r1

Status: implementation and required verification completed for the guidance/template slice. The local pinned TypeScript runtime was prepared and the unchanged required checks pass.

## Basis

- Assessment: [Baseline Layout Assessment](baseline-layout-assessment.md)
- Spec: [SPEC-BASELINE-LAYOUT-01 r1](baseline-layout-spec.md)
- Current skill: engineering-workflow 1.13.0
- User direction: separate current and historical baseline content; preserve the existing workflow.

## Plan

| ID | Work | Verification |
| --- | --- | --- |
| PL-BL-01 | Add current/history role guidance and evidence/target boundaries to the skill references, with a short entry-point summary. | Guidance review confirms no stage, approval, gate, command, timeout, coverage, or CI policy change. |
| PL-BL-02 | Extend manifest/document conventions additively so `active_baseline` and existing current IDs retain their meaning while optional history siblings can be declared. | Legacy manifests pass unchanged; new role/history declarations are parsed and linked. |
| PL-BL-03 | Add skill guidance and templates so new-project baseline initialization creates paired current/history view files with an explicit empty-history marker, without changing `adopt_project.py`. | Guidance review confirms deterministic initialization instructions and preserves existing adoption behavior. |
| PL-BL-04 | Add a one-time agent-guided upgrade procedure for existing projects: classify sections, move target/evidence content to its authority, create history siblings, and record evidence in the existing Task. | Review the resulting current/history documents and Task; no recurring tool diagnostic or implicit content write is introduced. |
| PL-BL-05 | Add guidance examples and governance traceability for the migration procedure; retain existing executable checks without adding checker behavior. | Existing TEST, COMPILE and GUIDANCE-COMPILE declarations remain unchanged if the project later implements the guidance update. |
| PL-BL-06 | Synchronize README, version/changelog, manifest and governance records after implementation review. | Version and changelog describe the additive compatibility change; traceability and impact records resolve. |

## Guardrails

No external project migration, no product/API/database changes, no new required approval round, no change to stage order, required commands, timeouts, coverage, checker/CI policy, or delivery gates. If a checker change is needed, it remains additive and preserves old-manifest behavior.

## Implementation authorization

Implementation was authorized by the user's direct decision on 2026-10-30. The active task is `TASK-BASELINE-LAYOUT-01`; the prior verification-closure task remains preserved with its original scope and records.
