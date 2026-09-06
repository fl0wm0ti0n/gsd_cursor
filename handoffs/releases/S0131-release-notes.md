# Release Notes — S0131 / BUG-0015

- **Sprint**: `S0131`
- **Bug / Story**: `BUG-0015` — OpenCode `/auto` never triggers orchestrator plugin dispatch and stops at command STOP
- **Release date**: `2026-09-06T15:30:00Z` (UTC) — **attempt 2** (gate-1 remediation re-run)
- **orchestrator_run_id**: `auto-20260906-bug0015`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-BUG0015-release-rerun-20260906T153000Z-fresh`
- **model_id**: `composer-2.5` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260906-bug0015-release-release-20260906T153000Z-BUG-0015`
- **proof_hash**: `1467A9436D9012A5974AC13C269E28EDFA1D1E9821BA3C94422E1DAB4D8FAD00`
- **proof_ttl**: `2026-09-06T16:30:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump)

## Verdict

**RELEASE_PASS (2nd attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green with **canonical harness Fail:0** (`tests/report.md` @ `2026-09-06T15:28:42Z` Pass:849 / Fail:0). Queue row S0131 remains `released` (idempotent). No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish. Critic `ik_bug0015_release_gate1_fail_nonzero` resolved after Homebrew → `0.1.3-6` remediation.

Attempt 1 (`2026-09-06T15:15:00Z`) was blocked by sovereign-critic for claiming PASS under Fail:3 — superseded by this re-run.

## Summary

BUG-0015 wires interactive `/auto` on the OpenCode host so the orchestrator plugin owns spawn:

- Primary attach: `command.transform` / `editor.add({ name: "auto", execute })` → `runAutoLifecycle` → `spawnPhase` / stop-matrix loop (AC-1).
- Missing attach → `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED` (AC-2).
- Missing `session.create` → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` (compose DEC-0124) (AC-3).
- IsolationEvidence minimum fields + Python `opencode_auto_bridge.py` → `state.md` SOT (AC-4).
- Concurrent `/auto` → `OPENCODE_AUTO_ALREADY_RUNNING` (mutex TTL `Date.now()` 7200s / clear-on-exit) (AC-5).
- `auto.md` remains dispatch-only (≤20 lines, no spawn literals) active+template (AC-6).
- Compose US-0124 spawn API / DEC-0124/0125 bodies UNCHANGED (AC-7).
- Seven additive `test_bug0015_*` markers green via mock-ctx harness (AC-8).

FRAMEWORK_KIT_REPO=1 — UAT probe class `contract_tests_primary`; 6 live-runtime classes waived `UAT_PROBE_FORBIDDEN`. No fake browser PASS.

## ACs satisfied (QA + verify-work, UAT 9/9)

**8/8 PASS** (live pytest 7/7 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | `/auto` starts plugin spawn via host attach | PASS (markers 1, 2) |
| AC-2 | Missing attach fail-closed | PASS (marker 3) |
| AC-3 | Missing `session.create` fail-closed | PASS (marker 4) |
| AC-4 | IsolationEvidence + state.md bridge | PASS (marker 2 + bridge; NB-1 informational) |
| AC-5 | Concurrent `/auto` mutex | PASS (marker 5) |
| AC-6 | `auto.md` dispatch-only | PASS (marker 6) |
| AC-7 | Compose US-0124 spawn API unchanged | PASS (marker 7 + us0124 12/12) |
| AC-8 | Seven additive `test_bug0015_*` | PASS (7/7) |

## Test results (release 2nd attempt)

- **BUG-0015 live pytest** (release re-run): `python -m pytest tests/bug0015_contract_test.py -v` → **7 passed in 0.69s**.
- **Compose**: `python -m pytest tests/us0124_contract_test.py -q` → **12 passed in 1.46s**.
- **Parity**: `python scripts/check_intake_template_parity.py --scope=bug-0015` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Metadata guard**: `python scripts/check-user-visible-metadata.py --repo . --json` → `OK` / `violations: []`.
- **README feature coverage**: `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]` (BUG-0015 OPEN — excluded).
- **Canonical harness** (`tests/report.md`): timestamp `2026-09-06T15:28:42Z`, **`Pass: 849 / Fail: 0`** — zero `[FAIL]` rows; Homebrew stable formula URL+version match npm `0.1.3-6`; Active context surface assert PASS.

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` Fail:0 + bug0015 7/7 + us0124 12/12 + parity bug-0015 + US-0071 metadata; `harness_fail_zero_claimed=true`) |
| qa | PASS (`sprints/S0131/qa-findings.md`; 0 blockers; NB-1..NB-3 informational) |
| verify_work | PASS (`sprints/S0131/uat.json` verdict=PASS; 8/8 ACs; 9/9 UAT incl `convergence_smoke`; 7/7 contract live) |
| uat | PASS (9/9; populated; `contract_tests_primary`; 6 live-runtime classes `UAT_PROBE_FORBIDDEN`) |
| isolation_evidence | PASS (execute+remediation+qa+verify-work+critic+release-rerun in `docs/engineering/state.md`; distinct markers; `model_id` set) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260906-bug0015-verify-work-qa-20260906T150500Z-BUG-0015` TTL `2026-09-06T16:05:00Z` consumed @ `15:30:00Z`; proof_hash recomputed MATCH `165F812E5357B9DC0BF07AC07628F96D62BB10DFA2056F7EA2C97ADE8C5A4117`) |
| readme_feature_coverage_3f | PASS (`coverage_missing=[]`; BUG-0015 OPEN excluded) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1`) |
| metadata_guard | PASS |
| triad_regression | PASS (`enforce-triad-hot-surface.py --check` exit 0) |
| critic_findings | **resolved** (`ik_bug0015_release_gate1_fail_nonzero` → 3 rows `status=resolved`) |
| backlog_reconciliation | not performed (closure owns per US-0120 / DEC-0082) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0`) |
| sync | not_eligible (`SYNC_POLICY_MODE=disabled`) |
| finalization | **PASS** (queue row S0131 = `released`, idempotent) |

## Run

```powershell
# BUG-0015-specific live contract test (7/7):
python -m pytest tests/bug0015_contract_test.py -v
#   Expected: 7 passed

python -m pytest tests/us0124_contract_test.py -q
#   Expected: 12 passed

python scripts/check_intake_template_parity.py --scope=bug-0015
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=bug-0015

python scripts/check-user-visible-metadata.py --repo .
#   Expected: exit 0 (silent PASS)

python scripts/validate_readme_feature_coverage.py --repo . --enforce
#   Expected: [README_FEATURE_COVERAGE_VALIDATE_OK]

# Canonical harness (Fail:0 required for gate-1):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: tests/report.md Fail: 0
```

Start command for the shipped pack (kit/OpenCode plugin story — not a long-running HTTP service):

```bash
# In an OpenCode host with the .opencode/ pack installed:
# Invoke /auto — plugin command.transform attach should start runAutoLifecycle.
python -m pytest tests/bug0015_contract_test.py -v
```

- **start_command**: `python -m pytest tests/bug0015_contract_test.py -v` (operator validation; interactive `/auto` attach is host-runtime)
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runbook.md` `### OpenCode /auto dispatch attach reason codes (BUG-0015)`; `docs/engineering/runtime-connectivity.md` (local kit — no remote service)

## Connect

- **service_url**: `n/a` (OpenCode plugin / contract-test kit — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + parity CLI + Fail:0 harness, not HTTP)

## Verify

1. `python -m pytest tests/bug0015_contract_test.py -v` → 7 passed
2. `python -m pytest tests/us0124_contract_test.py -q` → 12 passed
3. `python scripts/check_intake_template_parity.py --scope=bug-0015` → `[INTAKE_TEMPLATE_PARITY_OK]`
4. `python scripts/check-user-visible-metadata.py --repo .` → exit 0
5. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`
6. `tests/report.md` header shows **Fail: 0** (post Homebrew `0.1.3-6` sync)
7. In OpenCode (optional live): `/auto` advances via plugin spawn or fails closed with documented `OPENCODE_*` reason code — not required for this CI slice

**expected_health_signal**: all 7 `test_bug0015_*` markers PASS; us0124 12/12; parity bug-0015 OK; metadata guard exit 0; README enforce OK; harness Fail:0; backlog BUG-0015 remains OPEN until `/closure`.

## Credentials

- **credential_source_refs**: `n/a` (no API keys required for contract-test verify)
- **expected_value_source**: operator OpenCode host + local kit checkout; no inline secrets

## Known Issues

None blocking.

- **NB-1** (informational): IsolationEvidence Python bridge soft-continue on `DRIVER_INVOKE_FAILED` (only `OPENCODE_SUBTASK_IGNORED` fail-closes lifecycle).
- **NB-2** (informational): `event.subscribe` secondary attach when transform missing — intended CF1/CF6 defense.
- **NB-3** (informational): Scope held — BUG-0016 / live OpenCode CI probe / DEC amend / DONE flip out of scope.

## Evidence refs

- `tests/report.md` (@ 2026-09-06T15:28:42Z — Fail:0)
- `sprints/S0131/qa-findings.md` (QA_PASS)
- `sprints/S0131/uat.json`, `sprints/S0131/uat.md` (verify-work PASS)
- `sprints/S0131/summary.md` (incl. Homebrew remediation)
- `sprints/S0131/release-findings.md`
- `docs/engineering/state.md` (execute / remediation / qa / verify-work / sovereign-critic / release re-run checkpoints)

## Next phase

`/closure` (fresh **qe** subagent, ship macro phase 2 of 3 per DEC-0082). Release does **not** spawn closure. Backlog BUG-0015 remains **OPEN**; acceptance L180 remains **unchecked** until closure.
