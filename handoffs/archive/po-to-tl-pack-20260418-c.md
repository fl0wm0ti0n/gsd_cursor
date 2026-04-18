# PO to TL archive pack (2026-04-18)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 40
- First archived heading: `## PO → TL Handoff — US-0090 (Discovery)`
- Last archived heading: `## PO → TL Handoff — US-0090 (Discovery)`
- Verification tuple (mandatory):
  - archived_body_lines=28
  - retained_body_lines=791

---

## PO → TL Handoff — US-0090 (Discovery)

- **Orchestrator**: **`auto-20260418-01`** — discovery complete in fresh **PO** context (`fresh_context_marker=po-US0090-discovery-20260418T204500Z-fresh`, `timestamp=2026-04-18T20:45:00Z`).
- **Story**: **`US-0090`** — Optional Caveman-style input compression (safe file scope). **Status: OPEN** per **US-0045** (closure at `/release`). Backlog drain segment: `backlog_drain_active=true`, `backlog_drain_stories_remaining_budget=5`, `segment_work_item_kind=story`.
- **Intake coverage**: pre-satisfied by bundled evidence **`handoffs/intake_evidence/US-0089-intake-20260414.json`** (`first-intake-pack`, `coverage_complete=true`, `plan_area_inventory` / `plan_area_coverage` map both **US-0089** and **US-0090**; `[INTAKE_EVIDENCE_VALIDATION_OK]` at original intake). `/intake` for US-0090 was **skipped** by the orchestrator with justification recorded in `docs/engineering/state.md` `## /auto orchestration materialization (2026-04-18) -- auto-20260418-01 (continuation -- discovery, US-0090)`.
- **Built-on-US-0089 shipped surface (references only; PO does not re-derive)**:
  - Scratchpad keys **`CAVEMAN_COMPRESS_INPUT=0|1`** (default **0**) and **`CAVEMAN_FILE_SCOPE=`** (default empty) exist as **documented no-ops** in `.cursor/scratchpad.md` + `.cursor/scratchpad.local.example.md` (+ `template/`) per **DEC-0072** §3. US-0090 **activates** them; does not rename.
  - **9-zone literal-region invariant** (DEC-0072 §4) reused verbatim as the compression byte-preserve contract.
  - **TOKEN_PROFILE × CAVEMAN_MODE non-substitution** (DEC-0072 §1) remains authoritative; US-0090 adds a third independent axis (`CAVEMAN_COMPRESS_INPUT`).
  - **`.cursor/rules/caveman.mdc`** (active + `template/`) rule body untouched unless architecture opts to add a single "Input-side extension (US-0090)" subsection.
- **Discovery findings (summary; full text in `docs/product/backlog.md` `## US-0090` discovery_notes + `docs/engineering/research.md` `R-0073` second Discovery extension)**:
  - **Hard deny-list (PO expectation baseline)**: `.env` / `.env.*`, **`handoffs/intake_evidence/*.json`**, **`docs/product/backlog.md`**, **`docs/product/acceptance.md`**, **`docs/engineering/state.md`**, **`docs/engineering/decisions.md`**, **`decisions/DEC-*.md`**, **`sprints/*/plan-verify.json`** / **`uat.json`** / **`summary.md`** / **`release-findings.md`**, binaries, **`package.json`** / **`package-lock.json`** / **`installer.*`** / **`.github/workflows/*.yml`** / **`.cursor/hooks/*.py`** / **`.cursor/rules/*.mdc`** / **`.cursor/commands/*.md`** / **`.cursor/skills/**/SKILL.md`**. Deny always wins over allow.
  - **Allow-list grammar**: architecture-locked; candidates include comma-separated globs, named profiles (`docs-prose-only`), or hybrid. Empty `CAVEMAN_FILE_SCOPE` MUST evaluate to "no files in scope" (pure opt-in default).
  - **Sidecar originals**: every `--write` creates/updates a sidecar; PO recommendation = parallel tree under `docs/.caveman-originals/<relative/path>/<file>` for `.gitignore` hygiene (architecture locks final pattern).
  - **Modes**: `--dry-run` (default), `--write`, `--verify-originals`, `--report`. Non-zero exit on any deny-hit / scope-violation / literal-region damage / idempotency break with deterministic reason code.
  - **Idempotency**: script MUST be pure-deterministic; second run on already-compressed file = byte-equal no-op (AC-6 test fixture planned).
  - **Reason-code candidates (architecture-locked final names)**: `CAVEMAN_COMPRESS_SCOPE_VIOLATION`, `CAVEMAN_COMPRESS_DENY_HIT`, `CAVEMAN_COMPRESS_NOT_IDEMPOTENT`, `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`, `CAVEMAN_COMPRESS_ORIGINAL_MISSING`, `CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_SCOPE_EMPTY`.
  - **Three-axis non-substitution doc**: publish in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (+ `template/`) — format (paragraphs vs 2x2x2 table) architecture-locked.
- **Research asks (for `/research`, tech-lead)**: deepen **R-0073** on Q9–Q19 (algorithm choice, sidecar naming, deny-list source-of-truth, allow-list grammar, `dry-run` / `write` UX, idempotency strategy, reason-code vocabulary lock, three-axis doc form, template parity inventory, security/compliance boundary reaffirmation, installer / publish surface).
- **Architecture asks (for `/architecture` after research; DEC-xxxx hints)**: extend DEC-0072 (NOT rewrite it) via a companion DEC that locks input-side gate semantics, sidecar policy, deny-list, allow-list grammar, compression algorithm, reason-code vocabulary, and three-axis doc form. Authors `docs/engineering/architecture.md` `# US-0090` with explicit forward-links to `# US-0089` / DEC-0072 / US-0053 / US-0080 / US-0085 / US-0078 / DEC-0060 and a "forbidden surfaces" subsection.
- **Risks (PO-surfaced, carried to research)**: (R1) broad glob rewriting a canonical artifact — deny-list script-enforced before scope expansion; (R2) sidecar drift — architecture locks pattern + optional `--verify-originals`; (R3) non-idempotent algorithm — dedicated AC-6 fixture; (R4) literal-region matcher missing a new zone — single shared constant + extension requires DEC; (R5) TOKEN_PROFILE / CAVEMAN_MODE / CAVEMAN_COMPRESS_INPUT confusion — three-axis non-substitution doc; (R6) secret leakage through sidecar — sidecar pattern deny-list-aware; (R7) vendor-install leak — DEC-0072 §8 ban carried forward to US-0090 docs/rule.
- **Out of scope (hard)**: no mandatory auto-compress in `/auto`; no Cursor tokenizer change; no translation of code to another natural language; no rewrite of deny-listed canonical artifacts; no new npm/pip runtime dep (stdlib-only Python); no change to TOKEN_PROFILE semantics; no change to AUTO_QUIET non-suppressible list; no change to strict-proof / isolation-evidence wording; no change to spawn-only / phase-role contracts; no change to DEC-0072 (US-0090 extends, never overrides).
- **Artifacts touched (this phase)**: `docs/product/backlog.md` (`## US-0090` discovery_notes appended), `docs/engineering/research.md` (`R-0073` second Discovery extension appended — US-0090 input-side), `handoffs/po_to_tl.md` (this prepended section), `handoffs/resume_brief.md` (new top pointer), `docs/engineering/state.md` (Discovery checkpoint + isolation evidence + strict runtime proof + phase boundary status).
- **Decision gate before research**: **none** — discovery satisfied; research readiness explicit on Q9–Q19.
- **Next**: **`/research`** (fresh **tech-lead**) for **US-0090**. Alternate: **`/auto start-from=research`**.

---

