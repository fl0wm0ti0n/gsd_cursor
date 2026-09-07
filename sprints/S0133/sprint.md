# Sprint S0133 - Sprint Plan (US-0131)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0131 |
| story_title | Cross-host Its-Magic runtime configuration and parity |
| sprint_id | S0133 |
| delivery_mode | ultra_lean |
| macro_phase | plan (plan-verify PASS; execute next) |
| current_phase | plan-verify |
| approach | A1 locked (from R-0116 DQ1–DQ10; DEC-0131 Accepted) |
| companion_DEC | DEC-0131 (Accepted) |
| research_anchor | R-0116 (DQ1–DQ10 LOCKED) |
| architecture_anchor | docs/engineering/architecture.md # US-0131 |
| orchestrator_run_id | auto-20260907-us0131 |
| fresh_context_marker | tl-US0131-sprint-plan-20260907T194500Z-fresh |
| timestamp | 2026-09-07T19:45:00Z (UTC) |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required on isolation) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 9 (T-anch + T-001..T-008; within 12; no split; T-009 folded into T-007 per critic NB3) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | PASS — `sprints/S0133/plan-verify.json` (`plan_verified_at=2026-09-07T19:52:00Z`, qa `qa-US0131-plan-verify-20260907T195200Z-fresh`) |
| backlog_status | OPEN (US-0045 — not mutated; AC-1..AC-8 unchecked) |
| sibling_out_of_scope | US-0132 |
| critic_carry_ins | 0 blocking; 3 architecture critic NBs `us0131arc-*` resolved non-blocking — routed below |

## Scope summary

Close the **cross-host Its-Magic runtime-configuration gap**. Shared lifecycle/governance settings resolve through host-neutral `.its-magic/config{,.local,.example}.json`. Cursor scratchpad remains DEC-0055 Model B + DEC-0039 compatibility adapter. OpenCode-only installs resolve shared settings without `.cursor/`. Shared Python kernel migrates off silent `.cursor/scratchpad*` hardcodes via `host_runtime_config_lib.resolve_runtime_config`. Host-specific capabilities fail/skip with reason codes. Ten `test_us0131_*` markers. US-0132 model catalogs / `MODEL_*` / materializers remain OUT OF SCOPE.

**Approach A1** (DEC-0131 Accepted): kit JSON SOT + LegacyScratchpadAdapter + resolver injection.

Out of scope: US-0132; amending DEC-0086/0087/0123; cloning Cursor command/rule bodies; dumping kit keys into `opencode.json`; reopening BUG-0015/BUG-0016; marking US-0131 DONE; ticking AC checkboxes.

## Critic NB closures routed into tasks (architecture sovereign-critic)

| NB | Finding / issue | Sprint-plan lock |
|---|---|---|
| NB1 | `host_mode=None` detection vs explicit OpenCode-only for `HOST_CONFIG_PATH_FORBIDDEN` | **T-001 / T-003**: `host_mode=None` = auto-detect from install surface (presence of `.opencode/` vs `.cursor/` without treating None as OpenCode-only). `HOST_CONFIG_PATH_FORBIDDEN` only when `host_mode="opencode"` (or detected OpenCode-only) **and** caller asks to treat `.cursor/` as sole SOT. |
| NB2 | T-004 hardcode inventory completeness (R1) | **T-004**: exhaustive R-0116 inventory — all 9 shared-kernel modules listed; marker 8 greps each. |
| NB3 | T-009 fold-candidate into T-007 | **Applied**: T-009 folded into **T-007**; marker 9 `test_us0131_model_keys_ignored_us0132_boundary` retained in the locked 10-marker table. No separate T-009. |

## Acceptance criteria (8) — US-0131 (status OPEN, unchecked per US-0045)

- **AC-1**: Host-neutral typed config contract (no credentials/secrets).
- **AC-2**: Cursor scratchpad compatibility adapter (DEC-0055/0039) into neutral contract.
- **AC-3**: OpenCode-only resolves shared settings without `.cursor/scratchpad*`.
- **AC-4**: Shared-kernel scripts accept resolved config explicitly (no silent `.cursor` hardcode for host-neutral behavior).
- **AC-5**: Host-specific capabilities classified; fail/skip deterministically; no silent unsupported parity.
- **AC-6**: `--host both` deterministic precedence; no conflicting duplicate writes; independent host-local overrides.
- **AC-7**: Installer delivers examples, preserves locals, never overwrites active scratchpad/config.
- **AC-8**: Cross-host contract tests + docs (precedence, migration, reason codes).

## Task summaries (9 — T-anch + T-001..T-008)

- **T-anch** (NO-OP / verification): Verify `# US-0131` H1 + DEC-0131 Accepted + A1 + R-0116 + 10-marker list. Record `sprints/S0133/t-anch-verification.md`. No architecture.md mutation in execute.
- **T-001** (AC-1): Schema v1 + `.its-magic/config.example.json` + `scripts/host_runtime_config_lib.py` `resolve_runtime_config` (pin `host_mode=None` auto-detect).
- **T-002** (AC-2): LegacyScratchpadAdapter — Model B pre-merge within Cursor layers, then map into shared namespace.
- **T-003** (AC-3): OpenCode-only resolve path from `.its-magic/` + defaults; `HOST_CONFIG_PATH_FORBIDDEN` only on explicit/detected OpenCode-only + forbidden `.cursor`-as-sole-SOT request.
- **T-004** (AC-4): Migrate exhaustive shared-kernel hardcode inventory to resolver (9 modules).
- **T-005** (AC-5, AC-6): Capability matrix + both-host precedence (DQ6) + `HOST_CONFIG_KEY_SHADOWED`.
- **T-006** (AC-7): Installer/manifest kernel delivery of example; never overwrite locals; materialize missing baseline.
- **T-007** (AC-8): `tests/us0131_contract_test.py` — **all 10 markers** (includes former T-009 marker 9) + template mirror.
- **T-008** (AC-8): Runbook h2 + README + auto-orchestration-reference + US-0126 additive `HOST_CONFIG_*` rows only.

Execution order: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 (acyclic; lib before callers; tests after migration; docs last).

## AC → Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (host-neutral SOT) | T-001, T-007 (marker 1, 6) |
| AC-2 (Cursor adapter) | T-002, T-007 (marker 2) |
| AC-3 (OpenCode-only) | T-003, T-007 (marker 3) |
| AC-4 (shared-kernel migration) | T-004, T-007 (marker 8) |
| AC-5 (capability matrix) | T-005, T-007 (marker 10) |
| AC-6 (both-host determinism) | T-005, T-007 (markers 4, 5) |
| AC-7 (installer safety) | T-006, T-007 (marker 7) |
| AC-8 (tests + docs) | T-007 (all 10 markers incl. marker 9), T-008 |
| DC / DEC baseline | T-anch |

**Surjectivity check**: 8/8 ACs covered (each AC ≥1 task). No `PLAN_AC_COVERAGE_GAP`. Marker 9 retained inside T-007 (T-009 folded).

## Locked 10-marker table (R-0116 DQ9 / architecture)

1. `test_us0131_neutral_path_no_cursor_required`
2. `test_us0131_cursor_adapter_preserves_dec0055_precedence`
3. `test_us0131_opencode_only_resolves_shared_from_its_magic`
4. `test_us0131_both_host_precedence_table`
5. `test_us0131_rejects_opencode_json_governance_dump`
6. `test_us0131_schema_fail_closed_codes`
7. `test_us0131_installer_preserves_local_config`
8. `test_us0131_shared_kernel_uses_resolver_not_hardcode`
9. `test_us0131_model_keys_ignored_us0132_boundary` ← former T-009; owned by T-007
10. `test_us0131_capability_matrix_reason_codes_documented`

## T-004 exhaustive migration inventory (NB2 / R1)

| # | Module | Role |
|---|---|---|
| 1 | `scripts/auto_outer_driver.py` | `_merge_scratchpad` — outer-driver autonomy gates |
| 2 | `scripts/opencode_auto_bridge.py` | `_merge_scratchpad` — OpenCode first-phase selection |
| 3 | `scripts/enforce-triad-hot-surface.py` | example/base/local merge for triad thresholds |
| 4 | `scripts/dev_environment_lib.py` | `SCRATCHPAD_*_REL` constants + merge |
| 5 | `scripts/caveman_compress_input.py` | baseline scratchpad path |
| 6 | `scripts/parallel_dev_arbiter.py` | default `.cursor/scratchpad.md` |
| 7 | `scripts/uat_probe_lib.py` | scratchpad pair merge |
| 8 | `scripts/validate_autonomy_stop_matrix.py` | scratchpad path default |
| 9 | `scripts/model_tier_validate.py` | path inject only — **ignore `MODEL_*`** (US-0132) |

Cursor-only parity tooling stays Cursor-scoped (not migrated): `check-scratchpad-pair-parity.py`, `check_intake_template_parity.py`, `validate_doc_profile.py`, `sync_push_gates.py`.

## Risks (R1–R5 — accepted)

| Risk | Severity | Mitigation |
|---|---|---|
| R1 migration miss | MEDIUM | T-004 exhaustive list + marker 8 |
| R2 both-host shadow | LOW–MEDIUM | T-005 `HOST_CONFIG_KEY_SHADOWED` + T-008 docs |
| R3 schema churn | LOW | T-001 `schema_version` + marker 6 |
| R4 installer overwrite | MEDIUM | T-006 + marker 7 + DEC-0039 |
| R5 US-0132 boundary leak | MEDIUM | T-007 marker 9 + ignore `MODEL_*` |

## Compose guards (UNCHANGED)

| Target | Result |
|---|---|
| US-0073 / DEC-0055 | compose — adapter preserves Model B |
| DEC-0039 | compose — never overwrite locals |
| US-0121 / DEC-0120 | compose — example is kernel path |
| US-0122..US-0126 | compose — additive `HOST_CONFIG_*` rows only |
| US-0092 / US-0069 | compose — unchanged |
| US-0132 | OUT OF SCOPE |
| BUG-0015 / BUG-0016 | DONE — do not reopen |
| US-0045 | Status stays OPEN |

## Phase role matrix (after sprint-plan)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh) | {phase_id:plan-verify, role:qa} — consume PENDING plan-verify.json |
| /execute | dev (fresh) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0131 |
| sprint_id | S0133 |
| orchestrator_run_id | auto-20260907-us0131 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0131-sprint-plan-20260907T194500Z-fresh |
| timestamp | 2026-09-07T19:45:00Z (UTC) |
| model_id | composer-2.5 (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0133/sprint.md, tasks.md, progress.md, plan-verify.json (PENDING), uat.json, uat.md, handoffs/tl_to_dev.md, handoffs/qa_plan_verify.md, docs/engineering/state.md, docs/product/backlog.md sprint_plan_notes, handoffs/resume_brief.md |

Prior phase proof consumed: `rp-auto-20260907-us0131-architecture-techlead-20260907T193500Z-US-0131` / `F31B058CC5CDEAF68EDD2F53F4EF790D1845CE842E2B16057247CF5FE4170C4C` — RUNTIME_PROOF_VALID (MATCH before TTL 2026-09-07T20:35:00Z; consumed 2026-09-07T19:45:00Z). Sovereign-critic architecture PASS (`critic-US0131-architecture-20260907T194000Z-fresh`; anti_slop=10; 0 blocking; NBs routed).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260907-us0131-sprint-plan-techlead-20260907T194500Z-US-0131 |
| proof_issued_at | 2026-09-07T19:45:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-09-07T20:45:00Z (UTC) |
| proof_hash | 96221EF4BC1FB83F9A0C288287672F1A18ACC023C80185029EA3A6DDABD84E66 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"composer-2.5","orchestrator_run_id":"auto-20260907-us0131","phase_id":"sprint-plan","proof_issued_at":"2026-09-07T19:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260907-us0131-sprint-plan-techlead-20260907T194500Z-US-0131","sprint_id":"S0133","story_id":"US-0131"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| missing_acceptance_criteria | none (8/8 ACs surjective) |
| task_count | 9 ≤ 12 |
| approach | A1 locked |
| companion_DEC | DEC-0131 Accepted |
| plan-verify | PENDING for qa |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 9 tasks (T-anch + T-001..T-008) within SPRINT_MAX_TASKS=12; T-009 folded into T-007
- [x] 8/8 ACs surjective; marker 9 retained
- [x] Critic NB1–NB3 routed
- [x] plan-verify.json PENDING
- [x] UAT placeholders
- [x] Traceability PLANNED
- [x] tl_to_dev + qa_plan_verify handoffs
- [x] Backlog Status OPEN + sprint_plan_notes
- [x] Isolation + DEC-0038 proof

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` |
| next_scheduled_role | dev |
| stop_condition | STOP after plan-verify PASS. Orchestrator may run sovereign-critic of plan-verify (CROSS_MODEL_REVIEW=1), then spawn `/execute` in fresh dev subagent (BUG-0006). Do NOT spawn execute from plan-verify qa. Do NOT mark US-0131 DONE. Do NOT work US-0132. |
