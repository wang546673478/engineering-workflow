# 1.10.0 / Unreleased

- Add an optional manifest-backed workflow state CLI that preserves completed, superseded/obsolete, deferred and unverified records in a rebuildable index; reads exact document snapshots with source hashes; and supports dry-run plus idempotent hash/archive-head guarded batch updates with conflict detection and recovery through the existing local archive.
- Preserve the existing 1.8 workflow stages, approval meanings, required checks, command timeouts and migration boundaries. The new CLI adds no required gate, automatic migration or host API integration; host cwd launch failures remain unsupported.
- Set the existing required TEST timeout to the user-approved 240 seconds to accommodate the full suite's measured near-boundary runtime; keep the same unittest command, all 260 test cases/assertions, COMPILE/GUIDANCE-COMPILE 30-second timeouts and workflow/approval stages unchanged.

# 1.9.0 / Unreleased

- Add an optional local task archive command for manifest-declared engineering records: immutable SQLite revisions outside the project root, drift detection, expected-head checkpoints, history, and restore-as-new-revision.
- Preserve the 1.8.0 workflow stages, approval meanings, diagnostic/strict defaults, required checks, command timeouts, and migration boundaries. Host-level blocking of arbitrary shell/editor writes remains explicitly unsupported when the host exposes unrestricted file access.

# 1.8.0 / Unreleased

- Reuse the already validated historical manifest within a single submission check and avoid repeated interpreter startup for static contract scenarios; retain all behavior assertions, independent commit/committed coverage and original time limits.

- Add an opt-in structured approval evidence contract that binds declared approvals to their original statement, timestamps, evidence record, reviewed Spec/Plan section hashes, and selected task batch/requirements. The checker reports legacy approvals as non-blocking `partial`; strict enforcement is explicit and protected against silent policy removal or weakening.
- Initialize new manifests and explicit legacy migrations in diagnostic mode by default. Add preview-before-apply migration, JSON evidence support, bounded approval reuse, optional same-timeline sequence diagnostics, and honest delivery-status guidance.
- Preserve the existing workflow stages, valid prior approvals, small-fix/greenfield paths, required TEST/COMPILE/GUIDANCE-COMPILE commands and timeouts, Git tree verification, and documentation-impact/synchronization rules. No external project is migrated automatically.

# 1.7.2 / Unreleased

- Clarify defect evidence in existing tasks: original reproduction, confirmed cause versus hypotheses, preserved behavior, before/after results and proportionate regression checks.
- Make the existing delivery convergence concrete with missing/partial/conflicting behavior, changes without an established basis, stale evidence and their authoritative destinations.
- Add optional EARS examples in Chinese and Given–When–Then acceptance guidance, linked from existing templates. Existing records and formats remain valid.
- Preserve workflow stages, approval meanings, small-fix/greenfield/recovery paths and all required commands, timeouts and control-plane protections. No new CLI, schema, dependencies, mandatory reports or automatic project migration.

# 1.7.1 / Unreleased

- Normalize the initializer library's project root before validating source scopes, matching the CLI and supporting Windows short-name/lexical aliases without weakening project-boundary checks.
- Add a root-alias regression; preserve the original workflow and every prior check. This corrects the Windows hosted failure found while validating 1.7.0.

# 1.7.0 / 2026-10-19

- Added complete project adoption: real manifest plus managed guidance, existing document mapping, actual skill/checker provenance, and read-only bootstrap diagnostics that keep unfinished work visible.
- Added optional declaration checks for the original stages and approval meanings, including evidenced empty-project/small-fix exceptions, prior-review reuse and shared explicit authorization; complete/approved delivery remains. Blocked commit checks do not execute project commands.
- Guidance installation rejects Markdown-as-JSON and target collisions while retaining guidance-first setup with an explicit incomplete receipt. Explicit legacy upgrades preserve existing policy/history and use atomic manifest replacement; old manifests retain compatibility until migrated.
- Updated skill guidance, templates and linked engineering views. No external project migration or automatic approval is performed. Local installation is updated separately under user authorization.

# 1.6.4 / 2026-10-19

- Bind commit/committed verification to HEAD and the index tree before reading inputs, reject post-check index/worktree/HEAD drift, and expose successful verified_tree/verification_head evidence.
- Report deep JSON, integer parser limits and non-object manifests as structured configuration failures; damaged historical manifests fail closed instead of becoming missing policy.
- Clean owned process families and output readers on normal completion, timeout and interruption. Windows commands start suspended, join a kill-on-close Job Object and then resume; POSIX retains process-group cleanup. CLI SIGINT/SIGTERM cancellation is non-success and restores handlers.
- Preserve required checks, limits, approval policy and original workflow stages. Boundary checks are not a hostile-code sandbox; POSIX SIGKILL and the Windows pre-assignment startup window still require external lifecycle controls for absolute guarantees.

# 1.6.3 / 2026-10-19

- Generate an explicit recursive node_modules exclusion in both initializer profiles, keeping existing manifests and checker policy unchanged.
- Surface optional Rust/Node/TypeScript parser failures and installation guidance in relation status, CLI output and summaries; retain valid partial results and distinguish analyzer execution failures.
- Fail parser regression setup with actionable guidance instead of cascading empty-graph assertions; document both pinned test runtimes without skipping required coverage.

# 1.6.2 / 2026-10-18

- Keep the original required checker outcome authoritative in reviewed and manually reviewed CI jobs, even when a diagnostic test rerun passes.
- Add a shared finalizer and regression coverage for both successful and failed checker outcomes; retain the diagnostic rerun for failure investigation.
- Keep required commands, test coverage, 120-second timeout, protected environment and approval duties unchanged.

# 1.6.1 / 2026-10-18

- Fix source collection on Windows Python3.11 by recognizing directory reparse points before traversal, including source/output ancestors.
- Canonicalize the read-failure test target so Windows short-path aliases still trigger the intended PermissionError; keep unreadable-source exclusion assertions.
- Isolate checker/initializer fixture environments from the enclosing CI task and approval variables, while preserving explicit environment-priority tests.
- Add older-Python reparse/root behavior regressions. Existing workflow, checker, CI, required tests and timeouts remain unchanged.

# 1.6.0 / 2026-10-18

- Added optional local source inventory/tree/statistics, complete compact reading packs and explicit read budgets/omissions.
- Added source-evidenced JS/TS and Rust module references with strict evidence checks and selectable summary/table/diagram outputs.
- Added scenario-specific invocation and scope/view rules; same-run discovery reuse avoids repeated scans without a persistent cache.
- Added exact optional-parser dependency locks and CI preparation for their behavior tests. Existing workflow stages, approval duties, checker code, required commands and protection scopes remain unchanged.
- Excluded product token estimation, Notebook conversion, incremental cache and additional model/cloud generation chains. Third-party MIT notices retained.

# Changelog

## 1.5.0 - 2026-10-18

- Make Global Baseline, Spec, Technical Plan and Task a versioned, traceable chain for new and existing projects.
- Add active Baseline/Spec/Plan/Task pointers, task artifact links and Baseline document references to new manifest skeletons.
- Validate declared linked-artifact references while preserving compatibility with existing manifests that omit the optional fields.
- Document evidence-driven Baseline correction, frozen approved Spec revisions, Plan/Task reconciliation and delivery-time convergence.
- Add an explicit greenfield bootstrap and evidenced not_applicable → partial → complete baseline lifecycle. Provisional states permit ongoing work but fail completion/handoff; existing-project gates remain intact.
- Require linked views consistently in full/lite skeletons, replace invalid root/unowned documentation triggers with reviewable source scopes, and check active optional document targets for existence.
- Reconcile this repository's current baseline, Spec, Plan, Tasks and traceability while preserving historical release/review evidence; align the skill frontmatter with the 1.5.0 candidate.

## 1.4.4 - 2026-10-17

- Continue authorized baseline investigation after saved batches and progress updates; prepare necessary local isolated runtimes, databases and caches and record actual validation and cleanup.
- Assign source and semantic investigation to the agent; bind user baseline review to the evidenced revision, scope, findings and limits without claiming production certification.
- Correct baseline errors discovered during testing or investigation even without code changes, synchronize affected views and preserve evidence/history; reopen only invalidated decisions and dependent implementation.
- Check inventory capabilities before adoption and align the manifest example with the existing full initializer's optional source inventories. Existing required gates, manual/partial results, checker behavior and project tests remain unchanged.

## 1.4.3 - 2026-10-16

- Apply the workflow to discussions of any feature/module change and continue active requirements without another explicit skill mention.
- Keep requirement decisions and deferred topics in authoritative documents throughout discussion; refresh current state and record dependencies and conditions for revisiting postponed work.
- Combine completeness checks and user review when each functional module's discussion finishes, while preserving continuous recording and existing baseline/proposal approval gates.
- Track requirement status separately from implementation status; synchronize persistent guidance, references and templates without changing checker or manifest APIs.

## 1.4.2 - 2026-10-15

- Clarify version-bump timing and PATCH/MINOR/MAJOR defaults for each substantive delivery batch, including skill instruction changes.
- Require version/changelog impact, synchronization paths and actual publication status in task records; preserve project-specific, generated and multi-package versioning.
- Keep unreleased notes distinct from published history and avoid repeated bumps for progress, verification or publication receipts that do not change delivered content.

## 1.4.1 - 2026-10-15

- Require global discovery and user baseline review before detailed feature interviews on first takeover of existing code without a valid baseline.
- Preserve basic goal clarification, reusable baseline evidence, small-fix workflows and new-project exceptions; add stage and transition evidence to the task template.
- Resolve the repository's active task through the manifest and correct stale task/document status.
- Include checker fixes since 1.4.0 for version reporting, cross-platform paths, exclusion globs, command validation/output limits and release-metadata protection.

## 1.4.0 - 2026-10-14

- Added persistent `AGENTS.md` adoption guidance and cross-agent thin-entry support.
- Added first-adoption control-plane diagnostics and verification-policy limitations.
- Added manifest/checker improvements tracked by GitHub issues #2-#8 and a manifest bootstrap helper.
- Added package version metadata and repository license.
