# Release Notes — S0133 / US-0131

- **Sprint**: `S0133`
- **Story**: `US-0131` — Cross-host Its-Magic runtime configuration and parity
- **Release date**: `2026-09-07T21:15:18Z` (UTC)
- **orchestrator_run_id**: `auto-20260907-us0131`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-US0131-release-20260907T211518Z-fresh`
- **model_id**: `composer-2.5` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260907-us0131-release-release-20260907T211518Z-US-0131`
- **proof_hash**: `10026570510E2C006AE4A86CFC2F0A70BE0CF170E30E43C13BEC342EC3E72D7A`
- **proof_ttl**: `2026-09-07T22:15:18Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS.** All mandatory release gates (1, 2, 3, 4, 4b) green with **canonical harness Fail:0** (`tests/report.md` @ `2026-09-07T21:15:18Z` Pass:853 / Fail:0, including US-0131 harness rows 26AE). Queue row S0133 → `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish.

Gate-1 remediation (pre-finalization): BUG-0016 README coverage backfill (DONE + user_visible); active↔template `its_magic/README.md` + `docs/developer/README.md` parity; wired US-0131 into `tests/run-tests.ps1` / `tests/run-tests.sh` (26AE); synced `auto-orchestration-reference.md` template; added `scripts/host_runtime_config_lib.py` to installer `[clean_paths]`; moved `# US-0131` architecture H1 before caveman tail (`# US-0089` / `# US-0090`) per DEC-0073 §11.

## Summary

US-0131 ships host-neutral runtime configuration so shared lifecycle/governance settings resolve without requiring `.cursor/` on OpenCode-only installs:

- `.its-magic/config{,.local,.example}.json` host-neutral SOT (AC-1)
- Cursor LegacyScratchpadAdapter preserves DEC-0055 Model B precedence (AC-2)
- OpenCode-only path resolves from `.its-magic/` without `.cursor/` (AC-3)
- Shared-kernel scripts use `resolve_runtime_config` (9 modules) (AC-4)
- Host capability matrix + deterministic reason codes (AC-5)
- `--host both` precedence + `HOST_CONFIG_KEY_SHADOWED` (AC-6)
- Installer delivers examples; never overwrites locals; metadata clean after B-1 (AC-7)
- 10/10 `test_us0131_*` markers + runbook/docs (AC-8)
- US-0132 OUT OF SCOPE (MODEL_* ignored; marker 9)

FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN`. No fake browser PASS.

## ACs satisfied (QA + verify-work, UAT 9/9)

**8/8 PASS** (live pytest 10/10 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Host-neutral typed config contract | PASS (markers 1,6) |
| AC-2 | Cursor scratchpad compatibility adapter | PASS (marker 2) |
| AC-3 | OpenCode-only without `.cursor/` | PASS (marker 3) |
| AC-4 | Shared-kernel uses resolver | PASS (marker 8) |
| AC-5 | Capability matrix reason codes | PASS (marker 10) |
| AC-6 | Both-host precedence | PASS (markers 4,5) |
| AC-7 | Installer preserves locals + metadata clean | PASS (marker 7; B-1 CLOSED) |
| AC-8 | Cross-host contract tests + docs | PASS (10/10 + runbook) |

## Test results (release)

- **US-0131 live pytest**: `python -m pytest tests/us0131_contract_test.py -v` → **10 passed**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=us-0131` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]` (US-0131 OPEN excluded; BUG-0016 DONE covered).
- **Canonical harness** (`tests/report.md`): timestamp `2026-09-07T21:15:18Z`, **`Pass: 853 / Fail: 0`** — includes `[PASS] check_intake_template_parity --scope=us-0131` + `[PASS] US-0131 contract tests pass`.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` Fail:0 + us0131 10/10 + parity us-0131 + US-0071 metadata; `harness_fail_zero_claimed=true`) |
| qa | PASS (`sprints/S0133/qa-findings.md`; 0 blockers; NB-1..NB-3 informational; B-1 CLOSED) |
| verify_work | PASS (`sprints/S0133/uat.json` verdict=PASS; 8/8 ACs; 9/9 UAT incl `convergence_smoke`; 10/10 contract live) |
| uat | PASS (9/9; populated; `contract_tests_primary`; 6 live-runtime classes `UAT_PROBE_FORBIDDEN`) |
| isolation_evidence | PASS (execute+remediation+qa+verify-work+sovereign-critic+release; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260907-us0131-verify-work-qa-20260907T204621Z-US-0131` TTL `2026-09-07T21:46:21Z` consumed @ `21:15:18Z`; proof_hash recomputed MATCH `7F59D8E38F3449966F5E07B861314CD4EC85DC5CC432828C8CB90A451175984F`) |
| readme_feature_coverage_3f | PASS (`coverage_missing=[]`; US-0131 OPEN excluded; BUG-0016 DONE backfilled) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (`enforce-triad-hot-surface.py --check` exit 0) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0133 = `released`) |

## Run

```powershell
# US-0131-specific live contract test (10/10):
python -m pytest tests/us0131_contract_test.py -v
#   Expected: 10 passed

python scripts/check_intake_template_parity.py --scope=us-0131
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=us-0131

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

python scripts/validate_readme_feature_coverage.py --repo . --enforce
#   Expected: [README_FEATURE_COVERAGE_VALIDATE_OK]

# Canonical harness (Fail:0 required for gate-1):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: tests/report.md Fail: 0
```

Start command for the shipped pack (kit/cross-host config story — not a long-running HTTP service):

```bash
# Validate host-neutral runtime config contract:
python -m pytest tests/us0131_contract_test.py -v
```

- **start_command**: `python -m pytest tests/us0131_contract_test.py -v` (operator validation; no live host probe required for this CI slice)
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` (**Cross-host runtime configuration (US-0131)**); `docs/engineering/runtime-connectivity.md` (local kit — no remote service)

## Connect

- **service_url**: `n/a` (host-neutral config contract — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + Fail:0 harness, not HTTP)

## Verify

1. `python -m pytest tests/us0131_contract_test.py -v` → 10 passed
2. `python scripts/check_intake_template_parity.py --scope=us-0131` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
4. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`
5. `tests/report.md` header shows **Fail: 0** (incl. US-0131 harness rows)
6. Spot-check: `.its-magic/config.example.json` present; OpenCode-only path does not require `.cursor/`

**expected_health_signal**: all 10 `test_us0131_*` markers PASS; parity us-0131 OK; metadata guard exit 0; README enforce OK; harness Fail:0; backlog US-0131 remains OPEN until `/closure`.

## Credentials

- **credential_source_refs**: `n/a` (no API keys required for contract-test verify)
- **expected_value_source**: operator host + local kit checkout; no inline secrets

## Known Issues

None blocking.

- **NB-1** (informational): Soft-fail / `HOST_CONFIG_KEY_SHADOWED` remain intentional; Status OPEN / ACs unchecked held.
- **NB-2** (informational): Architecture/DEC read-only for story body; H1 reorder was Fail:0 remediation only (caveman tail invariant).
- **NB-3** (informational): Do not mark US-0131 DONE at release; do not tick acceptance L159; do not work US-0132; no publish under confirm mode.

## Evidence refs

- `tests/report.md` (@ 2026-09-07T21:15:18Z — Fail:0)
- `sprints/S0133/qa-findings.md` (QA_PASS)
- `sprints/S0133/uat.json`, `sprints/S0133/uat.md` (verify-work PASS)
- `sprints/S0133/summary.md`
- `sprints/S0133/release-findings.md`
- `docs/engineering/state.md` (execute / qa / verify-work / sovereign-critic / release checkpoints)

## Next phase

`/closure` (fresh **qe** subagent, ship macro phase 2 of 3 per DEC-0082). Release does **not** spawn closure. Backlog US-0131 remains **OPEN**; acceptance L159 remains **unchecked** until closure.
