# Verification Closure Assessment / 2026-10-28

Status: assessment complete. The user asked whether 1.12.0 needs another focused change and requested a GitHub upload for trial: “那你看看是不是需要再次修改skill,然后重新上传github进行试验”. This assessment is limited to the engineering-workflow repository; it does not authorize a Liantong project change, merge, or GitHub Release.

## Finding

Version 1.12.0 already says to reconcile affected views after implementation stabilizes and then run final required checks. It does not say how to freeze the exact candidate tree or handle validation and publication facts that become known only after those checks.

The prior task record shows the gap in practice. Its content commit gate passed with TEST 185.015s, its committed gate passed with TEST 171.521s, and a later publication-receipt commit ran the required gate again with TEST 181.703s. The task also records an omitted impact document on an early attempt, a preview without `--run-checks`, and a report-path collision on a later attempt. These failures and policy-required checks are distinct; the reports are bound to different states.

This evidence does not show that every repeat was avoidable or that the skill alone caused the elapsed time. Some runs were required by the repository's commit/committed policy, and failed attempts cannot count as passes. The actionable gap is that the skill did not direct the agent to plan result storage before the final gate or explain that a receipt-only tracked commit creates a new tree requiring the existing checks.

## Recommendation

Add narrow guidance to freeze the candidate tree after all known tracked changes, bind reports to exact commit/tree, use project-approved external or ignored evidence when policy permits, and revalidate a receipt-bearing tree when tracking is mandatory. Preserve every existing approval, command, timeout, check, coverage rule and delivery gate. Keep the trial on a dedicated GitHub branch and measure behavior on a later comparable task; do not claim savings from this single case.

The strict workflow-state index also exposed duplicate decision and verification-result keys in the old completed Task object in `engineering-manifest.json`. They are consolidated into single fields while retaining the full decisions and evidence, allowing the current linked task state to be parsed unambiguously.
