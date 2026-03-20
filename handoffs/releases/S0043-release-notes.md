# Release Notes - S0043 (`US-0063`)

## What shipped

- Added OS-aware + stack-aware installer bootstrap for runbook command keys.
- Added deterministic command validation and fail-fast diagnostics:
  - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED`
  - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:<reason>`
- Preserved explicit user runbook command overrides on upgrade reruns.
- Updated installer/CLI help and runbook/README docs.
- Expanded regression coverage for bootstrap behavior.

## Operational notes

- Projects with detectable stack markers now receive concrete defaults during
  install/upgrade.
- If baseline command cannot be resolved, installer exits with remediation
  guidance instead of silent placeholder behavior.
