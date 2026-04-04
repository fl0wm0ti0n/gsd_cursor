# PO to TL archive pack (2026-04-04)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 45
- First archived heading: `## PO → TL intake handoff — **US-0085** (2026-04-04)`
- Last archived heading: `## PO → TL intake handoff — **US-0085** (2026-04-04)`
- Verification tuple (mandatory):
  - archived_body_lines=11
  - retained_body_lines=797

---

## PO → TL intake handoff — **US-0085** (2026-04-04)

- **Scope**: Repo-root **`.env`** (gitignored) holds **values** for env vars used with **`.cursor/remote.json`** and **`docs/engineering/release-targets.json`** / operator connectivity (**US-0064**); committed **`.env.example`** = **names + comments only**; **agents must not read `.env`**; operators **source** `.env` (or export) **before** shells that run `ssh`, **`remote_config_summary`**, or release connectivity checks so processes see normal env without the AI opening the file.
- **Intake evidence**: `handoffs/intake_evidence/US-0085-intake-20260404.json` — `python scripts/intake_evidence_validate.py --file handoffs/intake_evidence/US-0085-intake-20260404.json` → **`[INTAKE_EVIDENCE_VALIDATION_OK]`**; routing `python scripts/intake_bug_routing_guard.py --kind story --file handoffs/intake_evidence/US-0085-intake-20260404-prose.txt` → **`[INTAKE_BUG_ROUTING_OK]`**.
- **Constraints**: Do **not** put secret **values** in **`release-targets.json`** or tracked **`remote.json`**; do **not** add agent-side automatic `.env` loading that exposes content to context; preserve **DEC-0070** `REMOTE_EXECUTION=0` zero-overhead posture.
- **Acceptance anchors**: AC-1..2 ignore rules; AC-3 `.env.example`; AC-4–6 runbook + connectivity docs + E2E doc; AC-7 rules; AC-8 optional non-secret helper; AC-9 gitignore test; AC-10 regression remote summary + US-0064 schema unchanged.
- **Risks**: Cursor still indexing `.env` if `.cursorignore` missing/wrong; operators assuming IDE injects `.env` into agents; accidental commit of `.env`; helper printing values.
- **Next phase**: **`/discovery`** (PO, fresh context) — refine design refs and TL research asks for `.env` vs shell-only sourcing vs optional wrapper script.

---

