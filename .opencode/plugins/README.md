# OpenCode plugins (US-0124 — reserved)

This directory reserves the slot for the OpenCode orchestrator plugin body
(US-0124). It is intentionally empty for US-0121 (the first slice of the
OpenCode adapter epic).

US-0121 ships the host-surface contract only:

- `template/.opencode/agents/.gitkeep` — placeholder for US-0122 role agents.
- `template/.opencode/commands/.gitkeep` — placeholder for US-0125 thin command
  bodies.
- `template/.opencode/plugins/README.md` — this file (US-0124 plugin slot).
- `template/.opencode/.gitignore` — Q10 four pattern groups (DEC-0120 §7).
- `template/.opencode/README.md` — pack overview.

Do not add a plugin body, vendor slugs, `model:` literals, or API keys here
(US-0102 volatile-ID rule). US-0124 will populate this directory.
