# Current Engineering Workflow Baseline

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
