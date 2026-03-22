# Release Notes (Legacy Compatibility Pointer)

This file remains backward-compatible for workflows that read
`handoffs/release_notes.md` as the latest release summary.

Canonical sprint history now lives under:
- `handoffs/releases/Sxxxx-release-notes.md`

Canonical queue state now lives under:
- `handoffs/release_queue.md`

---

## Latest finalized release pointer

- **Latest released sprint:** `S0054`
- **Latest canonical notes:** `handoffs/releases/S0054-release-notes.md`
- **Latest release date:** 2026-03-21
- **Latest release story:** US-0075

## Unreleased queue visibility

Check `handoffs/release_queue.md` for all pending entries where `status=unreleased`
or `status=blocked` before finalization.

## Release readiness note (S0054)

- Sprint: `S0054`
- Story: `US-0075`
- Verify-work: PASS
- UAT status: PASS (`11/11`, `0` failed)
- QA findings: PASS with no in-scope blockers (`sprints/S0054/qa-findings.md`)
- Release readiness: Finalized as `released` in `handoffs/release_queue.md`
  with canonical sprint-scoped notes.

## Latest operator summary (Run/Connect/Verify)

- **Start command:** Refer to `## Run` in
  `handoffs/releases/S0054-release-notes.md`.
- **Endpoint + port:** Refer to `## Connect` in
  `handoffs/releases/S0054-release-notes.md`.
- **Verification steps + health signal:** Refer to `## Verify` in
  `handoffs/releases/S0054-release-notes.md`.
- **Credentials source refs (sanitized):** Refer to `## Credentials` in
  `handoffs/releases/S0054-release-notes.md` (env-ref only).
- **Known issues:** Refer to `## Known Issues` in
  `handoffs/releases/S0054-release-notes.md`.

## Historical references

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
