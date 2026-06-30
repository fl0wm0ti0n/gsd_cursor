# Sprint S0108 — US-0108 Parallel Instance Arbitrage for dev phase

- sprint_id: S0108
- story_id: US-0108
- governance: DEC-0108
- architecture_ref: docs/engineering/architecture.md # US-0108
- research_ref: R-0096
- status: released
- created_at: 2026-06-29T21:32:00Z
- orchestrator_run_id: auto-20260628-04
- task_count: 11
- within_limit: true (11 <= SPRINT_MAX_TASKS=12)
- sprint_auto_split_triggered: false

## AC-to-task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Scratchpad keys | T-001 |
| AC-2 Worktree isolation | T-002, T-003 |
| AC-3 Selection predicate | T-004, T-005 |
| AC-4 Merge policy + pick JSON | T-006 |
| AC-5 Resource guard | T-007 |
| AC-6 Execute steps 25-28 | T-008 |
| AC-7 Backward compat + tests | T-009, T-010 |
| AC-8 Parity + runbook | T-011 |

## Tranche order (A→E)

- **A** Keys + reason codes — T-001
- **B** Worktree lib — T-002, T-003
- **C** Selection + anti-slop — T-004, T-005
- **D** Merge + resource guard + execute steps — T-006, T-007, T-008
- **E** Tests + parity + runbook — T-009, T-010, T-011

## Tasks

- [x] **T-001** Scratchpad keys + reason codes (AC-1)
- [x] **T-002** Worktree isolation lib (AC-2)
- [x] **T-003** Worktree cleanup post-merge (AC-2)
- [x] **T-004** Selection predicate (AC-3)
- [x] **T-005** Anti-slop score reader (AC-3)
- [x] **T-006** Merge policy + pick JSON (AC-4)
- [x] **T-007** Resource guard (AC-5)
- [x] **T-008** Execute steps 25-28 (AC-6)
- [x] **T-009** Backward compat guard (AC-7)
- [x] **T-010** Contract tests (AC-7)
- [x] **T-011** Parity + runbook (AC-8)
