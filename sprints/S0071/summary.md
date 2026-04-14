# Sprint S0071 — summary (US-0087)

- **Sprint**: **S0071**
- **Story**: **US-0087** — **`/auto`** explicit bug targeting (**DONE** per **`US-0045`**; **`/release`** **PASS** **`2026-04-12`**)
- **Orchestrator run**: **auto-20260405-01**
- **QA cycle**: initial **`/qa`** **FAIL** (**790**/4); **dev remediation** + **DEC-0054** triad rollover (**`state-pack-20260407-b.md`**) before final harness; **fresh `/qa`** **PASS** (**794**/0, **`2026-04-07`**) — **`sprints/S0071/qa-findings.md`**, **`handoffs/qa_to_verify_work.md`**, **`handoffs/dev_to_qa.md`**.

## Implemented (execute / dev)

- **T-001..T-010** complete per **`sprints/S0071/tasks.md`**.
- **`.cursor/commands/auto.md`** + **`template/.cursor/commands/auto.md`**: **`bug-target=BUG-####`**, **`bug-target=all-open`**, optional bug-queue section, fail-closed codes, **`AUTO_SCHEDULER_CONFLICT`** mutex, extended resume precedence, **AC-10** bug-field pointer, spawn-only bug-queue cross-refs (**`BUG-0006`**, **`US-0069`**, **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**).
- **`docs/engineering/auto-orchestration-reference.md`** + **`template/docs/engineering/auto-orchestration-reference.md`**: normative **Optional bug-queue mode (US-0087)** (OPEN queue, numeric sort, **`AUTO_BUG_MAX_ITEMS`**, empty-queue **`AUTO_BUG_QUEUE_EMPTY`**), mutex, **`DEC-0069`** segment field table, Steps + per-item summary extensions, resume precedence + fail-fast code list updates.
- **`.cursor/scratchpad.md`**, **`template/.cursor/scratchpad.local.example.md`**, **`template/.cursor/scratchpad.md`**, **`.cursor/scratchpad.local.example.md`**: **`AUTO_BUG_*`** keys + US-0087 catalog where required for **US-0075** pair parity; materialized baseline **`RELEASE_PUBLISH_MODE=confirm`** (harness + safe default).
- **`docs/engineering/runbook.md`** + **`template/docs/engineering/runbook.md`**: **Targeted bug auto drain (US-0087)** operator subsection.
- **`docs/engineering/architecture.md`**: **`# US-0087`** mutex prose aligned with **`[AUTO_RESUME_ERROR]`** documentation (no “TBD”).
- **`tests/auto_command_contract_test.py`**: markers for argv literals, scheduler conflict, **`US-0087`** / **`DEC-0069`**, reference↔template parity test, scratchpad key presence tests.
- **QA remediation**: **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** resume-precedence substring aligned to shipped **`auto.md`** text.

## Tests / checks (dev)

| Command | Outcome |
|---------|---------|
| `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` | **PASS** (exit **0**) — post-remediation full harness |
| `python scripts/check-scratchpad-pair-parity.py --repo .` | **`[SCRATCHPAD_PAIR_OK]`** |
| `python -m pytest tests/auto_command_contract_test.py -q` | **PASS** — 7 passed, 41 subtests (prior + still green) |
| `python scripts/check-user-visible-metadata.py` | **PASS** (exit 0) |
| `python scripts/enforce-triad-hot-surface.py` | **`--rollover`** (`units=1` → **`state-pack-20260407-a.md`**) then harness green; final **`--check`** after state append per execute closeout |

## Open risks

- **Behavioral orchestrator** implementation in Cursor still interprets these docs; contract tests lock **literals and parity**, not runtime scheduling.
- **`AUTO_BACKLOG_DRAIN=1`** on active repo scratchpad remains **story** scheduling; **`AUTO_BUG_QUEUE=0`** avoids mutex until operators opt in.

## Release + curator closure

- **`/release`** **PASS** **`2026-04-12`** — **`sprints/S0071/release-findings.md`**, **`handoffs/releases/S0071-release-notes.md`**, **`handoffs/release_queue.md`** **`S0071`** **`released`**.
- **`/refresh-context`** **PASS** **`2026-04-12T20:35:00Z`** (curator) — reconciled **`docs/engineering/decisions.md`**, this summary, **`docs/engineering/research.md`** (**`R-0070`** closed), **`handoffs/resume_brief.md`**; checkpoint + **DEC-0038** tuple on **`docs/engineering/state.md`**.

## Next (portfolio)

- **`US-0088`** **OPEN** — **`/discovery`** (fresh **PO**) or **`/auto start-from=discovery`**; intake evidence **`handoffs/intake_evidence/US-0088-intake-20260407.json`**.
