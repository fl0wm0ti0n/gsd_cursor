# PO to TL archive pack (2026-03-21)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 23
- First archived heading: `## Discovery Addendum — US-0073`
- Last archived heading: `## Discovery Addendum — US-0073`
- Verification tuple (mandatory):
  - archived_body_lines=50
  - retained_body_lines=768

---

## Discovery Addendum — US-0073

### Discovery focus and references

- Discovery objective: refine **scratchpad delivery simplification** from intake
  intent into architecture-ready constraints: one canonical installer
  baseline, deterministic **merged scratchpad** semantics, and non-regressive
  automation behavior.
- References captured:
  - `docs/product/vision.md` — Discovery Notes — US-0073
  - Overlap stories: `US-0018` (upgrade/install), `US-0057` / `DEC-0039`
    (example refresh + ownership), `US-0072` (hot surfaces; orthogonal)
  - Research seed: `R-0050` in `docs/engineering/research.md`

### Discovery conclusions for TL

- Treat **delivery model** and **resolution precedence** as explicit design
  outputs: either retain a committed `.cursor/scratchpad.md` baseline or adopt
  example-only with a documented materialization path (generated or copied on
  first use) — ambiguity is unacceptable for `/auto` flag reads.
- **Fail-closed** remains mandatory when required automation keys are missing or
  invalid after merge; diagnostics must name the layer (example, committed
  baseline, local) and remediation (`AC-4`).
- **Upgrade parity**: `--mode upgrade` must apply the chosen policy while
  preserving `.cursor/scratchpad.local.md` and refreshing framework-owned
  example per `DEC-0039` (`AC-3`, `AC-5`).
- **Regression posture**: plan for installer parity (PS1/sh/py/CLI), README +
  runbook operator narrative, and tests for fresh install, upgrade from dual-file
  history, missing baseline, and local-only overrides (`AC-6`–`AC-9`,
  `AC-10` overlap resolution with `US-0018`/`US-0057`).

### Research handoff targets

1. Document candidate merge orders and failure modes for example-only vs
   dual-artifact baselines; pick a single canonical precedence for
   implementation.
2. Define migration rules for existing repos (both files present) under each
   candidate model.
3. Align findings with `DEC-0039` / `US-0057` and `US-0018` so no ownership or
   upgrade regression is introduced.
4. Produce minimal acceptance-test mapping updates if research changes AC
   wording (PO backlog remains authoritative for AC edits in `/sprint-plan`).

### Recommendation

- Proceed to **`/research`** for **`US-0073`** with emphasis on merged
  scratchpad semantics, installer materialization, and fail-closed diagnostics.

---

