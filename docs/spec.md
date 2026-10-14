# Self-Maintenance Specification

Status: `current`

This repository is the maintained source of the `engineering-workflow` Codex skill. The skill must remain useful to unfamiliar projects, cross-layer changes, documentation impact gates, and verification work.

## Requirements

- REQ-SELF-01: The repository maintains a traceable baseline for its own instructions, modules, contracts, business flow, database-adapter boundary, and verification checks.
- REQ-SELF-02: Changes to the skill are reviewed with applicable skills, tests, documentation-impact analysis, and Git commit evidence.
- REQ-SELF-03: Database adapters remain metadata-only, explicit, and safe to run without exposing credentials or business values.

## Acceptance

- AT-SELF-01: The active manifest and baseline documents pass the checker in baseline mode.
- AT-SELF-02: The test suite and Python compilation checks pass for the current source tree.
- AT-SELF-03: A self-maintenance change records skill applicability, affected modules, documentation gates, tests, and manual-review status.

## Scope and ownership

The skill instructions own the workflow rules. The checker owns mechanical manifest, impact, inventory, and Git gate validation. The adapter scripts own metadata extraction. Tests are the executable behavior evidence. User decisions and repository-specific rules remain higher priority than this skill.

## Non-goals

This baseline does not claim that the checker discovers every dynamic dependency, proves database business semantics, or replaces human review of its own design.
