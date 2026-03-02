---
description: "its-magic QA: test plan, findings, verify fixes."
---

# /qa

## Subagents
- qa

## Execution model
- Run `/qa` in a fresh QA subagent context.
- After writing outputs, stop and hand off to `/execute` (if issues) or
  `/verify-work` (if clear) in a new subagent/chat.
- Each QA pass in the implementation loop must be a new QA subagent.

## Isolation evidence write requirement (US-0048 / DEC-0029)

At the end of `/qa`, append an isolation evidence entry to
`docs/engineering/state.md`:

- `phase_id=qa`
- `role=qa`
- `fresh_context_marker=<new marker for this subagent>`
- `timestamp=<ISO UTC>`
- `evidence_ref=<primary output ref>` (recommended: `sprints/Sxxxx/qa-findings.md` and/or `handoffs/qa_to_dev.md`)

In an execute↔QA implementation loop (`AUTO_IMPLEMENTATION_LOOP=1`), each new
`/qa` cycle must have a new `fresh_context_marker` (marker reuse is treated as
stale isolation evidence).

## Inputs
- `handoffs/dev_to_qa.md`
- `sprints/S0001/summary.md`

## Outputs (artifacts)
- `sprints/S0001/qa-findings.md`
- `handoffs/qa_to_dev.md` (if issues)
- `docs/engineering/state.md`

## Stop conditions
- Critical defects require decision
- Missing test plan coverage

## Release gate prerequisite (US-0039)

QA completion evidence is required before `/release` may proceed. Record findings in
`sprints/Sxxxx/qa-findings.md`; unresolved blocking findings block release with
`RELEASE_QA_BLOCKERS_OPEN`. When clear, handoff to `/verify-work` so release gate can
verify no unresolved blockers.

## Steps
0. If `SECURITY_REVIEW=1`, verify `docs/engineering/security-review.md` exists
   and has no unresolved `critical` findings before proceeding. If unresolved
   critical findings exist, stop at a decision gate.
1. Define a test plan and run verification using the runbook commands
   (`TEST_COMMAND`, `LINT_COMMAND`, `TYPECHECK_COMMAND` in `docs/engineering/runbook.md`).
   - `TEST_COMMAND` is mandatory baseline evidence for push eligibility.
   - Optional checks run only when configured and should be reported as
     `pass|fail|skipped` deterministically.
2. Record findings and severity.
   - Explicitly classify blockers that must prevent auto-push:
     unresolved blocking QA findings and unresolved critical issues.
3. Update state and handoff to dev if needed.
   - For sync-policy evidence, include deterministic `reason_code` guidance:
     - `PRE_QA_AUTOPUSH_FORBIDDEN` (feature work before QA completion)
     - `BLOCKING_QA_FINDINGS` (open blockers/criticals)
     - `SYNC_PUSHED` (eligible + checks passed + branch safe)
4. If `AUTO_IMPLEMENTATION_LOOP=1` and blocking issues exist, handoff to dev and
   return to `/execute` automatically (bounded by `AUTO_LOOP_MAX_CYCLES`).
5. Follow with `/verify-work` for user acceptance when blocking issues are closed.
6. If `AUTO_PAUSE_REQUEST=1` at safe boundary, run `/pause` before next phase.
7. Before pushing, suggest running `scripts/validate-and-push` to catch failures
   locally before they reach CI. If CI fails, the auto-fix job in
   `.github/workflows/ci.yml` attempts automatic lint/format fixes and retries.
8. Optional compatibility observability QA checks (US-0034):
   - If `CROSS_REPO_OBSERVABILITY=0`, add zero required compatibility overhead.
   - If `CROSS_REPO_OBSERVABILITY=1`, verify compatibility artifacts exist and
     are current (`docs/engineering/compatibility-signals.md`,
     `docs/engineering/compatibility-report.md`) with traceable references to
     story/sprint/task context.
   - If unresolved critical compatibility findings exist and
     `COMPATIBILITY_GATE_ON_CRITICAL=1`, mark as release-blocking and require
     decision gate before `/release`.
9. Optional component-scope protection checks (US-0035):
   - If `COMPONENT_SCOPE_MODE=0`, add zero required protection overhead.
   - If `COMPONENT_SCOPE_MODE=1`, verify unaffected-component protection checks
     for declared `non_target_components` and record evidence in
     `docs/engineering/component-scope-report.md`.
   - If unapproved out-of-scope impact is detected, mark as blocking and require
     decision gate before `/release`.
10. Optional spec-pack verification (US-0031):
   - If `SPEC_PACK_MODE=0`, add no required spec-pack checks (zero overhead).
   - If `SPEC_PACK_MODE=1`, verify target-story spec-pack artifacts exist and
     required sections are populated; report gaps in qa-findings; see runbook
     for minimum sections and traceability.
11. Optional user-guide verification (US-0032):
   - If `USER_GUIDE_MODE=0`, add no required user-guide checks or blocking (zero overhead).
   - If `USER_GUIDE_MODE=1`, verify target-story user guide exists at
     `docs/user-guides/US-xxxx.md` and required sections are present; report
     gaps in qa-findings; see runbook for minimum schema.

