# Tasks — Sprint S0003

## T-001: Enforce isolation in core rules
- Story: US-0023
- Status: done
- Files: `.cursor/rules/core.mdc`, `.cursor/rules/handoffs.mdc`, template copies
- Description: Add explicit fresh-context and handoff-only-memory requirements.
- AC covered: AC-1

## T-002: Add execution model to phase commands
- Story: US-0023
- Status: done
- Files: `.cursor/commands/*.md` (phase commands + quick/pause/resume), template copies
- Description: Add `Execution model` section requiring fresh subagent per phase.
- AC covered: AC-2

## T-003: Rework /auto to orchestration-only
- Story: US-0023
- Status: done
- Files: `.cursor/commands/auto.md`, `template/.cursor/commands/auto.md`
- Description: Define `/auto` as phase orchestrator that spawns fresh subagents.
- AC covered: AC-4, AC-5

## T-004: Update role definitions for fresh-start/stop-after-handoff
- Story: US-0023
- Status: done
- Files: `.cursor/agents/*.mdc`, template copies
- Description: Add fresh-context startup rule and explicit stop-after-handoff behavior.
- AC covered: AC-3

## T-005: Document isolation model
- Story: US-0023
- Status: done
- Files: `README.md`, `template/README.md`
- Description: Add agent isolation section and clarify `/auto` semantics.
- AC covered: AC-4

## T-006: Keep active/template parity
- Story: US-0023
- Status: done
- Files: all modified workflow files under active and `template/.cursor/`
- Description: Ensure both active and template behavior match for this story.
- AC covered: AC-6
