# PO to TL archive pack (2026-06-06)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 13
- First archived heading: `## Research → Architecture handoff — US-0090 (input-side Caveman-style compression)`
- Last archived heading: `## Research → Architecture handoff — US-0090 (input-side Caveman-style compression)`
- Verification tuple (mandatory):
  - archived_body_lines=63
  - retained_body_lines=778

---

## Research → Architecture handoff — US-0090 (input-side Caveman-style compression)

- **From**: **tech-lead** (**`/research`** phase for US-0090, `auto-20260418-01`, `fresh_context_marker=tl-US0090-research-20260418T210000Z-fresh`)
- **To**: **tech-lead** (fresh **`/architecture`** subagent, next phase; **do not reuse this phase's context**)
- **Research anchor**: **`R-0073`** (extended under shared anchor — **no** new `R-xxxx` allocated; US-0089 intake bundle `plan_area_coverage` maps both stories; DEC-0011 precedent).
- **Research closure**: **PASS**. Eleven questions **Q9–Q19** resolved — **Q13 / Q14 / Q18** `status=resolved` (concrete; architecture ratifies verbatim); **Q9 / Q10 / Q11 / Q12 / Q15 / Q16 / Q17 / Q19** `status=deferred_to_architecture` with explicit research recommendations; **zero** `still-open`.
- **Evidence (read these first, in order)**:
  1. `docs/engineering/research.md` **`R-0073`** "Research phase resolution pass (2026-04-18, TL, `auto-20260418-01`, US-0090 input-side)" — authoritative Q9–Q19 resolution matrix, option tradeoffs, and risk catalog (R8–R11).
  2. `docs/product/backlog.md` `## US-0090` `research_notes (2026-04-18, TL, ...)` — condensed summary; backlog status **OPEN** (US-0045).
  3. `decisions/DEC-0072.md` — the **binding** contract US-0090 extends (do **NOT** rewrite; extend under a new companion DEC).
  4. `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` — byte-identical; SHA-256 `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` at research time.
  5. `docs/engineering/architecture.md` `# US-0089` — substrate; new `# US-0090` section is an **addition**, not a replacement.
  6. `docs/engineering/runbook.md` Caveman subsection + `docs/engineering/auto-orchestration-reference.md` `TOKEN_PROFILE × CAVEMAN_MODE` paragraph — extension points for Q16 three-axis publication.
  7. `handoffs/intake_evidence/US-0089-intake-20260418.json` — intake bundle; `plan_area_coverage` includes US-0090 under the shared `R-0073` anchor.

- **What architecture MUST decide (eleven sections, candidate companion DEC §1–§11)**:
  1. **§1 — Three-axis non-substitution** (Q16): exact wording for the `TOKEN_PROFILE` vs `CAVEMAN_MODE` vs `CAVEMAN_COMPRESS_INPUT` orthogonality paragraph in `docs/engineering/auto-orchestration-reference.md` + `docs/engineering/runbook.md` (active + `template/`); decide three parallel sentences (research recommended) vs 2x2x2 table fallback; decide whether `DEC-0072` §1 is extended in-place or §1 of the companion DEC forward-links to `DEC-0072` §1.
  2. **§2 — Activation gate** (Q13): exact `CAVEMAN_COMPRESS_INPUT=1` + non-empty `CAVEMAN_FILE_SCOPE` activation semantics; empty-scope default = pure opt-in (no files in scope; fails closed with `CAVEMAN_COMPRESS_SCOPE_EMPTY`); decide flag-conflict precedence rules (e.g. `--dry-run --write` simultaneously — research recommends fail-closed with `CAVEMAN_COMPRESS_FLAG_CONFLICT`); lock whether `--purge-orphans` ships in v1 (research recommends **deferred**).
  3. **§3 — Sidecar original policy** (Q10): lock Option B parallel-tree path pattern `docs/.caveman-originals/<relative/path>/<file>`; decide `.gitkeep` presence; decide whether `.cursorignore` receives a parity entry (research recommends leaving operator-owned per **US-0085**).
  4. **§4 — Deny-list source of truth** (Q11): lock Option C hybrid (hard-coded baseline + `.gitignore` secret-pattern merge + optional `.cursorignore` overlay); decide DEC-revision policy for the hard-coded baseline ("who can amend and through which DEC"); decide evaluation order — research recommends **deny-hard → ignore-merge → cursorignore overlay → allow-list → literal-region scan → write**.
  5. **§5 — Allow-list grammar** (Q12): lock Option C hybrid (named profile + raw globs + `profile:<name>;globs:<csv>` hybrid form); lock v1 profile set membership — candidate `docs-prose-only` → `docs/user-guides/**/*.md`, `docs/engineering/runbook.md`, `docs/engineering/state-archive/**/*.md`, `handoffs/archive/*.md`; decide unknown-profile behavior (research recommends fail-closed with `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`).
  6. **§6 — Compression algorithm** (Q9): lock hybrid tiering — `--mode=safe` default (line-level minifier: duplicate-blank-line collapse + trailing-whitespace trim + LF normalization) and `--mode=aggressive` opt-in (whitespace-collapse + frozen filler-word list + markdown-structure-preservation); decide whether aggressive mode ships in v1 or defers; lock exact `--mode` grammar and filler-word list contents (if aggressive ships); LLM-assisted compression **rejected** — architecture must not reopen.
  7. **§7 — Reason-code vocabulary** (Q15): lock 9-code set verbatim: `CAVEMAN_COMPRESS_SCOPE_VIOLATION`, `CAVEMAN_COMPRESS_DENY_HIT`, `CAVEMAN_COMPRESS_NOT_IDEMPOTENT`, `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`, `CAVEMAN_COMPRESS_ORIGINAL_MISSING`, `CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_SCOPE_EMPTY`, `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`, `CAVEMAN_COMPRESS_FLAG_CONFLICT`; forbid post-write reason codes (all must be pre-write / during-write); group into three families (scope, integrity, gating) to control proliferation risk (R9).
  8. **§8 — CLI contract** (Q13): lock entrypoint name `scripts/caveman_compress_input.py`; lock modes `--dry-run` (default when no mutation mode), `--write`, `--verify-originals`, `--report`; lock exit-code contract (non-zero on any violation; `0` only when zero violations and zero unresolved parity asserts); `--mode=safe|aggressive` orthogonal to mutation mode.
  9. **§9 — Template parity** (Q17): lock 8-row inventory — (a) `scripts/caveman_compress_input.py` + `template/scripts/caveman_compress_input.py` byte-identical; (b) `docs/engineering/runbook.md` operator-UX section + mirror; (c) `docs/engineering/auto-orchestration-reference.md` three-axis paragraph + mirror; (d) `docs/engineering/architecture.md` `# US-0090` active-only; (e) `tests/auto_command_contract_test.py` extension **active-only**; (f) `tests/fixtures/caveman_compress/` active-only; (g) `.gitignore` `docs/.caveman-originals/` anchor; (h) optional `.cursor/rules/caveman.mdc` "Input-side extension (US-0090)" subsection — decide yes/no; if yes, active + `template/` must stay byte-identical (US-0017, risk R10).
  10. **§10 — Installer / publish surface** (Q19): lock `docs/engineering/context/installer-owned-paths.manifest` entry for `template/scripts/caveman_compress_input.py` under `install_include_paths` (defense against BUG-0003 regression class — risk R11); no new npm script; no new runtime dep per **`DEC-0072`** §8; decide parity-test strategy — (A) extend `scripts/check_intake_template_parity.py --scope=caveman-compress` (research recommended) vs (B) new `scripts/check_caveman_template_parity.py`; decide install-completeness fixture — extend `tests/installer_completeness_bug0003_test.py` vs new `tests/installer_caveman_completeness_test.py`.
  11. **§11 — Non-goals** (forward-link to `DEC-0072` §8; reaffirm carried bans): no `TOKEN_PROFILE` change, no `DEC-0072` rewrite, no vendor install path (no `npx skills add …`), no strict-proof / isolation-evidence wording change, no mandatory auto-compress in `/auto`, no tokenizer change, no npm / pip runtime dep (stdlib-only Python), no canonical-artifact rewrites (backlog / acceptance / state / intake-evidence / DEC-* / sprint-* / contract surfaces).

- **Mandatory architecture artifacts** (architecture phase must produce):
  1. **Companion DEC** (next available `DEC-xxxx` after current max) with §1–§11 above; forward-links (not rewrites) to `DEC-0072`.
  2. `docs/engineering/architecture.md` **`# US-0090`** section (active-only; does **not** mirror to `template/` per existing DEC-0072 §7 row 6 pattern) linking `# US-0089`, **US-0053**, **US-0085**, **US-0078** / **DEC-0060**, and explicitly enumerating forbidden surfaces (Q18 deny-list).
  3. `docs/engineering/decisions.md` index + full-record entry for the companion DEC (canonical context pack).
  4. `handoffs/tl_to_dev.md` pre-sprint architecture handoff prepended at top; preserve prior US-0089 stanza as superseded (lineage).
  5. `handoffs/resume_brief.md` new top pointer post-`/architecture` for US-0090 (mark prior post-`/research` US-0090 pointer superseded).
  6. `docs/engineering/state.md` Architecture checkpoint (2026-04-18) — US-0090 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/sprint-plan`).

- **Risks carried to architecture** (from research resolution pass):
  - **R8** (Q9): aggressive-mode filler-word list drift → mitigation = architecture locks DEC-revision policy + `--report` emits list hash for operator drift detection.
  - **R9** (Q15): reason-code proliferation at 9 codes — upper edge for single rule-file page. Mitigation = group into three families; forbid further proliferation without DEC.
  - **R10** (Q17): if architecture adds a `caveman.mdc` subsection, active + `template/` byte-identity must hold (US-0017); sprint-plan task acceptance evidence must recompute SHA-256 post-edit; pre-US-0090 baseline `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`.
  - **R11** (Q19): omitting install-completeness fixture would reintroduce the exact defect class **BUG-0003** fixed. Architecture must not ship US-0090 without this fixture even under sprint-size pressure.

- **Scope guards for architecture** (non-negotiables; do not cross):
  - **Do not rewrite** `DEC-0072` — write a new companion DEC that extends via §-references.
  - **Do not change** `.cursor/rules/caveman.mdc` without mirroring in `template/` byte-identically (US-0017).
  - **Do not change** `TOKEN_PROFILE` / `CAVEMAN_MODE` semantics (US-0080, DEC-0062, DEC-0072 §1 orthogonality).
  - **Do not change** strict-proof / isolation-evidence wording (US-0056 / DEC-0038, US-0048 / DEC-0029) or AC-10 phase-boundary block contract.
  - **Do not change** `AUTO_QUIET` non-suppressible list (US-0088), spawn-only / phase-role (US-0069 / DEC-0051 / BUG-0006), or user-visible metadata policy (US-0071).
  - **Do not alter** `docs/product/backlog.md` status for US-0090 (stays **OPEN** — US-0045 status authority; closure at `/release`).
  - **Do not** seed sprint tasks — that is `/sprint-plan`'s job after `/architecture` lands the companion DEC.

- **Next phase**: **`/architecture`** (fresh **tech-lead**) for **US-0090** — lock companion DEC §1–§11 (as above) + write `# US-0090` architecture section.
- **Decision-gate posture**: **none** expected before `/architecture` produces the companion DEC; architecture phase **is itself** the decision gate.
- **Status authority**: **US-0090** stays **OPEN** per **US-0045**. No acceptance rows checked by research.
- **Artifact refs**:
  - `docs/engineering/research.md` **`R-0073`** "Research phase resolution pass (2026-04-18 ...)" (appended this phase)
  - `docs/product/backlog.md` **`## US-0090`** `research_notes (2026-04-18, TL, auto-20260418-01)` (appended this phase)
  - `docs/engineering/state.md` — Research checkpoint (2026-04-18) — US-0090 / `auto-20260418-01` (isolation + DEC-0038 strict proof + phase boundary block + AC-10 line + preflight for `/architecture`)
  - `handoffs/resume_brief.md` — new top pointer post-`/research` US-0090 (prior post-`/discovery` US-0090 pointer marked superseded)
  - `decisions/DEC-0072.md` (binding substrate; architecture extends via companion DEC)
  - `.cursor/rules/caveman.mdc` + `template/.cursor/rules/caveman.mdc` (byte-identical research-verified baseline)
  - `docs/engineering/architecture.md` **`# US-0089`** (substrate for new `# US-0090` section)

