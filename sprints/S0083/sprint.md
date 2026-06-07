# Sprint S0083

## Metadata

- **sprint_id**: S0083
- **story_refs**: US-0094
- **goal**: Deliver README visionary intro + tiered feature hierarchy — rewrite root `README.md` opening (3 intro paragraphs + four pillar teasers under `## Features`), preserve catalog anchors and deep body sections, pass post-edit coverage/profile/metadata gates, and maintain root/template byte parity — per architecture `# US-0094` (composes on **DEC-0074**, **DEC-0059**, **US-0017**, **US-0092** / **DEC-0078**; research **R-0080**).
- **status**: planned
- **created_at**: 2026-06-07T13:30:00Z
- **orchestrator_run_id**: auto-20260607-01
- **fresh_context_marker**: tl-S0083-US0094-sprint-plan-20260607T133000Z-fresh

## Scope

- **US-0094**: README visionary intro + tiered feature hierarchy (root/template parity)
- **Architecture**: `docs/engineering/architecture.md` `# US-0094`
- **Binding governance**: discovery locks + **`R-0080`** Q1–Q4 (no companion **DEC-xxxx**; **DEC-0074** not amended)
- **Research anchor**: `docs/engineering/research.md` `R-0080`

## Non-goals (hard, from architecture `# US-0094`)

- No rewrite of **US-0091** validator semantics or **DEC-0074** predicate/gate wiring.
- No replacement of **DEC-0059** audience profiles or new `USER_*` H2 literals.
- No cross-H2 relocation of the three `### Feature coverage catalog (US-0091)` blocks.
- No regeneration of **`docs/developer/README.md`** body (**AC-10**).
- No new scripts, parity scopes, or release-gate wiring.
- No per-feature user guides (`USER_GUIDE_MODE` unchanged).
- **Status authority (US-0045)**: US-0094 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: architecture `# US-0094`; research **R-0080**; discovery/vision/backlog IA locks
- **Governance stack**: **US-0091** / **DEC-0074** (static coverage gate — re-run only), **US-0077** / **DEC-0059** (H2 budget), **US-0017** (root/template byte parity), **US-0092** / **DEC-0078** (full-autonomy messaging), **US-0071** (metadata hygiene), **US-0030** (delta gate — unchanged), **US-0045** (status authority)

## Acceptance criteria coverage (AC-1..AC-10 → T-xxx; strict bijection)

| AC | Description (summary) | Task | Architecture anchor |
|----|-----------------------|------|---------------------|
| AC-1 | Framework purpose lead (3 intro ¶) | T-001 | § Intro contract |
| AC-2 | Tiered hierarchy (4 pillar `###`) | T-002 | § Pillar contract |
| AC-3 | Detail preservation (deep body) | T-003 | § Information architecture diagram |
| AC-4 | Coverage re-audit (`--report` zero gaps) | T-004 | § Execute workflow (gate 1) |
| AC-5 | Root/template byte parity | T-005 | § Execute workflow (gate 4) |
| AC-6 | Audience profile compliance | T-006 | § Execute workflow (gate 2) |
| AC-7 | Metadata hygiene | T-007 | § Execute workflow (gate 3) |
| AC-8 | Full-autonomy messaging placement | T-008 | § Intro contract ¶3; § Pillar contract P1 |
| AC-9 | Regression guards green | T-009 | § Execute workflow; US-0017 / coverage tests |
| AC-10 | DEV shard unchanged | T-010 | § Overview (edit surfaces) |

**Bijection**: **AC-1..AC-10 ↔ T-001..T-010** (strict 1:1 per architecture `# US-0094` § Atomic task seeds). No `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 10
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (10 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Bijection**: **task_ac_bijection=true** (10 ACs, 10 tasks; 1:1 mapping)

## Governance

- Architecture `# US-0094` (binding) — each task cites governing §(s).
- **R-0080** (research anchor).
- **DEC-0074** composed (coverage re-audit only — not amended).
- **US-0045** canonical status authority (US-0094 stays OPEN through this sprint).

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `README.md` (intro + pillars) | `template/README.md` (byte-copy) | T-001, T-002, T-005 | Positive (byte-identical per **US-0017**) |

**Active-only** (read-only at execute):

- `docs/developer/README.md` (body unchanged — **AC-10**)
- `scripts/validate_readme_feature_coverage.py` (gate — read-only)
- `scripts/validate_doc_profile.py` (gate — read-only)
- `scripts/check-user-visible-metadata.py` (gate — read-only)
- `docs/engineering/context/readme-section-affinity.json` (affinity resolver — no moves)
- `tests/` (regression contract tests — read-only gate in T-009)

## Post-edit gate sequence (architecture § Execute workflow)

1. `python scripts/validate_readme_feature_coverage.py --repo . --report` → `coverage_missing=[]`
2. `python scripts/validate_doc_profile.py` → PASS for active profile cell
3. `python scripts/check-user-visible-metadata.py` → PASS on changed README paths
4. Root `README.md` === `template/README.md` (byte-identical)

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Narrative gates (T-001, T-002, T-003, T-008)

- Manual review: intro 3 ¶ within 120–210 soft / 240 hard max; four pillar exact titles; id-free teaser bullets; deep sections preserved; full-autonomy in intro ¶3 + P1 + catalog tertiary.

### Scripted gates (T-004, T-006, T-007)

- Coverage `--report`, `validate_doc_profile.py`, `check-user-visible-metadata.py` — all exit 0.

### Parity (T-005)

- Single-source edit on root `README.md`; byte-copy to `template/README.md`; `fc` / `cmp` identity check.

### Regression (T-009)

- Existing **US-0017** template-drift and readme-feature-coverage contract tests remain green.

### DEV shard (T-010)

- `docs/developer/README.md` body diff empty vs pre-edit baseline; optional ≤1-sentence intro cross-link only.

## Risks and mitigations (architecture § Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Pillar/catalog duplication | T-002 id-free teasers only; catalog remains authoritative |
| R2 | Affinity break on catalog relocation | T-003/T-004 forbid cross-H2 moves; `--report` gate |
| R3 | Intro bloat vs budgets | T-001 hard max 240 words / 3 ¶ |
| R4 | Active/template drift | T-005 single-source + byte-copy + identity check |
| R5 | Autonomy overclaim | T-008 default-off / opt-in pairing (**DEC-0078**) |
| R6 | Silent deletion of operator detail | T-003 manual review of preserved subtree |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 10 acceptance criteria covered 1:1 by T-001..T-010.
- `sprints/S0083/plan-verify.json` reaches **PASS** with `plan_integrity.task_ac_bijection=true`, `task_count=10`, `within_limit=true`.
- Post-edit gates 1–4 all pass before commit.
- `docs/product/backlog.md` **`## US-0094`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0083`** / **US-0094** — verify AC-1..AC-10 ↔ T-001..T-010 bijection, task-count bound, governance alignment. Target: `sprints/S0083/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
