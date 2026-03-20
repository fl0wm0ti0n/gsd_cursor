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
4. Enforce state hot-surface rollover when configured thresholds are exceeded:
   - evaluate `STATE_HOT_MAX_LINES` and `STATE_HOT_MAX_CHECKPOINTS` from
     `.cursor/scratchpad.md`,
   - archive oldest low-frequency checkpoints into deterministic pack files under
     `docs/engineering/state-archive/`,
   - preserve only bounded recent checkpoints in `docs/engineering/state.md`,
   - write deterministic verification evidence (archive boundary, moved entries,
     retained hot-surface markers); fail closed on verification mismatch.

## Deterministic artifact ordering contract (US-0058 / DEC-0040)

- Writes must follow `docs/engineering/artifact-ordering-policy.md`.
- `docs/engineering/state.md` refresh checkpoints are append-bottom only.
- `docs/engineering/decisions.md` compact index remains newest-first in bounded
  section while preserving canonical header structure.
- `sprints/S0001/summary.md` context-pack pointer is prepend-top within its
  context section; historical details remain intact.
- Missing/ambiguous anchors fail with `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`
  (no partial write).
- Archive write or rollover boundary ambiguity fails with
  `STATE_ARCHIVE_WRITE_FAILED` or `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`
  (no partial write).
- Archive verification mismatch fails with `STATE_ARCHIVE_VERIFICATION_FAILED`
  (no partial write).

## Cross-phase ownership guard (US-0061 / DEC-0043)

- Refresh-context mutations must comply with
  `docs/engineering/artifact-ownership-policy.md`.
- Only curator-owned compaction scopes may be mutated; non-owned section
  rewrites fail closed with `PHASE_OWNERSHIP_VIOLATION`.

