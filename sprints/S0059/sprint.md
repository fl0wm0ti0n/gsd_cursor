# Sprint S0059

- Story: `US-0080`
- Goal: **Token-cost hardening** — measurable **`cache_read_tokens`** / **`input_tokens`** / **`output_tokens`** / **`phase_call_count`** baselines (**AC-1**), **≥50%** reduction on comparable runs via **`run_class_hash`** (**AC-2**), command/rule slimming with **active + `template/`** parity manifest (**AC-3**, **AC-9**), bounded phase-context without weakening **US-0048** / **US-0056** / **US-0069** / **US-0039** (**AC-4**, **AC-5**), append-only **`handoffs/token_cost_runs/*`** + **`token_cost_evidence_ref`** (**AC-6**), operator guidance (**AC-7**), regression tests (**AC-8**), **DEC-0062** / **`# US-0080`** traceability closure (**AC-10**).
- Status: **Verify-work complete (qa)** — **`T-001..T-010`** **done**; **`/qa`** **PASS**; **`/verify-work`** **PASS** **`2026-03-29`**; story **`US-0080`** **`DONE`** (**US-0045**); **`handoffs/release_queue.md`** **`S0059`** **`ready`**; plan-verify **`sprints/S0059/plan-verify.json`** **PASS** preserved; **next**: **`/release`**.

## Scope

- **AC-1** — Canonical metric fields + per-run/per-phase capture per **`DEC-0062`** §1; **`phase_call_count`** per canonical **`phase_id`**.
- **AC-2** — Baseline vs target on **same `run_class_hash`**; **`TOKEN_COST_RUN_CLASS_MISMATCH`** for invalid comparisons; gates unchanged.
- **AC-3** — Slim **`.cursor/commands/`** (orchestration-heavy) and related policy surfaces; deterministic **active/`template/`** parity via manifest.
- **AC-4** — Bounded phase-context inputs; **no** removal of mandatory isolation / strict-proof / role / release fields from governed surfaces.
- **AC-5** — **`/auto`** and quality/safety contracts unchanged (**US-0048**, **US-0056**, **US-0069**, **US-0039**).
- **AC-6** — Append-only **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** (or **`.jsonl`**) + **`token_cost_evidence_ref`** on **`state.md`** when metrics exist.
- **AC-7** — **README** + **`docs/engineering/runbook.md`**: fresh chat boundaries, explicit **`start-from`**, **`TOKEN_PROFILE`** selection.
- **AC-8** — Regression tests: post-slimming command behavior + artifact contracts; optional metric / **`run_class_hash`** fixture validation.
- **AC-9** — Versioned parity manifest (**DEC-0062** §5) + CI parity beyond scratchpad-only where listed paths differ.
- **AC-10** — Operator surfaces + **`docs/engineering/decisions.md`** index cite **`DEC-0062`** + **`architecture.md`** **`# US-0080`** (DEC authoritative; sprint completes citations).

## Governance

- **`decisions/DEC-0062.md`**
- **`docs/engineering/architecture.md`** **`# US-0080`**
- **`docs/engineering/research.md`** **`R-0057`**
- Related: **`DEC-0052`** (run-class **`resolved_phase_plan`**), **`US-0053`** (token profile), **`US-0030`** (parity), **`US-0039`** (release chain)
