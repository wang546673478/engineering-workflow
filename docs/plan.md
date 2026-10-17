# Linked Baseline / Spec / Plan / Task Technical Plan

Revision: `PLAN-LINKED-02` (2026-10-18). Status: implemented and locally verified; the subsequent user upload instruction authorizes submission/publication of this batch.

Basis: [Spec](spec.md) `SPEC-LINKED-02`; input baseline is published `9df5662` plus the recorded pre-existing working-tree changes. The evolving output is [BASELINE-LINKED-02](../planning/baseline-review.md). Input/output baseline revisions differ intentionally as implementation proceeds; historical approval does not transfer to the output.

The user requested “那就开始完整的更改吧” and asked to compare and organize existing documents on 2026-10-18. This authorizes completing the local batch including the greenfield path described in the preceding discussion. The later instruction “升级完成就上传github” now authorizes committing and uploading this completed batch; the current Task records scope and evidence. This revision supersedes the initial unnumbered draft, whose six decisions are retained in PL-01..03 and PL-05 below.

## Implementation items

| Item | Requirements / acceptance | Design and affected baseline views | Verification |
| --- | --- | --- | --- |
| PL-01 | REQ-LINKED-01 / AT-LINKED-03 | Define ownership and revisions in one reference; route from SKILL and persistent guidance. Freeze approved Spec boundaries; distinguish current summaries and history. Views: map, workflow | Review references, template, current Spec/Plan/Task and links |
| PL-02 | REQ-LINKED-02 / AT-LINKED-01..02 | Reuse schema 1 optional active pointers, artifact_links and baseline.document_ids; check IDs/file existence without requiring new fields on old manifests. Views: CLI, map | Existing compatibility tests and focused linkage failures |
| PL-03 | REQ-LINKED-03 / AT-LINKED-03 | Correct evidenced facts first, reconcile Plan/Task, reopen Spec only for changed intent/premises. Preserve approval history. Views: baseline, workflow | Reconcile repository docs and retain original review |
| PL-04 | REQ-LINKED-04 / AT-LINKED-04 | Explicit greenfield initialization and implementation scopes. Init stays planned; evidenced not_applicable → partial → factual complete. Reuse ordinary task/check/control gates. Views: CLI, baseline, workflow | Both profiles from empty directory to first code and completion; reject existing-origin exemptions, unsafe scopes, hidden implementation and premature completion/handoff |
| PL-05 | REQ-LINKED-05 / AT-LINKED-05 | Refresh current authority, status/basis/links and execution steps; retain historical decisions and approvals. Sync 1.5.0/Unreleased. Views: all current docs | Reconciliation table, unchanged required checks, skill validator, change-scope and diff review |

## Dependencies and execution

PL-01/03 establish the model; PL-02/04 implement its mechanical portion; PL-05 reconciles final behavior and evidence. Task steps TW-01..05 and results are in [the current Task](../planning/linked-artifact-model-task.md); mappings are in [traceability](../planning/traceability.md).

The checker inspects declared paths/references; it cannot prove semantic consistency, revision alignment, origin truth or approval authenticity. Provisional lifecycle success reports completion_ready=false. Existing required checks and control protections remain intact. Flat/no-source initialization must not emit illegal root triggers; generated scopes and default TEST remain reviewable candidates, not a discovered architecture or verification policy.

## Compatibility, migration and recovery

Old manifests omitting new fields retain their complete/approved path. Existing projects receive no provisional exemption. Both newly generated profiles require linked views; lite omits inventories and records implementation impact, while full conservatively requires baseline views. Review actual project boundaries rather than weakening existing rules.

The initializer writes only a skeleton and refuses overwrite by default. Reconcile manifests in place after review; retain previous Spec/Plan/review evidence and correct current authority. Database adapters, business data, external projects and hosted settings are outside this batch; no business-data migration is needed. Local changes remain reviewable in the working tree, with submission/publication separate.

## Verification and release

Run unchanged TEST, COMPILE and GUIDANCE-COMPILE; skill-creator validation with isolated PyYAML; local links, change-scope and diff review. New transitions run in disposable fixtures. Commit/committed gates apply when submission is authorized. Record exact results/limits in Task. The 1.5.0 source batch was uploaded on 2026-10-18 as `46d57a6cefd5cc80ae62e47099b782d4cb381504`; publication receipts do not change the design or require another version bump. Hosted CI is verified separately.
