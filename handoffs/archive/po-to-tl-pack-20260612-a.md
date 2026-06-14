# PO to TL archive pack (2026-06-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated intake handoff — BUG-0012 / cursor-20260612-BUG0012-intake`
- Last archived heading: `## Orchestrated intake handoff — BUG-0012 / cursor-20260612-BUG0012-intake`
- Verification tuple (mandatory):
  - archived_body_lines=64
  - retained_body_lines=789

---

## Orchestrated intake handoff — BUG-0012 / cursor-20260612-BUG0012-intake

### Target

- `bug_id=BUG-0012`
- `intake_run_id=cursor-20260612-BUG0012-intake`
- phase completed: **`intake`** (**`po`**)
- `selected_pack=small-intake-pack`
- `decomposition=single_bug` (per **US-0051** bug path)
- `next_scheduled_phase=discovery`

### Summary

- **`/intake bug`** **PASS** — operator reports **`AUTO_FLOW_MODE=full_autonomy`** + **`AUTO_BACKLOG_DRAIN=1`** still requires manual **`/auto`** after **every** user-story segment completion; end-of-run messaging cites active drain/full_autonomy while instructing re-invocation. **Regression** against delivered **US-0095** / **DEC-0080** native in-chat auto-chain (**S0084** released **2026-06-07**).
- **Not duplicate of US-0095** — that story delivered the contract; **BUG-0012** tracks **runtime/operator-observed** failure to honor it post-recent adjustments.

### Intake evidence (US-0078 / DEC-0060)

- `asked_topics`: outcome_success_criteria, impacted_components, constraints_compatibility_risks, required_tests_acceptance_checks, done_definition
- `missing_topics`: (none)
- `assumptions_confirmed`: (none)
- `topic_coverage`: `handoffs/intake_evidence/BUG-0012-intake-20260612.json` — validator **`[INTAKE_EVIDENCE_VALIDATION_OK]`**

### Scope boundaries

| In scope | Out of scope |
|----------|--------------|
| IDE **`/auto`** native-chain continuation loop | Rewriting **US-0095** intent |
| Drain-advance-without-pause execution (step 7 spawn) | Mandatory outer-driver as primary path |
| Forbidden terminal "re-run /auto" prose under **`full_autonomy`** | **`DELIVERY_MODE`** / **US-0096** lifecycle shape |
| Contract-test + operator multi-segment E2E regression | Weakening **DEC-0078** hard gates |

### Key assumptions / risks

1. **Doc-vs-runtime gap**: **US-0095** contract tests may pass while orchestrator agent stops at Cursor turn boundaries — discovery must confirm enforcement mechanism.
2. **Prior arc**: same symptom triggered **US-0095** (**2026-06-07**); fix may need **behavioral** guardrails not just documentation.
3. **Scratchpad**: operator uses **`full_autonomy`** + drain + **`AUTO_QUIET=1`** — quiet mode must not suppress required continuation (only routine PASS chatter per **US-0095**).

### Evidence refs

- `handoffs/intake_evidence/BUG-0012-intake-20260612.json`
- `docs/product/backlog.md` (`### BUG-0012`)
- `docs/engineering/research.md` (**`R-0083`** stub)
- `.cursor/scratchpad.md` (automation flags)
- `.cursor/commands/auto.md` § Native in-chat auto-chain
- `decisions/DEC-0080.md`, `docs/product/backlog.md` **`## US-0095`** (DONE)
- Prior operator **`/ask`** thread (US-0095 origin)

### Discovery asks

1. Reproduce: single **`/auto`** run through one full story segment — capture **`stop_reason`**, **`native_chain_active`**, drain-advance branch taken or skipped.
2. Identify root cause class: orchestrator stops early vs missing Task spawn vs stale **`resume_brief`** blocking advance (**`RESUME_BRIEF_STALE`**).
3. Lock fix surface: command contract amendment, orchestrator loop invariant, and/or stronger end-of-run gate that **refuses** terminal stop when next segment schedulable.

### Next

- **`/discovery`** (fresh **PO**) for **`BUG-0012`**

### Decision gate

- **None** at intake — defect-shaped input routed correctly via **`/intake bug`**.

---

