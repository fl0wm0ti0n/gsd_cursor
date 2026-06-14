# PO to TL archive pack (2026-06-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated research handoff — BUG-0012 / auto-20260612-01`
- Last archived heading: `## Orchestrated research handoff — BUG-0012 / auto-20260612-01`
- Verification tuple (mandatory):
  - archived_body_lines=56
  - retained_body_lines=789

---

## Orchestrated research handoff — BUG-0012 / auto-20260612-01

### Target

- `bug_id=BUG-0012`
- `orchestrator_run_id=auto-20260612-01`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0012-research-20260612T213000Z-fresh`
- `next_scheduled_phase=architecture`
- `segment_work_item_kind=bug`
- `native_chain_active=true`
- `research_anchor=R-0083`

### Summary

- **`/research`** **PASS** — extended **`R-0083`** with Q1–Q6 resolution. **Post-US-0095 runtime regression**: static **`test_us0095_*`** contract **PASS** but operator observes stop after every story segment with manual re-**`/auto`** despite **`full_autonomy`** + drain. **Root cause**: orchestrator **agent compliance gap** (no executable continuation hook) amplified by residual **US-0088/US-0092** stop priming in **`auto.md`** Steps/matrix and reference outer-driver re-invoke row — **not** missing **DEC-0080** contract.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **Q1 contract vs runtime**: seven **`test_us0095_*`** green; runtime FAIL = orchestrator stops after subagent return; fix = orchestrator-only **MUST Task-spawn** mandate + demote Option B escape to **`NATIVE_CHAIN_UNAVAILABLE`** / headless only.
2. **Q2 drain-advance step 7**: steps 1–6 (DEC-0069 pairing) often complete; **step 7 immediate spawn skipped** — invalid `segment exhausted` when budget > 0; add `drain_advance_action` breadcrumb.
3. **Q3 forbidden prose**: positive guards in native section only; **gap** — US-0088 matrix L68 + Steps L419–420 + reference L783 not negative-grep tested.
4. **Q4 `native_chain_active`**: gate eligibility only — add `native_chain_continuing` + `drain_advance_action` for continuation truth.
5. **Q5 interactions**: **`AUTO_QUIET=1`** messaging ambiguity (not root alone); **US-0096** orthogonal when unset; operator symptom ≠ **`NATIVE_CHAIN_UNAVAILABLE`**.
6. **Q6 tests**: four **`test_bug0012_*`** markers + multi-segment operator E2E runbook recipe (≥2 story boundaries, single `/auto`).

### Evidence refs

- `docs/engineering/research.md` (**`R-0083`** research extension — Q1–Q6 resolved)
- `docs/product/backlog.md` (`### BUG-0012` — `research_notes`)
- `docs/product/vision.md` (**Discovery Notes — BUG-0012**)
- `handoffs/intake_evidence/BUG-0012-intake-20260612.json`
- `.cursor/commands/auto.md` § Native in-chat auto-chain + § Steps (divergence L68, L419–420)
- `docs/engineering/auto-orchestration-reference.md` (L783 outer-driver row; drain-advance algorithm)
- `decisions/DEC-0080.md`; `tests/auto_command_contract_test.py` (`test_us0095_*` — coverage gap)
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)
- Adjacent: **US-0095**, **US-0092**, **DEC-0078**, **BUG-0006**, **DEC-0069**, **R-0081**

### Architecture asks

1. Author **`docs/engineering/architecture.md`** **`# BUG-0012`** (or US-0095 regression amendment) — orchestrator continuation mandate, native-chain precedence over US-0088 Option B, breadcrumb truth fields, four **`test_bug0012_*`** literal strings, runbook E2E recipe.
2. Confirm whether companion **`DEC-xxxx`** amends **DEC-0080** or architecture section alone suffices (research: optional amendment).
3. Lock fix surface: **`auto.md`** + reference + `resume_brief` spawn wording + `state.md` breadcrumbs + contract tests — preserve **BUG-0006**, **DEC-0078**, **DEC-0038**, **DEC-0069**.

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`BUG-0012`** — lock architecture before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; bug **OPEN**.

---

