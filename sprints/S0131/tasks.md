# Sprint S0131 - Task checklist (BUG-0015)

Total tasks: 7 (T-anch + T-001..T-006). SPRINT_MAX_TASKS=12; SPRINT_AUTO_SPLIT=1; no split needed.

**Isolation**: `tl-BUG0015-sprint-plan-20260906T143000Z-fresh` · `model_id=composer-2.5` · `orchestrator_run_id=auto-20260906-bug0015`

## Task execution order

1. T-anch (NO-OP / verification)
2. T-001 (`command.transform` / `editor.add({ name: "auto", execute })` attach + missing-attach fail-closed; active + template)
3. T-002 (`runAutoLifecycle` + mutex TTL 7200s / clear-on-exit + spawnPhase / dispatchStopMatrix loop + headless compose)
4. T-003 (Python IsolationEvidence → state.md bridge + first-phase selectors argv → resume_brief → scratchpad → US-0087)
5. T-004 (`auto.md` STOP-only assert; active + template; no spawn literals)
6. T-005 (NEW `tests/bug0015_contract_test.py` + template mirror — 7 markers; do not amend us0124/us0125)
7. T-006 (runbook h3 stub for two new reason codes + US-0126 cross-link; optional parity scope `bug-0015`)
8. Integration verification

## Critic NB awareness (execute)

- **T-002 / T-005** (`b0015ar-challenger-001` / `ik_bug0015_arch_edge_and_proof`): Prove mutex gate on dual-fire / secondary `command.executed` after STOP (marker 5). Document mutex TTL clock source + clear-on-fail-closed paths.
- **T-003 / T-006** (`b0015ar-architect-002` / `ik_bug0015_arch_layer_coupling`): IsolationEvidence + first-phase via Python only (no OpenCode-only resolver). Runbook h3 stub only (US-0126 owns full table). Active+template parity for orchestrator.ts / auto.md / bug0015_contract_test.
- **T-anch / scope** (`b0015ar-subtractor-003` / `ik_bug0015_arch_scope_minimal`): T-anch read-only; no architecture.md mutation; do not mark BUG-0015 DONE; 7 markers required; do not expand to BUG-0016 / live OpenCode probe / DEC amend.

## Task checklist

- [x] **T-anch**: Verify `# BUG-0015` H1 present in `docs/engineering/architecture.md` (added in /architecture per DEC-0076); verify approach A* locked + R-0114 DQ1–DQ7 LOCKED + CF1–CF7 CLOSED; verify companion DEC none; verify DEC-0124 / DEC-0125 bodies not amended; verify 7-marker contract-test list locked; verify compose guards (no BUG-0016 / US-0131/US-0132 / Cursor Task / TS stop-matrix / live probe); verify `tests/bug0015_contract_test.py` does NOT yet exist (or document baseline if partially present); verify `.opencode/plugins/orchestrator.ts` still lacks `command.transform` / `editor.add({ name: "auto" })` attach (gap still present pre-execute). Record results to `sprints/S0131/t-anch-verification.md`. T-anch is NO-OP / verification only — NO mutation to `docs/engineering/architecture.md` in /execute. (AC-7 baseline; NO-OP / verification only)

- [x] **T-001**: Edit `.opencode/plugins/orchestrator.ts` AND `template/.opencode/plugins/orchestrator.ts` (byte-identical) per architecture DQ1 / CF1 / CF6. In `setup(ctx)`, register `ctx.command.transform` → `editor.add({ name: "auto", execute })` as **primary** host-invoked entry. `execute` must call `runAutoLifecycle` (implemented in T-002 — may stub-wire then complete). If `ctx.command.transform` unavailable **and** no usable event subscribe attach → emit **`OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED`**, stop `/auto`. Do **not** treat returning `{ spawnPhase }` from `setup()` as attach. Optional secondary `ctx.event.subscribe` / `command.executed` for `name === "auto"` — defense only, mutex-gated (second entry → `OPENCODE_AUTO_ALREADY_RUNNING`). Preserve existing `tool.hook("execute.before")` write-guard (DEC-0124 DQ8). MUST keep active ↔ template byte-identical after edit. Tests: markers 1, 3. (AC-1, AC-2)

- [x] **T-002**: In same plugin surfaces (active + template), implement shared internal **`runAutoLifecycle(ctx, opts)`** per architecture DQ2/DQ4 / CF4/CF5. Owns: in-flight mutex (clear-on-exit success or fail-closed; safety TTL **7200s**); call `spawnPhase` + `dispatchStopMatrix` loop; wire headless `invokeHeadless` compose path through the same entry. Concurrent/re-entrant → **`OPENCODE_AUTO_ALREADY_RUNNING`** (distinct from `AUTO_SCHEDULER_CONFLICT`). Missing `session.create` → existing **`OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`**. Document mutex TTL clock source in code comment. MUST keep active ↔ template byte-identical. Tests: markers 2, 4, 5. (AC-1, AC-3, AC-5)

- [x] **T-003**: Implement IsolationEvidence durable write via **Python subprocess bridge** appending to `docs/engineering/state.md` (US-0048 / DEC-0029 SOT) — prefer thin helper or extend existing driver argv; **not** `ctx.storage` as durable SOT. Minimum fields: `parentID`, `sessionID`, `role`, `phase_id`, `timestamp`, `fresh_context_marker` with `sessionID !== parentID`. Null/throw/identical-id → **`OPENCODE_SUBTASK_IGNORED`**. First-phase selection via Python kit selectors: argv → resume_brief → scratchpad → US-0087 bug-queue (mutex `AUTO_SCHEDULER_CONFLICT` unchanged). No OpenCode-only TS resolver (CF2/CF3). Active+template plugin call sites + any new Python helper mirrored. (AC-4)

- [x] **T-004**: Keep `.opencode/commands/auto.md` AND `template/.opencode/commands/auto.md` STOP-only (DEC-0125 DQ5): ≤20 lines; no spawn literals (`ctx.session.create` / `Session.create` / spawn-call logic in body). Discoverability + `agent: auto` binding only — must **not** dual-fire spawn. MUST keep active ↔ template byte-identical. Tests: marker 6. (AC-6)

- [x] **T-005**: Create `tests/bug0015_contract_test.py` with 7 markers per architecture DQ6 (AC-8). Markers:
  1. `test_bug0015_command_transform_registers_auto` — `setup` registers transform / `editor.add({ name: "auto" })`
  2. `test_bug0015_auto_execute_invokes_spawn_phase` — mock execute → `session.create` with parentID/agent
  3. `test_bug0015_missing_attach_fail_closed` — no attach → `OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED`
  4. `test_bug0015_missing_session_create_fail_closed` — attach ok, create missing → `OPENCODE_PLUGIN_SPAWN_UNSUPPORTED`
  5. `test_bug0015_concurrent_reentry_fail_closed` — second `/auto` → `OPENCODE_AUTO_ALREADY_RUNNING`
  6. `test_bug0015_auto_md_dispatch_only_static` — `auto.md` ≤20 lines; no spawn literals
  7. `test_bug0015_compose_us0124_spawn_api_unchanged` — existing `spawnPhase` / reason-code exports present (read-only)
All markers mock-ctx / static; **no live OpenCode probe**. Do **not** amend `test_us0124_*` / `test_us0125_*`. Mirror to `template/tests/bug0015_contract_test.py` byte-identical. Extend mock-ctx harness additively if needed. (AC-2..AC-8)

- [x] **T-006**: Edit `docs/engineering/runbook.md` AND `template/docs/engineering/runbook.md` (byte-identical). Add BUG-0015 h3 stub documenting **`OPENCODE_PLUGIN_DISPATCH_ATTACH_UNSUPPORTED`** and **`OPENCODE_AUTO_ALREADY_RUNNING`**; cross-link US-0126 full reason-code table (do not move ownership). Optional: add parity scope `bug-0015` in `check_intake_template_parity.py` for touched OpenCode plugin/command/test surfaces if a clean pair set exists — do not invent broad new scopes. (AC-2, AC-5)

## Integration verification (post T-006)

- [x] Test gate: `python -m pytest tests/bug0015_contract_test.py -v` -> 7/7 PASS
- [x] Compose gate: do not amend `tests/us0124_*` / `tests/us0125_*` bodies; existing markers still green if run
- [x] Parity gate: active + template `orchestrator.ts` byte-identical
- [x] Parity gate: active + template `auto.md` byte-identical
- [x] Parity gate: active + template `bug0015_contract_test.py` byte-identical (if mirrored)
- [x] Parity gate: active + template runbook.md byte-identical
- [x] Compose gate: DEC-0124 / DEC-0125 / DEC-0122 bodies UNCHANGED
- [x] Scope gate: no BUG-0016 permission edits; no US-0131/US-0132; no live OpenCode CI probe; no Cursor Task port; no TS stop-matrix rewrite
- [x] Status gate: BUG-0015 remains OPEN; acceptance BUG-0015 unchecked; intake JSON not mutated

## Files to touch (scope)

### New (create)

- `tests/bug0015_contract_test.py`
- `template/tests/bug0015_contract_test.py` (byte-identical mirror for parity)
- Thin Python isolation/resume helper (if not extending existing driver argv) + template mirror if applicable
- `sprints/S0131/t-anch-verification.md`

### Edit (scoped, additive only)

- `.opencode/plugins/orchestrator.ts` (attach + `runAutoLifecycle` + mutex + reason codes + isolation write bridge)
- `template/.opencode/plugins/orchestrator.ts` (byte-identical mirror)
- `.opencode/commands/auto.md` (STOP-only assert only — no spawn literals)
- `template/.opencode/commands/auto.md` (byte-identical mirror)
- `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` (BUG-0015 h3 stub)
- Optional: `scripts/check_intake_template_parity.py` + template (`bug-0015` scope pairs)
- Optional: mock-ctx harness extension used by contract tests

### Verify read-only (no mutation)

- `docs/engineering/architecture.md # BUG-0015` (T-anch NO-OP; locked source of truth)
- `docs/product/backlog.md ### BUG-0015` (read-only Status/ACs — US-0045; sprint_plan_notes already written this phase)
- `docs/product/acceptance.md` BUG-0015 row (read-only — US-0045 derived view)
- `handoffs/intake_evidence/BUG-0015-intake-20260906.json` (read-only — never mutate prior intake evidence)
- `docs/engineering/research.md ## R-0114` (read-only)

### Compose-guard UNCHANGED (DO NOT TOUCH)

| File | Reason |
|---|---|
| `docs/product/backlog.md` Status/ACs | US-0045 canonical status — `/closure` mutates ONLY at execution time |
| `docs/product/acceptance.md` | US-0045 derived view — same |
| `docs/engineering/architecture.md` | Do not rewrite; T-anch is verification only |
| `decisions/DEC-0124.md` / `decisions/DEC-0125.md` | Compose-only; bodies UNCHANGED |
| `decisions/DEC-0122.md` + `.opencode/agents/*.md` matrix | BUG-0016 out of scope |
| `tests/us0124_*` / `tests/us0125_*` bodies | Do not amend (DQ6) |
| US-0131 / US-0132 backlog rows | Do not reopen |
| US-0126 full reason-code ownership | Stub + cross-link only |

## AC -> Task surjective coverage

| AC | Task(s) |
|---|---|
| AC-1 (`/auto` starts spawn via attach) | T-001, T-002, T-005 (markers 1, 2) |
| AC-2 (missing attach fail-closed) | T-001, T-005 (marker 3), T-006 |
| AC-3 (missing session.create) | T-002, T-005 (marker 4) |
| AC-4 (IsolationEvidence + state.md) | T-003, T-005 |
| AC-5 (concurrent `/auto` mutex) | T-002, T-005 (marker 5), T-006 |
| AC-6 (`auto.md` dispatch-only) | T-004, T-005 (marker 6) |
| AC-7 (compose US-0124 spawn API) | T-anch, T-005 (marker 7) |
| AC-8 (seven additive markers) | T-005 (all 7 markers) |

**Surjectivity check**: 8/8 ACs covered (AC-1..AC-8 each have at least 1 task). No `PLAN_AC_COVERAGE_GAP`.
