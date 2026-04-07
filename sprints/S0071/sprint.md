# Sprint S0071

- **Story**: **`US-0087`**
- **Goal**: Ship **default-off**, **fail-closed** **`/auto`** bug targeting: explicit **`bug-target=BUG-####`** / **`bug-target=all-open`** argv; merged **`AUTO_BUG_*`** scratchpad keys (**`template/`** parity); **one active scheduler** vs **`AUTO_BACKLOG_DRAIN`** (**`AUTO_SCHEDULER_CONFLICT`**); OPEN-bug queue semantics (**numeric sort**, **`AUTO_BUG_MAX_ITEMS`**, **`AUTO_BUG_QUEUE_EMPTY`**); **`resume_brief.md`** + **`state.md`** segment breadcrumbs (**`DEC-0069`**, **AC-10** tuple); **spawn-only** orchestrator contract unchanged; **`tests/auto_command_contract_test.py`** markers; **`architecture.md`** **`# US-0087`** + **`runbook.md`** operator recipe; **active + `template/`** parity — per **`docs/engineering/architecture.md`** **`# US-0087`** and **`docs/engineering/research.md`** **`R-0070`**.
- **Status**: **OPEN** — **`sprints/S0071/plan-verify.json`** **`PASS`** (`2026-04-06T23:00:00Z`, **qa**); next **`/execute`** (**dev**).

## Scope (sprint-local AC themes)

- **AC-1** - **Syntax contract**: exact **`/auto`** argv spellings **`bug-target=BUG-####`** / **`bug-target=all-open`**; deterministic fail-closed codes (**`AUTO_BUG_TARGET_UNKNOWN`**, **`AUTO_BUG_TARGET_NOT_OPEN`**, **`AUTO_BUG_QUEUE_EMPTY`**, etc.) — **`# US-0087`** vocabulary.
- **AC-2** - **Scratchpad + `template/`**: **`AUTO_BUG_QUEUE`**, **`AUTO_BUG_TARGET`**, **`AUTO_BUG_MAX_ITEMS`**, **`AUTO_BUG_ON_BLOCK`** — **default-off** commentary and examples.
- **AC-3** - **`auto-orchestration-reference.md`** + **`.cursor/commands/auto.md`**: resume precedence extended for bug-target; **`AUTO_BACKLOG_DRAIN`** vs bug scheduler **mutex** documented (**argv** resolution path).
- **AC-4** - **Queue semantics**: **OPEN** bugs only, ascending **numeric** **`BUG-####`** order; **`AUTO_BUG_MAX_ITEMS`** cap; empty queue → locked reason code.
- **AC-5** - **`resume_brief.md`** + **`state.md`**: per-segment **`bug_id`**, queue cursor fields (**`bug_queue_position`**, **`bug_queue_remaining`**) without **`RESUME_BRIEF_STALE`** false positives for lawful runs.
- **AC-6** - **Spawn-only**: orchestrator does **not** execute phase work in-process (**`BUG-0006`** / **`US-0069`**) — explicit in bug-queue prose.
- **AC-7** - **Tests**: **`tests/auto_command_contract_test.py`** — literals / rows for argv tokens, **`AUTO_SCHEDULER_CONFLICT`**, template parity hooks.
- **AC-8** - **Architecture** **`# US-0087`**: reason codes, flag names, interaction matrix (**`US-0044`**, **`DEC-0069`**, **`US-0070`**, **`US-0079`**) — kept consistent with shipped docs/tests.
- **AC-9** - **Runbook**: operator recipe **“targeted bug auto drain”** in **`docs/engineering/runbook.md`**.
- **AC-10** - **Active + `template/`** parity for all touched command / reference / scratchpad paths.

## Governance

- `docs/engineering/architecture.md` `# US-0087`
- `docs/engineering/research.md` `R-0070`
- Related: **`US-0044`**, **`US-0045`**, **`US-0069`**, **`US-0070`**, **`US-0079`**, **`DEC-0069`**, **`BUG-0006`**
