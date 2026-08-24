# Release Notes — S0123 / US-0123

- **Sprint**: `S0123`
- **Story**: `US-0123` — Per-role OpenCode model slug routing (multi-provider example catalog + materializer + fail-closed validator + 8 contract-test markers)
- **Release date**: `2026-08-24T15:32:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260824-01`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0123-release-20260824T153200Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260824-01-release-release-20260824T153200Z-US-0123`
- **proof_hash**: `EED2303A06C30EB5DAC490D738B95F1B1D7E281A0CF20F1DCC6C8B8E7ECD81F6`
- **proof_ttl**: `2026-08-24T16:32:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump per S0121/S0122 precedent)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0123 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=disabled` → deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Harness **not re-run** this spawn — accepted `tests/report.md` @ `2026-08-24T15:12:17Z` Pass:845 / Fail:0 per orchestrator gate-1 brief (post execute harness-refresh; later QA/verify-work checkpoints appended `state.md` only as triad oversize process artifact).

## Summary

US-0123 ships **per-role OpenCode model slug routing** for the its-magic kit:

- Example catalog `template/.opencode/model-catalog.local.example.json` (8 roles, placeholder slugs, 6 providers).
- Materializer `scripts/opencode_model_catalog_apply.py` (no-op when catalog absent; fail-closed `OPENCODE_MODEL_SLUG_UNKNOWN`; injects into installed `.opencode/agents/*.md` only).
- Triple-installer hook when `--host opencode|both` and catalog present (`installer.py`, `installer.ps1` `-InstallHost`, `installer.sh`).
- Validator extension `scripts/model_tier_validate.py --scope opencode-catalog` (+ template mirror).
- Contract tests `tests/us0123_contract_test.py` (8 markers) byte-identical to `template/tests/us0123_contract_test.py`.
- Runbook `## OpenCode model slug routing (US-0123)` h2 mirrored byte-identical to `template/docs/engineering/runbook.md`.
- `OPENCODE_ADAPTER_PAIRS` extended in `scripts/check_intake_template_parity.py` (`--scope=opencode-adapter`).

Compose guards 6/6 UNCHANGED (additive only): backlog US-0123 OPEN; acceptance unchecked; architecture `# US-0123` anchor; DEC-0123 Accepted; template agents omit `model:`; runbook + manifest mirrors byte-identical.

## ACs satisfied (QA loop-2 + verify-work loop-2, live + static-contract)

**10/10 PASS** (live pytest 8/8 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Resolution chain | PASS (markers 1, 6) |
| AC-2 | Multi-provider examples | PASS (marker 3 — 6 providers) |
| AC-3 | No vendor IDs in template | PASS (markers 1, 2, 3) |
| AC-4 | Unknown slug fail-closed | PASS (markers 5, 6) |
| AC-5 | Auth store | PASS (marker 7) |
| AC-6 | Compose US-0101/US-0102 | PASS (marker 8 — Cursor unchanged) |
| AC-7 | Per-role assignment | PASS (marker 4) |
| AC-8 | Contract tests | PASS (8/8 live) |
| AC-9 | Chinese APIs as capability | PASS (marker 4) |
| AC-10 | Tool-calling quality | PASS (runbook h2 byte-identical) |

## Test results (release 1st attempt — harness NOT re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-24T15:12:17Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `\[FAIL\]` → 0 matches. US-0071 metadata guard coverage rows present (L712–L717). Accepted as gate-1 evidence (execute harness-refresh @ `2026-08-24T15:12:30Z`; no product/test mutations after 15:12:17Z from qa/verify-work phases).
- **US-0123 live pytest** (verify-work loop-2, 2026-08-24T15:24:00Z): `python -m pytest tests/us0123_contract_test.py -v` → **8/8 PASSED in 0.20s** (Python 3.12.10; pytest 9.1.1).
- **Parity**: `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Validator**: `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` → `[MODEL_TIER_VALIDATION_OK]`.
- **Runbook byte-identical**: SHA-256 `66ee024a...` equal active+template (196778 bytes both sides).

## Compose guards

**6/6 UNCHANGED** — backlog OPEN L4248; acceptance unchecked L151; architecture US-0123 anchor; DEC-0123 Accepted; template agents no `model:`; mirrors byte-identical (release does not mutate backlog/acceptance/architecture/DEC-0123).

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ 2026-08-24T15:12:17Z Pass:845 / Fail:0 literal; zero `[FAIL]` rows; metadata guard rows L712–L717; harness not re-run this release spawn) |
| qa | PASS (`sprints/S0123/qa-findings.md` loop-2; 0 blockers; 1 non-blocking carry-forward) |
| verify_work | PASS (`sprints/S0123/uat.json` 10/10; verify-work loop-2 8/8 contract live) |
| uat | PASS (10/10 ACs; not placeholder) |
| isolation_evidence | PASS (execute harness-refresh, qa loop-2, verify-work loop-2 in `docs/engineering/state.md`; distinct `fresh_context_marker`; `model_id` set; phase role alignment OK) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260824-01-verify-work-qa-20260824T152400Z-US-0123` TTL 2026-08-24T16:24:00Z > release now 15:32:00Z; proof_hash `5DBDB6549E0E7841974CE7A8D8FE81889AB7ADD0ED79F8FA10AF4C4CD7CA3BE8`; no reuse) |
| readme_feature_coverage_3f | deferred (kit/pack story; harness rows pass) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1` per S0114..S0122 precedent) |
| backlog_reconciliation | not performed (closure owns per US-0120) |
| publish | skipped (`RELEASE_PUBLISH_MODE=disabled`) |
| sync | not_eligible (`SYNC_DISABLED`) |
| finalization | **PASS** (queue row S0123 = `released`) |

## Run

```powershell
# US-0123-specific live contract test (8/8 per verify-work loop-2 2026-08-24T15:24:00Z):
python -m pytest tests/us0123_contract_test.py -v
#   Expected: 8 passed in ~0.20s

python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter

python scripts/model_tier_validate.py --scope opencode-catalog --repo .
#   Expected: [MODEL_TIER_VALIDATION_OK]

# Consolidated harness (already Pass:845 / Fail:0 @ 2026-08-24T15:12:17Z — re-run only if product/tests change):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0; zero [FAIL] rows
```

Start command for the shipped pack (kit/template story — not a service):

```bash
# Install kit with OpenCode host + optional catalog materialization:
its-magic --target <repo> --mode missing --host opencode
# Or both hosts:
its-magic --target <repo> --mode missing --host both
# Place operator catalog at .opencode/model-catalog.local.json (gitignored) before install for slug injection
```

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (pack/contract story — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests, not HTTP)
- **runtime_context_ref**: kit repo — `template/.opencode/model-catalog.local.example.json`; operator catalog `.opencode/model-catalog.local.json` (local-only, gitignored)

## Verify

1. `python -m pytest tests/us0123_contract_test.py -v` → 8 passed (confirmed per verify-work loop-2)
2. `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` → `[MODEL_TIER_VALIDATION_OK]`
4. `tests/report.md` → `Fail: 0` literal at L5; zero `[FAIL]` rows (timestamp ≥ 2026-08-24T15:12:17Z)
5. `docs/engineering/runbook.md` → `## OpenCode model slug routing (US-0123)` h2 present + byte-identical mirror
6. `rg "^model:" template/.opencode/agents` → 0 matches (no vendor slugs in template)

**expected_health_signal**: all contract markers PASS; parity OK; validator OK; harness Fail:0 when last product-changing execute completed.

## Credentials

- **credential_source_refs**: `n/a` (API keys via OpenCode `/connect`; never in template or git)
- **expected_value_source**: operator places keys in OpenCode auth store; catalog uses placeholder slugs only (`<your-*-slug>`)

## Known Issues

- `ik_us0123_installer_hook_not_contract_tested` — installer `--host opencode|both` hook not pytest-marked (non-blocking; integration-level coverage via installer parity + manual spot-check).

## Evidence refs

- `tests/report.md` (@ 2026-08-24T15:12:17Z)
- `sprints/S0123/qa-findings.md` (loop-2)
- `sprints/S0123/verify-work-findings.md` (loop-2)
- `sprints/S0123/uat.json`, `sprints/S0123/uat.md`
- `sprints/S0123/release-findings.md`
- `sprints/S0123/summary.md`
- `handoffs/verify_to_release.md`
- `docs/engineering/state.md` (execute harness-refresh / qa loop-2 / verify-work loop-2 checkpoints)
- `decisions/DEC-0123.md`

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick, `sprints/S0123/closure-verification.md`. Release does NOT spawn closure.
