# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 17
- First archived heading: `## Discovery Addendum — US-0088 (tail)`
- Last archived heading: `## Discovery Addendum — US-0085 (tail)`
- Verification tuple (mandatory):
  - archived_body_lines=62
  - retained_body_lines=796

---

## Discovery Addendum — US-0088 (tail)

- **Orchestrator**: **`auto-20260405-01`** — discovery complete in fresh **PO** context (**`2026-04-12T22:00:00Z`**).
- **`fresh_context_marker=po-US0088-discovery-20260412T220000Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`## US-0088`** — discovery_notes **PASS**); **`docs/engineering/state.md`** (Discovery checkpoint + isolation + **DEC-0038** strict proof); **`docs/engineering/research.md`** **`R-0071`** (discovery survey extension); **`handoffs/resume_brief.md`** → **`/research`**.
- **Scope recap**: **Continuous `/auto`** through intersected phases per **Step 5** until **US** or **sprint-segment** boundary; **`AUTO_BACKLOG_DRAIN=1`** with **`backlog_drain_stories_remaining_budget=9`**; **quiet** operator notifications only on **`decision_gate`**, **`error`**, **`pause`**, **`loop_max`**, **`blocked`**, **missing inputs**; regression for **one-phase-stop** + **drain advance**; **spawn-only** unchanged (**BUG-0006** / **US-0069**).
- **Scratchpad context (merged)**: **`INTAKE_GUIDED_MODE=1`**, **`EARLY_RESEARCH=1`**, **`TOKEN_PROFILE=balanced`** — research must reconcile **`AC-2`** with optional **`AUTO_QUIET`** vs profile composition.
- **Research asks** (extend **`R-0071`**):
  1. Line-level **Step 5** vs **`auto.md`** / reference / runbook drift that enables **single-spawn** misread.
  2. **Contract-test** shape: assert continuation when policy requires it; fixture boundaries for orchestrator vs subagent roles.
  3. **`resume_brief` / `state.md`** tuple for **phase depth** + **story cursor** under **US-0037** / **DEC-0069** during long **`/auto`** runs.
  4. **US-0087** mutex: cite **R-0070** / **`# US-0087`** only — no new bug-queue semantics in **US-0088**.
- **Risks**: Over-quiet automation hiding gates; **RESUME_BRIEF_STALE** false positives; template/command parity drift (**AC-5** / **AC-10**).
- **Status authority**: **`US-0088`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next** *(historical at discovery writer)*: **`/research`** — **PASS** **`2026-04-12T23:15:00Z`**; see **Research Addendum — US-0088** below → **`/architecture`**.
- **Decision gate before research**: none (discovery satisfied).

---

## Research Addendum — US-0088 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-12T23:15:00Z`**).
- **Evidence**: **`docs/engineering/research.md`** **`R-0071`** (Step 5 vs compact-step drift, contract-test anchors, **`AUTO_QUIET`** vs **`TOKEN_PROFILE`**, **`resume_brief`/`state.md`** pairing); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0088`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** **`proof_hash=dce665eedb088088e3205e3c81575c45af5cdda1108af0aa3b4f6370461c52c0`**); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Findings**: Normative **multi-phase** loop lives in **`auto-orchestration-reference.md`** **`## Steps`** item **5**; **`.cursor/commands/auto.md`** compact numbering diverges — architecture should lock cross-anchors or outer-driver equivalence (**AC-1**).
- **Next**: **`/architecture`** — **`docs/engineering/architecture.md`** **`# US-0088`** (quiet, drain, resume, tests) + optional **DEC** if required.
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

## Sprint Plan Addendum — US-0088 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/sprint-plan`** complete in fresh **tech-lead** context (**`2026-04-12T23:55:00Z`**).
- **`fresh_context_marker=tl-US0088-sprint-plan-20260412T235500Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`sprint_plan_notes`** under **`## US-0088`**); **`sprints/S0072/sprint.md`**, **`sprints/S0072/tasks.md`**, **`sprints/S0072/plan-verify.json`** (**PENDING** / **`AWAITING_QA_PLAN_VERIFY`**); **`docs/engineering/state.md`** (Sprint-plan checkpoint + **DEC-0038** **`proof_hash=e160a10f33af56b56437d3be302aeceedc47ab995563169402a068b82b3318ae`**); **`handoffs/resume_brief.md`**, **`handoffs/tl_to_dev.md`**, **`handoffs/qa_plan_verify.md`** → **`/plan-verify`** (**qa**).
- **Coverage intent**: **AC-1..AC-7** ↔ **T-001..T-007** for continuous **`/auto`**, **`AUTO_QUIET`**, **`US-0044`** drain + tests, **`template/`** parity, **`# US-0088`** consistency, runbook recipe.
- **Status authority**: **`US-0088`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next**: **`/plan-verify`** (**qa**) for **`S0072`** — then **`/execute`** (**dev**) when **`plan-verify.json`** → **PASS**.

---

## Discovery Addendum — US-0085 (tail)

- **Orchestrator**: **`auto-20260405-01`** — discovery complete in fresh **PO** context (**`2026-04-13T12:05:00Z`**).
- **`fresh_context_marker=po-US0085-discovery-20260413T120500Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`## US-0085`** — discovery_notes **PASS**); **`docs/product/vision.md`** (**Discovery Notes — US-0085**); **`docs/engineering/state.md`** (Discovery checkpoint + isolation + **DEC-0038** strict proof); **`docs/engineering/research.md`** **`R-0072`** (discovery survey stub); **`handoffs/resume_brief.md`** → **`/research`**.
- **Scope recap**: Standardize **repo-root `.env`** (gitignored) for `*Env` values used by **`.cursor/remote.json`** and **`release-targets.json`** operator connectivity flows (**US-0064**); committed **`.env.example`** with names only; **`.cursorignore`** + agent/rule exclusion so AI never reads `.env`; runbook + `runtime-connectivity.md` + `us-0084-remote-e2e.md` doc updates; optional AC-8 helper; template parity; regression tests.
- **Intake evidence**: `handoffs/intake_evidence/US-0085-intake-20260404.json` (**`small-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`**).
- **Market context**: `.env` + `.gitignore` is baseline; AI dev tools require **`.cursorignore`** and/or explicit agent rules because agents have developer-level filesystem access. Defense-in-depth (config exclusion + behavioral rules) is industry practice.
- **Repo survey findings**: `.gitignore` exists (no `.env` entry); no `.cursorignore`; no `.env.example`; `runtime-connectivity.md` and `us-0084-remote-e2e.md` in active + `template/`.
- **Research asks** (extend **`R-0072`** in **`/research`**):
  1. Full `*Env` variable name inventory from `.cursor/remote.json` template and `release-targets.json` schema for `.env.example` content.
  2. `.cursorignore` file format and path-matching semantics; whether Cursor rules augment or replace it for agent file-context exclusion.
  3. AC-8 decision inputs: deterministic `scripts/print_remote_env_hint.py` (names-only) vs documented shell recipe.
  4. AC-9 regression test shape: `git check-ignore` fixture or Python test.
  5. Template parity touchpoints for new/modified files (`.gitignore`, `.cursorignore`, `.env.example`, runbook, runtime-connectivity, us-0084-remote-e2e, rules).
- **Risks**: `.cursorignore` syntax may differ across Cursor versions; `.env` pattern may conflict with framework-generated `.env` in generated projects; AC-8 helper could leak secret patterns if not strictly names-only.
- **Status authority**: **`US-0085`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next**: ~~**`/research`**~~ → **`/architecture`** (tech-lead) for **US-0085**.
- **Decision gate before research**: none (discovery satisfied; story **OPEN**).

---

