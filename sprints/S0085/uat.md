# Sprint S0085 UAT — BUG-0012

- **Sprint**: `S0085`
- **Work item**: **BUG-0012** — `/auto` full_autonomy stops after each story despite native chain (US-0095 regression)
- **Governance**: **DEC-0081** + architecture `# BUG-0012` + **R-0083**
- **Orchestrator run**: **auto-20260612-01**
- **Machine-readable**: `sprints/S0085/uat.json`
- **Status**: **verified** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **BUG-0012** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0085/qa-findings.md` (PASS)
- **verify_work_timestamp**: 2026-06-13T00:15:00Z
- **fresh_context_marker**: `qa-S0085-BUG0012-verify-work-20260613T001500Z-fresh`

## Target acceptance criteria (from architecture `# BUG-0012`)

- **AC-1**: Orchestrator **MUST Task-spawn** mandate + actor distinction
- **AC-2**: Native chain precedence over US-0088 Option B
- **AC-3**: Drain-advance step 7 no-stop between steps 6–7
- **AC-4**: Continuation-truth breadcrumbs (`native_chain_continuing`, `drain_advance_action`)
- **AC-5**: Four **`test_bug0012_*`** contract subtests green
- **AC-6**: Forbidden-prose negative grep in full_autonomy normative blocks
- **AC-7**: **`resume_brief`** orchestrator spawn wording (**DEC-0069** pairing)
- **AC-8**: Runbook multi-segment operator E2E + template parity `--scope=bug-0012`

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 8 |
| FAIL | 0 |
| SKIP | 0 |
| PENDING | 0 |
| Total | 8 |

**Verify-work verdict: PASS** — all UAT steps green. UAT-8 satisfied via **procedural attestation** per runbook § **BUG-0012 regression verify** (live multi-segment `/auto` native-chain E2E not runnable in fresh QA subagent per **BUG-0006** spawn-only).

## Preconditions

- Python 3.12+ available.
- DEC-0081 execute deliverables merged.
- `scripts/auto_outer_driver.py` retained (optional fallback).

## UAT steps (verify-work)

### UAT-1 — Contract tests (`test_bug0012_*`) — AC-5 — `verdict=PASS`

`pytest -k bug0012 tests/auto_command_contract_test.py` → **5 passed**, 20 subtests (verify-work independent re-run).

### UAT-2 — US-0095 regression — AC-5 — `verdict=PASS`

`pytest -k us0095 tests/auto_command_contract_test.py` → **7 passed**, 30 subtests (verify-work independent re-run).

### UAT-3 — Template parity — AC-8 — `verdict=PASS`

`python scripts/check_intake_template_parity.py --scope=bug-0012` → `[INTAKE_TEMPLATE_PARITY_OK]`.

### UAT-4 — Orchestrator mandate + native precedence — AC-1, AC-2 — `verdict=PASS`

Spot-check: `auto.md` § Orchestrator post-subagent continuation mandate; literals present; Option B scoped to fallback.

### UAT-5 — Drain-advance + breadcrumbs — AC-3, AC-4 — `verdict=PASS`

Spot-check: step 6→7 no-stop; `native_chain_continuing` + `drain_advance_action` documented.

### UAT-6 — Forbidden-prose negative grep — AC-6 — `verdict=PASS`

`test_bug0012_forbidden_drain_stop_prose_negative_grep` green (verify-work re-run).

### UAT-7 — resume_brief spawn pairing — AC-7 — `verdict=PASS`

Spot-check: orchestrator **MUST Task-spawn** — not operator re-`/auto`.

### UAT-8 — Runbook operator E2E — AC-8 — `verdict=PASS` (procedural attestation)

**Attestation type**: procedural (runbook recipe verification).

Live multi-segment `/auto` native-chain drain-advance E2E requires IDE orchestrator spawn — not executable in fresh QA subagent (**BUG-0006** spawn-only). Procedural verification:

1. Runbook § **BUG-0012 regression verify** present with 6-step operator recipe.
2. Pass criteria documented: `drain_advance_action=spawned`, `native_chain_continuing=true`, `resume_brief` `story_id` advance, no forbidden terminal prose.
3. Contract tests (`test_bug0012_*`) provide static regression coverage for mandate literals, drain-advance no-stop, forbidden-prose negative grep, and DEC-0081 architecture linkage.
4. Template parity `--scope=bug-0012` confirms active/template mirror for runbook + auto.md surfaces.

## AC ↔ UAT results summary

| AC | UAT ref | Result |
|----|---------|--------|
| AC-1 | UAT-4 | PASS |
| AC-2 | UAT-4 | PASS |
| AC-3 | UAT-5 | PASS |
| AC-4 | UAT-5 | PASS |
| AC-5 | UAT-1, UAT-2 | PASS |
| AC-6 | UAT-6 | PASS |
| AC-7 | UAT-7 | PASS |
| AC-8 | UAT-3, UAT-8 | PASS |

## Next

- **`/release`** (fresh **release**) for **`S0085`** / **`BUG-0012`**.
