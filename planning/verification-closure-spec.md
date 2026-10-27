# SPEC-VERIFICATION-CLOSURE-01 r1

Status: authorized for implementation by the user's direct request on 2026-10-28: “那你看看是不是需要再次修改skill,然后重新上传github进行试验”. Scope is this repository's workflow guidance and linked release/governance records.

## Goal

Reduce avoidable full-check reruns caused by late tracked result or publication receipts while preserving exact-tree verification and every project-defined delivery gate.

## Requirements

- **REQ-VFC-01:** Before the final required-check set, reconcile all currently known implementation, test, task, manifest, impact, and version changes into one candidate tree; decide where later-generated validation and publication evidence will live; then freeze the tree.
- **REQ-VFC-02:** Bind each final report to its exact commit/tree. Any later tracked-file change is a new candidate and must satisfy the project's existing checks; earlier results remain historical for their original tree.
- **REQ-VFC-03:** When project policy permits, use its approved ignored report, CI artifact, or delivery response for results and publication SHAs learned after verification instead of a tracked receipt-only commit. If tracked receipts are required, consolidate them and verify the resulting tree.
- **REQ-VFC-04:** Preserve approvals, required commands, scopes, timeouts, coverage, CI behavior, review rules, and publication boundaries. Do not claim efficiency savings without a comparable task sample.

## Acceptance

- **AT-VFC-01:** Guidance explains final-tree freeze, exact commit/tree binding, and the need to revalidate later tracked changes.
- **AT-VFC-02:** Guidance permits external/ignored evidence only where project policy allows it and gives a compliant path when tracked receipts are mandatory.
- **AT-VFC-03:** README and version/changelog surfaces describe the behavior consistently.
- **AT-VFC-04:** Existing TEST, COMPILE, GUIDANCE-COMPILE commands, timeouts, approval checks, and CI policy are unchanged.

## Scope boundaries

In scope: `SKILL.md`, `references/implementation-workflow.md`, README, version/changelog metadata, manifest and linked task-governance records. Out of scope: checker code/schema, required checks or timeouts, CI workflow, Liantong files, merge, and GitHub Release.
