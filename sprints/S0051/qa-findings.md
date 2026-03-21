# Sprint S0051 QA Findings

- Story: `US-0072`
- Sprint: `S0051`
- Result: PASS

## Test plan

- Run triad enforcement directly (per `handoffs/dev_to_qa.md`):
  - `python scripts/enforce-triad-hot-surface.py --self-test`
  - `python scripts/enforce-triad-hot-surface.py --check`
- Run baseline regression:
  `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`.
- Validate implementation against **US-0072** AC-1..AC-10, **`DEC-0054`**, and sprint
  tasks **T-001..T-010**.

## Findings

- Triad script `--self-test`: **PASS** (exit `0`).
- Triad script `--check` on repo: **PASS** (exit `0`).
- Baseline command executed:
  `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (exit code `1`).
- Evidence: `tests/report.md` (`Timestamp: 2026-03-21T15:18:44Z`, `Pass: 698`,
  `Fail: 4`).
- In-scope **US-0072** / **26f** regression (triad hot-surface enforcement): **PASS**
  in `tests/report.md` — script exists, self-test, check + idempotent rerun, runbook
  (active + template), execute + refresh-context gate strings (active + template).
- Contract surfaces consistent with execute handoff: `scripts/enforce-triad-hot-surface.py`,
  archive packs under `handoffs/archive/` and `docs/engineering/architecture-archive/`,
  `docs/engineering/phase-context.md` (+ template), scratchpad threshold keys, runbook
  minimal-read / reason-code guidance, command gates on listed phases (active +
  template).

### Non-blocking baseline failures (explicit classification)

The following failures are **out of scope** for **US-0072** QA and are treated as
**known baseline debt** (tracked under **`US-0074`** — baseline regression cleanup):

- `Homebrew stable formula URL uses npm version tag`
- `Homebrew stable formula version matches npm version`
- `Installer bootstraps TEST_COMMAND for detectable stack`
- `CLI missing install bootstraps TEST_COMMAND for detectable stack`

They do **not** indicate regression in triad enforcement, archive rollover, or **26f**
assertions.

## Acceptance validation (US-0072)

- AC-1: **PASS** — Deterministic hot/archive contract for `state.md`, `po_to_tl.md`,
  `architecture.md` with scratchpad-bound thresholds and pack naming (**DEC-0054** /
  `enforce-triad-hot-surface.py` / scratchpad keys).
- AC-2: **PASS** — Same-phase rollover or fail-closed semantics documented on mutating
  phases; `--check` enforces caps without silent oversize hot surfaces.
- AC-3: **PASS** — Archive pack headers carry verification fields (`boundary`, moved /
  retained counts, `pack_ref`); `--check` after rollover **PASS**; idempotent rerun
  covered by **26f**.
- AC-4: **PASS** — `/refresh-context`, `/intake`, `/discovery`, `/architecture`,
  `/execute` document triad gate / rollover (**26f** string checks).
- AC-5: **PASS** — Runbook (+ template) defines minimal-read policy and bounded budgets
  per phase.
- AC-6: **PASS** — `docs/engineering/phase-context.md` (+ template) present as compact
  pointer surface.
- AC-7: **PASS** — Reason-code taxonomy aligned to **DEC-0054** / architecture
  (e.g. `STATE_ARCHIVE_REQUIRED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`) documented in
  runbook and enforced in script diagnostics.
- AC-8: **PASS** — Archive packs retain content with headers linking source paths;
  hot surfaces remain within policy under merged scratchpad.
- AC-9: **PASS** — Active/template parity maintained for listed command, scratchpad
  example, runbook, README, and test coverage surfaces (**26f** template rows **PASS**).
- AC-10: **PASS** — Regression **26f** covers script self-test, repo `--check`,
  idempotent second check, and documentation gates.

## Verdict

- QA verdict for **`S0051`** / **`US-0072`**: **PASS**.
- Blocking findings in-scope: **none**.
- Recommended next phase: **`/verify-work`**.
