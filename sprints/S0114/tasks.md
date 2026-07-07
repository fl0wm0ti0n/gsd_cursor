# Sprint S0114 — Tasks (US-0114)

**sprint_id**: S0114
**story_refs**: US-0114
**dec_ref**: none (companion_dec=none; US-0114 documentation-only)
**architecture_ref**: `docs/engineering/architecture.md#US-0114` (h1 anchor at L914)
**research_ref**: `docs/engineering/research.md` `R-0102`
**task_count**: 6
**within_limit**: true (6 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-8 surjective via T-001..T-006 (8 ACs, 6 tasks; multi-AC tasks T-002 (AC-2+AC-7), T-005 (AC-4+AC-6))

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-001 | Add `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section under `## Commands and workflow` | AC-1 |
| T-002 | Add 4 per-feature `#### US-xxxx` operator subsections nested under umbrella (release-workflow angle + bidirectional US-0113 pointers + runbook cross-links) | AC-2, AC-7 |
| T-003 | Extend `### Full scratchpad reference (detailed)` with `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block (net-new keys + cross-link pointers only) | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` | AC-5 |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`) and fix any drift | AC-4, AC-6 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q`); confirm green | AC-8 |

**Total**: 6 tasks covering 8 ACs (surjective).

---

## Task Seeds

### T-001: Add `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section

**Coverage**: AC-1
**Risk**: LOW
**Dependencies**: None
**Files to touch**:
- `its_magic/README.md` (append new `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` section under `## Commands and workflow` (L350), placed **immediately after** the closing of the US-0113 sovereign-loop umbrella block (which ends before L1225 `### Full scratchpad reference (detailed)`), keeping the two family umbrellas visually adjacent as siblings)

**Scope**:
- Add `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella section containing:
  - **Default-off posture callout** — explicit statement that all release & distribution features are opt-in via scratchpad keys and impose zero overhead when disabled.
  - **4-step recommended enable order** — dependency chain: `US-0062` (installer-owned `its_magic/` folder + `FRAMEWORK_KIT_REPO`/`PROJECT_README_ENFORCE`) → `US-0041` (lifecycle QA matrix) → `US-0112` (model-catalog example presets on install/upgrade) → `US-0111` (release trigger adapters). Order rationale: installer boundary first → QA gate next → preset delivery (uses installer manifest) → release trigger (consumes installed/preset state).
  - **Runbook pointer** — single cross-link to a release & distribution runbook section (existing anchor only; no content duplication).
  - **Zero-overhead-when-off contract paragraph** — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern: disabled features incur no runtime cost, no artifact emission, no side effects.

**Acceptance (deterministic, testable)**:
- `its_magic/README.md` contains a `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` heading under `## Commands and workflow` and after the US-0113 sovereign-loop umbrella block (i.e., before `### Full scratchpad reference (detailed)` at L1225).
- The umbrella section names all 4 in-scope features (US-0041/US-0062/US-0111/US-0112) at least once.
- The umbrella section contains the 4-step recommended enable order with all 4 features/anchors listed in order (US-0062 → US-0041 → US-0112 → US-0111).
- The umbrella section contains a default-off posture callout and a zero-overhead-when-off contract paragraph.
- The umbrella section contains a runbook cross-link (existing anchor; no new runbook content added to `docs/engineering/runbook.md`).

---

### T-002: Add 4 per-feature `#### US-xxxx` operator subsections nested under the umbrella

**Coverage**: AC-2, AC-7
**Risk**: LOW
**Dependencies**: T-001 (umbrella section must exist first to nest under)
**Files to touch**:
- `its_magic/README.md` (add 4 `#### US-xxxx` subsections nested under the T-001 umbrella, ordered **US-id-ascending** (deterministic — matches catalog one-liner order at L82 / L1611 / L1651 / L1652): US-0041 → US-0062 → US-0111 → US-0112)

**Scope**:
- Add 4 per-feature `#### US-xxxx` operator subsections. Each subsection contains:
  - **1–3 sentence narrative** — what the feature does (release-workflow angle), grounded in the backlog row + scratchpad keys. For US-0111/US-0112, use the **release-workflow angle**: US-0111 = release-trigger adapters as a release-workflow tool (GitHub webhook, npm publish, git tag, manual `/release` dispatch mechanics + changelog derivation mechanics; `RELEASE_TRIGGER_SOURCE` / `RELEASE_TRIGGER_TIMEOUT_SEC` / `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` as release operator controls); US-0112 = model-catalog example preset shipping via installer/upgrade (installer payload + version sync mechanics; preset file layout under `template/.cursor/model-catalog.local.example*.json`; operator opt-in by copying to `.cursor/model-catalog.local.json`). For US-0041 = end-to-end lifecycle QA for `its-magic` install/upgrade/clean (lifecycle QA matrix). For US-0062 = installer-owned `its_magic/` folder for framework metadata (installer ownership boundary declared by DEC-0045, amended by US-0097/DEC-0083).
  - **Master enable flag + related keys with defaults** — the controlling scratchpad keys (master flag + related keys), with default values. For US-0062: `PROJECT_README_ENFORCE=0|1` (default `1` post-bootstrap), `FRAMEWORK_KIT_REPO=0|1` (default `0`; kit repo exception). For US-0111: `RELEASE_PUBLISH_MODE=disabled|confirm|auto` (default `confirm`), `RELEASE_TARGETS_FILE` (default `docs/engineering/release-targets.json`), `RELEASE_TARGETS_DEFAULT` (default empty). For US-0112: reference existing delivery/catalog keys (`DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP`, `MODEL_TIER` from `.cursor/scratchpad.md` L181–199 region) — no new scratchpad block. For US-0041: reference existing installer completeness reason codes / runbook `## Lifecycle QA matrix (US-0041)` L2522 anchor (no dedicated lifecycle-QA scratchpad block per R-0102 open question #3 resolution).
  - **Zero-overhead-when-off wording** — mirrors `.cursor/scratchpad.md` `# Default-off` pattern.
  - **Runbook cross-link** — existing anchor only (AC-7 forbids duplication). All 4 cross-link targets already exist (R-0102):
    - US-0041 → `## Lifecycle QA matrix (US-0041)` (runbook L2522).
    - US-0062 → `## Project README coverage validation (US-0097 / DEC-0083)` (runbook L171) **with explanatory note** "(US-0062 installer ownership boundary amended by US-0097 / DEC-0083; original DEC-0045 referenced from `docs/engineering/decisions.md` § DEC-0045)" (R-0102 open question #2 resolution).
    - US-0111 → `## Release Trigger Adapters (US-0111 / DEC-0111)` (runbook L3378).
    - US-0112 → `## Model-catalog example preset delivery (US-0112 / DEC-0112)` (runbook L941).
- **Bidirectional "see US-0113" pointers**: US-0111 and US-0112 subsections MUST include explicit "see US-0113 for sovereign-loop angle on this feature" pointers (mirror US-0113's "see US-0114" pointer convention per R-0101; US-0113's subsections already ship the "see US-0114" pointer per S0113 RELEASED state).

**Acceptance (deterministic, testable)**:
- `its_magic/README.md` contains exactly 4 `#### US-xxxx` subsections nested under the `### Release & distribution (US-0041 / US-0062 / US-0111 / US-0112)` umbrella.
- Subsection order is US-id-ascending: US-0041, US-0062, US-0111, US-0112.
- Each subsection contains the master enable flag(s) with default value(s) (e.g., `PROJECT_README_ENFORCE=1` for US-0062).
- Each subsection contains a zero-overhead-when-off statement.
- Each subsection contains a runbook cross-link to an existing anchor (no new runbook content added to `docs/engineering/runbook.md`).
- US-0062 subsection cross-links to `## Project README coverage validation (US-0097 / DEC-0083)` (L171) with the explanatory note referencing DEC-0045 / US-0097 / DEC-0083.
- US-0041 subsection cross-links to `## Lifecycle QA matrix (US-0041)` (L2522).
- US-0111 and US-0112 subsections contain explicit "see US-0113 for sovereign-loop angle on this feature" pointers.
- US-0111 subsection uses release-workflow angle (release-trigger adapters as a release-workflow tool — webhook/npm/git-tag/manual dispatch + changelog derivation mechanics).
- US-0112 subsection uses release-workflow angle (installer payload + version sync + preset file layout + operator opt-in).
- No runbook content is duplicated in the README (AC-7).

---

### T-003: Extend `### Full scratchpad reference (detailed)` with `### Release & distribution keys` sub-block

**Coverage**: AC-3
**Risk**: LOW
**Dependencies**: T-002 (per-feature subsections complete first to keep narrative+reference ordering coherent)
**Files to touch**:
- `its_magic/README.md` (extend the `### Full scratchpad reference (detailed)` section, L1225, with a `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block as a sibling to `### Sovereign-loop era keys` (L1242))

**Scope**:
- Append `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block as a sibling to `### Sovereign-loop era keys (US-0103–US-0112)` (L1242) under `### Full scratchpad reference (detailed)` (L1225).
- **Net-new key rows ONLY** (carry-over (b) locked — preserve US-0113 byte-stability, no duplicate rows):
  - **US-0062 net-new keys** (from `.cursor/scratchpad.md` L260–267): `PROJECT_README_ENFORCE=0|1` (default `1` post-bootstrap), `FRAMEWORK_KIT_REPO=0|1` (default `0`; kit repo exception). Document defaults + flip guidance.
- **Grouped cross-links** (no new rows — cross-link pointers to existing rows elsewhere in the README):
  - **US-0054 publish controls** (from `.cursor/scratchpad.md` L200–209 / README L541–547): `RELEASE_PUBLISH_MODE=disabled|confirm|auto` (default `confirm`), `RELEASE_TARGETS_FILE` (default `docs/engineering/release-targets.json`), `RELEASE_TARGETS_DEFAULT` (default empty) — referenced for US-0111 release-workflow operator surface.
  - **Shared release surface** (from `.cursor/scratchpad.md` L66–67 / README L1233/L1235): `AUTO_INSTALL_DEPS=0|1` (default `1`), `AUTO_RELEASE_NOTES=0|1` (default `1`) — referenced for US-0041/US-0062 shared release gate surface.
- **Cross-link pointers to US-0113's `### Sovereign-loop era keys` block** for overlapping US-0111/US-0112 keys (DO NOT re-document — preserve byte-stability):
  - US-0111 overlap keys (already documented at README L1338–1346 inside `### Sovereign-loop era keys`): `RELEASE_TRIGGER_SOURCE`, `RELEASE_TRIGGER_TIMEOUT_SEC`, `RELEASE_TRIGGER_FALLBACK_TO_LOCAL`.
  - US-0112 overlap keys (already documented at README L1348–1364 inside `### Sovereign-loop era keys`): `DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP`, `MODEL_TIER`.
  - Cross-link pointer wording: "See `### Sovereign-loop era keys (US-0103–US-0112)` above for the canonical key rows of US-0111's `RELEASE_TRIGGER_*` family and US-0112's delivery/catalog keys. US-0114 documents these from the release-workflow operator angle in the narrative subsection above; the canonical key rows remain in the sovereign-loop era block for byte-stability."
- **US-0041 special case**: US-0041 has NO dedicated release-distribution scratchpad key block — its normative surface is the runbook `## Lifecycle QA matrix (US-0041)` L2522 + installer completeness reason codes (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING`). The `### Release & distribution keys` sub-block notes this and cross-links to the runbook anchor + the shared `AUTO_INSTALL_DEPS` / `AUTO_RELEASE_NOTES` keys (R-0102 open question #3 resolution).
- **No duplicate key rows**: each key appears in exactly one canonical location (US-0113's block for US-0111/US-0112 overlap keys; US-0114's block for US-0062 net-new keys + grouped cross-links to US-0054/AUTO_INSTALL_DEPS/AUTO_RELEASE_NOTES).
- **Default-off / zero-overhead-when-off wording** per AC-3 — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern.

**Acceptance (deterministic, testable)**:
- `its_magic/README.md` `### Full scratchpad reference (detailed)` section contains a new `### Release & distribution keys (US-0041 / US-0062 / US-0111 / US-0112)` sub-block as a sibling to (after) `### Sovereign-loop era keys (US-0103–US-0112)`.
- The sub-block documents US-0062's `PROJECT_README_ENFORCE` and `FRAMEWORK_KIT_REPO` with defaults + flip guidance (the only net-new key rows).
- The sub-block contains grouped cross-link pointers to US-0054 publish controls (`RELEASE_PUBLISH_MODE`/`RELEASE_TARGETS_FILE`/`RELEASE_TARGETS_DEFAULT`) and shared `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` keys (no new rows — cross-references only).
- The sub-block contains cross-link pointers to `### Sovereign-loop era keys (US-0103–US-0112)` for overlapping US-0111/US-0112 keys — those 7 keys are NOT re-documented in US-0114's block (no duplicate rows).
- The sub-block notes US-0041's "no dedicated release-distribution scratchpad block" and cross-links to the runbook `## Lifecycle QA matrix (US-0041)` L2522 anchor + shared `AUTO_INSTALL_DEPS`/`AUTO_RELEASE_NOTES` keys.
- US-0113's `### Sovereign-loop era keys` block (L1242) is byte-stable — none of its rows are modified, reordered, or removed.
- Each net-new key row contains default-off / zero-overhead-when-off wording.
- No duplicate key rows exist between US-0113's block and US-0114's block.

---

### T-004: Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md`

**Coverage**: AC-5
**Risk**: MEDIUM (parity lockstep — highest risk in this sprint)
**Dependencies**: T-001, T-002, T-003 (all `its_magic/README.md` edits complete first)
**Files to touch**:
- `template/its_magic/README.md` (one-way copy from `its_magic/README.md`)

**Scope**:
- One-way copy: `its_magic/README.md` → `template/its_magic/README.md` (byte-identical).
- Re-run parity gates:
  - `cmd /c fc /b its_magic\README.md template\its_magic\README.md` → expect **no differences**.
  - `python scripts/check_intake_template_parity.py` → expect `[INTAKE_TEMPLATE_PARITY_OK]`.

**Acceptance (deterministic, testable)**:
- `cmd /c fc /b its_magic\README.md template\its_magic\README.md` reports no differences.
- `python scripts/check_intake_template_parity.py` emits `[INTAKE_TEMPLATE_PARITY_OK]` (exit 0).
- `template/its_magic/README.md` is byte-identical to `its_magic/README.md`.

**Note**: QA within `build+verify` must re-verify both parity gates (highest-risk mitigation per architecture).

---

### T-005: Run validators and fix any drift

**Coverage**: AC-4, AC-6
**Risk**: LOW
**Dependencies**: T-004 (template synced before validator runs)
**Files to touch**:
- `its_magic/README.md` and `template/its_magic/README.md` (only if drift requires prose fix; re-sync after any fix)

**Scope**:
- Run coverage validator:
  - `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` **unchanged** (US-0117 pre-existing gap; DC-1 + DC-2 out-of-scope). Catalog block L63 + L1235–L1243 treated as read-only.
  - **Encoding hygiene prerequisite:** working-tree `docs/product/backlog.md` has 185 stray `0xa7` bytes (Windows-1252 corruption flagged in R-0102 + architecture) that break this validator's strict UTF-8 read — orchestrator must restore encoding hygiene before execute so this gate can re-pass post-execute.
- Run audience + metadata validators:
  - `python scripts/validate_doc_profile.py` → expect PASS.
  - `python scripts/check-user-visible-metadata.py` → expect PASS.
- **Fix any drift**: if any validator fails, fix the narrative prose. **Convention**: reuse existing `(US-xxxx)` parenthetical-tag pattern; avoid `DEC-xxxx`/`R-xxxx`/reason-code families in narrative sentences. US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. US-0062's explanatory note is the only place a DEC id appears in prose — kept inside a parenthetical cross-link, not a user-visible sentence. If a prose fix is applied to `its_magic/README.md`, re-run T-004 one-way copy to re-sync `template/its_magic/README.md`.

**Acceptance (deterministic, testable)**:
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` emits `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=["US-0117"]` unchanged.
- `python scripts/validate_doc_profile.py` emits PASS (exit 0).
- `python scripts/check-user-visible-metadata.py` emits PASS (exit 0).
- No narrative prose leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs appear only in parenthetical catalog tags `(US-xxxx)` (with the documented US-0062 explanatory note exception inside a parenthetical cross-link).
- If any prose fix was applied, `template/its_magic/README.md` re-synced and both parity gates re-confirmed green.

---

### T-006: Run regression tests and confirm green

**Coverage**: AC-8
**Risk**: LOW–MEDIUM (forbid test weakenings)
**Dependencies**: T-005 (all prose finalized before regression confirmation)
**Files to touch**: None (regression tests are read-only gates)

**Scope**:
- Run regression tests:
  - `python -m pytest tests/scratchpad_example_parity_test.py -q` → expect **4 passed**.
- **No test weakenings**: US-0114 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`, so the scratchpad parity tests remain green by construction. **If a test fails, the prose is wrong, not the test** — fix prose (re-run T-005), never relax the test.

**Acceptance (deterministic, testable)**:
- `python -m pytest tests/scratchpad_example_parity_test.py -q` reports 4 passed (exit 0).
- No edits to `tests/scratchpad_example_parity_test.py`, `.cursor/scratchpad.md`, or `template/.cursor/scratchpad.local.example.md` (forbid test weakenings).
- If a test failed and prose was fixed, the fix is documented and the test re-run green without modification.

---

## Appendix: Task Dependencies (Visual)

```
T-001 (umbrella section)
    ↓
T-002 (4 per-feature subsections)
    ↓
T-003 (scratchpad ref extension — net-new + cross-links)
    ↓
T-004 (template byte-sync)
    ↓
T-005 (validators)
    ↓
T-006 (regression tests)
```

---

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006
