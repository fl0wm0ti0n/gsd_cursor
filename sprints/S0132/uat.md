# Sprint S0132 — UAT (BUG-0016) — populated at /verify-work (DEC-0009)

- **uat_lifecycle**: populated (verify-work PASS; DEC-0009 placeholder → populated complete)
- **sprint_id**: S0132
- **bug_refs**: BUG-0016
- **phase**: verify-work (build+verify macro)
- **role**: qa (fresh per BUG-0006)
- **orchestrator_run_id**: auto-20260906-bug0016
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **story_type**: code (OpenCode Layer-1 permission matrix + contract-test slice; FRAMEWORK_KIT_REPO=1)
- **fresh_context_marker**: `qa-BUG0016-verify-work-20260906T192500Z-fresh`
- **timestamp**: 2026-09-06T19:25:00Z (UTC)
- **model_id**: composer-2.5 (CROSS_MODEL_REVIEW=1 — required)
- **producer_phase_id**: qa (role=qa; **QA_PASS**; `blocking_count=0`)
- **critic_phase_id**: sovereign-critic of qa (tech-lead, composer-2.5-fast; PASS; anti_slop=10; marker `critic-BUG0016-qa-20260906T192000Z-fresh`)
- **verdict**: **PASS** (verify-work) — UAT 9/9 pass, 0 fail (AC-1..AC-8 → UAT-1..UAT-8 + canonical `convergence_smoke`); live `pytest tests/bug0016_contract_test.py -v` → **7 passed in 0.03s**; isolation execute+qa+verify-work present
- **total_steps**: 9 (UAT-1..UAT-8 + canonical `convergence_smoke`)
- **passed**: 9 | **failed**: 0
- **bug_status**: OPEN (do not mark BUG-0016 DONE — US-0045; acceptance BUG-0016 L181 unchecked; intake JSON not mutated)
- **blocking_findings**: 0
- **non_blocking_findings**: 3 (NB-1..NB-3 carry-forwards — informational)
- **harness_fail_zero_claimed**: false (slice contract tests are the required evidence)
- **browser_probe_used**: false (no fake browser PASS)

## Probe class — OpenCode Layer-1 permission contract

BUG-0016 is a Layer-1 agent-frontmatter / DEC-0122 contract-test slice. Applicable probe: `contract_tests_primary` (7 markers). No web UI. Six live-runtime classes waived with **`UAT_PROBE_FORBIDDEN`**: `browser_smoke`, `api_health`, `process_health`, `cli_smoke`, `build`, `manual_operator`. **No silent browser PASS.** MCP browser sequence not run.

Canonical surrogate step `id=convergence_smoke` kept `result=pass` because `contract_test_failed=0` (7/7 pytest).

## Target bug + acceptance criteria (architecture `# BUG-0016`)

- **BUG-0016** — OpenCode Layer-1 role permissions block required lifecycle validators/writes (matrix vs kit duties)
  - AC-1: PASS — `po` / `tech-lead` / `curator` use `bash: ask` (UAT-1; marker 1)
  - AC-2: PASS — PO edit allows intake_evidence/** + resume_brief + state.md; `**` deny last (UAT-2; marker 2)
  - AC-3: PASS — Sprint keys use `sprints/S*/…` not `Sxxxx` (UAT-3; marker 3)
  - AC-4: PASS — Release duty paths complete (UAT-4; marker 4; CF2 informational)
  - AC-5: PASS — Success test (c) preserved — non-dev no production/code allow (UAT-5; marker 5)
  - AC-6: PASS — `security` / `auto` unchanged (UAT-6; marker 6)
  - AC-7: PASS — Active ↔ template agent parity (UAT-7; marker 7)
  - AC-8: PASS — DEC-0122 §2 sole matrix SOT; no DEC-0130; us0122 realign (UAT-8)

## UAT step results (verify-work)

| Step | AC | Result | Evidence |
|------|----|--------|----------|
| UAT-1 | AC-1 | pass | `test_bug0016_po_tl_curator_bash_ask` |
| UAT-2 | AC-2 | pass | `test_bug0016_po_intake_resume_state_allows` |
| UAT-3 | AC-3 | pass | `test_bug0016_sprint_globs_are_s_star_not_sxxxx` |
| UAT-4 | AC-4 | pass | `test_bug0016_release_duty_paths`; CF2 informational |
| UAT-5 | AC-5 | pass | `test_bug0016_success_test_c_non_dev_no_production_allow` |
| UAT-6 | AC-6 | pass | `test_bug0016_security_auto_unchanged` |
| UAT-7 | AC-7 | pass | `test_bug0016_active_template_agent_parity` |
| UAT-8 | AC-8 | pass | us0122 8/8; DEC-0122 §2 sole SOT; no DEC-0130 |
| convergence_smoke | surrogate | pass | `contract_test_failed=0`; 6 waived probes `UAT_PROBE_FORBIDDEN` |

## Contract test markers (7) — verify-work live re-run

`python -m pytest tests/bug0016_contract_test.py -v` — **7 passed** in 0.03s (2026-09-06T19:25:00Z).

1. `test_bug0016_po_tl_curator_bash_ask` — PASS
2. `test_bug0016_po_intake_resume_state_allows` — PASS
3. `test_bug0016_sprint_globs_are_s_star_not_sxxxx` — PASS
4. `test_bug0016_release_duty_paths` — PASS
5. `test_bug0016_success_test_c_non_dev_no_production_allow` — PASS
6. `test_bug0016_security_auto_unchanged` — PASS
7. `test_bug0016_active_template_agent_parity` — PASS

## Waived probes (honest live-runtime)

| Probe | reason_code |
|-------|-------------|
| browser_smoke | `UAT_PROBE_FORBIDDEN` (OpenCode Layer-1 permission contract; no web UI) |
| api_health | `UAT_PROBE_FORBIDDEN` (no runtime HTTP API) |
| process_health | `UAT_PROBE_FORBIDDEN` (no runtime app server) |
| cli_smoke | `UAT_PROBE_FORBIDDEN` (static harness only; no live OpenCode CI probe) |
| build | `UAT_PROBE_FORBIDDEN` (no separate build step) |
| manual_operator | `UAT_PROBE_FORBIDDEN` (contract markers cover permission matrix) |

## Isolation compliance gate (US-0048 / DEC-0029)

| Phase | Marker | Result |
|-------|--------|--------|
| execute | `dev-BUG0016-execute-20260906T190500Z-fresh` | PASS |
| qa | `qa-BUG0016-qa-20260906T191500Z-fresh` | PASS |
| verify-work | `qa-BUG0016-verify-work-20260906T192500Z-fresh` | PASS (this phase) |

## Runtime proofs

| Phase | runtime_proof_id | proof_hash |
|-------|------------------|------------|
| execute | `rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016` | `519A7617F1ADBEAFD95A940AF28B130F8EB309350F3F787C0AC02152FBEC76BF` |
| qa (consumed) | `rp-auto-20260906-bug0016-qa-qa-20260906T191500Z-BUG-0016` | `2258AE43B09997167501DD437B38DBA1A01356D1D09991707C1098EBC8D5523D` (MATCH; consumed 19:25 before ttl 20:15) |
| verify-work (issued) | `rp-auto-20260906-bug0016-verify-work-qa-20260906T192500Z-BUG-0016` | `C9DE18A187C251AEC3081E43EA65645CBA3B7C8341D0F10639567CF3224B5B41` |

## Results summary vs acceptance

| Bucket | Count |
|--------|-------|
| PASS | 9 |
| FAIL | 0 |
| Total steps | 9 |

All eight acceptance criteria (AC-1..AC-8) map to UAT-1..UAT-8 and **PASS**. Canonical `convergence_smoke` **PASS**. Backlog Status remains **OPEN** (US-0045); acceptance L181 unchecked. Machine-readable: `sprints/S0132/uat.json`.

## Next

- Sovereign-critic of verify-work (if CROSS_MODEL_REVIEW=1) → **`/release`** (fresh **release**) for **`S0132`** / **`BUG-0016`**
- STOP — do not spawn `/release` from this subagent. Do NOT mark BUG-0016 DONE. Do NOT tick acceptance.
