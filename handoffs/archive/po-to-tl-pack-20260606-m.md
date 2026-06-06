# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated discovery handoff — BUG-0011 / auto-20260606-02`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0011 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=57
  - retained_body_lines=754

---

## Orchestrated discovery handoff — BUG-0011 / auto-20260606-02

### Target

- `bug_id=BUG-0011`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0011-discovery-20260606T163655Z-fresh`
- `next_scheduled_phase=research`
- `segment_work_item_kind=bug`
- `bug_queue_position=3` / `bug_queue_remaining=1`

### Summary

- **`/discovery`** **PASS** — root cause confirmed: **US-0089** / **DEC-0072** shipped Caveman **scaffolding** (gates, 9-zone literal invariant, toggles, default-off) but `.cursor/rules/caveman.mdc` lacks upstream voice-compression rules. With **`CAVEMAN_MODE=1`**, replies stay verbose because no rule text instructs drop-filler/fragment/level semantics. Fix completes **response-side voice** only; **US-0090** input compression remains orthogonal and unchanged.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (research inputs)

1. **Gap**: local rule has scratchpad gate + 9-zone MUST + toggles; upstream adds **Rules**, **Intensity**, **Auto-Clarity**, **Persistence** — all missing.
2. **Portable upstream concepts**: lite/full/ultra table, drop articles/filler/hedging, fragments OK, auto-clarity exceptions, token-saving terse prose (not roleplay).
3. **Out of scope**: Wenyan modes, vendor token-percent claims, `npx skills add`, input-side compression changes.
4. **Discovery-locked fix**: append **`## Voice compression (when CAVEMAN_MODE=1)`** to rule + template; extend runbook; additive **`test_caveman_voice_*`** markers; intentional SHA-256 baseline bump for US-0090 pin.
5. **Invariants preserved**: DEC-0072 §4 nine-zone literal list verbatim; US-0088 non-suppressible gates; default-off when `CAVEMAN_MODE=0`.

### Research asks (extend R-0077)

1. SHA-256 bump vs substring-only assertion strategy after rule edit.
2. Level table wording (upstream-adapted vs kit-native examples).
3. User-rule precedence paragraph placement in always-on rule.
4. Contract test marker token list for voice section.
5. Runbook example selection and depth.
6. Architecture surface: `# BUG-0011` vs amend `# US-0089`.
7. Ultra-level abbreviation boundaries vs 9-zone literal overlap.

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0011` — `discovery_notes`)
- `docs/product/vision.md` (Intake notes + Discovery Notes — BUG-0011)
- `docs/engineering/research.md` (**`R-0077`** discovery extension)
- `handoffs/intake_evidence/BUG-0011-intake-20260606.json`
- `.cursor/rules/caveman.mdc`; `template/.cursor/rules/caveman.mdc`
- `decisions/DEC-0072.md` §2 (rule-only), §4 (9-zone), §6 (voice quality deferred)
- Upstream reference: JuliusBrussee/caveman `skills/caveman/SKILL.md` (MIT, not vendored)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (research pointer)

### Next

- **`/research`** (fresh **tech-lead** context) for **`BUG-0011`** — resolve **`R-0077`** Q1–Q7 before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; bug **OPEN**.

---

