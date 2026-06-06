# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 13
- First archived heading: `## Orchestrated research handoff — BUG-0010 / auto-20260606-02`
- Last archived heading: `## Orchestrated research handoff — BUG-0010 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=52
  - retained_body_lines=778

---

## Orchestrated research handoff — BUG-0010 / auto-20260606-02

### Target

- `bug_id=BUG-0010`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`research`** (**`tech-lead`**)
- `fresh_context_marker=tl-BUG0010-research-20260606T163000Z-fresh`
- `next_scheduled_phase=architecture`
- `segment_work_item_kind=bug`
- `bug_queue_position=2` / `bug_queue_remaining=2`

### Summary

- **`/research`** **PASS** — extended **`R-0076`** with Q1–Q6 resolution. **Archiver**: two-pattern scan (`STORY_HEADING_H1` for `# US-` / `# BUG-`; `STORY_HEADING_H2` for `## US-`) + H1-wins precedence filter in `split_arch_stories`. **Enforcement**: in-place `enforce-triad-hot-surface.py` diff-gated policy — hard fail `ARCH_STORY_HEADING_LEVEL_INVALID` when H2 story-heading count increases during `/architecture`; grandfathered `## US-` sections remain rollover-visible. **Tests**: extended `--self-test` + `test_bug0010_*` + harness **§29A** candidate. **Template**: byte-identical script mirror only (no new parity scope).
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (architecture inputs)

1. **Dual-level split (Q1)**: Option B two-pattern scan + precedence filter — reject single alternation regex and two-pass merge.
2. **Precedence (Q2)**: H1 wins when same `US-xxxx` at both levels; only `^## US-\d{4}` is H2 boundary (not generic `##`).
3. **Validator (Q3)**: Extend `enforce-triad-hot-surface.py` in place; `count_h2_story_headings` + baseline snapshot at architecture mutation boundary.
4. **Severity (Q4)**: Diff-gated hard fail — not warn-only, not static fail on any legacy H2.
5. **Regression (Q5)**: Six fixture classes in `--self-test`; contract tests `test_bug0010_*`; harness **§29A**.
6. **BUG parity (Q6)**: `# BUG-xxxx` in H1 rollover family; forward enforcement targets `## US-` only.

### Evidence refs

- `docs/engineering/research.md` (**`R-0076`** research extension)
- `docs/product/backlog.md` (`### BUG-0010` — `research_notes`)
- `docs/product/acceptance.md` (`BUG-0010` row — unchecked)
- `handoffs/intake_evidence/BUG-0010-intake-20260606.json`
- `scripts/enforce-triad-hot-surface.py`; `decisions/DEC-0054.md`
- `docs/engineering/state.md` (Research checkpoint — this run)
- `handoffs/resume_brief.md` (architecture pointer)

### Architecture asks (companion DEC-xxxx)

1. Lock dual-level regex + precedence table + diff-gated enforcement API in companion **DEC-xxxx** composing on **DEC-0054** + **DEC-0043**.
2. Author `docs/engineering/architecture.md` **`# BUG-0010`** with archiver merge algorithm, reason codes, command/runbook contract, template parity inventory.
3. Confirm harness section id (**§29A** candidate) and fixture directory policy.

### Next

- **`/architecture`** (fresh **tech-lead** context) for **`BUG-0010`** — lock companion DEC + architecture section before **`/sprint-plan`**.

### Decision gate

- **None** — research satisfied; bug **OPEN**.

---

