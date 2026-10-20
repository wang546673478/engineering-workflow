# Issue 22 enhancement Spec traceability (current)

当前实现：BASELINE-ISSUE22-02 ← 原Spec r1 / Plan r2的三项增强已完成，E01..E10按所列S22场景与原门槛核对通过。SOURCE全量审读依最新用户指令延后，与本批交付范围分开；不冒称已审。

历史状态（阶段性报告时，2026-10-20）：用户明确当前文件读完即先报告。全量SOURCE审读暂缓且未完成；已有证据支持三项兼容增强建议，但E01..E10均尚未实施或验收。本次阶段性结论见[assessment](issue-22-assessment.md)，不冒充原完整调查完成。

2026-10-20; `BASELINE-ISSUE22-01` → [SPEC-ISSUE22-ENHANCEMENT-01](issue-22-spec.md)（r1正文保持）→ [PLAN-ISSUE22-ENHANCEMENT-01](issue-22-plan.md)（r1，按用户请求编写）→ [TASK-ISSUE-22-REVIEW / T22-01..16](issue-22-task.md#可执行任务与进度)。用户最新明确“那就按照这个增强的文档去实施”，按Plan r2完成三项本地增强及原验证；完整外部审读延后。

| Requirement | Acceptance | Plan / Task | Current evidence / status |
| --- | --- | --- | --- |
| REQ-ISSUE22-E01 | AT-ISSUE22-E01 | P22-01,03..07 / T22-01,08..13 | 原阶段、审批、例外、授权、验证合同保持；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E02 | AT-ISSUE22-E02 | P22-03,06 / T22-08,11,13 | 原记录中的按需缺陷证据；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E03 | AT-ISSUE22-E03 | P22-03,07 / T22-08,13 | 修复结论对应真实证据及限制；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E04 | AT-ISSUE22-E04 | P22-03,07 / T22-08,13 | 按影响验证，复用测试与小修边界；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E05 | AT-ISSUE22-E05 | P22-04,06 / T22-09,11..13 | 本批双向核对，未来/延后范围保持；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E06 | AT-ISSUE22-E06 | P22-04,07 / T22-09,13 | 差异回流 Baseline/Plan/Task/Spec 的原归属；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E07 | AT-ISSUE22-E07 | P22-05,06 / T22-10,11,13 | 可选 EARS 与中文/旧格式兼容；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E08 | AT-ISSUE22-E08 | P22-05,06 / T22-10,11,13 | 可选验收句式、保留原 ID/追踪；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E09 | AT-ISSUE22-E09 | P22-01..02,06..08 / T22-01..07,11..16 | 全局接入、旧工件及工具合同兼容；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |
| REQ-ISSUE22-E10 | AT-ISSUE22-E10 | P22-01..02,06..08 / T22-01..07,11..16 | 实际受影响资料与验证一致；已实施；对应S22手工场景核对与原正式检查通过，范围/局限见Task |

外部来源独立任务：REQ/AT-ISSUE22-SOURCE → P22-02 / T22-02..06；REQ/AT-ISSUE22-DECISION → P22-02,08 / T22-07,16。全部调查不因Plan编写改为完成。场景S22-01..10与B22-01..10依据见Plan，不额外新建需求或验收体系。

## Prior assessment traceability (investigation incomplete)

# Issue 22 assessment traceability

2026-10-20; `BASELINE-ISSUE22-01` → `SPEC-ISSUE22-REVIEW-01` → `PLAN-ISSUE22-REVIEW-01` → [TASK-ISSUE-22-REVIEW](issue-22-task.md) → [assessment](issue-22-assessment.md). Source `868e496` / 1.7.1. Prior implementation rows below retain their original scope.

| Requirement | Acceptance | Plan action | Current evidence / status |
| --- | --- | --- | --- |
| REQ-ISSUE22-REVIEW | AT-ISSUE22-REVIEW | 1, 3 | Open Issue retrieved; local source/critical upstream claims checked; absence claims corrected |
| REQ-ISSUE22-PARITY | AT-ISSUE22-PARITY | 3, 4 | Candidate preserves original nodes/exceptions; no new gate or skill change implemented |
| REQ-ISSUE22-SOURCE | AT-ISSUE22-SOURCE | 2 | All 3,601 tracked files inventoried; 3,543 complete text files collected; full per-file semantic review incomplete |
| REQ-ISSUE22-DECISION | AT-ISSUE22-DECISION | 4, 5 | Source-bound provisional assessment exists; final adoption decision depends on remaining semantic review |

## Prior task traceability

# Adoption Lifecycle Traceability

Revision `TRACE-ADOPTION-LIFECYCLE-02`: `BASELINE-ADOPTION-LIFECYCLE-02` → `SPEC-ADOPTION-LIFECYCLE-02` → `PLAN-ADOPTION-LIFECYCLE-02` → `TASK-ADOPTION-LIFECYCLE-01`.

| Requirement / acceptance | Plan / execution | Evidence and affected views |
| --- | --- | --- |
| REQ-ADOPTION-01 / AT-ADOPTION-01 | ADOPT-01 | adoption CLI, guidance tests, contracts and Task |
| REQ-ADOPTION-02 / AT-ADOPTION-02 | ADOPT-02 | initializer/manifest fixtures, Baseline, contracts and Task |
| REQ-ADOPTION-03 / AT-ADOPTION-03 | ADOPT-03 | checker stage fixtures, module/flow/contract views and Task |
| REQ-ADOPTION-04 / AT-ADOPTION-04 | ADOPT-04 | SKILL/README/references, Baseline and Task limits |
| REQ-ADOPTION-05 / AT-ADOPTION-05 | ADOPT-05 | [verification](adoption-lifecycle-verification.json): 205 tests/109.390s, compile/package checks; 1.7.0 Unreleased |

REQ-ADOPTION-PARITY / AT-ADOPTION-PARITY → original-flow scenarios in checker/guidance tests and current verification; same core SKILL sections plus preserved local installation rehearsal.

## Prior traceability

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


Published implementation5f9b3e1d54a0709241fb5f11173e13ce00af3ffd passed local184-test staged/exact-commit gates and original Windows/Ubuntu reports in approved run39157028881; source upload and #19/#20/#21 replies/completed closure were verified on 2026-10-19. Receipt-only updates do not change implementation, targets, limits or prior approval scope.

Publication receipt (2026-10-19): implementation c15b94397314b8e84b3ee94877267f8245c3351c passed original local staged/exact-commit gates with 205 tests and the unchanged 120-second limit, was uploaded to main, and was installed as 1.7.0 with prior local work preserved. GitHub run39277812120 has a verified human environment approval but original platform reports are still pending; no hosted pass is claimed. This receipt changes evidence/status only, not source behavior or acceptance.

1.7.1 correction: normalize initializer library roots through the same existing project_root function as the CLI; hosted Windows exposed short-name aliases. Scope checks and the original workflow remain unchanged; 1.7.0 Ubuntu success/Windows failure are historical, and fresh local/exact/hosted checks are required.
