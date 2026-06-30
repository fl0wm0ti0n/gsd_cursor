# UAT Plan — US-0108 Parallel Instance Arbitrage

**Sprint**: S0108
**Story**: US-0108
**Phase**: /verify-work
**Role**: qa
**Timestamp**: 2026-06-29T22:30:00Z
**Orchestrator run**: auto-20260628-04

## UAT Scenarios (derived from AC-1..AC-8)

| Step | ID | Scenario (from AC) | Expected Outcome |
|------|----|--------------------|-------------------|
| 1 | UAT-1 (AC-1) | Scratchpad keys declared with zero-overhead default | `SOVEREIGN_PARALLEL_DEV=0` yields no worktree creation, no lockfile, reason `PARALLEL_DEV_DISABLED`; all 10 keys + 12 reason codes present |
| 2 | UAT-2 (AC-2) | Worktree isolation naming and cleanup | Pattern `.git/worktrees/us0108-<story>-<idx>/`, `GIT_DIR`/`GIT_WORK_TREE` env, `cleanup_worktrees` removes all post-merge |
| 3 | UAT-3 (AC-3) | Selection predicate determinism | `select_winner()` filters qa_verdict=pass, picks highest anti_slop, tie-breaks on earliest `proof_issued_at` |
| 4 | UAT-4 (AC-4) | Merge policy + pick artifact schema v1 | `parallel_dev_pick.json` schema_version=1, 11 required fields present, write-once guarantee |
| 5 | UAT-5 (AC-5) | Resource guard cap enforcement | Lockfile at `.git/us0108_parallel_dev.lock`; acquire/release works; system cap 6 enforced |
| 6 | UAT-6 (AC-6) | Execute steps 25-28 integration | `execute_parallel_dev` spawns → QA → select_winner → merge_winner + cleanup pipeline runs end-to-end |
| 7 | UAT-7 (AC-7) | Backward compat when disabled | `SOVEREIGN_PARALLEL_DEV=0` → early return, no side effects, 2 dedicated tests pass |
| 8 | UAT-8 (AC-8) | Parity scope + runbook | `sovereign-parallel-dev` scope in `check_intake_template_parity.py`; US-0108 section in runbook + standalone runbook |

## Compose-Guard Coverage

- US-0047 (bulk execute): UNCHANGED
- US-0092 (full autonomy): UNCHANGED
- US-0103 (audit ledger): UNCHANGED
- US-0104 (critic schema): UNCHANGED
- US-0107 (sovereign loop): UNCHANGED
