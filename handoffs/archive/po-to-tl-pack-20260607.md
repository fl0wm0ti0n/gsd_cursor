# PO to TL archive pack (2026-06-07)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 14
- First archived heading: `## Orchestrated discovery handoff — BUG-0010 / auto-20260606-02`
- Last archived heading: `## Orchestrated discovery handoff — BUG-0010 / auto-20260606-02`
- Verification tuple (mandatory):
  - archived_body_lines=55
  - retained_body_lines=785

---

## Orchestrated discovery handoff — BUG-0010 / auto-20260606-02

### Target

- `bug_id=BUG-0010`
- `orchestrator_run_id=auto-20260606-02`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-BUG0010-discovery-20260606T141701Z-fresh`
- `next_scheduled_phase=research`
- `segment_work_item_kind=bug`
- `bug_queue_position=2` / `bug_queue_remaining=2`

### Summary

- **`/discovery`** **PASS** — root cause confirmed: `enforce-triad-hot-surface.py` `STORY_HEADING` matches only H1 `# US-xxxx`; `## US-xxxx` story sections invisible → `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` when `architecture.md` exceeds `ARCH_HOT_MAX_LINES` with zero archivable chunks. Kit repo mixed inventory: **26** H1 + **5** H2 `## US-` (3495 lines). Operator fix (**both**, intake-locked): (A) extend archiver for `##` backward-compat rollover; (B) enforce H1 `# US-xxxx` for new `/architecture` writes.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Key findings (research inputs)

1. **Defect line**: `STORY_HEADING = re.compile(r'^# US-\d{4}\s*[:\u2014\-].+$')` — `split_arch_stories` / `rollover_architecture` lines 138–356.
2. **Failure mode**: oversize + `stories=[]` → `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` (not `ARTIFACT_HOT_SURFACE_OVERSIZE` after failed rollover attempt).
3. **Kit vs downstream**: kit can rollover via H1 boundaries; `##`-only downstream repos cannot (operator: 3021/3000 lines).
4. **Mixed-file precedence (discovery stub)**: H1 wins when same `US-xxxx` at both levels; only `## US-\d{4}` is a story boundary (not generic `##`).
5. **Enforcement surfaces**: `.cursor/commands/architecture.md` + `template/`; optional validator script; `enforce-triad-hot-surface.py --self-test`; runbook triad section; harness + template parity.

### Research asks (extend R-0076)

1. Dual-level regex shape and merge algorithm for `split_arch_stories`.
2. Mixed-file precedence table (kit has US-0067..0070 + US-0083 at H2).
3. Validator placement and reason-code family for forward enforcement.
4. Block vs warn at `/architecture` completion boundary.
5. Self-test + harness regression matrix (`##`-only, `# US-`, mixed, idempotent rollover).
6. `BUG-xxxx` H1 pattern parity; installer/template parity scope.

### Evidence refs

- `docs/product/backlog.md` (`### BUG-0010` — `discovery_notes`)
- `docs/product/vision.md` (Intake notes + Discovery Notes — BUG-0010)
- `docs/engineering/research.md` (**`R-0076`** discovery extension)
- `handoffs/intake_evidence/BUG-0010-intake-20260606.json`
- `scripts/enforce-triad-hot-surface.py`; `decisions/DEC-0054.md` §2
- `docs/engineering/architecture.md` (mixed `# US-` / `## US-` inventory)
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (research pointer)

### Next

- **`/research`** (fresh **tech-lead** context) for **`BUG-0010`** — resolve **`R-0076`** Q1–Q6 before **`/architecture`**.

### Decision gate

- **None** — discovery satisfied; bug **OPEN**.

---

