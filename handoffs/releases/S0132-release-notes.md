# Release Notes — S0132 / BUG-0016

- **Sprint**: `S0132`
- **Bug / Story**: `BUG-0016` — OpenCode Layer-1 role permissions block required lifecycle validators/writes (matrix vs kit duties)
- **Release date**: `2026-09-06T19:35:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260906-bug0016`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-BUG0016-release-20260906T193500Z-fresh`
- **model_id**: `composer-2.5` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260906-bug0016-release-release-20260906T193500Z-BUG-0016`
- **proof_hash**: `FB658AA87D763F7282EEE5279116C551AF40C5F03A4D8DEF491E09EF2538135F`
- **proof_ttl**: `2026-09-06T20:35:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS.** All mandatory release gates (1, 2, 3, 4, 4b) green with **canonical harness Fail:0** (`tests/report.md` @ `2026-09-06T20:46:57Z` Pass:851 / Fail:0, including BUG-0016 harness rows). Queue row S0132 → `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish.

Gate-1 remediation (pre-finalization): synced `template/docs/engineering/runbook.md` to active (S0131 attempt-2 drift); backfilled BUG-0015 README feature coverage after S0131 closure marked DONE; wired BUG-0016 into `tests/run-tests.ps1` / `tests/run-tests.sh` (26AD). Lesson from BUG-0015 critic: slice pytest alone is insufficient when harness Fail≠0.

## Summary

BUG-0016 amends OpenCode Layer-1 agent frontmatter (active+template) so role duties match kit contracts while preserving success test (c):

- `po` / `tech-lead` / `curator`: `bash: ask` (AC-1)
- PO edit: `handoffs/intake_evidence/**` + `handoffs/resume_brief.md` + `docs/engineering/state.md`; `**` deny last (AC-2)
- Sprint globs: `sprints/S*/…` (not `Sxxxx`) (AC-3)
- Release duty paths: release-findings + verify-work-to-release + state + resume_brief + runbook (AC-4)
- Success test (c): non-dev no production/code allow (AC-5)
- `security` / `auto` unchanged (AC-6)
- Active↔template agent parity (AC-7)
- DEC-0122 §2 sole matrix SOT; us0122 intentional realign; no DEC-0130 (AC-8)
- T-007: plugin write-guard path-based only; DEC-0124/0125 untouched (DQ8)

FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN`. No fake browser PASS.

## ACs satisfied (QA + verify-work, UAT 9/9)

**8/8 PASS** (live pytest 7/7 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | po/tl/curator `bash: ask` | PASS (marker 1) |
| AC-2 | PO intake_evidence/** + resume_brief + state; deny-last | PASS (marker 2) |
| AC-3 | `sprints/S*/…` globs (not Sxxxx) | PASS (marker 3) |
| AC-4 | Release duty paths complete | PASS (marker 4) |
| AC-5 | Success test (c) preserved | PASS (marker 5) |
| AC-6 | security / auto unchanged | PASS (marker 6) |
| AC-7 | Active ↔ template agent parity | PASS (marker 7) |
| AC-8 | DEC-0122 §2 sole SOT; us0122 realign | PASS (us0122 8/8) |

## Test results (release)

- **BUG-0016 live pytest**: `python -m pytest tests/bug0016_contract_test.py -v` → **7 passed**.
- **Compose**: `python -m pytest tests/us0122_contract_test.py -q` → **8 passed**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=bug-0016` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo . --json` → `OK` / `violations: []`.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]` (BUG-0015 DONE covered; BUG-0016 OPEN excluded).
- **Canonical harness** (`tests/report.md`): timestamp `2026-09-06T20:46:57Z`, **`Pass: 851 / Fail: 0`** — includes `[PASS] check_intake_template_parity --scope=bug-0016` + `[PASS] BUG-0016 contract tests pass`.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` Fail:0 + bug0016 7/7 + us0122 8/8 + parity bug-0016 + US-0071 metadata; `harness_fail_zero_claimed=true`) |
| qa | PASS (`sprints/S0132/qa-findings.md`; 0 blockers; NB-1..NB-3 informational) |
| verify_work | PASS (`sprints/S0132/uat.json` verdict=PASS; 8/8 ACs; 9/9 UAT incl `convergence_smoke`; 7/7 contract live) |
| uat | PASS (9/9; populated; `contract_tests_primary`; 6 live-runtime classes `UAT_PROBE_FORBIDDEN`) |
| isolation_evidence | PASS (execute+qa+verify-work+sovereign-critic+release; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260906-bug0016-verify-work-qa-20260906T192500Z-BUG-0016` TTL `2026-09-06T20:25:00Z` consumed @ `19:35:00Z`; proof_hash recomputed MATCH `C9DE18A187C251AEC3081E43EA65645CBA3B7C8341D0F10639567CF3224B5B41`) |
| readme_feature_coverage_3f | PASS (`coverage_missing=[]`; BUG-0016 OPEN excluded; BUG-0015 DONE backfilled) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (`enforce-triad-hot-surface.py --check` exit 0) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0132 = `released`) |

## Run

```powershell
# BUG-0016-specific live contract test (7/7):
python -m pytest tests/bug0016_contract_test.py -v
#   Expected: 7 passed

python -m pytest tests/us0122_contract_test.py -q
#   Expected: 8 passed

python scripts/check_intake_template_parity.py --scope=bug-0016
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=bug-0016

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

python scripts/validate_readme_feature_coverage.py --repo . --enforce
#   Expected: [README_FEATURE_COVERAGE_VALIDATE_OK]

# Canonical harness (Fail:0 required for gate-1):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: tests/report.md Fail: 0
```

Start command for the shipped pack (kit/OpenCode permission-matrix story — not a long-running HTTP service):

```bash
# Validate Layer-1 agent frontmatter contract:
python -m pytest tests/bug0016_contract_test.py -v
```

- **start_command**: `python -m pytest tests/bug0016_contract_test.py -v` (operator validation; live OpenCode agent probe not required for this CI slice)
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` (OpenCode host / DEC-0122 compose); `docs/engineering/runtime-connectivity.md` (local kit — no remote service)

## Connect

- **service_url**: `n/a` (OpenCode agent permission contract — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + Fail:0 harness, not HTTP)

## Verify

1. `python -m pytest tests/bug0016_contract_test.py -v` → 7 passed
2. `python -m pytest tests/us0122_contract_test.py -q` → 8 passed
3. `python scripts/check_intake_template_parity.py --scope=bug-0016` → `[INTAKE_TEMPLATE_PARITY_OK]`
4. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
5. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`
6. `tests/report.md` header shows **Fail: 0** (incl. BUG-0016 harness rows)
7. Spot-check: `.opencode/agents/{po,tech-lead,curator}.md` have `bash: ask`; sprint keys use `S*`

**expected_health_signal**: all 7 `test_bug0016_*` markers PASS; us0122 8/8; parity bug-0016 OK; metadata guard exit 0; README enforce OK; harness Fail:0; backlog BUG-0016 remains OPEN until `/closure`.

## Credentials

- **credential_source_refs**: `n/a` (no API keys required for contract-test verify)
- **expected_value_source**: operator OpenCode host + local kit checkout; no inline secrets

## Known Issues

None blocking.

- **NB-1** (informational): Keep `S*` (not `S[0-9]*`); deny-last + non-dev no production allow; T-007 no-double-deny.
- **NB-2** (informational): DEC-0122 §2 sole SOT; CF2 runbook Layer-1 allow ≠ US-0126 ownership; no DEC-0130.
- **NB-3** (informational): Do not mark BUG-0016 DONE at release; do not tick acceptance; do not reopen BUG-0015 / US-0131 / US-0132; no `bash:allow`; no live OpenCode probe.

## Evidence refs

- `tests/report.md` (@ 2026-09-06T20:46:57Z — Fail:0)
- `sprints/S0132/qa-findings.md` (QA_PASS)
- `sprints/S0132/uat.json`, `sprints/S0132/uat.md` (verify-work PASS)
- `sprints/S0132/summary.md`
- `sprints/S0132/release-findings.md`
- `docs/engineering/state.md` (execute / qa / verify-work / sovereign-critic / release checkpoints)

## Next phase

`/closure` (fresh **qe** subagent, ship macro phase 2 of 3 per DEC-0082). Release does **not** spawn closure. Backlog BUG-0016 remains **OPEN**; acceptance L181 remains **unchecked** until closure.
