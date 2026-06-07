# Sprint S0084 UAT — US-0095

- **Sprint**: `S0084`
- **Work item**: **US-0095** — Native in-Cursor `/auto` auto-chaining (no outer driver required)
- **Governance**: **DEC-0080** + architecture `# US-0095` + **R-0081**
- **Orchestrator run**: **auto-20260607-02**
- **Machine-readable**: `sprints/S0084/uat.json`
- **Status**: **populated** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0095** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0084/qa-findings.md` (PASS)
- **verify_work_executed_at**: 2026-06-07T22:30:00Z
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0084-US0095-verify-work-20260607T223000Z-fresh`
- **verify_work_verdict**: **PASS** (10/10 UAT steps PASS; 0 FAIL; 0 SKIP)

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 10 |
| FAIL | 0 |
| SKIP | 0 |
| Total | 10 |

Verify-work verdict: **PASS**. Closure preflight: **PASS** (9/9 gates). Story **US-0095** remains **OPEN** per **US-0045**.

## Preconditions

- Python 3.12+ available.
- **DEC-0080** execute deliverables merged (native in-chat auto-chain §, drain-advance algorithm, outer-driver demotion, contract tests).
- `scripts/auto_outer_driver.py` retained (scope guard).

## UAT steps

### UAT-1 — Native in-chat auto-chain (AC-1) — `verdict=PASS`

- **Command**: `pytest -k test_us0095_native_in_chat_auto_chain_markers tests/auto_command_contract_test.py -q`
- **Expected**: Native in-chat auto-chain § in `auto.md` + reference Step 5 IDE-primary; foreground sequential Task loop; `NATIVE_CHAIN_UNAVAILABLE` fail-closed.
- **Evidence**: subtest PASS; `.cursor/commands/auto.md` § **Native in-chat auto-chain (US-0095 / DEC-0080)**.

### UAT-2 — Drain-without-pause IDE (AC-2) — `verdict=PASS`

- **Command**: `pytest -k test_us0095_ide_drain_advance_without_outer_driver tests/auto_command_contract_test.py -q`
- **Expected**: 7-step IDE drain-advance algorithm; literals `immediately`, `without operator re-`/auto``; no mandatory outer-driver prose in IDE-primary native §.
- **Evidence**: subtest PASS; `auto.md` § **IDE drain-advance-without-pause** steps 1–7.

### UAT-3 — Spawn-only preserved (AC-3) — `verdict=PASS`

- **Command**: `pytest -k test_us0095_spawn_only_regression tests/auto_command_contract_test.py -q`
- **Expected**: Spawn-only loop invariants preserved; **US-0069** preflight/post; forbidden in-band patterns absent from native §.
- **Evidence**: subtest PASS; `auto.md` § **Loop invariants (spawn-only — BUG-0006 unchanged)**.

### UAT-4 — Stop matrix hard gates (AC-4) — `verdict=PASS`

- **Check**: manual review of stop matrix in `auto.md` + reference
- **Expected**: Hard stops unchanged: `decision_gate`, isolation/strict-proof violations, security deny, `BACKLOG_MAX_STORIES_REACHED`, `AUTO_LOOP_MAX_CYCLES`, unrecoverable `error`, `pause_request`.
- **Evidence**: stop matrix table present; relaxable transient stops per **DEC-0078** when configured.

### UAT-5 — Outer driver demoted (AC-5) — `verdict=PASS`

- **Commands**: `pytest -k test_us0095_outer_driver_fallback_not_mandatory_ide tests/auto_command_contract_test.py -q`
- **Check**: manual README + runbook review
- **Expected**: Outer driver **optional** / **fallback** for IDE `full_autonomy`; `scripts/auto_outer_driver.py` retained.
- **Evidence**: subtest PASS; README.md L18–19 optional/fallback; runbook § **Native in-chat auto-chain (US-0095)** + primary/fallback boundary table.

### UAT-6 — Operator surface / AUTO_QUIET (AC-6) — `verdict=PASS`

- **Command**: `pytest -k test_us0095_auto_quiet_no_outer_driver_mandatory tests/auto_command_contract_test.py -q`
- **Expected**: `AUTO_QUIET` suppression table; forbidden mandatory outer-driver/re-`/auto`/segment-exhausted wait patterns; gates/caps/errors non-suppressible.
- **Evidence**: subtest PASS; `auto.md` § **`AUTO_QUIET` under native chain**.

### UAT-7 — DEC-0069 pairing (AC-7) — `verdict=PASS`

- **Command**: `pytest -k test_us0095_resume_brief_pairing_markers tests/auto_command_contract_test.py -q`
- **Expected**: **DEC-0069** pairing mandate; drain-advance step 2 ASSERT pairing; stale brief → `RESUME_BRIEF_STALE` fail-closed.
- **Evidence**: subtest PASS; pairing mandate + `RESUME_BRIEF_STALE` in `auto.md`.

### UAT-8 — Contract tests (AC-8) — `verdict=PASS`

- **Command**: `pytest -k us0095 tests/auto_command_contract_test.py -v`
- **Expected**: Seven `test_us0095_*` subtests green.
- **Evidence**: verify-work re-run **7 passed**, 30 subtests passed.

### UAT-9 — Template parity (AC-9) — `verdict=PASS`

- **Commands**: `python scripts/check_intake_template_parity.py --scope=us-0095`; `pytest -k test_us0095_template_parity_auto_surfaces tests/auto_command_contract_test.py -q`
- **Expected**: `[INTAKE_TEMPLATE_PARITY_OK]`; active + `template/` mirrors for `auto.md`, reference, runbook.
- **Evidence**: both green on verify-work re-run.

### UAT-10 — Caps + security (AC-10) — `verdict=PASS`

- **Check**: manual review of reference cap/ledger + security deny-list
- **Expected**: `AUTO_LOOP_MAX_CYCLES`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BLOCK_RETRY_MAX` honored; `remediation_action` values; breadcrumb fields; security deny-list unchanged.
- **Evidence**: `auto-orchestration-reference.md` § unified cap/ledger + **Security deny-list**; `native_chain_active`, `outer_cycle_index`, `implementation_loop_index` breadcrumbs.

## Closure preflight (9 gates — all PASS)

| Gate | Verdict | Evidence |
|------|---------|----------|
| `tasks_done` | PASS (10/10) | T-001..T-010 done per `sprints/S0084/tasks.md` |
| `ac_qa_pass` | PASS (10/10) | `sprints/S0084/qa-findings.md` §Per-AC verdicts |
| `ac_uat_pass` | PASS (10/10) | this UAT matrix (UAT-1..UAT-10) |
| `plan_verify_status` | PASS | `sprints/S0084/plan-verify.json` status=PASS |
| `bug_validator` | `[BUG_VALIDATION_OK]` | verify-work independent re-run exit 0 |
| `parity` | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0095 |
| `script_self_tests` | PASS | `pytest -k us0095` 7 passed (30 subtests) |
| `test_baselines_no_regression` | PASS | zero US-0095 regressions; `scripts/auto_outer_driver.py` retained |
| `dec_invariants` | PASS | **BUG-0006** spawn-only + **DEC-0069** pairing + **DEC-0078** stop matrix preserved |

## Results summary (trace to acceptance criteria)

| AC | UAT step(s) | Verdict | Evidence |
|----|-------------|---------|----------|
| AC-1 Native in-chat auto-chain | UAT-1 | PASS | `test_us0095_native_in_chat_auto_chain_markers` |
| AC-2 Drain-without-pause (IDE) | UAT-2 | PASS | 7-step algorithm + subtest |
| AC-3 Spawn-only preserved | UAT-3 | PASS | `test_us0095_spawn_only_regression` |
| AC-4 Stop matrix hard gates | UAT-4 | PASS | stop matrix unchanged |
| AC-5 Outer driver demoted | UAT-5 | PASS | README/runbook optional/fallback |
| AC-6 Operator surface / AUTO_QUIET | UAT-6 | PASS | suppression table + subtest |
| AC-7 DEC-0069 pairing | UAT-7 | PASS | `test_us0095_resume_brief_pairing_markers` |
| AC-8 Contract tests | UAT-8 | PASS | `pytest -k us0095` 7 passed |
| AC-9 Template parity | UAT-9 | PASS | `--scope=us-0095` + parity subtest |
| AC-10 Caps + security | UAT-10 | PASS | cap/ledger + deny-list docs |

**UAT outcome**: **10 / 10 PASS** — ready for **`/release`**. Story **US-0095** stays **OPEN** until release closure per **US-0045**.
