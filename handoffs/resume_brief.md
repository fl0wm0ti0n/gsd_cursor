# Resume Brief

## Current status

- Workflow is paused at a safe phase boundary after execute completion for
  `S0008` / `US-0036`.
- Dev implementation is complete and handed off; `sprints/S0008/tasks.md` and
  `sprints/S0008/progress.md` show all tasks done.
- `docs/engineering/state.md` includes a pause checkpoint and confirms QA-ready
  status for remote config contract/doc/validation artifacts.
- Latest relevant handoff is `handoffs/dev_to_qa.md`; scope is complete and
  pending QA verification only.

## Next actions

1. Resume in phase: `qa`.
2. Run `/qa` for Sprint `S0008` (`US-0036`) and execute the checklist from
   `handoffs/dev_to_qa.md`.
3. Verify positive/negative remote-config coverage and active/template parity
   remain green in current workspace state.
4. If QA passes without blockers, continue to `/verify-work`; if not, hand back
   to dev with findings.

## Intended resume phase

`qa`

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
