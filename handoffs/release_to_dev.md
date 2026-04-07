# Release -> Dev Handoff — Sprint S0070 (BUG-0008) — **BLOCKED**

## Status

- Result: **BLOCKED** (`2026-04-04T23:30:00Z`)
- Sprint: `S0070`
- Bug: `BUG-0008`

## Blocking reason (active)

- Primary reason codes: **`RELEASE_UAT_INCOMPLETE`**, **`RELEASE_TEST_FAILED`**, prior **`OPERATOR_PUBLISH_AND_E2E_MISSING`**
- Summary: Mandatory **`/release`** gates failed closed — UAT **UAT-5**/**UAT-6** still **BLOCKED**, **`tests/report.md`** not all **PASS** (7 fails), and no **`RELEASE_GATE_OVERRIDE_APPROVED`**. **`BUG-0008`** remains **OPEN** (**US-0045**).

## Evidence refs

- `sprints/S0070/release-findings.md`
- `sprints/S0070/uat.json`, `sprints/S0070/uat.md`
- `sprints/S0070/qa-findings.md`
- `tests/report.md`
- `handoffs/release_queue.md`
- `handoffs/releases/S0070-release-notes.md`

## Required remediation

1. Operator: **`npm publish`** **`its-magic@0.1.2-41`** per **`RELEASE_PUBLISH_MODE`**; run Debian global **E2E** per **`handoffs/releases/S0070-release-notes.md`** checklist; add **`evidence_refs`** (paths/logs) to sprint handoffs or **`handoffs/dev_to_qa.md`**.
2. Re-run **`/verify-work`** (**qa**) with populated UAT, then **`/release`** in fresh **release** context.
3. Optionally: restore **`tests/report.md`** to **Fail: 0** or document deterministic **`baseline_note`** in queue **`gate_snapshot`** per team policy.

## Re-run criteria

- `sprints/S0070/release-findings.md` shows **PASS** and queue **S0070** may transition **`blocked` → `released`** per contract.
- `docs/product/backlog.md` **BUG-0008** **DONE** only after honest gate **PASS** and **US-0045** alignment.

---

# Release -> Dev Handoff — Sprint S0013 (US-0041)

## Status

- Result: RESOLVED
- Sprint: `S0013`
- Story: `US-0041`

## Blocking reason (resolved)

- Primary reason code: `RELEASE_TEST_FAILED`
- Summary: Mandatory baseline test gate failed before release finalization; issue
  is now remediated and release finalization completed.

## Evidence refs

- `sprints/S0013/release-findings.md`
- `handoffs/release_queue.md`
- `tests/report.md`
- `sprints/S0013/qa-findings.md`
- `sprints/S0013/uat.json`

## Required remediation

1. Baseline blockers were fixed (`remote.json` schema and validate-and-push
   text-contract checks).
2. Mandatory suite rerun is green (`tests/report.md`: `Pass=165`, `Fail=0`).

## Re-run criteria

- `sprints/S0013/release-findings.md` updated to PASS.
- Queue row is `released` in `handoffs/release_queue.md`.
- Canonical release notes: `handoffs/releases/S0013-release-notes.md`.
