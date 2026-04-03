# Architecture

## Overview

US-0018 adds a fourth installer mode (`--mode upgrade`) that safely updates its-magic framework files in a target repo while preserving user data files. The design introduces three new concepts: file classification, version tracking, and an upgrade flow algorithm.

The existing installer architecture (Node.js CLI wrapper → OS-specific installer script → file copy loop) remains unchanged. Upgrade mode is an additional branch in the existing mode switch, using the same file listing and copy infrastructure.

---

# US-0039: Release Gate Tightening for Check-In Tests and QA/UAT Completion

## Overview

US-0039 tightens `/release` readiness with deterministic mandatory gates and
explicit evidence requirements. The objective is to block release when check-in
tests, QA completion, or UAT completeness are missing/stale/failing. Evidence
flow is read-from-canonical-artifacts only; no inferred pass from absence of
evidence (per R-0020).

## Assumption challenge and alternatives

### Option A: Keep UAT-only gate in release

Pros:
- Minimal documentation changes.

Cons:
- Missing hard checks for check-in test status and QA completion.
- Permits inconsistent release readiness evidence.

### Option B: Single combined "quality gate"

Pros:
- Shorter release step text.

Cons:
- Non-deterministic ordering and weak auditability.
- Harder to diagnose exactly which prerequisite failed.

### Option C: Deterministic ordered gates with explicit evidence (chosen)

Pros:
- Clear pass/fail sequencing and remediation.
- Strong audit trail in release artifacts/state.
- No default bypass path.

Cons:
- Adds explicit gate reporting requirements.

## Minimal architecture

### 1) Release gates and evidence flow

- **Evidence flow**: Gates read from canonical evidence artifacts only. Pass is
  asserted only when evidence exists and indicates pass; missing or stale
  evidence never implies pass.
- **Canonical evidence sources**:
  - Check-in test: `tests/report.md` (or runbook-defined test output location).
  - QA completion: `sprints/Sxxxx/qa-findings.md` (no unresolved blocking
    findings in current sprint context).
  - UAT completion: `sprints/Sxxxx/uat.json`, `sprints/Sxxxx/uat.md` (no
    placeholder, incomplete, or unresolved-fail state).

### 2) Deterministic gate order

Release gate sequence is fixed and documented; ordering is enforced so audit
trails are unambiguous:

1. **Check-in test gate** — `TEST_COMMAND` baseline evidence.
2. **QA completion gate** — no unresolved blocking findings.
3. **UAT completion gate** — verified/populated UAT artifacts.
4. **Release notes + runbook update steps** — only after gates 1–3 pass.

No later gate is evaluated as pass if an earlier mandatory gate fails.

### 3) Stale and missing evidence behavior

- **Missing evidence**: Block release with deterministic reason code and
  remediation (e.g. run `TEST_COMMAND`, re-run QA, complete verify-work). Do not
  infer pass.
- **Stale evidence**: Block release when evidence is absent or does not satisfy
  validity criteria (e.g. evidence exists and passed; optional timestamp/re-run
  policy per runbook). Prefer simple rule: "evidence exists and passed" plus
  optional timestamp check rather than complex TTL.
- **Reason codes** (aligned with R-0020 and existing release vocabulary):
  - `RELEASE_SPRINT_UNRESOLVED` — sprint context not resolvable for release.
  - `RELEASE_TEST_FAILED` — check-in test run failed.
  - `RELEASE_TEST_STALE` — test evidence missing or stale; re-run required.
  - `RELEASE_QA_EVIDENCE_MISSING` — QA evidence absent for sprint context.
  - `RELEASE_QA_BLOCKERS_OPEN` — unresolved blocking findings in QA artifact.
  - `RELEASE_UAT_INCOMPLETE` — UAT placeholder or incomplete.
  - `RELEASE_UAT_FAILED` — UAT has unresolved fail state.
  - `RELEASE_GATE_OVERRIDE_APPROVED` — override with DEC reference (exception path only).

Each code must have documented remediation (what to fix, which artifact/command, next step).

### 4) No-bypass default and decision-gate override path

- **Default**: No release path may bypass test/QA/UAT gates. Default
  configuration has no bypass (per vision Discovery Notes — US-0039).
- **Override** (exception-only): Allowed only via explicit decision gate: user
  approval, documented rationale (e.g. `DEC-xxxx`), and audit trail. Release
  output must record override with `RELEASE_GATE_OVERRIDE_APPROVED` and DEC
  reference. See DEC-0019.

### 5) Auditable gate evidence

- Each gate writes pass/fail and evidence pointers to handoff/state artifacts so
  QA and TL can verify decisions; no silent or inferred state.
- Canonical destinations: release handoff, `sprints/Sxxxx/release-findings.md`,
  `docs/engineering/state.md` (as applicable).
- Per-gate verdict fields: gate name, status, reason_code, evidence_refs,
  remediation; for overrides, decision_ref (DEC-xxxx) required.

### 6) Compatibility constraints

- Keep existing workflow stop conditions and escalation semantics.
- Preserve teams with blank optional lint/typecheck commands from false
  failures (release still requires test + QA + UAT evidence only).
- Maintain active/template parity for gate semantics (see Template parity scope below).

## Template parity scope

Active and `template/` release/qa/execute guidance must stay behaviorally
aligned so installed repos get the same release-safety contract. Drift between
active and template causes inconsistent gate semantics for new installs.

**Canonical files for gate-semantics parity:**

- `.cursor/commands/release.md`
- `.cursor/commands/qa.md`
- `.cursor/commands/execute.md`
- Runbook sections covering release gates, reason codes, and evidence locations
- Release-findings and reason-code documentation (e.g. runbook, release command text)

**Mitigation:** (1) List these files in release checklist or parity
verification steps; (2) Include template-parity verification in release
checklist or regression tests; (3) Document gate order and reason codes in both
active and template copies.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Stale-evidence threshold too strict or ambiguous | Prefer "evidence exists and passed" plus optional timestamp check; avoid complex TTL. Document in runbook. |
| Template parity drift | Canonical file list above; parity check in release checklist or regression; gate order and reason codes documented in both active and template. |
| Over-strict validation blocks runs if evidence writes are incomplete | Deterministic reason codes and remediation guidance (which command/artifact to fix); fail closed only when gate evidence is required and missing/invalid. |
| Operator friction on override path | Override remains exception-only; explicit decision gate + DEC reference keeps audit trail and discourages casual bypass. |

## Decision linkage

- Research: R-0020, R-0005
- Decision: DEC-0019

## Sprint-plan readiness (decomposition-ready)

Implementation should split into:
1. Update `/release` gate contract with strict ordered gates.
2. Define freshness/validity criteria for "latest check-in test" evidence (simple rule preferred).
3. Add QA evidence contract checks for unresolved blockers.
4. Preserve and tighten UAT verified-state gate wording.
5. Add structured gate verdict logging to release notes/state/release-findings artifacts.
6. Define explicit decision-gate override template and constraints (DEC ref required).
7. Add QA regression matrix with positive/negative and stale-evidence cases.
8. Template parity: align and verify release/qa/execute and runbook sections per canonical file list.

---

# US-0040: Per-Sprint Release Notes and Release Queue Tracker

## Overview

US-0040 replaces single mutable release notes with sprint-scoped artifacts and a
canonical queue that tracks each sprint's release lifecycle state. The goal is
to prevent overwrite, preserve history, and make unreleased work visible before
release finalization.

Scope remains workflow/process-level only. No deployment runtime changes.

## Assumption challenge and alternatives

### Option A: Keep single mutable `handoffs/release_notes.md`

Pros:
- No new artifacts or migration.

Cons:
- Fails history preservation and non-overwrite requirements.
- Cannot represent multiple unreleased sprint states deterministically.

### Option B: Keep single file with appended history sections

Pros:
- Preserves one-file discoverability.
- Better history than overwrite model.

Cons:
- Queue state remains implicit and harder to validate.
- High risk of inconsistent section formatting and parsing ambiguity.
- Backfill and partial-release state tracking remain brittle.

### Option C: Per-sprint immutable notes + canonical queue index (chosen)

Pros:
- Deterministic per-sprint history with no cross-sprint overwrite.
- Explicit queue model (`planned -> ready -> unreleased -> released`) per sprint.
- Clear migration and failure-safe semantics.

Cons:
- Adds one queue artifact and compatibility pointer rules.

## Minimal architecture

### 1) Canonical artifacts

Release notes:
- `handoffs/releases/Sxxxx-release-notes.md` (primary, sprint-scoped)

Queue index:
- `handoffs/release_queue.md` (canonical release state tracker)

Backward-compatibility pointer file:
- `handoffs/release_notes.md` remains and is updated as "latest release pointer"
  + compatibility summary (no destructive rewrite of historical sprint notes).

### 2) Queue schema and states

Each queue row records at minimum:
- `sprint_id` (for example `S0010`)
- `story_refs` (one or more `US-xxxx`)
- `status` (`planned|ready|unreleased|released|blocked`)
- `last_updated` (ISO timestamp)
- `release_notes_ref` (`handoffs/releases/Sxxxx-release-notes.md`)
- `gate_snapshot` (test/qa/uat summary or reason code)
- `release_version` (optional until final release)

State semantics:
- `planned`: sprint exists but release flow not yet entered.
- `ready`: verify-work complete and release can be attempted.
- `unreleased`: release flow entered; notes created/updated; finalization not done.
- `released`: release finalization succeeded for that sprint.
- `blocked`: deterministic failure (for example unresolved sprint identity or gate
  failure) with remediation guidance.

### 3) Deterministic transition contract

Only the target sprint row may transition during one `/release` run:

1. Resolve sprint ID from current context.
2. If unresolved:
   - do not write any sprint notes file,
   - do not mutate another sprint's queue row,
   - add/update `blocked` queue entry keyed as `UNKNOWN` with reason code
     (`RELEASE_SPRINT_UNRESOLVED`) and remediation.
3. If resolved:
   - ensure queue row exists (create if missing),
   - set row to `unreleased`,
   - write/update only `handoffs/releases/Sxxxx-release-notes.md`,
   - keep other sprint rows untouched.
4. On successful gate completion + finalization:
   - transition same row `unreleased -> released`,
   - update `release_version`/timestamp,
   - refresh compatibility pointer in `handoffs/release_notes.md`.
5. On failure after notes write:
   - keep row in `unreleased` or `blocked` with reason code,
   - never delete or overwrite other sprint note files.

### 4) Backward compatibility contract

`handoffs/release_notes.md` remains supported and becomes:
- latest release summary for the most recently finalized sprint,
- pointer list to recent per-sprint files,
- explicit note that canonical history lives under `handoffs/releases/`.

Existing workflows reading `handoffs/release_notes.md` continue to work for
"latest release" use cases, while full history is preserved per sprint.

### 5) Migration/backfill contract

One-time migration policy for legacy `handoffs/release_notes.md`:

1. Attempt to resolve sprint identity from legacy file content and state context.
2. If resolvable:
   - create `handoffs/releases/Sxxxx-release-notes.md` using legacy content,
   - preserve original legacy file content (append compatibility pointer section).
3. If not resolvable:
   - keep legacy file unchanged,
   - add queue note in `handoffs/release_queue.md` with `blocked` status and
     reason `LEGACY_NOTES_SPRINT_UNRESOLVED`,
   - include manual migration guidance.

Migration is non-destructive and repeat-safe (idempotent by sprint file existence
check).

### 6) Failure-safe behavior for metadata inconsistency

When queue and notes metadata disagree (missing file, wrong status, missing row):
- fail closed for release finalization (no forced `released` transition),
- preserve existing note artifacts as-is,
- write deterministic reason code in queue row:
  - `QUEUE_ENTRY_MISSING`
  - `NOTES_REF_MISSING`
  - `STATUS_TRANSITION_INVALID`
  - `RELEASE_SPRINT_UNRESOLVED`
- provide remediation steps (rebuild row, restore ref, rerun `/release`).

No automatic destructive reconciliation is allowed.

### 7) Ownership and phase touchpoints

- `/verify-work`: marks sprint release-candidate readiness (`ready`) in state
  context.
- `/release`: owns transitions `ready -> unreleased -> released` and note file
  generation/update for target sprint only.
- `/refresh-context`: curates queue readability, keeps stale blocked entries
  visible, and preserves historical integrity.

### 8) Template parity requirements

Implementation must keep active and `template/` guidance aligned for:
- `.cursor/commands/release.md` (new queue + per-sprint notes semantics)
- related rules/handoff guidance where release artifact paths are referenced
- placeholder artifacts for `handoffs/release_queue.md` and
  `handoffs/releases/` conventions.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split into:
1. Add canonical artifact contracts and queue schema docs.
2. Add resolver + fail-safe transition semantics in release guidance.
3. Add migration/backfill steps for legacy `handoffs/release_notes.md`.
4. Add backward-compatible pointer behavior in legacy release notes file.
5. Add QA matrix for unresolved sprint, overwrite prevention, queue-note mismatch,
   migration success/failure, and active/template parity.

---

# US-0046: Explicit `/sprint-plan --bulk` Mode

## Overview

US-0046 adds an explicit bulk planning mode for `/sprint-plan` so multiple OPEN
stories can be planned in one bounded run. The architecture keeps current
single-scope behavior as default and adds deterministic selection/grouping rules
only when bulk mode is explicitly enabled.

## Assumption challenge and alternatives

### Option A: Keep current `/sprint-plan` behavior only

Pros:
- No command contract changes.
- Lowest implementation complexity.

Cons:
- Does not satisfy the requirement for explicit multi-story planning throughput.
- Forces repetitive manual planning runs for large backlogs.

### Option B: Implicitly auto-bulk whenever many OPEN stories exist

Pros:
- Minimal user input.
- High throughput potential.

Cons:
- Ambiguous operator intent.
- High risk of surprising large planning mutations.
- Harder to audit and bound safely.

### Option C: Explicit bulk planning trigger with bounded deterministic policy (chosen)

Pros:
- Clear operator intent and safer defaults.
- Deterministic selection/grouping output.
- Predictable bounded behavior with explicit stop reasons.

Cons:
- Adds policy controls and additional regression surface.

## Minimal architecture

### 1) Explicit mode trigger and defaults

- Add an explicit trigger for bulk planning in `/sprint-plan` (flag/argument).
- Default behavior without trigger remains current non-bulk planning.
- Invalid or ambiguous bulk arguments fail safe with actionable guidance.

### 2) Deterministic story selection policy

Selection order:
1. Story priority (highest first)
2. Backlog order (stable tie-breaker)

Policy requirements:
- Stable ordering for reproducibility.
- No hidden randomness.
- Story selection evidence logged in planning breadcrumbs.

### 3) Bounded planning controls

Required controls:
- max stories per bulk run
- max generated sprints per run

Stop outcomes must be deterministic and recorded:
- reached max stories
- reached max generated sprints
- no eligible OPEN stories
- blocked by missing/ambiguous acceptance

### 4) Grouping and splitting contract

Bulk planning uses deterministic grouping:
- prefer single-story sprints by default,
- allow multi-story grouping only when estimated task count remains within
  `SPRINT_MAX_TASKS`,
- if estimated size exceeds threshold and `SPRINT_AUTO_SPLIT=1`, split and
  continue within run bounds.

No grouping rule may bypass sizing safety controls.

### 5) Artifact completeness and traceability

For each generated sprint, planning output must be complete:
- `sprint.md`
- `tasks.md`
- `progress.md`
- UAT placeholders
- `plan-verify` readiness contract

Traceability updates in `state.md` must remain deterministic and non-duplicative.

### 6) Risk model

| Risk | Mitigation |
|------|------------|
| Bulk run plans too much at once | bounded max stories/sprints controls + explicit stop reasons |
| Story starvation in repeated bulk runs | deterministic priority ordering with stable backlog tie-break and periodic fairness review |
| Incomplete generated artifacts | enforce per-sprint completeness checklist before moving to next item |
| Confusing behavior change for current users | explicit mode trigger; default non-bulk behavior unchanged |

## Decision linkage

- Research basis: `R-0010`, `R-0011`, `R-0013`
- Decision: `DEC-0023`

---

# US-0047: Explicit Bulk Execute Orchestration Mode

## Overview

US-0047 introduces explicit bulk execution orchestration that processes planned
sprints/stories continuously while preserving strict fresh-context isolation,
execute↔QA loop controls, and deterministic stop/skip behavior. In team mode,
execution must be scoped to member-owned tasks only.

## Assumption challenge and alternatives

### Option A: Rely only on existing `/auto` flag combinations

Pros:
- Reuses current functionality.
- No new command-level contract.

Cons:
- Operator intent remains implicit and easier to misconfigure.
- Team-member task scoping is not explicit in execution contract.
- Harder to communicate/verify bounded behavior per run.

### Option B: Global bulk execute without team-scope enforcement

Pros:
- Maximum throughput in single-user scenarios.

Cons:
- Unsafe for concurrent team members.
- High duplicate-work and task-collision risk.

### Option C: Explicit bulk execute mode with team-scoped guardrails (chosen)

Pros:
- Clear activation semantics and safer defaults.
- Enforces member/task scope in team mode.
- Keeps bounded and auditable behavior.

Cons:
- Requires additional scope-check logic and reason-code coverage.

## Minimal architecture

### 1) Explicit mode trigger and defaults

- Define explicit bulk execute mode (new command or explicit mode argument).
- Without explicit trigger, keep current non-bulk execution behavior.
- Invalid/ambiguous trigger input fails safe with remediation.

### 2) Work-item selection and breadcrumbs

Selection policy must be deterministic and logged:
- selected sprint/story id
- selection policy source
- team-context snapshot (when enabled):
  `TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`

### 3) Isolation and loop contract

- Fresh subagent context is mandatory per phase for each item.
- Fresh subagent context is mandatory for each execute↔QA loop cycle.
- Loop bounds (`AUTO_IMPLEMENTATION_LOOP`, max cycles) apply per item.

### 4) Team-scope enforcement model

When `TEAM_MODE=1`:
- only tasks in `ACTIVE_TASK_IDS` for the current `TEAM_MEMBER` are executable,
- pre-mutation scope validation is mandatory before task execution writes,
- out-of-scope tasks must be handled deterministically:
  - `skip` with reason code, or
  - `block` with reason code based on configured policy,
- no writes are allowed for out-of-scope tasks.

### 5) Bounded controls and stop policy

Required bounded controls:
- max items per run
- block handling policy (`stop` or `skip`)

Deterministic stop/skip outcomes:
- max items reached
- blocked item stop
- blocked item skipped
- no eligible scoped items
- decision gate pause

### 6) Resume semantics

Interrupted bulk runs require deterministic checkpoint fields:
- last completed item
- next candidate item
- stop reason
- stop phase
- team-context snapshot (if team mode)

Resume must continue safely from recorded checkpoint state.

### 7) Risk model

| Risk | Mitigation |
|------|------------|
| Duplicate or conflicting team execution | member-scope filter + no-write rule for out-of-scope tasks |
| Long unattended runs hide failures | bounded controls + deterministic reason-code breadcrumbs |
| Context bleed between items | fresh subagent per phase and per execute↔QA cycle |
| Ambiguous resume after interruption | explicit checkpoint schema with next-item and stop metadata |

## Decision linkage

- Research basis: `R-0010`, `R-0012`, `R-0013`
- Decision: `DEC-0024`

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

# US-0050: Clean Install Hygiene and Complete Clean-Repo Coverage

## Context and scope

US-0050 addresses installer trust and determinism gaps observed in real installs:
partial cleanup with `--clean-repo`, seeded historical starter data in template
artifacts, and starter references that look like cross-repo memory carryover.
Scope includes installer cleanup contract, template artifact neutrality, and
install/clean regression coverage. Out of scope: runtime product behavior and
non-workflow repository content.

## Assumption challenge and alternatives

### Option A: Keep per-installer hardcoded cleanup path lists

- **Pros**: Lowest immediate implementation effort.
- **Cons**: Path drift risk across PS1/SH/PY; recurring partial cleanup defects.
  Rejected.

### Option B: Ownership manifest as single source of truth (chosen)

- **Pros**: Deterministic cleanup coverage, simpler parity verification, safer
  scope control (installer-owned only), easier regression testing.
- **Cons**: Requires introducing and maintaining one canonical ownership
  artifact and readers in each installer.

## Minimal architecture

### 1) Ownership contract

- Introduce a canonical installer-managed ownership manifest (for example
  `template/docs/engineering/context/installer-owned-paths.json`) that defines:
  - directory ownership entries
  - file ownership entries
  - optional exclusions/safety guards
- All installer entry points (`installer.ps1`, `installer.sh`, `installer.py`)
  consume this same manifest for:
  - install include scope
  - clean-repo deletion scope

### 2) Clean-repo execution model

- `--clean-repo` resolves managed paths from ownership manifest.
- Delete only installer-owned paths that exist in target repo.
- Never traverse or delete paths outside manifest ownership boundaries.
- Emit deterministic cleanup summary (removed paths + skipped missing paths).

### 3) Template neutrality rules

- Starter artifacts in `template/docs/engineering/*` must be neutral placeholders:
  no seeded operational history rows from this repository.
- Cross-references to concrete runtime IDs are allowed only when matching baseline
  records are intentionally shipped and documented; otherwise use neutral wording.

### 4) Regression coverage

- Add install/clean lifecycle assertions:
  - fresh install => no preloaded story/decision/research operational history rows
  - clean-repo => full removal of installer-owned artifacts
  - reinstall after clean => same clean baseline
  - parity across installer entry points
- Maintain US-0018 upgrade contract compatibility.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-cleaning deletes non-framework project files | Ownership manifest must be explicit allowlist only; no broad wildcard deletes. |
| Under-cleaning leaves artifacts behind | Regression tests assert full ownership set removal per installer path. |
| Template hygiene regresses over time | Add template neutrality checks in lifecycle test suite and release checklist. |

## Decision linkage

- Research basis: `R-0024`, `R-0025`
- Decision: `DEC-0032`

# US-0051: Intelligent Intake Decomposition and Risk-Aware PO Questioning

## Context and scope

US-0051 improves intake quality by splitting broad requests into multiple
independently valuable stories and by increasing PO follow-up depth when request
breadth/risk is high (not ambiguity-only). Out of scope: downstream execute/release
contracts and runtime feature implementation.

## Assumption challenge and alternatives

### Option A: Keep single-story default with larger AC lists

- **Pros**: Simpler logic; minimal behavior change.
- **Cons**: Oversized stories, weaker sprintability, lower traceability of split
  intent. Rejected.

### Option B: Deterministic decomposition heuristics + explicit user confirmation (chosen)

- **Pros**: Better backlog quality, bounded behavior, user authority retained,
  clearer sprint planning input.
- **Cons**: More intake logic and documentation; requires robust heuristics to
  avoid over-splitting.

## Minimal architecture

### 1) Decomposition evaluator

- Add intake-time evaluator that scores request breadth using heuristics:
  - feature count / workflow-step count
  - cross-cutting impact surface
  - acceptance set size
  - risk and unknown dependencies
- If score exceeds threshold, propose multi-story decomposition.

### 2) Split strategy

- Prefer vertical slices/workflow-step slices with independent value.
- Avoid technical-layer-only split output (frontend-only/backend-only stories).
- Persist split rationale in backlog and PO->TL handoff.

### 3) Adaptive questioning policy

- Keep `INTAKE_GUIDED_MODE=1` behavior but add risk-aware escalation:
  - ambiguity-based questions (existing)
  - risk/breadth-based questions (new)
- Keep question loop bounded (max rounds or stop when acceptance confidence is sufficient).
- Preserve explicit user choice to accept/merge/adjust proposed splits.

### 4) Low-touch compatibility

- `INTAKE_GUIDED_MODE=0` keeps low-touch path and mandatory duplicate check.
- No forced decomposition in low-touch mode unless user requests decomposition.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-splitting into too many tiny stories | Threshold + bounded split count + explicit user confirmation before persist. |
| Under-splitting broad requests | Include breadth and risk heuristics; emit rationale when staying single-story. |
| Endless follow-up loop | Bounded question rounds and deterministic stop conditions. |

## Decision linkage

- Research basis: `R-0024`, `R-0025`
- Decision: `DEC-0033`

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

# US-0056: Strict Runtime Proof for Per-Phase Subagent Isolation

## Overview

US-0056 strengthens the existing isolation contract by requiring runtime
attestation at each phase boundary. Artifact markers remain required, but `/auto`
must fail closed unless each completed phase provides valid, unique, fresh, and
linkable runtime proof.

## Architecture goals

- Add strict runtime attestation without weakening current isolation evidence.
- Enforce deterministic boundary validation and fail-closed continuation.
- Preserve pause/resume traceability with strict-proof provenance.
- Keep active/template parity and bounded compatibility handling for legacy runs.

## Minimal architecture

1. **Runtime attestation envelope**
   - Required fields per completed phase run:
     - `orchestrator_run_id`
     - `runtime_proof_id`
     - `phase_id`
     - `role`
     - `proof_issued_at` (UTC/RFC3339)
     - `proof_ttl_seconds`
     - `proof_hash` (deterministic hash over canonical tuple fields)
   - Evidence must be linked to canonical checkpoint in `docs/engineering/state.md`.

2. **Boundary validator in `/auto`**
   - After each phase, `/auto` validates attestation tuple and linkage before
     advancing.
   - Fail-closed reasons are deterministic:
     - `RUNTIME_PROOF_MISSING`
     - `RUNTIME_PROOF_INVALID`
     - `RUNTIME_PROOF_REUSED`
     - `RUNTIME_PROOF_STALE`
     - `RUNTIME_PROOF_AMBIGUOUS_LINK`

3. **Strict-proof provenance for pause/resume**
   - `handoffs/resume_brief.md` stores strict-proof provenance reference for last
     valid boundary.
   - Resume resolution fails closed when provenance is stale/unparseable or
     strict-proof chain cannot be validated.

4. **Gate integration**
   - Isolation/release verification consumes strict attestation in addition to
     existing artifact evidence fields from US-0048/DEC-0029.
   - No gate bypass: missing strict-proof evidence blocks continuation/release.

5. **Legacy compatibility contract**
   - No historical rewrite.
   - Legacy runs without strict attestation produce remediation guidance and
     deterministic blocked outcomes.

## Guardrail invariants

- `/auto` remains orchestration-only; phase work is still isolated by role.
- Strict runtime proof augments, not replaces, existing evidence requirements.
- Fail-closed behavior is mandatory on missing/invalid/reused/stale proof.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| False blocks due to tight freshness windows | bounded TTL defaults + clear remediation guidance |
| Proof-ID collision/reuse ambiguity | deterministic uniqueness constraints + reuse checks |
| Partial rollout causes parity drift | active/template contract parity + regression coverage |

## Decision linkage

- Research basis: `R-0034`
- Decision: `DEC-0038` accepted for strict attestation tuple + validator contract
- Boundaries: workflow orchestration proof contract only; no product runtime behavior changes.

---

# US-0057: Upgrade-Safe Scratchpad Example Refresh and Parity

## Overview

US-0057 tightens installer upgrade behavior so the framework-owned scratchpad
example is always refreshed while user-owned local overrides remain preserved.
The solution extends existing upgrade ownership semantics (US-0018/US-0050)
with explicit scratchpad-surface rules and deterministic operator diagnostics.

## Ownership model

- Framework-owned: `.cursor/scratchpad.local.example.md`
- User-owned: `.cursor/scratchpad.local.md`
- Mixed/shared defaults remain unchanged (`.cursor/scratchpad.md`).

## Upgrade behavior contract

In `--mode upgrade`, installers must:
1. Refresh framework-owned scratchpad example to latest release content.
2. Preserve user-owned local scratchpad with no overwrite path.
3. Emit deterministic diagnostics:
   - scratchpad example status (`added|updated|unchanged`)
   - user local file preservation signal when present.

## Parity and validation

- The same behavior is required in all installer implementations:
  - `installer.ps1`
  - `installer.sh`
  - `installer.py`
- Regression coverage validates:
  - framework refresh for example file,
  - preservation of user local overrides,
  - no regression in existing install/upgrade/clean guarantees.

## Decision linkage

- Research basis: `R-0032`
- Decision: `DEC-0039`

---

# US-0058: Deterministic Artifact Ordering and Write Discipline

## Overview

US-0058 standardizes write ordering across mutable workflow artifacts. The goal
is deterministic, idempotent artifact mutations so command reruns do not
oscillate insertion direction or reorder unrelated entries.

## Architecture goals

- Define one canonical ordering matrix for mutable artifact surfaces.
- Keep `state.md` checkpoint writes append-bottom only.
- Keep backlog/acceptance story ordering sorted-canonical and aligned.
- Enforce fail-safe behavior when insertion anchors are missing or ambiguous.
- Preserve canonical ownership guarantees from US-0045/US-0055.

## Minimal architecture

1. **Ordering matrix artifact**
   - New canonical policy file:
     `docs/engineering/artifact-ordering-policy.md`
   - Defines per-artifact policy: `append-bottom`, `prepend-top`,
     `sorted-canonical`.

2. **Command contract integration**
   - Commands that mutate ordering-sensitive artifacts must reference the matrix:
     `/auto`, `/intake`, `/release`, `/refresh-context`, `/status-reconcile`.
   - Command behavior must remain target-scoped; no broad rewrites.

3. **Fail-safe anchor handling**
   - Missing/ambiguous placement anchors trigger deterministic fail-closed code:
     `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`.
   - No partial writes on fail-safe path.

4. **Idempotence requirement**
   - Re-running commands with no semantic changes must keep identical order.
   - No top/bottom insertion flips across repeated runs.

## Decision linkage

- Research basis: `R-0033`
- Decision: `DEC-0040`

---

# US-0059: Deterministic Intake Runtime Capability Guard and Single-Writer Drift Safety

## Overview

US-0059 hardens `/intake` runtime behavior so missing role-capability and
concurrent-writer scenarios are handled deterministically and fail safe.

## Architecture goals

- Fail fast when required role-specific intake subagent capability is missing.
- Prevent silent fallback in default policy.
- Distinguish self-write updates from external concurrent artifact drift.
- Preserve deterministic ordering and canonical ownership guarantees.
- Keep active/template contracts and regression checks aligned.

## Minimal architecture

1. **Capability preflight contract**
   - `/intake` performs capability preflight for role-specific `po` subagent
     before artifact mutation.
   - Missing capability fails fast with deterministic reason code
     `SUBAGENT_CAPABILITY_UNAVAILABLE`.
   - Default policy denies fallback (`INTAKE_SUBAGENT_FALLBACK=deny`);
     fallback requires explicit opt-in (`allow`).

2. **Single-writer intake scope**
   - Each intake run binds deterministic writer identity metadata:
     - `writer_id`
     - `intake_run_id`
   - Mutation scope is constrained to target intake artifacts:
     `vision`, `backlog`, `acceptance`, and `po_to_tl`.

3. **Self-write-aware drift detection**
   - Drift checks must accept self-generated writes for the same
     `(writer_id, intake_run_id)` as valid continuation.
   - Conflicting external concurrent mutation fails safe with reason code
     `INTAKE_CONCURRENT_WRITER_DETECTED` and no partial overwrite.

4. **Ordering/ownership compatibility**
   - Existing canonical ownership (`backlog` authority) remains unchanged.
   - Sorted-canonical intake placement and monotonic timestamp constraints remain
     mandatory and non-bypass.

5. **Verification and parity**
   - Add regression coverage for:
     - capability-missing fail-fast path,
     - self-write non-false-positive path,
     - external concurrent writer fail-safe path.
   - Keep active/template command/runbook/README parity.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Strict preflight blocks valid fallback workflows | explicit opt-in fallback policy via `INTAKE_SUBAGENT_FALLBACK=allow` |
| Incomplete writer identity causes residual false positives | deterministic run-scoped writer IDs and target-scoped mutation checks |
| Broad drift handling accidentally suppresses real conflicts | fail-safe only for same writer/run identity; external conflicting writes remain blocking |

## Decision linkage

- Research basis: `R-0035`
- Decision: `DEC-0041`
- Boundaries: workflow runtime guard behavior only; no product runtime feature changes.

---

# US-0060: Deterministic State Hot-Surface Rollover and Archive Enforcement

## Overview

US-0060 enforces bounded growth for `docs/engineering/state.md` by introducing
deterministic rollover triggers and non-destructive archival into
`docs/engineering/state-archive/`.

## Architecture goals

- Keep `state.md` as a compact hot surface for recent checkpoints.
- Enforce deterministic rollover thresholds instead of policy-only guidance.
- Preserve full historical evidence via append-only archive packs.
- Keep rollover idempotent and fail-safe on ambiguous boundaries or write errors.
- Preserve ordering, canonical ownership, and retrieval contracts.

## Minimal architecture

1. **Rollover trigger contract**
   - Configure via scratchpad:
     - `STATE_HOT_MAX_LINES` (default `1200`)
     - `STATE_HOT_MAX_CHECKPOINTS` (default `80`)
   - `/refresh-context` evaluates both thresholds and triggers rollover when
     either is exceeded.

2. **Deterministic archive mechanics**
   - Move oldest low-frequency checkpoints from hot surface into deterministic
     archive packs (`state-pack-YYYY-QN.md` or `state-pack-YYYYMMDD.md`).
   - Preserve chronology and evidence references.
   - Keep bounded recent checkpoints in hot surface.

3. **Fail-safe behavior**
   - If archive boundary cannot be safely determined:
     `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`.
   - If archive write cannot be completed:
     `STATE_ARCHIVE_WRITE_FAILED`.
   - Both fail-safe paths forbid partial mutation.

4. **Retrieval compatibility**
   - `/ask` and `/refresh-context` continue latest-first hot-surface reads.
   - Bounded expansion to archives only when unresolved.

5. **Parity and verification**
   - Active/template parity across scratchpad flags, command contracts,
     runbook/README, and policy artifacts.
   - Regression coverage for threshold-crossing rollover, idempotent reruns,
     and fail-safe error paths.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Thresholds too low reduce near-term debugging context | conservative defaults with explicit scratchpad overrides |
| Non-deterministic archive boundaries cause churn | deterministic boundary selection and stable pack naming |
| Partial archive writes corrupt traceability | fail-safe no-partial-write on archive boundary/write errors |

## Decision linkage

- Research basis: `R-0036`
- Decision: `DEC-0042`
- Boundaries: workflow artifact compaction enforcement only; no product runtime behavior changes.

---

# US-0061: Cross-Phase Artifact Ownership Guard and Deterministic Archive Control

## Overview

US-0061 hardens non-destructive artifact mutation behavior across phases and
adds stricter archive execution controls. The goal is to prevent cross-phase
history loss (especially in `docs/engineering/architecture.md`) while making
state archival deterministic and verifiable.

## Architecture goals

- Define explicit phase/artifact ownership boundaries.
- Fail closed on non-owned section deletion/rewrite attempts.
- Allow only explicit, auditable override-authorized mutation paths.
- Preserve architecture history across all normal phase runs.
- Strengthen state archive execution with deterministic verification evidence.

## Minimal architecture

1. **Ownership matrix contract**
   - Canonical policy artifact:
     `docs/engineering/artifact-ownership-policy.md`.
   - Matrix defines:
     - artifact scope ownership,
     - allowed phases,
     - override-authorized phases.

2. **Cross-phase guardrail enforcement**
   - Every mutable command phase must enforce ownership policy before write.
   - Non-authorized section rewrite/deletion fails safe with
     `PHASE_OWNERSHIP_VIOLATION`.
   - Override-authorized mutation requires explicit evidence fields; missing
     evidence fails with `PHASE_OVERRIDE_EVIDENCE_MISSING`.

3. **Architecture history protection**
   - `docs/engineering/architecture.md` is history-preserving:
     - append new `US-xxxx` section for new stories,
     - update target section only when needed,
     - unrelated story-section deletion is forbidden.
   - Detection fail-safe: `ARCH_HISTORY_DELETION_DETECTED`.

4. **Deterministic archive control hardening**
   - `/refresh-context` archive behavior remains threshold-driven
     (`STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS`).
   - Add deterministic archive verification evidence (boundary + moved/retained
     markers).
   - Verification mismatch fails with `STATE_ARCHIVE_VERIFICATION_FAILED`.

5. **Parity and verification**
   - Active/template parity required for commands, rules, policy docs, runbook,
     README, and regression assertions.
   - Regression coverage includes:
     - prohibited cross-phase deletion path,
     - explicit override evidence requirement path,
     - archive verification fail-safe path.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Ownership matrix too strict blocks legitimate target updates | target-scope rules are explicit per artifact; no broad denial defaults |
| Override path becomes implicit bypass | override-authorized list is explicit and evidence-gated |
| Archive verification adds overhead | verification output remains deterministic and bounded |

## Decision linkage

- Research basis: `R-0037`
- Decision: `DEC-0043`
- Boundaries: workflow artifact mutation/archival safety only; no product runtime feature changes.

---

# US-0064: Remote Runtime Connectivity Contract for QA/Release/Publish

## Overview

US-0064 extends release target configuration with runtime connectivity metadata
and defines phase-level consumption rules for remote/local contexts. It enables
release and QA workflows to provide deterministic operator connection guidance
without weakening gates or exposing secrets.

## Architecture goals

- Extend target schema for runtime connectivity and ingress metadata.
- Support Docker-over-SSH runtime/deploy patterns as first-class contract data.
- Keep remote behavior config-driven and deterministic for release/QA/execute.
- Provide canonical operator connectivity documentation.
- Preserve existing quality/release gates and secret safety constraints.

## Minimal architecture

1. **Connectivity schema extension**
   - Add deterministic metadata to `docs/engineering/release-targets.json`:
     - `runtime.mode` (`local|remote`)
     - endpoint fields (`domainEnv|ipEnv|hostEnv`, `port`, `protocol`)
     - optional ingress (`traefik.enabled`, `router`, `entrypoint`, `tls`)
     - optional `dockerOverSsh` contract for SSH targets.

2. **Validation and fail-safe behavior**
   - Enforce type-specific connectivity validation in release/remote-aware phase
     contracts.
   - Missing/invalid required connectivity fields fail with
     `REMOTE_CONNECTIVITY_CONFIG_INVALID`.
   - Connectivity document write failures fail with
     `RUNTIME_CONNECTIVITY_DOC_WRITE_FAILED`.

3. **Phase consumption contract**
   - `/release` consumes enriched connectivity metadata and emits operator-safe
     endpoint guidance.
   - `/qa` supports optional remote runtime verification/debug context when
     target runtime is remote.
   - `/execute` records remote/local execution context for handoff/state
     evidence when remote target context is active.

4. **Canonical operator documentation**
   - Add `docs/engineering/runtime-connectivity.md` as canonical sanitized
     runtime endpoint summary and connection guide.
   - Keep secrets out of artifacts (env-reference names only).

5. **Parity and verification**
   - Active/template parity for schema, commands, runbook/README, and docs.
   - Regression checks cover schema fields, phase contracts, and connectivity doc
     presence.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Schema complexity increases onboarding effort | provide minimal deterministic default fields and documented examples |
| Secret leakage in operator outputs | enforce env-reference-only policy and explicit redaction contract |
| Remote/local ambiguity in phase behavior | require explicit `runtime.mode` and deterministic skip/no-op semantics |

## Decision linkage

- Research basis: `R-0040`
- Decision: `DEC-0044`
- Boundaries: workflow release/QA/execute connectivity context only; no product runtime behavior changes.

---

# US-0062: Installer-Owned `its_magic/` Folder for Framework Metadata

## Overview

US-0062 introduces a deterministic installer-owned metadata boundary so
framework metadata is kept separate from project artifacts. Canonical installer
metadata now lives under `its_magic/`, while project-owned surfaces remain in
their existing product/engineering locations.

## Architecture goals

- Define a stable metadata home for installer/runtime framework markers.
- Preserve non-destructive behavior for existing repositories.
- Keep install/upgrade/clean behavior manifest-driven and auditable.
- Maintain active/template parity across installer implementations.

## Minimal architecture

1. **Canonical metadata home**
   - Installer-managed metadata surfaces are placed under `its_magic/`.
   - Canonical installed version marker path becomes
     `its_magic/.its-magic-version`.
   - Framework metadata README surface is emitted as `its_magic/README.md`.

2. **Manifest and ownership classification**
   - `installer-owned-paths.manifest` install/clean sections include `its_magic`.
   - Installer classifiers treat `its_magic/*` as framework-owned scope.
   - Project content locations remain outside `its_magic/` and are not relocated.

3. **Upgrade migration compatibility**
   - Upgrade/read logic accepts legacy root `.its-magic-version` for backward
     compatibility.
   - Write path always targets `its_magic/.its-magic-version`.
   - Legacy root marker is removed after successful canonical write.

4. **Clean-repo safety**
   - Clean operation removes framework-owned `its_magic/` contents and legacy
     root marker if present.
   - Non-owned project content remains untouched.

5. **Verification and parity**
   - Regression tests cover fresh install, upgrade migration, and clean behavior.
   - Active/template installer scripts and manifests remain contract-equivalent.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Legacy repositories rely on root version marker | read fallback supports legacy marker; write migrates to canonical location |
| Metadata boundary drift across platforms | align PowerShell/shell/Python installers plus shared manifest contract |
| Clean behavior removes too broadly | clean remains restricted to manifest-owned paths only |

## Decision linkage

- Research basis: `R-0038`
- Decision: `DEC-0045`
- Boundaries: installer metadata placement/migration only; no product runtime feature behavior changes.

---

# US-0063: OS-Aware Runbook Command Auto-Bootstrap with Verified Quality Gates

## Overview

US-0063 adds deterministic installer-time bootstrap for runbook command keys to
avoid first-run blockers while preserving strict quality gate behavior.

## Architecture goals

- Auto-populate real baseline command defaults from OS + stack signals.
- Preserve user-provided explicit runbook commands.
- Keep mandatory gate policy intact (`TEST_COMMAND` required).
- Emit deterministic diagnostics for unresolved/invalid baseline generation.

## Minimal architecture

1. **Bootstrap contract + precedence**
   - Apply `user override > detected defaults > fail-fast diagnostics`.
   - Never overwrite non-empty user command values in runbook.

2. **Detection + mapping**
   - Detect stack from canonical markers:
     - `package.json` scripts (`test`, optional `lint`, optional `typecheck`)
     - `go.mod`
     - Python markers (`pyproject.toml`, `requirements.txt`, `setup.py`)
     - platform test scripts where appropriate.
   - Map to deterministic defaults:
     - Node: `npm run test` (+ optional `npm run lint`, `npm run typecheck`)
     - Go: `go test ./...`
     - Python: `python -m pytest`

3. **Validation and fail-fast**
   - Probe candidate commands for baseline validity prior to write.
   - If baseline remains unresolved or invalid, emit deterministic diagnostics:
     - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED`
     - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:<reason>`
   - Installer exits non-zero on unresolved mandatory baseline.

4. **Parity and compatibility**
   - Implement equivalent behavior in PowerShell/shell/Python installers.
   - Keep active/template docs and tests aligned.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Incorrect default inferred for custom stack | user override always wins and is never overwritten |
| Optional command over-detection causes false confidence | only populate optional commands when confidently detectable |
| Regression across installer variants | enforce cross-installer parity and lifecycle regression tests |

## Decision linkage

- Research basis: `R-0039`
- Decision: `DEC-0046`
- Boundaries: installer/bootstrap and workflow gate readiness only; no runtime product behavior change.

---

# US-0065: Runtime QA Autopilot for Generated Projects

## Overview

US-0065 makes runtime verification mandatory for generated projects so QA cannot
pass on static checks alone. The architecture adds a minimal deterministic
runtime-validation contract across execute/qa, with bounded retries and
structured evidence.

## Architecture goals

- Require startup, readiness/connectivity, and runtime-log validation before
  PASS.
- Keep retry behavior bounded and auditable.
- Preserve remote-runtime support using existing connectivity contract surfaces.
- Keep scope strict to runtime verification/evidence only (no test scaffold or
  release hint schema expansion in this story).

## Minimal architecture

1. **Runtime verification pipeline (mandatory)**
   - Canonical stage order:
     `startup -> readiness/connectivity -> log scan -> bounded retry loop -> verdict`.
   - PASS requires all mandatory stages to succeed (or be deterministically
     skipped by explicit policy).
   - Evidence contract must include:
     - startup command/profile,
     - runtime mode (`local|remote`) and endpoint/health result,
     - retry ledger (attempt, delay, outcome),
     - log severity summary,
     - final verdict + reason code.

2. **Reason-code taxonomy (deterministic)**
   - Runtime failure boundaries use explicit families:
     - `RUNTIME_STARTUP_FAILED`
     - `RUNTIME_ENDPOINT_UNREACHABLE`
     - `RUNTIME_LOG_CRITICAL_DETECTED`
     - `RUNTIME_RETRY_BUDGET_EXHAUSTED`
     - `RUNTIME_STACK_PROFILE_UNRESOLVED`
   - Each reason code includes concise remediation guidance and evidence refs.

3. **Bounded retry policy**
   - Retries apply only to transient startup/connectivity failures.
   - Retry ceiling and delay/backoff are configured and capped.
   - Non-transient signals (for example critical runtime log severity) fail
     closed without broad retry loops.

4. **Stack-aware runtime profile selection**
   - Minimum supported stack profiles: Node, Python, Go, Java, .NET.
   - Unknown/ambiguous stack falls back deterministically to explicit fail-safe
     (`RUNTIME_STACK_PROFILE_UNRESOLVED`) rather than silent PASS.

5. **Webapp verification path (when applicable)**
   - For HTTP/UI runtime contexts, include browser-surface runtime checks and
     console/network error inspection evidence.
   - Keep this as runtime-truth verification, not release-hint or scaffold work.

## Alternatives challenged and tradeoffs

1. **Strict mandatory runtime pipeline vs optional best-effort checks**
   - Alternative: optional runtime checks with warning-only outcome.
   - Tradeoff: lower friction but preserves false-PASS risk.
   - Decision: choose strict mandatory pipeline because acceptance requires
     deterministic runtime proof.
   - Risk: slower QA runs on large projects.
   - Mitigation: bounded retries and explicit timeout caps.

2. **Unified retry policy vs stack-specific retry heuristics**
   - Alternative: per-stack retry semantics.
   - Tradeoff: potentially better tuning but higher complexity/drift.
   - Decision: start with unified bounded policy plus deterministic caps.
   - Risk: defaults may be suboptimal for some stacks.
   - Mitigation: keep policy configurable and evidence-first for tuning.

3. **Fail-fast unknown stack vs permissive generic runtime attempt**
   - Alternative: generic fallback command attempts.
   - Tradeoff: broader coverage but unpredictable behavior/noise.
   - Decision: fail-fast unresolved stack profile for deterministic outcomes.
   - Risk: legitimate projects may require manual profile mapping initially.
   - Mitigation: explicit remediation output and future profile extension path.

## Decision gates

- **Gate A (must pass):** reason-code set and evidence schema approved as
  canonical contract for execute/qa.
- **Gate B (must pass):** bounded retry defaults validated as strict enough to
  prevent retry storms while avoiding common transient false negatives.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Timeout defaults produce false negatives on slower runtimes | require configurable timeout ceilings with deterministic evidence output |
| Retry policy masks persistent defects | limit retries to transient classes and fail fast on critical log severity |
| Stack detection ambiguity causes inconsistent behavior | enforce explicit unresolved-stack fail-safe reason code and remediation |
| Browser checks increase runtime overhead for web stacks | run browser path conditionally only for detected HTTP/UI contexts |

## Decision linkage

- Research basis: `R-0042` (and `R-0041` for baseline workflow pattern alignment)
- Decision: `DEC-0047`
- Boundaries: runtime verification contract/evidence only for generated projects; no test scaffolding (`US-0066`) and no release-hint schema expansion (`US-0067`).

---

# Architecture Addendum (US-0066): Generated Test Scaffolding and Auto-Run Contract

Date: 2026-03-16
Story: `US-0066`
Research anchor: `R-0043` (plus `R-0041` baseline context)

## Problem statement

Generated app repositories can pass process gates without guaranteed baseline
tests when projects start with no test assets. `US-0066` closes this gap by
enforcing deterministic, non-destructive baseline test scaffolding and
automatic QA execution evidence.

## Scope and boundaries (strict)

- In scope:
  - workflow-level baseline test scaffold generation for Node/Python/Go/Java/.NET,
  - deterministic `TEST_COMMAND` baseline wiring for resolved stacks,
  - mandatory `/qa` baseline test auto-run evidence,
  - idempotent rerun and non-destructive preservation behavior.
- Out of scope:
  - advanced framework-specific test architecture generation,
  - runtime startup/connectivity verdict replacement (remains `US-0065`),
  - release operator hint schema expansion (`US-0067`) and intake packs (`US-0068`).

## Architecture decision summary

1. **Deterministic stack-profile baseline generation**
   - Detect supported stack/project profile (Node/Python/Go/Java/.NET).
   - Generate only missing baseline unit/integration/acceptance scaffold assets.
   - Write generated path inventory to execution evidence.

2. **Runbook command baseline wiring**
   - Resolve one minimal runnable baseline `TEST_COMMAND` per supported stack.
   - Apply non-destructive precedence:
     - keep existing user-authored runnable command,
     - fill only missing/unset baseline command.

3. **Mandatory QA auto-run evidence**
   - `/qa` must execute resolved baseline tests automatically.
   - Evidence requires command, pass/fail verdict, and output reference.

4. **Fail-closed unsupported/unresolved handling**
   - Deterministic diagnostics are required when profile resolution or generation
     fails:
     - `TEST_SCAFFOLD_STACK_UNRESOLVED`
     - `TEST_SCAFFOLD_UNSUPPORTED_STACK`
     - `TEST_SCAFFOLD_GENERATION_FAILED`

5. **Idempotent rerun contract**
   - Stable scaffold paths/conventions; no duplicate baseline files on rerun.
   - No oscillating command rewrites between repeated `/execute` runs.

6. **Runtime-autopilot integration boundary**
   - Static baseline test PASS is necessary but not sufficient.
   - Runtime startup/connectivity/log verdict remains governed by `US-0065`.

## Alternatives challenged and tradeoffs

1. **Mandatory scaffolding vs optional best-effort**
   - Alternative: warning-only scaffold attempt.
   - Tradeoff: lower friction, weaker guarantees.
   - Decision: mandatory fail-closed contract to satisfy AC-2/4/5/10.
   - Risk: stricter failures in partially configured repos.
   - Mitigation: deterministic remediation diagnostics and explicit evidence refs.

2. **Per-stack deterministic templates vs one generic template**
   - Alternative: single generic scaffold shape.
   - Tradeoff: simpler implementation, weaker runnable correctness.
   - Decision: per-stack minimal deterministic profiles to stay runnable by default.
   - Risk: profile matrix maintenance overhead.
   - Mitigation: keep first iteration limited to five minimum stacks.

3. **Built-in profile matrix vs plugin architecture (v1)**
   - Alternative: extensible plugin model immediately.
   - Tradeoff: future flexibility, higher complexity/risk now.
   - Decision: built-in deterministic matrix in v1 (simplest viable approach).
   - Risk: slower onboarding for niche stacks.
   - Mitigation: explicit unsupported-stack fail-safe and future extension path.

## Decision gates

- **Gate A (must pass):** non-destructive precedence behavior is canonical and
  testable (existing user tests/commands preserved).
- **Gate B (must pass):** unsupported/unresolved stack handling is deterministic
  and fail-closed with actionable remediation.
- **Gate C (must pass):** QA auto-run evidence schema is complete and auditable.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Wrong stack chosen in polyglot repos | deterministic stack-selection precedence + unresolved fail-safe |
| Baseline generation clobbers user-authored assets | explicit non-destructive precedence and scoped writes to missing assets only |
| Repeated runs create duplicate/oscillating artifacts | stable path conventions + rerun idempotence checks in regression suite |
| Static tests pass while runtime still broken | preserve strict `US-0065` runtime-autopilot gate as independent mandatory verdict |

## Decision linkage

- Research basis: `R-0043` (with `R-0041` supporting baseline patterns).
- Decision: `DEC-0048`.
- Boundary note: `US-0066` covers generated test scaffolding + QA auto-run
  evidence only; release operator hint schema remains `US-0067`.

## US-0067 Architecture: Release operator Run/Connect/Verify hints contract

### Scope and constraints

- Story: `US-0067`
- Scope: release-operator guidance contract only for `Run/Connect/Verify` hints.
- In-scope:
  - deterministic release artifact schema and ordering,
  - required field validation and fail-closed behavior,
  - concise legacy pointer parity for latest release summary.
- Out-of-scope:
  - runtime autopilot logic and evidence contract (`US-0065`),
  - generated test scaffold logic (`US-0066`),
  - deployment engine orchestration or platform-specific operators.

### Architecture decisions

1. **Canonical operator section with fixed order**
   - Canonical sprint release notes must include:
     `Run -> Connect -> Verify -> Credentials (env-ref only) -> Known Issues`.
   - Fixed order is mandatory for idempotent reruns and operator readability.

2. **Required-field contract for release finalization**
   - Release completion must validate required fields before final PASS.
   - Missing or ambiguous required fields fail closed with deterministic reason
     codes and remediation guidance in release findings.

3. **Runtime context explicitness**
   - `runtime_mode` must be explicit as `local|remote`.
   - When `docs/engineering/runtime-connectivity.md` exists, endpoint/connectivity
     claims in release artifacts must align with that contract.

4. **Credentials safety boundary**
   - Credentials guidance is env-reference-only.
   - Inline secret values in release/operator artifacts are prohibited.

5. **Legacy pointer surface parity**
   - `handoffs/release_notes.md` remains concise and points to canonical sprint
     release notes while preserving a deterministic latest run/connect summary.

### Deterministic validation and reason-code baseline

- Required validation boundaries for finalization:
  - missing required operator fields,
  - ambiguous run/connect values,
  - missing explicit runtime mode,
  - credentials section violating env-ref-only policy.
- Deterministic fail-closed reason-code baseline:
  - `RELEASE_OPERATOR_HINTS_MISSING_REQUIRED_FIELD`
  - `RELEASE_OPERATOR_HINTS_AMBIGUOUS_FIELD`
  - `RELEASE_OPERATOR_HINTS_RUNTIME_CONTEXT_MISSING`
  - `RELEASE_OPERATOR_HINTS_CREDENTIALS_POLICY_VIOLATION`

### Alternatives challenged and tradeoffs

1. **Flexible free-form notes without fixed schema**
   - Alternative: allow arbitrary operator narrative.
   - Tradeoff: lower authoring friction, weaker reproducibility and readability.
   - Decision: fixed schema to keep output deterministic and auditable.

2. **Warning-only validation for missing fields**
   - Alternative: permit completion with warnings.
   - Tradeoff: fewer blocked releases, but poor operator actionability.
   - Decision: fail-closed finalization on missing/ambiguous required fields.

3. **Embedding credentials directly in notes**
   - Alternative: include inline secrets for convenience.
   - Tradeoff: short-term ease, unacceptable security exposure.
   - Decision: env-ref-only credentials contract.

### Decision gates

- **Gate A (must pass):** canonical release notes include fixed-order operator
  sections with all required fields.
- **Gate B (must pass):** release finalization blocks with deterministic reason
  code when required fields are missing or ambiguous.
- **Gate C (must pass):** credentials guidance is env-ref-only and no inline
  secrets appear in release surfaces.

### Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Operator notes drift into non-deterministic formatting | enforce fixed-order section schema and parity checks |
| Release passes without actionable run/connect details | fail-closed required-field validation with reason-code remediation |
| Runtime context mismatch across docs/surfaces | explicit `local|remote` field and alignment check against runtime-connectivity contract |
| Secret leakage into release notes | env-ref-only credentials rule plus validation guardrails |

### Decision linkage

- Research basis: `R-0044` (with `R-0041` supporting baseline patterns).
- Decision: `DEC-0049`.
- Boundary note: `US-0067` covers release operator hints only; runtime execution
  truth and generated test scaffolding remain governed by `US-0065`/`US-0066`.

## US-0068 Architecture: Mandatory intake question packs for first and small intakes

### Scope and constraints

- Story: `US-0068`
- Scope: intake questionnaire and persistence-gate policy only.
- In-scope:
  - deterministic two-pack intake schema (`first-intake-pack`, `small-intake-pack`),
  - required topic coverage validation before persistence,
  - bounded assumptions confirmation path as explicit compatibility mechanism,
  - low-touch mode compatibility without safety-topic bypass,
  - deterministic intake evidence fields for downstream trust.
- Out-of-scope:
  - runtime QA autopilot contract (`US-0065`),
  - generated test scaffolding contract (`US-0066`),
  - release operator `Run/Connect/Verify` hints contract (`US-0067`).

### Architecture decisions

1. **Two deterministic intake packs with explicit coverage taxonomy**
   - `first-intake-pack` captures comprehensive foundation topics for new/first
     requests.
   - `small-intake-pack` captures compact but mandatory topics for narrow follow-up
     work.
   - Both packs use stable topic IDs with required/optional classification.

2. **Fail-closed persistence gate**
   - Story persistence to backlog/acceptance is blocked when required topic
     coverage is incomplete.
   - Persistence may proceed only when:
     - required coverage is complete, or
     - bounded assumptions are explicitly confirmed by the user and recorded.

3. **Low-touch compatibility with safety floor**
   - Low-touch interaction remains available for speed.
   - Critical safety coverage cannot be skipped by low-touch path when required
     fields are missing.

4. **Deterministic intake evidence contract**
   - Intake outputs must persist structured evidence fields:
     - `asked_topics`
     - `missing_topics`
     - `assumptions_confirmed`
   - Coverage state becomes auditable and machine-verifiable for downstream phases.

5. **Bounded rounds and deterministic diagnostics**
   - Guided/adaptive follow-ups remain allowed but bounded.
   - Missing required coverage emits deterministic fail-closed diagnostics with
     remediation guidance.

### Deterministic validation and reason-code baseline

- Required validation boundaries:
  - unresolved required topic coverage for selected pack,
  - missing explicit user confirmation when assumptions are used,
  - attempted persistence while required coverage remains incomplete.
- Deterministic fail-closed reason-code baseline:
  - `INTAKE_REQUIRED_TOPIC_MISSING`
  - `INTAKE_REQUIRED_PACK_INCOMPLETE`
  - `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`
  - `INTAKE_PERSISTENCE_BLOCKED`

### Alternatives challenged and tradeoffs

1. **Adaptive-only intake without fixed minimum packs**
   - Alternative: continue fully dynamic prompting.
   - Tradeoff: lower upfront friction, weaker deterministic quality floor.
   - Decision: enforce two fixed minimum packs.

2. **Single comprehensive pack for every intake**
   - Alternative: always ask full questionnaire.
   - Tradeoff: stronger completeness, higher friction for small requests.
   - Decision: use two-pack model to balance quality and flow.

3. **Warning-only persistence when coverage is incomplete**
   - Alternative: persist with warnings.
   - Tradeoff: fewer blocks, degraded downstream reliability.
   - Decision: fail closed until coverage or confirmed assumptions exist.

### Decision gates

- **Gate A (must pass):** deterministic pack schemas include required topic IDs
  matching `US-0068` acceptance coverage.
- **Gate B (must pass):** persistence blocks deterministically on incomplete
  required coverage.
- **Gate C (must pass):** low-touch path preserves critical safety coverage and
  records structured evidence fields.

### Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Question packs become too broad and increase friction | maintain two-pack model with compact small-intake scope and bounded follow-ups |
| Weak topic taxonomy allows false coverage completion | require deterministic topic IDs with required/optional classification |
| Low-touch path bypasses critical safety topics | enforce fail-closed safety floor before persistence |
| Drift between active/template intake policy surfaces | keep deterministic reason-code and schema parity checks in intake command/rules updates |

### Decision linkage

- Research basis: `R-0045` (with `R-0041` supporting baseline intake patterns).
- Decision: `DEC-0050`.
- Boundary note: `US-0068` governs intake coverage enforcement only; runtime/test/release
  contracts remain `US-0065`/`US-0066`/`US-0067`.

---

## US-0069 Architecture: Strict phase role enforcement for `/auto`

### Scope and constraints

- Story: `US-0069`
- Scope: `/auto` orchestration — canonical phase→role mapping, preflight
  capability resolution, boundary evidence validation, diagnostics, and
  alignment with strict runtime proof (`DEC-0038`).
- In-scope:
  - deterministic matrix for all canonical `/auto` phase IDs,
  - scratchpad policy keys for allowed alternates (`research`, `plan-verify`,
    `refresh-context`),
  - preflight gate before phase spawn (no silent unrelated-role fallback),
  - checkpoint rejection when isolation `role` conflicts with expected contract,
  - strict-proof `role` / `proof_hash` consistency with resolved canonical role,
  - default deny for `execute` outside `dev` except documented override path,
  - resume / `start-from` parity with preflight re-evaluation.
- Out-of-scope:
  - configurable phase include/exclude profiles (`US-0070`),
  - product/runtime semantics of generated application code.

### Architecture model

1. **Single-valued expected role per boundary**  
   For each transition, `/auto` computes one expected `role` from the canonical
   matrix plus alternate policy (see `DEC-0051`). That value drives:
   - which subagent capability must be available preflight,
   - what isolation evidence must record,
   - what strict-proof tuple must attest.

2. **Preflight admission**  
   Treat role resolution like fail-closed admission: if the required capability
   cannot be satisfied, emit `PHASE_ROLE_CAPABILITY_MISSING` with
   `phase_id`, expected role, observed result, and remediation — do not spawn
   phase work under a substitute role.

3. **Post-completion validation**  
   When a phase completes, validate isolation evidence `role` against the same
   expected role computed preflight. Mismatch → `PHASE_ROLE_MISMATCH` and no
   forward progress.

4. **Strict-proof linkage**  
   The `DEC-0038` tuple’s `role` must match isolation `role` (both equal to the
   resolved canonical role). `proof_hash` remains SHA-256 over sorted-key JSON of
   the tuple fields (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`,
   `role`, `proof_issued_at`, `proof_ttl_seconds`).

5. **Execute default deny**  
   `execute` expects `dev`. Non-`dev` requires `AUTO_EXECUTE_ROLE_OVERRIDE` plus
   `execute_override_governance_ref` per `DEC-0051` (rare, audited).

6. **Continuation parity**  
   Every `/auto` invocation (including resume) recomputes policy and
   capability; stale `resume_brief` cannot bypass the gate.

### Operator and documentation surfaces

- `/auto` command text, related agent/command docs, runbook, README, and
  scratchpad examples must document the matrix, policy keys, reason codes, and
  override contract for active + template parity (implementation tranche).

### Regression and QA implications (planning hook)

- Pass path: capability available, correct role, aligned isolation + proof.
- Fail path: missing capability → `PHASE_ROLE_CAPABILITY_MISSING`.
- Evidence path: wrong `role` in checkpoint → `PHASE_ROLE_MISMATCH`.
- No silent fallback: assert orchestrator stops rather than substituting roles.
- Reason-code vocabulary stable and documented (AC-9).

### Decision linkage

- Research basis: `R-0048`
- Decision: `DEC-0051`
- Boundary note: phase-selection configuration remains `US-0070`; this story does
  not define skip/include profiles.

---

## US-0070 Architecture: Configurable `/auto` phase selection policy

### Scope and constraints

- Story: `US-0070`
- Scope: scratchpad-driven **resolved phase plan** for `/auto` (subset of the
  canonical lifecycle in order), interaction with `start-from`, continuation
  modes (resume, backlog-drain, bulk execute, team scope), and operator-visible
  diagnostics — **without** silent safety bypass or role substitution.
- In-scope:
  - single active policy mode (`AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`,
    `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE`) with fail-closed conflict
    handling,
  - deterministic expansion → non-skippable reinstatement (default profile) →
    `start-from` intersection,
  - breadcrumb contract for selected/skipped phases and reason codes,
  - explicit compatibility with `DEC-0051` / `US-0069` (roles apply only to
    planned phases; no alternate-role fallback when a phase is omitted).
- Out-of-scope:
  - concrete `/auto` implementation and automated tests (execute/QA tranche),
  - changing per-phase internal work semantics inside a retained phase.

### Architecture model

1. **Plan as first-class input to orchestration**  
   Before any phase spawn, materialize an ordered list of canonical `phase_id`
   values. Treat this list as the only schedule `/auto` may execute for that run
   (subject to stop conditions, loops, and security-review inserts per existing
   command contract).

2. **Policy modes (exactly one)**  
   Follow `DEC-0052`: default `full`; otherwise `exclude`, `include`, or
   `profile` with deterministic validation and `PHASE_POLICY_CONFLICT` (or
   equivalent) when multiple selectors compete.

3. **Non-skippable reinstatement (default)**  
   After computing the candidate list, reinsert members of the **default
   non-skippable set** that were removed:
   - minimum **safety gates**: `qa`, `verify-work`, `release`,
   - plus any phase required so that every **later planned phase** still has a
     valid chain of isolation + strict-proof evidence for the same story/run
     under `DEC-0029` / `DEC-0038` (do not assert downstream gates passed
     without their checkpoints).  
   Record each reinstatement in breadcrumbs with reason `non_skippable_gate` (or
   more specific documented codes).

4. **`start-from` intersection**  
   When `start-from=<phase>` is present, drop planned phases strictly before the
   anchor, then require a non-empty remainder; else fail closed with resolved
   plan vs requested anchor (backlog discovery contract).

5. **Continuation parity**  
   Reload merged scratchpad policy on every `/auto` entry (including resume);
   recompute the plan; never revive omitted phases without explicit breadcrumb
   explanation.

6. **Role and capability gates (`US-0069`)**  
   For each phase in the resolved plan, run the same preflight role resolution
   and capability admission as today (`DEC-0051`). Skipping a phase does **not**
   change the expected role of any other phase.

### Operator surfaces

- Scratchpad keys, mode precedence, non-skippable defaults, profile/ack
  requirements, and reason codes must appear in `/auto` command text,
  scratchpad examples, runbook, and README with active/template parity
  (`US-0070` AC-8).

### Regression and QA implications (planning hook)

- Default path: full plan unchanged vs pre-`US-0070` behavior.
- Selective path: exclude `research` and/or `sprint-plan` still reinstate safety
  gates and preserves evidence chain.
- Fail paths: unknown phase id, empty include, policy conflict, bad profile,
  `start-from` empty intersection — each deterministic code, no partial spawn.
- Resume path: policy bytes stable across interruption; plan reproducible.

### Decision linkage

- Research basis: `R-0049`
- Decision: `DEC-0052`
- Boundary note: role enforcement remains `DEC-0051` / `US-0069`; this story adds
  **which phases are scheduled**, not **who may run** them.

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

# US-0073: Scratchpad delivery simplification (example-only install policy)

## Overview

`US-0073` selects **Model B** from `R-0050`: installers ship **framework-owned**
`.cursor/scratchpad.local.example.md` as the primary default catalog; an
**effective baseline** is established only through **explicit materialization**
(or legacy committed `.cursor/scratchpad.md` on upgrade). The goal is simpler
delivery without weakening deterministic automation, upgrade parity, or
ownership rules already fixed in `DEC-0039`.

## Merge and safety model

### 1) Canonical precedence (merged key/value resolution)

Apply **after** loading each participating file:

1. `.cursor/scratchpad.local.md` (user-owned, never installer-overwritten).
2. `.cursor/scratchpad.md` **or** materialized baseline bytes (stable /
   auditable equivalent to historical committed baseline).
3. `.cursor/scratchpad.local.example.md` (framework-owned defaults; refreshed on
   upgrade per `DEC-0039`).

### 2) Fail-closed missing keys

If a **required** automation key is absent or invalid after merge, stop with
diagnostics that name which layers were consulted and how to remediate — **no**
silent inference (`AC-2`, `AC-4`).

### 3) Upgrade / legacy

- Preserve user local; refresh example only (`DEC-0039`).
- Repos with existing committed `scratchpad.md` keep deterministic behavior;
  migration paths that remove or replace baseline must be **explicitly**
  documented and test-covered.

### 4) Parity

Same policy across `installer.ps1`, `installer.sh`, `installer.py`, CLI, and
`template/` (`AC-6`, `AC-8`).

### 5) Regression focus

Fresh install, upgrade from legacy dual-file layout, missing baseline /
materialization, and local-only override; each maps to deterministic outcomes
(`AC-9`, `AC-10`).

## Decision linkage

- Research basis: `R-0050`
- Decision: `DEC-0055`

---

# US-0074: Baseline version-sync and TEST_COMMAND bootstrap

## Overview

`US-0074` closes persistent baseline failures in `tests/run-tests.ps1` /
`tests/run-tests.sh`: Homebrew stable formula alignment with npm, and installer
/ CLI bootstrap of `TEST_COMMAND` in materialized `docs/engineering/runbook.md`.
The design pins **one canonical version source** and **one bootstrap outcome
contract** so execute/QA can restore a fully green baseline without scope creep.

## Version sync model

### Canonical source

- **`package.json` `version`** is authoritative for semantic version and for the
  GitHub tag segment `v{version}` used in the Homebrew `url`.

### Homebrew stable formula rules

- Committed `packaging/homebrew/its-magic.rb` must satisfy, on every release that
  bumps npm:
  - `url` contains `.../refs/tags/v{package.json.version}.tar.gz`
  - Ruby `version "{package.json.version}"`
  - `sha256` matches the tarball for that tag
- Release scripts are the default enforcement path so formula and npm cannot
  diverge casually.

## TEST_COMMAND bootstrap model

### Surfaces and precedence

- Installers and CLI entrypoints materialize runbook commands per **`DEC-0046`**
  (user override wins; then stack detection; fail-fast diagnostics when
  unresolved).
- Baseline asserts require the **resolved** `TEST_COMMAND` after bootstrap to be
  **only** `npm run test` **or** `sh tests/run-tests.sh` for the detectable-stack
  scenarios under test (see **`R-0051`** post-discovery notes for detector/path
  pitfalls).

### Parity

- **`DEC-0056`** requires identical logical outcomes across
  `installer.ps1`, `installer.sh`, `installer.py`, and `bin/its-magic.js`
  delegation, with active + `template/` parity.

### PowerShell runner

- Emitting `tests/run-tests.ps1` as the bootstrap `TEST_COMMAND` is **out of
  scope** for the current baseline contract; widening requires an explicit future
  decision and test updates (`R-0051`).

## Verification

- Story acceptance re-runs consolidated tests and QA evidence so all four
  formerly failing checks pass without assert weakening (`US-0074` `AC-6`,
  `AC-7`, `AC-9`).
- Regression guidance lives in **`DEC-0056`** and this section for future drift.

## Decision linkage

- Research basis: **`R-0051`**
- Decision: **`DEC-0056`**

---

# US-0075: Upgrade scratchpad example–first refresh and paired catalog parity

## Overview

`US-0075` closes **example drift** and **paired-surface skew**: upgrade/install must refresh
**`.cursor/scratchpad.local.example.md`** from the shipped template **before or together with**
any step that advances materialized **`.cursor/scratchpad.md`**, so operators always see a
current **copy-from** catalog. **`AC-11`** adds **deterministic parity** between each
**baseline ↔ example** pair (active repo and `template/`) on **`##` sections** and **`KEY=`**
lines, with values allowed to differ only for documented conservative defaults.

## Ordering model

1. **Template catalog authority** — Framework vocabulary ships in
   **`template/.cursor/scratchpad.local.example.md`** (and is mirrored to active example on
   upgrade/install per pipeline design).
2. **No stale example + fresh baseline** — Any refresh of materialized **`scratchpad.md`**
   from **`template/.cursor/scratchpad.md`** is preceded by or bundled with example refresh
   from **`template/.cursor/scratchpad.local.example.md`** (**`DEC-0057`** §1).
3. **Parity surfaces** — Same ordering and diagnostics across installers, CLI, manifest, and
   `template/` (**`DEC-0057`**, **`US-0075`** **`AC-4`**, **`AC-8`**).

## Merge and ownership (unchanged)

- Precedence and layers remain **`DEC-0055`** (local → materialized baseline → example).
- User **`.cursor/scratchpad.local.md`** is never overwritten by framework refresh (**`DEC-0039`**).

## AC-11 parity gate

- Compare **paired** paths only: active **`.cursor/scratchpad.md`** ↔
  **`.cursor/scratchpad.local.example.md`** and **`template/.cursor/scratchpad.md`** ↔
  **`template/.cursor/scratchpad.local.example.md`**.
- Require **set equality** of **`##` section headers** and **`KEY=`** keys; manifest-documented
  local-only exceptions are the only allowed asymmetry (**`R-0052`** design).
- Enforce in **`tests/run-tests.*`** (or equivalent CI hook), not review-only.

## Diagnostics

- Distinguish **example** vs **materialized baseline** vs **user local** actions with
  deterministic reason families (**`DEC-0039`** alignment, **`US-0075`** **`AC-5`**).

## Verification

- Regression tests for outdated example + current template, post-upgrade example bytes, and
  absence of “baseline moved / example older than template” paths (**`US-0075`** **`AC-6`**,
  **`AC-9`**).

## Decision linkage

- Research basis: **`R-0052`**
- Decision: **`DEC-0057`**

---

# US-0076: Executable scratchpad-driven sync and auto-push wiring

## Overview

**`US-0076`** wires **merged scratchpad** (**`DEC-0055`**) into **`scripts/validate-and-push.ps1`**
and **`scripts/validate-and-push.sh`** so **`SYNC_POLICY_MODE`**, **`ALLOW_AUTO_PUSH`**,
**`SYNC_CUSTOM_PHASES`** (when applicable), and **`AUTO_PUSH_BRANCH_ALLOWLIST`** **actually**
gate an **opt-in** push path, while **`DEC-0018` / `US-0038`** remain the semantic authority
for **reason codes** and **gate order** (**`decisions/DEC-0058.md`** records the executable
contract).

## Approach

1. **Reuse merge** — Invoke **`installer.py`** `parse_scratchpad_file` + `merge_scratchpad_layers`
   (or a tiny extracted shared module) from both scripts so **local → baseline → example**
   precedence cannot drift from **`DEC-0055`**.
2. **Extend validate-and-push only** — Keep a **single** operator entrypoint (**PO/discovery**
   recommendation); avoid a parallel **`sync-from-scratchpad.*`** unless security review forces
   a split (not indicated).
3. **Policy evaluation before git** — After merge, evaluate **disabled / manual / eligibility**
   per **`DEC-0018`**; exit with **`SYNC_DISABLED`**, **`MANUAL_MODE_NO_AUTO`**,
   **`AUTO_PUSH_NOT_ENABLED`**, or **`SYNC_TRIGGER_NOT_ELIGIBLE`** without running tests when
   push is already ruled out (deterministic short-circuit order documented in runbook).
4. **Runbook commands unchanged in role** — Continue reading **`TEST_COMMAND`** and optional
   checks from **`docs/engineering/runbook.md`** only.
5. **QA scan** — Bounded file glob + marker rules per **`DEC-0058`** §6 (not free-form chat
   parsing).
6. **Optional dry-run** — Flag to print decisions and reason codes without **`git push`**.

## Invariants

- **No push** when **`ALLOW_AUTO_PUSH=0`** or mode is **`disabled`** / **`manual`** (**`AC-1`**).
- **No push** on merge/parse failure; **no silent push** on allowlist mismatch (**`AC-4`**).
- **Tests before push** when push is eligible: **`TEST_COMMAND`** required; optional checks
  when configured (**`AC-3`**).
- **Cross-platform parity** — PS1 and sh exit codes and reason tokens match (**`AC-6`**).
- **Operator strings** — **`US-0071`** hygiene on all new/changed script output (**`AC-9`**).

## Components / scripts touched (execute phase)

| Surface | Change |
|--------|--------|
| **`scripts/validate-and-push.ps1`** | Merged scratchpad gate + QA scan + branch allowlist + dry-run |
| **`scripts/validate-and-push.sh`** | Same behavior as PS1 |
| **`installer.py`** (or **`scripts/`** helper) | Callable merge entry (avoid duplicating precedence) |
| **`docs/engineering/runbook.md`** | Document invocation contract, **`SYNC_PHASE_BOUNDARY`**, scan rules |
| **`README.md`** + **`template/`** mirrors | **`AC-7`** operator guidance |
| **`tests/run-tests.ps1`** / **`.sh`** | **`AC-8`** regression fixtures / dry-run assertions |
| **`decisions/DEC-0058.md`** | Executable supplement to **`DEC-0018`** (accepted with architecture) |

## Failure reason codes (non-exhaustive; align with **`US-0038`**)

| Code | When |
|------|------|
| **`SYNC_DISABLED`** | Mode **`disabled`** |
| **`MANUAL_MODE_NO_AUTO`** | Mode **`manual`** or unset invalid treated as manual per policy |
| **`AUTO_PUSH_NOT_ENABLED`** | **`ALLOW_AUTO_PUSH≠1`** |
| **`SYNC_TRIGGER_NOT_ELIGIBLE`** | Boundary/mode mismatch (e.g. **`by_phase`** invocation not eligible per script rules) |
| **`TEST_COMMAND_MISSING`** / **`TEST_FAILED`** / **`TEST_TIMEOUT`** | Runbook test gate |
| **`OPTIONAL_CHECK_FAILED`** | Lint/typecheck when configured |
| **`BRANCH_NOT_ALLOWLISTED`** | Branch pattern fails deterministic allowlist match |
| **`BLOCKING_QA_FINDINGS`** | **`DEC-0058`** §6 scan hit |
| **`PRE_QA_AUTOPUSH_FORBIDDEN`** | **`US-0038`** QA-first signal not met (bounded rule in runbook) |
| **`[SCRATCHPAD_MERGE_ERROR]`** (family) | Merge/parse failure — **no push** |

## Tests strategy (**`AC-8`**)

- **Fixture or temp repo** paths: disabled/manual → no push path; allowlist mismatch →
  **`BRANCH_NOT_ALLOWLISTED`**; merged local override wins over baseline (**`DEC-0055`** spot
  check); **qa-findings** fixture with blocking marker → **`BLOCKING_QA_FINDINGS`**.
- **Dry-run** assertions: happy path reports **`SYNC_PUSHED`** or documented success token
  without invoking **`git push`** when tests are mocked/skipped in CI-safe mode.
- **PS1 / sh** both run the same cases where feasible.

## Migration / compatibility

- **Default-off unchanged**: teams with **`ALLOW_AUTO_PUSH=0`** or **`manual`/`disabled`** see
  **no new push behavior** — scripts may exit earlier with explicit reason codes (**`AC-1`**).
- **No Cursor auto-invocation** added by this story; CI/operator must **run** the script
  (**backlog boundaries**).
- **`DEC-0018`** records remain valid; **`DEC-0058`** **adds** executable interpretation — no
  weakening of **`US-0038`** gates.

## Decision linkage

- Research basis: **`R-0053`**
- Decision: **`DEC-0058`** (executable wiring; **`DEC-0018`** policy authority retained)

---

# US-0077: Documentation audience profiles and dual README strategy

## Overview

**`US-0077`** adds **merged-scratchpad** (**`DEC-0055`**) controls **`DOC_AUDIENCE_PROFILE`**
and **`DOC_DETAIL_LEVEL`** so documentation generation and validation produce deterministic,
audience-appropriate output. **`R-0054`** supplies the **9-cell** semantic-key matrix;
**`DEC-0059`** locks paths, split rules, reason codes, validator location, and migration
defaults.

## Profile semantics

- **Dimensions**: `DOC_AUDIENCE_PROFILE` ∈ {`user`, `developer`, `both`} ×
  `DOC_DETAIL_LEVEL` ∈ {`concise`, `balanced`, `technical-deep`}.
- **Inputs**: **merged** scratchpad only (local → materialized baseline → example); invalid
  combination values → **`DOC_PROFILE_INVALID`**; merge failure → **`DOC_PROFILE_MERGE_ERROR`**.
- **Optional modes**: `SPEC_PACK_MODE` / `USER_GUIDE_MODE` are **additive** only — validators
  must not require their artifacts when **0** (**`R-0054`** §6).
- **Required keys per cell**: same **semantic key** sets as **`R-0054`** matrix (USER_* and
  DEV_* vocabulary); architecture adds **normative H2 literals** below for resolver binding.

## Artifact ownership

| Artifact | Role |
|----------|------|
| **`README.md`** (repo root) | **User channel** — all **`USER_*`** keys required for the resolved cell when profile audience includes **`user`**. |
| **`docs/developer/README.md`** | **Developer channel** — all **`DEV_*`** keys required when audience includes **`developer`** or **`both`**. |
| **`docs/engineering/runbook.md`** | **US-0030** command surface — unchanged; README may link into runbook; no profile-driven rewriting of runbook keys in this story. |
| **`docs/user-guides/US-xxxx.md`** | **US-0032** when enabled. |
| Spec-pack paths | **US-0031** when enabled. |

Cross-links from README to developer shard or runbook are allowed; **authoritative** section
bodies for **`DEV_*`** keys must not live in root README when the cell requires the developer
shard (**`DEC-0059`** §3).

## README split strategy

- **Canonical layout**: **two files** — root **`README.md`** + **`docs/developer/README.md`**.
- **`both` × `concise` / `balanced` / `technical-deep`**: user vs developer keys **split** per
  **`R-0054`**; **`technical-deep`** forbids inlining full **`DEV_*`** bodies in root (pointers
  only).
- **`developer` × \***: **`DEV_*`** content **only** in developer shard; root may include one
  minimal pointer section.
- **H2 budgets** (root README, user-facing body): follow **`R-0054`** table; overflow →
  **`DOC_SECTION_BUDGET_EXCEEDED`**.

## Semantic keys → canonical H2 titles (validator)

Exact heading text (Markdown `## …`) — execute phase implements resolver with trim/normalize
only; renames require updating this table and tests together.

**User channel (`README.md`)**

| Key | H2 title |
|-----|----------|
| `USER_PURPOSE` | `Purpose` |
| `USER_QUICKSTART` | `Quickstart` |
| `USER_EXAMPLES` | `Examples` |
| `USER_TROUBLESHOOTING` | `Troubleshooting` |
| `USER_LIMITATIONS` | `Limitations` |
| `USER_RELATED_DOCS` | `Related documentation` |

**Developer channel (`docs/developer/README.md`)**

| Key | H2 title |
|-----|----------|
| `DEV_PREREQS` | `Prerequisites` |
| `DEV_WORKFLOW` | `Workflow` |
| `DEV_QUALITY_GATES` | `Quality gates` |
| `DEV_ARCHITECTURE` | `Architecture notes` |
| `DEV_CONTRACTS` | `Contracts and interfaces` |
| `DEV_DECISIONS` | `Engineering decisions` |

Optional root pointer for developer-audience navigation (not a semantic-key substitute):
`## Contributing` with a single link line to **`docs/developer/README.md`** — does not count
toward **`DEV_*`** satisfaction.

## Validator and test strategy

1. **Script**: **`scripts/validate_doc_profile.py`** — loads merged scratchpad via
   **`installer.py`** merge (**`DEC-0058`** pattern); resolves cell; checks parse gates,
   completeness (**`DOC_SECTION_MISSING:<key>`**), H2 counts (**`DOC_SECTION_BUDGET_EXCEEDED`**),
   and **active + `template/`** mirror paths for the same logical files (**`DOC_TEMPLATE_PARITY_FAIL`**).
2. **Tests**: **`tests/run-tests.ps1`** / **`.sh`** invoke Tier **A/B/C** fixtures per **`R-0054`**
   (**`AC-8`**): three anchor snapshots, table-driven remaining cells, wiring smoke per
   audience at **`balanced`** depth.
3. **CI cost**: full 9× heavy generation is **not** required every run — resolver + fixture
   trees prove matrix coverage.
4. **US-0071**: validator and generator stdout/stderr use reason codes; markdown bodies on
   scanned surfaces stay within metadata guard allowlists (**extend** in execute if new tools
   emit planning tokens).

## Migration constraints

- **Defaults**: template/example scratchpad documents **`both`** + **`balanced`** as the
  framework recommendation; **absent keys** on merged scratchpad follow **`DEC-0059`** §6
  transition rule (treat as **`both`×`balanced`** for resolver until CI mandates explicit
  keys).
- **Repos without `docs/developer/README.md`**: must add it before claiming **`developer`** or
  **`both`** cells in validation; no silent split — generator/docs updates are **non-destructive**
  (relocate content deliberately, do not drop).
- **Installer/template**: when the framework ships the developer shard, update
  **`docs/engineering/context/installer-owned-paths.manifest`** (and **`template/`** mirror)
  per **`US-0030`** parity.

## Decision linkage

- Research basis: **`R-0054`**
- Decision: **`DEC-0059`**

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

# US-0082: Agent-driven codebase map bootstrap

## Overview

**`US-0082`** ensures fresh repos can rely on `docs/engineering/codebase-map.md` through deterministic workflow ownership, while preserving **`/map-codebase`** as an explicit manual command. **`R-0060`** frames vendor practice (rules/docs as primary context) vs repo-owned map artifacts; **`DEC-0065`** locks lifecycle gates, idempotency, ownership, diagnostics, and parity expectations.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Guidance-only | Runbook reminders, no lifecycle hook | Rejected — misses **AC-1** for unattended bootstrap. |
| B - Generate on every `/auto` phase | Maximum automation | Rejected — churn / **`state.md`** noise (**R-0060**). |
| C - CI-only | Fail pipeline without map | Rejected as sole owner — late signal; still needs **AC-1** lifecycle naming. |
| D - Phase-gated + manual (chosen) | **`/architecture`** primary; optional **`/refresh-context`**; **`/map-codebase`** manual | **Chosen** — minimal automation that meets ACs and respects **DEC-0052**. |

## Deterministic approach

1. **Primary lifecycle point**: **`/architecture`** completion (**tech-lead**) — ensure map exists or deterministic block/skip with diagnostics before **`/sprint-plan`** handoff (sprint implements invocation: command wrapper, script, or documented mandatory step).
2. **Secondary (policy-gated)**: **`/refresh-context`** may re-materialize or verify map when scratchpad/profile explicitly enables refresh (default off to limit churn).
3. **Manual path**: **`/map-codebase`** unchanged for explicit operator runs (**AC-2**).
4. **Idempotency**: Stable ordering; avoid no-op file churn (**AC-3**).
5. **Ownership**: Same write surfaces as **`/map-codebase`**; **`state.md`** append-only discipline preserved (**AC-4**).
6. **Diagnostics**: **`CODEBASE_MAP_*`** reason family + remediation (**AC-5**).
7. **Guidance**: Runbook + **`/ask`** name responsibility locus (**AC-6**).
8. **Verification**: Active/template parity + fresh / rerun / failure-path tests (**AC-7**, **AC-8**).
9. **Compatibility**: Non-destructive treatment of existing maps (**AC-9**).
10. **Traceability**: **`BUG-0002`** closed as mismatch; this story owns implementation (**AC-10**).

## Fail codes (deterministic vocabulary)

- **`CODEBASE_MAP_MISSING`** — expected artifact absent at lifecycle checkpoint.
- **`CODEBASE_MAP_BLOCKED:<subreason>`** — generation blocked (permissions, policy, profile skip); subreason bounded in sprint.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Custom phase plans skip architecture | Diagnostics + optional CI guard (**DEC-0065** §9). |
| Overwriting local map customizations | Idempotent merge / section-stable refresh; destructive modes out of scope unless explicit. |
| Active/template drift | Parity manifest or existing test patterns for commands/rules (**AC-7**). |

## Decision linkage

- Research basis: **`R-0060`**
- Decision: **`DEC-0065`**
- Related: **`US-0001`** (command exists), **`BUG-0002`** (closed), **`DEC-0052`** (phase profiles)

---

# BUG-0003: Deterministic installer completeness in `missing`/`upgrade`

## Overview

**`BUG-0003`** closes a mode-specific installer trust gap where framework scripts may remain absent after `missing` and `upgrade` runs. **`R-0061`** confirms branch logic parity across `installer.ps1`, `installer.sh`, and `installer.py`; root cause is required-inventory omission (`scripts/enforce-triad-hot-surface.py`) from `docs/engineering/context/installer-owned-paths.manifest`. **`DEC-0066`** locks the minimal fix: manifest-authoritative required script inventory plus deterministic post-install completeness checks and parity tests.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Keep current flow + operator reminders | No structural change | Rejected - allows silent incompleteness recurrence. |
| B - Hard-code required scripts in PS1/SH/PY | Explicit lists per installer | Rejected - highest maintenance and parity drift risk. |
| C - Manifest as single source + shared completeness validator (chosen) | Minimal, deterministic, testable | **Chosen** - simplest path that satisfies bug acceptance and parity constraints. |

## Deterministic approach

1. **Single required inventory source**: `docs/engineering/context/installer-owned-paths.manifest` owns required framework script paths for install completeness checks.
2. **Required path inclusion**: ensure `scripts/enforce-triad-hot-surface.py` is included in installer-owned install scope with paired clean ownership policy.
3. **Post-install invariant**: after mode-specific copy/classification logic, validate all required script paths exist; fail closed on missing entries.
4. **Stable diagnostics**: emit deterministic reason codes (`INSTALL_COMPLETENESS_FAILED`, `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`) with remediation pointing to manifest parity/update path.
5. **Parity-safe implementation**: prefer shared completeness logic in `installer.py` with wrappers (`installer.ps1`, `installer.sh`) consuming the same contract.
6. **Status authority preserved**: `BUG-0003` remains **OPEN** in `docs/product/backlog.md` until execute/qa/verify-work/release close-out (**US-0045**).

## Verification strategy

- **Positive matrix**: `missing` and `upgrade` both produce complete required script set after install.
- **Negative matrix**: intentionally remove required script from staged source and assert deterministic fail code.
- **Parity matrix**: active + `template/` installer surfaces and manifest remain aligned.
- **Symmetry matrix**: install include and clean path ownership stay paired for required scripts.
- **Regression entrypoints**: extend installer-focused tests and lifecycle smoke checks referenced by sprint tasks.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Future manifest omissions reintroduce silent misses | Required inventory checks + regression fixtures tied to manifest updates. |
| Divergent wrapper behavior across platforms | Shared Python validation contract and wrapper reuse. |
| Over-blocking custom repos | Limit completeness gate to installer-owned framework paths. |
| Install/clean mismatch | Explicit paired review and test coverage for `install_include_paths` + `clean_paths`. |

## Decision linkage

- Research basis: **`R-0061`**
- Decision: **`DEC-0066`**
- Related: **`BUG-0001`**, **`US-0018`**, **`US-0045`**, **`DEC-0038`**

---

# BUG-0004: POSIX-safe installer shell startup for Unix CLI path

## Overview

**`BUG-0004`** addresses startup failure in Linux shell environments where installer execution aborts with `set: Illegal option -`. Research **`R-0063`** confirms Unix CLI flow (`bin/its-magic.js`) executes installer via `sh installer.sh`, so installer startup must remain POSIX-`sh` compatible and avoid bash-only `set` semantics. **`DEC-0068`** is normative for invocation/compatibility boundaries and regression requirements.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Force bash invocation in CLI | `bash installer.sh` on Unix | Rejected - adds dependency and weakens portability. |
| B - Dynamic shell detection and launcher branching | choose shell at runtime | Rejected - more complexity than needed for defect scope. |
| C - Keep `sh` contract and enforce POSIX-safe startup (chosen) | minimal and deterministic | **Chosen** - preserves current CLI behavior and fixes failure root. |

## Deterministic approach

1. **Unix launcher contract unchanged**: keep `bin/its-magic.js` Unix execution path via `spawnSync("sh", ...)`.
2. **Startup option safety**: `installer.sh` startup path must use POSIX-safe `set` options only (`set -e` baseline); no unconditional bash-only flags.
3. **Failure prevention**: startup must not fail on `/bin/sh` variants due to option incompatibility.
4. **Status authority preserved**: `BUG-0004` remains **OPEN** in `docs/product/backlog.md` until sprint delivery closes verification/release chain (**US-0045**).

## Verification strategy

- **Direct `sh` matrix**:
  - `sh installer.sh --target <tmp> --mode missing --create`
  - `sh installer.sh --target <tmp> --mode upgrade`
- **CLI Unix matrix**:
  - `node bin/its-magic.js --target <tmp> --mode missing --create`
- **Non-regression matrix**:
  - install completeness checks and existing manifest-governed behavior remain intact.
- **Parity matrix**:
  - retain consistent installer behavior expectations across wrapper paths and test harness coverage.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Bash-only options reintroduced later | Keep explicit `sh`-path regression coverage in shared tests. |
| Local shell mismatch hides regressions | Verify both direct `sh` and CLI invocation paths in deterministic tests. |
| Scope drift into unrelated resume bugs | Keep this architecture bounded to shell startup compatibility (`BUG-0005` tracked separately). |

## Decision linkage

- Research basis: **`R-0063`**
- Decision: **`DEC-0068`**
- Related: **`BUG-0005`**, **`US-0008`**, **`US-0018`**, **`US-0045`**

---

# BUG-0005: `resume_brief` refresh at bug-intake boundary for `/auto` resume

## Overview

**`BUG-0005`** addresses **`RESUME_BRIEF_STALE`** on **`/auto`** immediately after canonical **`/intake bug`** persistence: the resume brief can still describe a pre-intake cycle (for example **`intake`**) while the backlog already reflects a new OPEN bug. Deterministic **`/auto`** precedence (**`start-from`** → parseable **`resume_brief`** → **`state.md`**) intentionally **does not** silently ignore a present-but-stale brief. **`R-0064`** and **`DEC-0069`** lock the fix as **intake-time refresh** of **`handoffs/resume_brief.md`** so normal **`/intake bug` → `/auto`** does not false-trigger stale-resume, without weakening fail-fast.

## Contracts (normative)

1. **Intake completion obligation**: On successful bug intake persistence (**`US-0045`**), the intake writer **must** refresh **`handoffs/resume_brief.md`** with **`bug_id`**, **`intended_resume_phase=discovery`** (default OPEN-bug continuation), boundary **`orchestrator_run_id`** / timestamp when known, and intake evidence pointer when present.
2. **Precedence unchanged**: Explicit **`start-from`** overrides; parseable brief is evaluated before **`state.md`**; stale/unparseable/ambiguous briefs **fail fast** (**`RESUME_BRIEF_STALE`**, etc.) — no silent fallback when a stale brief is present.
3. **Backlog authority**: Brief content **must not** contradict **`docs/product/backlog.md`** status facts for the referenced **`bug_id`**.
4. **Optional self-heal**: Orchestrator-side reconciliation is **not** normative for **`BUG-0005`**; any future self-heal requires strict predicates, idempotency, **`state.md` audit**, and a separate decision (**`DEC-0069`** §4).

## Affected artifacts

- **`handoffs/resume_brief.md`** — primary handoff surface refreshed at intake boundary.
- **`docs/engineering/state.md`** — phase breadcrumbs and auto continuation checkpoints remain authoritative for history; they do not replace a parseable brief in precedence order.
- **`.cursor/commands/intake.md`** (and **`template/`** parity) — normative command surface for implementing intake-time refresh.
- **`docs/engineering/auto-orchestration-reference.md`** / **`.cursor/commands/auto.md`** — precedence and fail-fast codes remain source of truth; **`DEC-0069`** adds intake-side obligation only.

## Acceptance / architecture alignment

- Satisfies **`BUG-0005`** expected behavior: after intake, **`/auto`** resolves a valid next phase without requiring manual **`start-from`** for the normal path.
- Preserves **`US-0045`** canonical status and **`US-0070` / `DEC-0052`** phase-plan materialization (default next phase after bug intake is **`discovery`** unless product documents an exception).
- Regression matrix: **`R-0064`** table (**five scenarios**) is minimum QA/sprint coverage.

## Decision linkage

- Research basis: **`R-0064`**
- Decision: **`DEC-0069`**
- Related: **`US-0037`**, **`US-0045`**, **`US-0070`**, **`US-0080`**, **`DEC-0038`** (strict-proof continuity on phase boundaries)

---

# US-0083: Explicit delegable intake topics without weakening fail-closed semantics

## Overview

**`US-0083`** adds a bounded, auditable delegation path for unresolved required intake topics so users can explicitly delegate a decision and continue, while preserving the existing fail-closed gate for non-delegated gaps. **`R-0062`** recommends the smallest viable extension: keep the current `topic_coverage` contract and add a third `satisfied_by` branch with strict evidence requirements. **`DEC-0067`** is normative for schema, validator branching, reason codes, and parity scope.

## Assumption challenge and alternatives

| Option | Summary | Verdict |
|--------|---------|---------|
| A - Keep current strict-only gate | No delegation branch | Rejected - preserves safety but fails AC-2/AC-3 user intent. |
| B - Global delegation toggle for all missing topics | One switch to bypass missing required topics | Rejected - too broad, increases implicit bypass risk. |
| C - Topic-scoped delegation branch in existing rows (chosen) | Minimal schema extension with explicit evidence per topic | **Chosen** - simplest path that preserves deterministic fail-closed semantics. |

## Deterministic approach

1. **Topic-row contract extension**: allow `topic_coverage[].satisfied_by=delegation_ref` in addition to existing `answer_ref` and `assumption_confirmation_ref`.
2. **Required delegation fields**: when `satisfied_by=delegation_ref`, require:
   - `delegation_scope` (bounded decision area),
   - `delegation_rationale` (why delegation is chosen),
   - `delegation_confidence` (`low|medium|high`).
3. **Evidence binding**: delegation rows must still carry a valid `ie:` `ref` and explicit `quoted_user_text`; hash verification remains deterministic and includes the delegated branch literal.
4. **Validator branch behavior**:
   - non-delegated unresolved required topic -> unchanged fail-closed path (`INTAKE_REQUIRED_TOPIC_MISSING`, optional `INTAKE_REQUIRED_PACK_INCOMPLETE`, umbrella `INTAKE_PERSISTENCE_BLOCKED`);
   - delegated topic with complete evidence -> passes as covered;
   - delegated topic with missing/malformed evidence -> fail closed with delegation-specific deterministic reason codes under `INTAKE_PERSISTENCE_BLOCKED`.
5. **Mode parity**: guided and low-touch intake use the same validation pipeline; delegation does not introduce mode-specific bypass behavior.
6. **Status authority unchanged**: canonical story status remains in `docs/product/backlog.md` (**`US-0045`**); `US-0083` stays `OPEN` through architecture.

## Fail codes (deterministic vocabulary)

- **`INTAKE_DELEGATION_EVIDENCE_MISSING`** - delegated topic is missing one or more required delegation fields.
- **`INTAKE_DELEGATION_EVIDENCE_INVALID`** - delegated topic has invalid field values or invalid/mismatched `ie:` evidence binding.
- **`INTAKE_PERSISTENCE_BLOCKED`** (umbrella) - retained for all blocked persistence outcomes.

## Verification strategy

- Delegated pass fixtures: required-topic rows with `delegation_ref` and complete evidence succeed.
- Non-delegated block fixtures: unresolved required topics without delegation remain blocked with existing codes.
- Delegated block fixtures: malformed/missing delegation fields fail with deterministic delegation codes.
- Parity fixtures: active + `template/` alignment for intake command/rules/validator surfaces.
- Mode parity fixtures: guided and low-touch produce the same validation outcome for equivalent evidence bundles.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Delegation becomes implicit bypass | Require explicit `delegation_ref` + `ie:`-bound user quote; no global toggle. |
| Schema drift across active/template | Include parity checks and mirrored fixtures in sprint scope. |
| Over-complex delegated metadata recreates intake friction | Keep metadata minimal (`scope`, `rationale`, `confidence`) only. |
| Downstream consumers treat delegated items as resolved facts | Preserve delegated marker and rationale in persisted evidence and handoffs. |

## Decision linkage

- Research basis: **`R-0062`**
- Decision: **`DEC-0067`**
- Related: **`US-0068`**, **`US-0078`**, **`US-0045`**, **`DEC-0050`**, **`DEC-0060`**

---

# BUG-0006: `/auto` spawn-only enforcement (orchestrator must not execute phase work)

## Overview

**`BUG-0006`** closes the gap between **process** `/auto` orchestration (US-0080) and operator behavior: the orchestrator role must **only** schedule materialization, spawn fresh **phase-role** subagents, and verify boundaries—it must **not** author phase deliverables or perform phase work in the same context. **`R-0065`** recommends doc-first enforcement plus static regression; this section locks literals, surfaces, and acceptance hooks.

## Locked reason-code vocabulary

| Code | Use | Remediation (operator-facing) |
|------|-----|-------------------------------|
| **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** | Attempted direct orchestrator execution of a lifecycle phase (or equivalent “run `architecture` / `execute` / … in orchestrator context”) instead of spawning the required subagent. | Stop; spawn a **fresh** subagent for the canonical **`phase_id`** and **role** per the phase→role matrix (**DEC-0051**); do not merge phase output into orchestrator turns. |
| **`PHASE_CONTEXT_ISOLATION_VIOLATION`** (existing) | Orchestrator wrote phase artifacts or violated per-phase isolation (**DEC-0029**). | Distinct from spawn failure: isolation applies **after** correct spawn boundary; keep both codes documented side-by-side. |
| **`RUNTIME_PROOF_*`**, **`PHASE_ROLE_*`**, **`PHASE_POLICY_*`** (existing) | Strict proof, capability, phase-plan failures (**DEC-0038**, **DEC-0052**). | Unchanged; **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** must not overload these families. |
| **`[AUTO_RESUME_ERROR]`** codes (existing) | Resume precedence / brief / state resolution. | Separate from spawn integrity; no merge of semantics. |

## Technical approach (doc-first, test-backed)

1. **Normative command (active + template)**: **`.cursor/commands/auto.md`** and **`template/.cursor/commands/auto.md`** — strengthen **non-negotiable** language: “spawn fresh subagent per phase,” “orchestrator must not execute phase work / write phase deliverables,” and enumerate **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** in the fail-fast / reason-code excerpt (alongside existing **`PHASE_CONTEXT_ISOLATION_*`** / **`RUNTIME_PROOF_*`** markers).
2. **Expanded reference**: **`docs/engineering/auto-orchestration-reference.md`** — mirror the spawn-only rule; cross-link **DEC-0029** (isolation) and **DEC-0038** (strict proof) so operators cannot satisfy one gate and ignore the other; document **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** with one-line remediation.
3. **Regression**: extend **`tests/auto_command_contract_test.py`** with required substrings: spawn-only phrasing, forbidden orchestrator phase execution, literal **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, and a **negative** check that the slim command does **not** imply in-orchestrator execution of named phases (pattern established in **`R-0065`** matrix rows 1–4).
4. **Out of scope**: no claim of runtime Cursor product enforcement; no replacement of isolation or proof tuples as subagent launchers.

## Files to touch (execute phase)

| Path | Change |
|------|--------|
| **`.cursor/commands/auto.md`** | Spawn-only + **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** + forbidden direct phase execution. |
| **`template/.cursor/commands/auto.md`** | Parity with active command (same literals where mirrored). |
| **`docs/engineering/auto-orchestration-reference.md`** | Expanded contract alignment + cross-links + reason code. |
| **`tests/auto_command_contract_test.py`** | Assertions for new literals and non-contradiction. |

Optional parity: if repo adds an **`auto`** template parity script later, include these paths; until then, **manual or sprint QA** verifies **`template/`** mirror.

## Acceptance hooks

- Contract test **`python tests/auto_command_contract_test.py`** (or full unittest suite per sprint) **PASS** after edits.
- **`BUG-0006`** **expected** in backlog: fail-fast when spawn boundary violated, with deterministic diagnostics — satisfied by documented **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`** plus existing isolation/proof codes.
- Canonical status remains **`docs/product/backlog.md`** only (**US-0045**); closure moves to **DONE** only after execute/QA/verify per backlog.

## Risks

| Risk | Mitigation |
|------|------------|
| Code overlaps **`PHASE_CONTEXT_ISOLATION_VIOLATION`** | Table above + remediation text distinguishes “no spawn” vs “wrong writer.” |
| Template drift | Edit **`template/.cursor/commands/auto.md`** in the same change set as active **`auto.md`**. |
| False sense of runtime enforcement | Docs + static tests only; reference states process contract, not IDE automation. |

## Decision linkage

- Research basis: **`R-0065`**
- Related: **`US-0048`**, **`US-0069`**, **`US-0080`**, **`US-0045`**, **`DEC-0029`**, **`DEC-0038`**, **`DEC-0051`**, **`DEC-0052`**

---

# BUG-0007: Intake evidence truthfulness for `asked_topics` / `topic_coverage`

## Overview

**`BUG-0007`** closes the gap where **`scripts/intake_evidence_validate.py`** can return **`[INTAKE_EVIDENCE_VALIDATION_OK]`** on bundles such as **`handoffs/intake_evidence/BUG-0007-intake-20260403.json`** that list a full **`small-intake-pack`** in **`asked_topics`** while every **`topic_coverage`** row uses **`satisfied_by=answer_ref`** with the **same** (or trivially duplicated) **`quoted_user_text`**—i.e. no real per-topic elicitation. **`R-0066`** shows **`validate_intake_evidence`** in **`scripts/intake_evidence_lib.py`** enforces structural pack coverage, **`ie:`** integrity, and **DEC-0060**-aligned bindings, but not semantic distinction of answers across topics. This section locks the minimal validator + contract + test matrix so the exemplar **fails** after implementation while **US-0083** delegation and **equivalent_evidence_ref** paths stay **PASS**.

## Assumption challenge and alternatives

| Option | Idea | Verdict |
|--------|------|---------|
| A | Documentation-only reminder in **`/intake`** | **Rejected** — validator already certifies the bad exemplar (**R-0066**). |
| B | External chat transcript ingestion | **Deferred** — out of repo scope unless product mandates it. |
| C | Deterministic lib rules + contract + fixtures (**chosen**) | **Chosen** — same validation pipeline for guided and low-touch; fail-closed subcodes under **`INTAKE_PERSISTENCE_BLOCKED`**. |

**Residual risk**: Duplicate-text heuristics alone do not prove a “question was asked”; optional future **`question_*`** fields or stronger artifacts may be needed. Document any grandfathering in sprint **`decisions.md`** if legacy bundles must migrate.

## Locked technical approach

### 1) Core validation (`scripts/intake_evidence_lib.py`)

Extend **`validate_intake_evidence`** (and shared helpers the lib owns) with deterministic rules applied **after** existing **`ie:`** / pack / delegation / assumption checks:

1. **Duplicate **`answer_ref`** prose across distinct required topics** — For **`small-intake-pack`** (and equivalent required-topic sets), when multiple rows share **`satisfied_by=answer_ref`** and **identical** **`quoted_user_text`** (normalized per existing string rules in the lib), **fail** unless the row is covered by an allowed alternate satisfaction path (**`equivalent_evidence_ref`** / **`evidence_source`** semantics already in lib, **`delegation_ref`** per **DEC-0067**, or **`assumption_confirmation_ref`**). This targets the BUG-0007 pattern without treating two accidental short duplicate answers as the same class of abuse (tune: require duplicate across **all** required keys or use minimum distinct-count threshold — implementation sprint chooses the smallest rule that makes the exemplar **FAIL** and keeps matrix row 2 **PASS**).
2. **Optional phase-2** — If product requires stronger audit: add optional **`question_prompt_ref`** / **`question_text`** (or bind to a stable prompt id) for **`answer_ref`** rows; then **`INTAKE_ASKED_TOPIC_NOT_EVIDENCED`** applies when **`asked_topics`** lists a key without a bound prompt artifact. **Architecture default for first sprint**: implement (1) first; gate (2) behind explicit backlog if false positives appear.

**`scripts/intake_evidence_validate.py`**: keep CLI contract (**`--file`**, **`--stdin`**, **`--self-test`**); surface lib stderr codes unchanged.

### 2) Normative contract (`.cursor/commands/intake.md` + **`template/`** mirror)

- **`asked_topics`** may list only topics for which a **user-visible question** was posed **or** a **DEC-0060**-allowed alternate applies (**`delegation_ref`**, **`equivalent_evidence_ref`**, **`assumption_confirmation_ref`**).
- Explicitly **forbid** fabricating per-topic **`answer_ref`** rows by echoing one bug-report blob across all keys to satisfy the validator.
- Cross-link **DEC-0060** / **DEC-0067** / **US-0083** so operators do not conflate **`ie:`** integrity with “question asked.”

Parity: **`scripts/check_intake_template_parity.py`** (or successor) must stay **PASS** for any **`intake.md`** edit.

### 3) Locked reason codes (under umbrella **`INTAKE_PERSISTENCE_BLOCKED`**)

| Code | When |
|------|------|
| **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** | Distinct **`topic_key`** rows with **`satisfied_by=answer_ref`** share non-distinct **`quoted_user_text`** without **`equivalent_evidence_ref`** / other allowed alternate. |
| **`INTAKE_ASKED_TOPIC_NOT_EVIDENCED`** | (Optional / phase-2) **`asked_topics`** includes a topic without required question-binding artifact when that feature is enabled. |
| **Existing** | **`INTAKE_DELEGATION_EVIDENCE_MISSING`**, **`INTAKE_DELEGATION_EVIDENCE_INVALID`**, **`INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`**, **`INTAKE_REQUIRED_TOPIC_MISSING`** — **do not overload** for BUG-0007 duplicate-answer semantics. |

### 4) Test fixtures and regression matrix (**R-0066** § table — sprint must automate)

| # | Scenario | Expected |
|---|----------|----------|
| 1 | Fixture aligned with **`BUG-0007-intake-20260403.json`** (duplicate **`answer_ref`** across keys) | **FAIL** with **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`** (or locked synonym) |
| 2 | Five **distinct** short answers + valid **`ie:`** | **PASS** |
| 3 | **`satisfied_by=delegation_ref`** + complete delegation metadata + valid **`ie:`** | **PASS** (**US-0083** / **DEC-0067** non-regression) |
| 4 | **`evidence_source=equivalent_evidence_ref`** row; topic omitted from **`asked_topics`** per lib rules | **PASS** |
| 5 | **`assumption_confirmation_ref`** path | **PASS** |
| 6 | **`python scripts/intake_evidence_validate.py --self-test`** | **PASS** after lib change |
| 7 | Active + **`template/`** parity | **PASS** |

Prefer **`tests/`** unittest module(s) invoking **`validate_intake_evidence`** directly (and/or subprocess on **`intake_evidence_validate.py`**) so CI mirrors operator commands.

## US-0083 / equivalent_evidence non-regression (hard gate)

- **Delegation**: Rows with **`satisfied_by=delegation_ref`**, required delegation fields, and valid **`ie:`** binding must **not** trip duplicate-**`answer_ref`** rules.
- **Equivalent evidence**: Topics satisfied via **`equivalent_evidence_ref`** / **`evidence_source`** must **not** be forced through fake per-topic **`answer_ref`** duplicates; validator behavior must match **`# US-0083`** architecture and **R-0062** intent.
- Sprint **execute** must add or extend fixtures that mirror **`handoffs/intake_evidence/US-0083-intake-20260331-b.json`** (or equivalent) and equivalent-evidence samples so matrix rows 3–4 cannot regress silently.

## Files to touch (execute phase — indicative)

| Path | Change |
|------|--------|
| **`scripts/intake_evidence_lib.py`** | New deterministic checks + codes. |
| **`.cursor/commands/intake.md`** | Truthfulness / forbid synthetic **`answer_ref`** echo. |
| **`template/.cursor/commands/intake.md`** | Parity. |
| **`tests/`** | New regression tests for BUG-0007 **FAIL** + US-0083 / equivalent-evidence **PASS**. |
| Optional | **`scripts/intake_bug_resume_brief_refresh.py`** / **`bug_issue_validate.py`** — only if a single choke-point should re-validate; avoid duplicate sources of truth (**R-0066**). |

## Risks

| Risk | Mitigation |
|------|------------|
| False positives on legitimate repeated short answers | Scope duplicate rule (e.g. “same blob across **all** pack keys”); tune in sprint with matrix row 2. |
| False confidence after only one heuristic | State residual risk; optional **`question_*`** follow-up. |
| Template drift | Same change set for active + **`template/`**; parity script **PASS**. |

## Decision linkage

- Research basis: **`R-0066`**
- Related: **`BUG-0007`**, **US-0068**, **US-0078**, **US-0079**, **US-0083**, **DEC-0060**, **DEC-0067**, **R-0062**, **R-0055**
