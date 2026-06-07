# PO to TL archive pack (2026-06-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 14
- First archived heading: `## Orchestrated architecture handoff — US-0095 / auto-20260607-02`
- Last archived heading: `## Orchestrated research handoff — US-0095 / auto-20260607-02`
- Verification tuple (mandatory):
  - archived_body_lines=103
  - retained_body_lines=789

---

## Orchestrated architecture handoff — US-0095 / auto-20260607-02

### Target

- `story_id=US-0095`
- `orchestrator_run_id=auto-20260607-02`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0095-architecture-20260607T193000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`
- `dec_id=DEC-0080`

### Summary

- **`/architecture`** **PASS** — **`DEC-0080`** authored; **`docs/engineering/architecture.md`** **`# US-0095`** appended; native in-chat auto-chain = foreground sequential Task loop; 7-step IDE drain-advance-without-pause; unified cap/ledger composing **DEC-0078**; outer driver demoted to optional IDE fallback; **`AUTO_QUIET`** messaging rules; **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed; spawn-only (**BUG-0006**) unchanged; six `test_us0095_*` contract markers + 8-surface parity inventory.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0080 summary)

1. **IDE-primary native chain** — foreground sequential Task/subagent loop within one `/auto` session when **`full_autonomy`** + IDE context.
2. **Drain-advance** — deterministic 7-step algorithm; immediate in-chat spawn; no mandatory outer driver / re-`/auto` under IDE primary path.
3. **Unified caps** — shared ledger + `native_chain_active`, `outer_cycle_index`, `implementation_loop_index` breadcrumbs.
4. **Fallback matrix** — IDE primary vs headless outer-driver recommended; **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed.
5. **Messaging** — forbidden mandatory outer-driver patterns; **`AUTO_QUIET`** suppression table unchanged for hard gates.
6. **Spawn-only** — **BUG-0006** / **US-0069** unchanged.

### Atomic task seeds (10; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# US-0095`** § Atomic task seeds.

### Evidence refs

- `decisions/DEC-0080.md`
- `docs/engineering/architecture.md` (**`# US-0095`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`## US-0095` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0081`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`US-0095`** — seed sprint from 10 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; story **OPEN**.

---

## Orchestrated research handoff — US-0095 / auto-20260607-02

### Target

- `story_id=US-0095`
- `orchestrator_run_id=auto-20260607-02`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-US0095-research-20260607T190000Z-fresh`
- `next_scheduled_phase=architecture`
- `decomposition=single_story` (per `US-0051`)
- `priority=P1`

### Summary

- **`/research`** **PASS** — extended **`R-0081`** with Q1–Q6 resolution. **Native in-chat auto-chain** = foreground sequential Task/subagent loop within one `/auto` session; IDE **drain-advance-without-pause** algorithm; unified cap/ledger with outer driver; outer driver demoted to optional IDE fallback; **`AUTO_QUIET`** messaging rules; six `test_us0095_*` contract markers + eight-surface parity inventory.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **Q1 continuation**: orchestrator `while` loop — preflight → spawn → await → verify → continue; **`NATIVE_CHAIN_UNAVAILABLE`** fail-closed when Task denied; **`segment exhausted`** invalid when continuation schedulable.
2. **Q2 drain-advance**: 7-step deterministic algorithm composing **US-0044**, **US-0087**, **DEC-0069** — budget decrement, story/bug selection, phase-plan recompute, immediate in-chat spawn.
3. **Q3 caps**: shared ledger **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`**; new `remediation_action` values; `outer_cycle_index` / `implementation_loop_index` breadcrumbs in `state.md`.
4. **Q4 fallback matrix**: IDE primary vs headless/CI outer-driver recommended; README ¶3 demotion within execute scope.
5. **Q5 messaging**: forbidden mandatory outer-driver / re-`/auto` phrases under IDE `full_autonomy`; quiet-mode suppression table unchanged for hard gates.
6. **Q6 tests/parity**: `pytest -k us0095`; touch `auto.md`, reference, runbook, README, contract tests, `# US-0095` architecture.

### Evidence refs

- `docs/engineering/research.md` (**`R-0081`** research extension)
- `docs/product/backlog.md` (`## US-0095` — `research_notes`)
- `docs/product/vision.md` (**Discovery Notes — US-0095**)
- `handoffs/intake_evidence/US-0095-intake-20260607.json`
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)
- Adjacent: **US-0092**, **DEC-0078**, **US-0088**, **R-0078**, **BUG-0006**, **US-0069**

### Architecture asks

1. Author **`docs/engineering/architecture.md`** **`# US-0095`** with native chain loop, drain-advance algorithm, cap/ledger unification, fallback boundary table, messaging rules.
2. Confirm whether companion **`DEC-xxxx`** is needed (research: optional — may compose on **DEC-0078** with IDE-primary amendment) or architecture section alone suffices.
3. Lock exact reason codes (`NATIVE_CHAIN_UNAVAILABLE`), state breadcrumb fields (`native_chain_active`, cycle indices), runbook primary/fallback labels, contract-test literal strings.

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`US-0095`** — lock architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; story **OPEN**.

---

