# Sprint S0057 Tasks

- Story: `US-0078`
- Sprint: `S0057`
- Governance: **`DEC-0060`** (interactive evidence + `ie:` refs + migration); **`DEC-0050`** (pack topics); **`R-0055`** (validation rules + AC-8 matrix); architecture **`# US-0078`**; parity **`US-0030`**

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Implement **required-topic coverage gate**: for `selected_pack`, every required key has a **`topic_coverage`** row with valid **`satisfied_by`** + parseable **`ie:`** `ref` per **`DEC-0060`**; on failure emit **`INTAKE_REQUIRED_TOPIC_MISSING`** / **`INTAKE_REQUIRED_PACK_INCOMPLETE`** as applicable — **before** any backlog/acceptance mutation | AC-1 |
| T-002 | done | Enforce **`assumptions_confirmed=yes`** only when **`assumption_confirmation_ref`** (or equivalent) is present and validator-approved; otherwise **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`** — no affirmative assumption without evidence | AC-2 |
| T-003 | done | Wire **fail-closed persistence**: on any validation failure emit **`INTAKE_PERSISTENCE_BLOCKED`** (preserve primary sub-codes in diagnostics) and **abort** writes to backlog/acceptance/vision intake surfaces | AC-3 |
| T-004 | done | Persist **auditable evidence fields** distinguishing **`asked_topics`** from answered/covered keys (`topic_coverage` / `answered_topics` as designed) and **`assumption_confirmation_ref`** alongside legacy **`DEC-0050`** literals | AC-4 |
| T-005 | done | **`INTAKE_GUIDED_MODE=1`**: keep bounded questioning; **prohibit** silent auto-satisfaction of required topics without evidence-backed assumptions (aligned with **`R-0055`** asked-vs-covered rules) | AC-5 |
| T-006 | done | **`INTAKE_GUIDED_MODE=0`**: run the **same** pre-persistence validation pipeline; low-touch may reduce follow-up prompts but **not** skip mandatory pack coverage | AC-6 |
| T-007 | done | Implement **deterministic diagnostics**: list missing required topics, cite reason codes, and surface **remediation prompts** to collect only unresolved required inputs | AC-7 |
| T-008 | done | Add **regression coverage** per **`R-0055`** AC-8 matrix: full answered pack **PASS**, explicit assumption confirmation **PASS**, missing topic **BLOCK**, false **`assumptions_confirmed`** **REJECT**, plus **Tier C** dual-mode smoke (`INTAKE_GUIDED_MODE` ∈ {0,1}) in **`tests/run-tests.ps1`** / **`.sh`** | AC-8 |
| T-009 | done | **Active/template parity**: align intake command(s), core rules, runbook, README, and `template/` mirrors for the strengthened evidence contract (**`US-0030`**) | AC-9 |
| T-010 | done | **AC-10 closure**: ensure operator docs, sprint surfaces, and **`docs/engineering/decisions.md`** index explicitly cite **`DEC-0060`**, fail-closed gate behavior, grandfather migration, and **`architecture.md`** **`# US-0078`** | AC-10 |

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
