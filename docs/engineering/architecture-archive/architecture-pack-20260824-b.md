# Architecture archive pack (2026-08-24)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 49
- First archived heading: `# US-0114 — Release & distribution operator documentation in framework README`
- Last archived heading: `## US-0115 — Integration & observability operator documentation in framework README`
- Verification tuple (mandatory):
  - archived_body_lines=351
  - preamble_lines=1
  - retained_body_lines=2869

---

# US-0114 — Release & distribution operator documentation in framework README

## Overview

**US-0114** is a documentation-only story closing the operator-documentation gap for the **release & distribution** functional family — US-0111 (Release Trigger Adapters), US-0112 (Model-Catalog Example Presets), US-0041 (End-to-End Lifecycle QA), US-0062 (Installer-Owned `its_magic/` Folder for Framework Metadata). It adds an umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` narrative section under `## Commands and workflow` (L350) in `its_magic/README.md`, as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940). The umbrella carries 4 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending (US-0041 → US-0062 → US-0111 → US-0112), with bidirectional `see US-0113 for sovereign-loop angle` pointers in the US-0111/US-0112 subsections. A matching `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1225) as a sibling to `### Sovereign-loop era keys` (L1242), covering **net-new** keys only (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links to existing US-0054 publish controls (L541–547) and shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` (L1233/L1235) + cross-link pointers to US-0113's block for overlapping US-0111/US-0112 keys. The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0114 is documentation-only; no architectural, policy, or schema surface is being changed; R-0102 § Decision-gate check confirmed no DEC required). **Research anchor**: **R-0102** (delivered 2026-07-04T02:45:40Z, 4/4 open questions closed). **Compose guards (non-negotiable)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0114-architecture-20260704T043446Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T04:34:46Z
**Verdict**: PASS
**Next**: `/sprint-plan`

## Companion DEC

**companion_dec=none**. Confirmed (not overriding research R-0102). Justification:

- US-0114 introduces **no** new architectural surface — no schema, no code path, no installer classification, no policy, no precedence rule, no role matrix change. It is a pure documentation backfill of the release & distribution family operator surface.
- The "operator-documentation gap closing" pattern is a recurring documentation-only pattern already established by US-0113 (sibling, `companion_dec=none` per R-0101) and BUG-0013 / BUG-0014 (both shipped with `companion_dec=none` per R-0099 / R-0100). US-0114 follows the same precedent as its US-0113 sibling.
- The 4 discovery open questions were all resolved within the `plan` macro as docs backfill decisions (R-0102 § Discovery open question resolution); none required operator input or a tradeoff record. The DC-2 deferral (US-0041/US-0062 architecture.md h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC.
- US-0114's release-workflow angle on US-0111/US-0112 does not amend DEC-0111 / DEC-0112 — those decisions define the features; US-0114 only documents the operator angle. No DEC surface is touched.
- Reserving a DEC id would be wasteful since there is no decision surface to record.

## Approach locked

**approach_locked=A1** — Single umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` section with 4 nested `#### US-xxxx` subsections (h4 under h3 umbrella), placed under `## Commands and workflow` (L350), as a **sibling** to US-0113's `### Sovereign-loop era (US-0103–US-0112)` umbrella (L940). Recommended placement: immediately **after** the closing of the US-0113 sovereign-loop umbrella block (which ends before L1225 `### Full scratchpad reference (detailed)`), keeping the two family umbrellas visually adjacent.

### Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | Single umbrella `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` + 4 nested `#### US-xxxx` subsections (h4 under h3) | **Locked** — preferred for navigation; consistent with US-0113 sibling approach (umbrella → per-feature detail); preserves AC-2 "per-feature operator subsections" wording naturally; keeps the 4 release & distribution features visually grouped as a functional family rather than scattered; mirrors US-0113's established pattern so the README has a uniform era/family-umbrella shape. |
| **A2** | Flat 4 `#### US-xxxx` subsections directly under `## Commands and workflow` with cross-links but no umbrella | **Rejected** — loses family grouping; scatters release & distribution features among unrelated workflow subsections; weakens AC-1 (umbrella section is an explicit AC); breaks parity with US-0113's sibling pattern; harder for operators to discover the release & distribution feature cluster. |
| **A3** | Place umbrella under `## Features (what its-magic can do)` instead of `## Commands and workflow` | **Rejected** — `## Features` already has the US-0091 catalog one-liners; AC-1 explicitly requires the umbrella under `## Commands and workflow`; narrative operator guides are workflow-shaped, not catalog-shaped. Same rationale that rejected A3 for US-0113. |

**Simplicity check**: A1 is the simplest approach that meets all 8 ACs. A2 violates AC-1. A3 violates AC-1. No simpler viable alternative exists; the alternative would be "do nothing" which fails AC-1..AC-3.

## Files to touch

| File | Action | Notes |
|---|---|---|
| `its_magic/README.md` | append `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella + 4 nested `#### US-xxxx` operator subsections under `## Commands and workflow` (L350), after the US-0113 sovereign-loop umbrella block (ends before L1225); append `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block under `### Full scratchpad reference (detailed)` (L1225), as sibling to `### Sovereign-loop era keys` (L1242) | AC-1, AC-2, AC-3, AC-7; catalog block (L63 anchor + L1235–L1243 one-liners) treated as read-only (AC-4); net-new keys only + cross-link pointers (AC-3) |
| `template/its_magic/README.md` | one-way byte-sync copy from `its_magic/README.md` after T-001/T-002/T-003 complete | AC-5 lockstep; `cmd /c fc /b its_magic\README.md template\its_magic\README.md` + `python scripts/check_intake_template_parity.py` re-run required |

**Explicitly NOT touched** (decision):

- `docs/engineering/architecture.md` — the missing `# US-0041` and `# US-0062` h1 anchors are **deferred to US-0117** (DC-2, parallel to US-0113's DC-1). See carry-over (a) below. The only architecture.md edit in this phase is the append of this `# US-0114` section (the architecture anchor for US-0114 itself).

## Files NOT to touch

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent; US-0114 only documents existing keys).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership; US-0114 does not extend the scratchpad canonical, only documents existing keys in README).
- `docs/product/backlog.md` — status authority (closure only at `/release`). **Note:** working-tree copy has 185 stray `0xa7` bytes (encoding regression flagged in R-0102) — research phase is read-only; orchestrator to restore encoding hygiene before execute so AC-4 can be re-verified post-execute.
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 4 runbook anchors already exist (US-0041 → `## Lifecycle QA matrix (US-0041)` L2522; US-0062 → `## Project README coverage validation (US-0097 / DEC-0083)` L171 with explanatory note; US-0111/US-0112 → existing anchors per R-0102).
- `docs/developer/README.md` — separate audience surface owned by US-0097 (project README parity) compose guard; AC-6 is a validator gate, not an edit mandate.
- `docs/engineering/architecture.md` (other than this `# US-0114` append) — missing `# US-0041` / `# US-0062` h1 anchors deferred to US-0117 (DC-2). **Do NOT add DC-2 anchors here.**
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 + US-0062/DEC-0045 + US-0041/BUG-0003 compose guards).
- All scripts (`scripts/validate_readme_feature_coverage.py`, `scripts/check_intake_template_parity.py`, `scripts/validate_doc_profile.py`, `scripts/check-user-visible-metadata.py`, etc.) — validators are read-only gates, not edit targets.
- All release & distribution scripts and Python/PowerShell/Shell files — US-0111/US-0112/US-0041/US-0062 features are **documented only**, not amended.
- All test files (`tests/scratchpad_example_parity_test.py`, etc.) — read-only regression gates (AC-8).

## Sprint seeds (T-001..T-006)

**6 task seeds** (≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered; mirror US-0113 sibling pattern).

| ID | Title | AC | Tranche |
|----|-------|----|:---------|:---------|
| **T-001** | Add `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section under `## Commands and workflow` (L350), placed immediately after the US-0113 sovereign-loop umbrella block (ends before L1225 `### Full scratchpad reference`). Content: default-off posture callout, 4-step recommended enable order (US-0062 → US-0041 → US-0112 → US-0111), runbook pointer line, zero-overhead-when-off contract paragraph. | AC-1 | A |
| **T-002** | Add 4 per-feature `#### US-xxxx` operator subsections nested under the umbrella, ordered US-id-ascending (US-0041 → US-0062 → US-0111 → US-0112). Each subsection: 1–3 sentence narrative (release-workflow angle for US-0111/US-0112), master enable flag + related keys with defaults, zero-overhead-when-off wording, runbook cross-link (existing anchor only — no duplication). US-0062 subsection cross-links to `## Project README coverage validation (US-0097 / DEC-0083)` (L171) with explanatory note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)". US-0041 subsection cross-links to `## Lifecycle QA matrix (US-0041)` (L2522). US-0111/US-0112 subsections include bidirectional "see US-0113 for sovereign-loop angle" pointers (mirror US-0113's "see US-0114" pointer convention per R-0101). | AC-2, AC-7 | A |
| **T-003** | Extend `### Full scratchpad reference (detailed)` (L1225) with `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block, as sibling to `### Sovereign-loop era keys` (L1242). Net-new key rows ONLY (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO` with defaults + flip guidance) + grouped cross-links to existing US-0054 publish controls (`RELEASE_PUBLISH_MODE` / `RELEASE_TARGETS_FILE` / `RELEASE_TARGETS_DEFAULT` — L541–547) and shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` (L1233/L1235) + cross-link pointers to US-0113's `### Sovereign-loop era keys` block for overlapping US-0111/US-0112 keys (`RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` / `DELIVERY_MODE` / `TOKEN_PROFILE` / `ID_NAMESPACE_BOOTSTRAP` / `MODEL_TIER`). No duplicate key rows. Default-off / zero-overhead-when-off wording per AC-3. | AC-3 | A |
| **T-004** | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy after T-001/T-002/T-003 complete). Re-run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). | AC-5 | B |
| **T-005** | Run validators (AC-4, AC-6) and fix any drift. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged (DC-1 + DC-2 out-of-scope). Note: working-tree `docs/product/backlog.md` encoding hygiene (185 stray `0xa7` bytes) must be restored by orchestrator before this gate can re-pass post-execute. `python scripts/validate_doc_profile.py` + `python scripts/check-user-visible-metadata.py` → expect PASS. Fix any narrative prose that leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. | AC-4, AC-6 | B |
| **T-006** | Run regression tests (AC-8) and confirm green. `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed (US-0114 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`). Confirm no test weakenings — if a test fails, the prose is wrong, not the test. | AC-8 | B |

### AC → task surjective map

| AC | Tasks |
|----|-------|
| AC-1 Umbrella section | T-001 |
| AC-2 Per-feature operator subsections | T-002 |
| AC-3 Full scratchpad reference extension | T-003 |
| AC-4 Coverage preserved | T-005 |
| AC-5 Framework README parity | T-004 |
| AC-6 Audience + metadata hygiene | T-005 |
| AC-7 Runbook cross-links per feature | T-002 |
| AC-8 Regression tests | T-006 |

**Surjectivity check**: AC-1..AC-8 all covered. **Total**: 6 task seeds ≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered.

## Test markers (existing — no new tests proposed)

| Marker | File | AC covered | Notes |
|--------|------|------------|-------|
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | Confirms `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.local.example.md` parity; US-0114 does not touch either file, so tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` must remain unchanged (DC-1 + DC-2 out-of-scope). |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** R-0102 confirmed no test weakenings; AC-8 is satisfied by existing tests remaining green. Adding new tests would violate the "no test weakenings" spirit (US-0114 is documentation-only; tests are read-only gates).

## Compose guards (non-negotiable — all UNCHANGED)

| Story | Compose rule |
|-------|--------------|
| **US-0091** | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners UNCHANGED — US-0114 appends narrative sections outside the catalog block. |
| **US-0097** | Project README parity surface UNCHANGED — US-0114 touches framework README pair only, not project README. (US-0062 cross-links here.) |
| **US-0017** | Framework README parity contract UNCHANGED — US-0114 preserves byte-parity via T-004 lockstep. |
| **US-0040** | Per-sprint release notes semantics UNCHANGED. |
| **US-0100** | Semantic changelog UNCHANGED. |
| **US-0101** | Catalog schema (DEC-0086) UNCHANGED. |
| **US-0102** | Role catalog precedence (DEC-0087) UNCHANGED. |
| **US-0103** | AI Decision Ledger schema/semantics UNCHANGED — documented only. |
| **US-0104** | Cross-Model Adversarial Critic schema/semantics UNCHANGED — documented only. |
| **US-0105** | Sovereign Memory schema/semantics UNCHANGED — documented only. |
| **US-0107** | Sovereign Loop Mode schema/semantics UNCHANGED — documented only. |
| **US-0108** | Parallel Instance Arbitrage schema/semantics UNCHANGED — documented only. |
| **US-0109** | Self-Healing Deploy Loop schema/semantics UNCHANGED — documented only. |
| **US-0110** | Goal-Based Convergence schema/semantics UNCHANGED — documented only. |
| **US-0111** | Release Trigger Adapters schema/semantics UNCHANGED — documented only (release-workflow angle owned by US-0114; sovereign-loop angle shipped in US-0113). |
| **US-0112** | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only (release-workflow angle owned by US-0114; sovereign-loop angle shipped in US-0113). |
| **US-0041** | End-to-End Lifecycle QA schema/semantics UNCHANGED — documented only (release-workflow angle). |
| **US-0062** | Installer-Owned `its_magic/` folder boundary (DEC-0045, amended by DEC-0083/US-0097) UNCHANGED — documented only. |

**18 guards UNCHANGED.** US-0114 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched).

## Carry-overs from research (resolution)

### (a) Missing `# US-0041` and `# US-0062` h1 anchors in `architecture.md` (DC-2)

**Decision: DEFER to US-0117** (phase & role governance family, which inherits DC-1 from US-0113 + DC-2 from US-0114 as architecture.md triad hygiene closure).

**Justification**:

- AC-7 only requires **runbook** cross-links, which exist for all 4 features (R-0102 § Per-feature sub-findings: US-0041 → L2522; US-0062 → L171 via US-0097/DEC-0083; US-0111/US-0112 → existing anchors). The missing `architecture.md` h1 anchors are NOT a US-0114 AC.
- US-0114 is scoped as a **framework README** documentation story (`its_magic/README.md` pair). The `architecture.md` h1 anchors are an internal engineering-docs surface, not an operator-facing README surface. Mixing the two would blur the story's vertical-slice boundary.
- US-0117 (phase & role governance family) is the natural owner: it already inherits DC-1 (5 missing h1 anchors for US-0103/0104/0105/0107/0110) from US-0113, and adding DC-2 (2 missing h1 anchors for US-0041/US-0062) fits its architecture-doc triad hygiene closure scope cleanly.
- Deferring keeps US-0114 at 6 task seeds (well under `SPRINT_MAX_TASKS=12`); adding T-007 would cross the story's vertical-slice boundary.
- Structurally parallel to US-0113's DC-1 deferral rationale (R-0101).

**Deferral note for orchestrator**: This is a **DC-2 deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions). Note for orchestrator: when US-0117 enters `plan` macro, its discovery should narrow-read this section and US-0113's carry-over (a), and add the 7 missing h1 anchors (5 from DC-1 + 2 from DC-2) as task seeds. Anchor format: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112` format).

### (b) Scratchpad reference extension — net-new keys + cross-link pointers only

**Decision: LOCK net-new keys + cross-link pointers** (per R-0102 open question #1 resolution).

**Justification**:

- US-0111's `RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` and US-0112's `DELIVERY_MODE` / `TOKEN_PROFILE` / `ID_NAMESPACE_BOOTSTRAP` / `MODEL_TIER` are **already present** in `its_magic/README.md` L1338–1358 inside `### Sovereign-loop era keys (US-0103–US-0112)` (L1242, shipped by US-0113/S0113).
- Re-documenting those 7 keys in a parallel `### Release & distribution keys` sub-block would (a) duplicate 7 keys, (b) risk byte-instability / divergence if defaults or wording drift between the two sub-blocks, and (c) violate US-0113's byte-stability contract on its sovereign-loop keys block.
- The net-new-only + cross-link-pointer approach preserves US-0113's byte-stability, avoids duplication, and gives operators a single canonical location per key (US-0113's block for US-0111/US-0112 overlap keys; US-0114's block for US-0062 net-new keys + grouped cross-links to US-0054/AUTO_INSTALL_DEPS/AUTO_RELEASE_NOTES).

## Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 overlap divergence** — US-0111/US-0112 overlap keys re-documented in US-0114's reference sub-block, drifting from US-0113's block | **MEDIUM→LOW** | LOCK net-new keys + cross-link pointers only (carry-over (b)); US-0114's `### Release & distribution keys` sub-block covers ONLY net-new keys (US-0062's `PROJECT_README_ENFORCE` / `FRAMEWORK_KIT_REPO`) + grouped cross-links to existing US-0054 publish controls + shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` + cross-link pointers to US-0113's block for overlapping US-0111/US-0112 keys. No duplicate key rows. US-0113's `### Sovereign-loop era keys` block byte-stability preserved. T-003 enforces; QA re-verifies. |
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). QA must re-verify both gates. Same mitigation as US-0113. |
| **AC-7 US-0062 anchor** — US-0062 has no dedicated runbook `## US-0062` h2 anchor; cross-link must target an existing anchor | **MEDIUM→LOW** | Cross-link to `## Project README coverage validation (US-0097 / DEC-0083)` (L171) with explanatory note "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)". This is the canonical active-anchor surface per DEC-0045 (declared) + DEC-0083 (amended). T-002 enforces; QA re-verifies. |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing | **LOW–MEDIUM** | US-0114 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| **AC-4 coverage drift** — catalog block accidentally reflowed OR working-tree backlog.md encoding regression blocks validator | **LOW** (catalog) / **MEDIUM** (encoding) | T-005 runs `validate_readme_feature_coverage.py --enforce`; `coverage_missing=["US-0117"]` must remain unchanged. Catalog block treated as read-only. **Encoding hygiene:** working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes (Windows-1252 corruption from untracked scripts per R-0102) — orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. Research phase is read-only on backlog.md. |
| **AC-6 metadata leakage** — internal IDs (DEC-xxxx/R-xxxx/reason-codes) leak into user-visible prose | **LOW** | T-005 runs `validate_doc_profile.py` + `check-user-visible-metadata.py`; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. US-0062's explanatory note is the only place a DEC id appears in prose — kept inside a parenthetical cross-link, not a user-visible sentence. |
| **Decomposition drift (US-0113 angle overlap)** — US-0111/US-0112 US-0114 subsections overlap confusingly with US-0113's subsections | **LOW** | US-0114 subsections include explicit "see US-0113 for sovereign-loop angle" pointers (T-002). US-0113 = sovereign-loop angle (shipped S0113); US-0114 = release-workflow angle. Bidirectional pointers already in US-0113's subsections (per R-0101). |

## Stop conditions

**stop_conditions_met=yes**:

- **No major tradeoff requires DEC** — confirmed (companion_dec=none; documentation-only; no architectural surface; R-0102 § Decision-gate check confirmed no DEC required).
- **No feasibility unknown** — R-0102 closed all 4 discovery open questions; architecture phase resolved both carry-overs (DC-2 defer to US-0117; scratchpad reference extension net-new + cross-link pointers only).
- **No data migration risk** — documentation-only; no schema, no data, no installer changes.

## Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. Both carry-overs resolved by tech-lead within the `plan` macro (defer DC-2 h1 anchors to US-0117; lock scratchpad reference extension = net-new keys + cross-link pointers). No sovereign-memory digest call needed (US-0114 documentation-only; existing digest context sufficient per R-0102).

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0114 documentation-only; existing digest context sufficient per R-0102). Sovereign-loop pattern identified for curator retrospective at segment close: "release & distribution family operator documentation follows US-0113's umbrella + per-feature subsection pattern, with net-new-keys-only + cross-link-pointer scratchpad reference extension to preserve byte-stability on the sibling era block." No write to `mistakes.jsonl` in architecture phase.

## Consequences

- Sprint: S0114 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 4 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 2 missing `architecture.md` h1 anchors (`# US-0041`, `# US-0062`) deferred to US-0117 (DC-2, parallel to US-0113's DC-1 — 5 anchors).
- No new tests; no new DECs; no compose-surface changes.

## Evidence references

- `docs/product/backlog.md` — `## US-0114` block (lines 3911–3927)
- `docs/engineering/research.md` — `R-0102` (delivered 2026-07-04T02:45:40Z, 4/4 open questions closed)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — release & distribution keys (L200–209 RELEASE_PUBLISH_MODE/RELEASE_TARGETS_*, L258–267 PROJECT_README_ENFORCE/FRAMEWORK_KIT_REPO, L529–539 RELEASE_TRIGGER_*, L66–67 AUTO_INSTALL_DEPS/AUTO_RELEASE_NOTES, L181–186 DELIVERY_MODE/TOKEN_PROFILE/ID_NAMESPACE_BOOTSTRAP) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L940 (`### Sovereign-loop era` US-0113 sibling umbrella); L1225 (`### Full scratchpad reference (detailed)`) extension target; L1242 (`### Sovereign-loop era keys` US-0113 sibling block — byte-stability preserved)
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717) exist; `# US-0041` and `# US-0062` missing (deferred to US-0117 as DC-2)
- `docs/engineering/decisions.md` — DEC-0045 (US-0062 installer-owned boundary), DEC-0083 (US-0097 amends DEC-0045), DEC-0111 (US-0111), DEC-0112 (US-0112) — referenced, not amended



## US-0115 — Integration & observability operator documentation in framework README

### Overview

**US-0115** is a documentation-only story closing the operator-documentation gap for the **integration & observability** functional family — US-0034 (Cross-repo compatibility observability), US-0084 (Codebase map freshness gate), US-0086 (Handoff hygiene validator), US-0093 (Scratchpad drift detector), US-0096 (Active context handoff), US-0101 (Model tier resolution), US-0102 (Role-based model catalog). It adds an umbrella `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` under `## Commands and workflow` (L350) in `its_magic/README.md`, as a sibling to US-0113's `### Sovereign-loop era (US-0103–US-0112) umbrella section` (L940) and US-0114's `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112) umbrella section` (L1225). The umbrella carries 7 nested per-feature `#### US-xxxx` operator subsections ordered US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102), with bidirectional `see US-0114 for installer-payload angle` pointers in the US-0101/US-0102 subsections (angle-distinct narrative contract — US-0115 owns resolver mechanics + role catalog; US-0114 owns installer payload US-0112 presets). A matching `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block is appended to `### Full scratchpad reference (detailed)` (L1410) as a sibling to `### Sovereign-loop era keys (US-0103–US-0112)` (L1427) and `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` (L1551), covering **net-new** keys only (US-0034 `CROSS_REPO_OBSERVABILITY` family, US-0096 `LEAN_MEMORY_*` family + `AUTO_DELIVERY_ROUTING`, US-0101 5 resolver keys, US-0102 `MODEL_SLUG_<PHASE_ID>`) + cross-link pointer to US-0114's block for the `DELIVERY_MODE` overlap + grouped cross-link to the main reference list above L1410 for US-0086's `REMOTE_EXECUTION` family + reason-code-only entries for US-0084 (`INSTALL_MANIFEST_ERROR`) / US-0093 (`SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT`). The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0115 is documentation-only; no architectural, policy, or schema surface is being changed; R-0103 § Decision-gate check confirmed no DEC required — mirrors US-0113 / US-0114 sibling precedent). **Research anchor**: **R-0103** (delivered 2026-07-04T07:53:00Z, 6/6 open questions closed). **Compose guards (non-negotiable, 23 — UNCHANGED, cumulative across all prior stories)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0115-architecture-20260704T080200Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-04T08:02:00Z
**Verdict**: PASS
**Next**: `/sprint-plan`

### Companion DEC

**companion_dec = none**. US-0115 is documentation-only (mirrors US-0113 / US-0114 sibling precedent). No architectural, policy, or schema surface is being changed. Grep for `^## DEC-` in `docs/engineering/decisions.md` confirmed no US-0115 companion DEC is required and none was proposed in R-0103 § Decision-gate check. The DC-3 deferral (7 missing `# US-xxxx` h1 anchors) is a triad-hygiene carry-over to US-0117, not a tradeoff requiring a DEC.

### Approach locked — A1

**A1: Single `### Integration & observability` umbrella + 7 nested `#### US-xxxx` subsections (h4 under h3 umbrella), sibling to US-0113's `### Sovereign-loop era` (L940) and US-0114's `### Release & distribution` (L1225) umbrellas, inserted immediately after the closing of US-0114's umbrella block (before L1410 `### Full scratchpad reference (detailed)`).**

**Justification**:
- **Consistency with prior stories** — US-0113 established the umbrella+subsection shape for the sovereign-loop family; US-0114 mirrored it for the release & distribution family; US-0115 mirrors it for the integration & observability family. Three sibling umbrellas in release order (US-0113 → US-0114 → US-0115) under `## Commands and workflow` form a clean triad.
- **Design challenge: alternatives considered.**
  - **A2 (rejected):** 7 separate top-level `### US-xxxx` h3 sections scattered under `## Commands and workflow` rather than grouped under an umbrella. Rejected: breaks the family-grouping precedent set by US-0113/US-0114, hurts operator discoverability (no single entry point for the integration & observability family), and complicates the AC-1 acceptance criterion which explicitly requires an umbrella section.
  - **A3 (rejected):** Reuse US-0034's existing L585 `### Optional cross-repo observability (US-0034)` h3 as the umbrella and nest the other 6 features under it. Rejected: US-0034 is one feature among seven; elevating it to umbrella-holder conflates a feature section with a family section, breaks byte-stability of the pre-US-0115 L585 block, and breaks the family-parity contract (US-0113/US-0114 each have a dedicated umbrella header).
  - **A1 is the only viable option** that satisfies AC-1 (umbrella section), preserves US-0113/US-0114 sibling consistency, and respects byte-stability of prior released blocks. Lock A1.

### Files to touch

- `its_magic/README.md` — APPEND umbrella `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` (after US-0114 umbrella close, before L1410) + 7 nested `#### US-xxxx` operator subsections (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102) + `### Integration & observability keys` sub-block under `### Full scratchpad reference (detailed)` (after US-0114's `### Release & distribution keys` block at L1551) covering net-new keys + cross-link pointers + reason-code-only entries.
- `template/its_magic/README.md` — byte-identical sync via one-way copy from `its_magic/README.md` (AC-5).

### Files NOT to touch

- `.cursor/scratchpad.md` — canonical scratchpad; US-0115 documents keys in README, never edits the canonical source.
- `docs/product/backlog.md` — status authority (US-0045); encoding hygiene prerequisite flagged separately to orchestrator.
- `docs/engineering/runbook.md` — AC-7 cross-links only (all 7 anchors pre-exist); no new runbook content.
- `docs/developer/README.md` — US-0097 compose guard.
- `docs/engineering/architecture.md` — other than this US-0115 anchor append; DC-3 (7 missing h1 anchors) deferred to US-0117.
- `installer.py` / `installer.ps1` / `installer.sh`, `scripts/*`, any test file — out of scope (documentation-only story).
- **Do NOT modify US-0113's `### Sovereign-loop era` / `### Sovereign-loop era keys` blocks (L940 / L1427) or US-0114's `### Release & distribution` / `### Release & distribution keys` blocks (L1225 / L1551)** in `its_magic/README.md` — byte-stability contract (both already released in S0113 / S0114). US-0115 adds cross-link pointers to these blocks from its own net-new block; it never edits them. Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks).

### Sprint seeds (T-001..T-006)

6 tasks within `SPRINT_MAX_TASKS=12` (mirror US-0113 / US-0114 sibling pattern; `SPRINT_AUTO_SPLIT` not triggered):

| Task | Description | ACs covered |
|------|-------------|-------------|
| **T-001** | Add umbrella `### Integration & observability (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102) umbrella section` under `## Commands and workflow` (after US-0114 umbrella close, before L1410). Default-off framing for optional features (US-0034 / US-0096 / US-0101 / US-0102) + always-on framing for publish/QA guards (US-0084 / US-0086 / US-0093). 7-step enable order (US-0034 → US-0096 → US-0101 → US-0102 → US-0084 → US-0086 → US-0093) + runbook pointer line. | AC-1 |
| **T-002** | Add 7 per-feature `#### US-xxxx` operator subsections under the umbrella, ordered US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102). US-0034 = cross-link only to existing L585 README section (byte-stability) + runbook cross-link to L1167. US-0096 = **net-new narrative** (R-0103 CORRECTION: no pre-existing L591 README section — L591 is a runbook line) + runbook cross-link to L591. US-0101/US-0102 = bidirectional "see US-0114 for installer-payload angle" pointers (angle-distinct narrative contract). US-0084/US-0086/US-0093 = reason codes + runbook cross-links (no scratchpad key blocks). Runbook cross-links per feature: US-0034 → L1167 h2; US-0084 → L1441/L1459 h3; US-0086 → L1398/L1471 h3; US-0093 → L1999 h3 (parent h2 = US-0065 runtime QA autopilot contract L1486); US-0096 → L591 h3; US-0101 → L653 h2; US-0102 → L771 h2. | AC-2, AC-7 |
| **T-003** | Add `### Integration & observability keys (US-0034 / US-0084 / US-0086 / US-0093 / US-0096 / US-0101 / US-0102)` sub-block under `### Full scratchpad reference (detailed)` (after US-0114's `### Release & distribution keys` block L1551). Net-new key rows only: US-0034 `CROSS_REPO_OBSERVABILITY` / `COMPATIBILITY_GATE_ON_CRITICAL` / `COMPATIBILITY_SOURCES`; US-0096 `LEAN_MEMORY_READ` / `LEAN_MEMORY_WRITE` / `LEAN_COLD_READ_MAX_SECTIONS` / `LEAN_STATE_INDEX_ROWS` / `AUTO_DELIVERY_ROUTING`; US-0101 `MODEL_TIER_DEFAULT` / `MODEL_CATALOG` / `MODEL_RESOLVE` / `MODEL_FALLBACK` / `MODEL_PROVIDER_MODE`; US-0102 `MODEL_SLUG_<PHASE_ID>` (with composition-on-US-0101 note). Cross-link pointers: `DELIVERY_MODE` → US-0114's block (US-0114 owns that row); US-0086 `REMOTE_EXECUTION` family → grouped cross-link to main reference list above L1410 (mirrors US-0114's `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` grouped cross-link pattern). Reason-code-only entries for US-0084 (`INSTALL_MANIFEST_ERROR`) / US-0093 (`SCRATCHPAD_HEADER_DRIFT` / `BACKLOG_STATUS_DRIFT`) + runbook cross-links. No duplicate key rows. Byte-stability of US-0113's L1427 + US-0114's L1551 blocks preserved (net-new-keys-only + cross-link-pointer shape). | AC-3 |
| **T-004** | Sync `template/its_magic/README.md` byte-identical via one-way copy from `its_magic/README.md`. Re-run `python -c "a=open(r'its_magic/README.md','rb').read(); b=open(r'template/its_magic/README.md','rb').read(); print('PARITY_OK' if a==b else 'PARITY_DIFF')"` (expect `PARITY_OK`) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`). | AC-5 |
| **T-005** | Run validators: `python scripts/validate_readme_feature_coverage.py --enforce` (expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 — catalog block read-only) + `python scripts/validate_doc_profile.py` (expect `[DOC_PROFILE_VALIDATE_OK]`) + `python scripts/check-user-visible-metadata.py` (expect exit 0; US-IDs only in parenthetical catalog tags). | AC-4, AC-6 |
| **T-006** | Run regression tests: `python -m pytest tests/scratchpad_example_parity_test.py -q` (expect 4/4 PASS). **Forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` — if a test fails, the prose is wrong, not the test (fix prose, never relax test). | AC-8 |

**Execution order**: T-001 (umbrella) → T-002 (7 subsections) → T-003 (scratchpad ref extension) → T-004 (template byte-sync) → T-005 (validators) → T-006 (regression tests). Acyclic, mirrors US-0113/US-0114.

### Test markers

Same 5 as US-0113 / US-0114 (no new tests proposed):

1. `tests/scratchpad_example_parity_test.py` — 4 markers (AC-5 indirect via scratchpad canonical parity, AC-8).
2. `scripts/validate_readme_feature_coverage.py --enforce` — AC-4.
3. `scripts/check_intake_template_parity.py` — AC-5.
4. `scripts/validate_doc_profile.py` — AC-6.
5. `scripts/check-user-visible-metadata.py` — AC-6.

### Compose guards (UNCHANGED — 23 guards, cumulative)

US-0115 is documentation-only and lives entirely outside the compose surface. The 23 compose guards (cumulative across all prior stories — US-0113 carried 18, US-0114 carried 18, US-0115 adds 5 family-internal guards to the documentation-only list for completeness: US-0034, US-0084, US-0086, US-0093, US-0096) remain UNCHANGED:

US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062.

### Stop conditions

**stop_conditions_met=yes**:

- **No DEC required** — confirmed (companion_dec=none; documentation-only; mirrors US-0113 / US-0114 sibling precedent; R-0103 § Decision-gate check confirmed no DEC candidate).
- **No feasibility unknown** — R-0103 closed all 6 discovery open questions (split resolution on US-0034/US-0096 narrative shape; net-new keys + cross-link pointers LOCKED for AC-3; reason-code-only entries for US-0084/US-0093; US-0086 grouped cross-link; US-0093 runbook anchor h-level CONFIRMED = h3; DC-3 deferred to US-0117).
- **No data migration risk** — documentation-only; no schema, no data, no installer, no scratchpad canonical changes.

### DC-3 resolution (deferred to US-0117)

**DC-3**: 7 missing `# US-xxxx` h1 anchors in active `docs/engineering/architecture.md` for the US-0115 family — `# US-0034`, `# US-0084`, `# US-0086`, `# US-0093`, `# US-0096`, `# US-0101`, `# US-0102`. Grep for `^# US-(0034|0084|0086|0093|0096|0101|0102)` in `docs/engineering/architecture.md` returned no matches (confirmed in R-0103 § Discovery open question #6 resolution). Not a US-0115 blocker — AC-7 is satisfiable via runbook cross-links (all 7 features have existing verified runbook anchors). US-0117 (Phase & role governance family) inherits DC-1 (5 anchors from US-0113: US-0103/0104/0105/0107/0110) + DC-2 (2 anchors from US-0114: US-0041/US-0062) + DC-3 (7 anchors from US-0115) = **14 total missing h1 anchors** as architecture.md triad hygiene closure.

**Deferral note for orchestrator**: This is a **deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions — segment-boundary advance hook handles it, not phase boundaries). `/architecture` documents the deferral in this findings block; does NOT add the h1 anchors. When US-0117 enters `plan` macro, its discovery should narrow-read this section and add the 7 missing h1 anchors as a task seed. Anchor format to use at that time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112`, `# US-0113`, `# US-0114` format).

### Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-3 byte-stability (3rd-story cumulative surface)** — US-0115 is the third story to extend `### Full scratchpad reference`; cumulative surface now covers 2 prior released blocks (US-0113 L1427 + US-0114 L1551). Risk of accidentally editing a prior released block. | **MEDIUM** | Net-new-keys-only + cross-link-pointer shape LOCKED in `/architecture` (T-003). Execute-phase must verify `git diff HEAD -- its_magic/README.md` shows pure addition in the post-L1551 range (no removals/modifications to US-0113's L1427 or US-0114's L1551 blocks). QA re-verifies. Mirrors S0114 retrospective pattern. |
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa). | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must re-run byte-parity check + `check_intake_template_parity.py`. QA re-verifies both gates. |
| **AC-2 US-0096 net-new narrative (R-0103 CORRECTION)** — Discovery handoff claimed "L591 `### Delivery modes` in README"; R-0103 confirmed L591 is a **runbook** line, not a README line. No pre-existing US-0096 README narrative section. | **LOW–MEDIUM** | `#### US-0096` subsection is net-new narrative (no byte-stability risk — no prior README section to preserve) + runbook cross-link to L591. Architecture locks the correction; execute-phase T-002 follows it. |
| **AC-2 US-0101/US-0102 angle overlap with US-0114** — US-0101/US-0102 model-tier-resolution + role-catalog angle owned by US-0115 vs US-0114's US-0112 installer-payload angle. | **MEDIUM→LOW** | Bidirectional "see US-0114 for installer-payload angle" pointers in US-0101/US-0102 subsections (T-002). US-0115 owns resolver mechanics + role catalog (DEC-0086 / DEC-0087); US-0114 owns installer payload (US-0112 presets). Angle boundary explicit. |
| **AC-3 `DELIVERY_MODE` overlap** — US-0114's `### Release & distribution keys` block (L1551) references `DELIVERY_MODE` from the release-workflow angle; US-0096 is in US-0115's family. | **MEDIUM→LOW** | Cross-link pointer to US-0114's block; US-0115 does NOT re-document `DELIVERY_MODE` defaults; US-0114 owns that row. |
| **AC-7 runbook cross-links** — 7 features, all anchors pre-exist (unlike US-0114's US-0062 gap which required an explanatory note). US-0093 h-level CONFIRMED = h3 (parent h2 = US-0065 runtime QA autopilot contract L1486). | **LOW** | All 7 anchors verified in R-0103: US-0034 L1167 h2; US-0084 L1441/L1459 h3; US-0086 L1398/L1471 h3; US-0093 L1999 h3; US-0096 L591 h3; US-0101 L653 h2; US-0102 L771 h2. |
| **AC-4 encoding hygiene prerequisite (carried from US-0114)** — Working-tree `docs/product/backlog.md` has 185 stray `0xa7` (§) bytes per R-0102. Orchestrator must restore encoding hygiene before execute so AC-4 can be re-verified post-execute. | **MEDIUM (carried)** | `/architecture` makes no backlog.md edits. Flag to orchestrator: restore backlog.md encoding hygiene before execute. NOT a US-0115 blocker (research was read-only on backlog.md; architecture is read-only on backlog.md). |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing. | **LOW–MEDIUM** | US-0115 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, fix prose, never relax test. T-006 confirms green. |
| **AC-1 umbrella placement** — Risk of inserting the umbrella inside US-0114's block rather than after it. | **LOW** | Insert after US-0114 umbrella close (before L1410 `### Full scratchpad reference`), NOT inside it. Mirrors US-0114-after-US-0113 placement pattern. |
| **Decomposition drift** — Drain mutex (US-0115 ships first; US-0116/US-0117 pick up other families). US-0101/US-0102 angle overlap with US-0114 is the only intentional cross-story overlap. | **LOW** | Bounded by angle-distinct narrative contract; bidirectional pointers (T-002). |

### Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. All 6 R-0103 carry-overs resolved by tech-lead within the `plan` macro:

1. Umbrella placement confirmed — after US-0114 umbrella close, before L1410.
2. Scratchpad reference extension placement confirmed — after US-0114's `### Release & distribution keys` block (L1551).
3. 7 per-feature subsection ordering confirmed — US-id-ascending (US-0034 → US-0084 → US-0086 → US-0093 → US-0096 → US-0101 → US-0102).
4. US-0034 cross-link-only shape confirmed (research recommendation (a) — cross-link to existing L585 README section, byte-stability preserved).
5. US-0096 net-new narrative shape confirmed (R-0103 CORRECTION — no pre-existing L591 README section; `#### US-0096` is net-new narrative + runbook cross-link to L591).
6. Bidirectional "see US-0114 for installer-payload angle" pointer convention confirmed in US-0101/US-0102 subsections.
7. DC-3 deferral confirmed — 7 missing h1 anchors deferred to US-0117 (US-0117 inherits 14 total).
8. Working-tree backlog.md encoding hygiene regression flagged to orchestrator for execute coordination.
9. Angle boundary for US-0101/US-0102 vs US-0114's US-0112 confirmed — US-0115 owns resolver mechanics + role catalog (DEC-0086 / DEC-0087); US-0114 owns installer payload (US-0112 presets).
10. `#### US-0084` / `#### US-0093` subsections document reason codes + runbook cross-links only (no scratchpad key blocks).

No sovereign-memory digest call needed (US-0115 is documentation-only; existing digest context sufficient per R-0103). Verdict: **PASS**.

### Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0115 documentation-only; existing digest context sufficient per R-0103). Sovereign-loop pattern for curator retrospective at segment close: "integration & observability family operator documentation completes the US-0113/US-0114/US-0115 umbrella triad under `## Commands and workflow`; cross-story byte-stability contract now covers **two** prior released blocks (US-0113 L1427 + US-0114 L1551) — net-new-keys-only + cross-link-pointer shape is the established triad-closure pattern." No write to `mistakes.jsonl` in architecture phase.

### Consequences

- Sprint: S0115 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 7 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 7 missing `architecture.md` h1 anchors deferred to US-0117 (DC-3, parallel to US-0113's DC-1 — 5 anchors — and US-0114's DC-2 — 2 anchors; US-0117 inherits 14 total).
- No new tests; no new DECs; no compose-surface changes.

### Evidence references

- `docs/product/backlog.md` — `## US-0115` block (lines 3929–3945, 8 ACs)
- `docs/engineering/research.md` — `R-0103` (delivered 2026-07-04T07:53:00Z, 6/6 open questions closed; 7 per-feature sub-findings)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — integration & observability keys (L156–161 TOKEN_PROFILE, L181–186 DELIVERY_MODE/LEAN_MEMORY_*, L221–228 CROSS_REPO_OBSERVABILITY family, L230–234 COMPONENT_SCOPE, L355–374 MODEL_TIER/MODEL_CATALOG/MODEL_RESOLVE/MODEL_SLUG) — canonical source for AC-3 extension (net-new + cross-links)
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L585 (`### Optional cross-repo observability (US-0034)` — existing US-0034 section, cross-link target for US-0034 subsection); L940 (`### Sovereign-loop era` US-0113 sibling umbrella); L1225 (`### Release & distribution` US-0114 sibling umbrella); L1410 (`### Full scratchpad reference (detailed)`) extension target; L1427 (`### Sovereign-loop era keys` US-0113 sibling block — byte-stability preserved); L1551 (`### Release & distribution keys` US-0114 sibling block — byte-stability preserved)
- `docs/engineering/runbook.md` — 7 anchors: US-0034 L1167 h2; US-0084 L1441/L1459 h3; US-0086 L1398/L1471 h3; US-0093 L1999 h3 (parent h2 = US-0065 runtime QA autopilot contract L1486); US-0096 L591 h3; US-0101 L653 h2; US-0102 L771 h2
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0111` (L335), `# US-0112` (L454), `# US-0113` (L717), `# US-0114` (L914) exist; `# US-0034`/`# US-0084`/`# US-0086`/`# US-0093`/`# US-0096`/`# US-0101`/`# US-0102` missing (deferred to US-0117 as DC-3)
- `docs/engineering/decisions.md` — DEC-0082 (US-0096 delivery modes), DEC-0086 (US-0101 per-phase model tier), DEC-0087 (US-0102 role-based model catalog), DEC-0045 (US-0062 installer-owned boundary, referenced via US-0084 publish guard), DEC-0047 (US-0065 runtime QA autopilot contract, referenced via US-0093) — referenced, not amended; no US-0115 companion DEC

---

