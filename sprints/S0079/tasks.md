# Sprint S0079 Tasks — BUG-0010

**sprint_id**: S0079  
**bug_refs**: BUG-0010  
**dec_ref**: DEC-0076 (binding; composes on DEC-0054 + DEC-0043)  
**task_count**: 9  
**within_limit**: true (9 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**coverage**: AC-1..AC-8 surjective via T-001..T-009 (8 ACs, 9 tasks; multi-AC rows per architecture seeds)

> No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — Dual-level `STORY_HEADING_H1`/`H2` + H1-wins `split_arch_stories` — AC-1, AC-2, AC-3, AC-7

- **ac_ref**: AC-1, AC-2, AC-3, AC-7
- **dec_ref**: DEC-0076 §1 (dual-level regex), §2 (H1-wins merge), §1 (BUG H1 parity)
- **description**: Replace monolithic `STORY_HEADING` in `scripts/enforce-triad-hot-surface.py` with `STORY_HEADING_H1 = ^# (?:US|BUG)-\d{4}\s*[:\u2014\-].+$` and `STORY_HEADING_H2 = ^## US-\d{4}\s*[:\u2014\-].+$`. Implement H1-wins merge in `split_arch_stories`: collect `(idx, story_id, level)` candidates; drop H2 when same `story_id` has H1; sort by `idx`; slice blocks (unchanged oldest-first rollover loop). Ship byte-identical `template/scripts/enforce-triad-hot-surface.py`.
- **files_affected**:
  - `scripts/enforce-triad-hot-surface.py`
  - `template/scripts/enforce-triad-hot-surface.py` (byte-identical)
- **parity_touchpoints**: DEC-0076 §6 row 1 (positive parity).
- **acceptance_check**:
  - `##`-only fixture over low `ARCH_HOT_MAX_LINES` → rollover moves ≥1 chunk; post `--check` exit 0.
  - Existing `# US-0001`/`# US-0002` self-test fixture unchanged (non-regression).
  - `# US-0067` + `## US-0067` → single boundary at H1 (mixed-file precedence).
  - `# BUG-0009` recognized as H1 story boundary (BUG H1 parity).
  - Active / template script SHA-256 equal.
- **status**: done

---

## T-002 — `count_h2_story_headings` + `check_arch_heading_policy` + CLI hook — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0076 §3 (diff-gated forward enforcement), §4 (reason codes)
- **description**: Add `count_h2_story_headings(text) -> int`, `check_arch_heading_policy(text_after, baseline_h2_count) -> Optional[str]` returning `ARCH_STORY_HEADING_LEVEL_INVALID` when H2 story-heading count **increases**; CLI flag `--check-arch-heading-policy [--baseline-h2-count N]`. Grandfathered `## US-` allowed; count decrease (normalization) allowed. Same file as T-001; ship byte-identical `template/` mirror.
- **files_affected**:
  - `scripts/enforce-triad-hot-surface.py`
  - `template/scripts/enforce-triad-hot-surface.py` (byte-identical)
- **parity_touchpoints**: DEC-0076 §6 row 1 (positive parity).
- **acceptance_check**:
  - Simulated H2 count increase → `ARCH_STORY_HEADING_LEVEL_INVALID`.
  - Stable H2 count or decrease → no policy error.
  - `--check-arch-heading-policy` CLI hook exits non-zero on violation.
  - No new standalone validator script added.
- **status**: done

---

## T-003 — Extend `--self-test` with dual-level fixture classes — AC-1, AC-2, AC-3, AC-6

- **ac_ref**: AC-1, AC-2, AC-3, AC-6
- **dec_ref**: DEC-0076 §5 (regression matrix + self-test)
- **description**: Extend `enforce-triad-hot-surface.py --self-test` with classes: `##`-only rollover; `# US-` non-regression; mixed H1+H2 same id; idempotent second rollover; enforcement-delta (`count_h2` increase); inner `##` subheading inside `# US-` block (no extra boundary). Ship byte-identical `template/` mirror.
- **files_affected**:
  - `scripts/enforce-triad-hot-surface.py`
  - `template/scripts/enforce-triad-hot-surface.py` (byte-identical)
- **parity_touchpoints**: DEC-0076 §6 row 1 (positive parity).
- **acceptance_check**:
  - `--self-test` exits 0 with all six fixture classes green.
  - Idempotent second `--rollover` → no-op when within caps.
  - Inner `## Details` inside `# US-0001` block does not create extra boundary.
  - Existing triad self-test cases remain green (additive only).
- **status**: done

---

## T-004 — Update `.cursor/commands/architecture.md` H1 mandate + policy step — AC-4, AC-5

- **ac_ref**: AC-4, AC-5
- **dec_ref**: DEC-0076 §3 (`/architecture` step 9 contract), §6 row 2 (command parity)
- **description**: Update `.cursor/commands/architecture.md` (+ `template/.cursor/commands/architecture.md`): mandate H1 `# US-xxxx` for story sections and `# BUG-xxxx` for bug sections; document baseline `count_h2_story_headings` capture **before** mutate; triad step 9 runs `--rollover`, `--check`, then heading policy check; reference `ARCH_STORY_HEADING_LEVEL_INVALID` as non-suppressible stop token.
- **files_affected**:
  - `.cursor/commands/architecture.md`
  - `template/.cursor/commands/architecture.md` (byte-identical mandate + policy text)
- **parity_touchpoints**: DEC-0076 §6 row 2 (positive parity).
- **acceptance_check**:
  - Command text requires H1 for new story/bug sections.
  - Step 9 documents baseline capture + policy check ordering.
  - `ARCH_STORY_HEADING_LEVEL_INVALID` listed as hard-fail stop token.
  - Active / template command files byte-identical for locked strings.
- **status**: done

---

## T-005 — Contract tests `test_bug0010_*` — AC-5, AC-6

- **ac_ref**: AC-5, AC-6
- **dec_ref**: DEC-0076 §5 (contract tests)
- **description**: Extend `tests/auto_command_contract_test.py` **in place** with `test_bug0010_*` subtests: architecture command H1 mandate text present; linkage to `# BUG-0010`; policy stop token reference. Additions only — do not modify unrelated subtests.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: Active-only (tests do not mirror).
- **acceptance_check**:
  - All `test_bug0010_*` subtests pass on clean tree post T-001..T-004.
  - Subtest fails if H1 mandate removed from architecture command.
  - Subtest fails if `ARCH_STORY_HEADING_LEVEL_INVALID` stop token removed.
- **status**: done

---

## T-006 — Harness section **§29A** — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0076 §5 (harness §29A)
- **description**: Add harness section **§29A** to `tests/run-tests.ps1` + `tests/run-tests.sh` wiring `enforce-triad-hot-surface.py --self-test` and contract-test subset for `test_bug0010_*`. Section id locked as **§29A** per DEC-0076. Additive — existing triad harness block unchanged.
- **files_affected**:
  - `tests/run-tests.ps1` (§29A)
  - `tests/run-tests.sh` (§29A)
- **parity_touchpoints**: Active-only (harness).
- **acceptance_check**:
  - §29A present in both PS1 and SH runners with matching semantics.
  - Section green when self-test + contract subtests pass.
  - Section fails closed when dual-level archiver regresses to H1-only boundaries.
- **status**: done

---

## T-007 — Optional `tests/fixtures/triad_arch_headings/` minimal fixtures — AC-1, AC-3

- **ac_ref**: AC-1, AC-3
- **dec_ref**: DEC-0076 §5 (optional fixtures)
- **description**: Add `tests/fixtures/triad_arch_headings/` with minimal markdown fixtures: `##`-only multi-section file; mixed H1+H2 same-id file. Consumed by self-test and/or contract tests. Optional per DEC-0076 but seeded for regression anchor stability.
- **files_affected**:
  - `tests/fixtures/triad_arch_headings/` (new)
- **parity_touchpoints**: Active-only (tests).
- **acceptance_check**:
  - `##`-only fixture enables rollover when artificially over line cap in test harness.
  - Mixed fixture asserts H1-wins single boundary for duplicate id.
  - Fixtures referenced by at least one automated test path.
- **status**: done

---

## T-008 — Runbook triad subsection — legacy `## US-` + remediation blurb — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0076 §7 (operator documentation)
- **description**: Ship verbatim remediation blurb from DEC-0076 §7 in `docs/engineering/runbook.md` triad hot-surface subsection (+ `template/docs/engineering/runbook.md` mirror). Covers legacy `## US-` rollover recognition, H1 mandate for new `/architecture` writes, optional `##`→`#` normalization guidance.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md` (byte-identical remediation subsection)
- **parity_touchpoints**: DEC-0076 §6 row 3 (positive parity).
- **acceptance_check**:
  - Verbatim blurb text matches DEC-0076 §7 (mentions BUG-0010, legacy H2, H1 mandate, optional normalization).
  - Active/template runbook remediation strings byte-identical.
  - No internal planning tokens in operator-facing prose (**US-0071**).
- **status**: done

---

## T-009 — Architecture + DEC linkage assert (read-only) — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0076 §6; architecture `# BUG-0010` § Related
- **description**: Assert-only subtest verifying `docs/engineering/architecture.md` `# BUG-0010` references **DEC-0076**, **DEC-0054**, **DEC-0043**, **US-0017**, **US-0072**, **R-0076**, and documents dual-track fix + template parity inventory. No rewrite of architecture or DEC files.
- **files_affected**:
  - `tests/auto_command_contract_test.py` (assert-only subtest under `test_bug0010_*` or sibling)
- **parity_touchpoints**: Active-only (read-only assert).
- **acceptance_check**:
  - Subtest passes when required cross-refs present in `# BUG-0010`.
  - Subtest fails if H1-wins precedence table or diff-gated policy removed from architecture.
  - `decisions/DEC-0076.md` exists and status Accepted (read-only assert).
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — dual-level archiver core (+ template mirror)
2. **T-002** — heading policy functions + CLI hook (same script)
3. **T-003** — extended `--self-test` (depends T-001, T-002)
4. **T-004** — architecture command H1 mandate (+ template mirror)
5. **T-007** — optional fixtures (can parallel T-003)
6. **T-005** — contract tests (depends T-001..T-004)
7. **T-006** — harness §29A (depends T-003, T-005)
8. **T-008** — runbook remediation docs
9. **T-009** — linkage assert (last — after architecture stable)
