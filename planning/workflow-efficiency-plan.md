# PLAN-WORKFLOW-EFFICIENCY-01 r1 (Approved)

Status: approved implementation path. User approval recorded in [Task](workflow-efficiency-task.md); this Plan remains the technical approach for the current batch.

## Basis

- Baseline: current repository at `4b2a5065037acb9c92e17d72f44a226663b3d145`; related views are the engineering workflow instructions, implementation guidance, baseline linkage, and existing efficiency pilot.
- Spec: `SPEC-WORKFLOW-EFFICIENCY-01 r1 (Approved)`.
- Evidence: [assessment](workflow-efficiency-assessment.md), including the Liantong change report and its measurement limits.

## Recommended approach

Make a guidance-only change first. Keep execution ownership with the existing Task and project rules. Do not create another CLI, data store, mandatory ledger, or checker policy. If a later pilot shows a repeated mechanical bottleneck that guidance cannot solve, register it as a separate scope change before adding tooling.

## Plan items

| ID | Requirements | Approved work | Verification |
| --- | --- | --- | --- |
| PL-WFE-01 | REQ-WFE-02, REQ-WFE-03, AT-WFE-01, AT-WFE-02 | Add a concise validation cadence and bounded parallelism section to `references/implementation-workflow.md`; link it from `SKILL.md`. | Review language against the existing required-check contract; verify command IDs, timeouts, and coverage are unchanged in the manifest. |
| PL-WFE-02 | REQ-WFE-04, AT-WFE-03 | Clarify evidence reuse, immediate factual correction, and the timing of final affected-view convergence in `references/baseline-linked-artifacts.md`. | Check consistency with current continuous-correction text; do not defer a known factual correction. |
| PL-WFE-03 | REQ-WFE-05, REQ-WFE-06, AT-WFE-04, AT-WFE-05 | Add concise progress and ETA reporting rules, including separate implementation/validation/delivery measures and unknown ETA when history is insufficient. | Use one task-shaped example; verify no mandatory new status field or ledger is introduced. |
| PL-WFE-04 | REQ-WFE-07, AT-WFE-06 | Keep the existing real-session pilot record explicit that no matched full-task comparison exists; after a naturally comparable task is measured, add the comparator and results. Do not add a recurring gate or collect private project/source data in this repository. | Current status is recorded as unverified. Later evidence must include comparator, matching acceptance, observed durations/calls/retries/results, and limitations. |
| PL-WFE-05 | REQ-WFE-08, AT-WFE-07 | Update README, CHANGELOG, version metadata, traceability, impact, and task state as applicable. | Run the existing `TEST`, `COMPILE`, and `GUIDANCE-COMPILE`; confirm protected-path and CI policies did not change. |

## Scope and release

Expected modules: `instructions` and `governance`. No checker, application API, database, CI workflow, or manifest check policy change is approved. Version impact: 1.11.0 to 1.12.0 / Unreleased for this backward-compatible instruction capability. No Git commit, push, merge, or release is included in this task.

## Risks and recovery

- Parallel execution can create port, build-cache, database, or file contention. Keep those checks serial unless isolation is demonstrated; separate failures by exact command and run.
- A completion percentage can look precise while criteria have different effort. State the criterion denominator and present completion separately from elapsed-time estimates.
- A focused test can pass while another required gate fails. Keep final required checks as the delivery condition.
- If implementation evidence requires checker/schema/CI changes or expands the affected modules, update this Plan and Task and request review of that changed scope before proceeding.
