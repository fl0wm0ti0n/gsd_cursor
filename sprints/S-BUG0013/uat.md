# UAT — Sprint S-BUG0013

## Target

- **BUG-0013**: Scratchpad example stale — template example missing 9 sections written to canonical scratchpad
  - AC-1: `template/.cursor/scratchpad.local.example.md` byte-identical to canonical except header + local overrides
  - AC-2: Installer refreshes consumer's example from template on every install/upgrade
  - AC-3: New contract test `tests/scratchpad_example_parity_test.py` verifies sync
  - AC-4: Runbook § "Scratchpad example parity" documents fix
  - AC-5: `bug_issue_validate.py --check-acceptance` → `[BUG_VALIDATION_OK]`
  - AC-6: `intake_bug_resume_brief_refresh.py --bug-id BUG-0013 --validate-file` → PASS

## Executed verification steps and results

(placeholder — populated at /execute / /qa / /verify-work)
