# PO to TL archive pack (2026-03-31)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 41
- First archived heading: `## Intake Addendum — Lifecycle QA Expansion for Installer + CLI`
- Last archived heading: `## Intake Addendum — Post-QA Release Findings Workflow`
- Verification tuple (mandatory):
  - archived_body_lines=60
  - retained_body_lines=785

---

## Intake Addendum — Lifecycle QA Expansion for Installer + CLI

### New intake

User requests deeper live QA for installation lifecycle behavior, including:
- install/update flows via `its-magic` command
- overwrite + backup behavior
- clean-repo safety (no accidental deletion of non-framework files)
- parity across PowerShell/shell/CI paths

### Overlap and duplicate evaluation

- Existing overlap:
  - `US-0008` (CLI installer) provides feature implementation.
  - current tests provide baseline install/upgrade checks.
- Gap identified:
  - missing full end-to-end lifecycle verification for clean-repo safety,
    CLI/direct-installer parity, and negative-path fail-fast behavior.
- Decision:
  - create focused QA expansion story `US-0041` (already added to backlog) to
    avoid mixing feature semantics with test-hardening scope.

### Accepted story

#### US-0041 — End-to-End Lifecycle QA for `its-magic` Install/Upgrade/Clean
- Priority: P1
- Status: OPEN
- Intent: increase release confidence with deterministic lifecycle coverage for
  install, overwrite+backup, upgrade, clean-repo safety, and invalid-argument paths.

### TL guidance and boundaries

- In scope:
  - lifecycle E2E test matrix for installer and CLI invocation paths
  - temp-dir isolation/idempotency guarantees in test scripts
  - platform parity subset in CI (`npm-test`, `brew-test`, `choco-test`)
  - README/runbook lifecycle QA documentation updates
- Out of scope:
  - redesigning installer behavior
  - introducing new installer modes or runtime deployment changes

---

## Intake Addendum — Post-QA Release Findings Workflow

### New intake

User requested an official workflow for issues found after QA at release gates,
with documentation symmetry to QA findings.

### Accepted story

#### US-0042 — Release Findings Artifact and Post-QA Issue Workflow
- Priority: P1
- Status: DONE
- Intent: ensure post-QA release issues are captured deterministically in a
  dedicated artifact + handoff path.

---

