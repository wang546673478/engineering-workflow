# SPEC-BASELINE-LAYOUT-01 r1

Status: approved for implementation on 2026-10-30 (Asia/Shanghai) by the user's direct “可以的” decision, with workflow preservation as a binding constraint.

## Goal

Separate current factual baseline views from their historical corrections while preserving the existing engineering workflow and keeping routine model reads small.

## Requirements

- **REQ-BL-01 Current authority:** Each declared baseline view has one current factual authority. The current view contains only the latest effective facts, scope, source/worktree revision, evidence boundary, limitations, and links.
- **REQ-BL-02 History authority boundary:** Each migrated view may have a history sibling that is explicitly non-authoritative. A history entry records the old claim, new claim, trigger, evidence, source/worktree revisions, affected scope, affected approvals, superseded relation, and current follow-up.
- **REQ-BL-03 View coverage:** The model applies to Global Baseline, Module Map, Frontend/Backend Contract, Database Dictionary, and Business Flow. Project-specific views such as Billing may opt in using the same role model.
- **REQ-BL-04 Evidence separation:** Exhaustive inventories, generated indexes, runtime receipts, and test logs remain evidence attachments. The current baseline links to them instead of copying their full enumerations.
- **REQ-BL-05 Target separation:** Future behavior, candidate decisions, confirmed requirements, and technical design remain in Spec, Plan, and Task. They must not be presented as current baseline facts or historical facts.
- **REQ-BL-06 Manifest compatibility:** `workflow.active_baseline` continues to identify the current Global Baseline. Existing `baseline.document_ids`, document IDs, paths, and manifests remain valid. New optional metadata can identify current/history roles and history siblings without changing old meanings.
- **REQ-BL-07 Adoption compatibility:** Existing projects keep their current paths as current views and add history mappings incrementally. The skill does not automatically rewrite or semantically classify external project documents.
- **REQ-BL-08 Workflow preservation:** Existing stages, user review meanings, approvals, implementation authorization, required checks, commands, timeouts, coverage, checker/CI policy, and delivery gates do not change.
- **REQ-BL-09 Review binding:** Historical review and approval remain bound to their original source revision, scope, and evidence. Splitting files must not transfer an old approval to corrected content silently.
- **REQ-BL-10 New-project bootstrap:** New-project initialization creates the current and history document pair for each default baseline view. An empty history file contains an explicit no-history-yet marker and is not treated as evidence of a historical review.
- **REQ-BL-11 Agent-guided upgrade:** Existing-project separation is a one-time workflow-upgrade task performed by the agent from the skill guidance. It records classification, moved sections, unresolved items, evidence, and the resulting current/history paths in the existing Task and linked documents.
- **REQ-BL-12 Adoption boundary:** `adopt_project.py` keeps its existing manifest, AGENTS guidance, and bootstrap responsibilities. It does not inspect baseline prose, run a recurring history-layout diagnostic, or enable a new strict mode.

## Acceptance

- **AT-BL-01:** New guidance defines current/history roles and the required history entry fields.
- **AT-BL-02:** New or upgraded manifests can link current and history views while old manifests remain readable and preserve existing `active_baseline` semantics.
- **AT-BL-03:** The adoption path provides a read-only or explicitly mapped migration route; no semantic content move occurs implicitly.
- **AT-BL-04:** Documentation explains that evidence/inventory is separate from current baseline prose and target design.
- **AT-BL-05:** Existing workflow stages, approval contracts, required check declarations, commands, timeouts, coverage, and CI policy are unchanged byte-for-byte unless a later approved plan identifies a necessary additive field.
- **AT-BL-06:** A new-project scaffold contains empty current/history view files with the no-history-yet marker and remains in its existing planned/takeover stage.
- **AT-BL-07:** An existing project can complete a one-time agent-guided separation with classification and evidence recorded in the existing Task; later adoption runs do not repeat the migration automatically.
- **AT-BL-08:** `adopt_project.py` retains its current behavior and does not add baseline-content inspection, recurring diagnostics, strict layout gates, or implicit content writes.

## Scope boundaries

In scope: `SKILL.md`, baseline and project-documentation references, adoption/manifest support, optional checker diagnostics, templates, tests, README, version/changelog, and linked governance records.

Out of scope: automatic migration of Liantong or any other external project, product source changes, changing workflow stages or approvals, changing required checks, changing CI policy, and changing the meaning of existing baseline approvals.
