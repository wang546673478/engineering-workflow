# Defect Repair and Task-Scoped Verification Assessment / 2026-11-03

Status: local implementation authorized by the user's direct request, “按照这个现状和得出的结论开始改吧”.

## Evidence and scope

This assessment reviews the repository's 1.15.0 `SKILL.md`, its defect evidence and verification guidance, the checker reference, and the user's read-only review of the Codex conversation titled “整体优化” (thread `01a196d6-4cb6-7680-83c0-dabe6c955d4f`). That conversation showed two different outcomes: an earlier sidebar issue was traced to a permission-branch overlap and regression-tested; a later chart error initially received a proposed formatter guard, then was traced after user correction to a mismatch between a numeric axis label and a tooltip series label. The latter turn was still active during review, so no final production outcome is claimed here.

The production-release turn reviewed in that conversation lasted about 99m56s and invoked the checker 10 times: four quick preflight failures, one full run that failed when Go/PostgreSQL tools were unavailable, and five passing full runs of about 12 minutes each. The work also included a verified backup, a large build upload, a Docker-builder compatibility retry, deployment checks, and receipt updates. These observations show repeated work, but do not attribute all elapsed time to gates or establish that project-wide checks may be removed.

## Findings

The defect guidance asks for a confirmed cause and a cause-related scope, but it does not directly require the proposed change to remove that cause. As a result, an agent can offer symptom containment before proving that the cause is unknown, upstream, or out of scope. The rule should default to the smallest complete correction at the responsible layer. A symptom-only measure should be named as mitigation and carry its reason, residual risk, possible masking, and revisit condition.

The verification guidance preserves required checks and exact-tree evidence, but task-wide check sets can be copied from a broad feature into an independent small follow-up or a receipt-only update. This can run unrelated long suites without improving confidence in the changed behavior. Check selection should be defined for the actual Task impact before its gate runs. Explicit project-wide checks remain mandatory, and a failed check must not be removed after the fact. Exact-tree reports remain bound to the tree they verified; documentation receipts need their own applicable checks or approved artifact location when project policy permits.

## Decision

Update generic guidance and focused guidance tests only. Do not change checker code/schema, CI, project required-check definitions, approval semantics, commands, timeouts, coverage, or any external project. Record the observations as evidence for a generic gap without hard-coding the observed application, timing, or deployment details into the skill.
