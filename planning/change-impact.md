# Self-Maintenance Change Impact

Change: Establish the engineering-workflow repository's own maintenance baseline  
Requirements/acceptance: `REQ-SELF-01`–`REQ-SELF-03`, `AT-SELF-01`–`AT-SELF-03`  
Status: `reviewed`

## Skill review

The active task records `skill-creator`, `tdd`, and `setup-pre-commit` decisions in `engineering-manifest.json`. The user will perform the final manual review.

## Impact map

- Modules: instructions, checker, adapters.
- Contracts: checker CLI modes and adapter snapshot format.
- Database: no application database; metadata-only adapter boundary documented.
- Tests: existing checker and adapter tests plus baseline/compile checks.
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
