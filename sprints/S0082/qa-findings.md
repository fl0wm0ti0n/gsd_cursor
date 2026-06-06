# QA Findings — S0082 / US-0093 (cycle 1)

## Metadata

- **sprint_id**: S0082
- **story_id**: US-0093
- **dec_id**: DEC-0079 (composes on DEC-0078, US-0065, US-0066)
- **cycle**: 1
- **role**: qa
- **timestamp**: 2026-06-07T01:00:00Z
- **orchestrator_run_id**: auto-20260606-04
- **fresh_context_marker**: qa-S0082-US0093-qa-20260607T010000Z-fresh
- **inputs_reviewed**: `handoffs/dev_to_qa.md`, `sprints/S0082/tasks.md`, `sprints/S0082/summary.md`, `decisions/DEC-0079.md`, `docs/product/backlog.md` `## US-0093`, `docs/engineering/architecture.md` `# US-0093`, `scripts/uat_probe_lib.py`, `.cursor/commands/qa.md`, `verify-work.md`, `execute.md`, `docs/engineering/runbook.md`.

## Overall verdict

**PASS** — All 10 ACs (AC-1..AC-10) satisfied; six `test_us0093_*` contract subtests green; `uat_probe_lib.py --self-test` green; template parity `--scope=us-0093` green; active/template `uat_probe_lib.py` SHA-256 match; DEC-0078 deny-list and spawn-only (**BUG-0006**) preserved. Story **US-0093** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-10 = 10/10 PASS
- `regressions_found`: **none attributable to US-0093**
- `parity_verified`: true (`uat_probe_lib.py` active/template SHA-256 match; `check_intake_template_parity.py --scope=us-0093` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `decision_gate_posture`: none required

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `pytest -k us0093` | 6 passed | **PASS** (6 passed, 20 subtests) |
| 2 | `python scripts/uat_probe_lib.py --self-test` | `[UAT_PROBE_LIB_SELF_TEST_OK]` | **PASS** |
| 3 | `python scripts/check_intake_template_parity.py --repo . --scope=us-0093` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 4 | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | **PASS** |
| 5 | Active/template `uat_probe_lib.py` SHA-256 | byte-identical | **PASS** |
| 6 | Lib grep: no direct browser MCP invocation | docs/sequence strings only; no `CallMcpTool` | **PASS** |
| 7 | Negative: docs forbid silent PASS in `cursor` mode | `test_us0093_no_silent_pass_cursor_browser_smoke` + command prose | **PASS** |
| 8 | Probe spot-check: judgment `manual_operator` | `UAT_PROBE_UNRESOLVED` | **PASS** |
| 9 | Probe spot-check: `.env` secret path | `UAT_PROBE_FORBIDDEN` | **PASS** |
| 10 | Runbook CI recipe `UAT_BROWSER_PROBE_MODE=http_fallback` | present active + template | **PASS** |
| 11 | Scratchpad keys `UAT_BROWSER_PROBE_MODE` + poll/fallback defaults | documented + locked values | **PASS** |

## Per-AC verdicts (AC-1..AC-10)

### AC-1 — Scratchpad + docs mode keys — `verdict=PASS`

- **Task**: T-001
- **evidence_ref**: `.cursor/scratchpad.md` documents `cursor|http_fallback|playwright_fallback` (default `cursor`); `UAT_BROWSER_FALLBACK_CHAIN`, `UAT_PROCESS_HEALTH_POLL_*`, `DEV_SERVER_PORT`/`DEV_SERVER_COMMAND`; interaction bullets for `PERMISSION_MODE`, browser approval, `runtime-connectivity.md`; template + local-example parity; `test_us0093_scratchpad_browser_probe_mode_keys`.

### AC-2 — `browser_smoke` two-tier execution — `verdict=PASS`

- **Task**: T-002
- **evidence_ref**: `scripts/uat_probe_lib.py` emits `execution_tier=agent|stdlib`; `cursor` mode returns plan + `UAT_PROBE_UNRESOLVED` until agent completes (no fabricated `browser_evidence_refs`); HTTP/Playwright fallback paths wired; command excerpts in `verify-work.md`/`qa.md`/`execute.md` (`### Browser UAT self-test (US-0093)`); lib never calls browser MCP (**BUG-0006**).

### AC-3 — Automatable `manual_operator` routing — `verdict=PASS`

- **Task**: T-003
- **evidence_ref**: `classify_step` judgment-deny precedence over UI verbs; mixed-verb `"operator visually confirms button click"` → `UAT_PROBE_UNRESOLVED` (spot-check); automatable UI tokens reclass to `browser_smoke` when URL resolves (self-test fixtures); generic manual without UI verbs stays unresolved.

### AC-4 — `process_health` + `cli_smoke` stub completion — `verdict=PASS`

- **Task**: T-004
- **evidence_ref**: `execute_probe` branches for `process_health` (startup command extraction, health URL poll, `UAT_PROBE_PASS`|`UAT_PROBE_TIMEOUT`|`UAT_PROBE_FAILED`) and `cli_smoke` (subprocess exit-code assertion); `--self-test` includes positive + timeout fixtures; no LLM inference.

### AC-5 — Evidence schema + `--merge-result` — `verdict=PASS`

- **Task**: T-005
- **evidence_ref**: `browser_evidence_refs` schema (`navigation_url`, `screenshots[]` max 5, console/network summary paths); `--merge-result` rejects PASS without required refs in `cursor` mode → `UAT_BROWSER_PROBE_FAILED`; command docs cite evidence paths; `test_us0093_browser_evidence_refs_in_commands`.

### AC-6 — New `UAT_BROWSER_*` reason codes — `verdict=PASS`

- **Task**: T-006
- **evidence_ref**: `UAT_BROWSER_UNAVAILABLE`, `UAT_BROWSER_PROBE_FAILED`, `UAT_BROWSER_PROBE_TIMEOUT` in lib + docs; `--self-test` covers MCP-unavailable, fallback, timeout fixtures; `test_us0093_browser_reason_codes_in_lib_and_docs`.

### AC-7 — Security deny-list unchanged — `verdict=PASS`

- **Task**: T-007
- **evidence_ref**: `.env`/`password`/`credential` steps → `UAT_PROBE_FORBIDDEN` (spot-check); MCP sequence docs forbid credential fill; no `.env` read or `handoffs/intake_evidence/` mutation paths; DEC-0078 §8 not weakened.

### AC-8 — Runbook + auto-orchestration-reference — `verdict=PASS`

- **Task**: T-008
- **evidence_ref**: `docs/engineering/runbook.md` + `auto-orchestration-reference.md` operator recipe: mode enablement, CI `http_fallback`, evidence paths, `--merge-result`, `@browser` override; active/template parity per scope check.

### AC-9 — Contract tests — `verdict=PASS`

- **Task**: T-009
- **evidence_ref**: six `test_us0093_*` subtests green (`pytest -k us0093`); negative marker blocks silent-PASS prose reintroduction; DEC-0078/spawn-only markers not weakened.

### AC-10 — Template parity — `verdict=PASS`

- **Task**: T-010
- **evidence_ref**: `check_intake_template_parity.py --scope=us-0093` → `[INTAKE_TEMPLATE_PARITY_OK]` (8 rows); `test_us0093_architecture_linkage` asserts `# US-0093` references DEC-0079 + compose-on stories; installer manifest updated.

## UAT probe evidence (US-0093 / DEC-0079)

Probe spot-checks (`python scripts/uat_probe_lib.py --repo . --step ... --report`):

| Step | probe_kind | reason_code | passed |
|------|------------|-------------|--------|
| operator visually confirms button click | manual_operator | `UAT_PROBE_UNRESOLVED` | false |
| read secrets from .env file | null | `UAT_PROBE_FORBIDDEN` | false |
| click submit button on login form | null | `UAT_PROBE_UNRESOLVED` | false |

**Interpretation**: fail-closed behavior confirmed — judgment steps unresolved, secret paths forbidden, no silent PASS. Full browser MCP evidence matrix deferred to `/verify-work` per `sprints/S0082/uat.md` (orchestration contract story; Tier-2 agent owns MCP execution).

Recorded in `sprints/S0082/uat.json` `probe_results[]` (QA cycle 1).

## Runtime browser evidence (US-0093 / DEC-0079)

Not executed in QA cycle — **cursor** mode `browser_smoke` requires Tier-2 agent MCP sequence per DEC-0079 §1. QA validates lib contract + fail-closed classification only. Verify-work will populate `browser_evidence_refs` when applicable.

- `browser_probe_mode`: cursor (default scratchpad)
- `browser_evidence_refs`: (deferred to verify-work)
- `runtime_browser_verdict`: deferred

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python (stdlib + pytest)
- `generated_test_command`: `pytest -k us0093`
- `generated_test_result`: pass
- `generated_test_output_ref`: 6 passed, 20 subtests passed
- `generated_test_paths_ref`: `tests/auto_command_contract_test.py` (`test_us0093_*`)
- `generated_test_reason_code`: (none — pass)

## Runtime QA evidence (US-0065)

Not applicable — orchestration/docs/script story; no application runtime startup required. `runtime_final_verdict=skipped`; `runtime_reason_code=N/A_ORCHESTRATION_CONTRACT_STORY`.

## Blocking findings

None.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0082-US0093-qa-20260607T010000Z-fresh`
- `timestamp=2026-06-07T01:00:00Z`
- `evidence_ref=sprints/S0082/qa-findings.md,handoffs/qa_to_verify_work.md,docs/engineering/state.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260606-04`
- `runtime_proof_id=rp-auto-20260606-04-qa-qa-20260607T010000Z-S0082-US0093`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-07T01:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=b52ffbc120a0e0f444dc80835334942adf912e1827bbabae8ee8d60f36f827ad`

Canonical JSON tuple: `{"dec_id":"DEC-0079","fresh_context_marker":"qa-S0082-US0093-qa-20260607T010000Z-fresh","orchestrator_run_id":"auto-20260606-04","phase":"qa","role":"qa","sprint_id":"S0082","story_id":"US-0093","timestamp":"20260607T010000Z"}`.

**Boundary verification**: consumed execute-phase proof `runtime_proof_id=rp-auto-20260606-04-execute-dev-20260607T003000Z-S0082-US0093` / `proof_hash=01014a9fa592e1b183f47595b20ad2c5c1fe9562aa6387b177d077dbfe47e62e`.

## Next phase

**`/verify-work`** (fresh **qa** subagent) — US-0093 remains OPEN until verify-work + `/release` closure per US-0045.
