# Architecture

## Overview

US-0018 adds a fourth installer mode (`--mode upgrade`) that safely updates its-magic framework files in a target repo while preserving user data files. The design introduces three new concepts: file classification, version tracking, and an upgrade flow algorithm.

The existing installer architecture (Node.js CLI wrapper → OS-specific installer script → file copy loop) remains unchanged. Upgrade mode is an additional branch in the existing mode switch, using the same file listing and copy infrastructure.

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

# US-0028: Security & Compliance Review Agent

## Overview

US-0028 adds an optional 7th agent role (security reviewer) and `/security-review`
command, activated via scratchpad flags. When enabled, the security agent
reviews at two workflow points: post-architecture (design review) and
post-execute (code review). When disabled (default), zero workflow overhead.

Findings go to `docs/engineering/security-review.md`. Critical findings create
decision records and block progression via the existing decision gate pattern.

Per DEC-0012, this is a dedicated agent role rather than augmented behavior on
existing agents.

## Assumption challenges

**Is a 7th agent the right granularity?** Yes (DEC-0012). Security expertise is
a distinct "hat" — mixing it with TL or QA dilutes both. The flag mechanism
ensures zero overhead when disabled. Follows established one-role-per-agent
pattern.

**How do compliance profiles work?** They're prompt-embedded checklists in the
agent definition, not external data sources. Each profile maps to a set of
review questions the agent evaluates. Consistent with the framework's philosophy:
AI-driven guidance, not automated scanning.

**Can this be simpler?** This is already minimal: one agent, one command (two
modes), two flags, one output file. No external tooling, no automated SAST, no
custom parsers.

## Design

### 1) Security agent definition (`security.mdc`)

```
You are the Security Reviewer. Evaluate architecture and code for security
risks and compliance alignment.
You start in a fresh agent context for this phase.

Inputs (design review mode):
- docs/engineering/architecture.md
- docs/engineering/decisions.md
- docs/engineering/state.md
- COMPLIANCE_PROFILES from .cursor/scratchpad.md

Inputs (code review mode):
- Current sprint tasks and implementation files
- docs/engineering/architecture.md
- COMPLIANCE_PROFILES from .cursor/scratchpad.md

Outputs:
- docs/engineering/security-review.md
- decisions/DEC-xxxx.md (for critical findings)

Rules:
- Review scope is guidance-based: architectural patterns, data flows, auth
  design, common vulnerability patterns. Not line-by-line static analysis.
- Use compliance profiles as review checklists when COMPLIANCE_PROFILES is set.
- When COMPLIANCE_PROFILES is empty, apply general security best practices.
- Critical findings (severity: critical) must create a DEC-xxxx record and
  flag a decision gate. Workflow pauses until resolved.
- Non-critical findings (severity: high/medium/low) are documented in
  security-review.md with remediation guidance.
- Use only artifact files as context, not prior chat history.
- After writing findings, stop. Next phase resumes in a new subagent/chat.
```

### 2) `/security-review` command with two modes

**Design review mode** (post-architecture):

```
Inputs: architecture.md, decisions.md, COMPLIANCE_PROFILES
Review scope:
- Architecture decisions for security implications
- Data flow and storage patterns
- Authentication and authorization design
- Third-party dependency risk
- Profile-specific requirements (when profiles set)
```

**Code review mode** (post-execute):

```
Inputs: sprint tasks, implementation files, architecture.md, COMPLIANCE_PROFILES
Review scope:
- Secrets/credentials in code or config
- Injection vulnerabilities (SQL, XSS, command)
- Authentication/authorization implementation gaps
- Input validation and output encoding
- Profile-specific implementation requirements
```

Command steps:

```
1. Read SECURITY_REVIEW and COMPLIANCE_PROFILES from scratchpad.md.
2. If SECURITY_REVIEW=0, exit with "Security review is disabled."
3. Determine mode: design review (if architecture just completed) or
   code review (if execute just completed). Mode can also be specified
   explicitly by the user.
4. Load review inputs for the selected mode.
5. If COMPLIANCE_PROFILES is set, load profile-specific checklists.
6. Evaluate against security criteria and profile requirements.
7. Write findings to docs/engineering/security-review.md with severity,
   affected components, and remediation guidance.
8. For critical findings: create DEC-xxxx record, flag decision gate.
9. Update docs/engineering/state.md with review status.
```

### 3) Workflow integration points

When `SECURITY_REVIEW=1`, `/auto` spawns the security agent at two points:

```
... -> architecture -> [security-review: design] -> sprint-plan -> ...
... -> execute -> [security-review: code] -> QA -> ...
```

Integration in `/auto` command steps (conditional):

```
- After architecture phase: if SECURITY_REVIEW=1, spawn security agent
  in design review mode before proceeding to sprint-plan.
- After execute phase: if SECURITY_REVIEW=1, spawn security agent in
  code review mode before proceeding to QA.
```

Integration in `/qa` command (reference):

```
- If SECURITY_REVIEW=1, check that security-review.md exists and has no
  unresolved critical findings before proceeding.
```

When `SECURITY_REVIEW=0` (default), these steps are skipped entirely.

### 4) Compliance profile mechanism

Profiles are prompt-embedded checklists. `COMPLIANCE_PROFILES` is a
comma-separated scratchpad value. When set, the security agent applies
profile-specific review criteria in addition to general security best practices.

| Profile | Key review areas |
|---------|-----------------|
| GDPR | Data minimization, consent flows, right to erasure, data processing agreements, cross-border data transfers |
| SOC2 | Access controls, audit logging, change management, availability monitoring, incident response |
| HIPAA | PHI handling, encryption at rest/transit, access controls, audit trails, business associate agreements |
| PCI-DSS | Cardholder data protection, network segmentation, encryption, access control, logging/monitoring |
| ISO27001 | Information security policy, risk assessment, access control, cryptography, operations security |

Profiles are NOT certifications. The security-review.md output explicitly
states that findings are AI-guided review, not compliance certification.
Human expert review is recommended for production compliance.

### 5) Scratchpad flags

New flags in `.cursor/scratchpad.md`:

```
# Security review
# - SECURITY_REVIEW: 0|1 (enable optional security review, default: off)
# - COMPLIANCE_PROFILES: comma-separated (e.g., GDPR,SOC2; empty = general)
SECURITY_REVIEW=0
COMPLIANCE_PROFILES=
```

Default is OFF — zero overhead for projects that don't need security review.

### 6) Critical findings → decision records

When the security agent identifies a critical finding:

1. Create a `decisions/DEC-xxxx.md` entry describing the vulnerability,
   affected components, risk assessment, and remediation options.
2. Set finding status to "blocking" in `security-review.md`.
3. The workflow pauses at a decision gate (consistent with existing escalation
   pattern) until the user resolves the finding.
4. Resolution options: fix the issue, accept the risk (with documented
   rationale), or defer with a mitigation plan.

This integrates with the existing decision gate pattern from `core.mdc` and
the escalation rules.

### 7) Security review output format

`docs/engineering/security-review.md` structure:

```markdown
# Security Review

## Review metadata
- Date: YYYY-MM-DD
- Mode: design|code
- Sprint: Sxxxx (code review only)
- Profiles: [list or "general"]

## Findings

### [severity: critical|high|medium|low] — [title]
- **Component**: [affected area]
- **Description**: [what was found]
- **Risk**: [impact if unaddressed]
- **Remediation**: [recommended fix]
- **Status**: [open|resolved|accepted|deferred]
- **Decision**: [DEC-xxxx reference, critical only]

## Summary
- Critical: N
- High: N
- Medium: N
- Low: N
- Overall: pass|fail (fail if any critical unresolved)
```

## File changes required

| File | Change |
|------|--------|
| `.cursor/agents/security.mdc` | New: security reviewer agent definition |
| `.cursor/commands/security-review.md` | New: command with design/code review modes |
| `.cursor/commands/auto.md` | Add conditional security review steps at two integration points |
| `.cursor/commands/qa.md` | Add reference to check security-review.md for unresolved criticals |
| `.cursor/scratchpad.md` | Add SECURITY_REVIEW=0 and COMPLIANCE_PROFILES= flags |
| `.cursor/rules/core.mdc` | Add security review to phase flow (conditional) |
| `docs/engineering/security-review.md` | New: placeholder for security review findings |
| `template/.cursor/agents/security.mdc` | Template copy |
| `template/.cursor/commands/security-review.md` | Template copy |
| `template/.cursor/commands/auto.md` | Template copy |
| `template/.cursor/commands/qa.md` | Template copy |
| `template/.cursor/scratchpad.md` | Template copy (add flags) |
| `template/docs/engineering/security-review.md` | Template copy (placeholder) |

## Risks

| Risk | Mitigation |
|------|------------|
| Security agent scope creep (tries to be SAST) | Agent definition constrains to architectural and pattern-level review. Not line-by-line static analysis. |
| False sense of security from compliance profiles | Output explicitly states findings are AI-guided review, not certification. Recommends human expert for production compliance. |
| Critical findings block workflow unnecessarily | User can "accept risk" to unblock, with documented rationale. Decision gate pattern already supports this. |
| Compliance profiles are shallow/generic | Profiles are guidance frameworks. They surface relevant questions, not definitive answers. Quality improves over time as prompts are refined. |
| Template/active file drift | All new files require template copies. Noted in file changes table for Dev. |

---

# US-0034: Multi-Repo and Contract Compatibility Observability

## Overview

US-0034 adds optional compatibility observability across repositories and
components using manifest artifacts and contract-change signals. The goal is
deterministic impact visibility for planning, QA, and release decisions, not
runtime dependency orchestration.

This architecture follows the user clarification:
- Keep a global view for inventory and cross-repo links.
- Keep per-repo and per-component manifests close to each codebase.
- Surface API changes directly to dependent repos/components so agents can
  derive required work.

## Minimal manifest model

### A1) Global registry manifest (inventory + links)

Canonical artifact:
- `docs/engineering/manifests/registry.manifest.yaml`

Purpose:
- Source-of-truth inventory of known repos/components.
- Cross-repo contract dependency links.
- Ownership and lifecycle visibility.

Minimum required fields:
- `schema_version`
- `generated_at`
- `repos[]`: `{ repo_id, repo_url_or_path, owner, status, manifest_ref }`
- `contracts[]`: `{ contract_id, producer_repo, producer_component, contract_ref, version }`
- `compatibility_links[]`: `{ contract_id, consumer_repo, consumer_component, expected_version_range, criticality }`

### A2) Per-repo manifest

Canonical artifact (inside each repo):
- `docs/engineering/manifests/repo.manifest.yaml`

Purpose:
- Local declaration of exposed and consumed contracts.
- Repo-level owner/version/status metadata.

Minimum required fields:
- `schema_version`
- `repo_id`
- `owner`
- `version`
- `components[]` (references to component manifests)
- `exports[]` (contracts this repo publishes)
- `imports[]` (contracts this repo consumes)

### A3) Per-component manifest

Canonical artifact:
- `docs/engineering/manifests/components/<component_id>.manifest.yaml`

Purpose:
- Unit of scoped change analysis and protection checks.

Minimum required fields:
- `component_id`
- `repo_id`
- `owner`
- `status` (`active|deprecated|experimental|retired`)
- `exposed_contracts[]` (`contract_id`, `api_spec_ref`, `version`)
- `consumed_contracts[]` (`contract_id`, `expected_version_range`)
- `protected_interfaces[]` (interfaces expected to remain stable for non-target work)

### A4) Compatibility map and contract links

Compatibility is represented as producer->consumer edges in
`registry.manifest.yaml.compatibility_links[]`, with each edge tied to a
specific `contract_id` and expected consumer version range.

This creates a deterministic impact graph:
- Contract changes from producer side identify all consumer edges.
- Each edge yields a candidate impact task in sprint planning.

### A5) Change signal model (contract diff + impact)

Canonical artifact:
- `docs/engineering/compatibility-signals.md`

Each signal entry records one observed contract change:
- `signal_id` (`CS-xxxx`)
- `date`
- `story_id`
- `producer_repo` / `producer_component`
- `contract_id`
- `from_version` / `to_version`
- `change_type` (`additive|behavioral|breaking|docs-only`)
- `impacted_consumers[]`
- `severity` (`info|low|medium|high|critical`)
- `required_actions[]` (for impacted repos/components)
- `status` (`open|planned|validated|accepted-risk|resolved`)

Severity baseline:
- `breaking` with impacted consumers -> `high` (or `critical` for
  production-critical links).
- `behavioral` -> `medium`.
- `docs-only` drift -> `low`.

## Workflow integration

### B1) Phase responsibilities

| Phase | Manifest/compatibility responsibilities |
|------|------------------------------------------|
| `/intake` | If enabled, declare target repos/modules and contract artifacts in story scope. |
| `/architecture` | Define/confirm registry and local manifest updates; create compatibility approach and risk policy. |
| `/sprint-plan` | Convert compatibility links + open change signals into explicit tasks per impacted consumer. |
| `/execute` | Update local manifests when contracts/components change; append contract-change signals. |
| `/qa` | Validate impacted consumer coverage and verify signal statuses/evidence. |
| `/verify-work` | Confirm traceability from story -> signals -> tasks -> QA evidence. |
| `/release` | Apply compatibility gate only when enabled and unresolved high/critical findings exist. |
| `/refresh-context` | Curator compacts stale signals, verifies manifest consistency, and updates state summary. |

### B2) Impact derivation model for agents

When a contract change is detected, agents derive work deterministically:
1. Find `contract_id` in `registry.manifest.yaml`.
2. Enumerate `compatibility_links` for consumers.
3. For each consumer edge, create/verify tasks:
   - contract alignment update,
   - consumer regression/smoke verification,
   - docs alignment if public API docs changed.
4. Record findings in `compatibility-report.md` and link to story/sprint tasks.

### B3) Findings and gating policy

Canonical compatibility findings artifact:
- `docs/engineering/compatibility-report.md`

Minimum finding fields:
- `finding_id`
- `story_id`
- `contract_id`
- `producer` + `consumer`
- `severity`
- `evidence`
- `recommended_action`
- `gate_recommendation` (`none|decision-gate`)

Gate behavior:
- Default: non-blocking advisory output.
- If `CROSS_REPO_OBSERVABILITY=1` and unresolved `critical` findings exist,
  trigger decision gate before release progression.

### B4) Default-off / zero-overhead behavior

Control flags in `.cursor/scratchpad.md`:
- `CROSS_REPO_OBSERVABILITY=0` (default)
- `COMPATIBILITY_GATE_ON_CRITICAL=1` (effective only when observability is on)

When `CROSS_REPO_OBSERVABILITY=0`:
- No required manifest processing.
- No required compatibility report updates.
- No additional blocking gates.

## Artifacts and status taxonomy

Canonical files:
- `docs/engineering/manifests/registry.manifest.yaml`
- `docs/engineering/manifests/repo.manifest.yaml`
- `docs/engineering/manifests/components/<component_id>.manifest.yaml`
- `docs/engineering/compatibility-signals.md`
- `docs/engineering/compatibility-report.md`

Status taxonomy:
- Manifest entity status: `active|deprecated|experimental|retired`
- Signal status: `open|planned|validated|accepted-risk|resolved`
- Finding severity: `info|low|medium|high|critical`

---

# US-0035: Component-Scoped Execution Mode with Protection Guards

## Overview

US-0035 introduces an optional scoped-execution mode for multi-component repos.
The mode constrains planning and implementation to declared target components
while requiring explicit protection checks for non-target components.

## Component scope model

### C1) Scope declaration contract

Canonical declaration artifact:
- `docs/engineering/component-scope.md`

Minimum required fields per scoped story:
- `story_id`
- `scope_mode` (`off|on`)
- `target_components[]`
- `non_target_components[]`
- `allowed_interface_touch[]` (explicitly permitted cross-component interfaces)
- `out_of_scope_constraints[]`
- `approval_policy` (who can approve scope expansion)

Scratchpad controls:
- `COMPONENT_SCOPE_MODE=0` (default off)
- `TARGET_COMPONENTS=` (comma-separated defaults for current cycle; optional)

### C2) Non-target protection model

When scope mode is enabled:
- `/sprint-plan` requires each task to include:
  - `target_component_ids`
  - `expected_impacted_interfaces`
- `/execute` enforces scope-first behavior:
  - no intentional edits outside targets unless escalation is approved
- `/qa` requires unaffected-component checks for `non_target_components`:
  - smoke/regression confirmation
  - compatibility signal review for unintended interface impact

Evidence destination:
- `docs/engineering/component-scope-report.md`

### C3) Decision-gate trigger conditions

Trigger decision gate when all conditions are true:
1. `COMPONENT_SCOPE_MODE=1`
2. Out-of-scope component impact is detected
3. Impact is not listed in `allowed_interface_touch[]`
4. No prior approval record exists in decisions/handoff artifacts

Gate outcomes:
- approve scope expansion (update scope artifact + tasks),
- split into separate story/sprint,
- rollback/defer cross-component change.

## Workflow integration (scoped mode)

| Phase | Scoped-mode behavior |
|------|-----------------------|
| `/intake` | Declare in-scope vs out-of-scope components. |
| `/architecture` | Define expected interface touch and protection strategy. |
| `/sprint-plan` | Require component-tagged tasks and impact assumptions. |
| `/execute` | Enforce target-only execution unless approved escalation. |
| `/qa` | Verify target outcomes plus non-target protection checks. |
| `/verify-work` | Confirm scope evidence coverage before pass recommendation. |
| `/release` | If unapproved out-of-scope impact remains, hold via decision gate. |

Default-off behavior:
- If `COMPONENT_SCOPE_MODE=0`, no extra required declarations/checks/gates.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Scope metadata becomes stale | Require `/sprint-plan` refresh of scope file each sprint. |
| False-positive out-of-scope alarms | Allow explicit `allowed_interface_touch[]` declarations. |
| Teams bypass non-target checks | QA checklist requires component-scope report evidence when mode is on. |

---

# US-0036: Official Remote Config Template, Docs, and Fail-Fast Validation

## Overview

US-0036 defines a canonical remote execution configuration contract and
validation behavior for optional remote workflows. The architecture is
process-level only: it specifies artifact contract, checks, error reporting,
and documentation expectations. It does not introduce a runtime transport
implementation.

Primary goals:
- Safe default-off behavior (`REMOTE_EXECUTION=0`) with zero required overhead.
- Deterministic fail-fast validation when remote mode is enabled.
- Clear, actionable error messages and security guardrails.

## Minimal architecture

### 1) Canonical contract artifact and parity

Canonical file path:
- Active repo: `.cursor/remote.json`
- Template copy: `template/.cursor/remote.json`

Parity rule:
- Both files represent the same contract shape and semantics.
- Placeholder values remain non-secret examples only.
- Any contract field changes must update active + template docs and references
  in the same change set.

### 2) Contract model (schema-level)

`remote.json` is a strict JSON object with explicit required and optional
fields. Suggested minimal shape:

```json
{
  "version": 1,
  "defaultTarget": "local-docker",
  "targets": [
    {
      "id": "local-docker",
      "type": "docker",
      "enabled": true,
      "host": "127.0.0.1",
      "port": 2375,
      "workspaceRoot": "/workspace",
      "auth": {
        "mode": "env",
        "tokenEnv": "REMOTE_DOCKER_TOKEN"
      }
    }
  ]
}
```

Validation contract:
- Required root fields: `version`, `defaultTarget`, `targets`.
- Required target fields: `id`, `type`, `enabled`, `host`, `port`,
  `workspaceRoot`.
- `type` allowed values: `docker`, `ssh`, `vm`.
- `auth.mode` allowed values: `none`, `env`.
- If `auth.mode=env`, environment variable references are required (for example
  `tokenEnv`) and inline secrets are forbidden.
- `defaultTarget` must match an existing enabled target id.

### 3) Validation model (mode-aware)

Validation trigger:
- Run remote config validation only when `REMOTE_EXECUTION=1`.
- Skip all remote config checks when `REMOTE_EXECUTION=0`.

Failure policy:
- Enabled mode (`REMOTE_EXECUTION=1`): fail fast on first blocking issue and
  stop the phase with remediation guidance.
- Disabled mode (`REMOTE_EXECUTION=0`): no blocking behavior and no extra
  required steps.

Validation classes:
1. Presence: configured path exists.
2. Syntax: valid JSON parse.
3. Contract: required fields/types/enums.
4. Semantics: cross-field checks (default target exists/enabled, unique ids).
5. Security: deny secret-like inline values in config.

### 4) Error reporting model

All validation failures must be actionable and include:
- failing location (`path`, for example `targets[0].port`)
- expected rule (`integer 1..65535`)
- actual value/type
- remediation hint

Message pattern:
`[REMOTE_CONFIG_ERROR] <path>: expected <rule>, got <actual>. Fix: <hint>.`

Examples:
- `[REMOTE_CONFIG_ERROR] .cursor/remote.json: file not found. Fix: create from template/.cursor/remote.json or set REMOTE_EXECUTION=0.`
- `[REMOTE_CONFIG_ERROR] targets[1].type: expected one of [docker, ssh, vm], got "k8s". Fix: use a supported type or extend contract in a new decision record.`
- `[REMOTE_CONFIG_ERROR] targets[0].auth.token: inline secret-like value detected. Fix: use auth.mode=env and reference tokenEnv.`

### 5) Security model

Security posture:
- Never commit tokens, passwords, private keys, or API secrets in
  `.cursor/remote.json`.
- Only commit environment-variable references (for example `tokenEnv`,
  `passwordEnv`, `privateKeyPathEnv`) or safe placeholders.
- Treat any secret-like literal in config as validation failure when remote is
  enabled.

Scope boundary:
- In scope: configuration contract and safety guidance.
- Out of scope: external secret manager integration or transport protocol work.

### 6) Docs integration model

Documentation updates required by design:
- `README.md`: user-facing remote setup, two target examples, and mode behavior
  (`REMOTE_EXECUTION` off/on).
- `docs/engineering/runbook.md`: operator-oriented validation contract,
  fail-fast expectations, and troubleshooting messages.

Doc parity expectation:
- README and runbook must describe the same contract and failure behavior with
  no contradictions.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split cleanly into:
1. Create canonical active/template `remote.json` artifacts with safe examples.
2. Document contract schema and allowed values.
3. Implement/define validation checks and error message contract.
4. Add security guidance and secret-prohibition checks.
5. Update README and runbook with remote setup + mode-specific expectations.
6. Verify parity across active/template files and docs references.

---

# US-0037: Mid-Process `/auto` Continuation with Deterministic Resume Point

## Overview

US-0037 adds deterministic continuation semantics for `/auto` so teams can
restart from mid-process with one command and continue remaining phases without
manual phase triggers. The design is workflow-level orchestration only. It does
not change phase deliverables, decision gates, or runtime product behavior.

## Assumption challenge and alternatives

### Option A: Keep implicit behavior only

Pros:
- No command contract changes.
- Lowest immediate implementation effort.

Cons:
- Resume behavior stays inference-heavy and non-deterministic.
- Ambiguous source resolution can silently choose the wrong phase.
- Does not satisfy ACs for explicit `start-from`, fail-fast conflicts, and
  inspectable breadcrumbs.

### Option B: Resume-only continuation (no `/auto start-from`)

Pros:
- Simpler than full unification.
- Reuses `resume_brief.md` as primary source.

Cons:
- No explicit operator override for urgent/manual recovery cases.
- Still weak when resume brief is stale/missing and state fallback is needed.
- Splits semantics across `/resume` and `/auto` instead of one deterministic
  control model.

### Option C: Unified deterministic model (chosen)

Pros:
- Explicit `/auto start-from=<phase>` override for intentional control.
- Deterministic source precedence when no override.
- Fail-fast on ambiguity/staleness/conflict rather than guessing.
- One-command continuation through remaining phases with existing stop rules.

Cons:
- Slightly more command/rule documentation work.
- Requires explicit conflict/error contract and breadcrumb schema.

## Minimal architecture

### 1) Canonical phase IDs and validation

Accepted canonical IDs for `start-from`:
- `intake`
- `discovery`
- `research`
- `architecture`
- `sprint-plan`
- `plan-verify`
- `execute`
- `qa`
- `verify-work`
- `release`
- `refresh-context`

Validation policy:
- Unknown/non-canonical phase -> fail fast.
- Alias forms are not accepted in v1 (`sprint_plan`, `verifywork`, etc.) to
  keep behavior deterministic.

### 2) Deterministic resume-source precedence

When `/auto` is invoked, resolve start phase in strict order:

1. **Explicit override**: command argument `start-from=<phase>`.
2. **Resume brief source**: `handoffs/resume_brief.md` intended resume phase.
3. **State fallback source**: infer next phase from `docs/engineering/state.md`.
4. **Fail-fast**: if unresolved, ambiguous, conflicting, or stale.

Deterministic rule:
- Once a higher-priority source resolves validly, lower sources are ignored for
  phase selection (but can still be used for consistency checks and warnings).

### 3) Conflict and staleness policy

Resolver outcomes:
- `resolved`: exactly one valid phase source selected by precedence.
- `conflict`: sources disagree and no explicit override exists.
- `stale`: source exists but points to an invalid/outdated context.
- `missing`: required data not present.
- `ambiguous`: multiple possible phases inferred from same source.

Policy:
- If explicit `start-from` is valid, proceed and record that it overrides other
  sources.
- If no explicit override and `resume_brief` conflicts with `state` inference:
  fail fast with actionable remediation.
- If `resume_brief` exists but is stale/unparseable, do not silently skip to
  state; fail fast and request cleanup or explicit override.
- Use `state` fallback only when `resume_brief` is genuinely absent.
- If state inference is ambiguous/unrecoverable, fail fast.

### 4) Error messaging contract (fail-fast)

All resolver failures must return a structured message contract:

`[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`

Required codes:
- `INVALID_START_FROM`
- `RESUME_BRIEF_MISSING`
- `RESUME_BRIEF_STALE`
- `RESUME_BRIEF_UNPARSEABLE`
- `RESUME_STATE_CONFLICT`
- `STATE_PHASE_AMBIGUOUS`
- `STATE_PHASE_UNRECOVERABLE`

Examples:
- `[AUTO_RESUME_ERROR] INVALID_START_FROM: "planverify" is not a canonical phase. Source=argument. Fix: use one of [intake..refresh-context].`
- `[AUTO_RESUME_ERROR] RESUME_STATE_CONFLICT: resume_brief=qa, state_inferred=verify-work. Source=resolver. Fix: run /resume to reconcile artifacts or rerun /auto start-from=<phase>.`

### 5) State fallback inference contract

`docs/engineering/state.md` fallback is intentionally conservative:
- Infer from latest explicit boundary/checkpoint statements that indicate
  "ready for <phase>" or "paused at <phase>".
- If multiple candidate phases are present in latest state slice, mark
  ambiguous and fail.
- If no trustworthy boundary phrase exists, mark unrecoverable and fail.

This keeps inference deterministic and avoids hidden heuristics.

### 6) One-command continuation flow (remaining phases only)

After phase resolution, `/auto` executes remaining phases in canonical order,
starting at resolved phase, preserving existing behavior:
- Fresh subagent per phase.
- Existing execute/QA loop behavior when `AUTO_IMPLEMENTATION_LOOP=1`.
- Existing optional security review steps when `SECURITY_REVIEW=1`.
- Existing stop conditions remain unchanged:
  - decision gate
  - missing critical input
  - pause request (`AUTO_PAUSE_REQUEST=1` at safe boundary)
  - loop max cycles reached

No gate bypass is allowed in continuation mode.

### 7) Observability and breadcrumb contract

Continuation must write deterministic breadcrumbs to artifacts so behavior is
auditable.

Minimum breadcrumb fields:
- `invocation_mode` (`auto`)
- `requested_start_from` (value or `none`)
- `resolved_start_phase`
- `resolution_source` (`argument|resume_brief|state_fallback`)
- `resolution_status` (`resolved|fail-fast`)
- `stop_reason` (`completed|decision_gate|missing_input|pause_request|loop_max`)
- `stop_phase`
- `timestamp`

Artifact update targets:
- `docs/engineering/state.md`: append a concise continuation checkpoint summary.
- `handoffs/resume_brief.md` (when stopped before completion): update intended
  resume phase plus stop reason and last completed phase.

### 8) Backward compatibility and safe defaults

- Existing manual workflows remain unchanged.
- `/resume` continues to work for context loading and status reporting.
- `/auto` gains explicit deterministic continuation behavior only when invoked.
- If no explicit `start-from` is provided, legacy users still get automatic
  continuation — now with deterministic source policy and fail-fast safety.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split into:
1. Define parser/validator for `start-from` canonical phase IDs.
2. Implement precedence resolver with strict conflict/staleness outcomes.
3. Implement fail-fast error message contract and user remediation text.
4. Implement conservative `state.md` inference helper with ambiguity handling.
5. Wire continuation flow to existing stop conditions (no behavior bypass).
6. Add breadcrumb writing contract to `state.md` and `resume_brief.md`.
7. Align `/auto`, `/resume`, `/pause` command guidance and template parity.

---

# US-0038: Phase-Triggered Sync Policy with Guarded Auto-Push

## Overview

US-0038 defines workflow-level sync policy semantics at phase boundaries. The
goal is deterministic and safe synchronization behavior with zero-overhead
defaults when automation is disabled. This architecture does not implement a
runtime git orchestrator; it defines policy contracts, gates, and artifacts.

## Assumption challenge and alternatives

### Option A: Always auto-push after every phase

Pros:
- Simple to explain.
- Frequent backups to remote.

Cons:
- Violates QA-first safety for feature work.
- High risk of pushing unstable/incomplete changes.
- Conflicts with teams that intentionally stay manual.

### Option B: Manual sync only

Pros:
- Maximum user control and least automation risk.
- Already compatible with existing workflow habits.

Cons:
- No deterministic cadence policy when teams want guarded automation.
- Misses requested phase/milestone trigger model.

### Option C: Policy-driven guarded auto-sync (chosen)

Pros:
- Supports disabled/manual/by-phase/by-milestone/custom modes.
- Enforces mandatory pre-push checks and QA-first restrictions.
- Preserves manual behavior and keeps default non-disruptive.

Cons:
- More policy/evidence fields to maintain in artifacts.

## Minimal architecture

### 1) Sync policy control model

Canonical policy object (stored in workflow artifacts/command context):
- `mode`: `disabled|manual|by_phase|by_milestone|custom_phase_list`
- `custom_phases[]`: canonical phase IDs (used only in `custom_phase_list`)
- `allow_auto_push`: `0|1` (default `0`)
- `auto_push_branch_allowlist[]`: explicit branch names/patterns allowed for
  auto-push
- `optional_checks_enabled`: inferred from runbook command presence

Mode semantics:
- `disabled`: no policy evaluation and no sync attempts.
- `manual`: only user-invoked sync; no auto-triggered sync.
- `by_phase`: evaluate eligibility on every phase-completion boundary.
- `by_milestone`: evaluate only at milestone completion boundary.
- `custom_phase_list`: evaluate only when completed phase matches configured
  list.

Default-safe posture:
- Default mode is non-auto (`manual` or `disabled`).
- If unset/invalid, fail closed to `manual`.

### 2) Guarded auto-push eligibility model

Policy evaluation runs only at phase completion boundaries. A sync attempt is
eligible only when all conditions are true:
1. Boundary trigger matches configured mode.
2. `allow_auto_push=1`.
3. QA-first guard passes for feature work:
   - before QA pass, auto-push is forbidden;
   - manual user-invoked sync is still allowed.
4. No unresolved blocking QA findings / critical unresolved issues.
5. Branch safety guard passes (see below).
6. Mandatory pre-push check chain passes.

If any condition fails, result is deterministic `no_push` with reason code.

### 3) Branch safety constraints

Auto-push branch policy:
- Deny auto-push to protected/default branches by default.
- Allow auto-push only on explicitly allowlisted branches.
- If branch is unknown/unclassified, fail closed (no auto-push).
- Manual push behavior remains unchanged and user-controlled.

### 4) Mandatory pre-push check chain

Pre-push chain order (deterministic):
1. `TEST_COMMAND` (mandatory baseline).
2. `LINT_COMMAND` (if configured and non-empty).
3. `TYPECHECK_COMMAND` (if configured and non-empty).

Rules:
- Missing/blank `TEST_COMMAND` blocks push.
- Test failure/timeout blocks push.
- Optional checks are skipped only when not configured.
- Optional check failures block push when configured.
- Result details must show which checks ran, skipped, passed, or failed.

This aligns with existing `validate-and-push` scripts where tests are already
required before push.

### 5) Observability and evidence artifacts

Canonical sync evidence destination:
- `docs/engineering/state.md` (session status + latest gate verdict)
- `handoffs/dev_to_qa.md` or phase handoff context as needed

Recommended structured entry fields per sync attempt:
- `sync_id` (`SYNC-xxxx`)
- `timestamp`
- `phase_boundary`
- `policy_mode`
- `trigger_source` (`manual|auto`)
- `branch`
- `checks` (`test`, `lint`, `typecheck` with `pass|fail|skipped`)
- `qa_status_snapshot`
- `push_decision` (`pushed|blocked|not_eligible`)
- `reason_code`
- `evidence_refs` (paths to runbook/sprint findings/test reports)

Reason code examples:
- `SYNC_DISABLED`
- `MANUAL_MODE_NO_AUTO`
- `PRE_QA_AUTOPUSH_FORBIDDEN`
- `BLOCKING_QA_FINDINGS`
- `BRANCH_NOT_ALLOWLISTED`
- `TEST_COMMAND_MISSING`
- `TEST_FAILED`
- `OPTIONAL_CHECK_FAILED`
- `SYNC_PUSHED`

### 6) Compatibility constraints

- Keep existing stop conditions and decision gate behavior unchanged.
- Preserve manual mode semantics; no forced push path is introduced.
- Keep optional runbook checks optional; only `TEST_COMMAND` is mandatory.
- Maintain active/template behavioral parity for command/rule/doc updates.

## Sprint-plan readiness (decomposition-ready)

Implementation should split into:
1. Define sync policy schema + defaults in workflow docs/command guidance.
2. Add phase-boundary eligibility evaluation contract and reason codes.
3. Define branch safety deny/allowlist policy for auto-push.
4. Align pre-push check contract with runbook commands and script semantics.
5. Add deterministic sync evidence format to state/handoff artifacts.
6. Add QA scenarios for pre-QA auto-push denial, check failures, and
   disabled/manual zero-overhead behavior.
7. Enforce active + `template/` parity for all touched behavior docs.

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
