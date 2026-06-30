# Sprint S0111 - US-0111 Release Trigger-Driven Version Changelog Derivation

- sprint_id: S0111
- story_id: US-0111
- governance: DEC-0111
- architecture_ref: docs/engineering/architecture.md # US-0111
- research_ref: R-0098
- status: OPEN
- created_at: 2026-06-30T18:20:00Z
- orchestrator_run_id: auto-20260628-04
- task_count: 12
- max_tasks: SPRINT_MAX_TASKS=12
- within_limit: true (12 <= SPRINT_MAX_TASKS=12)
- sprint_auto_split_triggered: false

## AC-to-task surjective map

| AC | Title | Tasks |
|----|-------|-------|
| AC-1 | Trigger adapter registry | T-001 |
| AC-2 | GitHub webhook adapter | T-002 |
| AC-3 | npm publish trigger | T-003 |
| AC-4 | Git tag push trigger | T-004 |
| AC-5 | Manual backward compatibility | T-005 |
| AC-6 | Version comparison logic | T-006 |
| AC-7 | Atomic promotion | T-007 |
| AC-8 | Per-version notes generation | T-008 |
| AC-9 | Sovereign loop integration | T-009 |
| AC-10 | Fail-closed reason codes | T-010 |
| AC-11 | Contract tests + template parity | T-011 |
| AC-12 | Documentation + runbook updates | T-012 |

## Tranche order (A->D)

- **A** — adapter registry + TriggerContext (T-001)
- **B** — four concrete adapters (T-002, T-003, T-004, T-005)
- **C** — version comparison + atomic promotion + per-version notes + sovereign loop integration + reason codes (T-006, T-007, T-008, T-009, T-010)
- **D** — contract tests + documentation + runbook (T-011, T-012)

## Tasks

- [ ] **T-001** Trigger adapter registry (AC-1)
- [ ] **T-002** GitHub webhook adapter (AC-2)
- [ ] **T-003** npm publish trigger (AC-3)
- [ ] **T-004** Git tag push trigger (AC-4)
- [ ] **T-005** Manual backward compatibility (AC-5)
- [ ] **T-006** Version comparison logic (AC-6)
- [ ] **T-007** Atomic promotion (AC-7)
- [ ] **T-008** Per-version notes generation (AC-8)
- [ ] **T-009** Sovereign loop integration (AC-9)
- [ ] **T-010** Fail-closed reason codes (AC-10)
- [ ] **T-011** Contract tests + template parity (AC-11)
- [ ] **T-012** Documentation + runbook updates (AC-12)

## Compose guards (non-negotiable)

| Story | Compose rule |
|-------|--------------|
| US-0100 | `compare_versions()` and `promote_unreleased()` UNCHANGED |
| US-0054 | `/release` command logic UNCHANGED |
| US-0103 | Ledger schema UNCHANGED |
| US-0040 | Release notes structure UNCHANGED |
| US-0008 | release-all.sh UNCHANGED |
| US-0107 | `sovereign_loop_lib` UNCHANGED |
| US-0110 | `list_open_deferrals()` UNCHANGED |
