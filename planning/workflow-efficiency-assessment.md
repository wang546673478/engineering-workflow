# Engineering Workflow Efficiency Assessment / 2026-10-28

Status: assessment complete. The user approved SPEC-WORKFLOW-EFFICIENCY-01 r1 and PLAN-WORKFLOW-EFFICIENCY-01 r1 on 2026-10-28; implementation and validation progress are tracked in [Task](workflow-efficiency-task.md).

## User request and boundary

The user asked which parts of the engineering workflow should be improved based on the current Liantong project summaries, then said: “按照这个改吧,需要写spec/plan/task吗?” After being told the complete proposal should be prepared for review before implementation, the user instructed: “按照这个改吧”. The user then reviewed the summaries and explicitly approved implementation with: “通过,开始实施”. That approval covers the current linked Spec/Plan for this repository only. It does not authorize changing the Liantong project, reducing its checks, or publishing this repository.

## Evidence reviewed

The Liantong project manifest currently selects `ORG-BALANCE-01`; its implementation status says `ORG-T15` is in progress and its Spec/Plan/Task revision is approved. The saved report `E:\liantongzhongzhuanzhan\planning\org-balance-validation-20261028.json` is a change-mode snapshot with 39 checks: 31 pass, 7 fail, 1 partial, and recorded command durations totaling 699.49 seconds. The slowest entries are `FRONTEND-TEST` (239.091s), `ROOT-GO-TEST` (216.037s), `POSTGRESQL-MIGRATION` (96.867s), `FRONTEND-LINT` (44.977s), and `ROOT-GO-VET` (30.953s). Failures include two source inventories, Go tests, frontend typecheck/lint/tests, and baseline evidence. This is evidence of substantial validation time and unresolved findings, not proof that process complexity alone caused the elapsed time or that every second is avoidable.

This repository already supports stable-ID and selected-slice reads through `workflow_state.py`, and its guidance already permits reusing unchanged evidence. Therefore the proposal emphasizes execution cadence and reporting rather than another index, state store, or batch tool. The existing real-session pilot also records a fast six-slice query, but has no matched legacy replay; total workflow savings remain unverified.

## Candidate improvements

1. Run a fast, relevant check after each small implementation slice; run the complete project-declared required checks before delivery. Keep failures visible and actionable throughout.
2. Run independent checks concurrently only when their data, ports, builds, and other resources are isolated. Preserve each command's exact status and the deterministic aggregate result.
3. Correct a confirmed factual baseline error as soon as evidence establishes it. Reuse unchanged slices during development and perform one complete affected-view convergence after implementation stabilizes.
4. Report progress against explicit acceptance items, separately for implementation, validation, and delivery. Give an approximate ETA only when comparable measured durations exist; otherwise say there is not enough evidence to estimate.
5. Measure the next naturally occurring comparable task with a small, de-identified pilot. Do not claim a savings percentage without a valid comparison and equivalent acceptance results.

## Guardrails

Keep all existing approval meanings, review points, required checks, commands, timeouts, coverage, security rules, and delivery gates. Do not add a mandatory progress ledger, checker mode, metric-reporting gate, or new user-review round. The proposed implementation is guidance and document changes only unless technical evidence later shows a necessary tool change; any expanded scope returns for review.
