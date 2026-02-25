---
description: "its-magic research: gather references and risks before architecture."
---

# /research

## Subagents
- tech-lead
- po

## Execution model
- Run `/research` in a fresh subagent context (tech-lead by default; include PO
  support only if needed for requirements clarification).
- After writing outputs, stop and hand off to `/architecture` in a new
  subagent/chat.

## Inputs
- `docs/product/vision.md`
- `docs/product/backlog.md`
- `docs/product/acceptance.md`

## Outputs (artifacts)
- `docs/engineering/research.md`
- `docs/engineering/decisions.md`
- `docs/engineering/state.md`

## Stop conditions
- Decision gate triggered
- Missing acceptance criteria

## Steps
1. Identify research topics from product vision, backlog, and acceptance criteria.
2. Search the web for relevant patterns, libraries, APIs, and risks.
3. Persist each finding as an R-xxxx entry in `docs/engineering/research.md`.
   Auto-increment the ID from the highest existing entry. Follow the entry schema
   defined in the research.md header (per DEC-0011).
4. Record any decisions triggered by research and update state.
