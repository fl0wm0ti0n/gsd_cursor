# Release Notes — S0130 / US-0130

- **Sprint**: `S0130`
- **Story**: `US-0130` — Operator-pinned sovereign-critic model via catalog `roles.critic` and scratchpad `MODEL_SOVEREIGN-CRITIC` (10 contract-test markers)
- **Release date**: `2026-08-26T22:42:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260826-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0130-release-20260826T224200Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required; same slug as critic → degraded_mode informational OK)
- **runtime_proof_id**: `rp-auto-20260826-01-release-release-20260826T224200Z-US-0130`
- **proof_hash**: `8CD2E1B2A5D252EE4778E18A5F274C7DF6359042AC8E414D5B24540BB598C8FE`
- **proof_ttl**: `2026-08-26T23:42:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0130 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Consolidated harness **re-run** this spawn @ `2026-08-26T22:41:33Z` → `Pass: 845 / Fail: 0` because prior `tests/report.md` @ `2026-08-26T20:57:42Z` preceded US-0130 execute (`2026-08-26T22:14:20Z`) and new `tests/us0130_contract_test.py` markers were not covered.

## Summary

US-0130 lets operators pin which model `/sovereign-critic` uses, aligned with v2 role-catalog patterns:

- Scratchpad `MODEL_SOVEREIGN-CRITIC=<slug>` (hyphen exact; highest precedence) consumed via `phase_to_model_key("sovereign-critic")` (AC-1).
- Catalog `roles.critic` optional additive v2 role via `CATALOG_OPTIONAL_ROLE_KEYS = frozenset({"critic"})`; absent key valid; empty-present reuses `MODEL_CATALOG_SCHEMA_V2_INVALID` (AC-2).
- `select_critic_model` overlay precedence: pin > `roles.critic` (when `role_catalog`) > opposition/`dev` via `_resolve_slug_for_tier` UNCHANGED; underscore alias not consumed (AC-3).
- Same-slug collision keeps `degraded=True` / `CROSS_MODEL_DEGRADED_MODE` (AC-4).
- One global critic overlay inside `select_critic_model` only; no per-lens overrides (AC-5).
- `tests/us0130_contract_test.py` — 10 `test_us0130_*` markers (+ template mirror) (AC-6).
- Compose do not amend US-0104 findings schema / US-0101 matrix / US-0102 5-step chain (AC-7).
- cursor_only example ships `critic=composer-2.5-fast` as 9th; installer never writes `model-catalog.local.json` (AC-8).
- Runbook `#### Degraded fallback troubleshooting` pin-precedence note; `--scope=sovereign-critic` + `--scope=model-tier-overrides` parity (AC-9).

Compose guards 9/9 UNCHANGED. FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN`.

## ACs satisfied (QA + verify-work, static-contract + UAT 9/9)

**9/9 PASS** (live pytest 10/10 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Scratchpad pin `MODEL_SOVEREIGN-CRITIC` highest precedence | PASS (markers 1, 6) |
| AC-2 | Catalog `roles.critic` optional additive v2 role | PASS (markers 2, 3, 7, 8) |
| AC-3 | `select_critic_model` precedence pin > catalog > opposition | PASS (markers 1, 2, 3, 6) |
| AC-4 | Same-slug keeps `CROSS_MODEL_DEGRADED_MODE` | PASS (marker 4) |
| AC-5 | One global critic; no per-lens overrides | PASS (marker 8 + overlay shape) |
| AC-6 | 10 `test_us0130_*` contract markers | PASS (all 10) |
| AC-7 | Compose do not amend US-0104 / US-0101 / US-0102 | PASS (marker 5 + us0104 10/10) |
| AC-8 | Examples + installer (cursor_only 9th; never write local.json) | PASS (markers 9, 10) |
| AC-9 | Docs + parity (scratchpad, runbook, template pairs) | PASS (both parity scopes OK) |

## Test results (release 1st attempt — harness re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-26T22:41:33Z`, `Pass: 845 / Fail: 0` literal at L5. Grep `^\- \[FAIL\]` → 0 matches. Re-run this release spawn (prior report @ `2026-08-26T20:57:42Z` stale vs execute).
- **US-0130 live pytest** (release spawn): `python -m pytest tests/us0130_contract_test.py -q` → **10 passed in 0.06s**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`; `--scope=model-tier-overrides` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]` (US-0130 OPEN — excluded).
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ `2026-08-26T22:41:33Z` Pass:845/Fail:0; metadata guard exit 0; harness **re-run** this release spawn) |
| qa | PASS (`sprints/S0130/qa-findings.md`; 0 blockers; NB-1 informational — superseded by harness re-run) |
| verify_work | PASS (`sprints/S0130/uat.json` verify_work verdict=PASS; 9/9 ACs; 10/10 contract live) |
| uat | PASS (10/10; populated incl. `convergence_smoke`; `contract_tests_primary`; 6 live-runtime classes `UAT_PROBE_FORBIDDEN`) |
| isolation_evidence | PASS (execute+qa+verify-work+sovereign-critic in `docs/engineering/state.md`; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260826-01-verify-work-qa-20260826T223136Z-US-0130` TTL `2026-08-26T23:31:36Z` consumed @ `22:42:00Z`; proof_hash recomputed MATCH `8CE4D169132A04FA3FCB84281F0F67B5D8A2C36B019A7B8E092DFC5C639CC1E1`) |
| readme_feature_coverage_3f | PASS (`coverage_missing=[]`; US-0130 OPEN excluded) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (pre/post append rollover+check) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0130 = `released`) |

## Run

```powershell
# US-0130-specific live contract test (10/10 per release spawn):
python -m pytest tests/us0130_contract_test.py -v
#   Expected: 10 passed in ~0.06s

python scripts/check_intake_template_parity.py --scope=sovereign-critic
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=sovereign-critic

python scripts/check_intake_template_parity.py --scope=model-tier-overrides
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=model-tier-overrides

python scripts/sovereign_critic_validate.py --repo . --enforce
#   Expected: [SOVEREIGN_CRITIC_VALIDATION_OK]

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

# Consolidated harness (Pass:845/Fail:0 @ 2026-08-26T22:41:33Z):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0
```

Start command for the shipped pack (kit/scripts story — not a long-running service):

```bash
# Pin critic model in scratchpad (comment placeholder — set slug in .cursor/scratchpad.local.md):
# MODEL_SOVEREIGN-CRITIC=<your-critic-model-slug>
python scripts/sovereign_critic_validate.py --repo . --enforce
# select_critic_model applies pin > roles.critic > opposition/dev per US-0130
```

- **start_command**: `python scripts/sovereign_critic_validate.py --repo . --enforce` (operator validation; pin consumed at `/sovereign-critic` spawn)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (scripts/docs kit — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + validator `--enforce`, not HTTP)
- **runtime_context_ref**: `docs/engineering/runbook.md` `#### Degraded fallback troubleshooting`; `scripts/sovereign_critic_lib.py` `select_critic_model`; `tests/us0130_contract_test.py`

## Verify

1. `python -m pytest tests/us0130_contract_test.py -v` → 10 passed (confirmed per release spawn)
2. `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` → `[INTAKE_TEMPLATE_PARITY_OK]`
4. `python scripts/sovereign_critic_validate.py --repo . --enforce` → `[SOVEREIGN_CRITIC_VALIDATION_OK]`
5. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
6. `tests/report.md` → `Fail: 0` literal at L5 (timestamp `2026-08-26T22:41:33Z`)

**expected_health_signal**: all 10 contract markers PASS; both parity scopes OK; harness Fail:0; metadata guard exit 0; validator enforce OK; `.cursor/model-catalog.local.json` absent.

## Credentials

- **credential_source_refs**: `n/a` (no API keys; model slugs live in operator `.cursor/scratchpad.local.md` only)
- **expected_value_source**: operator scratchpad local layer; example catalogs under `.cursor/model-catalog.local.example.*.json`

## Known Issues

None blocking. **NB-1** (informational, superseded): prior harness timestamp preceded execute — resolved by gate-1 re-run @ `2026-08-26T22:41:33Z`.

## Evidence refs

- `tests/report.md` (@ 2026-08-26T22:41:33Z)
- `sprints/S0130/qa-findings.md` (QA_PASS)
- `sprints/S0130/uat.json`, `sprints/S0130/uat.md` (verify-work PASS)
- `sprints/S0130/summary.md`
- `sprints/S0130/release-findings.md`
- `docs/engineering/state.md` (execute / qa / verify-work / sovereign-critic / release checkpoints)

## Next phase

`/closure` (fresh **qe** subagent, ship macro phase 2 of 3 per DEC-0082). Release does **not** spawn closure. Backlog US-0130 remains **OPEN**; acceptance L158 remains **unchecked** until closure.
