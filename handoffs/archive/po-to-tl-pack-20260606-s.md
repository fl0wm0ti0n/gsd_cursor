# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Intake handoff — US-0093 / cursor-20260606-US0093-intake`
- Last archived heading: `## Intake handoff — US-0093 / cursor-20260606-US0093-intake`
- Verification tuple (mandatory):
  - archived_body_lines=54
  - retained_body_lines=766

---

## Intake handoff — US-0093 / cursor-20260606-US0093-intake

### Target

- `story_id=US-0093`
- `intake_run_id=cursor-20260606-US0093-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=story`

### Summary

- **Problem**: **US-0092** / **DEC-0078** catalogued **`browser_smoke`**, **`process_health`**, **`cli_smoke`**, and **`manual_operator`** probes, but **`scripts/uat_probe_lib.py`** still returns **`UAT_PROBE_UNRESOLVED`** for browser/process/cli execution; **`manual_operator`** UI steps are never auto-run. Operator wants its-magic to **self-test apps** using **Cursor built-in browser** (navigate, click, type, console/network evidence) for maximum automation per prior **`/ask`** thread.
- **Proposed delivery**: single story **US-0093** — Cursor browser as **primary** web probe path; HTTP/Playwright **fallback**; automatable **manual_operator** UI routing; evidence in **`uat.json`**; new fail-closed codes (**`UAT_BROWSER_UNAVAILABLE`**, etc.); docs/tests/template parity.
- **Decomposition**: single story (PO default); TL may split at architecture only with explicit authority.
- Status authority: **OPEN** in `docs/product/backlog.md` per **US-0045**; closure at `/release`.

### Plan areas (US-0081)

| plan_area_id | maps to |
|---|---|
| `browser-smoke-execution` | US-0093 |
| `manual-operator-ui-routing` | US-0093 |
| `probe-stub-completion` | US-0093 |
| `agent-command-contract` | US-0093 |
| `evidence-and-reason-codes` | US-0093 |
| `docs-tests-parity` | US-0093 |

### Risks (carry to /discovery)

- **R1**: Browser MCP absent in headless/CI — mitigate with HTTP/Playwright fallback + **`UAT_BROWSER_UNAVAILABLE`**.
- **R2**: False PASS on unimplemented agent browser steps — fail closed; contract tests on command excerpts + reason codes.
- **R3**: Over-automation of judgment steps — keep human-only **`manual_operator`** fail closed with explicit keyword guards.
- **R4**: Security — browser must not submit secrets; respect Cursor approval/origin guardrails.

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=first-intake-pack`
- `coverage_complete=true`
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0093-intake-20260606.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**

### Evidence refs

- `docs/product/backlog.md` (`## US-0093`)
- `docs/product/acceptance.md` (portfolio row unchecked)
- `handoffs/intake_evidence/US-0093-intake-20260606.json`
- `docs/engineering/research.md` (**`R-0079`** stub)

### Next

- **`/discovery`** (fresh PO context) for **`US-0093`** — lock Cursor browser agent contract vs stdlib fallback, manual_operator routing rules, evidence schema. Research stub: **`R-0079`**.

---

