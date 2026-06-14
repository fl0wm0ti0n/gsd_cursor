# Architecture archive pack (2026-06-13)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 14
- First archived heading: `# US-0086: Automation-driven remote execution selection (Docker / SSH / NL container intent)`
- Last archived heading: `# US-0089: Cursor Caveman mode (scratchpad-configurable terse responses)`
- Verification tuple (mandatory):
  - archived_body_lines=354
  - preamble_lines=10
  - retained_body_lines=2793

---

# US-0086: Automation-driven remote execution selection (Docker / SSH / NL container intent)

## Overview

**`US-0086`** adds a deterministic, **automation-only** remote target-routing
contract that composes with **`US-0064`** and **`US-0085`**: when automation
profile is enabled, workflows may resolve Docker/SSH/local execution targets
from canonical config and explicit operator intent; when disabled, default
manual behavior remains local-first with zero new remote overhead.

Research basis: **`R-0068`** (routing precedence, reason-code candidates,
evidence tuple, and external references).

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | Always-on remote routing for all runs | Rejected - violates manual-first default and adds unwanted remote dependencies to daily local use. |
| B | Implicit heuristic-only routing (no explicit intent phrase) | Rejected - ambiguous behavior and harder operator debugging. |
| C | Automation-profile gate + explicit NL intent + deterministic fallback matrix (chosen) | Chosen - simplest model that satisfies AC-1..AC-10 while preserving fail-closed behavior. |

## Architecture-locked contracts

### 1) Automation profile gate

- **Mode off**: emit deterministic skip posture (`REMOTE_AUTOMATION_MODE_OFF`)
  and continue local/default execution path.
- **Mode on**: routing policy may select remote targets for execute/qa/release
  and related automation surfaces.
- Manual operator workflows remain unchanged unless profile is explicitly
  enabled.

### 2) Deterministic routing precedence

1. **Explicit NL intent**: `start container <target_id>` resolves first.
2. **Target validation**: `target_id` must map to canonical enabled
   `targets[].id`; unknown/disabled targets fail closed.
3. **Heuristic fallback** (automation mode only): apply documented file-class
   matrix (Docker-oriented changes -> container-capable target; SSH/runtime
   infra changes -> ssh-capable target; else local/default).
4. **No silent reroute when mode off**.

### 3) Reason-code vocabulary (locked)

| Code | When |
|------|------|
| `REMOTE_AUTOMATION_MODE_OFF` | Automation routing requested while profile is disabled. |
| `REMOTE_TARGET_UNKNOWN` | Explicit target id does not exist in canonical config. |
| `REMOTE_TARGET_DISABLED` | Target id exists but is disabled/unavailable by config. |
| `REMOTE_TARGET_UNROUTABLE` | Mode on, routing attempted, but no deterministic target can satisfy policy. |

### 4) Evidence tuple contract (handoffs/state)

When remote automation routing is used, phase evidence must include:

- `target_id`
- `environment_label`
- `automation_profile`
- `routing_source` (`explicit_intent|heuristic_fallback`)
- `secret_surface=names_only`

No secret values may appear in state/handoffs.

### 5) Security continuity with US-0085

- Automation may use already-exported environment variables.
- Automation must not read `.env` directly.
- Logs and handoffs remain names-only for secret references.

### 6) Compatibility boundaries

- **US-0064/DEC-0070** schema remains unchanged; this story adds routing policy,
  not new canonical remote schema.
- **US-0084** tooling stays valid; routing composes with existing
  `remote_config_summary` and runtime-connectivity docs.

## Delivery surfaces (execute phase)

| Path class | Scope |
|------------|-------|
| `.cursor/scratchpad*` (+ `template/`) | Automation-profile literals and defaults. |
| `.cursor/commands/*` + orchestration reference | Routing contract, reason codes, NL intent literals, mode-on/off behavior. |
| Agent rules (`.cursor/rules/*` + `template/`) | Deterministic routing guidance and no-reroute-on-off guardrails. |
| Runbook/docs (`docs/engineering/*` + `template/`) | Manual vs automation split and CI recipe notes. |
| Tests (`tests/*`) | Target resolution pass/fail fixtures and non-regression for mode-off behavior. |

## Risks

| Risk | Mitigation |
|------|------------|
| Ambiguous intent parsing for free-form NL | Keep v1 literal constrained to `start container <target_id>`; aliases require explicit architecture update. |
| Hidden remote reroute surprises | Enforce mode gate + explicit reason codes + runbook/manual-vs-automation split. |
| Secret leakage in evidence | Inherit US-0085 names-only contract; no `.env` reads and no value logging. |
| Target drift across active/template/docs | AC-10 parity checks on command/rule/scratchpad surfaces. |

## Decision linkage

- Research: **`R-0068`**
- Related: **`US-0064`**, **`US-0084`**, **`US-0085`**, **`DEC-0070`**, **`DEC-0071`**

---

# US-0089: Cursor Caveman mode (scratchpad-configurable terse responses)

## Overview

**`US-0089`** adds an optional **response-side** Caveman voice to Cursor
assistant output, toggled from **`.cursor/scratchpad.md`** and **default
off**. The feature lets operators trade reply prose for terse / imperative
delivery while leaving every machine-verifiable region of output literal.

Research basis: **`R-0073`** (research-phase extension dated 2026-04-18).
Governance decision: **`DEC-0072`**. **`US-0090`** covers **input-side** file
compression and is deferred; this story only reserves the shared scratchpad
vocabulary.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A | Orthogonal composition: `TOKEN_PROFILE` owns context breadth (US-0080 / DEC-0062); `CAVEMAN_*` owns voice. Rule-only composition, no new skill. Default off. | **Chosen** — minimal surface, zero regression risk for default-off operators, independent axes remain independent. |
| B | Explicit `TOKEN_PROFILE × CAVEMAN_MODE` precedence matrix baked into commands/rules. | Rejected — adds doc surface and invites misreadings; Option A's non-substitution paragraph already covers every cell. |
| C | Collapse voice into `TOKEN_PROFILE` (e.g. `lean-caveman`). | Rejected — breaks US-0080 semantics and couples two independent concerns. |
| D | Rule + focused skill (`.cursor/skills/its-magic-caveman/SKILL.md`). | Rejected for US-0089 — higher maintenance; no current discoverability evidence. Can be reconsidered in a future story. |
| E | Skill-only composition (no rule). | Rejected — literal-region invariants must live in rules; skills are contextual. |
| F | Single key `CAVEMAN=off|lite|full|ultra`. | Rejected — collides with repo `0|1` convention and couples enable flag to level. |

## Architecture-locked contracts

### 1) Scratchpad key contract

Locked names, defaults, and test strings:

| Key | Values | Default | Semantics |
|-----|--------|---------|-----------|
| `CAVEMAN_MODE` | `0` or `1` | `0` | `0` = pre-US-0089 behavior. `1` = voice rule active. Absence = `0`. |
| `CAVEMAN_LEVEL` | `lite`, `full`, `ultra`, or empty | empty | With `MODE=0`: inert. With `MODE=1` and empty: treat as `full`. Unknown value -> `CAVEMAN_LEVEL_UNKNOWN` and fall back to pre-US-0089 voice. |
| `CAVEMAN_COMPRESS_INPUT` | `0` or `1` | `0` | **Reserved for US-0090**. No-op in US-0089. |
| `CAVEMAN_FILE_SCOPE` | string (empty) | empty | **Reserved for US-0090**. No-op in US-0089. |

Exact contract lines (tests match byte-for-byte):

```
CAVEMAN_MODE=0
CAVEMAN_LEVEL=
CAVEMAN_COMPRESS_INPUT=0
CAVEMAN_FILE_SCOPE=
```

Same four lines (identical defaults) mirrored in
`.cursor/scratchpad.local.example.md` and
`template/.cursor/scratchpad.local.example.md`. Comment anchoring text:
`# reserved for US-0090; inert in US-0089; no behavior until compression story ships`.

### 2) Composition surface (Option A — rule-only)

- **New authoritative file**: `.cursor/rules/caveman.mdc` (active) +
  `template/.cursor/rules/caveman.mdc` (template mirror).
- Rule scope: `globs: ["**/*"]` (always-on, same posture as `core.mdc`).
- **No new skill** in US-0089. `.cursor/skills/its-magic/SKILL.md` is NOT
  modified.
- Rule body hosts: `CAVEMAN_MODE` gate, 9-zone literal-region invariant,
  operator phrase catalog, non-suppressible gate list (inherited from
  US-0088), and single-line attribution line
  `Inspired by JuliusBrussee/caveman (MIT). External reference only; not vendored.`
- No `npx skills add` reference anywhere in the kit.

### 3) TOKEN_PROFILE x CAVEMAN precedence (orthogonal, non-substitution)

| TOKEN_PROFILE \ CAVEMAN_MODE | 0 (off) | 1 (on) |
|------------------------------|---------|--------|
| `lean` | Pre-US-0089 behavior, lean pack. | Lean pack + Caveman voice; literals untouched. |
| `balanced` (default) | Pre-US-0089 behavior, balanced pack. | Balanced pack + Caveman voice. |
| `full` | Pre-US-0089 behavior, full pack. | Full pack + Caveman voice. |

Canonical non-substitution paragraph (published verbatim in
`docs/engineering/auto-orchestration-reference.md`,
`docs/engineering/runbook.md`, and template mirrors):

> `TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls reply
> voice. Neither substitutes for the other; setting one does not change the
> other. Combine freely.

### 4) Literal-region invariant (nine-zone list, hard MUST)

When `CAVEMAN_MODE=1`, these regions remain byte-literal (no abbreviation,
no rewording, no casing change):

1. Fenced code blocks (both plain and CODE REFERENCE `startLine:endLine:filepath` forms).
2. File/path strings in backticks (any repo path or filename with extension).
3. AC checklist items `- [ ]` / `- [x]` and their full text.
4. Reason codes (`ALL_CAPS_WITH_UNDERSCORES`) — e.g.
   `PHASE_CONTEXT_ISOLATION_VIOLATION`, `RUNTIME_PROOF_MISSING`,
   `AUTO_RESUME_ERROR`, `REMOTE_TARGET_UNKNOWN`, `CAVEMAN_LEVEL_UNKNOWN`,
   `INTAKE_PERSISTENCE_BLOCKED`.
5. IDs — `US-xxxx`, `DEC-xxxx`, `R-xxxx`, `BUG-####`, `S0xxx`, `T-xxx`.
6. Contract markers — `[BUG_VALIDATION_OK]`,
   `[INTAKE_EVIDENCE_VALIDATION_OK]`, `[SCRATCHPAD_PAIR_OK]`,
   `[ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS]`, `[CODEBASE_MAP_OK]`.
7. Strict-proof tuple fields (DEC-0038) — `orchestrator_run_id`,
   `runtime_proof_id`, `proof_hash`, `proof_issued_at`, `proof_ttl_seconds`,
   `phase_id`, `role`.
8. Isolation evidence fields (DEC-0029) — `fresh_context_marker`,
   `evidence_ref`, `timestamp`.
9. Commit / git refs when quoted — `git commit` messages, branch names,
   SHAs, `HEAD`, tag names.

### 5) Operator toggle phrase catalog

| Phrase | Effect |
|--------|--------|
| `caveman on` | Enable Caveman voice for the session (overlay). Effective next turn. |
| `caveman off` | Disable Caveman voice for the session (overlay). Effective next turn. |
| `stop caveman` | Alias for `caveman off`. |
| `normal mode` | Alias for `caveman off`. |
| `caveman: lite` / `caveman: full` / `caveman: ultra` | Set level (implies `caveman on`). Effective next turn. |

Determinism rules:

- Scratchpad `CAVEMAN_MODE` / `CAVEMAN_LEVEL` are authoritative across
  subagent spawns. Session toggles are overlays only; they do NOT persist
  across a fresh subagent context.
- Within a session, the last explicit toggle wins.
- Mid-turn toggle applies from the next turn onward. Current-turn
  machine-verifiable artifacts (gate messages, reason codes, tuples) remain
  literal regardless of the toggle.
- Ambiguous phrases (`be caveman-lite`, `quiet caveman`, `cave man off`,
  etc.) are not recognized — only the exact literals above.

### 6) Default-off invariant (test contract)

`tests/auto_command_contract_test.py` is extended **in place** (no new test
module) with the `test_caveman_default_off_*` subtests enumerated in
**DEC-0072 §6** (8 subtests). Highlights:

- Scratchpad key lines present in active + example + template example files
  (byte-literal).
- `.cursor/rules/caveman.mdc` present active + `template/`; contains the
  tokens `CAVEMAN_MODE`, `literal`, and all five canonical toggle phrases.
- Non-substitution paragraph present in `auto-orchestration-reference.md`
  and `runbook.md` (active + template).
- Existing `required` token list (spawn-only / BUG-0006 / reason codes /
  `AUTO_QUIET` / `# US-0086`) remains **unchanged** — patch may only add.
- Non-suppressible gate vocabulary (`decision_gate`, `missing input`,
  `pause`, `loop_max`, `blocked`, `[BUG_VALIDATION_OK]`,
  `[INTAKE_EVIDENCE_VALIDATION_OK]`) preserved in `auto.md` and reference.
- No `npx skills add` token in runbook or rule.

Byte-for-byte baseline invariant: with `CAVEMAN_MODE` unset or `=0`, all
other `.cursor/commands/*.md`, `.cursor/rules/*` files (excluding the new
`caveman.mdc`), and handoff template stubs remain byte-identical to
pre-US-0089 content.

**Voice rules** (delivered in **`BUG-0011`** / **`DEC-0077`**): actionable
voice-compression directives append to `.cursor/rules/caveman.mdc` under
`## Voice compression (when CAVEMAN_MODE=1)`. **Not CI-tested**: qualitative
brevity under `CAVEMAN_MODE=1` remains operator-verified (token-presence
contract tests only; see **`# BUG-0011`**).

### 7) Template parity inventory (delivery checklist)

`/sprint-plan` atomizes one task per row; all rows marked "active" +
"template" produce two-surface edits.

| # | Active path | Template path | Action |
|---|-------------|---------------|--------|
| 1 | `.cursor/scratchpad.md` | n/a (example-only install per US-0073 / DEC-0055) | Add 4 key lines + `## Caveman mode (US-0089)` comment block. |
| 2 | `.cursor/scratchpad.local.example.md` | `template/.cursor/scratchpad.local.example.md` | Add identical 4 key lines + comment block. |
| 3 | `.cursor/rules/caveman.mdc` (**new**) | `template/.cursor/rules/caveman.mdc` (**new**) | Create rule per §2 / §4 / §5. |
| 4 | `docs/engineering/auto-orchestration-reference.md` | `template/docs/engineering/auto-orchestration-reference.md` | Insert non-substitution paragraph near TOKEN_PROFILE / AUTO_QUIET discussion. |
| 5 | `docs/engineering/runbook.md` | `template/docs/engineering/runbook.md` | Add `### Caveman mode (US-0089)` subsection with key table, phrase catalog, non-substitution paragraph. |
| 6 | `docs/engineering/architecture.md` `# US-0089` | active-only | This section (already written). |
| 7 | `tests/auto_command_contract_test.py` | active-only | Extend in place per §6. |
| 8 | `.cursor/skills/its-magic/SKILL.md` | `template/.cursor/skills/its-magic/SKILL.md` | **No change** (negative parity assertion). |

Files explicitly **not** touched by US-0089: `docs/engineering/decisions.md`
body (index/context-pack additions only are part of this DEC),
`docs/product/backlog.md` outside the `## US-0089` `architecture_notes`
append, `handoffs/intake_evidence/*.json`, `docs/engineering/state.md`
schema, `scripts/*`, `installer*`, `package.json`, `.env` / `.env.example`.

## Boundaries vs related stories

- **vs US-0090** (input-side compression — deferred). US-0089 reserves
  `CAVEMAN_COMPRESS_INPUT` and `CAVEMAN_FILE_SCOPE` as documented no-ops.
  US-0089 **must not** include any script, installer change, or file
  mutator. US-0090 will extend `R-0073` in its own discovery/research.
- **vs US-0080 / DEC-0062** (TOKEN_PROFILE / token-cost hardening). Fully
  orthogonal per §3. Caveman does not change context packs, parity
  manifests, run-class metrics, or `handoffs/token_cost_runs/` records.
- **vs US-0053 / DEC-0035** (tiered profile). Untouched. No new profile
  value. `TOKEN_PROFILE` remains `lean|balanced|full`.
- **vs US-0088** (`AUTO_QUIET` + continuous `/auto` loop). The Caveman rule
  MUST preserve the `AUTO_QUIET` non-suppressible gate vocabulary verbatim.
  Caveman voice never drops or compresses a gate message.
- **vs US-0071** (user-visible internal metadata sanitization). Caveman
  terseness MUST NOT cause the agent to drop visible `US-xxxx`, `DEC-xxxx`,
  `R-xxxx`, or `BUG-####` references (§4, zone 5).
- **vs US-0078 / DEC-0060** (intake evidence). `handoffs/intake_evidence/*.json`
  are never rewritten by anything US-0089 ships.
- **vs US-0048 / DEC-0029** (isolation), **US-0056 / DEC-0038** (strict
  proof), **BUG-0006** (spawn-only). All three contracts unchanged.
  Caveman voice does not alter tuple wording (§4, zones 7-8).

## Non-goals

- No input-side file compression.
- No new npm / Python dependencies.
- No change to spawn-only orchestration or strict-proof schema.
- No change to `TOKEN_PROFILE` semantics.
- No rewrite of canonical `backlog.md`, `acceptance.md`, `state.md`,
  `decisions.md` body, or DEC files.
- No vendor plugin install (`npx skills add`) surfaced in runbook or rule.
- No unit test of voice quality under `CAVEMAN_MODE=1`.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Caveman voice drops a reason code or path string. | 9-zone MUST list in rule (§4); contract-test assertion of gate vocabulary preservation. |
| Operator reads `CAVEMAN_MODE=1` as "lean equivalent". | Verbatim non-substitution paragraph in reference + runbook (§3); test asserts presence in both surfaces. |
| Scratchpad key rename churn breaks tests. | DEC-0072 §3 locks exact byte strings BEFORE dev phase authors tests. |
| Session toggle leaks state across subagent spawn. | Rule specifies scratchpad is authoritative across spawns; overlay applies only to current conversation (§5). |
| Mid-turn toggle masks a gate message. | Rule forbids overlay affecting current-turn gate artifacts (§5); contract test guards gate token preservation. |
| Template drift (rule added active-side only). | Parity inventory §7 lists both surfaces; contract-test subtests #2 and #3 assert template mirror presence. |
| Vendor `npx skills add` leaks into runbook. | Contract-test subtest #8 asserts token absence. |
| US-0090 gets implemented inadvertently under US-0089. | Reserved keys documented as no-ops; DEC-0072 §8 forbids scripts, installer changes, mutators. |
| `CAVEMAN_LEVEL` typo produces undefined behavior. | Rule specifies deterministic fallback via `CAVEMAN_LEVEL_UNKNOWN` + pre-US-0089 voice. |

## Delivery surfaces (execute phase summary)

| Path class | Scope |
|------------|-------|
| `.cursor/scratchpad.md` (active) | Caveman keys + comment block (US-0073 / DEC-0055 example-only install policy means template ships only the `.example.md` mirror). |
| `.cursor/scratchpad.local.example.md` (active + `template/`) | Caveman keys + comment block, literal byte-parity. |
| `.cursor/rules/caveman.mdc` (active + `template/`) | New always-on rule hosting gate, literal invariant, phrases, attribution. |
| `docs/engineering/auto-orchestration-reference.md` (active + `template/`) | Single non-substitution paragraph. |
| `docs/engineering/runbook.md` (active + `template/`) | Caveman subsection (key table, phrases, non-substitution, attribution). |
| `docs/engineering/architecture.md` `# US-0089` | This section (active-only). |
| `tests/auto_command_contract_test.py` | Extend with 8 `test_caveman_default_off_*` subtests. |

## Decision linkage

- Research basis: **`R-0073`**
- Decision: **`DEC-0072`**
- Related: **`US-0090`** (deferred), **`US-0080`** / **`DEC-0062`**,
  **`US-0053`** / **`DEC-0035`**, **`US-0088`**, **`US-0071`**,
  **`US-0048`** / **`DEC-0029`**, **`US-0056`** / **`DEC-0038`**,
  **`US-0069`** / **`DEC-0051`**, **`BUG-0006`**, **`US-0017`**,
  **`DEC-0040`**, **`DEC-0055`**, **`US-0078`** / **`DEC-0060`**,
  **`US-0045`**.
- External reference (not vendored): JuliusBrussee/caveman (MIT) —
  `https://github.com/JuliusBrussee/caveman`.

