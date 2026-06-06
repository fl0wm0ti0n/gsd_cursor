# Sprint S0080

## Metadata

- **sprint_id**: S0080
- **bug_refs**: BUG-0011
- **goal**: Complete **US-0089** response-side Caveman delivery — append voice-compression directives to `.cursor/rules/caveman.mdc`, runbook level table, nine `test_caveman_voice_*` contract markers, intentional SHA baseline bump, harness **§30A**, operator UAT spot-check — per **DEC-0077** (composes on **DEC-0072**; **US-0090** orthogonal).
- **status**: planned
- **created_at**: 2026-06-06T16:43:29Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: tl-S0080-BUG0011-sprint-plan-20260606T164329Z-fresh

## Scope

- **BUG-0011**: Caveman mode missing voice compression rules — `CAVEMAN_MODE=1` does not produce terse replies (**US-0089** incomplete delivery)
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0011` (active-only); `# US-0089` §6 cross-link (architecture phase)
- **Binding decision**: `decisions/DEC-0077.md` (Accepted 2026-06-06)
- **Research anchor**: `docs/engineering/research.md` `R-0077`

## Non-goals (hard, from DEC-0077 §10)

- No Wenyan modes or vendor ~75% token claims.
- No `npx skills add` install path.
- No new skill under `.cursor/skills/`.
- No scratchpad key rename or new keys.
- No weakening of **DEC-0072** §4 nine-zone literal invariant.
- No change to `CAVEMAN_COMPRESS_INPUT` / deny-list / `scripts/caveman_compress_input.py`.
- No modification of `test_caveman_default_off_*` assertion bodies.
- No CI unit test of LLM voice quality (operator UAT spot-check only).
- No new `check_intake_template_parity.py` scope.
- **Status authority (US-0045)**: BUG-0011 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: **DEC-0077** (§1–§10); architecture `# BUG-0011`; research **R-0077**
- **Governance stack**: **US-0089** / **DEC-0072** (scaffolding, not rewritten), **US-0090** / **DEC-0073** (input compression orthogonal), **US-0017** (`caveman.mdc` byte parity), **US-0088** (non-suppressible gate vocabulary), **US-0045** (status authority), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof)

## Acceptance criteria coverage (AC-1..AC-8 → T-xxx; surjective, 8 tasks / 8 ACs)

| AC | Description (summary) | Task(s) | DEC-0077 § |
|----|-----------------------|---------|------------|
| AC-1 | Voice section outline in `caveman.mdc` | T-001, T-008 | §2, §3, §8 |
| AC-2 | Template byte parity for `caveman.mdc` | T-001 | §1, §9 |
| AC-3 | User-rule `### Precedence` subsection | T-001 | §2 row 1 |
| AC-4 | Ultra defers to 9-zone (no duplicate list) | T-001 | §2 row 6 |
| AC-5 | `test_caveman_voice_*` + SHA baseline bump | T-003, T-004 | §4, §5 |
| AC-6 | Runbook voice levels (US-0090 untouched) | T-002 | §7 |
| AC-7 | `test_caveman_default_off_*` bodies preserved | T-006 | §4 invariants |
| AC-8 | Harness **§30A** + operator voice UAT | T-005, T-007 | §6, §10 |

**Multi-AC tasks** (justified by architecture `# BUG-0011` § Atomic task seeds): **T-001** (AC-1+AC-2+AC-3+AC-4). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 8
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (8 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-8 coverage; **not** strict 1:1 bijection (T-001 spans four ACs; T-003/T-004 share AC-5; T-005/T-007 share AC-8)

## Governance

- **DEC-0077** §1–§10 (binding) — each task cites governing §(s).
- **R-0077** (research anchor).
- **DEC-0072** forward-link only — `test_caveman_default_off_*` bodies frozen.
- **US-0045** canonical status authority (BUG-0011 stays OPEN through this sprint).

## Template parity plan (DEC-0077 §9)

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `.cursor/rules/caveman.mdc` | `template/.cursor/rules/caveman.mdc` | T-001 | Positive (byte-identical after voice append) |
| 2 | `docs/engineering/runbook.md` (Caveman subsection) | `template/docs/engineering/runbook.md` | T-002 | Positive (`#### Voice compression levels` only) |

**Active-only** (no `template/` mirror; intentional per DEC-0077 §9):

- `docs/engineering/architecture.md` `# BUG-0011`, `# US-0089` §6 cross-link
- `tests/auto_command_contract_test.py` extensions (`test_caveman_voice_*`, SHA bump)
- `tests/run-tests.ps1` + `tests/run-tests.sh` §30A
- `sprints/S0080/uat.md` / `uat.json` (operator voice spot-check)

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** add new `check_intake_template_parity.py` scope.
- Do **not** modify `scripts/caveman_compress_input.py` or `CAVEMAN_COMPRESS_INPUT` semantics.
- Do **not** modify `test_caveman_default_off_*` assertion bodies.
- Do **not** duplicate 9-zone literal list in voice section (pointer stub only).

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Voice rule delivery (T-001, T-002)

- Append `## Voice compression (when CAVEMAN_MODE=1)` + six subsections per DEC-0077 §2
- Pre-voice scaffolding blocks preserved verbatim
- Active / template `caveman.mdc` SHA-256 equal post-delivery

### Contract tests (T-003, T-004, T-006)

- Nine additive `test_caveman_voice_*` subtests (token-presence markers)
- Bump `_CAVEMAN_RULE_BASELINE_SHA256` in `test_caveman_compress_input_rule_byte_identity` to post-voice digest
- Assert `test_caveman_default_off_*` bodies byte-unchanged (regression guard)

### Harness (T-005)

- New section **§30A** in `tests/run-tests.ps1` + `tests/run-tests.sh`
- Scope: `pytest -k caveman_voice` (or equivalent prefix filter)
- Additive — existing caveman harness blocks unchanged

### Operator UAT (T-007)

- Spot-check with `CAVEMAN_MODE=1` + `CAVEMAN_LEVEL=full`: visibly shorter prose; literals (reason codes, gate tokens) intact
- Qualitative brevity not CI-tested — documented in UAT

### Linkage assert (T-008)

- Read-only subtest: `# BUG-0011` references **DEC-0077**, **DEC-0072**, **R-0077**; `# US-0089` §6 cross-link present

## Risks and mitigations (DEC-0077 §Risks)

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | US-0090 SHA pin break | T-004 intentional baseline bump + release-note callout |
| R2 | Literal garbling under `ultra` | T-001 §6 pointer stub; unchanged 9-zone MUST |
| R3 | User-rule conflict | T-001 `### Precedence` paragraph |
| R4 | Ultra abbreviates reason codes | Forbidden by existing invariant; T-001 stub defers |
| R5 | Runbook vs rule drift | T-002 summary table only; rule normative |
| R6 | Accidental edit to DEC-0072 pinned tests | T-006 regression guard on `test_caveman_default_off_*` bodies |

## Definition of done (sprint-plan → plan-verify → execute → qa → verify-work → release)

- All 8 acceptance criteria covered by T-001..T-008 (surjective; no gaps).
- `sprints/S0080/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_gap=false`, `task_count=8`, `within_limit=true`.
- Nine `test_caveman_voice_*` subtests green; harness **§30A** green; `test_caveman_default_off_*` bodies unchanged.
- Positive-parity byte equality across DEC-0077 §9 inventory rows 1–2.
- Operator UAT spot-check documents visibly shorter prose under `CAVEMAN_MODE=1`.
- `docs/product/backlog.md` **`### BUG-0011`** retains **`OPEN`** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S0080`** / **BUG-0011** — verify AC-1..AC-8 surjective coverage, task-count bound, governance alignment. Target: `sprints/S0080/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
