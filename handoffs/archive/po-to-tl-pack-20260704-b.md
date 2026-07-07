# po_to_tl archive pack (2026-07-04-b)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Rollover pass: 1 (US-0115 refresh-context terminal)
- Archived handoffs (oldest first, contiguous suffix): 4 (US-0114 lifecycle — sprint-plan, architecture, research, discovery; US-0113 lifecycle handoffs already archived in `po-to-tl-pack-20260704-a.md`)
- Retained handoffs in hot file: 4 (US-0115 lifecycle — sprint-plan, architecture, research, discovery)
- First archived heading: `# Sprint-plan handoff — US-0114 / auto-20260704-01`
- Last archived heading: `# Discovery handoff — US-0114 / auto-20260704-01`
- Verification tuple (mandatory):
  - archived_body_lines=364
  - preamble_lines=14

---

# Sprint-plan handoff — US-0114 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: sprint-plan (complete)
**Role**: tech-lead
**Story**: US-0114 — Release & distribution operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (sprint-plan — third canonical phase of `plan` macro)
**fresh_context_marker**: tl-US0114-sprint-plan-20260704T050000Z-fresh
**timestamp**: 2026-07-04T05:00:00Z

<!-- Archive pointer: US-0113 lifecycle handoffs (sprint-plan, architecture, research, discovery) + intake handoffs (broadening + sovereign-only prior) rolled over to `handoffs/archive/po-to-tl-pack-20260704-a.md` on 2026-07-04 by curator (US-0114 refresh-context terminal). Retained: US-0114 lifecycle handoffs (this file). -->

## Sprint

- **Sprint ID**: S0114
- **Sprint directory**: `sprints/S0114/`
- **Artifacts**: `sprints/S0114/sprint.md`, `sprints/S0114/tasks.md`, `sprints/S0114/summary.md`

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

## Compose guards (18 — all UNCHANGED)

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0041, US-0062. US-0114 lives entirely outside the compose surface (documentation-only).

## Architecture anchor

- `docs/engineering/architecture.md#US-0114` (h1 anchor appended at L914 in architecture phase; approach_locked=A1; companion_dec=none; stop_conditions_met=yes)
- Research anchor: R-0102 (4/4 discovery open questions closed)

## Non-goals (hard)

- No scratchpad canonical edits (`.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`)
- No installer changes (`installer.py/ps1/sh`)
- No runbook content additions (`docs/engineering/runbook.md` — AC-7 cross-links only; all 4 anchors exist — US-0062 → L171 via US-0097/DEC-0083 with explanatory note; US-0041 → L2522)
- No `docs/developer/README.md` edits (US-0097 compose guard)
- No `docs/engineering/architecture.md` edits beyond the `# US-0114` anchor already appended at L914 (2 missing `# US-0041`/`# US-0062` h1 anchors deferred to US-0117 — DC-2)
- No new tests proposed; no `scripts/*` edits (read-only gates)
- No release & distribution script amendments (US-0041/US-0062/US-0111/US-0112 documented only)
- No `tests/scratchpad_example_parity_test.py` edits (fix prose not test)
- **Encoding hygiene prerequisite**: orchestrator must restore working-tree `docs/product/backlog.md` encoding hygiene (185 stray `0xa7` bytes per R-0102) before execute so AC-4 can be re-verified post-execute.

## Decision gate

**No DECISION_GATE raised.** Architecture resolved both carry-overs within `plan` macro (DC-2 h1 anchors deferred to US-0117; scratchpad reference extension locked = net-new keys + cross-link pointers). Sprint-plan revealed no question requiring operator input. Verdict: **PASS**.

## Plan-verify readiness (ultra_lean merge note)

In **ultra_lean**, `/plan-verify` is **merged into the `build+verify` macro under QA**. This sprint does **not** pre-create `sprints/S0114/plan-verify.json` (orchestrator routes). Sprint-plan output is plan-verify-ready (surjective AC coverage, atomic tasks, test markers aligned) so QA can verify in one spawn within `build+verify`.

## Sovereign memory note

Sprint-plan phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not re-assembled in sprint-plan (architecture phase already noted existing digest context sufficient per R-0102; US-0114 documentation-only). DC-2 deferral noted in sprint non-goals for traceability.

## Next phase

Per **ultra_lean**, the orchestrator routes to the **`build+verify` macro**:
- `/execute` (dev, first canonical phase of `build+verify`)
- → `/qa` (qa, merges plan-verify + execute QA + verify-work)

Orchestrator will Task-spawn dev for `/execute`. Handoff via artifacts only.

---

# Architecture handoff — US-0114 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: architecture (complete)
**Role**: tech-lead
**Story**: US-0114 — Release & distribution operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (architecture — second canonical phase of `plan` macro)
**fresh_context_marker**: tl-US0114-architecture-20260704T043446Z-fresh
**timestamp**: 2026-07-04T04:34:46Z (UTC)

## Architecture anchor

- **`docs/engineering/architecture.md#US-0114`** (h1 anchor appended at L914 — `# US-0114 — Release & distribution operator documentation in framework README`). Architecture phase is the US-0114 anchor itself; the deferred `# US-0041` and `# US-0062` h1 anchors (DC-2) are NOT added in this phase — deferred to US-0117.

## Approach locked

**approach_locked=A1** — Single umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` section with 4 nested `#### US-xxxx` subsections (h4 under h3 umbrella), placed under `## Commands and workflow` (L350), as a **sibling** to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940). Recommended placement: immediately after the US-0113 sovereign-loop umbrella block (ends before L1225). Alternatives A2 (flat subsections, no umbrella) and A3 (place under `## Features`) rejected — see architecture.md § Approach locked for rationale.

## Sprint seeds preview (T-001..T-006)

**6 task seeds** (≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered; mirror US-0113 sibling pattern). Full task definitions in `docs/engineering/architecture.md#US-0114` § Sprint seeds.

| ID | Title (short) | AC |
|----|---------------|----|
| T-001 | Add `### Release & distribution` umbrella section under `## Commands and workflow` (after US-0113 block) | AC-1 |
| T-002 | Add 4 per-feature `#### US-xxxx` operator subsections (US-0041 → US-0062 → US-0111 → US-0112); release-workflow angle; bidirectional "see US-0113" pointers for US-0111/US-0112; runbook cross-links (US-0062 → L171 with note; US-0041 → L2522) | AC-2, AC-7 |
| T-003 | Extend `### Full scratchpad reference` with `### Release & distribution keys` sub-block — net-new keys only (US-0062's `PROJECT_README_ENFORCE`/`FRAMEWORK_KIT_REPO`) + grouped cross-links (US-0054, `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES`) + cross-link pointers to US-0113's block for overlapping US-0111/US-0112 keys | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical (one-way copy); re-run `fc /b` + `check_intake_template_parity.py` | AC-5 |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`); fix any drift; `coverage_missing=["US-0117"]` unchanged | AC-4, AC-6 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed); no test weakenings | AC-8 |

**Surjectivity**: AC-1..AC-8 all covered (AC-1→T-001; AC-2,AC-7→T-002; AC-3→T-003; AC-4,AC-6→T-005; AC-5→T-004; AC-8→T-006).

## Companion DEC

**companion_dec=none**. Confirmed (not overriding research R-0102). US-0114 is documentation-only — no architectural, policy, or schema surface changed. Pattern precedent: US-0113 sibling (shipped `companion_dec=none` per R-0101), BUG-0013 / BUG-0014 (per R-0099 / R-0100). The DC-2 deferral (US-0041/US-0062 h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC. See architecture.md § Companion DEC for full justification.

## Carry-overs resolved

- **(a) DC-2 — `# US-0041` and `# US-0062` h1 anchors missing in `architecture.md`**: **DEFER to US-0117** (parallel to US-0113's DC-1 — 5 anchors). US-0117 inherits DC-1 + DC-2 (7 anchors total) as architecture.md triad hygiene closure. **Do NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions) — note for orchestrator's segment-boundary advance hook.
- **(b) Scratchpad reference extension shape**: **LOCK net-new keys + cross-link pointers** (per R-0102 open question #1). US-0113's `### Sovereign-loop era keys` block byte-stability preserved; no duplicate key rows.

## Risks finalized

| Risk | Severity | Mitigation (short) |
|------|----------|--------------------|
| AC-3 overlap divergence | MEDIUM→LOW | Net-new keys + cross-link pointers only; US-0113 byte-stability preserved (T-003) |
| AC-5 parity lockstep | MEDIUM | T-004 one-way copy + `fc /b` + `check_intake_template_parity.py` |
| AC-7 US-0062 anchor | MEDIUM→LOW | Cross-link to L171 (`## Project README coverage validation (US-0097 / DEC-0083)`) with explanatory note |
| AC-8 regression tests | LOW–MEDIUM | Forbid edits to scratchpad canonical + test file; T-006 confirms green |
| AC-4 coverage drift / encoding | LOW (catalog) / MEDIUM (encoding) | `coverage_missing=["US-0117"]` unchanged; orchestrator must restore working-tree `backlog.md` encoding hygiene (185 stray `0xa7` bytes) before execute |
| AC-6 metadata leakage | LOW | T-005 validators; US-IDs only in parenthetical catalog tags |
| Decomposition drift (US-0113 angle overlap) | LOW | Bidirectional "see US-0113"/"see US-0114" pointers (T-002) |

## Compose guards (non-negotiable — all UNCHANGED)

**18 guards UNCHANGED**: US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0041, US-0062. US-0114 lives entirely outside the compose surface (documentation-only).

## Stop conditions

**stop_conditions_met=yes**:

- No major tradeoff requires DEC (companion_dec=none; documentation-only).
- No feasibility unknown (R-0102 closed all 4 open questions; architecture resolved both carry-overs).
- No data migration risk (documentation-only).
- No DECISION_GATE raised.

## Next phase

- **next_scheduled_phase=architecture** (tech-lead, `plan` macro — second canonical phase). Fresh spawn-only — do NOT carry chat context across phases per US-0048 / DEC-0029.
- **stop_condition=STOP after architecture artifacts are written (architecture.md `# US-0114` appended, this handoff prepended, state.md architecture checkpoint appended, resume_brief.md drain-advance block updated); orchestrator Task-spawns tech-lead for `/sprint-plan` (plan macro — third canonical phase).**

---

# Research handoff — US-0114 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: research (complete)
**Role**: tech-lead
**Story**: US-0114 — Release & distribution operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: plan (research — first canonical phase)
**fresh_context_marker**: tl-US0114-research-20260704T024540Z-fresh
**timestamp**: 2026-07-04T02:45:40Z

## Research anchor

- **R-0102** — `docs/engineering/research.md` (appended, ~280 lines). Per US-0053 / DEC-0011 ID auto-increment (highest existing was R-0101 per US-0113 sibling; no R-0102 collision verified via grep before append).

## 4 open questions resolution status (all RESOLVED — no DECISION_GATE)

| # | Discovery question | Resolution (R-0102 § Discovery open question resolution) | Status |
|---|---|---|---|
| 1 | AC-3 reference extension shape — net-new keys + cross-link pointers vs re-documented overlap keys? | **Net-new keys + cross-link pointers LOCKED.** US-0114's `### Release & distribution keys` sub-block covers ONLY net-new keys (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links to existing US-0054 publish controls (its_magic/README.md L541–547) and shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` (L1233/L1235) + cross-link pointers to US-0113's `### Sovereign-loop era keys` block for overlapping US-0111/US-0112 keys. No duplicate key rows. Byte-stability of US-0113's block preserved. | RESOLVED |
| 2 | AC-7 US-0062 runbook cross-link target — L171 vs L941 vs new stub? | **Cross-link to L171 LOCKED** (`## Project README coverage validation (US-0097 / DEC-0083)`) with explanatory note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)". L941 is structurally a US-0112 surface (conflates US-ids); new stub violates runbook hygiene (every `## US-xxxx` anchor carries normative content). | RESOLVED |
| 3 | US-0111/US-0112 narrative angle — release-workflow vs sovereign-loop (already shipped in S0113)? | **Release-workflow angle LOCKED.** US-0111 = trigger-source dispatch + changelog derivation mechanics + publish-mode composition; US-0112 = installer payload + version sync + operator opt-in. Both US-0114 subsections include bidirectional "see US-0113 for sovereign-loop angle" pointers (mirror US-0113's "see US-0114" pointer convention per R-0101). Backlog authority permits same US-id in two stories' subsections with angle-distinct narratives. | RESOLVED |
| 4 | US-0041/US-0062 architecture.md h1 anchors — add in US-0114 /architecture or defer to US-0117? | **DEFER TO US-0117 (DC-2) LOCKED.** Structurally parallel to US-0113's DC-1 (5 missing h1 anchors for US-0103/0104/0105/0107/0110 deferred to US-0117 per R-0101). US-0114's AC-7 is satisfiable via runbook cross-links (US-0041 ✓ L2522; US-0062 via US-0097 L171), so missing h1 anchors are NOT a US-0114 blocker. US-0117 (Phase & role governance family) inherits DC-1 + DC-2 as architecture.md triad hygiene closure. | RESOLVED (deferred to US-0117 as DC-2) |

**Verdict on open questions:** 4/4 RESOLVED. No DECISION_GATE raised. No operator input required.

## Recommended architecture approach (high-level — do NOT lock; architecture phase)

- **Umbrella (AC-1):** New `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` under `## Commands and workflow` (L350), as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112) umbrella section` (L940). Recommended placement: immediately **after** the closing of the US-0113 sovereign-loop umbrella block (which ends before L1225 `### Full scratchpad reference`), keeping the two era/family umbrellas visually adjacent. Default-off posture framing + 4-step recommended enable order (US-0062 → US-0041 → US-0112 → US-0111) + runbook pointer line.
- **Per-feature subsections (AC-2):** 4 `#### US-xxxx` subsections under the umbrella, ordered US-id-ascending (deterministic — matches catalog one-liner order at L82 / L1611 / L1651 / L1652): US-0041 → US-0062 → US-0111 → US-0112. Bidirectional "see US-0113 for sovereign-loop angle" pointers in US-0111/US-0112 subsections.
- **Scratchpad reference extension (AC-3):** New `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block as a sibling to `### Sovereign-loop era keys (US-0103–US-0112)` (L1242) under `### Full scratchpad reference (detailed)` (L1225). Net-new key rows ONLY (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links to existing US-0054 publish controls (L541–547) and shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` (L1233/L1235) + cross-link pointers to US-0113's block for overlapping US-0111/US-0112 keys. No duplicate key rows.
- **DC-2 deferral:** `/architecture` documents the DC-2 deferral (US-0041/US-0062 h1 anchors missing) in its architecture findings block; does NOT add the h1 anchors. Orchestrator's segment-boundary advance hook handles `handoffs/sovereign_deferrals.jsonl` at segment close (not phase boundaries).
- **Risks:** AC-5 MEDIUM (parity lockstep via one-way copy — same as US-0113); AC-3 MEDIUM→LOW (mitigated by overlap resolution — net-new keys + cross-link pointers only); AC-7 MEDIUM→LOW (mitigated by L171 cross-link with explanatory note); AC-1/2/4/6/8 LOW; decomposition-drift LOW.
- **Compose guards (16 — all UNCHANGED, same as US-0113):** US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112.

## Working-tree hygiene regression flagged (NOT a US-0114 blocker)

`docs/product/backlog.md` working-tree copy has 185 stray `0xa7` (§) bytes (Windows-1252 encoding corruption from untracked scripts `fix_backlog.py` / `insert_stories.py` per `git status`) that break `validate_readme_feature_coverage.py`'s strict UTF-8 read. HEAD baseline verified via stash-aside: 104 covered, 0 missing, status=PASS. Research phase is read-only on backlog.md. **Flag to orchestrator:** restore backlog.md encoding hygiene before execute (or coordinate via stash-aside workflow) so AC-4 can be re-verified post-execute.

## AC baselines (read-only, established in R-0102)

- **AC-4 (HEAD baseline via stash):** 104 covered, 0 missing, 0 gaps, status=PASS. US-0117 pre-existing gap (US-0103/0104/0105/0107/0110 catalog one-liners missing per R-0101) out of US-0114 scope — DC-1 deferral to US-0117 unchanged.
- **AC-5:** PARITY_OK (`cmd /c fc /b its_magic\README.md template\its_magic\README.md` → `FC: no differences encountered`). US-0113 shipped this state 2026-07-04T03:00:00Z.
- **AC-6:** Baseline not re-run in research (no README edits in research); execute phase re-runs `validate_doc_profile.py` + `check-user-visible-metadata.py` after edits.
- **AC-8:** 4 passed (`python -m pytest tests/scratchpad_example_parity_test.py -q` → `.... [100%] 4 passed in 0.07s`). US-0113 shipped this state.
- **Intake template parity:** `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`.

## Next phase

- **next_scheduled_phase=architecture** (tech-lead, `plan` macro — second canonical phase). Fresh spawn-only — do NOT carry chat context across phases per US-0048 / DEC-0029.
- **stop_condition=STOP after research artifacts are written (R-0102 appended, this handoff prepended, state.md checkpoint appended, resume_brief.md drain-advance block updated); orchestrator Task-spawns tech-lead for `/architecture`.**

---

# Discovery handoff — US-0114 / auto-20260704-01

**Date**: 2026-07-04
**Phase**: discovery (complete)
**Role**: po
**Story**: US-0114 — Release & distribution operator documentation in framework README
**orchestrator_run_id**: auto-20260704-01
**delivery_mode**: ultra_lean
**macro_phase**: spec (discovery — intake already complete per 5-story decomposition in this file)
**fresh_context_marker**: po-US0114-discovery-20260704T004200Z-fresh
**timestamp**: 2026-07-04T00:42:00Z

## Confirmed in-scope feature set (4 US ids)

Per `docs/product/backlog.md` US-0114 block (L3911–3927, status OPEN) `related_us` field and the 5-story decomposition intake handoff below (L362–368):

- **US-0111** — Release-Trigger-Driven Version Changelog Derivation (release-trigger adapters)
- **US-0112** — Ship Model-Catalog Example Presets on Install/upgrade
- **US-0041** — End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean
- **US-0062** — Installer-Owned `its_magic/` Folder for Framework Metadata

**Decomposition confirmation**: US-0114 = release & distribution family slice only. US-0115..US-0117 work is **out of scope** for this story (drain mutex — one story at a time per `handoffs/resume_brief.md` priority order; backlog_drain_stories_remaining=4 with US-0114 active). US-0091 (catalog anchor), US-0097 (project README parity), US-0017 (framework README parity) are **compose-touch references**, not in-scope feature work — they are AC-4/AC-5/AC-6 contract surfaces.

## Angle-distinct narrative confirmation (US-0111 / US-0112)

Per R-0101 (US-0113 research) and the US-0113 sprint-plan handoff (this file, sprint-plan block T-002): US-0111 and US-0112 appear in BOTH US-0113 (sovereign-loop family — **already shipped**, S0113 RELEASED 2026-07-04T03:00:00Z per `handoffs/resume_brief.md` L15) AND US-0114 (release & distribution family). Same US-id, two angle-distinct narratives:

- **US-0113 sovereign-loop angle (SHIPPED — do not duplicate in US-0114)**: US-0111 = release-trigger adapter as a sovereign-loop notification/ledger surface (emits release event tuple to US-0103 ledger; `SOVEREIGN_NOTIFY_TARGET=hook` wiring); US-0112 = preset delivery as a sovereign-loop bootstrap aid (presets tune `MODEL_TIER` / `TOKEN_PROFILE` / `DELIVERY_MODE` / `ID_NAMESPACE_BOOTSTRAP` — values the loop reads at phase boundaries). US-0113's `its_magic/README.md` subsections at L1166 (US-0111) and L1191 (US-0112) already ship the sovereign-loop angle and include explicit "see US-0114 for release-workflow operator docs on this feature" pointers.
- **US-0114 release-workflow angle (US-0114 OWNS)**: US-0111 = release-trigger adapters as a release-workflow tool (GitHub webhook, npm publish, git tag, manual `/release` dispatch mechanics + changelog derivation mechanics, `RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` as release operator controls); US-0112 = model-catalog example preset shipping via installer/upgrade (installer payload + version sync mechanics, preset file layout under `template/.cursor/model-catalog.local.example*.json`, operator opt-in by copying to `.cursor/model-catalog.local.json`). US-0114's US-0111/US-0112 subsections MUST include explicit "see US-0113 for sovereign-loop angle" pointers (mirror US-0113's "see US-0114" pointer convention).

**Risk (decomposition drift)**: LOW. Mitigation: angle-distinct narrative contract above + bidirectional "see US-xxxx" pointers (US-0113 → US-0114 already shipped; US-0114 → US-0113 must be added in execute). Tech-lead (`plan` macro) should re-confirm the angle boundary in `/research` and lock it in `/architecture`.

## README operator-doc structure map (`its_magic/README.md`)

Current README structure (post-S0113 RELEASED state — 2023 lines per `git status`; US-0113 added the sovereign-loop era umbrella + 9 subsections + scratchpad reference extension):

- L22 `## Features (what its-magic can do)` — tiered feature hierarchy (catalog-one-liner depth)
- L63 `<!-- readme-feature-coverage-catalog -->` — US-0091 catalog anchor (preserved, AC-4)
- L65 `### Feature coverage catalog (US-0091)` — existing one-liners (US-0041 L82, US-0062 L1611 already present at catalog-one-liner depth)
- L218 `### Lifecycle QA matrix (US-0041)` — existing US-0041 surface in `## Setup` region (NOT under `## Commands and workflow`) — narrative operator guide (AC-2) for US-0041 lands as a NEW `#### US-0041` subsection under the new release & distribution umbrella, NOT by editing this existing Setup block (read-only)
- L350 `## Commands and workflow` — AC-1 umbrella insertion parent
- L940 `### Sovereign-loop era (US-0103–US-0112) umbrella section` — US-0113-shipped umbrella (sibling)
- L1225 `### Full scratchpad reference (detailed)` — AC-3 extension target (parent)
- L1242 `### Sovereign-loop era keys (US-0103–US-0112)` — US-0113-shipped scratchpad reference sub-block (sibling; covers US-0111/US-0112 keys — see overlap note below)

**Where the umbrella section lands (AC-1)**: New `### Release & distribution (US-0111 / US-0112 / US-0041 / US-0062) umbrella section` is inserted **under `## Commands and workflow`** as a sibling to the US-0113 sovereign-loop era umbrella. Recommended placement: **immediately after** the US-0113 sovereign-loop era umbrella block (which closes before L1225 `### Full scratchpad reference`), keeping the two era/family umbrellas visually adjacent under `## Commands and workflow`. Per AC-1 wording the umbrella must live under `## Commands and workflow`, not under `## Features` (Features already has catalog one-liners; umbrella is narrative operator guide).

**Per-feature operator subsection sequence (AC-2)**: 4 subsections under the umbrella, ordered by US-id-ascending (deterministic, matches backlog `related_us` ordering):

1. `#### US-0041 — End-to-End Lifecycle QA for its-magic install/upgrade/clean`
2. `#### US-0062 — Installer-Owned its_magic/ folder for framework metadata`
3. `#### US-0111 — Release Trigger Adapters (release-workflow angle)`
4. `#### US-0112 — Ship Model-Catalog Example Presets on install/upgrade (release-workflow angle)`

Note: US-0041 and US-0062 are pre-release / installer-domain features that precede US-0111/US-0112 numerically; ordering US-id-ascending keeps the family list deterministic and matches the catalog one-liner order at L82 / L1611. Tech-lead (`plan` macro) may reorder if a release-workflow narrative dependency chain argues otherwise — default recommendation is US-id-ascending.

## Scratchpad reference extension map (AC-3)

`### Full scratchpad reference (detailed)` at L1225 is the extension parent. US-0113 already added a sibling `### Sovereign-loop era keys (US-0103–US-0112)` sub-block at L1242 covering sovereign-loop keys including US-0111 (`RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` at L1338–1346) and US-0112 (`DELIVERY_MODE` / `TOKEN_PROFILE` / `ID_NAMESPACE_BOOTSTRAP` / `MODEL_TIER` at L1348–1364).

**Overlap finding (flag for tech-lead)**: The user-query assumption that US-0114's release & distribution keys are "disjoint from US-0113's sovereign-loop keys" is **only true for US-0041 and US-0062**. US-0111's `RELEASE_TRIGGER_*` keys and US-0112's `DELIVERY_MODE` / `TOKEN_PROFILE` / `ID_NAMESPACE_BOOTSTRAP` / `MODEL_TIER` keys are **already present** in the US-0113 sovereign-loop era keys block (L1338–1364). Discovery does NOT decide whether US-0114 adds a parallel `### Release & distribution keys` sub-block that re-documents these keys from the release-workflow angle, or instead adds a `### Release & distribution keys` sub-block covering ONLY US-0041/US-0062 net-new keys + cross-link pointers to the US-0113 block for US-0111/US-0112 overlap keys. This is a `plan`-macro clarification (architecture phase locks the reference-extension shape); discovery flags it as open question #1 below.

**Net-new release & distribution keys (from `.cursor/scratchpad.md` narrow reads)** — disjoint from US-0113's sovereign-loop keys, candidates for US-0114's reference extension:

| Feature | Scratchpad keys (from `.cursor/scratchpad.md`) | Source lines |
|---|---|---|
| US-0041 (lifecycle QA — no dedicated scratchpad block; lifecycle QA matrix is runbook-anchored, see runbook L2522) | (no dedicated lifecycle-QA scratchpad keys; installer completeness keys `INSTALL_MANIFEST_ERROR` / `INSTALL_COMPLETENESS_FAILED` are reason codes, not scratchpad flags) | n/a — flag for tech-lead |
| US-0062 (installer-owned `its_magic/` folder) | `PROJECT_README_ENFORCE=0\|1` (default `1` post-bootstrap), `FRAMEWORK_KIT_REPO=0\|1` (default `0`; kit repo exception) | L260–267 |
| US-0041 / US-0062 shared release surface | `AUTO_INSTALL_DEPS=0\|1` (default `1`), `AUTO_RELEASE_NOTES=0\|1` (default `1`) | L66–67 |
| US-0111 (release-trigger — overlap with US-0113 sovereign-loop keys) | `RELEASE_TRIGGER_SOURCE`, `RELEASE_TRIGGER_TIMEOUT_SEC`, `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` | L529–539 (already in US-0113 block L1338) |
| US-0111 publish controls (US-0054 family — release-workflow angle) | `RELEASE_PUBLISH_MODE=disabled\|confirm\|auto` (default `confirm`), `RELEASE_TARGETS_FILE` (default `docs/engineering/release-targets.json`), `RELEASE_TARGETS_DEFAULT` (default empty) | L200–209 |
| US-0112 (catalog presets — overlap with US-0113 sovereign-loop keys) | `DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP`, `MODEL_TIER` | L181–199 (already in US-0113 block L1348) |
| Delivery mode (cross-cutting — release-workflow angle) | `DELIVERY_MODE=ultra_lean\|mega_quick\|balanced\|highend` (default `balanced`), `LEAN_MEMORY_READ`, `LEAN_MEMORY_WRITE`, `LEAN_COLD_READ_MAX_SECTIONS`, `LEAN_STATE_INDEX_ROWS`, `AUTO_DELIVERY_ROUTING` | L181–186 |

**Open question for tech-lead (US-0041 scratchpad surface)**: US-0041 has NO dedicated scratchpad key block — its normative surface is the runbook `## Lifecycle QA matrix (US-0041)` L2522 + `tests/run-tests.*` lifecycle test markers + installer completeness reason codes (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING`). The `plan` macro-phase (tech-lead) should confirm whether US-0041's operator subsection references existing installer completeness keys / reason codes (no new scratchpad block) or gets a new release-distribution-adjacent key block. **Discovery does not decide this** — flagging as a `plan`-phase clarification, not a decision gate (no operator input required; tech-lead can resolve from runbook L2522 + `architecture.md` archive packs `architecture-pack-20260606-b.md` `# US-0062`).

## Runbook cross-link targets (AC-7 — existing anchors only)

Existing runbook section anchors in `docs/engineering/runbook.md` for cross-linking (no new runbook content in US-0114 — AC-7 forbids runbook content duplication):

| Feature | Runbook anchor (existing) | Line | Status |
|---|---|---|---|
| US-0111 | `## Release Trigger Adapters (US-0111 / DEC-0111)` | L3378 | ✓ existing |
| US-0112 | `## Model-catalog example preset delivery (US-0112 / DEC-0112)` | L941 | ✓ existing |
| US-0041 | `## Lifecycle QA matrix (US-0041)` | L2522 | ✓ existing |
| US-0062 | (no dedicated `## US-0062` h2 anchor — referenced only from `## Project README coverage validation (US-0097 / DEC-0083)` L171 + installer completeness sections L492–494) | n/a | ✗ AC-7 GAP |

**AC-7 gap finding (US-0062)**: US-0062 has NO dedicated `## US-0062` h2 anchor in `docs/engineering/runbook.md`. AC-7 wording requires "Runbook cross-links per feature (no runbook content duplication)" — US-0114's US-0062 operator subsection needs an existing anchor to cross-link. Three options for the tech-lead (`plan` macro) to resolve:

1. **Cross-link to existing `## Project README coverage validation (US-0097 / DEC-0083)` L171** (which amends DEC-0045 / US-0062 per decisions.md L311 + L445) — closest existing runbook anchor that documents the US-0062 installer ownership boundary. Mitigation: US-0114's US-0062 subsection cross-links to L171 with note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083)". **Discovery default recommendation**.
2. **Cross-link to `## Model-catalog example preset delivery (US-0112 / DEC-0112)` L941** (which covers installer manifest framework-file semantics L944–946, the surface US-0062 declared) — secondary existing anchor covering the installer-owned-paths manifest.
3. **Add a new `## US-0062 — Installer-Owned its_magic/ folder (DEC-0045)` h2 anchor to runbook.md** — violates AC-7 "no runbook content duplication" only if it duplicates content; a minimal stub cross-link anchor may be acceptable. Tech-lead decides; if it requires runbook content addition, it is a deferral candidate (DC-2, see below).

**Discovery does NOT add runbook content** (AC-7 forbids; execute-phase work only). Flagging as open question #2 below.

**Architecture.md h1 anchor inventory (related_us family)** — for tech-lead awareness (NOT a US-0114 AC, but informs `/research`):

| Feature | architecture.md h1 anchor | Line | Status |
|---|---|---|---|
| US-0111 | `# US-0111 — Release-Trigger-Driven Version Changelog Derivation` | L335 | ✓ existing |
| US-0112 | `# US-0112 — Ship Model-Catalog Example Presets on Install/upgrade` | L454 | ✓ existing |
| US-0041 | (no h1 in active `architecture.md`; only in archive `architecture-pack-20260606-b.md` etc.) | n/a | ✗ GAP |
| US-0062 | (no h1 in active `architecture.md`; only in archive `architecture-pack-20260606-b.md` `# US-0062: Installer-Owned its_magic/ Folder` L156) | n/a | ✗ GAP |

US-0041 and US-0062 missing h1 anchors in active `architecture.md` are a **deferral candidate** (DC-2, parallel to US-0113's DC-1 for US-0103/0104/0105/0107/0110). Not a US-0114 blocker (AC-7 only requires runbook cross-links; US-0111/US-0112 h1 anchors exist; US-0041/US-0062 operator subsections can be grounded in runbook + archive packs). Tech-lead may add minimal h1 anchors in `/architecture` or defer to US-0117 (phase & role governance family — likely owns architecture.md triad hygiene closure). See Deferral candidates below.

## Risks

- **AC-1 (umbrella placement)**: LOW. US-0113 already established the umbrella-under-`## Commands and workflow` pattern (L940 sibling); US-0114 reuses it. Risk: edit accidentally lands inside the US-0113 sovereign-loop umbrella block. Mitigation: execute-phase must insert the new umbrella **after** the closing of the US-0113 sovereign-loop umbrella (which ends before L1225 `### Full scratchpad reference`), not inside it.
- **AC-2 (per-feature subsections)**: LOW–MEDIUM. US-0111/US-0112 angle overlap with US-0113 (already-shipped sovereign-loop angle). Risk: execute-phase prose duplicates US-0113's sovereign-loop angle instead of writing the release-workflow angle. Mitigation: angle-distinct narrative contract above + bidirectional "see US-0113" pointers; tech-lead locks the angle boundary in `/architecture`.
- **AC-3 (scratchpad reference extension)**: MEDIUM. US-0111/US-0112 key overlap with US-0113's `### Sovereign-loop era keys` block (L1338–1364). Risk: US-0114 re-documents the same keys with conflicting default/wording, breaking byte-stability of the US-0113 block. Mitigation: tech-lead locks whether US-0114's reference sub-block covers ONLY net-new keys (US-0041/US-0062 + `RELEASE_PUBLISH_MODE` family + delivery mode keys) and cross-links to US-0113's block for overlap keys, OR re-documents overlap keys from the release-workflow angle in a separate sub-block with explicit "see US-0113 sovereign-loop era keys for sovereign-loop angle" pointer. Default recommendation: net-new keys + cross-link pointers (avoids byte-stability risk on the US-0113 block).
- **AC-4 (coverage preserved)**: LOW. `validate_readme_feature_coverage.py --enforce` is green per US-0113 release (117/117 per state.md L770; US-0117 pre-existing gap out of US-0114 scope). US-0114 only **adds** narrative sections; it does not remove or rewrite catalog one-liners. The `<!-- readme-feature-coverage-catalog -->` anchor at L63 and existing one-liners (US-0041 L82, US-0111 L88, US-0062 L1611, US-0112 implicit via catalog) must remain byte-stable. Risk: an edit accidentally reflows the catalog block. Mitigation: execute-phase must treat the catalog block as read-only and append new narrative sections outside it.
- **AC-5 (framework README parity)**: MEDIUM. `its_magic/README.md` ↔ `template/its_magic/README.md` must stay byte-identical. US-0113 established the parity lockstep pattern (one-way copy + `fc /b` + `check_intake_template_parity.py`); US-0114 reuses it. Risk: edit only one surface. Mitigation: execute-phase must edit `its_magic/README.md` then one-way copy to `template/its_magic/README.md` in lockstep and re-run `fc /b` + `check_intake_template_parity.py` before QA.
- **AC-6 (audience + metadata hygiene)**: LOW. `validate_doc_profile.py` and `check-user-visible-metadata.py` must pass. New narrative sections must use operator-audience wording (not internal-only IDs in user-visible prose). Risk: leaking internal IDs (US-xxxx, DEC-xxxx, R-xxxx) into user-visible prose. Mitigation: follow existing README convention — US-IDs allowed in parenthetical catalog tags `(US-0111)` but not in narrative sentences.
- **AC-7 (runbook cross-links)**: MEDIUM. US-0062 has NO dedicated runbook h2 anchor (see AC-7 gap finding above). Risk: execute-phase either invents a non-existent anchor (broken link) or duplicates runbook content (AC-7 violation). Mitigation: tech-lead locks the cross-link target in `/architecture` (default recommendation: cross-link to `## Project README coverage validation (US-0097 / DEC-0083)` L171 with explanatory note).
- **AC-8 (regression tests)**: LOW–MEDIUM. Coverage parity contract tests must remain green; no test weakenings. US-0113 established the pattern (forbid edits to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, `tests/scratchpad_example_parity_test.py` in execute; if test fails, fix prose not test). US-0114 reuses it. Risk: a test is "relaxed" to accommodate a new section. Mitigation: execute-phase must not modify `tests/scratchpad_example_parity_test.py` or coverage contract tests.
- **Decomposition drift risk**: LOW. US-0115..US-0117 are queued and could tempt scope creep into US-0114. Mitigation: drain mutex — US-0114 ships first; US-0115..US-0117 pick up other families. US-0111/US-0112 angle overlap with US-0113 is the only intentional cross-story overlap (per backlog authority) and is bounded by the angle-distinct narrative contract.

## Open questions / decision gate recommendations

**No DECISION_GATE raised.** All identified questions are resolvable by the tech-lead in the `plan` macro-phase without operator input:

1. **Scratchpad reference extension shape (AC-3)** — does US-0114's reference sub-block cover ONLY net-new release & distribution keys (US-0041/US-0062 + `RELEASE_PUBLISH_MODE` family + delivery mode keys) and cross-link to US-0113's `### Sovereign-loop era keys` block for US-0111/US-0112 overlap keys, OR re-document overlap keys from the release-workflow angle in a separate sub-block? (Resolvable by tech-lead; discovery default recommendation: net-new keys + cross-link pointers to avoid byte-stability risk on the US-0113 block.)
2. **US-0062 runbook cross-link target (AC-7)** — cross-link to `## Project README coverage validation (US-0097 / DEC-0083)` L171 (default recommendation), OR `## Model-catalog example preset delivery (US-0112 / DEC-0112)` L941, OR add a new minimal `## US-0062` h2 stub anchor to runbook.md (may edge into AC-7 "no runbook content duplication" territory — tech-lead decides)? (Resolvable by tech-lead narrow read.)
3. **US-0041 scratchpad key surface** — does US-0041's operator subsection reference existing installer completeness reason codes (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING`) + runbook `## Lifecycle QA matrix (US-0041)` L2522 anchor (no new scratchpad block), OR get a new release-distribution-adjacent key block? (Resolvable by tech-lead from runbook L2522 + `architecture.md` archive packs.)
4. **US-0041 / US-0062 architecture.md h1 anchors** — should `/architecture` add minimal `# US-0041` and `# US-0062` h1 anchors to active `architecture.md` (parallel to US-0113's DC-1 deferred anchors), OR defer to US-0117 (phase & role governance family — likely owns architecture.md triad hygiene closure)? (Resolvable by tech-lead; not a US-0114 AC blocker.)

No `EARLY_RESEARCH` web search needed — all release & distribution concepts (release-trigger adapters, model-catalog presets, lifecycle QA, installer-owned `its_magic/` folder) are internal to the its-magic framework and already documented in `docs/engineering/architecture.md` (US-0111 L335, US-0112 L454) + archive packs (US-0041, US-0062), `docs/engineering/runbook.md` (L941, L2522, L3378), and `.cursor/scratchpad.md`. No new R-xxxx entry created in discovery (research phase may add an R-0102-style entry if the tech-lead needs to deepen the angle-distinct narrative contract or the AC-3 reference extension shape — that is the tech-lead's call in `plan` macro).

## Deferral candidates (sovereign-loop mode — noted, not written)

Under `AUTO_SOVEREIGN=1` + `SOVEREIGN_GOAL_MODE=goal_convergence`, deferral writes happen at the segment boundary (post `ship` macro-phase), not at phase boundaries. Discovery phase does NOT call `advance_sovereign_loop`. Noting for the orchestrator's segment-boundary advance hook (DO NOT append to `handoffs/sovereign_deferrals.jsonl` in discovery phase):

- **DC-2** (US-0114 family): `# US-0041` and `# US-0062` h1 anchors are missing from active `docs/engineering/architecture.md` (only present in archive packs `architecture-pack-20260606-b.md`). US-0114's AC-7 is satisfiable via runbook cross-links (US-0041 ✓ L2522; US-0062 via US-0097 L171 default recommendation), so the gap is NOT a US-0114 blocker. Candidate for `sovereign_deferrals.jsonl` if the segment boundary detects the gap; otherwise US-0117 (phase & role governance family) is the natural owner for architecture.md triad hygiene closure (it already inherits DC-1 from US-0113 for US-0103/0104/0105/0107/0110 h1 anchors — DC-2 is structurally parallel). When US-0117 enters `plan` macro, its discovery should narrow-read `architecture.md` h1 inventory and add the missing `# US-0041` / `# US-0062` (and DC-1's `# US-0103` / `# US-0104` / `# US-0105` / `# US-0107` / `# US-0110`) h1 anchors as task seeds (anchor format: `# US-xxxx — <feature title>`).

## Decision gate

**No DECISION_GATE raised.** All 4 open questions are resolvable by the tech-lead in the `plan` macro-phase without operator input. Verdict: **PASS**.

## Sovereign memory note

Discovery phase does NOT call `advance_sovereign_loop` (advance hook runs at segment boundary post `ship` macro). Sovereign-memory digest not assembled in discovery (US-0113 retrospective `docs/engineering/sovereign-memory/retrospectives/S0113.md` established the reusable pattern: "operator-documentation gap closing follows 5-story decomposition by functional family with angle-distinct narratives" — applied to US-0114 as the release & distribution family slice with US-0111/US-0112 angle-distinct from US-0113's sovereign-loop angle). No mistake event in discovery (no write to `mistakes.jsonl`).

## Next phase

`/research` → tech-lead, `plan` macro-phase (first canonical phase). Fresh subagent spawn. The research-phase tech-lead should narrow-read this discovery handoff block, `docs/product/backlog.md` US-0114 block (L3911–3927), `docs/engineering/architecture.md` h1 anchors for US-0111 (L335) / US-0112 (L454) + archive packs for US-0041 / US-0062, `docs/engineering/runbook.md` anchors (L941, L2522, L3378, L171), `.cursor/scratchpad.md` release & distribution keys (L66–67, L181–209, L260–267, L529–539), and `its_magic/README.md` post-S0113 structure (L940 sovereign-loop umbrella sibling, L1225 scratchpad reference parent, L1242 US-0113 sovereign-loop keys sub-block for overlap check), then close the 4 open questions above and hand off to `/architecture`.

Orchestrator will Task-spawn tech-lead for `/research`. Hand off via artifacts only.
