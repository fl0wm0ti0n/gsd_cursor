# Sprint S0002

## Goal
Add lightweight interaction channel (/ask) and critical evaluation behavior to /intake and /architecture, so the AI challenges ideas before accepting them and users can ask questions without full workflow overhead.

## Scope
- **In scope**: US-0020 (/ask command) — 5 acceptance criteria.
- **In scope**: US-0021 (Critical evaluation in intake/architecture) — 7 acceptance criteria.
- **In scope**: US-0022 (Sprint sizing rules + scratchpad config) — 7 acceptance criteria.
- **Out of scope**: US-0016 (Homebrew version sync) — release task, not dev work.
- **Out of scope**: US-0017 (template drift guard) — separate effort.

## Risks
- Over-gatekeeping in /intake: evaluation must be constructive, not blocking (AC-7).
- Template/active drift: every file change must update both copies in the same task.
- /ask context pack may be expensive if all files are read for simple questions — mitigated by "read only what's needed" rule.

## Definition of Done
- `/ask` command exists and answers questions without modifying files.
- `/intake` evaluates ideas (duplicate check, feasibility, alternatives, scope) before creating stories.
- `/architecture` challenges design assumptions before accepting them.
- PO and Tech Lead agent definitions updated with evaluation/challenge rules.
- `/sprint-plan` evaluates scope and proposes splitting when work exceeds configurable threshold.
- Scratchpad has SPRINT_MAX_TASKS and SPRINT_AUTO_SPLIT options.
- Both active and template copies updated for all changed files.
- README documents /ask as lightweight interaction channel.
