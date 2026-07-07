# Release Notes — S0119 / US-0119

- **Sprint**: `S0119`
- **Story**: `US-0119` — Autonomous-autonomy presets and configurable hard-stop relaxation
- **Release date**: 2026-07-06 (UTC; 2026-07-06T19:03:00Z UTC, 21:03:00 UTC+2)
- **orchestrator_run_id**: `auto-20260705-05`
- **delivery_mode**: `ultra_lean`
- **macro_phase**: `ship` (release — first canonical phase of ship per ultra_lean)
- **policy_mode**: `disabled` (`RELEASE_PUBLISH_MODE=disabled`)
- **trigger_source**: `manual` (`RELEASE_TRIGGER_SOURCE=manual`)
- **branch**: `local` (no push; `SYNC_POLICY_MODE=disabled` per DEC-0018)
- **fresh_context_marker**: `release-US0119-20260706T210300Z-fresh`
- **runtime_proof_id**: `rp-auto-20260706-release-release-20260706T210200Z-US-0119`
- **release_version**: (none — out-of-band; default-off feature, no installer-visible behavior change; S0118 precedent)

## Summary

Ship the **second code-bearing** story of the post-US-0117 drain (after US-0118's work-kind classifier). US-0119 introduces **autonomous-autonomy presets** — a single `AUTONOMY_PRESET={none|balanced|full}` scratchpad flag (default `none`) whose value expands deterministically via `scripts/autonomy_preset_lib.py:expand_autonomy_preset(preset, overrides) -> dict` into a well-defined bundle of twelve per-feature autonomy flags (all default-off individually so backward compatibility is preserved). Complements this with `AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}` (default `block`) that classifies every fail-closed reason code in `docs/engineering/autonomy-stop-matrix.md` as `security_hard` (never auto-resolved; 18+ codes) or `autonomy_resolvable` (bounded auto-repair with a per-run cap + ledger). New bounded auto-repair ledger at `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl` (gitignored) with cap exhaustion escalation (`AUTONOMY_REPAIR_CAP_EXHAUSTED`). Operator authority preserved via breadcrumb in `docs/engineering/state.md` (`autonomy_relaxed: <reason_code> -> <auto_repair_kind>`). Composes (read-only) with 6 consumers: US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 — preset expansion uses existing flag keys only, never rewrites their semantics. 12 ACs, 10 `test_us0119_*` markers, 6/6 `autonomy_preset_lib.py --self-test` tests, 6/6 compose guards UNCHANGED. Consumer wiring includes `scripts/sovereign_loop_lib.py` (10 AUTONOMY_PRESET refs) + `scripts/release_changelog_lib.py` (AUTONOMY_PRESET refs) + `.cursor/commands/auto.md` + `docs/engineering/runbook.md` + `template/*` byte-parities. Compose guards preserved via contract test `test_us0119_preset_expansion_uses_known_keys_only`. **`## US-0119`** architecture section **resolved in `/architecture` phase** (T-anch in S0119 = NO-OP / verification per R-0105 Q-2 LOCKED — no execute-phase write to architecture.md; anchor confirmed at L1925).

## ACs satisfied

**12/12 PASS** (independently re-verified by release; all prior-cycle blockers resolved in cycle 5):

| AC | Description | Status |
|----|-------------|--------|
| AC-1 | AUTONOMY_PRESET scratchpad flag (`none|balanced|full`, default `none`) | PASS |
| AC-2 | Deterministic preset expansion (`expand_autonomy_preset`) — known-keys-only | PASS |
| AC-3 | AUTONOMY_STOP_POLICY flag (`block|auto_repair_then_block|auto_repair_then_skip`, default `block`) | PASS |
| AC-4 | Autonomy stop matrix manifest (MD + YAML + validator + template mirrors) | PASS |
| AC-5 | Per-feature autonomy flags wired (sovereign_loop_lib + release_changelog_lib + auto.md + runbook + installer) | PASS |
| AC-6 | Backward compatibility (`AUTONOMY_PRESET=none` = byte-identical pre-US-0119) | PASS (`test_us0119_preset_none_is_noop`) |
| AC-7 | Security-hard gates never softened (18+ codes classified `security_hard`) | PASS (`test_us0119_security_hard_gates_never_auto_repaired`) |
| AC-8 | Bounded auto-repair ledger (gitignored; per-run cap; `AUTONOMY_REPAIR_CAP_EXHAUSTED` escalation) | PASS |
| AC-9 | Operator authority preserved via breadcrumb in `docs/engineering/state.md` | PASS |
| AC-10 | Tests + parity (10 `test_us0119_*` markers + `--scope=us-0119` + validator `--self-test`) | PASS |
| AC-11 | Documentation (autonomy-stop-matrix.md + architecture.md ## US-0119 + runbook.md h2 + auto.md h2 + template parities) | PASS |
| AC-12 | Compose, do not amend (6 read-only consumers + 6/6 compose guards UNCHANGED) | PASS |

## Files shipped

- `scripts/autonomy_preset_lib.py` (NEW — T-001) — preset expansion lib (`expand_autonomy_preset(preset, overrides) -> dict`)
- `template/scripts/autonomy_preset_lib.py` (NEW mirror — T-001/T-009)
- `scripts/autonomy_repair_ledger_lib.py` (NEW — T-005) — bounded auto-repair ledger (append-only JSONL; gitignored)
- `template/scripts/autonomy_repair_ledger_lib.py` (NEW mirror — T-005)
- `scripts/data/autonomy_stop_matrix.yaml` (NEW — T-003) — autonomy stop matrix manifest companion
- `docs/engineering/autonomy-stop-matrix.md` (NEW — T-003) — 28 reason codes (18 security_hard, 10 autonomy_resolvable)
- `template/docs/engineering/autonomy-stop-matrix.md` (NEW mirror — T-003)
- `scripts/validate_autonomy_stop_matrix.py` (NEW — T-003) — matrix validator with `--self-test`
- `template/scripts/validate_autonomy_stop_matrix.py` (NEW mirror — T-003)
- `tests/us0119_autonomy_preset_test.py` (NEW — T-007) — 10 `test_us0119_*` markers
- `template/tests/us0119_autonomy_preset_test.py` (NEW mirror — T-007)
- `scripts/sovereign_loop_lib.py` (10 AUTONOMY_PRESET refs — T-004) — consumer wiring
- `scripts/release_changelog_lib.py` (AUTONOMY_PRESET refs — T-004) — consumer wiring
- `its_magic/README.md` — `### Autonomy presets (US-0119)` umbrella + `#### US-0119` operator subsection + scratchpad ref extension (pure addition; `fc_its_magic_vs_template:PARITY_OK_*_*`)
- `template/its_magic/README.md` — byte-synced one-way copy
- `docs/engineering/runbook.md` — `## Autonomy presets (US-0119)` h2
- `template/docs/engineering/runbook.md` — byte-synced mirror
- `.cursor/commands/auto.md` — `## Autonomy presets (US-0119)` h2 + prose
- `template/.cursor/commands/auto.md` — byte-synced mirror
- `.cursor/commands/intake.md` — AUTONOMY_PRESET hook (T-004)
- `template/.cursor/commands/intake.md` — byte-synced mirror
- `.cursor/scratchpad.md` — `AUTONOMY_PRESET=none` + `AUTONOMY_STOP_POLICY=block` + 12 per-feature flags with comment block
- `.cursor/scratchpad.local.example.md` — mirror
- `template/.cursor/scratchpad.local.example.md` — mirror
- `handoffs/autonomy_repair_ledger/` (NEW directory; gitignored — T-005)
- `docs/engineering/context/installer-owned-paths.manifest` — new scripts listed
- `template/docs/engineering/context/installer-owned-paths.manifest` — mirror
- `scripts/check_intake_template_parity.py` — `AUTONOMY_PRESET_PAIRS` + `--scope=us-0119` flag (T-008)
- `template/scripts/check_intake_template_parity.py` — byte-synced mirror (T-008)

## Validator outputs

```
$ python -m pytest tests/us0119_autonomy_preset_test.py -v
... 10 passed ...

$ python -m pytest tests/scratchpad_example_parity_test.py -v
... 4 passed ...

$ python scripts/autonomy_preset_lib.py --self-test
[PASS] Test 1..6 — 6/6 tests passed

$ python scripts/validate_autonomy_stop_matrix.py --self-test
[MATRIX_SELF_TEST_OK] 0 violations

$ python scripts/check_intake_template_parity.py --repo .
[INTAKE_TEMPLATE_PARITY_OK] scope=intake

$ python scripts/check_intake_template_parity.py --scope=us-0119 --repo .
[INTAKE_TEMPLATE_PARITY_OK] scope=us-0119

$ python scripts/validate_readme_feature_coverage.py --repo . --enforce
[README_FEATURE_COVERAGE_VALIDATE_OK]

$ python scripts/validate_doc_profile.py --repo .
[DOC_PROFILE_VALIDATE_OK]

$ python scripts/check-user-visible-metadata.py --repo .
(exit 0 — silent PASS)

$ python -c "...PARITY_OK..."
PARITY_OK 20083 20083
```

## Compose guards (6/6 UNCHANGED — `rg` enforced)

- US-0092 (`FULL_AUTONOMY_*`): UNCHANGED
- US-0095 (`AUTO_PHASE_*`): UNCHANGED
- US-0056 (`RUNTIME_PROOF_*`): UNCHANGED
- US-0068 (`ISOLATION_*`): UNCHANGED
- US-0096 (`DELIVERY_MODE` / delivery modes): UNCHANGED
- BUG-0007 (`INTAKE_*` evidence): UNCHANGED

US-0119 does NOT become a new compose guard — it's a preset-dispatch layer.

## Run / Connect / Verify

### Run

- **start_command**: `python scripts/autonomy_preset_lib.py --self-test` (quick smoke) or `python -m pytest tests/us0119_autonomy_preset_test.py -v` (full contract)
- **runtime_mode**: `local` (no remote runtime; pure scratchpad config + stdlib libs)
- **runtime_context_ref**: N/A (no remote connectivity required; `docs/engineering/runtime-connectivity.md` untouched)

### Connect

- **service_url**: N/A (library-level feature — no service endpoint)
- **service_port**: N/A
- **health_endpoint**: N/A

### Verify

1. `python scripts/autonomy_preset_lib.py --self-test` → `[PASS] Test 1..6 — 6/6 tests passed`
2. `python -m pytest tests/us0119_autonomy_preset_test.py -v` → `10 passed`
3. `python scripts/validate_autonomy_stop_matrix.py --self-test` → `[MATRIX_SELF_TEST_OK] 0 violations`
4. `python scripts/check_intake_template_parity.py --scope=us-0119 --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=us-0119`
5. `rg "AUTONOMY_PRESET" scripts/sovereign_loop_lib.py` → 10 matches (consumer wiring confirmed)

### Credentials

- **API_TOKEN_ENV**: N/A (no external API)
- **AUTONOMY_PRESET**: Scratchpad config key (default `none` — no env secret)

### Known Issues

- None (all 12 ACs satisfied; 5 non-blocking findings are orthogonal pre-existing issues — see release-findings.md)

## Drain-advance note

**1 story shipped this cycle (US-0119).** Backlog drain active. Drain budget remaining: 9. Prior drain-advance flagged **US-0108 status-drift** as non-blocking (US-0108 shipped but backlog row was not flipped OPEN→DONE). US-0119 release does not repair this orthogonal drift (out-of-scope for US-0119's surjective AC set). Reconcile separately.

## Version bump rationale

**No version bump**. Out-of-band documentation+code story (default-off feature — `AUTONOMY_PRESET=none` is byte-identical pre-US-0119 behavior; default `AUTONOMY_STOP_POLICY=block` preserves existing hard-stop semantics). No installer-visible behavior change for operators using defaults. Following S0118 precedent — next operator-initiated packaging release will consolidate US-0113..US-0119 + any intervening stories into a single bump.

## Publish / Sync

- **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- **`SYNC_POLICY_MODE=disabled`** — `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **`RELEASE_TRIGGER_SOURCE=manual`** — no adapter subprocess

## Decision gate

**FALSE** (no override required). DEC-0119 accepted, approach A1 locked, 12/12 ACs satisfied, 17/17 tests PASS, PARITY_OK on all 7 surfaces, 6/6 compose guards UNCHANGED.

## Cycle-5 resolution note

US-0119 required 5 dev+QA cycles via `AUTO_LOOP_MAX_CYCLES=5`. Cycles 1-4 surfaced: missing execute-summary.md, missing test file, missing template mirrors, validator bug (over-broad orphan detection), missing consumer wiring (sovereign_loop_lib + release_changelog_lib), scratchpad parity regressions. Cycle 5 (final cycle) resolved all blockers; release subagent independently verified all gates organically.

## Next

**`/refresh-context`** (fresh curator subagent per BUG-0006 isolation; ship macro — second canonical phase of ship per ultra_lean) for segment closeout; backlog drain continues with drain-advance to next OPEN story (drain budget remaining = 9).
