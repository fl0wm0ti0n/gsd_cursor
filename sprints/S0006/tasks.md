# Tasks — Sprint S0006

## US-0029: Knowledge Curation & Early Research

### T-001: Restructure research.md with R-xxxx entry format and migrate existing content
- Story: US-0029
- Status: pending
- Files: `docs/engineering/research.md`
- Description: Restructure `docs/engineering/research.md` from free-form prose
  to the structured R-xxxx entry format per DEC-0011. Migrate existing US-0023
  research content to R-0001 entry with required fields (ID, date, topic) and
  applicable optional fields (findings, linked stories/decisions, status).
  Add a file header explaining the entry schema and auto-increment convention.
- AC covered: AC-4, AC-9
- Notes: This is the foundation task. All subsequent tasks depend on this schema.

### T-002: Update /research command for structured R-xxxx output
- Story: US-0029
- Status: pending
- Files: `.cursor/commands/research.md`
- Description: Update `/research` command steps to produce structured R-xxxx
  entries. Steps become: (1) identify research topics from product vision,
  backlog, and acceptance criteria, (2) search the web for relevant patterns,
  libraries, APIs, and risks, (3) persist each finding as an R-xxxx entry in
  docs/engineering/research.md, (4) record any decisions triggered by research
  and update state. Auto-increment ID from highest existing entry.
- AC covered: AC-3
- Depends on: T-001

### T-003: Update PO agent with early research behavior
- Story: US-0029
- Status: pending
- Files: `.cursor/agents/po.mdc`
- Description: Add early research sub-step to the PO evaluation section. When
  `EARLY_RESEARCH=1` in scratchpad.md, PO searches the web for relevant context
  (competitor approaches, library docs, API references, prior art) before
  evaluating the idea. Persists findings as an R-xxxx entry in research.md.
  References the entry ID in handoffs/po_to_tl.md. When `EARLY_RESEARCH=0`,
  skip the research sub-step. `/research` command remains available manually
  regardless of flag.
- AC covered: AC-1
- Depends on: T-001

### T-004: Update /intake command with research sub-step
- Story: US-0029
- Status: pending
- Files: `.cursor/commands/intake.md`
- Description: Add research sub-step within step 1 (Evaluate). Step 1 becomes:
  (a) check backlog for duplicates, assess feasibility, suggest alternatives,
  (b) if `EARLY_RESEARCH=1`, search the web for relevant context and persist
  findings as R-xxxx entry in research.md, (c) reference research in evaluation
  reasoning, (d) present evaluation and recommendation — user decides.
- AC covered: AC-1, AC-5
- Depends on: T-003

### T-005: Update Tech Lead agent with early research behavior
- Story: US-0029
- Status: pending
- Files: `.cursor/agents/tech-lead.mdc`
- Description: Add early research sub-step to the TL design challenge section.
  When `EARLY_RESEARCH=1` in scratchpad.md, TL searches the web for technical
  references (framework docs, pattern comparisons, performance benchmarks,
  security considerations) before challenging design assumptions. Persists
  findings as an R-xxxx entry in research.md. References entry IDs in
  architecture decisions and DEC-xxxx records. When `EARLY_RESEARCH=0`, skip.
- AC covered: AC-2
- Depends on: T-001

### T-006: Update /architecture command with research sub-step
- Story: US-0029
- Status: pending
- Files: `.cursor/commands/architecture.md`
- Description: Add research sub-step within step 1 (Challenge). Step 1 becomes:
  (a) if `EARLY_RESEARCH=1`, search for technical references and persist as
  R-xxxx entry in research.md, (b) question design assumptions ("what's the
  alternative?"), (c) check for simpler approaches ("can this be simpler?"),
  (d) inventory risks for each architectural choice.
- AC covered: AC-2, AC-5
- Depends on: T-005

### T-007: Update Curator agent with research knowledge base maintenance
- Story: US-0029
- Status: pending
- Files: `.cursor/agents/curator.mdc`
- Description: Add research knowledge base to curator's maintenance scope.
  During `/refresh-context`: review docs/engineering/research.md for freshness,
  mark entries as "outdated" if sources are stale or context has changed,
  consolidate duplicate entries (point newer to older or merge), flag entries
  not linked to any active story/decision for potential pruning.
- AC covered: AC-7
- Depends on: T-001

### T-008: Add EARLY_RESEARCH scratchpad flag
- Story: US-0029
- Status: pending
- Files: `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`
- Description: Add `EARLY_RESEARCH=1` flag to `.cursor/scratchpad.md` under a
  "Knowledge curation" comment section. Add the same flag with documentation
  to `.cursor/scratchpad.local.example.md` so users see the new option.
  Default is ON (1). Users who want faster workflows without research can
  set to 0. `/research` command always works regardless of flag value.
- AC covered: AC-8

### T-009: Template parity for all US-0029 changes
- Story: US-0029
- Status: pending
- Files:
  - `template/.cursor/agents/po.mdc`
  - `template/.cursor/agents/tech-lead.mdc`
  - `template/.cursor/agents/curator.mdc`
  - `template/.cursor/commands/intake.md`
  - `template/.cursor/commands/architecture.md`
  - `template/.cursor/commands/research.md`
  - `template/.cursor/scratchpad.md`
  - `template/docs/engineering/research.md`
- Description: Copy all US-0029 active file changes to their template
  counterparts. Ensure every modification made in T-002 through T-008 is
  reflected in the corresponding template/ file. Template research.md gets
  the structured format header and empty entry schema (no R-0001 migration
  content — templates are clean starting points).
- AC covered: AC-10
- Depends on: T-001 through T-008
- Notes: Execute after all active file tasks are complete to ensure copies
  are accurate. Template research.md should have the structured format header
  but no populated entries (templates start clean).

### T-010: Update docs and cross-reference verification
- Story: US-0029
- Status: pending
- Files: `docs/engineering/state.md`, `docs/engineering/decisions.md`
- Description: Update engineering state with sprint completion status. Verify
  that R-xxxx entry IDs are referenceable across agents by confirming agent
  definitions and command steps reference the R-xxxx format. Update decisions
  index if DEC-0011 is not already listed. Ensure cross-referencing guidance
  is present in the research.md header.
- AC covered: AC-6
- Depends on: T-001 through T-009

## Implementation order and constraints

- Execute tasks in sequence: T-001 → T-010.
- T-001 is the foundation — establishes the R-xxxx schema that all other tasks
  reference.
- T-003/T-004 (PO agent + /intake) and T-005/T-006 (TL agent + /architecture)
  are paired — each agent update should be followed by its command update.
- T-009 (template parity) must execute after T-002 through T-008 to capture
  all active file changes.
- T-010 (docs/verification) is the final cleanup task.
- Auto-increment R-xxxx IDs from the highest existing ID in research.md.
- All agent updates must gracefully skip research when EARLY_RESEARCH=0.
- Reference DEC-0011 for the entry schema in all research-producing tasks.
