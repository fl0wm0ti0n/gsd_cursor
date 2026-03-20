# Sprint S0001 — Summary

## Goal

Implement Smart Upgrade Mode (US-0018) and document empty runbook commands (US-0015).

## Result

All 11 tasks completed. `--mode upgrade` is implemented across all three installers (PS1, sh, py), the JS CLI, and both test suites.

## Changes

### New files
- `template/.its-magic-version` — version tracking placeholder (0.0.0)

### Modified files
- `bin/its-magic.js` — accepts `upgrade` mode, updated help text and examples
- `installer.ps1` — Classify-File function, upgrade branch, version tracking, summary output
- `installer.sh` — classify_file function, upgrade branch, version tracking, summary output
- `installer.py` — classify_file function, upgrade branch, version tracking, summary output
- `tests/run-tests.ps1` — upgrade scenario test added
- `tests/run-tests.sh` — upgrade scenario test added
- `README.md` — upgrade section, --mode upgrade in options table, runbook note
- `template/README.md` — same as root README

## Stories completed
- US-0018: Smart Upgrade Mode (AC-1 through AC-5, AC-7, AC-8)
- US-0015: Document empty runbook commands

## Deferred
- AC-6 (upgrade from pre-version repos): deferred per sprint plan

## Context refresh pack (2026-03-22 — post S0050 / US-0071)

- Latest released sprint: **`S0050`** for **`US-0071`** (`DEC-0053`); state hot-surface
  rollover: **12** oldest checkpoints → `docs/engineering/state-archive/state-pack-20260322.md`
  (**39** retained on hot surface; `STATE_HOT_MAX_LINES=1200`).
- Next OPEN story: **`US-0072`** — resume at **`/discovery`** (see `handoffs/resume_brief.md`).
- Compact decision index: `docs/engineering/decisions.md` — **Current context pack (2026-03-22 — post S0050 / US-0071)**.

## Context refresh pack (2026-03-21 — post S0049 / US-0070)

- Latest released sprint: **`S0049`** for **`US-0070`** (`DEC-0052`); state hot-surface
  rollover: **11** oldest checkpoints → `docs/engineering/state-archive/state-pack-20260321.md`
  (41 retained on hot surface; `STATE_HOT_MAX_LINES=1200`).
- Next OPEN story: **`US-0071`** — resume at **`/discovery`** (see `handoffs/resume_brief.md`).
- Compact decision index: `docs/engineering/decisions.md` — **Current context pack (2026-03-21 — post S0049 / US-0070)**.

## Context refresh pack (2026-03-21)

- Latest released sprint: **`S0048`** for **`US-0069`** (`DEC-0051`); state hot-surface
  rollover archived to `docs/engineering/state-archive/state-pack-20260320.md`.
- Next OPEN story: **`US-0070`** — resume at **`/discovery`** (see `handoffs/resume_brief.md`).
- Compact decision index refreshed in `docs/engineering/decisions.md` (context pack dated 2026-03-21).

## Context refresh pack (2026-03-16)

- Latest finalized sprint: `S0044` for `US-0065` (released).
- Current in-flight sprint: `S0045` for `US-0066` (`/execute` complete).
- Execute evidence:
  - `sprints/S0045/summary.md`
  - `handoffs/dev_to_qa.md` (S0045 section)
  - `docs/engineering/state.md` (execute checkpoint + strict runtime proof tuple)
- Remaining OPEN stories by priority:
  - `US-0066`, `US-0067`, `US-0068` (all `P1`).
- Auto progression status: `US-0066` advanced through `/execute`; continuation should proceed to `/qa`.
- Recommended next phase: `/qa` for `S0045` (`US-0066`).

## Execute loop remediation (2026-03-16)

- Target: `S0045` / `US-0066` QA blocker from `handoffs/qa_to_dev.md`.
- Fix: reconciled sprint artifact status mismatch by updating
  `sprints/S0045/progress.md` to `T-001..T-010` done, aligned with
  `sprints/S0045/tasks.md` and `sprints/S0045/summary.md`.
- Handoff refreshed: `handoffs/dev_to_qa.md` now includes execute-loop
  remediation context for QA rerun.
