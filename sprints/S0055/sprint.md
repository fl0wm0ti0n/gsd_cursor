# Sprint S0055

- Story: `US-0076`
- Goal: wire **merged scratchpad** (**`DEC-0055`**) into **`scripts/validate-and-push.ps1`** and **`scripts/validate-and-push.sh`** so **`SYNC_POLICY_MODE`**, **`ALLOW_AUTO_PUSH`**, **`SYNC_CUSTOM_PHASES`**, and **`AUTO_PUSH_BRANCH_ALLOWLIST`** **deterministically** gate an **opt-in** push path with **`DEC-0018` / `US-0038`** reason codes, bounded **`qa-findings.md`** scanning (**`DEC-0058`** §6), cross-platform parity, operator docs (**`AC-7`**), regression tests (**`AC-8`**), and **`US-0071`**-safe output — per **`decisions/DEC-0058.md`**, architecture **`# US-0076`**, **`R-0053`**, and backlog **AC-1..AC-10**.
- Status: **plan-verified** (**`/plan-verify` PASS** 2026-03-27; ready for **`/execute`**)

## Scope

- **Default-off / manual-disabled** short-circuit with explicit **`SYNC_DISABLED`**, **`MANUAL_MODE_NO_AUTO`**, **`AUTO_PUSH_NOT_ENABLED`** (**AC-1**).
- **Merged scratchpad** evaluation for sync flags; **fail closed** on merge/parse errors with remediation (**AC-2**).
- **Runbook** test + optional lint/typecheck chain **before** any push attempt (**AC-3**).
- **Branch allowlist** match; **`BRANCH_NOT_ALLOWLISTED`** when blocked (**AC-4**).
- **QA-first / blocking scan** over **`sprints/S*/qa-findings.md`** per **`DEC-0058`** §6; **`PRE_QA_AUTOPUSH_FORBIDDEN`** where runbook-bound rule applies (**AC-5**).
- **PowerShell / shell parity** for scratchpad-driven gates (**AC-6**).
- **README** + **`template/`** + **runbook** operator scheduling guidance (**`AC-7`**).
- **Regression tests** in **`tests/run-tests.*`** (dry-run / fixtures / exit parity) (**AC-8**).
- **US-0071** hygiene on new/changed script stdout (**AC-9**).
- **Decision traceability**: **`DEC-0058`** linked from operator surfaces; executable vs policy-only deprecation documented (**AC-10**).
