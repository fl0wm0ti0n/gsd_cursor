# Sprint S0001

## Goal
Implement smart upgrade mode (`--mode upgrade`) for the its-magic installer so users can safely update framework files without losing project data.

## Scope
- **In scope**: US-0018 (smart upgrade mode) — all 8 acceptance criteria.
- **In scope**: US-0015 (document empty runbook commands) — small doc task, bundled for efficiency.
- **Out of scope**: US-0016 (Homebrew version sync) — happens during next release, not dev work.
- **Out of scope**: US-0017 (template drift guard) — separate effort, deferred.

## Risks
- Triple installer parity: PS1 implemented first, then ported to sh and py. Divergence caught by tests.
- File classification edge cases: new files in future versions, renamed files. Mitigated by defaulting unknowns to framework.
- Mixed file detection (scratchpad.md) may produce false positives if user hasn't customized it. Low impact — just a warning message.

## Definition of Done
- `--mode upgrade` works in all three installers (PS1, Bash, Python).
- `.its-magic-version` written on every install/upgrade.
- Framework files updated, user data preserved, mixed files warned.
- Upgrade summary printed after completion.
- New files delivered regardless of category.
- Tests cover upgrade scenario in both test runners.
- README documents the upgrade workflow.
- All existing tests still pass.
