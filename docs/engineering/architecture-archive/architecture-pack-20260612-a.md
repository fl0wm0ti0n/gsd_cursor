# Architecture archive pack (2026-06-12)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 5
- Retained units in hot file: 25
- First archived heading: `# US-0078: Enforced interactive intake question evidence`
- Last archived heading: `# US-0081: First-intake full-plan coverage and story-map gate`
- Verification tuple (mandatory):
  - archived_body_lines=285
  - preamble_lines=10
  - retained_body_lines=3448

---

# US-0078: Enforced interactive intake question evidence

## Overview

**`US-0078`** closes the gap between **`DEC-0050`** pack semantics and **provable** in-session questioning/confirmation. Intake MUST NOT persist backlog/acceptance changes unless each required pack topic has **`topic_coverage`** with a valid **`ref`**, **`asked_topics`** aligns with default asked-vs-covered rules, and assumption confirmations carry **`assumption_confirmation_ref`**. Research **`R-0055`** is normative for validation rules and **`AC-8`** fixtures; decision **`DEC-0060`** locks **`ref`** format and migration.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Policy text only | Rely on prompts/runbook | Rejected — silent persistence remains possible. |
| B — Heuristic inference | Infer coverage from model summaries | Rejected — not auditable; fails AC-1/AC-2. |
| C — Structured evidence + gate | **`topic_coverage`** + deterministic validator | **Chosen** — matches **`R-0055`** / **`DEC-0060`**. |

## Evidence model (runtime)

Persisted bundle (location: inline intake handoff block, sidecar JSON, or equivalent — execute chooses storage; validator consumes the same logical shape):

| Field | Role |
|-------|------|
| `selected_pack` | `first-intake-pack` \| `small-intake-pack` |
| `asked_topics` | Required keys actually **prompted** in-session |
| `missing_topics` | Unsatisfied keys at gate (empty when pass) |
| `topic_coverage` | One row per required key: `topic_key`, `satisfied_by`, `ref` |
| `satisfied_by` | `answer_ref` \| `assumption_confirmation_ref` |
| `ref` | **`ie:`** binding per **`DEC-0060`** §4 |
| `assumptions_confirmed` | Literal field per **`DEC-0050`** |
| `assumption_confirmation_ref` | Required for affirmative assumptions |

**Invariant**: “answered” set = keys in `topic_coverage`; audits compare to `asked_topics` per **`R-0055`** rule 3 (default fail-closed).

## Validation pipeline (deterministic)

1. Resolve `required_keys` from `selected_pack` (**`DEC-0050`** / intake command lists).
2. Validate each required key has a `topic_coverage` row with parseable **`ie:`** `ref` and matching metadata.
3. Enforce asked-vs-covered (default: every covered key ∈ `asked_topics`).
4. Enforce assumption literal + `assumption_confirmation_ref` (**`R-0055`** rules 4–5).
5. On failure: emit `INTAKE_REQUIRED_TOPIC_MISSING`, `INTAKE_REQUIRED_PACK_INCOMPLETE`, `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`, and/or umbrella `INTAKE_PERSISTENCE_BLOCKED`; **abort writes**.

**Modes**: **`INTAKE_GUIDED_MODE=1`** and **`0`** both run the pipeline; low-touch does not bypass the gate.

## Workflow integration

| Phase | Behavior |
|-------|----------|
| `/intake` | Emit questions/prompts; accumulate `asked_topics` and coverage rows; gate before persistence. |
| `/execute` | Implement validator, persistence ordering, and tests per **`DEC-0060`** + **`R-0055`**. |
| `/qa` | Verify negative paths and reason codes; scan for bypass of persistence hook. |
| Docs | Active + `template/` parity for intake/runbook/README (**AC-9**). |

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Friction for operators | Targeted diagnostics (**AC-7**); bounded prompts. |
| `ref` implementation drift | Single parser module + **`AC-8`** golden vectors. |
| Legacy stories without coverage | **`DEC-0060`** grandfather read-only until next intake touch supplies full evidence. |

## Tests strategy (**AC-8**)

Follow **`R-0055`** matrix (P1–P5): Tier A unit tests on synthetic `intake_evidence`; Tier B golden markdown snippets; Tier C dual-mode smoke (`INTAKE_GUIDED_MODE` ∈ {0,1}).

## Migration

Per **`DEC-0060`** §5: no silent partial writes; optional backfill tools are explicit and out of band.

## Decision linkage

- Research basis: **`R-0055`**
- Decision: **`DEC-0060`** (extends **`DEC-0050`**)

---

# US-0079: First-class bug issue workflow (`BUG-xxxx`)

## Overview

**`US-0079`** introduces a **second canonical work-item family** for defects: **`BUG-####`** with **`OPEN`/`DONE`** only, explicit intake routing, minimum reproducibility fields, and parallel **`US-0045`** reconciliation. Research **`R-0056`** informs field and test guidance; **`DEC-0061`** is normative for literals, routing signals, storage, and migration.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Track bugs as `US-xxxx` | Single artifact shape | Rejected — conflates feature intent and defects. |
| B — Full triage / SLA | Enterprise defect model | Rejected — explicit out of scope. |
| C — `BUG-xxxx` + lightweight lifecycle | Dedicated id + `OPEN`/`DONE` | **Chosen** — aligns with **`R-0056`** / **`DEC-0061`**. |

## Architecture surfaces

| Surface | Behavior |
|---------|----------|
| **`docs/product/backlog.md`** | Section **`## Bug issues (canonical)`**; append new bugs; sort by id; status in header. |
| **`docs/product/acceptance.md`** | Section **`## Bug acceptance (canonical)`** per **`DEC-0061`** §8 — portfolio checkboxes for **`BUG-xxxx`**. |
| Intake | **`INTAKE_WORK_ITEM_KIND`** (`story`/`bug`) **and/or** explicit **`/intake bug`**; fail closed without signal (**`DEC-0061`** §5). |
| Sprint / QA / release | Same traceability row style as **`US-0042`**; **`BUG-xxxx`** allowed alongside **`US-xxxx`**. |
| **`/ask`** | Extend id-family allowlists to **`BUG-####`**. |

## Schema (minimum)

**`environment`**, **`steps_to_reproduce`**, **`expected`**, **`actual`**, **`evidence_refs`** (non-empty). Optional **`related_us`**, **`blocks_us`**, **`duplicate_of`**, **`supersedes`**.

## Phase boundary visibility

Per **`DEC-0061`** §13: when a phase mutates bug records, **optional** **`bug_ids=<csv>`** on **`state.md`** phase boundary entries improves **US-0070 AC-10** inspectability without requiring backlog parses.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Duplicate US + BUG for same defect | **`duplicate_of`/`supersedes`**; routing fail-closed; docs in **`DEC-0061`**. |
| Validator drift | Single module + **`R-0056`** Tier A fixtures. |
| File size | Default single backlog section; optional split only per **`DEC-0061`** §2. |

## Tests strategy

Follow **`R-0056`** Tier A–D mapping to **AC-1..AC-10** (routing, schema, reconciliation, traceability spot-checks).

## Migration

Grandfather **`US-xxxx`**-only historical defects (**`DEC-0061`** §11); new work uses **`BUG-xxxx`** post-delivery.

## Decision linkage

- Research basis: **`R-0056`**
- Decision: **`DEC-0061`**

---

# US-0080: Token-cost hardening for orchestrated runs

## Overview

**`US-0080`** reduces **cache-read-equivalent** token volume for long `/auto` and phase-command runs by **structural** levers: slimmer repeated command/policy surfaces, **bounded phase-context** inputs, and **auditable** per-run metrics — without disabling cache, removing gates, or weakening **`US-0048`**, **`US-0056`**, **`US-0069`**, or **`US-0039`**. Research **`R-0057`** motivates vendor-aligned semantics; **`DEC-0062`** is normative for metric names, **`run_class_hash`**, evidence paths, parity manifest, and AC-10 trade-offs.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Rely on pricing / cache tolerance | No engineering change | Rejected — fails measurable AC-1/AC-2. |
| B — `TOKEN_PROFILE=lean` only | Scratchpad profile | Rejected — insufficient alone (**`R-0057`**). |
| C — Slimming + bounded context + committed metrics | Structural + auditable | **Chosen** — aligns with backlog and **`DEC-0062`**. |

## Metric and comparison model

- **Fields**: **`cache_read_tokens`**, **`input_tokens`**, **`output_tokens`**, **`phase_call_count`** per phase; optional **`cache_creation_tokens`**, **`orchestrator_call_estimate`**; host mapping per **`DEC-0062`** §1.
- **Comparable runs**: Same **`run_class_hash`** over the canonical tuple (**`DEC-0062`** §2): `story_id`, merged **`TOKEN_PROFILE`**, **`SECURITY_REVIEW`**, **`phase_policy_mode`**, ordered **`resolved_phase_plan`**, resume anchor triple.
- **AC-2 target**: ≥ **50%** reduction in **total run `cache_read_tokens`** vs baseline for the **same `run_class_hash`**, with gates unchanged.

## Evidence and observability

- **Append-only** **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** (or **`.jsonl`**) as canonical audit trail; **`docs/engineering/state.md`** carries **`token_cost_evidence_ref`** pointer (**`DEC-0062`** §3, §7).
- IDE usage panes remain **supplementary**.

## Slimming and parity

- **Active + `template/`** parity for touched **`.cursor/commands/`**, **`.cursor/rules/`**, and mirrored template paths — enforced via **`DEC-0062`** §5 manifest + CI extension beyond scratchpad-only checks.
- **AC-4**: Phase handoffs stay within bounded context packs; **no** removal of mandatory isolation, strict-proof, role, or release evidence fields from governed surfaces.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-slimming hides policy | Deep links + runbook; AC-8 command-behavior tests |
| Metric gaming / wrong baselines | **`run_class_hash`** equality rule; **`TOKEN_COST_RUN_CLASS_MISMATCH`** |
| Template drift | Versioned parity manifest + checks |

## Tests strategy (**AC-8**)

Regression coverage for: command/rule behavior parity after slimming; **`tests/auto_command_contract_test.py`** (slim **`/auto`** contract markers); **`tests/token_cost_fixtures_test.py`** + **`tests/fixtures/token_cost/`** for **`run_class_hash`** + **`token_cost_compare.py`** CLI; **`python scripts/check_token_cost_parity.py --repo .`** (manifest-listed paths); **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** §26M.

## Decision linkage

- Research basis: **`R-0057`**
- Decision: **`DEC-0062`**

---

# BUG-0001: Intake gate script install completeness

## Overview

**`BUG-0001`** fixes **missing mandatory `/intake` gate scripts** in packaged installs: consumers receive **`template/`** from npm/Chocolatey/Homebrew paths, but **`template/scripts/`** omitted the three **`intake_*`** modules that exist in repo **`scripts/`**. **`DEC-0063`** is normative for ship path, **`package.json` `files`** policy, parity tests, and **`US-0018`** upgrade delivery. Research **`R-0058`** bounds minimal payload and installer **`SOURCE_ROOT`** behavior.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A — Publish via **`files`** only (repo **`scripts/`** root) | Skips **`template/scripts/`** | **Rejected** — PS1/SH installers copy **`template/`** only (**`R-0058`**). |
| B — Full **`scripts/`** mirror into **`template/scripts/`** | Maximum parity | **Rejected** — violates intake-only completeness scope. |
| C — Three-file **`template/scripts/`** mirror + parity checks | Minimal + testable | **Chosen** — **`DEC-0063`**. |

## Minimal architecture

1. **Authoritative consumer layout**: **`template/scripts/intake_evidence_validate.py`**, **`intake_evidence_lib.py`**, **`intake_bug_routing_guard.py`** — content-aligned with repo **`scripts/`** (**`DEC-0063`** §1).
2. **npm manifest**: **`template/`** subtree remains the primary ship vehicle; optional explicit **`scripts/intake_*.py`** **`files`** entries only as redundant documentation (**`DEC-0063`** §2).
3. **Verification**: **`scripts/check_intake_template_parity.py`** (intake trio + checker self-pair) and **`tests/intake_template_parity_fixtures_test.py`**, wired in **`tests/run-tests.*`** §26N; active/**`template/`** byte sync for those paths.
4. **Upgrade**: **`installer-owned-paths.manifest`** lists the intake modules (and parity checker) under **`scripts/`** so **`installer.ps1` / `installer.sh`** copy them on fresh install and **`--mode upgrade`** (default **`framework`** classification for `scripts/*.py` not under user-data prefixes).

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Copy drift | Parity gate; same PR for both trees when changing intake modules |
| Upgrade misses new files | Sprint AC covers **`--mode upgrade`** evidence |

## Tests strategy

- **S0060**: **`check_intake_template_parity.py`** + **`tests/intake_template_parity_fixtures_test.py`** (see **`sprints/S0060/summary.md`**).
- Installer / lifecycle tests as sprint defines (align **`US-0041`** / **`US-0008`** where overlap).

## Decision linkage

- Research basis: **`R-0058`**
- Decision: **`DEC-0063`**
- Related: **`DEC-0061`** (bug schema), **`US-0018`** (upgrade)

---

# US-0081: First-intake full-plan coverage and story-map gate

## Overview

**`US-0081`** adds a deterministic persistence gate for first/new/broad intake so major plan areas cannot be silently dropped. Intake must persist a normalized **`plan_area_inventory`** and complete coverage bindings (**`plan_area_id -> story_id[] | deferred_ref`**) before backlog write. **`R-0059`** supplies the pattern baseline; **`DEC-0064`** is normative for contract fields, fail codes, and verification policy.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Keep decomposition guidance only | Human-only quality check | Rejected - non-deterministic; misses AC-2/AC-7. |
| B - Auto-generate stories for all areas | Maximum automation | Rejected - overreaches; low signal in ambiguous intake. |
| C - Mandatory coverage map gate (chosen) | Deterministic + bounded + auditable | **Chosen** - simplest approach that still enforces complete-plan accounting. |

## Deterministic approach

1. **Scope trigger**: Apply gate when intake is first/new/broad (detected by existing intake policy path and explicit intake context).
2. **Normalize plan inventory**: Build canonical **`plan_area_inventory[]`** with stable **`plan_area_id`** ordering and deterministic text normalization.
3. **Require total mapping**: Every **`plan_area_id`** must resolve to either:
   - non-empty **`story_ids[]`**, or
   - explicit **`deferred_ref`** with bounded rationale.
4. **Fail closed before persistence**: Any uncovered major area blocks backlog mutation under **`INTAKE_PERSISTENCE_BLOCKED`** with specific subcode.
5. **Status authority preserved**: Story status remains canonical in **`docs/product/backlog.md`** per **`US-0045`**.

## Data contract additions

- Intake evidence payload gains:
  - **`plan_area_inventory`**: array of `{ plan_area_id, title, description, priority_hint? }`
  - **`plan_area_coverage`**: array of `{ plan_area_id, story_ids?, deferred_ref?, deferred_reason? }`
  - **`coverage_complete`**: boolean derived by validator (must be `true` to persist)
  - **`coverage_validation_ref`**: deterministic validator trace id/hash reference
- Contract invariants:
  - each **`plan_area_id`** appears exactly once in inventory and coverage
  - each coverage row has exactly one path: `story_ids` xor `deferred_ref`
  - `story_ids` values must exist in the candidate story set for this intake write

## Fail codes (deterministic)

- **`INTAKE_PERSISTENCE_BLOCKED`** (umbrella)
- **`INTAKE_PLAN_COVERAGE_MISSING`**: one or more major plan areas unmapped
- **`INTAKE_PLAN_AREA_ID_INVALID`**: malformed or duplicate `plan_area_id`
- **`INTAKE_PLAN_COVERAGE_CONTRACT_INVALID`**: contract shape/xor invariant violated
- **`INTAKE_PLAN_DEFERRED_REF_MISSING`**: defer selected without required reference

## Verification strategy

- **Unit fixtures**: pass/fail/defer matrices for canonical coverage cases (AC-10).
- **Contract validator tests**: deterministic ordering, id uniqueness, xor enforcement.
- **Policy-path tests**: low-touch and guided intake both enforce gate for first/new/broad scope (AC-5).
- **Parity checks**: active + `template/` alignment across intake command, PO guidance, and validator fixtures (AC-9).
- **Operator guidance checks**: `/ask` and runbook text include coverage-map requirement and fail-code remediation (AC-8).

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-classifying "major areas" causes false blocks | Keep bounded area taxonomy with deterministic normalization rules (DEC-0064). |
| Coverage map drift between prose and artifacts | Validator derives `coverage_complete`; persistence blocked on mismatch. |
| Policy/document drift between active and template | Explicit parity fixtures in AC-9 test scope. |

## Decision linkage

- Research basis: **`R-0059`**
- Decision: **`DEC-0064`**

---

