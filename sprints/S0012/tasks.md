# Tasks — Sprint S0012

## US-0040: Per-Sprint Release Notes and Release Queue Tracker

### T-001: Define canonical per-sprint immutable release notes path
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `handoffs/releases/Sxxxx-release-notes.md`
- Description: Define sprint-scoped release notes contract and target-sprint-only
  write semantics to prevent cross-sprint overwrite.
- AC covered: AC-1

### T-002: Define canonical release queue tracker schema and artifact contract
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/runbook.md`
- Description: Define queue artifact with required fields (sprint ID, status,
  timestamp, notes reference) and canonical ownership semantics.
- AC covered: AC-2
- Depends on: T-001

### T-003: Define deterministic queue state transitions for target sprint only
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `docs/engineering/state.md`
- Description: Define deterministic transition flow on release entry/finalization
  (`ready -> unreleased -> released`) and restrict mutations to target sprint.
- AC covered: AC-3
- Depends on: T-002

### T-004: Define unresolved sprint fail-safe behavior and reason codes
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md`
- Description: Define fail-closed behavior when sprint identity cannot be
  resolved, including explicit reason codes and remediation guidance.
- AC covered: AC-4
- Depends on: T-003

### T-005: Define migration/backfill contract for legacy release notes
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `handoffs/release_notes.md`, `handoffs/releases/Sxxxx-release-notes.md`
- Description: Define one-time, non-destructive legacy migration/backfill for
  resolvable sprint context and manual-guidance path for unresolved context.
- AC covered: AC-5
- Depends on: T-004

### T-006: Define backward-compatible legacy release notes behavior
- Story: US-0040
- Status: done
- Files: `handoffs/release_notes.md`, `.cursor/commands/release.md`
- Description: Preserve legacy read path by defining latest-release pointer and
  summary behavior without historical data loss.
- AC covered: AC-6
- Depends on: T-005

### T-007: Define queue/notes mismatch fail-safe handling contract
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `handoffs/release_queue.md`, `docs/engineering/state.md`
- Description: Define mismatch detection and reason codes for missing queue
  entries, missing notes refs, and invalid status transitions with no destructive
  auto-reconciliation.
- AC covered: AC-4, AC-7
- Depends on: T-006

### T-008: Define unreleased queue visibility in release readiness/reporting
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `docs/engineering/state.md`, `handoffs/release_notes.md`
- Description: Surface unreleased sprint queue entries in release readiness and
  finalization context so pending releases are visible before completion.
- AC covered: AC-7
- Depends on: T-007

### T-009: Align ownership and phase touchpoints across release guidance
- Story: US-0040
- Status: done
- Files: `.cursor/commands/release.md`, `.cursor/rules/core.mdc`, `.cursor/rules/handoffs.mdc`, `docs/engineering/runbook.md`
- Description: Define and align ownership/touchpoints for queue transitions and
  sprint note generation across verify-work, release, and refresh-context flows.
- AC covered: AC-8
- Depends on: T-008

### T-010: Enforce active/template parity for queue and per-sprint note semantics
- Story: US-0040
- Status: done
- Files: `template/.cursor/commands/release.md`, `template/.cursor/rules/core.mdc`, `template/.cursor/rules/handoffs.mdc`, `template/docs/engineering/runbook.md`
- Description: Mirror active release guidance changes into template copies and
  include placeholder conventions for release queue and sprint-scoped notes.
- AC covered: AC-9
- Depends on: T-009

### T-011: Add regression matrix for positive, negative, and migration paths
- Story: US-0040
- Status: done
- Files: `sprints/S0012/uat.md`, `sprints/S0012/uat.json`, `sprints/S0012/plan-verify.json`
- Description: Plan verification for success path, overwrite prevention,
  unresolved sprint failure path, mismatch reason codes, legacy migration success
  and unresolved-manual path, and parity checks.
- AC covered: AC-1, AC-3, AC-4, AC-5, AC-6, AC-7, AC-9
- Depends on: T-010
