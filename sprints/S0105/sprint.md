# Sprint S0105

## Metadata

- **sprint_id**: S0105
- **story_refs**: US-0105
- **goal**: Ship **sovereign memory** — default-off **`SOVEREIGN_MEMORY`** scratchpad gate, **`docs/engineering/sovereign-memory/`** JSONL substrate (decisions-log, mistakes, patterns, plan-drift-register + sprint retrospectives), bounded top-N/top-K char-capped injection via **`scripts/sovereign_memory_lib.py`**, **`scripts/sovereign_memory_validate.py`** validator CLI, phase spawn **`sovereign_memory_digest`** hook, curator retrospective + optional ledger promotion, dedup + mistake-tagging hooks, JSONL archive rollover, eight **`test_us0105_*`** contract markers, **`SOVEREIGN_MEMORY_PAIRS`** parity manifest, and runbook operator recipes — per **DEC-0105** (composes **US-0029** / **US-0080** / **US-0103** / **US-0072** / **US-0096** additive only; research **R-0093**).
- **status**: planned
- **created_at**: 2026-06-29T00:08:00Z
- **orchestrator_run_id**: auto-20260628-04
- **fresh_context_marker**: tl-S0105-sprint-plan-20260629T000800Z-fresh

## Scope

- **US-0105**: Sovereign Memory — project-level learnings substrate + bounded injection
- **Architecture**: `docs/engineering/architecture.md` `# US-0105`
- **Binding decision**: `decisions/DEC-0105.md` (Accepted 2026-06-29)
- **Research anchor**: `docs/engineering/research.md` `R-0093` (closed Q1–Q7)

## Non-goals (hard, from DEC-0105 / architecture `# US-0105`)

- No amendment of **US-0029** / **US-0080** / **US-0103** / **US-0072** / **US-0096** base semantics — compose, do not amend.
- No always-on memory — default **`SOVEREIGN_MEMORY=0`**; zero overhead when off.
- No empty tracked JSONL seed files — create-on-first-write; `.gitkeep` only.
- No retrospective injection v1 — `retrospectives/<sprint_id>.md` is human audit only.
- No triad hot-surface changes — sovereign-memory excluded from **US-0072** archives.
- No conflation of per-run ledger with `decisions-log.jsonl`.
- **US-0107** drain-generate orchestration out of scope (read API stability only).
- **Status authority (US-0045)**: US-0105 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0105**; architecture `# US-0105`; research **R-0093** (closed); research stub **`scripts/sovereign_memory_lib.py`**
- **Governance stack**: **US-0029** (external research — unchanged), **US-0080** / **DEC-0062** (token-cost — lib-side digest only), **US-0103** (per-run ledger — optional promotion hook), **US-0072** / **DEC-0054** (triad — sovereign-memory excluded), **US-0096** (lean memory layers — distinct substrate), **US-0023** (fresh-context — digest is read-only additive), **US-0107** (read API consumer — stable lib surface), **US-0017** (template parity), **US-0045** (status authority)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 11 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Scratchpad keys `SOVEREIGN_MEMORY_*` (5 keys) + defaults + zero-overhead when `0` | T-001, T-002 | § Scratchpad keys |
| AC-2 | Directory `docs/engineering/sovereign-memory/` + four JSONL families + retrospectives + v1 schemas | T-003, T-006 | § Directory surface; § JSONL v1 schemas |
| AC-3 | `sovereign_memory_lib.py` bounded injection API: top-N recent + top-K high-impact + char cap | T-004 | § Injection merge algorithm |
| AC-4 | Phase spawn `sovereign_memory_digest` block when enabled (US-0023-safe additive) | T-007 | § Phase spawn hook |
| AC-5 | Curator `/refresh-context` retrospective + optional `promote_from_ledger` | T-005, T-009 | § Curator retrospective + ledger promotion |
| AC-6 | Dedup via `decision_key` + mistake-tagging hooks on fix-fail/revert/fidelity | T-005, T-008 | § Dedup + mistake-tagging |
| AC-7 | Eight `test_us0105_*` markers + `SOVEREIGN_MEMORY_PAIRS` parity scope | T-010, T-011 | § Contract tests + parity |
| AC-8 | Reason codes, validator, runbook, compose guards; architecture `# US-0105` pre-satisfied | T-002, T-006, T-010, T-011 | § Reason codes; § Backward compatibility |

**Multi-AC tasks** (justified by architecture `# US-0105` § Atomic task seeds): **T-002** (AC-1+AC-8), **T-005** (AC-5+AC-6), **T-006** (AC-2+AC-8), **T-011** (AC-7+AC-8). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

**AC-8 architecture pre-satisfied** at `/architecture` (`# US-0105` written in architecture phase).

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011)

## Governance

- **DEC-0105** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0093** (research anchor — closed).
- **US-0103** compose — per-run ledger unchanged; optional promotion at refresh-context.
- **US-0045** canonical status authority (US-0105 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-001, T-002 | Positive |
| 2 | `docs/engineering/reason_codes.md` | (active-only) | T-002 | N/A |
| 3 | `decisions/DEC-0105.md` | `template/decisions/DEC-0105.md` | T-002 | Positive |
| 4 | `docs/engineering/sovereign-memory/.gitkeep` | `template/docs/engineering/sovereign-memory/.gitkeep` | T-003 | Positive |
| 5 | `scripts/sovereign_memory_lib.py` | `template/scripts/sovereign_memory_lib.py` | T-004, T-005 | Positive |
| 6 | `scripts/sovereign_memory_validate.py` | `template/scripts/sovereign_memory_validate.py` | T-006 | Positive |
| 7 | `tests/us0105_contract_test.py` | (active-only) | T-010 | N/A |
| 8 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-011 | Positive |
| 9 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-011 | Positive |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** amend **US-0029** / **US-0080** / **US-0103** / **US-0072** / **US-0096** base semantics.
- Do **not** enable memory by default — `SOVEREIGN_MEMORY=0` is zero-overhead discipline.
- Do **not** inject retrospectives v1.
- Do **not** conflate per-run ledger with `decisions-log.jsonl`.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0105` → all eight subtests + compose guards green
2. `python scripts/sovereign_memory_lib.py --self-test` → `[SOVEREIGN_MEMORY_SELF_TEST_OK]`
3. `python scripts/sovereign_memory_validate.py --self-test` → `[SOVEREIGN_MEMORY_VALIDATION_OK]`
4. `python scripts/check_intake_template_parity.py --scope=sovereign-memory` → PASS (**`SOVEREIGN_MEMORY_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — scratchpad keys + reason codes + directory (T-001..T-003)

- Five **`SOVEREIGN_MEMORY_*`** keys in active + template scratchpad (byte-parity)
- Comment block documenting default-off + top-N/top-K/char-cap/rollover semantics
- 8 reason codes in `docs/engineering/reason_codes.md` § US-0105
- **`DEC-0105`** template mirror
- Directory `.gitkeep` + `retrospectives/.gitkeep` bootstrap

### Tranche B — lib read/injection core (T-004)

- Finalize **`sovereign_memory_lib.py`** read/injection core from research stub: schemas, `build_injection_digest`, `read_entries`, `schema_check`, `scan_secrets`, `self_test`

### Tranche C — lib mutations + validator (T-005, T-006)

- Append/dedup/rollover/promotion/retrospective bodies in **`sovereign_memory_lib.py`**
- **`scripts/sovereign_memory_validate.py`** + template mirror

### Tranche D — spawn hook + mistake-tagging + curator (T-007, T-008, T-009)

- Phase spawn `sovereign_memory_digest` block integration (US-0023-safe additive)
- Mistake-tagging hooks: `/auto` fix-fail, `/execute` revert, fidelity compose **US-0103**
- `/refresh-context` curator retrospective + `promote_from_ledger` wiring

### Tranche E — contract tests + parity + runbook (T-010, T-011)

- Eight **`test_us0105_*`** contract markers + compose regression guards in `tests/us0105_contract_test.py`
- **`SOVEREIGN_MEMORY_PAIRS`** parity scope `--scope=sovereign-memory`
- Runbook `### Sovereign Memory (US-0105)` + zero-overhead default-off path

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Token bloat | Char cap + tail read + lib-side digest in T-004 |
| R2 | Research vs learnings overlap | `provenance_ref` only; compose guard in T-010 |
| R3 | Ledger vs decisions-log confusion | Distinct schemas + runbook table in T-011 |
| R4 | Stale injection | `status` supersession on all entries in T-004 |
| R5 | Secret leakage | `SOVEREIGN_MEMORY_SECRET_DETECTED` in T-004 |
| R6 | **US-0107** read API coupling | Stable lib surface; `schema_version` in T-004 |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-011).
- `sprints/S0105/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0105` green; parity **`--scope=sovereign-memory`** PASS.
- `python scripts/sovereign_memory_lib.py --self-test` → `[SOVEREIGN_MEMORY_SELF_TEST_OK]`.
- `python scripts/sovereign_memory_validate.py --self-test` → `[SOVEREIGN_MEMORY_VALIDATION_OK]`.
- Active/template byte-parity verified for all `SOVEREIGN_MEMORY_PAIRS`.
- `docs/product/backlog.md` **`## US-0105`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release` (**US-0045**).

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0105`** / **US-0105** — verify AC-1..AC-8 ↔ T-001..T-011 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0105/plan-verify.json` **`PENDING`** → **`PASS`**.
