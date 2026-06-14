# Sprint S0090 Tasks — US-0100

**sprint_id**: S0090  
**story_refs**: US-0100  
**dec_ref**: DEC-0085 (binding; composes US-0040, US-0054, US-0067, US-0008; research R-0087)  
**task_count**: 12  
**within_limit**: true (12 ≤ `SPRINT_MAX_TASKS=12`; `SPRINT_AUTO_SPLIT` not triggered)  
**coverage**: AC-1..AC-10 surjective via T-001..T-012 (10 ACs, 12 tasks; architecture seeds 1:1; AC-10 pre-satisfied at architecture; multi-AC tasks T-001, T-004, T-007, T-008, T-011, T-012)

> No implementation or test code is authored in this phase — dev owns delivery in `/execute`.

---

## T-001 — **`release_changelog_lib.py`** — API surface + coalesce + fingerprint idempotency — AC-3, AC-7

- **ac_ref**: AC-3, AC-7
- **dec_ref**: DEC-0085 §3; architecture `# US-0100` § `release_changelog_lib.py` API; § Reason codes
- **description**: Implement **`scripts/release_changelog_lib.py`** (+ template mirror) with required symbols per **DEC-0085** §3: **`normalize_semver`**, **`derive_work_items`**, **`coalesce_sprints_by_semver`**, **`build_version_doc`**, **`promote_unreleased`**, **`append_unreleased`**, **`version_fingerprint`**, **`bind_queue_release_version`**, **`extract_changelog_section`**. Derivation precedence (sprint notes → backlog → queue) in docstring/constants. Fingerprint idempotency per semver; informational **`RELEASE_CHANGELOG_IDEMPOTENCY_OK`**; fail codes **`DUPLICATE_VERSION`**, **`IDEMPOTENCY_VIOLATION`**.
- **files_affected**:
  - `scripts/release_changelog_lib.py`
  - `template/scripts/release_changelog_lib.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 1; **`RELEASE_CHANGELOG_PAIRS`** lib pair.
- **acceptance_check**:
  - All nine API symbols defined and importable.
  - **`derive_work_items`** follows L4 precedence order documented in lib.
  - **`version_fingerprint`** = semver + sorted work_item_ids.
  - **`coalesce_sprints_by_semver`** groups **`released`** rows by normalized semver.
  - Category map: US→Added, BUG→Fixed, user_visible:false→Changed.
  - Active/template lib byte-identical for touched symbols.
- **status**: done

---

## T-002 — **`CHANGELOG.md`** stub + **`template/CHANGELOG.md`** — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0085 §1; architecture `# US-0100` § Artifact paths
- **description**: Create repo-root **`CHANGELOG.md`** with Keep a Changelog 1.1.0 header and mandatory top **`## [Unreleased]`** section (empty). Mirror stub in **`template/CHANGELOG.md`** for installer/template parity.
- **files_affected**:
  - `CHANGELOG.md`
  - `template/CHANGELOG.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 2; **`RELEASE_CHANGELOG_PAIRS`** changelog pair.
- **acceptance_check**:
  - **`CHANGELOG.md`** exists at repo root with **`[Unreleased]`** section.
  - Semver sections newest-first convention documented in header comment.
  - **`template/CHANGELOG.md`** byte-matches active stub structure.
  - No historical backfill content in stub — backfill is T-007/T-008.
- **status**: done

---

## T-003 — Per-version path convention + **`vX.Y.Z-release-notes.md.example`** — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0085 §1; architecture `# US-0100` § Artifact paths
- **description**: Document and scaffold per-version path **`handoffs/releases/{semver}-release-notes.md`** (semver stem without leading **`v`**). Add **`template/handoffs/releases/vX.Y.Z-release-notes.md.example`** with minimum sections: **`## Work items`**, **`## Sprint evidence`**. Example is pattern doc only — not a live semver file.
- **files_affected**:
  - `template/handoffs/releases/vX.Y.Z-release-notes.md.example`
- **parity_touchpoints**: architecture § Atomic task seeds row 3; **`test_us0100_changelog_artifact_paths_literals`**.
- **acceptance_check**:
  - Example file documents rename-at-use pattern.
  - Path literals **`{semver}-release-notes.md`** grep-able in architecture/DEC.
  - Per-version docs must not overwrite unrelated version files (documented in example header).
  - Pre-release stem example (e.g. **`0.1.2-41`**) noted without **`v`** prefix.
- **status**: done

---

## T-004 — **`/release`** step **19** (19a–19d) active + template **`release.md`** — AC-3, AC-4, AC-8

- **ac_ref**: AC-3, AC-4, AC-8
- **dec_ref**: DEC-0085 §5; architecture `# US-0100` § `/release` touchpoint — step 19
- **description**: Append step **19** after step **18** operator hints in **`.cursor/commands/release.md`** (+ template byte-identical): **19a** resolve semver; **19b** **`derive_work_items`** + coalesce peers; **19c** semver known → **`build_version_doc`** + **`promote_unreleased`** + **`bind_queue_release_version`** else **`append_unreleased`**; **19d** when **`RELEASE_CHANGELOG_ENFORCE=1`** → **`release_changelog_validate.py --enforce`**; record in **`release-findings.md`** § version-doc gates.
- **files_affected**:
  - `.cursor/commands/release.md`
  - `template/.cursor/commands/release.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 4; **`test_us0100_release_step19_literals`**; **`RELEASE_CHANGELOG_PAIRS`** release.md pair.
- **acceptance_check**:
  - Step **19** sub-steps **19a–19d** present in active + template **`release.md`**.
  - Placement after step **9** finalization context and step **18** operator hints documented.
  - **`RELEASE_CHANGELOG_ENFORCE`** default **`1`** documented.
  - Doc writes explicitly not publish (**US-0054** compose).
  - Contract subtest **`test_us0100_release_step19_literals`** passes (after T-011).
- **status**: done

---

## T-005 — Queue **`release_version`** binding via **`bind_queue_release_version`** — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0085 §3 (`bind_queue_release_version`); architecture `# US-0100` § Derivation precedence
- **description**: Wire **`bind_queue_release_version(sprint_ids, semver, repo_root)`** in lib (T-001) to mutate only target sprint queue rows in **`handoffs/release_queue.md`**. Populate **`release_version`** deterministically on finalization; cross-reference **`sprint_id`**, **`story_refs`**, and **`handoffs/releases/Sxxxx-release-notes.md`** in per-version doc **`## Sprint evidence`** section.
- **files_affected**:
  - `scripts/release_changelog_lib.py` (binding logic — delivered in T-001; this task verifies integration)
  - `handoffs/release_queue.md` (schema contract only — no test mutations in execute)
- **parity_touchpoints**: architecture § Atomic task seeds row 5; queue row target-scoped mutation guard.
- **acceptance_check**:
  - **`bind_queue_release_version`** mutates only specified sprint rows.
  - Unrelated sprint rows unchanged on bind.
  - Per-version doc **`## Sprint evidence`** links contributing **`Sxxxx`** notes.
  - Workflow-only release (no semver) leaves **`release_version`** empty; **`append_unreleased`** only.
- **status**: done

---

## T-006 — **`release_changelog_validate.py`** + 10 reason codes — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0085 §9; architecture `# US-0100` § Reason codes
- **description**: Implement **`scripts/release_changelog_validate.py`** (+ template mirror) with **`--enforce`** CLI. Ten fail-closed codes: **`VERSION_MISSING`**, **`DUPLICATE_VERSION`**, **`WORK_ITEM_GAP`**, **`ORDER_INVALID`**, **`UNRELEASED_MISSING`**, **`QUEUE_DRIFT`**, **`VERSION_DOC_MISSING`**, **`SPRINT_ORPHAN`**, **`BACKFILL_AMBIGUOUS`**, **`IDEMPOTENCY_VIOLATION`**. Informational **`IDEMPOTENCY_OK`**. Remediation text per code.
- **files_affected**:
  - `scripts/release_changelog_validate.py`
  - `template/scripts/release_changelog_validate.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 6; **`test_us0100_reason_code_inventory`**; **`RELEASE_CHANGELOG_PAIRS`** validator pair.
- **acceptance_check**:
  - All 10 fail codes emitted on stderr with **`RELEASE_CHANGELOG_`** prefix family.
  - **`--enforce`** exits non-zero on any fail code.
  - Checks: changelog ordering, required US/BUG refs, queue/changelog consistency.
  - Active/template validator byte-identical.
  - Contract subtest **`test_us0100_reason_code_inventory`** passes (after T-011).
- **status**: done

---

## T-007 — **`release_changelog_backfill.py`** three-tier A/B/C — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0085 §6; architecture `# US-0100` § Coalesce + backfill
- **description**: Implement **`scripts/release_changelog_backfill.py`** (+ template mirror) for idempotent one-time seed: **Tier A** explicit queue semver; **Tier B** operator manifest overrides; **Tier C** synthetic **`0.0.0-wf.{NNN}`** per sprint when semver blank. Coalesce by normalized semver; dedupe work items; exemplar **`S0070`/`S0071`→`0.1.2-41`**.
- **files_affected**:
  - `scripts/release_changelog_backfill.py`
  - `template/scripts/release_changelog_backfill.py`
- **parity_touchpoints**: architecture § Atomic task seeds row 7; **`RELEASE_CHANGELOG_PAIRS`** backfill pair.
- **acceptance_check**:
  - Three-tier precedence: queue semver → manifest → synthetic.
  - Re-run is idempotent (no duplicate version sections).
  - Sources from existing **`released`** queue rows + **`Sxxxx`** notes only.
  - **`BACKFILL_AMBIGUOUS`** fail-closed when Tier B conflicts.
  - Active/template backfill script byte-identical.
- **status**: done

---

## T-008 — **`release-version-backfill.manifest.yaml`** + runbook operator guidance — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0085 §6; architecture `# US-0100` § Coalesce + backfill
- **description**: Create **`docs/engineering/context/release-version-backfill.manifest.yaml`** with **`schema_version: 1`**, **`entries[]`** (`sprint_id`, `semver`, optional `notes`). Document Tier B operator remediation in **`docs/engineering/runbook.md`** (partial — full version-doc workflow completed in T-010).
- **files_affected**:
  - `docs/engineering/context/release-version-backfill.manifest.yaml`
  - `docs/engineering/runbook.md` (backfill subsection — active + template in T-010)
- **parity_touchpoints**: architecture § Atomic task seeds row 8; **`test_us0100_backfill_manifest_schema_literals`**.
- **acceptance_check**:
  - Manifest schema **`schema_version: 1`** + **`entries`** shape validated.
  - Operator remediation column for ambiguous rows documented.
  - Synthetic semver **`0.0.0-wf.{NNN}`** labeling explained.
  - Contract subtest **`test_us0100_backfill_manifest_schema_literals`** passes (after T-011).
- **status**: done

---

## T-009 — **`release-all.sh`** **`-F`** replace **`--generate-notes`** + enforce preflight — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0085 §7; architecture `# US-0100` § `release-all.sh` touchpoint
- **description**: Replace L94–99 **`gh release create --generate-notes`** in **`scripts/release-all.sh`**: (1) ensure **`handoffs/releases/${NEW_VERSION}-release-notes.md`** exists (derive/coalesce via lib CLI if needed); (2) **`python scripts/release_changelog_validate.py --repo . --enforce`**; (3) **`gh release create "$TAG_NAME" -F "$VERSION_NOTES" --title "$TAG_NAME" $GH_PRERELEASE`**; (4) fail-closed **`RELEASE_CHANGELOG_VERSION_DOC_MISSING`** unless **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=1`**.
- **files_affected**:
  - `scripts/release-all.sh`
- **parity_touchpoints**: architecture § Atomic task seeds row 9; **`test_us0100_release_all_f_replace_literals`**; **`RELEASE_CHANGELOG_PAIRS`** release-all.sh pair.
- **acceptance_check**:
  - **`-F`** flag used instead of **`--generate-notes`** when version doc exists.
  - Validator **`--enforce`** runs before **`gh`** attach.
  - Fail-closed branch documented when notes file missing.
  - **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES=0`** default preserved.
  - Contract subtest **`test_us0100_release_all_f_replace_literals`** passes (after T-011).
- **status**: done

---

## T-010 — **`docs/engineering/runbook.md`** version-doc workflow (active + template) — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0085 §8; architecture `# US-0100` § Scratchpad keys
- **description**: Update **`docs/engineering/runbook.md`** (+ template mirror) with version-doc operator workflow: local **`/release`** vs **`release-all.sh`** vs CI tag push; GitHub release body SOT = per-version file; **`RELEASE_CHANGELOG_ENFORCE`** / **`RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES`** scratchpad keys; compose with **US-0054** publish mode.
- **files_affected**:
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: architecture § Atomic task seeds row 10; **`RELEASE_CHANGELOG_PAIRS`** runbook pair.
- **acceptance_check**:
  - Version-doc touchpoints documented with deterministic step order.
  - Per-version file = GitHub **`-F`** SOT; sprint notes = workflow evidence only.
  - Scratchpad keys table matches architecture § Scratchpad keys.
  - Active/template runbook parity for touched sections.
- **status**: done

---

## T-011 — Ten **`test_us0100_*`** contract subtests — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0085 §10; architecture `# US-0100` § Contract tests + parity
- **description**: Add ten contract subtests in **`tests/auto_command_contract_test.py`**: **`test_us0100_changelog_artifact_paths_literals`**, **`test_us0100_release_changelog_lib_api_surface`**, **`test_us0100_reason_code_inventory`**, **`test_us0100_derivation_precedence_literals`**, **`test_us0100_release_step19_literals`**, **`test_us0100_release_all_f_replace_literals`**, **`test_us0100_backfill_manifest_schema_literals`**, **`test_us0100_unreleased_promotion_literals`**, **`test_us0100_compose_us0040_sprint_notes_unchanged`**, **`test_us0100_template_parity_scope`**. Run `pytest -k us0100` → all ten green.
- **files_affected**:
  - `tests/auto_command_contract_test.py`
- **parity_touchpoints**: architecture § Contract tests table; active-only.
- **acceptance_check**:
  - All ten **`test_us0100_*`** function names present with assertions per architecture table.
  - `pytest -k us0100 tests/auto_command_contract_test.py` exits 0 after T-001..T-010 edits.
  - **`test_us0100_compose_us0040_sprint_notes_unchanged`** verifies **`Sxxxx`** path preserved.
- **status**: done

---

## T-012 — **`RELEASE_CHANGELOG_PAIRS`** parity + harness **§26Y** — AC-9, AC-10

- **ac_ref**: AC-9, AC-10
- **dec_ref**: DEC-0085 §11; architecture `# US-0100` § Contract tests + parity (Harness)
- **description**: Register **`RELEASE_CHANGELOG_PAIRS`** in **`scripts/check_intake_template_parity.py`** (+ template mirror) with **`--scope=release-changelog`**. Register harness section **§26Y** (next after **§26X**) in **`tests/run-tests.ps1`** + **`tests/run-tests.sh`** covering `pytest -k us0100` and `python scripts/check_intake_template_parity.py --scope=release-changelog`.
- **files_affected**:
  - `scripts/check_intake_template_parity.py`
  - `template/scripts/check_intake_template_parity.py`
  - `tests/run-tests.ps1`
  - `tests/run-tests.sh`
- **parity_touchpoints**: architecture § Atomic task seeds row 12; harness **§26Y**; **`test_us0100_template_parity_scope`**.
- **acceptance_check**:
  - **`RELEASE_CHANGELOG_PAIRS`** table covers scripts, **`CHANGELOG.md`**, **`release.md`** step **19**, **`release-all.sh`**, template example.
  - Harness **§26Y** registered in both run-tests scripts.
  - `python scripts/check_intake_template_parity.py --scope=release-changelog` → **`[INTAKE_TEMPLATE_PARITY_OK]`**.
  - Contract subtest **`test_us0100_template_parity_scope`** passes.
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — `release_changelog_lib.py` API (Tranche A)
2. **T-002** → **T-003** — CHANGELOG stub + per-version example (Tranche A)
3. **T-006** — validator (Tranche C — after lib)
4. **T-004** → **T-005** — `/release` step 19 + queue binding (Tranche B)
5. **T-007** → **T-008** — backfill script + manifest (Tranche C)
6. **T-009** — `release-all.sh` `-F` (Tranche D)
7. **T-010** — runbook version-doc workflow (Tranche E)
8. **T-011** — contract subtests (after scripts/docs)
9. **T-012** — harness §26Y + parity sweep (last)
