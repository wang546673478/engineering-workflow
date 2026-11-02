# PLAN-DEFECT-GATE-GUIDANCE-01 r1

Status: local implementation completed under r1; r2 below extends only the delivery scope under the user's separate publication request.

## Basis

- Baseline: current `BASELINE` at repository HEAD `af4a8456acfa95eeb808d2e17510d4c52a91afa0`.
- Assessment: [Defect Repair and Task-Scoped Verification Assessment](defect-gate-guidance-assessment.md).
- Spec: [SPEC-DEFECT-GATE-GUIDANCE-01 r1](defect-gate-guidance-spec.md).
- Input skill: `engineering-workflow` 1.15.0.

## Plan

| ID | Work | Verification |
| --- | --- | --- |
| PL-DGF-01 | Strengthen defect evidence guidance so the proposed fix removes a confirmed cause by default; define a bounded mitigation path. | Review the distinction between a cause-directed correction, a valid invariant guard, and symptom-only containment. |
| PL-DGF-02 | Clarify Task-specific required-check selection and independent follow-up/receipt tasks. Preserve exact-tree commit/committed semantics and explicit project-wide required checks. | Scenario-review a broad feature, a narrow follow-up, a failed required check, and a receipt-only tree. |
| PL-DGF-03 | Update the short SKILL entrypoint, README, and synchronized 1.16.0 metadata/changelog. | Compare all version surfaces and confirm unchanged workflow and gate definitions. |
| PL-DGF-04 | Add focused guidance-contract assertions and synchronize Assessment/Spec/Plan/Task, Baseline, impact, skill review, manifest, and traceability. | Parse JSON, resolve linked documents, and review the complete diff. |
| PL-DGF-05 | Run TEST, COMPILE and GUIDANCE-COMPILE unchanged, plus the skill validator and `git diff --check`. | Preserve each original command, timeout, and result. No commit/push/publication is included. |

## Guardrails

No new workflow stage, approval round, required command, check definition, timeout, coverage reduction, checker/CI behavior, external migration, or publication. A narrower Task check set is chosen before execution and must retain explicit project-wide requirements; it cannot be used to erase a failed result.

## Publication extension / PLAN-DEFECT-GATE-GUIDANCE-01 r2

On 2026-11-03, the user separately requested “上传到github吧”. This extends r1's local-only delivery boundary to publish the completed 1.16.0 candidate to `origin/main`; the target follows this repository's preceding main-publication decision and the current worktree's `origin/main` base. Use a normal fast-forward only. Do not force-push, create a tag or Release, deploy, or change an external project.

Before push, prepare the exact candidate and run the existing `commit` gate on the staged tree and `committed` gate on the resulting commit with the unchanged TEST, COMPILE and GUIDANCE-COMPILE checks. Because `SKILL.md`, `VERSION`, `CHANGELOG.md` and the manifest are protected, a human must inspect this exact diff before the one-run `--allow-control-plane-change` approval signal is supplied. Verify the pushed remote SHA; hosted checks remain separately reported. This extension does not change the source implementation, Spec, required-check definitions or their commands/timeouts.

The r1 no-publication boundary remains historical evidence for the original implementation authorization and is superseded only for this explicitly requested delivery action.
