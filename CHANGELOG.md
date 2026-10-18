# 1.6.3 / Unreleased

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
