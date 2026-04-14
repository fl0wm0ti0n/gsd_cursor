# PO to TL archive pack (2026-04-14)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 44
- First archived heading: `## PO → TL Handoff — US-0076 (Intake)`
- Last archived heading: `## PO → TL Handoff — US-0076 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=36
  - retained_body_lines=800

---

## PO → TL Handoff — US-0076 (Intake)

> Placement note: appended after **DEC-0054** rollover archived the prior top copy into `handoffs/archive/po-to-tl-pack-20260324.md`; TL read model uses file **tail** (runbook).

### New intake

User requests **executable** behavior: scratchpad **`SYNC_POLICY_MODE`**, **`ALLOW_AUTO_PUSH`**, and **`AUTO_PUSH_BRANCH_ALLOWLIST`** should **drive** whether/when **git push** runs — not remain **policy-only** relative to **`validate-and-push`**.

### Overlap

- **US-0038** (DONE): eligibility contract — **US-0076** implements the missing **script/operator** linkage.
- **DEC-0018**: amend or extend with **DEC-0058** (execute phase) for “scratchpad + script” contract.

### Decomposition

- **Single story** **US-0076** — scratchpad parse/merge, gate chain, script changes, docs, tests, decision.

### Intake pack

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### TL scope

- Prefer **extend `validate-and-push.ps1` / `.sh`** to read **merged** scratchpad; add **dry-run** / **reason-code** exits; map **`by_phase`** to **explicit invocation** contract unless architecture selects **state.md** phase reader.
- **AC-5** QA blocking rule needs a **bounded, testable** definition.
- Research: **`R-0053`**.

### Recommendation

**`/discovery`** → **`/research`** (finalize **R-0053**) → **`/architecture`** (**`DEC-0058`**) → **`/sprint-plan`**.

---

