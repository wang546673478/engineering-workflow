# Current Source Context Traceability

Revision TRACE-CONTEXT-03: BASELINE-CONTEXT-03 → SPEC-CONTEXT-03 → PLAN-CONTEXT-03 → TASK-CONTEXT-RELEASE-01.

| Requirement / acceptance | Plan / execution | Evidence and affected views |
| --- | --- | --- |
| REQ-CONTEXT-01 / AT-CONTEXT-01 | [Plan](../docs/plan.md), CR-01 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-02 / AT-CONTEXT-02 | [Plan](../docs/plan.md), CR-02 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-03 / AT-CONTEXT-03 | [Plan](../docs/plan.md), CR-03 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-04 / AT-CONTEXT-04 | [Plan](../docs/plan.md), CR-04 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |
| REQ-CONTEXT-05 / AT-CONTEXT-05 | [Plan](../docs/plan.md), CR-05 | [Task](source-context-task.md), [evidence](source-context-evidence.json), map/contract/flow/baseline |

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
