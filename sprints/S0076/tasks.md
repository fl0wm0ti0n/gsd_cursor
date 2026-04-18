# Sprint S0076 Tasks — US-0090

**sprint_id**: S0076  
**story_refs**: US-0090  
**dec_ref**: DEC-0073 (binding; composes on DEC-0072 via forward-link)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered

> AC-to-task bijection is per-AC surjective (every AC has ≥1 task); multi-AC tasks are justified by the **Architecture Addendum — US-0090** in `handoffs/po_to_tl.md` and cited inline per task. No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — `scripts/caveman_compress_input.py` (v1)

- **ac_ref**: AC-1, AC-2, AC-3, AC-4, AC-5 (multi-AC — Addendum seed #1: "script is the CLI contract; five ACs land inside one binary by design")
- **dec_ref**: DEC-0073 §2 (activation gate), §3 (sidecar atomic write), §4 + §4.1 (deny-list source of truth + baseline), §5 + §5.1 (allow-list grammar + `docs-prose-only` profile), §6 (safe-mode algorithm), §7 (9-code reason vocabulary), §8 (CLI contract)
- **description**: Create new Python 3.10+ stdlib-only script (`argparse`, `hashlib`, `json`, `os`, `pathlib`, `re`, `sys`) implementing: activation gating (mode + scope + explicit `--write`), deny-list evaluation (hard-coded baseline + optional `.gitignore` merge + optional `.cursorignore` overlay; deny always wins), allow-list grammar (named profile / raw globs / hybrid; `docs-prose-only` frozen profile), sidecar-first atomic write under `docs/.caveman-originals/<relative/path>/<file>`, safe-mode minifier (line collapse → trailing-whitespace trim → LF normalization), 9-code reason-code vocabulary in 3 families (Gating / Scope / Integrity), flags `--dry-run` (default) / `--write` / `--verify-originals` / `--report` (mutually exclusive with `--write`; conflict → `CAVEMAN_COMPRESS_FLAG_CONFLICT`), pre-write and post-transform 9-zone literal-region equality check, and `--report` JSON output including stable `deny_list_version` SHA-256.
- **files_affected**:
  - `scripts/caveman_compress_input.py` (new)
  - `template/scripts/caveman_compress_input.py` (new — byte-identical mirror)
- **parity_touchpoints**: Positive parity row 1 (DEC-0073 §9). Active / template byte-identical.
- **acceptance_check** (QA verification):
  - File exists at both active + template paths; SHA-256 equal.
  - `python scripts/caveman_compress_input.py --help` exits 0 and documents all four flags.
  - `python scripts/caveman_compress_input.py --write` without env vars exits non-zero with JSON reason `CAVEMAN_COMPRESS_MODE_DISABLED`.
  - `CAVEMAN_COMPRESS_INPUT=1 python scripts/caveman_compress_input.py --write` with empty `CAVEMAN_FILE_SCOPE` exits non-zero with reason `CAVEMAN_COMPRESS_SCOPE_EMPTY`.
  - `--dry-run --write` exits non-zero with reason `CAVEMAN_COMPRESS_FLAG_CONFLICT`.
  - `--report` emits JSON containing `deny_list_version` field with SHA-256 hex string (64 chars).
  - Attempting to compress any path matching DEC-0073 §4.1 deny baseline (e.g., `.env`, `docs/product/backlog.md`, `decisions/DEC-0073.md`) fails closed with reason `CAVEMAN_COMPRESS_DENY_HIT` — even if `CAVEMAN_FILE_SCOPE` nominally allows it (deny wins).
  - Script uses stdlib only (no `import` of third-party packages).
- **status**: done

---

## T-002 — Runbook subsection (Caveman input compression)

- **ac_ref**: AC-5
- **dec_ref**: DEC-0073 §8 (CLI contract documentation), §9 row 2 (runbook parity)
- **description**: Append a runbook subsection to `docs/engineering/runbook.md` documenting the 3-step operator flow — (1) `--dry-run` (default; inspect plan), (2) `--verify-originals` (detect orphan sidecars pre-write), (3) `--write` — plus manual revert procedure (restore from sidecar), three-axis non-substitution reminder (TOKEN_PROFILE × CAVEMAN_MODE × CAVEMAN_COMPRESS_INPUT are orthogonal), and explicit `.cursorignore` is operator-owned note (US-0085 / DEC-0071). Mirror byte-identically to `template/docs/engineering/runbook.md`.
- **files_affected**:
  - `docs/engineering/runbook.md` (append subsection)
  - `template/docs/engineering/runbook.md` (byte-identical mirror)
- **parity_touchpoints**: Positive parity row 2 (DEC-0073 §9). Active / template byte-identical on the appended subsection block.
- **acceptance_check**:
  - Subsection heading exists at both active + template paths.
  - Section diffs byte-identical across `active` vs `template/` for the appended block.
  - Subsection mentions all four CLI flags (`--dry-run`, `--write`, `--verify-originals`, `--report`).
  - Three-axis non-substitution sentence present verbatim.
  - `.cursorignore` operator-owned note present.
- **status**: done

---

## T-003 — Three-axis non-substitution paragraph (reference doc)

- **ac_ref**: AC-7
- **dec_ref**: DEC-0073 §1 (three-axis non-substitution publishing), §9 row 3 (reference parity)
- **description**: Replace the existing two-sentence paragraph in `docs/engineering/auto-orchestration-reference.md` discussing Caveman mode with an extended three-sentence paragraph establishing **TOKEN_PROFILE × CAVEMAN_MODE × CAVEMAN_COMPRESS_INPUT** as three orthogonal axes that never substitute for one another. Mirror byte-identically to `template/docs/engineering/auto-orchestration-reference.md`.
- **files_affected**:
  - `docs/engineering/auto-orchestration-reference.md`
  - `template/docs/engineering/auto-orchestration-reference.md` (byte-identical)
- **parity_touchpoints**: Positive parity row 3 (DEC-0073 §9). Active / template byte-identical.
- **acceptance_check**:
  - Paragraph is three sentences long (not two).
  - All three axes named explicitly.
  - No rewrite of any surrounding paragraph (diff localized to the target paragraph + its mirror).
  - Active / template SHA-256 equal.
- **status**: done

---

## T-004 — Sidecar tree anchor (`.gitignore` + `.gitkeep`)

- **ac_ref**: AC-2
- **dec_ref**: DEC-0073 §3 (sidecar originals policy — parallel tree + anchor)
- **description**: Add an anchor entry in repo-root `.gitignore` (e.g., `# US-0090 Caveman input sidecar originals\ndocs/.caveman-originals/**` — exact string locked by DEC-0073 §3) and create empty anchor file `docs/.caveman-originals/.gitkeep`. Installer does not own repo-root `.gitignore`; therefore no `template/` mirror.
- **files_affected**:
  - `.gitignore` (append anchor block)
  - `docs/.caveman-originals/.gitkeep` (new empty file)
- **parity_touchpoints**: Active-only (DEC-0073 §9 row 7). No `template/` mirror.
- **acceptance_check**:
  - `.gitignore` contains the US-0090 anchor block (exact DEC-0073 §3 string).
  - `docs/.caveman-originals/.gitkeep` exists and is zero-byte (or contains only LF).
  - `docs/.caveman-originals/` tracked in git via `.gitkeep`.
  - Running T-001's script with a whitelisted target produces sidecar at the correct parallel path.
- **status**: done

---

## T-005 — Contract-test extension (`tests/auto_command_contract_test.py`) — grouped seeds 5 + 7

- **ac_ref**: AC-6, AC-8 (multi-AC — Addendum seed #5 + seed #7: "same test file; grouping to minimize test-file churn while keeping rule byte-identity (R10) and deny-list version (§4.2) drift-detection guards in the same subtest class")
- **dec_ref**: DEC-0073 §6 (test strategy), §7 (9-code vocabulary completeness), §9 row 1 (script SHA-256 positive parity), §9 negative-parity set (rule byte-identity — R10)
- **description**: In-place extension of `tests/auto_command_contract_test.py` with a new `test_caveman_compress_input_*` subtest class covering the eleven assertions enumerated in `sprints/S0076/sprint.md` Test strategy § Contract tests (1–11): script presence + SHA-256 parity, default behavior, gating (mode / scope / conflict), unknown-profile handling, deny-first evaluation, sidecar anchor + `.gitkeep` presence, **`.cursor/rules/caveman.mdc` active vs template SHA-256 equality (R10 — seed 7a)**, **`--report` `deny_list_version` stable SHA-256 (seed 7b)**, and reason-code vocabulary cardinality = 9 in 3 families (R9). Existing `test_caveman_default_off_*` subtests MUST remain byte-unchanged (DEC-0072 §6 row 6).
- **files_affected**:
  - `tests/auto_command_contract_test.py` (extend only; preserve S0075 subtest bodies)
- **parity_touchpoints**: Active-only (tests do not mirror).
- **acceptance_check**:
  - New subtest class present; eleven assertions pass under `pytest`.
  - Existing `test_caveman_default_off_*` bodies byte-unchanged (diff scoped to additions).
  - Rule file SHA-256 equality subtest asserts baseline `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE`.
  - Reason-code cardinality subtest asserts exactly 9 codes grouped in 3 families (Gating / Scope / Integrity).
  - Deny-list version subtest asserts `deny_list_version` SHA-256 hex is 64 chars + matches a pinned baseline.
  - Test run green under both `tests/run-tests.ps1` and `tests/run-tests.sh` harnesses.
- **status**: done

---

## T-006 — Fixture directory (`tests/fixtures/caveman_compress/`)

- **ac_ref**: AC-6
- **dec_ref**: DEC-0073 §9 test-strategy block (fixture classes 1–8)
- **description**: Create `tests/fixtures/caveman_compress/` with the eight fixture classes: (1) whitespace baseline, (2) literal-region preservation — one fixture per DEC-0072 §4 zone (9 files), (3) deny-list refusal — one fixture per §4.1 entry class, (4) scope violation, (5) idempotency (`compress(compress(f)) == compress(f)`), (6) mode-disabled, (7) original-missing, (8) flag-conflict.
- **files_affected**:
  - `tests/fixtures/caveman_compress/**` (new tree)
- **parity_touchpoints**: Active-only (fixtures do not mirror).
- **acceptance_check**:
  - All eight fixture class directories exist.
  - Fixture class #2 has 9 sub-fixtures (one per DEC-0072 §4 zone).
  - Fixture class #3 has one sub-fixture per DEC-0073 §4.1 deny entry.
  - Fixture class #5 idempotency pair: `input.txt` + `expected.txt` byte-identical after compression.
  - T-005 contract subtests load fixtures successfully.
- **status**: done

---

## T-007 — Installer manifest entry

- **ac_ref**: AC-8
- **dec_ref**: DEC-0073 §10 (installer-completeness — BUG-0003 class) + §9 row 8 (manifest parity)
- **description**: Add a manifest row for `scripts/caveman_compress_input.py` in `docs/engineering/context/installer-owned-paths.manifest` so all three installer entrypoints (`installer.sh`, `installer.ps1`, `installer.py`) deliver the new script in `--mode missing` + `--mode upgrade` executions. Mirror byte-identically to `template/docs/engineering/context/installer-owned-paths.manifest`.
- **files_affected**:
  - `docs/engineering/context/installer-owned-paths.manifest`
  - `template/docs/engineering/context/installer-owned-paths.manifest`
- **parity_touchpoints**: Positive parity row 8 (DEC-0073 §9). Active / template byte-identical.
- **acceptance_check**:
  - Manifest contains a row for `scripts/caveman_compress_input.py`.
  - Active / template diff zero.
  - Installer dry-runs (all three entrypoints) list `scripts/caveman_compress_input.py` as an owned path.
- **status**: done

---

## T-008 — Parity-test extension (`scripts/check_intake_template_parity.py --scope=caveman-compress`)

- **ac_ref**: AC-8
- **dec_ref**: DEC-0073 §9 row 9 (parity-script self-coverage)
- **description**: Extend `scripts/check_intake_template_parity.py` with a new `--scope=caveman-compress` mode that asserts byte equality across DEC-0073 §9 positive-parity rows (1 / 2 / 3 / 8 + self row 9) and asserts negative-parity invariants (rule file SHA-256 baseline, DEC-0072 §3 key byte strings present). Mirror byte-identically to `template/scripts/check_intake_template_parity.py`.
- **files_affected**:
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py` (byte-identical)
- **parity_touchpoints**: Positive parity row 9 (DEC-0073 §9). Active / template byte-identical.
- **acceptance_check**:
  - `python scripts/check_intake_template_parity.py --scope=caveman-compress` exits 0 on a clean tree.
  - Manually mutating any §9 row 1 / 2 / 3 / 8 active vs template causes exit non-zero with a clear `PARITY_DRIFT_DETECTED` reason.
  - Mutating `.cursor/rules/caveman.mdc` SHA-256 away from baseline causes exit non-zero.
  - Active / template diff zero for the parity script.
- **status**: done

---

## T-009 — Install-completeness + harness extension

- **ac_ref**: AC-6, AC-8 (multi-AC — Addendum seed #10: "tests live under AC-6; installer / harness surface is AC-8 — single fixture + harness row lands both")
- **dec_ref**: DEC-0073 §10 (install-completeness — R11 mitigation; BUG-0001 / DEC-0063 + BUG-0003 / DEC-0066 class non-regression)
- **description**: Extend `tests/installer_completeness_bug0003_test.py` with a new assertion class verifying `--mode missing` + `--mode upgrade` for all three installer entrypoints deliver `template/scripts/caveman_compress_input.py`. Wire new contract subtests + install-completeness class into `tests/run-tests.ps1` and `tests/run-tests.sh` as a new section (candidate `§26S`; dev locks exact number during /execute to match last assigned).
- **files_affected**:
  - `tests/installer_completeness_bug0003_test.py` (extend)
  - `tests/run-tests.ps1` (add section)
  - `tests/run-tests.sh` (add section)
- **parity_touchpoints**: Active-only (tests + harness do not mirror).
- **acceptance_check**:
  - Install-completeness subtest asserts `template/scripts/caveman_compress_input.py` delivered by `installer.sh`, `installer.ps1`, `installer.py` in both `--mode missing` and `--mode upgrade`.
  - Harness section invokes both contract subtests (T-005) and install-completeness subtest (T-009) in PS1 + SH.
  - `bash tests/run-tests.sh` and `pwsh tests/run-tests.ps1` exit 0 on a clean tree; section number is monotonically the next unassigned.
- **status**: done

---

## T-010 — Architecture linkage check (assert-only)

- **ac_ref**: AC-7
- **dec_ref**: DEC-0073 §1 (three-axis publishing), §11 (cross-cutting non-goal — no architecture rewrite this sprint) + DEC-0072 §7 row 6 active-only precedent (`docs/engineering/architecture.md` has no `template/` mirror)
- **description**: Add an assert-only linkage subtest (may live in `tests/auto_command_contract_test.py` or `tests/test_architecture_links.py` — dev picks in `/execute` per existing precedent for linkage-only tests) verifying `docs/engineering/architecture.md` `# US-0090` section exists, references `DEC-0073` + `DEC-0072` + `R-0073`, and names links back to `# US-0089`, US-0053, US-0085, US-0078 / DEC-0060. No mutation of the architecture document in this sprint.
- **files_affected**:
  - `tests/auto_command_contract_test.py` or `tests/test_architecture_links.py` (assert-only addition)
- **parity_touchpoints**: Active-only (tests do not mirror; architecture active-only per DEC-0072 §7 row 6).
- **acceptance_check**:
  - Linkage subtest present and green.
  - Subtest asserts presence of strings: `# US-0090`, `DEC-0073`, `DEC-0072`, `R-0073`, `# US-0089`, `US-0053`, `US-0085`, `US-0078`, `DEC-0060`.
  - No modification of `docs/engineering/architecture.md` during `/execute` beyond what was authored at `/architecture` (assert-only posture).
  - No new `template/` files created (active-only invariant preserved).
- **status**: done

---

## Cross-cutting (DEC-0073 §11 absorption)

§11 cross-cutting integration / invariant concerns are absorbed as per-task acceptance checks (not a separate task), as recommended by the orchestrator handoff:

- **Three-axis non-substitution** — T-002 (runbook), T-003 (reference), T-005 (contract-test presence assertion).
- **No DEC-0072 rewrite** — sprint non-goal; enforced at plan-verify (governance check).
- **Negative-parity preservation** (`.cursor/rules/caveman.mdc`, scratchpad byte-strings, `SKILL.md`) — T-005 subtests #9 + deny evaluation; DEC-0072 §6 row 6 invariant preserves existing S0075 subtests byte-unchanged.
- **No mandatory auto-compress in `/auto`** — T-002 documents out-of-band operator workflow.
- **`.cursorignore` operator-owned** — T-002 runbook note; T-001 only reads it as optional overlay (deny accumulates).
- **Status authority** — US-0090 stays **OPEN** through plan-verify / execute / qa / verify-work; closure at `/release` only.
