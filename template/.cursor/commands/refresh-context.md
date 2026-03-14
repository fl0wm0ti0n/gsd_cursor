---
description: "its-magic refresh context: compact state and decisions."
---

# /refresh-context

## Subagents
- curator

## Execution model
- Run `/refresh-context` in a fresh Curator subagent context.
- After writing outputs, stop. Next phase starts in a new subagent/chat.

## Inputs
- Current sprint artifacts
- Decisions and handoffs

## Outputs (artifacts)
- `docs/engineering/state.md`
- `docs/engineering/decisions.md`
- `sprints/S0001/summary.md`

## Stop conditions
- Missing critical artifacts

## Steps
1. Compact state and decisions into a short context pack.
2. Update sprint summary with current status.
3. Ensure handoffs and state are consistent.

## Deterministic artifact ordering contract (US-0058 / DEC-0040)

- Writes must follow `docs/engineering/artifact-ordering-policy.md`.
- `docs/engineering/state.md` refresh checkpoints are append-bottom only.
- `docs/engineering/decisions.md` compact index remains newest-first in bounded
  section while preserving canonical header structure.
- `sprints/S0001/summary.md` context-pack pointer is prepend-top within its
  context section; historical details remain intact.
- Missing/ambiguous anchors fail with `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`
  (no partial write).

