# Release Notes — S0074 / US-0086

- **sprint_id**: S0074
- **story_refs**: US-0086
- **release_date**: 2026-04-13T22:30:00Z
- **orchestrator_run_id**: auto-20260405-01
- **verdict**: **PASS**

## Summary

**US-0086**: automation-driven remote execution selection (Docker / SSH / NL
container intent).

Release finalizes deterministic automation routing controls, intent literal
handling (`start container <target_id>`), fail-closed reason codes, and
evidence tuple continuity from execute through verify-work and release.

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

- **verification_steps**:
  1. Run `python -m pytest tests/auto_command_contract_test.py -q` — expect 19 passed, 94 subtests.
  2. Run `python -m pytest tests/remote_config_summary_test.py -q` — expect 4 passed.
  3. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` — expect baseline pass profile with only pre-existing failures.
  4. Confirm `sprints/S0074/qa-findings.md` is PASS and `sprints/S0074/uat.json` is 10/10 pass.
  5. Confirm release queue row `S0074` is `released` and backlog/acceptance are reconciled.
- **expected_health_signal**: Release artifacts complete; canonical status surfaces show `US-0086` as `DONE`.

## Credentials

- Env-reference-only policy remains in effect; no inline secrets in artifacts.
- Remote/release connectivity values are referenced by env var names only.

## Known Issues

- `tests/run-tests.ps1` still reports pre-existing failures outside US-0086 scope.

## Gate audit snapshot (US-0039)

| gate | verdict | reason_code | evidence_refs |
|------|---------|-------------|---------------|
| check-in_test | pass | - | `tests/report.md` baseline from QA gating |
| qa | pass | - | `sprints/S0074/qa-findings.md` |
| uat | pass | - | `sprints/S0074/uat.json`, `sprints/S0074/uat.md` |
| isolation | pass | - | `docs/engineering/state.md` |
| strict_proof | pass | - | `docs/engineering/state.md` |
| scratchpad_pair | pass | - | `sprints/S0074/qa-findings.md` |
| metadata_guard | pass | - | `sprints/S0074/qa-findings.md` |
| bug_validate | pass | - | `sprints/S0074/qa-findings.md` |
| finalization | pass | - | this file, `handoffs/release_queue.md`, `handoffs/release_notes.md` |

## Publish status

- **RELEASE_PUBLISH_MODE**: `confirm`
- **publish_snapshot**: `skipped_pending_operator_confirm`
- Operator confirmation is required before any publish target execution.

## Sync (DEC-0018)

- **ALLOW_AUTO_PUSH**: `0`
- **push_decision**: `not_eligible`
- **reason_code**: `MANUAL_MODE_NO_AUTO`

## Strict runtime proof

- **orchestrator_run_id**: `auto-20260405-01`
- **runtime_proof_id**: `rp-auto-20260405-01-release-release-20260413T223000Z-S0074-US0086`
- **phase_id**: `release`
- **role**: `release`
- **proof_issued_at**: `2026-04-13T22:30:00Z`
- **proof_ttl_seconds**: `3600`
- **proof_hash**: `3bc64c2345bb8861075d957ae665280da80f41d0ce21ba4caa6e55e865b96153`

## Next

- **`/refresh-context`** (fresh **curator** context) for segment closeout.
