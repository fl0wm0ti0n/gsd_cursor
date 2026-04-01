# Sprint S0059 Tasks

- Story: `US-0080`
- Sprint: `S0059`
- Governance: **`DEC-0062`**; **`architecture.md`** **`# US-0080`**; **`R-0057`**; **`US-0045`** / **`US-0030`** parity

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Implement per-run and per-phase metric capture using **`DEC-0062`** §1 literals (`cache_read_tokens`, `input_tokens`, `output_tokens`, `phase_call_count`, optional `cache_creation_tokens` / `orchestrator_call_estimate`) with `metric_source` mapping rules | AC-1 |
| T-002 | done | Baseline + target harness: record **`run_class_hash`** (sorted-key JSON SHA-256 per **DEC-0062** §2); compare **only** same-hash runs for **50%** `cache_read_tokens` claim; emit **`TOKEN_COST_RUN_CLASS_MISMATCH`** when violated | AC-2 |
| T-003 | done | Slim orchestration-heavy **`.cursor/commands/`** (and related governed surfaces as needed); maintain **active + `template/`** equivalence for touched paths per **DEC-0062** §5–§6 | AC-3 |
| T-004 | done | Apply bounded phase-context / handoff contracts: remove redundancy only where parity manifest proves equivalence; **no** stripping **US-0048** / **US-0056** / **US-0069** / **US-0039** mandatory fields | AC-4 |
| T-005 | done | Verify **`/auto`** command text and role/phase gates remain semantically intact after slimming (spot-diff + contract checklist vs **DEC-0029**, **DEC-0038**, **DEC-0051**, **DEC-0052**) | AC-5 |
| T-006 | done | Create append-only **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** (or **`.jsonl`**) schema; wire **`token_cost_evidence_ref`** on **`docs/engineering/state.md`** checkpoints when metrics recorded | AC-6 |
| T-007 | done | Document operator low-cost patterns in **`README.md`** and **`docs/engineering/runbook.md`** (fresh context, **`start-from`**, **`TOKEN_PROFILE`**, evidence file location) | AC-7 |
| T-008 | done | Add regression tests for slimmed commands/rules (behavior + artifact contracts) and optional metric / **`run_class_hash`** validator or fixtures per **`architecture.md`** tests strategy | AC-8 |
| T-009 | done | Author versioned **token-cost parity manifest** + extend CI parity checks for manifest-listed command/rule/template paths (**DEC-0062** §5) | AC-9 |
| T-010 | done | **AC-10 closure**: index + operator traceability — **`docs/engineering/decisions.md`**, sprint summary, handoffs explicitly cite **`DEC-0062`** + **`# US-0080`** + **§6** trade-off table | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005
- AC-6 → T-006
- AC-7 → T-007
- AC-8 → T-008
- AC-9 → T-009
- AC-10 → T-010
