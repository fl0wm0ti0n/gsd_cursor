# Release notes — S0030 (US-0051)

## Summary

- **Sprint:** S0030
- **Story:** US-0051 — Intelligent Intake Decomposition and Risk-Aware PO Questioning
- **Release date:** 2026-03-12
- **Status:** Released

## Scope

Deterministic intake decomposition and risk-aware PO questioning behavior for
`/intake`: bounded multi-story proposal semantics for broad/high-risk intake,
explicit user split control, bounded adaptive follow-up rules, low-touch
compatibility preservation, and active/template parity with regression coverage.

## Delivered

- **AC-1:** `/intake` can propose bounded multi-story decomposition when breadth/risk heuristics exceed threshold.
- **AC-2:** Decomposition guidance enforces independently valuable vertical-slice/workflow-step stories.
- **AC-3:** Split rationale persistence contract added (why split, axis, boundaries).
- **AC-4:** User authority preserved with explicit accept/merge/adjust flow before persistence.
- **AC-5:** Small/narrow intake remains single-story by default (no forced over-splitting).
- **AC-6:** Guided questioning adapts to scope/risk/unknowns beyond ambiguity-only triggers.
- **AC-7:** Adaptive questioning remains concise and bounded with deterministic stopping criteria.
- **AC-8:** `INTAKE_GUIDED_MODE=0` low-touch behavior remains available; duplicate safety remains mandatory.
- **AC-9:** Intake artifact traceability contract includes decomposition/questioning evidence.
- **AC-10:** Active/template intake+PO guidance and regression checks remain aligned.

## Gate evidence

| Gate | Result | Evidence |
|------|--------|----------|
| Check-in tests | PASS | `tests/report.md` 2026-03-12T17:58:01Z, Pass: 422, Fail: 0 |
| QA completion | PASS | `sprints/S0030/qa-findings.md`, no blockers |
| UAT completeness | PASS | `sprints/S0030/uat.json` and `sprints/S0030/uat.md` (10/10) |
| Isolation compliance | PASS | `docs/engineering/state.md` execute + qa + verify-work evidence for S0030 |
| Backlog reconciliation | PASS | `US-0051` set to DONE; AC checkboxes reconciled |

## Artifacts

- `.cursor/commands/intake.md`, `template/.cursor/commands/intake.md`
- `.cursor/agents/po.mdc`, `template/.cursor/agents/po.mdc`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0030/qa-findings.md`, `sprints/S0030/uat.json`, `sprints/S0030/uat.md`, `sprints/S0030/release-findings.md`
