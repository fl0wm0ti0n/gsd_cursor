# QA Findings — S0079 / BUG-0010 (cycle 1)

## Metadata

- **sprint_id**: S0079
- **bug_id**: BUG-0010
- **dec_id**: DEC-0076 (composes on DEC-0054 + DEC-0043)
- **cycle**: 1
- **role**: qa
- **timestamp**: 2026-06-06T14:32:18Z
- **orchestrator_run_id**: auto-20260606-02
- **fresh_context_marker**: qa-S0079-BUG0010-qa-20260606T143218Z-fresh
- **inputs_reviewed**: `sprints/S0079/tasks.md`, `sprints/S0079/summary.md`, `sprints/S0079/plan-verify.json`, `handoffs/dev_to_qa.md`, `decisions/DEC-0076.md`, `docs/product/backlog.md` `### BUG-0010`, `docs/engineering/architecture.md` `# BUG-0010`, `tests/run-tests.ps1` §29A.

## Overall verdict

**PASS** — All 8 ACs (AC-1..AC-8) satisfied; harness **§29A** green; dual-level archiver self-test + `test_bug0010_*` contract + template parity verified; no regressions attributable to BUG-0010. Bug **BUG-0010** remains **OPEN** per **US-0045** (closure at `/release`).

- `ac_coverage`: AC-1..AC-8 = 8/8 PASS
- `regressions_found`: **none attributable to BUG-0010** (harness Fail=14 vs S0078 QA baseline Fail=14; +5 pass from §29A additions; all failures disjoint from DEC-0076 deliverables)
- `parity_verified`: true (active/template SHA-256 match for `enforce-triad-hot-surface.py` and `architecture.md` command; runbook remediation blurb present active + template)
- `bug_validator`: `[BUG_VALIDATION_OK]`
- `decision_gate_posture`: none required

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | §29A green; canonical report | **PASS** (harness exit 1 due to 14 pre-existing disjoint fails) — Pass=807 / Fail=14 (`tests/report.md` Timestamp=2026-06-06T14:31:49Z); §29A lines 816–820 all `[PASS]` |
| 2 | `python scripts/enforce-triad-hot-surface.py --self-test` | exit 0; H2-only rollover, mixed H1-wins, policy delta, inner `##` | **PASS** |
| 3 | `python -m pytest tests/auto_command_contract_test.py -q -k bug0010` | 7 passed | **PASS** (7 passed, 16 subtests) |
| 4 | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | **PASS** |
| 5 | `python scripts/enforce-triad-hot-surface.py --check-arch-heading-policy --baseline-h2-count 5` | exit 0 on current repo (no H2 increase) | **PASS** |
| 6 | `.cursor/commands/architecture.md` step 9 | H1 mandate + baseline capture + `ARCH_STORY_HEADING_LEVEL_INVALID` | **PASS** |
| 7 | Active/template script SHA-256 | byte-identical per DEC-0076 §6 | **PASS** |
| 8 | Runbook triad remediation blurb | verbatim DEC-0076 §7 active + template | **PASS** (contract subtest `test_bug0010_runbook_remediation_parity`) |
| 9 | `tests/fixtures/triad_arch_headings/` | H2-only + mixed fixtures | **PASS** (contract subtest `test_bug0010_triad_arch_headings_fixtures`) |
| 10 | Scope guards | no standalone validator; no static `## US-` fail; no new intake parity scope | **PASS** (dev handoff + sprint non-goals confirmed) |

## Per-AC verdicts (AC-1..AC-8)

### AC-1 — `## US-` backward-compat rollover — `verdict=PASS`

- **DEC-0076 §**: §1, §2, §5
- **evidence_ref**: `STORY_HEADING_H2` pattern; `--self-test` H2-only rollover class; `tests/fixtures/triad_arch_headings/h2_only_multi.md`.

### AC-2 — H1 `# US-` non-regression — `verdict=PASS`

- **DEC-0076 §**: §1, §5
- **evidence_ref**: `--self-test` existing `# US-0001`/`# US-0002` fixture unchanged; contract subtests green.

### AC-3 — Mixed-file H1-wins precedence — `verdict=PASS`

- **DEC-0076 §**: §2, §5
- **evidence_ref**: `split_arch_stories` H1-wins filter; `--self-test` mixed class; `tests/fixtures/triad_arch_headings/mixed_h1_h2_same_id.md`.

### AC-4 — Diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` — `verdict=PASS`

- **DEC-0076 §**: §3, §4
- **evidence_ref**: `count_h2_story_headings`, `check_arch_heading_policy`, `--check-arch-heading-policy`; `--self-test` enforcement-delta class; architecture command step 9 baseline capture.

### AC-5 — `/architecture` command H1 mandate + template parity — `verdict=PASS`

- **DEC-0076 §**: §3, §6
- **evidence_ref**: `test_bug0010_architecture_command_h1_mandate`, `test_bug0010_architecture_command_policy_stop_token`, `test_bug0010_architecture_command_baseline_policy_step`; active/template `architecture.md` SHA-256 match.

### AC-6 — `--self-test` + `test_bug0010_*` + harness §29A — `verdict=PASS`

- **DEC-0076 §**: §5
- **evidence_ref**: `--self-test` exit 0; `pytest -k bug0010` 7 passed; harness §29A (5 assertions) all PASS.

### AC-7 — `# BUG-` H1 rollover + script template parity — `verdict=PASS`

- **DEC-0076 §**: §1, §6
- **evidence_ref**: `STORY_HEADING_H1` includes `# BUG-`; `test_bug0010_script_template_parity_sha256` PASS; active/template script byte-identical.

### AC-8 — Operator runbook remediation note — `verdict=PASS`

- **DEC-0076 §**: §7
- **evidence_ref**: `test_bug0010_runbook_remediation_parity` PASS; verbatim DEC-0076 §7 blurb in `docs/engineering/runbook.md` triad subsection (+ template).

## Canonical check-in baseline comparison

| Checkpoint | Pass | Fail | Notes |
|------------|------|------|-------|
| BUG-0009 QA (S0078) | 802 | 14 | Prior bug QA baseline |
| **BUG-0010 QA (S0079)** | **807** | **14** | **+5 pass / +0 fail** (§29A additive assertions) |

**Fail=14 (all disjoint from BUG-0010 / DEC-0076)** — unchanged set vs S0078 QA: Homebrew formula (2), installer/CLI TEST_COMMAND (2), triad repo `--check` (2), scratchpad pair parity (1), slim auto contract markers (1), readme feature coverage repo report + idempotent (2), plus collateral from US-0090/US-0091/triad hot-surface growth.

**BUG-0010 harness additions (all PASS)**: `enforce-triad-hot-surface.py` exists; template mirror exists; active/template SHA-256 match; dual-level `--self-test`; `BUG-0010 contract subtests pass`.

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python (stdlib + pytest)
- `generated_test_command`: `python -m pytest tests/auto_command_contract_test.py -q -k bug0010`
- `generated_test_result`: pass
- `generated_test_output_ref`: 7 passed, 16 subtests passed
- `generated_test_paths_ref`: `tests/auto_command_contract_test.py` (`test_bug0010_*`)
- `generated_test_reason_code`: (none — pass)

## Runtime QA evidence (US-0065)

Not applicable — triad archiver / heading-policy story; no application runtime startup required. `runtime_final_verdict=skipped`; `runtime_reason_code=N/A_TRIAD_ARCHIVER_STORY`.

## Blocking findings

None.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0079-BUG0010-qa-20260606T143218Z-fresh`
- `timestamp=2026-06-06T14:32:18Z`
- `evidence_ref=sprints/S0079/qa-findings.md,handoffs/qa_to_verify_work.md,docs/engineering/state.md,tests/report.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260606-02`
- `runtime_proof_id=rp-auto-20260606-02-qa-qa-20260606T143218Z-S0079-BUG0010`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-06T14:32:18Z`
- `proof_ttl_seconds=3600`
- `proof_hash=82bff131201c2324e4dc7b408f8cbc04cd8c6e409084964eb81081272ba40e73`

Canonical payload: `{"orchestrator_run_id":"auto-20260606-02","phase_id":"qa","proof_issued_at":"2026-06-06T14:32:18Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260606-02-qa-qa-20260606T143218Z-S0079-BUG0010"}`.

## Next phase

**`/verify-work`** (fresh **qa** subagent) — BUG-0010 remains OPEN until verify-work + `/release` closure per US-0045.
