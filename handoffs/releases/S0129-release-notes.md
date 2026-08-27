# Release Notes — S0129 / US-0129

- **Sprint**: `S0129`
- **Story**: `US-0129` — Architecture hot-surface rollover linkage guard (active contract preservation — 8 contract-test markers)
- **Release date**: `2026-08-27T08:42:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260827-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0129-release-20260827T084200Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260827-01-release-release-20260827T084200Z-US-0129`
- **proof_hash**: `3E9968156A9C5EEF3338ADE30856B30A8166FCCFA085A5BD667CA49AEE6D5399`
- **proof_ttl**: `2026-08-27T09:42:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0129 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Consolidated harness **re-run** this spawn @ `2026-08-27T08:41:43Z` → `Pass: 847 / Fail: 0` because prior `tests/report.md` @ `2026-08-26T22:41:33Z` preceded US-0129 execute (`2026-08-27T08:04:38Z`) and harness **26AB** was not covered.

## Summary

US-0129 prevents triad architecture rollover from breaking active contract-test linkage:

- `scripts/arch_linkage_guard.py` pre/post wraps `enforce-triad-hot-surface.py --rollover`; discovers required H1 headings from contract tests (AC-1).
- Fail-closed `ARCH_LINKAGE_ROLLOVER_BLOCKED` with metadata; `security_hard` matrix row; no partial archive write (AC-2).
- Optional `ARCH_LINKAGE_AUTO_REPAIR=0|1` default-off scratchpad comment; idempotent H1 stub restore; not in `AUTONOMY_PRESET` (AC-3).
- `/refresh-context` step 4: pre-guard → `--rollover` → post-guard → `--check`; runbook h3; `--scope=arch-linkage` parity (AC-4).
- `tests/us0129_contract_test.py` — 8 `test_us0129_*` markers; harness **26AB** (AC-5).
- Compose DEC-0054/DEC-0073/US-0049; US-0126 B-1 fixture only; L157 unchecked (AC-6).

Compose guards 8/8 UNCHANGED. FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN`.

## ACs satisfied (QA + verify-work, static-contract + UAT 7/7)

**6/6 PASS** (live pytest 8/8 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Linkage guard script pre/post `--rollover` | PASS (markers 1, 2, 6) |
| AC-2 | Fail-closed `ARCH_LINKAGE_ROLLOVER_BLOCKED` | PASS (markers 2, 3) |
| AC-3 | Optional auto-repair default-off | PASS (markers 4, 5) |
| AC-4 | `/refresh-context` wiring + runbook + parity | PASS (markers 6, 7) |
| AC-5 | 8 `test_us0129_*` + harness 26AB | PASS (all 8) |
| AC-6 | Compose guards; L157 unchecked | PASS (T-anch + status) |

## Test results (release 1st attempt — harness re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-27T08:41:43Z`, `Pass: 847 / Fail: 0` literal at L5. Grep `^\- \[FAIL\]` → 0 matches. Re-run this release spawn (prior report @ `2026-08-26T22:41:33Z` stale vs execute).
- **US-0129 live pytest** (release spawn): `python -m pytest tests/us0129_contract_test.py -q` → **8 passed in 0.58s**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=arch-linkage` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]`.
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ `2026-08-27T08:41:43Z` Pass:847/Fail:0; metadata guard exit 0; harness **re-run** this release spawn) |
| qa | PASS (`sprints/S0129/qa-findings.md`; 0 blockers; NB-1 superseded by harness re-run) |
| verify_work | PASS (`sprints/S0129/uat.json` verify_work verdict=PASS; 6/6 ACs; 7/7 UAT incl. `convergence_smoke`; 8/8 contract live) |
| uat | PASS (7/7; populated; `contract_tests_primary`; 6 live-runtime classes `UAT_PROBE_FORBIDDEN`) |
| isolation_evidence | PASS (execute+qa+verify-work+sovereign-critic in `docs/engineering/state.md`; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260827-01-verify-work-qa-20260827T082626Z-US-0129` TTL `2026-08-27T09:26:26Z` consumed @ `08:42:00Z`; proof_hash recomputed MATCH `E2680802E03BFC8C6B1F44690ED5F648E8F5C876E83AA32611B54CB908AB2280`) |
| readme_feature_coverage_3f | PASS (`coverage_missing=[]`; US-0129 OPEN excluded) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (arch_linkage pre/post + state rollover `state-pack-20260827-g.md` + `--check`) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0129 = `released`) |

## Run

```powershell
# US-0129-specific live contract test (8/8 per release spawn):
python -m pytest tests/us0129_contract_test.py -v
#   Expected: 8 passed in ~0.6s

python scripts/check_intake_template_parity.py --scope=arch-linkage
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=arch-linkage

python scripts/arch_linkage_guard.py --pre --repo .
#   Expected: exit 0 before triad rollover

python scripts/enforce-triad-hot-surface.py --rollover --repo .
python scripts/arch_linkage_guard.py --post --repo .
python scripts/enforce-triad-hot-surface.py --check --repo .
#   Expected: exit 0 after guarded rollover

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

# Consolidated harness (Pass:847/Fail:0 @ 2026-08-27T08:41:43Z):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0
```

Start command for the shipped pack (kit/scripts story — not a long-running service):

```bash
# Guarded triad rollover (wired in /refresh-context step 4):
python scripts/arch_linkage_guard.py --pre --repo .
python scripts/enforce-triad-hot-surface.py --rollover --repo .
python scripts/arch_linkage_guard.py --post --repo .
python scripts/enforce-triad-hot-surface.py --check --repo .
```

- **start_command**: `python scripts/arch_linkage_guard.py --pre --repo .` (first step of guarded rollover chain)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (scripts/docs kit — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + guarded triad `--check`, not HTTP)
- **runtime_context_ref**: `docs/engineering/runbook.md` `#### Architecture rollover linkage guard (US-0129)`; `scripts/arch_linkage_guard.py`; `tests/us0129_contract_test.py`

## Verify

1. `python -m pytest tests/us0129_contract_test.py -v` → 8 passed (confirmed per release spawn)
2. `python scripts/check_intake_template_parity.py --scope=arch-linkage` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/arch_linkage_guard.py --pre --repo .` → exit 0 on healthy repo
4. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
5. `tests/report.md` → `Fail: 0` literal at L5 (timestamp `2026-08-27T08:41:43Z`)

**expected_health_signal**: all 8 contract markers PASS; arch-linkage parity OK; harness Fail:0 post-execute; metadata guard exit 0; guarded triad `--check` exit 0.

## Credentials

- **credential_source_refs**: `n/a` (no API keys; guard operates on local repo state)
- **expected_value_source**: operator repo checkout
- **scratchpad_flags**: `ARCH_LINKAGE_AUTO_REPAIR` documented in `.cursor/scratchpad.local.md` only (default-off; no live `=1` in committed scratchpad)

## Known Issues

- **NB-1 (informational, CLOSED)**: Prior `tests/report.md` timestamp preceded execute — superseded by harness re-run @ `2026-08-27T08:41:43Z`.
- **Release remediation**: US-0130 README coverage added this spawn (DONE story drift); US-0129 architecture prose de-hashed false-positive linkage tokens (not a product scope change).

## Next

`/closure` (fresh **qe** subagent per DEC-0082) — backlog OPEN→DONE, acceptance tick L157, `sprints/S0129/closure-verification.md`. Release does not spawn closure.
