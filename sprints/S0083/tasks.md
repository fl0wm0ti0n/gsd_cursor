# Sprint S0083 Tasks — US-0094

**sprint_id**: S0083  
**story_refs**: US-0094  
**governance**: architecture `# US-0094` + **R-0080** (no companion DEC; **DEC-0074** composed, not amended)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**bijection**: AC-1..AC-10 ↔ T-001..T-010 (strict 1:1)

> No README edits in this phase — dev owns narrative delivery in `/execute`.

---

## T-001 — Replace pre-`## Features` intro (3 ¶ discovery copy within word budget) — AC-1

- **ac_ref**: AC-1
- **arch_ref**: architecture `# US-0094` § Intro contract
- **description**: Replace generic tagline (lines 5–9) with discovery-locked 3 paragraphs before `## Features`: (1) operator as dreamer/customer + role-based AI team; (2) artifact-first phased workflow `/intake`→`/release` + pause/resume/decision gates; (3) opt-in `AUTO_FLOW_MODE=full_autonomy` + outer driver + `/auto` backlog drain (**US-0092**, default-off pairing per **DEC-0078**). Stay within 120–210 words soft / 240 hard max; ≤80 words per ¶; no 4th paragraph or intro bullet list.
- **files_affected**:
  - `README.md` (intro zone only)
- **parity_touchpoints**: Byte-copy to `template/README.md` in T-005 (US-0017).
- **acceptance_check**:
  - Exactly 3 non-blank paragraphs before `## Features`.
  - Total intro word count ≤ 240 (target 120–210).
  - Paragraph semantics match discovery lock (dreamer, artifacts, full autonomy opt-in).
  - Optional ≤1-sentence DEV shard cross-link (≤25 words) in ¶2 or ¶3 only.
- **status**: done

---

## T-002 — Insert 4 pillar `###` sections with id-free teaser bullets under `## Features` — AC-2

- **ac_ref**: AC-2
- **arch_ref**: architecture `# US-0094` § Pillar contract
- **description**: Under existing `## Features (what its-magic can do)`, insert four `###` pillars with **exact discovery titles**: **Autonomous AI workflow** · **Quality & verification gates** · **Distribution & install** · **Operator control & ergonomics**. Each pillar gets 3–6 id-free teaser bullets (commands/flags/outcomes by name; no `US-xxxx`/`BUG-xxxx` lines). Optional one-line cross-link per pillar to catalog block in parent H2 (navigation only). No new `##` H2 literals.
- **files_affected**:
  - `README.md` (Features subsection — pillars before first catalog block)
- **parity_touchpoints**: Byte-copy to `template/README.md` in T-005.
- **acceptance_check**:
  - Four pillar `###` titles match discovery lock exactly.
  - Each pillar has 3–6 teaser bullets; bullets are id-free.
  - No encyclopedic duplication of catalog prose.
  - Existing three `<!-- readme-feature-coverage-catalog -->` markers untouched in parent H2s.
- **status**: done

---

## T-003 — Verify deep body sections preserved (Setup, How-to, Commands, walkthroughs, etc.) — AC-3

- **ac_ref**: AC-3
- **arch_ref**: architecture `# US-0094` § Information architecture diagram (preserved subtree)
- **description**: After T-001/T-002 edits, confirm all substantive pre-change sections remain present below the new hierarchy: `## Setup`, `## How-to`, `## Commands and workflow`, walkthroughs, scratchpad reference, quality chain, contributing, etc. Relocation within affinity home allowed; silent deletion forbidden. Cross-H2 catalog moves forbidden.
- **files_affected**:
  - `README.md` (review — deep body below new tiers)
- **parity_touchpoints**: Preserved content included in T-005 byte-copy.
- **acceptance_check**:
  - Manual diff/review: no operator-facing detail section silently removed.
  - Three catalog blocks remain in affinity-home parent H2s (Features / Commands / Other useful capabilities).
  - Diataxis boundary preserved: Setup/How-to/walkthroughs retain procedural depth.
- **status**: done

---

## T-004 — Post-edit `validate_readme_feature_coverage.py --report` → zero gaps — AC-4

- **ac_ref**: AC-4
- **arch_ref**: architecture `# US-0094` § Execute workflow (gate 1)
- **description**: Run `python scripts/validate_readme_feature_coverage.py --repo . --report` after narrative edits. Assert `coverage_missing=[]` and `coverage_total=104` (baseline parity). Every in-scope US/BUG anchor from **US-0091** catalog remains detectable.
- **files_affected**:
  - `README.md` (read-only gate target)
  - `scripts/validate_readme_feature_coverage.py` (read-only — no changes)
- **parity_touchpoints**: N/A (gate only).
- **acceptance_check**:
  - `--report` exits 0.
  - JSON output: `coverage_missing=[]`.
  - `coverage_total` unchanged from baseline (104).
- **status**: done

---

## T-005 — Byte-copy `README.md` → `template/README.md` + identity check — AC-5

- **ac_ref**: AC-5
- **arch_ref**: architecture `# US-0094` § Execute workflow (gate 4); **US-0017**
- **description**: After T-001/T-002 content is final and gates T-004/T-006/T-007 pass on root copy, byte-copy root `README.md` to `template/README.md`. Verify identity with `fc` (Windows) or `cmp` (Unix). Single-source edit workflow — no independent template edits.
- **files_affected**:
  - `template/README.md` (byte-identical copy from root)
- **parity_touchpoints**: Root ↔ template README byte-identical (**US-0017**).
- **acceptance_check**:
  - `diff README.md template/README.md` is empty (or `fc` reports no differences).
  - SHA-256 of both files equal.
  - No drift introduced after copy.
- **status**: done

---

## T-006 — `validate_doc_profile.py` pass (H2 budget unchanged) — AC-6

- **ac_ref**: AC-6
- **arch_ref**: architecture `# US-0094` § Pillar contract (no new H2); § Execute workflow (gate 2); **DEC-0059**
- **description**: Run `python scripts/validate_doc_profile.py` on post-edit README. Confirm existing `USER_*` H2 vocabulary preserved; H2 count within `both`×`balanced` budget (8 H2); only new headings are four `###` pillars under Features.
- **files_affected**:
  - `README.md` (read-only gate target)
  - `scripts/validate_doc_profile.py` (read-only)
- **parity_touchpoints**: N/A (gate only).
- **acceptance_check**:
  - `validate_doc_profile.py` exits 0 for active profile cell.
  - No new `##` H2 literals introduced.
  - Section budgets not exceeded.
- **status**: done

---

## T-007 — `check-user-visible-metadata.py` pass on changed README paths — AC-7

- **ac_ref**: AC-7
- **arch_ref**: architecture `# US-0094` § Execute workflow (gate 3); **US-0071**
- **description**: Run `python scripts/check-user-visible-metadata.py` on changed README surfaces (root + template after T-005). Fix any planning-token leakage in intro/pillar blurbs.
- **files_affected**:
  - `README.md`, `template/README.md` (content review/fix only if scanner fails)
- **parity_touchpoints**: Root ↔ template remain byte-identical after any fixes.
- **acceptance_check**:
  - `check-user-visible-metadata.py` exits 0 on root and template README paths.
  - No sprint ids, orchestrator tokens, or internal phase names in operator blurbs.
- **status**: done

---

## T-008 — Full-autonomy placement audit (intro ¶3 + P1 + catalog tertiary) — AC-8

- **ac_ref**: AC-8
- **arch_ref**: architecture `# US-0094` § Intro contract ¶3; § Pillar contract (P1 placement); **DEC-0078**
- **description**: Audit full-autonomy messaging is not appendix-only: (1) intro ¶3 primary — continuous `/auto`, backlog/bug drain, self-verify UAT in operator language with default-off opt-in; (2) P1 pillar bullet secondary; (3) existing **US-0092** catalog line in Commands affinity tertiary. No overclaim vs scratchpad default-off.
- **files_affected**:
  - `README.md` (intro ¶3 + P1 pillar bullets)
- **parity_touchpoints**: Included in T-005 byte-copy.
- **acceptance_check**:
  - Intro ¶3 names `AUTO_FLOW_MODE=full_autonomy` with default-off pairing.
  - P1 pillar includes `/auto` + outer-driver teaser.
  - Full-autonomy value prop appears above deep engineering-only sections.
  - **DEC-0078** compliance (opt-in language mandatory).
- **status**: done

---

## T-009 — Regression guards — US-0017 / readme-feature-coverage contract tests green — AC-9

- **ac_ref**: AC-9
- **arch_ref**: architecture `# US-0094` § Execute workflow; existing US-0017 / coverage contract tests
- **description**: Run existing **US-0017** template-drift and readme-feature-coverage contract tests. Confirm no weakening of **US-0030** delta-gate surfaces. Fix only if regression introduced by README edits (unlikely if parity workflow followed).
- **files_affected**:
  - `tests/` (read-only gate — dev runs relevant contract subtests)
- **parity_touchpoints**: N/A (test gate).
- **acceptance_check**:
  - US-0017 template-drift contract tests green.
  - Readme-feature-coverage contract tests green (if present in harness).
  - No edits to **US-0030** delta-gate command surfaces.
- **status**: done

---

## T-010 — DEV shard body unchanged; optional ≤1-sentence cross-link in intro only — AC-10

- **ac_ref**: AC-10
- **arch_ref**: architecture `# US-0094` § Overview (edit surfaces)
- **description**: Confirm `docs/developer/README.md` body is unchanged vs pre-edit baseline. Optional single cross-link sentence in root intro (T-001) pointing implementers to DEV shard is allowed; no visionary intro duplication in DEV shard.
- **files_affected**:
  - `docs/developer/README.md` (read-only — no body edits)
  - `README.md` (optional cross-link in intro only — if used, covered in T-001)
- **parity_touchpoints**: DEV shard active-only (no template mirror per **DEC-0059**).
- **acceptance_check**:
  - `docs/developer/README.md` body diff vs pre-edit baseline is empty.
  - If intro cross-link present: ≤1 sentence, ≤25 words, in ¶2 or ¶3 only.
  - No regeneration of DEV shard visionary copy.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — intro rewrite (foundation)
2. **T-002** — four pillar `###` sections
3. **T-003** — deep-body preservation review
4. **T-008** — full-autonomy placement audit (during narrative review)
5. **T-004** — coverage `--report` gate
6. **T-006** — doc profile gate
7. **T-007** — metadata gate
8. **T-005** — byte-copy root → template + identity check (after gates pass on root)
9. **T-009** — regression contract tests
10. **T-010** — DEV shard unchanged confirmation (last)
