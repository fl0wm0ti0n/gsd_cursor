# Sprint S0125 - Task checklist (US-0125)

Total tasks: 10 (T-anch + T-001..T-009). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (NEW 15 command files `template/.opencode/commands/<name>.md`)
3. T-002 (Clone-guard contract test marker; after T-001) - parallel with T-003, T-004, T-007
4. T-003 (Validator→artifact mapping verify-or-extract-to-test-fixture; after T-001) - parallel
5. T-004 (Validator subprocess bridge prose; after T-001) - parallel
6. T-007 (Installer manifest rows; after T-001) - parallel
7. T-008 (README + parity + runbook stub; after T-001 + T-007)
8. T-005 (Mock-subprocess harness; after T-003)
9. T-006 (NEW `tests/us0125_contract_test.py` — 11 markers; tests last)
10. T-009 (Validator extension decision; after T-006)
11. Integration verification

## Task checklist

- [x] **T-anch**: Verify `# US-0125` H1 anchor present in `docs/engineering/architecture.md` (added in /architecture phase per DEC-0076 / BUG-0010; AFTER `# US-0124` L1632 and BEFORE `# US-0089` L2103 per DEC-0073 §11 — verified at L1836); verify DEC-0125 authored Accepted at `decisions/DEC-0125.md` (§1 command file inventory, §2 clone guard, §3 validator bridge contract, §4 defense-in-depth, §5 `/auto` dispatch-only, §6 frontmatter shape, §7 reason-code boundary, §8 mock-ctx+mock-subprocess harness); verify compose guards 7/7 UNCHANGED baseline (US-0001, US-0078/DEC-0060, US-0121/DEC-0120, US-0122/DEC-0122, US-0124/DEC-0124, US-0126, US-0102/DEC-0087); verify 11-marker contract-test list locked in architecture AC-8 table; verify command inventory (15 files) + clone-guard (line ≤ 20 + similarity ≤ 0.30 via difflib) + validator-bridge (two named CLIs + generic bridge) + defense-in-depth (command prose = diagnostics; plugin = enforcement) + `/auto` dispatch-only (`agent: auto` + `subtask: false` + no spawn logic) + frontmatter shape (`description` + `agent`; `/ask` omits `agent`; no `model:`; `subtask: false` only on `/auto`) + reason-code boundary (raw Python codes + `OPENCODE_DRIVER_INVOKE_FAILED` for subprocess failure; no `OPENCODE_*` wrapper) + stub-harness (mock-ctx + mock-subprocess reusing US-0124 `MockCtx`) locked in DEC-0125 §1–§8; verify `template/.opencode/commands/` exists with only `.gitkeep` (US-0121 reserved slot — US-0125 owns directory body); verify `tests/us0125/` directory does NOT yet exist; verify `tests/us0125_contract_test.py` does NOT yet exist; verify `docs/engineering/runbook.md` does NOT yet have `## OpenCode thin commands + validator bridge (US-0125)` h2 (last US-0124 h2 at L3995); verify `[opencode_install_include_paths]` section exists in active + template manifest (US-0121) but does NOT yet list `template/.opencode/commands/**` source row. Record results to `sprints/S0125/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` or `decisions/DEC-0125.md` in /execute; T-anch records baseline observations only (mirrors US-0122 / US-0123 / US-0124 T-anch ceremony). (AC-9, AC-10 baseline; NO-OP / verification only)

- [x] **T-001**: Create 15 dispatch-only markdown command files at `template/.opencode/commands/<name>.md` per architecture DQ1 + DQ6 LOCKED + DEC-0125 §1, §6. Inventory (15 files): `intake.md` (agent: po, phase: intake), `discovery.md` (agent: po, phase: discovery), `research.md` (agent: tech-lead, phase: research), `architecture.md` (agent: tech-lead, phase: architecture), `sprint-plan.md` (agent: tech-lead, phase: sprint-plan), `plan-verify.md` (agent: qa, phase: plan-verify), `execute.md` (agent: dev, phase: execute), `qa.md` (agent: qa, phase: qa), `verify-work.md` (agent: qa, phase: verify-work), `release.md` (agent: release, phase: release), `closure.md` (agent: qa with prompt `role=qe` per DEC-0051 / US-0120 — no `qe.md` agent in pack, phase: closure), `refresh-context.md` (agent: curator, phase: refresh-context), `auto.md` (agent: auto + `subtask: false` — dispatch-only, no spawn logic per DQ5), `quick.md` (agent: tech-lead — mega_quick delivery-mode entry per US-0096 / DEC-0082), `ask.md` (omits `agent:` — agent-agnostic, read-only). Each file: frontmatter (`description: "its-magic <phase>: <one-line role summary>."` + `agent: <role>`; `/auto` adds `subtask: false`; `/ask` omits `agent`) + dispatch-only body (≤ ~12 lines) naming the phase_id + artifact path list + STOP. No `model:` in any template command (US-0102 + US-0123 — `test_us0125_command_frontmatter_shape` marker 11 enforces). No `$ARGUMENTS`, no shell injection, no `@file` inclusion. Each file ≤ 20 lines (DQ2 line cap — `test_us0125_clone_guard` marker 2 enforces). No 200-line Cursor command clones (AC-1, AC-9 — `test_us0125_cursor_commands_unchanged` marker 9 + `test_us0125_command_inventory` marker 1 enforce). Tests: marker 1 asserts 15 files present + no extra + no `.gitkeep` after populate; marker 11 asserts frontmatter shape; marker 8 asserts `/auto` dispatch-only (≤ 20 lines + no `ctx.session.create`/`Session.create`/`spawn` literals + `agent: auto` frontmatter present). (AC-1)

- [x] **T-002**: Clone-guard contract test — Create `test_us0125_clone_guard` marker inside `tests/us0125_contract_test.py` per architecture DQ2 LOCKED + DEC-0125 §2. Two metrics, defense in depth: (i) per-file line cap ≤ 20 (including frontmatter + body); (ii) normalized-text similarity ≤ 0.30 vs `.cursor/commands/<name>.md` via stdlib `difflib.SequenceMatcher` (no new test dependency). **Normalization strip list LOCKED** (critic NB `ik_us0125_dq2_normalization_strip_list_open` closed here): the strip list is documented as a Python constant `US0125_CLONE_GUARD_STRIP_TOKENS` in the test file. Strip order: (1) strip frontmatter (text between leading `---` fences); (2) lowercase; (3) strip punctuation (replace `[^\w\s]` with space); (4) strip the canonical phase id token (e.g. `intake`, `discovery`, ..., `ask`); (5) strip the shared vocabulary words: `its-magic`, `command`, `phase`, `artifact`, `STOP`, `run`, `validator`, `plugin`, `script`, `python`, `scripts`, `repo`, `the`, `a`, `an`, `to`, `of`, `and`, `or`, `before`, `after`, `above`, `below`, `path`, `list`, `id`. After stripping, compute `difflib.SequenceMatcher(None, normalized_opencode, normalized_cursor).ratio()` and assert ≤ 0.30. `test_us0125_clone_guard` iterates over the 15 shipped `.opencode/commands/*.md` files; for each, asserts (i) line count ≤ 20, (ii) normalized similarity vs `.cursor/commands/<name>.md` ≤ 0.30. Fails on either violation. The strip list constant is the single source of truth so US-0126 inherits it without re-derivation. (AC-2)

- [x] **T-003**: Validator→artifact mapping table — verify-or-extract-to-test-fixture. The mapping table already lives in the US-0125 architecture section (`docs/engineering/architecture.md` L1939-L1945 — authored in /architecture phase; consumed read-only by the US-0124 plugin `ctx.tool.hook("execute.before")`). T-003 in /execute is **verify-or-extract-to-test-fixture**, NOT a rewrite of architecture.md. /execute work: (a) verify the mapping table is present in `docs/engineering/architecture.md # US-0125` (3 rows: `handoffs/intake_evidence/*.json` → `scripts/intake_evidence_validate.py --repo . --enforce` with reason codes `INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, ...; `docs/product/backlog.md` bug rows + `docs/product/acceptance.md` bug rows → `scripts/bug_issue_validate.py --repo . --check-acceptance` with reason code `BUG_ISSUE_VALIDATION_FAILED`, ...; other persistence-blocking artifacts → generic bridge contract `python scripts/<validator>.py --repo . [--enforce] [--scope <scope>]` — US-0126 owns enumeration); (b) extract the mapping into a test fixture (e.g. `tests/us0125/fixtures/validator_artifact_mapping.json`) consumed by `test_us0125_validator_subprocess_fail_closed` (marker 3) and `test_us0125_release_blocked_after_failing_validator` (marker 4) so the contract tests do not re-parse architecture.md prose at runtime; (c) assert the mapping is additive data (US-0125-owned, US-0124-consumed) — no plugin code change in `template/.opencode/plugins/orchestrator.ts`. T-003 does NOT mutate `docs/engineering/architecture.md` (T-anch NO-OP ceremony preserves the architecture mapping table as the locked source of truth). (AC-3, AC-4)

- [x] **T-004**: Validator subprocess bridge — command prose line shape. Author the validator-subprocess bridge line shape in the 12 lifecycle phase command bodies + `/auto` + `/quick` + `/ask` per architecture DQ3 + DQ4 + DQ7 LOCKED + DEC-0125 §3, §4, §7. Each lifecycle command body that owns a persistence-blocking artifact (e.g. `/intake` → `handoffs/intake_evidence/*.json`; `/release` → `handoffs/release_queue.md`, `handoffs/releases/*-release-notes.md`; etc.) includes a short line: "Before writing to `<artifact>`, run `python scripts/<validator>.py --repo .` and surface any non-zero exit reason code to the operator. The orchestrator plugin enforces persistence." This is *informational* (DQ4 — diagnostics, not enforcement). The plugin `ctx.tool.hook("execute.before")` enforcement is US-0124 territory — US-0125 authors the contract prose, US-0124 authors the hook. Reason codes: raw Python reason codes for validator non-zero exit (e.g. `INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`); `OPENCODE_DRIVER_INVOKE_FAILED` (DEC-0124 DQ6) for subprocess invocation failure (missing Python, missing script, timeout); no new `OPENCODE_*` wrapper (DQ7 — `test_us0125_reason_code_raw_python` marker 5 asserts zero hits for `OPENCODE_VALIDATOR_FAILED` wrapper). No silent skip (AC-5). Tests: marker 3 asserts bridge contract for the two named CLIs — stubbed non-zero → command/plugin does not proceed to persistence; marker 5 asserts no `OPENCODE_VALIDATOR_FAILED` wrapper; marker 6 (`test_us0125_no_policy_in_commands`) asserts no policy text duplicating validator logic (grep 15 command files for policy text — zero hits). (AC-3, AC-5)

- [x] **T-005**: Mock-subprocess harness extension — Extend the US-0124 `MockCtx` harness (`tests/us0124/mock_ctx.ts`) with a `mockSubprocess` field OR add a sibling `tests/us0125/mock_subprocess.ts` imported by the US-0125 test, per architecture DQ8 LOCKED + DEC-0125 §8. The mock subprocess accepts a scripted `nextExitCode` (0 or non-zero) + `nextStderr` (the raw Python reason code) + `nextThrow` (for `OPENCODE_DRIVER_INVOKE_FAILED` simulation). The plugin's `ctx.tool.hook("execute.before")` calls the mock subprocess; tests assert the hook refuses the write on non-zero. No OpenCode runtime dependency — CI runs pure Node/Bun (same as US-0124). **Runner: Node** (consistent with US-0124 DQ3; CI already has it via `tests/run-tests.ps1 Ensure-NodeOnPath`); Bun optional. Tests: marker 4 (`test_us0125_release_blocked_after_failing_validator`) — success test (b) — load `template/.opencode/plugins/orchestrator.ts` via dynamic import, call `setup(mockCtx)`, program `mockCtx.subprocess` to return exit code 1 + stderr `INTAKE_PERSISTENCE_BLOCKED`, drive the plugin's `ctx.tool.hook("execute.before")` with a synthetic `edit` tool call to a release-persistence artifact path, assert the hook (i) calls `mockCtx.subprocess` with the expected validator argv, (ii) refuses the write, (iii) emits the raw Python reason code `INTAKE_PERSISTENCE_BLOCKED` (not a wrapper); repeat with `mockCtx.subprocess` programmed to throw → assert `OPENCODE_DRIVER_INVOKE_FAILED` and refuse the write; marker 10 (`test_us0125_no_new_npm_runtime`) asserts no new runtime deps in `package.json` + consumer app code. (AC-4, AC-8, AC-10)

- [x] **T-006**: Create `tests/us0125_contract_test.py` with 11 markers per architecture AC-8 table + DEC-0125 §9:
  1. `test_us0125_command_inventory` — 15 files present at `template/.opencode/commands/`; no extra; no `.gitkeep` after populate (AC-1).
  2. `test_us0125_clone_guard` — per-file line cap ≤ 20 + normalized-text similarity ≤ 0.30 via `difflib.SequenceMatcher` vs `.cursor/commands/<name>.md`; strip list per T-002 constant `US0125_CLONE_GUARD_STRIP_TOKENS` (AC-2).
  3. `test_us0125_validator_subprocess_fail_closed` — bridge contract for the two named CLIs (`intake_evidence_validate.py`, `bug_issue_validate.py`) — stubbed non-zero → command/plugin does not proceed to persistence (AC-3).
  4. `test_us0125_release_blocked_after_failing_validator` — success test (b) — mock-ctx+mock-subprocess; validator non-zero → plugin `ctx.tool.hook("execute.before")` refuses write to release persistence path; raw Python reason code emitted; subprocess throw → `OPENCODE_DRIVER_INVOKE_FAILED` (AC-4).
  5. `test_us0125_reason_code_raw_python` — grep command/plugin source for `OPENCODE_VALIDATOR_FAILED` wrapper — zero hits; raw Python codes surface as-is; `OPENCODE_DRIVER_INVOKE_FAILED` only for subprocess invocation failure (AC-5).
  6. `test_us0125_no_policy_in_commands` — grep 15 command files for policy text duplicating validator logic — zero hits (AC-6).
  7. `test_us0125_missing_command_does_not_disable_plugin` — delete a command file in a temp copy → plugin still loads via `.opencode/plugins/` auto-discovery; `@auto` agent still invocable (AC-7).
  8. `test_us0125_auto_command_dispatch_only` — `auto.md` ≤ 20 lines + no `ctx.session.create`/`Session.create`/`spawn` literals + `agent: auto` frontmatter present (AC-1, AC-7).
  9. `test_us0125_cursor_commands_unchanged` — git diff `.cursor/commands/*.md` — zero changes (AC-9).
  10. `test_us0125_no_new_npm_runtime` — grep `package.json` + consumer app code for new runtime deps — zero hits; validator bridge is kit scripts + plugin subprocess (AC-10).
  11. `test_us0125_command_frontmatter_shape` — 15 files: `description` present; `agent` present for 14 (omitted for `/ask`); no `model:` in any; `subtask: false` only on `/auto` (AC-1, AC-8).
  Mirror to `template/tests/us0125_contract_test.py` byte-identical for parity pairing. (AC-8)

- [x] **T-007**: Installer manifest rows — Add `template/.opencode/commands/**` source row under `[opencode_install_include_paths]` in `docs/engineering/context/installer-owned-paths.manifest` AND `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical). Existing rows UNCHANGED — additive row only. Triple-installer (PS/Bash/Python) reads opencode sections only when `--host` includes opencode (US-0121 compose; `host_gates_cursor_row` predicate). (AC-1)

- [x] **T-008**: README + parity + runbook stub — Extend `scripts/check_intake_template_parity.py` `--scope=opencode-adapter` `OPENCODE_ADAPTER_PAIRS` to cover the 15 command files + mock-subprocess harness + contract-test surface (byte-identical active ↔ template pairs where applicable; materializer is kit-only, not paired). Update `its_magic/README.md` to cross-link the OpenCode thin commands + validator bridge capability + pointer to DEC-0125. Add `## OpenCode thin commands + validator bridge (US-0125)` h2 stub to `docs/engineering/runbook.md` as a **stub one-liner per code** per DEC-0125 §7 — list the two named validator CLIs (`intake_evidence_validate.py`, `bug_issue_validate.py`) + their canonical Python reason codes (`INTAKE_PERSISTENCE_BLOCKED`, `INTAKE_REQUIRED_TOPIC_MISSING`, `BUG_ISSUE_VALIDATION_FAILED`, ...) + cross-link to US-0126 for the full reason-code table. US-0126 owns the full runbook section text; US-0125 ships the stub only — no duplication of remediation text. **MUST keep `docs/engineering/runbook.md` byte-identical with `template/docs/engineering/runbook.md` after edit** — edit both files identically (verified via `python -c "a=open('docs/engineering/runbook.md','rb').read(); b=open('template/docs/engineering/runbook.md','rb').read(); assert a==b"`). Mirror parity script to `template/scripts/check_intake_template_parity.py` byte-identical. (AC-8)

- [x] **T-009**: Validator extension — default no new script. Default = extend contract tests (T-006) + reuse `scripts/model_tier_validate.py --scope opencode-catalog` from US-0123; do NOT create a new `scripts/opencode_command_validate.py`. Fall back to a new validator script ONLY if US-0125 command files need static validation beyond contract tests AND coupling forces a separate validator class (trigger: command-specific checks cannot reuse >50% of existing `--scope opencode-catalog` helpers, OR scope-tag plumbing requires touching >3 unrelated `--scope` modes). If fallback triggers, raise a DEC follow-up; do NOT silently split. (AC-8)

## Integration verification (post T-009 + T-006)

- [x] Test gate: `python -m pytest tests/us0125_contract_test.py -v` → 11/11 PASS
- [x] Parity gate: `check_intake_template_parity.py --scope=opencode-adapter` PASS
- [x] Parity gate: active + template manifest byte-identical
- [x] Parity gate: active + template runbook byte-identical
- [x] Compose gate: 7/7 UNCHANGED
- [x] No-secrets gate: `api_key`/`apikey`/`sk-`/`auth.json`/`.env` grep zero hits on command files + harness
- [x] No-Cursor-clone gate: unique-to-Cursor phrases zero hits on command files (per T-002 strip list)
- [x] Clone-guard gate: 15 files ≤ 20 lines + normalized similarity ≤ 0.30 vs `.cursor/commands/<name>.md`
- [x] Frontmatter gate: 15 files `description` present; `agent` present for 14 (omitted for `/ask`); no `model:`; `subtask: false` only on `/auto`
- [x] Auto-dispatch gate: `auto.md` has no `ctx.session.create`/`Session.create`/`spawn` literals
- [x] No-new-npm-runtime gate: `package.json` + consumer app code grep zero hits for new runtime deps

## Files to touch (scope)

### New (create)

- `template/.opencode/commands/intake.md`
- `template/.opencode/commands/discovery.md`
- `template/.opencode/commands/research.md`
- `template/.opencode/commands/architecture.md`
- `template/.opencode/commands/sprint-plan.md`
- `template/.opencode/commands/plan-verify.md`
- `template/.opencode/commands/execute.md`
- `template/.opencode/commands/qa.md`
- `template/.opencode/commands/verify-work.md`
- `template/.opencode/commands/release.md`
- `template/.opencode/commands/closure.md`
- `template/.opencode/commands/refresh-context.md`
- `template/.opencode/commands/auto.md`
- `template/.opencode/commands/quick.md`
- `template/.opencode/commands/ask.md`
- `tests/us0125_contract_test.py`
- `template/tests/us0125_contract_test.py` (byte-identical mirror for parity)
- `tests/us0125/mock_subprocess.ts` (or extension to `tests/us0124/mock_ctx.ts`)
- `tests/us0125/fixtures/validator_artifact_mapping.json` (extracted from architecture.md — T-003)
- `sprints/S0125/t-anch-verification.md`

### Edit (scoped, additive only)

- `scripts/check_intake_template_parity.py` (extend `OPENCODE_ADAPTER_PAIRS` for 15 command files + mock-subprocess harness + contract-test surface)
- `template/scripts/check_intake_template_parity.py` (byte-identical mirror)
- `docs/engineering/context/installer-owned-paths.manifest` (add `template/.opencode/commands/**` source row under `[opencode_install_include_paths]`)
- `template/docs/engineering/context/installer-owned-paths.manifest` (byte-identical)
- `docs/engineering/runbook.md` (append `## OpenCode thin commands + validator bridge (US-0125)` h2 stub + US-0126 cross-link placeholder)
- `template/docs/engineering/runbook.md` (byte-identical mirror)
- `its_magic/README.md` (cross-link OpenCode thin commands + validator bridge capability + DEC-0125 pointer)
- `scripts/model_tier_validate.py` (extend `--scope opencode-catalog` ONLY if T-009 fallback triggers; default = no edit)

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # US-0125` (T-anch NO-OP; mapping table at L1939-L1945 is the locked source of truth — T-003 extracts to fixture, does NOT mutate)
- `decisions/DEC-0125.md` (T-anch NO-OP)
- `template/.opencode/agents/*.md` (US-0122 — agent files unchanged; commands bind via `agent:` frontmatter per DQ5/DQ8)
- `template/.opencode/plugins/orchestrator.ts` (US-0124 — plugin unchanged; US-0125 authors mapping data, not plugin code)
- `.cursor/commands/*.md` (25 files — read-only compose for clone-guard baseline; `test_us0125_cursor_commands_unchanged` marker 9 enforces zero diff)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| Compose-guard story surfaces (US-0001, US-0078/DEC-0060, US-0121/DEC-0120, US-0122/DEC-0122, US-0124/DEC-0124, US-0126, US-0102/DEC-0087) | 7/7 UNCHANGED — US-0125 adds additive commands + bridge contract + stub harness only |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (dispatch-only commands) | T-001, T-006 (markers 1, 8, 11), T-007 |
| AC-2 (clone guard) | T-002, T-006 (marker 2) |
| AC-3 (validator source of truth) | T-003, T-004, T-006 (markers 3, 4) |
| AC-4 (success test b) | T-003, T-005, T-006 (marker 4) |
| AC-5 (fail-closed reason codes) | T-004, T-006 (marker 5) |
| AC-6 (no policy in commands) | T-006 (marker 6) |
| AC-7 (optional commands) | T-006 (markers 7, 8) |
| AC-8 (contract tests) | T-006 (all 11 markers), T-008 (parity + runbook stub) |
| AC-9 (compose US-0001) | T-anch (baseline), T-006 (marker 9) |
| AC-10 (no new npm runtime) | T-005, T-006 (marker 10) |

**Surjectivity check**: 10/10 ACs covered (AC-1..AC-10 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
