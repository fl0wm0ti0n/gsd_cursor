# Sprint S0077 Tasks — US-0091

**sprint_id**: S0077  
**story_refs**: US-0091  
**dec_ref**: DEC-0074 (binding; composes on DEC-0059)  
**task_count**: 10  
**within_limit**: true (10 ≤ `SPRINT_MAX_TASKS=12`); `SPRINT_AUTO_SPLIT` not triggered  
**bijection**: AC-1..AC-10 ↔ T-001..T-010 (strict 1:1)

> No implementation or test code is authored in this phase — dev owns that in `/execute`.

---

## T-001 — Predicate library (`readme_feature_coverage_lib.py`) — AC-1

- **ac_ref**: AC-1
- **dec_ref**: DEC-0074 §1 (Option A predicate), §2 (H1–H8 migration heuristic)
- **description**: Create stdlib-only `scripts/readme_feature_coverage_lib.py` (+ byte-identical `template/` mirror) implementing: backlog parser for `## US-xxxx` / `### BUG-xxxx` blocks; canonical `user_visible: true|false` field read; DONE-only filter; heuristic H1–H8 when `README_FEATURE_COVERAGE_ENFORCE=0`; fail-closed `README_FEATURE_COVERAGE_INPUT_INVALID` on ambiguous H7 stories or malformed values; heuristic disabled when enforce=1.
- **files_affected**:
  - `scripts/readme_feature_coverage_lib.py` (new)
  - `template/scripts/readme_feature_coverage_lib.py` (new — byte-identical)
- **parity_touchpoints**: DEC-0074 §9 row 1 (positive parity).
- **acceptance_check**:
  - Module importable; stdlib-only imports.
  - Predicate matrix unit tests (via `--self-test` in T-005) cover: explicit `true`, explicit `false`, H1 slash-command, H5 out, H6 operator-wins, H7 ambiguous story, H8 bug default-out.
  - Active / template SHA-256 equal.
- **status**: done

---

## T-002 — Audit report (`--audit-out` / `--report` gaps) — AC-2

- **ac_ref**: AC-2
- **dec_ref**: DEC-0074 §5 (`--audit-out`, `--report` gap artifact)
- **description**: Wire audit mode producing deterministic gap report: every in-scope DONE item mapped to expected `root_h2` + `dev_h2` from affinity resolver; gaps explicit. Emit `docs/engineering/context/readme-feature-coverage-audit.json` (active-only snapshot) via `--audit-out`; `--report` lists sorted `gaps` with id, kind, predicate_source, anchor H2s.
- **files_affected**:
  - `scripts/validate_readme_feature_coverage.py` (audit flags — depends T-005 shell or co-developed)
  - `docs/engineering/context/readme-feature-coverage-audit.json` (generated artifact)
- **parity_touchpoints**: Active-only (audit artifact per DEC-0040).
- **acceptance_check**:
  - `--audit-out` writes JSON with every in-scope DONE item and gap status.
  - Gap entries include `root_h2`, `dev_h2`, `id`, `kind`, `predicate_source`.
  - Re-running audit on unchanged tree yields byte-identical artifact (LF, sorted keys).
- **status**: done

---

## T-003 — Three-file README backfill + `user_visible:` markers — AC-3

- **ac_ref**: AC-3
- **dec_ref**: DEC-0074 §3 (three-file coverage target)
- **description**: One-time backfill: root `README.md` operator blurbs (1–2 sentences under existing `USER_*` H2s); `docs/developer/README.md` DEV traceability rows (id + US/DEC + scratchpad flags); `template/README.md` byte-identical to root per **US-0017**. Author explicit `user_visible:` on every DONE item touched during backfill pass in `docs/product/backlog.md`.
- **files_affected**:
  - `README.md`
  - `template/README.md` (byte-identical to root)
  - `docs/developer/README.md`
  - `docs/product/backlog.md` (`user_visible:` markers on touched blocks only)
- **parity_touchpoints**: Root ↔ template README byte parity (US-0017); DEV shard active-only.
- **acceptance_check**:
  - Every gap from T-002 audit has corresponding blurb (root) + DEV row (shard).
  - `diff README.md template/README.md` is empty.
  - Each backfilled item has `user_visible: true` or `false` explicitly set in backlog.
  - No new H2 literals introduced.
- **status**: done

---

## T-004 — Section-affinity manifest + audience boundary enforcement — AC-4

- **ac_ref**: AC-4
- **dec_ref**: DEC-0074 §4 (affinity manifest), §3 + §6 (`README_FEATURE_COVERAGE_PROFILE_VIOLATION`)
- **description**: Ship `docs/engineering/context/readme-section-affinity.json` (+ `template/` mirror) per DEC-0074 §4 locked schema. Integrate affinity resolver in lib (tag → `root_h2` + `dev_h2`). Post-backfill profile budget check via `doc_profile_lib` composition; violations emit `README_FEATURE_COVERAGE_PROFILE_VIOLATION`.
- **files_affected**:
  - `docs/engineering/context/readme-section-affinity.json` (new)
  - `template/docs/engineering/context/readme-section-affinity.json` (byte-identical)
  - `scripts/readme_feature_coverage_lib.py` (affinity resolver — extends T-001)
- **parity_touchpoints**: DEC-0074 §9 row 3 (positive parity).
- **acceptance_check**:
  - Manifest `affinity_version=1` with five locked rules per DEC-0074.
  - Active / template manifest SHA-256 equal.
  - Backfill respects existing `USER_*` / `DEV_*` H2 vocabulary (no renames).
  - `validate_doc_profile.py` budgets pass on post-backfill README family OR validator emits `README_FEATURE_COVERAGE_PROFILE_VIOLATION` with remediation.
- **status**: done

---

## T-005 — Validator CLI + reason codes + `--self-test` — AC-5

- **ac_ref**: AC-5
- **dec_ref**: DEC-0074 §5 (CLI + lib split), §6 (reason-code vocabulary)
- **description**: Create `scripts/validate_readme_feature_coverage.py` (+ `template/` mirror) — stdlib-only entrypoint importing `readme_feature_coverage_lib`. Flags: `--repo`, `--backlog`, `--self-test`, `--report`, `--audit-out`, `--enforce`, `--no-template-parity`. Exit codes: 0 pass, 1 `README_FEATURE_COVERAGE_BLOCKED` (+ sub-codes on stderr), 2 invocation/self-test failure. `--self-test` → `[README_FEATURE_COVERAGE_SELF_TEST_OK]`.
- **files_affected**:
  - `scripts/validate_readme_feature_coverage.py` (new)
  - `template/scripts/validate_readme_feature_coverage.py` (byte-identical)
- **parity_touchpoints**: DEC-0074 §9 row 2 (positive parity).
- **acceptance_check**:
  - `--help` documents all flags.
  - `--self-test` exits 0 with `[README_FEATURE_COVERAGE_SELF_TEST_OK]` token.
  - Sub-codes present: `README_FEATURE_COVERAGE_GAP:<id>`, `README_FEATURE_COVERAGE_PARITY_FAIL`, `README_FEATURE_COVERAGE_INPUT_INVALID`, `README_FEATURE_COVERAGE_PROFILE_VIOLATION`.
  - Umbrella `README_FEATURE_COVERAGE_BLOCKED` on stderr first line when blocking.
  - Active / template SHA-256 equal.
- **status**: done

---

## T-006 — Release step 3f + runbook subsection — AC-6

- **ac_ref**: AC-6
- **dec_ref**: DEC-0074 §7 (release-gate composition with US-0030)
- **description**: Add step **3f** to `.cursor/commands/release.md` (+ `template/` full-file parity) after **3e**, before step **4** UAT: read `README_FEATURE_COVERAGE_ENFORCE` (default 0); when 0 skip with `skipped` evidence; when 1 run `python scripts/validate_readme_feature_coverage.py --repo . --enforce`. Append runbook subsection documenting delta (US-0030) vs static (US-0091) remediation table (+ `template/` mirror).
- **files_affected**:
  - `.cursor/commands/release.md`
  - `template/.cursor/commands/release.md`
  - `docs/engineering/runbook.md`
  - `template/docs/engineering/runbook.md`
- **parity_touchpoints**: DEC-0074 §9 rows 4–5 (positive parity).
- **acceptance_check**:
  - Step 3f block byte-identical active vs template `release.md`.
  - Runbook subsection names both gates and remediation paths.
  - US-0030 delta checklist text unchanged (addition only).
  - `release-findings.md` § doc gates documents both checks.
- **status**: done

---

## T-007 — Idempotent `--report` + harness §27U — AC-7

- **ac_ref**: AC-7
- **dec_ref**: DEC-0074 §5 (stable `--report` JSON schema)
- **description**: Implement stable `--report` JSON (`coverage_total`, `coverage_present`, `coverage_missing`, sorted `gaps`, `report_schema_version=1`, no timestamps in body). Add `tests/fixtures/readme_feature_coverage/` (minimal trees) and harness section **§27U** in `tests/run-tests.ps1` + `tests/run-tests.sh` wiring self-test + double-run idempotence assertion.
- **files_affected**:
  - `scripts/validate_readme_feature_coverage.py` (report emitter — extends T-005)
  - `tests/fixtures/readme_feature_coverage/**` (new)
  - `tests/run-tests.ps1` (§27U)
  - `tests/run-tests.sh` (§27U)
- **parity_touchpoints**: Active-only (fixtures + harness).
- **acceptance_check**:
  - Two consecutive `--report` runs on same tree: identical stdout JSON and exit code.
  - JSON keys sorted; UTF-8 LF; counts match gap list cardinality.
  - Harness §27U green in both PS1 and SH runners.
- **status**: done

---

## T-008 — US-0071 metadata hygiene on backfilled paths — AC-8

- **ac_ref**: AC-8
- **dec_ref**: DEC-0074 §3 (root blurb preference — command/flag tokens over internal ids)
- **description**: Verify backfilled operator blurbs contain no internal planning tokens (sprint ids, phase names, orchestrator tokens, etc.). Run `python scripts/check-user-visible-metadata.py` on changed README family paths; fix any violations in T-003 content. Prefer slash-command / scratchpad-key tokens in root blurbs per US-0071.
- **files_affected**:
  - `README.md`, `template/README.md`, `docs/developer/README.md` (content review/fix only if scanner fails)
- **parity_touchpoints**: Root ↔ template unchanged after fixes.
- **acceptance_check**:
  - `check-user-visible-metadata.py` exits 0 on all three changed surfaces.
  - Root blurbs avoid bare `US-xxxx` where a command/flag token exists (preference, not hard fail if id required in DEV shard).
  - No regression in existing US-0071 contract tests.
- **status**: done

---

## T-009 — Template parity + installer manifest — AC-9

- **ac_ref**: AC-9
- **dec_ref**: DEC-0074 §9 (parity inventory + `--scope=readme-feature-coverage`)
- **description**: Extend `scripts/check_intake_template_parity.py` with `--scope=readme-feature-coverage` asserting byte equality across §9 inventory (scripts, affinity manifest, release.md 3f block, runbook subsection, installer manifest, self row). Add installer-owned-paths manifest entries for both new scripts. Compose with US-0017 README guard — do not duplicate parity logic inside validator.
- **files_affected**:
  - `scripts/check_intake_template_parity.py` (+ `template/` mirror)
  - `docs/engineering/context/installer-owned-paths.manifest` (+ `template/` mirror)
- **parity_touchpoints**: DEC-0074 §9 rows 6–7 (positive parity).
- **acceptance_check**:
  - `python scripts/check_intake_template_parity.py --scope=readme-feature-coverage` exits 0.
  - Manifest lists both `validate_readme_feature_coverage.py` and `readme_feature_coverage_lib.py`.
  - Mutating any §9 active vs template pair causes non-zero exit with clear drift reason.
  - Existing `US-0017` template-drift guard remains green.
- **status**: pending

---

## T-010 — Grandfathering toggle + activation + DEC linkage assert — AC-10

- **ac_ref**: AC-10
- **dec_ref**: DEC-0074 §8 (grandfathering / first-activation), §AC-Traceability
- **description**: Add scratchpad key `README_FEATURE_COVERAGE_ENFORCE=0|1` (default **0**) to active `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` (+ template example parity). Document activation procedure in runbook (if not fully covered in T-006): complete backfill → explicit markers → verify `--report` `coverage_missing: []` → flip 0→1 same commit. Add assert-only linkage subtest verifying `DEC-0074`, `# US-0091`, US-0030, DEC-0059, US-0017, US-0071 references in architecture/decisions surfaces.
- **files_affected**:
  - `.cursor/scratchpad.md`
  - `.cursor/scratchpad.local.example.md`
  - `template/.cursor/scratchpad.local.example.md`
  - `docs/engineering/runbook.md` (activation note if needed)
  - `tests/` (assert-only linkage subtest — dev picks file per precedent)
- **parity_touchpoints**: Scratchpad example surfaces active + template; `decisions/DEC-0074.md` already authored (read-only assert).
- **acceptance_check**:
  - `README_FEATURE_COVERAGE_ENFORCE=0` in merged scratchpad at sprint start; flip to `1` only after T-003 backfill + T-007 idempotence pass.
  - `decisions/DEC-0074.md` documents predicate, composition with DEC-0030 + DEC-0059, grandfathering (no rewrite required — assert-only).
  - Linkage subtest green for required cross-refs.
  - No retroactive `/release` block when enforce=0 (release step 3f skips).
- **status**: done

---

## Recommended /execute ordering

1. **T-001** — lib foundation (predicate + parser)
2. **T-004** — affinity manifest (unblocks audit/backfill routing)
3. **T-005** — CLI shell + self-test
4. **T-002** — audit mode (depends T-001, T-004, T-005)
5. **T-003** — backfill (depends T-002 gap report)
6. **T-008** — metadata hygiene (depends T-003 content)
7. **T-006** — release wiring + runbook
8. **T-009** — parity script + manifest
9. **T-007** — fixtures + harness §27U
10. **T-010** — enforce flip + linkage assert (last — after coverage green)
