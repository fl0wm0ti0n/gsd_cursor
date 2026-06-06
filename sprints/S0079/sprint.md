# Sprint S0079

## Metadata

- **sprint_id**: S0079
- **bug_refs**: BUG-0010
- **goal**: Fix triad archiver blindness to `## US-xxxx` story headings — dual-level `STORY_HEADING_H1`/`H2` with H1-wins merge, diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` forward enforcement, extended `--self-test` + `test_bug0010_*` + harness **§29A**, architecture command H1 mandate, runbook remediation — per **DEC-0076** (composes on **DEC-0054** triad compaction + **DEC-0043** artifact ownership).
- **status**: planned
- **created_at**: 2026-06-06T17:00:00Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: tl-S0079-BUG0010-sprint-plan-20260606T170000Z-fresh

## Scope

- **BUG-0010**: triad archiver ignores `## US-xxxx` → `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` when `architecture.md` exceeds `ARCH_HOT_MAX_LINES`
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0010` (active-only)
- **Binding decision**: `decisions/DEC-0076.md` (Accepted 2026-06-06)
- **Research anchor**: `docs/engineering/research.md` `R-0076`

## Non-goals (hard, from DEC-0076 §9)

- No new standalone `validate_architecture_headings.py`.
- No static fail on any pre-existing `## US-` in file (diff-gated only).
- No `## BUG-` pattern in v1.
- No global markdownlint MD025 on entire `architecture.md`.
- No change to `state.md` or `po_to_tl.md` rollover semantics.
- No threshold key changes in scratchpad defaults (`ARCH_HOT_MAX_LINES`, `ARCH_HOT_MAX_STORY_SECTIONS`).
- No new `check_intake_template_parity.py` scope.
- No mandatory bulk `##`→`#` normalization in kit repo.
- **Status authority (US-0045)**: BUG-0010 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0076** (§1–§9); architecture `# BUG-0010`; research **R-0076**
- **Governance stack**: **US-0072** / **DEC-0054** (triad hot-surface), **DEC-0043** (history-preserving appends), **US-0017** (script mirror), **US-0061** (cross-phase ownership), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 9 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | DEC-0076 § |
|----|-----------------------|---------|------------|
| AC-1 | `## US-` backward-compat rollover | T-001, T-003, T-007 | §1, §2, §5 |
| AC-2 | H1 `# US-` non-regression | T-001, T-003 | §1, §5 |
| AC-3 | Mixed-file H1-wins precedence | T-001, T-003, T-007 | §2, §5 |
| AC-4 | Diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` | T-002, T-004 | §3, §4 |
| AC-5 | `/architecture` command H1 mandate + template parity | T-004, T-005, T-009 | §3, §6 |
| AC-6 | `--self-test` + `test_bug0010_*` + harness **§29A** | T-003, T-005, T-006 | §5 |
| AC-7 | `# BUG-` H1 rollover + script template parity | T-001 | §1, §6 |
| AC-8 | Operator runbook remediation note | T-008 | §7 |

**Multi-AC tasks** (justified by architecture `# BUG-0010` § Atomic task seeds): **T-001** (AC-1+AC-2+AC-3+AC-7), **T-003** (AC-1+AC-2+AC-3+AC-6), **T-004** (AC-4+AC-5), **T-005** (AC-5+AC-6), **T-007** (AC-1+AC-3). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 9
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (9 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **not** strict 1:1 bijection (8 ACs, 9 tasks per architecture seeds)

## Governance

- **DEC-0076** §1–§9 (binding) — each task cites governing §(s).
- **R-0076** (research anchor).
- **DEC-0054** §2 doc-only amendment (rollover read path vs authoring write path).
- **US-0045** canonical status authority (BUG-0010 stays OPEN through this sprint).

## Template parity plan (DEC-0076 §6)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `scripts/enforce-triad-hot-surface.py` | `template/scripts/enforce-triad-hot-surface.py` | T-001, T-002, T-003 | Positive (byte-identical) |
| 2 | `.cursor/commands/architecture.md` | `template/.cursor/commands/architecture.md` | T-004 | Positive (H1 mandate + policy step) |
| 3 | `docs/engineering/runbook.md` (triad subsection) | `template/docs/engineering/runbook.md` | T-008 | Positive (remediation blurb) |

**Active-only** (no `template/` mirror; intentional per DEC-0076 §6):

- `docs/engineering/architecture.md` `# BUG-0010`
- `tests/auto_command_contract_test.py` extensions
- `tests/fixtures/triad_arch_headings/` (if added)
- `tests/run-tests.ps1` + `tests/run-tests.sh` §29A

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** add new `check_intake_template_parity.py` scope.
- Do **not** add standalone `validate_architecture_headings.py`.
- Do **not** static-fail on grandfathered `## US-` sections.

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Archiver core (T-001, T-002, T-003)

- `python scripts/enforce-triad-hot-surface.py --self-test` → extended classes green
- Dual-level boundary scan + H1-wins merge filter
- `count_h2_story_headings` + `check_arch_heading_policy` → `ARCH_STORY_HEADING_LEVEL_INVALID` on count increase

### Command contract (T-004)

- `.cursor/commands/architecture.md` mandates H1 `# US-xxxx` / `# BUG-xxxx`
- Baseline capture + heading policy check in triad step 9

### Contract tests (T-005)

- Extend `tests/auto_command_contract_test.py` in place with `test_bug0010_*` prefix
- Command H1 mandate text; architecture linkage

### Harness (T-006)

- New section **§29A** in `tests/run-tests.ps1` + `tests/run-tests.sh`
- Additive — existing triad self-test block unchanged

### Fixtures (T-007, optional)

- `tests/fixtures/triad_arch_headings/` — `##`-only + mixed markdown minimal fixtures

### Runbook (T-008)

- Verbatim DEC-0076 §7 remediation blurb in triad subsection

## Risks and mitigations (DEC-0076 §Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Double-count H1+H2 same id | T-001 H1-wins filter (§2) |
| R2 | Split on inner `##` subheadings | T-001 strict `## US-\d{4}` regex only (§1) |
| R3 | Enforcement blocks legitimate subheadings | T-002 diff-gated policy (§3) |
| R4 | Template script drift | T-001/T-002/T-003 byte-identical active + `template/` commit (§6) |
| R5 | DEC-0054 §2 text drift | DEC-0076 §8 doc-only amendment; T-009 linkage assert |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered by T-001..T-009 (surjective; no gaps).
- `sprints/S0079/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_gap=false`, `task_count=9`, `within_limit=true`.
- `enforce-triad-hot-surface.py --self-test` green; harness **§29A** green.
- `##`-only fixture rollovers when over cap; `# US-` non-regression; mixed H1+H2 same-id single boundary.
- Positive-parity byte equality across DEC-0076 §6 inventory rows 1–3.
- `docs/product/backlog.md` **`### BUG-0010`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0079`** / **BUG-0010** — verify AC-1..AC-8 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0079/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
