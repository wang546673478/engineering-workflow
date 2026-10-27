# PLAN-VERIFICATION-CLOSURE-01 r1

Status: implementation authorized by the user's request recorded in [Task](verification-closure-task.md). The approved scope is guidance and linked governance metadata only.

## Basis

- Baseline: repository branch `codex/workflow-efficiency-1.12.0` at `72c75f9b37b7669619d7dceca821de5ba90c3024`.
- Assessment: [Verification Closure Assessment](verification-closure-assessment.md).
- Spec: [SPEC-VERIFICATION-CLOSURE-01 r1](verification-closure-spec.md).

## Plan

| ID | Work | Verification |
| --- | --- | --- |
| PL-VFC-01 | Add final-tree freeze and exact commit/tree binding guidance to `references/implementation-workflow.md`, linked from `SKILL.md`. | Confirm the text preserves the rule to rerun required checks for a changed tracked tree. |
| PL-VFC-02 | Summarize the result and receipt policy in README. | Verify the README agrees with the reference and describes the tracked-receipt fallback. |
| PL-VFC-03 | Add the new task, requirements, acceptance IDs, impact, skill review, traceability, and corrected Baseline finding to manifest-linked records. | Parse the manifest, resolve links, and run the repository's workflow-state index. |
| PL-VFC-04 | Bump the additive guidance version to 1.13.0 and add an Unreleased changelog entry. | Compare `VERSION`, `SKILL.md`, README, `agents/openai.yaml`, and CHANGELOG; verify existing check declarations byte-for-byte. |
| PL-VFC-05 | Run the declared required checks and publish the verified branch for trial. | Run TEST, COMPILE, and GUIDANCE-COMPILE with their existing commands/timeouts; run skill validation and `git diff --check`; push `codex/workflow-verification-closure-1.13.0` without merge or Release. |

## Boundaries

No checker, CI, approval, gate, test-coverage, or timeout change. No Liantong project modification. Validation output and the pushed SHA are reported from the final exact tree; avoid a later tracked receipt commit unless repository policy requires one.
