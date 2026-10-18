# Engineering Workflow Maintenance Flow

Status: `current`; the manifest's active task owns current implementation and review status.

## Checker path and documentation flow

1. The checker reads manifest paths and normalizes `/` and `\\` separators at the safety boundary; foreign drive/UNC paths on POSIX, root escapes and link traversal fail before validation continues.
2. Baseline validation resolves literal documents and modules. Exclusion globs are validated as project-relative segment patterns, and matching directory subtrees are pruned before child links are inspected.
3. Change/commit validation compares Git paths against literal module/document coverage. Excluded paths are reported separately and are not coverage. A `when_paths` common parent shared by source scopes from at least two selected modules triggers all configured documentation updates, but does not make unrelated descendants covered.
4. The checker validates command arguments before execution, bounds declared check output, and emits a JSON report whose `tool_version` comes from `VERSION`. Commit/committed modes run declared tests only after submitted-tree gates pass; other modes retain their declared-command behavior, with failures visible in the report.
5. A command that emits beyond its output limit is terminated and recorded as a failed check with byte-count/hash evidence. `VERSION` and `CHANGELOG.md` changes enter the protected control-plane review path.
6. New manifests expose active Baseline/Spec/Plan/Task pointers and tasks may link their artifact documents; the checker validates those declared references without claiming semantic approval.

## Greenfield and documentation reconciliation flow

1. Inspect repository/inherited scaffolding, external constraints and rules. Existing implementation without docs follows discovery; a genuinely empty project explicitly selects greenfield initialization. The skeleton stays planned and creates no source/documents/approval.
2. Record evidenced no-implementation scope and constraints, then interview and plan. Set not_applicable only after inspection; target module/API/schema designs remain in Plan. Declared files invalidate that state regardless of exclusions.
3. Approved implementation creates partial factual views incrementally. Normal task approvals, tests, documentation-impact and control-plane protections remain active. A provisional lifecycle pass reports completion_ready=false.
4. Reconcile actual source/evidence and affected views into a complete factual baseline before completing the selected Task or handoff. Future unimplemented requirements remain in Spec/Plan/Task, outside the delivered slice.
5. Workflow updates trigger comparison of current authority, summaries, revisions and links. Correct evidenced errors, retain superseded plans/original approvals and refresh Spec/Plan/Task only within their change rules. The current Task records the reconciliation scope and limitations; external projects are not auto-migrated.

## Persistent project adoption and recovery

1. The project chooses to adopt engineering-workflow. The agent reads existing project rules and selects the project's existing manifest, task and state locations.
2. Merge the managed block into repository-root `AGENTS.md`, preserving rules outside its markers. The installer can repeat this update. Record the skill source/revision and canonical state locations in project files.
3. For a project's selected agent, add a thin reference from its native instruction entry to `AGENTS.md` only when needed. Check the host's loading behavior; do not assume that every agent discovers every filename.
4. At task start, resume, handoff, incomplete context, agent change or scope change, reload project rules, the adopted skill source/revision, manifest, active Baseline/Spec/Plan/Task pointers (with `workflow.active_task` unless an explicit task ID is supplied), and recent progress/handoff before editing. Reconcile those records with the working tree; scope changes refresh skill review and impact analysis.
5. Keep plans, decisions, impact, progress, verification and handoff in the project's authoritative files. `AGENTS.md` remains the stable entry, rather than accumulating every task's history.
6. Review and verify the concrete adoption change. New protected-rule changes require their own final approval; a past task's approval cannot be reused. Missing skill access or unverified host integration is recorded explicitly.
7. CI consumes the manifest's active task pointer instead of copying a historical task ID into workflow files. Changing the active task is a governed manifest/state change and must be reviewed with its documentation impact.

## Hosted protected review

1. A pull request runs ordinary checks without approval variables or protected environment values.
2. If a control-plane path changes, CODEOWNERS and branch protection require maintainer review. A submitted approval triggers the workflow again only when its `commit_id` equals the current PR head.
3. The reviewed job enters the fixed `engineering-control-review` environment, checks out that exact commit, and runs the committed checker on Ubuntu and Windows. The environment value is never exposed to ordinary or fork jobs.
4. The reviewed job is limited to same-repository PR heads; fork PRs never receive the environment value. The aggregate `quality` result is the branch-protection target. Review records, environment approval and checker reports form the audit trail. Pushes to `main` provide final verification; `workflow_dispatch` remains a manual fallback.
5. If a reviewed checker report proves all rule/scope gates pass and only TEST fails, the workflow prints verbose fixture-test diagnostics. A passing rerun recovers a transient TEST failure; rule or scope failures remain failures.

Historical adoption, installer verification and publication are recorded in [TASK-PERSISTENCE-01](../planning/persistence-task.md). Current work follows the manifest's active task; AGENTS.md points to that stable selector rather than maintaining a second current-task link.

## Skill change path

1. Maintainer identifies a workflow, checker, adapter, documentation, or release change.
2. Applicable skills are reviewed and recorded in the active task `skill_review`.
3. The module map and impact record identify affected modules, contracts, database boundaries, and tests.
4. Code and the corresponding documentation are staged together.
5. Tests, compilation and independent skill structure validation produce a concrete result for human review. Explain the result and any choices in plain language.
6. The `commit` gate checks the index. Protected-rule edits remain blocked until the user reviews those edits; approval to implement is not approval of the finished rules. Exercise the approval path only in disposable test fixtures while review is pending.
7. After the reviewed change is committed, use `committed` locally or in the project's chosen CI. GitHub and GitHub Actions are optional for users of the skill; this repository opts in to Actions.

## Failure and recovery

| Trigger | Expected behavior | Recovery |
| --- | --- | --- |
| Missing manifest or baseline evidence | Baseline fails | Restore the missing control document and rerun baseline |
| Code change without declared documentation impact | Commit gate fails | Add the canonical gate and update the affected documents |
| Protected rule changed without human approval | Protected-rule gate fails | Show the exact change and its effect to the reviewer; after approval supply the short-lived external acknowledgement |
| Shallow or incomplete Git history | Submission check cannot establish prior rules; commands are not run | Obtain the missing history and rerun the check |
| Required test fails or is skipped | Handoff remains incomplete | Fix the failure or document a user-approved scope change |
| Remote adapter lacks driver/credentials | Adapter reports unsupported | Install the optional driver or use an offline snapshot |
| Managed guidance markers are malformed or a target leaves the project root | Installer rejects the target | Correct the selected target or conflicting block; preserve project-authored rules |
| Native instruction entry is not loaded by the selected host | Automatic persistence is unverified | Use the host's supported project-rule entry and verify that it follows the canonical file |
| Skill or task state cannot be read after resumption | Missing context remains explicit | Record the missing source and recover the authoritative project files before dependent work |

## Ownership

The repository maintainer owns semantic review. The installer owns only the marked guidance blocks and thin references. Project task files own current state. The checker owns mechanical evidence. The skill-creator validator owns skill package structure. The user performs final review before any push or release.

This repository's ordinary Actions path runs the submission gate before declared project checks. Protected-rule updates use a separate manual run for an exact reviewed SHA, after the repository owner configures a protected environment and required reviewers. The earlier setup and publication evidence is recorded in [the historical impact record](../planning/change-impact.md); that evidence does not verify this working tree or approve this task. Other projects can keep the entire review and verification flow local.

## First-takeover stage flow

Project rules and skill review → global discovery → reviewable current-system Baseline → user Baseline confirmation → detailed feature interview → Spec/Plan/Task proposal approval → implementation, Baseline refresh and verification. Basic goal clarification returns to discovery. Restore stage evidence on resumption; apply the small-fix, valid-baseline and no-existing-code exceptions from SKILL.md. This is an agent instruction, not an automated checker state machine.

## Continuous feature discussion flow

1. Restore the active task and latest authoritative requirements. In an adopted project, interpret follow-up answers within that task even when the user does not name the skill again. Source facts without new change information reuse existing records.
2. Identify feature changes and update the same requirement/decision record during discussion. Distinguish facts, candidates, confirmations and deferrals; refresh the current summary, phase, next action and dependencies rather than only appending history. Keep requirement and implementation states separate.
3. Preserve each deferred topic's module, existing conclusion, question, impact/dependencies and resumption condition. Before dependent design or implementation, reopen the relevant topic; an unresolved high-impact dependency remains subject to existing readiness rules.
4. Briefly tell the user where material updates were saved and what remains open, then continue with the next material question. Report write failures accurately. This ongoing recording does not require a new per-turn approval or concentrated review gate.
5. When the module discussion converges, consolidate its requirements, recent changes, open/deferred topics and connected impacts. Present that concrete result for user review and record the user's wording, scope and document version. Adjust the module if needed; later changes reopen only affected parts.
6. Carry reviewed requirements into the complete implementation proposal under the existing approval rules. Module requirement review does not replace first-takeover baseline confirmation or authorize implementation by itself. Continue implementation and documentation verification only within the approved scope.

The agent owns recording and state recovery; the user owns semantic module review. The checker verifies supplied files and mechanical evidence without reading conversation messages. These instructions do not provide a host execution hook or guarantee compliance. Current changes and scenario evidence belong to [TASK-CONTINUITY-01](../planning/continuous-requirements-task.md).

The 1.4.3 source push completed on 2026-10-16. Its date and verification receipt follow the publication flow below without altering feature-discussion behavior or consuming another version.

## Version and changelog delivery flow

Project policy and batch diff → release-impact classification and version source → target version and synchronization of actual consumers → Unreleased change notes → version/content/status verification → authorized delivery/publication → actual publication date and evidence. Evidence-only receipts can document a no-bump decision without restarting this cycle. Existing project conventions and package release boundaries remain authoritative; checker protection of metadata is distinct from deciding that a release is appropriate.

The 1.4.2 batch has reached source publication on 2026-10-15. Its follow-up records the actual date and check/push evidence without changing behavior or bumping the version again.

## Autonomous discovery and continuous baseline correction

Authorized scoped discovery → source/semantic investigation → necessary local isolated environment and validation → update current coverage/evidence → continue remaining actionable investigation → reviewable baseline or concrete unresolved blocker. A progress report does not reset authorization. User review accepts the actual revision, scope, findings and limits; product implementation keeps its separate approval boundary.

Before creating required inventory gates, compare provenance/scope with supported adapters. The corrected example matches the existing full initializer's optional source inventories while requiring applicable documentary and semantic coverage. Existing required/manual conflicts remain unsatisfied until a concrete project-governed resolution; repeating successful tests cannot resolve that conflict.

Later test/runtime/source finding → flag disputed claims → reconcile source and confirmed requirements → correct current Baseline module/contract/dictionary/flow/inventory views → propagate affected Plan/Task impacts → preserve old/new evidence and revision → revalidate affected conclusions. If an approved premise changes, notify and reopen only its affected review, pausing dependent implementation while valid independent work proceeds. No product-code edit is necessary to trigger this flow. Current batch: [TASK-LINKED-ARTIFACTS-01](../planning/linked-artifact-model-task.md). The publication receipt follows the delivery flow above and changes no investigation/correction behavior.

1.5.0 publication: commit/committed checks passed, source commit `46d57a6cefd5cc80ae62e47099b782d4cb381504` was pushed to origin/main on 2026-10-18 and the remote SHA matched. Date/status receipts follow the same gates; hosted CI results remain separate from source upload.


## Local source helper flow

Task goal → inventory/direct search → full selected reading → optional syntax/config references → evidence checks → summary or requested table/diagram → existing semantic baseline/impact verification. First onboarding and cross-boundary uncertainty trigger suitable scope; small isolated edits may skip analysis. Discovery may be reused within one execution, not persisted as a stale cache. Existing review/plan/implementation gates remain. [Guide](../references/source-context.md) and [Task](../planning/source-context-task.md).


1.6.0 source publication: `502fd69a16ffcd0a32dc0acbffb32bf8ccf1109b`, verified on origin/main on 2026-10-18. This receipt does not change implementation/approval scope; exact local gates are in [the current Task](../planning/source-context-task.md). Hosted CI is tracked separately.


### Windows Python3.11 correction (1.6.1)

The collector additionally checks lstat reparse attributes before scanning links and source/output ancestors; it does not depend on Path.is_junction being available. The permission-error fixture uses a canonical target to cover Windows short-path aliases. Existing checker source, workflow semantics/CI and required commands/timeouts stay unchanged. SPEC-CONTEXT-03/REQ-CONTEXT-01..05 remain applicable; current execution/evidence are in [Task](../planning/source-context-task.md). BASELINE-CONTEXT-04/PLAN-CONTEXT-04 cover this correction; 1.6.0 validation remains historical.
