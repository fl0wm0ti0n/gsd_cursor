# PO to TL archive pack (2026-08-26)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 11
- First archived heading: `## Spec handoff — US-0130 Operator-pinned sovereign-critic model (intake RE-ATTEST + discovery)`
- Last archived heading: `## Spec handoff — US-0130 Operator-pinned sovereign-critic model (intake RE-ATTEST + discovery)`
- Verification tuple (mandatory):
  - archived_body_lines=17
  - retained_body_lines=650

---

## Spec handoff — US-0130 Operator-pinned sovereign-critic model (intake RE-ATTEST + discovery)

- **Phase completed**: spec (intake RE-ATTEST + `/discovery`). **Role**: po. **Story**: US-0130. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Orchestrator**: `auto-20260826-01`. **Delivery mode**: ultra_lean. **Prior story**: US-0128 DONE / S0128 released (drain-advance).
- **Timestamps**: intake RE-ATTEST 2026-08-26T21:22:00Z; discovery 2026-08-26T21:23:00Z.
- **Fresh markers**: `po-US0130-intake-reattest-20260826T212200Z-fresh`, `po-US0130-discovery-20260826T212300Z-fresh`.
- **Runtime proofs** (DEC-0038 lowercase keys; prior intake proofs RUNTIME_PROOF_STALE — not forged):
  - intake RE-ATTEST: `rp-auto-20260826-01-intake-po-20260826T212200Z-US-0130` (`proof_hash=A2584FDA224EF9E03B23601D19085A7F36CAD9440EC88F3E85350E441241B4C3`, ttl `2026-08-26T22:22:00Z`)
  - discovery: `rp-auto-20260826-01-discovery-po-20260826T212300Z-US-0130` (`proof_hash=FA8F130C5E4BA56665955E2DAD008998F68359FC3726492D8371CD29472D3821`, ttl `2026-08-26T22:23:00Z`)
- **Intake RE-ATTEST**: `handoffs/intake_evidence/US-0130-intake-20260826.json` re-validated `[INTAKE_EVIDENCE_VALIDATION_OK]`; JSON **not mutated**; AC-1..AC-9 unchanged; operator locks **both_precedence**, **degraded_keep**, **one_global**, **plus_installer**.
- **Current gap (locked)**: `select_critic_model` uses tier opposition on `sovereign-critic` and ignores `MODEL_SOVEREIGN-CRITIC` / `roles.critic`; `CATALOG_ROLE_KEYS` has no `critic`.
- **Discovery locks D1–D10**: D1 `MODEL_SOVEREIGN-CRITIC` scratchpad pin; D2 optional `roles.critic`; D3 precedence overlay in `select_critic_model`; D4 same-slug `CROSS_MODEL_DEGRADED_MODE`; D5 one global critic; D6 `test_us0130_*`; D7 compose US-0104/US-0101/US-0102 unchanged; D8 US-0112 example/installer `critic` key; D9 docs/parity (no PO architecture anchor); D10 compose US-0127/US-0128 DONE, US-0129 out, R-0088 doc-only.
- **Research routing**: DQ1..DQ8 → `/research` (tech-lead); expect **R-0112** (do not extend R-0111 US-0128).
- **Compose guards**: US-0104 findings JSONL / lenses / `CROSS_MODEL_*` keys unchanged; US-0127/US-0128 DONE not reopened; US-0129 untouched; no `model-catalog.local.json` writes; no `# US-0130` in architecture.md from PO.
- **Isolation**: `phase_id=intake|discovery`, `role=po`, `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1); evidence: `docs/product/backlog.md ## US-0130`, `docs/product/vision.md ## Discovery Notes — US-0130`, `docs/product/acceptance.md` L158 (unchecked).
- **Status**: OPEN. **Next**: `/research` (tech-lead, fresh subagent). `stop_condition=STOP after spec completes; hand off via artifacts only`.

