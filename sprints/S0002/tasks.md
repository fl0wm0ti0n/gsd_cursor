# Tasks — Sprint S0002

## T-001: Create /ask command definition
- Story: US-0020
- Status: done
- Files: `.cursor/commands/ask.md`, `template/.cursor/commands/ask.md`
- Description: Create the /ask slash command with read-only behavior, context pack inputs, behavior rules (no file writes, no state changes), and no subagent role. Create both active and template copies.
- AC covered: US-0020 AC-1, AC-2, AC-3, AC-4

## T-002: Document /ask in README
- Story: US-0020
- Status: done
- Files: `README.md`, `template/README.md`
- Description: Add /ask to the core commands list in README. Document it as the lightweight interaction channel for questions, status checks, and "how does X work" queries. Update both active and template copies.
- AC covered: US-0020 AC-5

## T-003: Update PO agent with evaluation rules
- Story: US-0021
- Status: done
- Files: `.cursor/agents/po.mdc`, `template/.cursor/agents/po.mdc`
- Description: Add evaluation rules to the PO agent definition: check backlog for duplicates, evaluate feasibility, suggest alternatives, suggest /quick for small tasks, challenge constructively. Update both active and template copies.
- AC covered: US-0021 AC-1, AC-2, AC-3, AC-6

## T-004: Update Tech Lead agent with challenge and sizing rules
- Story: US-0021, US-0022
- Status: done
- Files: `.cursor/agents/tech-lead.mdc`, `template/.cursor/agents/tech-lead.mdc`
- Description: Add challenge rules to the Tech Lead agent definition: question assumptions, prefer simplicity, list risks explicitly. Also add sprint sizing rules: respect SPRINT_MAX_TASKS from scratchpad, propose splitting when threshold exceeded, recommend /quick for small tasks. Update both active and template copies.
- AC covered: US-0021 AC-6, US-0022 AC-1

## T-005: Update /intake command with evaluation step
- Story: US-0021
- Status: done
- Files: `.cursor/commands/intake.md`, `template/.cursor/commands/intake.md`
- Description: Add step 1 "Evaluate" before the existing steps in the /intake command. The step covers duplicate check, feasibility, alternatives, and scope check. Renumber existing steps. Update both active and template copies.
- AC covered: US-0021 AC-4, AC-7

## T-006: Update /architecture command with challenge step
- Story: US-0021
- Status: done
- Files: `.cursor/commands/architecture.md`, `template/.cursor/commands/architecture.md`
- Description: Add step 1 "Challenge" before the existing steps in the /architecture command. The step covers questioning assumptions, simplicity check, and risk inventory. Renumber existing steps. Update both active and template copies.
- AC covered: US-0021 AC-5

## T-007: Add sprint sizing rules to /sprint-plan command
- Story: US-0022
- Status: done
- Files: `.cursor/commands/sprint-plan.md`, `template/.cursor/commands/sprint-plan.md`
- Description: Add a scope evaluation step to /sprint-plan that reads SPRINT_MAX_TASKS from scratchpad, evaluates whether work exceeds the threshold, and proposes splitting into multiple sprints or milestones when needed. Also add guidance for routing small ideas to /quick and new ideas during active sprints to the next sprint. Update both active and template copies.
- AC covered: US-0022 AC-2, AC-4, AC-5

## T-008: Add sprint planning options to scratchpad
- Story: US-0022
- Status: done
- Files: `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`, `template/.cursor/scratchpad.local.example.md`
- Description: Add SPRINT_MAX_TASKS (default: 12) and SPRINT_AUTO_SPLIT (default: 1) to the scratchpad under a new "Sprint planning" section. Update both active and template copies, plus the local example file.
- AC covered: US-0022 AC-3, AC-6, AC-7
