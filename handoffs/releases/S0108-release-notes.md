# Release Notes — S0108 / US-0108 (Parallel Instance Arbitrage)

- **sprint_id**: S0108
- **story_refs**: US-0108
- **release_name**: `S0108 — US-0108 parallel instance arbitration for dev phase`
- **release_date**: 2026-06-29
- **orchestrator_run_id**: auto-20260628-04
- **verdict**: **PASS**
- **binding_decision**: `DEC-0108`
- **composes**: `US-0047` / `US-0092` (unchanged — extend dev phase only)

## Summary

Default-off parallel instance arbitration for execute phase. When operators enable `SOVEREIGN_PARALLEL_DEV=1`, execute spawns N (bounded, default 3) parallel dev subagents in isolated git worktrees with different models/lenses. QA cross-reviewer evaluates all N outputs; passing one selected (first PASS + highest anti-slop score; ties break by earliest proof_issued_at). Merge via `AUTO_SOVEREIGN_MERGE_RESOLVE=first_pass_wins|last_pass_wins|manual`. Resource guard `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` (default 6 total parallel processes system-wide). Composes with US-0047/US-0092 — no bulk-execute or outer-driver contract changes.

## What's new

- **Scratchpad keys (AC-1)** — `SOVEREIGN_PARALLEL_DEV=0|1` (default `0` → single dev as before), `AUTO_SOVEREIGN_PARALLEL_N` (default `3`, bounded by `AUTO_SOVEREIGN_WORKTREE_MAX` default `6`), `AUTO_SOVEREIGN_MERGE_RESOLVE=first_pass_wins|last_pass_wins|manual` (default `first_pass_wins`), `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` (default `6` system-wide); active + template byte-parity.
- **Worktree isolation (AC-2)** — Each dev subagent spawns in isolated git worktree via `scripts/parallel_dev_arbiter.py`; `AUTO_SOVEREIGN_WORKTREE_MAX` bounded; worktree created on-demand, cleaned after merge decision.
- **Selection predicate (AC-3)** — First PASS + highest US-0104 anti-slop score; ties break earliest `proof_issued_at`; selection logic in `parallel_dev_arbiter.py::select_winner()`.
- **Merge policy (AC-4)** — `first_pass_wins` (default) picks first QA-PASS verdict; `last_pass_wins` picks last; `manual` blocks merge until operator decision via `/auto` decision gate per US-0107 drain-generate semantics.
- **Resource guard (AC-5)** — `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` cap on total parallel processes; `PARALLEL_DEV_RESOURCE_EXHAUSTED` fail-closed when cap exceeded; zero overhead when `SOVEREIGN_PARALLEL_DEV=0`.
- **Contract tests (AC-6)** — Eight `test_us0108_*` markers covering scratchpad keys, worktree lifecycle, selection predicate, merge policy branches, resource guard, compose guards, reason codes, backward compatibility.
- **Documentation (AC-7)** — `docs/engineering/runbook.md` § US-0108 with operator recipes; `docs/engineering/architecture.md` `# US-0108`; DEC-0108 locked.
- **Backward compatibility (AC-8)** — `SOVEREIGN_PARALLEL_DEV=0` (default): existing single-dev execute unchanged; US-0047 bulk-execute and US-0092 outer-driver contracts UNCHANGED; `test_us0108_us0047_compose_no_bulk_matrix_change` regression guard.

## Run

```bash
pytest tests/us0108_contract_test.py -v
# Expected: 9 passed
```

## Verify

- All 8 acceptance criteria PASS
- 9/9 contract tests PASS
- Worktree isolation verified (parallel execute+QA flows in isolated git worktrees)
- Selection predicate deterministic (first PASS + highest anti-slop)
- Merge policy branches covered (first_pass_wins, last_pass_wins, manual)
- Resource guard active (caps total parallel processes at 6)
- Compose guards verified (US-0047 bulk matrix unchanged, US-0092 outer driver unchanged)

## Known Issues

None. Default-off zero-overhead design; existing single-dev execute path unchanged when disabled.

## Governance

- **DEC-0108** locked (parallel dev + worktree isolation + merge policy)
- Composes US-0047/US-0092 (unchanged — extend dev phase only)
- Research **R-0096** (closed, Q1–Q6 answered)
