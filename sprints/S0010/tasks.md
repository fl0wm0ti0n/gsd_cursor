# Tasks — Sprint S0010

## US-0038: Phase-Triggered Sync Policy with Guarded Auto-Push

### T-001: Define canonical sync policy modes and defaults
- Story: US-0038
- Status: done
- Files: `.cursor/commands/auto.md`, `README.md`, `docs/engineering/runbook.md`
- Description: Define `disabled|manual|by_phase|by_milestone|custom_phase_list`
  policy modes and default non-auto fallback behavior.
- AC covered: AC-1, AC-10

### T-002: Define phase-boundary-only eligibility evaluation contract
- Story: US-0038
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/execute.md`
- Description: Ensure sync policy evaluation is performed only at phase
  completion boundaries and emits deterministic eligibility verdicts.
- AC covered: AC-2
- Depends on: T-001

### T-003: Enforce mandatory pre-push TEST_COMMAND gate semantics
- Story: US-0038
- Status: done
- Files: `scripts/validate-and-push.ps1`, `scripts/validate-and-push.sh`, `docs/engineering/runbook.md`
- Description: Preserve mandatory test-before-push behavior and explicitly block
  push on missing, failing, or timed-out `TEST_COMMAND`.
- AC covered: AC-3, AC-9
- Depends on: T-002

### T-004: Define optional-check execution and reporting behavior
- Story: US-0038
- Status: done
- Files: `docs/engineering/runbook.md`, `.cursor/commands/qa.md`, `.cursor/commands/release.md`
- Description: Clarify conditional lint/typecheck/formatter checks when
  configured and deterministic skip/report behavior when not configured.
- AC covered: AC-4
- Depends on: T-003

### T-005: Define QA-first auto-push restrictions for feature work
- Story: US-0038
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/qa.md`
- Description: Forbid auto-push before QA completion and document that only
  explicit manual sync is allowed pre-QA.
- AC covered: AC-5
- Depends on: T-004

### T-006: Define blocker-aware auto-push denial and remediation guidance
- Story: US-0038
- Status: done
- Files: `.cursor/commands/qa.md`, `.cursor/commands/release.md`, `docs/engineering/state.md`
- Description: Ensure unresolved blocking QA findings or critical issues force a
  `no_push` decision with actionable remediation output.
- AC covered: AC-6
- Depends on: T-005

### T-007: Define branch safety deny-by-default and allowlist contract
- Story: US-0038
- Status: done
- Files: `.cursor/commands/auto.md`, `README.md`, `docs/engineering/runbook.md`
- Description: Enforce protected/default branch denial for auto-sync unless
  explicit allowlist criteria are configured.
- AC covered: AC-7
- Depends on: T-006

### T-008: Define deterministic sync evidence and reason-code schema
- Story: US-0038
- Status: done
- Files: `docs/engineering/state.md`, `handoffs/dev_to_qa.md`, `docs/engineering/runbook.md`
- Description: Standardize sync evidence fields (phase, policy mode, checks,
  decision, reason code, evidence refs) for auditable outcomes.
- AC covered: AC-8
- Depends on: T-007

### T-009: Add regression matrix for sync positive and negative paths
- Story: US-0038
- Status: done
- Files: `sprints/S0010/uat.md`, `sprints/S0010/uat.json`, `sprints/S0010/plan-verify.json`
- Description: Plan and verify negative-path tests for disallowed auto-push:
  branch safety denial, failed tests, pre-QA restrictions, and unresolved
  blocker scenarios.
- AC covered: AC-3, AC-5, AC-6, AC-7, AC-8
- Depends on: T-008

### T-010: Align active and template validate/sync behavior references
- Story: US-0038
- Status: done
- Files: `template/docs/engineering/runbook.md`, `template/README.md`, `template/.cursor/commands/auto.md`, `template/.cursor/commands/qa.md`, `template/.cursor/commands/release.md`
- Description: Mirror all sync-policy and gate semantics into template command
  and documentation copies.
- AC covered: AC-9, AC-10
- Depends on: T-009

### T-011: Finalize planning traceability and handoff readiness
- Story: US-0038
- Status: done
- Files: `docs/engineering/state.md`, `handoffs/tl_to_dev.md`
- Description: Record planned traceability row and execution constraints for
  deterministic sync policy implementation.
- AC covered: AC-8, AC-10
- Depends on: T-010
