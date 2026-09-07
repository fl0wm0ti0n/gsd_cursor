# Sprint S0133 — UAT (US-0131) — populated at /verify-work (DEC-0009)

- **uat_lifecycle**: populated (verify-work PASS; DEC-0009 placeholder → populated complete)
- **sprint_id**: S0133
- **story_id**: US-0131
- **phase**: verify-work (build+verify macro)
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260907-us0131
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **story_type**: code (scripts/docs/examples/contract-test slice; FRAMEWORK_KIT_REPO=1)
- **fresh_context_marker**: `qa-US0131-verify-work-20260907T204621Z-fresh`
- **timestamp**: 2026-09-07T20:46:21Z (UTC)
- **model_id**: composer-2.5 (CROSS_MODEL_REVIEW=1 — required)
- **producer_phase_id**: qa (role=qa; **QA_PASS** re-run; `blocking_count=0`; B-1 CLOSED)
- **critic_phase_id**: sovereign-critic of qa re-run (tech-lead, composer-2.5-fast; PASS; anti_slop=10; marker `critic-US0131-qa-rerun-20260907T204015Z-fresh`)
- **verdict**: **PASS** (verify-work) — UAT 9/9 pass, 0 fail (AC-1..AC-8 → UAT-1..UAT-8 + canonical `convergence_smoke`); live `pytest tests/us0131_contract_test.py -v` → **10 passed in 0.11s**; isolation execute+qa+verify-work present
- **total_steps**: 9 (UAT-1..UAT-8 + canonical `convergence_smoke`)
- **passed**: 9 | **failed**: 0
- **story_status**: OPEN (do not mark US-0131 DONE — US-0045 / US-0120; acceptance L159 unchecked; intake JSON not mutated)
- **blocking_findings**: 0
- **non_blocking_findings**: 3 (NB-1..NB-3 carry-forwards — informational)
- **harness_fail_zero_claimed**: false (slice contract tests are the required evidence)
- **browser_probe_used**: false (no fake browser PASS)

## Probe class — cross-host runtime config contract

US-0131 is a host-neutral config / shared-kernel / installer contract-test slice. Applicable probe: `contract_tests_primary` (10 markers). No web UI. Six live-runtime classes waived with **`UAT_PROBE_FORBIDDEN`**: `browser_smoke`, `api_health`, `process_health`, `cli_smoke`, `build`, `manual_operator`. **No silent browser PASS.** MCP browser sequence not run.

Canonical surrogate step `id=convergence_smoke` kept `result=pass` because `contract_test_failed=0` (10/10 pytest) and metadata guard exit 0.

## Target story + acceptance criteria

**US-0131** — Cross-host Its-Magic runtime configuration and parity (Status OPEN — checkboxes remain unchecked; `/closure` owns DONE + acceptance ticks per US-0120)

- [ ] AC-1: Host-neutral typed config contract (no credentials/secrets) — **PASS** (UAT-1; markers 1,6)
- [ ] AC-2: Cursor scratchpad compatibility adapter — **PASS** (UAT-2; marker 2)
- [ ] AC-3: OpenCode-only resolves shared settings without `.cursor/scratchpad*` — **PASS** (UAT-3; marker 3)
- [ ] AC-4: Shared-kernel scripts accept resolved config explicitly — **PASS** (UAT-4; marker 8)
- [ ] AC-5: Host-specific capabilities classified; fail/skip deterministically — **PASS** (UAT-5; marker 10)
- [ ] AC-6: `--host both` deterministic precedence — **PASS** (UAT-6; markers 4,5)
- [ ] AC-7: Installer delivers examples; preserves locals — **PASS** (UAT-7; marker 7; B-1 metadata closed)
- [ ] AC-8: Cross-host contract tests + docs — **PASS** (UAT-8; 10/10 + runbook h2)

## UAT step results (verify-work)

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | pass | `test_us0131_neutral_path_no_cursor_required` (+ schema fail-closed m6) |
| UAT-2 | AC-2 | pass | `test_us0131_cursor_adapter_preserves_dec0055_precedence` |
| UAT-3 | AC-3 | pass | `test_us0131_opencode_only_resolves_shared_from_its_magic` |
| UAT-4 | AC-4 | pass | `test_us0131_shared_kernel_uses_resolver_not_hardcode` |
| UAT-5 | AC-5 | pass | `test_us0131_capability_matrix_reason_codes_documented` |
| UAT-6 | AC-6 | pass | `test_us0131_both_host_precedence_table` (+ reject opencode.json dump m5) |
| UAT-7 | AC-7 | pass | `test_us0131_installer_preserves_local_config`; metadata exit 0 |
| UAT-8 | AC-8 | pass | all 10 markers; runbook `## Cross-host runtime configuration (US-0131)` |
| convergence_smoke | surrogate | pass | `contract_test_failed=0`; 6 waived probes `UAT_PROBE_FORBIDDEN` |

## Contract test markers (10) — verify-work live re-run

`python -m pytest tests/us0131_contract_test.py -v` — **10 passed** in 0.11s (2026-09-07T20:46:21Z).

1. `test_us0131_neutral_path_no_cursor_required` — PASS
2. `test_us0131_cursor_adapter_preserves_dec0055_precedence` — PASS
3. `test_us0131_opencode_only_resolves_shared_from_its_magic` — PASS
4. `test_us0131_both_host_precedence_table` — PASS
5. `test_us0131_rejects_opencode_json_governance_dump` — PASS
6. `test_us0131_schema_fail_closed_codes` — PASS
7. `test_us0131_installer_preserves_local_config` — PASS
8. `test_us0131_shared_kernel_uses_resolver_not_hardcode` — PASS
9. `test_us0131_model_keys_ignored_us0132_boundary` — PASS
10. `test_us0131_capability_matrix_reason_codes_documented` — PASS

Parity: `python scripts/check_intake_template_parity.py --scope=us-0131` → `[INTAKE_TEMPLATE_PARITY_OK]`.  
Metadata: `python scripts/check-user-visible-metadata.py --repo .` → exit 0 (B-1 CLEARED).

## Waived probes (honest live-runtime)

| Probe | reason_code |
|-------|-------------|
| browser_smoke | `UAT_PROBE_FORBIDDEN` (contract-test slice; no web UI) |
| api_health | `UAT_PROBE_FORBIDDEN` (no runtime HTTP API) |
| process_health | `UAT_PROBE_FORBIDDEN` (no runtime app server) |
| cli_smoke | `UAT_PROBE_FORBIDDEN` (static harness only; no live installer smoke) |
| build | `UAT_PROBE_FORBIDDEN` (no separate build step) |
| manual_operator | `UAT_PROBE_FORBIDDEN` (contract markers + runbook cover operator surface) |

## Isolation compliance gate (US-0048 / DEC-0029)

| Phase | Marker | Result |
|-------|--------|--------|
| execute | `dev-US0131-execute-20260907T200826Z-fresh` | PASS |
| execute remediation | `dev-US0131-execute-remediation-20260907T202531Z-fresh` | PASS |
| qa (re-run) | `qa-US0131-qa-20260907T203347Z-fresh` | PASS |
| verify-work | `qa-US0131-verify-work-20260907T204621Z-fresh` | PASS (this phase) |

## Runtime proofs

| Phase | runtime_proof_id | proof_hash |
|-------|------------------|------------|
| execute remediation | `rp-auto-20260907-us0131-execute-remediation-dev-20260907T202531Z-US-0131` | `7BB3B2E38B12A434B1039A1FEC7BC90727CD15823C36328B1A32BF5E12FEB95C` |
| qa re-run (consumed) | `rp-auto-20260907-us0131-qa-qa-20260907T203347Z-US-0131` | `84692196079278DF25EDF8781DCCE750282DC8F7DFCBA4A9039D7F5FBDCB87CC` (MATCH; consumed 20:46:21 before ttl 21:33:47) |
| verify-work (issued) | `rp-auto-20260907-us0131-verify-work-qa-20260907T204621Z-US-0131` | `7F59D8E38F3449966F5E07B861314CD4EC85DC5CC432828C8CB90A451175984F` |

## Results summary vs acceptance

| Bucket | Count |
|--------|-------|
| PASS | 9 |
| FAIL | 0 |
| Total steps | 9 |

All eight acceptance criteria (AC-1..AC-8) map to UAT-1..UAT-8 and **PASS**. Canonical `convergence_smoke` **PASS**. Backlog Status remains **OPEN** (US-0045); acceptance L159 unchecked (US-0120 `/closure` owns DONE + ticks). Machine-readable: `sprints/S0133/uat.json`.

## Next

- Sovereign-critic of verify-work (if CROSS_MODEL_REVIEW=1) → **`/release`** (fresh **release**) for **`S0133`** / **`US-0131`**
- STOP — do not spawn `/release` from this subagent. Do NOT mark US-0131 DONE. Do NOT tick acceptance.
