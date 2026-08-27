# Architecture archive pack (2026-08-26)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 16
- First archived heading: `# US-0120 — Dedicated `/closure` phase for exclusive Story Closure responsibility`
- Last archived heading: `# US-0120 — Dedicated `/closure` phase for exclusive Story Closure responsibility`
- Verification tuple (mandatory):
  - archived_body_lines=300
  - preamble_lines=1
  - retained_body_lines=2764

---

# US-0120 — Dedicated `/closure` phase for exclusive Story Closure responsibility

## Overview

**US-0120** extracts Story Closure (Status `OPEN`→`DONE` in `docs/product/backlog.md` + acceptance checkbox `[ ]`→`[x]` in `docs/product/acceptance.md` + `docs/engineering/state.md` closure checkpoint + `sprints/Sxxxx/closure-verification.md` artifact) from `/release` step 10–12 into a **dedicated `/closure` phase** with exclusive `qe` role ownership. The ultra-lean ship macro becomes `release → closure → refresh-context` (3 phases instead of 2). Orchestrator post-closure `rg` verification enforces materialization fidelity (fixes the US-0119 closure fidelity gap where the release subagent claimed closure but files remained `OPEN`/unchecked — same pattern as BUG-0006 execute cycle).

This is a **governance-only** change: no new code surfaces beyond a schema validator (`scripts/validate_closure_verification.py`) and contract tests (`tests/us0120_closure_phase_test.py`). The compose surface (US-0043, US-0045, US-0040, US-0048, US-0056, US-0096) remains UNCHANGED — `/closure` is the dedicated executor of the contracts those stories already define. Forward-compat only (R8 ACCEPTED): already-DONE stories are untouched; no retroactive `closure-verification.md` generation.

**Research anchor**: **R-0108** (research `docs/engineering/state.md` L1102–L1231 — resolved all 10 open questions Q1..Q10 LOCKED; 8 risks R1..R8 ACCEPTED; approach A1 locked; compose guards 6/6 UNCHANGED). **No companion DEC** (modifies DEC-0052 phase→role matrix + DEC-0082 ship macro directly — both are additive scoped edits, no new DEC needed per R-0108 ID resolution).

**Fresh context marker**: `tl-US0120-architecture-20260707T215000Z-fresh`
**Orchestrator run id**: `manual-20260707-us0120`
**Timestamp**: 2026-07-07T21:50:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

## Approach locked (A1 — from discovery)

**Approach A1** (locked, carried from discovery): Extract Story Closure from `/release` step 10–12 into dedicated `/closure` phase with exclusive `qe` role ownership. Ship macro becomes 3-phase: `release → closure → refresh-context`. Orchestrator post-closure `rg` verification enforces materialization fidelity. Forward-compat only (no retroactive closure for already-DONE stories).

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Dedicated `/closure` phase with exclusive `qe` ownership + orchestrator post-verification** | **Preferred** — resolves US-0119 fidelity gap; follows "one phase, one responsibility" principle; deterministic drain hook detection for in-flight stories. |
| A2 (rejected) | Keep closure inside `/release` but add orchestrator-side verification of step 10–12 execution. | **Rejected** — same fidelity pattern as US-0119 BUG-0006; release subagent overloaded with 19 steps; verification cannot fix non-materialization. |
| A3 (rejected) | Extract closure into `/qa` phase (`qa` already owns quality gate). | **Rejected** — conflates quality findings with status reconciliation (different US-0043 contract); `/qa` runs BEFORE `/release`, closure must run AFTER `/release`; violates phase ordering. |

## Phase definition

### /closure phase contract

| Attribute | Value |
|-----------|-------|
| **phase_id** | `closure` |
| **macro_phase** | `ship` (ultra_lean), canonical for all 3 delivery modes (standard, ultra_lean, mega_quick) |
| **role** | `qe` (default; `curator` fallback via `AUTO_ROLE_CLOSURE` scratchpad override — Q2 LOCKED) |
| **phase ordering** | AFTER `/release` PASS; BEFORE `/refresh-context` |
| **input prerequisites** | (a) `handoffs/release_queue.md` row `status=released` exists for target sprint, (b) `handoffs/releases/Sxxxx-release-notes.md` EXISTS with PASS verdict, (c) `sprints/Sxxxx/qa-findings.md` EXISTS. Fail-gated: `CLOSURE_RELEASE_EVIDENCE_MISSING`. |
| **outputs (all mandatory)** | (1) `docs/product/backlog.md` target story block: `- Status: OPEN` → `- Status: DONE` (canonical ownership per US-0045), (2) `docs/product/acceptance.md` target row: `- [ ] US-xxxx:` → `- [x] US-xxxx:`, (3) `docs/engineering/state.md` closure checkpoint append (phase_id=closure, role, story_id, sprint_id, fresh_context_marker, timestamp, verdict), (4) `sprints/Sxxxx/closure-verification.md` NEW artifact (schema below) |
| **orchestrator post-verification (D12)** | After `/closure` returns, orchestrator runs direct `rg` verification: (i) `rg "^- Status: DONE$" docs/product/backlog.md` constrained to target story block, (ii) `rg "^\- \[x\] US-xxxx:" docs/product/acceptance.md`. State.md: two-stage grep `rg "phase_id=closure" docs/engineering/state.md \| rg "story_id=US-xxxx"`. If any check FAIL → escalate `CLOSURE_VERIFICATION_FAILED`. |

### closure-verification.md schema (Q6/Q7 LOCKED)

Markdown format (not JSON — Q6 LOCKED; follows existing lifecycle artifact convention: qa-findings.md, release-findings.md, uat.md — all `.md`).

**REQUIRED fields** (validator `scripts/validate_closure_verification.py` checks these):

| Field | Format | Description |
|-------|--------|-------------|
| `story_id` | `US-xxxx` | Target story ID |
| `closure_date` | ISO-8601 UTC (e.g. `2026-07-07T22:00:00Z`) | When closure executed |
| `closure_role` | `qe \| curator` | Actual role that performed closure |
| `pre_closure_status` | `OPEN` | Pre-condition status (must be `OPEN`) |
| `post_closure_status` | `DONE` | Post-condition status (must be `DONE`) |
| `release_evidence_refs[]` | array of paths | Paths to release artifacts closure consumed (release_queue row ref, release-notes ref, qa-findings ref; optionally uat ref, release-findings ref) |
| `isolation_evidence{}` | object | `{phase_id: closure, role, fresh_context_marker, timestamp, evidence_ref: closure-verification.md path}` per US-0048 |
| `runtime_proof{}` | object | `{runtime_proof_id, proof_hash, proof_ttl_seconds: 3600}` per US-0056 / DEC-0038 |

**OPTIONAL fields** (extensible — Q7 LOCKED):

| Field | Format | Description |
|-------|--------|-------------|
| `normalization_notes` | free-text | Edge cases (legacy stories, in-flight reconciliation) |
| `backward_compat_note` | free-text | For in-flight story closure at US-0120 ship boundary |

Schema is **additive-extensible**: validator only checks required fields; future extensions do not break prior closure-verification.md files (R7 ACCEPTED).

## Artifacts

### New artifacts

| Artifact | Path | Responsibility |
|----------|------|----------------|
| `/closure` command (active) | `.cursor/commands/closure.md` | NEW — closure phase command for operator/subagent |
| `/closure` command (template) | `template/.cursor/commands/closure.md` | NEW — byte-identical mirror (T-002; `check_intake_template_parity.py --scope=closure-phase` enforces) |
| Closure verification artifact | `sprints/Sxxxx/closure-verification.md` | NEW — per-sprint closure execution record |
| Closure validator | `scripts/validate_closure_verification.py` | NEW — enforces required-field schema; pure stdlib |
| Contract tests | `tests/us0120_closure_phase_test.py` | NEW — 10 test markers (Q10 LOCKED) |
| This section | `docs/engineering/architecture.md` `# US-0120` | NEW (this phase) |
| Runbook section | `docs/engineering/runbook.md` `## Story closure (US-0120)` | NEW in `/execute` |

### Mutated artifacts (scoped edits only)

| Artifact | Mutation | Scope |
|----------|----------|-------|
| `.cursor/commands/release.md` (active + template) | Remove steps 10–12 (backlog reconciliation + derived views + normalization report); insert pointer at new step 10: "Backlog reconciliation is now handled by the dedicated `/closure` phase — see `.cursor/commands/closure.md`." Renumber old step 13 → new step 10, old step 14 → new step 11, etc. Sequential renumbering, no gaps. Active + template byte-identical. | T-005 |
| `decisions/DEC-0052.md` | ADD canonical phase→role matrix row: `closure \| qe \| AUTO_ROLE_CLOSURE scratchpad override to curator allowed`. ADD `AUTO_ROLE_CLOSURE` row to §2 override contract table. ADD `closure` row to §3 preflight capability gate. Existing 12 phase→role mappings UNTOUCHED. | T-003 |
| `decisions/DEC-0082.md` | Modify ship macro from `[release, refresh-context]` → `[release, closure, refresh-context]` (2→3 phases). Other macro definitions UNTOUCHED. | T-004 |
| `.cursor/commands/auto.md` + `template/.cursor/commands/auto.md` | Add closure to phase plan arrays in all delivery modes; after `/release` completes, orchestrator spawns closure subagent (fresh per BUG-0006). Add `AUTO_ROLE_CLOSURE` scratchpad key. | T-004 |
| `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` | Add `AUTO_ROLE_CLOSURE` key + closure phase pointer. | T-003/T-004 |
| `docs/engineering/state.md` | Append architecture checkpoint (this phase); runtime closure checkpoints appended per-sprint by `/closure`. | This phase |
| `handoffs/po_to_tl.md` | Prepend architecture handoff block (this phase). | This phase |
| `installer-owned-paths.manifest` | Add rows for new scripts + closure.md active + template. | T-009 |

### Files NOT to touch (compose guard UNCHANGED)

| File | Reason |
|------|--------|
| `docs/product/backlog.md` | US-0045 canonical status — `/closure` mutates ONLY at execution time. |
| `docs/product/acceptance.md` | US-0045 derived view — same. |
| Compose-guard story surfaces (US-0043, US-0045, US-0040, US-0048, US-0056, US-0096) | All 6 UNCHANGED — `/closure` EXECUTES their existing contracts. |

## Contracts

### DEC-0052 phase→role matrix extension (scoped — R3 ACCEPTED)

**ADD only** — existing 12 phase→role mappings UNTOUCHED.

| §1 Canonical phase→role matrix | New row |
|-------------------------------|---------|
| `closure` \| `qe` \| `AUTO_ROLE_CLOSURE` override to `curator` | |

| §2 Override contract table | New row |
|---------------------------|---------|
| `AUTO_ROLE_CLOSURE` \| values: `qe`, `curator` \| default: `qe` \| `curator must not write qa-owned surfaces` | |

| §3 Preflight capability gate | New row |
|------------------------------|---------|
| `closure` \| capability: `role:qe` or override \| fail-closed: `PHASE_CAPABILITY_MISSING` | |

### DEC-0082 ship macro extension (scoped — R4 ACCEPTED)

| Macro phase | Old ship | New ship |
|-------------|----------|----------|
| `ship` | `[release, refresh-context]` (2) | `[release, closure, refresh-context]` (3) |

### /auto orchestration wiring (AC-4)

1. All 3 delivery modes include `closure` after `release`.
2. After `/release` PASS → spawn closure subagent (fresh `qe` / `curator` fallback per BUG-0006).
3. After `/closure` PASS → spawn `/refresh-context` (unchanged).
4. `AUTO_ROLE_CLOSURE` scratchpad key (empty = `qe` fallback per Q2).

### Orchestrator post-closure verification protocol (D12 — R1 mitigation)

After `/closure` completes, orchestrator runs deterministic `rg` checks:

```
rg "^- Status: DONE$" docs/product/backlog.md  # constrained to target story block
rg "^\- \[x\] US-xxxx:" docs/product/acceptance.md  # exact match
rg "phase_id=closure" docs/engineering/state.md | rg "story_id=US-xxxx"  # two-stage
```

MISMATCH → fail-gate `CLOSURE_VERIFICATION_FAILED` (non-suppressible, R1 ACCEPTED).

### Drain hook for in-flight stories (Q4 — R2 mitigation)

1. Enumerate stories with `release_queue.md` row `status=released`.
2. For each, check `backlog.md` status + `acceptance.md` checkbox.
   - If `Status: OPEN` AND `- [ ] US-xxxx:` → closure SKIPPED.
   - **Post-US-0120**: spawn `/closure` with backfill mode.
   - **Pre-US-0120**: `CLOSURE_LEGACY_DRIFT` (manual reconciliation or automatic backfill; no retroactive closure-verification.md).
3. SKIP `Status: DONE` stories (R8 — no retroactive touch for US-0108/US-0119).

## Orchestrator wiring

### /auto phase plan update

Phase plan arrays in all 3 delivery modes:
- **standard**: `[..., release, closure, refresh-context]`
- **ultra_lean**: `[release, closure, refresh-context]`
- **mega_quick**: `[..., release, closure, refresh-context]`

### /closure subagent spawn contract

```
phase_id=closure
role=qe (or curator via AUTO_ROLE_CLOSURE override)
story_id=US-xxxx
sprint_id=Sxxxx
orchestrator_run_id=<current>
fresh_context_marker=tl-US0120-closure-<timestamp>-fresh (per BUG-0006)
```

Fresh subagent per BUG-0006 / US-0048 isolation. Produces own isolation evidence + runtime proof per US-0048 / US-0056.

### Release subagent post-US-0120

`.cursor/commands/release.md` steps 10–12 REMOVED. New step 10 = pointer to `/closure`. Release subagent focuses on release artifacts only. Active + template byte-identical (R5/R6 ACCEPTED).

## Compose guards (6/6 UNCHANGED)

| Compose target | Verification | Result |
|---|---|---|
| US-0043 | inline ref (20 matches) — US-0120 EXECUTES US-0043 | ✅ read-only |
| US-0045 | inline ref (20 matches) — US-0120 FOLLOWS US-0045 | ✅ read-only |
| US-0040 | inline ref (7 matches) — US-0120 operates AFTER US-0040 | ✅ read-only |
| US-0048 | inline ref (3 matches) — US-0120 produces own isolation evidence | ✅ read-only |
| US-0056 | inline ref (3 matches) — US-0120 produces own runtime proof | ✅ read-only |
| US-0096 | `## US-0096` at L1684 | ✅ read-only (ship macro extended, semantics unchanged) |

Contract test `test_us0120_compose_guards_unchanged` enforces at execute boundary.

## Risks mitigated

All 8 risks from R-0108 ACCEPTED:

| Risk | Severity | Mitigation |
|------|----------|------------|
| R1: Subagent fidelity gap | MEDIUM | D12 orchestrator post-closure `rg` → `CLOSURE_VERIFICATION_FAILED` |
| R2: In-flight story backward compat | LOW | Q4 drain hook 3-signal detection |
| R3: DEC-0052 scope creep | LOW–MEDIUM | T-003 scoped ADDITIVE edit |
| R4: DEC-0082 scope creep | LOW–MEDIUM | T-004 scoped ship-only edit |
| R5: release.md renumbering | LOW | T-005 deterministic renumber |
| R6: closure.md template parity drift | LOW | T-001+T-002 byte-identical + parity checker extension |
| R7: closure-verification.md schema rigidity | LOW | Extensible schema, required-field-only validator |
| R8: Already-released S0119 backward compat | LOW | Q4 SKIPs DONE stories |

## Sprint seeds preview (10 tasks within SPRINT_MAX_TASKS=12)

| Seed | Description | AC |
|------|-------------|-----|
| **T-anch** | Verify `# US-0120` H1 anchor present; compose guards 6/6; DEC-0052/DEC-0082 scoped-edit contract. | AC-12, AC-11 |
| **T-001** | NEW `.cursor/commands/closure.md` (active). | AC-1 |
| **T-002** | NEW `template/.cursor/commands/closure.md` (byte-identical). | AC-1 |
| **T-003** | DEC-0052 scoped edit + `AUTO_ROLE_CLOSURE` scratchpad key. | AC-2 |
| **T-004** | DEC-0082 ship + auto.md phase plan arrays + closure spawn. | AC-3, AC-4 |
| **T-005** | release.md step 10–12 removal + renumbering (active + template). | AC-5 |
| **T-006** | NEW `scripts/validate_closure_verification.py`. | AC-6 |
| **T-007** | Closure isolation evidence + runtime proof contract in closure.md. | AC-7, AC-8 |
| **T-008** | NEW `tests/us0120_closure_phase_test.py` (10 markers). | AC-9 |
| **T-009** | Drain hook + installer manifest rows. | AC-10 |
| **T-010** | Runbook `## Story closure (US-0120)` h2 + architecture.md (this). | AC-11 |

**Total: 10 tasks (T-anch + T-001..T-010) — within `SPRINT_MAX_TASKS=12`.**

## Test markers (10 — Q10 LOCKED)

| Marker | AC |
|--------|----|
| `test_us0120_closure_command_file_exists_active` | AC-1 |
| `test_us0120_closure_command_file_exists_template` | AC-1 |
| `test_us0120_closure_command_file_parity` | AC-1 |
| `test_us0120_dec_0052_phase_role_matrix_includes_closure` | AC-2 |
| `test_us0120_dec_0082_ship_macro_includes_closure` | AC-3 |
| `test_us0120_auto_phase_plan_includes_closure` | AC-4 |
| `test_us0120_release_md_steps_10_12_removed` | AC-5 |
| `test_us0120_closure_verification_schema_defined` | AC-6 |
| `test_us0120_compose_guards_unchanged` | AC-12 |
| `test_us0120_backward_compat_drain_hook` | AC-10 |

Surjective AC coverage: markers 1-3→AC-1, 4→AC-2, 5→AC-3, 6→AC-4, 7→AC-5, 8→AC-6, 9→AC-12, 10→AC-10; AC-7/AC-8/AC-9/AC-11 covered indirectly by markers 1+8/4/6.

## DC check

`dc_check=clean`. No `# US-0120` or `## US-0120` existed prior to THIS write. H1 anchor added per DEC-0076 / BUG-0010 heading policy. Deferral register clean.

## Stop conditions

- `decision_gate=false`
- `missing_acceptance_criteria=none` (12/12 ACs covered)
- `compose_guards=6/6 UNCHANGED`
- `dc_check=clean`
- 10/10 Q LOCKED, 8/8 R ACCEPTED, A1 locked
- Triad baseline `baseline_h2_count=41` preserved (H1 used)
- Codebase map gate: delegated to `/sprint-plan` handoff

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called. No write to `mistakes.jsonl`.

## Consequences

- **Positive**: Closure gets exclusive phase ownership (resolves US-0119 fidelity gap); lifecycle follows "one phase, one responsibility".
- **Negative**: New command file (active + template); new validator; new tests; one extra spawn cycle in ship macro.
- **Neutral**: DEC-0052 + DEC-0082 additive scoped edits; compose UNCHANGED; forward-compat only.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0120`, `sprint_id=S0120`
- `orchestrator_run_id=manual-20260707-us0120`
- `delivery_mode=ultra_lean`, `macro_phase=plan`
- `fresh_context_marker=tl-US0120-architecture-20260707T215000Z-fresh`
- `timestamp=2026-07-07T21:50:00Z` (UTC)
- `evidence_ref=docs/product/backlog.md (## US-0120 L4072-L4119), docs/product/acceptance.md (US-0120 L147), handoffs/po_to_tl.md (top research + discovery handoffs), docs/engineering/state.md (research checkpoint L1102-L1231 full read), docs/engineering/architecture.md (## US-0096 L1684 + inline refs for US-0043/US-0045/US-0040/US-0048/US-0056 + DC clean + H2 baseline=41)`
- Fresh tech-lead subagent per BUG-0006 / US-0048; no prior chat history.
- Prior proof consumed: `rp-manual-20260707-us0120-research-tl-20260707T214500Z-US-0120`
- Triad baseline `baseline_h2_count=41` preserved via H1 anchor.

## Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-manual-20260707-us0120-architecture-tl-20260707T215000Z-US-0120`
- Canonical payload: `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"manual-20260707-us0120","phase_id":"architecture","proof_issued_at":"2026-07-07T21:50:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-manual-20260707-us0120-architecture-tl-20260707T215000Z-US-0120","sprint_id":"S0120","story_id":"US-0120"}`
- `proof_hash=6293266bfcdf3e6e668cf28a34d831e55cc05a17e5dea1fc8ee94b70ca67b99f`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-07-07T22:50:00Z`

## Decision gate

- `decision_gate=false` (no companion DEC per R-0108 — scoped edits to DEC-0052 + DEC-0082 directly)
- `stop_conditions_met=yes`

## Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (tech-lead, third phase of `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent per BUG-0006`

---


