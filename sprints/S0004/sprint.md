# Sprint S0004

## Goal

Deliver US-0024 by adding a dedicated `/memory-audit` command that produces a
non-blocking memory drift report and clearly separates memory drift
(implementation scope) from template drift (US-0017 reference-only scope).

## Scope

- **In scope**: US-0024 (AC-1..AC-6), including command definition, report
  format, documentation, and verification coverage.
- **Out of scope**: US-0017 implementation (template drift guard/sync
  automation). Only reference/routing to US-0017 is included.
- **Out of scope**: changing `/verify-work` or `/map-codebase` ownership beyond
  documentation cross-references.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned atomic tasks: 6
- Result: within threshold, no split required.

## Risks

- Heuristic checks can over-report drift if evidence rules are vague.
- Command/report wording can blur US-0024 and US-0017 boundaries unless enforced
  in both command and docs.
- Active/template parity can drift if updates are applied only to active files.

## Definition of Done

- `/memory-audit` command exists and is read-only for source/workflow/sprint
  artifacts (AC-1).
- Command writes `docs/engineering/memory-drift-report.md` with required
  metadata, findings, and severity structure (AC-2).
- Detection guidance covers changed code without artifact updates, unresolved
  decision TODOs, and sprint/story status mismatches (AC-3).
- Report and command explicitly split memory drift from template drift and route
  template concerns to US-0017 (AC-4).
- Output is advisory/non-blocking with recommended next actions and command
  suggestions (AC-5).
- README and runbook document execution timing and interpretation guidance
  before handoff/QA/release (AC-6).
