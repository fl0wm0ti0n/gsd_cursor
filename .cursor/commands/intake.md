---
description: "its-magic intake: clarify idea and capture story + acceptance."
---

# /intake

## Subagents
- po

## Execution model
- Run `/intake` in a fresh PO subagent context.
- After writing outputs, stop and hand off to `/discovery` or `/architecture`
  in a new subagent/chat.

## Inputs
- User idea (text or voice transcription)
- Constraints, audience, success criteria

## Outputs (artifacts)
- `docs/product/vision.md`
- `docs/product/backlog.md`
- `docs/product/acceptance.md`
- `handoffs/po_to_tl.md`

## Stop conditions
- Missing acceptance criteria or unclear scope
- Decision gate triggered (see escalation rule)

## Steps
1. Evaluate:
   a. Check `docs/product/backlog.md` for duplicates, assess feasibility, suggest alternatives if a simpler approach exists, check scope (suggest `/quick` for small tasks, propose breakdown for large ones).
   b. If `EARLY_RESEARCH=1` in `.cursor/scratchpad.md`, search the web for relevant context (competitor approaches, library docs, API references, prior art) and persist findings as an R-xxxx entry in `docs/engineering/research.md` (auto-increment ID, per DEC-0011).
   c. Reference research entry IDs in evaluation reasoning.
   d. Present evaluation and recommendation — user decides.
2. Ask targeted questions until the story and acceptance are concrete.
3. Persist the story and acceptance in product docs.
4. Write a PO -> TL handoff with scope and risks.

