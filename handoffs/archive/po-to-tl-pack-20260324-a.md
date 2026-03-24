# PO to TL archive pack (2026-03-24)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 23
- First archived heading: `## Discovery Addendum — US-0075 (2026-03-26)`
- Last archived heading: `## Intake Addendum — Configurable Guided Intake Behavior`
- Verification tuple (mandatory):
  - archived_body_lines=66
  - retained_body_lines=765

---

## Discovery Addendum — US-0075 (2026-03-26)

### Discovery focus

- Example **`.cursor/scratchpad.local.example.md`** must refresh on every install/upgrade scratchpad touch **before or with** materialized **`.cursor/scratchpad.md`** (**AC-1**, **AC-3**).
- **AC-11**: machine-verifiable paired **section + `KEY=`** inventory (active + **`template/`** pairs); no framework key in only one paired file without a documented manifest exception.

### TL conclusions

- Ordering + parity are one contract across installers, manifest, and tests (splitting re-opens drift).
- Example = operator copy-from catalog; materialized baseline = **DEC-0055** merge input; **`.cursor/scratchpad.local.md`** stays user-owned — diagnostics name which layer changed (**AC-5**).
- Regression: stale-example + fresh-template upgrade → post-run example matches template bytes (**AC-6**, **AC-9**).

### Research targets (**`R-0052`**)

1. Deterministic refresh sequence: **`installer.ps1` / `.sh` / `.py`**, **`bin/its-magic.js`**, **`installer-owned-paths.manifest`** (+ `template/` mirror).
2. Parity check spec: normalization, **`KEY=`** taxonomy, allowed value-only differences in example.
3. **DEC-0055** / **DEC-0039** / **US-0057** interaction — amend **DEC** only if ordering needs normative text beyond current records.

### Next

- **`/research`** (extend **`R-0052`**), then **`/architecture`** if a **DEC** tweak is required.

> Full narrative also in `docs/product/vision.md` (**Discovery Notes — US-0075**) and `docs/product/backlog.md` (discovery refinement). Prior rollover copy: `handoffs/archive/po-to-tl-pack-20260321-c.md`.

---

## Intake Addendum — Configurable Guided Intake Behavior

### New intake

User requests stronger PO intake behavior:
- Ask reasonable follow-up questions when unclear.
- Suggest options instead of prematurely selecting implementation.
- Include PO web research.
- Provide a switch to disable this proactive behavior.

### Overlap and duplicate evaluation

- Existing overlap:
  - `US-0021` (DONE): already requires critical evaluation, alternatives, and user-final-decision behavior.
  - `US-0029` (inconsistent status across artifacts, but behavior already present in active command/agent docs): includes PO early web research and `EARLY_RESEARCH` toggle.
- Gap identified:
  - No single intake behavior switch that disables proactive follow-up + options + intake-time research while keeping baseline duplicate safety.
- Decision:
  - Create `US-0033` as a focused behavior-mode story instead of reopening/compressing prior story scope.

### Accepted story

#### US-0033 — Configurable Guided Intake Behavior
- Priority: P1
- Status: OPEN
- Intent: default guided intake quality, optional low-touch mode for teams that want minimal interaction overhead.

### TL guidance and boundaries

- In scope:
  - Define one explicit scratchpad flag for intake behavior mode (default guided/on).
  - Specify guided mode requirements (targeted follow-ups, options, recommendation without overriding user decision).
  - Specify low-touch mode requirements (no proactive follow-up/options/research overhead).
  - Preserve baseline duplicate/overlap check in both modes.
  - Keep active and `template/` guidance aligned.
- Out of scope:
  - Changing architecture/sprint/release semantics.
  - Removing manual `/research` usage when low-touch mode is enabled.

