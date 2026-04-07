# PO to TL archive pack (2026-04-04)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 45
- First archived heading: `## PO → TL intake pointer — **US-0086** / **US-0087** (2026-04-04)`
- Last archived heading: `## PO → TL intake pointer — **US-0086** / **US-0087** (2026-04-04)`
- Verification tuple (mandatory):
  - archived_body_lines=6
  - retained_body_lines=795

---

## PO → TL intake pointer — **US-0086** / **US-0087** (2026-04-04)

- **US-0086** (automation remote target selection; **“start container \<target_id\>**”; manual default-off): full handoff body **archived** per **DEC-0054** → **`handoffs/archive/po-to-tl-pack-20260404-b.md`**. Evidence **`handoffs/intake_evidence/US-0086-intake-20260404.json`**; **`R-0068`**. **US-0085** still **OPEN** — backlog.
- **US-0087** (**`/auto`** bug-target **all OPEN `BUG-####`** / single id): intake handoff archived **`handoffs/archive/po-to-tl-pack-20260404-e.md`**; evidence **`handoffs/intake_evidence/US-0087-intake-20260404.json`**; **`R-0070`**. Discovery **2026-04-04** (**PO**, `cursor-20260404-US0087-discovery`) **PASS** → next **`/architecture`**. **US-0086** also **OPEN**.
- **BUG-0008** (CRLF manifest / Linux global npm): discovery **2026-04-04T20:00:00Z** (**PO**, `fresh_context_marker=po-BUG0008-discovery-20260404T200000Z-fresh`) **PASS** — repo mitigations + **`tests/installer_manifest_crlf_bug0008_test.py`**; **remain** republish + Debian E2E (**`R-0069`**). Next **`/architecture`**.
---
