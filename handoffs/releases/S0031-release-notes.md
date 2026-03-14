# Release notes — S0031 (US-0052)

## Summary

- **Sprint:** S0031
- **Story:** US-0052 — Optional Fresh-Project ID Namespace Bootstrap
- **Release date:** 2026-03-12
- **Status:** Released

## Scope

Optional fresh-project ID namespace bootstrap behavior for `its-magic` artifacts:
deterministic bootstrap eligibility checks, explicit default-off bootstrap
control, first-ID initialization for fresh repos, highest-existing continuation
for non-fresh repos, and parity-safe operator/test contracts across active and
template surfaces.

## Delivered

- **AC-1:** Added optional bootstrap control `ID_NAMESPACE_BOOTSTRAP` (default off).
- **AC-2:** Defined first-ID bootstrap behavior for eligible fresh repos:
  `US-0001`, `DEC-0001`, `R-0001`.
- **AC-3:** Preserved non-fresh highest-existing-ID continuation; no historical renumbering.
- **AC-4:** Added deterministic freshness criteria and auditable ineligible diagnostic (`ID_BOOTSTRAP_NOT_FRESH`).
- **AC-5:** Preserved collision-safe sequential generation semantics across ID namespaces.
- **AC-6:** Added operator documentation in runbook/README for behavior, constraints, and caveats.
- **AC-7:** Added regression coverage for fresh bootstrap path, non-fresh continuation path, and mixed-edge assertions.
- **AC-8:** Maintained active/template parity for commands, agents, docs, scratchpad, and tests.

## Gate evidence

| Gate | Result | Evidence |
|------|--------|----------|
| Check-in tests | PASS | `tests/report.md` 2026-03-12T20:06:45Z, Pass: 440, Fail: 0 |
| QA completion | PASS | `sprints/S0031/qa-findings.md`, no blockers |
| UAT completeness | PASS | `sprints/S0031/uat.json` and `sprints/S0031/uat.md` (8/8) |
| Isolation compliance | PASS | `docs/engineering/state.md` execute + qa + verify-work evidence for S0031 |
| Backlog reconciliation | PASS | `US-0052` set to DONE; AC checkboxes reconciled |

## Artifacts

- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
- `.cursor/commands/intake.md`, `template/.cursor/commands/intake.md`
- `.cursor/commands/research.md`, `template/.cursor/commands/research.md`
- `.cursor/commands/architecture.md`, `template/.cursor/commands/architecture.md`
- `.cursor/agents/po.mdc`, `template/.cursor/agents/po.mdc`
- `.cursor/agents/tech-lead.mdc`, `template/.cursor/agents/tech-lead.mdc`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0031/qa-findings.md`, `sprints/S0031/uat.json`, `sprints/S0031/uat.md`, `sprints/S0031/release-findings.md`
