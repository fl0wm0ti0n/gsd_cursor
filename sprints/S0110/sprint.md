# Sprint S0110

## Metadata

- **sprint_id**: S0110
- **story_refs**: US-0110
- **goal**: Ship **goal-based convergence loops** — default-off **`SOVEREIGN_GOAL_MODE`** scratchpad gate, **`scripts/sovereign_convergence_lib.py`** five-conjunct **`evaluate_convergence`** predicate + vision auto-derive, **`scripts/sovereign_convergence_validate.py`** validator CLI, curator **`goal_progress`** block in **`handoffs/resume_brief.md`**, iteration-timeout partial-delivery report, eight **`test_us0110_*`** contract markers, **`SOVEREIGN_CONVERGENCE_PAIRS`** parity manifest, and runbook operator recipes — per **DEC-0110** (composes **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** read-only; research **R-0091**).
- **status**: planned
- **created_at**: 2026-06-28T18:30:00Z
- **orchestrator_run_id**: auto-20260628-04
- **fresh_context_marker**: tl-S0110-US0110-sprint-plan-20260628T183000Z-fresh

## Scope

- **US-0110**: Goal-Based Convergence Loops — sovereign-loop terminal condition + mid-loop progress visibility + partial delivery on timeout
- **Architecture**: `docs/engineering/architecture.md` `# US-0110`
- **Binding decision**: `decisions/DEC-0110.md` (Accepted 2026-06-28)
- **Research anchor**: `docs/engineering/research.md` `R-0091` (closed Q1–Q7)

## Non-goals (hard, from DEC-0110 / architecture `# US-0110`)

- No amendment of **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** — compose, do not amend.
- No always-on convergence — default **`SOVEREIGN_GOAL_MODE=phase_driven`**; zero overhead when off.
- No wall-clock timeout v1 — iteration count only; default **`SOVEREIGN_GOAL_TIMEOUT_MAX=0`** (disabled).
- No **US-0109** post-deploy smoke as convergence conjunct — canonical chain locked to **US-0093** (`tests/report.md` + sprint `uat.json`).
- No writes to composed story surfaces — read-only backlog/deferral/critic/smoke/ledger consumption.
- **Status authority (US-0045)**: US-0110 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0110**; architecture `# US-0110`; research **R-0091** (closed)
- **Governance stack**: **US-0088** (quiet mode — unchanged), **US-0092** (outer driver — unchanged), **US-0095** (native-chain segments — unchanged), **US-0044** (backlog drain — unchanged), **US-0103** (ledger read-only via `decision_ledger_lib.read_entries`), **US-0107** (downstream consumer — out of scope for this sprint), **US-0017** (template parity), **US-0045** (status authority), **US-0093** (smoke canonical chain)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 11 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Scratchpad keys `SOVEREIGN_GOAL_MODE`, `SOVEREIGN_GOAL`, `SOVEREIGN_GOAL_TOP_N`, `SOVEREIGN_GOAL_MAX_CHARS`, `SOVEREIGN_GOAL_TIMEOUT_MAX` + defaults | T-001, T-002 | § Scratchpad keys |
| AC-2 | `evaluate_convergence` contract + five-conjunct predicate + degrade matrix + memoization | T-003, T-004, T-006 | § ConvergenceResult; § Five-conjunct predicate; § Validator CLI |
| AC-3 | Explicit goal wins + vision top-N auto-derive + `SOVEREIGN_GOAL_DERIVE_FAILED` | T-005 | § Vision auto-derive algorithm |
| AC-4 | Curator `goal_progress` JSON block in `resume_brief.md` | T-007 | § goal_progress block schema |
| AC-5 | `SOVEREIGN_GOAL_TIMEOUT` + `handoffs/sovereign_partial_delivery.md` sections | T-008 | § Helper library; § Partial-delivery |
| AC-6 | Eight `test_us0110_*` contract markers + `SOVEREIGN_CONVERGENCE_PAIRS` parity | T-009, T-010 | § Contract tests + parity |
| AC-7 | `phase_driven` zero-overhead + compose regression vs US-0088/US-0092/US-0095/US-0044 | T-011 | § Backward compatibility; § Integration points |
| AC-8 | Reason codes, validator, parity, runbook; architecture `# US-0110` pre-satisfied | T-002, T-006, T-010, T-011 | § Reason codes; § Validator CLI; § Runbook |

**Multi-AC tasks** (justified by architecture `# US-0110` § Atomic task seeds): **T-002** (AC-1+AC-8), **T-006** (AC-2+AC-8), **T-009** (AC-6), **T-010** (AC-6+AC-8), **T-011** (AC-7+AC-8). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

**AC-8 architecture pre-satisfied** at `/architecture` (`# US-0110` written in architecture phase).

## Task count

- **Total**: 11
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (11 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (11 architecture seeds → T-001..T-011)

## Governance

- **DEC-0110** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0091** (research anchor — closed).
- **US-0103** compose — ledger read-only via `decision_ledger_lib.read_entries(last_n=100)`; no ledger writes.
- **US-0045** canonical status authority (US-0110 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-001, T-002 | Positive |
| 2 | `docs/engineering/reason_codes.md` | (active-only) | T-002 | N/A |
| 3 | `scripts/sovereign_convergence_lib.py` | `template/scripts/sovereign_convergence_lib.py` | T-003..T-008 | Positive |
| 4 | `scripts/sovereign_convergence_validate.py` | `template/scripts/sovereign_convergence_validate.py` | T-006 | Positive |
| 5 | `.cursor/commands/refresh-context.md` | `template/.cursor/commands/refresh-context.md` | T-007 | Positive |
| 6 | `handoffs/resume_brief.md` | (active-only emission target) | T-007 | N/A |
| 7 | `handoffs/sovereign_partial_delivery.md` | (active-only runtime artifact) | T-008 | N/A |
| 8 | `tests/us0110_contract_test.py` | (active-only) | T-009 | N/A |
| 9 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-010 | Positive |
| 10 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-011 | Positive |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** amend **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** semantics.
- Do **not** enable convergence by default — `SOVEREIGN_GOAL_MODE=phase_driven` is zero-overhead discipline.
- Do **not** write to composed surfaces (backlog, deferrals, critic, smoke, ledger).
- Do **not** use wall-clock timeout or **US-0109** deploy smoke as v1 conjunct.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0110` → all eight subtests green
2. `python scripts/sovereign_convergence_lib.py --self-test` → `[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]`
3. `python scripts/sovereign_convergence_validate.py --self-test` → `[SOVEREIGN_CONVERGENCE_VALIDATION_OK]`
4. `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` → PASS (**`SOVEREIGN_CONVERGENCE_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — scratchpad keys + reason codes (T-001..T-002)

- Five **`SOVEREIGN_GOAL_*`** keys in active + template scratchpad (byte-parity)
- Comment block documenting default-off + iteration-count timeout semantics
- 10 reason codes in `docs/engineering/reason_codes.md` § US-0110

### Tranche B — convergence library core (T-003..T-005)

- Finalize **`sovereign_convergence_lib.py`** schemas + `is_goal_convergence_enabled` + `schema_check_*` + `self_test`
- **`evaluate_convergence`** five-conjunct predicate + degrade matrix + mtime memoization
- **`resolve_goal`** vision auto-derive algorithm (explicit wins; `SOVEREIGN_GOAL_DERIVE_FAILED` fail-closed)

### Tranche C — validator CLI (T-006)

- **`scripts/sovereign_convergence_validate.py`** + template mirror
- Flags: `--convergence-json`, `--goal-progress-json`, `--repo`, `--self-test`, `--enforce`

### Tranche D — progress + partial delivery (T-007..T-008)

- **`build_goal_progress_block`** + curator `/refresh-context` emission under `### goal_progress`
- **`write_partial_delivery_report`** + **`check_timeout`** (`SOVEREIGN_GOAL_TIMEOUT`)

### Tranche E — contract tests + parity + runbook (T-009..T-011)

- Eight **`test_us0110_*`** contract markers in `tests/us0110_contract_test.py`
- **`SOVEREIGN_CONVERGENCE_PAIRS`** parity scope `--scope=sovereign-convergence`
- Runbook `### Goal-Based Convergence (US-0110)` + `phase_driven` zero-overhead + compose regression subtests

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Predicate cost on large backlogs | T-004: line-scoped scan + memoization (≤50ms p95) |
| R2 | Upstream artifacts absent (US-0104/US-0107) | T-004: degrade matrix skip semantics locked |
| R3 | Smoke probe ambiguity | T-004: canonical chain `tests/report.md` + sprint `uat.json` only |
| R4 | Native-chain bypass | T-011: `test_us0110_compose_no_stop_matrix_change` regression guard |
| R5 | Timeout semantics | T-008: iteration count; default `0` disabled |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-011).
- `sprints/S0110/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=11`, `within_limit=true`.
- `pytest -k us0110` green; parity **`--scope=sovereign-convergence`** PASS.
- `python scripts/sovereign_convergence_lib.py --self-test` → `[SOVEREIGN_CONVERGENCE_SELF_TEST_OK]`.
- `python scripts/sovereign_convergence_validate.py --self-test` → `[SOVEREIGN_CONVERGENCE_VALIDATION_OK]`.
- `docs/product/backlog.md` **`## US-0110`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release` (**US-0045**).

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0110`** / **US-0110** — verify AC-1..AC-8 ↔ T-001..T-011 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0110/plan-verify.json` **`PENDING`** → **`PASS`**.
