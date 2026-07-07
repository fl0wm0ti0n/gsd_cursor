# Sprint S-BUG0013

## Metadata

- **sprint_id**: S-BUG0013
- **bug_refs**: BUG-0013
- **goal**: Fix scratchpad-example-stale defect — sync `template/.cursor/scratchpad.local.example.md` from canonical `.cursor/scratchpad.md` (preserve example-header L1–L5, exclude project-local overrides), add parity test `tests/scratchpad_example_parity_test.py`, add runbook § "Scratchpad example parity" — per architecture `# BUG-0013` (research **R-0099**, no DEC required per R-0099 Q6).
- **status**: planned
- **created_at**: 2026-07-01T23:31:00Z
- **orchestrator_run_id**: auto-20260701-01
- **fresh_context_marker**: tl-SBUG0013-BUG0013-sprint-plan-20260701T233100Z-fresh
- **priority**: P3 (defect)
- **estimated_effort**: 1 day

## Scope

- **BUG-0013**: `template/.cursor/scratchpad.local.example.md` stale — 9 sections (lines 388–539 of canonical) missing.
- **Architecture**: `docs/engineering/architecture.md` `# BUG-0013`
- **Companion DEC**: none (R-0099 Q6 confirms packaging defect, no decision surface).
- **Research anchor**: `docs/engineering/research.md` `R-0099` (delivered, Q1–Q6 closed).

## Non-goals (hard, from architecture `# BUG-0013`)

- No modification of `.cursor/scratchpad.md` (canonical source, read-only).
- No modification of `installer.py`, `installer.ps1`, `installer.sh` (already correct per R-0099 Q2).
- No modification of any compose guard: **US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110** — all UNCHANGED.
- No new DEC record (pure packaging/parity fix).
- No data migration.
- **Status authority (US-0045)**: BUG-0013 stays **OPEN** throughout this sprint; closure at `/release`.

## Dependencies

- **Upstream (locked)**: architecture `# BUG-0013`; research **R-0099**.
- **Governance stack**: **US-0045** (status authority), **US-0017** (template parity), **US-0048** / **DEC-0029** (isolation), **US-0056** / **DEC-0038** (strict proof), **US-0088** (scratchpad merge precedence), **DEC-0055** (Model B catalog).

## Acceptance criteria coverage (AC-1..AC-6 → T-001..T-003; surjective)

| AC | Description (summary) | Task(s) | Architecture anchor |
|----|-----------------------|---------|---------------------|
| AC-1 | `template/.cursor/scratchpad.local.example.md` byte-identical to canonical except header + local overrides | T-001 | § Fix approach (A1) |
| AC-2 | Installer `materialize_scratchpad_example()` refreshes from template; manifest lists template as packaged source | T-001 (verify), already correct per R-0099 Q2 | § Fix approach (A2) |
| AC-3 | New contract test `tests/scratchpad_example_parity_test.py` verifies template/canonical sync | T-002 | § Fix approach (A3), § Test markers |
| AC-4 | Runbook § "Scratchpad example parity" documents fix + single-source-of-truth preference | T-003 | § Fix approach (A4) |
| AC-5 | `bug_issue_validate.py --check-acceptance` → `[BUG_VALIDATION_OK]` | T-001, T-002, T-003 | § Fix approach (A5) |
| AC-6 | `intake_bug_resume_brief_refresh.py --bug-id BUG-0013 --validate-file` → PASS | T-001, T-002, T-003 | § Fix approach (A5) |

**Task-AC mapping**: T-001 → AC-1 + AC-2; T-002 → AC-3 (+ AC-5/AC-6 validator enablement); T-003 → AC-4 (+ AC-5/AC-6 validator enablement). Every AC has ≥1 task; no `PLAN_AC_COVERAGE_GAP`.

## Task count

- **Total**: 3
- **SPRINT_MAX_TASKS**: 12 (from merged scratchpad)
- **Within limit**: yes (3 ≤ 12; `SPRINT_AUTO_SPLIT` not triggered)
- **Coverage**: surjective AC-1..AC-6 coverage; strict 1:1 task-to-seed (3 architecture seeds → T-001..T-003)

## Governance

- **Companion DEC**: none (per R-0099 Q6; packaging defect, no architectural decision surface).
- **R-0099** (research anchor, delivered Q1–Q6 closed).
- **US-0045** canonical status authority (BUG-0013 stays OPEN through this sprint).
- No compose guard amendments.

## Edit surfaces and parity plan

| # | Active path | Template path | Task | Parity |
|---|-------------|---------------|------|--------|
| 1 | `template/.cursor/scratchpad.local.example.md` | (this IS the template — target of sync from canonical) | T-001 | Primary sync target |
| 2 | `.cursor/scratchpad.local.example.md` | (repo-local copy — should mirror template) | T-002 (verify) | Mirror parity |
| 3 | `tests/scratchpad_example_parity_test.py` | (active-only) | T-002 | N/A — contract tests active-only |
| 4 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | T-003 | Positive (US-0017) |
| 5 | `docs/engineering/architecture.md` `# BUG-0013` | (active-only) | (already written at /architecture) | Linkage assert only |

**Active-only** (read-only or reference at execute):

- `docs/engineering/state.md` (sprint-plan checkpoint)
- `docs/product/backlog.md` (sprint_plan_notes append)
- `handoffs/resume_brief.md` (next-phase pointer)

**NEGATIVE parity (MUST NOT violate)**:

- Do **not** modify `.cursor/scratchpad.md` (canonical source).
- Do **not** modify `installer.py`, `installer.ps1`, `installer.sh`.
- Do **not** amend any of the 9 compose guards (US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110).

## Post-edit gate sequence

1. `pytest -k bug0013 tests/scratchpad_example_parity_test.py` → all three subtests green.
2. Verify `template/.cursor/scratchpad.local.example.md` contains all 9 section headers (US-0103..US-0111) from canonical.
3. Verify example-header (first 5 lines of template) unchanged.
4. Verify project-local overrides section NOT leaked into template.
5. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → `[BUG_VALIDATION_OK]`.
6. `python scripts/intake_bug_resume_brief_refresh.py --bug-id BUG-0013 --backlog docs/product/backlog.md --resume-brief handoffs/resume_brief.md --validate-file` → PASS.

## Test strategy summary (strategy locked for /execute; no test code in sprint-plan)

### Parity check (T-002, `test_bug0013_parity_check`)

- Template example must contain every feature-flag key and section header present in canonical `.cursor/scratchpad.md`.
- Diff-ignore: example-header (first 5 lines), project-local overrides section.
- 9 sections verified: US-0103, US-0110, US-0104, US-0105, US-0107, US-0106, US-0108, US-0109, US-0111.

### Header preserved (T-002, `test_bug0013_header_preserved`)

- First 5 lines of `template/.cursor/scratchpad.local.example.md` must match the example-only header documenting consumer-facing copy-to-local semantics.
- Header must NOT be overwritten by canonical content during sync.

### Local overrides preserved (T-002, `test_bug0013_local_overrides_preserved`)

- Project-local overrides section (operator-specific values at end of canonical scratchpad) must NOT be present in template example.
- Parity test asserts absence of local-override markers in template.

## Risks and mitigations

| ID | Risk | Sprint guard |
|----|------|--------------|
| R1 | Template example drifts again after fix | T-002 parity test enforces key/section parity on every CI run |
| R2 | Project-local overrides leak into template during sync | T-002 `test_bug0013_local_overrides_preserved` + explicit diff ignore-list |
| R3 | Example header overwritten by canonical content | T-002 `test_bug0013_header_preserved` asserts header intact |

## Definition of done

- All 6 acceptance criteria covered surjectively by T-001..T-003.
- `sprints/S-BUG0013/plan-verify.json` reaches **PASS** with `plan_integrity.ac_coverage_surjective=true`, `task_count=3`, `within_limit=true`.
- `pytest -k bug0013` green (3 subtests); `python scripts/bug_issue_validate.py` → `[BUG_VALIDATION_OK]`.
- `docs/product/backlog.md` `### BUG-0013` retains **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release`.

## Next

- **`/plan-verify`** (fresh **qa**) for **`S-BUG0013`** / **BUG-0013** — verify AC-1..AC-6 ↔ T-001..T-003 surjective coverage, task-count bound, governance alignment. Target: `sprints/S-BUG0013/plan-verify.json` `status` **`PENDING`** → **`PASS`**.
