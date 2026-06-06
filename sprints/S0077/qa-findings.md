# QA Findings — S0077 / US-0091 (cycle 1)

## Metadata

- **sprint_id**: S0077
- **story_id**: US-0091
- **dec_id**: DEC-0074 (composes on DEC-0059)
- **cycle**: 1
- **role**: qa
- **timestamp**: 2026-06-06T13:45:00Z
- **orchestrator_run_id**: auto-20260606-01
- **fresh_context_marker**: qa-S0077-US0091-qa-20260606T134500Z-fresh
- **inputs_reviewed**: `sprints/S0077/tasks.md`, `sprints/S0077/summary.md`, `sprints/S0077/plan-verify.json`, `handoffs/dev_to_qa.md`, `decisions/DEC-0074.md`, `docs/product/backlog.md` `## US-0091`, `docs/engineering/architecture.md` `# US-0091`, `docs/engineering/runbook.md`, `.cursor/commands/release.md`, `tests/run-tests.ps1` §27U.

## Overall verdict

**PASS** — All 10 ACs satisfied; harness §27U green; `coverage_missing: []` with `README_FEATURE_COVERAGE_ENFORCE=1`; zero regressions attributable to US-0091. Story **US-0091** remains **OPEN** per **US-0045** (closure at `/verify-work`).

- `ac_coverage`: AC-1..AC-10 = 10/10 PASS
- `regressions_found`: **none** (canonical harness Fail=9 unchanged vs US-0090 QA baseline; +11 pass from §27U additions only)
- `parity_verified`: true (`check_intake_template_parity.py --scope=readme-feature-coverage` → `[INTAKE_TEMPLATE_PARITY_OK]`)
- `bug_validator`: `[BUG_VALIDATION_OK]`
- `decision_gate_posture`: none required

## Test plan

| Step | Command / check | Expected | Result |
|------|-----------------|----------|--------|
| 1 | `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` | §27U green; no new harness failures vs prior baseline | **PASS** — Pass=802 / Fail=9 (`tests/report.md` Timestamp=2026-06-06T13:39:09Z) |
| 2 | `python scripts/validate_readme_feature_coverage.py --self-test` | `[README_FEATURE_COVERAGE_SELF_TEST_OK]` exit 0 | **PASS** |
| 3 | `python scripts/validate_readme_feature_coverage.py --repo . --report` | `status=PASS`, `coverage_missing=[]` | **PASS** — `coverage_total=98` |
| 4 | `python scripts/validate_readme_feature_coverage.py --repo . --enforce` | `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 | **PASS** |
| 5 | `python scripts/check_intake_template_parity.py --scope=readme-feature-coverage` | `[INTAKE_TEMPLATE_PARITY_OK]` | **PASS** |
| 6 | `python scripts/check-user-visible-metadata.py --repo .` | exit 0 | **PASS** |
| 7 | `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` | `[BUG_VALIDATION_OK]` | **PASS** |
| 8 | `python -m pytest tests/readme_feature_coverage_fixtures_test.py -q` | 3 passed | **PASS** (3 passed, 5 subtests) |
| 9 | Release step **3f** presence + scratchpad `README_FEATURE_COVERAGE_ENFORCE=1` | step wired; enforce active post-backfill | **PASS** |
| 10 | Report idempotence (harness + fixture) | byte-identical consecutive `--report` stdout | **PASS** |

## Per-AC verdicts (AC-1..AC-10)

### AC-1 — User-visible predicate — `verdict=PASS`

- **DEC-0074 §**: §1, §2 (H1–H8)
- **evidence_ref**: `scripts/readme_feature_coverage_lib.py` + template mirror; `--self-test` covers explicit true/false, H1 slash-command, H5 out, H6 operator-wins, H7 ambiguous story, H8 bug default-out; `README_FEATURE_COVERAGE_INPUT_INVALID` on ambiguous/malformed inputs; heuristic disabled when `README_FEATURE_COVERAGE_ENFORCE=1` (scratchpad confirms `=1`).

### AC-2 — Audit report — `verdict=PASS`

- **DEC-0074 §**: §5 (`--audit-out`, `--report` gaps)
- **evidence_ref**: `docs/engineering/context/readme-feature-coverage-audit.json` present; `--report` emits sorted gaps with `id`, `kind`, `predicate_source`, `root_h2`, `dev_h2`; repo `--report` shows `gaps=[]`.

### AC-3 — Three-file backfill — `verdict=PASS`

- **DEC-0074 §**: §3
- **evidence_ref**: `coverage_missing: []` with 98 in-scope items; root `README.md` + `docs/developer/README.md` populated; harness asserts scratchpad `README_FEATURE_COVERAGE_ENFORCE`; dev handoff confirms `user_visible:` markers on touched backlog blocks.

### AC-4 — Audience boundaries — `verdict=PASS`

- **DEC-0074 §**: §3, §4, §6
- **evidence_ref**: `docs/engineering/context/readme-section-affinity.json` + template mirror (`affinity_version=1`, five locked rules); `validate_doc_profile.py` PASS per dev handoff; no new H2 literals introduced.

### AC-5 — Validator CLI + reason codes — `verdict=PASS`

- **DEC-0074 §**: §5, §6
- **evidence_ref**: `scripts/validate_readme_feature_coverage.py` + template mirror; `--self-test` → `[README_FEATURE_COVERAGE_SELF_TEST_OK]`; sub-codes implemented (`README_FEATURE_COVERAGE_GAP:<id>`, `README_FEATURE_COVERAGE_PARITY_FAIL`, `README_FEATURE_COVERAGE_INPUT_INVALID`, `README_FEATURE_COVERAGE_PROFILE_VIOLATION`); umbrella `README_FEATURE_COVERAGE_BLOCKED` on stderr in blocking mode.

### AC-6 — Release gate composition — `verdict=PASS`

- **DEC-0074 §**: §7
- **evidence_ref**: `.cursor/commands/release.md` step **3f** documents `README_FEATURE_COVERAGE_ENFORCE` skip/enforce semantics; runbook subsection documents delta (US-0030) vs static (US-0091) remediation table; parity scope green.

### AC-7 — Idempotent `--report` + harness §27U — `verdict=PASS`

- **DEC-0074 §**: §5
- **evidence_ref**: Two consecutive `--report` runs byte-identical (harness §27U assertion); `report_schema_version=1`; sorted keys; `tests/fixtures/readme_feature_coverage/minimal/` + `tests/readme_feature_coverage_fixtures_test.py`; harness lines 805–815 all `[PASS]`.

### AC-8 — US-0071 metadata hygiene — `verdict=PASS`

- **DEC-0074 §**: §3 (root blurb preference)
- **evidence_ref**: `python scripts/check-user-visible-metadata.py --repo .` → exit 0 on README family surfaces.

### AC-9 — Template parity — `verdict=PASS`

- **DEC-0074 §**: §9
- **evidence_ref**: `check_intake_template_parity.py --scope=readme-feature-coverage` → `[INTAKE_TEMPLATE_PARITY_OK]`; `installer-owned-paths.manifest` lists both new scripts (active + template rows).

### AC-10 — Grandfathering + DEC linkage — `verdict=PASS`

- **DEC-0074 §**: §8, §AC-Traceability
- **evidence_ref**: `README_FEATURE_COVERAGE_ENFORCE=1` in `.cursor/scratchpad.md` post-backfill; `decisions/DEC-0074.md` documents predicate, US-0030 composition, grandfathering; linkage subtest `test_readme_feature_coverage_architecture_linkage` asserts `DEC-0074`, `US-0030`, `DEC-0059`, `US-0017`, `US-0071` in architecture `# US-0091` section.

## Canonical check-in baseline comparison

| Checkpoint | Pass | Fail | Notes |
|------------|------|------|-------|
| US-0090 QA (S0076) | 791 | 9 | Prior story QA baseline |
| **US-0091 QA (S0077)** | **802** | **9** | **+11 pass / 0 new fail** |

**Pre-existing Fail=9 (disjoint from US-0091)** — unchanged name set vs S0076 QA:

1. Homebrew stable formula URL uses npm version tag
2. Homebrew stable formula version matches npm version
3. Installer runbook TEST_COMMAND present (detectable stack)
4. CLI missing install runbook TEST_COMMAND present
5. scratchpad includes TOKEN_PROFILE (active)
6. auto includes strict-proof boundary step 11b (active)
7. auto includes strict-proof boundary step 11b (template)
8. scratchpad pair parity check passes on repo
9. slim auto command contract markers pass

**US-0091 harness additions (all PASS)**: validate_readme_feature_coverage.py exists; readme_feature_coverage_lib.py exists; fixtures test exists; scratchpad README_FEATURE_COVERAGE_ENFORCE; runbook docs (active + template); self-test; repo --report; report idempotent; parity scope; fixtures pass.

## Generated baseline test evidence (US-0066 / DEC-0048)

- `generated_test_stack_profile`: python (stdlib)
- `generated_test_command`: `python -m pytest tests/readme_feature_coverage_fixtures_test.py -q`
- `generated_test_result`: pass
- `generated_test_output_ref`: 3 passed, 5 subtests passed
- `generated_test_paths_ref`: `tests/readme_feature_coverage_fixtures_test.py`, `tests/fixtures/readme_feature_coverage/minimal/`
- `generated_test_reason_code`: (none — pass)

## Runtime QA evidence (US-0065)

Not applicable — docs/validator story; no application runtime startup required. `runtime_final_verdict=skipped`; `runtime_reason_code=N/A_DOCS_ONLY_STORY`.

## Blocking findings

None.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=qa-S0077-US0091-qa-20260606T134500Z-fresh`
- `timestamp=2026-06-06T13:45:00Z`
- `evidence_ref=sprints/S0077/qa-findings.md,handoffs/qa_to_verify_work.md,handoffs/resume_brief.md,docs/engineering/state.md,tests/report.md`

## Strict runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260606-01`
- `runtime_proof_id=rp-auto-20260606-01-qa-qa-20260606T134500Z-S0077-US0091`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-06T13:45:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=19925a6c2f331252cd8588753aa0f274e8080b7d8bc540339be2dc1ae54683c0`

Canonical payload: `{"orchestrator_run_id":"auto-20260606-01","phase_id":"qa","proof_issued_at":"2026-06-06T13:45:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260606-01-qa-qa-20260606T134500Z-S0077-US0091"}`.

## Next phase

**`/verify-work`** (fresh **qa** subagent) — US-0091 remains OPEN until verify-work closure per US-0045.
