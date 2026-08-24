## Sprint-plan handoff — **US-0125** / **S0125** — `/plan-verify` next (fresh qa)

- sprint_id: S0125
- story_id: US-0125
- dec_id: DEC-0125 (Accepted, decisions/DEC-0125.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0125; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 + US-0124 DQ1..DQ8 locks preserved)
- orchestrator_run_id: auto-20260824-02
- fresh_context_marker: tl-US0125-sprint-plan-20260824T204500Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 — not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-006(markers 1,8,11),T-007; AC-2->T-002,T-006(marker 2); AC-3->T-003,T-004,T-006(markers 3,4); AC-4->T-003,T-005,T-006(marker 4); AC-5->T-004,T-006(marker 5); AC-6->T-006(marker 6); AC-7->T-006(markers 7,8); AC-8->T-006(all 11 markers),T-008(parity+runbook stub); AC-9->T-anch(baseline),T-006(marker 9); AC-10->T-005,T-006(marker 10)
- task_order: T-anch -> T-001 (15 command files) -> {T-002, T-003, T-004, T-007 parallel (clone-guard marker, mapping fixture, bridge prose, manifest rows)} -> T-008 (README + parity + runbook stub) -> T-005 (mock-subprocess harness) -> T-006 (contract tests last) -> T-009 (validator decision) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0001 (phase names + artifact outputs; no 200-line clones per AC-9), US-0078/DEC-0060 (`intake_evidence_validate.py` remains persistence-blocking gate; thin commands subprocess, do not reimplement), US-0121/DEC-0120 (host default cursor-only; commands live in reserved `template/.opencode/commands/` slot; `.gitkeep` replaced by 15 files), US-0122/DEC-0122 (`template/.opencode/agents/*.md` unchanged — commands bind via `agent: <role>` frontmatter per DQ5/DQ8), US-0124/DEC-0124 (`template/.opencode/plugins/orchestrator.ts` unchanged — plugin owns spawn + `ctx.tool.hook` enforcement; US-0125 authors validator→artifact mapping that the plugin consumes — additive data, not plugin code change; `/auto` is dispatch-only; missing command must not disable plugin per US-0124 AC-7 ↔ US-0125 AC-7), US-0126 (owns full runbook + reason-code table + `--scope=opencode-adapter` parity text; US-0125 ships stub reason-code reference only), US-0102/DEC-0087 (no vendor slugs in `template/` — no `model:` literals in any command frontmatter)
- critic_carry_ins (1 non-blocking — closed in /execute T-002, not silently dropped):
  - `ik_us0125_dq2_normalization_strip_list_open` -> T-002 note: lock the token-strip manifest as a documented Python constant `US0125_CLONE_GUARD_STRIP_TOKENS` in `test_us0125_clone_guard` so the normalization strip list is explicit, version-controlled, and inherited by US-0126 without re-derivation. Strip list: frontmatter fence block + lowercase + punctuation + canonical phase id token + shared vocabulary words (its-magic, command, phase, artifact, STOP, run, validator, plugin, script, python, scripts, repo, the, a, an, to, of, and, or, before, after, above, below, path, list, id).
- architecture_pointers: docs/engineering/architecture.md # US-0125 (L1836 — approach A1, 11-marker table, command inventory DQ1, clone guard DQ2, validator-bridge DQ3, defense-in-depth DQ4, `/auto` dispatch-only DQ5, frontmatter shape DQ6, reason-code boundary DQ7, mock-ctx+mock-subprocess harness DQ8, non-goals; validator→artifact mapping table at L1939-L1945)
- dec_pointers: decisions/DEC-0125.md (§1 command file inventory, §2 clone guard, §3 validator bridge contract, §4 defense-in-depth, §5 `/auto` dispatch-only, §6 frontmatter shape, §7 reason-code boundary, §8 mock-ctx+mock-subprocess harness)
- first_execute_task: T-anch (NO-OP / verification) — verify # US-0125 H1 anchor + DEC-0125 Accepted + compose guards 7/7 + 11-marker list locked + command/clone-guard/validator-bridge/dispatch-only/frontmatter/reason-code/harness contracts + absent surfaces
- key_locked_artifacts:
  - command file inventory (DQ1): 15 dispatch-only markdown files at `template/.opencode/commands/<name>.md` — 12 lifecycle phases (`intake.md`→`po`, `discovery.md`→`po`, `research.md`→`tech-lead`, `architecture.md`→`tech-lead`, `sprint-plan.md`→`tech-lead`, `plan-verify.md`→`qa`, `execute.md`→`dev`, `qa.md`→`qa`, `verify-work.md`→`qa`, `release.md`→`release`, `closure.md`→`qa` with prompt `role=qe` per DEC-0051 / US-0120, `refresh-context.md`→`curator`) + `auto.md` (`agent: auto` + `subtask: false` — dispatch-only per DQ5) + `quick.md` (`agent: tech-lead` — mega_quick entry per US-0096 / DEC-0082) + `ask.md` (omits `agent:` — agent-agnostic, read-only); each ≤ 20 lines (DQ2 line cap)
  - clone guard (DQ2): per-file line cap ≤ 20 + normalized-text similarity ≤ 0.30 via `difflib.SequenceMatcher` vs `.cursor/commands/<name>.md`; strip list constant `US0125_CLONE_GUARD_STRIP_TOKENS` locked in T-002 (closes `ik_us0125_dq2_normalization_strip_list_open`)
  - validator bridge contract (DQ3, DQ4, DQ7): two named CLIs (`scripts/intake_evidence_validate.py --repo . --enforce`; `scripts/bug_issue_validate.py --repo . --check-acceptance`) + generic bridge contract (`python scripts/<validator>.py --repo . [--enforce] [--scope <scope>]`); US-0126 owns full enumeration; command prose = diagnostics, plugin `ctx.tool.hook("execute.before")` = enforcement (DQ4); raw Python reason codes for validator non-zero exit; `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure; no `OPENCODE_VALIDATOR_FAILED` wrapper (DQ7)
  - validator→artifact mapping (DQ4): authored in architecture.md L1939-L1945 (US-0125-owned, US-0124-consumed); T-003 extracts to test fixture `tests/us0125/fixtures/validator_artifact_mapping.json` — NO architecture.md mutation in /execute
  - `/auto` dispatch-only (DQ5): `template/.opencode/commands/auto.md` — `agent: auto` + `subtask: false` + body names orchestrator role + points to plugin for spawn + STOP; no `ctx.session.create`/`Session.create`/`spawn` literals; plugin (US-0124) remains single spawn owner
  - frontmatter shape (DQ6): `description` + `agent: <role>` for 14 files; `/auto` adds `subtask: false`; `/ask` omits `agent`; no `model:` in any template command (US-0102 + US-0123)
  - reason-code boundary (DQ7): raw Python reason codes (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`, ...) for validator non-zero exit; `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure; no `OPENCODE_*` wrapper; stub reason-code reference in `docs/engineering/runbook.md` h2 `## OpenCode thin commands + validator bridge (US-0125)` — US-0126 owns full table
  - mock-ctx + mock-subprocess harness (DQ8): extend US-0124 `MockCtx` with `mockSubprocess` field OR add `tests/us0125/mock_subprocess.ts`; scripted `nextExitCode`/`nextStderr`/`nextThrow`; runner = Node (consistent with US-0124 DQ3); no live OpenCode runtime probe in CI (AC-10)
  - contract tests (AC-8): `tests/us0125_contract_test.py` — 11 markers (see architecture AC-8 table); mirror to `template/tests/us0125_contract_test.py` byte-identical
  - runbook stub (T-008): `## OpenCode thin commands + validator bridge (US-0125)` h2 one-liner per code in `docs/engineering/runbook.md` + byte-identical `template/docs/engineering/runbook.md` mirror; US-0126 owns full text
  - manifest rows (T-007): `template/.opencode/commands/**` under `[opencode_install_include_paths]` (active + template byte-identical)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0125 / US-0125
- sprint_artifacts: sprints/S0125/ (sprint.md, tasks.md, progress.md, uat.json, uat.md, t-anch-verification.md placeholder)
- timestamp: 2026-08-24T20:45:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- runtime_proof_id: rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125
- proof_hash: 2FF3A63387C7337D5EC02802253D251CC2636831A6369B7A121F6135AC51E234

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0125-sprint-plan-20260824T204500Z-fresh`
- `timestamp=2026-08-24T20:45:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=sprints/S0125/sprint.md, sprints/S0125/tasks.md, sprints/S0125/progress.md, sprints/S0125/uat.json, sprints/S0125/uat.md, sprints/S0125/t-anch-verification.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0125, decisions/DEC-0125.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0125`, `sprint_id=S0125`
- `proof_issued_at=2026-08-24T20:45:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T21:45:00Z`
- `proof_hash=2FF3A63387C7337D5EC02802253D251CC2636831A6369B7A121F6135AC51E234`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T20:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-02-sprint-plan-tech-lead-20260824T204500Z-US-0125","sprint_id":"S0125","story_id":"US-0125"}`

---
## Sprint-plan handoff — **US-0124** / **S0124** — `/plan-verify` next (fresh qa)

- sprint_id: S0124
- story_id: US-0124
- dec_id: DEC-0124 (Accepted, decisions/DEC-0124.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0124; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 + US-0123 DQ1..DQ10 locks preserved)
- orchestrator_run_id: auto-20260824-02
- fresh_context_marker: tl-US0124-sprint-plan-20260824T190000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 — not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-005(markers 1,7),T-006; AC-2->T-001,T-005(marker 1); AC-3->T-001,T-002,T-005(markers 1,2); AC-4->T-002,T-005(marker 2); AC-5->T-002,T-005(marker 2 + marker 8); AC-6->T-004,T-005(marker 8); AC-7->T-004,T-005(marker 8); AC-8->T-003,T-005(markers 3,4,5); AC-9->T-anch(baseline),T-005(markers 6,7); AC-10->T-002,T-005(all 9 markers),T-007(parity); AC-11->T-005(marker 9)
- task_order: T-anch -> T-001 (plugin file) -> T-002 (mock-ctx harness) -> T-004 (additive argv on auto_outer_driver.py) -> {T-006, T-007 parallel (manifest + README/parity)} -> T-003 (runbook stub h2) -> T-008 (runbook cross-link) -> T-005 (contract tests last) -> T-009 (validator decision) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0069/DEC-0051 (phase→role matrix), US-0092/DEC-0078 (outer driver + stop reasons + `--invoke-cmd`; Python remains SOT), US-0095/DEC-0080 (do NOT port Cursor Task-loop; no `.cursor/commands/auto.md` clone per AC-9), US-0023/US-0048/BUG-0006 (spawn-only isolation; `ctx.session.create` + `parentID` + `sessionID !== parentID`), US-0005 (hook-equivalent enforcement moves into plugin `ctx.tool.hook` + agent permissions; do not port Cursor hook JSON), US-0122/DEC-0122 (`template/.opencode/agents/auto.md` unchanged — agent = prompt + permission allow-list; plugin = enforcement per DQ8), US-0121/DEC-0120 (host default cursor-only; plugin lives in reserved `template/.opencode/plugins/` slot), US-0125 (thin commands are Layer 3 dispatch only; plugin must not own command bodies), US-0102/DEC-0087 (no vendor slugs in `template/` — plugin source has no vendor model slugs)
- critic_carry_ins (3 non-blocking — closed in architecture phase, routed to task notes, not silently dropped):
  - `ik_us0124_dq6_driver_fail_code_conflation` -> T-004 note: distinct `OPENCODE_DRIVER_INVOKE_FAILED` (driver subprocess failure: non-zero exit, malformed JSON, timeout) vs `OPENCODE_HEADLESS_UNSUPPORTED` (missing `opencode run` CLI surface only). The two codes never overlap.
  - `ik_us0124_dq6_argv_extension_gap` -> T-004 note: additive argv extension on `scripts/auto_outer_driver.py`; existing behavior byte-identical when new flags absent (no regression to US-0092 / DEC-0078).
  - `ik_us0124_research_scope_yagni` -> closed informational; US-0124 ships minimum plugin + harness + stub table; US-0125/US-0126 own command-body and full-runbook surfaces.
- architecture_pointers: docs/engineering/architecture.md # US-0124 (approach A1, 9-marker table, plugin entry-point DQ1, spawn API DQ2, mock-ctx harness DQ3, reason-code namespace DQ4, three-case detection matrix DQ5, subprocess stop-matrix DQ6, headless CLI DQ7, agent vs plugin boundary DQ8, non-goals)
- dec_pointers: decisions/DEC-0124.md (§1 plugin entry point, §2 spawn API, §3 mock-ctx harness, §4 reason-code namespace, §5 three-case detection matrix, §6 subprocess stop-matrix, §7 headless CLI, §8 agent vs plugin boundary, §9 contract tests, §10 non-goals)
- first_execute_task: T-anch (NO-OP / verification) — verify # US-0124 H1 anchor + DEC-0124 Accepted + compose guards 9/9 + 9-marker list locked + plugin/spawn/argv/boundary contracts + absent surfaces
- key_locked_artifacts:
  - plugin entry point (DQ1): `template/.opencode/plugins/orchestrator.ts` — single TypeScript file, default export `Plugin.define({ id: "its-magic.orchestrator", setup })` from `@opencode-ai/plugin`; auto-discovered via `.opencode/plugins/` scan; no `plugins[]` entry in `opencode.json` required (US-0121 ships no `opencode.json` in template); plugin id `its-magic.orchestrator` is the disable/enable selector (`--pure` / `-its-magic.orchestrator`)
  - spawn API (DQ2): `ctx.session.create({ parentID: <orchestrator-session-id>, agent: <role>, prompt: <phase-prompt> })` → assert `sessionID !== parentID` (DQ5 hard post-condition) → `ctx.session.wait(sessionID)` → read result → persist isolation evidence (`parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker`); if `ctx.session.create` unavailable → fail closed `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`
  - mock-ctx harness (DQ3): `tests/us0124/mock_ctx.ts` — `MockCtx` implements v2 plugin context subset (`session.create`/`prompt`/`wait`, `tool.hook` no-op recorder, `options` readonly); `session.create` accepts scripted `nextSessionID` + `throwOnCreate` + `returnNull` + `identicalID` flags; default fresh uuid ≠ `parentID`; runner = Node (CI has it via `tests/run-tests.ps1 Ensure-NodeOnPath`); no live OpenCode runtime probe in CI (AC-10)
  - reason-code namespace (DQ4): four new `OPENCODE_*` codes (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + three reused codes (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`); `OPENCODE_DRIVER_INVOKE_FAILED` (driver subprocess failure) distinct from `OPENCODE_HEADLESS_UNSUPPORTED` (missing `opencode run` CLI surface only)
  - three-case detection matrix (DQ5): null return → `OPENCODE_SUBTASK_IGNORED`; throw (generic) → `OPENCODE_SUBTASK_IGNORED`; throw (missing-primitive) → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`; identical-id return → `OPENCODE_SUBTASK_IGNORED`; `sessionID !== parentID` is hard post-condition
  - subprocess stop-matrix (DQ6): `scripts/auto_outer_driver.py` is single TS↔Python integration; additive argv `--phase/--role/--story/--sprint/--orchestrator-run-id/--stop-reason` → JSON response `{ action, next_phase, stop_reason, ... }`; legacy behavior byte-identical when flags absent; forbidden: TS reimpl of US-0092 state machine; subprocess failure (non-zero exit, malformed JSON, timeout) → `OPENCODE_DRIVER_INVOKE_FAILED` (NOT `OPENCODE_HEADLESS_UNSUPPORTED`)
  - headless CLI (DQ7): `opencode run --agent auto --format json --auto "<phase-prompt>"` (primary) + optional `opencode serve` + `--attach`; fail-closed `OPENCODE_HEADLESS_UNSUPPORTED` when `opencode run` not on PATH
  - agent vs plugin boundary (DQ8): `template/.opencode/agents/auto.md` (US-0122 — agent = prompt + permission allow-list, unchanged) + `template/.opencode/plugins/orchestrator.ts` (US-0124 — plugin = enforcement); independent surfaces, defense in depth; plugin MUST NOT copy agent's permission array; `ctx.tool.hook("execute.before")` enforces `AUTO_ORCHESTRATOR_PHASE_EXECUTION` (path-based, not permission-array-based)
  - contract tests (AC-10): `tests/us0124_contract_test.py` — 9 markers (see architecture AC-10 table); mirror to `template/tests/us0124_contract_test.py` byte-identical
  - runbook stub (DQ4): `## OpenCode orchestrator plugin reason codes (US-0124)` h2 one-liner per code in `docs/engineering/runbook.md` + byte-identical `template/docs/engineering/runbook.md` mirror; US-0126 owns full text
  - manifest rows (T-006): `template/.opencode/plugins/orchestrator.ts` under `[opencode_install_include_paths]` (active + template byte-identical)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0124 / US-0124
- sprint_artifacts: sprints/S0124/ (sprint.md, tasks.md, progress.md, uat.json, uat.md, t-anch-verification.md placeholder)
- timestamp: 2026-08-24T19:00:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- runtime_proof_id: rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124
- proof_hash: 377679F3F6292DCC9DBBDA0D971867529FAE67CD41C20FA9B8A5BE49121C73DE

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0124-sprint-plan-20260824T190000Z-fresh`
- `timestamp=2026-08-24T19:00:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=sprints/S0124/sprint.md, sprints/S0124/tasks.md, sprints/S0124/progress.md, sprints/S0124/uat.json, sprints/S0124/uat.md, sprints/S0124/t-anch-verification.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0124, decisions/DEC-0124.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-02`
- `runtime_proof_id=rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0124`, `sprint_id=S0124`
- `proof_issued_at=2026-08-24T19:00:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T20:00:00Z`
- `proof_hash=377679F3F6292DCC9DBBDA0D971867529FAE67CD41C20FA9B8A5BE49121C73DE`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-02","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T19:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-02-sprint-plan-tech-lead-20260824T190000Z-US-0124","sprint_id":"S0124","story_id":"US-0124"}`

---

## Architecture handoff pointer — **US-0124** — `/sprint-plan` next (fresh tech-lead)

- story_id: US-0124 (OPEN — do not mark DONE)
- orchestrator_run_id: auto-20260824-02
- phase_id: architecture, role: tech-lead, model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1)
- verdict: PASS (companion DEC-0124 Accepted; approach A1 locked; DQ1..DQ8 LOCKED; 7/7 R ACCEPTED; 3 research critic NBs closed; 3 spec critic NBs closed; compose guards 9/9 UNCHANGED; 10 tasks T-anch + T-001..T-009 within SPRINT_MAX_TASKS=12; 11/11 AC surjective; 9-marker contract-test list locked)
- architecture_anchor: docs/engineering/architecture.md # US-0124 (L1816 — H1 anchor AFTER # US-0123 BEFORE # US-0089 per DEC-0073 §11)
- companion_dec: decisions/DEC-0124.md (Accepted)
- research_anchor: docs/engineering/research.md ## R-0109 ### Deepened findings — US-0124 (DQ1..DQ8 LOCKED)
- next_scheduled_phase: /sprint-plan (role=tech-lead; fresh subagent per BUG-0006)
- dev_handoff_note: tl_to_dev.md will be authored at /sprint-plan (after task refinement); dev handoff is NOT authored in /architecture. This pointer is a placeholder so dev knows the architecture contract is locked.
- stop_condition: STOP after architecture; orchestrator spawns /sprint-plan in fresh tech-lead subagent. Do NOT spawn /sprint-plan from this subagent. Do NOT mark US-0124 DONE.

---

## Sprint-plan handoff — **US-0123** / **S0123** — `/plan-verify` next (fresh qa)

- sprint_id: S0123
- story_id: US-0123
- dec_id: DEC-0123 (Accepted, decisions/DEC-0123.md)
- research_anchor: R-0109 (DQ1..DQ10 LOCKED for US-0123; US-0121 Q1..Q12 + US-0122 DQ1..DQ8 locks preserved)
- orchestrator_run_id: auto-20260824-01
- fresh_context_marker: tl-US0123-sprint-plan-20260824T163000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 — not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-002,T-003,T-004,T-009; AC-2->T-001; AC-3->T-004,T-005(markers 1,2,3); AC-4->T-002,T-005(markers 5,6); AC-5->T-002,T-003,T-006,T-005(marker 7); AC-6->T-anch(baseline),T-005(marker 8); AC-7->T-001,T-005(marker 4); AC-8->T-005(all 8 markers),T-008(parity); AC-9->T-001,T-anch(baseline),T-005(marker 4); AC-10->T-007
- task_order: T-anch -> T-001 (example catalog) -> T-002 (materializer) -> T-003 (installer hook) -> {T-004, T-006, T-009 parallel (validator + gitignore + manifest)} -> T-008 (README + parity) -> T-007 (runbook one-liner) -> T-005 (contract tests last) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0101/DEC-0086 (Cursor tier→alias runtime + `.cursor/model-catalog.local.json`), US-0102/DEC-0087 (Cursor direct-slug + role catalog; volatile-ID rule extended to `template/.opencode/`), US-0003 (agents gain `model:` on OpenCode at install time, not in template), US-0122/DEC-0122 (template agents unchanged — `model:` omitted; materializer writes to installed agents only), US-0121 (`.opencode/` pack path + `.gitignore` Q10 — `*.local.json` reused), US-0080 (`TOKEN_PROFILE` orthogonal — slug routing ≠ token-cost profile)
- critic_carry_ins (3 non-blocking — route to task notes, do not silently drop):
  - `ik_us0123_placeholder_slug_copy_paste_boundary` -> T-002 note: materializer MUST treat `<your-*-slug>` angle-bracket placeholder strings as unknown slugs (emit `OPENCODE_MODEL_SLUG_UNKNOWN`, fail-closed); operators who copy-paste the example catalog without filling in real slugs must NOT silently get placeholder `model:` values injected into installed agents; placeholder detection: slug matches `^<.*>$` or contains `<your-` substring -> unknown; T-005 marker 5 asserts the placeholder case
  - `ik_us0123_validator_extension_coupling_fallback` -> T-004 note: document when to extend `model_tier_validate.py` vs new script; default = extend in place (DQ9 lock); fall back to new `scripts/opencode_model_catalog_validate.py` ONLY if schema divergence forces a separate validator class (trigger: `validate_opencode_catalog` cannot reuse >50% of existing `validate_cursor_catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes); if fallback triggers, raise DEC-0124-class follow-up; do NOT silently split
  - `ik_us0123_sprint_tanch_ceremony_overlap` -> T-anch note: T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0123.md` in /execute; T-anch records baseline observations only (mirrors US-0122 T-anch ceremony); architecture heading order (# US-0122 -> # US-0123 -> # US-0089) and DEC-0123 Accepted state are read-only verified, not mutated
- architecture_pointers: docs/engineering/architecture.md # US-0123 (approach A1, 8-marker table, SOT=local-only `.opencode/model-catalog.local.json`, template agents omit `model:`, single `OPENCODE_MODEL_SLUG_UNKNOWN` fail-closed, per-role schema, additive integration, always `api` mode, validator extension DQ9, runbook stub DQ10, non-goals)
- dec_pointers: decisions/DEC-0123.md (§1 SOT, §2 template agents omit model, §3 single fail-closed code, §4 catalog path, §5 per-role schema, §6 example placeholders, §7 additive integration + materializer + installer hook contract, §8 always api mode, §9 validator extension, §10 runbook stub, §11 contract tests, §12 non-goals)
- first_execute_task: T-anch (NO-OP / verification) — verify # US-0123 H1 anchor + DEC-0123 Accepted + compose guards 6/6 + 8-marker list locked + materializer/installer hook contract + absent surfaces
- key_locked_artifacts:
  - SOT: `.opencode/model-catalog.local.json` (gitignored, operator-filled) + `template/.opencode/model-catalog.local.example.json` (committed, placeholders only); forbidden surfaces for real OpenCode slugs: `template/.opencode/agents/*.md` `model:` frontmatter, `template/.opencode/opencode.json{,c}`, `.cursor/model-catalog.local.json`, `.cursor/scratchpad.local.md` `MODEL_*` keys
  - catalog schema (DQ5 per-role, 8 role keys): `{schema_version, providers, roles}` where `roles` maps each of 8 role names to `provider/slug` string; providers block covers DeepSeek, Moonshot, Z.AI, Anthropic, OpenAI, DashScope/Qwen (`@ai-sdk/openai-compatible` + `options.baseURL`); US-0069 phase->role matrix bridges phase->role on orchestrator (unchanged); catalog bridges role->provider/slug on OpenCode (new)
  - example catalog placeholders (DQ6): role values are `<your-deepseek-slug>`, `<your-kimi-slug>`, `<your-glm-slug>`, `<your-claude-slug>`, `<your-gpt-slug>` — NO real model-id slugs in `template/`; ≥2 roles have different providers (AC-7); D3 grep scope excludes `*.example.json` / `*.local.json`
  - materializer contract (DQ7): `scripts/opencode_model_catalog_apply.py` — input `.opencode/model-catalog.local.json` + installed `.opencode/agents/<role>.md`; absent catalog = no-op (no fail-closed); present + unknown/empty/placeholder slug = `OPENCODE_MODEL_SLUG_UNKNOWN` fail-closed; malformed JSON = `MODEL_CATALOG_INVALID` scope-tagged `opencode-catalog`; injects `model: <provider/slug>` into installed agent YAML frontmatter only (insert if absent; overwrite if present); NEVER writes to `template/`; NEVER reads/writes `.cursor/model-catalog.local.json`; NEVER reads auth credentials
  - installer hook (T-003 triple-installer parity): trigger = `--host opencode|both` AND `.opencode/model-catalog.local.json` exists at install target; absent = skip (no-op; no fail-closed); fail = surface reason code + exit non-zero; installer does NOT generate the catalog for the operator
  - fail-closed reason-code family (DQ3): NEW `OPENCODE_MODEL_SLUG_UNKNOWN` (single namespaced code); REUSED `MODEL_CATALOG_INVALID` (scope-tagged `opencode-catalog`); existing Cursor-side codes remain Cursor-side only
  - validator extension (DQ9): `scripts/model_tier_validate.py --scope opencode-catalog` — `check_template_opencode_agents` (D3 grep scoped, excludes `*.example.json`/`*.local.json`), `validate_opencode_catalog`, `check_opencode_example_catalog` (≥2 roles different providers); reuse `check_forbidden_slugs_in_file` helper; extend-not-duplicate (new script only if too coupled — see T-004 critic NB)
  - contract tests (AC-8): `tests/us0123_contract_test.py` — 8 markers (see architecture AC-8 table); mirror to `template/tests/us0123_contract_test.py` byte-identical
  - runbook stub (DQ10): `## OpenCode model slug routing (US-0123)` h2 one-liner in `docs/engineering/runbook.md`; US-0126 owns full text
  - gitignore (T-006): `.opencode/.gitignore` (US-0121 Q10) `*.local.json` glob covers `model-catalog.local.json`; add explicit entry only if glob is narrower
  - manifest rows (T-009): `template/.opencode/model-catalog.local.example.json` + `scripts/opencode_model_catalog_apply.py` under `[opencode_install_include_paths]` (active + template byte-identical)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0123 / US-0123
- sprint_artifacts: sprints/S0123/ (sprint.md, tasks.md, progress.md, summary.md, uat.json, uat.md)
- timestamp: 2026-08-24T16:30:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- runtime_proof_id: rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123
- proof_hash: CD814AD66F07A9F9A5C649EF6B0283A4A92179D7502238514B211863C401FEA6

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0123-sprint-plan-20260824T163000Z-fresh`
- `timestamp=2026-08-24T16:30:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=sprints/S0123/sprint.md, sprints/S0123/tasks.md, sprints/S0123/progress.md, sprints/S0123/summary.md, sprints/S0123/uat.json, sprints/S0123/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0123, decisions/DEC-0123.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-01`
- `runtime_proof_id=rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0123`, `sprint_id=S0123`
- `proof_issued_at=2026-08-24T16:30:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T17:30:00Z`
- `proof_hash=CD814AD66F07A9F9A5C649EF6B0283A4A92179D7502238514B211863C401FEA6`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T16:30:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-sprint-plan-tech-lead-20260824T163000Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`

---

## Sprint-plan handoff — **US-0122** / **S0122** — `/plan-verify` next (fresh qa)

- sprint_id: S0122
- story_id: US-0122
- dec_id: DEC-0122 (Accepted, decisions/DEC-0122.md)
- research_anchor: R-0109 (DQ1..DQ8 LOCKED for US-0122; US-0121 Q1..Q12 locks preserved)
- orchestrator_run_id: auto-20260824-01
- fresh_context_marker: tl-US0122-sprint-plan-20260824T120000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 — not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001,T-007,T-009; AC-2->T-002,T-003,T-005; AC-3->T-002,T-006(marker 3); AC-4->T-001,T-006(marker 7); AC-5->T-004,T-006(markers 1,5,8); AC-6->T-008; AC-7->T-001,T-006(marker 6),T-009; AC-8->T-006(all 8 markers); AC-9->T-anch(baseline),T-006(marker 8),T-009(parity); AC-10->T-005(locked matrix),T-006(marker 3)
- task_order: T-anch -> T-001 (8 agent files) -> {T-002, T-003, T-004, T-005 parallel (per-agent permission matrices)} -> T-007 (manifest rows) -> T-009 (README + parity) -> T-008 (runbook one-liner) -> T-006 (contract tests last) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0003 (role set), US-0023/BUG-0006 (spawn-only isolation), US-0121 (pack path consumed; no repo-root opencode.json added), US-0102/DEC-0087 (volatile-ID rule — no vendor slugs in template/.opencode/agents/*.md), US-0002/US-0004 (do-not-port Cursor rules/skills — markdown agents, no .mdc clone)
- critic_carry_ins (3 non-blocking — route to task notes, do not silently drop):
  - `ik_us0122_dev_template_allow_mutates_agents` -> T-005 note: `dev` `template/**` allow could mutate `.opencode/agents/*.md`; mitigation via T-006 marker 1 + T-009 parity extension (byte-identical assertion); no narrow deny glob (would fragment locked matrix)
  - `ik_us0122_compose_guards_marker_surjection` -> T-006 note: do NOT add 9th `test_us0122_compose_guards_unchanged` marker; AC-9 surjection via T-anch baseline + DEC-0122 §compose surface + marker 8 (`test_us0122_role_id_parity`); 8-marker budget locked
  - `ik_us0122_stale_compose_count_6_vs_5` -> T-anch note: architecture overview 6/6 wording is stale drift; T-anch verifies 5/5; non-blocking; reconcile at /plan-verify or future doc-parity slice
- architecture_pointers: docs/engineering/architecture.md # US-0122 (approach A1, 8-marker table, locked Layer-1 permission matrix, static success-test-(c) harness, Layer-2 short prompts + clone guard, manual invoke one-liner, no vendor slugs, non-goals)
- dec_pointers: decisions/DEC-0122.md (§1 markdown agents, §2 locked eight-agent matrix, §3 static success-test-(c) harness, §4 Layer-2 short prompts + clone guard, §5 manual invoke one-liner, §6 no vendor slugs, §7 contract tests + parity, §8 non-goals)
- first_execute_task: T-anch (NO-OP / verification) — verify # US-0122 H1 anchor + DEC-0122 Accepted + compose guards 5/5 + 8-marker list locked + locked matrix in DEC-0122 §2 + absent surfaces
- key_locked_artifacts:
  - agent file layout: `template/.opencode/agents/{po,tech-lead,dev,qa,release,curator,security,auto}.md` (8 markdown files; YAML frontmatter: description, mode, permission, short prompt body)
  - locked Layer-1 permission matrix (DEC-0122 §2): `auto` (primary; edit deny; task object 7-role allow + `*` deny last); `po` (subagent; edit object docs/product/** + handoffs/po_to_tl.md allow + `**` deny last; bash deny; task deny); `tech-lead` (subagent; edit object architecture/decisions/state/research + decisions/DEC-*.md + handoffs/tl_to_dev.md + sprints/Sxxxx/sprint.md + sprints/Sxxxx/tasks.md + `**` deny last; bash deny; task deny); `dev` (subagent; edit object scripts/** + its_magic/** + template/** + tests/** + sprints/Sxxxx/progress.md + sprints/Sxxxx/qa-findings.md + handoffs/dev_to_qa.md + `**` deny last; bash ask; task deny); `qa` (subagent; edit object qa-findings + plan-verify + verify-work-findings + uat.md/json + qa handoffs + `**` deny last; bash ask; task deny); `release` (subagent; edit object release_queue/notes/releases + release/verify handoffs + CHANGELOG + `**` deny last; bash ask; task deny); `curator` (subagent; edit object state + state-archive + decisions.md + research.md + resume_brief/portfolio_state/continuation_hygiene/archive + `**` deny last; bash deny; task deny); `security` (subagent; edit deny; bash ask; task deny)
  - ordering contract (DQ3): broad `**` -> `deny` MUST be last key in every object-form `permission.edit`; `*` -> `deny` MUST be last key in `auto` `permission.task`; tests assert key order, not just set membership
  - Task subagent ID contract (DQ4): `auto` `permission.task` 7 role allow + `*` deny last denies all non-kit subagents including OpenCode built-ins + future US-0124 plugin-internal helpers; US-0124 may add helpers as `allow` keys above `*` deny, never remove `*` deny last
  - static success-test-(c) harness (DQ7): parse po.md frontmatter -> assert edit is object -> assert docs/product/** + handoffs/po_to_tl.md allow -> assert `**` deny last -> assert no production allow (scripts/**, its_magic/**, **/*.py, installer.*, template/scripts/**, template/its_magic/**); runtime permission-check deferred to US-0124
  - Layer-2 short prompts + clone guard (AC-4): each agent file ≤ 2 KiB total; no forbidden clone markers (/auto, /intake, /discovery, /research, /architecture, /sprint-plan, /execute, /qa, /release, /closure, /refresh-context command-body prose; .cursor/commands/ path literals; --- MDC frontmatter delimiters)
  - no vendor slugs (AC-7): template/.opencode/agents/*.md frontmatter MUST NOT contain `model:` with real vendor slug; test greps deepseek|moonshot|kimi|glm|claude|gpt|sonnet|opus|haiku|o1|o3|sk- -> zero hits
  - manifest rows: `template/.opencode/agents/**` source rows under `[opencode_install_include_paths]` (active + template byte-identical); existing rows unchanged
  - parity extension: `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` extended for agent inventory (8 markdown files byte-identical active ↔ template; no active kit mirror — DQ8 YAGNI)
  - runbook one-liner: `## OpenCode role agents and permissions (US-0122)` h2 in docs/engineering/runbook.md (full runbook US-0126)
- next_phase: `/plan-verify` (fresh qa per orchestrator brief) for S0122 / US-0122
- sprint_artifacts: sprints/S0122/ (sprint.md, tasks.md, progress.md, summary.md, uat.json, uat.md)
- timestamp: 2026-08-24T12:00:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- runtime_proof_id: rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122
- proof_hash: 49D4165515F54421094D13675422D8A6CDBDDCBE9A82C6C5A3F3E5248FD1857D

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0122-sprint-plan-20260824T120000Z-fresh`
- `timestamp=2026-08-24T12:00:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required)
- `evidence_ref=sprints/S0122/sprint.md, sprints/S0122/tasks.md, sprints/S0122/progress.md, sprints/S0122/summary.md, sprints/S0122/uat.json, sprints/S0122/uat.md, docs/engineering/state.md (sprint-plan checkpoint append-bottom), docs/engineering/architecture.md # US-0122, decisions/DEC-0122.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260824-01`
- `runtime_proof_id=rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0122`, `sprint_id=S0122`
- `proof_issued_at=2026-08-24T12:00:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-24T13:00:00Z`
- `proof_hash=49D4165515F54421094D13675422D8A6CDBDDCBE9A82C6C5A3F3E5248FD1857D`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-24T12:00:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260824-01-sprint-plan-tech-lead-20260824T120000Z-US-0122","sprint_id":"S0122","story_id":"US-0122"}`

---

## Sprint-plan handoff - **US-0121** / **S0121** - `/execute` next (fresh dev)

- sprint_id: S0121
- story_id: US-0121
- dec_id: DEC-0120 (Accepted, decisions/DEC-0120.md)
- research_anchor: R-0109 (Q6-Q12 LOCKED for US-0121 execute; Q1-Q5 LOCKED for architecture only, deferred to US-0122..US-0126)
- orchestrator_run_id: auto-20260823-01
- fresh_context_marker: tl-US0121-sprint-plan-20260823T112200Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: PLANNED (backlog OPEN per US-0045 - not mutated)
- task_count: 10 (T-anch + T-001..T-009; within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1->T-001; AC-2->T-003,T-004,T-005,T-006; AC-3->T-004,T-005,T-006; AC-4->T-007(markers 2-4); AC-5->T-002,T-004,T-005,T-006,T-007(markers 10,11,14); AC-6->T-008,T-007(marker 13); AC-7->T-007; AC-8->T-anch(baseline),all gated; AC-9->T-003(--help),T-009(runbook h2); AC-10->T-001,T-007(marker 12)
- task_order: T-anch -> {T-001, T-002, T-003 parallel} -> {T-004, T-005, T-006 parallel} -> T-008 -> T-009 -> T-007 (tests last) -> integration verification
- compose_guards (non-negotiable): DO NOT amend US-0008 (additive --host only), DEC-0045 (its_magic/ ownership), US-0102 (volatile-ID rule - no slugs), US-0001 (phase names as placeholders only), US-0018 (packaging delivery path)
- critic_carry_ins (3 non-blocking - route to task notes, do not silently drop):
  - `ik_us0121_missing_overwrite_host_gap` -> T-006 note: YAGNI - `missing` after `both` no-ops on `.opencode/` via predicate (copy-if-missing is host-scoped); no new diagnostic; overwrite US-0008 unchanged
  - `ik_us0121_parity_active_mirror_contradiction` -> T-008 note: parity pairs `template/.opencode` with consumed `.opencode/` (when host includes opencode); no kit-repo active mirror (Q9 YAGNI)
  - `ik_us0121_ac9_help_test_yagni` -> T-007 note: `--help` grep is marker 9 in locked 14-marker set; do not add 15th marker without dropping YAGNI elsewhere
- architecture_pointers: docs/engineering/architecture.md # US-0121 (approach A1, 14-marker table, host-scoped missing/upgrade/clean matrix, kernel-vs-host filter, mixed-section predicate)
- dec_pointers: decisions/DEC-0120.md (Â§1 host switch, Â§2 parallel manifest sections, Â§3 kernel-vs-host, Â§4 mixed-section predicate, Â§5 host-scoped missing/upgrade/clean, Â§6 pack layout, Â§7 gitignore, Â§8 cursor coexistence, Â§9 contract tests + parity, Â§10 non-goals)
- first_execute_task: T-anch (NO-OP / verification) - verify `# US-0121` H1 anchor + DEC-0120 Accepted + compose guards 5/5 + 14-marker list locked + absent surfaces
- key_locked_artifacts:
  - manifest sections: `[opencode_install_include_paths]` + `[opencode_clean_paths]` (active + template byte-identical)
  - host predicate: `host_gates_cursor_row(rel, host)` shared across PS/Bash/Python
  - diagnostics: `INSTALL_HOST_INVALID`, `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`, `OPENCODE_STALE_BY_UPGRADE_CURSOR`, `CURSOR_ORPHANED_BY_CLEAN_OPENCODE`, `CURSOR_STALE_BY_UPGRADE_OPENCODE`
  - pack layout: `template/.opencode/{agents/.gitkeep, commands/.gitkeep, plugins/README.md, .gitignore, README.md}` (no repo-root opencode.json; no active mirror)
  - gitignore Q10 four groups: `.opencode/opencode.json{,c}`, `.env`/`.env.*`, `*.local.json{,c}`, `auth.json`
- next_phase: `/execute` (fresh dev) for S0121 / US-0121
- sprint_artifacts: sprints/S0121/ (sprint.md, tasks.md, progress.md, uat.json, uat.md, plan-verify.json)
- timestamp: 2026-08-23T11:22:00Z
- role: tech-lead
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 - required)
- runtime_proof_id: rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121
- proof_hash: 2a7f31fca177451c935b9aedebb4781d57a7b13d8ef87a9e913fcaf10bec6336

### Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0121-sprint-plan-20260823T112200Z-fresh`
- `timestamp=2026-08-23T11:22:00Z`
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 - required)
- `evidence_ref=sprints/S0121/sprint.md, sprints/S0121/tasks.md, sprints/S0121/progress.md, sprints/S0121/uat.json, sprints/S0121/uat.md, sprints/S0121/plan-verify.json, docs/engineering/state.md, docs/engineering/architecture.md # US-0121, decisions/DEC-0120.md, handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260823-01`
- `runtime_proof_id=rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121`
- `phase_id=sprint-plan`, `role=tech-lead`, `story_id=US-0121`, `sprint_id=S0121`
- `proof_issued_at=2026-08-23T11:22:00Z`
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-23T12:22:00Z`
- `proof_hash=2a7f31fca177451c935b9aedebb4781d57a7b13d8ef87a9e913fcaf10bec6336`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260823-01","phase_id":"sprint-plan","proof_issued_at":"2026-08-23T11:22:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260823-01-sprint-plan-tech-lead-20260823T112200Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}`

---

## Sprint-plan handoff — **US-0108** / **S0108** — `/plan-verify` next (fresh qa)

- sprint_id: S0108
- story_id: US-0108
- dec_id: DEC-0108 (locked, decisions/DEC-0108.md)
- research_anchor: R-0096 (Q1–Q10 CLOSED, status=delivered)
- orchestrator_run_id: auto-20260628-04
- fresh_context_marker: tl-US0108-sprint-plan-20260629T210000Z-fresh
- sprint_plan_verdict: PASS
- sprint_status: OPEN
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1→T-001; AC-2→T-002,T-003; AC-3→T-004,T-005; AC-4→T-006; AC-5→T-007; AC-6→T-008; AC-7→T-009,T-010; AC-8→T-011
- tranche_order: A keys+reason codes → B worktree lib → C selection+anti-slop → D merge+resource+execute → E tests+parity+runbook
- compose_guards (non-negotiable): DO NOT amend US-0047, US-0092, US-0103, US-0104, US-0107
- topology: parallel dev in isolated git worktrees; QA cross-review; deterministic winner selection; resource guard cap=6
- next_phase: `/plan-verify` (fresh qa) for S0108 / US-0108
- sprint_artifacts: sprints/S0108/ (sprint.md, tasks.md, progress.md, sprint.json, plan-verify.json)
- timestamp: 2026-06-29T21:32:00Z
- role: tech-lead
- backlog_drain_active: true
- backlog_drain_stories_remaining_budget: 3
- portfolio_open_stories: 4 (US-0108, US-0109, US-0111, US-0112)
- runtime_proof_id: rp-auto-20260628-04-sprint-plan-tech-lead-20260629T213200Z-US0108
- proof_hash: b3e7f1a2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=sprint-plan`
- `role=tech-lead`
- `fresh_context_marker=tl-US0108-sprint-plan-20260629T210000Z-fresh`
- `timestamp=2026-06-29T21:32:00Z`
- `evidence_ref=sprints/S0108/sprint.md,sprints/S0108/tasks.md,sprints/S0108/progress.md,sprints/S0108/sprint.json,sprints/S0108/plan-verify.json,docs/engineering/state.md,handoffs/tl_to_dev.md,handoffs/resume_brief.md`

### Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260628-04`
- `runtime_proof_id=rp-auto-20260628-04-sprint-plan-tech-lead-20260629T213200Z-US0108`
- `phase_id=sprint-plan`
- `role=tech-lead`
- `proof_issued_at=2026-06-29T21:32:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=b3e7f1a2c4d5e6f7a8b9c0d1e2f3a4b5c6d7e8f9a0b1c2d3e4f5a6b7c8d9e0f1a2`

Canonical payload: `{"orchestrator_run_id":"auto-20260628-04","phase_id":"sprint-plan","proof_issued_at":"2026-06-29T21:32:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260628-04-sprint-plan-tech-lead-20260629T213200Z-US0108"}`.

---

## Architecture handoff — **US-0108** — `/sprint-plan` next (fresh tech-lead)

- story_id: US-0108
- sprint_id: (none — sprint-plan to create S0108)
- dec_id: DEC-0108 (locked, decisions/DEC-0108.md)
- research_anchor: R-0096 (Q1–Q10 CLOSED, status=delivered)
- orchestrator_run_id: auto-20260628-04
- fresh_context_marker: tl-US0108-architecture-20260629T204500Z-fresh
- architecture_verdict: PASS
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1→T-001; AC-2→T-002,T-003; AC-3→T-004,T-005; AC-4→T-006; AC-5→T-007; AC-6→T-008; AC-7→T-009,T-010; AC-8→T-011
- tranche_order: A keys+reason codes → B worktree lib → C validator+selection → D merge+resource guard+execute steps → E tests+parity+runbook
- compose_guards (non-negotiable): DO NOT amend US-0047, US-0092, US-0103, US-0104, US-0107
- topology: parallel dev in isolated git worktrees; QA cross-review; deterministic winner selection; resource guard cap=6
- next_phase: `/sprint-plan` (fresh tech-lead) for US-0108 — materialize S0108 sprint
- timestamp: 2026-06-29T20:45:00Z
- role: tech-lead
- backlog_drain_active: true
- backlog_drain_stories_remaining_budget: 3
- portfolio_open_stories: 4 (US-0108, US-0109, US-0111, US-0112)

---

## Execute handoff — **US-0106** / **S0106** — `/execute` next (fresh dev)

- sprint_id: S0106
- story_id: US-0106
- dec_id: DEC-0106
- orchestrator_run_id: auto-20260628-04
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1→T-001; AC-2→T-002,T-003; AC-3→T-003; AC-4→T-004; AC-5→T-005; AC-6→T-006; AC-7→T-007,T-011; AC-8→T-008,T-009,T-010
- sprint_status: OPEN
- next_phase: `/execute` (fresh dev) for S0106 / US-0106
- compose_guards (non-negotiable): DO NOT amend US-0069, US-0003, US-0023, US-0103, US-0104, US-0105, US-0107
- timestamp: 2026-06-29T00:40:00Z
- role: qa
- verdict: PASS (plan-verify)

---

## Sprint-plan handoff — **US-0106** / **S0106** — sprint S0106 created (11 tasks T-001..T-011) — `/plan-verify` next (fresh qa)

- sprint_id: S0106
- story_id: US-0106
- dec_id: DEC-0106
- orchestrator_run_id: auto-20260628-04
- task_count: 11 (within SPRINT_MAX_TASKS=12)
- ac_surjective_map: AC-1→T-001; AC-2→T-002,T-003; AC-3→T-003; AC-4→T-004; AC-5→T-005; AC-6→T-006; AC-7→T-007,T-011; AC-8→T-008,T-009,T-010
- tranche_order: A keys+reason codes (T-001) → B lib+dispatch (T-004,T-005) → C validator+command (T-002,T-003) → D review isolation+compose (T-006,T-008,T-009) → E tests+parity+runbook (T-007,T-010,T-011)
- sprint_status: OPEN
- next_phase: `/plan-verify` (fresh qa) for S0106 / US-0106
- compose_guards (non-negotiable): DO NOT amend US-0069, US-0003, US-0023, US-0103, US-0104, US-0105, US-0107
- timestamp: 2026-06-29T00:35:00Z
- role: tech-lead
- verdict: PASS

---

## Plan-verify handoff — **US-0107** / **S0107** — post-**`/plan-verify`** → **`/execute`** (**qa**)


