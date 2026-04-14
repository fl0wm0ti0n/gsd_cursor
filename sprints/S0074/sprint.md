# Sprint S0074

## Metadata

- **sprint_id**: S0074
- **story_refs**: US-0086
- **goal**: Deliver automation-only remote execution selection with deterministic target routing, explicit NL intent handling, fail-closed reason codes, evidence tuple capture, security continuity with US-0085, and active/template parity without changing manual default behavior.
- **status**: planned
- **created_at**: 2026-04-13T19:45:00Z
- **orchestrator_run_id**: auto-20260405-01

## Scope

- **US-0086**: Automation-driven remote execution selection (Docker / SSH / NL container intent)
- **Architecture**: `docs/engineering/architecture.md` `# US-0086`
- **Research**: `docs/engineering/research.md` `R-0068`

## Architecture reference

- `docs/engineering/architecture.md` `# US-0086`
- `docs/engineering/research.md` `R-0068`

## Acceptance criteria coverage

| AC | Description | Task |
|----|-------------|------|
| AC-1 | Scratchpad + template define automation-only remote profile, default manual unchanged | T-001 |
| AC-2 | Runbook + template document manual vs automation modes | T-002 |
| AC-3 | Agent/rules + template deterministic mode-on routing and mode-off no-reroute | T-003 |
| AC-4 | NL phrase `start container <target_id>` resolves deterministically with fail-closed unknown/disabled handling | T-004 |
| AC-5 | Execute/QA handoff evidence includes `target_id`, `environment_label`, `automation_profile` (names-only) | T-005 |
| AC-6 | Optional CI path-filter/matrix recipe documented deterministically | T-006 |
| AC-7 | Security contract: never read `.env`, never print secrets, names-only outputs | T-007 |
| AC-8 | Tests/contract script for target resolution + unknown-target failure; mode-off non-regression | T-008 |
| AC-9 | Architecture lock consistency maintained for reason codes, key names, US-0064/DEC-0070 compatibility | T-009 |
| AC-10 | Active + template parity for touched command/rule/scratchpad surfaces | T-010 |

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12
- **Within limit**: yes

## Governance

- **R-0068**: routing precedence, reason-code candidates, evidence tuple
- **US-0064 / DEC-0070**: remote schema compatibility unchanged
- **US-0085 / DEC-0071**: `.env` secrecy and names-only evidence posture

## Template parity plan

| # | Active path class | Template path class | Action |
|---|-------------------|---------------------|--------|
| 1 | `.cursor/scratchpad*` | `template/.cursor/scratchpad*` | Add automation-profile literals and docs |
| 2 | `.cursor/commands/auto.md` | `template/.cursor/commands/auto.md` | Add routing contract and reason codes |
| 3 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | Add deterministic routing + fail-closed behavior |
| 4 | `.cursor/rules/*.mdc` | `template/.cursor/rules/*.mdc` | Add mode-on/mode-off routing guidance |
| 5 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | Manual vs automation operator workflow split |
