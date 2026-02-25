# Dev -> QA Handoff — Sprint S0012 (US-0040)

## Status

S0012 implementation is complete for `US-0040` and ready for `/qa`.

## Scope completed

1. Canonical sprint-scoped release notes contract delivered:
   - `handoffs/releases/Sxxxx-release-notes.md`
   - target-sprint-only write semantics (no cross-sprint overwrite)
2. Canonical release queue tracker delivered:
   - `handoffs/release_queue.md`
   - required fields and deterministic status model
3. Deterministic transition semantics documented:
   - `ready -> unreleased -> released`
   - only target sprint queue row may mutate per `/release` run
4. Fail-safe unresolved sprint policy implemented with deterministic reason codes:
   - `RELEASE_SPRINT_UNRESOLVED`
   - `LEGACY_NOTES_SPRINT_UNRESOLVED`
   - `QUEUE_ENTRY_MISSING`
   - `NOTES_REF_MISSING`
   - `STATUS_TRANSITION_INVALID`
5. Legacy migration/backfill contract documented as non-destructive and idempotent.
6. Legacy `handoffs/release_notes.md` behavior updated to backward-compatible
   latest-pointer/summary with unreleased queue visibility.
7. Ownership/touchpoints aligned across `/release`, `core.mdc`, and
   `handoffs.mdc` guidance.
8. Active/template parity completed for all US-0040 touched command/rule/doc and
   handoff artifacts.
9. Regression matrix and automated checks delivered:
   - `sprints/S0012/uat.md`, `sprints/S0012/uat.json`,
     `sprints/S0012/plan-verify.json`
   - `tests/run-tests.ps1`, `tests/run-tests.sh`

## QA verification checklist

1. Re-run tests:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
2. Confirm test evidence:
   - `tests/report.md` shows `Pass: 142`, `Fail: 0`
   - timestamp `2026-02-25T23:11:21Z`
3. Verify canonical release artifacts exist in active and template:
   - `handoffs/release_queue.md`
   - `handoffs/releases/Sxxxx-release-notes.md`
4. Verify release command enforces:
   - target-sprint-only mutation
   - unresolved sprint fail-safe
   - queue/notes mismatch reason-code handling
   - non-destructive migration/backfill contract
5. Verify backward compatibility:
   - `handoffs/release_notes.md` operates as latest-pointer/summary
   - unreleased queue visibility guidance present
6. Verify runbook and README include US-0040 queue/history model semantics.
7. Verify active/template parity for all touched release command/rule/doc
   artifacts.
8. Confirm process-level scope only:
   - no deployment runtime rewrite claims.

## Artifacts updated for QA

- `.cursor/commands/release.md`
- `.cursor/rules/core.mdc`
- `.cursor/rules/handoffs.mdc`
- `docs/engineering/runbook.md`
- `README.md`
- `handoffs/release_notes.md`
- `handoffs/release_queue.md`
- `handoffs/releases/Sxxxx-release-notes.md`
- `sprints/S0012/tasks.md`
- `sprints/S0012/progress.md`
- `sprints/S0012/summary.md`
- `sprints/S0012/uat.md`
- `sprints/S0012/uat.json`
- `sprints/S0012/plan-verify.json`
- `docs/engineering/state.md`
- `tests/run-tests.ps1`
- `tests/run-tests.sh`
- Template parity copies under `template/` for touched command/rule/doc/handoff
  artifacts.

---

# Dev -> QA Handoff — Sprint S0010 (US-0038)

## Status

S0010 implementation is complete for `US-0038` and ready for `/qa`.

## Scope completed

1. Canonical sync policy modes and defaults are documented and aligned:
   - `disabled|manual|by_phase|by_milestone|custom_phase_list`
   - default-safe posture: `SYNC_POLICY_MODE=manual`, `ALLOW_AUTO_PUSH=0`
2. Sync eligibility is explicitly phase-boundary-only (no intra-phase evaluation).
3. Mandatory pre-push gate semantics are implemented in both validate scripts:
   - `TEST_COMMAND` is required
   - missing/failing/timed-out test blocks push deterministically
4. Optional checks (`LINT_COMMAND`, `TYPECHECK_COMMAND`) are evaluated only when
   configured and reported as `pass|fail|skipped`.
5. QA-first guardrails are documented:
   - feature auto-push forbidden before QA completion
   - blocker-aware no-push on unresolved blocking QA findings/critical issues
6. Branch safety deny-by-default + allowlist model is documented:
   - protected/default branch denied unless explicitly allowlisted
7. Deterministic sync reason codes/evidence schema is added across command/runbook/state guidance.
8. Active/template parity is completed for all touched command/docs/config files.
9. Regression matrix for positive and negative paths is added in S0010 UAT artifacts.

## QA verification checklist

1. Re-run tests:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
2. Confirm US-0038 contract checks are present in `tests/report.md`:
   - sync policy flags in active and template scratchpad
   - guarded eligibility contract in active and template `/auto`
   - sync reason code references in active and template runbook
   - validate scripts require `TEST_COMMAND`
   - validate scripts include optional `TYPECHECK_COMMAND` handling
3. Verify pre-push gate semantics from scripts:
   - missing `TEST_COMMAND` fails with reason code
   - failing/timed-out tests block push
4. Verify optional-check semantics:
   - `LINT_COMMAND` / `TYPECHECK_COMMAND` skipped when unset
   - configured failures block eligibility
5. Verify QA-first and blocker-aware restrictions are present in `/qa` and `/release`.
6. Verify branch safety deny-by-default + allowlist contract is present in docs.
7. Verify deterministic sync evidence fields and reason codes are consistently documented.
8. Verify no runtime orchestrator claims were introduced (process guidance only).

## Artifacts updated for QA

- `.cursor/commands/auto.md`
- `.cursor/commands/execute.md`
- `.cursor/commands/qa.md`
- `.cursor/commands/release.md`
- `.cursor/scratchpad.md`
- `docs/engineering/runbook.md`
- `README.md`
- `scripts/validate-and-push.ps1`
- `scripts/validate-and-push.sh`
- `tests/run-tests.ps1`
- `tests/run-tests.sh`
- `sprints/S0010/tasks.md`
- `sprints/S0010/progress.md`
- `sprints/S0010/summary.md`
- `sprints/S0010/uat.md`
- `sprints/S0010/uat.json`
- `sprints/S0010/plan-verify.json`
- `docs/engineering/state.md`
- template parity copies under `template/` for touched command/docs/config files.

---

# Dev -> QA Handoff — Sprint S0009 (US-0037)

## Status

S0009 implementation is complete for `US-0037` and ready for `/qa`.

## Scope completed

1. Deterministic `/auto start-from=<phase>` contract delivered with canonical
   phase IDs.
2. Resolver precedence documented and aligned:
   - explicit argument
   - `handoffs/resume_brief.md`
   - conservative `docs/engineering/state.md` fallback
   - fail-fast on ambiguity/conflict/unrecoverable
3. Conflict/staleness/unparseable policy added with mandatory
   `[AUTO_RESUME_ERROR]` format and required error codes.
4. Existing stop conditions explicitly preserved in continuation mode:
   decision gate, missing critical input, pause request, loop max cycles.
5. Breadcrumb contract added for inspectability:
   start source, resolved phase, resolution status, stop reason, stop phase,
   timestamp in state/resume artifacts.
6. `/pause`, `/resume`, `/auto`, README, and runbook continuation semantics are
   aligned.
7. Active/template parity completed for all changed continuation-related
   command/rule/doc files.
8. Contract-level tests updated in:
   - `tests/run-tests.ps1`
   - `tests/run-tests.sh`

## QA verification checklist

1. Re-run tests:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
   - Latest dev execution evidence: `tests/report.md` timestamp
     `2026-02-25T13:26:07Z` (`Pass=103`, `Fail=0`)
2. Confirm report contains US-0037 contract checks:
   - canonical `start-from` phase list present
   - precedence order (`argument > resume_brief > state > fail-fast`)
   - stale/unparseable/conflict fail-fast policy
   - `[AUTO_RESUME_ERROR]` format + required code list
   - breadcrumb fields in continuation guidance
3. Confirm `/pause`, `/resume`, and `/auto` guidance is semantically aligned.
4. Confirm stop-condition preservation is explicit and unchanged.
5. Confirm process-level scope only:
   - no runtime orchestrator rewrite or product runtime feature claims.
6. Confirm active/template parity for all US-0037 touched files.

## Artifacts updated for QA

- `sprints/S0009/tasks.md`
- `sprints/S0009/progress.md`
- `sprints/S0009/summary.md`
- `sprints/S0009/uat.md`
- `sprints/S0009/uat.json`
- `docs/engineering/state.md`
