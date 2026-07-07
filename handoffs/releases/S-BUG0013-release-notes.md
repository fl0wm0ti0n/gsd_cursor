# Release Notes — S-BUG0013

## Summary

- **Sprint**: S-BUG0013
- **Bug**: BUG-0013 (scratchpad-example-stale)
- **Release date**: 2026-07-02
- **Orchestrator run**: auto-20260701-01
- **Release verdict**: PASS

Fixed scratchpad template synchronization by adding 9 missing sovereign-loop-era feature sections to `template/.cursor/scratchpad.local.example.md`. Template is now byte-identical to canonical `.cursor/scratchpad.md` (minus example-only header and project-local overrides). Added parity test and runbook recipe.

## Acceptance Criteria

- [x] AC-1: Template synced from canonical (byte-identical except header + project-local overrides)
- [x] AC-2: Installer correctly reads from template (pre-existing, no changes needed)
- [x] AC-3: Parity test written (4 tests, all PASS)
- [x] AC-4: Runbook section added ("Scratchpad example parity")
- [x] AC-5: bug_issue_validate.py passes ([BUG_VALIDATION_OK])
- [x] AC-6: intake_bug_resume_brief_refresh.py passes (with INFO-003 format drift note)

## Test Results

- 4/4 PASS (pytest tests/scratchpad_example_parity_test.py)
  - test_bug0013_parity_check: PASS
  - test_bug0013_header_preserved: PASS
  - test_bug0013_local_overrides_preserved: PASS
  - test_bug0013_active_example_mirror_in_sync: PASS

## Compose Guards

9/9 UNCHANGED: US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110

## Files Changed

1. `template/.cursor/scratchpad.local.example.md` — synced from canonical (+152 lines, 9 sovereign-loop-era sections)
2. `.cursor/scratchpad.local.example.md` — active mirror synced (mirror of template)
3. `tests/scratchpad_example_parity_test.py` — created (4 test markers)
4. `docs/engineering/runbook.md` — added § "Scratchpad example parity"
5. `template/docs/engineering/runbook.md` — synced BUG-0013 section from active

## Run

- `start_command`: `pytest tests/scratchpad_example_parity_test.py -v`
- `runtime_mode`: local
- `runtime_context_ref`: docs/engineering/runbook.md § "Scratchpad example parity"

## Connect

- `service_url`: N/A (framework kit repo, no service)
- `service_port`: N/A
- `health_endpoint`: N/A

## Verify

1. `pytest tests/scratchpad_example_parity_test.py -v` — all 4 tests PASS
2. `python scripts/check_intake_template_parity.py --scope=scratchpad-example` — [INTAKE_TEMPLATE_PARITY_OK]
3. `python scripts/bug_issue_validate.py --backlog docs/product/back.md --check-acceptance` — [BUG_VALIDATION_OK]

## Credentials

- N/A (no secrets required)

## Known Issues

None.

## Release Evidence

- Gate snapshot: tests=4/4 PASS, qa=PASS (6/6 ACs, 0 blockers), verify-work=PASS (6/6 ACs), isolation=PASS
- Strict runtime proofs: execute (rp-auto-20260701-01-execute-dev-20260701T232000Z-BUG0013), qa (rp-auto-20260701-01-qa-qa-20260702T003000Z-BUG0013), verify-work (rp-auto-20260701-01-verify-work-qa-20260702T004500Z-BUG0013)
- Compose guards: 9/9 UNCHANGED
- Discrepancies vs /qa: NONE
- Blocking findings: 0
- Non-blocking findings: 0

## Artifacts

- `sprints/S-BUG0013/summary.md`
- `sprints/S-BUG0013/qa-findings.md`
- `sprints/S-BUG0013/qa-verdict.json`
- `sprints/S-BUG0013/verify-work-verdict.json`
- `handoffs/resume_brief.md`
- `docs/engineering/state.md` (release checkpoint)
