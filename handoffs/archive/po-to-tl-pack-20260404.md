# PO to TL archive pack (2026-04-04)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 44
- First archived heading: `## Intake handoff — US-0084 (2026-04-04)`
- Last archived heading: `## Intake handoff — US-0084 (2026-04-04)`
- Verification tuple (mandatory):
  - archived_body_lines=20
  - retained_body_lines=781

---

## Intake handoff — US-0084 (2026-04-04)

### Scope summary

- **Story**: **`US-0084`** — POSIX-safe **global npm** `installer.sh` (fix **`set: Illegal option -`** under Debian **`dash`** / SSH / Docker) **and** operator/dev/QA paths to run tests against **WSL**, **SSH Linux**, or **Docker** using existing remote contracts (**`US-0064`**, **`REMOTE_CONFIG`**, **`.cursor/remote.json`**).
- **Evidence**: **`handoffs/intake_evidence/US-0084-intake-20260404.json`** — **`small-intake-pack`**, **`[INTAKE_EVIDENCE_VALIDATION_OK]`**.
- **Priority**: **P1**; **Status**: **OPEN** (**`docs/product/backlog.md`**).

### TL focus for `/discovery`

- Confirm whether **npm publish** pipeline copies a **different** `installer.sh` than repo root (version skew / CRLF).
- Map minimal **helper script** surface vs pure-docs approach for **AC-5** / **AC-10**.
- Keep **US-0064** schema authoritative; avoid duplicate remote config languages.

### Next phase

- Run **`/discovery`** (PO, fresh context) then **`/research`** / **`/architecture`** per lifecycle — or **`/auto`** with resume **`discovery`** for **`US-0084`**.

---

