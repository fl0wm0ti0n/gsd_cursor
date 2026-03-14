# Release Notes — S0036

- Sprint: `S0036`
- Story: `US-0057`
- Date: 2026-03-14
- Status: released

## Scope

Delivered upgrade-safe scratchpad local example refresh and installer parity.

## What shipped

1. `.cursor/scratchpad.local.example.md` refreshed and expanded (active/template).
2. Upgrade diagnostics now report scratchpad example status in all installers.
3. User local scratchpad preservation signal added to installer output.
4. Installer + CLI regression checks now validate example refresh and local
   preservation behavior.
5. Documentation updated for upgrade contract and troubleshooting
   (`README.md`, `docs/engineering/runbook.md`, template parity).

## Gate evidence

- Check-in tests: PASS (`tests/report.md`)
- QA: PASS (`sprints/S0036/qa-findings.md`)
- UAT: PASS (`sprints/S0036/uat.json`, `sprints/S0036/uat.md`)
- Release findings: PASS (`sprints/S0036/release-findings.md`)

## Artifacts updated

- `.cursor/scratchpad.local.example.md` (+ template parity copy)
- `installer.ps1`, `installer.sh`, `installer.py`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `README.md`, `docs/engineering/runbook.md` (+ template parity copies)
- `docs/engineering/architecture.md`, `docs/engineering/decisions.md`
- `decisions/DEC-0039.md`
