# Sprint S0057

- Story: `US-0078`
- Goal: enforce **runtime intake question-pack evidence** before persistence — **`topic_coverage`** with valid **`ie:`** refs (**`DEC-0060`**), **`asked_topics`** vs covered alignment (**`R-0055`**), **`assumption_confirmation_ref`** for affirmative assumptions, fail-closed **`INTAKE_PERSISTENCE_BLOCKED`** / sub-codes (**`AC-1..AC-3`**); persist auditable distinction of asked vs answered (**`AC-4`**); **guided** and **low-touch** (`INTAKE_GUIDED_MODE=0`) both gate before writes (**`AC-5`**, **`AC-6`**); deterministic diagnostics (**`AC-7`**); tiered regression per **`R-0055`** matrix (**`AC-8`**); active + `template/` parity (**`AC-9`**); operator traceability to **`DEC-0060`** + architecture **`# US-0078`** (**`AC-10`**).
- Status: **verify-work complete** — QA + UAT **PASS** **`2026-03-28`** (`orchestrator_run_id=auto-20260328-01`); sprint artifacts **`sprints/S0057/uat.json`**, **`sprints/S0057/uat.md`**; next **`/release`** (`next_scheduled_phase=release`).

## Scope

- **Coverage gate (AC-1)** — required pack keys must each have **`topic_coverage`** row + parseable **`ie:`** `ref`; no silent satisfaction.
- **Assumption literal (AC-2)** — `assumptions_confirmed=yes` only with in-session confirmation evidence; else **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`**.
- **Abort writes (AC-3)** — validator runs before backlog/acceptance mutation; **`INTAKE_REQUIRED_TOPIC_MISSING`** / **`INTAKE_REQUIRED_PACK_INCOMPLETE`** / umbrella blocked path.
- **Persisted evidence shape (AC-4)** — `asked_topics`, coverage rows, `assumption_confirmation_ref` (or equivalent) auditable in handoff/sidecar per architecture.
- **Guided mode (AC-5)** — bounded prompts; no auto-fill of required topics without evidence-backed assumptions.
- **Low-touch mode (AC-6)** — same validation pipeline; fewer follow-ups allowed, not a bypass of mandatory coverage.
- **Diagnostics (AC-7)** — missing topics, remediation prompts, deterministic reason codes.
- **Regression (AC-8)** — P1–P5 matrix: full pack pass, explicit assumption pass, missing topic block, false `assumptions_confirmed` reject, dual-mode smoke.
- **Parity (AC-9)** — `.cursor/commands/intake.md` (and related), rules, runbook, README, `template/` mirrors.
- **Traceability (AC-10)** — sprint/operator surfaces cite **`DEC-0060`**, **`DEC-0050`** pack authority, migration grandfather; cross-link **`architecture.md`** **`# US-0078`**.

## Governance

- **`decisions/DEC-0060.md`**, **`decisions/DEC-0050.md`** (pack semantics)
- **`docs/engineering/architecture.md`** **`# US-0078`**
- **`docs/engineering/research.md`** **`R-0055`**
- Related: **`US-0068`** (DONE packs), **`US-0033`** (guided/low-touch), **`US-0030`** (parity)
