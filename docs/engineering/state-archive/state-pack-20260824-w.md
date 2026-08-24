# State archive pack (2026-08-24)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 28
- First archived heading: `## QA checkpoint — US-0123 / S0123 / auto-20260824-01`
- Last archived heading: `## QA checkpoint — US-0123 / S0123 / auto-20260824-01`
- Verification tuple (mandatory):
  - archived_body_lines=49
  - preamble_lines=15
  - retained_body_lines=1170

---

## QA checkpoint — US-0123 / S0123 / auto-20260824-01

- **phase_id**: qa
- **role**: qa (fresh per BUG-0006)
- **story_id**: US-0123
- **sprint_id**: S0123
- **orchestrator_run_id**: auto-20260824-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **verdict**: PASS (8/8 contract tests independent re-run + opencode-adapter parity + opencode-catalog validator + compose 6/6 UNCHANGED + byte-identical mirrors + ACs 10/10 covered + UAT probes static-contract mapped + no fake browser PASS)
- **fresh_context_marker**: qa-US0123-qa-20260824T145500Z-fresh
- **timestamp (UTC)**: 2026-08-24T14:55:00Z
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required on isolation; **NEW** fresh_context_marker per US-0048)
- **producer_model_id**: composer-2.5 (execute dev)
- **producer_runtime_proof_id**: rp-auto-20260824-01-execute-dev-20260824T144800Z-US-0123
- **producer_proof_hash**: 3579702AE6A0305460FE137BB73B612C12DA88B57F6D8A32D109E7895F07BEB5
- **producer_proof_ttl**: 2026-08-24T15:48:00Z (consumed before expiry — OK)
- **evidence_ref**: sprints/S0123/qa-findings.md, handoffs/qa_to_verify.md, sprints/S0123/uat.json, sprints/S0123/uat.md
- **story_status**: OPEN (not marked DONE — US-0045; closure owns the flip)
- **acceptance_row_unchecked**: true (docs/product/acceptance.md L151 — read-only)
- **blocking_findings**: 0
- **non_blocking_findings**: 1 (carry-forward `ik_us0123_installer_hook_not_contract_tested` — non-blocking)
- **compose_guards_unchanged**: 6/6 (backlog OPEN L4248, acceptance unchecked L151, architecture anchor L1703, DEC-0123 Accepted L4, template agents no `^model:`, byte-identical mirrors)
- **full_harness_claim**: none (tests/report.md @ 2026-08-24T13:02:49Z predates execute @ 2026-08-24T14:48:00Z — stale; no green claim)
- **browser_probe_used**: false (pack/contract story — no web UI; static contract-test mapping justified per US-0092 / DEC-0078)
- **next_scheduled_phase**: /verify-work (fresh qa subagent per BUG-0006)
- **stop_condition**: STOP after /qa. Hand off via artifacts only to /verify-work.

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`
- `role=qa`
- `story_id=US-0123`
- `sprint_id=S0123`
- `fresh_context_marker=qa-US0123-qa-20260824T145500Z-fresh`
- `timestamp=2026-08-24T14:55:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation; **NEW** fresh_context_marker — marker reuse = stale isolation evidence)
- `evidence_ref=sprints/S0123/qa-findings.md, handoffs/qa_to_verify.md, sprints/S0123/uat.json, sprints/S0123/uat.md, docs/engineering/state.md (this qa checkpoint append-bottom)`

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-qa-qa-20260824T145500Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"qa","proof_issued_at":"2026-08-24T14:55:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-qa-qa-20260824T145500Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`
- `proof_hash=6D35A32F5E471232B0750442E370047E536442C87F36692A67D811F87C08CDAD`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T15:55:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

---

