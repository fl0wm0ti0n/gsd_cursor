# Sprint S0082 UAT — US-0093

- **Sprint**: `S0082`
- **Work item**: **US-0093** — Cursor browser-integrated UAT self-test
- **DEC**: **DEC-0079**
- **Orchestrator run**: **auto-20260606-04**
- **Machine-readable**: `sprints/S0082/uat.json`
- **Status**: **populated** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0093** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0082/qa-findings.md` (PASS)
- **verify_work_executed_at**: 2026-06-07T01:15:00Z
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0082-US0093-verify-work-20260607T011500Z-fresh`
- **verify_work_verdict**: **PASS** (10/10 UAT steps PASS; 0 FAIL; 0 SKIP)

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 10 |
| FAIL | 0 |
| SKIP | 0 |
| Total | 10 |

Verify-work verdict: **PASS**. Closure preflight: **PASS** (9/9 gates). Story **US-0093** remains **OPEN** per **US-0045**.

## Preconditions

- Python 3.12+ available.
- DEC-0079 execute deliverables merged (`scripts/uat_probe_lib.py` two-tier browser, verb routing, stub completion, evidence schema).
- Template parity scope `us-0093` green at QA boundary.

## UAT steps

### UAT-1 — Scratchpad `UAT_BROWSER_PROBE_MODE` + keys (AC-1) — `verdict=PASS`

- **Command**: `python -m pytest tests/auto_command_contract_test.py -q -k test_us0093_scratchpad_browser_probe_mode_keys`
- **Expected**: `cursor|http_fallback|playwright_fallback` (default `cursor`); poll/fallback keys; `PERMISSION_MODE` + `runtime-connectivity.md` interaction docs.
- **Evidence**: contract subtest PASS; scratchpad active + template + local-example parity.

### UAT-2 — `browser_smoke` two-tier execution (AC-2) — `verdict=PASS`

- **Commands**: `pytest -k test_us0093_no_silent_pass_cursor_browser_smoke`; `python scripts/uat_probe_lib.py --self-test`
- **Expected**: `execution_tier=agent|stdlib`; no silent PASS in `cursor` mode without `browser_evidence_refs`; HTTP/Playwright fallback wired; lib spawn-only (no direct browser MCP).
- **Evidence**: contract subtest PASS; `[UAT_PROBE_LIB_SELF_TEST_OK]`; command excerpts in `verify-work.md`/`qa.md`/`execute.md`.

### UAT-3 — Automatable `manual_operator` routing (AC-3) — `verdict=PASS`

- **Commands**: probe `--report` on judgment step; probe `--report` on UI click step without URL
- **Expected**: judgment tokens → `UAT_PROBE_UNRESOLVED`; automatable UI reclassifies when URL resolves; mixed verbs fail-closed.
- **Evidence**: `operator visually confirms button click` → `manual_operator`/`UAT_PROBE_UNRESOLVED`; `click submit button on login form` → `UAT_PROBE_UNRESOLVED` (URL unresolved).

### UAT-4 — `process_health` + `cli_smoke` stub completion (AC-4) — `verdict=PASS`

- **Command**: `python scripts/uat_probe_lib.py --self-test`
- **Expected**: bounded subprocess + readiness poll / exit-code assertion; `UAT_PROBE_PASS`|`UAT_PROBE_TIMEOUT`|`UAT_PROBE_FAILED` family.
- **Evidence**: `[UAT_PROBE_LIB_SELF_TEST_OK]` covers positive + timeout fixtures.

### UAT-5 — Evidence schema + `--merge-result` (AC-5) — `verdict=PASS`

- **Command**: `pytest -k test_us0093_browser_evidence_refs_in_commands`
- **Expected**: `browser_evidence_refs` schema; PASS in `cursor` mode requires refs; evidence under `sprints/Sxxxx/evidence/browser/`.
- **Evidence**: contract subtest PASS; `--merge-result` reject-without-refs documented.

### UAT-6 — `UAT_BROWSER_*` reason codes (AC-6) — `verdict=PASS`

- **Command**: `pytest -k test_us0093_browser_reason_codes_in_lib_and_docs`
- **Expected**: `UAT_BROWSER_UNAVAILABLE`, `UAT_BROWSER_PROBE_FAILED`, `UAT_BROWSER_PROBE_TIMEOUT` in lib + docs; self-test fixtures.
- **Evidence**: contract subtest PASS; `[UAT_PROBE_LIB_SELF_TEST_OK]`.

### UAT-7 — Security deny-list (AC-7) — `verdict=PASS`

- **Command**: `python scripts/uat_probe_lib.py --repo . --step "read secrets from .env file" --report`
- **Expected**: `UAT_PROBE_FORBIDDEN`; no credential auto-fill; no intake evidence mutation.
- **Evidence**: `.env` step → `UAT_PROBE_FORBIDDEN` (verify-work re-run).

### UAT-8 — Runbook + auto-orchestration-reference (AC-8) — `verdict=PASS`

- **Commands**: verify runbook + reference operator recipes; `uat_probe_lib.py --self-test`
- **Expected**: mode enablement, CI `http_fallback`, evidence paths, `--merge-result`, `@browser` override; active + template parity.
- **Evidence**: operator recipes present active + template; CI `http_fallback` documented.

### UAT-9 — Contract tests (AC-9) — `verdict=PASS`

- **Command**: `python -m pytest tests/auto_command_contract_test.py -q -k us0093`
- **Expected**: six `test_us0093_*` subtests PASS; DEC-0078/spawn-only markers not weakened.
- **Evidence**: **6 passed**, 20 subtests (verify-work independent re-run).

### UAT-10 — Template parity (AC-10) — `verdict=PASS`

- **Commands**: `python scripts/check_intake_template_parity.py --repo . --scope=us-0093`; `pytest -k test_us0093_architecture_linkage`
- **Expected**: `[INTAKE_TEMPLATE_PARITY_OK]` (8 rows); architecture `# US-0093` references DEC-0079.
- **Evidence**: parity OK (verify-work re-run); architecture linkage subtest PASS; `uat_probe_lib.py` active/template SHA-256 match.

## Runtime browser evidence (US-0093 / DEC-0079)

Orchestration contract story — its-magic repo has no resolvable webapp URL for live Cursor browser MCP navigation. Verify-work validates the **two-tier contract** and fail-closed classification:

- `browser_probe_mode`: cursor (default scratchpad)
- `browser_evidence_refs`: N/A for live MCP in this repo context — contract tests + self-test stdlib fallback provide execution evidence
- `runtime_browser_verdict`: contract-validated (no fabricated PASS; `UAT_PROBE_UNRESOLVED` until agent completes in cursor mode)

## Closure preflight (9 gates — all PASS)

| Gate | Verdict | Evidence |
|------|---------|----------|
| `tasks_done` | PASS (10/10) | T-001..T-010 done per `sprints/S0082/tasks.md` |
| `ac_qa_pass` | PASS (10/10) | `sprints/S0082/qa-findings.md` §Per-AC verdicts |
| `ac_uat_pass` | PASS (10/10) | this UAT matrix (UAT-1..UAT-10) |
| `plan_verify_status` | PASS | `sprints/S0082/plan-verify.json` status=PASS |
| `bug_validator` | `[BUG_VALIDATION_OK]` | verify-work independent re-run exit 0 |
| `parity` | PASS | `[INTAKE_TEMPLATE_PARITY_OK]` scope=us-0093 |
| `script_self_tests` | PASS | `[UAT_PROBE_LIB_SELF_TEST_OK]` |
| `test_baselines_no_regression` | PASS | `pytest -k us0093` 6 passed; zero US-0093 regressions |
| `dec_invariants` | PASS | DEC-0078 deny-list + spawn-only (**BUG-0006**) preserved |

## Results summary (trace to acceptance criteria)

| AC | UAT step(s) | Verdict | Evidence |
|----|-------------|---------|----------|
| AC-1 Scratchpad + docs mode keys | UAT-1 | PASS | `test_us0093_scratchpad_browser_probe_mode_keys` |
| AC-2 `browser_smoke` two-tier execution | UAT-2 | PASS | no-silent-PASS contract + self-test |
| AC-3 Automatable `manual_operator` routing | UAT-3 | PASS | judgment/UI probe spot-checks |
| AC-4 Stub completion | UAT-4 | PASS | self-test process_health/cli_smoke |
| AC-5 Evidence schema | UAT-5 | PASS | `test_us0093_browser_evidence_refs_in_commands` |
| AC-6 `UAT_BROWSER_*` reason codes | UAT-6 | PASS | reason-code contract subtest |
| AC-7 Security deny-list | UAT-7 | PASS | `.env` → `UAT_PROBE_FORBIDDEN` |
| AC-8 Runbook + reference | UAT-8 | PASS | operator recipes active + template |
| AC-9 Contract tests | UAT-9 | PASS | `pytest -k us0093` 6 passed |
| AC-10 Template parity | UAT-10 | PASS | `--scope=us-0093` + architecture linkage |
