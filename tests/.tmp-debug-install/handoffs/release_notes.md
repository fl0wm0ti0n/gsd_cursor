# Release Notes (Legacy Compatibility Pointer)

This file remains backward-compatible for workflows that read
`handoffs/release_notes.md` as the latest release summary.

Canonical sprint history now lives under:
- `handoffs/releases/Sxxxx-release-notes.md`

Canonical queue state now lives under:
- `handoffs/release_queue.md`

---

## Latest finalized release pointer

- **Latest released sprint:** `Sxxxx`
- **Latest canonical notes:** `handoffs/releases/Sxxxx-release-notes.md`
- **Latest release date:** YYYY-MM-DD
- **Latest release story:** US-xxxx

## Unreleased queue visibility

Check `handoffs/release_queue.md` for all pending entries where `status=unreleased`
or `status=blocked` before finalization.

## Latest operator summary (Run/Connect/Verify)

- **Start command:** Refer to `## Run` in
  `handoffs/releases/Sxxxx-release-notes.md`.
- **Endpoint + port:** Refer to `## Connect` in
  `handoffs/releases/Sxxxx-release-notes.md`.
- **Verification steps + health signal:** Refer to `## Verify` in
  `handoffs/releases/Sxxxx-release-notes.md`.
- **Credentials source refs (sanitized):** Refer to `## Credentials` in
  `handoffs/releases/Sxxxx-release-notes.md` (env-ref only).
- **Known issues:** Refer to `## Known Issues` in
  `handoffs/releases/Sxxxx-release-notes.md`.

## Historical references

- `Sxxxx`: `handoffs/releases/Sxxxx-release-notes.md`

---

## Compatibility behavior contract

- Keep this file as a pointer/summary; do not treat it as canonical historical
  storage.
- `/release` must update sprint-scoped notes first, then refresh this pointer.
- Never delete or destructively rewrite historical sprint-scoped note files
  through this legacy path.
