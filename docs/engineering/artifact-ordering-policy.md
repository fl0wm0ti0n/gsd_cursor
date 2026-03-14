# Artifact Ordering Policy (US-0058 / DEC-0040)

This policy defines deterministic write order for mutable workflow artifacts.
Commands that mutate these artifacts must use this matrix and fail safe when
anchors are missing or ambiguous.

## Canonical matrix

| Artifact | Policy | Deterministic rule |
|---|---|---|
| `docs/engineering/state.md` | `append-bottom` | Add new checkpoints only at end of file, in chronological order. |
| `docs/product/backlog.md` | `sorted-canonical` | Keep stories sorted by numeric `US-xxxx` ID; mutate only target story block. |
| `docs/product/acceptance.md` | `sorted-canonical` | Keep `US-xxxx` rows ordered by numeric ID aligned to backlog order. |
| `handoffs/release_queue.md` | `append-bottom` | Append only one row per new sprint in release order. |
| `handoffs/release_notes.md` | `prepend-top` | Update latest pointer section first; preserve historical references list. |
| `handoffs/resume_brief.md` | `prepend-top` | Update current status/next-actions sections without rewriting unrelated history. |

## Idempotence contract

- Re-running a command without semantic changes must not reorder rows/blocks.
- No oscillation between top and bottom insertion paths.
- No broad rewrites of unrelated story/sprint entries.

## Fail-safe behavior

If required placement anchors are missing or ambiguous:
- stop with reason code `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`,
- emit remediation guidance with expected anchor and file path,
- perform no partial mutation.
