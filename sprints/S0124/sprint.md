# Sprint S0124 - Sprint Plan (US-0124)

## Metadata

| Field | Value |
|---|---|
| story_id | US-0124 |
| story_title | OpenCode orchestrator plugin Task-spawns US-0069 roles, never executes phase work in-session |
| sprint_id | S0124 |
| delivery_mode | ultra_lean |
| macro_phase | plan (sprint-plan — terminal canonical phase per ultra_lean; /plan-verify runs standalone per orchestrator brief, role=qa) |
| current_phase | sprint-plan |
| approach | A1 locked |
| companion_DEC | DEC-0124 (Accepted) |
| research_anchor | R-0109 (DQ1..DQ8 LOCKED for US-0124; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 locks preserved) |
| orchestrator_run_id | auto-20260824-02 |
| fresh_context_marker | tl-US0124-sprint-plan-20260824T190000Z-fresh |
| timestamp | 2026-08-24T19:00:00Z (UTC) |
| verdict | PASS |
| decision_gate | false |
| SPRINT_MAX_TASKS | 12 |
| SPRINT_AUTO_SPLIT | 1 |
| task_count | 10 (T-anch + T-001..T-009; within 12; no split) |
| CROSS_MODEL_REVIEW | 1 (model_id=glm-5.2-high required) |
| COMPONENT_SCOPE_MODE | 0 |
| USER_GUIDE_MODE | 0 |
| plan-verify | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| backlog_status | OPEN (US-0045 — not mutated) |
| ac_checkboxes | unchecked (US-0045 — not mutated) |

## Scope summary

Ship the fourth slice of the OpenCode adapter epic (US-0121..US-0126): the **orchestrator plugin** that makes `/auto` spawn-only on the OpenCode host. The plugin **is** the OpenCode native chain (do NOT port US-0095 Cursor Task-loop per AC-9). It resolves `phase_id → role` via US-0069 / DEC-0051, spawns an isolated child session via v2 `ctx.session.create({ parentID, agent, prompt })`, asserts `sessionID !== parentID` (DQ5 hard post-condition), writes isolation evidence, honors the US-0092 stop matrix via a Python subprocess callout to `scripts/auto_outer_driver.py`, and refuses orchestrator (or any role) performing another role's artifact writes via a `ctx.tool.hook("execute.before", ...)` write-guard.

This is an **additive plugin + mock-harness + stub-table** change. US-0124 adds: (a) one new template plugin file `template/.opencode/plugins/orchestrator.ts`; (b) one new mock-ctx harness `tests/us0124/mock_ctx.ts`; (c) one new contract test file `tests/us0124_contract_test.py` (9 markers); (d) one stub runbook h2 one-liner per code; (e) one additive CLI extension on `scripts/auto_outer_driver.py` (T-004 — legacy behavior byte-identical when new flags absent); (f) installer manifest rows for the plugin file; (g) `--scope=opencode-adapter` parity extension; (h) README cross-link. Template agent files (`template/.opencode/agents/*.md`) are NOT edited by US-0124 — the plugin composes with the US-0122 `auto.md` agent (DQ8 — independent surfaces, defense in depth).

Four new `OPENCODE_*` reason codes (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + three reused codes (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`). `OPENCODE_DRIVER_INVOKE_FAILED` (driver subprocess failure) is distinct from `OPENCODE_HEADLESS_UNSUPPORTED` (missing `opencode run` CLI surface only) — critic NB `ik_us0124_dq6_driver_fail_code_conflation` closed.

Out of scope: US-0125 (thin command bodies), US-0126 (full runbook — owns the full reason-code table text; US-0124 ships stub only), repo-root `opencode.json`, active kit `.opencode/agents/` mirror, kit-operated proxy for Chinese APIs, Cursor BYOK fixes, embedding keys, live OpenCode runtime probe in CI (AC-10 — DQ3 mock-ctx harness), TS reimplementation of US-0092 state machine (forbidden — DQ6; Python remains SOT), new validator script (default rejected — extend contract tests + `model_tier_validate.py --scope opencode-catalog` from US-0123).

## Acceptance criteria (11) - US-0124 (status OPEN, checkboxes untouched per US-0045)

- **AC-1**: Spawn-only `/auto` — orchestrator plugin/primary agent must not write phase artifacts in its own session. Attempt → fail-closed `AUTO_ORCHESTRATOR_PHASE_EXECUTION` analogue.
- **AC-2**: US-0069 resolve — next phase maps to the matrix role; wrong-role spawn fails closed `PHASE_ROLE_MISMATCH` analogue.
- **AC-3**: Isolation evidence — each spawned session records `phase_id`, `role`, `fresh_context_marker`, timestamp (US-0023 / US-0048 pattern).
- **AC-4**: Success test (a) — contract/harness proves a prompt-ignoring orchestrator still cannot skip spawn isolation (same-session roleplay is rejected).
- **AC-5**: Success test (d) — `/auto` cannot continue to the next phase without a fresh session for the next role.
- **AC-6**: Stop matrix — plugin/outer-driver honors US-0092 stop reasons (decision_gate, loop_max, blocked, pause). No silent continue.
- **AC-7**: Headless `--invoke-cmd` — US-0092 outer driver can invoke OpenCode non-interactive/session API; when native in-session chain is unavailable, emit `NATIVE_CHAIN_UNAVAILABLE` analogue rather than roleplay.
- **AC-8**: Subtask-ignored fail-closed — if OpenCode V2 command `subtask` (or equivalent) is ignored and child sessions cannot be isolated, fail closed with a documented `OPENCODE_*` reason code; do not degrade to one-chat multi-role (R-0001 / R-0109).
- **AC-9**: No US-0095 port — `.cursor/commands/auto.md` Cursor Task-chain prose is not copied into the plugin. Cursor `/auto` remains for the Cursor host.
- **AC-10**: Contract tests — `test_us0124_*` cover spawn-only deny, isolation evidence fields, stop-matrix wiring, `--invoke-cmd` hook, and subtask-ignored fail-closed.
- **AC-11**: Secrets — plugin logs must not print API keys or `.env` contents (US-0085 posture).

## Task summaries (10 - T-anch + T-001..T-009)

- **T-anch** (NO-OP / verification): Verify `# US-0124` H1 anchor in `docs/engineering/architecture.md` AFTER `# US-0123` and BEFORE `# US-0089` (DEC-0073 §11); verify DEC-0124 Accepted (§1–§10); verify compose guards 9/9 UNCHANGED baseline; verify 9-marker contract-test list locked in architecture AC-10 table; verify plugin entry-point + spawn API + stop-matrix argv + agent/plugin boundary locked in DEC-0124 §1–§8; verify `template/.opencode/plugins/orchestrator.ts`, `tests/us0124/mock_ctx.ts`, `tests/us0124_contract_test.py` do NOT yet exist; verify `scripts/auto_outer_driver.py` does NOT yet have the new argv; verify `docs/engineering/runbook.md` does NOT yet have `## OpenCode orchestrator plugin reason codes (US-0124)` h2; verify `[opencode_install_include_paths]` exists but does NOT yet list `template/.opencode/plugins/orchestrator.ts`. Record to `sprints/S0124/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `architecture.md` or `DEC-0124.md` in /execute (mirrors US-0122 / US-0123 T-anch ceremony). (AC-9, AC-10 baseline; NO-OP / verification only)
- **T-001** (NEW plugin file): Create `template/.opencode/plugins/orchestrator.ts` per architecture DQ1 + DQ2 + DQ8 LOCKED + DEC-0124 §1, §2, §8. Canonical v2 module shape: `import { Plugin } from "@opencode-ai/plugin"; export default Plugin.define({ id: "its-magic.orchestrator", setup(ctx) { ... } })`. Auto-discovered via `.opencode/plugins/` scan — no `plugins[]` entry in `opencode.json` required. `setup(ctx)` registers: (a) `ctx.tool.hook("execute.before", ...)` write-guard detecting `AUTO_ORCHESTRATOR_PHASE_EXECUTION`; (b) spawn entry point resolving `phase_id → role` via US-0069 / DEC-0051, calling `ctx.session.create({ parentID, agent, prompt })`, asserting `sessionID !== parentID` (DQ5 hard post-condition), `ctx.session.wait(sessionID)`, persisting isolation evidence; (c) subprocess callout to `scripts/auto_outer_driver.py` for stop-matrix decisions (DQ6 — additive argv; Python SOT unchanged; forbidden TS reimpl). If `ctx.session.create` unavailable → fail closed `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`. Three-case subtask-ignored matrix (null/throw/identical-id) → `OPENCODE_SUBTASK_IGNORED` (DQ5). Throw-discrimination: missing-primitive throw → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`; otherwise → `OPENCODE_SUBTASK_IGNORED`. Plugin MUST NOT copy agent's permission array (DQ8 — no `edit:`/`bash:` literals, no 7 role names hardcoded). Plugin MUST NOT clone `.cursor/commands/auto.md` prose (AC-9). Plugin source has zero vendor model slugs (US-0102 / DEC-0087). (AC-1, AC-2, AC-3, AC-9)
- **T-002** (NEW mock-ctx harness): Create `tests/us0124/mock_ctx.ts` per architecture DQ3 LOCKED + DEC-0124 §3. `MockCtx` implements the v2 plugin context subset: `ctx.session.create`, `ctx.session.prompt`, `ctx.session.wait`, `ctx.tool.hook` (no-op recorder), `ctx.options` (readonly). `MockCtx.session.create` accepts scripted `nextSessionID` + optional `throwOnCreate` + `returnNull` + `identicalID` flags. Default: fresh uuid ≠ `parentID`. Tests load `template/.opencode/plugins/orchestrator.ts` via dynamic import, call `setup(mockCtx)`, drive spawn entry, assert call args + `sessionID !== parentID` + isolation evidence persisted. **Runner: Node** (CI already has it via `tests/run-tests.ps1 Ensure-NodeOnPath`); Bun optional. No live OpenCode runtime probe in CI (AC-10). (AC-3, AC-4, AC-10)
- **T-003** (Runbook stub — byte-identical mirror): Add `## OpenCode orchestrator plugin reason codes (US-0124)` h2 to `docs/engineering/runbook.md` as a **stub one-liner per code** per DEC-0124 §4 / DQ4 LOCKED. List four new `OPENCODE_*` codes + three reused codes with one-line semantics + fail-closed action each. Cross-link to US-0126 for the full table (T-008 owns the cross-link placeholder). US-0126 owns the full runbook section text; US-0124 ships stub only — no duplication of remediation text. **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically. T-003 does NOT author a full runbook section (YAGNI — US-0126 owns it). (AC-8)
- **T-004** (Subprocess argv contract — additive CLI extension): Extend `scripts/auto_outer_driver.py` with additive argv `--phase <phase_id> --role <role> --story <story_id> --sprint <sprint_id> --orchestrator-run-id <run_id> --stop-reason <reason>` per architecture DQ6 LOCKED + DEC-0124 §6. When the new flags are present, the driver returns JSON on stdout: `{ "action": "spawn_next" | "hard_stop" | "ledger_write" | "pause_boundary", "next_phase": "<phase_id>", "stop_reason": "<reason>", ... }`. When new flags are **absent**, existing behavior is byte-identical (no regression to US-0092 / DEC-0078) — additive CLI surface only. Plugin parses JSON and dispatches (`spawn_next` → `ctx.session.create`; `hard_stop` → emit + halt; `ledger_write` → write + continue; `pause_boundary` → emit + halt). Plugin does NOT own stop-reason logic; Python remains SOT. **Subprocess error-handling contract** (critic NB `ik_us0124_dq6_driver_fail_code_conflation` closed): non-zero exit / malformed JSON / timeout → `OPENCODE_DRIVER_INVOKE_FAILED` (NOT `OPENCODE_HEADLESS_UNSUPPORTED`); `opencode run` CLI missing on PATH (DQ7 headless path, separate from DQ6) → `OPENCODE_HEADLESS_UNSUPPORTED`. The two codes are distinct and never overlap. (AC-6)
- **T-005** (Contract tests + template mirror): Create `tests/us0124_contract_test.py` with 9 markers per architecture AC-10 table + DEC-0124 §9. Markers: (1) `test_us0124_spawn_isolation_static` [AC-1, AC-3]; (2) `test_us0124_spawn_isolation_runtime` [AC-3, AC-4, AC-10]; (3) `test_us0124_subtask_ignored_null_return` [AC-8]; (4) `test_us0124_subtask_ignored_throw` [AC-8]; (5) `test_us0124_subtask_ignored_identical_id` [AC-8]; (6) `test_us0124_no_cursor_auto_clone` [AC-9]; (7) `test_us0124_agent_plugin_compose` [AC-1, AC-9]; (8) `test_us0124_invoke_cmd_hook` [AC-7]; (9) `test_us0124_secrets_no_logging` [AC-11]. Marker 4 includes throw-discrimination rule (generic throw → `OPENCODE_SUBTASK_IGNORED`; missing-primitive throw → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`). Marker 7 asserts: both `template/.opencode/agents/auto.md` + `template/.opencode/plugins/orchestrator.ts` exist; plugin source has zero matches for 7 role names + `edit:`/`bash:` literals; `ctx.tool.hook("execute.before")` callback present and calls stop-matrix subprocess for `AUTO_ORCHESTRATOR_PHASE_EXECUTION` detection. Marker 8 asserts argv construction `opencode run --agent auto --format json --auto "<prompt>"` + JSON parsing OR fail-closed `OPENCODE_HEADLESS_UNSUPPORTED`; not a live OpenCode probe. Marker 9 greps plugin source + harness for `api_key`/`apikey`/`sk-`/`auth.json`/`.env` — zero hits in log/print/error paths. Mirror to `template/tests/us0124_contract_test.py` byte-identical for parity pairing. (AC-10, AC-11)
- **T-006** (Installer manifest rows): Add `template/.opencode/plugins/orchestrator.ts` source row under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows UNCHANGED — additive row only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose; `host_gates_cursor_row` predicate). (AC-1)
- **T-007** (README + parity extension): Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover the plugin file + mock harness + contract-test surface (byte-identical active ↔ template pairs where applicable; materializer is kit-only, not paired). Update `its_magic/README.md` to cross-link the OpenCode orchestrator plugin capability + pointer to DEC-0124. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-10)
- **T-008** (Runbook cross-link placeholder to US-0126): Add a one-line cross-link placeholder in the US-0124 runbook h2 stub (added in T-003) pointing to US-0126 for the full reason-code table. US-0126 owns the full table text; US-0124 ships the cross-link anchor only. **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically. (AC-8)
- **T-009** (Validator extension — default no new script): Default = extend contract tests (T-005) + reuse `scripts/model_tier_validate.py --scope opencode-catalog` from US-0123; do NOT create a new `scripts/opencode_plugin_validate.py`. Fall back to a new validator script ONLY if US-0124 plugin source needs static validation beyond contract tests AND coupling forces a separate validator class (trigger: plugin-specific checks cannot reuse >50% of existing `--scope opencode-catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes). If fallback triggers, raise a DEC follow-up; do NOT silently split. (AC-10)

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (spawn-only deny) | T-001, T-005 (markers 1, 7), T-006 |
| AC-2 (US-0069 resolve) | T-001, T-005 (marker 1) |
| AC-3 (isolation evidence) | T-001, T-002, T-005 (markers 1, 2) |
| AC-4 (success test a) | T-002, T-005 (marker 2) |
| AC-5 (success test d) | T-002, T-005 (marker 2 + marker 8) |
| AC-6 (stop matrix) | T-004, T-005 (marker 8) |
| AC-7 (headless --invoke-cmd) | T-004, T-005 (marker 8) |
| AC-8 (subtask-ignored fail-closed) | T-003, T-005 (markers 3, 4, 5) |
| AC-9 (no US-0095 port) | T-anch (baseline), T-005 (markers 6, 7) |
| AC-10 (contract tests) | T-002, T-005 (all 9 markers), T-007 (parity) |
| AC-11 (secrets) | T-005 (marker 9) |

**Surjectivity check**: 11/11 ACs covered (each AC has at least 1 task). No `PLAN_AC_COVERAGE_GAP`.

## Critic carry-ins (3 non-blocking findings from research sovereign-critic — closed in architecture, not silently dropped)

- `ik_us0124_dq6_driver_fail_code_conflation` → T-004 task note: distinct `OPENCODE_DRIVER_INVOKE_FAILED` (driver subprocess failure: non-zero exit, malformed JSON, timeout) vs `OPENCODE_HEADLESS_UNSUPPORTED` (missing `opencode run` CLI surface only). The two codes never overlap.
- `ik_us0124_dq6_argv_extension_gap` → T-004 task note: additive argv extension on `scripts/auto_outer_driver.py`; existing behavior byte-identical when new flags absent (no regression to US-0092 / DEC-0078).
- `ik_us0124_research_scope_yagni` → closed informational; US-0124 ships minimum plugin + harness + stub table; US-0125/US-0126 own command-body and full-runbook surfaces.

## Compose guards (9/9 UNCHANGED — additive plugin + mock-ctx harness + stub table only)

| Compose target | Verification | Result |
|---|---|---|
| US-0069 / DEC-0051 (phase→role matrix) | plugin resolves `phase_id → role` via matrix; no matrix rewrite | ✅ untouched |
| US-0092 / DEC-0078 (outer driver + stop reasons + `--invoke-cmd`) | Python SOT unchanged; plugin calls subprocess (DQ6); `--invoke-cmd` maps to `opencode run` (DQ7) | ✅ untouched |
| US-0095 / DEC-0080 (Cursor native Task-loop) | NOT ported — plugin IS the OpenCode native chain; no `.cursor/commands/auto.md` clone (AC-9) | ✅ NOT ported |
| US-0023 / US-0048 / BUG-0006 (spawn-only isolation) | `ctx.session.create` + `parentID` + `sessionID !== parentID` assertion; fail-closed on no-op spawn | ✅ compose |
| US-0005 (Cursor hook JSON) | NOT ported — enforcement moves into plugin (`ctx.tool.hook`) + agent permissions | ✅ NOT ported |
| US-0122 / DEC-0122 (`auto.md` agent) | US-0124 does not edit `template/.opencode/agents/auto.md`; agent = prompt + permission allow-list; plugin = enforcement (DQ8) | ✅ untouched |
| US-0121 / DEC-0120 (host default cursor-only + reserved `template/.opencode/plugins/`) | plugin lives in reserved slot; no `opencode.json` in template | ✅ consumed |
| US-0125 (thin commands Layer 3 only) | plugin must not own command bodies | ✅ untouched |
| US-0102 / DEC-0087 (no vendor slugs in `template/`) | plugin source has no vendor model slugs | ✅ untouched |

Contract test `test_us0124_agent_plugin_compose` (marker 7) + `test_us0124_no_cursor_auto_clone` (marker 6) enforce at execute boundary.

## Task dependency graph

```
[T-anch] --> [T-001] (plugin file) --> [T-002] (mock-ctx harness, after T-001)
                                          |
                                          v
                                      [T-004] (additive argv on auto_outer_driver.py, after T-001)
                                          |
                                          v
                                      [T-006] (manifest rows, after T-001) - parallel with T-007
                                          |
                                          v
                                      [T-007] (README + parity, after T-001 + T-006)
                                          |
                                          v
                                      [T-003] (runbook stub h2, after T-001) --> [T-008] (runbook cross-link, after T-003)
                                          |
                                          v
                                  [T-005] (contract tests last, assert all outputs)
                                          |
                                          v
                                  [T-009] (validator extension decision, after T-005)
                                          |
                                          v
                                  Integration verification
```

**Execution order (deterministic)**: T-anch → T-001 (plugin file) → T-002 (mock-ctx harness) → T-004 (additive argv) → {T-006, T-007 parallel (manifest + README/parity)} → T-003 (runbook stub h2) → T-008 (runbook cross-link) → T-005 (contract tests last) → T-009 (validator decision) → integration verification.

## Execute phase role (per DEC-0051 / US-0069)

| Phase | Role | Isolation |
|---|---|---|
| /plan-verify | qa (fresh per BUG-0006) | {phase_id:plan-verify, role:qa} — standalone per orchestrator brief |
| /execute | dev (fresh per BUG-0006) | {phase_id:execute, role:dev} |
| /qa | qa (fresh) | {phase_id:qa, role:qa} |
| /verify-work | qa (fresh) | {phase_id:verify-work, role:qa} |
| /release | release (fresh) | {phase_id:release,role:release} |
| /closure | qe (fresh) | {phase_id:closure, role:qe} |
| /refresh-context | curator (fresh) | {phase_id:refresh-context, role:curator} |

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

| Field | Value |
|---|---|
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0124 |
| sprint_id | S0124 |
| orchestrator_run_id | auto-20260824-02 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| fresh_context_marker | tl-US0124-sprint-plan-20260824T190000Z-fresh |
| timestamp | 2026-08-24T19:00:00Z (UTC) |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| evidence_ref | sprints/S0124/sprint.md, sprints/S0124/tasks.md, sprints/S0124/progress.md, sprints/S0124/uat.json, sprints/S0124/uat.md, sprints/S0124/t-anch-verification.md, handoffs/tl_to_dev.md (US-0124 prepend), docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0124, decisions/DEC-0124.md |

Prior phase proof consumed: `rp-auto-20260824-02-architecture-tech-lead-20260824T183000Z-US-0124` (proof_hash=9FFF0B5A30F1A2711A966539B6ED043ADE53B6842C86D64D6A391A2DDF9D2A0A, ttl 2026-08-24T19:30:00Z — consumed before RUNTIME_PROOF_STALE). Sovereign-critic architecture PASS at 2026-08-24T18:35:00Z (anti_slop_aggregate=8; 0 blocking findings; 3 research critic NBs closed in architecture phase).

## Runtime proof (DEC-0038)

| Field | Value |
|---|---|
| runtime_proof_id | rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124 |
| phase_id | sprint-plan |
| role | tech-lead |
| story_id | US-0124 |
| sprint_id | S0124 |
| orchestrator_run_id | auto-20260824-02 |
| delivery_mode | ultra_lean |
| macro_phase | plan |
| model_id | glm-5.2-high (CROSS_MODEL_REVIEW=1 — required) |
| proof_issued_at | 2026-08-24T19:00:00Z |
| proof_ttl_seconds | 3600 |
| proof_ttl | 2026-08-24T20:00:00Z (UTC) |
| proof_hash | 377679F3F6292DCC9DBBDA0D971867529FAE67CD41C20FA9B8A5BE49121C73DE |
| canonical_payload | `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T19:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124","sprint_id":"S0124","story_id":"US-0124"}` |

## Decision gate

| Field | Value |
|---|---|
| decision_gate | false |
| stop_conditions_met | yes |
| missing_acceptance_criteria | none (11/11 ACs covered by 9 contract-test markers + compose guards + T-003 runbook stub) |
| compose_guards | 9/9 UNCHANGED (additive plugin + mock-ctx harness + stub table only) |
| dc_check | clean |
| task_count | 10 (within SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1 but no split needed) |
| risks_finalized | 7/7 ACCEPTED (R1..R7 from R-0109 US-0124) + 3 research critic NBs closed (driver_fail_code_conflation; argv_extension_gap; research_scope_yagni) |
| approach | A1 locked |
| Q | DQ1..DQ8 LOCKED for US-0124; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 locks preserved |
| plan-verify readiness | standalone /plan-verify next (role=qa per orchestrator brief); plan-verify.json NOT written in this spawn |
| sovereign_memory_note | `assemble_sovereign_memory_digest(...)` NOT called; no mistakes.jsonl write |

## Definition of done (sprint-plan)

- [x] 10 tasks enumerated (T-anch + T-001..T-009) — within SPRINT_MAX_TASKS=12
- [x] 11/11 ACs covered by 9 contract-test markers + compose guards + T-003 runbook stub (surjective)
- [x] Task dependency graph documented
- [x] Execute phase role matrix documented (including standalone /plan-verify per orchestrator brief)
- [x] Compose guards 9/9 UNCHANGED (additive plugin + mock-ctx harness + stub table only)
- [x] Critic carry-ins (3) explicitly closed (not silently dropped)
- [x] Isolation evidence + runtime proof emitted (model_id=glm-5.2-high present)
- [x] Sprint-plan checkpoint appended to `docs/engineering/state.md` (append-bottom; never truncate)
- [x] Sprint-plan handoff prepended to `handoffs/tl_to_dev.md`
- [x] Sprint-plan PASS prepended to `handoffs/resume_brief.md` (→ /plan-verify, role=qa)
- [x] UAT placeholders written (`uat.json` empty steps, `uat.md` ACs no results)
- [x] Backlog status OPEN (US-0045 — not mutated); AC checkboxes untouched

## Next scheduled phase

| Field | Value |
|---|---|
| next_scheduled_phase | `/plan-verify` (role=qa per orchestrator brief; fresh qa subagent per BUG-0006) |
| next_scheduled_role | qa |
| next_sprint_macro | plan (terminal — /plan-verify is the verification gate before build+verify macro) |
| stop_condition | STOP after sprint-plan completes; hand off via artifacts only to /plan-verify in fresh qa subagent per BUG-0006. Do not spawn /plan-verify from this subagent. |
| artifacts_written | sprints/S0124/sprint.md, sprints/S0124/tasks.md, sprints/S0124/progress.md, sprints/S0124/uat.json, sprints/S0124/uat.md, sprints/S0124/t-anch-verification.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), handoffs/tl_to_dev.md (US-0124 prepend), handoffs/resume_brief.md (sprint-plan PASS prepend → /plan-verify) |
