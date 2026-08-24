# PO to TL archive pack (2026-08-24)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 11
- First archived heading: `## US-0124 spec PASS — pointer`
- Last archived heading: `## Spec handoff — US-0124 OpenCode orchestrator plugin spawn-only `/auto``
- Verification tuple (mandatory):
  - archived_body_lines=17
  - retained_body_lines=650

---

## US-0124 spec PASS — pointer

- US-0124 spec (intake+discovery) PASS; Status OPEN; AC-1..AC-11 unchecked; full narrative `docs/product/vision.md ## Intake Notes — US-0124` + `## Discovery Notes — US-0124`; research anchor **R-0109** (US-0124 DQ1..DQ8 to be deepened by tech-lead; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 locks PRESERVED — not wiped); next `/research` (tech-lead) deepens R-0109 US-0124 subsection, then `/architecture` locks plugin entry-point + spawn API + reason-code namespace + headless path + agent/plugin boundary; proofs intake `2ADC7B01895C80C62ABB5658D417E5B826A6AD029A109B4122FE9E141662C462` discovery `3E617F6C2F2F6630F7A75790D990ACD890ED63507F8643884A5FF1A346896648` (model_id=glm-5.2-high).

## Spec handoff — US-0124 OpenCode orchestrator plugin spawn-only `/auto`

- **Phase completed**: spec (`intake + discovery`). **Role**: po. **Story**: US-0124. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: intake 2026-08-24T15:55:00Z; discovery 2026-08-24T15:58:00Z. **Fresh markers**: `po-US0124-intake-20260824T155500Z-fresh`, `po-US0124-discovery-20260824T155800Z-fresh`.
- **Runtime proofs**: intake `rp-auto-20260824-01-intake-po-20260824T155500Z-US-0124` (`proof_hash=2ADC7B01895C80C62ABB5658D417E5B826A6AD029A109B4122FE9E141662C462`, ttl 2026-08-24T16:55:00Z); discovery `rp-auto-20260824-01-discovery-po-20260824T155800Z-US-0124` (`proof_hash=3E617F6C2F2F6630F7A75790D990ACD890ED63507F8643884A5FF1A346896648`, ttl 2026-08-24T16:58:00Z).
- **Intake verdict**: PASS by existing program evidence; no new story ID allocated, no ACs wiped. `handoffs/intake_evidence/US-0121-intake-20260822.json` maps `orchestrator-plugin-spawn` + `headless-invoke-cmd` → [US-0124], `coverage_complete=true`, `missing_topics=[]`, `selected_pack=first-intake-pack`. Intake evidence JSON NOT mutated. US-0121/US-0122/US-0123 remain DONE; US-0124 remains OPEN.
- **Spawn-only posture (intake-locked)**: plugin **is** the OpenCode native chain — do **not** port US-0095; do **not** copy `.cursor/commands/auto.md` (AC-9). `/auto` is spawn-only: US-0069 phase→role, isolated child session, isolation evidence, US-0092 stop matrix, refuse orchestrator performing another role's writes. Headless uses US-0092 `--invoke-cmd`; native-chain-unavailable → `NATIVE_CHAIN_UNAVAILABLE` analogue. Plugin v1 vs v2 = R-0109 Q1 (LOCKED for /architecture as v2). Success tests (a)(d).
- **Discovery locks D1–D10**: D1 plugin location `template/.opencode/plugins/` (US-0121 reserved slot); D2 v1 vs v2 → v2 `Plugin.define` + `ctx.tool.hook("execute.before")` + `ctx.session.*` (R-0109 Q1, /architecture locks); D3 static + runtime isolation proof (`test_us0124_spawn_isolation_static` + `test_us0124_spawn_isolation_runtime`); D4 reason codes `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` / `OPENCODE_SUBTASK_IGNORED` / `OPENCODE_HEADLESS_UNSUPPORTED` + reuse `AUTO_ORCHESTRATOR_PHASE_EXECUTION` / `PHASE_ROLE_MISMATCH` / `NATIVE_CHAIN_UNAVAILABLE`; D5 subtask-ignored fail-closed (no one-chat multi-role per R-0001); D6 no Cursor auto.md clone (grep guard); D7 stop-matrix wiring (no TS reimplementation; calls `scripts/auto_outer_driver.py`); D8 headless `--invoke-cmd` (R-0109 Q3 /architecture lock; fail-closed `OPENCODE_HEADLESS_UNSUPPORTED`); D9 compose with US-0122 `auto.md` agent (agent=prompt layer, plugin=enforcement layer; plugin does not duplicate agent permission array); D10 `test_us0124_*` contract-test inventory (static + stub-harness, no live OpenCode probe).
- **Discovery question count**: 8. **Questions for `/research` / R-0109 (US-0124 subsection)**: DQ1 plugin entry-point shape + auto-load vs `plugins[]` in `opencode.json`; DQ2 spawn API surface (`ctx.session.create` vs `ctx.task` / `ctx.agent.spawn`) + signature; DQ3 stub-harness contract for runtime isolation proof; DQ4 reason-code namespace (new `OPENCODE_*` vs reuse) + canonical table location; DQ5 subtask-ignored detection signal (null/throw/identical-id); DQ6 stop-matrix integration (subprocess vs import vs stdio bridge); DQ7 headless CLI surface (which R-0109 Q3 candidate is /architecture-locked); DQ8 agent vs plugin ownership boundary (double-enforcement risk).
- **Compose guards**: US-0069/US-0092/US-0023/US-0048/BUG-0006 compose only; do **not** port US-0095; do **not** clone `.cursor/commands/auto.md`. US-0122 `auto.md` agent unchanged (plugin composes with agent — D9). US-0121 host default remains cursor-only until explicit `--host opencode|both`. US-0125 thin commands are Layer 3 (plugin must not own command bodies). No vendor slugs in `template/` (US-0102 family).
- **Isolation**: `phase_id=intake`, `role=po`, `model_id=glm-5.2-high`, `fresh_context_marker=po-US0124-intake-20260824T155500Z-fresh`; `phase_id=discovery`, `role=po`, `model_id=glm-5.2-high`, `fresh_context_marker=po-US0124-discovery-20260824T155800Z-fresh`; evidence refs: `docs/product/backlog.md ## US-0124`, `docs/product/vision.md ## Intake Notes — US-0124` + `## Discovery Notes — US-0124`, this handoff.
- **Status**: OPEN. **Next**: `/research` (tech-lead) to deepen **R-0109** for US-0124. `stop_condition=STOP after spec completes; hand off via artifacts only`.

