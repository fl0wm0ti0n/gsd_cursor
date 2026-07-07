# Sprint S-BUG0013 Tasks — BUG-0013

**sprint_id**: S-BUG0013  
**bug_refs**: BUG-0013  
**dec_ref**: none (packaging defect; per R-0099 Q6 no DEC required)  
**task_count**: 3  
**within_limit**: true (3 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**coverage**: AC-1..AC-6 surjective via T-001..T-003 (6 ACs, 3 tasks; 1:1 architecture-seed bijection)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — Sync `template/.cursor/scratchpad.local.example.md` from canonical — AC-1, AC-2

- **ac_ref**: AC-1, AC-2
- **dec_ref**: architecture `# BUG-0013` § Fix approach (A1), § Files to touch
- **description**: Replace content of `template/.cursor/scratchpad.local.example.md` with canonical `.cursor/scratchpad.md` content. Preserve example-only header (first 5 lines of template documenting copy-to-local semantics: `# its-magic scratchpad (framework default catalog — Model B / DEC-0055)` block). Exclude project-local override section (operator-specific values at end of canonical). Feature-flag keys, section structure, and default values must match canonical byte-for-byte after the header. After sync, verify installer manifest already lists `template/.cursor/scratchpad.local.example.md` as packaged source (R-0099 Q2 confirms correct — no installer changes needed).
- **files_affected**:
  - `template/.cursor/scratchpad.local.example.md`
  - `.cursor/scratchpad.local.example.md` (repo-local copy — mirror template after sync)
- **parity_touchpoints**: architecture § Fix approach (A1); 9 section headers (US-0103, US-0110, US-0104, US-0105, US-0107, US-0106, US-0108, US-0109, US-0111).
- **acceptance_check**:
  - `template/.cursor/scratchpad.local.example.md` contains all 9 missing sections from canonical.
  - Example-only header (first 5 lines of template) is preserved intact.
  - Project-local overrides section NOT present in template.
  - Byte-identical content between canonical and template (after header, before local overrides).
  - `.cursor/scratchpad.local.example.md` mirrors `template/.cursor/scratchpad.local.example.md`.
  - `installer.py` materialize function still reads from `template/` (unchanged — verify no regression).
- **status**: planned

---

## T-002 — Write parity test `tests/scratchpad_example_parity_test.py` — AC-3

- **ac_ref**: AC-3
- **dec_ref**: architecture `# BUG-0013` § Fix approach (A3), § Test markers
- **description**: Create `tests/scratchpad_example_parity_test.py` with three mandatory test markers:
  1. **`test_bug0013_parity_check`** — template example contains every feature-flag key and section header present in canonical `.cursor/scratchpad.md` (diff-ignore: example-header + project-local overrides). Verifies all 9 sections present (US-0103, US-0110, US-0104, US-0105, US-0107, US-0106, US-0108, US-0109, US-0111).
  2. **`test_bug0013_header_preserved`** — example-only header (first 5 lines of template) is intact, not overwritten by canonical content.
  3. **`test_bug0013_local_overrides_preserved`** — project-local overrides section (operator-specific values) is NOT leaked into template example.
  Optional but recommended: per-section coverage markers (`test_bug0013_section_US0103_present` … `test_bug0013_section_US0111_present`). Parity scope: `--scope=scratchpad-example`.
- **files_affected**:
  - `tests/scratchpad_example_parity_test.py` (new)
- **parity_touchpoints**: architecture § Test markers; active-only test file.
- **acceptance_check**:
  - All three test function names present with assertions per architecture table.
  - `pytest -k bug0013` exits 0 after T-001 template sync.
  - Parity check covers all 9 missing sections.
  - Header preservation check asserts first 5 lines unchanged.
  - Local-overrides check asserts absence of project-local override markers in template.
- **status**: planned

---

## T-003 — Add runbook § "Scratchpad example parity" — AC-4

- **ac_ref**: AC-4
- **dec_ref**: architecture `# BUG-0013` § Fix approach (A4)
- **description**: Add runbook subsection **`### Scratchpad example parity`** (+ template mirror `template/docs/engineering/runbook.md`) documenting:
  - When the canonical `.cursor/scratchpad.md` is extended with new feature sections, the template example `template/.cursor/scratchpad.local.example.md` must be re-synced.
  - Single-source-of-truth preference: template example = canonical minus example-header + project-local values.
  - Sync procedure: copy canonical content preserving example-header (first 5 lines), excluding project-local overrides.
  - Verification: run `pytest -k bug0013` to confirm parity.
  - Active/template byte-identical for runbook section.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Fix approach (A4); active/template mirror.
- **acceptance_check**:
  - Runbook subsection title `Scratchpad example parity` present.
  - Single-source-of-truth preference documented.
  - Sync procedure documented with header-preservation + local-overrides-exclusion rules.
  - Verification command (`pytest -k bug0013`) referenced.
  - Active/template runbook delta byte-identical for this section.
- **status**: planned

---

## Recommended /execute ordering

1. **T-001** — Sync template from canonical (foundation — other tasks depend on correct template)
2. **T-002** — Write parity test (validates T-001 + prevents regression)
3. **T-003** — Add runbook § (documents procedure + prevention)
