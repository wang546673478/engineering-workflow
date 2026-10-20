# Spec / Plan / Task Record

## Linked artifact revisions

Global Baseline document/revision and source/worktree revision:

Spec document/revision and approval state:

Plan document/revision and approval state:

Task document/ID and current implementation state:

Traceability index and affected Baseline views:

## Global Baseline

Entry path (existing implementation / greenfield; evidence, inherited scaffolding and external constraints):

Greenfield lifecycle (planned → evidenced not_applicable → partial after first implementation → complete/approved before delivery); implementation_paths and reasons:

Current facts versus target modules/contracts/schema (target stays in Plan until implemented):

Current-system scope and source/worktree revision:

Module map, entrypoints, callers and dependencies:

Frontend/backend contracts and permission boundaries:

Database tables/fields, writers/readers, migrations and transaction rules:

Business flows, cache/config/background tasks and runtime evidence:

Known defects, external unknowns, coverage gaps and validity limits:

Baseline review status, user scope acceptance and correction history:

Existing-document reconciliation (authoritative files reviewed, stale/current content corrected, superseded history retained, approval limits and unresolved conflicts):

## Spec

Goal and users:

In scope / out of scope:

Requirements and acceptance IDs:

Optional expression help: [EARS / Given–When–Then examples](../../references/requirements-interview.md#optional-requirement-and-acceptance-examples). Keep existing IDs, source and state; existing formats remain valid. These links locate guidance in this skill; when copying the template, reference the adopted skill's actual source rather than creating project-local copies of its rules.

Current requirement entries (facts / candidates / confirmed decisions / deferred discussion; sources and requirement state using project vocabulary; link existing entries):

Business rules, permissions, data owners, constraints:

Failure, recovery, compatibility, rollout:

Confirmed decisions and interview log:

Deferred items (module/requirement; existing conclusions; remaining questions; effects/dependencies; resumption condition):

Module review when the functional topic concludes (requirements/changes/open or deferred items/related effects; user's statement, date, scope and reviewed version):

## Plan

Baseline revision and Spec revision used:

Milestones and dependency order:

Plan items (stable ID; requirement/acceptance IDs; baseline facts/revision; reuse/new/extend/replace; code entry and target design; migration/compatibility/recovery; verification; affected baseline views):

Affected modules/contracts/tables/flows:

Documentation and verification gates:

Implementation approval record (who/when/scope/what version; requirement confirmation and module review are separate):

## Task: `<ID>`

Linked Baseline / Spec / Plan / Traceability document IDs:

Objective and deliverables:

Current stage and applicability (takeover / baseline review / detailed interview / proposal approval / implementation; or justified minimal workflow):

Baseline paths, source revision, coverage/gaps and validity check:

Investigation coverage and continuation (applicable modules/entrypoints/consumers/tables/fields; source/semantic/runtime evidence; remaining work; concrete blockers and independent next actions):

Environment preparation (available tooling; necessary local installs/isolated data and ports; versions; migrations/tests/results; cleanup or retained-environment recovery; limits of existing authority):

Inventory capability review (provenance/scope versus supported adapter; achievable required gates; existing gate conflicts and concrete reviewable proposals; partial remains partial):

Stage transition evidence (user statement, date, scope, reviewed version; baseline confirmation is separate from proposal approval):

Baseline correction history (discovery trigger, old/new claim, source/worktree revision, confirming evidence, affected views/dependencies, current status; preserved historical review and affected approvals needing review):

Next action allowed in this stage:

Prerequisites and parallel work:

Executable steps (ID, Plan item, requirement/acceptance IDs, dependency, owner, status, affected baseline views, actual evidence; planned design is not implemented fact):

Required reading:

Skill review:
- Catalog/registry source and scope:
- Checked at (timestamp/timezone):
- Scope keywords and deliverables searched:
- Candidates (repeat per candidate): name/ID; source path or URI; version/release date (or `not provided`); decision (`adopted | not-adopted | unavailable`); fit/conflict or unavailability reason; evidence read:
- Recheck trigger/result after scope or catalog changes:

Implementation owner and old-path replacement:

Impact analysis:

If this is a defect, optionally link existing symptom/reproduction, cause evidence versus hypotheses, fix/preserved behavior and before/after checks; use the [existing-task evidence prompts](../../references/implementation-workflow.md#defect-evidence-within-the-existing-task) as needed, without a separate required document or fixed form.

Acceptance scenarios and exact checks:

Within the existing [delivery convergence](../../references/baseline-linked-artifacts.md#交付前收敛), record any in-scope missing/partial/conflicting behavior, changes without an established basis or stale/unverified evidence and its authoritative destination. Keep future/deferred scope separate; no additional report or approval is required.

Release impact (policy/source; bump required or exemption and reason; old/target version; PATCH/MINOR/MAJOR or project equivalent; affected packages and synchronization paths; CHANGELOG/equivalent notes; Unreleased/published status; checks and publication evidence):

Current requirement state / implementation state and evidence (use project vocabulary; neither recording nor confirmation authorizes implementation):

Current open/deferred items and next action (refresh when decisions change; retain superseded history separately):

Handoff/remaining risk:
