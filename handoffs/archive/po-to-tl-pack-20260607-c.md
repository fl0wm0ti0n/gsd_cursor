# PO to TL archive pack (2026-06-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Intake handoff — US-0095 / cursor-20260607-US0095-intake`
- Last archived heading: `## Intake handoff — US-0095 / cursor-20260607-US0095-intake`
- Verification tuple (mandatory):
  - archived_body_lines=49
  - retained_body_lines=789

---

## Intake handoff — US-0095 / cursor-20260607-US0095-intake

### Target

- `story_id=US-0095`
- `intake_run_id=cursor-20260607-US0095-intake`
- `selected_pack=small-intake-pack`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`

### Summary

- Operator reports **`AUTO_FLOW_MODE=full_autonomy`** + **`AUTO_BACKLOG_DRAIN=1`** still stops at **`completed (segment exhausted)`** with guidance to re-run `/auto` or **`python scripts/auto_outer_driver.py`** — contradicts expected hands-off drain in Cursor IDE.
- **US-0095** closes the gap: **native in-chat auto-chain** for `/auto` across phases **and** backlog-drain segments without mandatory outer driver; **`auto_outer_driver.py`** remains optional headless/CI fallback per **DEC-0078** composition.

### Scope boundaries

- **In**: `.cursor/commands/auto.md`, `auto-orchestration-reference.md`, `architecture.md`, runbook, contract tests, operator messaging under **`AUTO_QUIET`**.
- **Out**: Removing decision gates; bypassing isolation/strict-proof/QA/release; deleting outer driver script.

### Constraints (architecture-locked)

- **BUG-0006** / **US-0069** spawn-only — orchestrator must not execute phase roles in-band.
- **US-0088** / **US-0092** hard stop matrix — unchanged for governance gates.
- **DEC-0069** — paired **`resume_brief`** + **`state.md`** at every boundary before in-chat continuation.

### Research asks (**R-0081**)

1. Cursor-native continuation model — orchestrator self-scheduling vs Task/subagent spawn loop within one `/auto` invocation.
2. IDE drain-advance algorithm — read segment boundary → select next OPEN story → recompute phase plan → continue without outer driver.
3. Cap interaction — **`AUTO_LOOP_MAX_CYCLES`**, **`AUTO_BACKLOG_MAX_STORIES`**, **`AUTO_BLOCK_RETRY_MAX`** in IDE chain vs outer driver.
4. Fallback boundary — when outer driver is still recommended (headless, CI, `--invoke-cmd`).

### Evidence refs

- `handoffs/intake_evidence/US-0095-intake-20260607.json`
- `docs/product/backlog.md` (`## US-0095`)
- Prior: **US-0092** / **DEC-0078**, **US-0088**, **US-0044**, **BUG-0006**

### Next

- **`/discovery`** (fresh **PO**) for **`US-0095`**

### Decision gate

- **None** at intake.

---

