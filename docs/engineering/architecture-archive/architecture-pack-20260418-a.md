# Architecture archive pack (2026-04-18)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 4
- Retained units in hot file: 30
- First archived heading: `# US-0052: Optional Fresh-Project ID Namespace Bootstrap`
- Last archived heading: `# US-0055: Deterministic Status Reconciliation Command`
- Verification tuple (mandatory):
  - archived_body_lines=305
  - preamble_lines=10
  - retained_body_lines=3462

---

# US-0052: Optional Fresh-Project ID Namespace Bootstrap

## Context and scope

US-0052 adds an optional bootstrap path for fresh repos so first IDs can start
at `US-0001` / `DEC-0001` / `R-0001`, while preserving current highest-existing-ID
continuation for non-fresh repositories. Out of scope: retroactive renumbering
or migration of existing histories.

## Assumption challenge and alternatives

### Option A: Always continue from highest discovered ID

- **Pros**: Simpler and backward compatible.
- **Cons**: Cannot satisfy fresh-project expectation in repos that want explicit
  namespace bootstrap semantics. Rejected as sole mode.

### Option B: Optional bootstrap mode with deterministic freshness checks (chosen)

- **Pros**: Supports fresh-project UX while maintaining compatibility in existing
  repos; no historical rewrites.
- **Cons**: Requires robust eligibility detection and collision safeguards.

## Minimal architecture

### 1) Bootstrap control

- Add explicit bootstrap control (flag or scratchpad/command argument), default off.
- Bootstrap applies only during eligible first-run/new-project initialization.

### 2) Freshness detection

- Determine eligibility from absence of existing `US-`, `DEC-`, and `R-` IDs in
  canonical artifacts.
- Emit deterministic diagnostics when bootstrap requested but repo is not fresh.

### 3) ID generation contract

- If bootstrap eligible and enabled: start at `0001`.
- Otherwise: continue from highest existing ID (current behavior).
- Never rewrite historical IDs.

### 4) Test coverage

- Add regression cases for:
  - fresh + bootstrap enabled
  - fresh + bootstrap disabled
  - non-fresh + bootstrap requested
  - mixed/partial artifact edge cases

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| ID collision in partially initialized repos | Multi-artifact freshness check and fail-fast diagnostics. |
| Operator confusion about bootstrap behavior | Clear README/runbook/help contract with examples and constraints. |
| Hidden behavior changes in existing repos | Default-off bootstrap and strict compatibility with highest-ID continuation. |

## Decision linkage

- Research basis: `R-0024`, `R-0025`
- Decision: `DEC-0034`

---

# US-0053: Context Compaction and Tiered Token-Cost Optimization Mode

## Overview

US-0053 introduces a deterministic token-efficiency control surface that reduces
recurring context volume while preserving workflow safety guarantees. The design
adds a tiered policy profile (`lean|balanced|full`), compact active-context
contracts for high-traffic artifacts, and a narrow-read retrieval strategy for
`/ask`.

## Challenge and alternatives

### Alternatives considered

1. **Manual per-flag tuning only** (no profile):
   flexible but error-prone; high operator overhead and inconsistent behavior.
2. **Single global token-saver on/off switch**:
   too coarse; insufficient control for teams needing intermediate depth.
3. **Tiered profile with documented override precedence** (selected):
   balances operator simplicity with deterministic, testable behavior.

### Simpler-path check

The selected architecture keeps existing features and safety gates, changing only
default intensity and retrieval scope. It avoids new runtime services or external
state stores and reuses existing artifact-first contracts.

## Minimal architecture

### 1) Token profile policy layer

- Add `TOKEN_PROFILE=lean|balanced|full` in scratchpad (default `balanced`).
- Define deterministic profile mapping to existing switches (automation looping,
  early research, intake depth, and optional overhead modes).
- Document explicit precedence:
  - mandatory gate invariants cannot be disabled by profile,
  - explicit manual flag overrides (when present) take precedence over profile
    defaults for documented keys.

### 2) Compact active-context contract

- Keep `docs/engineering/state.md` as canonical active evidence store but define
  a bounded **active context pack** section for routine reads.
- Archive older checkpoint blocks into versioned archive packs under a dedicated
  state-archive path; keep canonical references in active state.
- Compaction is append-safe and non-destructive: no historical deletion, only
  bounded active window + archive pointers.

### 3) Decisions index compaction

- Keep `docs/engineering/decisions.md` as compact current index:
  - current context pack,
  - bounded decision summary list,
  - canonical pointers to full `decisions/DEC-xxxx.md`.
- Prevent uncontrolled growth by moving long historical narrative detail to DEC
  records only.

### 4) `/ask` narrow-read retrieval strategy

- Update `/ask` policy to question-scoped retrieval:
  1. targeted section reads first (latest relevant checkpoints/story blocks),
  2. bounded expansion only when unresolved,
  3. explicit "not found in artifacts" response when evidence is absent.
- Preserve strict read-only behavior and zero artifact mutation contract.

### 5) Guardrail invariants

- Mandatory workflow gates remain unchanged:
  - `/qa` completion requirements,
  - `/verify-work` UAT completeness,
  - `/release` deterministic gate chain and isolation checks.
- Token savings are achieved via retrieval scope and default overhead intensity,
  not by removing safeguards.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Profile ambiguity causes inconsistent behavior | Publish deterministic profile mapping + precedence contract and regression tests. |
| Over-compaction hides needed evidence | Keep archive links canonical and require escalation path from active to archive reads. |
| Lean mode under-questions complex work | Document escalation guidance (`lean` -> `balanced`/`full`) and preserve manual override path. |
| Safety regression under token optimization | Lock mandatory gate invariants in tests and runbook contracts. |

## Decision linkage

- Research basis: `R-0027`, `R-0028`
- Decision: `DEC-0035`

---

# US-0054: Configurable Multi-Target Release Publish with Confirmation Gate

## Overview

US-0054 adds an optional post-release publish orchestration contract so each
repository can configure its own publish destinations (for example npm, choco,
brew, git, docker, cloud, custom servers) while enforcing a default confirmation
boundary before publish execution.

## Architecture goals

- Keep `/release` gate chain semantics unchanged and mandatory.
- Add publish-target behavior as a configuration-driven post-release layer.
- Support built-in target types and generic custom/SSH targets without hardcoded
  provider coupling.
- Fail fast on invalid target definitions with deterministic diagnostics.
- Preserve active/template parity and secret-safety contracts.

## Minimal architecture

1. **Target contract surface**
   - Canonical configurable target file under engineering docs (example schema).
   - Each target entry includes stable `id`, `type`, `enabled`, `order`,
     execution command/template, and optional environment/credential references.

2. **Execution mode control**
   - Scratchpad-controlled publish mode:
     - `disabled` (no publish step),
     - `confirm` (default; operator approval required),
     - `auto` (explicit opt-in).
   - Optional default target selection list, overridable per run.

3. **Target taxonomy**
   - Built-in `type` guidance for common destinations: `npm`, `choco`, `brew`,
     `git`, `docker`, `cloud`.
   - Generic `custom` target for arbitrary command workflows.
   - First-class `ssh` target with host/user/port/auth-reference/remote command.

4. **Safety and validation boundary**
   - Deterministic pre-execution validation for required fields and type
     constraints.
   - Env-reference-only sensitive values (`*Env` style) for tokens/passwords/keys.
   - Invalid or incomplete config blocks publish execution with explicit reason
     codes and no partial target side effects.

5. **Deterministic run semantics**
   - Explicit target selection (single/multi-target) per publish run.
   - Deterministic order by configured `order` then stable ID tie-break.
   - Disabled targets are skipped with explicit audit entries.

## Guardrail invariants

- Mandatory release quality gates remain unchanged:
  check-in tests -> QA -> UAT -> isolation -> release finalization.
- Publish target execution is additional post-release behavior and cannot bypass
  release evidence requirements.
- Existing story/decision/research ID semantics remain unchanged.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Ambiguous target config creates non-deterministic runs | strict schema and deterministic ordering rules |
| Missing confirmation triggers unintended publish | default `confirm` mode, explicit operator approval gate |
| Secret leakage in repo config | env-reference-only sensitive fields and fail-fast validation |
| Provider lock-in | built-in target guidance plus generic `custom` and `ssh` types |

## Decision linkage

- Research basis: `R-0029`, `R-0030`
- Decision: `DEC-0036`
- Boundaries: add configurable publish target layer only; do not alter mandatory
  `/release` gate chain contract.

---

# US-0055: Deterministic Status Reconciliation Command

## Overview

US-0055 adds a dedicated reconciliation command to normalize status drift across
canonical and derived workflow artifacts so continuation (`/auto`) can safely
resume from the correct next OPEN story and phase.

## Architecture goals

- Preserve canonical status ownership (`docs/product/backlog.md`).
- Reconcile derived artifacts deterministically (`acceptance`, `state`, `resume`).
- Keep mutation scope bounded to mismatched stories and linked derived entries.
- Emit auditable normalization evidence and deterministic reason codes.
- Preserve release-gate safety invariants and non-destructive history behavior.

## Minimal architecture

1. **New reconciliation command contract**
   - Add command (for example `/status-reconcile`) with deterministic detection,
     repair, and fail-closed blocked/conflict behavior.
   - Distinguish from `/memory-audit`:
     - `/memory-audit` remains read-only detection,
     - `/status-reconcile` performs bounded reconciliation writes.

2. **Canonical precedence model**
   - Authoritative source: backlog story `Status` (`OPEN|DONE`).
   - Derived surfaces:
     - `docs/product/acceptance.md` check rows,
     - backlog AC checkboxes for DONE stories,
     - `handoffs/resume_brief.md` next story + intended phase,
     - state reconciliation checkpoint.
   - If canonical status conflicts with release evidence, fail closed with reason
     code and remediation (no silent correction).

3. **Deterministic mutation boundaries**
   - Update only stories detected as mismatched.
   - Do not rewrite unrelated story blocks, sprint history, or narrative content.
   - Normalize DONE stories with unchecked ACs and acceptance drift in target scope.

4. **Auditability contract**
   - Write normalization evidence rows to canonical report artifact
     (`docs/engineering/status-normalization-report.md`):
     story ID, prior values, resolved values, evidence refs, timestamp.
   - Append reconciliation checkpoint in `docs/engineering/state.md`.

5. **Continuation readiness contract**
   - Recompute next OPEN story by canonical backlog priority/order.
   - Update `handoffs/resume_brief.md` deterministically:
     next actions, intended resume phase, latest breadcrumb metadata.

## Guardrail invariants

- Mandatory `/qa` -> `/verify-work` -> `/release` gate semantics remain unchanged.
- Reconciliation must not bypass release evidence requirements.
- No destructive rewrite of unrelated historical artifacts.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-broad repair mutates unrelated history | strict target-scoped mutation rules |
| Ambiguous conflict handling yields inconsistent outcomes | deterministic precedence + fail-safe reason codes |
| Hidden drift after repair | mandatory normalization report rows + state checkpoint evidence |

## Decision linkage

- Research basis: `R-0031`
- Decision: `DEC-0037`
- Boundaries: add reconciliation command and evidence contract only; do not
  change feature/runtime behavior beyond workflow status normalization.

---

