# Q0002 — README OpenCode visibility

## Result
`acceptance_met: true`

## Problem
Root README framed its-magic as Cursor-only in the hero. OpenCode existed only as a late `### OpenCode host operator runbook (US-0126)` blurb — easy to miss.

## Changes
- `README.md` + `template/README.md` (byte-identical):
  - Hero: **Cursor or OpenCode**
  - New **Hosts** paragraph (`--host opencode|both`, default cursor-only, `/connect`, runbook pointer)
  - Features: distribution `--host` bullet; `/auto` host-neutral wording
  - Quick start: OpenCode install examples; step 3 renamed to Cursor or OpenCode
  - US-0126 subsection strengthened with cross-link to intro Hosts blurb
- `its_magic/README.md` + `template/its_magic/README.md`: matching early-visibility edits (framework catalog)

## Verify
- OpenCode named in first viewport / Features / Quick start without scrolling to US-0126 alone
- No new DEC literals in added operator sentences
