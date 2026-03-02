# Release notes — S0027 (US-0032)

## Summary

- **Sprint:** S0027  
- **Story:** US-0032 — Optional Feature User Guide Generation  
- **Release date:** 2026-03-02  
- **Status:** Released  

## Scope

Optional user-guide workflow behind `USER_GUIDE_MODE=0|1` with zero-overhead default-off behavior: canonical path and schema, release gate 3d and `USER_GUIDE_INCOMPLETE`, story→guide traceability, US-0031 boundary, and active/template parity.

## Delivered

- **AC-1:** `USER_GUIDE_MODE=0|1` in `.cursor/scratchpad.md` (active + template), default `0`.
- **AC-2:** When `USER_GUIDE_MODE=0`, intake, architecture, sprint-plan, execute, qa, release add no required user-guide steps or blocking checks.
- **AC-3:** Canonical path when enabled: `docs/user-guides/US-xxxx.md` per feature story (runbook, `docs/user-guides/README.md`).
- **AC-4:** Minimum schema (Purpose, Prerequisites, Usage steps, Example, Limitations, Troubleshooting) in runbook and user-guides README.
- **AC-5:** Release gate step 3d; when `USER_GUIDE_MODE=1`, validate target-story user guide; block with `USER_GUIDE_INCOMPLETE` when missing or sections absent.
- **AC-6:** Story ID → user guide traceability in handoffs.mdc and runbook for handoff/release context.
- **AC-7:** Boundaries with US-0031: user guides end-user only; no duplicate spec-pack content (runbook, docs/user-guides/README.md).
- **AC-8:** Active and template parity: commands, runbook, README, docs/user-guides/README.md, handoffs.mdc; regression assertions in run-tests.ps1/run-tests.sh for USER_GUIDE_MODE and USER_GUIDE_INCOMPLETE.

## Gate evidence

| Gate | Result | Evidence |
|------|--------|----------|
| Check-in tests | PASS | tests/report.md 2026-03-02T19:51:49Z, Pass: 383, Fail: 0 |
| QA completion | PASS | sprints/S0027/qa-findings.md, no blockers |
| UAT completeness | PASS | sprints/S0027/uat.json (8/8), uat.md |
| Isolation compliance | PASS | state.md verify-work + qa + release phase evidence |
| Backlog reconciliation | — | US-0032 → DONE, ACs checked |

## Artifacts

- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md` (USER_GUIDE_MODE)
- Commands: intake, architecture, sprint-plan, execute, qa, release (active + template)
- `docs/engineering/runbook.md` — Optional user-guide documentation mode (US-0032)
- `docs/user-guides/README.md` (active + template)
- `.cursor/rules/handoffs.mdc` — user-guide traceability
- `tests/run-tests.ps1`, `tests/run-tests.sh` (US-0032 assertions)
