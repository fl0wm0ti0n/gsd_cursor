# OpenCode adapter pack (US-0121)

This is the **empty-but-valid** OpenCode host pack shipped by US-0121, the
first slice of the six-story OpenCode adapter epic (US-0121..US-0126). It is
delivered into consumer repos by the existing its-magic installer when run with
`--host opencode` or `--host both`.

## Layout

```
.opencode/
  agents/         # US-0122 role agents (8 markdown files; see below)
  commands/       # US-0125 thin command bodies (placeholder .gitkeep for US-0121)
  plugins/        # US-0124 orchestrator plugin slot (README only for US-0121)
  .gitignore      # Q10 four pattern groups (DEC-0120 §7)
  README.md       # this file
```

### Role agents (US-0122)

Eight markdown agents ship under `agents/` (filename minus `.md` is the OpenCode
agent name):

- `po.md` — Product Owner
- `tech-lead.md` — Tech Lead
- `dev.md` — Dev
- `qa.md` — QA
- `release.md` — Release
- `curator.md` — Curator
- `security.md` — Security
- `auto.md` — Auto orchestrator (primary; Task-spawns role agents)

Each file carries YAML frontmatter (`description`, `mode`, `permission`) and a
short prompt body. Layer-1 permission matrix is locked in `decisions/DEC-0122.md`
§2 (deny-last ordering on object-form `edit`; `auto` `task` 7-role allow + `*`
deny last). No `model:` vendor slugs (US-0123 owns provider routing).

## Install

```bash
# Cursor-only (default; .opencode/ is NOT installed)
its-magic --target . --mode missing

# OpenCode-only (.cursor/ rows are skipped; kernel paths still install)
its-magic --target . --mode missing --host opencode

# Both host trees
its-magic --target . --mode missing --host both
```

`--host` accepts `cursor | opencode | both` (case-insensitive, whitespace-trimmed).
Default is `cursor` when omitted. Unknown or duplicate `--host` argv fails
closed with `INSTALL_HOST_INVALID` (no last-wins).

## Kernel vs host

`--host` gates **only** `.cursor/` and `.opencode/` trees. Kernel paths
(`docs/`, `scripts/`, `its_magic/`, `handoffs/`, `decisions/`, `sprints/`,
`.github/workflows/`) always install regardless of `--host`.

## Gitignore posture (Q10 LOCKED — four pattern groups)

- `.opencode/opencode.json{,c}` — project-local config overrides; template
  ships no `opencode.json` (a consumer repo may add one with provider
  credentials; do not commit it).
- `.env` / `.env.*` — provider keys per OpenCode docs.
- `*.local.json{,c}` — mirrors kit `.cursor/` volatile-ID convention (US-0102).
- `auth.json` — defense-in-depth; lives outside the repo per OpenCode docs.

No further speculative globs. No repo-root `opencode.json` (R-0109 Q6 — would
prematurely lock US-0122 permission matrix + US-0123 provider config).

## Host-shrink diagnostics

- `clean --host cursor` after `--host both` does **not** delete `.opencode/`;
  emits `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`.
- `upgrade --host cursor` after `--host both` does **not** refresh `.opencode/`;
  emits `OPENCODE_STALE_BY_UPGRADE_CURSOR`.
- Symmetric: `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`.

## Non-goals (this slice)

US-0122 (role agents), US-0123 (per-role provider/slug routing), US-0124
(plugin body), US-0125 (thin command bodies), US-0126 (full operator runbook)
are not filled here. No active kit `.opencode/` mirror (Q9 YAGNI). No
VS Code contrib rewrite, no OpenCode fork, no standalone runtime.

## Pointers

- Architecture: `docs/engineering/architecture.md` `# US-0121`
- Decision: `decisions/DEC-0120.md`
- Runbook hook: `docs/engineering/runbook.md` `## OpenCode host mode (US-0121)`
- Tests: `tests/us0121_host_mode_test.py` (14 markers)
- Parity: `scripts/check_intake_template_parity.py --scope=opencode-adapter`
