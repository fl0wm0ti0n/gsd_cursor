# Architecture archive pack (2026-06-13)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 15
- First archived heading: `# US-0085: Gitignored `.env` for remote and release connectivity (no AI read)`
- Last archived heading: `# US-0085: Gitignored `.env` for remote and release connectivity (no AI read)`
- Verification tuple (mandatory):
  - archived_body_lines=173
  - preamble_lines=10
  - retained_body_lines=2959

---

# US-0085: Gitignored `.env` for remote and release connectivity (no AI read)

## Overview

**US-0085** standardizes a repo-root **`.env`** (gitignored) holding **values** for
the 20 `*Env` environment variables referenced by **`.cursor/remote.json`** and
**`docs/engineering/release-targets.json`** (**US-0064**), alongside a committed
**`.env.example`** with **names only**. Agents **must not read `.env`**; operators
source it outside agent context so SSH/Docker/remote helpers see normal process env.

The architecture locks a **4-layer defense-in-depth** contract (**DEC-0071**):
`.gitignore` (git tracking) + `.cursorignore` (agent file tools) + Cursor rules
(behavioral) + operator discipline (don't open `.env` in editor).

## Assumption challenge and alternatives

| # | Question | Options | Verdict |
|---|----------|---------|---------|
| 1 | **Secret carrier format** | A: repo-root `.env` (standard) / B: `secrets.json` / C: OS keyring | **A** — `.env` is universal, works with `source`, `dotenv`, and shell `export`; B/C add vendor deps with no benefit for local dev. |
| 2 | **Agent exclusion layers** | A: `.gitignore` only / B: `.gitignore` + `.cursorignore` / C: `.gitignore` + `.cursorignore` + rules + operator discipline (4-layer) | **C** — `.gitignore` alone is insufficient (agents have filesystem access beyond git); `.cursorignore` blocks agent file tools but not terminal/MCP; rules add behavioral guard; operator discipline covers open-tab leak. Formalized as **DEC-0071**. |
| 3 | **AC-8 helper** | A: `scripts/print_remote_env_hint.py` (names-only, validates parity with `*Env` fields) / B: documented shell recipe (`source .env && env \| grep`) / C: deliberate omission | **A** — cross-platform, deterministic, validates parity, never touches `.env` values; B is POSIX-only and leaks values to stdout; C loses parity enforcement. |
| 4 | **Template `.gitignore`** | A: create `template/.gitignore` with `.env` entry / B: document that template users add their own | **A** — this repo ships a template; shipped templates should include `.env` in `.gitignore` so new projects inherit gitignore safety from day one. |
| 5 | **Agent rule placement** | A: extend `.cursor/rules/coding-standards.mdc` / B: new dedicated rule file | **A** — existing `coding-standards.mdc` already has the **DEC-0016** remote config security bullet; one additional bullet is simpler than a new file. Template parity via `template/.cursor/rules/coding-standards.mdc`. |

## File layout (locked)

| Path | Status | Content |
|------|--------|---------|
| **`.env`** | gitignored, cursorignored, **never committed** | Operator-local values for 20 `*Env` variables |
| **`.env.example`** | committed (active + `template/`) | Names only, grouped by source config, with comments |
| **`.gitignore`** | updated (active + `template/`) | Add `.env` and `.env.local` patterns |
| **`.cursorignore`** | **new** (active + `template/`) | `.env`, `.env.local`, `.env.*` exclusion patterns |
| **`.cursor/rules/coding-standards.mdc`** | updated (active + `template/`) | Add `.env` exclusion rule bullet |
| **`scripts/print_remote_env_hint.py`** | **new** (active only) | Names-only parity helper (AC-8) |
| **`docs/engineering/runbook.md`** | updated (active + `template/`) | `.env` copy/source recipe |
| **`docs/engineering/runtime-connectivity.md`** | updated (active + `template/`) | `*Env` sourcing from `.env` |
| **`docs/engineering/us-0084-remote-e2e.md`** | updated (active + `template/`) | `.env` / `.env.example` refs in Path B/C |
| **`tests/test_env_gitignore.py`** | **new** (active only) | AC-9 regression: `git check-ignore` assertions |

## `.env.example` content contract

Names grouped by source — **no values, no secret-shaped literals**.

### From `template/.cursor/remote.json` (3 names)

```
REMOTE_DOCKER_TOKEN
REMOTE_SSH_USER
REMOTE_SSH_KEY_PATH
```

### From `docs/engineering/release-targets.json` (17 names)

```
PUBLIC_DOMAIN
CHOCO_API_KEY
GITHUB_TOKEN
DOCKER_TOKEN
DOCKER_RUNTIME_HOST
AWS_PROFILE
APP_DOMAIN
APP_IP
CUSTOM_DOMAIN
CUSTOM_IP
SSH_HOST
SSH_USER
SSH_PRIVATE_KEY
RUNTIME_DOMAIN
RUNTIME_IP
DOCKER_HOST
DOCKER_CONTEXT
```

Total: **20 unique `*Env` names**. `.env.example` must list all 20 with section
comments indicating which config file references each group. The helper script
(**AC-8**) validates this set against the JSON source files at runtime.

## `.cursorignore` contract

```
# Agent exclusion — secrets must not be ingested by AI tools (US-0085 / DEC-0071)
.env
.env.local
.env.*
```

Semantics per Cursor documentation: `.gitignore` syntax; blocks agent file tools
(`read_file`, `grep`, `@` mentions); does **not** block terminal commands or MCP
tools. Open-tab caveat: files open in editor may still leak to context.

## Agent rule text (`.cursor/rules/coding-standards.mdc`)

Append after existing DEC-0016 remote config bullet:

```
- `.env` exclusion (DEC-0071 / US-0085): do not open, attach, read, search
  inside, or index `.env` or `.env.*` files. Use environment variable names
  in prose only. Operators source `.env` outside agent context.
```

## `scripts/print_remote_env_hint.py` contract (AC-8)

- **Input**: reads `.env.example` for names; reads `template/.cursor/remote.json`
  and `docs/engineering/release-targets.json` for `*Env` field inventory.
- **Output**: prints required env var names to stdout (one per line, grouped).
- **Parity check**: reports any name in JSON `*Env` fields not in `.env.example`
  (exit 1 with `ENV_EXAMPLE_PARITY_MISMATCH`), and any name in `.env.example`
  not in JSON sources (warning, exit 0).
- **Safety**: **never** opens, reads, or prints from `.env` — values stay local.
- **Exit codes**: 0 = PASS / parity ok; 1 = parity mismatch (missing names).

## Test approach (AC-9)

`tests/test_env_gitignore.py` using `subprocess.run`:

1. `git check-ignore .env` → exit code 0 (`.env` is gitignored).
2. `git check-ignore .env.example` → exit code 1 (`.env.example` is NOT ignored).
3. Optional: assert `.cursorignore` file exists and contains `.env` pattern.

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

Scripts (`print_remote_env_hint.py`) and tests (`test_env_gitignore.py`) are
**active-only** (not shipped in template — template users write their own).

## Interaction with related stories

| Story | Interaction |
|-------|-------------|
| **US-0064** (DONE) | `release-targets.json` contract **unchanged** — still `*Env` name references only; `.env` supplies **values** locally. |
| **US-0084** (DONE) | `remote_config_summary.py` reads `remote.json` names, **not** `.env` values — **AC-10 PASS** guaranteed. `us-0084-remote-e2e.md` updated to mention `.env` sourcing pattern. |
| **US-0086** (OPEN) | Automation profile must **compose** with `.env` — automation may **use** env already set; **must not** read `.env` (inherits **DEC-0071** contract). |

## Defense-in-depth layering (**DEC-0071**)

| Layer | Mechanism | Blocks | Does NOT block |
|-------|-----------|--------|----------------|
| 1. `.gitignore` | Git tracking exclusion | Commit/push of `.env` | Agent filesystem reads |
| 2. `.cursorignore` | Cursor file-tool exclusion | `read_file`, `grep`, `@` mentions | Terminal commands, MCP tools |
| 3. Cursor rules | Behavioral instruction | Agent intent to open/search `.env` | Operator or terminal bypass |
| 4. Operator discipline | Human practice | Opening `.env` in editor (context leak) | Nothing (last resort) |

**Residual risk**: An operator who opens `.env` in the editor tab may leak it to
agent context. Mitigation: runbook warns explicitly; `.cursorignore` still blocks
proactive agent file-tool access.

## Risks

| Risk | Severity | Mitigation |
|------|----------|------------|
| Terminal bypass (agent runs `cat .env`) | Medium | Cursor rules instruct agents not to; `.cursorignore` blocks file tools; runbook warns operators. Cannot be fully prevented at framework level. |
| Open-tab leak (`.env` open in editor) | Low | Runbook + rules warn; `.cursorignore` blocks proactive agent reads. |
| `.env` framework collision (e.g. Node dotenv auto-loads) | Low | This repo is a toolkit, not a Node app; document in `.env.example` header. |
| Template `.env.example` divergence when `*Env` fields change | Low | `print_remote_env_hint.py` parity check catches drift; run in CI or pre-release. |
| `remote_config_summary.py` regression | Low | AC-10 explicitly requires existing tests PASS; script reads `remote.json`, not `.env`. |

## Decision linkage

- Decision: **`DEC-0071`** — 4-layer defense-in-depth `.env` exclusion contract
- Research: **`R-0072`**
- Related: **`US-0064`**, **`DEC-0070`**, **`US-0084`**, **`US-0086`**, **`DEC-0016`**, **`R-0067`**, **`R-0068`**

---

