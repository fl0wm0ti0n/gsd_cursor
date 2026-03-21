# Sprint S0053 Tasks

- Story: `US-0074`
- Sprint: `S0053`
- Governance: **`DEC-0056`** (baseline version-sync + `TEST_COMMAND` bootstrap); related **`DEC-0046`** (runbook command bootstrap precedence)

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Reproduce and **classify** each of the four failing baseline checks with deterministic root-cause notes and **owning artifact paths** (formula, installers, CLI, runbook, tests as applicable) | AC-1 |
| T-002 | done | Fix **Homebrew stable** `packaging/homebrew/its-magic.rb` so **URL tag** and Ruby **`version`** stay in lockstep with **`package.json` `version`** (and `sha256` integrity where required by release discipline) | AC-2 |
| T-003 | done | Fix **installer + CLI missing-install** paths so materialized `docs/engineering/runbook.md` **`TEST_COMMAND`** satisfies the baseline-allowed contract (`npm run test` \| `sh tests/run-tests.sh`) for **detectable stacks**, with deterministic diagnostics on failure | AC-3 |
| T-004 | done | Verify **no regression** to existing upgrade/install **ownership** contracts (**`US-0018`**, **`US-0057`**, **`US-0063`**) while changing bootstrap/version surfaces | AC-4 |
| T-005 | done | Ensure **cross-platform parity**: same logical bootstrap outcomes across `installer.ps1`, `installer.sh`, `installer.py`, and CLI wrapper / delegation per **`DEC-0056`** | AC-5 |
| T-006 | done | Adjust or extend **tests** only to assert corrected behavior — **no forced passes**, relaxed greps, or masked failures | AC-6 |
| T-007 | done | Close **QA** for this story with **zero** remaining failures from the **known four-check set**; record evidence in `sprints/S0053/qa-findings.md` | AC-7 |
| T-008 | done | Maintain **active/template parity** for Homebrew formula, installer scripts, runbook/bootstrap guidance, and consolidated validation scripts | AC-8 |
| T-009 | done | Update **release/readiness** artifacts with **auditable evidence** (e.g. `tests/report.md`, release notes pointers) that all four checks **pass** | AC-9 |
| T-010 | done | Document **deterministic remediation guidance** for future version-sync and `TEST_COMMAND` drift (README/runbook/architecture pointers as appropriate) | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005
- AC-6 → T-006
- AC-7 → T-007
- AC-8 → T-008
- AC-9 → T-009
- AC-10 → T-010
