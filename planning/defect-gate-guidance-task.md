# TASK-DEFECT-GATE-GUIDANCE-01

## Current status

- Stage: implementation checks complete; GitHub publication is authorized and exact-tree protected gates are pending human review of the candidate diff.
- Active chain: [Baseline](baseline-review.md) → [Assessment](defect-gate-guidance-assessment.md) → [Spec r1](defect-gate-guidance-spec.md) → [Plan r2 publication extension](defect-gate-guidance-plan.md) → this Task → code/evidence.
- User authorization on 2026-11-03: “按照这个现状和得出的结论开始改吧”. Scope is the two conclusions from the conversation review: cause-directed defect fixes with an explicit mitigation exception, and task-scoped required checks that retain project-wide mandates and exact-tree evidence.
- No checker/CI implementation, check-definition, external-project, deployment, tag or Release change is authorized.

## Publication authorization and target

- User statement: “上传到github吧” on 2026-11-03 (Asia/Shanghai). This separately authorizes publication of the completed 1.16.0 candidate; it does not replace the protected-path human review or exact-tree gates.
- Target: `origin/main`, using a normal fast-forward. Basis: the current checkout is at the `origin/main` tracking SHA `af4a8456acfa95eeb808d2e17510d4c52a91afa0`, and this repository's immediately preceding publication scope selected `origin/main`. No force push, tag, Release, deployment or external-project change.
- Status: authorized; exact staged diff is being prepared. `SKILL.md`, `VERSION`, `CHANGELOG.md` and `engineering-manifest.json` are protected. Do not pass `ENGINEERING_CONTROL_PLANE_APPROVED=1` until the human reviewer has inspected this exact candidate.

## Skill review

Checked 2026-11-03 (Asia/Shanghai) against the current session Skills catalog, repository `AGENTS.md`, manifest, and applicable references. Adopt repository `engineering-workflow` 1.15.0 as the governing skill and system `skill-creator` (`C:/Users/54667/.codex/skills/.system/skill-creator/SKILL.md`, visible version not provided) because this task updates an existing skill. Do not adopt TDD: no executable feature or checker behavior is added; the existing guidance test suite will verify documented invariants. Do not adopt planning-with-files because this repository's manifest-linked artifacts are authoritative. Recheck if the task expands to checker code, CI, external migration, or publication.

## Requirements and acceptance

REQ-DGF-01..04 and AT-DGF-01..05 are defined in [Spec r1](defect-gate-guidance-spec.md). The scope is a focused guidance improvement; no new workflow stage or approval round is introduced.

## Impact and release

- Modules: instructions, tests, and governance.
- Expected paths: `SKILL.md`, `references/implementation-workflow.md`, `README.md`, `agents/openai.yaml`, `VERSION`, `CHANGELOG.md`, `scripts/tests/test_guidance.py`, manifest-linked planning records, baseline, impact, and traceability.
- Required checks: retain the repository's existing TEST, COMPILE, and GUIDANCE-COMPILE definitions unchanged.
- Release: 1.15.0 → 1.16.0 / Unreleased for backward-compatible workflow capability additions.

## Execution and evidence

| Step | Status | Evidence / next action |
| --- | --- | --- |
| DGF-00 | complete | Reviewed the actual skill rules and the user's read-only session evidence; kept application-specific details out of generic guidance. |
| DGF-01 | complete | Recorded scope, user authorization, requirements, acceptance, and skill review. |
| DGF-02 | complete | `SKILL.md` and implementation reference default to complete correction of confirmed causes; mitigation records rationale, residual/masking risk, revisit owner/trigger and validation. |
| DGF-03 | complete | Task impact selects applicable checks; project-wide mandatory checks, failed-gate integrity and exact-tree receipt verification remain explicit. |
| DGF-04 | complete | Added focused defect/check-scope guidance tests; synchronized README, 1.16.0 metadata, Baseline, skill review, impact and traceability. |
| DGF-05 | complete | Local unchanged required checks passed: TEST 292/203.876s, COMPILE and GUIDANCE-COMPILE; skill quick validator and independent semantic review passed. The initial TEST attempt failed before preparing the pinned TypeScript runtime; see verification record below. |
| DGF-06 | in progress | Publication to `origin/main` is authorized. Stage and present the exact diff for protected-path human review, then run original exact-tree `commit`/`committed` gates, commit, fast-forward push and verify remote SHA. |

## Environment and verification

- Environment: Python 3.14.7; Node.js v24.21.0 and npm 11.13.0. `scripts/context-runtime/package-lock.json` pins TypeScript 6.0.3; after the first test diagnosed it missing, `npm ci --ignore-scripts --prefix scripts/context-runtime` prepared the ignored local `node_modules` directory. PyYAML 6.0.3 was installed only under ignored `work/validation-deps` for the skill validator.
- Focused tests: `python -m unittest scripts.tests.test_guidance -q` passed (15 tests); after installing TypeScript, the combined guidance/source-relation/Windows-path regression set passed (33 tests).
- TEST: the first `python -m unittest discover -s scripts/tests -q` attempt ran 276 tests but failed because the JS/TS parser was unavailable; two relation-path assertions consequently had no evidence, and the relation suite could not initialize. After preparing the lockfile-pinned runtime, the unchanged command passed: 292 tests in 203.876s.
- COMPILE: `python -m py_compile scripts/check_project.py scripts/extract_database.py scripts/extract_sqlite.py` passed.
- GUIDANCE-COMPILE: `python -m py_compile scripts/install_agents_guidance.py scripts/init_manifest.py scripts/adopt_project.py` passed.
- Skill validation: skill-creator `quick_validate.py .` passed with UTF-8 enabled and the task-local PyYAML path (`Skill is valid!`).
- Integrity: all required manifest document paths exist; `git diff --check` passed. Independent semantic review found no remaining ambiguity in the distinction between an invariant-restoring guard and symptom-only mitigation.
- Scope boundary: local implementation checks above passed before the publication-record update. No staged/committed exact-tree gate, commit or push has run yet; those are pending the required human review and will use the existing protected-path rules. No deployment or Release is authorized.

## Completion rule

Complete only after the guidance and records agree, the required checks pass, and any protected-path review requirement is reported accurately. Do not stage, commit, push, publish, or claim a protected control-plane gate passed without its required human review.
