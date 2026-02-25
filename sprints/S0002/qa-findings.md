# QA Findings — Sprint S0002

## Test plan

1. Active/template parity check for all 8 file pairs
2. Content verification against acceptance criteria (19 AC across 3 stories)
3. Installer compatibility check (new ask.md file picked up correctly)
4. README documentation check

## Parity check

| # | File pair | Result |
|---|-----------|--------|
| 1 | ask.md | IDENTICAL |
| 2 | po.mdc | IDENTICAL |
| 3 | tech-lead.mdc | IDENTICAL |
| 4 | intake.md | IDENTICAL |
| 5 | architecture.md | IDENTICAL |
| 6 | sprint-plan.md | IDENTICAL |
| 7 | scratchpad.md | 1 expected diff (AUTO_RELEASE_NOTES=1 vs 0) |
| 8 | scratchpad.local.example.md | IDENTICAL |

**Result**: PASS. All S0002 changes are in sync. The scratchpad diff is a pre-existing project-level override, not introduced by this sprint.

## Acceptance criteria verification

### US-0020: /ask command

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | Command exists, read-only | PASS | ask.md has "Outputs: (none)", behavior rules say "Do NOT create, modify, or delete" |
| AC-2 | Context pack loaded | PASS | 8 context files listed in Inputs section |
| AC-3 | References by ID | PASS | Behavior rule: "Reference stories (US-xxxx), decisions (DEC-xxxx), and tasks (T-xxx) by ID" |
| AC-4 | Works for questions/status/how | PASS | Steps cover question answering; no type restriction |
| AC-5 | Documented in README | PASS | /ask in core commands list + "Lightweight interaction" section in both READMEs |

### US-0021: Critical evaluation

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | PO checks for duplicates | PASS | po.mdc evaluation rule 1: "Check backlog.md for duplicates or overlapping stories" |
| AC-2 | PO evaluates feasibility | PASS | po.mdc evaluation rule 2: "Evaluate feasibility" + rule 3: "Suggest alternatives" |
| AC-3 | PO challenges assumptions | PASS | po.mdc evaluation rule 5: "Challenge assumptions constructively" |
| AC-4 | /intake steps updated | PASS | intake.md has 4 steps, step 1 is "Evaluate" |
| AC-5 | /architecture steps updated | PASS | architecture.md has 4 steps, step 1 is "Challenge" |
| AC-6 | Agent definitions updated | PASS | po.mdc has 5 evaluation rules, tech-lead.mdc has 3 challenge rules |
| AC-7 | Constructive, not blocking | PASS | po.mdc says "user always has the final say. If the user says 'do it anyway,' proceed." Behavioral — verified by rule text. |

### US-0022: Sprint sizing

| AC | Description | Status | Evidence |
|----|-------------|--------|----------|
| AC-1 | TL has sizing rules | PASS | tech-lead.mdc "Sprint sizing" section with SPRINT_MAX_TASKS, auto-split, /quick routing |
| AC-2 | /sprint-plan evaluates scope | PASS | sprint-plan.md step 1: "Evaluate scope" + stop condition for exceeding threshold |
| AC-3 | Scratchpad has options | PASS | SPRINT_MAX_TASKS=12 and SPRINT_AUTO_SPLIT=1 in scratchpad.md |
| AC-4 | New idea routing | PASS | tech-lead.mdc: "When a new idea arrives during an active sprint, recommend: add/defer/quick" |
| AC-5 | Milestone breakdown | PASS | sprint-plan.md step 1: "propose splitting into multiple sprints or milestones" |
| AC-6 | Active + template updated | PASS | Parity check passed for all pairs |
| AC-7 | Sensible defaults | PASS | SPRINT_MAX_TASKS=12 default, SPRINT_AUTO_SPLIT=1 default |

## Installer compatibility

The new `ask.md` is under `.cursor/commands/` which is already in `includePaths` and classified as `framework` in all three installers. No changes needed — the file will be automatically copied and upgraded correctly.

## Observations

### OBS-001 (Low): tech-lead.mdc references `sprints/S0001/*`
The Tech Lead outputs section still says `sprints/S0001/*` instead of the generic `sprints/Sxxxx/*`. This is a pre-existing cosmetic issue, not introduced by S0002.

## Bugs found

None.

## Result

**PASS** — All 19 acceptance criteria verified. No bugs found. No blocking issues.
