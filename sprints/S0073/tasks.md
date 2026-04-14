# Tasks — S0073 / US-0085

## T-001 — Update `.gitignore` (active + template) — AC-1

- **AC**: AC-1
- **Description**: Add `.env` and `.env.local` patterns to the active `.gitignore`. Create `template/.gitignore` with the same `.env`/`.env.local` entries so new projects inherit gitignore safety from day one.
- **Files**: `.gitignore`, `template/.gitignore` (new)
- **Status**: done
- **Acceptance**: `git check-ignore .env` returns exit 0; `git check-ignore .env.example` returns exit 1.

## T-002 — Create `.cursorignore` (active + template) — AC-2

- **AC**: AC-2
- **Description**: Create `.cursorignore` at repo root (and `template/.cursorignore`) with `.env`, `.env.local`, `.env.*` exclusion patterns per DEC-0071 layer 2. Blocks agent file tools (`read_file`, `grep`, `@` mentions); does not block terminal commands or MCP tools.
- **Files**: `.cursorignore` (new), `template/.cursorignore` (new)
- **Status**: done
- **Acceptance**: `.cursorignore` exists and contains `.env` pattern; template parity verified.

## T-003 — Create `.env.example` (active + template) — AC-3

- **AC**: AC-3
- **Description**: Create committed `.env.example` at repo root (and `template/.env.example`) with 20 `*Env` variable names grouped by source config. No values, no secret-shaped literals. Groups: 3 from `template/.cursor/remote.json` (`REMOTE_DOCKER_TOKEN`, `REMOTE_SSH_USER`, `REMOTE_SSH_KEY_PATH`), 17 from `docs/engineering/release-targets.json` (`PUBLIC_DOMAIN`, `CHOCO_API_KEY`, `GITHUB_TOKEN`, `DOCKER_TOKEN`, `DOCKER_RUNTIME_HOST`, `AWS_PROFILE`, `APP_DOMAIN`, `APP_IP`, `CUSTOM_DOMAIN`, `CUSTOM_IP`, `SSH_HOST`, `SSH_USER`, `SSH_PRIVATE_KEY`, `RUNTIME_DOMAIN`, `RUNTIME_IP`, `DOCKER_HOST`, `DOCKER_CONTEXT`).
- **Files**: `.env.example` (new), `template/.env.example` (new)
- **Status**: done
- **Acceptance**: File contains exactly 20 unique `*Env` names, grouped with section comments; no secret values.

## T-004 — Update runbook with `.env` recipe (active + template) — AC-4

- **AC**: AC-4
- **Description**: Add section to `docs/engineering/runbook.md` (and `template/docs/engineering/runbook.md`) documenting: copy `.env.example` -> `.env`, fill locally, source before remote/SSH/release connectivity checks. Explicitly state forbidden actions (committing `.env`, agents reading `.env`) and allowed actions (running `ssh` / `python scripts/remote_config_summary.py` when env is set).
- **Files**: `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- **Status**: done
- **Acceptance**: Runbook contains `.env` copy/source recipe with forbidden/allowed guidance.

## T-005 — Update runtime-connectivity docs (active + template) — AC-5

- **AC**: AC-5
- **Description**: Update `docs/engineering/runtime-connectivity.md` (and `template/docs/engineering/runtime-connectivity.md`) to state that operators may populate `release-targets.json`-referenced `*Env` variables from a sourced `.env` (values never in JSON).
- **Files**: `docs/engineering/runtime-connectivity.md`, `template/docs/engineering/runtime-connectivity.md`
- **Status**: done
- **Acceptance**: Doc contains `*Env` sourcing from `.env` note.

## T-006 — Update us-0084-remote-e2e docs (active + template) — AC-6

- **AC**: AC-6
- **Description**: Update `docs/engineering/us-0084-remote-e2e.md` (and `template/docs/engineering/us-0084-remote-e2e.md`) to reference `.env` / `.env.example` where Path B/C mention `REMOTE_*` env vars.
- **Files**: `docs/engineering/us-0084-remote-e2e.md`, `template/docs/engineering/us-0084-remote-e2e.md`
- **Status**: done
- **Acceptance**: Doc references `.env`/`.env.example` in Path B/C sections.

## T-007 — Append `.env` exclusion rule to agent rules (active + template) — AC-7

- **AC**: AC-7
- **Description**: Append `.env` exclusion bullet to `.cursor/rules/coding-standards.mdc` (and `template/.cursor/rules/coding-standards.mdc`) after existing DEC-0016 remote config security bullet. Text per architecture: "`.env` exclusion (DEC-0071 / US-0085): do not open, attach, read, search inside, or index `.env` or `.env.*` files. Use environment variable names in prose only. Operators source `.env` outside agent context."
- **Files**: `.cursor/rules/coding-standards.mdc`, `template/.cursor/rules/coding-standards.mdc`
- **Status**: done
- **Acceptance**: Rule file contains `.env` exclusion bullet referencing DEC-0071; template parity.

## T-008 — Create `scripts/print_remote_env_hint.py` (active-only) — AC-8

- **AC**: AC-8
- **Description**: Create `scripts/print_remote_env_hint.py` that reads `.env.example` for names; reads `template/.cursor/remote.json` and `docs/engineering/release-targets.json` for `*Env` field inventory; prints required env var names to stdout (one per line, grouped). Parity check: reports any name in JSON `*Env` fields not in `.env.example` (exit 1 with `ENV_EXAMPLE_PARITY_MISMATCH`), and any name in `.env.example` not in JSON sources (warning, exit 0). Never opens, reads, or prints from `.env`.
- **Files**: `scripts/print_remote_env_hint.py` (new)
- **Status**: done
- **Acceptance**: Script runs successfully; reports parity PASS; exit 0 when aligned; exit 1 on mismatch.

## T-009 — Create `tests/test_env_gitignore.py` (active-only) — AC-9

- **AC**: AC-9
- **Description**: Create `tests/test_env_gitignore.py` using `subprocess.run`: (1) `git check-ignore .env` -> exit code 0 (`.env` is gitignored); (2) `git check-ignore .env.example` -> exit code 1 (`.env.example` is NOT ignored); (3) assert `.cursorignore` file exists and contains `.env` pattern.
- **Files**: `tests/test_env_gitignore.py` (new)
- **Status**: done
- **Acceptance**: All test assertions pass; pytest collects and runs the tests.

## T-010 — Verify `remote_config_summary.py` + tests remain PASS — AC-10

- **AC**: AC-10
- **Description**: After all other changes, verify that `python scripts/remote_config_summary.py` and existing `remote_config_summary` tests remain PASS. US-0064 JSON contract unchanged — script reads `remote.json` names, not `.env`. No code changes expected; this is a verification-only task.
- **Files**: (verification only — no new files)
- **Status**: done
- **Acceptance**: `remote_config_summary.py` runs without error; existing tests pass.
