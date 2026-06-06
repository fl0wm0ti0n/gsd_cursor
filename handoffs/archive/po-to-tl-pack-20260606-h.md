# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 3
- Retained units in hot file: 15
- First archived heading: `## Research Addendum — US-0085 (tail mirror)`
- Last archived heading: `## Research Addendum — US-0086 (tail mirror)`
- Verification tuple (mandatory):
  - archived_body_lines=55
  - retained_body_lines=793

---

## Research Addendum — US-0085 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-13T12:15:00Z`**).
- **`fresh_context_marker=tl-US0085-research-20260413T121500Z-fresh`**
- **Evidence**: **`docs/engineering/research.md`** **`R-0072`** (extended — `*Env` inventory, `.cursorignore` semantics, AC-8/AC-9 recommendations, template parity, risks); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0085`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** **`proof_hash=b04b45a6f9110e8da20cfee684320bc05c2cb775387f651a2ab315aa982f221b`**); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Key findings**:
  1. **`*Env` inventory**: 20 unique env var names (3 from `remote.json` template, 17 from `release-targets.json`) for `.env.example`.
  2. **`.cursorignore` confirmed**: `.gitignore` syntax, blocks agent file tools, does **not** block terminal/MCP. Defense-in-depth requires 4 layers.
  3. **AC-8**: recommend `scripts/print_remote_env_hint.py` (names-only, cross-platform, parity check with JSON schemas).
  4. **AC-9**: `git check-ignore` Python test fixture.
  5. **Template parity**: 7 touchpoints; no `template/.gitignore` exists (architecture decides create vs omit).
  6. **AC-10**: `remote_config_summary.py` unaffected — reads `remote.json` names, not `.env` values.
  7. **Risks**: terminal bypass (medium), open-tab leak (low), framework collision (low).
- **Next**: **`/architecture`** — **`docs/engineering/architecture.md`** **`# US-0085`** (defense-in-depth layers, `.env.example` content contract, template parity decisions, AC-8 helper shape).
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

## Discovery Addendum — US-0086 (tail)

- **Orchestrator**: **`auto-20260405-01`** — discovery complete in fresh **PO** context (**`2026-04-13T18:30:00Z`**).
- **`fresh_context_marker=po-US0086-discovery-20260413T183000Z-fresh`**
- **Evidence**: **`docs/product/backlog.md`** (**`## US-0086`** — discovery_notes **PASS**); **`docs/product/vision.md`** (**Discovery Notes — US-0086**); **`docs/engineering/research.md`** (**`R-0068`** discovery extension); **`docs/engineering/state.md`** (Discovery checkpoint + isolation + **DEC-0038** strict proof); **`handoffs/resume_brief.md`** → **`/research`**.
- **Scope recap**: keep **manual** workflow default local/no-reroute; add **automation-only** deterministic target choice path for dev/CI/DI/QA/release when enabled.
- **Locked discovery contracts**:
  1. Explicit intent phrase **"start container `<target_id>`"** resolves to canonical **`targets[].id`**.
  2. Unknown/disabled target must fail closed with deterministic reason-code diagnostics.
  3. Composition with **US-0085** remains strict: no `.env` reads, names-only outputs, no secret echo in evidence.
- **Research asks** (`/research`, extend **`R-0068`**):
  1. Deterministic routing matrix from changed-file classes + explicit operator intent for Docker/SSH/local selection.
  2. Evidence tuple contract for automation remote runs (`target_id`, `environment_label`, `automation_profile`) across execute/qa/release handoffs.
  3. Candidate reason-code vocabulary and scratchpad key naming options for architecture lock.
  4. Minimum regression-test surface for target-id resolution and mode-off/no-reroute behavior.
- **Status authority**: **`US-0086`** remains **OPEN** in **`docs/product/backlog.md`** (**US-0045**).
- **Next**: **`/research`** (**tech-lead**) for **`US-0086`**.
- **Decision gate before research**: none (discovery satisfied; story **OPEN**).

---

## Research Addendum — US-0086 (tail mirror)

- **Orchestrator**: **`auto-20260405-01`** — **`/research`** complete in fresh **tech-lead** context (**`2026-04-13T19:00:00Z`**).
- **`fresh_context_marker=tl-US0086-research-20260413T190000Z-fresh`**
- **Evidence**: **`docs/engineering/research.md`** **`R-0068`** (research extension with routing matrix, reason-code candidates, evidence tuple contract, external references); **`docs/product/backlog.md`** (**`research_notes`** under **`## US-0086`**); **`docs/engineering/state.md`** (Research checkpoint + **DEC-0038** strict proof); **`handoffs/resume_brief.md`** → **`/architecture`**.
- **Key findings**:
  1. **Routing precedence**: explicit NL intent `start container <target_id>` first, then automation-mode heuristic fallback, else local default.
  2. **External contract anchors**: GitHub path filters support deterministic CI routing; Docker context precedence supports stable target binding; OpenSSH options support fail-fast host validation.
  3. **Evidence tuple**: `target_id`, `environment_label`, `automation_profile`, `routing_source`, `secret_surface=names_only`.
  4. **Reason-code candidates** for architecture lock: `REMOTE_AUTOMATION_MODE_OFF`, `REMOTE_TARGET_UNKNOWN`, `REMOTE_TARGET_DISABLED`, `REMOTE_TARGET_UNROUTABLE`.
  5. **Security continuity** with **US-0085**: no `.env` reads; no secret values in logs/handoffs.
- **Next**: **`/architecture`** — lock scratchpad key names, reason codes, routing matrix, and parity/test surfaces for **AC-1..AC-10**.
- **Decision gate before architecture**: none (research satisfied; story **OPEN** **US-0045**).

---

