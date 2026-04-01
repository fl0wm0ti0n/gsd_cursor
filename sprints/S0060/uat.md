# UAT — S0060 / BUG-0001 (`auto-20260330-01`)

**Closure**: `/verify-work` (**qa**, fresh context), **2026-03-30**.

## Operator narrative

Consumer installs that ship `template/` must include the three mandatory intake gate modules under `template/scripts/` in byte parity with `scripts/`, with a deterministic check and regression fixtures. This UAT re-ran the parity script and fixture test at verify-work boundary, reviewed sprint QA findings, and reconciled canonical backlog + acceptance per **US-0045** / **DEC-0061** §8.

## Evidence

- `sprints/S0060/uat.json` — **5/5** pass (**AC-1..AC-5**).
- `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK]`
- `pytest tests/intake_template_parity_fixtures_test.py` → **1 passed**
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → `[BUG_VALIDATION_OK]`

## Out of scope

Full `tests/run-tests.ps1`: **2** known failures (Homebrew stable vs `package.json` version) — same out-of-scope posture as **S0060** `/qa`.
