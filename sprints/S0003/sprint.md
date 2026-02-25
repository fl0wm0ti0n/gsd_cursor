# Sprint S0003

## Goal

Enforce true fresh-context boundaries per workflow phase and align `/auto` to
spawn fresh subagents for every phase and execute/qa loop cycle.

## Scope

- **In scope**: US-0023 (fresh subagent context + `/auto` orchestration model)
- **Out of scope**: Runtime orchestration engine changes outside workflow
  artifacts and command/rule documentation

## Risks

- Behavior can still drift if future phase commands are added without execution
  model sections.
- Teams may continue manual role switching in one chat unless they follow the
  workflow contract.

## Definition of Done

- Core rules explicitly require fresh contexts at handoff boundaries.
- All phase commands define fresh-context execution behavior.
- Agent role files require fresh startup and stop-after-handoff behavior.
- `/auto` is documented as orchestration-only with fresh subagent spawns.
- Active and template workflow files are aligned.
