# Tasks — Sprint S0020

## US-0047: Explicit Bulk Execute Orchestration Mode

### T-001: Define explicit bulk execute activation contract
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `README.md`
- Description: Add explicit bulk execute activation semantics (`--execute-bulk`
  or scratchpad switch) and preserve default-safe non-bulk behavior.
- AC covered: AC-1

### T-002: Define deterministic planned-item selection and breadcrumb evidence
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `docs/engineering/state.md`
- Description: Define deterministic work-item selection policy and breadcrumb
  evidence including team-context snapshot fields when enabled.
- AC covered: AC-2
- Depends on: T-001

### T-003: Enforce fresh-context isolation per phase and execute↔QA cycle
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/execute.md`
- Description: Preserve strict fresh subagent isolation contract for each phase
  and each execute↔QA loop cycle in bulk mode.
- AC covered: AC-3
- Depends on: T-002

### T-004: Preserve bounded execute↔QA loop controls per item
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/scratchpad.md`
- Description: Ensure `AUTO_IMPLEMENTATION_LOOP` and max cycle controls remain
  bounded and apply per processed sprint/story item.
- AC covered: AC-4
- Depends on: T-003

### T-005: Define bounded run controls and deterministic stop-vs-skip reasons
- Story: US-0047
- Status: done
- Files: `.cursor/scratchpad.md`, `.cursor/commands/auto.md`
- Description: Add bounded max-item controls and deterministic reason-code
  outcomes for blocked item stop/skip behavior.
- AC covered: AC-5
- Depends on: T-004

### T-006: Preserve decision-gate behavior in bulk execute progression
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`
- Description: Keep decision gates mandatory so bulk progression pauses until
  user decision is recorded.
- AC covered: AC-6
- Depends on: T-005

### T-007: Define deterministic resume semantics for interrupted bulk runs
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `handoffs/resume_brief.md`
- Description: Define deterministic checkpoint fields for interrupted runs,
  including next item, stop reason, and stop phase.
- AC covered: AC-7
- Depends on: T-006

### T-008: Enforce team-scoped no-write behavior for out-of-scope tasks
- Story: US-0047
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/execute.md`
- Description: In team mode, enforce member/task scope checks and deterministic
  skip/block outcomes with no writes for out-of-scope tasks.
- AC covered: AC-8
- Depends on: T-007

### T-009: Add regression coverage for bulk execute contract
- Story: US-0047
- Status: done
- Files: `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0020/plan-verify.json`
- Description: Add positive and negative contract checks for explicit trigger,
  bounded controls, team-scope guardrails, and reason-code vocabulary.
- AC covered: AC-9
- Depends on: T-008

### T-010: Align active/template semantics and finalize handoff docs
- Story: US-0047
- Status: done
- Files: `template/.cursor/commands/auto.md`, `template/README.md`, `template/docs/engineering/runbook.md`, `handoffs/tl_to_dev.md`
- Description: Complete active/template parity for bulk execute semantics and
  finalize handoff guidance.
- AC covered: AC-10
- Depends on: T-009
