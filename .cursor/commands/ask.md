---
description: "its-magic ask: answer questions using project context, read-only."
---

# /ask

## Subagents
- (none — uses default agent)

## Inputs (context pack)
Read only the files relevant to the question:
- `docs/engineering/state.md` — current status, progress, known issues
- `docs/product/backlog.md` — all stories with status
- `docs/product/acceptance.md` — what's done, what's remaining
- `docs/engineering/architecture.md` — technical approach and decisions
- `docs/engineering/decisions.md` — decision index
- `docs/engineering/runbook.md` — commands and project config
- `sprints/S*/progress.md` — active sprint progress (latest sprint)
- `.cursor/scratchpad.md` — automation flags and config

## Outputs (artifacts)
- (none — this command is strictly read-only)

## Stop conditions
- (none — answer the question and stop)

## Behavior rules
- Do NOT create, modify, or delete any files.
- Do NOT update state.md or any sprint artifacts.
- Reference stories (US-xxxx), decisions (DEC-xxxx), and tasks (T-xxx) by ID.
- Suggest next actions but do not execute them.
- If the question reveals a bug or feature idea, suggest running `/intake`.

## Steps
1. Read the context files relevant to the user's question.
2. Answer the question using the project's own artifacts as the source of truth.
3. If the answer is not in the artifacts, say so.
