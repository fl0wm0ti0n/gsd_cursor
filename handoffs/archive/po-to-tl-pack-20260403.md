# PO to TL archive pack (2026-04-03)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 43
- First archived heading: `## PO -> TL Handoff - BUG-0004 (Intake)`
- Last archived heading: `## PO -> TL Handoff - BUG-0004 (Intake)`
- Verification tuple (mandatory):
  - archived_body_lines=38
  - retained_body_lines=773

---

## PO -> TL Handoff - BUG-0004 (Intake)

### Intake context

User reported a Linux runtime failure during installer execution:

- command: `its-magic --mode missing`
- environment: `root@docker-dmz:/workdir/dev_git/ai_docker_manager`
- failure: `/usr/lib/node_modules/its-magic/installer.sh: 2: set: Illegal option -`

### Duplicate/overlap evaluation

- Related bug: `BUG-0003` (install payload completeness in `missing`/`upgrade`).
- Assessment: not a duplicate; this intake targets shell-option/runtime compatibility at installer startup, while `BUG-0003` targeted missing required scripts after install paths.
- Decision: persist as `BUG-0004` under canonical bug workflow.

### Intake evidence and routing

- selected_pack=`small-intake-pack`
- asked_topics=`outcome_success_criteria`,`impacted_components`,`constraints_compatibility_risks`,`required_tests_acceptance_checks`,`done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`
- evidence bundle: `handoffs/intake_evidence/BUG-0004-intake-20260403.json`
- bug routing: explicit `/intake bug` request satisfied (`DEC-0061` / `US-0079`).

### TL discovery focus

1. Confirm exact shell/runtime path causing `set` option incompatibility (`sh`/`dash` vs `bash`) for `installer.sh`.
2. Define deterministic compatibility contract: either portable startup flags for POSIX shell execution or explicit guaranteed bash invocation with diagnostics.
3. Preserve behavior parity across installer entry paths (`installer.sh`, `installer.py`, CLI wrapper) and ensure no regression for `missing`/`upgrade`.
4. Add regression coverage reproducing the reported startup failure and validating corrected behavior.

### Recommendation

Proceed to `/discovery` for `BUG-0004`, then `/research` if needed for shell-compatibility options before architecture lock.

---

