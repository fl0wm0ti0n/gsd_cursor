# Tasks — Sprint S0019

## US-0046: Explicit `/sprint-plan --bulk` Mode

### T-001: Define explicit bulk planning trigger contract
- Story: US-0046
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `README.md`
- Description: Add explicit bulk-mode activation semantics and document
  default-safe fallback to current non-bulk behavior.
- AC covered: AC-1

### T-002: Define deterministic bulk selection policy
- Story: US-0046
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `docs/engineering/runbook.md`
- Description: Define deterministic story ordering (priority then backlog order),
  tie behavior, and selection evidence fields.
- AC covered: AC-2
- Depends on: T-001

### T-003: Define bounded bulk planning controls and stop reasons
- Story: US-0046
- Status: done
- Files: `.cursor/scratchpad.md`, `.cursor/commands/sprint-plan.md`, `docs/engineering/state.md`
- Description: Add bounded planning controls (max stories/max generated sprints)
  and deterministic stop-reason vocabulary.
- AC covered: AC-3
- Depends on: T-002

### T-004: Integrate bulk planning with sizing safeguards
- Story: US-0046
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `docs/engineering/runbook.md`
- Description: Ensure `SPRINT_MAX_TASKS` and `SPRINT_AUTO_SPLIT` constraints apply
  per generated sprint and are never bypassed in bulk mode.
- AC covered: AC-4
- Depends on: T-003

### T-005: Define deterministic grouping/splitting contract
- Story: US-0046
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `docs/engineering/architecture.md`
- Description: Define when bulk planning creates single-story versus multi-story
  sprints and how split decisions are made deterministically.
- AC covered: AC-5
- Depends on: T-004

### T-006: Define per-sprint artifact completeness in bulk flow
- Story: US-0046
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `template/.cursor/commands/sprint-plan.md`
- Description: Require full artifact set for each generated sprint
  (`sprint.md`, `tasks.md`, `progress.md`, UAT placeholders, plan-verify readiness).
- AC covered: AC-6
- Depends on: T-005

### T-007: Define traceability/state update behavior for multi-sprint planning
- Story: US-0046
- Status: done
- Files: `docs/engineering/state.md`, `.cursor/commands/sprint-plan.md`
- Description: Define deterministic non-duplicative traceability updates when bulk
  planning creates multiple sprint entries in one run.
- AC covered: AC-7
- Depends on: T-006

### T-008: Preserve fail-safe stops for missing/ambiguous inputs
- Story: US-0046
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `.cursor/rules/core.mdc`
- Description: Preserve decision-gate and missing-input fail-safe behavior for
  ambiguous acceptance or incomplete scope in bulk mode.
- AC covered: AC-8
- Depends on: T-007

### T-009: Add bulk-planning regression matrix
- Story: US-0046
- Status: done
- Files: `tests/run-tests.ps1`, `tests/run-tests.sh`, `sprints/S0019/plan-verify.json`
- Description: Define positive, negative, and boundary-limit regression checks for
  bulk planning behavior.
- AC covered: AC-9
- Depends on: T-008

### T-010: Align active/template behavior and finalize planning handoff
- Story: US-0046
- Status: done
- Files: `template/.cursor/commands/sprint-plan.md`, `template/README.md`, `handoffs/tl_to_dev.md`
- Description: Ensure active/template parity for bulk planning semantics and
  finalize TL->Dev execution guidance.
- AC covered: AC-10
- Depends on: T-009
