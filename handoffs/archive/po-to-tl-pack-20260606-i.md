# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 13
- First archived heading: `## PO → TL Handoff — US-0089 / US-0090 (Intake) (tail mirror)`
- Last archived heading: `## Architecture Addendum — US-0089 (tail mirror)`
- Verification tuple (mandatory):
  - archived_body_lines=112
  - retained_body_lines=786

---

## PO → TL Handoff — US-0089 / US-0090 (Intake) (tail mirror)

> Placement: **tail** hot copy for TL read model (**runbook**). Prefix rollovers: **`handoffs/archive/po-to-tl-pack-20260414.md`** (first **US-0089**/**US-0090** prepend), then **`handoffs/archive/po-to-tl-pack-20260414-a.md`** (line-cap rebalance).

### New intake

Operator wants **Caveman-style** terse communication (**JuliusBrussee/caveman**-like) in **Cursor**, **scratchpad-configurable**, **default off**, **without losing** existing **its-magic** features. **Split stories**: **US-0089** (response style + scratchpad + rules/skill + tests) then **US-0090** (optional **input-side** file compression with **original preserved** and **hard deny** for canonical/evidence paths).

### Evidence

- **`handoffs/intake_evidence/US-0089-intake-20260414.json`** — **`first-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`** (`intake_run_id=cursor-20260414-caveman-intake`).
- **`docs/product/backlog.md`** — **`## US-0089`**, **`## US-0090`**; **`docs/product/acceptance.md`**; **`docs/product/vision.md`**; **`docs/engineering/research.md`** **`R-0073`**.

### Decomposition (US-0051)

- **US-0089**: Caveman **output** mode + scratchpad keys + **rules/skill** + **`architecture.md`** **`# US-0089`** + tests (**default-off** invariant).
- **US-0090**: Optional compress path; **gates** on **`CAVEMAN_MODE`** + explicit compress policy; **deny** intake evidence, backlog, acceptance, **`state.md`**, **`.env`**; **`template/`** parity.

### TL scope / risks

- Lock **`TOKEN_PROFILE`** vs **`CAVEMAN_*`** composition (**US-0080** lineage).
- **US-0090** loss avoidance: **sidecar originals** + immutable deny-list; never rewrite **`handoffs/intake_evidence/*.json`** by default (**US-0078** / **DEC-0060**).

### Triad (**DEC-0054**) verification tuple

- **boundary**: `2026-04-14` (intake + line-cap rebalance)
- **moved**: (1) first prepend → **`handoffs/archive/po-to-tl-pack-20260414.md`** (`units=4,1`); (2) rebalance prefix → **`handoffs/archive/po-to-tl-pack-20260414-a.md`** (`units=1`)
- **retained**: hot **`handoffs/po_to_tl.md`** within **`PO_TO_TL_HOT_MAX_LINES`** / section caps after second rollover
- **pack_ref**: **`handoffs/archive/po-to-tl-pack-20260414.md`**, **`handoffs/archive/po-to-tl-pack-20260414-a.md`**
- **tooling**: `python scripts/enforce-triad-hot-surface.py --rollover` then `--check` → **PASS**

### Recommendation

**`/discovery`** (**US-0089** first) → **`/research`** (**`R-0073`**) → **`/architecture`** → **`/sprint-plan`** (**US-0089** before **US-0090**).

---

## Discovery Addendum — US-0089 (tail mirror)

- **Orchestrator**: **`auto-20260418-01`** — **`/discovery`** complete in fresh **PO** context (**`2026-04-18T12:05:00Z`**).
- **`fresh_context_marker=po-US0089-discovery-20260418T120500Z-fresh`**
- **Scope closure**: Response-side (voice) only; input-side file compression stays fully out of scope (explicit handoff to **US-0090**). Confirmed in-scope surfaces = scratchpad keys (**`CAVEMAN_MODE`** default **0**, **`CAVEMAN_LEVEL`** enum reserved — exact values architecture-locked), Cursor rules and/or focused skill composing with existing **`.cursor/skills/its-magic/SKILL.md`**, operator control phrasing contract, tests (default-off byte-equivalence + scratchpad doc markers), **`# US-0089`** architecture section, and **`template/`** parity for all touched `.cursor/` + `docs/engineering/` surfaces.
- **Risks flagged for research/architecture**: (1) Caveman voice vs **US-0021** anti-fluff + **US-0088 `AUTO_QUIET`** non-suppressible gate list — gate language, reason codes, `[BUG_VALIDATION_OK]`, `[INTAKE_EVIDENCE_VALIDATION_OK]`, `blocked`, `missing input`, `pause`, `loop_max` must stay verbatim; (2) **US-0071** — terseness does not license dropping visible **`US-xxxx`** / **`DEC-xxxx`** / **`R-xxxx`** / **`BUG-####`** IDs or reason codes from user-facing output; (3) **US-0080 / `TOKEN_PROFILE`** composition — orthogonal by default; docs must publish precedence matrix or explicit non-substitution statement (no silent override either direction); (4) literal-region preservation rule (fenced code, paths, AC checklists, filenames) as machine-verifiable invariant; (5) template parity drift if only active **`.cursor/`** is updated (**US-0017**).
- **Decision gate posture**: **none** — discovery satisfied; no DEC requested at this boundary. Story remains **OPEN** in **`docs/product/backlog.md`** per **US-0045**.
- **Next phase**: **`/research`** (fresh **tech-lead**) extending **`R-0073`** — lock composition contract options, default-off byte-equivalence test strategy, operator control phrasing shortlist, and TOKEN_PROFILE precedence matrix. No architecture/sprint artifacts authored in this PO discovery segment.
- **Artifact refs**:
  - **`docs/product/backlog.md`** — **`## US-0089`** `discovery_notes` (2026-04-18, PO, `auto-20260418-01`)
  - **`docs/product/vision.md`** — **Discovery Notes — US-0089**
  - **`docs/engineering/research.md`** — **`R-0073`** Discovery extension (2026-04-18)
  - **`handoffs/resume_brief.md`** — new top pointer post-`/discovery` US-0089
  - **`docs/engineering/state.md`** — Discovery checkpoint (2026-04-18) — US-0089 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/research`)

---

## Research Addendum — US-0089 (tail mirror)

> Placement: **tail** hot copy for TL read model. `orchestrator_run_id=auto-20260418-01`. Research-phase extension of **`R-0073`** completed in fresh **tech-lead** context (**`2026-04-18T12:15:00Z`**, `fresh_context_marker=tl-US0089-research-20260418T121500Z-fresh`).

- **Closure**: **`/research`** (**tech-lead**) **PASS** for **US-0089**. **`R-0073`** extended with eight implementation anchors, risks, and mitigations; **no DEC authored** (architecture owns decisions); **no architecture section** authored.
- **Anchors (summary)**:
  1. **TOKEN_PROFILE × CAVEMAN**: recommend **Option A (orthogonal, non-substitution)** — `TOKEN_PROFILE` owns context-breadth (**US-0080** / **DEC-0062**), `CAVEMAN_*` owns voice; publish a single non-substitution paragraph in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (+ `template/` mirrors). Option B (explicit precedence matrix) is the architecture-fallback; Option C (collapse) rejected.
  2. **Rule vs rule+skill**: Option A = `.cursor/rules/caveman.mdc` only (minimal surface); Option B = rule + `.cursor/skills/its-magic-caveman/SKILL.md` (discoverability). Skill-only rejected. Non-suppressible gate list stays in the rule either way.
  3. **Default-off tests**: extend **`tests/auto_command_contract_test.py`** in place with `test_caveman_default_off_*` subtests (scratchpad key presence active + `template/`, existing `required` token list intact, non-suppressible gate vocabulary preserved). Voice quality **not** unit-tested.
  4. **Operator toggle vocabulary**: shortlist `caveman on|off`, `stop caveman` / `normal mode`, `caveman: lite|full|ultra`. Scratchpad is authoritative across subagent spawns; session toggle = overlay for next turn; current-turn gate artifacts remain literal.
  5. **Literal-region invariant**: 9-zone protected set (fenced code, paths, AC checklists, ALL_CAPS reason codes, IDs `US-xxxx`/`DEC-xxxx`/`R-xxxx`/`BUG-####`/`S0xxx`/`T-xxx`, contract markers `[BUG_VALIDATION_OK]`/`[INTAKE_EVIDENCE_VALIDATION_OK]`, strict-proof tuple fields, isolation-evidence fields, commit/git refs). Rule MUST, not SHOULD.
  6. **External pattern (JuliusBrussee/caveman, MIT)**: portable concepts only (levels, "compress prose not code"); vendor install path (`npx skills add`) and token-savings claims stay **out** of normative kit docs; single-line attribution acceptable.
  7. **Scratchpad key naming**: recommend `CAVEMAN_MODE=0|1` default **0**, `CAVEMAN_LEVEL=lite|full|ultra` default empty; reserved-for-US-0090 keys `CAVEMAN_COMPRESS_INPUT=0|1` (default **0**) and `CAVEMAN_FILE_SCOPE=` (empty) as documented **no-ops** until US-0090.
  8. **Template parity inventory**: 9-item file list for **`/sprint-plan`** to atomize (scratchpad active + template, scratchpad example active + template, new rule active + template, optional new skill active + template, reference + runbook + template mirrors, architecture + tests active-only).
- **Architecture asks (DEC-xxxx hints)**:
  - `DEC-xxxx` — TOKEN_PROFILE × CAVEMAN precedence (**Option A** recommended; Option B fallback).
  - `DEC-xxxx` — rule-only (Option A) vs rule + focused skill (Option B).
  - `DEC-xxxx` — scratchpad key spellings locked **before** contract tests reference them.
  - `DEC-xxxx` — 9-zone literal-region invariant published in `# US-0089`.
  - `DEC-xxxx` — canonical operator phrase set + runbook publication location.
- **Status authority**: **US-0089** stays **OPEN** in **`docs/product/backlog.md`** per **US-0045**.
- **Next phase**: **`/architecture`** (fresh **tech-lead**) for **US-0089** — lock DEC(s) + write `docs/engineering/architecture.md` `# US-0089`.
- **Decision-gate posture**: **none** expected at pre-architecture boundary (architecture asks are routine, not gate-blocking).
- **Artifact refs**:
  - **`docs/engineering/research.md`** — **`R-0073`** Research extension (2026-04-18, TL, `auto-20260418-01`)
  - **`docs/product/backlog.md`** — **`## US-0089`** `research_notes` (2026-04-18, TL, `auto-20260418-01`)
  - **`handoffs/resume_brief.md`** — new top pointer post-`/research` US-0089
  - **`docs/engineering/state.md`** — Research checkpoint (2026-04-18) — US-0089 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/architecture`)

---

## Architecture Addendum — US-0089 (tail mirror)

> Placement: **tail** hot copy for TL read model. `orchestrator_run_id=auto-20260418-01`. Architecture-phase lock completed in fresh **tech-lead** context (**`2026-04-18T12:30:00Z`**, `fresh_context_marker=tl-US0089-architecture-20260418T123000Z-fresh`).

- **Closure**: **`/architecture`** (**tech-lead**) **PASS** for **US-0089**. **`DEC-0072`** authored and accepted; **`docs/engineering/architecture.md`** **`# US-0089`** written; **`docs/engineering/decisions.md`** (index + canonical record) updated.
- **DEC ref**: **`DEC-0072`** — *Caveman mode scratchpad contract, composition surface, and default-off invariant*. Status **Accepted** 2026-04-18.
- **Locked decisions (summary)**:
  1. **TOKEN_PROFILE × CAVEMAN precedence** = **Option A (orthogonal, non-substitution)**. Verbatim non-substitution paragraph in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (active + `template/`).
  2. **Composition surface** = **Option A (rule-only)**. New `.cursor/rules/caveman.mdc` active + `template/.cursor/rules/caveman.mdc`. **No new skill** in US-0089; `.cursor/skills/its-magic/SKILL.md` unchanged.
  3. **Scratchpad keys**: `CAVEMAN_MODE=0|1` default **`0`**; `CAVEMAN_LEVEL=lite|full|ultra` default empty (fallback `full` when MODE=1; unknown value -> `CAVEMAN_LEVEL_UNKNOWN`). Reserved-for-US-0090 no-ops `CAVEMAN_COMPRESS_INPUT=0|1` default **`0`** and `CAVEMAN_FILE_SCOPE=` empty (documented no-ops with explicit "inert in US-0089" comments).
  4. **9-zone literal-region invariant** (hard **MUST**): fenced code, file paths, AC checklists, reason codes (`ALL_CAPS_WITH_UNDERSCORES`), IDs (`US-xxxx`/`DEC-xxxx`/`R-xxxx`/`BUG-####`/`S0xxx`/`T-xxx`), contract markers (`[BUG_VALIDATION_OK]`/`[INTAKE_EVIDENCE_VALIDATION_OK]`/siblings), strict-proof tuple fields (DEC-0038), isolation evidence fields (DEC-0029), git/commit refs.
  5. **Canonical operator phrases**: `caveman on`, `caveman off`, `stop caveman`, `normal mode`, `caveman: lite|full|ultra`. Scratchpad authoritative across subagent spawns; session toggles are next-turn overlays only; current-turn gate artifacts remain literal.
  6. **Default-off tests**: extend `tests/auto_command_contract_test.py` **in place** with **8** `test_caveman_default_off_*` subtests (exact byte strings locked in DEC-0072 §3 / §6).
  7. **Template parity inventory** — 8 rows locked in architecture `# US-0089` §7 + DEC-0072 §7; includes negative-parity row for `.cursor/skills/its-magic/SKILL.md` (no change).
  8. **Non-goals (hard)**: no input-side compression (US-0090 only), no `TOKEN_PROFILE` change, no canonical artifact rewrites, no new npm/python deps, no `npx skills add` leak, no voice-quality unit test.
- **Next phase**: **`/sprint-plan`** (fresh **tech-lead**) for **US-0089** — atomize DEC-0072 §7 parity inventory into tasks against **AC-1..AC-8** (within `SPRINT_MAX_TASKS=12`).
- **Decision-gate posture**: **none** expected before **`/sprint-plan`**.
- **Status authority**: **US-0089** stays **OPEN** in **`docs/product/backlog.md`** per **US-0045**.
- **Artifact refs**:
  - **`decisions/DEC-0072.md`**
  - **`docs/engineering/architecture.md`** **`# US-0089`**
  - **`docs/engineering/decisions.md`** (index + context pack; canonical full-record entry)
  - **`docs/product/backlog.md`** — **`## US-0089`** `architecture_notes` (2026-04-18, TL, `auto-20260418-01`)
  - **`handoffs/tl_to_dev.md`** — **US-0089** pre-sprint architecture handoff (top of file)
  - **`handoffs/resume_brief.md`** — new top pointer post-`/architecture` US-0089 (prior post-`/research` US-0089 marked superseded)
  - **`docs/engineering/state.md`** — Architecture checkpoint (2026-04-18) — US-0089 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/sprint-plan`)

