# PO to TL archive pack (2026-06-12)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated intake handoff — US-0096 / cursor-20260611-US0096-intake`
- Last archived heading: `## Orchestrated intake handoff — US-0096 / cursor-20260611-US0096-intake`
- Verification tuple (mandatory):
  - archived_body_lines=57
  - retained_body_lines=789

---

## Orchestrated intake handoff — US-0096 / cursor-20260611-US0096-intake

### Target

- `story_id=US-0096`
- `intake_run_id=cursor-20260611-US0096-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `decomposition=single_story` (per **US-0051**)
- `priority=P1`
- `selected_pack=first-intake-pack`
- `coverage_complete=true`

### Summary

- **`/intake`** **PASS** for **US-0096** — delivery modes with layered memory. New **`DELIVERY_MODE`** scratchpad axis (**`standard`** \| **`ultra_lean`** \| **`mega_quick`**, default **`standard`**) controls lifecycle shape; orthogonal to **`TOKEN_PROFILE`** and **`CAVEMAN_MODE`**. **`ultra_lean`**: 4 macro-phases + **`pack.json`** + **`active-context.md`**. **`mega_quick`**: **`/quick`** semantics under **`/auto`**. Tranche A universal token wins without mode toggle. Standard mode byte-compatible.

### Key scope boundaries

1. **Not amnesia**: lean modes use delta writes + section-scoped cold reads of vision/architecture/decisions.
2. **Mode-scoped reinstatement**: **DEC-0052** full-chain reinstatement applies only when **`DELIVERY_MODE=standard`**.
3. **Quality floor**: tests + AC traceability in all modes; conditional arch/decision deltas when new patterns emerge.
4. **Out of scope**: removing standard lifecycle; bypassing tests; weakening **US-0039** gates for standard mode.

### Plan area coverage (DEC-0064)

| plan_area_id | story_ids |
|---|---|
| delivery-mode-scratchpad | US-0096 |
| universal-token-wins | US-0096 |
| ultra-lean-lifecycle | US-0096 |
| layered-memory | US-0096 |
| mega-quick-mode | US-0096 |
| auto-phase-resolver | US-0096 |
| docs-tests-parity | US-0096 |

### Risks (intake)

- **R1**: Lean modes lose institutional memory if pack/index contract weak → mitigate with **AC-5** / **AC-9**.
- **R2**: Operators expect phase exclude to save tokens under standard mode → docs must state **DEC-0052** reinstatement unchanged for **`standard`**.
- **R3**: **`mega_quick`** used for greenfield → eligibility rules + backlog routing (**AC-8**).
- **R4**: Universal hot-surface tightening breaks long-running standard repos → Tranche A changes must be rollover-safe with operator override.

### Evidence refs

- `handoffs/intake_evidence/US-0096-intake-20260611.json`
- `docs/product/backlog.md` (`## US-0096`)
- `docs/product/acceptance.md` (US-0096 row)
- `docs/product/vision.md` (**Intake Notes — US-0096**)
- `docs/engineering/research.md` (**R-0082** stub)

### Research asks for **`R-0082`** extension

See **`R-0082`** intake-locked asks before **`/architecture`**.

---

