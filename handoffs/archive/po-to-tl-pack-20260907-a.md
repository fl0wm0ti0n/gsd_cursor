# PO to TL archive pack (2026-09-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Architecture handoff — BUG-0016 OpenCode Layer-1 permissions vs kit duties`
- Last archived heading: `## Architecture handoff — BUG-0016 OpenCode Layer-1 permissions vs kit duties`
- Verification tuple (mandatory):
  - archived_body_lines=14
  - retained_body_lines=647

---

## Architecture handoff — BUG-0016 OpenCode Layer-1 permissions vs kit duties

- **Phase completed**: architecture. **Role**: tech-lead. **Bug**: BUG-0016 only. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp (UTC)**: 2026-09-06T18:45:00Z. **Fresh marker**: `tl-BUG0016-architecture-20260906T184500Z-fresh`.
- **Orchestrator**: `orchestrator_run_id=auto-20260906-bug0016`, `delivery_mode=ultra_lean`, macro=`plan`.
- **Architecture anchor**: `docs/engineering/architecture.md` `# BUG-0016` (H1; `baseline_h2_count=0`).
- **Approach A\*** LOCKED: amend **DEC-0122 §2** sole SOT + agent frontmatter (active+template) — bash ask for po/tl/curator; PO +intake_evidence/** +resume_brief +state.md; `sprints/S*/` globs; release duty paths; 7 `test_bug0016_*`; success test (c) preserved. Companion DEC: **none**.
- **DEC**: `decisions/DEC-0122.md` §2 amended in THIS phase (R-0115 DQ6). DEC-0130 rejected.
- **Seeds for `/sprint-plan`**: T-anch + T-001..T-007 (8; under SPRINT_MAX_TASKS=12).
- **Runtime proof**: `rp-auto-20260906-bug0016-architecture-techlead-20260906T184500Z-BUG-0016` / `proof_hash=7AC851CDF1953594365AFF11B015BFD850E737F75A327FA2A02B1CCB544D5A31` / ttl `2026-09-06T19:45:00Z`.
- **Status**: BUG-0016 remains **OPEN**. **Next**: `/sprint-plan` in fresh tech-lead subagent. Do not spawn sprint-plan from this architecture chat. STOP.

---

