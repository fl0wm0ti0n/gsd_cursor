# PO to TL archive pack (2026-07-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 10
- First archived heading: `## Orchestrated discovery handoff — BUG-0014 / auto-20260703-01`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0014 / auto-20260703-01`
- Verification tuple (mandatory):
  - archived_body_lines=132
  - retained_body_lines=597

---

## Orchestrated discovery handoff — BUG-0014 / auto-20260703-01

### Target

- `bug_id=BUG-0014`
- `orchestrator_run_id=auto-20260703-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0014-discovery-20260703T154200Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_bug` (per **US-0079 / DEC-0061**)
- `runtime_proof_id=rp-auto-20260703-01-discovery-po-20260703T154200Z-BUG-0014`
- `proof_hash=a7983bc260df84fabc7d3a4ec9dbab8bfc991da1ca9db8bb6905bdf492460e63`

### Summary

**`/discovery`** **PASS_WITH_SCOPE_CONCERN** — bounded documentation-coverage backfill defect spanning 2 surfaces:
(1) `README.md` feature coverage catalog (lines 65–88) missing 11 sovereign-era feature entries (US-0103..US-0112 + BUG-0013).
(2) `handoffs/release_notes.md` legacy pointer missing 5 finalized-note entries (S0103, S0104, S0105, S0106, S0108).
All evidence_refs verified. Compose guards identified (10 US-xxx, ALL UNCHANGED). Risk is LOW (documentation-only).

### Scope Concern (CRITICAL — tech-lead must address)

**AC-3 as-written cannot pass with a narrow 12-row fix alone.** Current validator state:
- `validate_readme_feature_coverage.py --enforce` reports **117 coverage_missing** items (US-0001..US-0102 + all BUGs + US-0111 + US-0112).
- BUG-0014 scope covers only 12 of these (US-0103..US-0112 + BUG-0013).
- Adding only the 12 sovereign-era rows would NOT produce `[README_FEATURE_COVERAGE_VALIDATE_OK]`.
- Additional parity fail: `its_magic/README.md != template/its_magic/README.md`.

**Tech-lead must determine**: does AC-3 require full catalog backfill (117 rows), or does the validator predicate matrix need adjustment so that the existing catalog entries (which use feature-name labels like `/acceptance`, `/auto`, `/lint` etc.) satisfy the predicate for pre-sovereign entries? This is the central research question.

### Decomposition evaluation

**Single bug** — no split. Two surfaces (README catalog + release_notes pointer) are tightly coupled — same root cause (sovereign-loop sprints released without catalog backfill). Bounded fix, no story split.

### Duplicate / overlap check

- **BUG-0013** (scratchpad example stale): **ORTHOGONAL** — scratchpad template file-copy parity vs README catalog coverage.
- **BUG-0012** (native chain regression): **ORTHOGONAL** — `/auto` drain-advance behavior vs documentation.
- All three bugs touch entirely different artifacts.

### Risk surface

**LOW** — documentation-only changes across 2 text files. No code, no installer, no scripts. No backward compatibility impact. No compose surface amendment.

### Compose guards (10, ALL UNCHANGED)

| Guard | Rationale |
|-------|-----------|
| US-0091 | README feature coverage gate — predicate matrix schema unchanged |
| US-0097 | Project README coverage — not touched by this fix |
| US-0040 | Release notes lifecycle — fix follows existing lifecycle |
| US-0100 | Release changelog lib — unchanged |
| US-0101 | Model tier catalog — unchanged |
| US-0102 | Role-based catalog — unchanged |
| US-0103 | AI Decision Ledger — catalog row only |
| US-0104 | Cross-Model Critic — catalog row only |
| US-0105 | Sovereign Memory — catalog row only |
| US-0106 | Sovereign Role Manifest — catalog row only |
| US-0107 | Sovereign Loop Mode — catalog row only |
| US-0108 | Parallel Instance Arbitrage — catalog row only |
| US-0109 | Self-Healing Deploy Loop — catalog row only |
| US-0110 | Goal-Based Convergence — catalog row only |
| US-0111 | Release Trigger Adapters — catalog row only |
| US-0112 | Model-Catalog Example Presets — catalog row only |

### Research questions Q1–Q6

1. **Q1 (SCOPE CRITICAL)**: What is the predicate matrix contract of `validate_readme_feature_coverage.py`? Does the validator expect every DONE backlog US-xxxx / BUG-xxxx to have a matching row, or is there a subset predicate? Clarify whether the 117-gap count represents the true required set.
2. **Q2**: Should BUG-0014 fix only the 12 sovereign-era rows (narrow fix), or should it backfill the entire catalog to zero gaps? If narrow, is there a separate tech-debt issue for remaining gaps?
3. **Q3**: The `its_magic/README.md != template/its_magic/README.md` parity fail — is this in scope for BUG-0014 or a separate defect?
4. **Q4**: What row format does the validator expect per missing catalog entry? (derive from `scripts/readme_feature_coverage_lib.py` predicate matrix)
5. **Q5**: For `handoffs/release_notes.md` AC-2 backfill, what is the expected entry format? (follow existing S0107/S0109–S0112 pattern?)
6. **Q6**: Are there any DEC implications from the sovereign-loop era (US-0103..US-0112) that must be reflected in catalog row text?

### Intake validation state

| Script | Current state |
|--------|--------------|
| `bug_issue_validate.py --check-acceptance` | `[BUG_VALIDATION_OK]` ✅ |
| `validate_readme_feature_coverage.py --enforce` | **FAIL** (117 gaps + parity fail) ❌ |

AC-4 already satisfied today. AC-1/AC-2 are text-additive (not script-gated). AC-3 gates on Q1/Q2 resolution.

### Governance alignment

- `README_FEATURE_COVERAGE_ENFORCE=1` ✅ (scratchpad.md line 255)
- `PROJECT_README_ENFORCE=1` ✅ (scratchpad.md line 266)
- `FRAMEWORK_KIT_REPO=1` ✅ (project README 3g skipped)
- `INTAKE_GUIDED_MODE=1` ✅
- `ID_NAMESPACE_BOOTSTRAP=0` ✅

### Files to touch

- `README.md` — add 12 feature coverage catalog rows (or more per Q2 resolution)
- `handoffs/release_notes.md` — add 5 finalized-note entries (S0103, S0104, S0105, S0106, S0108)

### Files NOT to touch

- `scripts/validate_readme_feature_coverage.py` — predicate matrix unchanged (unless Q1 reveals need for adjustment)
- `scripts/readme_feature_coverage_lib.py` — same
- All compose-guard files (16 US-xxx listed above)
- `.cursor/scratchpad.md` — flag values unchanged
- All installer files, all sovereign-loop scripts

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0014` — lines 4168–4182)
- `handoffs/resume_brief.md` (top pointer → `/research`)
- `docs/engineering/state.md` (plan materialization + this discovery checkpoint)
- `README.md` lines 65–88 (feature coverage catalog section)
- `handoffs/release_notes.md` (legacy pointer — 5 missing entries confirmed)
- `handoffs/release_queue.md` (S0103–S0112 all `released`)
- `handoffs/releases/S0103-release-notes.md` through `S0112-release-notes.md` (all 10 exist and are finalized)
- `handoffs/releases/S-BUG0013-release-notes.md` (exists and finalized)
- `docs/product/acceptance.md` lines 130–160 (BUG-0014 row `[ ] — OPEN`)
- `scripts/validate_readme_feature_coverage.py` (validation logic understood)
- `.cursor/scratchpad.md` (flag values verified)

### Next

- **`/research`** (fresh **tech-lead** context) for **BUG-0014** — close Q1–Q6; produce **`R-0014`**; determine AC-3 scope (narrow vs full backfill), derive row format, identify parity fail ownership. Handoff to **`/architecture`** when research-ready.

### Decision gate

- **None** — discovery satisfied; research readiness explicit. SCOPE_CONCERN carried forward for research resolution.

### Status authority

- **OPEN** per **US-0045**; closure at `/release`.

---

