## Dev -> QA Handoff — US-0086 / S0074

> **2026-04-13T21:05:00Z** — `/execute` complete (dev, `orchestrator_run_id=auto-20260405-01`). Story **US-0086** remains **OPEN** (US-0045). Sprint **S0074**. All 10 tasks (T-001..T-010) done. Ready for `/qa`.

### What changed

1. **Scratchpad automation profile keys** (AC-1):
   - `.cursor/scratchpad.md`
   - `template/.cursor/scratchpad.md`
   - `.cursor/scratchpad.local.example.md`
   - `template/.cursor/scratchpad.local.example.md`
   Added `AUTO_REMOTE_AUTOMATION_PROFILE` and `AUTO_REMOTE_ENVIRONMENT_LABEL`
   with default-off/manual-safe values.

2. **Manual vs automation mode docs** (AC-2, AC-6, AC-7):
   - `docs/engineering/runbook.md`
   - `template/docs/engineering/runbook.md`
   - `docs/engineering/runtime-connectivity.md`
   - `template/docs/engineering/runtime-connectivity.md`
   Added deterministic mode split, fail-closed reason codes, names-only tuple
   contract, and optional deterministic CI routing recipe.

3. **Deterministic routing contract updates** (AC-3, AC-4):
   - `.cursor/commands/auto.md`
   - `template/.cursor/commands/auto.md`
   - `docs/engineering/auto-orchestration-reference.md`
   - `template/docs/engineering/auto-orchestration-reference.md`
   Added `start container <target_id>` literal, mode-off no-reroute guardrail,
   and locked reason-code vocabulary.

4. **Security/rule guidance** (AC-7):
   - `.cursor/rules/coding-standards.mdc`
   - `template/.cursor/rules/coding-standards.mdc`
   Added explicit US-0086 guardrail for no silent remote reroute when profile
   is off, plus fail-closed unknown/disabled target handling.

5. **Evidence tuple handoff guidance** (AC-5):
   - `handoffs/qa_to_verify_work.md`
   Added required names-only routing tuple fields.

6. **Execute artifact updates**:
   - `sprints/S0074/tasks.md` -> all statuses set to `done`
   - `sprints/S0074/summary.md` -> execute checkpoint and next phase pointer
   - `docs/engineering/state.md` -> execute checkpoint + strict proof + phase boundary
   - `handoffs/resume_brief.md` -> top pointer moved to `intended_resume_phase=qa`

7. **Contract tests** (AC-8, AC-10):
   - `tests/auto_command_contract_test.py`
   Added US-0086 token assertions for command/reference docs, scratchpad keys,
   and runbook/handoff tuple guidance.

### Remote-routing evidence tuple for this execute run

- `target_id=local-default`
- `environment_label=local`
- `automation_profile=off`
- `routing_source=local_default`
- `secret_surface=names_only`

### Test evidence

- `python -m pytest tests/auto_command_contract_test.py -q` -> PASS
- `python -m pytest tests/remote_config_summary_test.py -q` -> PASS

### Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-execute-dev-20260413T210500Z-S0074-US0086`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-13T21:05:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=672482884dfa858726a194e3eb07f77ca7f3eb077b3d58c24c096fe6cefafc41`

### Next

- `/qa` (fresh qa subagent) for S0074 / US-0086

## Dev -> QA Handoff — US-0085 / S0073

> **2026-04-13T14:00:00Z** — `/execute` complete (dev, `orchestrator_run_id=auto-20260405-01`). Story **US-0085** remains **OPEN** (US-0045). Sprint **S0073**. All 10 tasks (T-001..T-010) done. Ready for `/qa`.

### What changed

1. **`.gitignore` + `template/.gitignore`** (AC-1): Added `.env`, `.env.local`, `.env.*` exclusion patterns with `!.env.example` negation to keep the example tracked.

2. **`.cursorignore` + `template/.cursorignore`** (AC-2): New files blocking agent file tools from `.env*` files, with `!.env.example` negation.

3. **`.env.example` + `template/.env.example`** (AC-3): 20 `*Env` variable names grouped by source config (3 from `remote.json`, 17 from `release-targets.json`). Names only, no values.

4. **`docs/engineering/runbook.md`** + template (AC-4): New "Operator `.env` setup" section with copy/source recipe, forbidden actions (committing `.env`, agents reading `.env`), and allowed actions.

5. **`docs/engineering/runtime-connectivity.md`** + template (AC-5): Added "`*Env` variable sourcing" section referencing `.env` pattern.

6. **`docs/engineering/us-0084-remote-e2e.md`** + template (AC-6): Path B and C updated to reference `.env`/`.env.example` for operator env var setup.

7. **`.cursor/rules/coding-standards.mdc`** + template (AC-7): Added `.env` exclusion rule bullet after DEC-0016 remote config security bullet.

8. **`scripts/print_remote_env_hint.py`** (AC-8): Names-only parity helper. Reads `.env.example` and JSON configs, validates 20-name parity. Exit 0 on PASS, exit 1 on mismatch. Never reads `.env`.

9. **`tests/test_env_gitignore.py`** (AC-9): 4 regression tests — `.env` gitignored, `.env.example` NOT gitignored, `.cursorignore` exists with pattern, `.env.example` has 20 names.

10. **Existing tests** (AC-10): `remote_config_summary.py` exit 0; full suite 56/0 passed/failed.

### Test evidence

- New tests: **4 passed** (`tests/test_env_gitignore.py`)
- Parity script: **Parity PASS** (20/20 names)
- Full test suite: **56 passed**, 4 skipped, 66 subtests passed, **0 failed**
- Triad hot surface: `--check` PASS
- User-visible metadata: PASS

### Environment

- Platform: Windows 10 (local)
- Tests ran locally via `python -m pytest tests/ -q`
- `REMOTE_EXECUTION` not set (skip mode — remote_config_summary exit 0)

### Files for QA review

| Path | Change type |
|------|------------|
| `.gitignore` | Modified — `.env*` patterns + `!.env.example` negation |
| `template/.gitignore` | New — `.env*` patterns + `!.env.example` negation |
| `.cursorignore` | New — agent exclusion patterns |
| `template/.cursorignore` | New — agent exclusion patterns |
| `.env.example` | New — 20 env var names, grouped, no values |
| `template/.env.example` | New — parity copy |
| `docs/engineering/runbook.md` | Modified — `.env` setup section |
| `template/docs/engineering/runbook.md` | Modified — parity copy |
| `docs/engineering/runtime-connectivity.md` | Modified — `*Env` sourcing note |
| `template/docs/engineering/runtime-connectivity.md` | Modified — parity copy |
| `docs/engineering/us-0084-remote-e2e.md` | Modified — `.env` refs in Path B/C |
| `template/docs/engineering/us-0084-remote-e2e.md` | Modified — parity copy |
| `.cursor/rules/coding-standards.mdc` | Modified — `.env` exclusion rule |
| `template/.cursor/rules/coding-standards.mdc` | Modified — parity copy |
| `scripts/print_remote_env_hint.py` | New — parity helper |
| `tests/test_env_gitignore.py` | New — regression tests |

### Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-execute-dev-20260413T140000Z-S0073-US0085`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-13T14:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=f0590356f1ae4922a5bd235db44a0213e63f96d57288ccfee86de5e2a56835bb`

### Next

- `/qa` (fresh qa subagent) for S0073 / US-0085
