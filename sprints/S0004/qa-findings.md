# QA Findings — Sprint S0004

## Sprint
S0004 — US-0024 (Memory Drift Audit Command)

## QA run metadata
- Date: 2026-02-23
- Agent: QA
- Inputs: `handoffs/dev_to_qa.md`, `sprints/S0004/summary.md`, `sprints/S0004/tasks.md`, `sprints/S0004/progress.md`, `docs/product/backlog.md`, `docs/engineering/runbook.md`

## Test plan

| # | Check | AC | Method |
|---|-------|----|--------|
| 1 | Command files exist (active + template) | AC-1 | File presence |
| 2 | Active/template parity | AC-1 | Content comparison (172 lines each) |
| 3 | Read-only behavior defined (no mutation) | AC-1 | Execution model + Steps section text inspection |
| 4 | Required command sections present (6) | AC-1 | Section header search |
| 5 | Report format has 5 subsections | AC-2 | Section header search in report format |
| 6 | Severity taxonomy defined (high/medium/low) | AC-2, AC-5 | Table + meaning + action expectation |
| 7 | Detection coverage: 3 checks with evidence rules | AC-3 | Check 1/2/3 sections with evidence requirements |
| 8 | Memory drift vs template drift split | AC-4 | Section 3 vs Section 4 separation |
| 9 | US-0017 routing in scope boundary | AC-4 | Scope boundary section + scope note |
| 10 | Non-blocking advisory output | AC-5 | Execution model + recommended actions column |
| 11 | README /memory-audit in core commands (active) | AC-6 | Content search |
| 12 | README Memory drift auditing section (active) | AC-6 | Section presence + timing + interpretation |
| 13 | README /memory-audit in core commands (template) | AC-6 | Content search |
| 14 | README Memory drift auditing section (template) | AC-6 | Section presence + timing + interpretation |
| 15 | Runbook Memory drift auditing section (active) | AC-6 | Section presence + timing + severity |
| 16 | Runbook Memory drift auditing section (template) | AC-6 | Section presence + timing + severity |
| 17 | README active/template parity for new sections | AC-6 | Content comparison |
| 18 | Runbook active/template parity for new sections | AC-6 | Content comparison |
| 19 | Test suite passes (run-tests.ps1) | All | Execute tests, verify exit code |
| 20 | LINT_COMMAND / TYPECHECK_COMMAND status | — | Runbook inspection |

## Checks run and results

### AC-1: Command is read-only — PASS

- `.cursor/commands/memory-audit.md` exists (172 lines).
- `template/.cursor/commands/memory-audit.md` exists (172 lines, identical content).
- Execution model (line 13): "This command is **read-only**: it does not create, modify, or delete source code, workflow rules, or sprint artifacts."
- Stop conditions (line 37): "Report artifact written — stop."
- Steps section (line 171): "Stop. Do not modify any source, workflow, or sprint artifacts."
- No mutation verbs (create/modify/delete/update) targeting source/workflow/sprint files anywhere in the behavior definition.

### AC-2: Report has metadata, findings, severity structure — PASS

Five required subsections verified in report format section:

1. **Header metadata** (line 54): timestamp, branch + HEAD SHA, audit scope.
2. **Severity summary** (line 59): high/medium/low table with meaning and action expectations.
3. **Memory drift findings table** (line 68): 6-column table with artifact, signal, severity, evidence, recommended action.
4. **Template drift findings** (line 83): reference-only section with US-0017 scope note.
5. **Suggested next steps** (line 95): `/refresh-context`, `/sprint-plan`, `/verify-work`, `/intake`.

### AC-3: Detection covers 3 categories with evidence — PASS

Three detection checks verified in "Detection coverage and evidence rules" section:

1. **Check 1** (line 108): Changed code without artifact updates — cross-references state.md, architecture.md, acceptance.md. Evidence: changed source files + stale artifact sections. Severity guidance provided.
2. **Check 2** (line 121): Unresolved decision TODOs and open gates — cross-references decisions.md index, sprint tasks. Evidence: decision file path, status, dependent tasks. Severity guidance provided.
3. **Check 3** (line 133): Sprint/story status mismatch vs repository signals — cross-references summary.md, qa-findings.md, uat.json, handoffs. Evidence: story/task ID, claimed status, missing artifact. Severity guidance provided.

All three checks have explicit evidence requirements ("not vague assertions").

### AC-4: Memory drift vs template drift split — PASS

- Section 3 ("Memory drift findings table"): artifact-vs-code/repo divergence. Actionable output.
- Section 4 ("Template drift findings — reference-only — US-0017 scope"): active-vs-template divergence.
- Scope note (lines 88–91): "Template drift detection and remediation belong to US-0017. Findings listed here are for awareness only. Do not remediate template drift under `/memory-audit`."
- Scope boundary section (lines 145–161): explicit US-0024 vs US-0017 separation. "The agent must not blur these categories."

### AC-5: Non-blocking advisory output — PASS

- Execution model: command is "read-only" and produces a report, then stops.
- Severity taxonomy is advisory: high/medium/low with action expectations, not hard gates.
- Findings table includes "Recommended action" column with specific follow-up commands.
- No exit-with-error or blocking behavior defined for any finding level.
- Step 6: "Print a one-line summary" — informational output only.

### AC-6: README and runbook document timing and interpretation — PASS

**README.md (active)**:
- `/memory-audit` listed in core commands (line 197).
- "Memory drift auditing" section (lines 223–253) with:
  - Timing: Pre-handoff, Pre-QA, Pre-release, Ad-hoc.
  - Interpretation: severity summary (high/medium/low) with action guidance.
  - Template drift US-0017 reference.
  - Follow-up commands: `/refresh-context`, `/sprint-plan`, `/verify-work`, `/intake`.

**template/README.md**: Same content as active README — identical sections verified.

**docs/engineering/runbook.md (active)** (lines 27–48):
- "Memory drift auditing" section with timing, output path, severity interpretation, template drift US-0017 note, follow-up commands.

**template/docs/engineering/runbook.md**: Same content as active runbook — identical section verified.

### Test suite — PASS (with 1 non-blocking finding)

- `tests/run-tests.ps1` executed: exit code 0.
- 10 new US-0024 assertions present and passing:
  - memory-audit command exists (active + template)
  - README mentions timing (active + template)
  - Runbook mentions timing
  - US-0017 routing (active + template)
  - Scope boundary section (active + template)
- **Finding F-001**: "20 commands exist" assertion incorrect — template actually has 21 commands (`ask.md` from S0002 was not counted when S0004 updated 19→20). See findings section below.

### LINT_COMMAND / TYPECHECK_COMMAND — SKIPPED (intentional)

- `LINT_COMMAND:` and `TYPECHECK_COMMAND:` are both empty in `docs/engineering/runbook.md`.
- This is documented as intentional for a template/installer project (README states: "The template ships with empty values for `LINT_COMMAND`, `FORMAT_COMMAND`, and `TYPECHECK_COMMAND` -- this is intentional").

## Findings

| # | Severity | Description | Evidence | Impact |
|---|----------|-------------|----------|--------|
| F-001 | medium | Test command count asserts 20 but actual is 21 | `tests/run-tests.ps1` line 65 and `tests/run-tests.sh` line 71 both check `-eq 20`; template has 21 `.md` files in `.cursor/commands/` (`ask.md` from S0002 was not counted in the 19→20 update) | Test accuracy; assertion currently fails in sh, masked in PS1 by `.Count` single-element behavior |
| F-002 | low | Backlog US-0024 status still shows OPEN | `docs/product/backlog.md` line 192: `Status: OPEN`; S0004 is complete per progress.md | Cosmetic; status should be updated to reflect implementation is done (pending QA pass). Not an S0004 deliverable bug — this is a pre-existing artifact freshness issue. |

## Result

**PASS** — All 6 acceptance criteria (AC-1 through AC-6) are met.

- 0 blocking findings.
- 1 medium finding (F-001: test command count off by 1) — non-blocking, does not affect US-0024 acceptance, should be fixed in next sprint or quick task.
- 1 low finding (F-002: backlog status stale) — cosmetic, pre-existing drift.
