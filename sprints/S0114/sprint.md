# Sprint S0114

## Metadata

- **sprint_id**: S0114
- **story_refs**: US-0114
- **priority**: P3
- **effort**: 1 day
- **owner**: dev
- **goal**: Close the operator-documentation gap for the **release & distribution family features** (US-0041, US-0062, US-0111, US-0112) in the framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`). Add the `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section under `## Commands and workflow` (L350), as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940), with 4 nested `#### US-xxxx` operator subsections ordered US-id-ascending (US-0041 → US-0062 → US-0111 → US-0112). Extend `### Full scratchpad reference (detailed)` (L1225) with a `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block — **net-new keys only** (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links (US-0054 publish controls, `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES`) + cross-link pointers to US-0113's `### Sovereign-loop era keys` block for overlapping US-0111/US-0112 keys. Preserve framework README byte-parity, run validators green, and keep regression tests green. Documentation-only; default-off posture preserved; zero new scratchpad keys; US-0113 sovereign-loop keys block byte-stability preserved.
- **status**: OPEN (per US-0045 — closure at /release)
- **created_at**: 2026-07-04T05:00:00Z
- **orchestrator_run_id**: auto-20260704-01
- **delivery_mode**: ultra_lean
- **macro_phase**: plan (sprint-plan — third canonical phase)
- **fresh_context_marker**: tl-US0114-sprint-plan-20260704T050000Z-fresh

## Scope

- **US-0114**: Release & distribution operator documentation in framework README
- **Architecture anchor**: `docs/engineering/architecture.md#US-0114` (h1 anchor appended at L914 in architecture phase)
- **Research anchor**: `docs/engineering/research.md` `R-0102` (delivered 2026-07-04T02:45:40Z — 4/4 discovery open questions closed)
- **Companion DEC**: none (US-0114 is documentation-only; no architectural, policy, or schema surface changed. Mirrors US-0113 sibling precedent. Next available would be DEC-0113 — not used since no decision surface to record. Precedent: US-0113 / BUG-0013 / BUG-0014 all shipped with `companion_dec=none`.)

## Acceptance criteria (US-0114 — 8 ACs)

| AC | Description |
|----|-------------|
| AC-1 | `### Release & distribution umbrella section` under `## Commands and workflow` |
| AC-2 | Per-feature operator subsections for US-0111/US-0112/US-0041/US-0062 (release-workflow angle) |
| AC-3 | Full scratchpad reference extension (net-new keys only + cross-link pointers) |
| AC-4 | Coverage preserved (`validate_readme_feature_coverage.py --enforce` green) |
| AC-5 | Framework README parity (`its_magic/README.md` ↔ `template/its_magic/README.md` byte-identical) |
| AC-6 | Audience + metadata hygiene |
| AC-7 | Runbook cross-links per feature (US-0062 → L171 with note) |
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

See `sprints/S0114/tasks.md` for atomic task definitions. Execution order (per architecture dependency chain):

```
T-001 (umbrella) → T-002 (4 subsections) → T-003 (scratchpad ref extension) →
T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests)
```

| ID | Title | ACs | Tranche | Risk |
|----|-------|-----|:--------|:-----|
| T-001 | Add `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section under `## Commands and workflow` (after US-0113 block; default-off posture + 4-step recommended enable order + runbook pointer + zero-overhead-when-off contract) | AC-1 | A | LOW |
| T-002 | Add 4 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-0041 → US-0062 → US-0111 → US-0112; release-workflow angle for US-0111/US-0112 with bidirectional "see US-0113" pointers; runbook cross-links — US-0062 → L171 with explanatory note, US-0041 → L2522) | AC-2, AC-7 | A | LOW |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block — net-new keys only + grouped cross-links + cross-link pointers to US-0113's block for overlap keys; US-0113 byte-stability preserved | AC-3 | A | LOW |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy); re-run `fc /b` + `check_intake_template_parity.py` | AC-5 | B | MEDIUM |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`); fix any drift; `coverage_missing=["US-0117"]` unchanged | AC-4, AC-6 | B | LOW |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed); no test weakenings | AC-8 | B | LOW–MEDIUM |

## Test markers (locked — no new tests proposed)

| Marker | File | ACs covered | Notes |
|--------|------|-------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | US-0114 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`; tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` must remain unchanged (DC-1 + DC-2 out-of-scope). |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** AC-8 satisfied by existing tests remaining green (read-only gates, not edit targets). R-0102 confirmed no test weakenings.

## Files to touch

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `its_magic/README.md` | `template/its_magic/README.md` | T-001, T-002, T-003, T-004 | Byte-identical via T-004 one-way copy |

## Files NOT to touch (non-goals — hard)

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent; US-0114 only documents existing keys).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership).
- `docs/product/backlog.md` — status authority (closure only at /release per US-0045). **Note:** working-tree copy has 185 stray `0xa7` bytes (encoding regression flagged in R-0102 + architecture) — orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute.
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 4 runbook cross-link targets already exist.
- `docs/developer/README.md` — separate audience surface owned by US-0097 (project README parity) compose guard; AC-6 is a validator gate, not an edit mandate.
- `docs/engineering/architecture.md` (other than the architecture phase `# US-0114` append already done at L914) — missing `# US-0041` / `# US-0062` h1 anchors **deferred to US-0117** (DC-2, parallel to US-0113's DC-1 — 5 anchors; US-0117 inherits 7 anchors total as architecture.md triad hygiene closure).
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 + US-0062/DEC-0045 + US-0041/BUG-0003 compose guards).
- All `scripts/*` — validators are read-only gates, not edit targets.
- All release & distribution scripts and Python/PowerShell/Shell files — US-0111/US-0112/US-0041/US-0062 features are **documented only**, not amended.
- `tests/scratchpad_example_parity_test.py` — read-only regression gate; if it fails, fix prose not test.

## Compose guards (18 — all UNCHANGED)

US-0114 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched).

| Story | Compose rule (UNCHANGED) |
|-------|---------------------------|
| US-0091 | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners UNCHANGED — US-0114 appends narrative sections outside the catalog block. |
| US-0097 | Project README parity surface UNCHANGED — US-0114 touches framework README pair only, not project README. (US-0062 cross-links here.) |
| US-0017 | Framework README parity contract UNCHANGED — US-0114 preserves byte-parity via T-004 lockstep. |
| US-0040 | Per-sprint release notes semantics UNCHANGED. |
| US-0100 | Semantic changelog UNCHANGED. |
| US-0101 | Catalog schema (DEC-0086) UNCHANGED. |
| US-0102 | Role catalog precedence (DEC-0087) UNCHANGED. |
| US-0103 | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| US-0104 | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| US-0105 | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| US-0107 | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| US-0108 | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| US-0109 | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| US-0110 | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| US-0111 | Release Trigger Adapters schema/semantics UNCHANGED — documented only (release-workflow angle owned by US-0114; sovereign-loop angle shipped in US-0113). |
| US-0112 | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only (release-workflow angle owned by US-0114; sovereign-loop angle shipped in US-0113). |
| US-0041 | End-to-End Lifecycle QA schema/semantics UNCHANGED — documented only (release-workflow angle). |
| US-0062 | Installer-Owned `its_magic/` folder boundary (DEC-0045, amended by DEC-0083/US-0097) UNCHANGED — documented only. |

**18 guards UNCHANGED.**

## Non-goals

- No scratchpad canonical edits (`.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`).
- No installer changes (`installer.py/ps1/sh`).
- No runbook content additions (`docs/engineering/runbook.md` — AC-7 cross-links only).
- No `docs/developer/README.md` edits (separate audience surface; US-0097 compose guard).
- No `docs/engineering/architecture.md` edits beyond the `# US-0114` anchor already appended in the architecture phase (L914). 2 missing feature h1 anchors (`# US-0041`, `# US-0062`) **deferred to US-0117** as DC-2 (parallel to US-0113's DC-1 — 5 anchors; US-0117 inherits 7 anchors total).
- No new tests proposed (read-only regression gates).
- No `scripts/*` edits (validators are read-only gates).
- No release & distribution script amendments (US-0041/US-0062/US-0111/US-0112 features documented only).
- **DC-2 deferral noted** for traceability; orchestrator's segment-boundary advance hook will handle at segment close. DO NOT append to `handoffs/sovereign_deferrals.jsonl` in sprint-plan phase.

## Plan-verify readiness (ultra_lean merge note)

In **ultra_lean** delivery mode, `/plan-verify` is **merged into the `build+verify` macro under QA** — the orchestrator routes; this sprint does **not** pre-create `sprints/S0114/plan-verify.json`. The sprint-plan output is plan-verify-ready (surjective AC coverage, atomic tasks, test markers aligned) so QA can verify in one spawn within `build+verify`.

`build+verify` macro canonical phases (per ultra_lean):
1. `/execute` (dev) — first canonical phase
2. `/qa` (qa) — merges plan-verify + execute QA + verify-work

## Decision gate check

**No DECISION_GATE raised.** Architecture phase resolved both carry-overs within the `plan` macro (defer DC-2 h1 anchors to US-0117; lock scratchpad reference extension = net-new keys + cross-link pointers). Sprint-plan revealed no question requiring operator input. Verdict: **PASS**.

## Sovereign memory note

Sprint-plan phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not re-assembled in sprint-plan (architecture phase already noted existing digest context sufficient per R-0102; US-0114 documentation-only). DC-2 deferral noted in non-goals for traceability.

## Risks and mitigations (carried from architecture)

| ID | Risk | Severity | Sprint guard |
|----|------|----------|--------------|
| R1 | AC-3 overlap divergence — US-0111/US-0112 overlap keys re-documented in US-0114's reference sub-block, drifting from US-0113's block | MEDIUM→LOW | T-003 mandates **net-new keys + cross-link pointers only** (carry-over (b) locked); US-0113's `### Sovereign-loop era keys` block byte-stability preserved. QA re-verifies. |
| R2 | AC-5 parity lockstep — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | MEDIUM | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase runs `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). QA re-verifies. |
| R3 | AC-7 US-0062 anchor — US-0062 has no dedicated runbook `## US-0062` h2 anchor | MEDIUM→LOW | T-002 mandates cross-link to `## Project README coverage validation (US-0097 / DEC-0083)` (L171) with explanatory note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)". QA re-verifies. |
| R4 | AC-8 regression tests — coverage parity contract tests weakened or failing | LOW–MEDIUM | US-0114 documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py`. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| R5 | AC-4 coverage drift / encoding — catalog block reflowed OR working-tree backlog.md encoding regression blocks validator | LOW (catalog) / MEDIUM (encoding) | T-005 runs `validate_readme_feature_coverage.py --enforce`; `coverage_missing=["US-0117"]` must remain unchanged. Catalog block L63 + L1235–L1243 treated as read-only. **Encoding hygiene:** orchestrator must restore working-tree `backlog.md` encoding hygiene (185 stray `0xa7` bytes) before execute. |
| R6 | AC-6 metadata leakage — internal IDs (DEC-xxxx/R-xxxx/reason-codes) leak into user-visible prose | LOW | T-005 runs `validate_doc_profile.py` + `check-user-visible-metadata.py`; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. US-0062's explanatory note is the only place a DEC id appears in prose — kept inside a parenthetical cross-link, not a user-visible sentence. |
| R7 | Decomposition drift (US-0113 angle overlap) — US-0111/US-0112 subsections overlap confusingly with US-0113's subsections | LOW | US-0114 subsections include explicit "see US-0113 for sovereign-loop angle" pointers (T-002). US-0113 = sovereign-loop angle (shipped S0113); US-0114 = release-workflow angle. Bidirectional pointers already in US-0113's subsections (per R-0101). |

## Definition of done

- All 8 acceptance criteria covered surjectively (AC-1..AC-8 → T-001..T-006).
- T-001..T-006 executed in dependency order; all exit criteria met.
- `python -m pytest tests/scratchpad_example_parity_test.py -q` → 4 passed (no test weakenings).
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged.
- `cmd /c fc /b its_magic\README.md template\its_magic\README.md` → no differences.
- `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- `python scripts/validate_doc_profile.py` → PASS.
- `python scripts/check-user-visible-metadata.py` → PASS.
- `docs/product/backlog.md` `## US-0114` retains **OPEN** through execute / qa / verify-work; closure at `/release` (US-0045).

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro** — `/execute` (dev, first canonical phase of `build+verify`), which then chains to `/qa` (merges plan-verify + execute QA + verify-work). Plan-verify is NOT a standalone phase in ultra_lean.

**Handoff**: `handoffs/po_to_tl.md` (sprint-plan handoff block prepended per ultra_lean artifact convention — orchestrator reads the topmost block).

**Stop**: sprint-plan complete; do not spawn the next phase. Orchestrator Task-spawns dev for `/execute`.
