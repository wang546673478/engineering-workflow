# Current Engineering Workflow Baseline

Current revision: `BASELINE-CONTEXT-06` (2026-10-18), based on source commit `82b3c8531a9a9867dd77756444a2bcbc922aa2c8`; receipt commits change only evidence and linked-view status. Current facts include unchanged engineering stages and checker commands, local collection/JS/TS/Rust module evidence, selectable views, and a corrected protected-CI result contract: diagnostic reruns cannot replace the original required checker outcome. Exact source SHA `3fab75ba5d8e2663af811d2b7daee53c90fe6818` passed the approved Ubuntu/Windows reviewed jobs and aggregate quality run `39115700117`. Exact scope and validation are in [Task](source-context-task.md) and [evidence](source-context-evidence.json). User authorization covers the CI correction and upload; it does not certify target-project business behavior.

## Historical 1.5.0 baseline (original evidence/review scope)


Revision: `BASELINE-LINKED-02` (2026-10-18); factual scope and required local checks complete, validation recorded in [the active Task](linked-artifact-model-task.md). Historical approval below applies only to its original tree; the subsequent 2026-10-18 upload instruction approves submission/publication of this completed revision, as recorded in the current Task.

Source basis: `9df566229c976e3f3523007934e9f079550c770f` as the implementation input; the 1.5.0 output was uploaded on 2026-10-18 as `46d57a6cefd5cc80ae62e47099b782d4cb381504`. Scope: SKILL/references, managed guidance, templates, manifest initialization, checker, tests and self-maintenance documentation. Earlier pre-existing assessment-task edits remain separately owned; no external project was migrated.

## Current facts and coverage

- Instructions define Baseline/current facts, stable approved Spec, technical Plan, executable Tasks and evidence-driven correction. Greenfield starting-state/partial/factual completion and existing-document reconciliation have explicit routes.
- The initializer only writes a planned manifest; explicit greenfield mode declares implementation scopes (default src/tests), not nonexistent system facts or approval. Full/lite link all views; existing flat projects use actual candidate scopes instead of root triggers.
- The checker validates declared pointers/files and greenfield provisional lifecycle. Provisional states require evidence metadata, reject existing origin, reject no-implementation claims when files occur in declared scopes, and block completion/handoff. Old manifests keep their prior gates.
- Current architecture and CLI facts are in [module map](../docs/module-map.md), [contracts](../docs/contracts.md) and [business flow](../docs/business-flow.md). [Spec](../docs/spec.md), [Plan](../docs/plan.md), [Task](linked-artifact-model-task.md) and [traceability](traceability.md) separate target, design and execution.
- No business database, application frontend or HTTP service exists here. The [database view](../docs/database.md) retains explicit metadata-only adapter scope. Adapters were not modified in this batch. Optional manual database/contract inventories remain partial; they do not prove semantic completeness.
- Verification: unchanged TEST (105 tests), COMPILE and GUIDANCE-COMPILE passed; the change-scope/manifest/task gates passed with no uncovered paths or documentation gaps. Official skill validation passed using existing isolated PyYAML. Local implementation report: work/linked-greenfield-final-check.json; source fingerprint: work/linked-greenfield-source.json. Source publication was additionally verified by staged/committed reports in the current Task. The active Task records results/limits; historical results below are not fresh evidence.

## Limits and review

Declared source scopes are not an automatically discovered dependency graph; a custom undeclared implementation location still requires agent discovery. The checker cannot prove semantic consistency, revision agreement or user approval. No hosted CI, external project, production database or host loading behavior is established by local checks. Finished protected changes and publication are authorized by the current user upload instruction; source upload and hosted CI still require their own evidence.

## Historical review retained verbatim

The following original review is retained as history, not as approval of BASELINE-LINKED-02.

# Engineering Workflow Baseline Review

Prepared: `2026-10-14`  
Repository: `engineering-workflow`

The mechanical baseline covers the skill entrypoint, public guide, UI metadata, references, templates, checker, adapters, and tests. The active manifest maps these areas to modules and records the database boundary as metadata-only. The database and contract inventories are intentionally partial because this repository has no application database and its CLI contract is manually documented.

On 2026-10-14 the user accepted separating mechanical checks from human review and accepted an empty business-database inventory with adapter documentation retained. The user allowed this repository's Actions workflow while requiring support for projects without GitHub, requested immediate rule protection, and authorized installing PyYAML to run skill validation.

The user subsequently reviewed the final plain-language summary and stated: “符合我的意思,是不是都已经改好了,改好了就上传github吧”. This authorizes the completed change and publication to the existing GitHub repository. The approved staged tree before recording this decision was `704b3d5a4ebbd5d298475d4efc9341c70093cd35`, based on local commit `91d0dcc`. Recording the approval, task completion and publication result does not expand the implementation scope.

Review status: approved on 2026-10-14. The external approval signal is supplied only for this reviewed change's verification; it is not stored as an executable setting or automatic approval for later changes. Hosted reviewer/branch settings and remote execution require their own evidence and are not established by this document.

PyYAML 6.0.3 was installed into ignored `work/pyyaml` at the user's request. The independent skill-creator quick validator succeeded with UTF-8 enabled. No global dependency was installed.


## Current source-context annex

BASELINE-CONTEXT-03 (2026-10-18): preserved existing workflow plus local source helpers, optional syntax adapters and selectable evidence views. Input c21e715; actual implementation/semantic scope, tests, two read-only source snapshots and publication evidence in [Task](source-context-task.md). Prior baseline reviews do not transfer to this revision; current user authorization explicitly covers selecting/integrating/uploading helper functions while keeping workflow phases/gates unchanged. External target-project business correctness is outside tool validation.


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.


The 1.6.1 hosted-report review additionally isolates checker/initializer test fixture task and approval environments; product checker/CI policy stays unchanged. Initial hosted artifacts remain failed historical evidence despite the workflow diagnostic retry succeeding. The follow-up validates the unchanged declared commands with the enclosing CI variables present; exact results are in the current source-context Task.


### BASELINE-CONTEXT-05: hosted test environment finding

Actual protected-run artifacts showed a test fixture inherited the parent task ID, making temporary projects run against the main manifest task. Isolating task/approval variables at fixture setup fixes only test setup; checker behavior and declared checks are unchanged. The original hosted artifacts remain failed history; the current correction has passed the same full command with those parent variables present. See [current Task](source-context-task.md) and machine evidence.


### BASELINE-CONTEXT-06: reviewed CI result integrity

Run `39110935645` showed that the original Windows TEST report failed while the diagnostic rerun passed; the workflow then marked the reviewed job successful. Both reviewed and manual-reviewed finalizers used the diagnostic rerun as an alternate success condition, so the aggregate quality job could report success without the original required checker passing. The finalizer now treats the original checker outcome as authoritative on both paths. The verbose rerun remains available for diagnosis and cannot recover a failed required check. Existing command definitions, test scope, 120-second timeout, protected environment, and approval duties remain unchanged. Implementation and new regression evidence are tracked in [the current Task](source-context-task.md).
