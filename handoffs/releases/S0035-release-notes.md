# Release Notes — S0035

- Sprint: `S0035`
- Story: `US-0056`
- Date: 2026-03-14
- Status: released

## Scope

Delivered strict runtime proof for per-phase subagent isolation with fail-closed
auto gates.

## What shipped

1. Strict runtime attestation contract accepted (`DEC-0038`) and linked to
   `US-0056`.
2. `/auto` contract now requires strict runtime-proof tuples at phase
   boundaries and fails closed on missing/invalid/reused/stale/ambiguous proof.
3. `/verify-work` and `/release` include strict runtime-proof gates.
4. Runbook and README document strict-proof fields, diagnostics, and reason
   codes.
5. Regression checks include US-0056 strict-proof assertions with active/template
   parity coverage.

## Gate evidence

- Check-in tests: PASS (`tests/report.md`)
- QA: PASS (`sprints/S0035/qa-findings.md`)
- UAT: PASS (`sprints/S0035/uat.json`, `sprints/S0035/uat.md`)
- Release findings: PASS (`sprints/S0035/release-findings.md`)

## Artifacts updated

- `.cursor/commands/auto.md` (+ template parity copy)
- `.cursor/commands/verify-work.md` (+ template parity copy)
- `.cursor/commands/release.md` (+ template parity copy)
- `docs/engineering/runbook.md` (+ template parity copy)
- `README.md` (+ template parity copy)
- `tests/run-tests.ps1`, `tests/run-tests.sh`
