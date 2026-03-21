# Sprint S0053

- Story: `US-0074`
- Goal: restore a **fully green** consolidated test baseline by fixing the four known failing checks (Homebrew stable formula URL/version vs `package.json`, installer and CLI missing-install `TEST_COMMAND` bootstrap into materialized runbook), with **no assert weakening**, triple-installer + CLI parity, active/`template/` alignment, auditable QA/release evidence, and future regression guidance — per **`DEC-0056`**, architecture **`# US-0074`**, **`R-0051`**, and backlog AC-1..AC-10.
- Status: **released** (verify-work + release + refresh-context complete for **`S0053`**)

## Scope

- Deterministic root-cause classification for each baseline failure with owning paths (**AC-1**).
- Homebrew `packaging/homebrew/its-magic.rb` locked to npm-canonical version + tag URL (**AC-2**).
- `TEST_COMMAND` bootstrap for detectable stacks across `installer.ps1`, `installer.sh`, `installer.py`, and `bin/its-magic.js` per **`DEC-0046`** / **`DEC-0056`** (**AC-3**, **AC-5**).
- No regressions to upgrade/install ownership contracts (**US-0018**, **US-0057**, **US-0063**) (**AC-4**).
- Tests and QA evidence prove all four checks pass without masking (**AC-6**, **AC-7**, **AC-9**).
- Active + `template/` parity for formula, installers, runbook, validation scripts (**AC-8**).
- Operator-facing remediation guidance for future drift (**AC-10**).
