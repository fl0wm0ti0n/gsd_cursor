# Sprint S0121 - Sprint Plan (US-0121)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0121 |
| story_title | OpenCode template pack and installer --host cursor/opencode/both |
| sprint_id | S0121 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan - terminal canonical phase per ultra_lean) |
| current_phase | sprint-plan |
| approach | A1 locked |
| companion_DEC | DEC-0120 (Accepted) |
| research_anchor | R-0109 (Q6-Q12 LOCKED for execute) |
| orchestrator_run_id | auto-20260823-01 |
| fresh_context_marker | tl-US0121-sprint-plan-20260823T112200Z-fresh |
| timestamp | 2026-08-23T11:22:00Z (UTC) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 10 (T-anch + T-001..T-009; within 12; no split) |
| CROSS_MODEL_REVIEW | 1 (model_id=glm-5.2-high required) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | ultra_lean skips standalone /plan-verify; plan-verify.json written in THIS spawn |
| backlog_status | OPEN (US-0045 - not mutated) |
| ac_checkboxes | unchecked (US-0045 - not mutated) |
## Scope summary

Ship the first vertical slice of the OpenCode adapter epic: empty-but-valid `template/.opencode/` pack (`agents/.gitkeep`, `commands/.gitkeep`, `plugins/README.md`, `.gitignore` Q10 four pattern groups, `README.md`) plus additive `--host cursor|opencode|both` on the existing its-magic installer (US-0008 compose, additive only). Default cursor-only. Parallel manifest sections `[opencode_install_include_paths]` / `[opencode_clean_paths]`. `--host` on JS CLI + PS `-Host` + sh/py `--host` with normalize-then-validate (unknown/duplicate -> `INSTALL_HOST_INVALID`). Kernel paths install regardless of `--host`. Shared `host_gates_cursor_row` predicate across triple-installer. Host-scoped missing/upgrade/clean with `OPENCODE_ORPHANED_BY_CLEAN_CURSOR` / `OPENCODE_STALE_BY_UPGRADE_CURSOR` (and symmetric cursor variants) - no silent deletion. 14 contract-test markers. `--scope=opencode-adapter` parity registered. Minimal docs hook (`--help` + runbook h2). Full runbook US-0126.

Out of scope: US-0122 role agents, US-0123 slugs, US-0124 plugin body, US-0125 command bodies, US-0126 full runbook, repo-root `opencode.json`, active kit `.opencode/` mirror (Q9 YAGNI), VS Code contrib rewrite, OpenCode fork, standalone runtime.

## Acceptance criteria (10) - US-0121 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: `template/.opencode/` tree - valid pack with `agents/`, `commands/`, `plugins/` + gitignore. Empty-but-valid.
- **AC-2**: `--host` flag - installer accepts `--host cursor|opencode|both`. Default = `cursor`. Unknown -> `INSTALL_HOST_INVALID`.
- **AC-3**: Install / upgrade / clean - host-scoped; `.cursor/` untouched when `--host opencode`.
- **AC-4**: Cursor coexistence - `--host cursor` byte-identical on `.cursor/` vs pre-US-0121. `--host both` leaves both trees.
- **AC-5**: Manifest + triple-installer - manifest lists `template/.opencode/**`; PS/Bash/Python honor `--host` with same semantics.
- **AC-6**: Parity - `check_intake_template_parity.py --scope=opencode-adapter` fails on drift.
- **AC-7**: Contract tests - `test_us0121_*` cover default, each `--host`, upgrade/clean, coexistence, invalid, manifest.
- **AC-8**: Compose, do not amend - US-0008 / DEC-0045 / US-0102 / US-0001 / US-0018 unchanged except additive host switch.
- **AC-9**: Docs hook (minimal) - `--help` / runbook mention `--host` + cursor-default lock.
- **AC-10**: No secrets in template - no API keys, `.env` contents, vendor slugs (US-0102).

## Task summaries (10 - T-anch + T-001..T-009)

- **T-anch** (NO-OP / verification): Verify `# US-0121` H1 anchor; DEC-0120 Accepted; compose guards 5/5; mixed-section predicate locked; 14-marker list locked; `template/.opencode/` + `tests/us0121_host_mode_test.py` + opencode manifest sections absent. (AC-8, AC-7 baseline)
- **T-001** (NEW `template/.opencode/` pack): `agents/.gitkeep`, `commands/.gitkeep`, `plugins/README.md`, `.gitignore` (Q10 four groups), `README.md`. No `opencode.json`, no active mirror, no slugs/secrets. (AC-1, AC-10)
- **T-002** (NEW manifest parallel sections): `[opencode_install_include_paths]` + `[opencode_clean_paths]` in active + template manifest byte-identical. Existing sections unchanged. (AC-5)
- **T-003** (`bin/its-magic.js` `--host`): Add argv parser (normalize lowercase+trim, validate, duplicate fail-closed `INSTALL_HOST_INVALID`), forward to PS/Bash, `--help` docs hook. (AC-2, AC-9)
- **T-004** (`installer.ps1` `-Host`): Parameter + normalize + `host_gates_cursor_row` predicate + opencode section reads + host-scoped missing/upgrade/clean + orphan/stale diagnostics. (AC-2, AC-3, AC-5)
- **T-005** (`installer.sh` `--host`): argparse + normalize + same predicate + opencode section reads + same diagnostics. (AC-2, AC-3, AC-5)
- **T-006** (`installer.py` `--host` - manifest authority): argparse + normalize + same predicate + opencode section reads + host-scoped missing/upgrade/clean + orphan/stale diagnostics. Critic carry-in `ik_us0121_missing_overwrite_host_gap`: YAGNI - `missing` after `both` no-ops on `.opencode/` via predicate (copy-if-missing is host-scoped); no new diagnostic needed; overwrite remains US-0008 unchanged. (AC-3, AC-7)
- **T-007** (NEW `tests/us0121_host_mode_test.py` - 14 markers): per architecture marker table. Critic carry-in `ik_us0121_ac9_help_test_yagni`: `--help` grep is marker 9; do not add 15th marker without dropping YAGNI elsewhere. (AC-7)
- **T-008** (`check_intake_template_parity.py --scope=opencode-adapter`): Register scope + `US0121_PARITY_PAIRS`. Critic carry-in `ik_us0121_parity_active_mirror_contradiction`: parity pairs `template/.opencode` with consumed `.opencode/` (when host includes opencode); no kit-repo active mirror (Q9 YAGNI). (AC-6)
- **T-009** (Runbook `## OpenCode host mode (US-0121)` h2 + `--help` line): minimal docs hook. Full runbook US-0126. (AC-9)

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 | T-001 |
| AC-2 | T-003, T-004, T-005, T-006 |
| AC-3 | T-004, T-005, T-006 |
| AC-4 | T-007 (markers 2-4) |
| AC-5 | T-002, T-004, T-005, T-006, T-007 (markers 10, 11, 14) |
| AC-6 | T-008, T-007 (marker 13) |
| AC-7 | T-007 |
| AC-8 | T-anch (baseline), all tasks gated |
| AC-9 | T-003 (`--help`), T-009 (runbook h2) |
| AC-10 | T-001, T-007 (marker 12) |

**Surjectivity check**: 10/10 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Critic carry-ins (3 non-blocking findings from architecture critic - not silently dropped)

- `ik_us0121_missing_overwrite_host_gap` -> T-006 task note (YAGNI with reason; overwrite US-0008 unchanged)
- `ik_us0121_parity_active_mirror_contradiction` -> T-008 task note (parity pairs template with consumed; no kit active mirror per Q9)
- `ik_us0121_ac9_help_test_yagni` -> T-007 task note (marker 9 covers `--help`; no 15th marker)

## Compose guards (5/5 UNCHANGED - additive only)

| Compose target | Verification |
|---|---|
| US-0008 (CLI installer) | additive `--host` only; missing/overwrite/clean/upgrade UNCHANGED |
| DEC-0045 (`its_magic/` ownership) | unchanged |
| US-0102 (volatile-ID rule) | template ships no slugs; `*.local.json{,c}` gitignore mirrors kit convention |
| US-0001 (phase names) | placeholders only; no command body clone |
| US-0018 (packaging delivery) | installer delivery path unchanged except additive `--host` forward |

## Task dependency graph

```
[T-anch] --> [T-001] --> [T-007] (needs T-001..T-006 outputs)
          |-> [T-002] --> [T-004, T-005, T-006] (need opencode sections)
          |-> [T-003] --> [T-004, T-005] (need forward contract)
                       |-> [T-006] (manifest authority)
                              |
                              v
                          [T-008] (parity scope, after T-001 + T-002)
                              |
                              v
                          [T-009] (docs hook, after T-003)
```

**Execution order (deterministic)**: T-anch -> {T-001, T-002, T-003 parallel} -> {T-004, T-005, T-006 parallel} -> T-008 -> T-009 -> T-007 (tests last, assert all outputs) -> integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa}; creates plan-verify.json (ultra_lean merge) |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release, role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0121 |
| sprint_id | S0121 |
| orchestrator_run_id | auto-20260823-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0121-sprint-plan-20260823T112200Z-fresh |
| timestamp | 2026-08-23T11:22:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 - required) |
| evidence_ref | sprints/S0121/sprint.md, sprints/S0121/tasks.md, sprints/S0121/progress.md, sprints/S0121/uat.json, sprints/S0121/uat.md, sprints/S0121/plan-verify.json, handoffs/tl_to_dev.md (US-0121 prepend), docs/engineering/state.md (sprint-plan checkpoint), docs/engineering/architecture.md # US-0121, decisions/DEC-0120.md |

Prior phase proof consumed: `rp-auto-20260823-01-architecture-tech-lead-20260823T111500Z-US-0121` (proof_hash=753a25c11f5ca67aee2e3d4915544d744f3635a1a4433289c03e93c8732ed99e).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0121 |
| sprint_id | S0121 |
| orchestrator_run_id | auto-20260823-01 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| proof_issued_at | 2026-08-23T11:22:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-23T12:22:00Z (UTC) |
| proof_hash | 2a7f31fca177451c935b9aedebb4781d57a7b13d8ef87a9e913fcaf10bec6336 |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260823-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-23T11:22:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (10/10 ACs covered by 14 contract-test markers + compose guards) |
| compose_guards | 5/5 UNCHANGED (additive only) |
| dc_check | clean |
| task_count | 10 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 8/8 ACCEPTED (R1..R8 from R-0109) + C1..C3 critic findings closed |
| approach | A1 locked |
| Q | Q6-Q12 LOCKED for execute; Q1-Q5 LOCKED for architecture only |
| plan-verify readiness | `sprints/S0121/plan-verify.json` written in THIS spawn (ultra_lean skips standalone /plan-verify phase) |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 10 tasks enumerated (T-anch + T-001..T-009) - within SPRINT_MAX_TASKS=12
- [x] 10/10 ACs covered by test markers (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented
- [x] Compose guards 5/5 UNCHANGED
- [x] Critic carry-ins (3) explicitly routed to task notes (not silently dropped)
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md`
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md`
- [x] `sprints/S0121/plan-verify.json` written (coverage matrix, gaps=[])
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Backlog status OPEN (US-0045 - not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/execute` (dev, first phase of build+verify macro per ultra_lean) |
| next_scheduled_role | dev |
| next_sprint_macro | build+verify |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /execute in fresh dev subagent per BUG-0006. Do not spawn /execute from this subagent. |
| artifacts_written | sprints/S0121/sprint.md, sprints/S0121/tasks.md, sprints/S0121/progress.md, sprints/S0121/uat.json, sprints/S0121/uat.md, sprints/S0121/plan-verify.json, docs/engineering/state.md (sprint-plan checkpoint appended), handoffs/tl_to_dev.md (US-0121 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend) |
