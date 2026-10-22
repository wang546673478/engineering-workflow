# Issue 22 enhancement Spec traceability (current)

Source upload receipt (2026-10-20T17:52:35.783179+08:00): REQ/AT-ISSUE22-E01..E10 local implementation 5b8013c9b67debff0b080da563781a39f6e69f74 is uploaded and exact-tree local checks pass. Full SOURCE audit remains incomplete/deferred; receipt-only updates do not extend semantic or hosted-validation scope.

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


## Issue 23 candidate proposal / 2026-10-21

Basis BASELINE-ISSUE23-01 / d214021 -> SPEC-ISSUE23-01 -> PLAN-ISSUE23-01 r1 -> TASK-ISSUE-23-PROPOSAL. Implementation authorized by “那就开始实施吧”; current output Baseline BASELINE-ISSUE23-02. T23-03..08 source implementation and validation recorded in current Task.

| Requirement / acceptance | Plan | Task | Facts / future evidence |
| --- | --- | --- | --- |
| REQ-ISSUE23-01 / AT-ISSUE23-01 | P23-01 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-02 / AT-ISSUE23-02 | P23-01 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-03 / AT-ISSUE23-03 | P23-02 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-04 / AT-ISSUE23-04 | P23-02/03 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-05 / AT-ISSUE23-05 | P23-03 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-06 / AT-ISSUE23-06 | P23-05 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-07 / AT-ISSUE23-07 | P23-04 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |
| REQ-ISSUE23-08 / AT-ISSUE23-08 | P23-06/07 | T23-01/02 complete; T23-03..08 complete locally | B23-01..07, planning/issue-23-evidence.json; current behavior/evidence in Task; original gate outcome authoritative |

Issue 23 closure: all eight REQ/AT implemented; formal-final report original commands pass on task-local CPython3.11.15. Scenario and source-hash evidence: planning/issue-23-evidence.json. Optional legacy/manual coverage partial and source/host limits remain explicit.

Issue23 source-upload closure: implementation 9723921ceac69db363fb4b655d761bc61b956e0f / tree 4165482e1a8b8cf781e1de56a545128540dcbdf2 passed original staged/committed gates and is verified on origin/main. Publication-only receipts retain the 1.8.0 version and do not change requirements or runtime evidence.


## Issue #24 efficiency assessment (research task; not the implementation approval)
REQ-ISSUE24-E01 AT-ISSUE24-E01 REQ-ISSUE24-E02 AT-ISSUE24-E02 REQ-ISSUE24-E03 AT-ISSUE24-E03 REQ-ISSUE24-E04 AT-ISSUE24-E04 REQ-ISSUE24-E05 AT-ISSUE24-E05 REQ-ISSUE24-E06 AT-ISSUE24-E06 REQ-ISSUE24-E07 AT-ISSUE24-E07 REQ-ISSUE24-E08 AT-ISSUE24-E08 REQ-ISSUE24-E09 AT-ISSUE24-E09 REQ-ISSUE24-E10 AT-ISSUE24-E10

`BASELINE-ISSUE23-02` → [ISSUE24 assessment](issue-24-efficiency-assessment.md) / [TASK-ISSUE24-EFFICIENCY-ASSESS-01](issue-24-efficiency-assessment.md). It is a separate research follow-up to the shipped 1.9.0 local archive. Its no-implementation-authorization statement describes that historical assessment scope only; implementation approval is recorded in the active task below.

## Issue #24 efficiency Spec/Plan/Task (approved implementation scope)

`BASELINE-ISSUE23-02` → [SPEC-ISSUE24-EFFICIENCY-01 r1 plus user-approved execution-policy amendment](issue-24-efficiency-spec.md) → [PLAN-ISSUE24-EFFICIENCY-01 r1 updated for TEST 240s](issue-24-efficiency-plan.md) → [TASK-ISSUE24-EFFICIENCY-01](issue-24-efficiency-task.md). User approved the complete proposal and implementation on 2026-10-22, then explicitly changed only this repository TEST timeout from 120s to 240s; exact words, times, boundaries, current progress and verification are in Task. The optional CLI preserves existing workflow stages, approval semantics, required checks and test coverage.

| Requirement/acceptance | Plan phase | Evidence/status |
| --- | --- | --- |
| REQ-ISSUE24-E01..04 / AT-ISSUE24-E01..04 | WFS-01 | index JSON/Markdown; completed/obsolete/deferred and unknown records retained; focused tests in `scripts/tests/test_workflow_state.py`; formal baseline checks pass. |
| REQ-ISSUE24-E05 / AT-ISSUE24-E05 | WFS-02 | exact snapshot IDs/sections with SHA-256 and active/open-state summary; focused tests and formal baseline checks pass. |
| REQ-ISSUE24-E06..07 / AT-ISSUE24-E06..07 | WFS-03 | guarded dry-run/apply, duplicate-key rejection, conflicts/CAS, idempotency, gate protections, archive revision and rollback; 29 focused tests pass; formal checks pass with user-approved TEST 240s timeout. |
| REQ-ISSUE24-E08 / AT-ISSUE24-E08 | WFS-04 | invalid process root returns unsupported once; host pre-start cwd failure remains unsupported. |
| REQ-ISSUE24-E01/E09/E10 / AT-ISSUE24-E01/E09/E10 | WFS-05..07 | 1.8 semantics retained; real efficiency pilot remains unverified; formal checks pass under the approved timeout; commit/upload pending. See active Task and report. |

Windows reviewed path-alias correction (2026-10-23): Actions run `39787233509` showed a Windows-only false path-escape rejection when TemporaryDirectory paths alternated between long and 8.3 forms. The fix stays within the existing Issue24 task and adds no gate or approval. Windows alias regressions and full 262-test/260-checker-test evidence are in [the current Task](issue-24-efficiency-task.md); local commit and upload remain pending.

## Issue 23 record integrity local recovery implementation / 2026-10-22

`BASELINE-ISSUE23-02` → [SPEC-ISSUE23-RI-01](issue-23-record-integrity-spec.md) → [PLAN-ISSUE23-RI-01](issue-23-record-integrity-plan.md) → [TASK-ISSUE23-RECORD-INTEGRITY-01](issue-23-record-integrity-task.md). User authorized local archive/recovery while preserving the existing 1.8 review and required-check flow.

| Requirement / acceptance | Plan scope | Current evidence and status |
| --- | --- | --- |
| REQ/AT-ISSUE23-RI-01, 02, 03, 04, 05, 07, 08, 09, 10, 11, 12 | P-RI-02, 04, 05 | Local archive CLI records manifest documents, detects whole-file drift, uses expected-head SQLite checkpoints, lists history, restores as a new revision and recovers a partial projection from head. Six focused integration scenarios pass. |
| REQ/AT-ISSUE23-RI-06 | P-RI-03 | Hard blocking of arbitrary shell/editor writes is unsupported by current host; optional archive detects and can recover changes but cannot prevent bypass. |
| REQ/AT-ISSUE23-RI-13 / AT-ISSUE23-RI-11..12 | P-RI-06 | Legacy external project migration remains explicit/not performed; project state IDs and store paths are selected by adopters. |

Archive implementation references: REQ-ISSUE23-RI-01, REQ-ISSUE23-RI-02, REQ-ISSUE23-RI-03, REQ-ISSUE23-RI-04, REQ-ISSUE23-RI-05, REQ-ISSUE23-RI-06, REQ-ISSUE23-RI-07, REQ-ISSUE23-RI-08, REQ-ISSUE23-RI-09, REQ-ISSUE23-RI-10, REQ-ISSUE23-RI-11, REQ-ISSUE23-RI-12, REQ-ISSUE23-RI-13; AT-ISSUE23-RI-01, AT-ISSUE23-RI-02, AT-ISSUE23-RI-03, AT-ISSUE23-RI-04, AT-ISSUE23-RI-05, AT-ISSUE23-RI-06, AT-ISSUE23-RI-07, AT-ISSUE23-RI-08, AT-ISSUE23-RI-09, AT-ISSUE23-RI-10, AT-ISSUE23-RI-11, AT-ISSUE23-RI-12.
Acceptance ID: AT-ISSUE23-RI-12.
- Requirement ID: REQ-ISSUE23-RI-01
- Requirement ID: REQ-ISSUE23-RI-02
- Requirement ID: REQ-ISSUE23-RI-03
- Requirement ID: REQ-ISSUE23-RI-04
- Requirement ID: REQ-ISSUE23-RI-05
- Requirement ID: REQ-ISSUE23-RI-06
- Requirement ID: REQ-ISSUE23-RI-07
- Requirement ID: REQ-ISSUE23-RI-08
- Requirement ID: REQ-ISSUE23-RI-09
- Requirement ID: REQ-ISSUE23-RI-10
- Requirement ID: REQ-ISSUE23-RI-11
- Acceptance ID: AT-ISSUE23-RI-01
- Acceptance ID: AT-ISSUE23-RI-02
- Acceptance ID: AT-ISSUE23-RI-03
- Acceptance ID: AT-ISSUE23-RI-04
- Acceptance ID: AT-ISSUE23-RI-05
- Acceptance ID: AT-ISSUE23-RI-06
- Acceptance ID: AT-ISSUE23-RI-07
- Acceptance ID: AT-ISSUE23-RI-08
- Acceptance ID: AT-ISSUE23-RI-09
- Acceptance ID: AT-ISSUE23-RI-10

| AT-ISSUE23-RI-12 | P-RI-02/04/05 | Transaction rollback and archive head remains on prior revision after injected write failure. |

The completed `SPEC-ISSUE23-01` / `PLAN-ISSUE23-01 r1`, T23-01..08 and 1.8 approval-flow contract remain unchanged.


## Preserved local 1.7.2 fragments (historical)

These pre-upgrade local fragments retain their original scope and review history. Current authority is the 1.8.0 section selected by the manifest; original bytes and patches are preserved in the installation backup.


### Local fragment 1

# Issue 22 enhancement Spec traceability (current)

Hosted/install receipt (2026-10-20T18:44:37.427693+08:00): the four exact source-bound Ubuntu/Windows reports pass and the shared1.7.2 entry is updated. Source/receipt commits remain5b8013c/d214021; full upstream SOURCE review remains incomplete/deferred. Backup and preservation evidence is in the active Task.

Source upload receipt (2026-10-20T17:52:35.783179+08:00): REQ/AT-ISSUE22-E01..E10 local implementation 5b8013c9b67debff0b080da563781a39f6e69f74 is uploaded and exact-tree local checks pass. Full SOURCE audit remains incomplete/deferred; receipt-only updates do not extend semantic or hosted-validation scope.

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


## Historical local assessment index preserved during upgrade

Previous current labels in the following snapshot are historical; the active index is above.

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


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


## Local pre-upgrade research index (historical labels retained)

The following locally saved research index is retained as history. Its old current-task labels do not replace the manifest-selected 1.6.0 task.

# Current Linked Artifact Traceability



Current work: [TASK-GITDIAGRAM-ASSESS-01](gitdiagram-assessment-task.md), 2026-10-18. REQ/AT-GITDIAGRAM-ASSESS-01 map to GD-01..05 and the fixed-source/validation evidence in that combined research Spec/Plan/Task. The prior low-token display guidance is recorded in the isolated Gitingest pilot Task; formal feature integration remains unapproved.



Previous research (2026-10-18): [TASK-GITINGEST-ASSESS-01](gitingest-assessment-task.md), a research-only annex with its own combined Spec/Plan/Task. REQ-GITINGEST-ASSESS-01 / AT-GITINGEST-ASSESS-01 map to GP-01..05 and the version-bound source/test evidence there; integration remains unapproved. The published product model and its mappings below retain their original revision and approval scope.



Published-model revision: `TRACE-LINKED-02`, 2026-10-18. Product Spec `SPEC-LINKED-02`, Plan `PLAN-LINKED-02`, output Baseline `BASELINE-LINKED-02` and its completed implementation Task `TASK-LINKED-ARTIFACTS-01`. The input baseline is the published source plus pre-existing worktree, as recorded in Plan. The checker validates declared IDs/files; the table's semantic/revision alignment is agent-reviewed. The current research Task is linked above and does not reopen that approved product scope.



| Requirement / acceptance | Spec | Plan item | Executable steps / evidence | Baseline views |

| --- | --- | --- | --- | --- |

| REQ-LINKED-01 / AT-LINKED-03 | [ownership and boundaries](../docs/spec.md) | [PL-01](../docs/plan.md) | [TW-01/02/04/05](linked-artifact-model-task.md) | [map](../docs/module-map.md), [flow](../docs/business-flow.md) |

| REQ-LINKED-02 / AT-LINKED-01 / AT-LINKED-02 | [linked fields and compatibility](../docs/spec.md) | [PL-02](../docs/plan.md) | [TW-03/05](linked-artifact-model-task.md) | [contracts](../docs/contracts.md) |

| REQ-LINKED-03 / AT-LINKED-03 | [correction and history](../docs/spec.md) | [PL-03](../docs/plan.md) | [TW-04/05](linked-artifact-model-task.md) | [baseline](baseline-review.md), [flow](../docs/business-flow.md) |

| REQ-LINKED-04 / AT-LINKED-04 | [greenfield lifecycle](../docs/spec.md) | [PL-04](../docs/plan.md) | [TW-02/03/05](linked-artifact-model-task.md) | [contracts](../docs/contracts.md), [map](../docs/module-map.md), [flow](../docs/business-flow.md) |

| REQ-LINKED-05 / AT-LINKED-05 | [document reconciliation](../docs/spec.md) | [PL-05](../docs/plan.md) | [TW-04/05 reconciliation table and current validation](linked-artifact-model-task.md) | [baseline](baseline-review.md), all current views |



Historical task/requirement registrations remain in the manifest and their original files. This current index does not transfer past approvals or rewrite release receipts.



Publication evidence: 1.5.0 source `46d57a6cefd5cc80ae62e47099b782d4cb381504`, uploaded 2026-10-18; staged and exact-commit check reports plus the source-upload receipt are recorded in the current Task. The requirement/Plan/step mappings remain unchanged.
