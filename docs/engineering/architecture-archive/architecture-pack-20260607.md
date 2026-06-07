# Architecture archive pack (2026-06-07)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 32
- First archived heading: `# US-0071: User-Visible Internal Metadata Sanitization Guard`
- Last archived heading: `# US-0072: Deterministic Context Slimming and Archive Enforcement (Triad)`
- Verification tuple (mandatory):
  - archived_body_lines=128
  - preamble_lines=10
  - retained_body_lines=3467

---

# US-0071: User-Visible Internal Metadata Sanitization Guard

## Overview

`US-0071` introduces a **channel-aware** policy: internal planning identifiers
are required for traceability in docs and comments, but must never appear in
**user-visible software outputs** (CLI/UI/errors/installer-visible text). The
architecture is a small, auditable control plane: **forbidden patterns** in
disallowed channels, **explicit allowlist** for internal surfaces, and **mandatory
execute → QA → release** evidence with shared reason codes.

## Policy model

### 1. Forbidden baseline (disallowed channels only)

Apply deterministic planning-shaped matchers in user-visible targets:

- `US-[0-9]{4}`
- `DEC-[0-9]{4}`
- `R-[0-9]{4}`

Matching should prefer planning-shaped tokens to limit accidental hits on
unrelated strings (`R-0046`).

### 2. Allowlisted internal surfaces

Permitted without guard failure:

- `docs/**`
- `.cursor/**`
- `sprints/**`, `handoffs/**`, `decisions/**` (and analogous template trees)
- **Source comments only** — not string literals that ship to users

### 3. Enforcement chain

| Boundary | Responsibility |
|----------|------------------|
| `/execute` | Default, non-bypass guard so in-scope changes do not introduce forbidden tokens into user-visible outputs. |
| `/qa` | Automated scan; fail closed with path evidence, token class, remediation; idempotent reruns. |
| `/release` / readiness | Attest checks **executed and passed** (AC-10), not policy-only. |

### 4. Reason codes (minimum vocabulary)

Use consistently across phases (`DEC-0053`):

- `USER_VISIBLE_INTERNAL_METADATA_DETECTED`
- `METADATA_SANITIZATION_POLICY_MISSING`
- `METADATA_SANITIZATION_SCOPE_AMBIGUOUS`

### 5. Parity and tests

- Active vs `template/` parity on commands, rules, runbook, README (AC-8).
- Regression: positive, negative, allowlist, rerun idempotence (AC-9).

## Decision linkage

- Research basis: `R-0046`
- Decision: `DEC-0053`

---

# US-0072: Deterministic Context Slimming and Archive Enforcement (Triad)

## Overview

`US-0072` makes **hot-surface compaction** and **bounded phase reads** a
first-class workflow contract for three canonical artifacts:
`docs/engineering/state.md`, `handoffs/po_to_tl.md`, and
`docs/engineering/architecture.md`. The design extends `DEC-0042` state rollover
with **parallel scratchpad thresholds**, **deterministic archive packs**,
**same-boundary enforcement**, and **verification tuples** so growth cannot pass
silently.

## Triad surfaces and caps

Thresholds are read from **merged scratchpad** (active + local) with defaults
documented in `DEC-0054`:

- **State** — `STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS` (existing).
- **PO→TL handoff** — `PO_TO_TL_HOT_MAX_LINES`, `PO_TO_TL_HOT_MAX_SECTIONS`.
- **Architecture** — `ARCH_HOT_MAX_LINES`, `ARCH_HOT_MAX_STORY_SECTIONS`.

## Archive layout

- `docs/engineering/state-archive/state-pack-*.md`
- `handoffs/archive/po-to-tl-pack-*.md`
- `docs/engineering/architecture-archive/architecture-pack-*.md`

Packs are append-only historical stores; hot files retain the newest material
per deterministic slice rules.

## Phase ownership gates

| Artifact | Typical mutator | Pre-completion gate |
|----------|-----------------|---------------------|
| `state.md` | Curator `/refresh-context` | Rollover or fail-closed when over cap. |
| `po_to_tl.md` | PO `/intake`, `/discovery`, handoff append paths | Rollover or fail-closed when over cap. |
| `architecture.md` | Tech-lead `/architecture` | Rollover or fail-closed when over cap; never delete unrelated `US-xxxx` sections (`DEC-0043`). |

Any phase that mutates a triad file inherits the gate for that run.

## Verification and idempotence

Successful rollover emits `boundary`, `moved`, `retained`, `pack_ref` in phase
evidence (for example `state.md` checkpoint body or sibling runbook table).
Reruns are idempotent: satisfied caps → no duplicate packs.

## Minimal-read model

Phase commands document **required files first**, numeric read budgets, and
**escalation only** to a named `pack_ref` when unresolved—aligned with
`DEC-0035` narrow-read retrieval. Optional compact pointer files or hot-header
blocks implement `AC-6` without duplicating full checkpoints.

## Reason codes

Minimum shared vocabulary (`DEC-0054`): `STATE_ARCHIVE_REQUIRED`,
`STATE_ARCHIVE_VERIFICATION_FAILED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`,
`CONTEXT_BUDGET_EXCEEDED`, plus `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` and
`STATE_ARCHIVE_WRITE_FAILED` where applicable.

## Decision linkage

- Research basis: `R-0047`
- Decision: `DEC-0054`

---

