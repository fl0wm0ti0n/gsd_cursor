# PO to TL archive pack (2026-06-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated architecture handoff — BUG-0012 / auto-20260612-01`
- Last archived heading: `## Orchestrated architecture handoff — BUG-0012 / auto-20260612-01`
- Verification tuple (mandatory):
  - archived_body_lines=51
  - retained_body_lines=789

---

## Orchestrated architecture handoff — BUG-0012 / auto-20260612-01

### Target

- `bug_id=BUG-0012`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`architecture`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0012-architecture-20260612T220000Z-fresh`
- `next_scheduled_phase=sprint-plan`
- `segment_work_item_kind=bug`
- `native_chain_active=true`
- `dec_id=DEC-0081`

### Summary

- **`/architecture`** **PASS** — **`DEC-0081`** authored (amends **`DEC-0080`** enforcement layer only); **`docs/engineering/architecture.md`** **`# BUG-0012`** appended; orchestrator **MUST Task-spawn** mandate + phase-role vs orchestrator actor distinction; native-chain precedence over US-0088 Option B; drain-advance step 7 no-stop + continuation-truth breadcrumbs (`native_chain_continuing`, `drain_advance_action`); four **`test_bug0012_*`** contract markers; forbidden-prose negative grep; runbook multi-segment E2E recipe.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Locked decisions (DEC-0081 summary)

1. **Orchestrator compliance** — after subagent return, **MUST Task-spawn** when continuation schedulable; phase-role "stop" ≠ run terminal.
2. **Native-chain precedence** — under **`full_autonomy`** IDE, supersedes US-0088 Option B / US-0092 outer-driver re-invoke (fallback only on **`NATIVE_CHAIN_UNAVAILABLE`** / headless).
3. **Step 7 enforcement** — no operator stop between drain-advance steps 6–7; `drain_advance_action=spawned` attestation.
4. **Continuation-truth breadcrumbs** — `native_chain_continuing` + `drain_advance_action` in `state.md`.
5. **Contract tests** — four **`test_bug0012_*`** additive markers; **`test_us0095_*`** preserved.
6. **Non-goals** — **BUG-0006**, **DEC-0078**, **DEC-0038**, **DEC-0069** unchanged; outer driver optional fallback.

### Atomic task seeds (8; `/sprint-plan` converts to T-xxx)

See **`docs/engineering/architecture.md`** **`# BUG-0012`** § Atomic task seeds.

### Evidence refs

- `decisions/DEC-0081.md`
- `docs/engineering/architecture.md` (**`# BUG-0012`**)
- `docs/engineering/decisions.md` (index + context pack)
- `docs/product/backlog.md` (`### BUG-0012` `architecture_notes`)
- `docs/engineering/research.md` (**`R-0083`**)
- `docs/engineering/state.md` (Architecture checkpoint — this run)
- `handoffs/resume_brief.md` (sprint-plan pointer)

### Next

- **`/sprint-plan`** (fresh **tech-lead** context) for **`BUG-0012`** — seed sprint from 8 task seeds + AC ↔ § map.

### Decision gate

- **None** — architecture satisfied; bug **OPEN**.

---

