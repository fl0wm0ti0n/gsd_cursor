# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 24
- First archived heading: `## Intake handoff — BUG-0011 / cursor-20260606-BUG0011-intake`
- Last archived heading: `## Intake handoff — BUG-0011 / cursor-20260606-BUG0011-intake`
- Verification tuple (mandatory):
  - archived_body_lines=52
  - retained_body_lines=794

---

## Intake handoff — BUG-0011 / cursor-20260606-BUG0011-intake

### Target

- `bug_id=BUG-0011`
- `intake_run_id=cursor-20260606-BUG0011-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `work_item_kind=bug` (`/intake bug`)
- `INTAKE_GUIDED_MODE=1`, `INTAKE_WORK_ITEM_KIND=bug` (argv override), `INTAKE_SUBAGENT_FALLBACK=deny`

### Summary

- **Defect**: **US-0089** Caveman mode ships scratchpad gates, literal-region invariants, operator toggles, and default-off contract tests — but `.cursor/rules/caveman.mdc` contains **no voice-compression directives**. With **`CAVEMAN_MODE=1`**, assistant replies remain verbose (full sentences, filler). Upstream JuliusBrussee/caveman intent is **token-saving terse prose**, not stereotypical caveman roleplay.
- **Diagnosis source**: prior `/ask` thread (2026-06-06) comparing local rule vs upstream `skills/caveman/SKILL.md` (drop filler/hedging, fragments OK, lite/full/ultra level table).
- Distinct from **US-0090** (input-side file compression — **DONE**). Related: **US-0089**, **DEC-0072**, **`R-0073`**, **US-0088** gate vocabulary.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Proposed fix direction (defer exact design to /architecture)

- Add **Voice compression (when `CAVEMAN_MODE=1`)** section to `.cursor/rules/caveman.mdc` + `template/` mirror: lite/full/ultra table, drop articles/filler/hedging/pleasantries, fragments OK, auto-clarity exceptions (security, destructive ops, ambiguous compression), pattern `[thing] [action] [reason]`.
- Extend runbook `### Caveman mode (US-0089)` with level semantics table.
- Additive contract-test markers in `tests/auto_command_contract_test.py`; preserve existing `test_caveman_default_off_*` and `test_caveman_compress_input_*` unless architecture updates pinned SHA intentionally.
- Precedence clause: when **`CAVEMAN_MODE=1`**, terse voice overrides conflicting user-rule “complete sentences / blog post” guidance.
- **Out of scope**: Wenyan modes; vendor install; changing **US-0090** input compression.

### Risks

- **SHA-256 drift**: **US-0090** negative-parity pinned `.cursor/rules/caveman.mdc` hash — sprint must update pinned assertions or scope to preserved substrings only.
- **Over-compression** of gate messages — mitigated by existing 9-zone MUST + non-suppressible list; auto-clarity exceptions for security/destructive ops.
- **User-rule conflict** without explicit precedence — mitigated by rule-level override sentence.

### Intake evidence (US-0078 / DEC-0060)

- `selected_pack=small-intake-pack`; `missing_topics=[]`; `assumptions_confirmed=(none)`
- `outcome_success_criteria` + `constraints_compatibility_risks` = `answer_ref`; `impacted_components` / `required_tests_acceptance_checks` / `done_definition` = `delegation_ref` per **DEC-0067**
- Validator: `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/BUG-0011-intake-20260606.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0011`); `docs/product/acceptance.md` (unchecked row)
- `handoffs/intake_evidence/BUG-0011-intake-20260606.json`
- `.cursor/rules/caveman.mdc`; `docs/engineering/architecture.md` `# US-0089`; `decisions/DEC-0072.md`; `docs/engineering/research.md` **`R-0073`** post-delivery gap extension
- `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → **`[BUG_VALIDATION_OK]`** (post-persist)
- `handoffs/resume_brief.md` refreshed: **`[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]`** (`bug_id=BUG-0011`, `intended_resume_phase=discovery`)

### Next

- **`/discovery`** (fresh PO context) for **BUG-0011** — confirm upstream voice-rule subset, level table, SHA pinning strategy, and runbook/contract-test scope.

---

