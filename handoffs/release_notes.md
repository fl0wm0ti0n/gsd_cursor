# Release Notes (Legacy Compatibility Pointer)

This file remains backward-compatible for workflows that read
`handoffs/release_notes.md` as the latest release summary.

Canonical sprint history now lives under:
- `handoffs/releases/Sxxxx-release-notes.md`

Canonical queue state now lives under:
- `handoffs/release_queue.md`

---

## Latest finalized release pointer

- **Latest released sprint:** `S0070`
- **Latest canonical notes:** `handoffs/releases/S0070-release-notes.md`
- **Latest release date:** 2026-04-05
- **Latest release work item:** BUG-0008

## Release finalized note (S0070)

- Sprint: `S0070`
- Bug: `BUG-0008` (CRLF **`installer-owned-paths.manifest`** / **`R-0069`**)
- Release: **finalized** (`2026-04-05T22:30:00Z`, `orchestrator_run_id=auto-20260404-03`, strict proof `proof_hash=29228ef7c322aa74d21b8a354adf4c45bbb8d4c64c967ee9dd3d58f7e9b2bf02`)
- Queue: **`handoffs/release_queue.md`** row **`S0070`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0070-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — **no** **`npm publish`** this boundary (deterministic no-op)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context)

## Release finalized note (S0069)

- Sprint: `S0069`
- Story: `US-0084` (POSIX npm installer + Linux remote test targets; **US-0064** alignment; **DEC-0070** remote-config helper skip policy)
- Release: **finalized** (`2026-04-05T00:10:00Z`, `orchestrator_run_id=auto-20260404-02`, strict proof `proof_hash=418cbee2c8f7508880e1cbcae744d67877c08e68c91432b3de38f0e1773b07fc`)
- Queue: **`handoffs/release_queue.md`** row **`S0069`** = **`released`**
- Publish posture: **`RELEASE_PUBLISH_MODE=confirm`** — no auto-publish without confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (no auto-push this boundary)
- **Next**: **`/refresh-context`** (fresh **curator** context)

## Release finalized note (S0068) (historical)

- Sprint: `S0068`
- Bug: `BUG-0007` (**R-0066** / **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**)
- Release: **finalized** (`2026-04-05T00:10:00Z`, `orchestrator_run_id=auto-20260404-01`, strict proof `proof_hash=6c824be4c8dfb3ecb25de8e8ca90910789436a2c916489fb15a935baf3c64202`)
- Queue: **`handoffs/release_queue.md`** row **`S0068`** = **`released`**
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (no auto-push this boundary)
- Portfolio: **`docs/product/backlog.md`** — canonical **bug** rows **BUG-0001..BUG-0007** all **DONE**; **next OPEN bug:** **(none)**
- **Next**: **`/refresh-context`** (fresh **curator** context) — **superseded** by **S0069** pointer above

## Release readiness note (S0068) (historical)

- Pre-release verify-work **PASS** (`2026-04-04T23:45:00Z`); superseded by **Release finalized note (S0068)** above.

## Release readiness note (S0067)

- Sprint: `S0067`
- Bug: `BUG-0006` (**spawn-only `/auto`**, **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, **R-0065**)
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0067-release-notes.md` (`2026-04-04T09:00:00Z`, `orchestrator_run_id=auto-20260403-03`); **`/refresh-context`** **complete** — successor track **`S0068`** / **`BUG-0007`** **released** (`2026-04-05`).

## Release readiness note (S0066)

- Sprint: `S0066`
- Bug: `BUG-0005` (**DEC-0069**)
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0066-release-notes.md`; **`/refresh-context`** **complete** (`auto-20260403-02`, **`2026-04-03T23:55:00Z`**) — superseded by **`S0067`** closure track; portfolio now advances via **`BUG-0007`** after **`S0067`** **`/refresh-context`**.

## Release readiness note (S0065)

- Sprint: `S0065`
- Bug: `BUG-0004`
- Release: **finalized** - queue row **`released`**; canonical notes `handoffs/releases/S0065-release-notes.md`; next **`/refresh-context`** completed.

## Release readiness note (S0064)

- Sprint: `S0064`
- Story: `US-0083`
- Release: **finalized** - queue row **`released`**; canonical notes `handoffs/releases/S0064-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0063)

- Sprint: `S0063`
- Bug: `BUG-0003`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0063-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0062)

- Sprint: `S0062`
- Story: `US-0082`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0062-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0061)

- Sprint: `S0061`
- Story: `US-0081`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0061-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0060)

- Sprint: `S0060`
- Bug: `BUG-0001`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0060-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0059)

- Sprint: `S0059`
- Story: `US-0080`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0059-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0058)

- Sprint: `S0058`
- Story: `US-0079`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0058-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Unreleased queue visibility

Check `handoffs/release_queue.md` for all pending entries where `status=unreleased`
or `status=blocked` before finalization.

- **`S0070` / `BUG-0008`**: **`blocked`** (`2026-04-04T23:30:00Z`) — **`RELEASE_TEST_FAILED`**, **`RELEASE_UAT_INCOMPLETE`**, deferred **publish**/**E2E**; canonical notes `handoffs/releases/S0070-release-notes.md`; do **not** treat **`S0069`** pointer as superseding this track until **`S0070`** **`released`** or row cleared.

## Release readiness note (S0057)

- Sprint: `S0057`
- Story: `US-0078`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0057-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0056)

- Sprint: `S0056`
- Story: `US-0077`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0056-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0055)

- Sprint: `S0055`
- Story: `US-0076`
- Verify-work: PASS
- UAT status: PASS (`10/10`, `0` failed)
- QA findings: PASS with no in-scope blockers (`sprints/S0055/qa-findings.md`)
- Release readiness: Finalized as `released` in `handoffs/release_queue.md`
  with canonical sprint-scoped notes.

## Latest operator summary (Run/Connect/Verify)

- **Start command:** Last finalized sprint **`S0069`**: refer to `## Run` in
  `handoffs/releases/S0069-release-notes.md`.
- **Endpoint + port:** Refer to `## Connect` in
  `handoffs/releases/S0069-release-notes.md`.
- **Verification steps + health signal:** Refer to `## Verify` in
  `handoffs/releases/S0069-release-notes.md`.
- **Credentials source refs (sanitized):** Refer to `## Credentials` in
  `handoffs/releases/S0069-release-notes.md` (env-ref only).
- **Known issues:** Refer to `## Known Issues` in
  `handoffs/releases/S0069-release-notes.md`.

## Historical references

- `S0069`: `handoffs/releases/S0069-release-notes.md`
- `S0068`: `handoffs/releases/S0068-release-notes.md`
- `S0067`: `handoffs/releases/S0067-release-notes.md`
- `S0066`: `handoffs/releases/S0066-release-notes.md`
- `S0065`: `handoffs/releases/S0065-release-notes.md`
- `S0064`: `handoffs/releases/S0064-release-notes.md`
- `S0063`: `handoffs/releases/S0063-release-notes.md`
- `S0062`: `handoffs/releases/S0062-release-notes.md`
- `S0061`: `handoffs/releases/S0061-release-notes.md`
- `S0060`: `handoffs/releases/S0060-release-notes.md`
- `S0059`: `handoffs/releases/S0059-release-notes.md`
- `S0058`: `handoffs/releases/S0058-release-notes.md`
- `S0057`: `handoffs/releases/S0057-release-notes.md`
- `S0056`: `handoffs/releases/S0056-release-notes.md`
- `S0055`: `handoffs/releases/S0055-release-notes.md`
- `S0054`: `handoffs/releases/S0054-release-notes.md`
- `S0053`: `handoffs/releases/S0053-release-notes.md`
- `S0052`: `handoffs/releases/S0052-release-notes.md`
- `S0051`: `handoffs/releases/S0051-release-notes.md`
- `S0050`: `handoffs/releases/S0050-release-notes.md`
- `S0049`: `handoffs/releases/S0049-release-notes.md`
- `S0048`: `handoffs/releases/S0048-release-notes.md`
- `S0047`: `handoffs/releases/S0047-release-notes.md`
- `S0046`: `handoffs/releases/S0046-release-notes.md`
- `S0045`: `handoffs/releases/S0045-release-notes.md`
- `S0044`: `handoffs/releases/S0044-release-notes.md`
- `S0043`: `handoffs/releases/S0043-release-notes.md`
- `S0042`: `handoffs/releases/S0042-release-notes.md`
- `S0041`: `handoffs/releases/S0041-release-notes.md`
- `S0040`: `handoffs/releases/S0040-release-notes.md`
- `S0039`: `handoffs/releases/S0039-release-notes.md`
- `S0038`: `handoffs/releases/S0038-release-notes.md`
- `S0037`: `handoffs/releases/S0037-release-notes.md`
- `S0036`: `handoffs/releases/S0036-release-notes.md`
- `S0035`: `handoffs/releases/S0035-release-notes.md`
- `S0034`: `handoffs/releases/S0034-release-notes.md`
- `S0033`: `handoffs/releases/S0033-release-notes.md`
- `S0032`: `handoffs/releases/S0032-release-notes.md`
- `S0031`: `handoffs/releases/S0031-release-notes.md`
- `S0030`: `handoffs/releases/S0030-release-notes.md`
- `S0029`: `handoffs/releases/S0029-release-notes.md`
- `S0011`: `handoffs/releases/S0011-release-notes.md`
- `S0025`: `handoffs/releases/S0025-release-notes.md`
- `S0026`: `handoffs/releases/S0026-release-notes.md`
- `S0027`: `handoffs/releases/S0027-release-notes.md`
- `S0028`: `handoffs/releases/S0028-release-notes.md`
- `S0024`: `handoffs/releases/S0024-release-notes.md`
- `S0023`: `handoffs/releases/S0023-release-notes.md`
- `S0022`: `handoffs/releases/S0022-release-notes.md`
- `S0021`: `handoffs/releases/S0021-release-notes.md`
- `S0020`: `handoffs/releases/S0020-release-notes.md`
- `S0019`: `handoffs/releases/S0019-release-notes.md`
- `S0018`: `handoffs/releases/S0018-release-notes.md`
- `S0017`: `handoffs/releases/S0017-release-notes.md`
- `S0016`: `handoffs/releases/S0016-release-notes.md`
- `S0015`: `handoffs/releases/S0015-release-notes.md`
- `S0013`: `handoffs/releases/S0013-release-notes.md`
- `S0012`: `handoffs/releases/S0012-release-notes.md`
- `S0010`: `handoffs/releases/S0010-release-notes.md`

---

## Per-gate audit verdict (US-0039)

When `/release` runs, each gate (check-in test, QA, UAT, finalization) is recorded with:
- **verdict**: pass | fail | override
- **reason_code**: e.g. RELEASE_TEST_FAILED, RELEASE_QA_BLOCKERS_OPEN, RELEASE_UAT_INCOMPLETE, RELEASE_GATE_OVERRIDE_APPROVED
- **remediation**: short steps when not pass
- **evidence_refs**: paths to tests/report.md, qa-findings.md, uat.json, release-findings.md, DEC-xxxx

Canonical per-run gate snapshot lives in `sprints/Sxxxx/release-findings.md` and queue row `gate_snapshot`; TL/QA audit from those artifacts and `docs/engineering/state.md` checkpoints.

**Override path (US-0039)**: When a gate is overridden, record decision record ref (DEC-xxxx), rationale, approver, and risk acceptance in release-findings and gate_snapshot; use reason code `RELEASE_GATE_OVERRIDE_APPROVED`.

## Compatibility behavior contract

- Keep this file as a pointer/summary; do not treat it as canonical historical
  storage.
- `/release` must update sprint-scoped notes first, then refresh this pointer.
- Never delete or destructively rewrite historical sprint-scoped note files
  through this legacy path.
