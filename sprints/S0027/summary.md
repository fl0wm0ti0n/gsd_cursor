# Sprint S0027 Summary — US-0032 Optional Feature User Guide Generation

## Delivered

1. **T-001 (AC-1)** — Added `USER_GUIDE_MODE=0|1` (default 0) in `.cursor/scratchpad.md` and `template/.cursor/scratchpad.md`.
2. **T-002 (AC-2)** — Documented in intake, architecture, sprint-plan, execute, qa, and release (active + template) that when `USER_GUIDE_MODE=0` no required user-guide steps or blocking checks are added (zero overhead).
3. **T-003 (AC-3)** — Defined canonical location and naming: `docs/user-guides/US-xxxx.md` per feature story in runbook and `docs/user-guides/README.md` (active + template).
4. **T-004 (AC-4)** — Defined minimum required guide schema (Purpose, Prerequisites, Usage steps, Example, Limitations, Troubleshooting) in runbook and `docs/user-guides/README.md`.
5. **T-005 (AC-5)** — Added optional release gate step 3d: when `USER_GUIDE_MODE=1`, validate target-story user guide; block with reason code `USER_GUIDE_INCOMPLETE` when guide missing or required sections absent. Documented in release command (active + template) and runbook.
6. **T-006 (AC-6)** — Defined story ID → user guide artifact traceability; referenced in `.cursor/rules/handoffs.mdc` and runbook for handoff/release context (active + template).
7. **T-007 (AC-7)** — Documented boundaries with US-0031: user guides end-user only; no duplicate spec-pack content; separation in runbook and `docs/user-guides/README.md`.
8. **T-008 (AC-8)** — Aligned active and template: commands, runbook, README, `docs/user-guides/README.md`, handoffs.mdc; added regression assertions in `tests/run-tests.ps1` and `tests/run-tests.sh` for USER_GUIDE_MODE and USER_GUIDE_INCOMPLETE.

## Files changed (active)

- `.cursor/scratchpad.md` — USER_GUIDE_MODE flag
- `.cursor/commands/intake.md`, `architecture.md`, `sprint-plan.md`, `execute.md`, `qa.md`, `release.md` — user-guide steps and gate
- `.cursor/rules/handoffs.mdc` — user-guide traceability
- `docs/engineering/runbook.md` — Optional user-guide documentation mode (US-0032) section
- `docs/user-guides/README.md` — canonical path and schema
- `README.md` — Optional user-guide documentation (US-0032) subsection
- `tests/run-tests.ps1`, `tests/run-tests.sh` — US-0032 assertions

## Files changed (template)

- `template/.cursor/scratchpad.md` — USER_GUIDE_MODE flag
- `template/.cursor/commands/intake.md`, `architecture.md`, `sprint-plan.md`, `execute.md`, `qa.md`, `release.md` — same contracts
- `template/.cursor/rules/handoffs.mdc` — traceability
- `template/docs/engineering/runbook.md` — user-guide section
- `template/docs/user-guides/README.md` — path and schema
- `template/README.md` — user-guide subsection

## AC mapping

- AC-1 → T-001 (flag)
- AC-2 → T-002 (zero-overhead docs)
- AC-3 → T-003 (canonical path)
- AC-4 → T-004 (schema)
- AC-5 → T-005 (validation gate)
- AC-6 → T-006 (traceability)
- AC-7 → T-007 (US-0031 boundary)
- AC-8 → T-008 (parity + tests)

## Next

- Run `/qa` for S0027; then `/verify-work` and `/release` when gates pass.
