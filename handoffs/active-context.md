# Active context index (US-0096 / DEC-0082)

> **Hot memory tier** at **`handoffs/active-context.md`** — lean spawn read/write surface.
> **`active-context.md` is NOT a triad member** (**DEC-0054**);
> **`enforce-triad-hot-surface.py`** does **not** scan this file.

## Index row schema

| Field | Description |
|-------|-------------|
| `story_id` | Active story (e.g. `US-0096`) |
| `delivery_mode` | `standard` \| `ultra_lean` \| `mega_quick` |
| `read_before_code[]` | Paths / anchors agents must read before code edits |
| `last_delta_utc` | ISO UTC of last material update |
| `open_risks[]` | Max **3** short risk bullets |

## Line budget

- Target **30–80** lines; hard cap **`LEAN_STATE_INDEX_ROWS`** (default **80**).
- Oversize with **`LEAN_MEMORY_WRITE=1`** → **`ACTIVE_CONTEXT_OVERSIZE`** (fail closed).

## Rollover

Archive to **`handoffs/archive/active-context-<story_id>-<utc>.md`** when:

1. Segment **`refresh-context`** completes, or
2. Line count exceeds **`LEAN_STATE_INDEX_ROWS`**.

Rewrite this file with a fresh stub after rollover.

## Current index

```yaml
story_id: (none)
delivery_mode: standard
read_before_code: []
last_delta_utc: (unset)
open_risks: []
```
