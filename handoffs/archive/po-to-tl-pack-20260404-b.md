# PO to TL archive pack (2026-04-04)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 45
- First archived heading: `## PO → TL intake handoff — **US-0086** (2026-04-04)`
- Last archived heading: `## PO → TL intake handoff — **US-0086** (2026-04-04)`
- Verification tuple (mandatory):
  - archived_body_lines=8
  - retained_body_lines=795

---

## PO → TL intake handoff — **US-0086** (2026-04-04)

- **Scope**: Scratchpad-gated **automation profile** so **dev/CI/DI/QA/release** pick **Docker** / **SSH** / other **declared** targets when **heuristics or explicit NL** (“**start container \<target_id\>**”) warrant it; **manual** daily work stays **default-off** (**no** silent **`TEST_COMMAND`** reroute). Composes with **US-0085** (**no** **`.env`** read); **US-0064** schema unchanged.
- **Evidence**: **`handoffs/intake_evidence/US-0086-intake-20260404.json`**; **`python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0086-intake-20260404.json`** → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**; research **`docs/engineering/research.md`** **`R-0068`**.
- **Risks / next**: over-broad agent autonomy; NL alias abuse; doc/parity drift. Next: **`/architecture`** locks scratchpad keys + reason codes; **`/discovery`** if TL wants bounded clarification first.

**US-0085** (OPEN): gitignored **`.env`** + **`.env.example`** + no-AI-read — see **`docs/product/backlog.md`**; evidence **`US-0085-intake-20260404.json`**.
---
