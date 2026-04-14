# Sprint S0073

## Metadata

- **sprint_id**: S0073
- **story_refs**: US-0085
- **goal**: Deliver gitignored `.env` for remote and release connectivity with 4-layer defense-in-depth exclusion, committed `.env.example`, agent/IDE exclusion, operator documentation, optional parity helper, regression tests, and template parity.
- **status**: planned
- **created_at**: 2026-04-13T12:45:00Z
- **orchestrator_run_id**: auto-20260405-01

## Scope

- **US-0085**: Gitignored `.env` for remote and release connectivity (no AI read)
- **DEC-0071**: 4-layer defense-in-depth `.env` exclusion contract
- **R-0072**: `*Env` inventory, `.cursorignore` semantics, AC-8/AC-9 recommendations

## Architecture reference

- `docs/engineering/architecture.md` `# US-0085`
- `decisions/DEC-0071.md`

## Acceptance criteria coverage

| AC | Description | Task |
|----|-------------|------|
| AC-1 | `.gitignore` (active + template/) lists `.env` / `.env.local` | T-001 |
| AC-2 | `.cursorignore` excludes `.env` from agent/IDE | T-002 |
| AC-3 | `.env.example` committed with names only (20 `*Env`) | T-003 |
| AC-4 | Runbook `.env` copy/source recipe (active + template/) | T-004 |
| AC-5 | Runtime-connectivity `*Env` sourcing note (active + template/) | T-005 |
| AC-6 | us-0084-remote-e2e `.env`/`.env.example` refs (active + template/) | T-006 |
| AC-7 | Agent/rules `.env` exclusion bullet (active + template/) | T-007 |
| AC-8 | `scripts/print_remote_env_hint.py` names-only parity helper | T-008 |
| AC-9 | `tests/test_env_gitignore.py` regression test | T-009 |
| AC-10 | `remote_config_summary.py` + tests remain PASS | T-010 |

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12
- **Within limit**: yes

## Governance

- **DEC-0071**: 4-layer defense-in-depth — `.gitignore` + `.cursorignore` + Cursor rules + operator discipline
- **US-0064** / **DEC-0070**: JSON schema unchanged; `.env` supplies values locally
- **US-0086** (OPEN): must compose with DEC-0071

## Template parity plan (7 touchpoints)

| # | Active path | Template path | Action |
|---|-------------|---------------|--------|
| 1 | `.gitignore` | `template/.gitignore` (**new**) | Create with `.env`/`.env.local` entries |
| 2 | `.cursorignore` (**new**) | `template/.cursorignore` (**new**) | Create with `.env*` patterns |
| 3 | `.env.example` (**new**) | `template/.env.example` (**new**) | Identical content (20 names) |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | Add `.env` copy/source recipe section |
| 5 | `docs/engineering/runtime-connectivity.md` | `template/docs/engineering/runtime-connectivity.md` | Add `*Env` sourcing note |
| 6 | `docs/engineering/us-0084-remote-e2e.md` | `template/docs/engineering/us-0084-remote-e2e.md` | Add `.env`/`.env.example` refs |
| 7 | `.cursor/rules/coding-standards.mdc` | `template/.cursor/rules/coding-standards.mdc` | Add `.env` exclusion bullet |
