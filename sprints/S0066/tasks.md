# Sprint S0066 Tasks

- **Bug**: `BUG-0005`
- **Sprint**: `S0066`
- **Governance**: `DEC-0069`; `architecture.md` `# BUG-0005`; `R-0064`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Implement **atomic** **`handoffs/resume_brief.md`** refresh on successful **`/intake bug`** persistence path (active repo — command contract + any script/validator hook that performs backlog mutation) | AC-1 |
| T-002 | done | Populate **DEC-0069 §1** minimum fields (**`bug_id`**, **`intended_resume_phase=discovery`**, **`resolution_source`**, boundary ids/timestamps, intake evidence ref); document **idempotent** full-replace or normative latest-block pattern | AC-2 |
| T-003 | done | Add validation or writer-side guard so brief content **cannot contradict** **`docs/product/backlog.md`** for the persisted **`bug_id`** | AC-3 |
| T-004 | done | Apply **active / `template/`** (and parity-required **rules**) updates for any touched **intake** surfaces | AC-4 |
| T-005 | done | Add deterministic regression for **R-0064 #1** (happy **`/intake bug` → brief → `/auto`** resume inputs — no false **`RESUME_BRIEF_STALE`**) | AC-5 |
| T-006 | done | Add regression or documented deterministic check for **R-0064 #2** (missing brief → **`state.md`** fallback ordering) | AC-6 |
| T-007 | done | Add regression coverage for **R-0064 #3–#4** (**`start-from`** precedence; backlog contradiction → fail-fast) | AC-7 |
| T-008 | done | Add regression coverage for **R-0064 #5** (portfolio switch / new OPEN bug, no stale **`intake`** target) | AC-8 |
| T-009 | done | Register new tests in **`tests/run-tests.sh`** and **`tests/run-tests.ps1`** (section + invocation) when fixtures land | AC-9 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
- AC-8 -> T-008
- AC-9 -> T-009
