# Self-Maintenance Change Impact

Change: Protect self-maintenance rules and explain user decisions plainly
Requirements/acceptance: `REQ-SELF-01`–`REQ-SELF-05`, `AT-SELF-01`–`AT-SELF-05`
Status: `approved for publication`

## Skill review

The active task records `skill-creator`, `tdd`, and `setup-pre-commit` decisions in `engineering-manifest.json`. The user completed final review and authorized publication; the approval evidence is in `planning/baseline-review.md`.

## Impact map

- Modules: instructions, checker, tests and governance.
- Contracts: protected-file check and explicit external acknowledgement for commit/committed modes.
- Database: no application database; user accepted an empty inventory. Adapter code and snapshot formats are unchanged.
- Tests: existing checker/adapter tests plus rule-removal, approval-variable substitution and protected-file review regression tests.
- Documentation: module map, contract, business flow, database boundary, baseline, and skill review.

## Gate decisions

- Module/call-chain connectivity: required.
- Contract: required.
- Database boundary: required for adapter changes.
- Business flow: required.
- Control-plane manifest: required and must be reviewed with the documentation set.

## Risks and review points

- The checker is declaration-based and cannot prove all dynamic dependencies.
- The manifest and gate rules are control-plane inputs and require human review.
- Remote adapters are not live database truth and must remain explicit and metadata-only.
- Local/CI approval signals must not be hardcoded into repository-controlled files. The agent will not set the live repository's approval variable to make this change pass before the user reviews it.
- This repository chooses GitHub Actions; other projects may use local checks or another CI. Hosted approval and branch settings are not changed as part of this local edit.

## Confirmed decisions

The user stated on 2026-10-14: “是需要用户看一遍的，并且和用户沟通需要通俗易懂的告诉用户”; accepted an empty inventory when there is no business database; allowed Actions for this repository but noted not all projects use GitHub; requested “现在就加强保护”; and authorized installing PyYAML and running the check. The final response “符合我的意思,是不是都已经改好了,改好了就上传github吧” approves this completed scope and uploading it to the existing repository.

## Local verification

- Full unittest suite: 56 tests passed, exit 0. Coverage includes rule removal, renamed approval variables, true shallow clones, missing parent objects, unstaged manifest changes and prevention of command side effects after failed checks.
- Python compilation: passed. Self-manifest structure: passed; the existing optional manual inventories remain partial.
- Independent skill-creator quick validation: passed with locally installed PyYAML 6.0.3 and UTF-8 enabled. Workflow YAML parsed successfully.
- Before human approval, the live submission gate correctly blocked the rule change and skipped declared commands. Following approval, a short-lived external signal may be supplied to verify this reviewed change only.
- Hosted Actions, environment reviewers and branch protections have not been configured or executed during this local task. Their activation is a separate publication step.

## Publication follow-up

The approved change was published as `147531c`. The protected review environment was configured with the repository owner as reviewer and admin bypass disabled. The exact-SHA reviewed run passed on Ubuntu; Windows passed all rule and scope checks but its test command exited 1. Add visible fixture-test diagnostics only after all required prechecks have passed, so the platform-specific failure can be corrected without weakening the rule gate. This is a routine validation follow-up within the user's request to publish the completed working change.

The diagnostic run identified one fixture using an unnormalized temporary root (`RUNNER~1`) while the resolved path used `runneradmin`. The CLI already normalizes roots through `safe_root`. The remote-inventory fixture now uses that same public root preparation, retaining all assertions and path containment checks. This fixes Windows test setup only; production checker, adapters and approval policy are unchanged.
