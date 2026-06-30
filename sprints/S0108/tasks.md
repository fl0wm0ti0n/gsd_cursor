# Sprint S0108 — US-0108 Parallel Instance Arbitrage for dev phase — Tasks

## AC-to-task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Scratchpad keys + zero-overhead when 0 | T-001 |
| AC-2 Worktree isolation (naming, GIT_DIR, cleanup) | T-002, T-003 |
| AC-3 Selection predicate (PASS → anti-slop → earliest) | T-004, T-005 |
| AC-4 Merge policy + `parallel_dev_pick.json` v1 | T-006 |
| AC-5 Resource guard (system-wide cap + lockfile) | T-007 |
| AC-6 Execute steps 25-28 + lib integration | T-008 |
| AC-7 Backward compat (zero change when off) + tests | T-009, T-010 |
| AC-8 Parity `--scope=sovereign-parallel-dev` + runbook | T-011 |

## Tranche order (A→E)

| Tranche | Title | Tasks |
|---------|-------|-------|
| A | Keys + reason codes | T-001 |
| B | Worktree lib | T-002, T-003 |
| C | Selection + anti-slop | T-004, T-005 |
| D | Merge + resource guard + execute steps | T-006, T-007, T-008 |
| E | Tests + parity + runbook | T-009, T-010, T-011 |

## Tasks

- [ ] **T-001** Scratchpad keys (AC-1): append `SOVEREIGN_PARALLEL_DEV=0`, `AUTO_SOVEREIGN_PARALLEL_N=3`, `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL=6`, `AUTO_SOVEREIGN_MERGE_RESOLVE=first_pass_wins`, `AUTO_SOVEREIGN_WORKTREE_KEEP=0`, `AUTO_SOVEREIGN_PARALLEL_QA=0` + optional `AUTO_SOVEREIGN_PARALLEL_MODEL_<idx>`, `AUTO_SOVEREIGN_PARALLEL_LENS_<idx>` to `.cursor/scratchpad.md` + template mirror. Reason code inventory: `PARALLEL_DEV_*` family. Default-off = zero overhead.

- [ ] **T-002** Worktree isolation lib (AC-2): create `parallel_dev_arbiter_lib.py` — `create_worktree(story_id, instance_idx)`, `list_worktrees()`, `remove_worktree()`. Deterministic naming `.git/worktrees/us0108-<story_id>-<instance_idx>/`; per-worktree `GIT_DIR` + `GIT_WORK_TREE` env; gitignore `.git/worktrees/us0108-*` in template. No shared lock conflicts.

- [ ] **T-003** Worktree cleanup post-merge (AC-2): winner promote, loser delete per `AUTO_SOVEREIGN_WORKTREE_KEEP`. Fail-open `PARALLEL_DEV_WORKTREE_CLEANUP_FAILED` on errors. After T-008 (steps 25-28).

- [ ] **T-004** Selection predicate (AC-3): `select_winner(qa_results[])` — filter `qa_verdict=PASS` → sort `-anti_slop_score` → tie-break earliest `proof_issued_at`. Deterministic single winner. v1 sequential N QA; optional `AUTO_SOVEREIGN_PARALLEL_QA=1` parallel v2.

- [ ] **T-005** Anti-slop score reader (AC-3): read-only extract `anti_slop_score` from sprint `qa-findings.md` or `sovereign_critic_findings.jsonl`; graceful degrade default `0` when US-0104 absent. Compose: US-0104 schema UNCHANGED (read-only).

- [ ] **T-006** Merge policy + `parallel_dev_pick.json` v1 (AC-4): `AUTO_SOVEREIGN_MERGE_RESOLVE`: `first_pass_wins` (default), `last_pass_wins`, `manual` → halt. Write-once artifact `handoffs/parallel_dev_pick.json` v1 schema `{schema_version:1, story_id, winner_instance_id, worktree_path, qa_verdict, anti_slop_score, proof_issued_at, merge_policy, runner_ts_utc, orchestrator_run_id, loser_instance_ids[]}`. Bounded conflict retry ≤2 then `PARALLEL_DEV_MERGE_CONFLICT` halt.

- [ ] **T-007** Resource guard (AC-5): atomic lockfile `.git/us0108_parallel_dev.lock`; `acquire_parallel_slot()` / `release_parallel_slot()`. System-wide cap `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL`. Fail-fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED`. Release on instance exit.

- [ ] **T-008** Execute steps 25-28 (AC-6): step 25 spawn N dev → step 26 QA cross-review → step 27 selection via T-004 → step 28 merge+cleanup via T-003. After US-0107 step 24; after US-0047 step 22. Integrate T-002 (worktree), T-006 (merge), T-007 (resource guard).

- [ ] **T-009** Backward compat guard (AC-7): `SOVEREIGN_PARALLEL_DEV=0` path — zero behavior change; no worktrees; no parallel QA; no pick JSON; no resource guard; US-0047/US-0092 semantics unchanged. Regression test `test_us0108_backward_compat_single_dev_unchanged`. Compose: US-0047/US-0092 UNCHANGED.

- [ ] **T-010** Eight contract tests (AC-7): create `tests/us0108_contract_test.py` with `test_us0108_scratchpad_keys_literals`, `test_us0108_worktree_isolation`, `test_us0108_selection_determinism`, `test_us0108_merge_and_pick_schema`, `test_us0108_resource_cap`, `test_us0108_execute_steps_25_28`, `test_us0108_backward_compat_single_dev_unchanged`, `test_us0108_parity_scope`.

- [ ] **T-011** Parity + runbook (AC-8): `scripts/check_intake_template_parity.py --scope=sovereign-parallel-dev` with `SOVEREIGN_PARALLEL_DEV_PAIRS` (scratchpad keys + arbiter lib + template lib + template gitignore + contract tests + pick JSON schema). Append § "Parallel Instance Arbitrage" to `docs/engineering/runbook.md`.

## Compose guards (non-negotiable)

| Story | Compose rule |
|-------|--------------|
| US-0047 | Bulk execute step 22 unchanged; US-0108 system-wide cap checked **after** bulk cap evaluation. |
| US-0092 | Full autonomy outer driver unchanged; parallel dev is execute-phase internal. |
| US-0103 | Ledger schema unchanged; US-0108 reads `handoffs/sovereign_decisions/*.jsonl` only. |
| US-0104 | Critic schema unchanged; US-0108 reads `anti_slop_score` from sprint `qa-findings.md` only. |
| US-0107 | Deferral register schema unchanged; US-0108 may append winner/loser outcome rows as consumer. |
