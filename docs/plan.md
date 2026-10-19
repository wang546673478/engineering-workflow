# Current plan: PLAN-ADOPTION-LIFECYCLE-02

Input `BASELINE-SAFE-19-21-01` / source `3c1cb36`; specification `SPEC-ADOPTION-LIFECYCLE-02`; output baseline `BASELINE-ADOPTION-LIFECYCLE-01`; execution: [Task](../planning/adoption-lifecycle-task.md).

1. ADOPT-01: Add a complete adoption CLI that preserves existing manifests, offers an explicit additive legacy migration with atomic replacement, writes a planned provenance-bound scaffold and guidance, and emits actual bundled read-only bootstrap diagnostics.
2. ADOPT-02: Extend initializer output with document overrides, lifecycle stage, implementation paths, independent approval placeholders and skill provenance fields.
3. ADOPT-03: Validate lifecycle invariants and block implementation-scope changes in discovery/review/interview/proposal stages while preserving legacy manifests without lifecycle fields.
4. ADOPT-04: Synchronize public guidance, templates, checker contract, module map, business flow, Baseline and traceability; distinguish skill source/version from host loading.
5. ADOPT-05: Run focused adoption/lifecycle regressions plus TEST, COMPILE, GUIDANCE-COMPILE and skill validation; record version 1.7.0 Unreleased and exact evidence.

Original-flow parity correction: guidance can precede manifest with an incomplete receipt; greenfield/small-fix not_applicable records require evidence; valid historical reviews remain reusable; a single explicit instruction may cover proposal plus implementation; complete/approved and original handoff requirements remain. Test real CLI/Git scenarios, retain original limits, upload exact tested source, rehearse a preserved-dirty-install upgrade, then update the existing global installation. No external adopted project or business data changes apply.

## Prior plans and evidence

# Current plan: PLAN-SAFE-19-21-01

Input BASELINE-UX-17-18-01 / 871bda427d3f46d114e568565dac10cca1395920 plus ASSESS-19-21-01; specification SPEC-SAFE-19-21-01; output BASELINE-SAFE-19-21-01. Implementation/status: [Task](../planning/issues-19-21-task.md).

1. SAFE-01: Snapshot Git HEAD/index before reading inputs, retain initial scope/control checks, and require final state consistency in commit and committed. Add verified_tree/verification_head only on overall success. Keep hook/CI exit-code consumption; validate a real pre-commit template and actual commit tree.
2. SAFE-02: Share file/history JSON decoding error handling; validate root type before workflow lookup; distinguish absent historical files from unreadable/damaged policy. Add deep object/array, integer, root and large-shallow behavior regressions without new arbitrary size limits.
3. SAFE-03: Own command lifecycle in finally, restore CLI cancellation handlers, preserve bounded output/waits, and clean ordinary groups/families. Windows Job Object creation/assignment precedes command execution via suspended startup; setup failure rejects execution. Validate native family, cancellation, timeout and platform lifetime boundaries, with no absolute POSIX SIGKILL guarantee.
4. SAFE-04: Refresh affected baseline/module/CLI/flow views, traceability and 1.6.4 PATCH metadata. Run original full checks plus focused native behavior tests and package validation, preserving failures as evidence.
5. SAFE-05: Exact staged/committed verification, authorized GitHub upload and independent hosted verification, then factual issue-specific replies/closure and publication receipts.

No business-data migration applies. Existing projects need no manifest migration. Generated ignored artifacts remain allowed, persistent source drift now fails. Protect the same checker entrypoint and policy; do not move lifecycle/security logic to an unprotected helper. External sandbox/strict hard-kill containment and new JSON resource policies remain deferred.

## Prior plans and evidence

# Current plan: PLAN-UX-17-18-01

Based on SPEC-UX-17-18-01 and input BASELINE-CONTEXT-06 / 0216e4cd341bee534ccc85a8824c83a40a7e9840 plus ASSESS-17-18-01. Output baseline: BASELINE-UX-17-18-01. Scope and implementation status are in [Task](../planning/issues-17-18-task.md).

1. UX-01: Reuse the existing segment-aware glob in initializer defaults, with both profiles and before/after-install fixtures. Preserve existing project manifests and explicit checker policy.
2. UX-02: Derive grouped dependency diagnostics from existing unsupported records. Add details to status/CLI/text; keep existing enums and valid partial graphs. Distinguish an installed JS analyzer execution failure from a missing runtime/parser.
3. UX-03: Make required parser fixture setup fail with preparation guidance; add simulated missing-environment and mixed/empty-reference behavior coverage. Document both optional runtimes and full-suite setup; no skip or gate relaxation.
4. UX-04: Refresh affected baseline views, traceability and version 1.6.3 PATCH. Run original TEST/COMPILE/GUIDANCE-COMPILE, focused behavior checks, package validation and exact commit gates.
5. UX-05: Publish tested source to GitHub, verify exact remote SHA, then post factual issue-specific replies and close #17/#18 as explicitly authorized. Hosted independent environment review remains separate.

Compatibility/recovery: new explicit defaults affect only newly generated manifests; old ones need reviewed migration. Diagnostics are additive JSON fields, core collection exit semantics stay unchanged, and no business-data migration applies. Avoid workspace-specific config parsers, implicit checker excludes, target-project dependency installation and new strict-analysis modes.

## Prior plans and evidence

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


UX-01..05 implementation/publication actions are complete on source 0040878 with passing original local gates and verified issue closure. This follow-up records real release date and receipts only, retaining 1.6.3 and all source/acceptance boundaries.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.


Published implementation5f9b3e1d54a0709241fb5f11173e13ce00af3ffd passed local184-test staged/exact-commit gates and original Windows/Ubuntu reports in approved run39157028881; source upload and #19/#20/#21 replies/completed closure were verified on 2026-10-19. Receipt-only updates do not change implementation, targets, limits or prior approval scope.
