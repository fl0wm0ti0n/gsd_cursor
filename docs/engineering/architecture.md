# Architecture

## Overview

US-0018 adds a fourth installer mode (`--mode upgrade`) that safely updates its-magic framework files in a target repo while preserving user data files. The design introduces three new concepts: file classification, version tracking, and an upgrade flow algorithm.

The existing installer architecture (Node.js CLI wrapper → OS-specific installer script → file copy loop) remains unchanged. Upgrade mode is an additional branch in the existing mode switch, using the same file listing and copy infrastructure.

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
tests, QA completion, or UAT completeness are missing/stale/failing.

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

### 1) Deterministic release gate order

Release gate sequence is fixed:
1. **Check-in test gate** (`TEST_COMMAND` evidence)
2. **QA completion gate** (no unresolved blocking findings)
3. **UAT completion gate** (verified/populated artifacts)
4. **Release notes + runbook update steps**

No later gate is evaluated as pass if an earlier mandatory gate fails.

### 2) Mandatory evidence prerequisites

Gate 1: Check-in tests
- Requires latest relevant check-in test evidence marked pass.
- Fail when evidence is missing, stale, failing, or unverifiable.
- Uses deterministic failure reason and remediation guidance.

Gate 2: QA completion
- Requires QA artifacts showing no unresolved blocking findings in current sprint
  context.
- Fail when blocking findings are open or QA evidence is absent.

Gate 3: UAT completion
- Existing UAT verified-state contract remains mandatory.
- Fail when artifacts are placeholder/incomplete or unresolved fail states exist.

### 3) No-bypass default and explicit override path

Default behavior:
- No bypass for test/QA/UAT gates.

Override behavior (exception-only):
- Allowed only through explicit decision gate.
- Must record rationale, approver, scope, and risk acceptance in decision
  artifacts.
- Release output must mark override as non-default path.

### 4) Observability and traceable gate verdicts

Canonical release gate evidence destinations:
- `handoffs/release_notes.md`
- `docs/engineering/state.md`

Per-gate verdict record fields:
- `release_gate_id` (`RG-xxxx`)
- `timestamp`
- `gate_name` (`checkin_test|qa|uat`)
- `status` (`pass|fail|override`)
- `reason_code`
- `evidence_refs` (artifact paths)
- `remediation`
- `decision_ref` (required for overrides)

Reason code examples:
- `RELEASE_TEST_EVIDENCE_MISSING`
- `RELEASE_TEST_EVIDENCE_STALE`
- `RELEASE_TEST_FAILED`
- `RELEASE_QA_BLOCKERS_OPEN`
- `RELEASE_QA_EVIDENCE_MISSING`
- `RELEASE_UAT_INCOMPLETE`
- `RELEASE_UAT_FAILED`
- `RELEASE_GATE_OVERRIDE_APPROVED`
- `RELEASE_READY`

### 5) Compatibility constraints

- Keep existing workflow stop conditions and escalation semantics.
- Preserve teams with blank optional lint/typecheck commands from false failures.
- Keep release blocked only on mandatory test + QA + UAT evidence.
- Maintain active/template parity across release/qa/execute guidance.

## Sprint-plan readiness (decomposition-ready)

Implementation should split into:
1. Update `/release` gate contract with strict ordered gates.
2. Define freshness/validity criteria for "latest check-in test" evidence.
3. Add QA evidence contract checks for unresolved blockers.
4. Preserve and tighten UAT verified-state gate wording.
5. Add structured gate verdict logging to release notes/state artifacts.
6. Define explicit decision-gate override template and constraints.
7. Add QA regression matrix with positive/negative and stale-evidence cases.

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
