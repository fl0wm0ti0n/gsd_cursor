# State archive pack (2026-08-24)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 29
- First archived heading: `## QA checkpoint (loop-2 after harness-refresh) - US-0123 / S0123 / auto-20260824-01 (producer: dev / execute harness-refresh)`
- Last archived heading: `## QA checkpoint (loop-2 after harness-refresh) - US-0123 / S0123 / auto-20260824-01 (producer: dev / execute harness-refresh)`
- Verification tuple (mandatory):
  - archived_body_lines=39
  - preamble_lines=15
  - retained_body_lines=1200

---

## QA checkpoint (loop-2 after harness-refresh) - US-0123 / S0123 / auto-20260824-01 (producer: dev / execute harness-refresh)

- `orchestrator_run_id=auto-20260824-01`
- `phase_id=qa`
- `role=qa`
- `story_id=US-0123`
- `sprint_id=S0123`
- `producer_phase=execute` (harness-refresh - gate-1 for /release)
- `producer_role=dev`
- `producer_model_id=composer-2.5`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 - required on isolation)
- `verdict=PASS` (8/8 contract tests independent re-run; opencode-adapter parity; opencode-catalog validator; compose 6/6 UNCHANGED; byte-identical mirrors; ACs 10/10; tests/report.md @ 2026-08-24T15:12:17Z Pass:845 Fail:0 literal; zero [FAIL]; no fake browser PASS)
- `fresh_context_marker=qa-US0123-qa-20260824T151700Z-fresh-loop2`
- `timestamp=2026-08-24T15:17:00Z` (UTC)
- `producer_runtime_proof_id=rp-auto-20260824-01-execute-harness-refresh-dev-20260824T151230Z-US-0123` (`proof_hash=029BE6F670D2B17AD7B86D297EE68B09392A649B540FE2FEE2A2BA7E68B54979`)
- `independent_checks=pytest us0123_contract_test 8/8 PASS (0.21s exit 0); check_intake_template_parity --scope=opencode-adapter [INTAKE_TEMPLATE_PARITY_OK]; model_tier_validate --scope opencode-catalog [MODEL_TIER_VALIDATION_OK]; rg "^model:" template/.opencode/agents 0; tests/report.md L3 Timestamp 2026-08-24T15:12:17Z >= threshold; L5 Fail:0 literal; rg [FAIL] 0; L4 Pass:845; runbook SHA-256 66ee024a... active==template; manifest SHA-256 f7c1c09c... active==template; backlog L4248 OPEN; acceptance L151 unchecked; arch L1382 US-0123 anchor; DEC-0123 L3 Accepted; mirrors byte-identical`
- `open_blocking_findings=0` (1 non-blocking carry-forward: `ik_us0123_installer_hook_not_contract_tested`)
- `full_harness_claim=MADE` (report timestamp >= 2026-08-24T15:12:17Z threshold; Fail:0 literal; zero [FAIL])
- `browser_probe_used=false` (pack/contract story; no fake browser PASS)
- `status=OPEN` (do not mark US-0123 DONE)
- `next_scheduled_phase=/verify-work`
- `next_scheduled_role=qa` (fresh subagent per BUG-0006)
- `stop_condition=STOP after /qa loop-2. Hand off via artifacts only to /verify-work. Do not spawn /verify-work from qa. Do not mark US-0123 DONE.`

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`, `role=qa`, `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 - required)
- `fresh_context_marker=qa-US0123-qa-20260824T151700Z-fresh-loop2`, `timestamp=2026-08-24T15:17:00Z`
- `evidence_ref=sprints/S0123/qa-findings.md + handoffs/qa_to_verify.md + sprints/S0123/uat.json + sprints/S0123/uat.md + docs/engineering/state.md (this checkpoint append-bottom)`

### Strict runtime proof (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-qa-qa-20260824T151700Z-US-0123-loop2`
- `proof_hash=9CC32FD6A0EE8C0EDE3696E060BDBD8A8F19E914BFFBE51719E1A7B79704F107`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T16:17:00Z` (UTC)

---

