# Release Notes — S0124 / US-0124

- **Sprint**: `S0124`
- **Story**: `US-0124` — OpenCode orchestrator plugin Task-spawns US-0069 roles, never executes phase work in-session
- **Release date**: `2026-08-24T19:35:00Z` (UTC)
- **orchestrator_run_id**: `auto-20260824-02`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release is phase 1 of 3: release → closure → refresh-context per DEC-0082)
- **policy_mode**: `confirm` (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → no publish execution)
- **trigger_source**: `auto`
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `rel-US0124-release-20260824T193500Z-fresh`
- **model_id**: `composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- **runtime_proof_id**: `rp-auto-20260824-02-release-release-20260824T193500Z-US-0124`
- **proof_hash**: `21738212CD0C94494ECB8951B233CFD0FFE663852BDF643E0598AE83E8043777`
- **proof_ttl**: `2026-08-24T20:35:00Z` (UTC)
- **release_version**: (none — workflow-only release; no semver bump per S0121/S0122/S0123 precedent)

## Verdict

**RELEASE_PASS (1st attempt).** All mandatory release gates (1, 2, 3, 4, 4b) green. Queue row S0124 transitions to `released`. No backlog mutation (closure owns OPEN→DONE + acceptance tick per US-0120 / DEC-0082). No publish (`RELEASE_PUBLISH_MODE=confirm` + `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `PUBLISH_CONFIRMATION_REQUIRED` / deterministic no-op). No sync (`SYNC_POLICY_MODE=disabled` → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`).

Harness **not re-run** this spawn — accepted `tests/report.md` @ `2026-08-24T19:17:58Z` Pass:845 / Fail:0 per orchestrator gate-1 brief (post execute loop-2 harness refresh; later QA/verify-work/release checkpoints appended `state.md` only as triad oversize process artifact).

## Summary

US-0124 ships the **spawn-only OpenCode orchestrator plugin** for `/auto`:

- Plugin `template/.opencode/plugins/orchestrator.ts` — v2 `Plugin.define` with `ctx.session.create` spawn isolation, `ctx.tool.hook("execute.before")` write-guard, US-0069 phase→role matrix, US-0092 stop-matrix dispatch, headless `opencode run` argv builder.
- Mock harness `tests/us0124/mock_ctx.ts` + `tests/us0124/run_harness.mjs` (Node `--experimental-strip-types`; no live OpenCode runtime per AC-10).
- Contract tests `tests/us0124_contract_test.py` (12 markers) byte-identical to `template/tests/us0124_contract_test.py`.
- Runbook `## OpenCode orchestrator plugin reason codes (US-0124)` h2 stub (4 new `OPENCODE_*` + 3 reused codes); byte-identical `template/docs/engineering/runbook.md` mirror.
- Additive argv on `scripts/auto_outer_driver.py` (`--phase/--role/--story/--sprint/--orchestrator-run-id/--stop-reason` → JSON); legacy `run_driver()` byte-identical when flags absent; template mirror.
- `OPENCODE_ADAPTER_PAIRS` extended in `scripts/check_intake_template_parity.py` (`--scope=opencode-adapter`).
- Installer manifest row for `template/.opencode/plugins/orchestrator.ts` under `[opencode_install_include_paths]`.

Execute loop-2 remediated pre-existing B-1 (US-0123 README feature-coverage gap in `docs/developer/README.md` `## Quality gates`) — not US-0124 product scope; harness refreshed to Pass:845 / Fail:0.

Compose guards 9/9 UNCHANGED (additive only): backlog US-0124 OPEN; acceptance unchecked; architecture `# US-0124` anchor; DEC-0124 Accepted; no `.cursor/commands/auto.md` clone; mirrors byte-identical.

## ACs satisfied (QA loop-2 + verify-work, live + static-contract)

**11/11 PASS** (live pytest 12/12 green):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | Spawn-only `/auto` | PASS (markers 1, 7) |
| AC-2 | US-0069 resolve | PASS (marker 10) |
| AC-3 | Isolation evidence | PASS (markers 1, 2) |
| AC-4 | Success test (a) | PASS (marker 2) |
| AC-5 | Success test (d) | PASS (markers 2 + 8) |
| AC-6 | Stop matrix | PASS (T-004 + marker 8) |
| AC-7 | Headless `--invoke-cmd` | PASS (marker 8) |
| AC-8 | Subtask-ignored fail-closed | PASS (markers 3, 4, 5) |
| AC-9 | No US-0095 port | PASS (markers 6, 7) |
| AC-10 | Contract tests | PASS (12/12 live) |
| AC-11 | Secrets | PASS (marker 9) |

## Test results (release 1st attempt — harness NOT re-run)

- **Canonical harness** (`tests/report.md`): timestamp `2026-08-24T19:17:58Z`, `Pass: 845 / Fail: 0` (literal zero at L5). Grep `\[FAIL\]` → 0 matches. Metadata guard coverage rows present (L712–L717). Accepted as gate-1 evidence (execute loop-2 harness refresh; no product/test mutations after 19:17:58Z from qa/verify-work/release phases).
- **US-0124 live pytest** (verify-work, 2026-08-24T19:28:00Z): `python -m pytest tests/us0124_contract_test.py -v` → **12/12 PASSED in 1.14s**.
- **Parity**: `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **README feature coverage**: `validate_readme_feature_coverage --report` → PASS `coverage_missing=[]` (B-1 closed in execute loop-2).
- **Runbook byte-identical**: active ↔ template (197981 bytes each per execute summary).

## Compose guards

**9/9 UNCHANGED** — US-0069/DEC-0051, US-0092/DEC-0078, US-0095/DEC-0080, US-0023/US-0048/BUG-0006, US-0005, US-0122/DEC-0122, US-0121/DEC-0120, US-0125, US-0102/DEC-0087 (release does not mutate backlog/acceptance/architecture/DEC-0124).

## Gate summary

| Gate | Result |
|------|--------|
| check_in_tests | **PASS** (`tests/report.md` @ 2026-08-24T19:17:58Z Pass:845 / Fail:0 literal; zero `[FAIL]` rows; metadata guard rows L712–L717; harness not re-run this release spawn) |
| qa | PASS (`sprints/S0124/qa-findings.md` loop-2; 0 blockers; B-1 closed) |
| verify_work | PASS (`sprints/S0124/uat.json` 11/11; verify-work 12/12 contract live) |
| uat | PASS (11/11 ACs; populated; not placeholder) |
| isolation_evidence | PASS (execute loop-2, qa loop-2, verify-work in `docs/engineering/state.md`; distinct `fresh_context_marker`; `model_id` set; phase role alignment OK) |
| strict_runtime_proof | **PASS** (verify-work `rp-auto-20260824-02-verify-work-qa-20260824T193000Z-US-0124` TTL 2026-08-24T20:30:00Z consumed @ release 19:35:00Z; proof_hash `C1453A18FFF838E5ADAB069E930F82F9B87C7CAC176C4D7DAAC7F8E77FB24B89`; no reuse) |
| readme_feature_coverage_3f | deferred (kit/plugin story; harness rows pass; B-1 closed) |
| project_readme_3g | skipped (`FRAMEWORK_KIT_REPO=1` per S0114..S0123 precedent) |
| triad_regression | PASS (`enforce-triad-hot-surface.py --check` exit 0; `--rollover` exit 0 post-release) |
| backlog_reconciliation | not performed (closure owns per US-0120) |
| publish | skipped (`RELEASE_PUBLISH_MODE=confirm`; `RELEASE_PUBLISH_AUTO_CONFIRM=0` → `publish_snapshot=skipped_pending_operator_confirm`) |
| sync | not_eligible (`SYNC_DISABLED`) |
| finalization | **PASS** (queue row S0124 = `released`) |

## Run

```powershell
# US-0124-specific live contract test (12/12 per verify-work 2026-08-24T19:28:00Z):
python -m pytest tests/us0124_contract_test.py -v
#   Expected: 12 passed in ~1.1s

python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter
#   Expected: [INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter

# Outer driver additive argv smoke (UAT-6):
python scripts/auto_outer_driver.py --phase execute --role dev --story US-0124 --sprint S0124 --orchestrator-run-id auto-20260824-02 --stop-reason none
#   Expected: JSON {action:spawn_next, phase:execute, role:dev}

# Consolidated harness (already Pass:845 / Fail:0 @ 2026-08-24T19:17:58Z — re-run only if product/tests change):
powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"
#   Expected: exit 0; tests/report.md Fail: 0; zero [FAIL] rows
```

Start command for the shipped pack (kit/template story — not a long-running service):

```bash
# Install kit with OpenCode host (plugin ships under template/.opencode/plugins/):
its-magic --target <repo> --mode missing --host opencode
# Or both hosts:
its-magic --target <repo> --mode missing --host both
# Plugin composes with template/.opencode/agents/auto.md — spawn-only /auto on OpenCode
```

- **start_command**: `its-magic --target <repo> --mode missing --host opencode` (or `--host both`)
- **runtime_mode**: `local`

## Connect

- **runtime_mode**: `local`
- **service_url**: `n/a` (pack/contract story — no service endpoint)
- **service_port**: `n/a`
- **health_endpoint**: `n/a` (health = contract tests + Node harness, not HTTP)
- **runtime_context_ref**: kit repo — `template/.opencode/plugins/orchestrator.ts`; `template/.opencode/agents/auto.md`; mock harness `tests/us0124/run_harness.mjs`

## Verify

1. `python -m pytest tests/us0124_contract_test.py -v` → 12 passed (confirmed per verify-work)
2. `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`
3. `python scripts/validate_readme_feature_coverage.py --repo . --report` → `status:PASS`, `coverage_missing:[]`
4. `tests/report.md` → `Fail: 0` literal at L5; zero `[FAIL]` rows (timestamp ≥ 2026-08-24T19:17:58Z)
5. `docs/engineering/runbook.md` → `## OpenCode orchestrator plugin reason codes (US-0124)` h2 present + byte-identical mirror
6. `rg "\.cursor/commands/auto\.md|AUTO_LOOP_MAX_CYCLES" template/.opencode/plugins/orchestrator.ts` → 0 matches (no Cursor clone)

**expected_health_signal**: all 12 contract markers PASS; opencode-adapter parity OK; harness Fail:0 when last product-changing execute loop-2 completed; plugin spawn-only with distinct `OPENCODE_*` reason codes.

## Credentials

- **credential_source_refs**: `n/a` (API keys via OpenCode `/connect`; never in template or git; plugin has zero `process.env` / secret references per AC-11)
- **expected_value_source**: operator places keys in OpenCode auth store; plugin does not log credentials

## Known Issues

None.

## Evidence refs

- `tests/report.md` (@ 2026-08-24T19:17:58Z)
- `sprints/S0124/qa-findings.md` (loop-2 PASS)
- `sprints/S0124/uat.json`, `sprints/S0124/uat.md`
- `sprints/S0124/summary.md`
- `sprints/S0124/release-findings.md`
- `handoffs/verify_to_release.md` (if present)
- `docs/engineering/state.md` (execute loop-2 / qa loop-2 / verify-work / release checkpoints)
- `decisions/DEC-0124.md`

## Next phase

**`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082) — backlog OPEN→DONE, acceptance tick, `sprints/S0124/closure-verification.md`. Release does NOT spawn closure.
