# Architecture archive pack (2026-08-24)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 50
- First archived heading: `# BUG-0014 — README Catalog Coverage Backfill (sovereign-loop era features + release_notes legacy pointer)`
- Last archived heading: `# US-0113 — Sovereign-loop operator documentation in framework README`
- Verification tuple (mandatory):
  - archived_body_lines=267
  - preamble_lines=1
  - retained_body_lines=2953

---

# BUG-0014 — README Catalog Coverage Backfill (sovereign-loop era features + release_notes legacy pointer)

## Overview

**BUG-0014** is a documentation-coverage defect — sovereign-loop era features (US-0103..US-0112, BUG-0013) were released between 2026-06-28 and 2026-07-02 without being added to the README feature coverage catalog surfaces. Additionally, `handoffs/release_notes.md` is missing finalized-note entries for 5 sprints (S0103, S0104, S0105, S0106, S0108). The validator `validate_readme_feature_coverage.py --enforce` reports 117 missing coverage rows — full backfill required.

**Research anchor**: **R-0100** (delivered 2026-07-03T17:35:00Z, Q1–Q6 closed). **Companion DEC: none** (documentation-only, no architectural surface changed). **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

## Fix approach (locked)

1. **(A1) Full catalog backfill**: Add 125 catalog rows (112 US + 13 BUG) to BOTH `its_magic/README.md` (root H2 sections) and `docs/developer/README.md` (dev H2 sections). Row format: `its_magic/README.md` uses bullet with item_id mention (e.g. `/slug description **US-xxxx**`); `docs/developer/README.md` uses bold item_id or traceability line (e.g. `**US-xxxx** description`).
2. **(A2) Template parity sync**: After catalog edits to `its_magic/README.md`, byte-copy to `template/its_magic/README.md` to satisfy parity check.
3. **(A3) Release notes backfill**: Add 5 finalized-note entries to `handoffs/release_notes.md` (S0103, S0104, S0105, S0106, S0108), following existing S0107/S0109–S0112 format.

## Files to touch

| File | Action | Notes |
|---|---|---|
| `its_magic/README.md` | backfill 125 catalog rows | US-0001..US-0112 + BUG-0001..BUG-0013 in root H2 sections |
| `docs/developer/README.md` | backfill same 125 catalog rows | US-0001..US-0112 + BUG-0001..BUG-0013 in dev H2 sections |
| `template/its_magic/README.md` | byte-copy from `its_magic/README.md` | after catalog edits (parity check) |
| `handoffs/release_notes.md` | add 5 finalized-note entries | S0103, S0104, S0105, S0106, S0108 (follow S0107/S0109–S0112 format) |

## Files NOT to touch

- All compose guards: US-0091, US-0097, US-0040, US-0100, US-0101, US-0102, US-0103..US-0112 (UNCHANGED)
- All scripts (`scripts/validate_readme_feature_coverage.py`, `scripts/readme_feature_coverage_lib.py`, etc.)
- All installer files (`installer.py`, `installer.ps1`, `installer.sh`)
- All sovereign-loop scripts and Python/PowerShell/Shell files

## Sprint task seeds (4 tasks; default `SPRINT_MAX_TASKS=12`)

- **T-001** — Backfill `its_magic/README.md` with 125 catalog rows (US-0001..US-0112 + BUG-0001..BUG-0013) in appropriate H2 sections. Row format per R-0100 Q4.
- **T-002** — Backfill `docs/developer/README.md` with same 125 catalog rows in dev H2 sections. Bold item_id or traceability line format.
- **T-003** — Sync `template/its_magic/README.md` from `its_magic/README.md` (byte-identical copy after edits).
- **T-004** — Add 5 missing release notes entries to `handoffs/release_notes.md` (S0103, S0104, S0105, S0106, S0108).

## Test markers (3 minimum)

- `test_bug0014_readme_catalog_backfill` — verify `validate_readme_feature_coverage.py --enforce` returns `[README_FEATURE_COVERAGE_VALIDATE_OK]` after T-001/T-002.
- `test_bug0014_template_parity` — verify `template/its_magic/README.md` matches `its_magic/README.md` after T-003.
- `test_bug0014_release_notes` — verify 5 entries present in `handoffs/release_notes.md` after T-004.

## Compose-guards confirmation

**16 guards UNCHANGED**: US-0091, US-0097, US-0040, US-0100, US-0101, US-0102, US-0103, US-0104, US-0105, US-0106, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112. This bug lives entirely outside the compose surface (documentation-only, no code/scripts/installers touched).

## Risks

- **R1 (MEDIUM)**: Full 125-row backfill is large but bounded. Mitigate with deterministic row template per R-0100 Q4/Q5, peer-review traceability before `/qa`.
- **R2 (LOW)**: Template copy of `its_magic/README.md` must be refreshed AFTER catalog edits. Mitigate with explicit step ordering in sprint (T-003 after T-001).
- **R3 (INFO)**: Backlog parser does not recognize DONE/user_visible fields for US-0103..US-0110 (parser-normalization debt tracked separately). Mitigate by adding catalog rows preemptively for those 8 US items.

## Evidence references

- `docs/product/backlog.md` — `### BUG-0014` (lines 4168–4182, discovery + research + architecture notes)
- `docs/engineering/research.md` — `R-0100` (delivered, Q1–Q6 closed)
- `docs/engineering/architecture.md` — this `# BUG-0014` section
- `docs/engineering/state.md` — architecture checkpoint (this phase)
- `handoffs/resume_brief.md` — next-phase pointer to `/sprint-plan`
- `handoffs/release_notes.md` — 5 entries to be added at `/execute`
- `its_magic/README.md` lines 65–88 — 125 rows to be added at `/execute`
- `docs/developer/README.md` — 125 rows to be added at `/execute`

## Stop condition

**PASS** — no major tradeoff requires DEC; no feasibility unknown; no data migration risk. Per R-0100 Q6, no DEC required. Handoff to `/sprint-plan` (tech-lead, fresh subagent spawn).

---

# US-0113 — Sovereign-loop operator documentation in framework README

## Overview

**US-0113** is a documentation-only story closing the operator-documentation gap for the sovereign-loop era feature set (US-0103..US-0112, excluding US-0106 which belongs to the US-0117 family). It adds an umbrella `### Sovereign-loop era (US-0103–US-0112)` narrative section under `## Commands and workflow` in `its_magic/README.md`, with 9 nested per-feature `####` operator subsections, plus a matching extension of the `### Full scratchpad reference (detailed)` section with sovereign-loop keys grouped by feature. The framework README pair (`its_magic/README.md` ↔ `template/its_magic/README.md`) is kept byte-identical via one-way copy. No code, schema, installer, scratchpad canonical, or runbook content changes.

**Binding decision**: **companion_dec=none** (US-0113 is documentation-only; no architectural, policy, or schema surface is being changed; R-0101 Q-scope resolved as docs backfill only). **Research anchor**: **R-0101** (delivered 2026-07-04T00:47:30Z, 3/3 open questions closed). **Compose guards (non-negotiable)**: DO NOT amend US-0091, US-0097, US-0017, US-0040, US-0100, US-0101, US-0102, US-0103..US-0112. **Status authority**: **OPEN** per **US-0045** (closure at `/release`).

**Fresh context marker**: `tl-US0113-architecture-20260703T232718Z-fresh`
**Orchestrator run id**: `auto-20260704-01`
**Timestamp**: 2026-07-03T23:27:18Z
**Verdict**: PASS
**Next**: `/sprint-plan`

## Companion DEC

**companion_dec=none**. Confirmed (not overriding research R-0101). Justification:

- US-0113 introduces **no** new architectural surface — no schema, no code path, no installer classification, no policy, no precedence rule, no role matrix change.
- The "operator-documentation gap closing" pattern is a recurring documentation-only pattern already established by BUG-0013 / BUG-0014 (both shipped with `companion_dec=none` per R-0099 / R-0100). US-0113 follows the same precedent.
- The 3 discovery open questions were all resolved within the `plan` macro as docs backfill decisions (R-0101 § open_questions_resolution); none required operator input or a tradeoff record.
- Next available DEC id would be `DEC-0113` (highest existing is `DEC-0112` in `decisions/DEC-0112.md`); reserving it would be wasteful since there is no decision surface to record.

## Approach locked

**approach_locked=A1** — Single umbrella `### Sovereign-loop era (US-0103–US-0112)` section with 9 nested `#### US-xxxx` subsections (h4 under h3 umbrella), placed under `## Commands and workflow` (L350), before `### Full scratchpad reference (detailed)` (L940).

### Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | Single umbrella `### Sovereign-loop era (US-0103–US-0112)` + 9 nested `#### US-xxxx` subsections (h4 under h3) | **Locked** — preferred for navigation; matches existing README hierarchy pattern (umbrella → per-feature detail); preserves AC-2 "per-feature operator subsections" wording naturally; keeps the 9 features visually grouped as an era rather than scattered across `## Commands and workflow`. |
| **A2** | Flat 9 `#### US-xxxx` subsections directly under `## Commands and workflow` with cross-links but no umbrella | **Rejected** — loses era grouping; scatters sovereign-loop features among unrelated workflow subsections; weakens AC-1 (umbrella section is an explicit AC); harder for operators to discover the sovereign-loop feature cluster. |
| **A3** | Place umbrella under `## Features (what its-magic can do)` instead of `## Commands and workflow` | **Rejected** — `## Features` already has the US-0091 catalog one-liners (L63 anchor, L1235–L1243); AC-1 explicitly requires the umbrella under `## Commands and workflow`; narrative operator guides are workflow-shaped, not catalog-shaped. |

## Files to touch

| File | Action | Notes |
|---|---|---|
| `its_magic/README.md` | append umbrella + 9 subsections under `## Commands and workflow`; extend `### Full scratchpad reference (detailed)` | AC-1, AC-2, AC-3; catalog block L63 + L1235–L1243 treated as read-only (AC-4) |
| `template/its_magic/README.md` | one-way byte-sync copy from `its_magic/README.md` after edits | AC-5 lockstep; `cmd /c fc /b` + `check_intake_template_parity.py` re-run required |

**Explicitly NOT touched** (decision):

- `docs/engineering/architecture.md` — the 5 missing `# US-xxxx` h1 anchors (US-0103/0104/0105/0107/0110) are **deferred to US-0117** (phase & role governance family), not added in US-0113. See carry-over (a) below. The only architecture.md edit in this phase is the append of this `## US-0113` section (the architecture anchor for US-0113 itself).
- `docs/developer/README.md` — research R-0101 did not identify this as a touch target. AC-6 (audience + metadata hygiene) is a **validator gate**, not an edit mandate; US-0113 narrative subsections live in the framework README pair only. The developer README is a separate audience surface owned by US-0097 (project README parity) compose guard.

## Files NOT to touch

- `.cursor/scratchpad.md` — canonical source of truth (never edit in docs stories; BUG-0013 precedent).
- `template/.cursor/scratchpad.local.example.md` — canonical example (BUG-0013 ownership; US-0113 does not extend the scratchpad canonical, only documents existing keys in README).
- `docs/product/backlog.md` — status authority (closure only at `/release`).
- `docs/engineering/runbook.md` — AC-7 cross-links only; **no new runbook content** (AC-7 forbids duplication). All 9 runbook anchors already exist (R-0101 § runbook cross-link targets).
- `docs/developer/README.md` — separate audience surface; not in US-0113 scope (see above).
- `docs/engineering/architecture.md` (other than this `## US-0113` append) — 5 missing feature h1 anchors deferred to US-0117.
- `installer.py`, `installer.ps1`, `installer.sh` — no installer changes (US-0008/US-0018/US-0057/US-0075 compose guards).
- All scripts (`scripts/validate_readme_feature_coverage.py`, `scripts/check_intake_template_parity.py`, `scripts/validate_doc_profile.py`, `scripts/check-user-visible-metadata.py`, etc.) — validators are read-only gates, not edit targets.
- All sovereign-loop scripts and Python/PowerShell/Shell files — US-0103..US-0112 features are **documented only**, not amended.

## Sprint seeds (T-001..T-006)

**6 task seeds** (≤ `SPRINT_MAX_TASKS=12` — `SPRINT_AUTO_SPLIT` not triggered).

| ID | Title | AC | Tranche |
|----|-------|----|:---------|:---------|
| **T-001** | Add `### Sovereign-loop era (US-0103–US-0112)` umbrella section under `## Commands and workflow` (L350), before `### Full scratchpad reference` (L940). Content: default-off posture callout, 9-step recommended enable order (AI_DECISION_LEDGER → SOVEREIGN_MEMORY → CROSS_MODEL_REVIEW → SOVEREIGN_GOAL_MODE=goal_convergence → AUTO_SOVEREIGN → SOVEREIGN_PARALLEL_DEV → AUTO_SOVEREIGN_SELF_HEALING_DEPLOY → RELEASE_TRIGGER_SOURCE → US-0112 presets), runbook pointer, zero-overhead-when-off contract paragraph. | AC-1 | A |
| **T-002** | Add 9 per-feature `#### US-xxxx` operator subsections nested under the umbrella, ordered US-id-ascending (US-0103 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0110 → US-0111 → US-0112). Each subsection: 1–3 sentence narrative (sovereign-loop angle for US-0111/US-0112), master enable flag + related keys with defaults, zero-overhead-when-off wording, runbook cross-link (existing anchor only — no duplication). US-0112 subsection references existing delivery/catalog keys (no new scratchpad block). US-0111/US-0112 subsections include "see US-0114 for release-workflow operator docs on this feature" pointers. | AC-2, AC-7 | A |
| **T-003** | Extend `### Full scratchpad reference (detailed)` (L940) with sovereign-loop keys. Ordering: **mirror `.cursor/scratchpad.md` L388–539 canonical ordering** (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending. 9 sub-sub-sections grouped by feature. US-0112 sub-sub-section notes no dedicated sovereign-loop block; references L181–199 delivery/catalog keys. Default-off / zero-overhead-when-off wording per AC-3. | AC-3 | A |
| **T-004** | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` (one-way copy after T-001/T-002/T-003 complete). Re-run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). | AC-5 | B |
| **T-005** | Run validators (AC-4, AC-6) and fix any drift. `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` unchanged. `python scripts/validate_doc_profile.py` + `python scripts/check-user-visible-metadata.py` → expect PASS. Fix any narrative prose that leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. | AC-4, AC-6 | B |
| **T-006** | Run regression tests (AC-8) and confirm green. `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect 4 passed (US-0113 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`). Confirm no test weakenings — if a test fails, the prose is wrong, not the test. | AC-8 | B |

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
| `test_bug0013_parity_check` + 3 companions | `tests/scratchpad_example_parity_test.py` | AC-5 (indirect), AC-8 | Confirms `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.local.example.md` parity; US-0113 does not touch either file, so tests remain green by construction. |
| `validate_readme_feature_coverage.py --enforce` | `scripts/validate_readme_feature_coverage.py` | AC-4 | Coverage gate; `coverage_missing=["US-0117"]` must remain unchanged. |
| `check_intake_template_parity.py` | `scripts/check_intake_template_parity.py` | AC-5 | Framework README byte-parity gate. |
| `validate_doc_profile.py` | `scripts/validate_doc_profile.py` | AC-6 | Audience profile gate. |
| `check-user-visible-metadata.py` | `scripts/check-user-visible-metadata.py` | AC-6 | Metadata hygiene gate. |

**No new tests proposed.** R-0101 confirmed no test weakenings; AC-8 is satisfied by existing tests remaining green. Adding new tests would violate the "no test weakenings" spirit (US-0113 is documentation-only; tests are read-only gates).

## Compose guards (non-negotiable — all UNCHANGED)

| Story | Compose rule |
|-------|--------------|
| **US-0091** | Feature coverage catalog anchor `<!-- readme-feature-coverage-catalog -->` (L63) + one-liners (L1235–L1243) UNCHANGED — US-0113 appends narrative sections outside the catalog block. |
| **US-0097** | Project README parity surface UNCHANGED — US-0113 touches framework README pair only, not project README. |
| **US-0017** | Framework README parity contract UNCHANGED — US-0113 preserves byte-parity via T-004 lockstep. |
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
| **US-0111** | Release Trigger Adapters schema/semantics UNCHANGED — documented only (sovereign-loop angle; release-workflow angle belongs to US-0114). |
| **US-0112** | Model-Catalog Example Presets schema/semantics UNCHANGED — documented only (sovereign-loop angle; release-workflow angle belongs to US-0114). |

**16 guards UNCHANGED.** US-0113 lives entirely outside the compose surface (documentation-only; no code/scripts/installers/scratchpad canonical touched).

## Carry-overs from research (resolution)

### (a) 5 missing `# US-xxxx` h1 anchors in `architecture.md`

**Decision: DEFER to US-0117** (phase & role governance family, which owns US-0069..US-0090 and naturally covers architecture anchors for sovereign-loop features).

**Justification**:

- AC-7 only requires **runbook** cross-links, which exist for all 9 features (R-0101 § runbook cross-link targets). The missing `architecture.md` h1 anchors are NOT a US-0113 AC.
- US-0113 is scoped as a **framework README** documentation story (`its_magic/README.md` pair). The `architecture.md` h1 anchors are an internal engineering-docs surface, not an operator-facing README surface. Mixing the two would blur the story's vertical-slice boundary.
- US-0117 (phase & role governance family) is the natural owner: it already covers architecture-doc anchors for governance features, and adding 5 minimal `# US-xxxx` h1 sections (summarizing locked normative content from R-0089/R-0092/R-0093/R-0094/R-0091 + DEC-0103/0104/0105/0107/0110) fits its scope cleanly.
- Deferring keeps US-0113 at 6 task seeds (well under `SPRINT_MAX_TASKS=12`); adding T-007 would still fit but would cross the story's vertical-slice boundary.

**Deferral note for orchestrator**: This is a **deferral candidate** for the orchestrator's segment-boundary advance hook. **DO NOT append to `handoffs/sovereign_deferrals.jsonl` in architecture phase** (per instructions). Note for orchestrator: when US-0117 enters `plan` macro, its discovery should narrow-read this section and add the 5 missing h1 anchors as a task seed. Anchor format to use at that time: `# US-xxxx — <feature title>` (matching existing `# US-0108`, `# US-0109`, `# US-0111`, `# US-0112` format).

### (b) Scratchpad reference extension ordering

**Decision: Mirror `.cursor/scratchpad.md` L388–539 canonical ordering** (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending.

**Justification**:

- The canonical scratchpad is the **source of truth** for sovereign-loop key grouping. Mirroring its ordering preserves source-of-truth parity and makes it trivial for operators to cross-reference a key in the README against the canonical scratchpad.
- Strict US-id-ascending ordering (US-0103 → US-0104 → US-0105 → US-0107 → ...) would re-order keys relative to the canonical scratchpad, creating a cognitive mismatch for operators who read both surfaces.
- The AC-2 per-feature **narrative subsections** (umbrella area) use US-id-ascending ordering (matching backlog `related_us` field) — this is the **narrative** surface where chronological/US-id ordering aids discovery. The AC-3 **scratchpad reference extension** is a **reference** surface where canonical-source parity aids lookup. The two surfaces have distinct ordering rationales; locking them differently is intentional, not inconsistent.
- This matches the research recommendation (R-0101 § Recommended architecture approach point 2).

## Risks (finalized)

| Risk | Severity | Mitigation |
|------|----------|------------|
| **AC-5 parity lockstep** — `its_magic/README.md` edited but `template/its_magic/README.md` not synced (or vice versa) | **MEDIUM** | T-004 mandates one-way copy `its_magic/README.md` → `template/its_magic/README.md` after T-001/T-002/T-003 complete. Execute-phase must run `cmd /c fc /b its_magic\README.md template\its_magic\README.md` (expect no differences) + `python scripts/check_intake_template_parity.py` (expect `[INTAKE_TEMPLATE_PARITY_OK]`). QA must re-verify both gates. |
| **AC-8 regression tests** — coverage parity contract tests weakened or failing | **LOW–MEDIUM** | US-0113 is documentation-only; **forbid edits** to `.cursor/scratchpad.md`, `template/.cursor/scratchpad.local.example.md`, and `tests/scratchpad_example_parity_test.py` in execute-phase task list. If a test fails, the prose is wrong, not the test — fix prose, never relax test. T-006 confirms green. |
| **AC-4 coverage drift** — catalog block accidentally reflowed | **LOW** | T-005 runs `validate_readme_feature_coverage.py --enforce`; `coverage_missing=["US-0117"]` must remain unchanged. Catalog block L63 + L1235–L1243 treated as read-only. |
| **AC-6 metadata leakage** — internal IDs (DEC-xxxx/R-xxxx/reason-codes) leak into user-visible prose | **LOW** | T-005 runs `validate_doc_profile.py` + `check-user-visible-metadata.py`; US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. |
| **Decomposition drift (US-0114 angle overlap)** — US-0111/US-0112 subsections overlap confusingly with US-0114 | **LOW** | US-0113 subsections include explicit "see US-0114 for release-workflow operator docs on this feature" pointers (T-002). US-0113 = sovereign-loop angle; US-0114 = release-workflow angle. |

## Stop conditions

**stop_conditions_met=yes**:

- **No major tradeoff requires DEC** — confirmed (companion_dec=none; documentation-only; no architectural surface).
- **No feasibility unknown** — R-0101 closed all 3 discovery open questions; architecture phase resolved both carry-overs.
- **No data migration risk** — documentation-only; no schema, no data, no installer changes.

## Decision gate check

**No DECISION_GATE raised.** Architecture phase revealed no question requiring operator input. Both carry-overs resolved by tech-lead within the `plan` macro (defer h1 anchors to US-0117; lock scratchpad reference ordering = canonical mirror). No sovereign-memory digest call needed (US-0113 is documentation-only; existing digest context sufficient per R-0101).

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called (US-0113 documentation-only; existing digest context sufficient per R-0101). Sovereign-loop pattern identified for curator retrospective at segment close: "operator-documentation gap closing follows 5-story decomposition by functional family with angle-distinct narratives for features that span families (US-0111/US-0112 appear in both US-0113 sovereign-loop and US-0114 release-workflow with distinct angles)." No write to `mistakes.jsonl` in architecture phase.

## Consequences

- Sprint: S0113 (pending `/sprint-plan`).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.
- Framework README pair grows by umbrella + 9 subsections + scratchpad reference extension (both `its_magic/README.md` and `template/its_magic/README.md` byte-identical).
- 5 missing `architecture.md` h1 anchors deferred to US-0117.
- No new tests; no new DECs; no compose-surface changes.

## Evidence references

- `docs/product/backlog.md` — `## US-0113` block (lines 3893–3909)
- `docs/engineering/research.md` — `R-0101` (delivered, 3/3 open questions closed)
- `handoffs/po_to_tl.md` — research handoff (topmost block) + discovery handoff
- `docs/engineering/state.md` — research checkpoint (latest) + architecture checkpoint (this phase, appended)
- `handoffs/resume_brief.md` — top block updated to reflect architecture complete
- `.cursor/scratchpad.md` — sovereign-loop keys block (L388–539) — canonical source for AC-3 extension ordering
- `its_magic/README.md` — L350 (`## Commands and workflow`) umbrella target; L940 (`### Full scratchpad reference (detailed)`) extension target
- `docs/engineering/architecture.md` — h1 inventory confirmed: `# US-0108` (L120), `# US-0109` (L220), `# US-0111` (L335), `# US-0112` (L454) exist; US-0103/0104/0105/0107/0110 missing (deferred to US-0117)
- `decisions/DEC-0112.md` — highest existing DEC (next available would be DEC-0113; not used — companion_dec=none)




