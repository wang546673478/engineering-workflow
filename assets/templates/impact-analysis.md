# Impact Analysis

Change: `<title>`  
Requirements/acceptance: `<IDs>`  
Status: `draft | reviewed | complete`

## Skill review

Catalog/registry source and scope: `<host Skills catalog, plugin registry, project inventory, or unavailable>`  
Checked at: `<timestamp and timezone>`  
Scope keywords/deliverables searched: `<...>`

| Candidate skill (name/ID) | Source path or URI | Version/release date | Decision | Fit, conflict, or unavailability reason | Evidence read |
| --- | --- | --- | --- | --- | --- |
| `<...>` | `<...>` | `<... or not provided>` | `adopted | not-adopted | unavailable` | `<...>` | `<SKILL.md or linked resource>` |

Recheck trigger and result: `<scope/catalog change, or none>`

## Existing implementation

Responsible module and current entrypoint:

Existing callers/consumers and reusable behavior:

## Impact map

- Frontend pages/components:
- Backend routes/types/services:
- Module connections (callers, dependents, dependency direction, events/consumers):
- Tables/fields/migrations:
- Events/jobs/cache/config:
- Permissions/data scopes:
- External integrations and compatibility:
- Financial, audit, security, and performance effects:

## Failure and recovery

Validation, timeout, retry, duplicate request, partial failure, rollback, and recovery behavior:

If this is a defect, optionally reference existing reproduction/environment/revision, cause evidence or hypotheses, fix scope and preserved behavior, before/after results and remaining verification limits. Use the skill's [defect evidence prompts](../../references/implementation-workflow.md#defect-evidence-within-the-existing-task) as applicable; no separate BUG file or completed form is required. When copying this template, point to the adopted skill's actual source for guidance.

## Plan

Implementation owner and dependency direction:

Old path replacement/deprecation:

Documents and tests to update:

Documentation gate decision:
- Module/call-chain connectivity: `required | not-applicable` (reason/evidence):
- Frontend/backend contract: `required | not-applicable` (reason/evidence):
- Database dictionary and schema inventory: `required | not-applicable` (reason/evidence):
- Business flow: `required | not-applicable` (reason/evidence):
- Post-change checker command and result:

## Review evidence

Searches/commands performed:

Open questions and defaults:
