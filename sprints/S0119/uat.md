# UAT Cycle 4 — S0119 / US-0119

## Isolation evidence

- phase_id=uat (merged into qa per ultra_lean)
- role=qa
- fresh_context_marker=qa-US0119-cycle4-qa-20260705T222729Z-fresh
- timestamp=2026-07-05T22:27:29Z
- orchestrator_run_id=auto-20260705-05

## Verdict: FAIL

10/12 UAT scenarios PASS, 2 FAIL (AC-5 consumer wiring partial, AC-10 tests+parity fail due to scratchpad parity regression + intake parity script mismatch).

## Failed UAT scenarios

### AC-5: Per-feature autonomy flags wired (PARTIAL)

- **Expected**: Each of the twelve flags in the preset expansion is documented AND consumed
- **Actual**: 6/8 consumer wiring checkpoints PASS. 2 FAIL:
  - sovereign_loop_lib.py has ZERO AUTONOMY_PRESET/AUTONOMY_STOP_POLICY matches
  - release_changelog_lib.py has ZERO AUTONOMY_PRESET/RELEASE_AUTO_CONFIRM matches
- **Remediation**: Wire autonomy preset expansion + stop policy dispatch into sovereign_loop_lib.py and release_changelog_lib.py

### AC-10: Tests + parity (FAIL)

- **Expected**: All pytest gates PASS + all parity checks PARITY_OK
- **Actual**: US-0119 tests 10/10 PASS. BUT:
  - scratchpad_example_parity_test.py 2/4 FAIL (BUG-0013 regression at line 181)
  - check_intake_template_parity.py default scope FAIL (20083b vs 19994b)
- **Remediation**: Sync scratchpad.local.example.md active<->template to byte-identity + copy check_intake_template_parity.py to template

## Runtime proof

- runtime_proof_id=rp-us0119-s0119-qa-cycle4-qa-2026-07-05T22:27:29Z
- proof_hash=f5f2abced05b6c2488a0142d913085ab4f84384b190f2b950457d1d0b9a2db33
