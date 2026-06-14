# Sprint S0087 UAT — US-0097

- **Sprint**: `S0087`
- **Work item**: **US-0097** — Project-owned root README bootstrap + per-story/sprint growth
- **Governance**: **DEC-0083** + architecture `# US-0097` + **R-0084**
- **Orchestrator run**: **auto-20260613-01**
- **Machine-readable**: `sprints/S0087/uat.json`
- **Status**: **verified** (verify-work PASS)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0097** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0087/qa-findings.md` (PASS)
- **qa_timestamp**: 2026-06-14T01:00:00Z
- **fresh_context_marker**: `qa-S0087-US0097-qa-20260614T010000Z-fresh`
- **verify_work_executed_at**: `2026-06-14T02:00:00Z`
- **verify_work_fresh_context_marker**: `qa-S0087-US0097-verify-work-20260614T020000Z-fresh`

## Target acceptance criteria (from backlog `## US-0097`)

- **AC-1**: Installer ownership — root **`README.md`** excluded from framework **`[install_paths]`**
- **AC-2**: Non-destructive migration **M1–M5** + sentinels **S1–S5**
- **AC-3**: Execute bootstrap scaffold when root missing/placeholder
- **AC-4**: Mandatory execute/release README delta per shipped **`US-xxxx`**
- **AC-5**: User + developer audience structure; framework catalog in **`its_magic/`** only
- **AC-6**: Split validators — **US-0091** → framework; project → root
- **AC-7**: Release **3g** + scratchpad **`PROJECT_README_ENFORCE`**
- **AC-8**: **US-0071** hygiene on project blurbs
- **AC-9**: Eight **`test_us0097_*`** + **`PROJECT_README_PAIRS`** parity + harness §26V
- **AC-10**: Architecture + runbook operator recipes

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 10 |
| FAIL | 0 |
| SKIP | 0 |
| PENDING | 0 |
| Total | 10 |

**Verify-work verdict: PASS** — all contract/regression UAT steps independently re-verified at `/verify-work` (10/10). UAT-10 satisfied via procedural attestation per runbook § **Project README coverage validation (US-0097 / DEC-0083)** operator recipes table.

## Preconditions

- Python 3.12+ available.
- DEC-0083 execute deliverables merged.
- `scripts/validate_project_readme_coverage.py` present active + template mirrors.

## UAT steps (verify-work verified)

### UAT-1 — Installer manifest — AC-1, AC-9 — `verdict=PASS`

`pytest -k us0097_installer_manifest` → root `README.md` excluded; `its_magic` retained.

### UAT-2 — Migration sentinels — AC-2 — `verdict=PASS`

`pytest -k us0097_placeholder` → S1–S5 + M1–M5 tables and reason codes present.

### UAT-3 — Execute step 23 — AC-3, AC-4, AC-8 — `verdict=PASS`

`pytest -k us0097_execute` → 23a bootstrap, 23b delta, 23c metadata hygiene literals.

### UAT-4 — Release step 3g — AC-4, AC-7 — `verdict=PASS`

`pytest -k us0097_release` → 3g after 3f order; `PROJECT_README_ENFORCE` gate.

### UAT-5 — Gate separation — AC-5, AC-6 — `verdict=PASS`

Framework validator → `its_magic/` only; project validator contract present.

### UAT-6 — Scratchpad keys — AC-7 — `verdict=PASS`

`PROJECT_README_ENFORCE=1`; active `FRAMEWORK_KIT_REPO=1`; template example `=0`.

### UAT-7 — Project validator self-test — AC-6, AC-9 — `verdict=PASS`

`python scripts/validate_project_readme_coverage.py --self-test` → `[PROJECT_README_COVERAGE_SELF_TEST_OK]`.

### UAT-8 — Template parity — AC-9 — `verdict=PASS`

`python scripts/check_intake_template_parity.py --scope=project-readme` → `[INTAKE_TEMPLATE_PARITY_OK]`.

### UAT-9 — US-0091 regression — AC-6, AC-9 — `verdict=PASS`

`pytest -k us0097_us0091` → release step 3f literals unchanged.

### UAT-10 — Runbook recipes — AC-10 — `verdict=PASS`

Runbook § **Project README coverage validation (US-0097 / DEC-0083)** operator recipes table present.

## AC ↔ UAT results summary

| AC | UAT step(s) | Verdict |
|----|-------------|---------|
| AC-1 | UAT-1 | PASS |
| AC-2 | UAT-2 | PASS |
| AC-3 | UAT-3 | PASS |
| AC-4 | UAT-3, UAT-4 | PASS |
| AC-5 | UAT-5 | PASS |
| AC-6 | UAT-5, UAT-7, UAT-9 | PASS |
| AC-7 | UAT-4, UAT-6 | PASS |
| AC-8 | UAT-3 | PASS |
| AC-9 | UAT-1, UAT-7, UAT-8, UAT-9 | PASS |
| AC-10 | UAT-10 | PASS |

## Next

- **`/release`** (fresh **release**) for **`S0087`** / **`US-0097`**.
