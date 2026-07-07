# Sprint S0115

## Metadata

- **sprint_id**: S0115
- **story_refs**: US-0115
- **priority**: P3
- **effort**: 1 day
- **owner**: dev
- **goal**: Close the operator-documentation gap for the **integration & observability family features** (US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Add the `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` under `## Commands and workflow` (L350), as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940) and US-0114's `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella (L1225), with 7 nested `#### US-xxxx` operator subsections ordered US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102). Extend `### Full scratchpad reference (detailed)` (L1410) with a `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block — **net-new keys only** (US-0034 `CROSS_REPO_*` family, US-0096 `LEAN_MEMORY_*` family + `AUTO_DELIVERY_ROUTING`, US-0101 5 resolver keys, US-0102 `MODEL_SLUG_<PHASE_ID>`) + cross-link pointer to US-0114's block for `DELIVERY_MODE` overlap + grouped cross-link to main reference list for US-0086 `REMOTE_EXECUTION` family + reason-code-only entries for US-0084/US-0093. Preserve framework README byte-parity, run validators green, and keep regression tests green. Documentation-only; default-off posture preserved for optional features; US-0113's L1427 sovereign-loop keys block and US-0114's L1551 release & distribution keys block byte-stability preserved (3rd-story cumulative byte-stability surface — pure addition, cross-link pointers only).
- **status**: OPEN (per US-0045 — closure at /release)
- **created_at**: 2026-07-04T08:09:00Z
- **orchestrator_run_id**: auto-20260704-01
- **delivery_mode**: ultra_lean
- **macro_phase**: plan (sprint-plan — third canonical phase)
- **fresh_context_marker**: tl-US0115-sprint-plan-20260704T080900Z-fresh
- **resolved_phase_plan**: `["spec","plan","build+verify","ship"]` (ultra_lean macro — recomputed at story boundary per US-0044 / DEC-0022; `spec` already done via 5-story decomposition intake; `plan` = research + architecture + sprint-plan; `build+verify` = `/execute` + `/qa` (merges plan-verify + execute QA + verify-work); `ship` = `/release` + `/refresh-context`)

## Scope

- **US-0115**: Integration & observability operator documentation in framework README
- **Architecture anchor**: `docs/engineering/architecture.md#US-0115` (h1 anchor appended in architecture phase; approach_locked=A1)
- **Research anchor**: `docs/engineering/research.md` `R-0103` (delivered 2026-07-04T07:53:00Z — 6/6 discovery open questions closed)
- **Companion DEC**: none (US-0115 is documentation-only; no architectural, policy, or schema surface changed. Mirrors US-0113 / US-0114 sibling precedent. R-0103 § Decision-gate check confirmed no DEC candidate; grep `^## DEC-` in `docs/engineering/decisions.md` returned no US-0115 companion DEC.)

## Acceptance criteria (US-0115 — 8 ACs)

| AC | Description |
|----|-------------|
| AC-1 | `### Integration & observability umbrella section` under `## Commands and workflow` |
| AC-2 | Per-feature operator subsections for US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 |
| AC-3 | Full scratchpad reference extension (net-new keys only + cross-link pointers + reason-code-only entries) |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) |
| AC-6 | Audience + metadata hygiene |
| AC-7 | Runbook cross-links per feature (7 features → 7 anchors: US-0034 → L1167 h2; US-0084 → L1441/L1459 h3; US-0086 → L1398/L1471 h3; US-0093 → L1999 h3; US-0096 → L591 h3; US-0101 → L653 h2; US-0102 → L771 h2) |
| AC-8 | Regression tests (coverage parity contract tests green; no test weakenings) |

## AC → task surjective coverage (6 tasks, 8 ACs)

| AC | Task(s) | Architecture anchor |
|----|---------|---------------------|
| AC-1 Umbrella section | T-001 | § Sprint seeds T-001 |
| AC-2 Per-feature operator subsections | T-002 | § Sprint seeds T-002 |
| AC-3 Full scratchpad reference extension | T-003 | § Sprint seeds T-003 |
| AC-4 Coverage preserved | T-005 | § Sprint seeds T-005 |
| AC-5 Framework README parity | T-004 | § Sprint seeds T-004 |
| AC-6 Audience + metadata hygiene | T-005 | § Sprint seeds T-005 |
| AC-7 Runbook cross-links per feature | T-002 | § Sprint seeds T-002 |
| AC-8 Regression tests | T-006 | § Sprint seeds T-006 |

**Surjectivity check**: AC-1..AC-8 all covered (8/8). Multi-AC tasks: **T-002** (AC-2+AC-7), **T-005** (AC-4+AC-6). Every AC has ≥1 task. No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 6
- **SPRINT_MAX_TASKS**: 12 (from `.cursor/scratchpad.md`)
- **Within limit**: yes (6 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **SPRINT_AUTO_SPLIT_TRIGGERED**: false

## Tasks (T-001..T-006)

See `sprints/S0115/tasks.md` for atomic task definitions. Execution order (per architecture dependency chain):

```
T-001 (umbrella) → T-002 (7 subsections) → T-003 (scratchpad ref extension) →
T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests)
```

| ID | Title | ACs | Tranche | Risk |
|----|-------|-----|:--------|:-----|
| T-001 | Add `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` umbrella section under `## Commands and workflow` (after US-0114 umbrella close, before L1410; default-off framing for optional features (US-0034/US-0096/US-0101/US-0102) + always-on framing for publish/QA guards (US-0084/US-0086/US-0093); 7-step enable order US-0034 → US-0096 → US-0101 → US-0102 → US-0084 → US-0086 → US-0093; runbook pointer line) | AC-1 | A | LOW |
| T-002 | Add 7 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102; US-0034 cross-link only to existing L585 + runbook L1167; US-0096 net-new narrative per R-0103 CORRECTION + runbook L591; US-0101/US-0102 bidirectional "see US-0114 for installer-payload angle" pointers + runbook L653/L771; US-0084/US-0086/US-0093 reason codes + runbook cross-links L1441/L1459, L1398/L1471, L1999) | AC-2, AC-7 | A | LOW–MEDIUM |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block — net-new keys only (US-0034 `CROSS_REPO_*` family, US-0096 `LEAN_MEMORY_*` family + `AUTO_DELIVERY_ROUTING`, US-0101 5 resolver keys, US-0102 `MODEL_SLUG_<PHASE_ID>`) + cross-link pointer to US-0114's block for `DELIVERY_MODE` + grouped cross-link to main reference list for US-0086 `REMOTE_EXECUTION` family + reason-code-only entries for US-0084/US-0093; US-0113 L1427 + US-0114 L1551 byte-stability preserved | AC-3 | A | MEDIUM |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy); re-run parity + intake template parity | AC-5 | B | MEDIUM |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`); fix any drift; `coverage_missing=["US-0117"]` unchanged | AC-4, AC-6 | B | LOW (catalog) / MEDIUM (encoding prerequisite) |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed); no test weakenings; forbid edits to scratchpad canonical + test file | AC-8 | B | LOW–MEDIUM |

## Test markers (locked — no new tests proposed)

| Marker | File | ACs covered | Notes |
|--------|------|-------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | US-0115 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`; tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` must remain unchanged (DC-1 + DC-2 + DC-3 out-of-scope). Catalog block read-only. |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** AC-8 satisfied by existing tests remaining green (read-only gates, not edit targets). R-0103 confirmed no test weakenings.

## Files to touch

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `its_magic/README.md` | `template/its_magic/README.md` | T-001, T-002, T-003, T-004 | Byte-identical via T-004 one-way copy |

## Files NOT to touch (non-goals — hard)

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent; US-0115 only documents existing keys).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership).
- `docs/product/backlog.md` — status authority (closure only at /release per US-0045). **Note:** working-tree copy has 185 stray `0xa7` bytes (encoding regression flagged in R-0102 + R-0103 + architecture) — orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute.
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 7 runbook cross-link targets already exist (verified in R-0103).
- `docs/developer/README.md` — separate audience surface owned by US-0097 (project README parity) compose guard; AC-6 is a validator gate, not an edit mandate.
- `docs/engineering/architecture.md` (other than the architecture phase `## US-0115` anchor already appended) — missing `# US-0034` / `# US-0084` / `# US-0086` / `# US-0093` / `# US-0096` / `# US-0101` / `# US-0102` h1 anchors **deferred to US-0117** (DC-3, parallel to US-0113's DC-1 — 5 anchors; US-0114's DC-2 — 2 anchors; US-0117 inherits 14 anchors total as architecture.md triad hygiene closure).
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 + US-0062/DEC-0045 + US-0041/BUG-0003 compose guards).
- All `scripts/*` — validators are read-only gates, not edit targets.
- All integration & observability scripts and Python/PowerShell/Shell files — US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 features are **documented only**, not amended.
- `tests/scratchpad_example_parity_test.py` — read-only regression gate; if it fails, fix prose not test.
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1427) or US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1551)** in `its_magic/README.md` — byte-stability contract (both already released in S0113 / S0114). US-0115 adds cross-link pointers to these blocks from its own net-net block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks).

## Compose guards (23 — all UNCHANGED, cumulative)

US-0115 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched). 23 guards cumulative across all prior stories — US-0113 carried 18, US-0114 carried 18, US-0115 adds 5 family-internal guards to the documentation-only list for completeness: US-0034, US-0084, US-0086, US-0093, US-0096.

| Story | Compose rule (UNCHANGED) |
|-------|---------------------------|
| US-0091 | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners UNCHANGED — US-0115 appends narrative sections outside the catalog block. |
| US-0097 | Project README parity surface UNCHANGED — US-0115 touches framework README pair only, not project README. |
| US-0017 | Framework README parity contract UNCHANGED — US-0115 preserves byte-parity via T-004 lockstep. |
| US-0040 | Per-sprint release notes semantics UNCHANGED. |
| US-0100 | Semantic changelog UNCHANGED. |
| US-0101 | Catalog schema (DEC-0086) UNCHANGED — documented only (integration & observability angle owned by US-0115; release-workflow angle shipped in US-0114). |
| US-0102 | Role catalog precedence (DEC-0087) UNCHANGED — documented only (integration & observability angle owned by US-0115; release-workflow angle shipped in US-0114). |
| US-0103 | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| US-0104 | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| US-0105 | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| US-0107 | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| US-0108 | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| US-0109 | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| US-0110 | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| US-0111 | Release Trigger Adapters schema/semantics UNCHANGED — documented only. |
| US-0112 | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only. |
| US-0034 | Cross-repo compatibility observability schema/semantics UNCHANGED — documented only. |
| US-0084 | Codebase map freshness gate schema/semantics UNCHANGED — documented only. |
| US-0086 | Handoff hygiene validator schema/semantics UNCHANGED — documented only. |
| US-0093 | Scratchpad drift detector schema/semantics UNCHANGED — documented only. |
| US-0096 | Active context handoff schema/semantics UNCHANGED — documented only. |
| US-0041 | End-to-End Lifecycle QA schema/semantics UNCHANGED — documented only. |
| US-0062 | Installer-Owned `its_magic/` folder boundary (DEC-0045, amended by DEC-0083/US-0097) UNCHANGED — documented only. |

**23 guards UNCHANGED.**

## Non-goals

- No scratchpad canonical edits (`.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`).
- No installer changes (`installer.py/ps1/sh`).
- No runbook content additions (`docs/engineering/runbook.md` — AC-7 cross-links only; all 7 anchors pre-exist).
- No `docs/developer/README.md` edits (separate audience surface; US-0097 compose guard).
- No `docs/engineering/architecture.md` edits beyond the `## US-0115` anchor already appended in the architecture phase. 7 missing feature h1 anchors (`# US-0034`, `# US-0084`, `# US-0086`, `# US-0093`, `# US-0096`, `# US-0101`, `# US-0102`) **deferred to US-0117** as DC-3 (parallel to US-0113's DC-1 — 5 anchors; US-0114's DC-2 — 2 anchors; US-0117 inherits 14 anchors total).
- No new tests proposed (read-only regression gates).
- No `scripts/*` edits (validators are read-only gates).
- No integration & observability script amendments (US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102 features documented only).
- **DC-3 deferral noted** for traceability; orchestrator's segment-boundary advance hook will handle at segment close. DO NOT append to `handoffs/sovereign_deferrals.jsonl` in sprint-plan phase.

## DC-3 deferral note (deferred to US-0117)

- **DC-3**: 7 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0115 family — `# US-0034`, `# US-0084`, `# US-0086`, `# US-0093`, `# US-0096`, `# US-0101`, `# US-0102`. Not a US-0115 blocker (AC-7 satisfied via runbook cross-links — all 7 features have existing verified runbook anchors). US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) = 14 total as architecture.md triad hygiene closure.
- Anchor format to use at US-0117 time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112`, `# US-0113`, `# US-0114` format).

## Encoding hygiene prerequisite (carried from US-0114)

- Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102 / R-0103. Sprint-plan phase is read-only on backlog.md. Flag to orchestrator: restore backlog.md encoding hygiene before execute so AC-4 can be re-verified post-execute. NOT a US-0115 blocker.

## Plan-verify readiness (ultra_lean merge note)

In **ultra_lean** delivery mode, `/plan-verify` is **merged into the `build+verify` macro under QA** — the orchestrator routes; this sprint does **not** pre-create `sprints/S0115/plan-verify.json`. The sprint-plan output is plan-verify-ready (surjective AC coverage, atomic tasks, test markers aligned) so QA can verify in one spawn within `build+verify`.

`build+verify` macro canonical phases (per ultra_lean):
1. `/execute` (dev) — first canonical phase
2. `/qa` (qa) — merges plan-verify + execute QA + verify-work

## Decision gate check

**No DECISION_GATE raised.** Architecture phase resolved all 10 carry-overs within the `plan` macro (approach A1 locked; sprint seeds T-001..T-006; files to touch/not to touch locked; DC-3 deferred to US-0117; encoding hygiene prerequisite flagged). Sprint-plan revealed no question requiring operator input. Verdict: **PASS**.

## Sovereign memory note

Sprint-plan phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not re-assembled in sprint-plan (architecture phase already noted existing digest context sufficient per R-0103; US-0115 documentation-only). DC-3 deferral noted in non-goals for traceability.

Sovereign-loop pattern for curator retrospective at segment close: "integration & observability family operator documentation completes the US-0113/US-0114/US-0115 umbrella triad under `## Commands and workflow`; cross-story byte-stability contract now covers two prior released blocks (US-0113 L1427 + US-0114 L1551) — net-new-keys-only + cross-link-pointer shape is the established triad-closure pattern."

## Risks and mitigations (carried from architecture)

| ID | Risk | Severity | Sprint guard |
|----|------|----------|--------------|
| R1 | AC-3 byte-stability (3rd-story cumulative surface) — US-0115 is the third story to extend `### Full scratchpad reference`; cumulative surface now covers 2 prior released blocks (US-0113 L1427 + US-0114 L1551). Risk of accidentally editing a prior released block. | MEDIUM | T-003 mandates **net-new-keys-only + cross-link-pointer shape** (architecture lock); US-0113's `### Sovereign-loop era keys` block + US-0114's `### Release & distribution keys` block byte-stability preserved. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks). QA re-verifies. Mirrors S0114 retrospective pattern. |
| R2 | AC-5 parity lockstep — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | MEDIUM | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase runs `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). QA re-verifies. |
| R3 | AC-2 US-0096 net-new narrative — R-0103 CORRECTION: discovery handoff's claim of "L591 `### Delivery modes` in README" was wrong; L591 is a runbook line; no pre-existing US-0096 README section → `#### US-0096` is net-new narrative + runbook cross-link to L591 | LOW–MEDIUM | T-002 mandates US-0096 subsection as net-new narrative grounded in `.cursor/scratchpad.md` L173–186 (LEAN_MEMORY_* family + AUTO_DELIVERY_ROUTING + DELIVERY_MODE documentation default = `standard`) + runbook cross-link to L591 h3. QA re-verifies. |
| R4 | AC-2 US-0101/US-0102 angle overlap with US-0114 — US-0115 owns resolver mechanics + role catalog (DEC-0086/DEC-0087); US-0114 owns installer payload US-0112 presets | MEDIUM→LOW | T-002 mandates bidirectional "see US-0114 for installer-payload angle" pointers in US-0101/US-0102 subsections (mirror US-0113/US-0114 pointer convention). US-0114's US-0112 subsections already ship the "see US-0115" pointer per S0114 RELEASED state. QA re-verifies. |
| R5 | AC-3 `DELIVERY_MODE` overlap with US-0114 — US-0114's `### Release & distribution keys` block (L1551) owns the `DELIVERY_MODE` row | MEDIUM→LOW | T-003 mandates cross-link pointer to US-0114's block for `DELIVERY_MODE`; US-0115 does NOT re-document `DELIVERY_MODE` defaults. QA re-verifies. |
| R6 | AC-7 runbook cross-links — 7 anchors pre-exist and were verified in R-0103 | LOW | T-002 mandates cross-link to existing anchors only (no new runbook content). All 7 verified: US-0034 L1167 h2; US-0084 L1441/L1459 h3; US-0086 L1398/L1471 h3; US-0093 L1999 h3 (parent h2 = US-0065 runtime QA autopilot contract L1486); US-0096 L591 h3; US-0101 L653 h2; US-0102 L771 h2. QA re-verifies. |
| R7 | AC-8 regression tests — coverage parity contract tests weakened or failing | LOW–MEDIUM | US-0115 documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| R8 | AC-4 encoding hygiene prerequisite — working-tree backlog.md has 185 stray `0xa7` bytes per R-0102/R-0103; could block validator | MEDIUM | T-005 runs `validate_readme_feature_coverage.py --enforce`; orchestrator must restore working-tree `backlog.md` encoding hygiene before execute. Catalog block L63 + US-0113/US-0114 narrative blocks treated as read-only. NOT a US-0115 blocker (orchestrator-owned prerequisite). |
| R9 | AC-1 umbrella placement — must be after US-0114 umbrella close, before L1410 `### Full scratchpad reference` | LOW | T-001 mandates placement immediately after US-0114 umbrella close (before L1410). QA re-verifies via grep. |
| R10 | Decomposition drift — US-0101/US-0102 angle overlap with US-0114's US-0112 installer-payload angle | LOW | US-0115 subsections include explicit "see US-0114 for installer-payload angle" pointers (T-002). US-0115 = resolver mechanics + role catalog angle; US-0114 = installer payload + version sync angle. Bidirectional pointers already in US-0114's US-0112 subsections per S0114 RELEASED state. |

## Definition of done

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-006).
- T-001..T-006 executed in dependency order; all exit criteria met.
- `python -m pytest tests/scratchpad_example_parity_test.py -q` → 4 passed (no test weakenings).
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged.
- `cmd /c fc /b its_magic\README.md template\its_magic\README.md` → no differences.
- `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- `python scripts/validate_doc_profile.py` → PASS.
- `python scripts/check-user-visible-metadata.py` → PASS.
- `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks).
- `docs/product/backlog.md` `## US-0115` retains **OPEN** through execute / qa / verify-work; closure at `/release` (US-0045).

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro** — `/execute` (dev, first canonical phase of `build+verify`), which then chains to `/qa` (merges plan-verify + execute QA + verify-work). Plan-verify is NOT a standalone phase in ultra_lean.

**Handoff**: `handoffs/po_to_tl.md` (sprint-plan handoff block prepended per ultra_lean artifact convention — orchestrator reads the topmost block).

**Stop**: sprint-plan complete; do not spawn the next phase. Orchestrator Task-spawns dev for `/execute`.
