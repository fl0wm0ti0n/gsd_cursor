# Release Notes — S0128 / US-0128

- **Sprint**: `S0128`
- **Story**: `US-0128` — Convergence smoke surrogate for contract-test and waived-probe UAT slices (11 contract-test markers)
- **Release date**: `2026-08-26T20:58:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260826-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0128-release-20260826T205800Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260826-01-release-release-20260826T205800Z-US-0128`
- **proof_hash**: `042AFE016454CE61643A0EEAA53AA44A9B2187EB2C19D8C944A77FBC6A335DFD`
- **proof_ttl**: `2026-08-26T21:58:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0128 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Consolidated harness **re-run** this spawn @ `2026-08-26T20:57:42Z` → `Pass: 845 / Fail: 0` because prior `tests/report.md` @ `2026-08-26T19:13:17Z` preceded US-0128 execute (`2026-08-26T20:30:23Z`) and new `tests/us0128_contract_test.py` markers were not covered.

## Summary

US-0128 unblocks `smoke_green` for ultra_lean/docs slices with waived live-runtime probes:

- `_eval_smoke_green` in `scripts/sovereign_convergence_lib.py`: legacy `_uat_smoke_passes` first; surrogate when 6 `UAT_PROBE_FORBIDDEN` waivers + `contract_test_failed=0` + `convergence_smoke` (or tail `probe_kind=contract_tests_primary`) (AC-1).
- Canonical `### Convergence smoke surrogate (US-0128)` in `.cursor/commands/qa.md` + `verify-work.md` (+ template mirrors); `/qa` and `/verify-work` emit `id=convergence_smoke` when `contract_test_failed=0` (AC-2, AC-4).
- `CONVERGENCE_SMOKE_SURROGATE_MISSING` in `docs/engineering/reason_codes.md` `## US-0128`; fail-closed when no smoke step / incomplete waivers / harness red (AC-3).
- `tests/us0128_contract_test.py` — 11 `test_us0128_*` markers (+ template mirror) (AC-5).
- Runbook `### Smoke surrogate for waived-probe UAT slices (US-0128)`; `SOVEREIGN_CONVERGENCE_PAIRS` +2 command rows (AC-6).

Compose guards 8/8 UNCHANGED (US-0109 deploy smoke, US-0126 reference fixture, US-0110 five-conjunct, US-0127 critic conjunct, US-0104 critic surfaces). FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN`.

## ACs satisfied (QA + verify-work, static-contract + UAT 7/7)

**6/6 PASS** (live pytest 11/11 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Surrogate eval — `_eval_smoke_green` legacy-first + waived-probe surrogate | PASS (markers 1–6, 8, 9) |
| AC-2 | Canonical uat step `convergence_smoke` from `/qa` + `/verify-work` | PASS (markers 5, 7, 8 + emission) |
| AC-3 | Fail closed — `CONVERGENCE_SMOKE_SURROGATE_MISSING` | PASS (markers 2, 3, 4, 6) |
| AC-4 | Command contracts — qa.md + verify-work.md additive subsections | PASS (markers 5, 7, 8) |
| AC-5 | 11 `test_us0128_*` contract markers | PASS (all 11) |
| AC-6 | Operator docs + `--scope=sovereign-convergence` parity | PASS (marker 8 + parity CLI) |

## Test results (release 1st attempt — harness re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-26T20:57:42Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `^\- \[FAIL\]` → 0 matches. Re-run this release spawn (prior report @ `2026-08-26T19:13:17Z` stale vs execute).
- **US-0128 live pytest** (release spawn): `python -m pytest tests/us0128_contract_test.py -q` → **11 passed in 1.42s**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]` (US-0128 OPEN — excluded).
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ `2026-08-26T20:57:42Z` Pass:845/Fail:0; metadata guard exit 0; harness **re-run** this release spawn) |
| qa | PASS (`sprints/S0128/qa-findings.md`; 0 blockers; NB-1 informational — superseded by harness re-run) |
| verify_work | PASS (`sprints/S0128/uat.json` verify_work verdict=PASS; 7/7 steps incl. `convergence_smoke`; 11/11 contract live) |
| uat | PASS (7/7; populated; `contract_tests_primary`; 6 live-runtime classes `UAT_PROBE_FORBIDDEN`) |
| isolation_evidence | PASS (execute+qa+verify-work+sovereign-critic in `docs/engineering/state.md`; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260826-01-verify-work-qa-20260826T204849Z-US-0128` TTL `2026-08-26T21:48:49Z` consumed @ `20:58:00Z`; proof_hash recomputed MATCH `DD09DA5BB0AFF6D69E39550B6EE8C43ED42765BD099E95A1BAF0B099E230AC88`) |
| readme_feature_coverage_3f | PASS (`coverage_missing=[]`; US-0128 OPEN excluded) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (pre/post append rollover+check) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0128 = `released`) |

## Run

```powershell
# US-0128-specific live contract test (11/11 per release spawn):
python -m pytest tests/us0128_contract_test.py -v
#   Expected: 11 passed in ~1.4s

python scripts/check_intake_template_parity.py --scope=sovereign-convergence
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-convergence

python scripts/sovereign_convergence_validate.py --repo . --enforce
#   Expected: [SOVEREIGN_CONVERGENCE_VALIDATION_OK] (smoke_green may pass with surrogate after US-0128)

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

# Consolidated harness (Pass:845/Fail:0 @ 2026-08-26T20:57:42Z):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0
```

Start command for the shipped pack (kit/scripts story — not a long-running service):

```bash
# Sovereign loop phases invoke /qa and /verify-work; surrogate fires when waived-probe slice + green contract tests:
python scripts/sovereign_convergence_validate.py --repo . --enforce
# After /verify-work emits convergence_smoke in uat.json, smoke_green conjunct may pass via surrogate
```

- **start_command**: `python scripts/sovereign_convergence_validate.py --repo . --enforce` (operator convergence check; surrogate path active for waived-probe slices)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (scripts/docs kit — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + validator `--enforce`, not HTTP)
- **runtime_context_ref**: `docs/engineering/runbook.md` `### Smoke surrogate for waived-probe UAT slices (US-0128)`; `scripts/sovereign_convergence_lib.py` `_eval_smoke_green`; `tests/us0128_contract_test.py`

## Verify

1. `python -m pytest tests/us0128_contract_test.py -v` → 11 passed (confirmed per release spawn)
2. `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/sovereign_convergence_validate.py --repo . --enforce` → `[SOVEREIGN_CONVERGENCE_VALIDATION_OK]`
4. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
5. `tests/report.md` → `Fail: 0` literal at L5 (timestamp `2026-08-26T20:57:42Z`)

**expected_health_signal**: all 11 contract markers PASS; sovereign-convergence parity OK; harness Fail:0 post-execute; metadata guard exit 0; validator enforce OK.

## Credentials

- **credential_source_refs**: `n/a` (no API keys; convergence lib operates on local repo state)
- **expected_value_source**: operator repo checkout

## Known Issues

- **NB-1** (informational, superseded): qa/verify-work noted `tests/report.md` @ `2026-08-26T19:13:17Z` stale vs execute — release spawn re-ran harness @ `2026-08-26T20:57:42Z` Pass:845/Fail:0.

## Evidence refs

- `tests/report.md` (@ 2026-08-26T20:57:42Z)
- `sprints/S0128/qa-findings.md` (QA_PASS)
- `sprints/S0128/uat.json`, `sprints/S0128/uat.md` (verify-work PASS)
- `sprints/S0128/summary.md`
- `sprints/S0128/release-findings.md`
- `docs/engineering/state.md` (execute / qa / verify-work / sovereign-critic / release checkpoints)

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick L156, `sprints/S0128/closure-verification.md`. Release does NOT spawn closure.
