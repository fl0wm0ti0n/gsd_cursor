# Sprint S0042 QA Findings

- Story: `US-0062`
- Sprint: `S0042`
- Result: PASS

## Verification

- Installer lifecycle tests validate:
  - fresh install writes `its_magic/.its-magic-version`,
  - upgrade keeps compatibility with legacy marker and migrates to canonical path,
  - clean-repo removes `its_magic/` while preserving non-framework marker content.
