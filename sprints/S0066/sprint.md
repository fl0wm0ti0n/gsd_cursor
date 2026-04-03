# Sprint S0066

- **Bug**: `BUG-0005`
- **Goal**: Implement **DEC-0069** — deterministic **atomic refresh** of **`handoffs/resume_brief.md`** on successful **`/intake bug`** persistence so **`/intake bug` → `/auto`** does not false-trigger **`RESUME_BRIEF_STALE`**, while preserving resume precedence and fail-fast contracts (**`R-0064`** matrix).
- **Status**: **Verify-work PASS** — canonical closure applied (**US-0045**); **`/release`** next (`orchestrator_run_id=auto-20260403-02`)

## Scope (sprint-local AC themes)

- **AC-1** - Wire intake completion writer to perform a **single deterministic** refresh of **`handoffs/resume_brief.md`** after successful bug-row persistence (**`US-0045`**).
- **AC-2** - Emit **minimum field set** per **DEC-0069 §1**: **`bug_id`**, **`intended_resume_phase=discovery`**, **`resolution_source`** seed, boundary **`orchestrator_run_id`** / timestamp when known, **`handoffs/intake_evidence/...`** pointer when present; document **idempotent** rewrite semantics.
- **AC-3** - Ensure refreshed brief **does not contradict** canonical **`docs/product/backlog.md`** facts for the referenced **`bug_id`**.
- **AC-4** - **Active / `template/`** parity for touched **`.cursor/commands/intake.md`** surfaces (and **rules / validator** mirrors per repo parity policy).
- **AC-5** - **R-0064 #1** — regression coverage: after intake persistence, brief targets **`discovery`**; resume resolution does not emit false **`RESUME_BRIEF_STALE`** for the normal path.
- **AC-6** - **R-0064 #2** — deterministic check or test: **absent** brief → **`state.md`** fallback per precedence (no false stale).
- **AC-7** - **R-0064 #3–#4** — explicit **`start-from`** wins; parseable brief **vs backlog** contradiction → fail-fast (**no silent continue**).
- **AC-8** - **R-0064 #5** — portfolio switch: prior bug **DONE**, new bug **OPEN** → brief **`bug_id`** and phase align; no stale **`intake`** carryover.
- **AC-9** - Wire new regression entrypoints into **`tests/run-tests.sh`** and **`tests/run-tests.ps1`** when executable tests are added.

## Governance

- `decisions/DEC-0069.md`
- `docs/engineering/architecture.md` `# BUG-0005`
- `docs/engineering/research.md` `R-0064`
- Related: `US-0037`, `US-0045`, `US-0070`, `US-0080`, `DEC-0038`
