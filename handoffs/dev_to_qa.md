# Dev → QA Handoff (T-001..T-011) → QA COMPLETE

- **Phase**: execute → qa (handoff complete, QA verified)
- **Sprint**: S0112
- **Story**: US-0112 — Ship model-catalog example presets on install/upgrade
- **Executor (dev)**: dev (fresh subagent spawn) — execute PASS
- **Executor (qa)**: qa (fresh QA subagent spawn) — QA PASS
- **Handoff Timestamp**: 2026-06-30T23:00:00Z (dev→qa); 2026-06-30T23:15:00Z (QA complete)
- **Dev Verdict**: PASS (all 12 tests PASS, parity PASS, 12/12 guards VERIFIED)
- **QA Verdict**: PASS (QA_PASSED, 12/12 tests green, compose clean, template parity OK)
- **Sprint Status**: CLOSED

## Compose Guards (VERIFIED UNCHANGED)

- US-0008: installer CLI unchanged (no changes to release-all.sh or installer.py CLI arg parsing)
- US-0018: smart upgrade semantics unchanged (upgrade mode behavior preserved)
- US-0040: canonical release artifacts unchanged (no changes to release process)
- US-0054: publish confirmation gates unchanged (no changes to publish flow)
- US-0057: example-first refresh unchanged (existing scratchpad.example behavior preserved)
- US-0075: scratchpad example-first unchanged (scratchpad.local.example semantics unchanged)
- US-0100: version-scoped changelog unchanged (no changes to changelog logic)
- US-0101: per-phase model tier unchanged (no changes to model_tier.py)
- US-0102: model-catalog installer presets unchanged (US-0112 implements US-0102 contract)
- US-0103: AI decision ledger unchanged (no changes to decision_ledger.py)
- US-0107: sovereign loop mode unchanged (no changes to sovereign_loop.py)
- US-0110: goal-based convergence unchanged (no changes to convergence.py)

## Test Results

- **pytest us0112 markers**: 12/12 PASS
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK] scope=model-catalog-examples`
- **Test file**: tests/us0112_contract_test.py

## Files Modified

1. docs/engineering/context/installer-owned-paths.manifest (T-001: +8 rows)
2. template/docs/engineering/context/installer-owned-paths.manifest (T-002: +8 rows, byte-parity)
3. scripts/installer.py (T-003: added 8 examples to FRAMEWORK_EXACT)
4. scripts/installer.ps1 (T-004: added 8 examples to $frameworkExact)
5. scripts/installer.sh (T-005: added glob pattern for model-catalog examples)
6. scripts/check_intake_template_parity.py (T-006: added MODEL_CATALOG_EXAMPLE_PAIRS + --scope=model-catalog-examples)
7. template/docs/engineering/runbook.md (T-007: added Model-catalog Example Presets section)
8. tests/us0112_contract_test.py (T-008: 12 test markers)
9. docs/engineering/architecture.md (T-009: confirmed # US-0112 section)
10. template/docs/engineering/architecture.md (T-010: added # US-0112 section for byte-parity)
11. docs/engineering/runbook.md (T-008: added Model-catalog Example Presets section)

## Sprint Artifacts Updated

1. sprints/S0112/sprint.json (status=OPEN, all tasks DONE)
2. sprints/S0112/progress.md (T-001..T-011 completion notes)
3. sprints/S0112/summary.md (execute summary)
4. docs/engineering/state.md (execute checkpoint + isolation evidence)
5. handoffs/resume_brief.md (resume pointer for /qa)
6. handoffs/dev_to_qa.md (this handoff document)

## Next Phase

/qa (QA subagent spawn)
