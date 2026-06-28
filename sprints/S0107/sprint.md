# Sprint S0107

## Metadata

- **sprint_id**: S0107
- **story_refs**: US-0107
- **goal**: Ship **sovereign loop mode** — default-off **`AUTO_SOVEREIGN`** scratchpad gate, **`handoffs/sovereign_deferrals.jsonl`** deferral register v1, **`scripts/sovereign_loop_lib.py`** advance/drain-generate/notification API + **`SovereignLoopStepResult`**, **`scripts/sovereign_loop_validate.py`** validator CLI, drain-generate PO spawn + mandatory decision gate per candidate, ntfy/hook notification adapters (fail-open), **US-0110** convergence compose via **`list_open_deferrals()`**, eight **`test_us0107_*`** contract markers + compose guards, **`SOVEREIGN_LOOP_PAIRS`** parity manifest, and runbook § Sovereign Loop Mode — per **DEC-0107** (composes **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** / **US-0105** / **US-0110** additive only; research **R-0094**).
- **status**: planned
- **created_at**: 2026-06-29T00:18:00Z
- **orchestrator_run_id**: auto-20260628-04
- **fresh_context_marker**: tl-S0107-sprint-plan-20260629T001800Z-fresh

## Scope

- **US-0107**: Sovereign Loop Mode — deferral register + drain-generate + notification + convergence hooks
- **Architecture**: `docs/engineering/architecture.md` `# US-0107`
- **Binding decision**: `decisions/DEC-0107.md` (Accepted 2026-06-29)
- **Research anchor**: `docs/engineering/research.md` `R-0094` (closed Q1–Q7)

## Non-goals (hard, from DEC-0107 / architecture `# US-0107`)

- No amendment of **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0103** / **US-0110** — compose, do not amend.
- No always-on sovereign loop — default **`AUTO_SOVEREIGN=0`**; zero overhead when off.
- No auto-enable **`SOVEREIGN_GOAL_MODE=goal_convergence`** when sovereign on — fail-closed **`SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`**.
- No auto-append drain candidates without decision gate — mandatory per candidate.
- No deploy smoke logic — **US-0109** owns **`DEPLOY_DEFERRED`** writer (integration declaration only).
- No email SMTP v1 — ntfy/hook only; email deferred stub.
- No empty tracked JSONL seed — create-on-first-write; `.gitkeep` only.
- **Status authority (US-0045)**: US-0107 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0107**; architecture `# US-0107`; research **R-0094** (closed); research stub **`scripts/sovereign_loop_lib.py`**
- **Governance stack**: **US-0088** (quiet mode — unchanged), **US-0092** (outer driver — unchanged), **US-0095** (native-chain segments — unchanged), **US-0044** / **US-0087** (drain mutex — unchanged), **US-0103** (optional `ledger_decision_id` provenance — ledger schema unchanged), **US-0105** (drain-generate reads `build_injection_digest` only), **US-0110** (import `evaluate_convergence` — do not amend DEC-0110), **US-0109** (downstream `DEPLOY_DEFERRED` writer — schema stable first), **US-0069** (spawn-only PO for drain-generate), **US-0017** (template parity), **US-0045** (status authority)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 12 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | Scratchpad keys `AUTO_SOVEREIGN_*` + `SOVEREIGN_NOTIFY_*` + zero-overhead when `0`; goal-mode coupling when `1` | T-001, T-002 | § Scratchpad keys |
| AC-2 | Deferral register JSONL v1 schema + bounded queue + CRUD API + validator CLI | T-003, T-004, T-006 | § Deferral register JSONL v1 |
| AC-3 | `advance_sovereign_loop` orchestrator advance + deferral policy + US-0110 compose | T-004, T-005, T-009 | § Advance algorithm |
| AC-4 | Drain-generate PO spawn + `DrainGenerateCandidateBundle` + decision gate per candidate | T-007 | § Drain-generate contract |
| AC-5 | Notification dispatch on convergence/timeout/caps; fail-open adapters | T-008 | § Notification dispatch |
| AC-6 | US-0109 integration point declaration (`DEPLOY_DEFERRED` → register); no deploy smoke | T-009, T-012 | § US-0109 integration |
| AC-7 | Eight `test_us0107_*` markers + `SOVEREIGN_LOOP_PAIRS` parity `--scope=sovereign-loop` | T-006, T-010, T-011 | § Contract tests + parity |
| AC-8 | Reason codes, compose guards, backward compat; architecture `# US-0107` pre-satisfied | T-002, T-010, T-012 | § Reason codes; § Backward compatibility |

**Multi-AC tasks** (justified by architecture `# US-0107` § Atomic task seeds): **T-002** (AC-1+AC-8), **T-004** (AC-2+AC-3), **T-009** (AC-3+AC-6), **T-012** (AC-6+AC-8). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

**AC-8 architecture pre-satisfied** at `/architecture` (`# US-0107` written in architecture phase).

## Task count

- **Total**: 12
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (12 ≤ 12; at threshold — `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **strict 1:1 task-to-seed** (12 architecture seeds → T-001..T-012)

## Governance

- **DEC-0107** (binding) — each task cites governing architecture §(s) and DEC §(s).
- **R-0094** (research anchor — closed).
- **US-0110** compose — wire `list_open_deferrals()` for `zero_deferrals`; do not amend DEC-0110.
- **US-0045** canonical status authority (US-0107 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/scratchpad.md` | `template/.cursor/scratchpad.md` | T-001, T-002 | Positive |
| 2 | `docs/engineering/reason_codes.md` | (active-only) | T-002 | N/A |
| 3 | `decisions/DEC-0107.md` | `template/decisions/DEC-0107.md` | T-002 | Positive |
| 4 | `handoffs/sovereign_deferrals/.gitkeep` | `template/handoffs/sovereign_deferrals/.gitkeep` | T-003 | Positive |
| 5 | `scripts/sovereign_loop_lib.py` | `template/scripts/sovereign_loop_lib.py` | T-004, T-005, T-007, T-008 | Positive |
| 6 | `scripts/sovereign_loop_validate.py` | `template/scripts/sovereign_loop_validate.py` | T-006 | Positive |
| 7 | `tests/us0107_contract_test.py` | (active-only) | T-010 | N/A |
| 8 | `scripts/check_intake_template_parity.py` | `template/scripts/check_intake_template_parity.py` | T-011 | Positive |
| 9 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-012 | Positive |

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** amend **US-0088** / **US-0092** / **US-0095** / **US-0044** / **US-0110** base semantics.
- Do **not** enable sovereign loop by default — `AUTO_SOVEREIGN=0` is zero-overhead discipline.
- Do **not** auto-enable goal mode when sovereign on.
- Do **not** auto-append drain candidates without decision gate.
- Do **not** implement US-0109 deploy smoke in this sprint.

## Post-edit gate sequence (architecture § Contract tests)

1. `pytest -k us0107` → all eight subtests + compose guards green
2. `python scripts/sovereign_loop_lib.py --self-test` → `[SOVEREIGN_LOOP_SELF_TEST_OK]`
3. `python scripts/sovereign_loop_validate.py --self-test` → `[SOVEREIGN_LOOP_VALIDATION_OK]`
4. `python scripts/check_intake_template_parity.py --scope=sovereign-loop` → PASS (**`SOVEREIGN_LOOP_PAIRS`**)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Tranche A — scratchpad keys + reason codes + bootstrap (T-001..T-003)

- Nine **`AUTO_SOVEREIGN_*`** + **`SOVEREIGN_NOTIFY_*`** keys in active + template scratchpad (byte-parity)
- Comment block documenting default-off, goal-mode coupling, deferral policy, notification targets
- 12 reason codes in `docs/engineering/reason_codes.md` § US-0107
- **`DEC-0107`** template mirror
- `handoffs/sovereign_deferrals/.gitkeep` + sidecar `sovereign_loop_state.json` v1 contract

### Tranche B — deferral lib core (T-004)

- Finalize **`sovereign_loop_lib.py`** deferral CRUD from research stub: `list_open_deferrals`, `append_deferral`, `resolve_deferral`, `schema_check_deferral`, secret scan, `self_test`

### Tranche C — advance + validator (T-005, T-006)

- `advance_sovereign_loop` + `SovereignLoopStepResult` bodies
- **`scripts/sovereign_loop_validate.py`** + template mirror

### Tranche D — drain-generate + notify + compose (T-007, T-008, T-009)

- `build_drain_generate_spawn_inputs` + bundle schema + `/auto` PO spawn + decision gate wiring
- `dispatch_notification` ntfy/hook adapters (fail-open; email defer stub)
- US-0110 `zero_deferrals` compose via `list_open_deferrals()` (no DEC-0110 amend)

### Tranche E — contract tests + parity + runbook (T-010, T-011, T-012)

- Eight **`test_us0107_*`** contract markers + compose regression guards in `tests/us0107_contract_test.py`
- **`SOVEREIGN_LOOP_PAIRS`** parity scope `--scope=sovereign-loop`
- Runbook § Sovereign Loop Mode + US-0109 `DEPLOY_DEFERRED` integration declaration

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Goal-mode coupling | Fail-closed + operator recipe in T-012 runbook |
| R2 | Drain-generate scope creep | 3-candidate cap + mandatory decision gate in T-007 |
| R3 | Deferral cap vs convergence | Shared `list_open_deferrals()` in T-004/T-009 |
| R4 | Notification secrets | Local-only config documented in T-012 |
| R5 | Sovereign terminal vs native segments | Additive stops only; regression test in T-010 |
| R6 | US-0109 ordering | Stable deferral schema in T-003/T-006 before US-0109 |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-012).
- `sprints/S0107/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=12`, `within_limit=true`.
- `pytest -k us0107` green; parity **`--scope=sovereign-loop`** PASS.
- `python scripts/sovereign_loop_lib.py --self-test` → `[SOVEREIGN_LOOP_SELF_TEST_OK]`.
- `python scripts/sovereign_loop_validate.py --self-test` → `[SOVEREIGN_LOOP_VALIDATION_OK]`.
- Active/template byte-parity verified for all `SOVEREIGN_LOOP_PAIRS`.
- `docs/product/backlog.md` **`## US-0107`** retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release` (**US-0045**).

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0107`** / **US-0107** — verify AC-1..AC-8 ↔ T-001..T-012 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0107/plan-verify.json` **`PENDING`** → **`PASS`**.
