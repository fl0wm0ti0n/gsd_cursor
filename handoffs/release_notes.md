# Release Notes (Legacy Compatibility Pointer)

This file remains backward-compatible for workflows that read
`handoffs/release_notes.md` as the latest release summary.

Canonical sprint history now lives under:
- `handoffs/releases/Sxxxx-release-notes.md`

Canonical queue state now lives under:
- `handoffs/release_queue.md`

---

## Latest finalized release pointer

- **Latest released sprint:** `S0012`
- **Latest canonical notes:** `handoffs/releases/S0012-release-notes.md`
- **Latest release date:** 2026-02-26
- **Latest release story:** US-0040

## Unreleased queue visibility

Check `handoffs/release_queue.md` for all pending entries where `status=unreleased`
or `status=blocked` before finalization.

## Release readiness note (S0012)

- Sprint: `S0012`
- Story: `US-0040`
- Verify-work: PASS
- UAT status: PASS (`9/9`, `0` failed)
- QA findings: PASS with no blockers (`sprints/S0012/qa-findings.md`)
- Release readiness: Finalized as `released` in `handoffs/release_queue.md`
  with canonical sprint-scoped notes.

## Historical references

- `S0012`: `handoffs/releases/S0012-release-notes.md`
- `S0010`: `handoffs/releases/S0010-release-notes.md`

---

## Compatibility behavior contract

- Keep this file as a pointer/summary; do not treat it as canonical historical
  storage.
- `/release` must update sprint-scoped notes first, then refresh this pointer.
- Never delete or destructively rewrite historical sprint-scoped note files
  through this legacy path.
