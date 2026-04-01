# Architecture archive pack (2026-03-29)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 34
- First archived heading: `# US-0035: Component-Scoped Execution Mode with Protection Guards`
- Last archived heading: `# US-0035: Component-Scoped Execution Mode with Protection Guards`
- Verification tuple (mandatory):
  - archived_body_lines=81
  - preamble_lines=10
  - retained_body_lines=3461

---

# US-0035: Component-Scoped Execution Mode with Protection Guards

## Overview

US-0035 introduces an optional scoped-execution mode for multi-component repos.
The mode constrains planning and implementation to declared target components
while requiring explicit protection checks for non-target components.

## Component scope model

### C1) Scope declaration contract

Canonical declaration artifact:
- `docs/engineering/component-scope.md`

Minimum required fields per scoped story:
- `story_id`
- `scope_mode` (`off|on`)
- `target_components[]`
- `non_target_components[]`
- `allowed_interface_touch[]` (explicitly permitted cross-component interfaces)
- `out_of_scope_constraints[]`
- `approval_policy` (who can approve scope expansion)

Scratchpad controls:
- `COMPONENT_SCOPE_MODE=0` (default off)
- `TARGET_COMPONENTS=` (comma-separated defaults for current cycle; optional)

### C2) Non-target protection model

When scope mode is enabled:
- `/sprint-plan` requires each task to include:
  - `target_component_ids`
  - `expected_impacted_interfaces`
- `/execute` enforces scope-first behavior:
  - no intentional edits outside targets unless escalation is approved
- `/qa` requires unaffected-component checks for `non_target_components`:
  - smoke/regression confirmation
  - compatibility signal review for unintended interface impact

Evidence destination:
- `docs/engineering/component-scope-report.md`

### C3) Decision-gate trigger conditions

Trigger decision gate when all conditions are true:
1. `COMPONENT_SCOPE_MODE=1`
2. Out-of-scope component impact is detected
3. Impact is not listed in `allowed_interface_touch[]`
4. No prior approval record exists in decisions/handoff artifacts

Gate outcomes:
- approve scope expansion (update scope artifact + tasks),
- split into separate story/sprint,
- rollback/defer cross-component change.

## Workflow integration (scoped mode)

| Phase | Scoped-mode behavior |
|------|-----------------------|
| `/intake` | Declare in-scope vs out-of-scope components. |
| `/architecture` | Define expected interface touch and protection strategy. |
| `/sprint-plan` | Require component-tagged tasks and impact assumptions. |
| `/execute` | Enforce target-only execution unless approved escalation. |
| `/qa` | Verify target outcomes plus non-target protection checks. |
| `/verify-work` | Confirm scope evidence coverage before pass recommendation. |
| `/release` | If unapproved out-of-scope impact remains, hold via decision gate. |

Default-off behavior:
- If `COMPONENT_SCOPE_MODE=0`, no extra required declarations/checks/gates.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Scope metadata becomes stale | Require `/sprint-plan` refresh of scope file each sprint. |
| False-positive out-of-scope alarms | Allow explicit `allowed_interface_touch[]` declarations. |
| Teams bypass non-target checks | QA checklist requires component-scope report evidence when mode is on. |

---

