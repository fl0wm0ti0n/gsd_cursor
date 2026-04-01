# Sprint S0058

- Story: `US-0079`
- Goal: first-class **bug issues** (`BUG-####`) with **`OPEN`/`DONE`** only — canonical **`## Bug issues (canonical)`** / **`## Bug acceptance (canonical)`**, explicit intake routing (**`INTAKE_WORK_ITEM_KIND`** / **`/intake bug`**), minimum reproducibility schema + validators, **`US-0045`** bug-family reconciliation, sprint/QA/release/**`/ask`** traceability, active + `template/` parity — per **`DEC-0061`**, **`architecture.md`** **`# US-0079`**, **`R-0056`**.
- Status: **UAT PASS — ready for `/release`** — **`sprints/S0058/plan-verify.json`** **PASS**; **`sprints/S0058/qa-findings.md`** **PASS**; **`sprints/S0058/uat.json`** / **`sprints/S0058/uat.md`** **PASS** (**`2026-03-30`**, `orchestrator_run_id=auto-20260329-01`); story **`DONE`** (**US-0045**); backlog **AC-1..AC-10** verified through verify-work.

## Scope

- **AC-1** — **`BUG-xxxx`** allocator, canonical backlog section, deterministic ordering.
- **AC-2** — Intake classifies bugs vs stories; explicit routing; no silent **`US-xxxx`** for defects.
- **AC-3** — Status literals **`OPEN`/`DONE`** only; reject triage state machine requirements.
- **AC-4** — Minimum fields: **environment**, **steps_to_reproduce**, **expected**, **actual**, **evidence_refs**; deterministic validation (**`BUG_VALIDATION_*`** family per **`DEC-0061`** / runbook).
- **AC-5** — Sprint **`tasks.md`** / **`summary.md`** may link **`BUG-xxxx`** without US conversion.
- **AC-6** — **`qa-findings`**, **`uat.*`**, **`release-findings`** reference **`BUG-xxxx`** consistently (**US-0042** style).
- **AC-7** — Reconciliation scripts / guards extend to **`BUG-`** family; no US regression.
- **AC-8** — **`/ask`** and context-pack id allowlists include **`BUG-####`**.
- **AC-9** — Commands, rules, runbook, README, **`template/`** parity.
- **AC-10** — Operator traceability to **`DEC-0061`** + architecture **`# US-0079`** (DEC already authoritative; execute completes citations/tests).

## Governance

- **`decisions/DEC-0061.md`**
- **`docs/engineering/architecture.md`** **`# US-0079`**
- **`docs/engineering/research.md`** **`R-0056`**
- Related: **`US-0045`**, **`US-0042`**, **`DEC-0055`** (scratchpad merge / **`INTAKE_WORK_ITEM_KIND`**), **`US-0030`** (parity), **`US-0070`** (optional **`bug_ids`** on phase boundaries)
