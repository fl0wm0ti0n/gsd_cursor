# UAT — Sprint S0010

## Target

- **US-0038**: Phase-Triggered Sync Policy with Guarded Auto-Push
  - AC-1: Canonical sync policy modes and default non-auto behavior
  - AC-2: Eligibility evaluation only at phase-completion boundaries
  - AC-3: Mandatory `TEST_COMMAND` check before push, including missing/fail/timeout denial
  - AC-4: Optional runbook checks honored when configured and reported clearly
  - AC-5: Feature auto-push forbidden before QA completion
  - AC-6: Auto-push denied when unresolved blocking QA findings exist
  - AC-7: Branch safety deny-by-default unless explicit allowlist
  - AC-8: Deterministic sync evidence and reason-code output
  - AC-9: Validate-and-push scripts remain behaviorally aligned
  - AC-10: Disabled/manual modes remain near-zero overhead and non-disruptive

## Planned verification steps

1. Verify policy mode contract includes `disabled|manual|by_phase|by_milestone|custom_phase_list`.
2. Verify sync eligibility runs only at phase boundaries.
3. Verify push blocks when `TEST_COMMAND` evidence is missing/failing/timed out.
4. Verify optional lint/typecheck/formatter checks run only when configured.
5. Verify pre-QA auto-push is denied for feature work.
6. Verify auto-push is denied when blocking QA findings remain unresolved.
7. Verify auto-push is denied on protected/default branch without allowlist.
8. Verify sync outputs include deterministic reason code and evidence refs.
9. Verify `scripts/validate-and-push.ps1` and `scripts/validate-and-push.sh`
   retain aligned mandatory-test gating behavior.
10. Verify `manual` and `disabled` policy modes do not introduce forced sync overhead.

## Negative-path focus

- Disallowed auto-push due to branch safety constraints.
- Disallowed auto-push due to failed/missing test evidence.
- Disallowed auto-push before QA completion or with unresolved blockers.

## Regression matrix (planned)

| ID | Scenario | Expected decision | Expected reason code |
|----|----------|-------------------|----------------------|
| S0010-UAT-001 | Mode `disabled` at phase boundary | `not_eligible` | `SYNC_DISABLED` |
| S0010-UAT-002 | Mode `manual` at phase boundary | `not_eligible` | `MANUAL_MODE_NO_AUTO` |
| S0010-UAT-003 | `by_phase` mode + `ALLOW_AUTO_PUSH=0` | `blocked` | `AUTO_PUSH_NOT_ENABLED` |
| S0010-UAT-004 | Feature work before QA completion | `blocked` | `PRE_QA_AUTOPUSH_FORBIDDEN` |
| S0010-UAT-005 | Blocking QA findings unresolved | `blocked` | `BLOCKING_QA_FINDINGS` |
| S0010-UAT-006 | Protected/default branch not allowlisted | `blocked` | `BRANCH_NOT_ALLOWLISTED` |
| S0010-UAT-007 | Missing `TEST_COMMAND` | `blocked` | `TEST_COMMAND_MISSING` |
| S0010-UAT-008 | `TEST_COMMAND` failure | `blocked` | `TEST_FAILED` |
| S0010-UAT-009 | `TEST_COMMAND` timeout | `blocked` | `TEST_TIMEOUT` |
| S0010-UAT-010 | Configured lint/typecheck failure | `blocked` | `OPTIONAL_CHECK_FAILED` |
| S0010-UAT-011 | Eligible boundary + all checks pass | `pushed` | `SYNC_PUSHED` |

## Executed verification steps and results

1. **AC-1** - Verified canonical sync policy mode contract includes
   `disabled|manual|by_phase|by_milestone|custom_phase_list` with default non-auto
   behavior (`SYNC_POLICY_MODE=manual`, `ALLOW_AUTO_PUSH=0`).  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `sprints/S0010/summary.md`
2. **AC-2** - Verified sync eligibility evaluation is phase-boundary-only in
   workflow guidance.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `sprints/S0010/summary.md`
3. **AC-3** - Verified mandatory `TEST_COMMAND` gating blocks push when tests
   are missing, failing, or timed out.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `tests/report.md`
4. **AC-4** - Verified optional checks (`LINT_COMMAND`, `TYPECHECK_COMMAND`,
   formatter/lint-fix) are run only when configured and reported with
   deterministic `pass|fail|skipped` semantics.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `docs/engineering/runbook.md`
5. **AC-5** - Verified feature auto-push before QA completion is forbidden and
   only manual sync is allowed pre-QA.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `sprints/S0010/summary.md`
6. **AC-6** - Verified unresolved blocking QA findings force no-push behavior
   with actionable remediation guidance.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `handoffs/qa_to_dev.md`
7. **AC-7** - Verified branch safety constraints are deny-by-default unless
   explicit allowlist configuration is present.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `docs/engineering/runbook.md`
8. **AC-8** - Verified deterministic sync evidence contract includes phase,
   mode, checks, decision, reason code, and evidence references.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `docs/engineering/runbook.md`
9. **AC-9** - Verified behavior parity across
   `scripts/validate-and-push.ps1` and `scripts/validate-and-push.sh` for
   mandatory test gating and optional checks.  
   **Result:** PASS  
   **Evidence:** `sprints/S0010/qa-findings.md`, `sprints/S0010/summary.md`
10. **AC-10** - Verified disabled/manual default modes preserve near-zero
    overhead and existing manual push behavior.  
    **Result:** PASS  
    **Evidence:** `sprints/S0010/qa-findings.md`, `sprints/S0010/summary.md`

## Results summary

- Total steps: 10
- Passed: 10
- Failed: 0
- UAT outcome: **PASS**

## Acceptance criteria traceability

- US-0038 AC-1 -> UAT Step 1 -> PASS
- US-0038 AC-2 -> UAT Step 2 -> PASS
- US-0038 AC-3 -> UAT Step 3 -> PASS
- US-0038 AC-4 -> UAT Step 4 -> PASS
- US-0038 AC-5 -> UAT Step 5 -> PASS
- US-0038 AC-6 -> UAT Step 6 -> PASS
- US-0038 AC-7 -> UAT Step 7 -> PASS
- US-0038 AC-8 -> UAT Step 8 -> PASS
- US-0038 AC-9 -> UAT Step 9 -> PASS
- US-0038 AC-10 -> UAT Step 10 -> PASS
