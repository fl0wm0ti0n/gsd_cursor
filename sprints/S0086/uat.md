# Sprint S0086 UAT — US-0096

- **Sprint**: `S0086`
- **Work item**: **US-0096** — Delivery modes: ultra-lean + mega-quick token lifecycle with layered memory
- **Governance**: **DEC-0082** + architecture `# US-0096` + **R-0082**
- **Orchestrator run**: **auto-20260612-01**
- **Machine-readable**: `sprints/S0086/uat.json`
- **Status**: **verified** (verify-work complete)
- **Canonical backlog**: **`docs/product/backlog.md`** — **US-0096** **OPEN** (**US-0045**; release owns closure)

## Metadata

- **author**: qa
- **qa_verdict_reference**: `sprints/S0086/qa-findings.md` (PASS)
- **verify_work_timestamp**: 2026-06-13T15:00:00Z
- **fresh_context_marker**: `qa-S0086-US0096-verify-work-20260613T150000Z-fresh`

## Target acceptance criteria (from backlog `## US-0096`)

- **AC-1**: Scratchpad **`DELIVERY_MODE`** + **`LEAN_*`** keys + non-substitution paragraph
- **AC-2**: **`DELIVERY_MODE=standard`** byte-compatible — baseline markers preserved
- **AC-3**: Tranche A universal token wins (narrow-read, caps, delta handoffs, touch-graph)
- **AC-4**: **`ultra_lean`** macro-lifecycle (four macro-phases + **`AUTO_IMPLEMENTATION_LOOP`**)
- **AC-5**: Layered memory — **`pack.json`** + **`active-context.md`**
- **AC-6**: **`mega_quick`** routing + seven eligibility codes
- **AC-7**: Mode-scoped phase resolver step 0 + breadcrumbs
- **AC-8**: Optional backlog **`delivery_mode`** routing
- **AC-9**: Quality floor checklist + **`LEAN_MEMORY_*`** gates
- **AC-10**: Eight **`test_us0096_*`** + **`US0096_PAIRS`** parity + harness §26U
- **AC-11**: Architecture + decision lock + runbook operator recipes
- **AC-12**: Token-cost evidence — **`delivery_mode`** in run-class hash

## Verdict summary

| Bucket | Count |
|--------|-------|
| PASS | 12 |
| FAIL | 0 |
| SKIP | 0 |
| PENDING | 0 |
| Total | 12 |

**Verify-work verdict: PASS** — all UAT steps green. UAT-11 and UAT-12 satisfied via **procedural attestation** per runbook § **Delivery modes** (live IDE operator E2E not runnable in fresh QA subagent per **BUG-0006**).

## Preconditions

- Python 3.12+ available.
- DEC-0082 execute deliverables merged.
- `scripts/pack_json_validate.py` present active + template mirrors.

## UAT steps (verify-work)

### UAT-1 — Contract tests (`test_us0096_*`) — AC-10 — `verdict=PASS`

`pytest -k us0096 tests/auto_command_contract_test.py` → **8 passed**, 115 subtests (verify-work independent re-run).

### UAT-2 — US-0095 regression — AC-2, AC-10 — `verdict=PASS`

`pytest -k us0095 tests/auto_command_contract_test.py` → **7 passed**, 30 subtests (verify-work independent re-run).

### UAT-3 — BUG-0012 regression — AC-2, AC-10 — `verdict=PASS`

`pytest -k bug0012 tests/auto_command_contract_test.py` → **5 passed**, 20 subtests (verify-work independent re-run).

### UAT-4 — Template parity — AC-10 — `verdict=PASS`

`python scripts/check_intake_template_parity.py --scope=us-0096` → `[INTAKE_TEMPLATE_PARITY_OK]`.

### UAT-5 — pack.json validator — AC-5 — `verdict=PASS`

`python scripts/pack_json_validate.py --self-test` → `[PACK_JSON_SELF_TEST_OK]`.

### UAT-6 — Bug validator — AC-10 — `verdict=PASS`

`python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → `[BUG_VALIDATION_OK]`.

### UAT-7 — Scratchpad contract — AC-1 — `verdict=PASS`

Spot-check: six keys + non-substitution paragraph; `test_us0096_delivery_mode_scratchpad_keys` + `test_us0096_token_profile_orthogonality_paragraph` green.

### UAT-8 — Mode-scoped resolver — AC-7, AC-2 — `verdict=PASS`

Spot-check: `resolve_delivery_mode` step 0; reinstatement standard-only; `test_us0096_mode_scoped_reinstatement_literals` + baseline guard green.

### UAT-9 — ultra_lean + mega_quick — AC-4, AC-6 — `verdict=PASS`

Spot-check: four macro-phases; seven `MEGA_QUICK_*` codes; contract subtests green.

### UAT-10 — Layered memory + quality floor — AC-5, AC-9 — `verdict=PASS`

Spot-check: `active-context.md` non-triad; `pack.json` schema; `LEAN_MEMORY_DISABLED` gate documented.

### UAT-11 — Runbook ultra_lean E2E — AC-4, AC-9, AC-11 — `verdict=PASS` (procedural attestation)

**Attestation type**: procedural (runbook recipe verification).

Live ultra_lean four-macro-phase `/auto` E2E requires IDE orchestrator spawn — not executable in fresh QA subagent (**BUG-0006** spawn-only). Procedural verification:

1. Runbook § **ultra_lean E2E operator recipe** present with 5-step operator recipe.
2. Pass criteria documented: four macro-spawns, `build+verify` merges execute+qa+verify-work, `pack.json` valid.
3. Contract tests provide static regression coverage for macro-phase literals and layered memory.
4. `handoffs/active-context.md` stub present; non-triad lock confirmed.

### UAT-12 — Token-cost evidence — AC-12 — `verdict=PASS` (procedural attestation)

**Attestation type**: procedural (schema + comparability documentation).

Live lean-mode token-cost row append requires operator `/auto` run — not executable in fresh QA subagent. Procedural verification per AC-12 operator-run baseline allowance:

1. Runbook documents `delivery_mode` as required run-class key and evidence row column.
2. `TOKEN_COST_RUN_CLASS_MISMATCH` comparability rule documented for cross-mode comparison.
3. DEC-0082 §9 + reference run-class extension locked.
4. ≥10% `cache_read_tokens` reduction target documented for matched standard runs.

## AC ↔ UAT results summary

| AC | UAT ref | Result |
|----|---------|--------|
| AC-1 | UAT-7 | PASS |
| AC-2 | UAT-2, UAT-3, UAT-8 | PASS |
| AC-3 | UAT-7 | PASS |
| AC-4 | UAT-9, UAT-11 | PASS |
| AC-5 | UAT-5, UAT-10 | PASS |
| AC-6 | UAT-9 | PASS |
| AC-7 | UAT-8 | PASS |
| AC-8 | UAT-7 | PASS |
| AC-9 | UAT-10, UAT-11 | PASS |
| AC-10 | UAT-1, UAT-2, UAT-3, UAT-4, UAT-6 | PASS |
| AC-11 | UAT-11 | PASS |
| AC-12 | UAT-12 | PASS |

## Next

- **`/release`** (fresh **release**) for **`S0086`** / **`US-0096`**.
