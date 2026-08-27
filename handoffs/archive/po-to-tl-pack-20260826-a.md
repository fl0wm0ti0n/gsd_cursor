# PO to TL archive pack (2026-08-26)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 11
- First archived heading: `## Spec handoff — US-0128 Convergence smoke surrogate (intake RE-ATTEST + discovery)`
- Last archived heading: `## Spec handoff — US-0128 Convergence smoke surrogate (intake RE-ATTEST + discovery)`
- Verification tuple (mandatory):
  - archived_body_lines=16
  - retained_body_lines=650

---

## Spec handoff — US-0128 Convergence smoke surrogate (intake RE-ATTEST + discovery)

- **Phase completed**: spec (intake RE-ATTEST + `/discovery`). **Role**: po. **Story**: US-0128. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Orchestrator**: `auto-20260826-01`. **Delivery mode**: ultra_lean. **Prior story**: US-0127 DONE / S0127 released.
- **Timestamps**: intake RE-ATTEST 2026-08-26T19:42:00Z; discovery 2026-08-26T19:43:00Z.
- **Fresh markers**: `po-US0128-intake-reattest-20260826T194200Z-fresh`, `po-US0128-discovery-20260826T194300Z-fresh`.
- **Runtime proofs** (DEC-0038 lowercase keys; prior `auto-20260825-01` proofs RUNTIME_PROOF_STALE — not forged):
  - intake RE-ATTEST: `rp-auto-20260826-01-intake-po-20260826T194200Z-US-0128` (`proof_hash=AEAC6B039E5EC857D1E8DB65F13F83A9CB9B5C4EA22B66C3059F3FD3966F4B56`, ttl `2026-08-26T20:42:00Z`)
  - discovery: `rp-auto-20260826-01-discovery-po-20260826T194300Z-US-0128` (`proof_hash=D4DDE4F258CB78A835B20D1AE01AA321B3576CD5A994FDCF77655ECD5307E335`, ttl `2026-08-26T20:43:00Z`)
- **Intake RE-ATTEST**: `handoffs/intake_evidence/US-0128-intake-20260825.json` re-validated `[INTAKE_EVIDENCE_VALIDATION_OK]`; `candidate_id=938c6987-27f9-4a9c-af48-920c908968bf`; JSON **not mutated**; AC-1..AC-6 unchanged.
- **Discovery locks D1–D10**: D1 `_eval_smoke_green` surrogate for waived-probe + green harness; D2 `convergence_smoke` uat step (or `contract_tests_primary` tail); D3 `CONVERGENCE_SMOKE_SURROGATE_MISSING` fail-closed; D4 `/qa` + `/verify-work` contracts; D5 `test_us0128_*`; D6 runbook; D7 `SOVEREIGN_CONVERGENCE_PAIRS`; D8–D10 compose US-0109/US-0126/US-0110/US-0127 read-only.
- **Research routing**: DQ1..DQ8 → `/research` (tech-lead); expect **R-0111** (do not extend R-0110 US-0127).
- **Compose guards**: US-0109 deploy smoke unchanged; US-0126 DONE not reopened; US-0127 DONE not amended; US-0129/US-0130 untouched; no fake browser PASS; no `# US-0128` in architecture.md from PO.
- **Isolation**: `phase_id=intake|discovery`, `role=po`, `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1); evidence: `docs/product/backlog.md ## US-0128`, `docs/product/vision.md ## Discovery Notes — US-0128`, `docs/product/acceptance.md` L156 (unchecked).
- **Status**: OPEN. **Next**: `/research` (tech-lead, fresh subagent). `stop_condition=STOP after spec completes; hand off via artifacts only`.

