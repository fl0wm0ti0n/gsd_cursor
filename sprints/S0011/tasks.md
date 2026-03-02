# Tasks — Sprint S0011

## US-0039: Release Gate Tightening for Check-In Tests and QA/UAT Completion

### T-001: Define mandatory release gate chain and strict ordering
- Story: US-0039
- Status: done
- Files: `.cursor/commands/release.md`, `docs/engineering/runbook.md`
- Description: Define deterministic gate order:
  `check-in test -> QA -> UAT -> release notes/runbook finalization`.
- AC covered: AC-1, AC-5

### T-002: Define latest check-in test evidence validity contract
- Story: US-0039
- Status: done
- Files: `.cursor/commands/release.md`, `docs/engineering/state.md`
- Description: Define freshness and validity rules for latest check-in test
  evidence and deterministic fail reasons for missing/stale/failing evidence.
- AC covered: AC-1, AC-2
- Depends on: T-001

### T-003: Define QA completion evidence gate semantics
- Story: US-0039
- Status: done
- Files: `.cursor/commands/release.md`, `.cursor/commands/qa.md`, `handoffs/qa_to_dev.md`
- Description: Require QA evidence with no unresolved blocking findings before
  release progression.
- AC covered: AC-3
- Depends on: T-002

### T-004: Tighten UAT completion gate semantics
- Story: US-0039
- Status: done
- Files: `.cursor/commands/release.md`, `sprints/S0011/uat.md`, `sprints/S0011/uat.json`
- Description: Preserve and tighten UAT verified-state requirements and explicit
  failure behavior for placeholder, incomplete, or unresolved-fail states.
- AC covered: AC-4
- Depends on: T-003

### T-005: Define per-gate audit verdict schema and evidence pointers
- Story: US-0039
- Status: done
- Files: `handoffs/release_notes.md`, `docs/engineering/state.md`, `docs/engineering/runbook.md`
- Description: Record pass/fail/override status for each gate with reason code,
  remediation, and evidence references for TL/QA auditability.
- AC covered: AC-6
- Depends on: T-004

### T-006: Enforce no-bypass default release behavior
- Story: US-0039
- Status: done
- Files: `.cursor/commands/release.md`, `.cursor/rules/core.mdc`
- Description: Explicitly deny non-decision bypass paths for test/QA/UAT gates
  in default workflow behavior.
- AC covered: AC-7
- Depends on: T-005

### T-007: Define decision-gate override evidence contract
- Story: US-0039
- Status: done
- Files: `.cursor/commands/release.md`, `decisions/DEC-0019.md`, `handoffs/release_notes.md`
- Description: Require explicit decision record, rationale, approver, and risk
  acceptance evidence when override path is used.
- AC covered: AC-7
- Depends on: T-006

### T-008: Add release gate regression matrix (positive, negative, stale)
- Story: US-0039
- Status: done
- Files: `sprints/S0011/uat.md`, `sprints/S0011/uat.json`, `sprints/S0011/plan-verify.json`
- Description: Plan gate coverage for stale evidence, missing QA/UAT evidence,
  unresolved blockers, and no-bypass behavior.
- AC covered: AC-2, AC-3, AC-4, AC-5, AC-7, AC-9
- Depends on: T-007

### T-009: Preserve optional-command compatibility in release gating
- Story: US-0039
- Status: done
- Files: `docs/engineering/runbook.md`, `.cursor/commands/release.md`, `README.md`
- Description: Ensure blank optional lint/typecheck keys do not fail release,
  while mandatory test + QA + UAT gates remain strict.
- AC covered: AC-10
- Depends on: T-008

### T-010: Align active and template release-gate semantics
- Story: US-0039
- Status: done
- Files: `template/.cursor/commands/release.md`, `template/.cursor/commands/qa.md`, `template/.cursor/commands/execute.md`, `template/docs/engineering/runbook.md`, `template/README.md`
- Description: Mirror release-gate ordering, no-bypass, and evidence semantics
  in template command/docs copies.
- AC covered: AC-8
- Depends on: T-009

### T-011: Finalize planning traceability and handoff readiness
- Story: US-0039
- Status: done
- Files: `docs/engineering/state.md`, `handoffs/tl_to_dev.md`
- Description: Record planned traceability row and execution guardrails for
  release gate tightening delivery.
- AC covered: AC-6, AC-8, AC-9
- Depends on: T-010
