# Sprint S0119

## Metadata

- **sprint_id**: S0119
- **story_refs**: US-0119
- **priority**: P1
- **effort**: 1–2 days
- **owner**: dev
- **goal**: Ship autonomous-autonomy presets (`AUTONOMY_PRESET={none|balanced|full}`) plus configurable hard-stop relaxation (`AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}`). Single `AUTONOMY_PRESET` scratchpad flag deterministically expands into twelve per-feature autonomy flags; `AUTONOMY_STOP_POLICY` dispatches every fail-closed reason code through a two-tier classification (`security_hard` / `autonomy_resolvable`) with bounded auto-repair ledger. `AUTONOMY_PRESET=none` is byte-identical pre-US-0119 behaviour. Compose read-only with US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 (additive only — preset expansion uses existing flag keys, stop policy is a dispatch layer on top of existing reason codes).
- **status**: OPEN (per US-0045 — closure at /release)
- **created_at**: 2026-07-05T22:52:00Z
- **orchestrator_run_id**: auto-20260705-01
- **delivery_mode**: ultra_lean
- **macro_phase**: plan (sprint-plan — third canonical phase of plan macro per US-0096 / DEC-0082; research + architecture + sprint-plan merged)
- **fresh_context_marker**: tl-US0119-sprint-plan-20260705T225200Z-fresh
- **resolved_phase_plan**: `["spec","plan","build+verify","ship"]` (ultra_lean macro — `spec` already done via intake+discovery merged; `plan` = research + architecture + sprint-plan all complete; `build+verify` = `/execute` + `/qa`; `ship` = `/release` + `/refresh-context`)

## Scope

- **US-0119**: Autonomous-autonomy presets + configurable hard-stop relaxation — `AUTONOMY_PRESET` scratchpad flag + `AUTONOMY_STOP_POLICY` + stop-matrix manifest + 12 per-feature flag wiring + bounded repair ledger + breadcrumb
- **Architecture anchor**: `docs/engineering/architecture.md` `## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation` (L1925; approach_locked=A1)
- **Research anchor**: `docs/engineering/research.md` `## R-0107 - US-0119 Autonomous-autonomy presets research` (10/10 open questions Q1..Q10 closed LOCKED)
- **Companion DEC**: **DEC-0119** (Required → Accepted; authored in architecture phase at `decisions/DEC-0119.md`; locks AUTONOMY_PRESET 3-tier enum + AUTONOMY_STOP_POLICY 3-value enum + 2-tier stop classification + 9-value auto_repair_kind taxonomy + cap=3 + AUTONOMY_PRESET=none byte-identity + 12 per-feature flags additive + precedence explicit>preset>defaults)

## DC resolution note

US-0119 is a continuation story (post-US-0118 drain). `grep "^## US-0119" docs/engineering/architecture.md` prior to the `/architecture` phase → no matches. The `## US-0119` h1 anchor was **added in the `/architecture` phase** (per R-0105 Q-2 LOCKED pattern — architecture artifacts live in `architecture.md`, not `/execute`). US-0118 had already resolved all DC candidates (US-0117 was the final deferred-candidate resolution point — 36 anchors). US-0119 inherits a clean deferral register; no DC candidates created or carried. **Consequence for this sprint**: **T-anch is a NO-OP / verification task** — the `## US-0119` anchor already exists at architecture.md L1925; T-anch verifies it remains present and that `git diff HEAD -- docs/engineering/architecture.md` shows no execute-phase edits to architecture.md.

## Acceptance criteria (US-0119 — 12 ACs verbatim from `docs/product/backlog.md` `## US-0119`)

| AC | Description (verbatim) |
|----|-------------|
| AC-1 | **AUTONOMY_PRESET scratchpad flag** — new `AUTONOMY_PRESET=none|balanced|full` (default `none`) in `.cursor/scratchpad.md` plus `template/.cursor/scratchpad.local.example.md`. When `none`, byte-identical pre-US-0119 behaviour. When `balanced` or `full`, deterministic expansion into per-feature autonomy flags documented in AC-2. |
| AC-2 | **Deterministic preset expansion** — `scripts/autonomy_preset_lib.py:expand_autonomy_preset(preset, overrides) -> dict` returns the flag bundle. Every preset line expands into already-existing scratchpad keys only; no new consumer semantics invented here. Explicit per-flag values in scratchpad (or scratchpad.local) always win over preset expansion. |
| AC-3 | **AUTONOMY_STOP_POLICY flag** — new `AUTONOMY_STOP_POLICY=block|auto_repair_then_block|auto_repair_then_skip` (default `block`). Every fail-closed reason code classified in `docs/engineering/autonomy-stop-matrix.md` as `security_hard` (never auto-resolved) or `autonomy_resolvable` (bounded auto-repair with a ledger cap). |
| AC-4 | **Autonomy stop matrix manifest** — new authoritative file `docs/engineering/autonomy-stop-matrix.md` plus `template/docs/engineering/autonomy-stop-matrix.md` (parity). YAML companion `scripts/data/autonomy_stop_matrix.yaml` with `scripts/validate_autonomy_stop_matrix.py` enforcing (a) no orphan code in scripts, (b) `security_hard` rows carry `auto_repair_kind=n/a`, (c) `autonomy_resolvable` rows carry finite `cap`. |
| AC-5 | **Per-feature autonomy flags wired** — each of the twelve flags in the preset expansion is documented and consumed. |
| AC-6 | **Backward compatibility is the default** — `AUTONOMY_PRESET=none` produces byte-identical orchestrator behaviour to pre-US-0119. Contract test `test_us0119_preset_none_is_noop` asserts the byte-identity surface. |
| AC-7 | **Security-hard gates never softened** — matrix `security_hard` rows include 18+ reason codes. Contract test `test_us0119_security_hard_gates_never_auto_repaired` fails on divergence. |
| AC-8 | **Bounded auto-repair ledger** — new append-only file `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl`. Cap per `(run, reason_code)` taken from matrix `cap` column (default 3). Cap exhaustion escalates with `AUTONOMY_REPAIR_CAP_EXHAUSTED`. File gitignored. |
| AC-9 | **Operator authority preserved** — breadcrumb `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` in `docs/engineering/state.md`. |
| AC-10 | **Tests + parity** — `tests/us0119_autonomy_preset_test.py` covering 10 markers. `check_intake_template_parity.py --scope=us-0119` enforces parity. `scripts/validate_autonomy_stop_matrix.py --self-test` exits 0. |
| AC-11 | **Documentation** — `docs/engineering/autonomy-stop-matrix.md`, `docs/engineering/architecture.md` `## US-0119`, `docs/engineering/runbook.md` `## Autonomy presets (US-0119)`, `.cursor/commands/auto.md` `## Autonomy presets (US-0119)`. Template parity. |
| AC-12 | **Compose, do not amend** — US-0092/US-0095/US-0056/US-0068/US-0096/BUG-0007 untouched. Contract test `test_us0119_preset_expansion_uses_known_keys_only` enforces it. |

## AC → task surjective coverage (12 tasks, 12 ACs)

| AC | Task(s) | Architecture anchor |
|----|---------|---------------------|
| AC-1 (AUTONOMY_PRESET scratchpad flag) | T-002 | § Sprint seeds T-002 |
| AC-2 (Deterministic preset expansion) | T-001 | § Sprint seeds T-001 |
| AC-3 (AUTONOMY_STOP_POLICY flag) | T-002 | § Sprint seeds T-002 |
| AC-4 (Autonomy stop matrix manifest) | T-003 | § Sprint seeds T-003 |
| AC-5 (Per-feature autonomy flags wired) | T-004 | § Sprint seeds T-004 |
| AC-6 (Backward compatibility default) | T-007, T-011 | § Sprint seeds T-007 / T-011 |
| AC-7 (Security-hard gates never softened) | T-003, T-007 | § Sprint seeds T-003 / T-007 |
| AC-8 (Bounded auto-repair ledger) | T-005 | § Sprint seeds T-005 |
| AC-9 (Operator authority / breadcrumb) | T-006 | § Sprint seeds T-006 |
| AC-10 (Tests + parity) | T-007, T-008, T-010, T-011 | § Sprint seeds T-007 / T-008 / T-010 / T-011 |
| AC-11 (Documentation) | T-008, T-009, T-anch | § Sprint seeds T-008 / T-009 / T-anch |
| AC-12 (Compose, do not amend) | T-anch, T-007 | § Sprint seeds T-anch / T-007 |

**Surjectivity check**: AC-1..AC-12 all covered (12/12) + DC resolution verified (T-anch). Multi-AC tasks: **T-007** (AC-6+AC-7+AC-10 partial+AC-12 indirect), **T-003** (AC-4+AC-7 partial), **T-008** (AC-10+AC-11 partial), **T-002** (AC-1+AC-3), **T-anch** (AC-11 partial+AC-12). Every AC has ≥1 task. No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 12 (T-anch + T-001..T-011)
- **SPRINT_MAX_TASKS**: 12 (from `.cursor/scratchpad.md`)
- **Within limit**: yes (12 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **SPRINT_AUTO_SPLIT_TRIGGERED**: false

## Compose, do not amend (verified — 6/6)

| Story | Status |
|-------|--------|
| US-0092 / DEC-0078 | ✓ UNCHANGED |
| US-0095 | ✓ UNCHANGED |
| US-0056 / DEC-0038 | ✓ UNCHANGED |
| US-0068 / DEC-0060 | ✓ UNCHANGED |
| US-0096 / DEC-0082 | ✓ UNCHANGED |
| BUG-0007 | ✓ UNCHANGED |

Verification: `rg -c '^## US-0092 ' docs/engineering/architecture.md` returns 1; same for US-0095/US-0096. US-0056/US-0068/BUG-0007 referenced inline (no h1 anchors per architecture convention). US-0119 is additive-only: new `AUTONOMY_PRESET` + `AUTONOMY_STOP_POLICY` + 12 per-feature flags are expansion into scratchpad schema keys; stop-matrix is a new authority file; repair ledger is a new audit surface; breadcrumb is additive in state.md. None of the 6 compose targets' architectural surfaces are edited.

## Risk summary (R1..R8)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R1** Backward-compat regression (`AUTONOMY_PRESET=none`) | MEDIUM | `test_us0119_preset_none_is_noop` asserts byte-identical surface |
| **R2** Security gate bypass via matrix drift | MEDIUM | `test_us0119_security_hard_gates_never_auto_repaired` + validator `--self-test` |
| **R3** Repair ledger growth | LOW | Per-run cap=3 + gitignore + operator override |
| **R4** Operator confusion (softened gates) | MEDIUM | Breadcrumb + ledger audit + terminal stop + `AUTONOMY_PRESET=none` default |
| **R5** Preset-expansion vs explicit-key precedence | LOW–MEDIUM | LOCKED: explicit per-flag > preset > defaults |
| **R6** Compose-do-not-amend drift | LOW | `test_us0119_preset_expansion_uses_known_keys_only` |
| **R7** Matrix validator grep fragility | LOW | LOCKED: explicit YAML manifest (Q8) |
| **R8** Breadcrumb format granularity | LOW–MEDIUM | LOCKED: one-line per soft-stop (Q10) |

## Plan-verify note (ultra_lean)

Per US-0096 / DEC-0082 ultra_lean delivery mode, plan-verify is merged into QA within `build+verify` macro. No separate `plan-verify.json` at sprint-plan phase; QA phase produces it during `/qa`.

## Sprint seeds (T-anch + T-001..T-011 = 12 tasks)

Execution order (per architecture dependency chain):

```
T-anch (verify `## US-0119` anchor + compose) → T-001 (preset lib) → T-002 (scratchpad flags) →
T-003 (stop matrix + YAML + validator) → T-004 (consumer wiring) → T-005 (repair ledger) →
T-006 (breadcrumb) → T-007 (contract tests) → T-008 (README + parity) → T-009 (docs + runbook + commands) →
T-010 (installer manifest) → T-011 (regression tests)
```

Acyclic. Rationale: T-anch first (NO-OP verification on architecture.md). T-001→T-002→T-003 core foundation (lib + flags + matrix). T-004→T-005→T-006 consumer integration + audit surface. T-007 tests (depend on lib+matrix+ledger). T-008→T-009→T-010 docs/manifest (depend on lib being finalized). T-011 regression guard last.

## Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260705-us0119-sprintplan-techlead-20260705T225200Z-US-0119`
- `proof_hash=c49fcbf16a74ec86907dc9fd0cd11bc446b04feae462efac3e9a668e93b5b8a2`
- `proof_ttl=2026-07-05T23:52:00Z`
