# Developer documentation

This shard holds contributor-facing material for the **its-magic** framework. End-user
setup stays in the root `README.md` (user channel).

## Prerequisites

- **Cursor** (or compatible editor) with the workflow files installed.
- **Python 3** on PATH for scratchpad merge validation and several repo scripts.
- **Node.js** if you use npm-packaged `its-magic` or npm-driven `TEST_COMMAND` defaults.

## Workflow

- Follow phased commands under `.cursor/commands/` (`intake`, `discovery`, `architecture`,
  `sprint-plan`, `execute`, `qa`, `release`, etc.).
- Keep handoffs and `docs/engineering/state.md` updated at phase boundaries.
- Use `.cursor/scratchpad.local.md` for personal overrides; never commit secrets.
- **US-0124** — OpenCode orchestrator plugin spawn-only `/auto`; traceability:
  runbook `## OpenCode orchestrator plugin reason codes (US-0124)`, architecture `# US-0124`, `decisions/DEC-0124.md`.

## Quality gates

- Run `TEST_COMMAND` from `docs/engineering/runbook.md` before push; CI should mirror the same.
- Run `python scripts/validate_doc_profile.py` when changing documentation profile flags or
  README surfaces.
- Observe `US-0071` hygiene for user-visible script output (see runbook).
- **US-0121** — OpenCode template pack + installer `--host` flag; traceability:
  runbook `## OpenCode host mode (US-0121)`, architecture `# US-0121`.
- **US-0123** — OpenCode per-role/per-phase model slug routing (multi-provider, no vendor IDs in template); traceability:
  runbook `## OpenCode model slug routing (US-0123)`, architecture `# US-0123`, `decisions/DEC-0123.md`.
- **US-0124** — OpenCode orchestrator plugin spawn-only `/auto` (Task-spawns US-0069 roles, never executes phase work in-session); traceability:
  runbook `## OpenCode orchestrator plugin reason codes (US-0124)`, architecture `# US-0124`, `decisions/DEC-0124.md`.
- **BUG-0015** — OpenCode `/auto` dispatch attach (plugin owns interactive spawn); traceability:
  runbook `### OpenCode `/auto` dispatch attach reason codes (BUG-0015)`, architecture `# BUG-0015`.
- **US-0126** — OpenCode host operator runbook, cross-host reason-code catalog, and `--scope=opencode-adapter` parity; traceability:
  runbook `## OpenCode host operator runbook (US-0126)`, architecture `# US-0126`.
- **US-0130** — Operator-pinned sovereign-critic model (`MODEL_SOVEREIGN-CRITIC` + catalog `roles.critic`); traceability:
  runbook **Degraded fallback troubleshooting**, architecture `# US-0130`, `decisions/DEC-0130.md`.

## Architecture notes

- **US-0122** — OpenCode role agents and Layer-1 permission table; traceability:
  architecture `# US-0122`, `decisions/DEC-0122.md`.
- **US-0125** — Thin OpenCode commands and Python validator bridge (dispatch-only `.opencode/commands/`; Python validators remain fail-closed SOT); traceability:
  architecture `# US-0125`, `decisions/DEC-0125.md`.
- High-level contracts live in `docs/engineering/architecture.md` (search for story ids).
- Installer ownership is driven by `docs/engineering/context/installer-owned-paths.manifest`.
- Template parity: changes in repo root often require the same edit under `template/`.

## Contracts and interfaces

- Scratchpad merge precedence: local → materialized `.cursor/scratchpad.md` →
  `.cursor/scratchpad.local.example.md` (Model B / **DEC-0055**).
- Documentation profile keys: `DOC_AUDIENCE_PROFILE`, `DOC_DETAIL_LEVEL` (**DEC-0059**).
- Optional modes: `SPEC_PACK_MODE`, `USER_GUIDE_MODE` remain orthogonal; when `0`, validators
  must not require those artifacts.

## Engineering decisions

- Decision records: `decisions/DEC-xxxx.md` and the compact index in
  `docs/engineering/decisions.md`.
- Profile semantics for this shard: **DEC-0059** and `# US-0077` in `architecture.md`.
