# Sprint S0077 UAT — US-0091

- **Sprint**: `S0077`
- **Work item**: **US-0091** — README ↔ backlog feature coverage backfill + blocking drift gate
- **DEC**: **DEC-0074** (composes on DEC-0059)
- **Orchestrator run**: **auto-20260606-01**
- **Machine-readable**: `sprints/S0077/uat.json`
- **Status**: **populated** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0091** **OPEN** (**US-0045**; release owns DONE flip)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0077/qa-findings.md` (PASS)
- **verify_work_executed_at**: 2026-06-06T13:40:48Z
- **verify_work_role**: qa
- **verify_work_fresh_context_marker**: `qa-S0077-US0091-verify-work-20260606T134048Z-fresh`
- **verify_work_verdict**: **PASS** (10/10 UAT steps PASS; 0 FAIL; 0 SKIP)

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 10 |
| FAIL | 0 |
| SKIP | 0 |
| Total | 10 |

Verify-work verdict: **PASS**. Closure preflight: **PASS** (9/9 gates). Story **US-0091** remains **OPEN** per **US-0045**.

## Preconditions

- Python 3.12+ available.
- Post-backfill merged scratchpad: `README_FEATURE_COVERAGE_ENFORCE=1`.
- Audit artifact: `docs/engineering/context/readme-feature-coverage-audit.json`.

## UAT steps

### UAT-1 — User-visible predicate (AC-1) — `verdict=PASS`

- **DEC-0074 §**: §1, §2 (H1–H8).
- **Command**: `python scripts/validate_readme_feature_coverage.py --self-test`
- **Expected**: exit 0; `[README_FEATURE_COVERAGE_SELF_TEST_OK]`; predicate matrix covers explicit true/false, H1, H5 out, H6 operator-wins, H7 ambiguous, H8 bug default-out.
- **Evidence**: `[README_FEATURE_COVERAGE_SELF_TEST_OK]` exit 0 (verify-work independent re-run).

### UAT-2 — Audit report (AC-2) — `verdict=PASS`

- **DEC-0074 §**: §5.
- **Commands**: audit artifact presence + `python scripts/validate_readme_feature_coverage.py --repo . --report`
- **Expected**: audit JSON present; `--report` `status=PASS`, `gaps=[]`.
- **Evidence**: `readme-feature-coverage-audit.json` present; `--report` → `coverage_total=98`, `coverage_missing=[]`, `gaps=[]`.

### UAT-3 — Three-file backfill (AC-3) — `verdict=PASS`

- **DEC-0074 §**: §3.
- **Command**: `python scripts/validate_readme_feature_coverage.py --repo . --report`
- **Expected**: `coverage_missing=[]` for all in-scope DONE items across root + template README + DEV shard.
- **Evidence**: 98 items in `coverage_present`; zero gaps; template byte parity per US-0017.

### UAT-4 — Audience boundaries (AC-4) — `verdict=PASS`

- **DEC-0074 §**: §3, §4, §6.
- **Commands**: affinity manifest presence + `validate_doc_profile.py`
- **Expected**: `readme-section-affinity.json` with five locked rules; doc profile PASS; no new H2 literals.
- **Evidence**: manifest present (active + template); `validate_doc_profile.py` PASS per execute/qa handoff.

### UAT-5 — Validator CLI + reason codes (AC-5) — `verdict=PASS`

- **DEC-0074 §**: §5, §6.
- **Commands**: `--self-test` + `--enforce`
- **Expected**: self-test OK token; enforce OK token; reason-code vocabulary complete.
- **Evidence**: `[README_FEATURE_COVERAGE_SELF_TEST_OK]`; `[README_FEATURE_COVERAGE_VALIDATE_OK]`; sub-codes GAP, PARITY_FAIL, INPUT_INVALID, PROFILE_VIOLATION.

### UAT-6 — Release gate composition (AC-6) — `verdict=PASS`

- **DEC-0074 §**: §7.
- **Check**: release step **3f** in `.cursor/commands/release.md`
- **Expected**: skip when `README_FEATURE_COVERAGE_ENFORCE=0`; blocking validator when `=1`; US-0030 delta gate unchanged.
- **Evidence**: step 3f at line 244 documents skip/enforce semantics; runbook delta-vs-static remediation table present.

### UAT-7 — Idempotent `--report` (AC-7) — `verdict=PASS`

- **DEC-0074 §**: §5.
- **Command**: two consecutive `--report` runs
- **Expected**: byte-identical stdout JSON; `report_schema_version=1`.
- **Evidence**: idempotent=PASS (verify-work re-run); harness §27U + fixtures test green.

### UAT-8 — US-0071 metadata hygiene (AC-8) — `verdict=PASS`

- **DEC-0074 §**: §3.
- **Command**: `python scripts/check-user-visible-metadata.py --repo .`
- **Expected**: exit 0 on README family.
- **Evidence**: `metadata_exit=0` (verify-work independent re-run).

### UAT-9 — Template parity (AC-9) — `verdict=PASS`

- **DEC-0074 §**: §9.
- **Command**: `python scripts/check_intake_template_parity.py --scope=readme-feature-coverage`
- **Expected**: `[INTAKE_TEMPLATE_PARITY_OK]` exit 0.
- **Evidence**: `[INTAKE_TEMPLATE_PARITY_OK] scope=readme-feature-coverage`; installer manifest rows for both scripts.

### UAT-10 — Grandfathering + DEC linkage (AC-10) — `verdict=PASS`

- **DEC-0074 §**: §8, §AC-Traceability.
- **Checks**: scratchpad `README_FEATURE_COVERAGE_ENFORCE=1`; `decisions/DEC-0074.md` present.
- **Expected**: enforce flipped post-backfill; DEC documents predicate, US-0030 composition, grandfathering.
- **Evidence**: scratchpad line 236 `README_FEATURE_COVERAGE_ENFORCE=1`; DEC-0074 accepted 2026-06-06; linkage subtest in fixtures.

## Results summary (trace to acceptance criteria)

| AC | UAT step(s) | Verdict | Evidence |
|----|-------------|---------|----------|
| AC-1 Predicate | UAT-1 | PASS | `--self-test` OK |
| AC-2 Audit | UAT-2 | PASS | audit JSON + `--report` gaps=[] |
| AC-3 Backfill | UAT-3 | PASS | coverage_missing=[] (98 items) |
| AC-4 Audience | UAT-4 | PASS | affinity manifest + doc profile |
| AC-5 Validator | UAT-5 | PASS | self-test + enforce OK |
| AC-6 Release gate | UAT-6 | PASS | release step 3f |
| AC-7 Idempotent report | UAT-7 | PASS | byte-stable consecutive `--report` |
| AC-8 US-0071 hygiene | UAT-8 | PASS | metadata scanner exit 0 |
| AC-9 Template parity | UAT-9 | PASS | scoped parity OK |
| AC-10 Grandfathering | UAT-10 | PASS | enforce=1 + DEC-0074 |

**UAT outcome**: **10 / 10 PASS** — ready for **`/release`**. Backlog status authority: **US-0091 OPEN** (US-0045).
