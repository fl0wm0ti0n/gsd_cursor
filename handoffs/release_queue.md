# Release Queue Tracker

Canonical release queue for sprint-level release state.

## Queue rows

| sprint_id | story_refs | status | last_updated | release_notes_ref | gate_snapshot | release_version | remediation |
|-----------|------------|--------|--------------|-------------------|---------------|-----------------|-------------|
| S0012 | US-0040 | released | 2026-02-26 | handoffs/releases/S0012-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=manual; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers/criticals); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=docs/engineering/runbook.md,tests/report.md,sprints/S0012/qa-findings.md,sprints/S0012/uat.json |  |  |
| S0013 | US-0041 | released | 2026-02-26 | handoffs/releases/S0013-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=manual; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0013/release-findings.md,sprints/S0013/qa-findings.md,sprints/S0013/uat.json |  |  |
| S0015 | US-0043 | released | 2026-02-26 | handoffs/releases/S0015-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0015/release-findings.md,sprints/S0015/qa-findings.md,sprints/S0015/uat.json,docs/product/backlog.md |  |  |
| S0016 | US-0015 | released | 2026-02-26 | handoffs/releases/S0016-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0016/release-findings.md,sprints/S0016/qa-findings.md,sprints/S0016/uat.json |  |  |
| S0017 | US-0044 | released | 2026-02-27 | handoffs/releases/S0017-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0017/release-findings.md,sprints/S0017/qa-findings.md,sprints/S0017/uat.json |  |  |
| S0018 | US-0016 | released | 2026-02-28 | handoffs/releases/S0018-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0018/release-findings.md,sprints/S0018/qa-findings.md,sprints/S0018/uat.json |  |  |
| S0019 | US-0046 | released | 2026-03-01 | handoffs/releases/S0019-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0019/release-findings.md,sprints/S0019/qa-findings.md,sprints/S0019/uat.json |  |  |
| S0020 | US-0047 | released | 2026-03-01 | handoffs/releases/S0020-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0020/release-findings.md,sprints/S0020/qa-findings.md,sprints/S0020/uat.json |  |  |
| S0021 | US-0045 | released | 2026-03-01 | handoffs/releases/S0021-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0021/release-findings.md,sprints/S0021/qa-findings.md,sprints/S0021/uat.json,docs/engineering/status-normalization-report.md |  |  |
| S0022 | US-0033 | released | 2026-03-01 | handoffs/releases/S0022-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0022/release-findings.md,sprints/S0022/qa-findings.md,sprints/S0022/uat.json |  |  |
| S0023 | US-0034 | released | 2026-03-01 | handoffs/releases/S0023-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0023/release-findings.md,sprints/S0023/qa-findings.md,sprints/S0023/uat.json,docs/engineering/compatibility-report.md |  |  |
| S0024 | US-0035 | released | 2026-03-01 | handoffs/releases/S0024-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0024/release-findings.md,sprints/S0024/qa-findings.md,sprints/S0024/uat.json,docs/engineering/component-scope-report.md |  |  |
| S0025 | US-0048 | released | 2026-03-02 | handoffs/releases/S0025-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=manual; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); uat_snapshot=10/10 verified; isolation_snapshot=PASS; push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0025/release-findings.md,sprints/S0025/qa-findings.md,sprints/S0025/uat.json,sprints/S0025/uat.md,handoffs/releases/S0025-release-notes.md |  |  |
| S0026 | US-0031 | released | 2026-03-02 | handoffs/releases/S0026-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=auto; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0026/qa-findings.md,sprints/S0026/uat.json,sprints/S0026/uat.md |  |  |
| S0011 | US-0039 | released | 2026-03-02 | handoffs/releases/S0011-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=manual; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); uat_snapshot=10/10 verified; evidence_refs=tests/report.md,sprints/S0011/qa-findings.md,sprints/S0011/uat.json,sprints/S0011/uat.md,sprints/S0011/release-findings.md |  |  |
| S0027 | US-0032 | released | 2026-03-02 | handoffs/releases/S0027-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=manual; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); uat_snapshot=8/8 verified; isolation_snapshot=PASS; push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0027/release-findings.md,sprints/S0027/qa-findings.md,sprints/S0027/uat.json,sprints/S0027/uat.md,docs/engineering/state.md |  |  |
| S0028 | US-0049 | released | 2026-03-02 | handoffs/releases/S0028-release-notes.md | phase_boundary=release; policy_mode=manual; trigger_source=manual; branch=local; checks=test:pass,lint:skipped,typecheck:skipped; qa_status_snapshot=PASS(no blockers); uat_snapshot=8/8 verified; isolation_snapshot=PASS; push_decision=not_eligible; reason_code=MANUAL_MODE_NO_AUTO; evidence_refs=tests/report.md,sprints/S0028/release-findings.md,sprints/S0028/qa-findings.md,sprints/S0028/uat.json,sprints/S0028/uat.md,handoffs/releases/S0028-release-notes.md,docs/engineering/state.md |  |  |

## Status model

- `planned`: sprint exists, release flow not entered
- `ready`: verify-work completed and release is eligible to start
- `unreleased`: release flow entered; notes written; finalization not completed
- `released`: release finalization completed for the sprint
- `blocked`: deterministic fail-safe condition requiring remediation

## Deterministic transition contract

- Allowed lifecycle: `planned -> ready -> unreleased -> released`.
- `blocked` can be set on deterministic failure conditions.
- Only the target sprint row may change during one `/release` run.
- No destructive auto-reconciliation is allowed by default.

## Fail-safe reason codes

- `RELEASE_SPRINT_UNRESOLVED`
- `LEGACY_NOTES_SPRINT_UNRESOLVED`
- `QUEUE_ENTRY_MISSING`
- `NOTES_REF_MISSING`
- `STATUS_TRANSITION_INVALID`
- `BACKLOG_STATUS_DRIFT`
- `CANONICAL_STATUS_CONFLICT`
- `COMPATIBILITY_CRITICAL_OPEN`
- `COMPONENT_SCOPE_VIOLATION_UNAPPROVED`

## Remediation guidance

- `RELEASE_SPRINT_UNRESOLVED`: set explicit sprint context (`Sxxxx`) and rerun `/release`.
- `LEGACY_NOTES_SPRINT_UNRESOLVED`: preserve legacy notes, identify sprint manually, then create target sprint notes file.
- `QUEUE_ENTRY_MISSING`: create the target sprint queue row with required fields, then rerun `/release`.
- `NOTES_REF_MISSING`: add canonical `release_notes_ref` for target sprint row and rerun `/release`.
- `STATUS_TRANSITION_INVALID`: correct row status to a valid predecessor state and rerun `/release`.
- `BACKLOG_STATUS_DRIFT`: reconcile target story status/ACs in `docs/product/backlog.md` using release evidence, then rerun `/release`.
- `CANONICAL_STATUS_CONFLICT`: resolve canonical backlog status mismatch versus derived artifacts and rerun `/release`.
- `COMPATIBILITY_CRITICAL_OPEN`: resolve or explicitly decide on open critical compatibility findings before rerun.
- `COMPONENT_SCOPE_VIOLATION_UNAPPROVED`: resolve or explicitly approve out-of-scope component impact before rerun.
