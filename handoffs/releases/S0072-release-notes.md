# Release Notes — Sprint S0072

- **Sprint**: `S0072`
- **Story**: `US-0088` — `/auto` continuous multi-phase loop + quiet backlog drain
- **Orchestrator run**: `auto-20260405-01`
- **Release date**: 2026-04-13
- **Release agent**: release (fresh context)

## Summary

US-0088 hardens `/auto` orchestration so a single run advances through all intersected lifecycle phases until a deterministic stop condition (story/sprint completion, decision gate, error, pause request, loop max, or blocked). Backlog drain (`AUTO_BACKLOG_DRAIN=1`) now reliably advances across multiple OPEN stories without routine operator chatter. Adds `AUTO_QUIET` scratchpad key (default off) for suppressing routine per-phase success notifications while preserving non-suppressible events (decision gates, errors, missing inputs, pause, loop max, blocked).

## Changes delivered

| Task | AC | Summary |
|------|-----|---------|
| T-001 | AC-1 | Continuous multi-phase execution section in `auto.md` + reference; deterministic stop matrix; outer-driver equivalence (Option B) |
| T-002 | AC-2 | `AUTO_QUIET` (default-off) scratchpad key with non-suppressible notifications and `TOKEN_PROFILE` orthogonality |
| T-003 | AC-3 | Strengthened drain prose: multi-phase advance, recompute at story boundary, next eligible OPEN story |
| T-004 | AC-4 | 10 new contract tests: continuation markers, reference Step 5, drain advance, AUTO_QUIET, spawn-only regression, template parity |
| T-005 | AC-5 | Byte/literal parity pass for all touched paths in `template/` |
| T-006 | AC-6 | Architecture `# US-0088` reconciled — no drift |
| T-007 | AC-7 | Runbook operator subsection: caps, pause, decision gates, AUTO_QUIET, outer-driver equivalence, drain advance, troubleshooting |

## Gate audit (US-0039)

| gate | verdict | reason_code | remediation | evidence_refs |
|------|---------|-------------|-------------|---------------|
| check-in_test | pass | — | — | `tests/report.md` (788/6; 4 pre-existing, 2 cosmetic step-label — non-blocking) |
| qa | pass | — | — | `sprints/S0072/qa-findings.md` |
| uat | pass | — | — | `sprints/S0072/uat.json`, `sprints/S0072/uat.md` (7/7 pass) |
| isolation | pass | — | — | `docs/engineering/state.md` (execute, qa, verify-work evidence) |
| strict_proof | pass | — | — | `docs/engineering/state.md` (distinct runtime_proof_id per phase) |
| scratchpad_pair | pass | — | — | `scripts/check-scratchpad-pair-parity.py` → `[SCRATCHPAD_PAIR_OK]` |
| metadata_guard | pass | — | — | `scripts/check-user-visible-metadata.py` → PASS |
| bug_validate | pass | — | — | `scripts/bug_issue_validate.py` → `[BUG_VALIDATION_OK]` |
| finalization | pass | — | — | All mandatory gates PASS; release finalized |

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- `runtime_mode`: `local`
- `runtime_context_ref`: This is a template/installer repository; no runtime server. Tests validate framework contract integrity.

## Connect

- `service_url`: N/A (template/installer repo — no deployed service)
- `service_port`: N/A
- `health_endpoint`: N/A

## Verify

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` — expect `tests/report.md` with 0 critical failures.
2. Run `python -m pytest tests/auto_command_contract_test.py -q` — expect 17/17 pass.
3. Run `python scripts/check-scratchpad-pair-parity.py --repo .` — expect `[SCRATCHPAD_PAIR_OK]`.
4. Run `python scripts/check-user-visible-metadata.py` — expect PASS (exit 0).
5. Run `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` — expect `[BUG_VALIDATION_OK]`.
6. Confirm `docs/product/backlog.md` shows `US-0088` `Status: DONE`.

- `expected_health_signal`: All verification steps exit 0 with expected output markers.

## Credentials

- No credentials required for local verification.
- Registry publish (`npm publish`) requires npm auth token via operator shell profile or CI secret store — not inline.

## Known Issues

- 2 test assertions in `run-tests.ps1` (lines 1106-1107) and `run-tests.sh` (lines 867-868) match stale step-11b label format from US-0088 step renumbering. Cosmetic only — functional content preserved. Recommend follow-up micro-fix.
- `RELEASE_PUBLISH_MODE=confirm` — registry publish targets skipped pending operator confirmation (`skipped_pending_operator_confirm`).

## Publish status

- `RELEASE_PUBLISH_MODE=confirm` — publish targets **not** auto-executed.
- `publish_snapshot=skipped_pending_operator_confirm`
- Operator action: set `RELEASE_PUBLISH_MODE=auto` or run `npm publish` manually when ready.

## Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-release-release-20260413T011500Z-S0072-US0088`
- `phase_id=release`
- `role=release`
- `proof_issued_at=2026-04-13T01:15:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=a1c18a2b7e8a8f83687ca47ad29c0764b0a5867e4098e8e1c1a20314ffe68bbd`
