# Release notes — S0032 (US-0053)

## Summary

- **Sprint:** S0032
- **Story:** US-0053 — Context Compaction and Tiered Token-Cost Optimization Mode
- **Release date:** 2026-03-13
- **Status:** Released

## Scope

Token-cost optimization for artifact-first workflow memory surfaces using a
tiered profile control (`lean|balanced|full`) and deterministic context
compaction policies for `state.md`, `decisions.md`, and `/ask` retrieval while
preserving mandatory quality and release gates.

## Delivered

- **AC-1:** Added documented `TOKEN_PROFILE=lean|balanced|full` control with deterministic semantics.
- **AC-2:** Lean-mode guidance reduces non-critical overhead defaults while preserving mandatory gates.
- **AC-3:** Balanced/full behavior and manual-override precedence documented and deterministic.
- **AC-4:** Added state hot-surface + archive policy with non-destructive archive strategy.
- **AC-5:** Compacted decisions index with bounded summaries and canonical DEC record pointer.
- **AC-6:** Updated `/ask` to narrow-read question-scoped retrieval (targeted first, bounded expansion).
- **AC-7:** Preserved active/template parity across command/agent/runbook/README/scratchpad/state surfaces.
- **AC-8:** Added regression assertions for profile/guardrail/compaction invariants in both test runners.
- **AC-9:** Added operator guidance for profile tradeoffs and escalation patterns.
- **AC-10:** Preserved existing ID semantics and release/history integrity (no destructive rewrites).

## Gate evidence

| Gate | Result | Evidence |
|------|--------|----------|
| Check-in tests | PASS | `tests/report.md` 2026-03-13T09:46:51Z, Pass: 459, Fail: 0 |
| QA completion | PASS | `sprints/S0032/qa-findings.md`, no blockers |
| UAT completeness | PASS | `sprints/S0032/uat.json` and `sprints/S0032/uat.md` (10/10) |
| Isolation compliance | PASS | `docs/engineering/state.md` execute + qa + verify-work evidence for S0032 |
| Backlog reconciliation | PASS | `US-0053` set to DONE; AC checkboxes reconciled |

## Artifacts

- `.cursor/commands/ask.md`, `template/.cursor/commands/ask.md`
- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `docs/engineering/state.md`, `template/docs/engineering/state.md`
- `docs/engineering/state-archive/README.md`, `template/docs/engineering/state-archive/README.md`
- `docs/engineering/decisions.md`, `template/docs/engineering/decisions.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0032/qa-findings.md`, `sprints/S0032/uat.json`, `sprints/S0032/uat.md`, `sprints/S0032/release-findings.md`
