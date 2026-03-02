# Sprint S0028 Summary — US-0049 Legacy DONE-Story Acceptance/Traceability Backfill Guard

## Delivered

1. **Detection rule (T-001 / AC-1)**  
   Documented in `docs/engineering/runbook.md`: legacy drift = backlog DONE and (acceptance unchecked OR traceability/state lacks entry OR release artifacts lack representation).

2. **Bounded target-scoped repair (T-002 / AC-2)**  
   Runbook and release guard: only stories matching the detection rule are mutated; no broad rewrite of unrelated artifacts.

3. **Audit report (T-003 / AC-3)**  
   Canonical path `docs/engineering/legacy-drift-audit.md` with required fields: story_id, prior_acceptance_state, prior_traceability_state, resolved_state, reason_code, evidence_ref, timestamp. Created in repo and in template.

4. **Reason codes (T-004 / AC-4)**  
   `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation in runbook and in release fail-safe list (active + template).

5. **One-time backfill (T-005 / AC-5)**  
   Documented in runbook: explicit trigger, detection over DONE stories, target-scoped repair, append audit; idempotent when no drift.

6. **Ongoing guard (T-006 / AC-6)**  
   Release step 3e: legacy drift guard at release/reconciliation; block with reason code or target-scoped repair with audit append; deterministic and documented (active + template).

7. **Template parity (T-007 / AC-7)**  
   `template/docs/engineering/runbook.md`, `template/.cursor/commands/release.md`, and `template/docs/engineering/legacy-drift-audit.md` aligned with active for backfill, guard, audit path, and reason codes.

8. **Regression (T-008 / AC-8)**  
   `tests/run-tests.ps1`: 14 assertions for canonical audit path, runbook section, reason codes, idempotent no-drift, release guard step (active + template). Pass 397, Fail 0.

## Files changed

- `docs/engineering/runbook.md` — US-0049 section (detection, audit, reason codes, backfill, guard)
- `docs/engineering/legacy-drift-audit.md` — new (schema + placeholder entries)
- `.cursor/commands/release.md` — step 3e, three reason codes
- `template/docs/engineering/runbook.md` — same US-0049 section
- `template/.cursor/commands/release.md` — step 3e, three reason codes
- `template/docs/engineering/legacy-drift-audit.md` — new (parity)
- `tests/run-tests.ps1` — block #27 US-0049 regression
- `sprints/S0028/tasks.md`, `progress.md`, `summary.md`, `uat.md`, `uat.json`
- `docs/engineering/state.md` — execute checkpoint + isolation evidence
- `handoffs/dev_to_qa.md` — S0028 handoff section

## Test result

- `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`: **PASS** (Pass: 397, Fail: 0).  
- Evidence: `tests/report.md` (Timestamp: 2026-03-02T21:56:25Z).

## Blockers

None.

## Ready for /qa

Yes. QA can verify US-0049 AC-1..AC-8 per checklist in `handoffs/dev_to_qa.md`.
