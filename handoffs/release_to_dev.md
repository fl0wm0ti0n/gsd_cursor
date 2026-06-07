# Release → Dev Handoff — Sprint S0083 (US-0094) — **BLOCKED**

## Status

- Result: **BLOCKED** (`2026-06-07T16:00:00Z`)
- Sprint: `S0083`
- Story: `US-0094`

## Blocking reason (active)

- Primary reason codes: **`RELEASE_UAT_INCOMPLETE`**, **`PHASE_CONTEXT_ISOLATION_MISSING`** (verify-work), **`RUNTIME_PROOF_MISSING`** (verify-work)
- Summary: Mandatory **`/release`** gates failed closed — **`/verify-work`** has not run; UAT artifacts (`sprints/S0083/uat.json`, `sprints/S0083/uat.md`) are still **placeholder** (`steps=[]`, `total=0`). QA **PASS** is not sufficient for release. **`US-0094`** remains **OPEN** (**US-0045**).

## Evidence refs

- `sprints/S0083/release-findings.md`
- `sprints/S0083/uat.json`, `sprints/S0083/uat.md` (placeholder)
- `sprints/S0083/qa-findings.md` (PASS)
- `handoffs/qa_to_verify_work.md`
- `handoffs/resume_brief.md` (`intended_resume_phase=verify-work`)
- `docs/engineering/state.md` (post-qa checkpoint; no verify-work isolation)

## Required remediation

1. Run **`/verify-work`** (fresh **qa**) for **`S0083`** / **`US-0094`** — populate UAT with AC-1..AC-10 steps/results; independent re-run of coverage/doc-profile/metadata/parity gates.
2. On verify-work **PASS**: set `handoffs/release_queue.md` **S0083** → **`ready`**; spawn **`/release`** (fresh **release**).
3. Do **not** advance backlog status or acceptance row until release gate chain **PASS**.

## Re-run criteria

- `sprints/S0083/uat.json` populated with `passed + failed = total` and no unresolved fail.
- `docs/engineering/state.md` contains verify-work isolation + strict-proof tuples for `auto-20260607-01`.
- `sprints/S0083/release-findings.md` shows **PASS** and queue **S0083** may transition **`blocked` → `ready` → `released`**.

---

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
