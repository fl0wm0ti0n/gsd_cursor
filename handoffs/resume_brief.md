# Resume Brief

## Current status

- Post S0028 release: `US-0049` (`S0028`) is finalized (PASS, released).
- Release gates passed; backlog/acceptance reconciled for US-0049.
- **OPEN stories: none** — backlog currently all DONE; next work via **intake**.

## Next actions

1. Next run: start from **intake** for new work (no OPEN story in backlog).
2. After intake selects/creates a story, run **discovery** → research → architecture → sprint-plan per workflow.

## Intended resume phase

`intake`

## Isolation provenance (US-0048 / DEC-0029)

- isolation_provenance_ref=docs/engineering/state.md (refresh-context checkpoint post S0028)
- resume_requires_fresh_context=1

## Auto continuation breadcrumb contract (US-0037)

When `/auto` continuation stops before completion, include:
- `requested_start_from`
- `resolved_start_phase`
- `resolution_source` (`argument|resume_brief|state_fallback`)
- `resolution_status` (`resolved|fail-fast`)
- `stop_reason`
- `stop_phase`
- `timestamp`

Fail-fast resolver errors must use:
`[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`
