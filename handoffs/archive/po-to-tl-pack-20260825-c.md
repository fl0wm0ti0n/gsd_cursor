# PO to TL archive pack (2026-08-25)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 11
- First archived heading: `## Spec handoff — US-0127 Convergence critic conjunct blocking-only + auto-resolve`
- Last archived heading: `## Spec handoff — US-0127 Convergence critic conjunct blocking-only + auto-resolve`
- Verification tuple (mandatory):
  - archived_body_lines=13
  - retained_body_lines=650

---

## Spec handoff — US-0127 Convergence critic conjunct blocking-only + auto-resolve

- **Phase completed**: discovery. **Role**: po. **Story**: US-0127. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-08-25T18:27:31Z. **Fresh context marker**: `po-US0127-discovery-20260825T182731Z-fresh`.
- **Runtime proof**: `rp-auto-20260825-01-discovery-po-20260825T182731Z-US-0127` (`proof_hash=649D169D12BFDDDE4F2071BB0B1048A558E890B85C14C2B1042E13CB6469B981`, ttl 2026-08-25T19:27:31Z, `hash_recompute_confirmation=true`).
- **Canonical payload**: `{"delivery_mode":"ultra_lean","macro_phase":"spec","model_id":"composer-2.5","orchestrator_run_id":"auto-20260825-01","phase_id":"discovery","proof_issued_at":"2026-08-25T18:27:31Z","proof_ttl_seconds":3600,"role":"po","runtime_proof_id":"rp-auto-20260825-01-discovery-po-20260825T182731Z-US-0127","sprint_id":"pending","story_id":"US-0127"}`
- **Intake producer proof** (consumed): `rp-auto-20260825-01-intake-po-20260825T182030Z-US-0127` (`proof_hash=7C37D25CBCD5494B16AFC39478ED7E73A8CABFBF351034E9C14AAEE386B87134`, ttl 2026-08-25T19:20:30Z).
- **Discovery locks D1–D10**: D1 replace `_critic_jsonl_has_open` with `read_open_blocking` semantics in `sovereign_convergence_lib.py`; D2 auto-resolve non-blocking at sovereign-critic PASS (idempotent); D3 `scripts/sovereign_critic_hygiene.py` CLI; D4 `test_us0127_*` contract tests; D5 runbook + reason codes; D6 `SOVEREIGN_CRITIC_PAIRS` extension; D7 QA fallback degrade matrix; D8–D10 compose read-only US-0104/US-0110/US-0107.
- **Discovery question count**: 8. **Questions for `/research`** (research owns R-id; do not extend R-0109 OpenCode epic): DQ1 auto-resolve scope key; DQ2 hygiene reason codes; DQ3 `test_us0127_*` inventory; DQ4 runbook section anchor; DQ5 parity pair rows; DQ6 hook placement; DQ7 QA fallback alignment; DQ8 batch resolve/idempotency.
- **Compose guards**: US-0104/US-0110/US-0107 read-only; US-0128/US-0129 siblings unchanged; US-0108/US-0121..US-0126 DONE preserved.
- **Isolation**: `phase_id=discovery`, `role=po`, `model_id=composer-2.5`, `fresh_context_marker=po-US0127-discovery-20260825T182731Z-fresh`; evidence refs: `docs/product/backlog.md ## US-0127`, `docs/product/vision.md ## Discovery Notes — US-0127`, this handoff.
- **Status**: OPEN. **Next**: `/research` (tech-lead). `stop_condition=STOP after discovery completes; hand off via artifacts only`.

