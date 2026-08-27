# Sprint S0130 — UAT (US-0130) — populated at /qa (DEC-0009)

- **uat_lifecycle**: populated (QA pass; `/verify-work` may re-attest)
- **sprint_id**: S0130
- **story_refs**: US-0130
- **phase**: qa (build+verify macro)
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260826-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **story_type**: code (scripts/docs/examples/contract-test slice; FRAMEWORK_KIT_REPO=1)
- **fresh_context_marker**: `qa-US0130-qa-20260826T222300Z-fresh`
- **timestamp**: 2026-08-26T22:23:00Z (UTC)
- **model_id**: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required)
- **verdict**: PASS
- **total_steps**: 10 (UAT-1..UAT-9 + canonical `convergence_smoke`)
- **passed**: 10 | **failed**: 0
- **story_status**: OPEN (do not mark US-0130 DONE — US-0045; acceptance L158 unchecked; intake JSON not mutated)
- **blocking_count**: 0

## Probe class — scripts/docs/examples/contract-test slice

US-0130 is a code+docs+examples+parity+contract-test slice. Applicable probe: `contract_tests_primary` (10 markers). No `browser_smoke`. Six live-runtime classes waived with `UAT_PROBE_FORBIDDEN`. No fake browser PASS. Live-runtime probes were not attempted.

Canonical surrogate step `id=convergence_smoke` emitted because `contract_test_failed=0` (10/10 pytest).

## Target stories + acceptance criteria

- **US-0130** — Operator-pinned sovereign-critic model (catalog role + scratchpad override) (9 ACs)
  - AC-1: PASS — Scratchpad pin `MODEL_SOVEREIGN-CRITIC=<slug>` (hyphen exact; highest precedence) (markers 1, 6)
  - AC-2: PASS — Catalog `roles.critic` optional additive v2 role (markers 2, 3, 7, 8)
  - AC-3: PASS — `select_critic_model` precedence pin > `roles.critic` (when `role_catalog`) > opposition/`dev` (markers 1, 2, 3, 6)
  - AC-4: PASS — Same-slug keeps `CROSS_MODEL_DEGRADED_MODE` (marker 4)
  - AC-5: PASS — One global critic (marker 8 + overlay shape)
  - AC-6: PASS — `test_us0130_*` 10 markers (all 10)
  - AC-7: PASS — Compose do not amend US-0104 findings schema / US-0101 matrix / US-0102 5-step chain (marker 5 + us0104 10/10)
  - AC-8: PASS — Examples + installer (cursor_only 9th; never write `model-catalog.local.json`) (markers 9, 10)
  - AC-9: PASS — Docs + parity (scratchpad comments, runbook, template pairs) (parity CLI both scopes)

## Contract test markers (10) — live QA re-run

`python -m pytest tests/us0130_contract_test.py -v` — **10 passed** in 0.06s.

## UAT step results

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | pass | hyphen pin comment + overlay consume; markers 1, 6 |
| UAT-2 | AC-2 | pass | optional `roles.critic`; markers 2, 3, 7, 8 |
| UAT-3 | AC-3 | pass | `_overlay_critic_slug` pin > catalog > opposition; markers 1, 2, 3, 6 |
| UAT-4 | AC-4 | pass | same-slug `degraded=True`; marker 4 |
| UAT-5 | AC-5 | pass | one global overlay; marker 8 |
| UAT-6 | AC-6 | pass | 10/10 `test_us0130_*` |
| UAT-7 | AC-7 | pass | marker 5; us0104 10/10 |
| UAT-8 | AC-8 | pass | markers 9, 10; local.json absent |
| UAT-9 | AC-9 | pass | runbook pin-precedence; both parity scopes OK |
| convergence_smoke | surrogate | pass | `contract_test_failed=0`; 6 waived probes |

## Waived probes

| Probe | reason_code |
|-------|-------------|
| browser_smoke | `UAT_PROBE_FORBIDDEN` (scripts/docs/examples/contract-test slice; FRAMEWORK_KIT_REPO=1) |
| api_health | `UAT_PROBE_FORBIDDEN` (no runtime API) |
| process_health | `UAT_PROBE_FORBIDDEN` (no runtime process/app server) |
| cli_smoke | `UAT_PROBE_FORBIDDEN` (lib + examples verified via contract tests) |
| build | `UAT_PROBE_FORBIDDEN` (no build step) |
| manual_operator | `UAT_PROBE_FORBIDDEN` (docs + contract tests; no live operator action) |

## Results summary

- **Total**: 10 steps
- **Passed**: 10
- **Failed**: 0
- **Verdict**: PASS
- **Blocking QA findings**: 0
- **Non-blocking**: NB-1 informational (`tests/report.md` timestamp `2026-08-26T20:57:42Z` precedes execute; full harness not re-run this pass)

## Producer proof consumed (execute)

- `runtime_proof_id=rp-auto-20260826-01-execute-dev-20260826T221420Z-US-0130`
- Independent SHA-256 MATCH `089947FF99F92DF799FA3FD51A10E503B3DF26052833DE33EC7942ED7C59DA9C`
- `proof_ttl=2026-08-26T23:14:20Z`; consumed_at `2026-08-26T22:23:00Z`

## Runtime proof (DEC-0038) — qa

- `runtime_proof_id=rp-auto-20260826-01-qa-qa-20260826T222300Z-US-0130`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"qa","proof_issued_at":"2026-08-26T22:23:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260826-01-qa-qa-20260826T222300Z-US-0130","sprint_id":"S0130","story_id":"US-0130"}`
- `proof_hash=7DCD83D45E1188B5102B46BCDE05EB43CC2A052EAF430647604C5B7BB3A46557`
- `proof_ttl=2026-08-26T23:23:00Z`

## Isolation evidence

- `phase_id=qa`, `role=qa`, `fresh_context_marker=qa-US0130-qa-20260826T222300Z-fresh`
- `timestamp=2026-08-26T22:23:00Z`
- `evidence_ref=sprints/S0130/qa-findings.md`

## Next (qa pass — historical)

`/verify-work` (orchestrator-owned fresh qa subagent). Do not spawn `/verify-work` from this subagent. Do not mark US-0130 DONE. Do not tick acceptance L158.

---

# Sprint S0130 — UAT verify-work (US-0130) — PASS

- **sprint_id**: S0130
- **story_refs**: US-0130
- **phase**: verify-work (build+verify macro)
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260826-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **story_type**: code (scripts/docs/examples/contract-test slice; FRAMEWORK_KIT_REPO=1)
- **uat_lifecycle**: populated (DEC-0009)
- **fresh_context_marker**: `qa-US0130-verify-work-20260826T223136Z-fresh`
- **timestamp**: 2026-08-26T22:31:36Z (UTC)
- **model_id**: cursor-grok-4.6-high (CROSS_MODEL_REVIEW=1 — required)
- **producer_phase_id**: qa (role=qa, cursor-grok-4.6-high; **QA_PASS**; `blocking_count=0`)
- **critic_phase_id**: sovereign-critic of qa (tech-lead, composer-2.5-fast; PASS; anti_slop=10; 0 blocking `a0130qa-*`; marker `tl-US0130-sovereign-critic-qa-20260826T223000Z-fresh`)
- **verdict**: **PASS** (verify-work) — UAT 10/10 pass, 0 fail (AC-1..AC-9 → UAT-1..UAT-9 + canonical `convergence_smoke`); live `pytest tests/us0130_contract_test.py -v` → **10 passed in 0.06s**; isolation execute+qa+verify-work present
- **story_status**: OPEN (do not mark US-0130 DONE — US-0045; acceptance L158 unchecked; intake JSON not mutated)
- **blocking_findings**: 0
- **non_blocking_findings**: 1 (NB-1 informational: `tests/report.md` timestamp `2026-08-26T20:57:42Z` precedes execute — carried from qa)
- **harness_fail_zero_claimed**: false (`tests/report.md` Timestamp `2026-08-26T20:57:42Z` is stale vs execute `2026-08-26T22:14:20Z`; FRAMEWORK_KIT_REPO=1 slice tests are the required evidence)
- **local_catalog_not_written**: true (`.cursor/model-catalog.local.json` absent)

## Probe class — scripts/docs/examples/contract-test slice

Applicable probe: `contract_tests_primary` (10 markers). No web UI. Six live-runtime classes waived with **`UAT_PROBE_FORBIDDEN`**: `browser_smoke`, `api_health`, `process_health`, `cli_smoke`, `build`, `manual_operator`. **No silent browser PASS.** MCP browser sequence not run. No screenshot. Live-runtime probes were not attempted.

Canonical surrogate step `id=convergence_smoke` kept `result=pass` because `contract_test_failed=0` (10/10 pytest).

## Target stories + acceptance criteria

- **US-0130** — Operator-pinned sovereign-critic model (catalog role + scratchpad override) (9 ACs)
  - AC-1: PASS — Scratchpad pin `MODEL_SOVEREIGN-CRITIC=<slug>` (hyphen exact; highest precedence) (UAT-1; markers 1, 6)
  - AC-2: PASS — Catalog `roles.critic` optional additive v2 role (UAT-2; markers 2, 3, 7, 8)
  - AC-3: PASS — `select_critic_model` precedence pin > `roles.critic` (when `role_catalog`) > opposition/`dev` (UAT-3; markers 1, 2, 3, 6)
  - AC-4: PASS — Same-slug keeps `CROSS_MODEL_DEGRADED_MODE` (UAT-4; marker 4)
  - AC-5: PASS — One global critic (UAT-5; marker 8 + overlay shape)
  - AC-6: PASS — `test_us0130_*` 10 markers (UAT-6; live re-run 10 passed in 0.06s)
  - AC-7: PASS — Compose do not amend US-0104 findings schema / US-0101 matrix / US-0102 5-step chain (UAT-7; marker 5 + us0104 10/10)
  - AC-8: PASS — Examples + installer (cursor_only 9th; never write `model-catalog.local.json`) (UAT-8; markers 9, 10)
  - AC-9: PASS — Docs + parity (scratchpad comments, runbook, template pairs) (UAT-9; both parity scopes)

## UAT step results (verify-work)

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | pass | hyphen pin comment + overlay consume; markers 1, 6 |
| UAT-2 | AC-2 | pass | optional `roles.critic`; markers 2, 3, 7, 8 |
| UAT-3 | AC-3 | pass | `_overlay_critic_slug` pin > catalog > opposition; markers 1, 2, 3, 6 |
| UAT-4 | AC-4 | pass | same-slug `degraded=True`; marker 4 |
| UAT-5 | AC-5 | pass | one global overlay; marker 8 |
| UAT-6 | AC-6 | pass | 10/10 `test_us0130_*` — live `10 passed in 0.06s` |
| UAT-7 | AC-7 | pass | marker 5; us0104 10/10 |
| UAT-8 | AC-8 | pass | markers 9, 10; local.json absent |
| UAT-9 | AC-9 | pass | runbook pin-precedence; both parity scopes OK |
| convergence_smoke | surrogate | pass | `contract_test_failed=0`; 6 waived probes `UAT_PROBE_FORBIDDEN` |

## Waived probes (honest live-runtime)

| Probe | reason_code |
|-------|-------------|
| browser_smoke | `UAT_PROBE_FORBIDDEN` (scripts/docs/examples/contract-test slice; FRAMEWORK_KIT_REPO=1) |
| api_health | `UAT_PROBE_FORBIDDEN` (no runtime API) |
| process_health | `UAT_PROBE_FORBIDDEN` (no runtime process/app server) |
| cli_smoke | `UAT_PROBE_FORBIDDEN` (lib + examples verified via contract tests) |
| build | `UAT_PROBE_FORBIDDEN` (no build step) |
| manual_operator | `UAT_PROBE_FORBIDDEN` (docs + contract tests; no live operator action) |

## Results summary

- **Total**: 10 steps
- **Passed**: 10
- **Failed**: 0
- **Verdict**: PASS
- **Blocking QA findings**: 0 (`sprints/S0130/qa-findings.md` verdict QA_PASS)

## Live contract-test evidence (verify-work)

`python -m pytest tests/us0130_contract_test.py -v` → **10 passed in 0.06s** (2026-08-26T22:31:36Z)

## Isolation compliance (US-0048 / DEC-0029)

| Phase | Marker | Present |
|-------|--------|---------|
| execute | `dev-US0130-execute-20260826T221420Z-fresh` | yes |
| qa | `qa-US0130-qa-20260826T222300Z-fresh` | yes |
| verify-work | `qa-US0130-verify-work-20260826T223136Z-fresh` | yes (this phase) |

## Producer proof consumed (qa)

- `runtime_proof_id=rp-auto-20260826-01-qa-qa-20260826T222300Z-US-0130`
- Independent SHA-256 MATCH `7DCD83D45E1188B5102B46BCDE05EB43CC2A052EAF430647604C5B7BB3A46557`
- `proof_ttl=2026-08-26T23:23:00Z`; consumed_at `2026-08-26T22:31:36Z` (before RUNTIME_PROOF_STALE)

## Runtime proof (DEC-0038) — verify-work

- `runtime_proof_id=rp-auto-20260826-01-verify-work-qa-20260826T223136Z-US-0130`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"cursor-grok-4.6-high","orchestrator_run_id":"auto-20260826-01","phase_id":"verify-work","proof_issued_at":"2026-08-26T22:31:36Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260826-01-verify-work-qa-20260826T223136Z-US-0130","sprint_id":"S0130","story_id":"US-0130"}`
- `proof_hash=8CE4D169132A04FA3FCB84281F0F67B5D8A2C36B019A7B8E092DFC5C639CC1E1`
- `proof_issued_at=2026-08-26T22:31:36Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-26T23:31:36Z`

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2) — verify-work

- `phase_id=verify-work`, `role=qa`, `model_id=cursor-grok-4.6-high` (CROSS_MODEL_REVIEW=1 — required)
- `fresh_context_marker=qa-US0130-verify-work-20260826T223136Z-fresh` (NEW per US-0048 / BUG-0006)
- `timestamp=2026-08-26T22:31:36Z` (UTC)
- `evidence_ref=sprints/S0130/uat.json + sprints/S0130/uat.md`

## Next scheduled phase

- `/release` (role=release; orchestrator-owned fresh subagent per BUG-0006; after sovereign-critic of verify-work if CROSS_MODEL_REVIEW=1)
- STOP after verify-work PASS. Do NOT spawn `/release` from this subagent. Do NOT mark US-0130 DONE. Do NOT tick acceptance L158. Do NOT mutate intake JSON. Do NOT mutate US-0129. Do NOT write `model-catalog.local.json`.
