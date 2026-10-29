# TASK-BASELINE-LAYOUT-01

## Current status

- Stage: implementation; approved Spec/Plan are being applied.
- User direction on 2026-10-30 (Asia/Shanghai): “可以的,然后不能改变现在的流程”. The accepted direction is current/history separation with workflow preservation. Implementation is authorized. Follow-up decisions: new projects create empty history files at baseline initialization; existing projects use a one-time agent-guided upgrade; `adopt_project.py` keeps its current responsibilities and does not run recurring baseline-content checks.
- Publication direction on 2026-10-30 (Asia/Shanghai): “上传到github”. This authorizes committing and pushing this repository's reviewed batch to `origin/main` after the unchanged commit/committed gates; no tag, GitHub Release, merge, or external project migration is included.
- Active task boundary: the manifest now selects `TASK-BASELINE-LAYOUT-01`; the prior verification-closure task remains preserved with its original scope and records.
- Scope: this skill repository's guidance, templates, one-time upgrade procedure, linked governance records, and publication of this reviewed repository batch. No adoption-script, checker, recurring diagnostic, tag/Release/merge, or external project migration change in this batch.

## Skill review

Rechecked on 2026-10-30 (Asia/Shanghai) against the current session Skills catalog, repository `AGENTS.md`, manifest, and applicable references. Adopt `engineering-workflow` from this repository (input 1.13.0) because it governs the change; adopt system `skill-creator` because the deliverable updates an existing skill; do not adopt `tdd` because the revised scope is guidance/templates/governance plus publication and preserves executable behavior; do not adopt `planning-with-files` because this repository's manifest-linked records are authoritative. The user later authorized publication of this repository to `origin/main`; no additional skill is required for the Git operation.

## Requirements and acceptance

Requirements REQ-BL-01..12 and acceptance AT-BL-01..08 are defined in [Spec r1](baseline-layout-spec.md). They preserve the current workflow and make current/history separation explicit without turning migration into a recurring gate.

## Impact

- Modules: instructions, governance, adoption/manifest compatibility, optional diagnostics, templates and tests.
- Expected paths: `SKILL.md`, `references/project-documentation.md`, `references/baseline-linked-artifacts.md`, `references/adoption-lifecycle.md`, applicable baseline/history templates, README, version/changelog, manifest, baseline, impact, skill review and traceability records.
- No product code, external baseline migration, workflow stage, approval meaning, required command, timeout, coverage, checker/CI policy or delivery-gate change.
- Candidate release impact: additive backward-compatible guidance, 1.13.0 → 1.14.0 / Unreleased for this implementation batch.
- Publication impact: commit and push this repository's reviewed batch to `origin/main` after the existing protected commit/committed gates; no tag, Release, merge, or external project change.

## Execution and evidence

| Step | Status | Evidence / next action |
| --- | --- | --- |
| BL-00 | complete | Read-only audit confirmed the generic skill has one Global Baseline with five default linked views and no physical history layout. |
| BL-01 | complete | User accepted the current/history direction and required workflow preservation. |
| BL-02 | complete | Candidate Assessment, Spec r1 and Plan r1 are written for review. |
| BL-02a | complete | User selected empty history files for new projects, one-time agent-guided upgrade for existing projects, and preservation of `adopt_project.py`'s current responsibilities. |
| BL-03 | complete | User approved the complete Spec/Plan and the workflow-preservation constraint. |
| BL-04 | complete | Implemented additive current/history guidance and templates; `adopt_project.py` and checker behavior remain unchanged. |
| BL-05 | complete | Prepared the pinned TypeScript runtime with `npm ci --ignore-scripts --prefix scripts/context-runtime`; the unchanged required TEST, COMPILE and GUIDANCE-COMPILE now pass. |
| BL-06 | in progress | Record the user's publication authorization, run protected commit/committed checks, commit the reviewed tree and push it to `origin/main`; then record the exact SHA and remote verification. |

## Verification

- Earlier checker runs before local parser setup are retained as historical evidence: manifest, COMPILE and GUIDANCE-COMPILE passed, while TEST failed because the parser runtime was unavailable.
- `python -m unittest scripts.tests.test_guidance scripts.tests.test_adoption scripts.tests.test_init -q`: 29 tests passed in 17.213s.
- The focused parser/path rerun passed 18 tests in 1.814s, including both Windows path cases and the source-relations fixture.
- After local runtime setup, direct full TEST passed: 286 tests in 173.878s.
- Final checker after local runtime setup passed with `required_checks_satisfied: true`: TEST 170.727s, COMPILE 0.316s and GUIDANCE-COMPILE 0.313s.
- `python -m json.tool` for the manifest and template: passed. `git diff --check`: passed.
- Publication verification is pending the protected commit/committed gates and remote SHA check.

## Completion rule

The guidance/template implementation and local required verification are complete. Publication is limited to this repository's reviewed batch; no external project is migrated, tagged, released, or merged. Preserve all historical approvals and source revisions.
