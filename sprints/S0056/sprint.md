# Sprint S0056

- Story: `US-0077`
- Goal: ship **merged-scratchpad** documentation profile controls (**`DOC_AUDIENCE_PROFILE`**, **`DOC_DETAIL_LEVEL`** per **`DEC-0055`**), **dual README** layout (**root `README.md`** + **`docs/developer/README.md`** per **`DEC-0059`**), deterministic validation via **`scripts/validate_doc_profile.py`**, **tiered AC-8** regression (**`R-0054`**), **active + `template/`** parity (**`US-0030`**), optional-mode boundaries (**`US-0031`** / **`US-0032`**), and **`US-0071`**-safe surfaces — per **`decisions/DEC-0059.md`**, architecture **`# US-0077`**, **`R-0054`**, and backlog **AC-1..AC-10**.
- Status: **verify-work-pass** — **`sprints/S0056/plan-verify.json`** **PASS** (`2026-03-28T02:00:00Z`, `orchestrator_run_id=auto-20260327-02`); **`/execute`** complete; **`sprints/S0056/qa-findings.md`** **PASS** (`2026-03-27`); **`sprints/S0056/uat.json`** / **`sprints/S0056/uat.md`** **PASS** (`2026-03-28T12:30:00Z`, `10/10`); next **`/release`**

## Scope

- **Scratchpad + enum validation** — **`DOC_PROFILE_INVALID`**, **`DOC_PROFILE_MERGE_ERROR`**; template/example ship explicit keys; transition default **`both`×`balanced`** per **`DEC-0059`** §6 (**AC-1**).
- **Reproducible generation/update paths** — profile inputs drive doc outputs idempotently (**AC-2**).
- **Audience-appropriate content** — **`USER_*`** vs **`DEV_*`** H2 literals in architecture; plain-language user channel vs developer guardrails (**AC-3**).
- **Dual-file split + ownership** — no contradictory bodies across channels; pointers vs shard rules (**AC-4**).
- **Optional modes** — **`SPEC_PACK_MODE`** / **`USER_GUIDE_MODE`** remain zero-overhead when **0**; profile-aware only when enabled (**AC-5**).
- **Validator** — required sections, budgets, **`DOC_SECTION_MISSING:<key>`**, **`DOC_SECTION_BUDGET_EXCEEDED`**, **`DOC_TEMPLATE_PARITY_FAIL`** (**AC-6**).
- **Parity** — README/runbook/template/installer manifest for new paths (**AC-7**).
- **Regression** — 9-cell matrix coverage Tier A/B/C in **`tests/run-tests.*`** (**AC-8**).
- **US-0071** — scan validator/tooling and generated markdown on in-scope surfaces (**AC-9**).
- **Traceability** — **`DEC-0059`** + architecture cross-linked from operator docs; migration guidance surfaced (**AC-10**).
