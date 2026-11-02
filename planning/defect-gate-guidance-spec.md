# SPEC-DEFECT-GATE-GUIDANCE-01 r1

Status: authorized for local implementation by the user's direct request on 2026-11-03. Scope is this repository's generic engineering-workflow guidance, linked documentation, and guidance tests.

## Goal

Make defect plans address confirmed causes by default and make required-check selection proportional to each independently scoped Task, while preserving project-wide requirements and exact-tree evidence.

## Requirements

### REQ-DGF-01 Cause-directed defect correction

When a cause is confirmed, propose the smallest complete correction at the responsible layer and connect the mechanism to the evidence for that cause. A guard or fallback is valid when it restores or enforces the violated invariant; it does not replace correction of a known upstream cause without an explicit reason.

### REQ-DGF-02 Explicit symptom mitigation

When a root-cause correction is not feasible, authorized, or safe in the current scope, label symptom containment as mitigation. Record why the cause correction is deferred, residual risk and behavior that could be masked, the owner or trigger for revisit, and a check that shows the mitigation does not conceal related failures. This does not add a diagnosis approval or require an architectural rewrite.

### REQ-DGF-03 Task-scoped required checks

At planning time, select `Task.required_checks` from the actual Task impact and the project's explicit always-required policy. Do not inherit an unrelated broad feature's complete check list into an independent narrow follow-up by default. Preserve every explicit project-wide mandatory check. Do not remove or weaken a declared check in response to its failure.

### REQ-DGF-04 Receipt-only and exact-tree evidence

Keep code and deployment reports bound to the exact tree they verified. For receipt-only or documentation-only work, use an approved ignored/artifact location when policy allows it, or a linked documentation/evidence Task with applicable integrity checks. Do not rerun unaffected product suites unless the project policy requires them or their inputs changed. If policy requires the full set, run it; never reuse a report as verification of a different tree.

## Acceptance

- **AT-DGF-01:** Defect guidance makes a cause-removing correction the default and allows guards when they enforce the diagnosed invariant.
- **AT-DGF-02:** Symptom-only containment is explicitly a mitigation and records deferral reason, residual/masking risk, revisit owner or trigger, and validation.
- **AT-DGF-03:** Guidance selects required checks for the actual Task while retaining project-wide mandatory checks and prohibits weakening a failed gate.
- **AT-DGF-04:** Receipt-only work remains separately scoped, honors project policy, and cannot claim an earlier code report verifies a changed tree.
- **AT-DGF-05:** Existing workflow stages, approvals, checker semantics, required-check definitions, commands, timeouts, coverage, and CI behavior remain unchanged.

## Boundaries

In scope: `SKILL.md`, `references/implementation-workflow.md`, README/version/changelog surfaces, manifest-linked records, and `scripts/tests/test_guidance.py`.

Out of scope: checker implementation or schema, CI workflows, changes to repository check definitions, external project migration, commits, pushes, deployment, or publication.
