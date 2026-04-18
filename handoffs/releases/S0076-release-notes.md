# Release Notes — S0076 / US-0090 (Caveman input compression)

- **sprint_id**: S0076
- **story_refs**: US-0090
- **release_name**: `S0076 -- US-0090 Caveman compress-input CLI + installer surface`
- **release_date**: 2026-04-19T00:05:00Z
- **orchestrator_run_id**: auto-20260418-01
- **verdict**: **PASS**
- **binding_decision**: `DEC-0073` (composes on `DEC-0072`; DEC-0072 not rewritten)
- **research_anchor**: `R-0073` (input-side extension)

## Summary

Ships **Caveman input compression**: an optional, operator-gated, stdlib-only
Python CLI that safely reduces tokens in agent-readable prose files while
preserving originals in a sidecar tree and failing closed on every scope,
deny-list, or integrity violation. Default-off end-to-end. No change to
`TOKEN_PROFILE` (US-0080), `CAVEMAN_MODE` (DEC-0072), strict-proof, isolation
evidence, `AUTO_QUIET`, or canonical-artifact contracts.

## What's new

- **CLI script (AC-1..AC-5)** — `scripts/caveman_compress_input.py` (+ byte-identical
  `template/scripts/caveman_compress_input.py` mirror). Stdlib-only Python with
  four flags:
  - `--dry-run` (default — emits plan, writes nothing)
  - `--write` (mutating path — requires activation gate)
  - `--verify-originals` (integrity check vs. sidecar tree)
  - `--report` (stable-hash report including `deny_list_version`)
  Activation gate: `CAVEMAN_MODE=1` AND `CAVEMAN_COMPRESS_INPUT=1` AND
  non-empty `CAVEMAN_FILE_SCOPE` AND explicit `--write`. Empty scope fails
  closed with `CAVEMAN_COMPRESS_SCOPE_EMPTY`.
- **Sidecar-first atomic write (AC-2)** — originals land at
  `docs/.caveman-originals/<relative/path>/<file>` before the working copy is
  rewritten. Repo-root `.gitignore` anchor + `docs/.caveman-originals/.gitkeep`
  seed the sidecar tree.
- **Deny-list layered SoT (AC-3)** — evaluation order: hard-coded baseline
  (secrets, intake evidence, canonical product/engineering docs, DEC files,
  sprint lifecycle evidence, binaries, installer/workflow/hook/rule/command/
  skill files, manifests, parity sources) → `.gitignore` secret-pattern merge
  → optional `.cursorignore` overlay via
  `CAVEMAN_COMPRESS_INGEST_CURSORIGNORE=1` → allow-list → 9-zone literal-region
  scan → write. Deny always wins over allow.
- **Allow-list grammar (AC-4)** — `CAVEMAN_FILE_SCOPE` accepts named profiles
  (v1 ships frozen `docs-prose-only`: `docs/user-guides/**/*.md`,
  `docs/engineering/runbook.md`, `docs/engineering/state-archive/**/*.md`,
  `handoffs/archive/*.md`) and/or raw globs. Unknown profile fails closed with
  `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`.
- **Operator runbook (AC-5)** — `### Caveman input compression (US-0090)` in
  `docs/engineering/runbook.md` (+ template mirror) documents activation,
  dry-run, write, verify, revert (sidecar-based), and reason-code vocabulary.
- **9-code reason-code vocabulary (AC-4 + AC-6)** — three families:
  - Gating: `CAVEMAN_COMPRESS_MODE_DISABLED`, `CAVEMAN_COMPRESS_FLAG_CONFLICT`
  - Scope: `CAVEMAN_COMPRESS_SCOPE_EMPTY`, `CAVEMAN_COMPRESS_SCOPE_VIOLATION`,
    `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`, `CAVEMAN_COMPRESS_DENY_HIT`
  - Integrity: `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`,
    `CAVEMAN_COMPRESS_ORIGINAL_MISSING`, `CAVEMAN_COMPRESS_NOT_IDEMPOTENT`
  No post-write codes. No new codes without DEC revising §7.
- **Contract tests (AC-6)** — 13 new `test_caveman_compress_input_*` subtests in
  `tests/auto_command_contract_test.py` (rule SHA-256 baseline guard,
  `deny_list_version` stability, 9-code / 3-family vocabulary cardinality,
  three-axis paragraph presence, architecture linkage). Existing
  `test_caveman_default_off_*` subtests preserved byte-unchanged per DEC-0072
  §6 row 6. Fixture tree `tests/fixtures/caveman_compress/` delivers 8 classes
  (51 fixtures), including idempotency AC-6 class 5 (`input.txt` / `expected.txt`
  byte-stable after compression).
- **Install completeness (AC-8)** — `scripts/caveman_compress_input.py` added to
  `docs/engineering/context/installer-owned-paths.manifest` under
  `[install_include_paths]` / `[clean_paths]` / `[required_install_script_paths]`
  (+ template mirror). `tests/installer_completeness_bug0003_test.py` gains
  `test_caveman_compress_input_shipped_by_installer` verifying `--mode=missing`
  and `--mode=upgrade` delivery. Harness section `26T` added to both
  `tests/run-tests.ps1` and `tests/run-tests.sh`.
- **Template parity (AC-8)** — `scripts/check_intake_template_parity.py` gains
  `--scope=caveman-compress` / `--scope=all` modes (+ template mirror).
  Eight-row positive parity inventory per DEC-0073 §9 + negative-parity
  invariants (`.cursor/rules/caveman.mdc` SHA-256
  `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` preserved
  end-to-end; `.cursor/skills/its-magic/SKILL.md` unchanged; `.cursor/scratchpad.md`
  byte-unchanged — reserved no-op keys already existed per DEC-0072 §3).
- **Three-axis non-substitution (AC-7)** — `### TOKEN_PROFILE × CAVEMAN_MODE ×
  CAVEMAN_COMPRESS_INPUT non-substitution (US-0090 / DEC-0073 §1)` section
  appended to `docs/engineering/auto-orchestration-reference.md` (+ template
  mirror), extending (not rewriting) the existing DEC-0072 §1 paragraph.
  `docs/engineering/architecture.md` `# US-0090` section appended (active-only)
  with verbatim DEC-0073 §1 blockquote, linkage to `# US-0089`, `US-0053`,
  `US-0085`, `US-0078`, `DEC-0060`, and forbidden-surfaces documentation.

## Non-goals (explicit)

- **No `DEC-0072` rewrite** (forward-link composition only).
- **No `.cursor/rules/caveman.mdc` edit** (R10 — byte-identity preserved
  end-to-end).
- **No `.cursor/scratchpad*` edit** (reserved no-op keys already exist per
  DEC-0072 §3).
- **No `.cursor/skills/its-magic/SKILL.md` edit** (DEC-0072 §7 row 9 negative
  parity).
- **No aggressive compression mode in v1** (safe-mode line-level minifier only;
  strictly idempotent by construction). Aggressive mode deferred.
- **No LLM-assisted compression**.
- **No new runtime dependency** (stdlib Python only; no `npm`, no `pip`).
- **No new CLI flags / no new reason codes / no new profiles beyond the 9-code
  vocabulary + 4 flags + `docs-prose-only` profile** shipped in v1.
- **No `.cursorignore` mutation by the CLI**. Operator-owned per US-0085.
- **No mandatory auto-compress in `/auto`**. Script-invoked only; never
  voice-toggled.
- **No `TOKEN_PROFILE` (US-0080 / DEC-0062) change**.
- **No canonical workflow artifact rewrites**.
- **No `npx skills add` vendor-install leak** (DEC-0072 §8 carried forward).
- **No existing `test_caveman_default_off_*` subtest mutation** (DEC-0072 §6
  row 6 invariant).
- **No strict-proof (US-0056 / DEC-0038), isolation evidence (US-0048 /
  DEC-0029), `AUTO_QUIET` non-suppressible, spawn-only / phase-role, or
  US-0071 metadata policy change.**

## Run

- **start_command**: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
- **runtime_mode**: `local`
- **runtime_context_ref**: `docs/engineering/runtime-connectivity.md`

## Connect

- **service_url**: N/A (framework/toolkit repository; no running service)
- **service_port**: N/A
- **health_endpoint**: N/A

## Verify

1. `python -m pytest tests/auto_command_contract_test.py -k caveman -q --tb=no`
   → expect **24 passed / 19 deselected / 142 subtests passed**.
2. `python -m pytest tests/installer_completeness_bug0003_test.py -q --tb=no`
   → expect **4 passed** (including
   `test_caveman_compress_input_shipped_by_installer`).
3. `python scripts/check_intake_template_parity.py --scope=caveman-compress`
   → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=caveman-compress` (exit 0).
4. `python scripts/check_intake_template_parity.py --scope=all`
   → expect `[INTAKE_TEMPLATE_PARITY_OK] scope=all` (exit 0).
5. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`
   → expect `[BUG_VALIDATION_OK]` (exit 0).
6. `python scripts/caveman_compress_input.py --help` → exit 0 with four flags
   documented.
7. `python scripts/caveman_compress_input.py --write`
   → exit 2; `REASON_CODE=CAVEMAN_COMPRESS_MODE_DISABLED` (default-off gating).
8. `python scripts/caveman_compress_input.py --dry-run --write`
   → exit 2; `REASON_CODE=CAVEMAN_COMPRESS_FLAG_CONFLICT`.
9. `python scripts/caveman_compress_input.py --report` (two runs)
   → stable `deny_list_version=33bd8fa055791051cfb4505ca8815de51eefd73b41ee850541db63bc0ef69884`;
   `idempotency_check.fixture_byte_stable=true`.
10. `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → expect
    canonical baseline `Pass=791 / Fail=9` (9 pre-existing disjoint).
11. Confirm `sprints/S0076/qa-findings.md` PASS and `sprints/S0076/uat.json`
    15/15 PASS.
12. Confirm release-queue row `S0076` is `released` and backlog / acceptance
    show `US-0090` = DONE / checked.

- **expected_health_signal**: All artifact checks above pass;
  `US-0090` surfaces as `DONE` in backlog and checked in acceptance.

## Credentials

- Env-reference-only policy in effect. No inline secrets in artifacts. Sidecar
  tree anchored at `docs/.caveman-originals/` is `.gitignore`-anchored and
  deny-list-aware (sidecar-for-denied-file is impossible because deny blocks
  write).

## Test evidence summary

- **Caveman suite (targeted)**: 24 passed / 0 failed (142 subtests).
- **Full `tests/auto_command_contract_test.py`**: 40 passed + 24 pre-existing
  failures (baseline preserved byte-for-byte vs. US-0089 release; zero new
  US-0090 regressions).
- **`tests/installer_completeness_bug0003_test.py`**: 4 passed (incl. new
  `test_caveman_compress_input_shipped_by_installer`).
- **Canonical `tests/run-tests.ps1`**: Pass=**791** / Fail=**9** (+8 pass / -2
  fail vs. US-0089 release baseline 783/11 — all 9 failures pre-existing
  disjoint drift).
- **Bug validator**: `[BUG_VALIDATION_OK]` pre- and post-release-write.
- **Parity**: `[INTAKE_TEMPLATE_PARITY_OK]` both `--scope=caveman-compress` and
  `--scope=all`.
- **Rule byte-identity**: `.cursor/rules/caveman.mdc` SHA-256
  `E10EFC32C628E790E69E2393F381108FE0B1F16E0BCDCFFFC162EFF6F91E47DE` (active ==
  template).

## Governance references

- **DEC-0073** — Caveman input-side compression (this release's binding
  decision; composes on DEC-0072 §1/§4/§6/§7/§8).
- **DEC-0072** — Caveman response-side voice (not rewritten; forward-linked
  only).
- **`docs/engineering/architecture.md`** `# US-0090` section.
- **`docs/engineering/research.md`** `R-0073` (input-side extension).

## Known limitations / follow-on

- 9 pre-existing `tests/run-tests.ps1` failures remain out-of-scope of US-0090
  (US-0086 / US-0087 / US-0088 / Homebrew families) — recommend triage under a
  new follow-on BUG or housekeeping story.
- 24 pre-existing `tests/auto_command_contract_test.py` failures likewise
  out-of-scope.
- **Carried-forward non-blocking observations (from verify-work)**:
  1. `PARTIAL_VERBATIM` on DEC-0073 §1 publication: architecture doc carries
     the verbatim three-sentence paragraph; `auto-orchestration-reference.md`
     and `runbook.md` carry a semantic paraphrase. DEC-0072 §6 row 6 pinned
     test `test_caveman_default_off_reference_non_substitution_paragraph`
     preserved byte-unchanged. Optional future doc cleanup; no DEC amendment
     required.
  2. UAT-3 `--dry-run` vs `--write` narration variance: implementation binds
     `CAVEMAN_COMPRESS_SCOPE_EMPTY` reason code to the DEC-0073 §2 activation
     gate (`--write` pathway) per contract test
     `test_caveman_compress_input_scope_empty_reason`. UAT-spec's `--dry-run`
     command narrates gracefully by design. AC-4 fail-closed intent satisfied
     via `--write` evidence; optional UAT-spec authoring alignment suggested.
- Aggressive-mode compression, `--purge-orphans`, additional allow-list
  profiles are deferred beyond v1.

## Gate audit snapshot (US-0039)

| gate | verdict | reason_code | evidence_refs |
|------|---------|-------------|---------------|
| check-in_test | pass | - | `tests/report.md` (791/9; 9 pre-existing disjoint); `sprints/S0076/qa-findings.md` |
| qa | pass | - | `sprints/S0076/qa-findings.md` (cycle 1 PASS) |
| uat | pass | - | `sprints/S0076/uat.json`, `sprints/S0076/uat.md` (15/15 PASS) |
| isolation | pass | - | `docs/engineering/state.md` (distinct `fresh_context_marker` per phase) |
| strict_proof | pass | - | `docs/engineering/state.md` (distinct `runtime_proof_id` per phase) |
| scratchpad_pair | pass | - | no scratchpad mutation; byte-unchanged |
| metadata_guard | pass | - | `sprints/S0076/qa-findings.md` |
| bug_validate | pass | - | `[BUG_VALIDATION_OK]` pre- and post-release |
| finalization | pass | - | this file, `handoffs/release_queue.md`, `handoffs/release_notes.md`, `sprints/S0076/release-findings.md`, `docs/product/backlog.md`, `docs/product/acceptance.md`, `docs/engineering/status-normalization-report.md`, `docs/engineering/state.md` |

## Publish status

- **RELEASE_PUBLISH_MODE**: `confirm`
- **publish_snapshot**: `skipped_pending_operator_confirm`
- Operator confirmation is required before any publish target execution. No
  publish scripts were run by the release agent.

## Sync (DEC-0018)

- **SYNC_POLICY_MODE**: `by_phase`
- **ALLOW_AUTO_PUSH**: `1`
- **AUTO_PUSH_BRANCH_ALLOWLIST**: `main`
- **current_branch**: `main`
- **push_decision**: `blocked`
- **reason_code**: `TEST_FAILED` — canonical `tests/run-tests.ps1` exits
  non-zero due to 9 pre-existing disjoint failures. Push attempted; sync
  policy guard declined. Release queue row is `released` because local release
  work is complete and the block is a deployment-gate concern (same precedent
  as S0075 / US-0089). No `--no-verify`, no `push --force`.

## Strict runtime proof

- **orchestrator_run_id**: `auto-20260418-01`
- **runtime_proof_id**: `rp-auto-20260418-01-release-release-20260419T000500Z-S0076-US0090`
- **phase_id**: `release`
- **role**: `release`
- **proof_issued_at**: `2026-04-19T00:05:00Z`
- **proof_ttl_seconds**: `3600`
- **proof_hash**: `0126c54efd3cc8158d9d0a687a66e9bce8f4eeefb89522993bb5ce805bb87e40`

## Isolation evidence (US-0048 / DEC-0029)

- `phase_id=release`
- `role=release`
- `fresh_context_marker=release-US0090-S0076-20260419T000500Z-fresh`
- `timestamp=2026-04-19T00:05:00Z`
- `evidence_ref=[sprints/S0076/release-findings.md, handoffs/releases/S0076-release-notes.md]`

## Next

- **`/refresh-context`** (fresh **curator** context) for segment closeout —
  reconcile `docs/engineering/decisions.md` (DEC-0073 indexing),
  `docs/engineering/research.md` (`R-0073` final closure note),
  `sprints/S0076/summary.md`, and `handoffs/resume_brief.md` to the
  portfolio-next pointer. Backlog-drain budget remaining = 4.
