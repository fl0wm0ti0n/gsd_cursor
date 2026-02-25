# Sprint S0005 — Summary

## Goal
Deliver US-0025, US-0027, and US-0026 by adding traceability contracts,
formalizing UAT artifact lifecycle, and defining milestone lifecycle governance
across existing command files, state artifacts, and their template copies.

## Outcome
All 9 tasks completed. 2 pre-sprint fixes (from S0004 QA) also applied.

## Pre-sprint fixes
- F-001: Test command count updated from 20 to 21 in `tests/run-tests.ps1` and
  `tests/run-tests.sh` (accounts for `ask.md` added in S0002).
- F-002: US-0024 status changed from OPEN to DONE in `docs/product/backlog.md`,
  all AC checkboxes marked.

## Deliverables

### US-0025: Backlog-to-Sprint Traceability Contract (T-001..T-003)
- `docs/engineering/state.md`: added `## Traceability Index` table with backfilled
  rows for S0001 (US-0018, US-0015), S0002 (US-0020, US-0021, US-0022),
  S0003 (US-0023), S0004 (US-0024), S0005 (US-0025, US-0027, US-0026).
- `.cursor/commands/sprint-plan.md` + template: added step for traceability index
  maintenance using DEC-0010 format.
- `.cursor/commands/verify-work.md` + template: added traceability verification
  step and pre-handoff check for missing entries.

### US-0027: UAT Artifact Lifecycle and Ownership (T-004..T-006)
- `.cursor/commands/sprint-plan.md` + template: added UAT placeholder creation
  guidance referencing DEC-0009 lifecycle taxonomy.
- `.cursor/commands/verify-work.md` + template: added UAT lifecycle rules section,
  minimum content requirements, and population step. Sprint cannot be marked
  complete with placeholder UAT.
- `.cursor/commands/release.md` + template: added UAT readiness gate section and
  verification step before release proceeds.

### US-0026: Milestone Lifecycle Definition and Exit Criteria (T-007..T-009)
- `.cursor/commands/milestone-start.md` + template: added lifecycle state table
  (created → active → in-review → completed | cancelled), required fields per
  state, placeholder vs real content distinction.
- `.cursor/commands/milestone-complete.md` + template: added exit criteria checklist
  (all sprints done, UAT passing, progress.md complete, summary.md written,
  traceability verified, no open blockers).
- `.cursor/commands/sprint-plan.md` + template: added milestone activation check
  for first sprint under a milestone.

## Acceptance coverage
- US-0025: AC-1 (index format), AC-2 (cross-reference), AC-3 (mismatch definition),
  AC-4 (sprint-plan guidance), AC-5 (verify-work check), AC-6 (scope boundary)
- US-0027: AC-1 (lifecycle by phase), AC-2 (ownership), AC-3 (minimum content),
  AC-4 (readiness evidence), AC-5 (AC linkage), AC-6 (scope boundary)
- US-0026: AC-1 (lifecycle states), AC-2 (required fields), AC-3 (command guidance),
  AC-4 (placeholder vs real), AC-5 (exit criteria), AC-6 (scope boundary)

## Files modified
- `tests/run-tests.ps1` — command count 20→21
- `tests/run-tests.sh` — command count 20→21
- `docs/product/backlog.md` — US-0024 status OPEN→DONE
- `docs/engineering/state.md` — traceability index + session status
- `.cursor/commands/sprint-plan.md` — traceability + UAT placeholder + milestone activation
- `.cursor/commands/verify-work.md` — traceability verification + UAT rules
- `.cursor/commands/release.md` — UAT readiness gate
- `.cursor/commands/milestone-start.md` — lifecycle states
- `.cursor/commands/milestone-complete.md` — exit criteria
- `template/.cursor/commands/sprint-plan.md` — matching active copy
- `template/.cursor/commands/verify-work.md` — matching active copy
- `template/.cursor/commands/release.md` — matching active copy
- `template/.cursor/commands/milestone-start.md` — matching active copy
- `template/.cursor/commands/milestone-complete.md` — matching active copy

## Stories completed
- US-0025 (AC-1 through AC-6)
- US-0027 (AC-1 through AC-6)
- US-0026 (AC-1 through AC-6)
