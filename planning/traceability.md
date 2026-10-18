# Current Source Context Traceability

Revision TRACE-CONTEXT-05: BASELINE-CONTEXT-06 → SPEC-CONTEXT-03 → PLAN-CONTEXT-06 → TASK-CONTEXT-RELEASE-01.

| Requirement / acceptance | Plan / execution | Evidence and affected views |
| --- | --- | --- |
| REQ-CONTEXT-01 / AT-CONTEXT-01 | [Plan](../docs/plan.md), CR-01 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-02 / AT-CONTEXT-02 | [Plan](../docs/plan.md), CR-02 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-03 / AT-CONTEXT-03 | [Plan](../docs/plan.md), CR-03 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-04 / AT-CONTEXT-04 | [Plan](../docs/plan.md), CR-04 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-05 / AT-CONTEXT-05 | [Plan](../docs/plan.md), CR-05 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |

### Hosted CI correction (1.6.2)

The 1.6.1 exact-SHA hosted run exposed a mismatch between the original checker artifact and the successful diagnostic rerun. BASELINE-CONTEXT-06 and PLAN-CONTEXT-06 keep SPEC-CONTEXT-03 and REQ-CONTEXT-01..05 unchanged while restoring the required-check contract: both protected finalizers now require the original checker to succeed. Source commit `82b3c8531a9a9867dd77756444a2bcbc922aa2c8` and receipt commits passed local gates; `3fab75ba5d8e2663af811d2b7daee53c90fe6818` was pushed to `main` and passed exact-SHA reviewed checks on Ubuntu/Windows plus aggregate quality in run `39115700117`. Per-platform artifacts and approval evidence are in the [current Task](source-context-task.md) and [machine evidence](source-context-evidence.json).

## Historical linked-model trace (original scope)

# Current Linked Artifact Traceability

Revision: `TRACE-LINKED-02`, 2026-10-18. Active Spec `SPEC-LINKED-02`, Plan `PLAN-LINKED-02`, output Baseline `BASELINE-LINKED-02` and Task `TASK-LINKED-ARTIFACTS-01`. The input baseline is the published source plus pre-existing worktree, as recorded in Plan. The checker validates declared IDs/files; the table's semantic/revision alignment is agent-reviewed.

| Requirement / acceptance | Spec | Plan item | Executable steps / evidence | Baseline views |
| --- | --- | --- | --- | --- |
| REQ-LINKED-01 / AT-LINKED-03 | [ownership and boundaries](../docs/spec.md) | [PL-01](../docs/plan.md) | [TW-01/02/04/05](linked-artifact-model-task.md) | [map](../docs/module-map.md), [flow](../docs/business-flow.md) |
| REQ-LINKED-02 / AT-LINKED-01 / AT-LINKED-02 | [linked fields and compatibility](../docs/spec.md) | [PL-02](../docs/plan.md) | [TW-03/05](linked-artifact-model-task.md) | [contracts](../docs/contracts.md) |
| REQ-LINKED-03 / AT-LINKED-03 | [correction and history](../docs/spec.md) | [PL-03](../docs/plan.md) | [TW-04/05](linked-artifact-model-task.md) | [baseline](baseline-review.md), [flow](../docs/business-flow.md) |
| REQ-LINKED-04 / AT-LINKED-04 | [greenfield lifecycle](../docs/spec.md) | [PL-04](../docs/plan.md) | [TW-02/03/05](linked-artifact-model-task.md) | [contracts](../docs/contracts.md), [map](../docs/module-map.md), [flow](../docs/business-flow.md) |
| REQ-LINKED-05 / AT-LINKED-05 | [document reconciliation](../docs/spec.md) | [PL-05](../docs/plan.md) | [TW-04/05 reconciliation table and current validation](linked-artifact-model-task.md) | [baseline](baseline-review.md), all current views |

Historical task/requirement registrations remain in the manifest and their original files. This current index does not transfer past approvals or rewrite release receipts.

Publication evidence: 1.5.0 source `46d57a6cefd5cc80ae62e47099b782d4cb381504`, uploaded 2026-10-18; staged and exact-commit check reports plus the source-upload receipt are recorded in the current Task. The requirement/Plan/step mappings remain unchanged.


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


## Issue #17/#18 fix batch (2026-10-19)

SPEC-UX-17-18-01 -> PLAN-UX-17-18-01 -> TASK-ISSUES-17-18 -> BASELINE-UX-17-18-01; implementation/validation and publication status: [Task](issues-17-18-task.md).

| Requirement | Acceptance | Plan | Evidence |
| --- | --- | --- | --- |
| REQ-UX-17 | AT-UX-17 | UX-01 | initializer/checker dependency-pruning fixtures; fix evidence |
| REQ-UX-18 | AT-UX-18 | UX-02 | CLI/status/summary and missing/mixed/empty-reference regressions |
| REQ-UX-VERIFY | AT-UX-VERIFY | UX-03..05 | required environment setup, original full checks, exact commit/upload and issue receipts |


REQ-UX-17/AT-UX-17, REQ-UX-18/AT-UX-18 and REQ-UX-VERIFY/AT-UX-VERIFY map to published source 0040878, fresh 170-test local gates and verified issue replies/closure. Receipt-only follow-up retains these boundaries; hosted outcome remains pending.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.


## Issue #19/#20/#21 repair batch

SPEC-SAFE-19-21-01 -> PLAN-SAFE-19-21-01 -> TASK-ISSUES-19-21 -> BASELINE-SAFE-19-21-01. Source, checks and publication: [Task](issues-19-21-task.md).

| Requirement | Acceptance | Plan | Evidence |
| --- | --- | --- | --- |
| REQ-SAFE-19 | AT-SAFE-19 | SAFE-01 | real Git drift and hook/commit-tree regressions |
| REQ-SAFE-20 | AT-SAFE-20 | SAFE-02 | structured input/history failures, no execution, large-shallow compatibility |
| REQ-SAFE-21 | AT-SAFE-21 | SAFE-03 | ordinary descendant cleanup, cancellation, native platform lifecycle and setup failure |
| REQ-SAFE-DELIVERY | AT-SAFE-DELIVERY | SAFE-04..05 | original full gates, source upload, hosted artifacts and issue receipts |
