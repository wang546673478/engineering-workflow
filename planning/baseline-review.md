# Current factual baseline: BASELINE-ISSUE23-02

## Issue #24 workflow-state implementation supplement / 2026-10-22

After the existing local archive/recovery CLI, this repository now contains a second independent optional helper, `scripts/workflow_state.py`. It reads the same manifest/task records and offers stdout index, exact snapshot, and explicit hash-guarded batch apply. Lifecycle metadata is optional and remains a view over manifest/task state; this batch does not migrate existing project manifests or populate guessed historical statuses. Unregistered Markdown under `planning/` appears as unknown/unverified. Completed Task status and approval status are separate index columns.

The writer accepts strict duplicate-key rejecting JSON, rejects protected workflow/task approval/gate targets, validates the full manifest link/lifecycle invariants and all target hashes, rejects requests stored among mutable project documents, checks workspace/archive drift, and stores the proposed full projection in one existing SQLite archive revision. Same-directory replacements preserve encoding/newline style and ordinary errors attempt reversal; a forced process interruption or rollback I/O failure may leave a partial workspace projection, which the archive drift check exposes and `restore --project-head` can reconstruct. This does not provide cross-file atomic visibility or host-level write enforcement. Host cwd failure before process startup remains unsupported.

Affected views: workflow-state module and test dependency, instruction routes/contracts, Baseline module/flow contracts, active Task/Spec/Plan/traceability and release metadata. No application database, API or checker mode change. Following the user's explicit decision, the sole gate adjustment is the TEST timeout 120s → 240s; TEST argv, coverage/assertions, required status and all workflow/approval contracts remain the same; COMPILE/GUIDANCE-COMPILE stay 30s. Revalidation against that updated manifest is recorded in [Issue #24 Task](issue-24-efficiency-task.md).

Windows Actions correction (2026-10-23): run 39787233509 exposed that Windows temporary paths can alternate between long names and 8.3 aliases. Public checker safe-path containment now expands existing short aliases component-by-component before root comparison. The original candidate/component link checks and final resolved-root containment remain in force; alias canonicalization does not replace link defense. Workflow-state archive/batch and explicit outside-alias rejection are covered by Windows regressions. Full 262-test checker and formal baseline checks pass, and cover the newly added checker and workflow-state path-alias regressions. Evidence and current source revision are recorded in the Issue #24 Task. No workflow stages, matrix legs, approvals, commands, or timeout policy changed.

2026-10-22 record-integrity implementation supplement: Added optional `scripts/task_archive.py`, which snapshots manifest-declared engineering files into an explicitly located local SQLite archive and supports drift detection, compare-and-swap checkpoints, history and restore-as-new-revision. It is outside the existing 1.8 approval/check flow. Five initial archive CLI behaviors (now six focused scenarios) are tracked in `planning/issue-23-record-integrity-task.md`. Direct shell/editor writes remain possible; host-level write isolation is unsupported. No project has been automatically migrated.

当前本机安装事实（2026-10-21）：共享路径已更新至1.8.0/a3129db，59个受管理资源Git对象匹配、19项本地修改保留；安装结构与CLI烟测通过。此记录不扩大源码/业务语义或活动会话加载认证范围；见[安装回执](issue-23-local-installation.json)。

同批技术保持性修正：提交校验在单次main内复用control-plane已读取的历史manifest，避免重复Git查询；缓存不跨验证运行。静态合同用例经同一公开CLI入口减少解释器启动，原安全断言、测试/超时/同步边界保持。新源码门槛结果见Issue23 Task/evidence。

源上传回执（2026-10-21）：1.8.0实现提交`9723921ceac69db363fb4b655d761bc61b956e0f`已上传origin/main，原commit/committed门槛与远端SHA核对通过。此记录只更新发布事实，原内容/限制及Unreleased保留；托管CI、全局安装和外部项目迁移分开记录。

最终本地验证：1.8.0 Unreleased，225项及原120/30/30秒门槛通过；当前source摘要、非必需partial和CPython3.14耗时限制见[Task](issue-23-task.md)及[正式证据](issue-23-evidence.json)。没有提交树/托管CI/全局安装认证。

2026-10-21; source d214021 plus current 1.8.0 Unreleased worktree. Approved basis: SPEC-ISSUE23-01 / PLAN-ISSUE23-01 r1, user “那就开始实施吧” after the explicit compatibility clarification. This is current implementation fact, not a transfer of old human approval to all new evidence.

- Checker now implements optional approval contract 1: Markdown/JSON records, safe path/duplicate-key/ID rejection, timestamps, original statement/source/scope, stable section hashes and selected task batch/REQ/AT plus Spec/Plan revision binding. Original lifecycle/old task approval gates remain.
- Current evidence resolution supports bounded explicit reuse, preserves original statement/time/source and subjects, and rejects invalidated or expanded scope. Technical equivalence uses an explicit review-basis relation that still needs agent semantic review.
- New scaffolds and legacy migrations default diagnostic; strict opt-in blocks invalid approval execution. Existing-stage migration previews proposed checks without mutating files, then explicitly applies via atomic replacement. No existing project is automatically migrated.
- History comparison protects enabled policy and strict path/stage scope; downgrades require original one-run external control approval. Optional sequence comparison is declared-event evidence, not host attestation. Capability flag and hook configuration detect use of an older checker.
- All existing required commands/timeouts, Git tree checks, metadata adapters and impact/synchronization paths are retained. No product DB, external application or global installation change. Current regressions and actual final gate status remain owned by [Task](issue-23-task.md) and evidence; do not infer all tests passed from this source summary.

Source module/contract/flow views were refreshed together. The original real-session audit and unimplemented-upstream review limits remain historical below.

## Prior assessment and evidence (original scope retained)

# Current factual assessment: BASELINE-ISSUE23-01

2026-10-21; source `d214021` / 1.7.2, initially clean worktree. Current Task: [TASK-ISSUE-23-PROPOSAL](issue-23-task.md). Existing implementation and prior local baseline coverage remain; this revision adds source-verified facts and bounded counterexamples, without implementing a new approval system.

- B23-01: SKILL distinguishes goal/requirement selection from complete proposal approval and implementation; original exceptions allow valid prior review reuse, established small fixes and evidenced greenfield scope.
- B23-02: workflow_lifecycle_gaps already checks approval evidence file existence when stage lifecycle is enabled. It does not read approval content or authenticate a human. This corrects Issue 23's literal claim that no existence check exists.
- B23-03: Legacy manifests without stage receive non-required workflow-lifecycle partial; implementation_gate is absent. The target manifest takes this path and its old implementation authorization is outside the new Plan/batch scope.
- B23-04: Five isolated real-CLI scenarios accept empty/placeholder approval files, a current Plan mismatch, a future approved_at, and a stale legacy authorization. [Evidence](issue-23-evidence.json) binds commands, source digests and individual original results. These are defect reproductions, not fixed-feature passes.
- B23-05: The inspected target conversation contains three turns; its final turn was active when read. One enterprise identity choice was followed by P1-P6 planning and product edits without an intervening full-plan user approval. Source item IDs and snapshot bounds: [session evidence](issue-23-session-evidence.json).
- B23-06: The target prior delivery report has required_checks_satisfied=false despite errors=[]; manual product-test success does not change required inventory partial, dependency fail or skipped declared commands. No target product tests were rerun in this investigation.
- B23-07: New targets are candidate [Spec](issue-23-spec.md) / [Plan](issue-23-plan.md), not current implementation. No scripts, required checks, protection rules, templates, adapters or product database changed. Module/contract/flow views receive factual annotations only.

Current source revision is not a new human approval. Prior approved revisions and Issue 22's deferred full upstream review retain their own scope. This local skill assessment does not certify target product behavior or later actions in the active chat.

## Prior records (historical; original scope retained)

# Current factual baseline: BASELINE-ISSUE22-02

1.7.2 source upload receipt (2026-10-20T17:52:35.783179+08:00): implementation 5b8013c9b67debff0b080da563781a39f6e69f74 is verified on origin/main with original local staged/exact-commit gates and tree 7c0c112192ea337ab4515113c4c342375924e497. This receipt changes evidence/status only; current local facts and original limits remain. Hosted CI and global installation are separate.

2026-10-20; input BASELINE-ISSUE22-01 / source `868e4967512c2cd400307368d924291a3d4d8eef`, plus the 1.7.2 Unreleased working-tree guidance changes. The three enhancements are now implemented in the original implementation-workflow, baseline-linked-artifacts and requirements-interview references, with short SKILL/README routes and optional prompts in the original spec-plan-task/impact-analysis templates. Current verification and source hashes are owned by [Task](issue-22-task.md) and [evidence](issue-22-evidence.json); the original local required checks and bounded same-agent manual scenarios have passed there; initial failed checks and environment correction remain in that evidence.

Responsibilities and information flow are reflected in [module map](../docs/module-map.md), [contracts](../docs/contracts.md) and [business flow](../docs/business-flow.md). There is no new CLI/schema/runtime module or product database; the original checker/adoption/source-context/adapters, required checks/timeouts, stage/approval/exception and control policies remain unchanged. Database-view non-applicability was rechecked against docs/database.md and unchanged adapter source. Existing records/formats remain valid; examples do not establish approval or test execution.

The user explicitly instructed “那就按照这个增强的文档去实施” after requesting an interim result and stopping exhaustive reading. This authorizes these local enhancements based on the bounded conclusions; full upstream semantic review remains incomplete and deferred (366 reviewed, 3,177 unread). This baseline covers the local skill changes and does not certify unreviewed upstream behavior, global installation, publication or hosted CI. Earlier approvals and evidence remain tied to their original content.

## Prior factual supplement: BASELINE-ISSUE22-01

当前执行更新（2026-10-20）：最新用户指令要求当前文件读完即先交阶段性结果，全量审读暂缓。当前本地skill事实和1.7.1源码未变；三项增强仍未实施。已读范围及限制见[assessment](issue-22-assessment.md)，原本地完整基线不扩大到未读上游。

Spec review update (2026-10-20): the user accepted the three enhancement directions and explicitly requested a globally scoped Spec while retaining the current workflow. [SPEC-ISSUE22-ENHANCEMENT-01](issue-22-spec.md) is a draft, not implemented behavior or transferred approval. This does not change the source facts or complete the independent upstream semantic review described below.

Plan/Task continuation (2026-10-20): [PLAN-ISSUE22-ENHANCEMENT-01](issue-22-plan.md) binds ten source-based facts B22-01..10 to existing B/M/C/D/F views and Spec requirements; [Task](issue-22-task.md) records the executable T22-01..16 dependencies. No enhancement target is promoted to implemented fact. Source and existing checker/adoption/adapter/source-context dependencies remain unchanged. The five-repository semantic gap stays open; this planning record does not extend the scope of a complete local implementation baseline to unreviewed upstreams.

2026-10-20; source `868e496` / 1.7.1, initially clean worktree. Current task is [TASK-ISSUE-22-REVIEW](issue-22-task.md), with [source assessment](issue-22-assessment.md). The existing implementation baseline below remains bounded to its original revisions and tests; prior adoption/publication approval does not approve Issue 22 enhancements.

Current source already specifies defect reproduction/localization, continuous correction and six-step delivery convergence. The checker verifies declared IDs/references/scopes, lifecycle exceptions and command outcomes; it does not infer behavioral correctness or execute a general code-to-requirements proof. `documents.kind` is a nonempty string, while `workflow_kind=small_fix` preserves a specific existing exception. These facts correct the Issue's absence claims without changing skill behavior.

All five user-selected upstream repositories are pinned and fully inventoried. Whole-file collection/AST inspection and reviewed critical chains are separate from full per-file semantic review, which is still incomplete. This supplement is not acceptance of unreviewed upstream behavior or certification of the 1.7.1 hosted results. No skill/CLI/template/test changes are made in this assessment batch; database, contracts and module dependencies retain their implementation scope.

Execution continuation (2026-10-20): the user explicitly authorized the complete Plan r1 with “开始实现吧”. Its source-review dependencies remain; targets have not become current implementation facts. Authorization does not recertify upstream coverage or hosted results and does not authorize publication. The current Task/manifest carry the actual approval and execution state.

## Prior implementation baseline and approval scope

# Baseline: BASELINE-ADOPTION-LIFECYCLE-02

Current parity correction: original core SKILL sections have been restored unchanged; tooling now supports guidance-first incomplete setup, evidenced greenfield/small-fix exceptions, valid prior-review reuse, shared explicit authorization and complete/approved completion. The earlier finding below is historical; new source passed 205 local tests and original compile gates; exact submission/commit validation and installation rehearsal follow before publication. User has authorized testing, GitHub upload on success and preserving the existing local installation. No external adopted project changes apply.

Historical 23:04 review finding: the first unreleased patch tightened original gates and did not satisfy workflow parity; original 200-test evidence did not establish semantic parity. Preserve that finding in Task/history rather than applying it as the current source conclusion.

2026-10-19; input `BASELINE-SAFE-19-21-01` / source `3c1cb36` plus the current 1.7.0 Unreleased adoption-lifecycle working tree. The original 1.6.4 installer-only entry could succeed without a manifest. Current source now provides complete adoption, a real JSON manifest requirement, explicit additive legacy migration, actual bundled read-only bootstrap diagnostics, and opt-in stage/approval/implementation-path gates. Original defect/recovery observations remain in [Task](adoption-lifecycle-task.md); they do not describe the new implementation as still missing.

Current facts: new scaffolds stay planned/pending and record skill/checker provenance; reruns preserve lifecycle state; atomic migration failure preserves the old manifest. Baseline review, proposal approval and task implementation authorization are separate. Change/handoff/both submit modes classify declared implementation paths, and blocked submit checks do not execute commands. Instructions call the bundled checker for diagnostics, then checker uses existing adapters; no reverse dependency or application database change.

Current coverage: entrypoints, initializer/guidance/checker code, template/schema, tests and linked governance views. All affected current views, release metadata and traceability are synchronized; fresh verification and exact source digests belong to [Task](adoption-lifecycle-task.md). Limits: old manifests remain compatible until explicitly migrated; declarations cannot prove semantic completeness, genuine human review, host loading, dynamic dependencies or missed implementation scopes. This repository's maintenance manifest keeps its prior approval model rather than manufacturing new lifecycle approvals. External adopted projects remain outside scope; updating the existing global skill installation is now explicitly authorized after validation, with all prior local work preserved. Historical reviews retain their original scope.

## Prior baseline revisions and review scope

2026-10-19; input871bda427d3f46d114e568565dac10cca1395920 plus TASK-ISSUES-19-21 working tree. Current implementation binds pre/post Git verification state, handles JSON input limits/root errors and historical corruption, and owns command family/reader cleanup including catchable cancellation. Windows commands are assigned to a kill-on-close Job Object before resume; POSIX uses existing process groups. Prior ASSESS-19-21-01 describes pre-fix facts and remains historical. Current scope and fresh validation: [Task](issues-19-21-task.md), [fix evidence](issues-19-21-fix-evidence.json).

Workflow stages, required command declarations/timeouts, existing exclusions and independent approval controls are unchanged. State checks are stricter after execution; corrupt historical policy and unavailable Windows lifecycle setup fail closed. No business database/adapter change applies. Hostile-code sandboxing, later-hook races, POSIX SIGKILL and Windows pre-assignment hard-kill windows remain limits, not completed features. Current implementation5f9b3e1 is published and its original local/hosted gates are verified; receipt-only updates retain separate validation identities.

## Prior baseline revisions and review scope

# Current baseline: BASELINE-UX-17-18-01

Known-defect supplement ASSESS-19-21-01 (2026-10-19, source871bda4): [assessment](issues-19-21-assessment.md) and [evidence](issues-19-21-evidence.json) confirm commit/committed state checks occur only before declared commands, leaving runtime index/worktree/HEAD drift undetected. File and historical JSON parsing can emit unstructured recursion errors; root-type/large-integer inputs expose related boundaries. Windows controlled interruption leaves descendants/readers alive, and timeout kills only the direct child. The intended consistency/cleanup goals remain unchanged; these are implementation gaps, not relaxed requirements. POSIX native signals and hostile-code sandboxing are not established by the Windows fixtures. Prior source hashes/tests/reviews retain their original limited scope; this assessment does not authorize fixes.

2026-10-19; source base 0216e4cd341bee534ccc85a8824c83a40a7e9840 plus the TASK-ISSUES-17-18 working tree. Current implementation now generates explicit recursive node_modules exclusions in both profiles, surfaces parser reasons/setup diagnostics in relation status/CLI/text, retains partial references, and fails required parser fixture setup early with actionable guidance. Core collection, existing manifests, checker rules and CI gates are unchanged. Current verification/publication evidence belongs to [Task](issues-17-18-task.md) and [fix evidence](issues-17-18-fix-evidence.json); prior 163-test assessment reports are historical. No business database or metadata-adapter change applies.

The user adopted the bounded assessment and requested implementation/upload and issue replies/closure; exact wording is in the Task. This is not a transfer of old baseline reviews, and the program checks still require fresh results. Modules, contracts and flows below are linked current views.

## Prior baseline revisions and assessment evidence

# Current Engineering Workflow Baseline

Current revision: `BASELINE-CONTEXT-06` (2026-10-18), based on source commit `82b3c8531a9a9867dd77756444a2bcbc922aa2c8`; receipt commits change only evidence and linked-view status. Current facts include unchanged engineering stages and checker commands, local collection/JS/TS/Rust module evidence, selectable views, and a corrected protected-CI result contract: diagnostic reruns cannot replace the original required checker outcome. Exact source SHA `3fab75ba5d8e2663af811d2b7daee53c90fe6818` passed the approved Ubuntu/Windows reviewed jobs and aggregate quality run `39115700117`. Exact scope and validation are in [Task](source-context-task.md) and [evidence](source-context-evidence.json). User authorization covers the CI correction and upload; it does not certify target-project business behavior.

Assessment-only supplement (2026-10-19): [ASSESS-17-18-01](issues-17-18-assessment.md) and [source-bound evidence](issues-17-18-evidence.json) verify initializer defaults, explicit exclusion consumers, optional parser statuses and required-test skip handling at remote 1.6.2/0216e4c. The initializer still emits root-only node_modules while the example manifest uses a recursive glob. Missing Rust/JS parsers already have explicit unsupported records; terminal guidance and test setup diagnostics remain usability gaps. Required unittest skips remain partial and cannot satisfy the gate. This factual supplement neither changes implementation nor transfers prior review/implementation approvals; the existing baseline revision/history below remains bounded to its original source.


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


The implementation source 0040878f69450657bb65ee779b6cecda4697049d was published on 2026-10-19; the same source passed fresh 170-test change/commit/committed gates. #17/#18 replies and completed closure are verified. This receipt revises evidence/status only; hosted approval/results remain separate.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.


Published implementation5f9b3e1d54a0709241fb5f11173e13ce00af3ffd passed local184-test staged/exact-commit gates and original Windows/Ubuntu reports in approved run39157028881; source upload and #19/#20/#21 replies/completed closure were verified on 2026-10-19. Receipt-only updates do not change implementation, targets, limits or prior approval scope.

Publication receipt (2026-10-19): implementation c15b94397314b8e84b3ee94877267f8245c3351c passed original local staged/exact-commit gates with 205 tests and the unchanged 120-second limit, was uploaded to main, and was installed as 1.7.0 with prior local work preserved. GitHub run39277812120 has a verified human environment approval but original platform reports are still pending; no hosted pass is claimed. This receipt changes evidence/status only, not source behavior or acceptance.

1.7.1 correction: normalize initializer library roots through the same existing project_root function as the CLI; hosted Windows exposed short-name aliases. Scope checks and the original workflow remain unchanged; 1.7.0 Ubuntu success/Windows failure are historical, and fresh local/exact/hosted checks are required.


## Preserved local 1.7.2 fragments (historical)

These pre-upgrade local fragments retain their original scope and review history. Current authority is the 1.8.0 section selected by the manifest; original bytes and patches are preserved in the installation backup.


### Local fragment 1

# Current factual baseline: BASELINE-ISSUE22-02

Shared installation / hosted receipt (2026-10-20T18:44:37.427693+08:00): both published source and receipt commits passed their original Ubuntu/Windows reports. The shared local checkout now uses d214021 /1.7.2 with canonical runtime/guidance content verified and pre-existing local work preserved in a separate backup. No implementation change or version bump; prior unverified statements remain historical.

1.7.2 source upload receipt (2026-10-20T17:52:35.783179+08:00): implementation 5b8013c9b67debff0b080da563781a39f6e69f74 is verified on origin/main with original local staged/exact-commit gates and tree 7c0c112192ea337ab4515113c4c342375924e497. This receipt changes evidence/status only; current local facts and original limits remain. Hosted CI and global installation are separate.

2026-10-20; input BASELINE-ISSUE22-01 / source `868e4967512c2cd400307368d924291a3d4d8eef`, plus the 1.7.2 Unreleased working-tree guidance changes. The three enhancements are now implemented in the original implementation-workflow, baseline-linked-artifacts and requirements-interview references, with short SKILL/README routes and optional prompts in the original spec-plan-task/impact-analysis templates. Current verification and source hashes are owned by [Task](issue-22-task.md) and [evidence](issue-22-evidence.json); the original local required checks and bounded same-agent manual scenarios have passed there; initial failed checks and environment correction remain in that evidence.

Responsibilities and information flow are reflected in [module map](../docs/module-map.md), [contracts](../docs/contracts.md) and [business flow](../docs/business-flow.md). There is no new CLI/schema/runtime module or product database; the original checker/adoption/source-context/adapters, required checks/timeouts, stage/approval/exception and control policies remain unchanged. Database-view non-applicability was rechecked against docs/database.md and unchanged adapter source. Existing records/formats remain valid; examples do not establish approval or test execution.

The user explicitly instructed “那就按照这个增强的文档去实施” after requesting an interim result and stopping exhaustive reading. This authorizes these local enhancements based on the bounded conclusions; full upstream semantic review remains incomplete and deferred (366 reviewed, 3,177 unread). This baseline covers the local skill changes and does not certify unreviewed upstream behavior, global installation, publication or hosted CI. Earlier approvals and evidence remain tied to their original content.

## Prior factual supplement: BASELINE-ISSUE22-01

当前执行更新（2026-10-20）：最新用户指令要求当前文件读完即先交阶段性结果，全量审读暂缓。当前本地skill事实和1.7.1源码未变；三项增强仍未实施。已读范围及限制见[assessment](issue-22-assessment.md)，原本地完整基线不扩大到未读上游。

Spec review update (2026-10-20): the user accepted the three enhancement directions and explicitly requested a globally scoped Spec while retaining the current workflow. [SPEC-ISSUE22-ENHANCEMENT-01](issue-22-spec.md) is a draft, not implemented behavior or transferred approval. This does not change the source facts or complete the independent upstream semantic review described below.

Plan/Task continuation (2026-10-20): [PLAN-ISSUE22-ENHANCEMENT-01](issue-22-plan.md) binds ten source-based facts B22-01..10 to existing B/M/C/D/F views and Spec requirements; [Task](issue-22-task.md) records the executable T22-01..16 dependencies. No enhancement target is promoted to implemented fact. Source and existing checker/adoption/adapter/source-context dependencies remain unchanged. The five-repository semantic gap stays open; this planning record does not extend the scope of a complete local implementation baseline to unreviewed upstreams.

2026-10-20; source `868e496` / 1.7.1, initially clean worktree. Current task is [TASK-ISSUE-22-REVIEW](issue-22-task.md), with [source assessment](issue-22-assessment.md). The existing implementation baseline below remains bounded to its original revisions and tests; prior adoption/publication approval does not approve Issue 22 enhancements.

Current source already specifies defect reproduction/localization, continuous correction and six-step delivery convergence. The checker verifies declared IDs/references/scopes, lifecycle exceptions and command outcomes; it does not infer behavioral correctness or execute a general code-to-requirements proof. `documents.kind` is a nonempty string, while `workflow_kind=small_fix` preserves a specific existing exception. These facts correct the Issue's absence claims without changing skill behavior.

All five user-selected upstream repositories are pinned and fully inventoried. Whole-file collection/AST inspection and reviewed critical chains are separate from full per-file semantic review, which is still incomplete. This supplement is not acceptance of unreviewed upstream behavior or certification of the 1.7.1 hosted results. No skill/CLI/template/test changes are made in this assessment batch; database, contracts and module dependencies retain their implementation scope.

Execution continuation (2026-10-20): the user explicitly authorized the complete Plan r1 with “开始实现吧”. Its source-review dependencies remain; targets have not become current implementation facts. Authorization does not recertify upstream coverage or hosted results and does not authorize publication. The current Task/manifest carry the actual approval and execution state.

## Prior implementation baseline and approval scope

# Baseline: BASELINE-ADOPTION-LIFECYCLE-02

Current parity correction: original core SKILL sections have been restored unchanged; tooling now supports guidance-first incomplete setup, evidenced greenfield/small-fix exceptions, valid prior-review reuse, shared explicit authorization and complete/approved completion. The earlier finding below is historical; new source passed 205 local tests and original compile gates; exact submission/commit validation and installation rehearsal follow before publication. User has authorized testing, GitHub upload on success and preserving the existing local installation. No external adopted project changes apply.

Historical 23:04 review finding: the first unreleased patch tightened original gates and did not satisfy workflow parity; original 200-test evidence did not establish semantic parity. Preserve that finding in Task/history rather than applying it as the current source conclusion.

2026-10-19; input `BASELINE-SAFE-19-21-01` / source `3c1cb36` plus the current 1.7.0 Unreleased adoption-lifecycle working tree. The original 1.6.4 installer-only entry could succeed without a manifest. Current source now provides complete adoption, a real JSON manifest requirement, explicit additive legacy migration, actual bundled read-only bootstrap diagnostics, and opt-in stage/approval/implementation-path gates. Original defect/recovery observations remain in [Task](adoption-lifecycle-task.md); they do not describe the new implementation as still missing.

Current facts: new scaffolds stay planned/pending and record skill/checker provenance; reruns preserve lifecycle state; atomic migration failure preserves the old manifest. Baseline review, proposal approval and task implementation authorization are separate. Change/handoff/both submit modes classify declared implementation paths, and blocked submit checks do not execute commands. Instructions call the bundled checker for diagnostics, then checker uses existing adapters; no reverse dependency or application database change.

Current coverage: entrypoints, initializer/guidance/checker code, template/schema, tests and linked governance views. All affected current views, release metadata and traceability are synchronized; fresh verification and exact source digests belong to [Task](adoption-lifecycle-task.md). Limits: old manifests remain compatible until explicitly migrated; declarations cannot prove semantic completeness, genuine human review, host loading, dynamic dependencies or missed implementation scopes. This repository's maintenance manifest keeps its prior approval model rather than manufacturing new lifecycle approvals. External adopted projects remain outside scope; updating the existing global skill installation is now explicitly authorized after validation, with all prior local work preserved. Historical reviews retain their original scope.

## Prior baseline revisions and review scope

2026-10-19; input871bda427d3f46d114e568565dac10cca1395920 plus TASK-ISSUES-19-21 working tree. Current implementation binds pre/post Git verification state, handles JSON input limits/root errors and historical corruption, and owns command family/reader cleanup including catchable cancellation. Windows commands are assigned to a kill-on-close Job Object before resume; POSIX uses existing process groups. Prior ASSESS-19-21-01 describes pre-fix facts and remains historical. Current scope and fresh validation: [Task](issues-19-21-task.md), [fix evidence](issues-19-21-fix-evidence.json).

Workflow stages, required command declarations/timeouts, existing exclusions and independent approval controls are unchanged. State checks are stricter after execution; corrupt historical policy and unavailable Windows lifecycle setup fail closed. No business database/adapter change applies. Hostile-code sandboxing, later-hook races, POSIX SIGKILL and Windows pre-assignment hard-kill windows remain limits, not completed features. Current implementation5f9b3e1 is published and its original local/hosted gates are verified; receipt-only updates retain separate validation identities.

## Prior baseline revisions and review scope

# Current baseline: BASELINE-UX-17-18-01

Known-defect supplement ASSESS-19-21-01 (2026-10-19, source871bda4): [assessment](issues-19-21-assessment.md) and [evidence](issues-19-21-evidence.json) confirm commit/committed state checks occur only before declared commands, leaving runtime index/worktree/HEAD drift undetected. File and historical JSON parsing can emit unstructured recursion errors; root-type/large-integer inputs expose related boundaries. Windows controlled interruption leaves descendants/readers alive, and timeout kills only the direct child. The intended consistency/cleanup goals remain unchanged; these are implementation gaps, not relaxed requirements. POSIX native signals and hostile-code sandboxing are not established by the Windows fixtures. Prior source hashes/tests/reviews retain their original limited scope; this assessment does not authorize fixes.

2026-10-19; source base 0216e4cd341bee534ccc85a8824c83a40a7e9840 plus the TASK-ISSUES-17-18 working tree. Current implementation now generates explicit recursive node_modules exclusions in both profiles, surfaces parser reasons/setup diagnostics in relation status/CLI/text, retains partial references, and fails required parser fixture setup early with actionable guidance. Core collection, existing manifests, checker rules and CI gates are unchanged. Current verification/publication evidence belongs to [Task](issues-17-18-task.md) and [fix evidence](issues-17-18-fix-evidence.json); prior 163-test assessment reports are historical. No business database or metadata-adapter change applies.

The user adopted the bounded assessment and requested implementation/upload and issue replies/closure; exact wording is in the Task. This is not a transfer of old baseline reviews, and the program checks still require fresh results. Modules, contracts and flows below are linked current views.

## Prior baseline revisions and assessment evidence

# Current Engineering Workflow Baseline

Current revision: `BASELINE-CONTEXT-06` (2026-10-18), based on source commit `82b3c8531a9a9867dd77756444a2bcbc922aa2c8`; receipt commits change only evidence and linked-view status. Current facts include unchanged engineering stages and checker commands, local collection/JS/TS/Rust module evidence, selectable views, and a corrected protected-CI result contract: diagnostic reruns cannot replace the original required checker outcome. Exact source SHA `3fab75ba5d8e2663af811d2b7daee53c90fe6818` passed the approved Ubuntu/Windows reviewed jobs and aggregate quality run `39115700117`. Exact scope and validation are in [Task](source-context-task.md) and [evidence](source-context-evidence.json). User authorization covers the CI correction and upload; it does not certify target-project business behavior.

Assessment-only supplement (2026-10-19): [ASSESS-17-18-01](issues-17-18-assessment.md) and [source-bound evidence](issues-17-18-evidence.json) verify initializer defaults, explicit exclusion consumers, optional parser statuses and required-test skip handling at remote 1.6.2/0216e4c. The initializer still emits root-only node_modules while the example manifest uses a recursive glob. Missing Rust/JS parsers already have explicit unsupported records; terminal guidance and test setup diagnostics remain usability gaps. Required unittest skips remain partial and cannot satisfy the gate. This factual supplement neither changes implementation nor transfers prior review/implementation approvals; the existing baseline revision/history below remains bounded to its original source.


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


The implementation source 0040878f69450657bb65ee779b6cecda4697049d was published on 2026-10-19; the same source passed fresh 170-test change/commit/committed gates. #17/#18 replies and completed closure are verified. This receipt revises evidence/status only; hosted approval/results remain separate.

Implementation-source hosted receipt: exact source 0040878 passed the original Windows/Ubuntu committed reports in run39151794183 after recorded environment approval. Receipt-only later commits retain separate validation identities.


Published implementation5f9b3e1d54a0709241fb5f11173e13ce00af3ffd passed local184-test staged/exact-commit gates and original Windows/Ubuntu reports in approved run39157028881; source upload and #19/#20/#21 replies/completed closure were verified on 2026-10-19. Receipt-only updates do not change implementation, targets, limits or prior approval scope.

Publication receipt (2026-10-19): implementation c15b94397314b8e84b3ee94877267f8245c3351c passed original local staged/exact-commit gates with 205 tests and the unchanged 120-second limit, was uploaded to main, and was installed as 1.7.0 with prior local work preserved. GitHub run39277812120 has a verified human environment approval but original platform reports are still pending; no hosted pass is claimed. This receipt changes evidence/status only, not source behavior or acceptance.

1.7.1 correction: normalize initializer library roots through the same existing project_root function as the CLI; hosted Windows exposed short-name aliases. Scope checks and the original workflow remain unchanged; 1.7.0 Ubuntu success/Windows failure are historical, and fresh local/exact/hosted checks are required.
