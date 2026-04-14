# Release Notes — S0073 / US-0085

- **sprint_id**: S0073
- **story_refs**: US-0085
- **release_date**: 2026-04-13T17:00:00Z
- **orchestrator_run_id**: auto-20260405-01
- **verdict**: **PASS**

## Summary

**US-0085**: Gitignored `.env` for remote and release connectivity (no AI read).

Implemented 4-layer defense-in-depth `.env` exclusion per DEC-0071:
`.gitignore` + `.cursorignore` + Cursor rules + operator runbook. Created
`.env.example` with 20 `*Env` names (3 from `remote.json`, 17 from
`release-targets.json`). Template parity across 7 touchpoints. Parity helper
script and regression tests pass.

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
  1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` — expect 790+ pass, 4 pre-existing fail, 0 new failures.
  2. Run `python scripts/check-scratchpad-pair-parity.py --repo .` — expect `[SCRATCHPAD_PAIR_OK]`.
  3. Run `python scripts/check-user-visible-metadata.py` — expect exit 0.
  4. Run `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` — expect `[BUG_VALIDATION_OK]`.
  5. Run `python scripts/print_remote_env_hint.py` — expect Parity PASS 20/20, exit 0.
  6. Run `python -m pytest tests/test_env_gitignore.py -v` — expect 4/4 pass.
  7. Run `python scripts/enforce-triad-hot-surface.py --check` — expect PASS.
- **expected_health_signal**: All checks pass; `tests/report.md` refreshed with 790+ pass.

## Credentials

- Env-reference-only: `*Env` fields in `.cursor/remote.json` and `docs/engineering/release-targets.json` reference env var **names**; operators populate values in `.env` (gitignored, never committed). See `docs/engineering/runbook.md` § Operator `.env` setup.

## Known Issues

- 4 pre-existing test failures (installer TEST_COMMAND detection in sandbox + US-0088 step-label drift); documented in `sprints/S0072/qa-findings.md`.
- `print_remote_env_hint.py` outputs parity line to stderr (cosmetic in PowerShell).

## Gate audit snapshot (US-0039)

| gate | verdict | reason_code | evidence_refs |
|------|---------|-------------|---------------|
| check-in_test | pass | — | `tests/report.md` (790/4 @ 2026-04-13T20:32:02Z) |
| qa | pass | — | `sprints/S0073/qa-findings.md` |
| uat | pass | — | `sprints/S0073/uat.json`, `sprints/S0073/uat.md` (10/10) |
| isolation | pass | — | `docs/engineering/state.md` (execute/qa/verify-work entries) |
| strict_proof | pass | — | `docs/engineering/state.md` (3 distinct proof IDs) |
| scratchpad_pair | pass | — | `scripts/check-scratchpad-pair-parity.py` |
| metadata_guard | pass | — | `scripts/check-user-visible-metadata.py` |
| bug_validate | pass | — | `scripts/bug_issue_validate.py` |
| finalization | pass | — | this file, `handoffs/release_queue.md` S0073 row |

## Publish status

- **RELEASE_PUBLISH_MODE**: `confirm`
- **publish_snapshot**: `skipped_pending_operator_confirm`
- Operator must explicitly confirm before any publish target execution.

## Sync (DEC-0018)

- **ALLOW_AUTO_PUSH**: `0`
- **push_decision**: `not_eligible`
- **reason_code**: `MANUAL_MODE_NO_AUTO`

## Strict runtime proof

- **orchestrator_run_id**: `auto-20260405-01`
- **runtime_proof_id**: `rp-auto-20260405-01-release-release-20260413T170000Z-S0073-US0085`
- **phase_id**: `release`
- **role**: `release`
- **proof_issued_at**: `2026-04-13T17:00:00Z`
- **proof_ttl_seconds**: `3600`
- **proof_hash**: `201375708766b544b12a336534d09e5a8c69369bf18e10c8ea8ac76717dcfb75`

## Next

- **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain).
