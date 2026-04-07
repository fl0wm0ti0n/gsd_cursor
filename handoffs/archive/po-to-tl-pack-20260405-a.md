# PO to TL archive pack (2026-04-05)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 45
- First archived heading: `## PO → TL discovery handoff — **US-0084** (`auto-20260404-02`)`
- Last archived heading: `## PO → TL discovery handoff — **US-0084** (`auto-20260404-02`)`
- Verification tuple (mandatory):
  - archived_body_lines=14
  - retained_body_lines=795

---

## PO → TL discovery handoff — **US-0084** (`auto-20260404-02`)

- **Scope recap**: Fix **published** npm **`installer.sh`** for **POSIX `/bin/sh` (dash)** and **LF** entrypoints; add **canonical dev/QA docs + optional automatable helper** so WSL / SSH Linux / Docker-over-SSH testing maps to existing **US-0064** / **`release-targets.json`** / **`runtime-connectivity`** — no parallel remote schema. **Constraints**: **US-0064** authoritative; **no secrets** (AC-7); **`REMOTE_EXECUTION=0`** zero-overhead; **active + `template/`** parity (AC-8).
- **Acceptance pointers**: **AC-1** publish POSIX/LF; **AC-2** CI/test guard; **AC-3** troubleshooting (`set` error, CRLF, sh vs bash); **AC-4** remote Linux profile doc map; **AC-5** helper / one-liner; **AC-6** execute/qa handoff + env labels; **AC-7** security; **AC-8** template parity; **AC-9** minimal E2E path; **AC-10** harness coverage.
- **Top risks**: **publish vs repo drift** reintroduces BUG-0004 class; over-scoped helper vs one-liner; doc divergence from **`runtime-connectivity.md`**; secret leakage in examples or logs.
- **Research asks** (same as backlog **discovery_notes**):
  1. POSIX/dash audit of **published** vs repo **`installer.sh`** + EOL policy.
  2. CI guard shape + harness registration.
  3. Remote profile doc map (WSL / SSH / Docker-over-SSH → **US-0064** artifacts).
  4. Helper script contract (non-secret summary, exit codes).
  5. Parity + **`/execute`**/**`/qa`** evidence cues + AC-10 fixtures.
- **Next phase**: **`/research`** (TL default).
---

