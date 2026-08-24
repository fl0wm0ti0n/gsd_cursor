# State archive pack (2026-08-24)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 28
- First archived heading: `## Sovereign-critic checkpoint — US-0123 / S0123 / auto-20260824-01 (producer: qa)`
- Last archived heading: `## Verify-work checkpoint — US-0123 / S0123 / auto-20260824-01 (role=qa; fresh per BUG-0006)`
- Verification tuple (mandatory):
  - archived_body_lines=80
  - preamble_lines=15
  - retained_body_lines=1157

---

## Sovereign-critic checkpoint — US-0123 / S0123 / auto-20260824-01 (producer: qa)

- **phase_id**: sovereign-critic, **role**: tech-lead (critic), **story_id**: US-0123, **sprint_id**: S0123
- `orchestrator_run_id=auto-20260824-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `producer_phase_id=qa`, `producer_role=qa`, `producer_model_id=glm-5.2-high`
- `critic_model_id=composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- `verdict=PASS` (independent checks green: critic re-ran pytest 8/8 PASS; parity + opencode-catalog validator PASS; backlog OPEN L4248; acceptance L151 unchecked; browser_probe_used=false; full-harness Fail:0 NOT falsely claimed — tests/report.md stale @ 13:02:49Z predates execute @ 14:48:00Z; 0 blocking findings; anti_slop_aggregate=8)
- `decision_gate=false`
- `status=OPEN` (do not mark US-0123 DONE)
- `fresh_context_marker=tl-US0123-sovereign-critic-qa-20260824T150000Z-fresh`
- `timestamp (UTC)=2026-08-24T15:00:00Z`
- `contract_tests=8/8 independently upheld` (tests/us0123_contract_test.py; critic re-run 0.22s exit 0)
- `critic_carry_ins_routed=1` (ik_us0123_installer_hook_not_contract_tested — non-blocking; T-003 hook not pytest-marked)
- `independent_checks=backlog US-0123 OPEN L4248; acceptance L151 unchecked; compose guards 6/6 UNCHANGED; sprints/S0123/uat.json browser_probe_used=false; uat.json full_harness_claim=none; check_intake_template_parity.py --scope=opencode-adapter PASS; model_tier_validate.py --scope opencode-catalog PASS`
- `producer_runtime_proof_ids=rp-auto-20260824-01-qa-qa-20260824T145500Z-US-0123 (proof_hash=6D35A32F5E471232B0750442E370047E536442C87F36692A67D811F87C08CDAD)`
- `evidence_ref=handoffs/sovereign_critic_findings.jsonl (US-0123 qa rows) + sprints/S0123/qa-findings.md + sprints/S0123/uat.json + sprints/S0123/uat.md + handoffs/qa_to_verify.md + docs/engineering/state.md (this checkpoint)`

### Next scheduled phase

- `next_scheduled_phase=/verify-work` (role=qa; fresh subagent per BUG-0006)
- `next_scheduled_role=qa`
- `stop_condition=STOP after sovereign-critic; orchestrator spawns /verify-work in fresh qa subagent (BUG-0006). Do NOT spawn /verify-work from sovereign-critic. Do NOT mark US-0123 DONE.`

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sovereign-critic`, `role=tech-lead`, `model_id=composer-2.5-fast` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=tl-US0123-sovereign-critic-qa-20260824T150000Z-fresh`, `timestamp=2026-08-24T15:00:00Z`
- `evidence_ref=handoffs/sovereign_critic_findings.jsonl (US-0123 qa rows) + docs/engineering/state.md (this checkpoint)`



---

## Verify-work checkpoint — US-0123 / S0123 / auto-20260824-01 (role=qa; fresh per BUG-0006)

- **phase_id**: verify-work, **role**: qa, **story_id**: US-0123, **sprint_id**: S0123
- `orchestrator_run_id=auto-20260824-01`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_model_id=composer-2.5-fast` (sovereign-critic phase)
- `producer_runtime_proof_id=rp-auto-20260824-01-qa-qa-20260824T145500Z-US-0123` (proof_hash=6D35A32F5E471232B0750442E370047E536442C87F36692A67D811F87C08CDAD; ttl 2026-08-24T15:55:00Z — consumed before expiry)
- `verdict=PASS` (10/10 ACs pass; 8/8 contract-test markers PASSED live re-run in 0.22s exit 0; opencode-adapter parity OK; opencode-catalog validator OK; compose 6/6 UNCHANGED; byte-identical mirrors; 0 blocking findings; no fake browser PASS)
- `decision_gate=false`
- `status=OPEN` (do not mark US-0123 DONE)
- `fresh_context_marker=qa-US0123-verify-work-20260824T150100Z-fresh` (NEW; distinct from prior qa-US0123-qa-20260824T145500Z-fresh)
- `timestamp (UTC)=2026-08-24T15:01:00Z`
- `blocking_findings=0`
- `non_blocking_findings=1` (carry-forward `ik_us0123_installer_hook_not_contract_tested` — non-blocking; T-003 hook not pytest-marked)
- `acceptance_row_unchecked=true` (docs/product/acceptance.md L151 — read-only)
- `compose_guards_unchanged=6/6` (backlog OPEN, acceptance unchecked, architecture anchor, DEC-0123 Accepted, template agents no `^model:`, byte-identical mirrors)
- `full_harness_claim=none` (tests/report.md @ 2026-08-24T13:02:49Z predates execute @ 2026-08-24T14:48:00Z — stale; no green claim)
- `release_harness_refresh_required=true` (/release gate-1 must re-run tests/run-tests.ps1 and refresh tests/report.md; orchestrator may insert execute harness-refresh first)
- `browser_probe_used=false` (pack/contract story — no web UI; static contract-test mapping justified per US-0092 / DEC-0078)
- `next_scheduled_phase=/release` (orchestrator may insert execute harness-refresh first)
- `next_scheduled_role=release`
- `stop_condition=STOP after verify-work. Hand off via artifacts only to /release. Do NOT spawn /release from this qa subagent. Do NOT mark US-0123 DONE.`

### Live evidence (verify-work re-run)

- `python -m pytest tests/us0123_contract_test.py -v` -> 8 passed in 0.22s (exit 0)
- `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` -> `[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`
- `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` -> `[MODEL_TIER_VALIDATION_OK]`

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=verify-work`, `role=qa`, `story_id=US-0123`, `sprint_id=S0123`
- `fresh_context_marker=qa-US0123-verify-work-20260824T150100Z-fresh` (NEW; not reused)
- `timestamp=2026-08-24T15:01:00Z` (UTC)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required; NEW fresh_context_marker per US-0048 — marker reuse = stale isolation evidence)
- `evidence_ref=sprints/S0123/verify-work-findings.md + sprints/S0123/uat.json + sprints/S0123/uat.md + handoffs/verify_to_release.md (US-0123 prepend) + docs/engineering/state.md (this verify-work checkpoint append-bottom)`
- QA verify-work subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward; no subagent spawned from this QA subagent.

### Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-verify-work-qa-20260824T150100Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"verify-work","proof_issued_at":"2026-08-24T15:01:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-verify-work-qa-20260824T150100Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`
- `proof_hash=E062CD6EDAA55EB02C96EF6101C5E21A39E1816BF9537AB129C7F71A8374A5E7` (SHA-256 of sorted-key JSON payload, UTF-8 bytes via python hashlib)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T16:01:00Z` (UTC = issued_at + 3600s)

---

