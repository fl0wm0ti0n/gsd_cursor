---
name: cursor-its-magic-kit
overview: Plan the build of the Cursor-native “its-magic Team Kit” template repo described in `Plan.md`, covering commands, rules, skills, agents, hooks, docs, and CI/CD templates.
todos:
  - id: scaffold-structure
    content: Scaffold directory structure and starter artifacts
    status: pending
  - id: commands-rules
    content: Add 10 commands and 4 rules with IO/stop gates
    status: pending
  - id: skills-agents
    content: Create its-magic skill, templates, and 6 agents
    status: pending
  - id: hooks-cicd-docs
    content: Implement hooks, CI/CD workflows, and README updates
    status: pending
isProject: false
---

# Cursor its-magic Kit Plan

## Scope Summary

Build a drop-in template repo that implements the full its-magic workflow (intake → discovery → architecture → sprint plan → execute → QA → release → pause/resume) using Cursor-native artifacts: commands, rules, skills, subagents, hooks, docs, and GitHub Actions. Voice input is documented as an input layer only. CI/CD is template-based and driven by runbook keys.

## Key Files and Structures

- Template structure per spec: [.cursor/](.cursor/), [docs/](docs/), [sprints/](sprints/), [handoffs/](handoffs/), [decisions/](decisions/), [.github/workflows/](.github/workflows/)
- Commands: `.cursor/commands/*.md` (10 commands)
- Rules: `.cursor/rules/*.mdc` (4 rules)
- Skills: `.cursor/skills/its-magic/SKILL.md` + `templates/*.md`
- Agents: `.cursor/agents/*.mdc` (PO, tech-lead, dev, QA, release, curator)
- Hooks: `.cursor/hooks.json`, `.cursor/hooks/hook.py`, `.cursor/scratchpad.md`
- Docs templates: `docs/product/*.md`, `docs/engineering/*.md`, `sprints/S0001/*`, `handoffs/*.md`, `decisions/DEC-0001.md`
- CI/CD: `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`
- README updates: voice options + runbook usage

## Implementation Outline

1. **Scaffold repo layout** per section 4 and add starter artifacts in `docs/`, `sprints/`, `handoffs/`, `decisions/`.
2. **Write 10 commands** in `.cursor/commands/` with explicit inputs/outputs, stop-conditions, and role usage.
3. **Define rules** in `.cursor/rules/` for phase flow, quality gates, handoffs/state persistence, and escalation.
4. **Create the skill** in `.cursor/skills/its-magic/` and template files for story/acceptance/architecture/decision/sprint/handoff.
5. **Define 6 subagents** with required IO and artifact persistence requirements.
6. **Implement hooks** (`hooks.json` + dispatcher script) with fail-open logic, context-refresh checks, and safe-command blocking.
7. **Add CI/CD workflows** that read `docs/engineering/runbook.md` keys and conditionally execute commands.
8. **Update README** to document quick start, voice input strategies, and runbook-driven CI/CD.

## Notes / Constraints

- Voice input is documented only; no runtime integration beyond documentation.
- Hooks and CI/CD must be fail-open unless commands are explicitly set.
- Decision gate should create `decisions/DEC-xxxx.md` and stop until user decision.

## Reference (Plan Spec)

Primary source: [Plan.md](Plan.md)