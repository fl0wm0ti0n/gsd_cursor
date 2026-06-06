# Sprint S0081 UAT — US-0092

- **Sprint**: `S0081`
- **Work item**: **US-0092** — Full-autonomy `/auto` mode + outer driver + self-verification
- **DEC**: **DEC-0078**
- **Orchestrator run**: **auto-20260606-03**
- **Machine-readable**: `sprints/S0081/uat.json`
- **Status**: **populated** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0092** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0081/qa-findings.md` (PASS)
- **verify_work_executed_at**: 2026-06-06T22:00:00Z
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0081-US0092-verify-work-20260606T220000Z-fresh`
- **verify_work_verdict**: **PASS** (10/10 UAT steps PASS; 0 FAIL; 0 SKIP)

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 10 |
| FAIL | 0 |
| SKIP | 0 |
| Total | 10 |

Verify-work verdict: **PASS**. Closure preflight: **PASS** (9/9 gates). Story **US-0092** remains **OPEN** per **US-0045**.

## Preconditions

- Python 3.12+ available.
- DEC-0078 execute deliverables merged (`scripts/auto_outer_driver.py`, `scripts/uat_probe_lib.py`, stop matrix, contract tests).
- Template parity scope `us-0092` green at QA boundary.

## UAT steps

### UAT-1 — Scratchpad `AUTO_FLOW_MODE` enum + keys (AC-1) — `verdict=PASS`

- **Command**: `python -m pytest tests/auto_command_contract_test.py -q -k test_us0092_scratchpad_full_autonomy_literal`
- **Expected**: `full_autonomy` literal alongside `manual` and `auto_until_decision`; `AUTO_BLOCK_RETRY_MAX=3`; `AUTO_OUTER_DRIVER_TIMEOUT_SECONDS` optional; interaction docs.
- **Evidence**: contract subtest PASS; scratchpad active + template + local example parity.

### UAT-2 — Outer driver script (AC-2) — `verdict=PASS`

- **Commands**: `python scripts/auto_outer_driver.py --self-test`; `python scripts/auto_outer_driver.py --repo . --dry-run`
- **Expected**: `[AUTO_OUTER_DRIVER_SELF_TEST_OK]`; activation gate exit **2** `AUTO_FLOW_MODE_NOT_FULL_AUTONOMY` without `full_autonomy`.
- **Evidence**: self-test OK (verify-work re-run); dry-run exit **2** confirmed.

### UAT-3 — UAT probe lib + self-verify excerpts (AC-3) — `verdict=PASS`

- **Commands**: `python scripts/uat_probe_lib.py --self-test`; probe `--report` on forbidden `.env` step
- **Expected**: `[UAT_PROBE_LIB_SELF_TEST_OK]`; fail-closed `UAT_PROBE_FORBIDDEN` / `UAT_PROBE_UNRESOLVED` — no silent PASS.
- **Evidence**: self-test OK; `.env` step → `UAT_PROBE_FORBIDDEN`; `/verify-work` + `/qa` command excerpts present.

### UAT-4 — Block-retry ledger (AC-4) — `verdict=PASS`

- **Commands**: `python scripts/auto_outer_driver.py --self-test`; verify `handoffs/auto_block_retry/` exists
- **Expected**: ledger writer; `BLOCK_RETRY_CAP_EXHAUSTED` exit **6**; cap interaction with `AUTO_BLOCK_RETRY_MAX`.
- **Evidence**: ledger directory present; `[AUTO_OUTER_DRIVER_SELF_TEST_OK]` covers cap exit; reference docs.

### UAT-5 — Drain-without-pause (AC-5) — `verdict=PASS`

- **Command**: `python -m pytest tests/auto_command_contract_test.py -q -k test_us0092_drain_advance_without_operator_phrases`
- **Expected**: drain-advance phrases without operator pause; `BACKLOG_MAX_STORIES_REACHED` exit **4**.
- **Evidence**: contract subtest PASS; runbook dry-run drain-advance note.

### UAT-6 — TOKEN_PROFILE orthography audit (AC-6) — `verdict=PASS`

- **Commands**: `pytest -k test_us0092_token_profile_orthogonality_string`; `pytest -k test_us0092_runbook_no_automation_breadth_conflict`
- **Expected**: orthogonality string in reference + runbook; no "automation breadth" conflict.
- **Evidence**: both subtests PASS (verify-work re-run).

### UAT-7 — Stop matrix docs (AC-7) — `verdict=PASS`

- **Command**: `pytest -k test_us0092_auto_stop_matrix_markers`
- **Expected**: `### Full-autonomy stop matrix (US-0092)` in `auto.md`; `RELEASE_PUBLISH_MODE=auto` explicit opt-in.
- **Evidence**: contract subtest PASS; stop matrix in `auto.md` + `auto-orchestration-reference.md`.

### UAT-8 — Contract tests (AC-8) — `verdict=PASS`

- **Command**: `python -m pytest tests/auto_command_contract_test.py -q -k us0092`
- **Expected**: nine `test_us0092_*` subtests PASS; US-0088 markers not weakened.
- **Evidence**: **9 passed**, 18 subtests (verify-work independent re-run).

### UAT-9 — Template parity + installer manifest (AC-9) — `verdict=PASS`

- **Command**: `python scripts/check_intake_template_parity.py --repo . --scope=us-0092`
- **Expected**: `[INTAKE_TEMPLATE_PARITY_OK]`; installer manifest lists new scripts.
- **Evidence**: parity OK (verify-work re-run); active/template script SHA-256 match.

### UAT-10 — Runbook + security deny-list (AC-10) — `verdict=PASS`

- **Command**: `pytest -k test_us0092_runbook_outer_driver_heading`
- **Expected**: `### Full-autonomy outer driver (US-0092)` subsection; security callout (no `.env`, no intake mutation, no publish without `RELEASE_PUBLISH_MODE=auto`).
- **Evidence**: contract subtest PASS; runbook subsection active + template.

## Closure preflight (9 gates — all PASS)

| Gate | Verdict | Evidence |
|------|---------|----------|
| `tasks_done` | PASS (10/10) | T-001..T-010 done per `sprints/S0081/tasks.md` |
| `ac_qa_pass` | PASS (10/10) | `sprints/S0081/qa-findings.md` §Per-AC verdicts |
| `ac_uat_pass` | PASS (10/10) | this UAT matrix (UAT-1..UAT-10) |
| `plan_verify_status` | PASS | `sprints/S0081/plan-verify.json` status=PASS |
| `bug_validator` | `[BUG_VALIDATION_OK]` | verify-work independent re-run exit 0 |
| `parity` | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0092 |
| `script_self_tests` | PASS | `[AUTO_OUTER_DRIVER_SELF_TEST_OK]` + `[UAT_PROBE_LIB_SELF_TEST_OK]` |
| `test_baselines_no_regression` | PASS | `pytest -k us0092` 9 passed; zero US-0092 regressions |
| `dec_invariants` | PASS | DEC-0078 non-goals preserved; US-0088 spawn-only unchanged |

## Results summary (trace to acceptance criteria)

| AC | UAT step(s) | Verdict | Evidence |
|----|-------------|---------|----------|
| AC-1 Scratchpad enum + keys | UAT-1 | PASS | `test_us0092_scratchpad_full_autonomy_literal` |
| AC-2 Outer driver | UAT-2 | PASS | self-test + activation gate exit **2** |
| AC-3 UAT probe lib | UAT-3 | PASS | self-test + fail-closed probe codes |
| AC-4 Block-retry ledger | UAT-4 | PASS | ledger dir + exit **6** cap |
| AC-5 Drain-without-pause | UAT-5 | PASS | drain-advance contract subtest |
| AC-6 TOKEN_PROFILE audit | UAT-6 | PASS | orthogonality + no conflict subtests |
| AC-7 Stop matrix | UAT-7 | PASS | `test_us0092_auto_stop_matrix_markers` |
| AC-8 Contract tests | UAT-8 | PASS | nine `test_us0092_*` green |
| AC-9 Template parity | UAT-9 | PASS | parity scope us-0092 OK |
| AC-10 Runbook + security | UAT-10 | PASS | runbook heading + deny-list subtest |

**UAT outcome**: **10 / 10 PASS** — ready for **`/release`**. Story **US-0092** stays **OPEN** until release closure per **US-0045**.
