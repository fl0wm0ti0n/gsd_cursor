# Architecture archive pack (2026-03-21)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 16
- Retained units in hot file: 29
- First archived heading: `# US-0043: Backlog Reconciliation Gate for Released Sprints`
- Last archived heading: `# US-0029: Knowledge Curation & Early Research`
- Verification tuple (mandatory):
  - archived_body_lines=1441
  - preamble_lines=10
  - retained_body_lines=3412

---

# US-0043: Backlog Reconciliation Gate for Released Sprints

## Overview

US-0043 introduces a deterministic reconciliation gate so backlog story status
and acceptance checkboxes cannot remain stale after sprint release finalization.
The architecture uses existing canonical release evidence and adds a scoped
reconciliation step plus fail-safe drift detection.

## Canonical evidence precedence

For a target sprint, reconciliation uses this precedence:

1. `handoffs/release_queue.md` target row status (`released` required)
2. `handoffs/releases/Sxxxx-release-notes.md` gate summary
3. Sprint QA/UAT artifacts (`sprints/Sxxxx/qa-findings.md`, `uat.json`, `uat.md`)
4. Sprint release findings (`sprints/Sxxxx/release-findings.md`) when present
5. Mandatory baseline test evidence (`tests/report.md`) if referenced by release
   gate output

If evidence is contradictory or missing, fail safe and do not silently mutate
backlog status.

## Reconciliation model

- Trigger point: `/release` finalization boundary (or deterministic equivalent
  post-release step).
- Scope: target sprint stories only (no global backlog sweep).
- Action when evidence is PASS:
  - set linked story status to `DONE`
  - reconcile linked story AC checkboxes to checked state
- Action when evidence contradicts `released` state:
  - fail-safe reason code `BACKLOG_STATUS_DRIFT`
  - include remediation guidance and evidence references

## Safety constraints

- No mutation of unrelated backlog stories.
- No pre-release auto-transition to `DONE`.
- Reconciliation is deterministic and idempotent for the same target sprint.
- Active/template command+docs parity is mandatory.

## QA and regression implications

Required coverage:
- Negative: `released` sprint with stale backlog story status/ACs triggers
  `BACKLOG_STATUS_DRIFT`.
- Positive: valid released evidence auto-reconciles target story to consistent
  `DONE` + checked AC state.
- Scope guard: unrelated backlog entries remain unchanged.

## Decision linkage

- Research basis: `R-0007`
- Decision: `DEC-0021`

---

# US-0044: Continuous `/auto` Backlog-Drain Mode

## Overview

US-0044 adds an optional orchestration mode where `/auto` continues across
multiple planned stories in one run. This extends workflow-level automation
without changing default-safe behavior.

## Control surface

- `AUTO_BACKLOG_DRAIN=0|1`
- `AUTO_BACKLOG_MAX_STORIES>=1`
- `AUTO_BACKLOG_ON_BLOCK=stop|skip`
- `AUTO_STORY_SELECTION=priority_then_backlog_order`

## Deterministic semantics

- Mode off (`0`): preserve current single-segment continuation behavior.
- Mode on (`1`): select next eligible OPEN story by deterministic policy, then
  run full lifecycle story-by-story until bounded stop criteria.
- Decision gates remain mandatory and pause flow for user decision.
- Blocked story handling follows policy:
  - `stop`: emit `BACKLOG_STORY_BLOCKED_STOP` and stop.
  - `skip`: emit `BACKLOG_STORY_BLOCKED_SKIPPED`, record, continue.

## Bounded run policy

- Stop on max stories limit with reason `BACKLOG_MAX_STORIES_REACHED`.
- Stop when no eligible stories remain with `BACKLOG_NO_ELIGIBLE_STORIES`.
- Keep existing global stop conditions and QA/verify/release gates intact.

## Decision linkage

- Research basis: `R-0008`
- Decision: `DEC-0022`

---

# US-0045: Canonical Story Status Source + Global Drift Guard

## Overview

US-0045 establishes canonical ownership for story status and introduces a
deterministic drift-prevention contract across product and engineering artifacts.
The goal is to prevent recurring OPEN/DONE mismatches while preserving
target-scoped, non-destructive workflow behavior.

## Canonical ownership model

- Canonical status owner: `docs/product/backlog.md` (`OPEN|DONE` only).
- Derived status views:
  - `docs/product/acceptance.md` (story completion checklist)
  - `docs/engineering/state.md` (traceability/checkpoint evidence)

Derived artifacts must never overrule canonical backlog story status.

## Reconciliation and precedence model

At release/reconciliation boundaries, apply deterministic precedence:

1. Canonical story status from `docs/product/backlog.md`
2. Target sprint release evidence (`release_queue`, sprint release notes,
   QA/UAT/release findings)
3. Derived artifact updates (`acceptance.md`, `state.md`)

Mutation scope:
- Target stories only for the current boundary.
- No broad rewrite of unrelated stories/sprints.

## One-time normalization baseline

Historical drift is repaired by a one-time normalization pass that:
- identifies previously completed stories with stale `OPEN`/unchecked status,
- updates canonical and derived artifacts to consistent state,
- records a durable audit report at
  `docs/engineering/status-normalization-report.md`.

Report rows are append-only and include:
- story id
- prior values
- resolved values
- evidence refs
- timestamp

## Fail-safe behavior

Contradictory outcomes at reconciliation boundary fail closed with deterministic
reason codes:
- `BACKLOG_STATUS_DRIFT`
- `CANONICAL_STATUS_CONFLICT`

Failures must include actionable remediation guidance and must not trigger
destructive auto-rewrites.

## Decision linkage

- Research basis: `R-0009`, `R-0014`
- Decision: `DEC-0025`

---

# US-0049: Legacy DONE-Story Acceptance/Traceability Backfill Guard

## Overview

US-0049 adds deterministic detection and bounded repair for legacy stories where
`docs/product/backlog.md` shows DONE but acceptance checkmarks or
traceability/release artifacts disagree. It provides a one-time backfill mode
and an ongoing guard at reconciliation/release boundaries, with an auditable
report and explicit reason-code vocabulary. Per R-0023; aligns with US-0045
(canonical source) and US-0043 (release-boundary reconciliation) without
duplicating their scope.

## Detection rule

A story is in **legacy drift** when:

- Backlog status is **DONE**, and
- At least one of:
  - Acceptance checklist item for that story is **unchecked**
  - Traceability index or `docs/engineering/state.md` **lacks an entry** for that story
  - Release artifacts (e.g. `handoffs/releases/Sxxxx-release-notes.md`, queue row)
    **lack clear representation** for that story

Repair and guard apply only to stories matching this rule; no broad sweep of
unrelated backlog/acceptance/state/release artifacts.

## Canonical audit artifact

- **Path**: `docs/engineering/legacy-drift-audit.md`
- **Required fields per entry**: story ID, prior acceptance state, prior
  traceability state, resolved state(s), reason code, evidence reference
- **Semantics**: append-only audit log; one-time backfill and ongoing guard
  append entries when drift is detected and repaired (or when guard blocks and
  reports)

## Reason-code vocabulary

- `BACKLOG_DONE_ACCEPTANCE_UNCHECKED` — backlog DONE but acceptance item unchecked
- `BACKLOG_DONE_TRACEABILITY_MISSING` — backlog DONE but traceability/state lacks entry
- `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` — backlog DONE but release artifacts lack representation

Each code must have documented remediation guidance (where to fix, what to update).

## One-time backfill mode

- **Trigger**: explicit command or flag (e.g. dedicated check or `/memory-audit`-related path).
- **Behavior**: run detection once over all DONE stories; for each legacy-drift story,
  perform target-scoped repair (update acceptance and/or traceability/release refs from
  canonical evidence) and append audit report entry.
- **Idempotent**: when no drift exists, run produces no mutations; report is empty or
  "no drift".
- **Safe**: only stories matching the detection rule are mutated; no destructive
  rewrite of unrelated entries.

## Ongoing guard

- **Integration points**: at release boundary or reconciliation boundary (or dedicated
  check step). When legacy drift is detected, either:
  - **Block** with explicit reason code and remediation guidance, or
  - **Repair** target-scoped and append audit entry (policy configurable/documentable).
- **Deterministic**: behavior and reason codes are documented; operators get explicit
  diagnostics, not silent block or blind repair.

## Guard placement and release/reconciliation

- Guard may run as part of `/release` pre-finalization checks or as a dedicated
  verification step before release/reconciliation.
- If guard blocks: emit reason code, remediation, and evidence refs; do not finalize
  release until resolved or explicit override (e.g. decision gate) is recorded.
- Template parity: active and `template/` command/rule/docs for backfill and guard
  behavior remain aligned.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Backfill touches many entries on large backlogs | Target-scoped repair only; audit report makes impact inspectable |
| Guard blocks release unexpectedly | Explicit reason codes and remediation; optional repair path with audit append |
| Overlap with US-0045/US-0043 | Scope limited to legacy-drift detection rule and procedure; canonical ownership and forward reconciliation unchanged |

## Decision linkage

- Research basis: `R-0023`
- Decision: `DEC-0031`
- Boundaries: does not change US-0045 canonical status ownership or US-0043
  broad reconciliation semantics; adds operational guard/backfill procedure and
  audit contract.

---

# US-0033: Configurable Guided Intake Behavior

## Overview

US-0033 adds configurable intake interaction behavior with a single switch.
Guided behavior is default-on for higher intake quality; low-touch mode is
explicitly available for teams that want minimal intake overhead.

## Mode contract

Switch:
- `INTAKE_GUIDED_MODE=1|0` in `.cursor/scratchpad.md` (default `1`)

Behavior:
- Guided mode (`1`):
  - targeted follow-up only when ambiguity prevents concrete acceptance
  - at least one viable option/alternative before recommendation
  - explicit user authority (PO recommends; user decides)
  - intake-time web research persisted as R-xxxx evidence
- Low-touch mode (`0`):
  - no proactive follow-up/options/research overhead unless user asks
  - duplicate/overlap backlog check remains active baseline safety

## Scope boundaries

- In scope: PO intake behavior, command/agent guidance, switch semantics,
  documentation and regression coverage.
- Out of scope: downstream architecture/sprint/release behavior changes.

## Decision linkage

- Research basis: `R-0015`
- Decision: `DEC-0026`

---

# US-0032: Optional Per-Feature User Guide Mode

## Overview

US-0032 adds an optional docs-as-code path for per-feature, end-user-facing guides
that explain what a feature does and how to use it. The mode is fully
flag-controlled and must impose zero additional required steps or blocking checks
when disabled.

## Control surface

- `USER_GUIDE_MODE=0|1` (default `0`) in `.cursor/scratchpad.md`.
- When `USER_GUIDE_MODE=0`, no phase command is required to read or write
  user-guide artifacts.
- When `USER_GUIDE_MODE=1`, each accepted feature story (for example `US-xxxx`)
  is expected to have a corresponding user guide artifact.

## Canonical location and naming

- Canonical root: `docs/user-guides/`
- One guide per feature story: `docs/user-guides/US-xxxx.md`
- Optional frontmatter/metadata (for future use): story id, title, audience,
  and any relevant feature-flag identifiers.

This pattern keeps guides easy to trace from backlog/acceptance (story IDs are
already canonical identifiers) while leaving room to introduce area-based
subfolders later without breaking existing paths.

## Guide schema (minimum required sections)

Each guide is a short, task-focused how-to with the following required sections
per `R-0021` and `R-0022`:

- **Purpose** — what the feature is and when to use it.
- **Prerequisites** — environment, permissions, and relevant flags/modes.
- **Usage steps** — step-by-step instructions.
- **Example** — at least one concrete usage example.
- **Limitations** — known caveats or boundaries.
- **Troubleshooting** — common issues and how to resolve them.

Validation is structural only: automation checks for the presence of required
headings/sections and basic format, not semantic quality of the text.

## Workflow behavior

### Mode disabled (`USER_GUIDE_MODE=0`)

- `/intake`, `/architecture`, `/sprint-plan`, `/execute`, `/qa`,
  `/verify-work`, and `/release` add **no required** user-guide steps or gates.
- Existing stories and sprints proceed exactly as today; any user guides that
  exist are treated as optional documentation.

### Mode enabled (`USER_GUIDE_MODE=1`)

- `/intake` and `/architecture`:
  - Ensure backlog/acceptance artifacts record the story ID in a way that can
    be mapped to `docs/user-guides/US-xxxx.md`.
  - May note that a user guide is expected for end-user-facing features, but do
    not block intake/architecture on guide content.

- `/sprint-plan`:
  - For feature stories that affect end users, include at least one task for
    creating or updating the corresponding user guide.

- `/execute`:
  - Dev work for an in-scope feature includes updating
    `docs/user-guides/US-xxxx.md` in the same change as the code when behavior
    changes.

- `/qa` and `/verify-work`:
  - QA may treat user-guide completeness as an advisory, structural check and
    record findings when required sections are missing or obviously placeholder.
  - QA/UAT remain responsible for feature correctness; guide checks focus only
    on schema completeness.

- `/release`:
  - Adds a **mode-conditioned** gate: for each story in the sprint when
    `USER_GUIDE_MODE=1`, require the canonical guide file to exist and pass
    structural validation.
  - On failure, block release with reason code `USER_GUIDE_INCOMPLETE` and
    remediation pointing to the missing guide or sections.

## Interaction with spec-pack mode (US-0031)

- User guides are end-user-facing how-to documents and must not duplicate
  Design Concept, CRS, or Technical Spec content.
- Spec-pack artifacts remain technical/engineering documents; user guides may
  link to them for background but are not required to.
- `SPEC_PACK_MODE` and `USER_GUIDE_MODE` are independent optional modes; either
  can be enabled without the other.

## Alternatives and tradeoffs

1. **Control surface: single global flag vs per-story toggle**
   - *Alternative*: encode guide requirements per story using backlog or
     acceptance metadata only (no global mode flag).
   - *Decision*: use a single scratchpad flag `USER_GUIDE_MODE` as the primary
     control and derive per-story expectations from backlog/acceptance context.
     This matches other optional modes (`SPEC_PACK_MODE`,
     `CROSS_REPO_OBSERVABILITY`, `COMPONENT_SCOPE_MODE`) and keeps configuration
     simple, at the cost of less granular per-feature switching.

2. **Location: story-id-only naming vs area/feature folders**
   - *Alternative*: use `docs/user-guides/<area>/<feature>.md` with the story
     ID only in frontmatter.
   - *Decision*: adopt `docs/user-guides/US-xxxx.md` as the initial canonical
     pattern, with optional frontmatter for area/feature metadata. This is easy
     to validate and trace from backlog and can evolve to area-based
     subfolders later without breaking existing guides.

3. **Gate placement: release-only vs earlier QA/verify-work gates**
   - *Alternative*: enforce guide completeness at `/qa` or `/verify-work`.
   - *Decision*: place the blocking structural completeness gate in `/release`
     only, keeping QA checks advisory. This minimizes disruption to existing
     QA/UAT flows and still guarantees that released features have structurally
     complete guides when the mode is enabled.

4. **Validation depth: structural vs semantic**
   - *Alternative*: add semantic validation or content scoring.
   - *Decision*: limit automation to structural validation and rely on human
     review for content quality. This keeps checks simple, deterministic, and
     low-risk.

## Risks and mitigations

- **Risk**: Enabling `USER_GUIDE_MODE` mid-project could block release for
  older features without guides.
  - **Mitigation**: Scope the release gate to the sprint/story set in scope;
    older DONE stories are not retroactively gated unless explicitly brought
    back into a sprint.

- **Risk**: Drift between feature behavior and guides despite structural checks.
  - **Mitigation**: Encourage definition-of-done patterns (guide tasks in
    sprints) and QA advisory checks; structural validation ensures a minimal,
    consistent shape but not absolute correctness.

- **Risk**: Confusion between user guides and spec-pack artifacts.
  - **Mitigation**: Keep audiences and locations distinct
    (`docs/user-guides/*` vs spec-pack locations) and clarify in commands/docs
    that user guides are for end users while spec-pack artifacts target
    engineers and stakeholders.

## Decision linkage

- Research basis: `R-0021`, `R-0022`
- Decision: `DEC-0030`

---

# US-0034: Optional Cross-Repo Compatibility Observability

## Overview

US-0034 introduces optional compatibility observability across repositories and
components with deterministic artifacts and release gate behavior.

## Control surface

- `CROSS_REPO_OBSERVABILITY=0|1` (default `0`)
- `COMPATIBILITY_GATE_ON_CRITICAL=0|1` (default `1`)
- `COMPATIBILITY_SOURCES=` explicit source declarations

## Behavior model

- Disabled mode (`0`): `/intake`, `/architecture`, `/execute`, and `/qa` add zero
  required compatibility overhead.
- Enabled mode (`1`):
  - monitored sources are declared explicitly,
  - compatibility signals and findings are persisted in canonical artifacts,
  - findings include severity, affected modules, evidence refs, and actions.

Canonical artifacts:
- `docs/engineering/compatibility-signals.md`
- `docs/engineering/compatibility-report.md`
- `docs/engineering/manifests/registry.manifest.yaml`
- `docs/engineering/manifests/repo.manifest.yaml`

## Release gate policy

When observability mode is enabled and unresolved critical compatibility
findings exist while `COMPATIBILITY_GATE_ON_CRITICAL=1`, release progression
must stop at decision gate with reason code `COMPATIBILITY_CRITICAL_OPEN`.

## Decision linkage

- Research basis: `R-0016`
- Decision: `DEC-0027`

---

# US-0035: Optional Component-Scoped Execution Mode

## Overview

US-0035 adds optional component-scoped workflow behavior so teams can work on
selected components without destabilizing non-target components.

## Control surface

- `COMPONENT_SCOPE_MODE=0|1` (default `0`)
- `TARGET_COMPONENTS=` comma-separated in-scope component IDs

## Behavior model

- Disabled mode (`0`): no required scoped behavior overhead.
- Enabled mode (`1`):
  - declare scope in `docs/engineering/component-scope.md`
  - include `target_components`, `non_target_components`, and
    `allowed_interface_touch`
  - require scoped task metadata in sprint planning
  - enforce scope-first execution in `/execute`
  - verify unaffected-component checks in `/qa` and record evidence in
    `docs/engineering/component-scope-report.md`

## Escalation policy

If out-of-scope impact is detected without prior approval, workflow must trigger
decision gate before release via reason code
`COMPONENT_SCOPE_VIOLATION_UNAPPROVED`.

## Decision linkage

- Research basis: `R-0017`
- Decision: `DEC-0028`

## Components

### 1. File Classification (path-pattern based)

All 86 template files are classified into three categories by directory/path pattern. No manifest file needed — the classification is embedded as path lists in each installer.

#### Framework files (56 files) — updated on upgrade

```
.cursor/commands/*                          19 slash commands
.cursor/rules/*                              5 AI behavior rules
.cursor/agents/*                             6 subagent definitions
.cursor/skills/its-magic/SKILL.md            1 skill definition
.cursor/skills/its-magic/templates/*        16 JSON/MD templates
.cursor/hooks/hook.py                        1 hook dispatcher
.cursor/hooks/README.md                      1 hook docs
.cursor/hooks.json                           1 hook config
.cursor/scratchpad.local.example.md          1 example config
scripts/validate-and-push.ps1                1 quality script
scripts/validate-and-push.sh                 1 quality script
.github/workflows/ci.yml                     1 CI workflow
.github/workflows/deploy.yml                 1 deploy workflow
docs/engineering/context/phase-template.json 1 phase template
```

#### User data files (28 files) — preserved on upgrade

```
docs/product/*                               3 product docs
docs/engineering/architecture.md             \
docs/engineering/state.md                     |
docs/engineering/research.md                  |
docs/engineering/runbook.md                   | 7 engineering docs
docs/engineering/decisions.md                 |
docs/engineering/codebase-map.md              |
docs/engineering/dependencies.json           /
sprints/S0001/*                              8 sprint artifacts
sprints/quick/Q0001/*                        2 quick task artifacts
handoffs/*                                   6 handoff files
decisions/*                                  2 decision records
```

#### Mixed files (2 files) — preserve + notify

```
.cursor/scratchpad.md      User-customized config flags → preserve, warn about new flags
README.md                  May contain project-specific content → preserve
```

#### Classification rules

- Path patterns are matched at the directory level. A file under `.cursor/commands/` is always framework.
- Any NEW file in a future version that doesn't match a user-data pattern is treated as framework (safe default — new features get delivered).
- Files that don't exist in the target repo are ALWAYS copied, regardless of category.

### 2. Version Tracking

A `.its-magic-version` file in the target repo root stores the installed version.

**Format**: plain text, single line, semver string (e.g. `0.1.2-17`).

**Lifecycle**:
- Written/updated after every successful install or upgrade.
- Read at the start of upgrade mode to determine the installed version.
- If missing (pre-upgrade-era install or first-time install): upgrade proceeds treating all existing user-data files as "preserve" and all framework files as "update."

**Git**: The file should be committed (it's useful for the team to know which version is installed). It's added to the template so new installs get it from the start.

### 3. Upgrade Flow Algorithm

```
1. Read .its-magic-version from target (or "unknown" if missing)
2. Print: "Upgrading from v{old} to v{new}"
3. List all source files from template/
4. For each file:
   a. If file does NOT exist in target:
      → Copy (new file delivery, regardless of category)
      → Track as "added"
   b. If file IS a framework file:
      → Compare source and target content
      → If identical: skip (no change needed)
      → If different: copy (update)
      → Track as "updated" or "unchanged"
   c. If file IS a user-data file:
      → Skip (preserve)
      → Track as "preserved"
   d. If file IS a mixed file:
      → Skip (preserve)
      → Compare source and target content
      → If different: track as "review recommended"
5. Write new version to .its-magic-version
6. Print upgrade summary:
   - Files added: N (list)
   - Files updated: N (list)
   - Files unchanged: N
   - Files preserved: N
   - Files needing review: N (list with guidance)
```

### 4. Upgrade Summary Output

After upgrade, the installer prints a structured summary:

```
Upgrade complete: v0.1.1 → v0.1.2

  Added (new):        3 files
    .cursor/commands/phase-context.md
    .cursor/skills/its-magic/templates/phase-context.json
    .cursor/skills/its-magic/templates/plan-verify.json

  Updated (framework): 7 files
    .cursor/commands/execute.md
    .cursor/rules/core.mdc
    .cursor/hooks/hook.py
    ...

  Unchanged:          46 files
  Preserved (user):   28 files

  Review recommended:  1 file
    .cursor/scratchpad.md
      New flags available. See .cursor/scratchpad.local.example.md for reference.
```

### 5. CLI Changes

`bin/its-magic.js`:
- Accept `upgrade` as a valid `--mode` value.
- Pass through to OS-specific installer.
- Help text updated with upgrade mode documentation.

`installer.ps1`, `installer.sh`, `installer.py`:
- Add `upgrade` to mode validation.
- Add `FRAMEWORK_PATHS` and `USER_DATA_PATHS` pattern lists.
- Add `classify_file(path)` function that returns `framework`, `user-data`, or `mixed`.
- Add upgrade branch in the file copy loop.
- Add `.its-magic-version` read/write logic.
- Add upgrade summary output.

### 6. Backup Interaction

- `--backup` flag works with upgrade mode: backs up all framework files before updating them. User-data files are not touched, so no backup needed for those.
- This provides a safety net: `its-magic --target . --mode upgrade --backup` backs up the old framework files, then updates them.

### 7. Migration Notes (future)

For now, the upgrade summary and the always-updated `scratchpad.local.example.md` provide sufficient guidance. If breaking changes occur in future versions:
- Add a `MIGRATION.md` to the package root (not installed to target repos).
- The installer can check for version-specific migration notes and print them during upgrade.
- This is a future enhancement, not required for the initial implementation.

## File Changes Required

| File | Change |
|------|--------|
| `bin/its-magic.js` | Add `upgrade` to mode validation, update help text |
| `installer.ps1` | Add path classification, upgrade branch, version tracking, summary output |
| `installer.sh` | Same as above |
| `installer.py` | Same as above |
| `template/.its-magic-version` | New file: `0.0.0` placeholder (gets overwritten with actual version on install) |
| `tests/run-tests.ps1` | Add upgrade scenario test |
| `tests/run-tests.sh` | Add upgrade scenario test |
| `README.md` | Document upgrade workflow |

## Risks

| Risk | Mitigation |
|------|------------|
| Triple installer parity | Implement one installer first (PS1), validate, then port to sh and py. Test all three in CI. |
| Classification drift | Path patterns are stable (directories rarely added). New directories default to framework (safe). Review classification on each release. |
| Mixed file false positives | Only 2 mixed files (scratchpad.md, README.md). Simple "differs from template" check is sufficient. |
| Pre-upgrade-era repos | If `.its-magic-version` is missing, treat as upgrading from "unknown". All logic still works — framework files get updated, user-data preserved. |
| Renamed/removed files in future versions | Not handled in v1. Old files from previous versions remain in the target repo. Can add cleanup logic later if needed. |

---

# US-0020: /ask Command

## Overview

A read-only command that loads the project context pack and answers questions without creating or modifying any artifacts. This is the lightweight interaction channel that sits outside the workflow engine.

## Design

### Command definition

`/ask` is a new slash command (`.cursor/commands/ask.md`) with no subagent role. It uses the default agent (the one responding to the user). It has no outputs and no stop conditions beyond answering the question.

### Context pack (inputs)

The command instructs the agent to read these files before answering:

```
docs/engineering/state.md          Current status, progress, known issues
docs/product/backlog.md            All stories with status
docs/product/acceptance.md         What's done, what's remaining
docs/engineering/architecture.md   Technical approach and decisions
docs/engineering/decisions.md      Decision index
docs/engineering/runbook.md        Commands and project config
sprints/S*/progress.md             Active sprint progress (latest sprint)
.cursor/scratchpad.md              Automation flags and config
```

The agent reads only what's needed to answer the question. For a status question, `state.md` alone may suffice. For a design question, `architecture.md` is needed. The command lists the full pack but does not mandate reading all files.

### Behavior rules

1. Read relevant context files before answering.
2. Do NOT create, modify, or delete any files.
3. Do NOT update `state.md` or any sprint artifacts.
4. Can reference stories (US-xxxx), decisions (DEC-xxxx), and tasks (T-xxx) by ID.
5. Can suggest next actions but does not execute them.
6. If the question reveals a bug or feature idea, suggest running `/intake` but do not auto-trigger it.

### File changes

| File | Change |
|------|--------|
| `.cursor/commands/ask.md` | New command definition |
| `template/.cursor/commands/ask.md` | Template copy |
| `README.md` + `template/README.md` | Add /ask to core commands list and document as lightweight channel |

---

# US-0021: Critical Evaluation in Intake and Architecture

## Overview

Update the PO and Tech Lead agent behavior so the AI evaluates ideas before accepting them. This applies to `/intake` (idea evaluation) and `/architecture` (design challenge). The goal is constructive friction: good ideas proceed faster because they've been validated; weak ideas get improved rather than blindly implemented.

## Design

### Evaluation protocol for /intake

Add a new step 0 ("evaluate") before the existing step 1 ("ask questions") in the intake command. The PO agent must:

1. **Duplicate check**: Scan `docs/product/backlog.md` for existing stories that overlap with the new idea. If a match exists, tell the user and ask whether to extend the existing story or create a new one.

2. **Feasibility check**: Consider whether the idea is technically viable within the current architecture. If unsure, say so and recommend `/research` first.

3. **Alternative check**: Ask "is there a simpler or better way to achieve this?" Propose at least one alternative when one exists. If the original idea is clearly best, say so and proceed.

4. **Scope check**: If the idea is too large for a single story, suggest breaking it down. If too small, suggest `/quick` instead.

5. **Proceed or challenge**: After evaluation, either proceed with story creation (with any improvements incorporated) or present concerns and ask the user to decide.

The evaluation must be **constructive** (AC-7): the AI presents its analysis and recommendation, but the user always has the final say. If the user says "do it anyway," the AI proceeds.

### Challenge protocol for /architecture

Add a step 0 ("challenge") to the architecture command. The Tech Lead agent must:

1. **Question assumptions**: For each major design decision, ask "what's the alternative?" If there's only one viable option, say so. If there are meaningful tradeoffs, present them as a DEC-xxxx decision.

2. **Simplicity check**: Ask "can this be simpler?" before accepting a design. Prefer the simplest approach that meets the acceptance criteria.

3. **Risk inventory**: Explicitly list what could go wrong with the chosen approach.

### Agent definition updates

**po.mdc** - Add evaluation rules:
```
- Before creating a new story, check backlog.md for duplicates/overlaps.
- Evaluate feasibility and suggest alternatives when a simpler approach exists.
- Challenge assumptions constructively: present analysis, let user decide.
- Suggest /quick for small tasks that don't need full sprint ceremony.
```

**tech-lead.mdc** - Add challenge rules:
```
- Question design assumptions: ask "what's the alternative?" for each decision.
- Prefer simplicity: ask "can this be simpler?" before accepting a design.
- List risks explicitly for every architectural choice.
```

### Command definition updates

**intake.md** steps become:
```
1. Evaluate: check backlog for duplicates, assess feasibility, suggest alternatives.
2. Ask targeted questions until the story and acceptance are concrete.
3. Persist the story and acceptance in product docs.
4. Write a PO -> TL handoff with scope and risks.
```

**architecture.md** steps become:
```
1. Challenge: question assumptions, check for simpler alternatives, list risks.
2. Define the minimal architecture and key components.
3. Record tradeoffs in decisions log.
4. Update engineering state and readiness.
```

### File changes

| File | Change |
|------|--------|
| `.cursor/agents/po.mdc` | Add evaluation rules |
| `.cursor/agents/tech-lead.mdc` | Add challenge rules |
| `.cursor/commands/intake.md` | Add evaluate step |
| `.cursor/commands/architecture.md` | Add challenge step |
| `template/.cursor/agents/po.mdc` | Template copy |
| `template/.cursor/agents/tech-lead.mdc` | Template copy |
| `template/.cursor/commands/intake.md` | Template copy |
| `template/.cursor/commands/architecture.md` | Template copy |

### Risks

| Risk | Mitigation |
|------|------------|
| Over-gatekeeping | AC-7 enforces "constructive, not blocking." User always has final say. |
| Slow intake | Evaluation adds 1 step but saves wasted sprints on bad ideas. Net positive. |
| Missed duplicates | Backlog scan is best-effort. Agent reads backlog.md which has all stories. |
| Template/active drift | Both copies updated in same task. |

---

## Decisions

- DEC-0003: `--mode upgrade` as 4th mode, path-pattern classification, `.its-magic-version` file -- Accepted
- DEC-0004: Mixed files (scratchpad.md, README.md) preserved + notify -- Accepted
- DEC-0005: /ask as read-only command with context pack, no subagent role -- Accepted
- DEC-0006: Critical evaluation as step 0 in /intake and /architecture, not separate commands -- Accepted
- DEC-0007: Every phase runs in a fresh subagent context; `/auto` is orchestration-only -- Accepted
- DEC-0008: Add dedicated `/memory-audit` read-only command with non-blocking report and explicit memory/template drift split -- Accepted
- DEC-0009: Artifact lifecycle taxonomy: shared placeholder/populated/verified states, phase-ownership matrix, minimum evidence rules -- Accepted
- DEC-0010: Traceability index lives in `docs/engineering/state.md`, not a separate file -- Accepted

---

# US-0025: Backlog-to-Sprint Traceability Contract

## Overview

US-0025 closes the gap where backlog stories and sprint artifacts exist
independently with no single cross-reference. The solution adds a lightweight
traceability index and guidance to existing commands — no new tooling.

## Assumption challenge

**Is a separate traceability index artifact needed, or can existing files be
enhanced?**

Sprint task files already reference story IDs (e.g., `Story: US-0018 (AC-1)`
in `tasks.md`). The forward link (story → sprint task) exists. What's missing
is a single project-wide reverse index that answers: "for any story, which
sprint and tasks handled it, and what's the evidence?"

Alternatives considered:
- Enhance `backlog.md` with sprint-mapping columns — rejected: mixes PO
  artifact (story definition) with execution tracking; backlog is 250+ lines.
- New `docs/engineering/traceability.md` — rejected: adds a file for what is
  essentially one table. Extra maintenance burden for the curator.
- Section in `docs/engineering/state.md` — **chosen** (DEC-0010): state.md is
  already the project-wide status artifact, already maintained by the curator.
  Natural fit, no new file.

## Design

### 1) Traceability index format

A Markdown table section in `state.md`:

```
## Traceability Index

| Story | Sprint | Tasks | Status | Evidence |
|-------|--------|-------|--------|----------|
| US-0018 | S0001 | T-001..T-011 | DONE | S0001/uat.json, S0001/summary.md |
```

### 2) Maintenance integration

| Command | Action |
|---------|--------|
| `/sprint-plan` | Tech Lead adds rows for each story assigned to the sprint. Status = `PLANNED`. |
| `/verify-work` | QA updates status to `PASS`/`FAIL`, fills evidence column. |
| `/refresh-context` | Curator verifies index matches actual sprint artifacts, compacts old entries. |

### 3) Guidance updates needed

- `/sprint-plan` steps: add "update traceability index in state.md" after
  task breakdown.
- `/verify-work` steps: add "update traceability index with results" after
  recording UAT.
- Pre-handoff verification: guidance that no OPEN/DONE story should lack a
  traceability entry.

### 4) Scope boundaries

- Distinct from US-0017 (template drift) and US-0024 (memory-vs-code drift).
- This story is artifact-linkage only — story IDs in sprint tasks, reverse
  index in state.md.

## File changes required

| File | Change |
|------|--------|
| `docs/engineering/state.md` | Add Traceability Index section with backfilled entries for completed sprints |
| `.cursor/commands/sprint-plan.md` | Add step: update traceability index |
| `.cursor/commands/verify-work.md` | Add step: update traceability index with results |
| `template/.cursor/commands/sprint-plan.md` | Template copy |
| `template/.cursor/commands/verify-work.md` | Template copy |

## Risks

| Risk | Mitigation |
|------|------------|
| Index falls out of date | Curator maintenance in `/refresh-context` catches drift. Index is small and auditable. |
| Index grows large in long projects | Curator compacts completed-sprint rows. Summarize archived sprints. |
| Developers forget to add story IDs to tasks | `/sprint-plan` guidance makes it explicit; existing convention already does this. |

---

# US-0027: UAT Artifact Lifecycle and Ownership

## Overview

US-0027 removes confusion around `uat.json` and `uat.md` by formalizing when
they are placeholders, when they get populated, who does each step, and what
minimum content is required before a sprint can be marked complete.

## Assumption challenge

**Should `/sprint-plan` create skeleton UAT steps from acceptance criteria, or
should only `/verify-work` populate them?**

Options:
- A) Sprint-plan creates UAT skeleton steps → verify-work fills results.
  Rejected: steps defined before implementation are premature and frequently
  need rewriting once actual code exists.
- B) Sprint-plan creates metadata-only placeholder → verify-work populates
  steps and results. **Chosen**: the placeholder records *what* will be tested
  (stories + ACs), and verify-work creates *how* (actual steps) when
  implementation is done and testable.
- C) Three-stage (sprint-plan → QA → verify-work). Rejected: unnecessary
  ceremony for the framework's scale.

**What's the ownership model?**

Three-role chain:
1. Tech Lead creates the placeholder (planning).
2. QA populates and tests (verification).
3. Release validates completeness (release gate).

## Design

### 1) UAT lifecycle by phase

Governed by DEC-0009 taxonomy (placeholder → populated → verified):

| Phase | Owner | `uat.json` state | `uat.md` state |
|-------|-------|-----------------|----------------|
| `/sprint-plan` | Tech Lead | `{ sprint, steps: [], passed: 0, failed: 0 }` | Header + "Target: US-xxxx AC-1..AC-N" (stories and ACs this sprint covers). No results. |
| `/verify-work` | QA | Steps array populated from ACs. Pass/fail counts accurate. | Each step listed with result. Results summary at bottom. |
| `/release` | Release | Reads and confirms populated + passing. | Reads and confirms coverage. |

### 2) Minimum content requirements

Before a sprint can be marked complete:
- `uat.json`: `steps` array is non-empty, each step has a `description` and
  `result` (`pass`/`fail`). `passed` + `failed` = total steps.
- `uat.md`: Steps section lists every step. Results section has pass/fail
  summary and links to story ACs.

### 3) Guidance updates needed

- `/sprint-plan`: update placeholder creation step to include target
  stories/ACs in the UAT files (not just empty structure).
- `/verify-work`: existing step 1 ("Convert acceptance criteria into testable
  UAT steps") is correct; add explicit reference to DEC-0009 lifecycle and
  minimum content rules.
- `/release`: add UAT completeness as a release readiness check.

### 4) Scope boundaries

- Distinct from US-0024 (memory-vs-code drift detection).
- This story governs UAT artifact lifecycle, not code verification.

## File changes required

| File | Change |
|------|--------|
| `.cursor/commands/sprint-plan.md` | Update UAT placeholder creation guidance |
| `.cursor/commands/verify-work.md` | Add minimum content rules reference, UAT population guidance |
| `.cursor/commands/release.md` | Add UAT completeness as release gate |
| `template/.cursor/commands/sprint-plan.md` | Template copy |
| `template/.cursor/commands/verify-work.md` | Template copy |
| `template/.cursor/commands/release.md` | Template copy |

## Risks

| Risk | Mitigation |
|------|------------|
| QA skips UAT population | Release gate checks for populated UAT. /verify-work guidance makes it mandatory. |
| Placeholder UAT accepted as "done" | DEC-0009 taxonomy explicitly separates placeholder from populated. |
| UAT steps don't match actual ACs | /verify-work derives steps from acceptance.md, ensuring alignment. |

---

# US-0026: Milestone Lifecycle Definition and Exit Criteria

## Overview

US-0026 formalizes milestone lifecycle behavior so milestones are intentionally
created, populated, progressed, and completed instead of remaining
placeholder-like. This is guidance and documentation, not automated enforcement.

## Assumption challenge

**Should lifecycle be enforced by commands or documented as guidance?**

Options:
- A) Command-enforced: commands validate required fields and block progression.
  Rejected: requires hook/validation logic changes, heavy for a process
  governance story. Inconsistent with framework philosophy (AI reads docs).
- B) Guidance-documented: lifecycle is documented, commands reference it, AI
  follows it. **Chosen**: consistent with how all other process governance
  works in this framework. The AI agents are the enforcement mechanism.
- C) Hybrid (warn but don't block). Rejected: warning logic still requires
  command changes. Guidance achieves the same effect through the AI reading
  the rules.

**Can milestone artifacts be simplified?**

The 4-file structure (`milestone.json`, `phases.json`, `progress.md`,
`summary.md`) is reasonable. `phases.json` could merge into `milestone.json`,
but restructuring artifacts is a design change beyond lifecycle governance
scope. Keep current structure and define lifecycle for it.

## Design

### 1) Milestone lifecycle states

Governed by DEC-0009 taxonomy. Five states with entry/exit criteria:

| State | Entry | milestone.json | phases.json | progress.md | summary.md | Exit |
|-------|-------|---------------|-------------|-------------|------------|------|
| **created** | `/milestone-start` run | id, status. Name/goal may be draft. | At least intake phase listed. | Initialized (header only). | Not required. | Sprint planning begins. |
| **active** | First sprint starts | name, goal, scope all populated. | Phases reflect actual planned work. | Updated per sprint completion. | Not required. | All planned sprints done. |
| **in-review** | All sprints complete | No change. | All phases show done/complete. | Shows all sprints complete. | Not required. | `/milestone-complete` run. |
| **completed** | `/milestone-complete` run | status = completed. | Final state. | Final state. | Finalized with outcomes and lessons. | — |
| **cancelled** | Decision to abandon | status = cancelled. | — | — | Records cancellation reason. | — |

### 2) Required field expectations by phase

**`milestone.json`:**
- `id`: required at creation (auto-assigned).
- `name`: may be draft at creation, must be real by active.
- `goal`: may be draft at creation, must be real by active.
- `scope`: may be empty at creation, must list story IDs by active.
- `status`: tracks lifecycle state.

**`phases.json`:**
- Must list at least the intake phase at creation.
- Must reflect actual planned phases (intake → architecture → sprint-plan →
  execute → qa → verify-work → release) by active state.
- Phase statuses updated as work progresses.

### 3) Command update points

| Command | Milestone action |
|---------|-----------------|
| `/milestone-start` | Creates milestone artifacts in **created** state. Populates id, initial phase list. |
| `/sprint-plan` | Transitions milestone to **active** if first sprint. Ensures name/goal/scope populated. |
| `/verify-work` | Updates `progress.md` with sprint results. |
| `/milestone-complete` | Validates all sprints done + UAT passing. Transitions to **completed**. Writes `summary.md`. |

### 4) Guidance updates needed

- `/milestone-start`: add lifecycle state expectations and required fields for
  created state.
- `/milestone-complete`: add exit criteria checklist (all sprints done, UAT
  passing, progress.md complete, summary.md written).
- `/sprint-plan`: add milestone activation check when first sprint under a
  milestone is planned.

### 5) Scope boundaries

- Distinct from sprint sizing/automation (US-0022, US-0023).
- This is lifecycle governance for milestone artifacts only.

## File changes required

| File | Change |
|------|--------|
| `.cursor/commands/milestone-start.md` | Add lifecycle state guidance, required fields |
| `.cursor/commands/milestone-complete.md` | Add exit criteria checklist |
| `.cursor/commands/sprint-plan.md` | Add milestone activation check |
| `template/.cursor/commands/milestone-start.md` | Template copy |
| `template/.cursor/commands/milestone-complete.md` | Template copy |
| `template/.cursor/commands/sprint-plan.md` | Template copy |

---

# US-0023: Fresh Subagent Context Per Phase and /auto Orchestration

## Overview

The workflow must guarantee real context isolation between phases. Switching
persona labels inside one long conversation is not sufficient for independent
review behavior. The design enforces fresh subagent boundaries at every handoff
and makes artifact files the only cross-phase memory.

## Design

### 1) Isolation contract

- Each phase command (`/intake` .. `/refresh-context`) runs in a fresh subagent
  context for its role.
- The current phase stops after writing artifacts/handoff outputs.
- The next phase starts as a new subagent/chat and reads only declared inputs.

### 2) Handoff-only memory transfer

- `handoffs/*.md`, sprint artifacts, and engineering/product docs are the
  canonical memory transfer layer.
- Cross-role continuity must not depend on prior chat history.

### 3) /auto orchestrator behavior

- `/auto` is orchestration-only and does not perform phase work inline.
- It spawns a fresh subagent per phase in sequence.
- In implementation loops it alternates fresh agents on every cycle:
  `execute(dev)` -> `qa(qa)` -> `execute(new dev)` -> `qa(new qa)`.

### 4) Enforcement points

- Rules: `core.mdc` + `handoffs.mdc` contain explicit isolation requirements.
- Commands: each phase command includes an `Execution model` section.
- Agents: role profiles state fresh-context startup and stop-after-handoff.
- Template parity: corresponding files under `template/.cursor/` mirror active
  behavior so generated repos inherit the same model.

## Consequences

- Stronger QA independence and less self-confirming loops in execute/qa cycles.
- Slightly higher orchestration overhead due to frequent context resets.
- Better resilience for pause/resume and long-running projects because artifacts
  are the enforced system of record.

---

# US-0024: Memory Drift Audit Command

## Overview

US-0024 adds a dedicated read-only command (`/memory-audit`) that checks whether
repository memory artifacts still match current repository signals. This is a
memory-vs-code consistency check, not a template sync check.

Scope boundary with US-0017:
- **US-0024 (this story):** memory artifacts vs real code/repo state.
- **US-0017:** active files vs `template/` alignment.

## Assumption challenge and alternatives

### Option A: Extend `/verify-work`

Pros: reuse QA phase and acceptance-oriented flow.
Cons: couples drift diagnostics to UAT timing, makes a read-only health check
harder to run earlier (before handoff/QA/release), and blurs QA outcome with
memory hygiene.

### Option B: Extend `/map-codebase`

Pros: map command already inspects repo structure.
Cons: `/map-codebase` is discovery-oriented and usually run during setup, not as
an ongoing hygiene check. Mixing baseline mapping with drift auditing increases
scope and ambiguity.

### Option C: New dedicated `/memory-audit` command

Pros: simplest clear mental model, explicit ownership, can run anytime, and can
produce a stable report artifact without changing workflow phase semantics.
Cons: one additional command to maintain.

**Decision:** Option C. A dedicated command is the minimal approach that still
meets US-0024 acceptance and keeps US-0017 concerns separate.

## Minimal architecture

### 1) Command behavior and scope

- Command: `/memory-audit`
- Mode: read-only for source/workflow/sprint artifacts (no mutations).
- Output artifact: `docs/engineering/memory-drift-report.md`
- UX: non-blocking. Findings are advisory with severity and recommended actions.
  Command returns success unless command invocation itself fails.

### 2) Detection signals and taxonomy

The report separates findings into two taxonomies:

1. **Memory drift findings** (in scope for US-0024)
   - Code or config files changed while relevant memory artifacts show no
     corresponding update signal.
   - Unresolved decision TODOs/open decision gates that block claimed progress.
   - Sprint/story status mismatches against repository signals (for example:
     story marked done while related changes remain unverified or incomplete).

2. **Template drift findings** (out of scope for US-0024 implementation)
   - Explicitly labeled as reference-only.
   - Link to US-0017 for remediation ownership.

### 3) Report artifact format

`docs/engineering/memory-drift-report.md` structure:

1. Header metadata: timestamp, branch/HEAD snapshot, audit scope.
2. Summary: counts by severity (`high`, `medium`, `low`) and category.
3. Memory drift findings table: artifact, repository signal, severity, evidence,
   recommended next command/action.
4. Template drift section: short list or "none detected", plus US-0017 link.
5. Suggested next steps: `/refresh-context`, `/sprint-plan`, `/verify-work`,
   `/intake` (for newly discovered work).

### 4) Integration points

- **Workflow usage:** run before handoff, before `/qa`/`/verify-work`, and before
  `/release` as a hygiene checkpoint.
- **Command ecosystem:** keep `/verify-work` focused on acceptance validation and
  `/map-codebase` focused on architecture/dependency mapping.
- **Documentation:** add run instructions and interpretation guidance in README
  and `docs/engineering/runbook.md` during implementation.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| False positives from strict heuristics | Start with minimal deterministic checks and severity tiers; keep output advisory. |
| False negatives from shallow checks | Include multiple signals (artifact freshness, decision status, sprint/repo mismatch). |
| Confusion with US-0017 | Force explicit report split: "Memory drift" vs "Template drift (US-0017)". |
| Workflow friction | Keep command non-blocking and focused on recommended follow-up commands. |

---

# US-0029: Knowledge Curation & Early Research

## Overview

US-0029 integrates web research into early workflow phases so PO and Tech Lead
agents have external references when making decisions. It enhances the existing
`/research` command for structured, referenceable output, restructures
`docs/engineering/research.md` with entry IDs, and expands the curator's scope
to include knowledge base maintenance.

This subsumes Q0002 (research persistence). The key insight: decisions are
better when informed by external context (API docs, library comparisons,
compliance references, prior art), and that context should persist across
sessions and agents.

## Assumption challenges

**Should research be blocking or optional?** Optional, flag-controlled. Not all
intake scenarios need external research (internal tooling, well-understood
patterns). `EARLY_RESEARCH=1` (default: on) enables research as an inline
sub-step; `EARLY_RESEARCH=0` skips it. `/research` remains available for manual
deep-dives regardless of the flag.

**Is the R-xxxx format too rigid?** No — semi-structured with minimal required
fields (DEC-0011). Only ID, date, and topic are required. Optional fields
(sources, confidence, linked stories) add value when relevant without blocking
entry creation.

## Design

### 1) Research entry schema (R-xxxx)

Per DEC-0011, entries in `docs/engineering/research.md` follow this format:

```markdown
## R-0001

- **Date**: 2026-02-23
- **Topic**: [short description]
- **Query**: [search query or research question, optional]
- **Sources**: [URLs or references, optional]
- **Findings**: [summary of what was found]
- **Linked**: [US-xxxx, DEC-xxxx references, optional]
- **Confidence**: [high/medium/low, default: medium]
- **Status**: [current/outdated/superseded, default: current]
```

Required: ID, Date, Topic. Everything else is optional. Status defaults to
"current" and is managed by the curator over time.

### 2) PO agent integration (`po.mdc`)

Add a research sub-step to the existing evaluation section:

```
Early research (when EARLY_RESEARCH=1 in scratchpad.md):
- Before evaluating the idea, search the web for relevant external context
  (competitor approaches, library docs, API references, prior art).
- Persist findings as an R-xxxx entry in docs/engineering/research.md.
- Reference the entry ID in the handoff (handoffs/po_to_tl.md).
- If EARLY_RESEARCH=0, skip this step. /research is always available manually.
```

### 3) Tech Lead agent integration (`tech-lead.mdc`)

Add a research sub-step to the existing design challenge section:

```
Early research (when EARLY_RESEARCH=1 in scratchpad.md):
- Before challenging design assumptions, search the web for technical references
  (framework docs, pattern comparisons, performance benchmarks, security
  considerations).
- Persist findings as an R-xxxx entry in docs/engineering/research.md.
- Reference entry IDs in architecture decisions and DEC-xxxx records.
- If EARLY_RESEARCH=0, skip this step.
```

### 4) `/research` command changes

The existing command steps become:

```
1. Identify research topics from product vision, backlog, and acceptance criteria.
2. Search the web for relevant patterns, libraries, APIs, and risks.
3. Persist each finding as an R-xxxx entry in docs/engineering/research.md.
4. Record any decisions triggered by research and update state.
```

Outputs remain the same files (`research.md`, `decisions.md`, `state.md`).
The change is in format (structured entries) not in scope.

### 5) `/intake` command changes

Add research sub-step within step 1 (Evaluate):

```
1. Evaluate:
   a. Check backlog for duplicates, assess feasibility, suggest alternatives.
   b. If EARLY_RESEARCH=1, search the web for relevant context and persist
      findings as R-xxxx entry in research.md.
   c. Reference research in evaluation reasoning.
   d. Present evaluation and recommendation — user decides.
```

### 6) `/architecture` command changes

Add research sub-step within step 1 (Challenge):

```
1. Challenge:
   a. If EARLY_RESEARCH=1, search for technical references and persist as
      R-xxxx entry in research.md.
   b. Question design assumptions ("what's the alternative?").
   c. Check for simpler approaches ("can this be simpler?").
   d. Inventory risks for each architectural choice.
```

### 7) Curator maintenance expansion (`curator.mdc`)

Add research knowledge base to curator's scope:

```
Research knowledge base maintenance:
- During /refresh-context, review docs/engineering/research.md for freshness.
- Mark entries as "outdated" if sources are stale or context has changed.
- Consolidate duplicate entries (point newer to older or merge).
- Flag entries not linked to any active story/decision for potential pruning.
```

### 8) Scratchpad flag

New flag in `.cursor/scratchpad.md`:

```
# Knowledge curation
# - EARLY_RESEARCH: 0|1 (PO/TL search web during intake/architecture)
EARLY_RESEARCH=1
```

Default is ON. Users who want faster workflows without research can set it to 0.
The `/research` command always works regardless of this flag.

### 9) research.md restructure

`docs/engineering/research.md` transitions from free-form prose to structured
entries. Existing content (US-0023 research) should be migrated to the first
R-xxxx entry. New format:

```markdown
# Research

## R-0001

- **Date**: 2026-02-XX
- **Topic**: Subagent context isolation for phase independence
- **Findings**: [migrated from existing content]
- **Linked**: US-0023, DEC-0007
- **Status**: current
```

## File changes required

| File | Change |
|------|--------|
| `.cursor/agents/po.mdc` | Add early research sub-step to evaluation section |
| `.cursor/agents/tech-lead.mdc` | Add early research sub-step to design challenge section |
| `.cursor/agents/curator.mdc` | Add research knowledge base to maintenance scope |
| `.cursor/commands/intake.md` | Add research sub-step within evaluate step |
| `.cursor/commands/architecture.md` | Add research sub-step within challenge step |
| `.cursor/commands/research.md` | Update steps for structured R-xxxx output |
| `.cursor/scratchpad.md` | Add EARLY_RESEARCH=1 flag |
| `docs/engineering/research.md` | Restructure to R-xxxx entry format, migrate existing content |
| `template/.cursor/agents/po.mdc` | Template copy |
| `template/.cursor/agents/tech-lead.mdc` | Template copy |
| `template/.cursor/agents/curator.mdc` | Template copy |
| `template/.cursor/commands/intake.md` | Template copy |
| `template/.cursor/commands/architecture.md` | Template copy |
| `template/.cursor/commands/research.md` | Template copy |
| `template/.cursor/scratchpad.md` | Template copy (add flag) |
| `template/docs/engineering/research.md` | Template copy (structured format) |

## Risks

| Risk | Mitigation |
|------|------------|
| Web research slows intake/architecture | Flag-controlled (EARLY_RESEARCH). Can be disabled per project. Research is a sub-step, not a full phase. |
| Research quality varies (hallucinated sources) | Entries include optional confidence level and source URLs for user verification. |
| Structured format is overhead for simple findings | Only 3 required fields (ID, date, topic). Minimal friction. |
| Existing research.md content lost during migration | Dev migrates existing US-0023 content to R-0001 entry. |
| R-xxxx ID collisions across parallel agents | IDs auto-increment from the highest existing ID in research.md. Sequential access pattern. |

---

