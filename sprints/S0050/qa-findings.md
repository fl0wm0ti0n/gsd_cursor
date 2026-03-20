# Sprint S0050 QA Findings

- Story: `US-0071`
- Sprint: `S0050`
- Result: PASS

## Test plan

- Run `python scripts/check-user-visible-metadata.py` (clean repo; expect exit `0`).
- Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and validate
  **26e** / user-visible metadata guard rows plus execute-delivered surfaces per
  `handoffs/dev_to_qa.md` (S0050 section).
- Map findings to `US-0071` AC-1..AC-10 via `sprints/S0050/tasks.md` (T-001..T-010).

## Commands executed

- `python scripts/check-user-visible-metadata.py` — exit code `0`.
- `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` — exit code `1`
  (suite-level; see baseline drift below).

## Evidence

- `tests/report.md` — `Timestamp: 2026-03-20T21:45:24Z`, `Pass: 683`, `Fail: 4`.
- In-scope **26e** / US-0071 regression rows — all **PASS**:
  - `metadata guard script exists`
  - `metadata guard clean repo scan passes`
  - `metadata guard idempotent rerun passes`
  - `metadata guard detects leak in user-visible bin`
  - `metadata guard passes when only non-scanned tree has tokens`
  - `metadata guard allows JS line comment with token shape`
  - `runbook documents user-visible metadata guard` (active + template)
  - `execute command documents metadata guard step` (active + template)

## Out-of-scope baseline failures (not US-0071 blockers)

- `Homebrew stable formula URL uses npm version tag`
- `Homebrew stable formula version matches npm version`
- `Installer bootstraps TEST_COMMAND for detectable stack`
- `CLI missing install bootstraps TEST_COMMAND for detectable stack`

## Acceptance validation (US-0071)

- AC-1: PASS — forbidden-token matchers and channel scope in
  `scripts/check-user-visible-metadata.py` + runbook (`DEC-0053` alignment).
- AC-2: PASS — internal-only allowlist documented (non-scanned trees, comments vs
  literals) in runbook and decision/architecture refs.
- AC-3: PASS — `/execute` step 20 mandates guard before completion (active +
  template); `quality.mdc` parity.
- AC-4: PASS — `/qa` mandates checker + fail-closed reason codes; **26e** verifies
  behavior.
- AC-5: PASS — remediation contract (evidence ref, token class, neutral copy) in
  runbook.
- AC-6: PASS — `USER_VISIBLE_INTERNAL_METADATA_DETECTED`,
  `METADATA_SANITIZATION_POLICY_MISSING`,
  `METADATA_SANITIZATION_SCOPE_AMBIGUOUS` documented on policy surfaces.
- AC-7: PASS — regression covers non-scanned `docs/` tree + JS line-comment path.
- AC-8: PASS — active/template parity asserted for runbook, execute, qa, release,
  README, `quality.mdc`.
- AC-9: PASS — positive, negative (leak detection), allowlist, idempotence rows
  green in `tests/report.md`.
- AC-10: PASS — release check-in gate references consolidated runner + US-0071
  metadata coverage (active + template); tests assert presence.

## Verdict

- QA verdict for `S0050` / `US-0071`: **PASS**.
- Blocking findings in-scope: **none**.
- Deterministic blocker reason code: **not applicable**.
- Recommended next phase: **`/verify-work`** for `S0050`.
