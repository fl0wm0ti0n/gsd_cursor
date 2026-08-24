# Sprint S0124 - Task checklist (US-0124)

Total tasks: 10 (T-anch + T-001..T-009). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (NEW plugin file `template/.opencode/plugins/orchestrator.ts`)
3. T-002 (NEW mock-ctx harness `tests/us0124/mock_ctx.ts`; after T-001)
4. T-004 (additive argv on `scripts/auto_outer_driver.py`; after T-001)
5. T-006 (Installer manifest rows; after T-001) - parallel with T-007
6. T-007 (README + `--scope=opencode-adapter` parity extension; after T-001 + T-006) - parallel with T-006
7. T-003 (Runbook stub `## OpenCode orchestrator plugin reason codes (US-0124)` h2; after T-001)
8. T-008 (Runbook cross-link placeholder to US-0126; after T-003)
9. T-005 (NEW `tests/us0124_contract_test.py` — 9 markers; tests last, assert all outputs)
10. T-009 (Validator extension decision; after T-005)
11. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0124` H1 anchor present in `docs/engineering/architecture.md` (added in /architecture phase per DEC-0076 / BUG-0010; AFTER `# US-0123` and BEFORE `# US-0089` per DEC-0073 §11); verify DEC-0124 authored Accepted at `decisions/DEC-0124.md` (§1 plugin entry point, §2 spawn API, §3 mock-ctx harness, §4 reason-code namespace, §5 three-case detection matrix, §6 subprocess stop-matrix, §7 headless CLI, §8 agent vs plugin boundary, §9 contract tests, §10 non-goals); verify compose guards 9/9 UNCHANGED baseline (US-0069/DEC-0051, US-0092/DEC-0078, US-0095/DEC-0080, US-0023/US-0048/BUG-0006, US-0005, US-0122/DEC-0122, US-0121/DEC-0120, US-0125, US-0102/DEC-0087); verify 9-marker contract-test list locked in architecture AC-10 table; verify plugin entry-point + spawn API + stop-matrix argv + agent/plugin boundary locked in DEC-0124 §1–§8; verify `template/.opencode/plugins/orchestrator.ts` does NOT yet exist; verify `tests/us0124/mock_ctx.ts` does NOT yet exist; verify `tests/us0124_contract_test.py` does NOT yet exist; verify `scripts/auto_outer_driver.py` does NOT yet have `--phase/--role/--story/--sprint/--orchestrator-run-id/--stop-reason` argv; verify `docs/engineering/runbook.md` does NOT yet have `## OpenCode orchestrator plugin reason codes (US-0124)` h2; verify `[opencode_install_include_paths]` section exists in active + template manifest (US-0121) but does NOT yet list `template/.opencode/plugins/orchestrator.ts` source row. Record results to `sprints/S0124/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0124.md` in /execute; T-anch records baseline observations only (mirrors US-0122 / US-0123 T-anch ceremony). (AC-9, AC-10 baseline; NO-OP / verification only)

- [x] **T-001**: Create `template/.opencode/plugins/orchestrator.ts` per architecture DQ1 + DQ2 + DQ8 LOCKED + DEC-0124 §1, §2, §8. Canonical v2 module shape: `import { Plugin } from "@opencode-ai/plugin"; export default Plugin.define({ id: "its-magic.orchestrator", setup(ctx) { ... } })`. Auto-discovered via `.opencode/plugins/` scan — no `plugins[]` entry in `opencode.json` required. `setup(ctx)` registers: (a) `ctx.tool.hook("execute.before", ...)` write-guard detecting `AUTO_ORCHESTRATOR_PHASE_EXECUTION` (orchestrator or any role performing another role's artifact writes) and fails closed; (b) spawn entry point that resolves `phase_id → role` via US-0069 / DEC-0051 matrix (compose, not amend), calls `ctx.session.create({ parentID: <orchestrator-session-id>, agent: <role>, prompt: <phase-prompt> })`, asserts `sessionID !== parentID` (DQ5 hard post-condition), `ctx.session.wait(sessionID)`, reads result, persists isolation evidence (`parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker`); (c) subprocess callout to `scripts/auto_outer_driver.py` for stop-matrix decisions (DQ6 — additive argv; Python SOT unchanged; forbidden TS reimpl). If `ctx.session.create` is unavailable, fail closed with `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`. Three-case subtask-ignored detection matrix (null/throw/identical-id) → `OPENCODE_SUBTASK_IGNORED` (DQ5). Throw-discrimination rule: missing-primitive throw (`ctx.session.create is not a function`) → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`; otherwise (null return, identical-id return, generic throw) → `OPENCODE_SUBTASK_IGNORED`. Plugin MUST NOT copy agent's permission array (DQ8 — no `edit:`/`bash:` literals, no 7 role names hardcoded; plugin resolves roles via US-0069 matrix). Plugin MUST NOT clone `.cursor/commands/auto.md` prose (AC-9 — `test_us0124_no_cursor_auto_clone` enforces). Plugin source has zero vendor model slugs (US-0102 / DEC-0087). Tests: marker 1 (`test_us0124_spawn_isolation_static`) asserts static grep/AST; marker 6 (`test_us0124_no_cursor_auto_clone`) asserts no Cursor prose; marker 7 (`test_us0124_agent_plugin_compose`) asserts DQ8 boundary. (AC-1, AC-2, AC-3, AC-9)

- [x] **T-002**: Create `tests/us0124/mock_ctx.ts` per architecture DQ3 LOCKED + DEC-0124 §3. `MockCtx` implements the v2 plugin context subset the orchestrator plugin uses: `ctx.session.create`, `ctx.session.prompt`, `ctx.session.wait`, `ctx.tool.hook` (no-op recorder), `ctx.options` (readonly). `MockCtx.session.create` accepts a scripted `nextSessionID` + optional `throwOnCreate` flag + optional `returnNull` flag + optional `identicalID` flag (returns `{ sessionID: parentID }` to test the DQ5 identical-id case). Default behavior: return a fresh uuid ≠ `parentID`. `MockCtx.session.wait` returns a scripted `result` string. Tests load `template/.opencode/plugins/orchestrator.ts` via dynamic import, call `setup(mockCtx)`, then drive the orchestrator's spawn entry point with a synthetic phase+role and assert: (i) `mockCtx.session.create` was called with `parentID === <orchestrator-session-id>` and `agent === <expected-role>`; (ii) the returned `sessionID !== parentID` (or fail-closed `OPENCODE_SUBTASK_IGNORED` when scripted null/throw/identical); (iii) isolation evidence was persisted with the required fields (`parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker`). **Runner: Node** (CI already has it via `tests/run-tests.ps1 Ensure-NodeOnPath`); Bun optional. No live OpenCode runtime probe in CI (AC-10). Tests: marker 2 (`test_us0124_spawn_isolation_runtime`) asserts runtime behavior; markers 3, 4, 5 (`test_us0124_subtask_ignored_*`) assert the three-case detection matrix. (AC-3, AC-4, AC-10)

- [x] **T-003**: Runbook stub — Add `## OpenCode orchestrator plugin reason codes (US-0124)` h2 to `docs/engineering/runbook.md` as a **stub one-liner per code** per DEC-0124 §4 / DQ4 LOCKED. List the four new `OPENCODE_*` codes (`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`, `OPENCODE_SUBTASK_IGNORED`, `OPENCODE_HEADLESS_UNSUPPORTED`, `OPENCODE_DRIVER_INVOKE_FAILED`) + three reused codes (`AUTO_ORCHESTRATOR_PHASE_EXECUTION`, `PHASE_ROLE_MISMATCH`, `NATIVE_CHAIN_UNAVAILABLE`) with one-line semantics + fail-closed action each. Cross-link to US-0126 for the full reason-code table (T-008 owns the cross-link placeholder body). US-0126 owns the full runbook section text; US-0124 ships the stub only — no duplication of remediation text. **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically (verified via `python -c "a=open('docs/engineering/runbook.md','rb').read(); b=open('template/docs/engineering/runbook.md','rb').read(); assert a==b"`). T-003 does NOT author a full runbook section (YAGNI — US-0126 owns it). (AC-8)

- [x] **T-004**: Subprocess argv contract — Extend `scripts/auto_outer_driver.py` with additive argv `--phase <phase_id> --role <role> --story <story_id> --sprint <sprint_id> --orchestrator-run-id <run_id> --stop-reason <reason>` per architecture DQ6 LOCKED + DEC-0124 §6. When the new flags are present, the driver returns a JSON object on stdout: `{ "action": "spawn_next" | "hard_stop" | "ledger_write" | "pause_boundary", "next_phase": "<phase_id>", "stop_reason": "<reason>", ... }`. When the new flags are **absent**, the existing `auto_outer_driver.py` behavior is byte-identical (no regression to US-0092 / DEC-0078) — additive CLI surface only. The plugin parses the JSON and dispatches: `spawn_next` → `ctx.session.create` for the next phase; `hard_stop` → emit stop reason + halt; `ledger_write` → write to ledger + continue; `pause_boundary` → emit pause + halt. The plugin does NOT own stop-reason logic; it only parses + dispatches. All state-machine transitions live in `scripts/auto_outer_driver.py` (Python SOT). **Subprocess error-handling contract** (critic NB `ik_us0124_dq6_driver_fail_code_conflation` closed): non-zero exit from `auto_outer_driver.py` → emit `OPENCODE_DRIVER_INVOKE_FAILED` (NOT `OPENCODE_HEADLESS_UNSUPPORTED`); fail closed; stop `/auto`. Malformed JSON response (parse error) → emit `OPENCODE_DRIVER_INVOKE_FAILED`; fail closed; stop `/auto`. Subprocess timeout → emit `OPENCODE_DRIVER_INVOKE_FAILED`; fail closed; stop `/auto`. `opencode run` CLI missing on PATH (DQ7 headless path, separate from DQ6) → emit `OPENCODE_HEADLESS_UNSUPPORTED`; fail closed; stop `/auto`. `OPENCODE_HEADLESS_UNSUPPORTED` is reserved exclusively for the missing `opencode run` CLI surface (DQ7). `OPENCODE_DRIVER_INVOKE_FAILED` is reserved exclusively for the Python driver subprocess failure (DQ6). The two codes are distinct and never overlap. Tests: marker 8 (`test_us0124_invoke_cmd_hook`) asserts argv + JSON parsing OR fail-closed path. (AC-6)

- [x] **T-005**: Create `tests/us0124_contract_test.py` with 9 markers per architecture AC-10 table + DEC-0124 §9:
  1. `test_us0124_spawn_isolation_static` — grep/AST on plugin source: asserts `ctx.session.create` is called with `parentID: <orchestrator-session-id>` and `agent: <role>`; no same-session spawn (AC-1, AC-3).
  2. `test_us0124_spawn_isolation_runtime` — mock `ctx` harness: `MockCtx.session.create` returns fresh uuid ≠ parentID; plugin asserts `sessionID !== parentID`; isolation evidence persisted with required fields (`parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker`) (AC-3, AC-4, AC-10).
  3. `test_us0124_subtask_ignored_null_return` — `MockCtx.session.create` returns null → plugin emits `OPENCODE_SUBTASK_IGNORED` + stops `/auto` (AC-8).
  4. `test_us0124_subtask_ignored_throw` — `MockCtx.session.create` throws generic error → plugin catches, emits `OPENCODE_SUBTASK_IGNORED` + stops `/auto`. Missing-primitive throw (`ctx.session.create is not a function`) → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED` (throw-discrimination rule) (AC-8).
  5. `test_us0124_subtask_ignored_identical_id` — `MockCtx.session.create` returns `{ sessionID: parentID }` → plugin detects `sessionID === parentID`, emits `OPENCODE_SUBTASK_IGNORED` + stops `/auto` (AC-8).
  6. `test_us0124_no_cursor_auto_clone` — grep plugin source for unique-to-Cursor phrases (`## Spawn-boundary integrity (BUG-0006)` heading, `AUTO_LOOP_MAX_CYCLES` prose, `.cursor/commands/auto.md` markers) — zero hits (AC-9).
  7. `test_us0124_agent_plugin_compose` — both `template/.opencode/agents/auto.md` + `template/.opencode/plugins/orchestrator.ts` exist; plugin source has zero matches for 7 role names + `edit:`/`bash:` permission literals; `ctx.tool.hook("execute.before")` callback present and calls stop-matrix subprocess for `AUTO_ORCHESTRATOR_PHASE_EXECUTION` detection (AC-1, AC-9).
  8. `test_us0124_invoke_cmd_hook` — asserts argv construction `opencode run --agent auto --format json --auto "<prompt>"` + JSON event parsing OR fail-closed `OPENCODE_HEADLESS_UNSUPPORTED` when `opencode` missing on PATH; not a live OpenCode probe (AC-7).
  9. `test_us0124_secrets_no_logging` — grep plugin source + harness for `api_key`/`apikey`/`sk-`/`auth.json`/`.env` patterns — zero hits in log/print/error paths; US-0085 posture (AC-11).
  Mirror to `template/tests/us0124_contract_test.py` byte-identical for parity pairing. (AC-10, AC-11)

- [x] **T-006**: Installer manifest rows — Add `template/.opencode/plugins/orchestrator.ts` source row under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows UNCHANGED — additive rows only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose; `host_gates_cursor_row` predicate). (AC-1)

- [x] **T-007**: README + parity extension — Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover the plugin file + mock harness + contract-test surface (byte-identical active ↔ template pairs where applicable; materializer is kit-only, not paired). Update `its_magic/README.md` to cross-link the OpenCode orchestrator plugin capability + pointer to DEC-0124. Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-10)

- [x] **T-008**: Runbook cross-link placeholder to US-0126 — Add a one-line cross-link placeholder in the US-0124 runbook h2 stub (added in T-003) pointing to US-0126 for the full reason-code table. US-0126 owns the full table text; US-0124 ships the cross-link anchor only. **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically. (AC-8)

- [x] **T-009**: Validator extension — default no new script. Default = extend contract tests (T-005) + reuse `scripts/model_tier_validate.py --scope opencode-catalog` from US-0123; do NOT create a new `scripts/opencode_plugin_validate.py`. Fall back to a new validator script ONLY if US-0124 plugin source needs static validation beyond contract tests AND coupling forces a separate validator class (trigger: plugin-specific checks cannot reuse >50% of existing `--scope opencode-catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes). If fallback triggers, raise a DEC follow-up; do NOT silently split. (AC-10)

## Integration verification (post T-009 + T-005)

- [ ] Test gate: `python -m pytest tests/us0124_contract_test.py -v` → 9/9 PASS
- [ ] Parity gate: `check_intake_template_parity.py --scope=opencode-adapter` PASS
- [ ] Parity gate: active + template manifest byte-identical
- [ ] Parity gate: active + template runbook byte-identical
- [ ] Compose gate: 9/9 UNCHANGED
- [ ] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on plugin source + harness
- [ ] No-Cursor-clone gate: unique-to-Cursor phrases zero hits on plugin source
- [ ] Agent-plugin boundary gate: 7 role names + `edit:`/`bash:` literals zero hits on plugin source
- [ ] Subprocess argv gate: `auto_outer_driver.py --phase ... --role ... --story ... --sprint ... --orchestrator-run-id ... --stop-reason ...` returns JSON; legacy flags byte-identical behavior

## Files to touch (scope)

### New (create)

- `template/.opencode/plugins/orchestrator.ts`
- `tests/us0124/mock_ctx.ts`
- `tests/us0124_contract_test.py`
- `template/tests/us0124_contract_test.py` (byte-identical mirror for parity)
- `sprints/S0124/t-anch-verification.md`

### Edit (scoped, additive only)

- `scripts/auto_outer_driver.py` (additive argv `--phase/--role/--story/--sprint/--orchestrator-run-id/--stop-reason` → JSON response; legacy behavior byte-identical when flags absent)
- `scripts/check_intake_template_parity.py` (extend `OPENCODE_ADAPTER_PAIRS` for plugin file + mock harness + contract-test surface)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)
- `docs/engineering/context/installer-owned-paths.manifest` (add `template/.opencode/plugins/orchestrator.ts` source row under `[opencode_install_include_paths]`)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical)
- `docs/engineering/runbook.md` (append `## OpenCode orchestrator plugin reason codes (US-0124)` h2 stub + US-0126 cross-link placeholder)
- `template/docs/engineering/runbook.md` (byte-identical mirror)
- `its_magic/README.md` (cross-link OpenCode orchestrator plugin capability + DEC-0124 pointer)
- `scripts/model_tier_validate.py` (extend `--scope opencode-catalog` ONLY if T-009 fallback triggers; default = no edit)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0124` (T-anch NO-OP)
- `decisions/DEC-0124.md` (T-anch NO-OP)
- `template/.opencode/agents/*.md` (US-0122 — agent files unchanged; plugin composes with agent per DQ8)
- `template/.opencode/plugins/README.md` (US-0121 reserved slot — US-0124 owns directory body via T-001)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| Compose-guard story surfaces (US-0069/DEC-0051, US-0092/DEC-0078, US-0095/DEC-0080, US-0023/US-0048/BUG-0006, US-0005, US-0122/DEC-0122, US-0121/DEC-0120, US-0125, US-0102/DEC-0087) | 9/9 UNCHANGED — US-0124 adds additive plugin + mock-ctx harness + stub table only |

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

**Surjectivity check**: 11/11 ACs covered (AC-1..AC-11 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
