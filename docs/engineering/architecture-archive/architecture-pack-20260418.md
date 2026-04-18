# Architecture archive pack (2026-04-18)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 33
- First archived heading: `# US-0050: Clean Install Hygiene and Complete Clean-Repo Coverage`
- Last archived heading: `# US-0051: Intelligent Intake Decomposition and Risk-Aware PO Questioning`
- Verification tuple (mandatory):
  - archived_body_lines=143
  - preamble_lines=10
  - retained_body_lines=3486

---

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

