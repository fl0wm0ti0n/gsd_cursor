# Release notes — S0025 (US-0048)

## Summary

- **Sprint:** S0025  
- **Story:** US-0048 — Enforced Per-Phase Subagent Isolation with Audit Gate  
- **Release date:** 2026-03-02  
- **Status:** Released  

## Scope

Hard-enforce per-phase fresh subagent isolation with auditable evidence schema,
deterministic reason codes, and fail-closed compliance gates (verify-work + release),
with active/template parity and regression coverage.

## Delivered

- **AC-1:** `/auto` orchestrator-only behavior with fail-closed isolation enforcement.
- **AC-2:** Isolation evidence schema + canonical store guidance (state as canonical store).
- **AC-3:** Execute↔QA loop requires fresh context marker per cycle with evidence fields.
- **AC-4:** Missing/invalid/stale evidence fail-safe behavior with deterministic reason codes.
- **AC-5:** Isolation compliance gates in `/verify-work` and `/release` (after UAT, before finalization).
- **AC-6:** Runbook documents evidence schema + canonical locations; contracts reflected in commands.
- **AC-7:** Reason-code taxonomy + remediation guidance documented.
- **AC-8:** Regression assertions cover positive/negative isolation cases (active + template).
- **AC-9:** Pause/resume isolation provenance fields and resume validation.
- **AC-10:** Active/template parity maintained across commands/runbook/README/agents and tests.

## Gate evidence

| Gate        | Result | Evidence |
|------------|--------|----------|
| Check-in tests | PASS | tests/report.md 2026-03-02T18:38:10Z, Pass: 371, Fail: 0 |
| QA completion  | PASS | sprints/S0025/qa-findings.md, no blockers |
| UAT completeness | PASS | sprints/S0025/uat.json + sprints/S0025/uat.md (10/10) |
| Isolation compliance | PASS | docs/engineering/runbook.md (US-0048/DEC-0029), docs/engineering/state.md (US-0048 trace) |
| Backlog reconciliation | — | US-0048 → DONE, ACs checked |

## Artifacts

- `sprints/S0025/qa-findings.md`
- `sprints/S0025/uat.json`, `sprints/S0025/uat.md`
- `sprints/S0025/release-findings.md`
- `handoffs/release_queue.md`, `handoffs/release_notes.md`
- `docs/product/backlog.md`, `docs/product/acceptance.md`

## Notes

- Deploy commands: none executed for this repo (runbook deploy keys are intentionally blank).
