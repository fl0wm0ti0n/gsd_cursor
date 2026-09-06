# PO to TL archive pack (2026-09-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2 (+ later rollover units in subsequent packs if any)
- First archived heading: `## Intake handoff — BUG-0015 and BUG-0016 OpenCode /auto dispatch + Layer-1 permission matrix`
- Last archived heading (this pack): `## Intake handoff — US-0131 and US-0132 Cross-host configuration and model contract`
- Note: Pack body rewritten 2026-09-06 to repair PowerShell backtick corruption in the BUG-0015/0016 unit; semantic content unchanged. Hot copy retained in `handoffs/po_to_tl.md`.

---

## Intake handoff — BUG-0015 and BUG-0016 OpenCode /auto dispatch + Layer-1 permission matrix

- **Phase completed**: intake (`/intake bug`). **Role**: po. **Bugs**: BUG-0015 (primary), BUG-0016 (also OPEN). **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-09-06T13:35:00Z. **Fresh marker**: `po-BUG0015-BUG0016-intake-20260906T133500Z-fresh`.
- **Writer**: `writer_id=po-cursor-20260906-opencode-bugs`, `intake_run_id=cursor-20260906-BUG0015-0016-intake`.
- **Routing**: argv `/intake bug` wins over scratchpad `INTAKE_WORK_ITEM_KIND=story`. `selected_pack=small-intake-pack`. `INTAKE_GUIDED_MODE=1`.
- **Evidence**:
  - `handoffs/intake_evidence/BUG-0015-intake-20260906.json` — `[INTAKE_EVIDENCE_VALIDATION_OK]`
  - `handoffs/intake_evidence/BUG-0016-intake-20260906.json` — `[INTAKE_EVIDENCE_VALIDATION_OK]`
  - `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` — `[BUG_VALIDATION_OK]`
  - `python scripts/intake_bug_resume_brief_refresh.py ... --bug-id BUG-0015` — `[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]` (primary continuation; BUG-0016 also OPEN)
- **Operator ask**: Persist two OPEN defects — (1) OpenCode `/auto` never starts orchestrator plugin dispatch (STOP); (2) OpenCode Layer-1 role permissions block legitimate lifecycle duties (audit all roles).
- **Decomposition (recommended)**: two independently valuable bugs — dispatch wiring vs permission matrix/duty mismatch. Do not fold into US-0131/US-0132.
- **Alternatives considered**:
  1. **Two OPEN bugs** (recommended) — separate dispatch vs permissions; independently testable.
  2. **Fold into US-0131** — rejected (wrong scope: config/model parity, not runtime dispatch/permissions).
  3. **Amend DEC-0122 only without bugs** — rejected (no OPEN work item / no acceptance row).
- **BUG-0015 (primary fix target)**: `.opencode/commands/auto.md` is STOP-only; `.opencode/plugins/orchestrator.ts` exports `spawnPhase` from `setup()` return API and hooks `execute.before` write-guard only — no command/event hook invokes spawn loop on `/auto`. Compose US-0124/US-0125 ships surfaces but runtime linkage gap remains.
- **BUG-0016 (permission audit — all roles)**:

| Role | Issue |
|------|--------|
| `po` | `bash: deny` blocks mandatory validators / resume-brief refresh; edit misses `handoffs/intake_evidence/**` and bug-intake `handoffs/resume_brief.md` (DEC-0069). |
| `tech-lead` | `bash: deny` blocks research/architecture validators; literal `sprints/Sxxxx/` likely fails real ids. |
| `dev` | `bash: ask` OK-ish; same `Sxxxx` glob risk; confirm owned paths vs execute ownership. |
| `qa` | `bash: ask` OK-ish; literal `Sxxxx` glob risk. |
| `release` | `bash: ask` OK-ish; may miss `sprints/*/release-findings.md` (scope carefully). |
| `curator` | `bash: deny` blocks `enforce-triad-hot-surface.py` / materialize scripts for `/refresh-context`. |
| `security` | `edit: deny` + `bash: ask` matches DEC-0122 v1 — in-contract unless contradiction found. |
| `auto` | spawn-only OK for Task path; OpenCode still broken by BUG-0015. |

- **Duplicate check**: Distinct from BUG-0006, BUG-0012, US-0122 DONE, US-0131/US-0132 OPEN (do not expand those stories).
- **Risks**: R1 — OpenCode host plugin API may lack a clean `/auto` hook (fail closed with `OPENCODE_*`); R2 — widening bash/edit for non-dev roles must preserve success test (c) production/code deny; R3 — DEC-0122 amendment + `test_us0122_*` / template parity churn; R4 — fixing permissions without BUG-0015 still leaves `/auto` dead.
- **Isolation**: `phase_id=intake`; `role=po`; `fresh_context_marker=po-BUG0015-BUG0016-intake-20260906T133500Z-fresh`; `timestamp=2026-09-06T13:35:00Z`; `evidence_ref=docs/product/backlog.md ## Bug issues BUG-0015 + BUG-0016, docs/product/acceptance.md bug rows, handoffs/resume_brief.md, this handoff`.
- **Status**: both OPEN per US-0045. **Next**: `/discovery` (fresh **po**) for **BUG-0015**, or `/auto bug-target=BUG-0015`. Do not run architecture/execute from this intake chat. STOP after intake.

## Intake handoff — US-0131 and US-0132 Cross-host configuration and model contract

- **Phase completed**: intake. **Role**: po. **Stories**: US-0131, US-0132. **Sprint**: (pending). **Verdict**: PASS (`decision_gate=false`).
- **Timestamp**: 2026-09-06T00:00:00Z. **Fresh marker**: `po-US0131-US0132-intake-20260906T000000Z-fresh`.
- **Evidence**: `handoffs/intake_evidence/US-0131-0132-intake-20260906.json` — `[INTAKE_EVIDENCE_VALIDATION_OK]`; `selected_pack=small-intake-pack`; `missing_topics=[]`.
- **Writer**: `writer_id=po-opencode-20260906-cross-host-config`, `intake_run_id=opencode-20260906-cross-host-config-intake`.
- **Operator ask**: Close the missing Its-Magic rules/configuration behavior in OpenCode and ensure all files shared by Cursor and OpenCode are handled correctly, especially scratchpad and model configuration files.
- **Story split**:
  - **US-0131** owns the host-neutral runtime configuration contract, Cursor scratchpad compatibility, OpenCode-only operation without `.cursor/`, shared-script configuration injection, host-specific boundaries, installer preservation, and cross-host parity tests.
  - **US-0132** owns canonical model-file names/ownership, separate Cursor and OpenCode schemas, precedence, materialization, fail-closed validation, local-file protection, and model documentation/tests. A generic undocumented `model.json` source of truth is forbidden.
- **Acceptance coverage**: US-0131 has 8 ACs; US-0132 has 8 ACs. Both remain `OPEN` with unchecked acceptance rows. No architecture or implementation files are changed by intake.
- **Compose do not amend**: US-0073/DEC-0055 Cursor scratchpad precedence; US-0101/US-0102 Cursor model resolution; US-0121..US-0126 OpenCode adapter slices; US-0123 OpenCode per-role catalog. Preserve local files, no provider proxy, no credentials or real slugs in templates.
- **Discovery questions**: choose the host-neutral config location and schema; define legacy scratchpad compatibility and precedence; enumerate host-neutral versus host-specific flags; define shared-script config injection; reconcile OpenCode plugin validator enforcement and closure role mapping; define canonical model-file names, migration, and both-host conflict diagnostics.
- **Isolation**: `phase_id=intake`; `role=po`; `fresh_context_marker=po-US0131-US0132-intake-20260906T000000Z-fresh`; `timestamp=2026-09-06T00:00:00Z`; `evidence_ref=docs/product/backlog.md ## US-0131 + ## US-0132, docs/product/acceptance.md US-0131/US-0132, docs/product/vision.md ## Intake Notes — US-0131 and US-0132, this handoff`.
- **Next**: `/discovery` (fresh **po**) for US-0131, then US-0132. Do not add architecture sections or implementation artifacts during intake.
