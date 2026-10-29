# Baseline Layout Assessment / BASELINE-LAYOUT-01

Status: complete assessment; implementation is recorded in the linked Task. No external project files were changed.

## Trigger and user direction

On 2026-10-30 (Asia/Shanghai), the user confirmed the direction to separate current baseline facts from historical baseline changes and stated that the existing workflow must not change. The direct examples are the Liantong frontend and database baseline documents, which mix current corrections, historical snapshots, target design, and evidence notes.

## Verified current behavior

- The generic skill defines one Global Baseline with queryable views for module map, frontend/backend contract, database dictionary, and business flow. Configuration, cache, jobs, verified behavior, defects, and unknowns are baseline content, not separate default baseline types.
- `scripts/init_manifest.py` registers `BASELINE`, `MAP`, `DB`, `CONTRACT`, and `FLOW` in the manifest. It writes a manifest skeleton and does not create or populate the linked Markdown documents.
- `adopt_project.py` maps existing documents and installs the stable project entry; it does not semantically migrate existing baseline prose.
- The current rules require preserving superseded conclusions and correction evidence, but do not define a physical current/history document layout.

## Problem and impact

The mixed layout makes routine current-state reads expensive and makes target statements look like facts. It also causes large domain files to carry both current summaries and old snapshots. A layout-only correction is insufficient if exhaustive route/field/source inventories remain duplicated inside the current factual summary.

## Options

1. **Per-view current plus history sibling (recommended):** preserve each existing current path, add a history sibling, and identify the roles in the manifest. This keeps links stable and lets an agent load only the affected history.
2. **One project-wide history file:** fewer files, but unrelated frontend, database, and contract changes become one long history stream.
3. **Rename every existing file to `*-current`:** explicit names, but it breaks existing links and creates an unnecessary migration burden.

## Proposed boundary

The current file is the sole authority for the latest factual view. Its header binds an as-of revision, scope, source, evidence boundary, and limitations. The history sibling is non-authoritative and records old/new claims, trigger, evidence, source/worktree revisions, affected approvals and supersession links. Target requirements and technical choices remain in Spec/Plan/Task. Exhaustive inventories and machine receipts remain evidence attachments referenced by the current view.

Existing projects retain their current paths and receive history files through a one-time, agent-guided workflow upgrade. The agent reads the project prompt and authoritative records, classifies current/history/target/evidence content, records the migration in the Task, and updates the documents. No helper repeatedly inspects content or generates a report on every adoption run.

## Guardrails

The existing stages, baseline review, module review, proposal approval, implementation authorization, required checks, commands, timeouts, coverage, checker policy, and delivery gates remain unchanged. Existing manifests remain readable. No external project is migrated in this planning batch.

## Resolved implementation decisions

- New-project initialization creates empty history files immediately, with an explicit no-history-yet marker.
- Existing-project migration is a one-time agent task before normal work resumes; there is no diagnostic-first/strict mode pair.
- `adopt_project.py` keeps its current manifest/guidance/bootstrap responsibilities and does not inspect or migrate baseline prose.
