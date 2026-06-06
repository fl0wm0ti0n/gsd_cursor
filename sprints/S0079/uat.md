# Sprint S0079 UAT — BUG-0010

- **Sprint**: `S0079`
- **Work item**: **BUG-0010** — dual-level architecture story headings + diff-gated H1 enforcement
- **DEC**: **DEC-0076**
- **Orchestrator run**: **auto-20260606-02**
- **Machine-readable**: `sprints/S0079/uat.json`
- **Status**: **populated** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **BUG-0010** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0079/qa-findings.md` (PASS)
- **verify_work_executed_at**: 2026-06-06T16:33:28Z
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0079-BUG0010-verify-work-20260606T163328Z-fresh`
- **verify_work_verdict**: **PASS** (8/8 UAT steps PASS; 0 FAIL; 0 SKIP)

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 8 |
| FAIL | 0 |
| SKIP | 0 |
| Total | 8 |

Verify-work verdict: **PASS**. Closure preflight: **PASS** (9/9 gates). Bug **BUG-0010** remains **OPEN** per **US-0045**.

## Preconditions

- Python 3.12+ available.
- DEC-0076 execute deliverables merged (dual-level archiver, policy CLI, harness §29A).
- Active + template mirrors for `enforce-triad-hot-surface.py` and architecture command.

## UAT steps

### UAT-1 — `## US-` backward-compat rollover (AC-1) — `verdict=PASS`

- **DEC-0076 §**: §1, §2, §5
- **Commands**: `--self-test` + `test_bug0010_triad_arch_headings_fixtures`
- **Expected**: H2-only story headings recognized for rollover.
- **Evidence**: verify-work independent re-run → `--self-test` exit 0; `h2_only_multi.md` fixture PASS.

### UAT-2 — H1 `# US-` non-regression (AC-2) — `verdict=PASS`

- **DEC-0076 §**: §1, §5
- **Command**: `python scripts/enforce-triad-hot-surface.py --self-test`
- **Expected**: Existing `# US-0001`/`# US-0002` fixture unchanged.
- **Evidence**: self-test exit 0; H1 non-regression class green.

### UAT-3 — Mixed-file H1-wins precedence (AC-3) — `verdict=PASS`

- **DEC-0076 §**: §2, §5
- **Commands**: `--self-test` + triad arch headings fixture subtest
- **Expected**: When same id has H1 and H2, H1 wins as single boundary.
- **Evidence**: mixed H1-wins self-test class exit 0; `mixed_h1_h2_same_id.md` PASS.

### UAT-4 — Diff-gated `ARCH_STORY_HEADING_LEVEL_INVALID` (AC-4) — `verdict=PASS`

- **DEC-0076 §**: §3, §4
- **Commands**: `--check-arch-heading-policy --baseline-h2-count 5` + `--self-test`
- **Expected**: Policy check passes at current baseline; H2 count increase fails with reason code.
- **Evidence**: policy CLI exit 0; enforcement-delta self-test class PASS.

### UAT-5 — `/architecture` command H1 mandate (AC-5) — `verdict=PASS`

- **DEC-0076 §**: §3, §6
- **Commands**: `test_bug0010_architecture_command_*` subtests (3)
- **Expected**: Step 9 documents H1 mandate, baseline capture, stop token; template parity.
- **Evidence**: 3 contract subtests PASS; active/template `architecture.md` SHA-256 match.

### UAT-6 — Self-test + contract + harness §29A (AC-6) — `verdict=PASS`

- **DEC-0076 §**: §5
- **Commands**: `--self-test` + `pytest -k bug0010`
- **Expected**: Self-test exit 0; 7 contract subtests PASS; harness §29A 5/5 PASS.
- **Evidence**: verify-work re-run → 7 passed / 16 subtests; `tests/report.md` §29A lines 816–820 all `[PASS]`.

### UAT-7 — `# BUG-` H1 rollover + script parity (AC-7) — `verdict=PASS`

- **DEC-0076 §**: §1, §6
- **Commands**: SHA-256 parity probe + `test_bug0010_script_template_parity_sha256`
- **Expected**: `# BUG-` in H1 pattern; active/template script byte-identical.
- **Evidence**: `script_match True`; parity subtest PASS.

### UAT-8 — Operator runbook remediation note (AC-8) — `verdict=PASS`

- **DEC-0076 §**: §7
- **Command**: `test_bug0010_runbook_remediation_parity`
- **Expected**: Verbatim DEC-0076 §7 blurb in runbook triad subsection (active + template).
- **Evidence**: contract subtest PASS; blurb at `runbook.md` line 506 (active + template).

## Closure preflight (9 gates — all PASS)

| Gate | Verdict | Evidence |
|------|---------|----------|
| `tasks_done` | PASS (9/9) | T-001..T-009 done per `sprints/S0079/tasks.md` |
| `ac_qa_pass` | PASS (8/8) | `sprints/S0079/qa-findings.md` §Per-AC verdicts |
| `ac_uat_pass` | PASS (8/8) | this UAT matrix |
| `plan_verify_status` | PASS | `sprints/S0079/plan-verify.json` status=PASS |
| `bug_validator` | `[BUG_VALIDATION_OK]` | verify-work independent re-run exit 0 |
| `parity` | PASS | `enforce-triad-hot-surface.py` + `architecture.md` command byte-identical active/template |
| `negative_parity` | PASS | `architecture.md` `# BUG-0010` active-only per DEC-0076 §6; no standalone validator added |
| `test_baselines_no_regression` | PASS | PS1 harness Pass=807/Fail=14 vs S0078 QA 802/14 (+5 pass from §29A; +0 fail) |
| `dec_invariants` | PASS | DEC-0076 §9 non-goals preserved; grandfathered `## US-` allowed; diff-gated enforcement only |

## Results summary

**8 / 8 PASS** — ready for **`/release`**. Bug **BUG-0010** stays **OPEN** until release closure per **US-0045**.
