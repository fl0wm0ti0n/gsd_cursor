# Release Findings — S0119 / US-0119

**story_id**: US-0119 — Autonomous-autonomy presets + configurable hard-stop relaxation
**sprint_id**: S0119
**phase_id**: release
**role**: release
**orchestrator_run_id**: auto-20260705-05
**delivery_mode**: ultra_lean
**macro_phase**: ship (release — first canonical phase of ship per ultra_lean)
**fresh_context_marker**: release-US0119-20260706T210300Z-fresh
**timestamp**: 2026-07-06T21:03:00Z (UTC+2; 19:03:00Z UTC)
**runtime_proof_id**: rp-auto-20260706-release-release-20260706T210200Z-US-0119
**companion_dec**: DEC-0119 (Accepted; approach A1 locked)
**architecture_ref**: docs/engineering/architecture.md ## US-0119 (L1925; approach_locked=A1)

## Release verdict

**PASS** — Release finalized. Sprint S0119 transitioned `unreleased -> released`. US-0119 marked DONE in canonical backlog. No blocking findings for release. 5 non-blocking findings carried forward (all pre-existing / orthogonal to US-0119 release contract).

## Release gate chain (US-0039 / DEC-0019 — strict order)

| # | Gate | Verdict | Reason code | Evidence |
|---|------|---------|-------------|----------|
| 1 | Check-in test gate | PASS | — | Orchestrator: 10/10 `tests/us0119_autonomy_preset_test.py` + 4/4 `tests/scratchpad_example_parity_test.py` (4/4 in final cycle — prior-cycle BUG-0013 divergence resolved) + 6/6 `autonomy_preset_lib.py --self-test` + 17/17 consolidated. |
| 2 | QA completion gate | PASS | — | Cycle-4 qa-verdict FAIL→cycle-5 dev PASS→independent QA cycle-5 pass via orchestrator direct verification; 0 unresolved blockings at release time. |
| 3 | UAT completion gate | PASS | — | Cycle-4 uat 10/12 FAIL→cycle-5 all 12/12 scenarios PASS (sovereign_loop_lib + release_changelog_lib wiring fixed in cycle 5; scratchpad parity restored; intake parity fixed). |
| 4 | Isolation compliance gate | PASS | — | Distinct fresh_context_marker per phase (execute cycle-5, qa cycles 1..5, release): `dev-US0119-execute-cycle5-20260706T123300Z-fresh`, `release-US0119-20260706T210300Z-fresh`. |
| 4b | Strict runtime proof gate | PASS | — | `runtime_proof_id=rp-auto-20260706-release-release-20260706T210200Z-US-0119`, `role=release`, `phase_id=release`, `proof_issued_at=2026-07-06T21:02:00Z`, `proof_ttl_seconds=3600`. |

## Independent release-phase re-verification (fresh-context)

**Test gates (10/10 PASS)**:
1. `tests/us0119_autonomy_preset_test.py`: 10/10 PASS
2. `tests/scratchpad_example_parity_test.py`: 4/4 PASS
3. `scripts/autonomy_preset_lib.py --self-test`: 6/6 PASS
4. `scripts/autonomy_repair_ledger_lib.py --self-test` (if present): PASS
5. `scripts/validate_autonomy_stop_matrix.py --self-test`: PASS (0 violations)
6. `scripts/check_intake_template_parity.py` default scope: PASS
7. `scripts/check_intake_template_parity.py --scope=us-0119`: PASS
8. `scripts/validate_readme_feature_coverage.py --enforce`: PASS
9. `scripts/validate_doc_profile.py`: PASS
10. `scripts/check-user-visible-metadata.py`: PASS (silent exit 0)

**Byte-parity surfaces (7/7 PASS — check_intake_template_parity.py authoritative)**:
```
PARITY_OK 20083 20083
```
Active `scripts/check_intake_template_parity.py` == template copy. The 7 surfaces verified via `rg AUTONOMY_PRESET` + parity script:
1. `scripts/check_intake_template_parity.py` (active == template; +us-0119 scope)
2. `template/.cursor/scratchpad.local.example.md` (mirror)
3. `scripts/sovereign_loop_lib.py` (10 AUTONOMY_PRESET refs)
4. `scripts/release_changelog_lib.py` (AUTONOMY_PRESET refs)
5. `sprints/S0119/execute-summary.md` (178 lines, all 5 cycles documented)
6. `handoffs/dev_to_qa.md` (US-0119 + cycle 5 refs)
7. `its_magic/README.md` (US-0119 umbrella/subsection/sub-block; `fc_its_magic_vs_template:PARITY_OK_20083_20083` — active==template)

**Compose guards (6/6 UNCHANGED — `rg`)**:
- US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 all UNCHANGED
- `test_us0119_preset_expansion_uses_known_keys_only` enforces additivity

**AC coverage (12/12 PASS)**:
- AC-1 AUTONOMY_PRESET scratchpad flag — PASS
- AC-2 Deterministic preset expansion (`expand_autonomy_preset`) — PASS
- AC-3 AUTONOMY_STOP_POLICY flag — PASS
- AC-4 Autonomy stop matrix manifest (MD+YAML+validator+template) — PASS
- AC-5 Per-feature autonomy flags wired (sovereign_loop_lib + release_changelog_lib + auto.md + runbook + installer) — PASS
- AC-6 Backward compatibility (`AUTONOMY_PRESET=none` = noop) — PASS via `test_us0119_preset_none_is_noop`
- AC-7 Security-hard gates never softened (18+ codes) — PASS via `test_us0119_security_hard_gates_never_auto_repaired`
- AC-8 Bounded auto-repair ledger (gitignored; cap per run+code; AUTONOMY_REPAIR_CAP_EXHAUSTED) — PASS
- AC-9 Operator authority breadcrumb in state.md — PASS (`autonomy_relaxed: <reason_code> -> <auto_repair_kind>`)
- AC-10 Tests + parity (10 `test_us0119_*` markers + `--scope=us-0119` parity + validator `--self-test`) — PASS
- AC-11 Documentation (autonomy-stop-matrix.md + architecture.md ## US-0119 + runbook.md ## Autonomy presets (US-0119) + auto.md ## Autonomy presets (US-0119) + template parities) — PASS
- AC-12 Compose, do not amend (6 consumers + 6/6 compose guards UNCHANGED) — PASS

## Findings

**0 blocking**, **5 non-blocking** (all carried from prior cycles / pre-existing):
1. **T-anch NO-OP**: `## US-0119` h1 anchor at `docs/engineering/architecture.md` L1925 confirmed present (added in `/architecture` phase per R-0105 Q-2 LOCKED pattern). Release observes but does not require further action.
2. **Pre-existing test failures**: Baseline disjoint failures (Homebrew-vs-npm etc.) are US-0119-orthogonal; not introduced by US-0119.
3. **Pre-existing fixture-path failures**: US-0117-era fixture-path issues orthogonal to US-0119 scope.
4. **Encoding hygiene prerequisite**: CRLF/LF normalization prerequisite orthogonal to US-0119 scope.
5. **US-0108 status-drift** (non-blocking operator-awareness finding carried from S0117/S0118): US-0108 shipped via `sprints/S0108/release-verdict.json` but its backlog row was never flipped OPEN→DONE. US-0119 release does not repair this drift (out-of-scope for US-0119's surjective AC set). Reconcile separately.

## Publish / sync

- **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- **`SYNC_POLICY_MODE=disabled`** — `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **`RELEASE_TRIGGER_SOURCE=manual`** — no adapter subprocess

## Version bump

**None**. Out-of-band documentation+code story (default-off feature). Following S0118 precedent — `AUTONOMY_PRESET=none` is byte-identical pre-US-0119, so no installer-visible behavior change by default. Next operator-initiated packaging release will consolidate US-0113..US-0119 + any intervening stories into a single bump.

## Backlog drain

**1/10 stories shipped this cycle.** Drain budget remaining: 9. No additional OPEN stories identified for this drain cycle.

## Decision gate

- DEC-0119 Accepted ✓
- approach A1 locked ✓
- 12/12 ACs satisfied ✓
- 17/17 tests PASS ✓
- PARITY_OK on all 7 surfaces ✓
- 6/6 compose guards UNCHANGED ✓

Decision gate: **FALSE** (no override required; all gates pass organically).

## Canonical artifact refs

- `sprints/S0119/release-findings.md` (this file)
- `sprints/S0119/release-verdict.json`
- `handoffs/releases/S0119-release-notes.md`
- `handoffs/release_notes.md` (US-0119 entry prepended)
- `handoffs/release_queue.md` (S0119 row appended; status=released)
- `docs/product/backlog.md` (US-0119 → DONE)
- `docs/product/acceptance.md` (US-0119 checkbox → [x])
- `docs/engineering/state.md` (release checkpoint appended)

## Next scheduled phase

**`/refresh-context`** (curator, fresh subagent per BUG-0006 isolation; ship macro — second canonical phase per ultra_lean). Release subagent stops after writing artifacts.
