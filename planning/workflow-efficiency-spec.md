# SPEC-WORKFLOW-EFFICIENCY-01 r1 (Approved)

Status: approved for this implementation batch. The user approved this Spec and linked Plan on 2026-10-28 with “通过,开始实施”. Scope remains limited to the engineering-workflow repository.

## Goal

Reduce avoidable waiting, repeated investigation, and unclear progress reporting when an agent carries out an engineering task, while preserving correctness, project policy, user approval, and final verification.

## Scope

In scope: guidance for validation cadence and safe parallel execution; incremental baseline evidence reuse and final convergence; progress/ETA reporting; a bounded, de-identified efficiency measurement for one comparable task.

Out of scope: changes to the Liantong repository or active task; weakening, skipping, or redefining project required checks; changing approval or review requirements; modifying checker policy or CI; adding a new state database, mandatory reporting tool, or workflow stage; claiming a general efficiency percentage from unmatched historical data.

## Requirements

- **REQ-WFE-01 (confirmed goal):** Improve the engineering workflow's time efficiency based on the observed task summaries without compromising correct behavior or evidence.
- **REQ-WFE-02 (approved):** During implementation, use narrow relevant checks for rapid feedback; before delivery, run every existing required check with its declared command, scope, and timeout. Failures and partial results remain visible and cannot be reported as passed.
- **REQ-WFE-03 (approved):** Independent checks may run concurrently only when their dependencies and mutable resources are isolated. Preserve each check's result and deterministic overall reporting; serialize conflicting checks.
- **REQ-WFE-04 (approved):** Reuse unchanged baseline slices when the source/worktree and evidence have not changed. Record and correct a confirmed factual error immediately; complete the affected-view reconciliation once implementation stabilizes.
- **REQ-WFE-05 (approved):** Report an approximate progress percentage from the task's explicit acceptance items, separately for implementation, validation, and delivery. State the denominator and label the measure as approximate when criteria differ in size.
- **REQ-WFE-06 (approved):** Estimate remaining time from measured durations of comparable completed steps/tasks, state confidence or range, and separate execution time from external/user wait. If there is no comparable evidence, report ETA as unknown rather than inventing one.
- **REQ-WFE-07 (approved):** Evaluate efficiency with a small de-identified pilot and equivalent acceptance criteria. Record observed task/tool duration, repeated reads/writes, retries, validation outcomes, and sample limits. Do not claim savings when the comparison is unmatched or too small.
- **REQ-WFE-08 (guardrail):** Preserve all existing approval points, required checks, commands, timeouts, test coverage, protected-path review, and delivery rules. Do not add a workflow stage or a mandatory metric gate.

## Acceptance criteria

- **AT-WFE-01:** Guidance distinguishes fast implementation feedback from the complete final required-check set and explicitly states that a focused pass does not satisfy final verification.
- **AT-WFE-02:** Guidance limits parallel execution to independent, resource-isolated checks; conflicting checks remain serialized and every result is retained.
- **AT-WFE-03:** Guidance permits same-task reuse of unchanged evidence, requires immediate correction of confirmed facts, and schedules final affected-view convergence after implementation stabilizes.
- **AT-WFE-04:** A progress report can show separate implementation, validation, and delivery percentages with explicit denominators and no unsupported implication that elapsed time equals completion.
- **AT-WFE-05:** ETA guidance requires comparable measured evidence and permits an explicit unknown result.
- **AT-WFE-06:** The pilot reports its comparator, acceptance equivalence, measures, results, and limitations; any unmatched measure is labeled directional or unverified.
- **AT-WFE-07:** Regression review confirms the existing approval, required-check, command, timeout, test-coverage, and protected-review policy is unchanged.

## Deferred questions

- Whether an automated progress or ETA helper is useful: defer until the guidance-only change is measured on a comparable task.
- Whether parallel test execution improves wall-clock time: defer any default parallel runner until resource conflicts and repeatability are measured.
- Whether to publish a numerical efficiency target: defer until there is at least one valid comparable sample; do not set a percentage target from the current unmatched reports.
