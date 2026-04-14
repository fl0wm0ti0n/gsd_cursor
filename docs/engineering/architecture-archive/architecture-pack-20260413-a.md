# Architecture archive pack (2026-04-13)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 34
- First archived heading: `# US-0048: Enforced Per-Phase Subagent Isolation with Audit Gate`
- Last archived heading: `# US-0048: Enforced Per-Phase Subagent Isolation with Audit Gate`
- Verification tuple (mandatory):
  - archived_body_lines=166
  - preamble_lines=10
  - retained_body_lines=3378

---

# US-0048: Enforced Per-Phase Subagent Isolation with Audit Gate

## Overview

US-0048 makes per-phase subagent isolation a hard-enforced workflow contract with
auditable evidence and fail-closed gates. Policy text already mandates isolation
(DEC-0007, US-0023); this story adds mandatory evidence writing, deterministic
reason codes, and blocking behavior at progression and release when evidence is
missing or violated.

Scope: workflow contract enforcement, evidence schema, gates, reason codes,
regression coverage. Out of scope: runtime product feature changes, external
orchestration platform migration.

## Assumption challenge and alternatives

### Option A: Advisory-only (logging deviation, no gates)

- **Pros**: Low effort; no blocking.
- **Cons**: Does not close recurrence risk; user reported breach was execution
  in one context instead of fresh subagent per phase. Rejected as insufficient.

### Option B: Hard enforcement + auditable evidence + fail-closed gates (chosen)

- **Pros**: Closes compliance gap; deterministic detection and blocking;
  operator gets explicit diagnostics (reason code, phase, evidence ref,
  remediation). Aligns with PO recommendation and vision discovery notes.
- **Cons**: Higher effort; evidence write discipline required; possible friction
  if evidence writes are inconsistent. Mitigated by clear schema, remediation
  guidance, and bounded migration for legacy artifacts.

## Minimal architecture

### 1) Components and data flow for isolation evidence

- **Orchestrator** (`/auto`): Must not execute phase work in-process; must
  spawn/trigger fresh subagent context per phase and per execute↔QA cycle.
  Reads handoffs and state; writes phase-boundary breadcrumbs and delegates
  phase execution to a new context.
- **Phase executors** (each phase command run in its role): On phase start/completion,
  write **isolation evidence** to canonical locations (see below). Evidence is
  the only cross-phase proof of fresh-context execution.
- **Gate evaluators** (`/verify-work`, `/release`): Before allowing progression
  or release finalization, read canonical isolation evidence for the current
  sprint/phase span; if required evidence is missing or invalid, block with
  deterministic reason code and remediation.
- **Canonical evidence store**: Single authoritative place where isolation
  evidence is written and read for gates. Recommended: a dedicated section in
  `docs/engineering/state.md` and/or phase-scoped footers in handoffs, plus
  optional append-only `docs/engineering/isolation-evidence.log` or equivalent
  for machine-checkable audit. Schema below.

Data flow:

1. Phase N starts in a **new** subagent context → executor writes isolation
   evidence (phase_id, role, fresh_context_marker, timestamp, evidence_ref).
2. Phase N completes → handoff written; evidence may be appended/updated for
   phase N completion.
3. Before phase N+1 or before verify-work/release, gate evaluator reads
   evidence for completed phases in scope; if any required row is missing or
   invalid → fail closed, emit reason code and remediation.
4. Pause/resume: resume checkpoint carries isolation provenance (last phase
   with valid evidence, evidence_ref) so continuation does not silently reuse
   context.

### 2) Isolation evidence schema (minimal)

Required fields (per phase boundary):

- `phase_id`: canonical phase identifier (e.g. intake, discovery, architecture,
  sprint-plan, execute, qa, verify-work, release, refresh-context).
- `role`: agent role that executed the phase (po, tech-lead, dev, qa, release,
  curator).
- `fresh_context_marker`: value attesting new context (e.g. session id or
  explicit "fresh" token; format defined in runbook).
- `timestamp`: ISO 8601.
- `evidence_ref`: pointer to this evidence record (e.g. state.md section id or
  log line id).

Optional for resume provenance:

- `session_id`, `parent_phase` (for chained continuation).

Canonical locations:

- Primary: `docs/engineering/state.md` — dedicated "Isolation evidence" section
  with one block per phase transition (sprint/phase scoped).
- Alternative/append: handoff footers or `docs/engineering/isolation-evidence.log`
  (append-only) for gate scripts to parse. Runbook documents where gates read
  from.

### 3) Reason-code taxonomy (isolation violations)

Deterministic codes for gate output and remediation:

| Code | Meaning | Remediation |
|------|---------|-------------|
| `PHASE_CONTEXT_ISOLATION_MISSING` | Required isolation evidence for one or more phases is absent | Run the missing phase(s) in a fresh subagent context and ensure evidence is written; re-run gate. |
| `PHASE_CONTEXT_ISOLATION_VIOLATION` | Evidence indicates reused context (e.g. same session across phases) or invalid role/phase mapping | Re-run affected phase(s) in a fresh context; correct role/phase mapping in commands. |
| `ISOLATION_EVIDENCE_STALE` | Evidence timestamp or scope does not match current sprint/phase span | Re-run phase(s) or refresh evidence; ensure state/handoffs are current. |
| `ISOLATION_EVIDENCE_INVALID` | Schema violation (missing required field, malformed) | Fix evidence schema in artifact or in writer (command/agent); re-run phase. |

Remediation guidance must be explicit in gate output (reason code, phase id,
evidence ref, suggested next action).

### 4) Verify-work and release gate placement and precedence

- **Verify-work**: Before marking verify-work as PASS, run an **isolation-compliance
  gate**: for the current sprint, all phases that should have been executed
  (from sprint start through execute and QA) must have valid isolation evidence.
  If not, verify-work outcome is BLOCKED; output includes reason code and
  remediation. Order: other verify-work checks (e.g. UAT) may run first or in
  parallel; isolation gate must pass before verify-work is considered complete.
- **Release**: Before release finalization, run the same **isolation-compliance
  gate** for the sprint being released. If isolation evidence is missing or
  invalid, release is blocked; release command output includes reason code,
  phase(s) affected, evidence ref, remediation. Gate order: check-in test →
  QA → UAT → **isolation compliance** → release notes/queue update. Isolation
  gate does not replace other gates; it is an additional mandatory gate.

Precedence: Isolation gate is mandatory and fail-closed. No bypass in default
configuration; any override requires explicit decision gate and documented
rationale (same pattern as US-0039 release overrides).

### 5) Pause/resume provenance behavior

- On **pause**: Persist current phase, last completed phase, and evidence_ref
  (or equivalent) for the last phase with valid isolation evidence in
  `handoffs/resume_brief.md` and/or `docs/engineering/state.md`.
- On **resume**: Resolver uses resume checkpoint; continuation must not assume
  the same context is still valid. Next phase must run in a **new** subagent
  context and write new isolation evidence. Breadcrumbs must record
  `resolved_start_phase`, `isolation_evidence_ref_at_resume`, and
  `continuation_fresh_context_required=true` so that gate evaluators can require
  evidence for the resumed phase and subsequent phases.
- Isolation evidence must **survive** pause/resume: evidence written before
  pause remains valid for gate checks after resume; no ambiguity that "resumed"
  implies reuse of pre-pause context for new work.

### 6) Active/template parity requirements

- Command contracts (`/auto`, `/execute`, `/qa`, `/verify-work`, `/release`)
  that define isolation semantics, evidence-writing steps, and gate behavior
  must be updated in both active repo and `template/` so that new installs
  get the same enforcement.
- Runbook and README must document: isolation evidence schema, canonical
  locations, reason-code list, and remediation guidance. Parity required for
  active and template copies.
- Regression coverage (positive: valid evidence allows progression; negative:
  missing evidence, reused context, invalid role/phase) must be reflected in
  test/QA guidance in both active and template where applicable.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-strict validation blocks runs when evidence writes are incomplete | Clear schema and runbook steps; remediation guidance; optional bounded migration or legacy handling for repos without prior evidence. |
| Backward compatibility: existing artifacts lack new evidence fields | Gates apply to "required evidence for phases in scope"; legacy runs can define grace period or one-time migration that backfills or waives for pre-US-0048 sprints (documented). |
| Operator friction on first failure | Deterministic reason codes and explicit remediation (phase, evidence ref, next action) so operators can fix without guesswork. |
| Resume ambiguity | Provenance in resume checkpoint (evidence ref at resume, continuation requires fresh context) and documentation that resumed phase writes new evidence. |

## Decision linkage

- Research basis: `R-0018`, `R-0019`
- Decision: `DEC-0029`

