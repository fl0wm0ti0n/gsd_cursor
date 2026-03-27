# PO to TL archive pack (2026-03-27)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 24
- First archived heading: `## Discovery Addendum — US-0076`
- Last archived heading: `## Discovery Addendum — US-0076`
- Verification tuple (mandatory):
  - archived_body_lines=18
  - retained_body_lines=783

---

## Discovery Addendum — US-0076

- **Scope**: Executable merged-scratchpad wiring for **`SYNC_*`**, **`ALLOW_AUTO_PUSH`**, and
  **`AUTO_PUSH_BRANCH_ALLOWLIST`** so opt-in push honors the **US-0038** gate chain with
  deterministic reason codes; **no** behavior change when auto-push is off.
- **Conclusions**: Gap validated (**R-0053**): **`validate-and-push`** currently does not enforce
  scratchpad merge inputs. **PO** recommends extending **`validate-and-push`** (PS1/SH parity) over
  new entrypoints unless architecture mandates a split. **`by_phase`**/**`by_milestone`** need an
  explicit boundary signal at invocation (not implicit Cursor phase). **AC-5** QA blocking rule
  must be architecture-bounded (sprint artifact contract).
- **Next recommendation**: Proceed with **`/research`** ( **`R-0053`** current) then **`/architecture`**
  to lock phase-boundary input, QA scan rule, installer/Python merge reuse vs duplicate, and
  **DEC-0058** / **DEC-0018** amendment plan.
- **Artifacts**: `docs/product/vision.md` (Discovery Notes — US-0076), `docs/product/backlog.md`
  (US-0076 discovery refinements), `docs/engineering/research.md` (**R-0053**).

---

