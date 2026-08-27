# PO to TL archive pack (2026-08-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 11
- First archived heading: `## Spec handoff — US-0129 Architecture hot-surface rollover linkage guard (intake RE-ATTEST + discovery)`
- Last archived heading: `## Spec handoff — US-0129 Architecture hot-surface rollover linkage guard (intake RE-ATTEST + discovery)`
- Verification tuple (mandatory):
  - archived_body_lines=17
  - retained_body_lines=650

---

## Spec handoff — US-0129 Architecture hot-surface rollover linkage guard (intake RE-ATTEST + discovery)

- **Phase completed**: spec (intake RE-ATTEST + `/discovery`). **Role**: po. **Story**: US-0129. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Orchestrator**: `auto-20260827-01`. **Delivery mode**: ultra_lean. **Prior run**: `auto-20260826-01` stopped `loop_max` after US-0130 ship; US-0127/US-0128/US-0130 DONE preserved.
- **Timestamps**: intake RE-ATTEST 2026-08-27T07:01:00Z; discovery 2026-08-27T07:02:00Z.
- **Fresh markers**: `po-US0129-intake-reattest-20260827T070100Z-fresh`, `po-US0129-discovery-20260827T070200Z-fresh`.
- **Runtime proofs** (DEC-0038 lowercase keys; prior intake proofs RUNTIME_PROOF_STALE — not forged):
  - intake RE-ATTEST: `rp-auto-20260827-01-intake-po-20260827T070100Z-US-0129` (`proof_hash=8821C91508F1BEBA91C754CC4868BCB3E08A0C51FE18939D8AF70C0F5A3F3E67`, ttl `2026-08-27T08:01:00Z`)
  - discovery: `rp-auto-20260827-01-discovery-po-20260827T070200Z-US-0129` (`proof_hash=0E0CBD2646F92DEF75D37C874AA2B3D0C2BE61C42150C721D3B61976ACF464EF`, ttl `2026-08-27T08:02:00Z`)
- **Intake RE-ATTEST**: `handoffs/intake_evidence/US-0129-intake-20260825.json` re-validated `[INTAKE_EVIDENCE_VALIDATION_OK]`; JSON **not mutated**; AC-1..AC-6 unchanged.
- **Current gap (locked)**: `rollover_architecture` archives oldest story blocks without guarding contract-test linkage; US-0126 B-1 Fail:7 when `# US-0090` / `# US-0091` / `# US-0093` archived while `tests/auto_command_contract_test.py` and readme-feature-coverage linkage tests grep active `architecture.md`.
- **Discovery locks D1–D10**: D1 `arch_linkage_guard.py` pre/post `--rollover`; D2 `ARCH_LINKAGE_ROLLOVER_BLOCKED` fail-closed metadata; D3 optional minimal H1 stub auto-repair from latest archive pack; D4 `/refresh-context` wiring; D5 US-0126 B-1 regression + harness marker; D6 `test_us0129_*`; D7 compose DEC-0054/DEC-0073/US-0049/US-0126 only; D8 template parity; D9 no PO architecture anchor; D10 no `ARCH_HOT_MAX_*` changes unless research proves.
- **Research routing**: DQ1..DQ8 → `/research` (tech-lead); expect **R-0113** (do not extend R-0112 US-0130).
- **Compose guards**: US-0126 B-1 fixture input only — do not reopen US-0126 product scope; US-0127/US-0128/US-0130 DONE not reopened; DEC-0054 triad archiver semantics unchanged; no `# US-0129` in architecture.md from PO.
- **Isolation**: `phase_id=intake|discovery`, `role=po`, `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1); evidence: `docs/product/backlog.md ## US-0129`, `docs/product/vision.md ## Discovery Notes — US-0129`, `docs/product/acceptance.md` L157 (unchecked).
- **Status**: OPEN. **Next**: `/research` (tech-lead, fresh subagent). `stop_condition=STOP after spec completes; hand off via artifacts only`.

