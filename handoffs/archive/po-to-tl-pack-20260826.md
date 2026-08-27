# PO to TL archive pack (2026-08-26)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 11
- First archived heading: `## Intake handoff — US-0130 operator-pinned sovereign-critic model`
- Last archived heading: `## Intake handoff — US-0130 operator-pinned sovereign-critic model`
- Verification tuple (mandatory):
  - archived_body_lines=13
  - retained_body_lines=650

---

## Intake handoff — US-0130 operator-pinned sovereign-critic model

- **Phase completed**: intake. **Role**: po. **Story**: US-0130. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-08-26T18:00:00Z. **Fresh marker**: `po-US0130-intake-20260826T180000Z-fresh`.
- **Evidence**: `handoffs/intake_evidence/US-0130-intake-20260826.json` — `[INTAKE_EVIDENCE_VALIDATION_OK]`; `selected_pack=small-intake-pack`; `missing_topics=[]`.
- **Writer**: `writer_id=po-cursor-20260826-US0130`, `intake_run_id=cursor-20260826-US0130-intake`.
- **Ask**: Pin which model `/sovereign-critic` uses, like v2 role catalog slugs.
- **Operator choices**: both_precedence; degraded_keep; one_global; plus_installer.
- **ACs**: 9 unchecked in backlog + acceptance. **Status**: OPEN (US-0045).
- **Compose do not amend**: US-0104 findings/lenses/`CROSS_MODEL_*` keys; US-0101 matrix; US-0102 canonical-phase chain; US-0112 active-catalog protection; US-0127 orthogonal.
- **Isolation**: `phase_id=intake`; `role=po`; `fresh_context_marker=po-US0130-intake-20260826T180000Z-fresh`; `timestamp=2026-08-26T18:00:00Z`; `evidence_ref=docs/product/backlog.md ## US-0130 + docs/product/acceptance.md US-0130 + this handoff`.
- **Next**: `/discovery` (fresh **po**) for **US-0130**. Do not add `# US-0130` to architecture.md from intake. In-flight **US-0127** resume is unchanged.

