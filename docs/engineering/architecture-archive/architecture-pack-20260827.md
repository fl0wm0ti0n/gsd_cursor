# Architecture archive pack (2026-08-27)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3000, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 17
- First archived heading: `# US-0121 — OpenCode template pack and installer host mode`
- Last archived heading: `# US-0121 — OpenCode template pack and installer host mode`
- Verification tuple (mandatory):
  - archived_body_lines=288
  - preamble_lines=1
  - retained_body_lines=2777

---

# US-0121 — OpenCode template pack and installer host mode

## Overview

**US-0121** is the first slice of the six-story OpenCode adapter epic (US-0121..US-0126). It ships an empty-but-valid `template/.opencode/` tree (`agents/`, `commands/`, `plugins/` + `.gitignore` + `README.md`) and an additive `--host cursor|opencode|both` switch on the existing its-magic installer (US-0008 compose, additive only). Default install remains **cursor-only** until explicit opt-in; cursor-only install must not regress `.cursor/` delivery (AC-4 byte-identity gate). No plugin body, no role agents, no model slugs, no command bodies beyond placeholders — those belong to US-0122..US-0126.

This is a **pack-and-installer** change: new template tree, additive manifest sections, additive `--host` argv in `bin/its-magic.js` + PowerShell `-Host` + Bash `--host` + Python `--host`, host-scoped `missing`/`upgrade`/`clean`, and a contract-test list. The compose surface (US-0008 missing/overwrite/clean/upgrade semantics, DEC-0045 `its_magic/` ownership, US-0102 volatile-ID rule) remains UNCHANGED — US-0121 adds the host-surface switch only.

**Research anchor**: **R-0109** (deepened 2026-08-23, tech-lead, `/research`, auto-20260823-01 — Q6–Q12 LOCKED for US-0121 execute; Q1–Q5 LOCKED for `/architecture` only, deferred to US-0122..US-0126; 8 risks R1–R8 ACCEPTED; approach A1 locked; compose guards verified). **Companion DEC**: **DEC-0120** (authored Accepted in THIS phase — captures Q7 manifest parallel sections + Q8 kernel-vs-host contract + Q9 YAGNI active mirror so US-0122..US-0126 inherit the host contract without re-deriving).

**Fresh context marker**: `tl-US0121-architecture-20260823T111500Z-fresh`
**Orchestrator run id**: `auto-20260823-01`
**Timestamp**: 2026-08-23T11:15:00Z (UTC)
**Verdict**: PASS
**Next**: `/sprint-plan`

## Approach locked (A1 — from R-0109 Q6–Q12)

**Approach A1** (locked): Ship `template/.opencode/{agents,commands,plugins}/` with one placeholder file per directory + `template/.opencode/.gitignore` + `template/.opencode/README.md` (no repo-root `opencode.json` this slice). Add parallel manifest sections `[opencode_install_include_paths]` and `[opencode_clean_paths]` to `installer-owned-paths.manifest`; existing `[install_include_paths]` / `[clean_paths]` remain the cursor-default rows. Add `--host cursor|opencode|both` to `bin/its-magic.js` argv parser (normalize lowercase + trim, then validate; unknown → `INSTALL_HOST_INVALID`; duplicate/conflicting `--host` argv → fail closed `INSTALL_HOST_INVALID`, no last-wins). Forward `--host` to PowerShell `-Host`, Bash `--host`, Python `--host`. `--host` gates **only** `.cursor/` and `.opencode/` surfaces; kernel paths install regardless of `--host`. `missing`/`upgrade`/`clean` are host-scoped: `clean --host cursor` after `--host both` does **not** delete `.opencode/` and emits `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`; `upgrade --host cursor` after `--host both` does not refresh `.opencode/` and emits `OPENCODE_STALE_BY_UPGRADE_CURSOR`. The mixed-section `[install_include_paths]` parser predicate skips `.cursor/` rows when `--host opencode` while still installing kernel rows from the same section.

| Option | Summary | Verdict |
|--------|---------|---------|
| **A1** | **Parallel manifest sections + placeholder pack + normalize-then-validate `--host` + host-scoped missing/upgrade/clean + kernel-vs-host copy filter** | **Preferred** — additive only (US-0008 compose); preserves existing parser contract; AC-5 manifest membership explicit; AC-4 byte-identity enforceable; critic findings 1–3 closed. |
| A2 (rejected) | Host-tagged rows: `.opencode/  @host=opencode,both` — adds a tag column to the existing line format. | **Rejected** — requires amending the parser to accept a tag column (a US-0008 rewrite, forbidden by D9); mixes concerns in one section; breaks the existing `[install_include_paths]` parser contract. |
| A3 (rejected) | Prefix filter at copy time only: keep `[install_include_paths]` flat, filter `.cursor/` vs `.opencode/` at copy time based on `--host`, no new manifest sections. | **Rejected** — hides `.opencode/` membership from the manifest, breaking AC-5 ("manifest lists `template/.opencode/**`"); loses explicit manifest membership for the OpenCode pack; parity checker cannot grep the manifest for opencode rows. |
| A4 (rejected) | Repo-root `opencode.json` stub in the template pack. | **Rejected** — would prematurely lock the US-0122 permission matrix and US-0123 provider config (R-0109 Q6 LOCKED: no repo-root `opencode.json` this slice). |


## Components

### Template pack layout (Q6 LOCKED)

```
template/.opencode/
  agents/.gitkeep
  commands/.gitkeep
  plugins/README.md
  .gitignore
  README.md
```

- One placeholder file per directory (`.gitkeep` for `agents/`/`commands/`, `README.md` for `plugins/` explaining the plugin slot is reserved for US-0124).
- `template/.opencode/README.md` explains the pack: empty-but-valid, three subdirs, gitignore posture, pointer to US-0122..US-0126 for fill.
- **No repo-root `opencode.json`** this slice (R-0109 Q6).
- **No active `.opencode/` mirror in this kit repo** (R-0109 Q9 — YAGNI).

### `template/.opencode/.gitignore` (Q10 LOCKED — four pattern groups, no speculative globs)

```
.opencode/opencode.json
.opencode/opencode.jsonc
.env
.env.*
*.local.json
*.local.jsonc
auth.json
```

Q10 LOCKED lists four pattern groups: (1) `.opencode/opencode.json{,c}`, (2) `.env` / `.env.*`, (3) `*.local.json{,c}` under `.opencode/`, (4) `auth.json` defense-in-depth. Critic `ik_us0121_gitignore_premature_patterns` asked to drop the extras; per the orchestrator brief we **decline dropping Q10** and **do not add** further speculative globs this slice. The `*.local.json{,c}` patterns are scoped to `.opencode/` (the `.gitignore` lives at `template/.opencode/.gitignore`, so unanchored patterns apply within that directory tree only). `auth.json` lives outside the repo per OpenCode docs but is listed as harmless defense-in-depth.

### Manifest sections (Q7 LOCKED — parallel additive sections)

Add to `docs/engineering/context/installer-owned-paths.manifest` (and `template/docs/engineering/context/installer-owned-paths.manifest` byte-identical):

```
[opencode_install_include_paths]
.opencode/agents
.opencode/commands
.opencode/plugins
.opencode/.gitignore
.opencode/README.md

[opencode_clean_paths]
.opencode
```

- Existing `[install_include_paths]` / `[clean_paths]` / `[required_install_script_paths]` **unchanged** (US-0008 additive only).
- Triple-installer reads `[opencode_install_include_paths]` only when `--host` includes opencode (`opencode` or `both`); reads `[opencode_clean_paths]` only when `--host` includes opencode.
- `[install_include_paths]` remains the cursor-default + kernel section. The mixed-section skip predicate (below) gates `.cursor/` rows by `--host`.

### Mixed-section `.cursor/` skip predicate (critic finding 2 — `ik_us0121_mixed_manifest_cursor_skip`)

The existing `[install_include_paths]` mixes kernel rows (`docs`, `sprints`, `handoffs`, `decisions`, `scripts/...`, `.github/workflows`, `its_magic`) with `.cursor/**` rows. The triple-installer must apply a **shared predicate** so the three installers do not diverge:

```python
def host_gates_cursor_row(rel, host):
    # Returns True if the row should be SKIPPED for this host.
    # host in {cursor, opencode, both} (normalized lowercase+trim)
    if host == "opencode":
        return rel.startswith(".cursor/")
    # cursor / both: never skip .cursor/ rows
    return False
```

- When `--host opencode`: `.cursor/` rows in `[install_include_paths]` are **skipped**; kernel rows in the same section are **still installed**; `[opencode_install_include_paths]` rows are installed.
- When `--host cursor` (default): `.cursor/` rows are installed; `[opencode_install_include_paths]` rows are skipped.
- When `--host both`: both sets installed; no skip.
- This predicate is the **interface contract** shared by `installer.ps1`, `installer.sh`, and `installer.py`. AC-7 contract test `test_us0121_mixed_section_cursor_skip_when_host_opencode` enforces parity.


### `--host` parse / normalize / validate (Q12 LOCKED — in `bin/its-magic.js` + PS `-Host` + sh/py `--host`)

**`bin/its-magic.js`** (additive argv parser extension):
- Add `--host <value>` to the argv loop. Accept `cursor`, `opencode`, `both` (case-insensitive, whitespace-trimmed). Default `cursor` when omitted.
- **Normalize**: `value.toLowerCase().trim()` before validate.
- **Validate**: unknown value → exit with reason code `INSTALL_HOST_INVALID` (ASCII diagnostic, no GUI per D11).
- **Duplicate / conflicting `--host`**: if `--host` appears more than once in argv → fail closed `INSTALL_HOST_INVALID` (no last-wins; closes critic finding 1).
- Forward normalized `--host` to PowerShell as `-Host <value>`, to Bash as `--host <value>`.
- `--help` documents `--host cursor|opencode|both` and the cursor-default lock (AC-9 minimal docs hook; full runbook is US-0126).

**`installer.ps1`**: add `-Host` parameter (PowerShell is case-insensitive by default, but normalize anyway for parity with Bash/Python). Apply the `host_gates_cursor_row` predicate + read `[opencode_install_include_paths]` / `[opencode_clean_paths]` when host includes opencode.

**`installer.sh`**: add `--host` argparse (Bash is case-sensitive; normalize lowercase). Same predicate + section reads.

**`installer.py`**: add `--host` argparse (Python argparse is case-sensitive; normalize lowercase). Same predicate + section reads. The Python installer is the manifest authority; PS/Bash delegate manifest reads to it where possible (existing pattern).

### Host-scoped missing / upgrade / clean (Q12 + Q8 LOCKED)

| Mode | `--host cursor` (default) | `--host opencode` | `--host both` |
|------|---------------------------|-------------------|---------------|
| `missing` | Copy `.cursor/` + kernel rows from `[install_include_paths]`; skip `.opencode/` rows. | Skip `.cursor/` rows; copy kernel rows + `[opencode_install_include_paths]`. | Copy all rows (`.cursor/` + kernel + `.opencode/`). |
| `upgrade` | Refresh `.cursor/` + kernel rows; leave `.opencode/` untouched. If `.opencode/` exists from a prior `--host both`, emit `OPENCODE_STALE_BY_UPGRADE_CURSOR` (diagnostic, not an error). | Refresh kernel + `.opencode/` rows; leave `.cursor/` untouched. If `.cursor/` exists from a prior `--host both`, emit `CURSOR_STALE_BY_UPGRADE_OPENCODE` (symmetric diagnostic). | Refresh all rows. |
| `clean` | Remove `[clean_paths]` (cursor-default + kernel); do **not** remove `.opencode/`. If `.opencode/` exists from a prior `--host both`, emit `OPENCODE_ORPHANED_BY_CLEAN_CURSOR` (diagnostic). | Remove `[opencode_clean_paths]` (`.opencode/`); do **not** remove `.cursor/` or kernel paths. If `.cursor/` exists from a prior `--host both`, emit `CURSOR_ORPHANED_BY_CLEAN_OPENCODE` (symmetric diagnostic). | Remove both `[clean_paths]` and `[opencode_clean_paths]`. |

- **Host-shrink `upgrade`/`missing`** (critic finding 1 — `ik_us0121_upgrade_host_transition`): shrinking `--host both` → `cursor` does **not silently delete** `.opencode/`; it leaves the other-host tree in place and emits a named diagnostic (`OPENCODE_STALE_BY_UPGRADE_CURSOR` for upgrade, `OPENCODE_ORPHANED_BY_CLEAN_CURSOR` for clean). The operator must run `clean --host opencode` or `clean --host both` to remove the orphan. Symmetric for `--host opencode` shrinking from `both`.
- **No silent deletion**: the only way to delete `.opencode/` is `clean --host opencode` or `clean --host both`. The only way to delete `.cursor/` (cursor-owned installer paths) is `clean --host cursor` or `clean --host both`.

### Kernel-vs-host copy filter (Q8 LOCKED)

`--host` gates **only** `.cursor/` and `.opencode/` surfaces. Kernel paths install regardless of `--host`:
- `docs/`, `scripts/` (manifest-listed), `its_magic/`, `handoffs/`, `decisions/`, `sprints/`, `.github/workflows/`.

This is the simplest contract satisfying AC-3 (opencode adds `.opencode/`) and AC-4 (cursor-only byte-identical). No exception needed; the rule is "`--host` is a host-surface switch, not a kernel switch."

### Coexistence byte-identity for `--host cursor` (AC-4)

`--host cursor` (default) must be byte-identical on `.cursor/` and Cursor-owned installer paths versus pre-US-0121 cursor-only install. Contract tests enforce:
- `test_us0121_cursor_only_byte_identical_pre_us0121`: install with `--host cursor` into a clean target; compare `.cursor/` tree + manifest-listed kernel paths against a pre-US-0121 baseline snapshot.
- `test_us0121_cursor_only_no_opencode_files`: `--host cursor` install produces zero `.opencode/` files in the target.
- `test_us0121_both_leaves_both_trees`: `--host both` leaves both `.cursor/` and `.opencode/` present.


### AC-7 contract-test list (locked)

`tests/us0121_host_mode_test.py` — markers:

| # | Marker | AC |
|---|--------|-----|
| 1 | `test_us0121_default_host_cursor_when_omitted` | AC-2 |
| 2 | `test_us0121_host_cursor_installs_cursor_and_kernel_no_opencode` | AC-2, AC-3, AC-4 |
| 3 | `test_us0121_host_opencode_skips_cursor_installs_opencode_and_kernel` | AC-2, AC-3, AC-4 |
| 4 | `test_us0121_host_both_installs_both_trees` | AC-2, AC-3, AC-4 |
| 5 | `test_us0121_invalid_host_fails_closed_install_host_invalid` | AC-2 |
| 6 | `test_us0121_host_normalize_case_and_whitespace` (e.g. `OpenCode`, `  opencode  `, `BOTH`) | AC-2 |
| 7 | `test_us0121_duplicate_host_argv_fails_closed` (no last-wins) | AC-2 |
| 8 | `test_us0121_clean_host_cursor_after_both_emits_orphan_diagnostic` (`OPENCODE_ORPHANED_BY_CLEAN_CURSOR`; `.opencode/` left intact) | AC-3, AC-7 |
| 9 | `test_us0121_upgrade_host_cursor_after_both_emits_stale_diagnostic` (`OPENCODE_STALE_BY_UPGRADE_CURSOR`; `.opencode/` left untouched) | AC-3, AC-7 |
| 10 | `test_us0121_mixed_section_cursor_skip_when_host_opencode` (kernel rows from `[install_include_paths]` installed; `.cursor/` rows skipped; `[opencode_install_include_paths]` installed) | AC-5, AC-7 |
| 11 | `test_us0121_manifest_lists_opencode_pack` (grep `[opencode_install_include_paths]` + `.opencode/` rows) | AC-5 |
| 12 | `test_us0121_no_secrets_in_pack` (grep `template/.opencode/**` for `apiKey|api_key|sk-|MODEL=` → zero hits; no vendor slugs) | AC-10 |
| 13 | `test_us0121_parity_scope_opencode_adapter_registered` (`check_intake_template_parity.py --scope=opencode-adapter` runs and fails on drift) | AC-6 |
| 14 | `test_us0121_triple_installer_host_parity` (PS/Bash/Python all normalize, validate, and apply the same skip predicate) | AC-5 |

Surjective AC coverage: AC-1 (pack layout via markers 11+12), AC-2 (markers 1–7), AC-3 (markers 2–4, 8, 9), AC-4 (markers 2–4), AC-5 (markers 10, 11, 14), AC-6 (marker 13), AC-7 (markers 8, 9, 10 + the full set), AC-8 (compose guards verified separately), AC-9 (`--help` grep test), AC-10 (marker 12). Every AC has ≥1 marker.

## Risks mitigated

All 8 risks from R-0109 ACCEPTED, plus critic findings 1–3 closed:

| Risk | Severity | Mitigation |
|------|----------|------------|
| R1: cursor-only install accidentally copies `.opencode/` | MEDIUM → LOW | Q7 parallel manifest sections (opencode sections read only when host includes opencode) + Q8 kernel-vs-host contract; marker 2 enforces. |
| R2: manifest encoding for host-specific paths underspecified | MEDIUM → LOW | Q7 locks parallel sections; section names locked here (`[opencode_install_include_paths]`, `[opencode_clean_paths]`); marker 11 enforces. |
| R3: empty pack rejected by stock OpenCode | LOW–MEDIUM → LOW | Q6 confirms empty dirs + placeholder files are tolerated; marker 11 asserts manifest membership. |
| R4: secret/slug leakage | LOW | D8 + AC-10 + Q10 gitignore patterns; marker 12 enforces. |
| R5: scope creep into US-0122..US-0126 | LOW | D10 + Q9 YAGNI lock; non-goals section below. |
| R6: triple-installer `--host` parsing divergence (case/whitespace) | LOW | Q12 normalize-then-validate; marker 6 enforces. |
| R7: `clean --host cursor` orphan | LOW | Q12 host-scoped `clean` + `OPENCODE_ORPHANED_BY_CLEAN_CURSOR`; marker 8 enforces. |
| R8: `bin/its-magic.js` forgets to forward `--host` | LOW | Q12 forwarding contract; marker 14 enforces triple-installer parity. |
| C1 (critic): host-shrink `upgrade`/`missing` silent stale | MEDIUM → LOW | `OPENCODE_STALE_BY_UPGRADE_CURSOR` + `CURSOR_STALE_BY_UPGRADE_OPENCODE` diagnostics; marker 9 enforces; no silent deletion. |
| C2 (critic): mixed-section `.cursor/` skip divergence | MEDIUM → LOW | Shared `host_gates_cursor_row` predicate locked as interface contract; marker 10 enforces. |
| C3 (critic): gitignore premature patterns | LOW | Q10 four pattern groups kept; no further speculative globs added; documented here as locked. |

## Non-goals (this slice)

- **US-0122** (role agents + Layer-1 permission table) — not filled; `template/.opencode/agents/` ships `.gitkeep` only.
- **US-0123** (per-role `provider/slug` routing) — no `model:` literals in template; no vendor slugs.
- **US-0124** (orchestrator plugin spawn) — `template/.opencode/plugins/` ships `README.md` only; no plugin body; v1 vs v2 deferred (R-0109 Q1).
- **US-0125** (thin command bodies) — `template/.opencode/commands/` ships `.gitkeep` only; no command bodies.
- **US-0126** (full runbook) — `--help` minimal docs hook only; full OpenCode operator runbook deferred.
- **Repo-root `opencode.json`** — not shipped this slice (R-0109 Q6).
- **Active kit `.opencode/` mirror** — YAGNI this slice (R-0109 Q9).
- **VS Code contrib rewrite** — out of scope (D9).
- **OpenCode fork** — out of scope (D9); stock host only.
- **Standalone runtime** — separate plan area; out of scope.

## Compose guards (UNCHANGED — additive only)

| Compose target | Verification | Result |
|---|---|---|
| US-0008 (CLI installer) | inline ref — US-0121 adds additive `--host` only; missing/overwrite/clean/upgrade semantics UNCHANGED | ✅ read-only (additive) |
| DEC-0045 (`its_magic/` ownership) | inline ref — `its_magic/` ownership unchanged | ✅ read-only |
| US-0102 (volatile-ID rule) | inline ref — template ships no vendor slugs; `*.local.json{,c}` gitignore mirrors kit convention | ✅ read-only |
| US-0001 (phase names) | inline ref — phase names may appear as placeholders only; no command body clone | ✅ read-only |
| US-0018 (packaging delivery) | inline ref — installer delivery path unchanged except additive `--host` forward | ✅ read-only |

Contract test `test_us0121_compose_guards_unchanged` enforces at execute boundary.


## Sprint seeds preview (within SPRINT_MAX_TASKS=12)

| Seed | Description | AC |
|------|-------------|-----|
| **T-anch** | Verify `# US-0121` H1 anchor present; compose guards 5/5; DEC-0120 authored; mixed-section predicate contract locked. | AC-8, AC-11 (implicit) |
| **T-001** | NEW `template/.opencode/` tree: `agents/.gitkeep`, `commands/.gitkeep`, `plugins/README.md`, `.gitignore` (Q10 four patterns), `README.md`. | AC-1, AC-10 |
| **T-002** | NEW manifest sections `[opencode_install_include_paths]` + `[opencode_clean_paths]` in active + template manifest (byte-identical). | AC-5 |
| **T-003** | `bin/its-magic.js` additive `--host` argv parser (normalize, validate, duplicate fail-closed) + forward to PS/Bash + `--help` docs hook. | AC-2, AC-9 |
| **T-004** | `installer.ps1` `-Host` parameter + normalize + `host_gates_cursor_row` predicate + opencode section reads. | AC-2, AC-3, AC-5 |
| **T-005** | `installer.sh` `--host` argparse + normalize + same predicate + opencode section reads. | AC-2, AC-3, AC-5 |
| **T-006** | `installer.py` `--host` argparse + normalize + same predicate + opencode section reads + host-scoped missing/upgrade/clean + orphan/stale diagnostics. | AC-3, AC-7 |
| **T-007** | NEW `tests/us0121_host_mode_test.py` (14 markers). | AC-7 |
| **T-008** | `check_intake_template_parity.py --scope=opencode-adapter` registration + `US0121_PARITY_PAIRS` manifest. | AC-6 |
| **T-009** | Runbook `## OpenCode host mode (US-0121)` h2 minimal + installer `--help` line. | AC-9 |

**Total: 9 tasks (T-anch + T-001..T-009) — within `SPRINT_MAX_TASKS=12`.** `/sprint-plan` may merge or split within the 12-task budget.

## DC check

`dc_check=clean`. No `# US-0121` or `## US-0121` existed prior to THIS write. H1 anchor added per DEC-0076 / BUG-0010 heading policy. Deferral register clean.

## Stop conditions

- `decision_gate=false`
- `missing_acceptance_criteria=none` (10/10 ACs covered by 14 contract-test markers + compose guards)
- `compose_guards=5/5 UNCHANGED (additive only)`
- `dc_check=clean`
- Q6–Q12 LOCKED for US-0121 execute; Q1–Q5 LOCKED for `/architecture` only (deferred to US-0122..US-0126); 8/8 R ACCEPTED; A1 locked
- Triad baseline `baseline_h2_count=41` preserved (H1 used, not H2)
- `validator_skipped=python_not_on_path` (Windows Store stub; `py -3` and `python` both missing — exit 9009); H2 count verified via PowerShell `Select-String -Pattern '^## US-'` (41, unchanged from US-0120 baseline)
- `enforce-triad-hot-surface.py --rollover/--check` skipped (python missing); `materialize_codebase_map.py --trigger architecture` skipped (python missing); not blocking per orchestrator brief

## Sovereign memory note

`assemble_sovereign_memory_digest(...)` NOT called. No write to `mistakes.jsonl`.

## Consequences

- **Positive**: Operators can install `.opencode/` into any consumer repo via the existing installer with `--host opencode|both`; cursor-only install remains byte-identical; epic US-0122..US-0126 inherits the host contract via DEC-0120 without re-deriving.
- **Negative**: New template tree; additive manifest sections; additive `--host` argv in 4 installer surfaces; new contract test file (14 markers); new parity scope.
- **Neutral**: US-0008 compose (additive only); DEC-0045 `its_magic/` ownership unchanged; US-0102 volatile-ID rule respected.

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=architecture`, `role=tech-lead`, `story_id=US-0121`, `sprint_id=(pending — created at sprint-plan)`
- `orchestrator_run_id=auto-20260823-01`
- `delivery_mode=ultra_lean`, `macro_phase=plan` (architecture — second canonical phase of `plan` macro per US-0096 / DEC-0082)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 — required; this spawn's producer model)
- `fresh_context_marker=tl-US0121-architecture-20260823T111500Z-fresh`, `timestamp=2026-08-23T11:15:00Z` (UTC)
- `evidence_ref=docs/engineering/architecture.md # US-0121 (this section), decisions/DEC-0120.md (companion DEC), docs/engineering/research.md ## R-0109 (Q6–Q12 LOCKED), docs/product/backlog.md ## US-0121 (D1–D11 + 10 ACs, status OPEN untouched, AC checkboxes untouched), docs/product/acceptance.md US-0121 row (unchecked), docs/product/vision.md ## Discovery Notes — US-0121, handoffs/po_to_tl.md US-0121 top section, handoffs/sovereign_critic_findings.jsonl last 3 rows (ik_us0121_upgrade_host_transition, ik_us0121_mixed_manifest_cursor_skip, ik_us0121_gitignore_premature_patterns), docs/engineering/architecture.md # US-0120 (format template), docs/engineering/decisions.md ## DEC-0119 (last DEC id), docs/engineering/context/installer-owned-paths.manifest (existing sections), bin/its-magic.js (argv parser surface), installer.ps1/installer.sh/installer.py (manifest read surfaces)`
- Fresh tech-lead subagent per BUG-0006 / US-0048 isolation; no prior chat history carried forward. Context limited to narrow-read files (US-0053). No `.env` reads, no credentials access, no intake-evidence mutation, no backlog status/AC mutation.
- Prior proof consumed: `rp-auto-20260823-01-research-tech-lead-20260823T123800Z-US-0121` (from `docs/engineering/state.md` research checkpoint, unchanged).
- Triad baseline `baseline_h2_count=41` preserved via H1 anchor (no new H2 `## US-` headings added).

## Strict runtime proof (DEC-0038)

- `runtime_proof_id=rp-auto-20260823-01-architecture-tech-lead-20260823T111500Z-US-0121`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"plan","orchestrator_run_id":"auto-20260823-01","phase_id":"architecture","proof_issued_at":"2026-08-23T11:15:00Z","proof_ttl_seconds":3600,"role":"tech-lead","runtime_proof_id":"rp-auto-20260823-01-architecture-tech-lead-20260823T111500Z-US-0121","sprint_id":"(pending)","story_id":"US-0121"}`
- `proof_hash=753a25c11f5ca67aee2e3d4915544d744f3635a1a4433289c03e93c8732ed99e` (SHA-256, UTF-8 bytes via PowerShell — python missing on PATH)
- `proof_ttl_seconds=3600`, `proof_ttl=2026-08-23T12:15:00Z` (UTC)

## Decision gate

- `decision_gate=false` (companion DEC-0120 authored Accepted in THIS phase; approach A1 locked; Q6–Q12 LOCKED for execute; Q1–Q5 LOCKED for architecture only; 8/8 R ACCEPTED; critic findings 1–3 closed; DC check clean; compose guards 5/5 UNCHANGED)
- `stop_conditions_met=yes`

## Next scheduled phase

- `next_scheduled_phase=/sprint-plan` (role=tech-lead per US-0069 / DEC-0051 phase→role matrix default; third canonical phase of `plan` macro per ultra_lean; research + architecture + sprint-plan merged into `plan` macro)
- `next_scheduled_role=tech-lead`
- `stop_condition=STOP after architecture completes; hand off via artifacts only to /sprint-plan in fresh tech-lead subagent (BUG-0006). Do not spawn /sprint-plan from this subagent.`

---


---

---

