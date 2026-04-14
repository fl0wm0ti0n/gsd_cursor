# PO to TL archive pack (2026-04-13)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 45
- First archived heading: `## Research reference`
- Last archived heading: `## Risks`
- Verification tuple (mandatory):
  - archived_body_lines=23
  - retained_body_lines=796

---

## Research reference

- `R-0024`: starter/template hygiene, deterministic cleanup ownership, vertical-slice story splitting, and adaptive elicitation questioning patterns.

## TL boundaries

- In scope:
  - installer cleanup ownership contract and parity across PS1/SH/PY.
  - starter artifact neutralization policy for template docs.
  - intake decomposition and adaptive PO questioning contracts.
  - optional ID bootstrap with deterministic eligibility rules.
  - regression coverage and active/template parity.
- Out of scope:
  - runtime product feature behavior changes.
  - retroactive renumbering of existing project histories.
  - bypassing existing release/decision-gate safety contracts.

## Risks

- Cleanup scope expansion could accidentally remove non-framework files if ownership rules are unclear.
- Intake decomposition may over-split without bounded heuristics and explicit user approval.
- Bootstrap ID mode could collide with existing repos if freshness detection is weak.

