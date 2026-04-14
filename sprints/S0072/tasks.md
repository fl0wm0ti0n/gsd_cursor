# Sprint S0072 Tasks

- **Story**: **`US-0088`**
- **Sprint**: **`S0072`**
- **Governance**: `architecture.md` `# US-0088`; `research.md` `R-0071`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Update **`.cursor/commands/auto.md`**, **`docs/engineering/auto-orchestration-reference.md`**, **`docs/engineering/runbook.md`** (+ **`template/`** mirrors): **continuous `/auto`** semantics, unambiguous **reference Step 5** pointer (vs compact steps), **deterministic stop reasons** for looping runs, **documented outer-driver equivalence** where **AC-1** allows **Option B** | AC-1 |
| T-002 | done | Add **`AUTO_QUIET`** (**default-off**) to **`.cursor/scratchpad.md`** and **`template/`** scratchpad examples; document **non-suppressible** notifications (**AC-2**) and **`TOKEN_PROFILE`** orthogonality (**`DEC-0035`** / **`US-0080`**) | AC-2 |
| T-003 | done | Normative **drain** prose: **`AUTO_BACKLOG_DRAIN=1`** advances through **multiple phases** until **US** / sprint-segment boundary; **recompute** materialized phase plan at story boundary (**`US-0044`**); add/extend **contract-test** substrings for **drain advance** / **reload** / **next OPEN story** per **`# US-0088`** / **`R-0071`** | AC-3 |
| T-004 | done | Extend **`tests/auto_command_contract_test.py`** (and fixtures): **continuation** when policy says continue (**not** one-phase-stop); **reference Step 5** markers; **spawn-only** regression (**`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**) | AC-4 |
| T-005 | done | **`template/`** byte/literal parity pass for every path touched in **T-001..T-004** and **T-002** (**`auto.md`**, reference, runbook, scratchpad) | AC-5 |
| T-006 | done | After doc/test edits, reconcile **`docs/engineering/architecture.md`** **`# US-0088`** (stop matrix, **`AUTO_QUIET`**, drain, **`DEC-0069`**, **`US-0087`** by reference, **`BUG-0006`**) — no drift vs shipped text | AC-6 |
| T-007 | done | **`docs/engineering/runbook.md`** (+ **`template/`**): operator subsection **continuous `/auto` + backlog drain** — caps, pause, decision gates, **`AUTO_QUIET`**, pointer to **reference Step 5** | AC-7 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
