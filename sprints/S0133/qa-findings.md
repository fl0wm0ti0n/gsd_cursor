# QA findings — US-0131 / S0133 / auto-20260907-us0131 (qa re-run after remediation)

- **phase_id**: qa, **role**: qa, **story_id**: US-0131 (OPEN — not marked DONE per US-0045), **sprint_id**: S0133
- `orchestrator_run_id=auto-20260907-us0131`, `delivery_mode=ultra_lean`, `macro_phase=build+verify`
- `AUTO_IMPLEMENTATION_LOOP=1` (B-1 remediation cycle complete)
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1 — required on isolation)
- `producer_phase_id=execute` (remediation), `producer_role=dev`, `producer_model_id=composer-2.5`
- `critic_phase_id=sovereign-critic` (execute remediation review), `critic_model_id=composer-2.5-fast`, `critic_verdict=PASS`, `anti_slop_aggregate=10`, `open_blocking_findings=0`
- `critic_fresh_context_marker=critic-US0131-execute-remediation-20260907T203025Z-fresh`
- `fresh_context_marker=qa-US0131-qa-20260907T203347Z-fresh` (NEW per US-0048 / BUG-0006; not reused from prior qa `qa-US0131-qa-20260907T201647Z-fresh`)
- `timestamp (UTC)=2026-09-07T20:33:47Z`
- **verdict: QA_PASS**
- `blocking_count=0`
- `non_blocking_count=3` (critic NB carry-forwards informational)
- `story_status=OPEN` (do not mark US-0131 DONE; acceptance L159 unchecked; intake JSON not mutated; architecture.md / DEC-0131 not mutated this phase)
- `acceptance_L159=NOT ticked`
- `intake_json=NOT mutated`
- `FRAMEWORK_KIT_REPO=1` (scripts/docs/examples/contract-test slice — no web UI; no fake browser PASS)
- `SECURITY_REVIEW=0`, `CROSS_REPO_OBSERVABILITY=0`, `COMPONENT_SCOPE_MODE=0` (zero overhead)
- `SPEC_PACK_MODE=0`, `USER_GUIDE_MODE=0`, `REMOTE_EXECUTION=0`
- `SYNC_POLICY_MODE=disabled` (no push)
- `sibling_out_of_scope=US-0132`

## Verdict rationale

Fresh QA re-run after execute remediation. Independent remapped AC-1..AC-8, re-ran US-0131 contract slice (10/10 PASS), `--scope=us-0131` parity (OK), triad `--check` (exit 0), and **metadata guard exit 0** (prior B-1 cleared — `US-0131` only in allowlisted `#` comment at `installer.py:268`; docstrings at `materialize_kit_config_example` / `run_kit_config_postinstall` are neutral). Execute remediation proof hash MATCH before TTL. Blocking findings: **none**. US-0131 remains OPEN; ACs unchecked; US-0132 not worked.

## Test plan

| # | Check | Expected |
|---|---|---|
| 1 | Independent AC-1..AC-8 remap vs files | Each AC has delivered surface + markers |
| 2 | `python -m pytest tests/us0131_contract_test.py -v` | 10/10 PASS |
| 3 | `python scripts/check_intake_template_parity.py --scope=us-0131` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| 4 | `python scripts/enforce-triad-hot-surface.py --check` | exit 0 |
| 5 | `python scripts/check-user-visible-metadata.py --repo .` | exit 0 (B-1 re-verify) |
| 6 | Active↔template byte identity for US-0131 pairs | IDENTICAL |
| 7 | Execute remediation DEC-0038 proof consume | MATCH before TTL |
| 8 | Status OPEN; ACs unchecked; US-0132 OOS | unchanged |
| 9 | Critic NBs (informational) | non-blocking |
| 10 | UAT probes | contract slice + convergence_smoke PASS; live-runtime waived `UAT_PROBE_FORBIDDEN` |

## Independent checks (run in this qa subagent)

| Check | Command | Result |
|---|---|---|
| Execute remediation proof SHA-256 | Python hashlib sorted-key compact lowercase JSON | **MATCH** `7BB3B2E38B12A434B1039A1FEC7BC90727CD15823C36328B1A32BF5E12FEB95C`; ttl `2026-09-07T21:25:31Z`; consumed_at `2026-09-07T20:33:47Z` — **RUNTIME_PROOF_VALID** |
| US-0131 contract tests | `python -m pytest tests/us0131_contract_test.py -v` | **10 passed** in 0.12s |
| us-0131 parity | `python scripts/check_intake_template_parity.py --scope=us-0131` | **exit 0** — `[INTAKE_TEMPLATE_PARITY_OK] scope=us-0131` |
| Triad hot-surface | `python scripts/enforce-triad-hot-surface.py --check` | **exit 0** (pre-write) |
| User-visible metadata | `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** — **B-1 CLEARED** |
| Template byte pairs (14) | SHA-256 / size compare active↔template | **14/14 IDENTICAL** |
| Backlog / acceptance | Status + checkbox spot-check | OPEN; 8/8 AC `- [ ]`; acceptance L159 `- [ ] US-0131` |
| Installer docstring spot-check | `materialize_kit_config_example` / `run_kit_config_postinstall` | Neutral docstrings; ID only in `#` L268 |
| LINT_COMMAND | (empty in runbook) | **skipped** |
| TYPECHECK_COMMAND | (empty in runbook) | **skipped** |
| Full harness `tests/run-tests.ps1` | not re-run this pass | **not claimed** — scoped slice + parity + metadata are the required gates for this FRAMEWORK_KIT_REPO=1 story |

## Blocking findings

None. Prior **B-1** `USER_VISIBLE_INTERNAL_METADATA_DETECTED` is **CLOSED** (metadata guard exit 0 after docstring remediation).

## Non-blocking findings (critic NB carry-forwards — informational)

| ID | Topic | QA note |
|---|---|---|
| NB1 / us0131exr-challenger-001 (+ prior us0131ex-*) | metadata allowlist; soft-fail / shadow | Metadata exit 0 re-verified. Soft-fail / `HOST_CONFIG_KEY_SHADOWED` remain intentional. Not blocking. |
| NB2 / us0131exr-architect-002 | remediation scope; 9-module + parity | Remediation confined to installer.py; 14/14 pairs IDENTICAL; architecture/DEC read-only held. |
| NB3 / us0131exr-subtractor-003 | no scope creep; marker depth | US-0132 OOS; no DONE flip; marker 8 PASS. Optional deeper AST audit deferred — not blocking. |

## AC remap (independent — files + tests)

| AC | Delivered surface | Markers | Result |
|---|---|---|---|
| AC-1 Host-neutral SOT | `.its-magic/config.example.json` + `resolve_runtime_config` | m1, m6 | **PASS** |
| AC-2 Cursor adapter | LegacyScratchpadAdapter / DEC-0055 layers | m2 | **PASS** |
| AC-3 OpenCode-only | OpenCode-only path + `HOST_CONFIG_PATH_FORBIDDEN` | m3 | **PASS** |
| AC-4 Shared-kernel migration | 9 modules → resolver | m8 | **PASS** |
| AC-5 Capability matrix | capability matrix + reason codes | m10 | **PASS** |
| AC-6 Both-host determinism | precedence + shadow diagnostic | m4, m5 | **PASS** |
| AC-7 Installer safety | `run_kit_config_postinstall` + local preserve + metadata clean | m7 | **PASS** (B-1 cleared) |
| AC-8 Tests + docs | 10 markers + runbook h2 + HOST_CONFIG_* rows | all 10 + T-008 | **PASS** |

**Overall AC gate**: **PASS** (slice) — Status remains OPEN; backlog/acceptance checkboxes **not** ticked (US-0045; `/verify-work` ownership).

## Contract marker results (10/10 slice)

| # | Marker | Result |
|---|---|---|
| 1 | `test_us0131_neutral_path_no_cursor_required` | PASS |
| 2 | `test_us0131_cursor_adapter_preserves_dec0055_precedence` | PASS |
| 3 | `test_us0131_opencode_only_resolves_shared_from_its_magic` | PASS |
| 4 | `test_us0131_both_host_precedence_table` | PASS |
| 5 | `test_us0131_rejects_opencode_json_governance_dump` | PASS |
| 6 | `test_us0131_schema_fail_closed_codes` | PASS |
| 7 | `test_us0131_installer_preserves_local_config` | PASS |
| 8 | `test_us0131_shared_kernel_uses_resolver_not_hardcode` | PASS |
| 9 | `test_us0131_model_keys_ignored_us0132_boundary` | PASS |
| 10 | `test_us0131_capability_matrix_reason_codes_documented` | PASS |

## Template byte-identity (US-0131 pairs)

| Pair | Result |
|---|---|
| `scripts/host_runtime_config_lib.py` | IDENTICAL |
| `tests/us0131_contract_test.py` | IDENTICAL |
| `.its-magic/config.example.json` | IDENTICAL |
| 9 migrated shared-kernel scripts | IDENTICAL |
| `scripts/validate_autonomy_stop_matrix.py` | IDENTICAL |
| `docs/engineering/context/installer-owned-paths.manifest` | IDENTICAL |

Note: `installer.py` is kit-root (not under `template/` mirror for this check); B-1 remediation verified on active `installer.py` via metadata guard.

## Compose / scope gates

| Gate | Result |
|---|---|
| US-0132 OUT OF SCOPE | HELD (marker 9 PASS; no MODEL_* expansion) |
| BUG-0015 / BUG-0016 | not reopened |
| US-0045 Status OPEN / ACs unchecked | HELD |
| No live OpenCode probe | HELD |
| DEC-0131 / architecture.md | read-only this phase |

## UAT / convergence (US-0128)

- Contract slice green (`contract_test_failed=0`); metadata guard exit 0.
- Canonical `convergence_smoke` recorded as **pass** in `sprints/S0133/uat.json`.
- Six live-runtime probe classes waived `UAT_PROBE_FORBIDDEN` (FRAMEWORK_KIT_REPO=1).
- Full UAT ownership remains with `/verify-work` (do not flip DONE / tick ACs here).

## Runtime proof (DEC-0038) — qa re-run

| Field | Value |
|---|---|
| runtime_proof_id | `rp-auto-20260907-us0131-qa-qa-20260907T203347Z-US-0131` |
| proof_issued_at | 2026-09-07T20:33:47Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-09-07T21:33:47Z |
| proof_hash | `84692196079278DF25EDF8781DCCE750282DC8F7DFCBA4A9039D7F5FBDCB87CC` |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"composer-2.5","orchestrator_run_id":"auto-20260907-us0131","phase_id":"qa","proof_issued_at":"2026-09-07T20:33:47Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260907-us0131-qa-qa-20260907T203347Z-US-0131","sprint_id":"S0133","story_id":"US-0131"}` |
| consumed_producer_proof | `rp-auto-20260907-us0131-execute-remediation-dev-20260907T202531Z-US-0131` / `7BB3B2E38B12A434B1039A1FEC7BC90727CD15823C36328B1A32BF5E12FEB95C` — RUNTIME_PROOF_VALID |

## Cross-reviewer findings (sovereign-critic of qa re-run)

- `critic_model_id=composer-2.5-fast`, `degraded_mode=false`, `verdict=PASS`
- `anti_slop_aggregate=10`, `blocking_count=0`, `open_blocking_count=0`
- `finding_ids=us0131qa2-challenger-001,us0131qa2-architect-002,us0131qa2-subtractor-003` (informational; US-0127 auto-resolved)
- `proof_consume=RUNTIME_PROOF_VALID` for `rp-auto-20260907-us0131-qa-qa-20260907T203347Z-US-0131` / `84692196079278DF25EDF8781DCCE750282DC8F7DFCBA4A9039D7F5FBDCB87CC`
- B-1 CLEARED confirmed; Status OPEN held; next=/verify-work (orchestrator spawn only)

## Next (superseded by verify-work)

- Original next was `/verify-work`. Completed 2026-09-07T20:46:21Z — see verify-work block below.

---

## Verify-work findings — US-0131 / S0133 (fresh qa)

- **phase_id**: verify-work, **role**: qa
- `fresh_context_marker=qa-US0131-verify-work-20260907T204621Z-fresh`
- `timestamp (UTC)=2026-09-07T20:46:21Z`
- `model_id=composer-2.5` (CROSS_MODEL_REVIEW=1)
- **verdict: VERIFY_WORK_PASS**
- `uat_lifecycle=populated` (DEC-0009)
- `uat_total=9`, `uat_passed=9`, `uat_failed=0` (UAT-1..UAT-8 + convergence_smoke)
- Consumed qa proof `rp-auto-20260907-us0131-qa-qa-20260907T203347Z-US-0131` / `84692196079278DF25EDF8781DCCE750282DC8F7DFCBA4A9039D7F5FBDCB87CC` — **RUNTIME_PROOF_VALID**
- Issued proof `rp-auto-20260907-us0131-verify-work-qa-20260907T204621Z-US-0131` / `7F59D8E38F3449966F5E07B861314CD4EC85DC5CC432828C8CB90A451175984F` / ttl `2026-09-07T21:46:21Z`
- Live re-run: pytest 10/10; parity OK; metadata exit 0; triad pre-check exit 0
- Isolation gate: execute + qa + verify-work **PASS**
- `story_status=OPEN` (no DONE; acceptance L159 unchecked — US-0120 closure)
- Artifacts: `sprints/S0133/uat.json`, `sprints/S0133/uat.md`
- **next_scheduled_phase**: `/release` (fresh **release**)
- **stop_condition**: STOP after verify-work. Do **not** spawn `/release` from this subagent. Do **not** mark US-0131 DONE. Do **not** work US-0132.

## Cross-reviewer findings (sovereign-critic of verify-work)

- `critic_model_id=composer-2.5-fast`, `degraded_mode=false`, `verdict=PASS`
- `anti_slop_aggregate=10`, `blocking_count=0`, `open_blocking_count=0`
- `finding_ids=us0131vw-challenger-001,us0131vw-architect-002,us0131vw-subtractor-003` (informational; US-0127 auto-resolved)
- `proof_consume=RUNTIME_PROOF_VALID` for `rp-auto-20260907-us0131-verify-work-qa-20260907T204621Z-US-0131` / `7F59D8E38F3449966F5E07B861314CD4EC85DC5CC432828C8CB90A451175984F`
- UAT 9/9 CONFIRMED; Status OPEN; acceptance L159 unchecked; B-1 CLEARED; next=/release (orchestrator spawn only)
- NB: `handoffs/verify-work-to-release.md` still cites BUG-0016/S0132 (stale) — `handoffs/resume_brief.md` is authoritative

## Cross-reviewer findings (sovereign-critic of release)

- critic_model_id=composer-2.5-fast, degraded_mode=false, erdict=PASS
- nti_slop_aggregate=10, locking_count=0, open_blocking_count=0
- inding_ids=us0131rel-challenger-001,us0131rel-architect-002,us0131rel-subtractor-003 (informational; US-0127 auto-resolved)
- proof_consume=RUNTIME_PROOF_VALID for 
p-auto-20260907-us0131-release-release-20260907T211518Z-US-0131 / 10026570510E2C006AE4A86CFC2F0A70BE0CF170E30E43C13BEC342EC3E72D7A
- RELEASE_PASS CONFIRMED; Fail:0; Status OPEN; L159 unchecked; queue S0133=released; next=/closure (orchestrator spawn only)
- NB: post-gate active-only runbook Release-status stamp broke live --scope=us-0131 template parity — sync at closure/refresh (non-blocking)

## Cross-reviewer findings (sovereign-critic of closure)

- critic_model_id=composer-2.5-fast, degraded_mode=false, verdict=PASS
- anti_slop_aggregate=10, blocking_count=0, open_blocking_count=0
- finding_ids=us0131clo-challenger-001,us0131clo-architect-002,us0131clo-subtractor-003 (informational; US-0127 auto-resolved)
- proof_consume=RUNTIME_PROOF_VALID for rp-auto-20260907-us0131-closure-qe-20260907T212848Z-US-0131 / 69B2C58BC1026E266C1533DB3E28D9202FD428362F4D34BEE4A15EFAB1CCD335
- CLOSURE_PASS CONFIRMED; Status DONE; L159 [x]; US-0132 OPEN; queue S0133=released; next=/refresh-context (orchestrator spawn only)
- NB: active runbook L4226 Release-status stamp still says OPEN until /closure — refresh should rewrite to DONE (parity already green)

