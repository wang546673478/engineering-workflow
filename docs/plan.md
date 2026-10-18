# Source Context Technical Plan

Revision PLAN-CONTEXT-06, based on unchanged SPEC-CONTEXT-03 and input BASELINE-CONTEXT-05/a407b112. The current user instruction authorizes the evidenced hosted-CI correction and upload; exact scope and wording are in [Task](../planning/source-context-task.md). Output BASELINE-CONTEXT-06.

1. Preserve existing engineering stages and checker controls; require the original checker result to pass on both protected review paths, keeping diagnostic reruns for evidence only.
2. Reuse safe path/glob primitives; provide complete source packs with explicit omitted states, per-run discovery reuse and optional syntax adapters.
3. Compare P1..P4 in the Task on both frozen corpora; prefer scoped task-first execution unless evidence justifies reference-led expansion; output one appropriate view.
4. Preserve original required checks and timeouts. Make the original checker outcome authoritative in reviewed and manual-reviewed paths through the shared `.github/scripts/finalize_reviewed_quality.py`; keep diagnostic reruns for evidence only and cover finalization behavior with regression tests.
5. Reconcile current views/version/evidence, then staged/committed checks, authorized upload and independent hosted-status evidence.

Local commit and exact-commit checks passed on source commit `82b3c8531a9a9867dd77756444a2bcbc922aa2c8` and receipt commit `a693a9e28c598f1ac5cf2dbd332646097f392523`. Source SHA `3fab75ba5d8e2663af811d2b7daee53c90fe6818` was approved for `engineering-control-review`; run `39115700117` passed its Ubuntu/Windows reviewed jobs and aggregate quality check. Machine-readable artifact digests are in the current Task evidence.

## Historical plan (original scope retained)

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


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](../planning/source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](../planning/source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


## CI fixture correction

Keep explicit assertions and existing commands/timeouts. Scope the parent task/approval environment only to the host project; each checker and initializer test fixture must provide an isolated environment so generated manifests exercise their own active task. Re-run all declared tests with the real outer variables present, then validate the exact commit on both hosted platforms. Full results are recorded in [Task](../planning/source-context-task.md).
