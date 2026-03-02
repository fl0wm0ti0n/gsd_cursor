# Sprint S0025 Summary — US-0048 Per-Phase Subagent Isolation

## Scope

Enforce fresh subagent context per phase (and per execute↔QA cycle) with
auditable isolation evidence, fail-closed gates, deterministic reason codes, and
pause/resume provenance per `DEC-0029`.

## Delivered

1. **T-001 (AC-1)** — `/auto` orchestrator-only enforcement and fail-closed
   contract (no phase work in orchestrator context) with deterministic reason
   codes in active + template `auto.md`.

2. **T-002 (AC-2, AC-6)** — Canonical isolation evidence schema and locations
   documented in runbook + README (active + template):
   `phase_id`, `role`, `fresh_context_marker`, `timestamp`, `evidence_ref`.

3. **T-003 (AC-2)** — Mandatory isolation evidence writing requirements added to
   phase commands and agents (active + template) for `execute`, `qa`,
   `verify-work`, `release`, `pause`, and `resume`.

4. **T-004 (AC-3)** — Execute↔QA loop semantics tightened: each cycle requires a
   fresh subagent and a new `fresh_context_marker` (marker reuse treated as
   stale evidence).

5. **T-005 (AC-4)** — Fail-safe, no-silent-continuation behavior defined for
   missing/invalid/stale evidence with explicit reason codes and remediation.

6. **T-006 (AC-5)** — `/verify-work` isolation compliance gate added; blocks
   handoff to `/release` on isolation violations.

7. **T-007 (AC-5)** — `/release` gate chain extended to include mandatory
   isolation compliance after UAT and before finalization (gate order preserved).

8. **T-008 (AC-7)** — Reason-code taxonomy and remediation documented in
   runbook/commands (active + template).

9. **T-009 (AC-9)** — Pause/resume provenance: resume brief includes isolation
   provenance fields; `/resume` validates provenance and requires fresh context
   + new evidence on resumed phases.

10. **T-010 (AC-8, AC-10)** — Regression assertions added in both test runners
   to enforce active/template parity and presence of isolation enforcement
   contracts.

## Artifacts touched

- `.cursor/commands/auto.md`, `execute.md`, `qa.md`, `verify-work.md`, `release.md`,
  `pause.md`, `resume.md` (active + template)
- `.cursor/agents/dev.mdc`, `qa.mdc`, `release.mdc`, `curator.mdc` (active + template)
- `docs/engineering/runbook.md`, `README.md` (active + template)
- `handoffs/resume_brief.md`, `template/handoffs/resume_brief.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0025/tasks.md`, `sprints/S0025/progress.md`, `sprints/S0025/summary.md`
