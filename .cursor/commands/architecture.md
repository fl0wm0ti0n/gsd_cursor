---
description: "its-magic architecture: define approach, risks, and decisions."
---

# /architecture

## Subagents
- tech-lead

## Execution model
- Run `/architecture` in a fresh Tech Lead subagent context.
- After writing outputs, stop and hand off to `/sprint-plan` in a new
  subagent/chat.

## Inputs
- Product vision and acceptance
- Constraints and risks
- `docs/engineering/research.md`

## Outputs (artifacts)
- `docs/engineering/architecture.md`
- `docs/engineering/decisions.md`
- `docs/engineering/state.md`
- `handoffs/po_to_tl.md` (read)

## Stop conditions
- Major tradeoff requires a decision
- Unknown feasibility or data migration risk

## Steps
1. Challenge:
   a. If `EARLY_RESEARCH=1` in `.cursor/scratchpad.md`, search for technical references (framework docs, pattern comparisons, benchmarks, security considerations) and persist as an R-xxxx entry in `docs/engineering/research.md` (auto-increment ID, per DEC-0011).
   b. Question design assumptions ("what's the alternative?").
   c. Check for simpler approaches ("can this be simpler?").
   d. Inventory risks for each architectural choice.
2. Define the minimal architecture and key components.
3. Record tradeoffs in decisions log.
4. Update engineering state and readiness.

