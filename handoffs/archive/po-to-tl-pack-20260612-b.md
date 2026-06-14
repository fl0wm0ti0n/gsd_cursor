# PO to TL archive pack (2026-06-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated discovery handoff — BUG-0012 / auto-20260612-01`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0012 / auto-20260612-01`
- Verification tuple (mandatory):
  - archived_body_lines=57
  - retained_body_lines=789

---

## Orchestrated discovery handoff — BUG-0012 / auto-20260612-01

### Target

- `bug_id=BUG-0012`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0012-discovery-20260612T204500Z-fresh`
- `next_scheduled_phase=research`
- `segment_work_item_kind=bug`
- `native_chain_active=true`

### Summary

- **`/discovery`** **PASS** — **post-US-0095 runtime regression** confirmed: operator with **`AUTO_FLOW_MODE=full_autonomy`** + **`AUTO_BACKLOG_DRAIN=1`** reports orchestration **stops after every user-story segment** and instructs manual re-**`/auto`** despite **DEC-0080** native in-chat auto-chain contract shipped **2026-06-07** (**US-0095** **DONE** / **S0084**). **Not duplicate of US-0095** — tracks **contract-vs-runtime gap** after recent adjustments. **Spawn-only preserved** (**BUG-0006**): fix targets orchestrator **scheduling/continuation**, not in-band phase execution.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (research inputs)

1. **Regression framing**: static doc/contract markers may **PASS** while Cursor orchestrator agent **stops at turn boundary** — prioritize executable loop audit over re-litigating **US-0095** intent.
2. **Primary failure modes**: (a) invalid terminal **`stop_reason=completed (segment exhausted)`** when drain target schedulable; (b) forbidden mandatory re-**`/auto`** / outer-driver prose under **`full_autonomy`**; (c) skipped **DEC-0080** drain-advance **step 7** spawn after **`refresh-context`**.
3. **Impacted surfaces**: `.cursor/commands/auto.md` native chain; `auto-orchestration-reference.md` drain-advance + **`AUTO_QUIET`** rules; orchestrator Task/subagent foreground loop; `resume_brief.md` segment pointers; `state.md` **`native_chain_active`** breadcrumbs; `tests/auto_command_contract_test.py`.
4. **Discovery-locked fix boundary**: restore IDE in-chat continuation + drain-advance; outer driver **optional fallback only**; **DEC-0078** hard gates unchanged.
5. **Out of scope**: spawn-only weakening; outer-driver deletion; **US-0096** delivery-mode changes; publish automation.

### Research asks (extend R-0083)

1. Reconcile doc/contract PASS vs operator runtime FAIL — agent compliance vs missing executable hook.
2. Drain-advance trigger audit: step 7 immediate spawn vs invalid segment-exhausted stop.
3. Forbidden-prose grep inventory under **`full_autonomy`** + drain.
4. **`native_chain_active`** breadcrumb truthfulness at segment stop.
5. **`AUTO_QUIET=1`**, **US-0096** doc interaction, **`NATIVE_CHAIN_UNAVAILABLE`** fallback boundary.
6. Multi-segment operator E2E + contract markers beyond static string presence.

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0012` — `discovery_notes`)
- `docs/product/vision.md` (**Discovery Notes — BUG-0012**)
- `docs/engineering/research.md` (**`R-0083`** discovery extension)
- `handoffs/intake_evidence/BUG-0012-intake-20260612.json`
- `.cursor/commands/auto.md` § Native in-chat auto-chain (**US-0095** / **DEC-0080**)
- `docs/engineering/auto-orchestration-reference.md` (IDE drain-advance-without-pause)
- `decisions/DEC-0080.md`; `docs/product/backlog.md` **`## US-0095`** (**DONE**)
- Prior arc: operator **`/ask`** **2026-06-07** → **US-0095** intake → native-chain shipped
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (research pointer)

### Next

- **`/research`** (fresh **tech-lead** context) for **`BUG-0012`** — resolve **`R-0083`** Q1–Q6 before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; bug **OPEN**.

---

