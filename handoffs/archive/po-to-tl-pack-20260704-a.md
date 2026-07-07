# po_to_tl archive pack (2026-07-04-a)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Rollover pass: 1 (US-0114 refresh-context terminal)
- Archived handoffs (oldest first, contiguous suffix): 4 (US-0113 lifecycle — sprint-plan, architecture, research, discovery) + intake handoffs (US-0113..US-0117 broadening + US-0113 sovereign-only prior)
- Retained handoffs in hot file: 4 (US-0114 lifecycle — sprint-plan, architecture, research, discovery)
- First archived heading: `# Sprint-plan handoff — US-0113 / auto-20260704-01`
- Last archived heading: `## Intake handoff — US-0113 sovereign-only (prior)`
- Verification tuple (mandatory):
  - archived_body_lines=398
  - preamble_lines=0

---

# Sprint-plan handoff — US-0113 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: sprint-plan (complete)
**Role**: tech-lead
**Story**: US-0113 — Sovereign-loop operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (sprint-plan — third canonical phase)
**fresh_context_marker**: tl-US0113-sprint-plan-20260704T014000Z-fresh
**timestamp**: 2026-07-04T01:40:00Z

## Sprint

- **Sprint ID**: S0113
- **Sprint directory**: `sprints/S0113/`
- **Artifacts**: `sprints/S0113/sprint.md`, `sprints/S0113/tasks.md`, `sprints/S0113/summary.md`

## Task count

- **6 tasks** (T-001..T-006) ≤ `SPRINT_MAX_TASKS=12`
- **SPRINT_AUTO_SPLIT triggered**: false (6 ≤ 12)
- **Execution order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006

## AC coverage

- **Surjective**: 8/8 ACs covered by 6 tasks
- **AC → task map**: AC-1 → T-001; AC-2 → T-002; AC-3 → T-003; AC-4 → T-005; AC-5 → T-004; AC-6 → T-005; AC-7 → T-002; AC-8 → T-006
- **Multi-AC tasks**: T-002 (AC-2+AC-7), T-005 (AC-4+AC-6)

## Test markers locked

- `tests/scratchpad_example_parity_test.py` (4 markers — AC-5 indirect, AC-8)
- `scripts/validate_readme_feature_coverage.py --enforce` (AC-4)
- `scripts/check_intake_template_parity.py` (AC-5)
- `scripts/validate_doc_profile.py` (AC-6)
- `scripts/check-user-visible-metadata.py` (AC-6)
- **No new tests proposed** (AC-8 satisfied by existing tests remaining green; read-only gates)

## Compose guards (16 — all UNCHANGED)

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112. US-0113 lives entirely outside the compose surface (documentation-only).

## Architecture anchor

- `docs/engineering/architecture.md#US-0113` (approach_locked=A1; companion_dec=none; stop_conditions_met=yes)
- Research anchor: R-0101 (3/3 open questions closed)

## Non-goals (hard)

- No scratchpad canonical edits (`.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`)
- No installer changes (`installer.py/ps1/sh`)
- No runbook content additions (`docs/engineering/runbook.md` — AC-7 cross-links only; all 9 anchors exist)
- No `docs/developer/README.md` edits (US-0097 compose guard)
- No `docs/engineering/architecture.md` edits beyond the US-0113 anchor already appended (5 missing feature h1 anchors deferred to US-0117 — DC-1)
- No new tests proposed; no `scripts/*` edits (read-only gates)
- No sovereign-loop script amendments (US-0103..US-0112 documented only)
- No `tests/scratchpad_example_parity_test.py` edits (fix prose not test)

## Decision gate

**No DECISION_GATE raised.** Architecture resolved both carry-overs within `plan` macro. Sprint-plan revealed no question requiring operator input. Verdict: **PASS**.

## Plan-verify readiness (ultra_lean merge note)

In **ultra_lean**, `/plan-verify` is **merged into the `build+verify` macro under QA**. This sprint does **not** pre-create `sprints/S0113/plan-verify.json` (orchestrator routes). Sprint-plan output is plan-verify-ready (surjective AC coverage, atomic tasks, test markers aligned) so QA can verify in one spawn within `build+verify`.

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro**:
- `/execute` (dev, first canonical phase of `build+verify`)
- → `/qa` (qa, merges plan-verify + execute QA + verify-work)

Orchestrator will Task-spawn dev for `/execute`. Handoff via artifacts only.

## Sovereign memory note

Sprint-plan phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not re-assembled in sprint-plan (architecture phase already noted existing context sufficient per R-0101; US-0113 documentation-only). DC-1 deferral noted in sprint non-goals for traceability.

---

# Architecture handoff — US-0113 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: architecture (complete)
**Role**: tech-lead
**Story**: US-0113 — Sovereign-loop operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (architecture — second canonical phase)
**fresh_context_marker**: tl-US0113-architecture-20260703T232718Z-fresh
**timestamp**: 2026-07-03T23:27:18Z

## Architecture anchor

- **`docs/engineering/architecture.md#US-0113`** — appended. Architecture decision for US-0113 (documentation-only; sovereign-loop operator docs in framework README).

## Approach locked

**A1** — Single umbrella `### Sovereign-loop era (US-0103–US-0112)` section with 9 nested `#### US-xxxx` subsections (h4 under h3 umbrella), placed under `## Commands and workflow` (L350), before `### Full scratchpad reference (detailed)` (L940). A2 (flat 9 subsections without umbrella) rejected — loses era grouping; weakens AC-1.

## Companion DEC

**companion_dec=none** (confirmed, not overriding R-0101). US-0113 is documentation-only; no architectural, policy, or schema surface changed. Next available DEC id would be DEC-0113 (highest existing is DEC-0112); reserving it would be wasteful since there is no decision surface to record. Precedent: BUG-0013 / BUG-0014 both shipped with companion_dec=none.

## Sprint seeds preview (T-001..T-006)

6 task seeds (≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered):

| ID | Title | AC |
|----|-------|----|
| **T-001** | Add `### Sovereign-loop era (US-0103–US-0112)` umbrella section under `## Commands and workflow` (default-off posture + 9-step recommended enable order + runbook pointer + zero-overhead-when-off contract) | AC-1 |
| **T-002** | Add 9 per-feature `#### US-xxxx` operator subsections nested under umbrella (US-id-ascending; sovereign-loop angle for US-0111/US-0112 with "see US-0114" pointers; runbook cross-links existing anchors only) | AC-2, AC-7 |
| **T-003** | Extend `### Full scratchpad reference (detailed)` with sovereign-loop keys grouped by feature, ordering mirrors `.cursor/scratchpad.md` L388–539 canonical (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112) | AC-3 |
| **T-004** | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy); re-run `fc /b` + `check_intake_template_parity.py` | AC-5 |
| **T-005** | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`) and fix any drift | AC-4, AC-6 |
| **T-006** | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q`); confirm green; no test weakenings | AC-8 |

**AC → task surjective map**: AC-1 → T-001; AC-2 → T-002; AC-3 → T-003; AC-4 → T-005; AC-5 → T-004; AC-6 → T-005; AC-7 → T-002; AC-8 → T-006. All 8 ACs covered surjectively.

## Carry-overs from research — resolution

- **(a) 5 missing `# US-xxxx` h1 anchors in `architecture.md` (US-0103/0104/0105/0107/0110)** — **DEFERRED to US-0117** (phase & role governance family). Justification: AC-7 only requires runbook cross-links (which exist for all 9); `architecture.md` h1 anchors are an internal engineering-docs surface, not an operator-facing README surface; mixing the two would blur US-0113's vertical-slice boundary. **Deferral candidate for orchestrator's segment-boundary advance hook** (DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase). When US-0117 enters `plan` macro, its discovery should narrow-read `architecture.md#US-0113` and add the 5 missing h1 anchors as a task seed (anchor format: `# US-xxxx — <feature title>`).
- **(b) Scratchpad reference extension ordering** — **Locked: mirror `.cursor/scratchpad.md` L388–539 canonical ordering** (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending. Justification: canonical scratchpad is source of truth; mirroring preserves parity for operator cross-reference. Narrative subsections (AC-2) use US-id-ascending for discovery; reference extension (AC-3) uses canonical mirror for lookup — distinct rationales, intentional.

## Risks finalized

- **AC-5 (MEDIUM)** parity lockstep — mitigation: T-004 one-way copy + `fc /b` + `check_intake_template_parity.py`; QA re-verifies.
- **AC-8 (LOW–MEDIUM)** regression tests — mitigation: forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py` in execute; if test fails, fix prose not test.
- AC-1/2/3/4/6/7: LOW. Decomposition drift (US-0114 angle overlap): LOW (mitigated by "see US-0114" pointers in T-002).

## Decision gate

**No DECISION_GATE raised.** Architecture revealed no question requiring operator input. Both carry-overs resolved by tech-lead within `plan` macro.

## Compose guards (16 — all UNCHANGED)

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112. US-0113 lives entirely outside the compose surface (documentation-only).

## Stop conditions

**stop_conditions_met=yes**: no major tradeoff requires DEC (confirmed); no feasibility unknown (R-0101 closed all); no data migration risk (documentation-only).

## Next phase

`/sprint-plan` → tech-lead, `plan` macro-phase (third canonical phase). Fresh subagent spawn. The sprint-plan tech-lead should narrow-read `docs/engineering/architecture.md#US-0113` (sprint seeds T-001..T-006), `handoffs/po_to_tl.md` (this architecture handoff block), and `docs/engineering/state.md` (architecture checkpoint), then produce `sprints/S0113/sprint.md` + `sprints/S0113/tasks.md` + `handoffs/tl_to_dev.md`.

---

# Research handoff — US-0113 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: research (complete)
**Role**: tech-lead
**Story**: US-0113 — Sovereign-loop operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (research — first canonical phase)
**fresh_context_marker**: tl-US0113-research-20260704T004730Z-fresh
**timestamp**: 2026-07-04T00:47:30Z

## Research anchor

- **R-0101** — `docs/engineering/research.md` (appended). US-0113 operator documentation research: 9-feature operator guide shape, scratchpad reference extension map, AC-4/5/6/8 baseline preservation, risk deepening, decision gate check. Verdict: PASS.

## 3 open questions from discovery — resolution status

All 3 RESOLVED (no operator input required, no DECISION_GATE raised):

1. **US-0112 scratchpad surface** — RESOLVED. US-0112 has NO dedicated sovereign-loop scratchpad block (`.cursor/scratchpad.md` L388–539 contains blocks for US-0103/0110/0104/0105/0107/0106/0108/0109/0111 but not US-0112). US-0112 operator subsection references existing delivery/catalog keys (`DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP`, `MODEL_TIER` from scratchpad L181–199 region) plus the installer manifest surface. No new scratchpad block required; no sovereign-loop-adjacent block introduced.
2. **US-0111/US-0112 narrative angle vs US-0114** — RESOLVED. Backlog authority confirms both US-0113 (`related_us` includes US-0111, US-0112) and US-0114 (`related_us` includes US-0111, US-0112) own angle-distinct narratives for these two features. US-0113 covers the **sovereign-loop aspect**: US-0111 = release-trigger adapter as a sovereign-loop notification/ledger surface; US-0112 = preset delivery as a sovereign-loop bootstrap aid (presets tune keys the loop reads at phase boundaries). US-0114 will cover the **release-workflow aspect** (trigger-source dispatch + changelog derivation mechanics; installer payload + version sync). Same US-id, two angles — backlog authority permits this per discovery handoff L99. US-0113 subsections include explicit "see US-0114 for release-workflow operator docs on this feature" pointers.
3. **Architecture h1 anchors for US-0103/0104/0105/0107/0110** — RESOLVED (carried to `/architecture` as a noted gap, NOT a US-0113 blocker). `docs/engineering/architecture.md` h1 inventory confirms only 4 of 9 features have dedicated h1 anchors — `# US-0108` (L120), `# US-0109` (L220), `# US-0111` (L335), `# US-0112` (L454). The other five (US-0103, US-0104, US-0105, US-0107, US-0110) are referenced from US-0106/US-0108/US-0109 compose sections and runbook `# US-xxxx` cross-links exist, but the architecture.md h1 anchors themselves are absent. **US-0113 can proceed without those h1 anchors** because AC-7 only requires runbook cross-links (which exist for all 9 features — confirmed). The `/architecture` phase tech-lead (next canonical phase, fresh spawn) should close the gap by adding 5 minimal `# US-xxxx` h1 sections summarizing the locked normative content already captured in R-0089 (US-0103), R-0092 (US-0104), R-0093 (US-0105), R-0094 (US-0107), R-0091 (US-0110) + corresponding DEC-0103/0104/0105/0107/0110, OR explicitly document the architectural decision that those 5 features have their normative locks recorded in research/DEC entries and runbook-only anchors (no standalone architecture.md h1). Recommendation: add 5 minimal h1 sections to keep the architecture triad (architecture.md / runbook.md / reason_codes.md) consistent.

## Per-feature research sub-findings (9 sovereign-loop features)

R-0101 contains a full per-feature sub-finding for each of: US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111 (sovereign-loop angle), US-0112 (sovereign-loop angle). Each sub-finding captures:
- What the feature does (1–3 sentences, grounded in backlog row + scratchpad keys).
- Which scratchpad keys control it (master enable flag + related keys, with defaults).
- Zero-overhead-when-off wording contract (mirroring `.cursor/scratchpad.md` own `# Default-off` pattern).
- Recommended operator-guide narrative shape (what the `#### US-xxxx` subsection in `its_magic/README.md` should contain).
- Runbook cross-link target (existing anchor only — AC-7).

## Umbrella section shape (AC-1)

R-0101 researches the recommended shape of the `### Sovereign-loop era (US-0103–US-0112) umbrella section` (AC-1) under `## Commands and workflow` (L350), before `### Full scratchpad reference (detailed)` (L940). Shape: default-off posture callout, recommended enable order (9-step dependency chain: AI_DECISION_LEDGER → SOVEREIGN_MEMORY → CROSS_MODEL_REVIEW → SOVEREIGN_GOAL_MODE=goal_convergence → AUTO_SOVEREIGN → SOVEREIGN_PARALLEL_DEV → AUTO_SOVEREIGN_SELF_HEALING_DEPLOY → RELEASE_TRIGGER_SOURCE → US-0112 presets), runbook pointer, and a zero-overhead-when-off contract paragraph.

## Scratchpad reference extension map (AC-3)

R-0101 researches which sovereign-loop keys (from `.cursor/scratchpad.md` L388–539) need to be added to the `### Full scratchpad reference (detailed)` section of `its_magic/README.md` (L940). 9 sub-sub-sections grouped by feature, mirroring the canonical scratchpad block ordering (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112). US-0112 sub-sub-section notes that US-0112 has no dedicated sovereign-loop scratchpad block and points to the existing delivery/catalog keys.

## AC baselines (preserved — read-only)

- **AC-4 (coverage)**: `validate_readme_feature_coverage.py --repo . --report` reports `coverage_total=105`, `coverage_present=105`, `coverage_missing=1` (US-0117 — pre-existing, out of US-0113 scope). US-0113's 9 in-scope features are all currently in `coverage_present`. US-0113 preservation contract: after execute, `coverage_missing` must remain `["US-0117"]` (unchanged). Catalog block L63 + L1235–L1243 treated as read-only.
- **AC-5 (parity)**: `cmd /c fc /b its_magic\README.md template\its_magic\README.md` → `PARITY_OK`. `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`. Lockstep mechanism: edit `its_magic/README.md` then one-way copy to `template/its_magic/README.md` then re-run `fc /b` + `check_intake_template_parity.py`.
- **AC-6 (audience + metadata)**: `validate_doc_profile.py` + `check-user-visible-metadata.py` are the gates (not run in research — no README edits performed). Convention: reuse existing `(US-xxxx)` parenthetical-tag pattern; avoid `DEC-xxxx`/`R-xxxx`/reason-code families in narrative sentences.
- **AC-8 (regression tests)**: `python -m pytest tests/scratchpad_example_parity_test.py -q` → 4 passed. US-0113 is documentation-only; scratchpad parity tests remain green by construction (US-0113 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`).

## Recommended architecture approach (high-level — NOT locked)

The `/architecture` phase (next canonical phase, fresh tech-lead spawn) should lock:

1. **Umbrella section placement** — under `## Commands and workflow` (L350), before `### Full scratchpad reference (detailed)` (L940). Insert as a new `###` section with the 9 `####` subsections ordered US-id-ascending (US-0103 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0110 → US-0111 → US-0112).
2. **Scratchpad reference extension ordering** — recommendation: mirror `.cursor/scratchpad.md` L388–539 canonical ordering (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending, to preserve source-of-truth parity. Architecture phase decides.
3. **Recommended enable order** — research recommends a 9-step dependency chain (see umbrella section shape above). Architecture phase validates the dependency ordering (e.g., is `SOVEREIGN_MEMORY=1` strictly required before `CROSS_MODEL_REVIEW=1`, or can they be enabled in parallel?) and locks it as a normative L-lock if needed.
4. **Architecture.md h1 gap (carry-over)** — close the 5 missing `# US-0103`/`# US-0104`/`# US-0105`/`# US-0107`/`# US-0110` h1 anchors. NOT a US-0113 blocker (AC-7 only requires runbook cross-links, which exist for all 9).
5. **No DEC required** — US-0113 is documentation-only; no architectural, policy, or schema surface is being changed. Existing compose guards (US-0091 predicate matrix, US-0097 project README, US-0017 framework README parity, US-0103–US-0112 sovereign features) remain UNCHANGED.

## Deferral candidates (sovereign-loop mode — noted, not written)

- **DC-1** (US-0106 gap) confirmed belongs to US-0117 family, not US-0113. US-0106 (Sovereign Role-Behavior Manifest) is a phase & role governance feature — its operator docs belong in US-0117. No write to `handoffs/sovereign_deferrals.jsonl` in research phase. Noting for the orchestrator's segment-boundary advance hook.

## Risks (deepened — see R-0101 risk summary)

- AC-1/2/3/4/6/7: LOW.
- AC-5 (framework README parity): MEDIUM — lockstep via one-way copy `its_magic/README.md` → `template/its_magic/README.md`.
- AC-8 (regression tests): LOW–MEDIUM — US-0113 is documentation-only; forbid edits to `.cursor/scratchpad.md` and `template/.cursor/scratchpad.local.example.md` in execute-phase task list.
- Decomposition drift (US-0114 angle overlap): LOW — US-0113 subsections include explicit "see US-0114" pointers.

## Decision gate

**No DECISION_GATE raised.** All 3 discovery open questions resolved without operator input. No new DEC required at research phase.

## Next phase

`/architecture` → tech-lead, `plan` macro-phase (second canonical phase). Fresh subagent spawn. The architecture-phase tech-lead should narrow-read R-0101 (especially the "Recommended architecture approach" and "carry_to_architecture" sections), then lock the README edit plan (umbrella + 9 subsections + scratchpad reference extension + runbook cross-links) and hand off to `/sprint-plan`.

---

# Discovery handoff — US-0113 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: discovery (complete)
**Role**: po
**Story**: US-0113 — Sovereign-loop operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**fresh_context_marker**: po-US0113-discovery-20260704T003300Z-fresh

## Confirmed in-scope feature set (9 US ids)

Per `docs/product/backlog.md` US-0113 `related_us` field and `handoffs/po_to_tl.md` intake handoff (5-story decomposition, sovereign-loop family slice):

- **US-0103** — AI Decision Ledger + Plan Fidelity
- **US-0104** — Cross-Model Adversarial Critic
- **US-0105** — Sovereign Memory
- **US-0107** — Sovereign Loop Mode (AUTO_SOVEREIGN)
- **US-0108** — Parallel Instance Arbitrage for dev phase
- **US-0109** — Self-Healing Deploy Loop
- **US-0110** — Goal-Based Convergence Loops
- **US-0111** — Release-Trigger-Driven Version Changelog Derivation
- **US-0112** — Ship Model-Catalog Example Presets on Install/upgrade

**Decomposition confirmation**: US-0113 = sovereign-loop family slice only. US-0114..US-0117 work is **out of scope** for this story (drain mutex — one story at a time per `handoffs/resume_brief.md` priority order). US-0091 (catalog anchor), US-0097 (project README parity), US-0017 (framework README parity) are **compose-touch references**, not in-scope feature work — they are AC-4/AC-5/AC-6 contract surfaces, not narrative subsection targets.

## README operator-doc structure map (`its_magic/README.md`)

Current README structure (1614 lines, TOC verified lines 1–80 + grep anchors):

- L22 `## Features (what its-magic can do)` — tiered feature hierarchy (already covers sovereign-loop features at catalog-one-liner depth)
- L63 `<!-- readme-feature-coverage-catalog -->` — US-0091 catalog anchor (preserved, AC-4)
- L65 `### Feature coverage catalog (US-0091)` — existing one-liners for US-0103..US-0112 (verified L1235–L1243)
- L90 `## Setup`
- L350 `## Commands and workflow`
- L940 `### Full scratchpad reference (detailed)` — AC-3 extension target
- L1363 `## Other useful capabilities`

**Where the umbrella section lands (AC-1)**: New `### Sovereign-loop era (US-0103–US-0112) umbrella section` is inserted **under `## Commands and workflow`** (after L350 heading area, before `### Full scratchpad reference` at L940). Per AC-1 wording the umbrella must live under `## Commands and workflow`, not under `## Features` (Features already has catalog one-liners; umbrella is narrative operator guide).

**Per-feature operator subsection sequence (AC-2)**: 9 subsections under the umbrella, ordered by US-id (deterministic, matches backlog `related_us` ordering and scratchpad key block ordering L388–L539):

1. `#### US-0103 — AI Decision Ledger + Plan Fidelity`
2. `#### US-0104 — Cross-Model Adversarial Critic`
3. `#### US-0105 — Sovereign Memory`
4. `#### US-0107 — Sovereign Loop Mode (AUTO_SOVEREIGN)`
5. `#### US-0108 — Parallel Instance Arbitrage for dev phase`
6. `#### US-0109 — Self-Healing Deploy Loop`
7. `#### US-0110 — Goal-Based Convergence Loops`
8. `#### US-0111 — Release-Trigger-Driven Version Changelog Derivation`
9. `#### US-0112 — Ship Model-Catalog Example Presets on Install/upgrade`

Note: US-0106 (Sovereign Role-Behavior Manifest) is intentionally **excluded** from US-0113's in-scope set per backlog `related_us` field — it belongs to a different family and is not in the US-0103–US-0112 sovereign-loop era set per the backlog authority. (US-0106 has its own scratchpad block at L462–L476 and a catalog one-liner at L1238; if the operator wants US-0106 included, that is a backlog amendment, not a discovery decision.)

## Scratchpad reference extension map (AC-3)

`### Full scratchpad reference (detailed)` at L940 is the extension target. The sovereign-loop keys to add are sourced from `.cursor/scratchpad.md` lines 388–539 (verified read). Extension must use **default-off / zero-overhead-when-off** wording per AC-3 and intake handoff AC-3 contract.

Key groups to add (one subsection per feature, matching the AC-2 subsection order):

| Feature | Scratchpad keys (from `.cursor/scratchpad.md`) | Source lines |
|---|---|---|
| US-0103 | `AI_DECISION_LEDGER`, `AUTO_PLAN_FIDELITY` | L388–396 |
| US-0110 | `SOVEREIGN_GOAL_MODE`, `SOVEREIGN_GOAL`, `SOVEREIGN_GOAL_TOP_N`, `SOVEREIGN_GOAL_MAX_CHARS`, `SOVEREIGN_GOAL_TIMEOUT_MAX` | L398–411 |
| US-0104 | `CROSS_MODEL_REVIEW`, `CROSS_MODEL_ANTISLOP_THRESHOLD`, `CROSS_MODEL_REWORK_MAX` | L413–422 |
| US-0105 | `SOVEREIGN_MEMORY`, `SOVEREIGN_MEMORY_TOP_N`, `SOVEREIGN_MEMORY_TOP_K`, `SOVEREIGN_MEMORY_MAX_CHARS`, `SOVEREIGN_MEMORY_JSONL_MAX_LINES` | L424–437 |
| US-0107 | `AUTO_SOVEREIGN`, `AUTO_SOVEREIGN_DEFERRAL_MAX`, `AUTO_SOVEREIGN_DRAIN_GENERATE_MAX`, `AUTO_SOVEREIGN_DEFERRAL_POLICY`, `SOVEREIGN_NOTIFY_TARGET`, `SOVEREIGN_NOTIFY_NTFY_TOPIC`, `SOVEREIGN_NOTIFY_NTFY_BASE`, `SOVEREIGN_NOTIFY_HOOK_URL`, `SOVEREIGN_NOTIFY_EMAIL_TO` | L439–461 |
| US-0108 | `SOVEREIGN_PARALLEL_DEV`, `AUTO_SOVEREIGN_PARALLEL_N`, `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL`, `AUTO_SOVEREIGN_MERGE_RESOLVE`, `AUTO_SOVEREIGN_WORKTREE_KEEP`, `AUTO_SOVEREIGN_PARALLEL_QA`, `AUTO_SOVEREIGN_PARALLEL_QA_ARBITER`, `AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD`, `AUTO_SOVEREIGN_PARALLEL_REWORK_MAX`, `AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC`, `AUTO_SOVEREIGN_PARALLEL_MODEL_<idx>`, `AUTO_SOVEREIGN_PARALLEL_LENS_<idx>` | L478–505 |
| US-0109 | `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY`, `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX`, `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC`, `AUTO_SOVEREIGN_DEPLOY_PROBE_KIND`, `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH`, `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` | L507–527 |
| US-0111 | `RELEASE_TRIGGER_SOURCE`, `RELEASE_TRIGGER_TIMEOUT_SEC`, `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` | L529–539 |
| US-0112 | (no sovereign-loop scratchpad keys; catalog/preset delivery — keys are in L181–199 region: `DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP` etc. — verify in `plan` macro) | L181–199 |

**Open question for tech-lead (US-0112 scratchpad surface)**: US-0112 is the only feature in the in-scope set without a dedicated sovereign-loop scratchpad block. The `plan` macro-phase (tech-lead) should confirm whether US-0112's operator subsection references existing delivery/catalog keys or gets a new sovereign-loop-adjacent key block. **Discovery does not decide this** — flagging as a `plan`-phase clarification, not a decision gate (no operator input required; tech-lead can resolve from architecture.md `# US-0112`).

## Runbook cross-link targets (AC-7 — existing anchors only)

Existing runbook section anchors in `docs/engineering/runbook.md` for cross-linking (no new runbook content in US-0113 — AC-7 forbids runbook content duplication):

| Feature | Runbook anchor (existing) | Line |
|---|---|---|
| US-0103 | `## AI Decision Ledger (US-0103 / DEC-0103)` | L2668 |
| US-0104 | `### Cross-Model Adversarial Critic (US-0104)` | L2855 |
| US-0105 | `### Sovereign Memory (US-0105)` | L2930 |
| US-0107 | `### Sovereign Loop Mode (US-0107)` (under `## Sovereign Loop Mode (US-0107 / DEC-0107)` region) | L3009 |
| US-0108 | `### Parallel Instance Arbitrage (US-0108)` | L3181 |
| US-0109 | `## Self-Healing Deploy Loop (US-0109 / DEC-0109)` | L3302 |
| US-0110 | `## Goal-Based Convergence (US-0110 / DEC-0110)` | L2764 |
| US-0111 | `## Release Trigger Adapters (US-0111 / DEC-0111)` | L3378 |
| US-0112 | `## Model-catalog example preset delivery (US-0112 / DEC-0112)` | L941 |

**All 9 features have existing runbook anchors** — AC-7 is satisfiable purely with cross-links. No new runbook content needed. (Architecture anchors also exist at `docs/engineering/architecture.md` `# US-0108` L120, `# US-0109` L220, `# US-0111` L335, `# US-0112` L454; US-0103/0104/0105/0107/0110 are referenced from US-0106/US-0108/US-0109 compose sections — `plan` macro will confirm exact `# US-0103`/`# US-0104`/`# US-0105`/`# US-0107`/`# US-0110` h1 anchors if not already present.)

## Risks

- **AC-4 (coverage preserved)**: LOW. `validate_readme_feature_coverage.py --enforce` is currently green (117/117 per state.md L770). US-0113 only **adds** narrative sections; it does not remove or rewrite catalog one-liners. The `<!-- readme-feature-coverage-catalog -->` anchor at L63 and existing one-liners L1235–L1243 must remain byte-stable. Risk: an edit accidentally reflows the catalog block. Mitigation: execute-phase must treat the catalog block as read-only and append new narrative sections outside it.
- **AC-5 (framework README parity)**: MEDIUM. `its_magic/README.md` ↔ `template/its_magic/README.md` must stay byte-identical. Both files are currently 1614 lines. Any edit to one must be mirrored to the other in the same commit. Risk: edit only one surface. Mitigation: execute-phase must edit both files in lockstep and re-run `check_intake_template_parity.py` before QA.
- **AC-6 (audience + metadata hygiene)**: LOW. `validate_doc_profile.py` and `check-user-visible-metadata.py` must pass. New narrative sections must use operator-audience wording (not internal-only IDs in user-visible channels). Risk: leaking internal IDs (US-xxxx, DEC-xxxx, R-xxxx) into user-visible prose. Mitigation: follow existing README convention — US-IDs are allowed in parenthetical catalog tags `(US-0103)` but not in narrative sentences.
- **AC-8 (regression tests)**: LOW–MEDIUM. Coverage parity contract tests must remain green; no test weakenings. Risk: a test is "relaxed" to accommodate a new section. Mitigation: execute-phase must not modify `tests/scratchpad_example_parity_test.py` or coverage contract tests; if a test fails, the prose is wrong, not the test.
- **Decomposition drift risk**: LOW. US-0114..US-0117 are queued and could tempt scope creep into US-0113 (e.g., US-0111/US-0112 are also in US-0114's family per intake handoff L15). Mitigation: drain mutex — US-0113 ships first, US-0114 picks up US-0111/US-0112 **release-and-distribution** narrative (different angle from US-0113's sovereign-loop angle). The same US-id can appear in two stories' narrative subsections **only if** the subsection angle differs (sovereign-loop vs release-workflow). **Flag for tech-lead**: confirm with operator whether US-0111/US-0112 subsections in US-0113 and US-0114 will overlap confusingly. Default recommendation: US-0113 covers the **sovereign-loop aspect** of US-0111/US-0112; US-0114 covers the **release/distribution aspect**. This is a `plan`-macro clarification, not a decision gate.

## Open questions / decision gate recommendations

**No DECISION_GATE raised.** All identified questions are resolvable by the tech-lead in the `plan` macro-phase without operator input:

1. **US-0112 scratchpad key surface** — does US-0112's operator subsection reference existing delivery keys or get a new sovereign-loop-adjacent block? (Resolvable from `architecture.md # US-0112`.)
2. **US-0111/US-0112 narrative angle vs US-0114** — confirm sovereign-loop angle in US-0113 vs release-workflow angle in US-0114. (Resolvable by reading both backlog blocks.)
3. **Architecture h1 anchors for US-0103/0104/0105/0107/0110** — confirm `# US-0103` etc. exist as h1 in `architecture.md` (verified for US-0108/0109/0111/0112; the other five are referenced from US-0106/US-0108 compose sections but the h1 anchors themselves were not directly grep-confirmed in discovery's narrow read). (Resolvable by tech-lead narrow read.)

No `EARLY_RESEARCH` web search needed — all sovereign-loop concepts are internal to the its-magic framework and already documented in `docs/engineering/architecture.md`, `docs/engineering/runbook.md`, and `.cursor/scratchpad.md`. No new R-xxxx entry created.

## Deferral candidates (sovereign-loop mode — noted, not written)

Under `AUTO_SOVEREIGN=1` + `SOVEREIGN_GOAL_MODE=goal_convergence`, deferral writes happen at the segment boundary (post `ship` macro-phase), not at phase boundaries. Discovery phase does NOT call `advance_sovereign_loop`. Noting for the orchestrator's segment-boundary advance hook:

- **DC-1**: US-0106 (Sovereign Role-Behavior Manifest) is not in US-0113's in-scope set but has a scratchpad block and catalog one-liner — operator may want a future story to cover it. Candidate for `sovereign_deferrals.jsonl` if the segment boundary detects the gap.

## Next phase

`/architecture` → tech-lead, `plan` macro-phase (first canonical phase is `research` inside the `plan` macro). Tech-lead should narrow-read `docs/engineering/architecture.md` h1 anchors for the 9 in-scope US ids and `docs/engineering/runbook.md` anchors listed above, then lock the README edit plan (umbrella + 9 subsections + scratchpad reference extension + runbook cross-links) and hand off to `/sprint-plan`.

---

# Intake handoff — US-0113..US-0117 scope broadening

**Date**: 2026-07-03
**Intake mode**: guided (`INTAKE_GUIDED_MODE=1`)

## Scope change

Operator requested broadening **US-0113** from sovereign-loop-only narrative documentation to **all features missing operator guides in the framework README**:

> "erweitere den letzten intake die US-113 darum, das alle fehlenden erweiterten feature beschriebungen ins readme erweitert werdden müssen, nicht nur die sovereign-loop era"

## New stories (decomposition: vertical slice by functional family)

- **US-0113** (existing) — Sovereign loop operator docs (US-0103..US-0110).
- **US-0114** (new) — Release & distribution operator docs (US-0111, US-0112, US-0041, US-0062).
- **US-0115** (new) — Integration & observability operator docs (US-0066, US-0065, US-0086, US-0093, US-0101).
- **US-0116** (new) — Delivery & lifecycle operator docs (US-0098, US-0099, US-0092, US-0095).
- **US-0117** (new) — Phase & role governance operator docs (US-0069..US-0090).

All 5 stories share the same AC pattern: (1) narrative section, (2) per-feature operator guide + scratchpad keys, (3) catalog preservation, (4) framework README parity.

## Acceptance

- [ ] AC-1: **Sovereign stack umbrella** section with default-off posture, recommended enable order, runbook pointer.
- [ ] AC-2: **Per-feature operator subsections** for every US owned by the story (narrative + scratchpad keys + master enable flags).
- [ ] AC-3: **Full scratchpad reference** extension covering all master enable flags and related keys for the US in scope, with defaults and zero-overhead-when-off wording.
- [ ] AC-4: **Coverage preserved / restored** — `validate_readme_feature_coverage.py --repo . --enforce` remains green.
- [ ] AC-5: **Framework README byte parity** — `its_magic/README.md` and `template/its_magic/README.md` byte-identical (via `check_intake_template_parity.py`).
- [ ] AC-6: **Audience + metadata** — `validate_doc_profile.py` and `check-user-visible-metadata.py` pass.
- [ ] AC-7: **Runbook cross-links** per feature (no runbook content duplication).
- [ ] AC-8: **Regression tests** — coverage parity contract tests remain green; no test weakenings.

## Status

- **US-0113..US-0117**: OPEN (ready for `/discovery`)
- **BUG-0014**: DONE (prior catalog coverage)
- **Portfolio**: 5 open stories

## Next

`/discovery` for US-0113 (or `/auto` to drain backlog in priority order).

---

## Intake handoff — US-0113 sovereign-only (prior)

**Date**: 2026-07-03
**Status**: SUPERSEDED by 5-story decomposition above.
