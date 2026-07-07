# Sprint S0113 — Tasks (US-0113)

**sprint_id**: S0113
**story_refs**: US-0113
**dec_ref**: none (companion_dec=none; US-0113 documentation-only)
**architecture_ref**: `docs/engineering/architecture.md#US-0113`
**research_ref**: `docs/engineering/research.md` `R-0101`
**task_count**: 6
**within_limit**: true (6 ≤ `SPRINT_MAX_TASKS=12`)
**coverage**: AC-1..AC-8 surjective via T-001..T-006 (8 ACs, 6 tasks; multi-AC tasks T-002 (AC-2+AC-7), T-005 (AC-4+AC-6))

---

## Task-to-AC Bijection Table

| Task ID | Title | ACs Satisfied |
|---------|-------|---------------|
| T-001 | Add umbrella `### Sovereign-loop era (US-0103–US-0112)` section under `## Commands and workflow` | AC-1 |
| T-002 | Add 9 per-feature `#### US-xxxx` operator subsections nested under umbrella | AC-2, AC-7 |
| T-003 | Extend `### Full scratchpad reference (detailed)` with sovereign-loop keys | AC-3 |
| T-004 | Sync `template/its_magic/README.md` byte-identical from `its_magic/README.md` | AC-5 |
| T-005 | Run validators (`validate_readme_feature_coverage.py --enforce`, `validate_doc_profile.py`, `check-user-visible-metadata.py`) and fix any drift | AC-4, AC-6 |
| T-006 | Run regression tests (`pytest tests/scratchpad_example_parity_test.py -q`); confirm green | AC-8 |

**Total**: 6 tasks covering 8 ACs (surjective).

---

## Task Seeds

### T-001: Add umbrella `### Sovereign-loop era (US-0103–US-0112)` section

**Coverage**: AC-1
**Risk**: LOW
**Dependencies**: None
**Files to touch**:
- `its_magic/README.md` (append new `### Sovereign-loop era (US-0103–US-0112)` section under `## Commands and workflow` (L350), before `### Full scratchpad reference (detailed)` (L940))

**Scope**:
- Add `### Sovereign-loop era (US-0103–US-0112)` umbrella section containing:
  - **Default-off posture callout** — explicit statement that all sovereign-loop features are opt-in via scratchpad keys and impose zero overhead when disabled.
  - **9-step recommended enable order** — dependency chain: `AI_DECISION_LEDGER` → `SOVEREIGN_MEMORY` → `CROSS_MODEL_REVIEW` → `SOVEREIGN_GOAL_MODE=goal_convergence` → `AUTO_SOVEREIGN` → `SOVEREIGN_PARALLEL_DEV` → `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY` → `RELEASE_TRIGGER_SOURCE` → US-0112 presets.
  - **Runbook pointer** — single cross-link to the sovereign-loop runbook section (existing anchor only; no content duplication).
  - **Zero-overhead-when-off contract paragraph** — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern: disabled features incur no runtime cost, no artifact emission, no side effects.

**Acceptance (deterministic, testable)**:
- `its_magic/README.md` contains a `### Sovereign-loop era (US-0103–US-0112)` heading under `## Commands and workflow` and before `### Full scratchpad reference (detailed)`.
- The umbrella section names all 9 in-scope features (US-0103/US-0104/US-0105/US-0107/US-0108/US-0109/US-0110/US-0111/US-0112) at least once.
- The umbrella section contains the 9-step recommended enable order with all 9 keys/anchors listed in order.
- The umbrella section contains a default-off posture callout and a zero-overhead-when-off contract paragraph.
- The umbrella section contains a runbook cross-link (existing anchor; no new runbook content).

---

### T-002: Add 9 per-feature `#### US-xxxx` operator subsections nested under the umbrella

**Coverage**: AC-2, AC-7
**Risk**: LOW
**Dependencies**: T-001 (umbrella section must exist first to nest under)
**Files to touch**:
- `its_magic/README.md` (add 9 `#### US-xxxx` subsections nested under the T-001 umbrella, ordered **US-id-ascending**: US-0103 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0110 → US-0111 → US-0112)

**Scope**:
- Add 9 per-feature `#### US-xxxx` operator subsections. Each subsection contains:
  - **1–3 sentence narrative** — what the feature does, grounded in the backlog row and scratchpad keys. For US-0111/US-0112, use the **sovereign-loop angle** (US-0111 = release-trigger adapter as a sovereign-loop notification/ledger surface; US-0112 = preset delivery as a sovereign-loop bootstrap aid). Include explicit **"see US-0114 for release-workflow operator docs on this feature"** pointers for US-0111 and US-0112.
  - **Master enable flag + related keys with defaults** — the controlling scratchpad keys (master flag + related keys), with default values.
  - **Zero-overhead-when-off wording** — mirrors `.cursor/scratchpad.md` `# Default-off` pattern.
  - **Runbook cross-link** — existing anchor only (AC-7 forbids duplication). All 9 runbook anchors already exist (R-0101 § runbook cross-link targets).
- **US-0112 special case**: subsection references existing delivery/catalog keys (`DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP`, `MODEL_TIER` from `.cursor/scratchpad.md` L181–199 region) — **no new scratchpad block** introduced; US-0112 has no dedicated sovereign-loop scratchpad block.

**Acceptance (deterministic, testable)**:
- `its_magic/README.md` contains exactly 9 `#### US-xxxx` subsections nested under the `### Sovereign-loop era (US-0103–US-0112)` umbrella.
- Subsection order is US-id-ascending: US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112.
- Each subsection contains the master enable flag with its default value (e.g., `AI_DECISION_LEDGER=0` for US-0103).
- Each subsection contains a zero-overhead-when-off statement.
- Each subsection contains a runbook cross-link to an existing anchor (no new runbook content added to `docs/engineering/runbook.md`).
- US-0111 and US-0112 subsections contain explicit "see US-0114 for release-workflow operator docs on this feature" pointers.
- US-0112 subsection references existing delivery/catalog keys (no new scratchpad block).
- No runbook content is duplicated in the README (AC-7).

---

### T-003: Extend `### Full scratchpad reference (detailed)` with sovereign-loop keys

**Coverage**: AC-3
**Risk**: LOW
**Dependencies**: T-002 (per-feature subsections complete first to keep narrative+reference ordering coherent)
**Files to touch**:
- `its_magic/README.md` (extend the `### Full scratchpad reference (detailed)` section, L940, with sovereign-loop keys)

**Scope**:
- Extend `### Full scratchpad reference (detailed)` with 9 sub-sub-sections grouped by feature.
- **Ordering: mirror `.cursor/scratchpad.md` L388–539 canonical ordering** (US-0103 → US-0110 → US-0104 → US-0105 → US-0107 → US-0108 → US-0109 → US-0111 → US-0112), NOT strict US-id-ascending. (Carry-over (b) resolution from architecture: canonical scratchpad is source of truth; mirroring preserves operator cross-reference parity. Narrative subsections (AC-2) use US-id-ascending for discovery; reference extension (AC-3) uses canonical mirror for lookup — distinct rationales, intentional.)
- Each sub-sub-section documents the sovereign-loop keys for that feature with defaults.
- **US-0112 special case**: sub-sub-section notes that US-0112 has no dedicated sovereign-loop scratchpad block and references the existing delivery/catalog keys (`DELIVERY_MODE`, `TOKEN_PROFILE`, `ID_NAMESPACE_BOOTSTRAP`, `MODEL_TIER` from `.cursor/scratchpad.md` L181–199 region).
- **Default-off / zero-overhead-when-off wording** per AC-3 — mirrors the `.cursor/scratchpad.md` `# Default-off` pattern.

**Acceptance (deterministic, testable)**:
- `its_magic/README.md` `### Full scratchpad reference (detailed)` section contains 9 sovereign-loop sub-sub-sections.
- Sub-sub-section order is canonical mirror: US-0103, US-0110, US-0104, US-0105, US-0107, US-0108, US-0109, US-0111, US-0112.
- Each sub-sub-section documents the feature's sovereign-loop keys with defaults (cross-reference parity with `.cursor/scratchpad.md` L388–539).
- The US-0112 sub-sub-section notes "no dedicated sovereign-loop scratchpad block" and references the delivery/catalog keys.
- Each sub-sub-section contains default-off / zero-overhead-when-off wording.

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
  - `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → expect `[README_FEATURE_COVERAGE_VALIDATE_OK]` with `coverage_missing=["US-0117"]` **unchanged** (US-0117 is pre-existing and out of US-0113 scope; catalog block L63 + L1235–L1243 treated as read-only).
- Run audience + metadata validators:
  - `python scripts/validate_doc_profile.py` → expect PASS.
  - `python scripts/check-user-visible-metadata.py` → expect PASS.
- **Fix any drift**: if any validator fails, fix the narrative prose. **Convention**: reuse existing `(US-xxxx)` parenthetical-tag pattern; avoid `DEC-xxxx`/`R-xxxx`/reason-code families in narrative sentences. US-IDs allowed only in parenthetical catalog tags `(US-xxxx)`. If a prose fix is applied to `its_magic/README.md`, re-run T-004 one-way copy to re-sync `template/its_magic/README.md`.

**Acceptance (deterministic, testable)**:
- `python scripts/validate_readme_feature_coverage.py --repo . --enforce` emits `[README_FEATURE_COVERAGE_VALIDATE_OK]` (exit 0) with `coverage_missing=["US-0117"]` unchanged.
- `python scripts/validate_doc_profile.py` emits PASS (exit 0).
- `python scripts/check-user-visible-metadata.py` emits PASS (exit 0).
- No narrative prose leaks internal IDs (DEC-xxxx/R-xxxx/reason-codes) into user-visible sentences; US-IDs appear only in parenthetical catalog tags `(US-xxxx)`.
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
- **No test weakenings**: US-0113 does NOT modify `.cursor/scratchpad.md` or `template/.cursor/scratchpad.local.example.md`, so the scratchpad parity tests remain green by construction. **If a test fails, the prose is wrong, not the test** — fix prose (re-run T-005), never relax the test.

**Acceptance (deterministic, testable)**:
- `python -m pytest tests/scratchpad_example_parity_test.py -q` reports 4 passed (exit 0).
- No edits to `tests/scratchpad_example_parity_test.py`, `.cursor/scratchpad.md`, or `template/.cursor/scratchpad.local.example.md` (forbid test weakenings).
- If a test failed and prose was fixed, the fix is documented and the test re-run green without modification.

---

## Appendix: Task Dependencies (Visual)

```
T-001 (umbrella section)
    ↓
T-002 (9 per-feature subsections)
    ↓
T-003 (scratchpad ref extension)
    ↓
T-004 (template byte-sync)
    ↓
T-005 (validators)
    ↓
T-006 (regression tests)
```

---

**Task Execution Order**: T-001 → T-002 → T-003 → T-004 → T-005 → T-006