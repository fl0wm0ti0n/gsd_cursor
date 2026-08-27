# Architecture archive pack (2026-08-25)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 16
- First archived heading: `## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation`
- Last archived heading: `## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation`
- Verification tuple (mandatory):
  - archived_body_lines=200
  - preamble_lines=1
  - retained_body_lines=2918

---

## US-0119 — Autonomous-autonomy presets and configurable hard-stop relaxation

### Overview

US-0119 adds two orthogonal primitives on top of the existing sovereignty stack (US-0092 / US-0095 / US-0103 / US-0104 / US-0105 / US-0107):

1. **`AUTONOMY_PRESET={none|balanced|full}`** (default `none`) — an ergonomic scratchpad flag that deterministically expands into twelve per-feature autonomy flags (all of which already exist individually or are added here as net-new keys). Each preset bundles the combination an operator would otherwise configure manually. `AUTONOMY_PRESET=none` is byte-identical to pre-US-0119 behaviour.
2. **`AUTONOMY_STOP_POLICY={block|auto_repair_then_block|auto_repair_then_skip}`** (default `block`) — classifies every fail-closed reason code in `docs/engineering/autonomy-stop-matrix.md` as either `security_hard` (never auto-resolved under any preset / policy) or `autonomy_resolvable` (bounded auto-repair with an append-only ledger before escalation).

The two mechanisms compose: the preset controls *which* per-feature flags are flipped on; the stop policy controls *how* softened reason codes are handled at phase boundaries. Neither mechanism modifies the semantics of the underlying consumers — the preset is an expansion into existing keys, and the stop policy is a dispatch layer on top of existing reason-code emissions.

### Companion DEC

**`decisions/DEC-0119.md`** — authored in THIS architecture phase (status=Accepted). Locks:
- (a) `AUTONOMY_PRESET` 3-tier enumeration `none|balanced|full` (default `none`)
- (b) `AUTONOMY_STOP_POLICY` 3-value enumeration `block|auto_repair_then_block|auto_repair_then_skip` (default `block`)
- (c) Two-tier stop classification `security_hard|autonomy_resolvable`
- (d) `security_hard` rows never auto-repaired (bounded cap = 0 from matrix)
- (e) Nine `auto_repair_kind` taxonomy values from R-0107 Q2
- (f) Nine `autonomy_resolvable` reason codes per Q2 mapping
- (g) `autonomy_repair_kind` taxonomy + uniform cap = 3 per `(run, reason_code)` per Q3
- (h) `AUTONOMY_PRESET=none` is byte-identical to pre-US-0119
- (i) Twelve per-feature flags are additive consumers only (no existing consumer semantics change)
- (j) Precedence: explicit per-flag > preset expansion > scratchpad defaults

Mirrors DEC-0082 (delivery modes) / DEC-0078 (full-autonomy stop matrix) precedent.

### Approach A1 (LOCKED)

Single vertical-slice approach. No alternatives retained — 2-tier (`none|full` preset) rejected as too coarse; 4-tier (`none|low|medium|high`) rejected as over-engineered (no operator demand); 3-tier stop-class (`security_hard|autonomy_resolvable|soft_warn`) rejected as over-engineered (operators want binary never/yes).

**A1 components**:

| Component | Artifact | Responsibility |
|-----------|----------|----------------|
| `AUTONOMY_PRESET` flag | `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | Scratchpad key; net-new (13th key in autonomy block) |
| `AUTONOMY_STOP_POLICY` flag | `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | Scratchpad key; net-new (14th key in autonomy block) |
| Preset expansion lib | `scripts/autonomy_preset_lib.py` | `expand_autonomy_preset(preset, overrides) -> dict`; pure stdlib; `--self-test` + `--explain` |
| Stop-matrix manifest | `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md` | Operator-facing authority file; `security_hard` and `autonomy_resolvable` rows |
| Stop-matrix YAML | `scripts/data/autonomy_stop_matrix.yaml` | Machine-readable companion for validators |
| Matrix validator | `scripts/validate_autonomy_stop_matrix.py` | `--self-test`; checks orphan codes, `security_hard` → `auto_repair_kind=n/a`, `autonomy_resolvable` → finite `cap` |
| Twelve per-feature flags | `.cursor/scratchpad.md` | Net-new keys; expansion targets (existing consumers where applicable) |
| Bounded repair ledger | `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl` | Append-only; per-run cap from matrix; gitignored |
| Breadcrumb | `docs/engineering/state.md` phase boundary | `autonomy_relaxed: <reason_code> -> <auto_repair_kind>` one-line per soft-stop (Q10 LOCKED) |
| Consumer wiring | `/auto`, `/intake`, `/execute`, `/qa`, `/release` | Wire 12 flags into existing consumers (additive only) |
| Tests + parity | `tests/us0119_autonomy_preset_test.py` + `check_intake_template_parity.py --scope=us-0119` | 10 contract test markers + template parity enforcement |
| Documentation | `docs/engineering/architecture.md` (this section) + `docs/engineering/runbook.md` (h2) + `.cursor/commands/auto.md` (anchor) | Operator-facing docs + template parity |

**Execution order**: T-anch → T-001 → T-002 → T-003 → T-004 → T-005 → T-006 → T-007 → T-008 → T-009 → T-010 → T-011 (acyclic; T-001..T-003 first since they're the code/manifest/flags foundation).

### Files to touch

| File | Change |
|------|--------|
| `docs/engineering/architecture.md` | Add `## US-0119` section (THIS phase — T-anch NO-OP / verification; no write in execute) |
| `.cursor/scratchpad.md` | Add `AUTONOMY_PRESET`, `AUTONOMY_STOP_POLICY`, 12 per-feature flags |
| `template/.cursor/scratchpad.local.example.md` | Mirror scratchpad additions |
| `scripts/autonomy_preset_lib.py` | NEW — `expand_autonomy_preset(preset, overrides) -> dict` |
| `template/scripts/autonomy_preset_lib.py` | NEW — byte-identical copy |
| `scripts/data/autonomy_stop_matrix.yaml` | NEW — machine-readable stop classification |
| `scripts/validate_autonomy_stop_matrix.py` | NEW — matrix validator |
| `template/scripts/validate_autonomy_stop_matrix.py` | NEW — byte-identical copy |
| `docs/engineering/autonomy-stop-matrix.md` | NEW — operator-facing authority file |
| `template/docs/engineering/autonomy-stop-matrix.md` | NEW — byte-identical copy |
| `tests/us0119_autonomy_preset_test.py` | NEW — 10 contract test markers |
| `.cursor/commands/auto.md` | Add `## Autonomy presets (US-0119)` anchor |
| `template/.cursor/commands/auto.md` | Mirror |
| `docs/engineering/runbook.md` | Add `## Autonomy presets (US-0119)` h2 |
| `template/docs/engineering/runbook.md` | Mirror |
| `its_magic/README.md` | Add `### Autonomy preset keys (US-0119)` sub-block (7th sub-block; preserves cross-story byte-stability surface) |
| `template/its_magic/README.md` | Mirror (byte-stability preserved) |
| `docs/engineering/state.md` | `autonomy_relaxed` breadcrumb at phase boundaries; architecture checkpoint (THIS phase) |
| `decisions/DEC-0119.md` | NEW — companion DEC (THIS phase) |
| `handoffs/po_to_tl.md` | Prepend architecture handoff (THIS phase) |
| `installer-owned-paths.manifest` | Add rows for new scripts |

### Files NOT to touch (compose, do not amend)

| File | Reason |
|------|--------|
| `.cursor/commands/execute.md` | US-0092 outer-driver semantics UNCHANGED |
| `.cursor/commands/qa.md` | US-0095 native auto-chain UNCHANGED |
| `.cursor/commands/release.md` | US-0056 strict runtime proof semantics UNCHANGED (`RUNTIME_PROOF_KIND=lightweight` is only an opt-in lighter attestation — proof kind select, not semantics rewrite) |
| `.cursor/commands/intake.md` (evidence gate logic) | US-0068 intake evidence gate NEVER bypassed; `INTAKE_AUTONOMY_MODE=1` only auto-derives answers on known-stack repeat projects |
| `scripts/scratchpad_example_parity_test.py` | BUG-0013 regression tests UNCHANGED |
| `handoffs/intake_evidence/US-*.json` (prior entries) | BUG-0007 truthfulness UNCHANGED — schema extension optional, never retroactive |

### Sprint seeds (12 tasks within SPRINT_MAX_TASKS=12)

| Seed | Description | AC coverage |
|------|-------------|-------------|
| **T-anch** | Verify `## US-0119` h1 anchor present in `architecture.md` (added in THIS phase); verify compose-do-not-amend 6/6 compose targets; lock compose-guard UNCHANGED set (23+ guards) | AC-12, AC-11 |
| **T-001** | `scripts/autonomy_preset_lib.py` — `expand_autonomy_preset(preset, overrides) -> dict` + `--self-test` + `--explain`; pure stdlib; deterministic | AC-1, AC-2 |
| **T-002** | Add `AUTONOMY_PRESET` + `AUTONOMY_STOP_POLICY` + 12 per-feature flags in `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md`; merge-precedence note (explicit > preset > defaults) | AC-1, AC-3, AC-5 |
| **T-003** | `docs/engineering/autonomy-stop-matrix.md` + `template/docs/engineering/autonomy-stop-matrix.md` parity + `scripts/data/autonomy_stop_matrix.yaml` + `scripts/validate_autonomy_stop_matrix.py --self-test` | AC-4, AC-10 |
| **T-004** | Wire 12 per-feature flags into existing consumers — `/auto` auto-expansion + `/intake` INTAKE_AUTONOMY_MODE / INTAKE_MINIMAL_PACK / INTAKE_ASSUME_STACK_CONTEXT + `/execute` RUNTIME_PROOF_KIND + `/qa` GOAL_CONVERGENCE_INTERVAL + `/release` RELEASE_PUBLISH_AUTO_CONFIRM | AC-5 |
| **T-005** | Bounded auto-repair ledger `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl` + cap logic + `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop reason | AC-8 |
| **T-006** | `autonomy_relaxed` breadcrumb in `docs/engineering/state.md` at phase boundary (one-line per soft-stop per Q10) | AC-9 |
| **T-007** | Contract tests `tests/us0119_autonomy_preset_test.py` — 10 markers: preset-none-noop, balanced-expansion, full-expansion, explicit-flag-overrides-preset, expansion-uses-known-keys-only, matrix-validator-passes, security-hard-gates-never-auto-repaired, stop-policy-repair-dispatch, repair-ledger-cap-escalates, matrix-no-orphan-codes | AC-6, AC-7, AC-10 |
| **T-008** | README `### Autonomy preset keys (US-0119)` 7th sub-block + `check_intake_template_parity.py --scope=us-0119` + `AUTONOMY_PRESET_PAIRS` manifest | AC-10, AC-11 |
| **T-009** | Runbook cross-link `## Autonomy presets (US-0119)` h2 + `.cursor/commands/auto.md` `## Autonomy presets (US-0119)` anchor + template parity | AC-11 |
| **T-010** | `installer-owned-paths.manifest` rows for `scripts/autonomy_preset_lib.py` + `template/scripts/autonomy_preset_lib.py` + `scripts/validate_autonomy_stop_matrix.py` + `template/scripts/validate_autonomy_stop_matrix.py` | AC-10 |
| **T-011** | Regression tests `pytest tests/scratchpad_example_parity_test.py -v` 4 passed + forbid edits to scratchpad + test; `PARITY_OK <size> <size>` byte-stability proof | AC-6, AC-10 |

### Test markers (AC-10 → 10 markers)

| Marker | AC | Description |
|--------|----| -----|
| `test_us0119_preset_none_is_noop` | AC-6 | `AUTONOMY_PRESET=none` produces byte-identical pre-US-0119 behaviour |
| `test_us0119_preset_balanced_expansion` | AC-2 | balanced expands into documented 12 flags |
| `test_us0119_preset_full_expansion` | AC-2 | full expands into documented 12 flags (superset of balanced) |
| `test_us0119_explicit_flag_overrides_preset` | AC-2 | explicit per-flag > preset expansion |
| `test_us0119_preset_expansion_uses_known_keys_only` | AC-12 | expansion output contains only keys in pre-US-0119 scratchpad schema |
| `test_us0119_matrix_validator_passes` | AC-4 | `scripts/validate_autonomy_stop_matrix.py --self-test` exits 0 |
| `test_us0119_security_hard_gates_never_auto_repaired` | AC-7 | matrix `security_hard` rows all carry `auto_repair_kind=n/a` |
| `test_us0119_stop_policy_affects_repair_dispatch` | AC-3 | `auto_repair_then_block` vs `auto_repair_then_skip` dispatch correctly |
| `test_us0119_repair_ledger_cap_escalates` | AC-8 | cap exhaustion → `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop |
| `test_us0119_matrix_no_orphan_codes` | AC-4 | no orphan reason codes outside YAML manifest |

### Compose guards UNCHANGED (6/6 verified)

| Story | architecture.md anchor | Status |
|-------|------------------------|--------|
| US-0092 / DEC-0078 | `## US-0092` L1696 | ✓ exists — delivery confirmation gate UNCHANGED; AUTONOMY_PRESET only adds relaxation layer above |
| US-0095 | `## US-0095` L1700 | ✓ exists — native auto-chain UNCHANGED |
| US-0056 / DEC-0038 | (inline reference — no h1 anchor; strict runtime proof semantics referenced in architecture text; `RUNTIME_PROOF_KIND=lightweight` is opt-in lighter attestation only — proof kind select, not semantics rewrite) | ✓ UNCHANGED |
| US-0068 / DEC-0060 | (inline reference — no h1 anchor; intake evidence gate referenced in intake commands; `INTAKE_AUTONOMY_MODE=1` only auto-derives answers on known-stack repeat projects — evidence gate NEVER bypassed) | ✓ UNCHANGED |
| US-0096 / DEC-0082 | `## US-0096` L1684 | ✓ exists — delivery modes UNCHANGED; AUTONOMY_PRESET only softens governance gates within them |
| BUG-0007 | (no h1 anchor — truthfulness rule; `INTAKE_ASSUME_STACK_CONTEXT=1` auto-fills stack/runtime from backlog history with `assumption_confirmation_ref` contract preserved) | ✓ UNCHANGED |

### DC (deferred-candidate) check

`grep "^## US-0119" docs/engineering/architecture.md` → **no matches prior to THIS write**. The `## US-0119` h1 anchor is added in THIS `/architecture` phase per R-0105 Q-2 LOCKED pattern (architecture artifacts live in `architecture.md`; T-anch resolves anchor presence in `/execute`). No deferred-candidate carry-over.

### Compose-do-not-amend verification

All 6 compose targets (US-0092 / US-0095 / US-0056 / US-0068 / US-0096 / BUG-0007) verified present in `architecture.md` with existing anchors or inline references; US-0119 is additive-only. US-0119 inherits no DC candidates from prior stories. No new DC candidates are created by US-0119 (its own `## US-0119` anchor is resolved HERE). Deferral register remains clean — no carry-over to a successor story.

### Risks finalized (R1..R8)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **R1** Backward-compat regression (`AUTONOMY_PRESET=none` byte-identical to pre-US-0119) | MEDIUM | `test_us0119_preset_none_is_noop` asserts byte-identical surface; explicit-flag > preset > default precedence chain |
| **R2** Security gate bypass via matrix drift | MEDIUM | `test_us0119_security_hard_gates_never_auto_repaired` asserts matrix divergence; validator `--self-test` enforces `auto_repair_kind=n/a` on all `security_hard` rows |
| **R3** Repair ledger growth | LOW | Per-run cap = 3 (Q3 LOCKED) + gitignore at `handoffs/autonomy_repair_ledger/*.jsonl`; operator override via `AUTONOMY_REPAIR_CAP_OVERRIDE` |
| **R4** Operator confusion (softened gates) | MEDIUM | Breadcrumb `autonomy_relaxed:` in state.md + ledger audit surface + `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop reason; `AUTONOMY_PRESET=none` default preserves current behaviour |
| **R5** Preset-expansion vs explicit-key precedence | LOW–MEDIUM | LOCKED: explicit per-flag > preset > defaults (documented in scratchpad merge-precedence note per US-0078 model B) |
| **R6** Compose-do-not-amend drift (expansion uses unknown keys) | LOW | `test_us0119_preset_expansion_uses_known_keys_only` enforces only pre-US-0119 scratchpad schema keys |
| **R7** Matrix validator grep fragility | LOW | LOCKED: explicit YAML manifest (Q8 LOCKED from R-0107), not grep-only; `scripts/data/autonomy_stop_matrix.yaml` is single source of truth |
| **R8** Breadcrumb format granularity (one-line per soft-stop vs aggregated) | LOW–MEDIUM | LOCKED: one-line per soft-stop (Q10 LOCKED from R-0107); operator can count per-code softening events |

### Stop conditions

- `decision_gate=false` — no decision gate triggered; companion DEC-0119 authored Accepted in THIS phase
- `missing_acceptance_criteria=none` — all 12 ACs covered by sprint seeds
- `task_count=12` (T-anch + T-001..T-011) — within `SPRINT_MAX_TASKS=12`
- `compose_guards=6/6 UNCHANGED` — verified
- `dc_check=clean` — no deferred-candidate carry-over

### Consequences

- **Positive**: Operators gain a single `AUTONOMY_PRESET=balanced|full` switch that deterministically configures twelve autonomy flags; `AUTONOMY_STOP_POLICY` provides explicit control over how softened non-security stops are handled; audit trail via ledger + breadcrumb; backward-compatible default.
- **Negative**: More scratchpad surface area (14 new keys: `AUTONOMY_PRESET` + `AUTONOMY_STOP_POLICY` + 12 per-feature flags); new code surface (`autonomy_preset_lib.py` + `validate_autonomy_stop_matrix.py` + tests); new stop-matrix authority file; 7th cumulative byte-stability sub-block in README.
- **Neutral**: Implementation lives in `/execute`; this decision fixes the architecture contract only. `/sprint-plan` may merge or split the 12 task seeds within the 12-task budget.

### Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0119`, `sprint_id=(pending)`, `orchestrator_run_id=auto-20260705-us0119-intake`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082; research + architecture + sprint-plan merged)
- `fresh_context_marker=tl-US0119-architecture-20260705T224500Z-fresh`
- `timestamp=2026-07-05T22:45:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0119 block L4028-L4070 narrow-read — 12 ACs), docs/product/acceptance.md (US-0119 row L146 narrow-read — 12 ACs OPEN), handoffs/po_to_tl.md (US-0119 research handoff L1-L205 narrow-read), docs/engineering/state.md (research checkpoint L854-L890 narrow-read), docs/engineering/research.md (R-0107 entry L8907-L9001 full read), docs/engineering/architecture.md (## US-0118 section L1713-L1923 as template + compose-anchor verification), decisions/DEC-0118.md (full read as DEC-0119 template), .cursor/scratchpad.md (AUTONOMY_PRESET/AUTONOMY_STOP_POLICY/12 per-feature flag grep — zero matches confirming net-new), handoffs/resume_brief.md (top ~15 lines narrow-read)`
- Tech-lead subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to the narrow-read files listed above (US-0053 / US-0096 Tranche A). No MCP / browser / shell side-effects beyond narrow-read grep + read tool calls + python SHA-256 computation for the strict runtime proof + the artifact writes listed in this phase (architecture.md `## US-0119` section append, decisions/DEC-0119.md NEW, po_to_tl.md architecture handoff prepend, state.md architecture checkpoint append). No `.env` reads, no credentials access, no intake-evidence mutation.
- `assemble_sovereign_memory_digest(...)` NOT called (US-0119 code+docs; existing digest context sufficient per R-0107 — US-0113..US-0118 introspectives established reusable patterns; autonomy-preset angle adds distinct 7th-family dimension).
- No write to `mistakes.jsonl` in architecture phase (no fix_failed / revert_applied / plan_fidelity_violation / scope_creep event occurred).
- Prior phase strict proof consumed: `rp-auto-20260705-us0119-research-techlead-20260705T223000Z-US-0119` (from R-0107 entry, unchanged).
- Current architecture-phase strict proof recorded below.

### Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260705-us0119-architecture-techlead-20260705T224500Z-US-0119`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260705-us0119-intake","phase_id":"architecture","proof_issued_at":"2026-07-05T22:45:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260705-us0119-architecture-techlead-20260705T224500Z-US-0119","sprint_id":"(pending)","story_id":"US-0119"}`
- `proof_hash=71d0ac09ece22e540a8c8002555fe8f6720c6b5bcd77eb6b6eb09cc34360b1e9` (SHA-256 of the sorted-key JSON payload above)
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-05T23:45:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

### Decision gate

- `decision_gate=false` (no DECISION_GATE; companion DEC-0119 authored Accepted in THIS phase; approach A1 locked; sprint seeds T-anch + T-001..T-011 within SPRINT_MAX_TASKS=12; risks R1..R8 finalized; DC check clean; compose-do-not-amend verified 6/6)
- `stop_conditions_met=yes` (no missing references — all 6 compose targets verified; no decision gate triggered; AC baselines green)

### Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `next_scheduled_sprint_macro=plan`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006)`

---

