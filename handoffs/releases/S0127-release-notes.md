# Release Notes — S0127 / US-0127

- **Sprint**: `S0127`
- **Story**: `US-0127` — Convergence critic conjunct: blocking-only open findings plus non-blocking auto-resolve at sovereign-critic PASS (13 contract-test markers)
- **Release date**: `2026-08-26T19:13:30Z` (UTC)
- **orchestrator_run_id**: `auto-20260826-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0127-release-20260826T191330Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260826-01-release-release-20260826T191330Z-US-0127`
- **proof_hash**: `A8C7F6BE6B9E8B17D591AF58D108157DCD2BC040AD351DBBA235D77B480C0EB5`
- **proof_ttl**: `2026-08-26T20:13:30Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0127 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Consolidated harness **re-run** this spawn @ `2026-08-26T19:13:17Z` → `Pass: 845 / Fail: 0` after gate-1 remediation for US-0126 post-closure README drift (`docs/developer/README.md` Quality gates `**US-0126**` row).

## Summary

US-0127 aligns sovereign-loop convergence with blocking-only critic semantics and ships operator hygiene tooling:

- `_critic_jsonl_has_open` in `scripts/sovereign_convergence_lib.py` delegates to `read_open_blocking(repo)`; `_eval_critic_resolved` JSONL-authoritative when non-empty (AC-1).
- Auto-resolve hook at `/sovereign-critic` PASS when `read_open_blocking(repo)==[]` via `auto_resolve_nonblocking_for_run` (AC-2).
- NEW `scripts/sovereign_critic_hygiene.py` (+ template mirror) with `--report` / `--resolve-nonblocking-for-run` / `--dry-run` / `--confirm` / `--self-test` / `--all-phases` / `--phase-id` and 6 reason codes (AC-3).
- `tests/us0127_contract_test.py` — 13 `test_us0127_*` markers (+ template mirror) (AC-4).
- Runbook `### Blocking-only conjunct-3 semantics (US-0127)` + `### Hygiene CLI (US-0127)`; `reason_codes.md` `## US-0127` (AC-5).
- `SOVEREIGN_CRITIC_PAIRS` + `--scope=sovereign-critic` parity extension (AC-6).

Compose guards 8/8 UNCHANGED (US-0104/US-0110/US-0107 read-only). FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; browser/api/process waived `UAT_PROBE_FORBIDDEN`.

## ACs satisfied (QA + verify-work, static-contract + UAT 6/6)

**6/6 PASS** (live pytest 13/13 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Blocking-only check — `_critic_jsonl_has_open` → `read_open_blocking` | PASS (markers 1,2,11,12,13) |
| AC-2 | Auto-resolve non-blocking at `/sovereign-critic` PASS | PASS (markers 3,4,5) |
| AC-3 | Hygiene CLI + 6 reason codes | PASS (markers 6–10; `--self-test` OK) |
| AC-4 | 13 `test_us0127_*` contract markers | PASS (all 13) |
| AC-5 | Operator docs (runbook subsections + reason_codes.md) | PASS |
| AC-6 | Template parity (`--scope=sovereign-critic`) | PASS |

## Test results (release 1st attempt — harness re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-26T19:13:17Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `^\- \[FAIL\]` → 0 matches. Re-run after US-0126 dev README remediation.
- **US-0127 live pytest** (release spawn): `python -m pytest tests/us0127_contract_test.py -q` → **13 passed in 0.63s**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]` (US-0127 OPEN — excluded).
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ `2026-08-26T19:13:17Z` Pass:845/Fail:0; metadata guard exit 0; harness re-run this release spawn) |
| qa | PASS (`sprints/S0127/qa-findings.md`; 0 blockers; NB-1 informational) |
| verify_work | PASS (`sprints/S0127/uat.json` verify_work verdict=PASS; 6/6 ACs; 13/13 contract live) |
| uat | PASS (6/6 ACs; populated; `contract_tests_primary`) |
| isolation_evidence | PASS (execute+qa+verify-work+sovereign-critic in `docs/engineering/state.md`; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260826-01-verify-work-qa-20260826T190216Z-US-0127` TTL `2026-08-26T20:02:16Z` consumed @ `19:13:30Z`; proof_hash recomputed MATCH) |
| readme_feature_coverage_3f | PASS (after US-0126 dev README remediation; US-0127 OPEN excluded) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (pre/post append rollover+check) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0127 = `released`) |

## Run

```powershell
# US-0127-specific live contract test (13/13 per release spawn):
python -m pytest tests/us0127_contract_test.py -v
#   Expected: 13 passed in ~0.6s

python scripts/check_intake_template_parity.py --scope=sovereign-critic
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-critic

python scripts/sovereign_critic_hygiene.py --self-test
#   Expected: [HYGIENE_SELF_TEST_OK]

python scripts/sovereign_critic_validate.py --repo . --enforce
#   Expected: [SOVEREIGN_CRITIC_VALIDATION_OK]

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

# Consolidated harness (Pass:845/Fail:0 @ 2026-08-26T19:13:17Z):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0
```

Start command for the shipped pack (kit/scripts story — not a long-running service):

```bash
# Sovereign loop phases invoke /sovereign-critic; hygiene CLI is operator-only:
python scripts/sovereign_critic_hygiene.py --report --repo .
# After /sovereign-critic PASS with zero blocking findings, non-blocking rows auto-resolve per US-0127 hook
```

- **start_command**: `python scripts/sovereign_critic_hygiene.py --report --repo .` (operator inventory; auto-resolve fires at `/sovereign-critic` PASS)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (scripts/docs kit — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + validator `--enforce`, not HTTP)
- **runtime_context_ref**: `docs/engineering/runbook.md` `### Blocking-only conjunct-3 semantics (US-0127)` + `### Hygiene CLI (US-0127)`; `scripts/sovereign_critic_hygiene.py`; `tests/us0127_contract_test.py`

## Verify

1. `python -m pytest tests/us0127_contract_test.py -v` → 13 passed (confirmed per release spawn)
2. `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/sovereign_critic_hygiene.py --self-test` → `[HYGIENE_SELF_TEST_OK]`
4. `python scripts/sovereign_critic_validate.py --repo . --enforce` → `[SOVEREIGN_CRITIC_VALIDATION_OK]`
5. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
6. `tests/report.md` → `Fail: 0` literal at L5 (timestamp `2026-08-26T19:13:17Z`)

**expected_health_signal**: all 13 contract markers PASS; sovereign-critic parity OK; harness Fail:0; metadata guard exit 0; validator enforce OK.

## Credentials

- **credential_source_refs**: `n/a` (no API keys; findings JSONL is local repo state)
- **expected_value_source**: operator repo checkout; hygiene `--confirm` requires explicit operator intent

## Known Issues

- **NB-1** (informational): runbook `SOVEREIGN_CRITIC_PAIRS` prose vs Python tuple hygiene-only — parity PASS; optional docs tidy later.

## Evidence refs

- `tests/report.md` (@ 2026-08-26T19:13:17Z)
- `sprints/S0127/qa-findings.md` (QA_PASS)
- `sprints/S0127/uat.json`, `sprints/S0127/uat.md` (verify-work PASS)
- `sprints/S0127/summary.md`
- `sprints/S0127/release-findings.md`
- `docs/engineering/state.md` (execute / qa / verify-work / sovereign-critic / release checkpoints)

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick L155, `sprints/S0127/closure-verification.md`. Release does NOT spawn closure.
