# Runbook

## Commands

TEST_COMMAND: npm run test
LINT_COMMAND:
TYPECHECK_COMMAND:
DEPLOY_STAGING_COMMAND: echo "No staging deploy target configured for this repository"
DEPLOY_PROD_COMMAND: echo "No production deploy target configured for this repository"

LINT_FIX_COMMAND:
FORMAT_COMMAND:
CI_AUTO_FIX: false
TEST_TIMEOUT_SECONDS: 120

## Notes
- Leave a command blank to skip that step.
- Use explicit commands, not placeholders.
- `TEST_TIMEOUT_SECONDS` limits how long any subprocess can run during tests.
  Prevents hangs from prompts, network waits, or infinite loops.
- `LINT_FIX_COMMAND` / `FORMAT_COMMAND` are used by CI auto-fix when checks fail
  (e.g. `npx eslint --fix .` or `npx prettier --write .`).
- `CI_AUTO_FIX`: set to `true` to enable the automatic fix-and-retry loop in
  GitHub Actions. When `false` (default), CI reports failures but does not
  attempt auto-fix commits.

## Intentional empty commands (US-0015)

For this template/installer repository, the following command keys may be
intentionally empty in the shipped template; they are not configuration errors:

- `TEST_COMMAND` (blank until installer bootstrap per stack; **DEC-0056**)
- `LINT_COMMAND`
- `FORMAT_COMMAND`
- `TYPECHECK_COMMAND`

Teams may set these keys when needed for their own project stack.

## OS-aware runbook command bootstrap (US-0063 / DEC-0046)

Installer/upgrade flows auto-bootstrap runbook command keys with deterministic
precedence:

- `user override > detected defaults > safe fail-fast`
- user-provided non-empty values are never overwritten
- defaults are inferred from OS + project stack markers
  (`package.json` scripts, `pyproject.toml`, `go.mod`, platform test scripts)

Baseline detection contract:

- `TEST_COMMAND` is mandatory for push-eligible quality gates.
- `LINT_COMMAND` and `TYPECHECK_COMMAND` are optional and only auto-populated
  when confidently detectable.
- if `TEST_COMMAND` remains unresolved/invalid, installer fails fast with:
  - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED`, or
  - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:<reason>`

Remediation:

- define `TEST_COMMAND` explicitly in `docs/engineering/runbook.md`, or
- add detectable stack markers/scripts then rerun installer upgrade.

## Codebase map bootstrap (US-0082 / DEC-0065)

**Goal:** `docs/engineering/codebase-map.md` exists in fresh repos without ad-hoc
operator memory, while **`/map-codebase`** stays the explicit manual analysis
command.

### Responsibility

| Path | Owner | Mechanism |
|------|-------|-----------|
| Primary | **`/architecture`** (tech-lead) | Before **`/sprint-plan`**, run `python scripts/materialize_codebase_map.py --trigger architecture` from repo root |
| Optional refresh | **`/refresh-context`** (curator) | Same script with `--trigger refresh-context` only when scratchpad sets **`CODEBASE_MAP_REFRESH_ON_ROLLOVER=1`** (default off) |
| Manual / deep pass | Operator | **`/map-codebase`** |

### Write surfaces

Same as **`/map-codebase`**: `docs/engineering/codebase-map.md`,
`docs/engineering/dependencies.json`. The materializer does **not** append
`docs/engineering/state.md`. Non-bootstrap maps (no bootstrap sentinel in the
file) are never replaced silently.

### Deterministic diagnostics

- **`CODEBASE_MAP_MISSING`** — use when a lifecycle checkpoint requires the map
  but it is absent and generation did not run (e.g. custom **`/auto`** profile
  skipped **`architecture`**).
- **`CODEBASE_MAP_BLOCKED:<subreason>`** — materializer or policy blocked
  creation (`policy_skip`, permissions, etc.); stdout includes remediation
  pointing here and to **`/map-codebase`**.

**Command:** `python scripts/materialize_codebase_map.py --repo .`  
**Tests:** `python tests/codebase_map_materialize_test.py`

Normative architecture: `docs/engineering/architecture.md` (**# US-0082**).

## Documentation profile validation (US-0077 / DEC-0059)

**Goal:** keep root `README.md` (user channel) and `docs/developer/README.md`
(developer shard) aligned with merged scratchpad keys `DOC_AUDIENCE_PROFILE` and
`DOC_DETAIL_LEVEL`, with deterministic reason codes and active/`template/` parity.

### Scratchpad keys

- `DOC_AUDIENCE_PROFILE`: `user` \| `developer` \| `both` (empty defaults to `both` during transition).
- `DOC_DETAIL_LEVEL`: `concise` \| `balanced` \| `technical-deep` (empty defaults to `balanced`).
- Invalid values → `DOC_PROFILE_INVALID`. Merge/read failures → `DOC_PROFILE_MERGE_ERROR`.
- Optional modes `SPEC_PACK_MODE` / `USER_GUIDE_MODE` stay additive only: when `0`, this
  validator does not require spec-pack or user-guide files.

### Command

```bash
python scripts/validate_doc_profile.py --repo .
python scripts/validate_doc_profile.py --repo . --no-template-parity   # fixture trees without template/
```

### Installer hook

`installer.py` scratchpad post-install refreshes missing normative `##` sections
(non-destructive append) from the resolved profile, then operators should keep
content accurate. Re-run `python installer.py --scratchpad-postinstall --target <repo> --mode missing`
after template upgrades if needed.

Normative H2 titles and matrix: `docs/engineering/architecture.md` (`# US-0077`).

## README feature coverage validation (US-0091 / DEC-0074)

**Goal:** ensure every DONE user-visible backlog item (`US-xxxx` / `BUG-xxxx` with
`user_visible: true`) has operator blurbs in **`its_magic/README.md`** (framework catalog)
and traceability rows in `docs/developer/README.md`, without inventing new `USER_*` / `DEV_*`
H2 literals (**DEC-0059** composes; **US-0030** delta gate unchanged). Consumer root
`README.md` is **out of scope** for this gate — see **US-0097** / **DEC-0083**.

### Delta vs static doc gates

| Gate | Question | Remediation |
|------|----------|-------------|
| **US-0030** (delta) | Did this sprint change commands/flags without README/runbook updates? | Update command docs for changed surfaces; agent checklist in `/release` step 3 family. |
| **US-0091** (static) | Is every DONE user-visible item documented in the framework README family? | Backfill **`its_magic/README.md`** + DEV shard; set `user_visible:` marker; run validator `--report`. |

### Scratchpad key

- `README_FEATURE_COVERAGE_ENFORCE`: `0` \| `1` (default `0` until backfill completes).
- When `0`: `/release` step **3f** records `skipped` evidence; migration heuristic H1–H8
  may classify unset `user_visible` during backfill.
- When `1`: explicit `user_visible:` required on all DONE items; heuristic disabled;
  `/release` runs blocking validator.

**Activation (same commit as backfill):** complete audit + three-file backfill → explicit
`user_visible:` markers → verify `--report` shows `coverage_missing: []` → flip `0` → `1`.

### Commands

```bash
python scripts/validate_readme_feature_coverage.py --self-test
python scripts/validate_readme_feature_coverage.py --repo . --report
python scripts/validate_readme_feature_coverage.py --repo . --audit-out docs/engineering/context/readme-feature-coverage-audit.json
python scripts/validate_readme_feature_coverage.py --repo . --enforce
python scripts/check_intake_template_parity.py --scope=readme-feature-coverage
```

Reason codes: `README_FEATURE_COVERAGE_BLOCKED`, `README_FEATURE_COVERAGE_GAP:<id>`,
`README_FEATURE_COVERAGE_PARITY_FAIL`, `README_FEATURE_COVERAGE_INPUT_INVALID`,
`README_FEATURE_COVERAGE_PROFILE_VIOLATION`.

Normative predicate + affinity manifest: `decisions/DEC-0074.md`,
`docs/engineering/context/readme-section-affinity.json`.

## Project README coverage validation (US-0097 / DEC-0083)

**Goal:** ensure project-owned root `README.md` has a bootstrap scaffold and growing
feature catalog under `<!-- project-readme-feature-catalog -->` for every DONE
`user_visible: true` backlog item. Framework catalog remains in **`its_magic/README.md`**
(**US-0091** gate **3f** — independent from project gate **3g**).

### Placeholder sentinels S1–S5

| Signal | Detection rule | Verdict |
|--------|----------------|---------|
| **S1** | H1 `# its-magic — AI dev team` | placeholder |
| **S2** | `<!-- readme-feature-coverage-catalog -->` | placeholder |
| **S3** | Heading `Feature coverage catalog (US-0091)` | placeholder |
| **S4** | Byte-identical to `template/README.md` | placeholder |
| **S5** | None of S1–S4 + custom title/purpose | **operator-authored** — preserve |

**Detection order**: `FRAMEWORK_KIT_REPO=1` → S1–S4 → S5. Hybrid roots fail closed with
`PROJECT_README_MIGRATION_AMBIGUOUS` or `PROJECT_README_SENTINEL_CONFLICT`.

### Migration algorithm M1–M5

| Step | Condition | Action |
|------|-----------|--------|
| **M1** | `FRAMEWORK_KIT_REPO=1` | Skip consumer migration |
| **M2** | Root **S5** | Preserve root; copy to **`its_magic/README.md`** if missing |
| **M3** | Root **S1–S4**, **`its_magic/`** missing | Lift root → **`its_magic/README.md`** |
| **M4** | Root **S1–S4** after **M3** | Replace root with project scaffold |
| **M5** | Hybrid / ambiguous | Fail closed |

### Scratchpad keys

- `PROJECT_README_ENFORCE`: `0` \| `1` (default `1` post-bootstrap).
- `FRAMEWORK_KIT_REPO`: `0` \| `1` (default `0`; consumer repos never `1`).

**Grandfathering:** set `PROJECT_README_ENFORCE=0` during migration; flip to `1` when
`validate_project_readme_coverage.py --report` shows `coverage_missing: []`.

### Commands

```bash
python scripts/validate_project_readme_coverage.py --self-test
python scripts/validate_project_readme_coverage.py --repo . --report
python scripts/validate_project_readme_coverage.py --repo . --audit-out docs/engineering/context/project-readme-coverage-audit.json
python scripts/validate_project_readme_coverage.py --repo . --enforce
python scripts/check_intake_template_parity.py --scope=project-readme
```

Reason codes: `PROJECT_README_COVERAGE_BLOCKED`, `PROJECT_README_COVERAGE_GAP:<id>`,
`PROJECT_README_DELTA_SKIPPED`, `PROJECT_README_BOOTSTRAP_SKIPPED`,
`PROJECT_README_MIGRATION_AMBIGUOUS`, `PROJECT_README_SENTINEL_CONFLICT`,
`PROJECT_README_PLACEHOLDER_UNRESOLVED`, `PROJECT_README_ENFORCE_SKIPPED`,
`PROJECT_README_INPUT_INVALID`.

### Operator recipes (US-0097)

| Scenario | Operator action |
|----------|-----------------|
| Fresh consumer repo | First **`/execute`** bootstraps project README; framework catalog in **`its_magic/`** |
| Legacy framework root README | Run **`upgrade`** — migration **M3**/**M4** lifts to **`its_magic/`** + project scaffold |
| Operator-authored root (S5) | Migration preserves root; adds **`its_magic/README.md`** if missing |
| Hybrid / ambiguous root | Fix manually per **`PROJECT_README_MIGRATION_AMBIGUOUS`** — remove mixed sentinel + custom prose |
| Migration window | Set **`PROJECT_README_ENFORCE=0`**; backfill catalog bullets; flip to **`1`** when **`--report`** clean |
| Kit repo dogfooding | Set **`FRAMEWORK_KIT_REPO=1`** — skip consumer bootstrap (**23a**/**23b**) and project validator root check |

**Troubleshooting:** `PROJECT_README_COVERAGE_BLOCKED` at release **3g** → run `--report`,
backfill missing `US-xxxx` bullets under `<!-- project-readme-feature-catalog -->`.
`PROJECT_README_MIGRATION_AMBIGUOUS` → split framework content to **`its_magic/README.md`**
manually, then re-run migration. Implementation tranche order: A (installer + migration) →
B (bootstrap) → C (execute **23** + release **3g** + scratchpad) → D (validators + tests).

Normative contract: `decisions/DEC-0083.md`, `docs/engineering/architecture.md` `# US-0097`.

## Dev environment auto-launch (US-0098 / DEC-0084)

**Goal:** execute-phase bounded rebuild/restart of dev stacks plus **Connect** surfacing after
implementation changes — distinct from **US-0065** phase QA, **US-0086** test routing, and
**US-0067** release hints. Default-off scratchpad gate; **no** `.env` reads (**US-0085**).

**Install-time bootstrap (US-0099):** on **`missing`**, **`upgrade`**, and **npm `postinstall`**, the
framework copies **`template/.cursor/dev-environment.json.example`** → resolved profile path
(**`.cursor/dev-environment.json`** by default) **only when the target file is absent** — never
overwrites operator-customized profiles. Customize **after** bootstrap (compose **`service`**, **`*Env`**
connect refs); manual copy is no longer a prerequisite to enable the gate.

| Before (US-0098) | After (US-0099) |
|------------------|-----------------|
| "Seed profile" = manual copy prerequisite | Bootstrap automatic on install/upgrade/postinstall |
| **`DEV_ENV_PROFILE_MISSING`** → manual copy first | Troubleshooting references auto-bootstrap + customize-after-bootstrap |

### Operator recipes

| Scenario | Operator action |
|----------|-----------------|
| Enable dev auto-launch | Set **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`** in scratchpad |
| Customize profile after bootstrap | Edit **`.cursor/dev-environment.json`** copied from example; set compose **`service`** + **`*Env`** connect refs |
| Force relaunch | Send exact phrase **`refresh dev environment`** (case-sensitive whole phrase) |
| Profile off / manual mode | Leave **`DEV_AUTO_LAUNCH_PROFILE=off`** (default) — execute step **24** zero overhead |
| Ambiguous stack | Fix compose path or seed profile; remediate **`DEV_ENV_DETECT_AMBIGUOUS`** |
| Remote + local both on | **US-0086** remote wins over **docker-host-local** — see precedence in **`DEC-0084`** §3 |
| Bind-mount hot reload | Default skip on source-only docker changes; use refresh or **`restart_on_source_change=true`** |
| Global npm install (no consumer repo) | **`[DEV_ENV_BOOTSTRAP_SKIP] no consumer repository detected`** — run **`its-magic`** install into target repo |

### Troubleshooting (`DEV_ENV_*` reason codes)

**Bootstrap family (install-time; distinct from runtime profile/relaunch families):**
**`DEV_ENV_BOOTSTRAP_COPIED`**, **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**, **`DEV_ENV_BOOTSTRAP_PATH_INVALID`**,
**`DEV_ENV_BOOTSTRAP_SOURCE_MISSING`**.

**Profile family:** **`DEV_ENV_PROFILE_DISABLED`**, **`DEV_ENV_PROFILE_INVALID`**,
**`DEV_ENV_PROFILE_MISSING`** (if bootstrap skipped or profile deleted — re-run install/upgrade or
**`python scripts/dev_environment_lib.py --bootstrap --target <repo>`** then customize),
**`DEV_ENV_DETECT_AMBIGUOUS`**, **`DEV_ENV_COMPOSE_UNRESOLVED`**, **`DEV_ENV_TARGET_DISABLED`**, **`DEV_ENV_SECRET_SURFACE_VIOLATION`**.

**Relaunch family:** **`DEV_ENV_RELAUNCH_SKIPPED_NO_SURFACE`**, **`DEV_ENV_RELAUNCH_SKIPPED_PROFILE_OFF`**,
**`DEV_ENV_RELAUNCH_FAILED`**, **`DEV_ENV_RELAUNCH_RETRY_EXHAUSTED`**, **`DEV_ENV_RELAUNCH_TIMEOUT`**, **`DEV_ENV_CONNECT_UNAVAILABLE`**.

### Commands

```bash
python scripts/dev_environment_lib.py --self-test
python scripts/dev_environment_lib.py --load .cursor/dev-environment.json
python scripts/dev_environment_lib.py --bootstrap --target .
python scripts/check_intake_template_parity.py --scope=dev-environment
pytest -k us0098 tests/auto_command_contract_test.py
pytest -k us0099 tests/auto_command_contract_test.py
```

Implementation tranche order: **A** (schema + scratchpad) → **B** (stdlib helper) → **C** (execute step **24** + docs) → **D** (contract tests + parity + harness).

Normative contract: `decisions/DEC-0084.md`, `docs/engineering/architecture.md` `# US-0098`, `# US-0099` (bootstrap posture).

## User-visible internal metadata guard (US-0071 / DEC-0053)

**Goal:** keep planning-shaped identifiers out of **operator-visible software
channels** (CLI/installer/validate-and-push strings), while they remain valid in
internal documentation trees and in source comments that are not emitted to
users.

### Forbidden tokens (user-visible channels only)

Match planning-shaped tokens:

- `US-[0-9]{4}`
- `DEC-[0-9]{4}`
- `R-[0-9]{4}`

### Inclusive scan roots (deterministic)

From repository root, the checker walks **only**:

- `bin/**` (`*.js`)
- `installer.py`, `installer.ps1`, `installer.sh`
- `packaging/**` (`*.js`, `*.py`, `*.ps1`, `*.sh`)
- `scripts/validate-and-push.ps1`, `scripts/validate-and-push.sh`

Paths outside this set are **not** scanned by this tool (for example `docs/**`,
`.cursor/**`, `sprints/**`, `handoffs/**`, `decisions/**` remain free to use
story/decision/research IDs). If a new operator-visible deliverable is added
outside these roots, extend the scan list or you risk
`METADATA_SANITIZATION_SCOPE_AMBIGUOUS` classification during review.

### Command

```bash
python scripts/check-user-visible-metadata.py
python scripts/check-user-visible-metadata.py --json
```

### Reason codes (minimum)

- `USER_VISIBLE_INTERNAL_METADATA_DETECTED` — forbidden token matched inside a
  scanned user-visible string/literal.
- `METADATA_SANITIZATION_POLICY_MISSING` — checker entrypoint missing or
  unusable.
- `METADATA_SANITIZATION_SCOPE_AMBIGUOUS` — cannot classify whether a path
  belongs in inclusive scan roots; treat as fail-closed until the runbook table
  is updated.

### Findings / remediation (contract)

On failure, diagnostics must cite **evidence_ref** (`path:line:column` when
available), **token class** (`US` \| `DEC` \| `R`), and remediation: remove the
token from operator-visible strings; keep traceability in allowlisted internal
artifacts or non-emitting comments per `DEC-0053`.

## Guided intake mode (US-0033)

Intake interaction behavior is controlled by one switch in
`.cursor/scratchpad.md`:

- `INTAKE_GUIDED_MODE=1` (default): guided PO behavior
  - targeted follow-up questions only when acceptance is ambiguous
  - at least one viable option/alternative before recommendation
  - explicit user decision authority
  - intake-time research persisted in `docs/engineering/research.md`
- `INTAKE_GUIDED_MODE=0`: low-touch intake
  - no proactive follow-up/options/research overhead unless user asks
  - duplicate/overlap backlog check remains mandatory baseline safety

## Intake decomposition and risk-aware questioning (US-0051)

When guided mode is enabled (`INTAKE_GUIDED_MODE=1`), intake adds bounded
decomposition and adaptive questioning behavior:

- Run deterministic breadth/risk heuristics before persisting a story:
  - feature/workflow-step count
  - cross-cutting impact surface
  - acceptance breadth
  - risk/unknown dependency surface
- If heuristics indicate broad/high-risk intake:
  - propose bounded multi-story decomposition (typically 2-5 stories)
  - prefer vertical-slice/workflow-step stories with independent user value
  - avoid technical-layer-only splits unless user explicitly requests
- Preserve user authority explicitly before persistence:
  - user can accept, merge, or adjust the proposed split
- Keep adaptive questioning concise and bounded:
  - ask ambiguity-driven questions plus risk-triggered questions
  - stop after bounded rounds or when acceptance confidence is sufficient
- Low-touch compatibility (`INTAKE_GUIDED_MODE=0`):
  - no forced decomposition
  - single-story default unless user explicitly asks for decomposition
  - duplicate/overlap safety remains mandatory
- Traceability requirement:
  - intake output must capture decomposition/questioning evidence in
    `docs/product/backlog.md`, `docs/product/acceptance.md`, and
    `handoffs/po_to_tl.md`.

## Mandatory intake question packs and persistence coverage gate (US-0068 / DEC-0050)

Intake persistence is fail-closed unless required topic coverage is complete (or
bounded assumptions are explicitly confirmed).

Deterministic pack contract:

- `first-intake-pack` (first/new/broad intake)
  - required topics:
    - `users_problem`
    - `runtime_target_environment`
    - `language_framework_runtime`
    - `architecture_preference`
    - `ui_design_expectations`
    - `security_compliance`
    - `non_functional_priorities`
    - `scope_timeline`
- `small-intake-pack` (small follow-up intake)
  - required topics:
    - `outcome_success_criteria`
    - `impacted_components`
    - `constraints_compatibility_risks`
    - `required_tests_acceptance_checks`
    - `done_definition`

Pack selection and coverage behavior:

- Select exactly one pack per intake write path.
- Unknown/ambiguous stack or project cues must fail closed to
  `first-intake-pack`.
- Required coverage must be evaluated before writing
  `docs/product/backlog.md` or `docs/product/acceptance.md`.
- Incomplete required coverage blocks persistence unless assumptions are
  explicitly confirmed.

Deterministic fail-closed reason codes:

- `INTAKE_REQUIRED_TOPIC_MISSING`
- `INTAKE_REQUIRED_PACK_INCOMPLETE`
- `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`
- `INTAKE_PERSISTENCE_BLOCKED`

Required remediation output on block:

- include `missing_topics`
- provide targeted follow-up prompts for missing required topics
- request explicit assumption confirmation when assumptions are used

Required persisted intake evidence fields:

- `asked_topics`
- `missing_topics`
- `assumptions_confirmed`

## First-intake full-plan coverage gate (US-0081 / DEC-0064)

For first/new/broad intake (`selected_pack=first-intake-pack`), persistence is
additionally blocked unless complete-plan coverage is machine-verifiable.

Required coverage contract fields:

- `plan_area_inventory[]` with unique stable `plan_area_id` values
- `plan_area_coverage[]` with exactly one row per `plan_area_id`
- xor mapping per row: `story_ids[]` or `deferred_ref` + `deferred_reason`
- `coverage_complete=true` only when derived validation succeeds

Coverage diagnostics (under umbrella `INTAKE_PERSISTENCE_BLOCKED`):

- `INTAKE_PLAN_COVERAGE_MISSING`
- `INTAKE_PLAN_AREA_ID_INVALID`
- `INTAKE_PLAN_COVERAGE_CONTRACT_INVALID`
- `INTAKE_PLAN_DEFERRED_REF_MISSING`

Guided and low-touch parity:

- `INTAKE_GUIDED_MODE=1` and `INTAKE_GUIDED_MODE=0` must run the same
  first-intake complete-plan validator path.
- Low-touch may reduce optional prompts but cannot bypass complete-plan coverage
  validation.

## Interactive intake evidence validation (US-0078 / DEC-0060 / US-0083 / DEC-0067)

- Interactive intake evidence validation (US-0078 / DEC-0060) — automation/harness anchor; extended rules for **US-0083** / **DEC-0067** follow in this section.

**US-0078** adds machine-verifiable **`topic_coverage`** rows, canonical **`ie:`** refs
(**DEC-0060**), asked-vs-covered enforcement, and **`assumption_confirmation_ref`**
binding before backlog/acceptance writes.

- Validator entrypoints: `python scripts/intake_evidence_validate.py --self-test`;
  `python scripts/intake_evidence_validate.py --file <bundle.json>` or `--stdin`.
- Library: `scripts/intake_evidence_lib.py` (shared rules for tests and tooling).
- Regression: `tests/intake_evidence_fixtures_test.py` (R-0055 **AC-8** matrix tiers A/B),
  invoked from `tests/run-tests.ps1` / `tests/run-tests.sh` §26k.
- **Packaged installs (BUG-0001 / DEC-0063)**: `intake_evidence_validate.py`, `intake_evidence_lib.py`, and `intake_bug_routing_guard.py` are mirrored under `template/scripts/` and listed in `docs/engineering/context/installer-owned-paths.manifest` so fresh install and `upgrade` copy them to the consumer’s `scripts/`. Drift guard: `python scripts/check_intake_template_parity.py --repo .` (also §26N in `tests/run-tests.*`). **Release (S0060)**: operator notes `handoffs/releases/S0060-release-notes.md` (gate summary + verify steps).
- **US-0084**: `remote_config_summary.py` and `guard_installer_publish.py` use the same **`template/scripts/`** mirror + manifest rows; npm **`package.json` `files`** also lists the active copies for publish.
- **Installer completeness gate (BUG-0003 / DEC-0066)**: post-install invariant checks every path in `[required_install_script_paths]` from `docs/engineering/context/installer-owned-paths.manifest`. Missing paths fail closed with `INSTALL_COMPLETENESS_FAILED` and `INSTALL_REQUIRED_SCRIPT_MISSING:<path>`. Remediation: update manifest parity (active + `template/`), ensure required script exists under `template/scripts/`, keep install/clean ownership paired, then rerun `its-magic --mode missing|upgrade` (or `python installer.py --validate-install-completeness --target <repo>` for direct diagnostics).
- **Guided** and **low-touch** (`INTAKE_GUIDED_MODE=0`) share the **same** pre-persistence
  validation pipeline; mandatory pack evidence is never skipped.
- Legacy intake evidence without **`ie:`** refs remains **grandfathered** for display until the
  next intake-driven mutation, which must supply full evidence (**DEC-0060** §5).
- **Delegated required-topic path (US-0083 / DEC-0067)**:
  - Allowed: `topic_coverage[].satisfied_by=delegation_ref` with required
    `delegation_scope`, `delegation_rationale`, `delegation_confidence` (`low|medium|high`).
  - Missing delegation fields fail closed with `INTAKE_DELEGATION_EVIDENCE_MISSING`.
  - Malformed delegation values or invalid `ie:` binding fail closed with
    `INTAKE_DELEGATION_EVIDENCE_INVALID`.
  - Non-delegated unresolved required topics remain unchanged fail-closed
    (`INTAKE_REQUIRED_TOPIC_MISSING` path).
- **Repetitive-ask suppression with accounting (US-0083 AC-1)**:
  - When equivalent evidence already exists, avoid re-asking by recording row-level
    `evidence_source=equivalent_evidence_ref` plus `equivalent_evidence_ref`.
  - Required-topic accounting remains explicit through `topic_coverage` rows.

## Bug issues (US-0079 / DEC-0061)

- **Canonical ids**: **`BUG-####`** in **`docs/product/backlog.md`** **`## Bug issues (canonical)`**; status literals **`OPEN`** | **`DONE`** only — illegal values fail **`BUG_VALIDATION_STATUS_INVALID`**.
- **Minimum fields** (non-empty): **`environment`**, **`steps_to_reproduce`**, **`expected`**, **`actual`**, **`evidence_refs`** — missing/empty → **`BUG_VALIDATION_FIELD_EMPTY`** (or **`BUG_VALIDATION_SECTION_MISSING`** when the region is absent).
- **Ordering**: bug blocks sorted by id ascending — violation → **`BUG_VALIDATION_ORDER_INVERSION`**.
- **Intake routing**: merged **`INTAKE_WORK_ITEM_KIND=story|bug`** and/or explicit **`/intake bug`**; defect-shaped prose with **`story`** kind → **`INTAKE_BUG_ROUTING_REQUIRED`** via **`python scripts/intake_bug_routing_guard.py`** (**DEC-0061** §5). Mismatch/conflict → **`INTAKE_WORK_ITEM_KIND_MISMATCH`** family (documented in command surfaces).
- **Acceptance reconciliation**: **`docs/product/acceptance.md`** **`## Bug acceptance (canonical)`** checkbox rows must match backlog bug status — drift codes **`BUG_RECONCILE_ACCEPTANCE_*`**.
- **Commands**:
  - `python scripts/bug_issue_validate.py --self-test`
  - `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md [--check-acceptance] [--print-next-id]`
  - `python scripts/intake_bug_routing_guard.py --kind story|bug --file <path>` (or **`--stdin`**)
- **Regression**: `tests/bug_issue_fixtures_test.py` (R-0056 Tier A/B), invoked from **`tests/run-tests.ps1` / `tests/run-tests.sh`** §26L.

## Optional ID namespace bootstrap (US-0052)

Fresh-project ID bootstrap is optional and default-off in
`.cursor/scratchpad.md`:

- `ID_NAMESPACE_BOOTSTRAP=0|1` (default `0`)

Deterministic behavior:

- If `ID_NAMESPACE_BOOTSTRAP=1`, evaluate freshness eligibility before creating
  new IDs:
  - no `US-` IDs in `docs/product/backlog.md`
  - no `DEC-` IDs in `docs/engineering/decisions.md` (and no existing
    `decisions/DEC-*.md`)
  - no `R-` IDs in `docs/engineering/research.md`
- If eligible, first created IDs start at:
  - `US-0001` for intake stories
  - `DEC-0001` for architecture decisions
  - `R-0001` for research entries
- If not eligible (or mode is off), continue from highest existing ID in each
  namespace.
- Never rewrite/renumber historical IDs.
- If bootstrap is requested but ineligible, emit deterministic diagnostic
  `ID_BOOTSTRAP_NOT_FRESH` and continue with highest-existing continuation.

## Context compaction and token profile mode (US-0053 / DEC-0035)

Tiered token-cost control is explicit and defaulted in `.cursor/scratchpad.md`:

- `TOKEN_PROFILE=lean|balanced|full` (default `balanced`)

Deterministic profile semantics:

- `lean`: lowest context breadth / token cost defaults while preserving mandatory
  quality/release gates.
- `balanced`: moderate context breadth / token cost.
- `full`: highest context breadth / token cost for complex/high-uncertainty work.

Manual override precedence:

- Explicit flag values remain authoritative for that flag.
- If a flag is explicitly set, it overrides profile defaults.
- Profile changes must not disable mandatory gate contracts
  (`/qa`, `/verify-work`, `/release`).

### Token-cost evidence + comparability (US-0080 / DEC-0062)

- **Fresh context**: spawn **new** subagents per `/auto` phase; avoid carrying prior chat
  reasoning as phase input.
- **`start-from`**: use **`/auto start-from=<canonical_phase_id>`** when resuming so the
  schedule intersection matches materialized **`resolved_phase_plan`** (**`DEC-0052`**).
- **`TOKEN_PROFILE`**: **TOKEN_PROFILE controls context breadth / token cost only**;
  does **not** change automation level, drain, outer-driver invocation, or remove
  isolation, strict-proof, role, or release gates.
- **Metrics**: append-only **`handoffs/token_cost_runs/<orchestrator_run_id>.md`** (or
  **`.jsonl`**); copy path into **`token_cost_evidence_ref`** on **`state.md`** checkpoints.
- **AC-2**: compare **`cache_read_tokens`** only when **`run_class_hash`** matches; else
  **`TOKEN_COST_RUN_CLASS_MISMATCH`**.
- **`delivery_mode`** (US-0096 / DEC-0082): required key in sorted JSON run-class object
  (amends **DEC-0062**). Evidence rows in **`handoffs/token_cost_runs/<orchestrator_run_id>.md`**
  **must** include **`delivery_mode`** column. **`ultra_lean`** vs **`standard`** on same story →
  **`TOKEN_COST_RUN_CLASS_MISMATCH`**. Tranche A target: **≥10%** **`cache_read_tokens`** reduction
  on matched **`standard`** runs vs pre-US-0096 baseline.
- **CI/repo checks**: `python scripts/check_token_cost_parity.py --repo .` (manifest-listed
  active/`template/` pairs); **`tests/run-tests.ps1`** / **`tests/run-tests.sh`** §26M.

### Delivery modes (US-0096 / DEC-0082)

> **`DELIVERY_MODE`** controls lifecycle shape and artifact surfaces only. **`TOKEN_PROFILE`** controls context breadth / token cost only (**DEC-0062**). **`CAVEMAN_MODE`** controls reply voice only (**DEC-0072**). None substitutes for another.

| Key | Values | Default |
|-----|--------|---------|
| **`DELIVERY_MODE`** | `standard` \| `ultra_lean` \| `mega_quick` | `standard` |
| **`LEAN_MEMORY_READ`** | `0` \| `1` | `1` |
| **`LEAN_MEMORY_WRITE`** | `0` \| `1` | `1` |
| **`LEAN_COLD_READ_MAX_SECTIONS`** | int ≥ 1 | `4` |
| **`LEAN_STATE_INDEX_ROWS`** | int ≥ 30 | `80` |
| **`AUTO_DELIVERY_ROUTING`** | `scratchpad_only` \| `backlog_then_scratchpad` | `scratchpad_only` |

**Tranche A default hot caps** (example scratchpad; explicit operator values override):
**`STATE_HOT_MAX_LINES=1000`**, **`PO_TO_TL_HOT_MAX_LINES=650`**, **`ARCH_HOT_MAX_LINES=3000`**.

#### Operator recipes

| Mode | When to use | Avoid when |
|------|-------------|------------|
| **`standard`** | Full lifecycle, cross-cutting stories, companion DEC, release gates | N/A (default) |
| **`ultra_lean`** | P1 stories with clear AC, token budget pressure, institutional memory needed | Mid-story mode switch; no validator/index |
| **`mega_quick`** | ≤3 AC, single component, docs-only or tiny fix | Architecture-first; existing **`Sxxxx`**; bug segments |

#### Tranche A universal wins (always-on)

1. **Narrow-read** in all phase command **`Inputs`** — cite **`phase-context.md`** + story section
   anchor; forbid full-file reads when heading exists.
2. **Delta handoffs** — append delta paragraphs to handoff bodies; no full rewrites of prior content.
3. **Touch-graph reads** — before **`/execute`**, read **`docs/engineering/codebase-map.md`**
   component slice + touched paths from sprint/tasks or pack.

#### `ultra_lean` E2E operator recipe (`build+verify`)

1. Set **`DELIVERY_MODE=ultra_lean`**, **`LEAN_MEMORY_READ=1`**, **`LEAN_MEMORY_WRITE=1`**.
2. Run **`/auto`** — expect four macro-phases: **`spec`**, **`plan`**, **`build+verify`**, **`ship`**.
3. **`build+verify`** merges execute + qa + verify-work in one spawn; **`AUTO_IMPLEMENTATION_LOOP`**
   loops inside macro-phase until green or cap.
4. Warm memory: **`work/<story_id>/pack.json`** (validate with **`scripts/pack_json_validate.py`**).
5. Hot index: **`handoffs/active-context.md`** (30–80 lines; **not** triad).

#### Layered memory + gates

- active-context.md is NOT a triad member — triad enforcement unchanged (**DEC-0054**).
- Rollover → **`handoffs/archive/active-context-<story_id>-<utc>.md`** on oversize or segment close.
- **`LEAN_MEMORY_READ=0`** or **`LEAN_MEMORY_WRITE=0`** on **`ultra_lean`** → **`LEAN_MEMORY_DISABLED`**.

#### Quality floor (all lean modes)

- Tests run before stop.
- AC traceability in **`pack.json`** or **`task.json`**.
- New patterns → architecture/decision delta.
- **`active-context.md`** updated on material learnings.
- No secrets / publish bypass (**`RELEASE_PUBLISH_MODE`** unchanged).

#### Backlog routing (optional)

When **`AUTO_DELIVERY_ROUTING=backlog_then_scratchpad`**, story row may declare optional
**`delivery_mode:`** field. Precedence: argv **`delivery-mode=`** → story row → scratchpad → **`standard`**.

**Release status (S0086 / US-0096)**: **`released`** (`2026-06-13T16:00:00Z`); **`US-0096`** **DONE** in canonical backlog. Operator verify: **`handoffs/releases/S0086-release-notes.md`** **## Verify**; publish skipped while **`RELEASE_PUBLISH_MODE=confirm`**.

## Per-phase model tier selection (US-0101 / DEC-0086)

`MODEL_TIER` selects LLM model strength (which model runs per lifecycle phase).
Three operator-facing tiers map to stable Cursor aliases — no vendor slugs in
template files.

| Key | Values | Default | Role |
|-----|--------|---------|------|
| **`MODEL_TIER_DEFAULT`** | `cheap` \| `balanced` \| `strong` | `balanced` | Fallback when phase-specific key absent |
| **`MODEL_TIER_<PHASE>`** | `cheap` \| `balanced` \| `strong` | *(per matrix)* | Per-phase tier override |
| **`MODEL_CATALOG`** | path | `.cursor/model-catalog.local.json` | Path to local slug catalog |
| **`MODEL_RESOLVE`** | `alias_only` \| `local_catalog` | `alias_only` | Resolution strategy |
| **`MODEL_FALLBACK`** | `inherit` | `inherit` | Fallback when catalog lookup fails |
| **`MODEL_PROVIDER_MODE`** | `cursor` \| `api` | `cursor` | Provider routing |

### Default phase→tier matrix (architecture-locked)

| Tier | Cursor alias | `model:` field | Phases |
|------|-------------|----------------|--------|
| **`cheap`** | `fast` | `model: fast` | `ask`, `refresh-context`, `memory-audit`, `status-reconcile`, `pause` |
| **`balanced`** | `inherit` | `model: inherit` | `intake`, `discovery`, `research`, `release`, `plan-verify` |
| **`strong`** | *(omit)* | no `model:` field | `architecture`, `execute`, `quick`, `qa`, `verify-work`, `security-review` |
| *(inherit parent)* | — | — | `auto` (orchestrator always inherits parent model) |

### Provider mode (MODEL_PROVIDER_MODE)

| Mode | Description |
|------|-------------|
| **`cursor`** (default) | All subagents route through Cursor-managed infrastructure; tier aliases work as designed |
| **`api`** | Operator uses BYOK via Cursor Settings → Models → API Key |

**Known limitation (confirmed 2026-06)**: Cursor subagents do **NOT** inherit
custom API keys or base URLs — they always bill against the Cursor plan. When
`MODEL_PROVIDER_MODE=api`, the local catalog is the only operator-controlled
surface; subagent `model:` aliases still resolve through Cursor infrastructure.

**Workaround recipes**:

1. **Parent model + `inherit`** — set the parent chat model to the desired BYOK
   model; subagents using `model: inherit` (balanced tier) pick it up.
2. **Manual phase runs** — run each phase in a separate chat with the desired
   model selected at the chat level (no subagent spawn).
3. **Local catalog override** — set `MODEL_RESOLVE=local_catalog` and populate
   `.cursor/model-catalog.local.json` with vendor slugs; materializer applies
   slugs at template materialization time (not at subagent runtime).

### Non-substitution paragraph

MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE

> **`MODEL_TIER`** selects LLM model strength (which model runs).
> **`TOKEN_PROFILE`** selects context breadth / token cost (how much context the model sees).
> **`DELIVERY_MODE`** selects lifecycle shape (standard / ultra_lean / mega_quick).
> These are **independent axes** — none substitutes for another. A `strong` tier
> with `lean` profile is valid; a `cheap` tier with `full` profile is valid.
> Setting one does not change the others. Combine freely.

### Reason codes — `MODEL_TIER_*` / `MODEL_CATALOG_*` / `MODEL_RESOLVE_*` / `MODEL_SLUG_*`

| Code | Trigger |
|------|---------|
| **`MODEL_TIER_INVALID`** | Unknown tier value (not `cheap`/`balanced`/`strong`) |
| **`MODEL_CATALOG_INVALID`** | Malformed catalog JSON (parse error, missing `schema_version`) |
| **`MODEL_SLUG_UNKNOWN`** | Tier key missing from catalog when `MODEL_RESOLVE=local_catalog` |
| **`MODEL_RESOLVE_FALLBACK`** | Catalog lookup failed but `MODEL_FALLBACK=inherit` → reason + fallback |

### Template agent defaults

| Agent role | Tier | `model:` field |
|-----------|------|----------------|
| `curator` | cheap | `model: fast` |
| `po` | balanced | `model: inherit` |
| `release` | balanced | `model: inherit` |
| `tech-lead` | strong | *(omit)* |
| `dev` | strong | *(omit)* |
| `qa` | strong | *(omit)* |
| `security` | strong | *(omit)* |

**Forbidden in `template/.cursor/agents/`**: hardcoded vendor slugs
(`composer-*`, `claude-*`, `gpt-*`, `opus-*`). Template files use aliases only.

### Local catalog schema (v1)

```json
{
  "schema_version": 1,
  "tiers": {
    "cheap": "<slug>",
    "balanced": "<slug>",
    "strong": "<slug>"
  },
  "notes": "optional free-text"
}
```

- Path: `.cursor/model-catalog.local.json` (gitignored)
- Example: `.cursor/model-catalog.local.example.json` (committed, placeholder values)
- All three tier keys required; values are opaque vendor slug strings

### Resolver algorithm

1. Read `MODEL_TIER_<PHASE>` from merged scratchpad → tier value
2. If `MODEL_RESOLVE=alias_only` (default): use built-in mapping (table above)
3. If `MODEL_RESOLVE=local_catalog`: load catalog JSON → lookup tier key → slug
4. If key missing → `MODEL_SLUG_UNKNOWN` fail-closed
5. If `MODEL_FALLBACK=inherit` and lookup fails → emit `MODEL_RESOLVE_FALLBACK` + use `inherit`
6. Unknown tier value → `MODEL_TIER_INVALID` fail-closed
7. Malformed catalog JSON → `MODEL_CATALOG_INVALID` fail-closed

### Validation commands

- `python scripts/model_tier_validate.py --repo .`
- `pytest -k us0101 tests/auto_command_contract_test.py`
- `python scripts/check_intake_template_parity.py --scope=model-tier`
- `tests/run-tests.ps1` / `tests/run-tests.sh` §26Z

Normative architecture: `docs/engineering/architecture.md` (**# US-0101**).

## Direct per-phase model slug override + role catalog (US-0102 / DEC-0087)

Composes on **US-0101** / **DEC-0086** — tier-only operators need no migration.

### 5-step precedence chain

| Step | Source | Outcome |
|------|--------|---------|
| **1** | `MODEL_<PHASE>` | Non-empty slug → return (validate per mode) or `MODEL_OVERRIDE_SLUG_UNKNOWN` |
| **2** | `MODEL_TIER_<PHASE>` | **DEC-0086** tier→alias / `local_catalog` chain |
| **3** | `MODEL_RESOLVE=role_catalog` | Phase→logical role → catalog `roles[<key>]`; miss → `MODEL_ROLE_SLUG_UNKNOWN` → fall through |
| **4** | `MODEL_TIER_DEFAULT` | **DEC-0086** tier chain |
| **5** | Cursor alias | **DEC-0086** built-in mapping |

When `MODEL_RESOLVE` is `alias_only` or `local_catalog`, step **3** is skipped.

### Scratchpad keys (new)

| Key | Default | Role |
|-----|---------|------|
| **`MODEL_<PHASE>`** | *(absent)* | Direct vendor slug; includes `MODEL_ASK` |
| **`MODEL_RESOLVE`** | `alias_only` | Extended: `alias_only` \| `local_catalog` \| **`role_catalog`** |

Operator slugs live in `.cursor/scratchpad.local.md` and `.cursor/model-catalog.local.json` only (gitignored).

### Role catalog enablement recipe

1. Copy a v2 example catalog:
   - `.cursor/model-catalog.local.example.role-based-balanced.json`, or
   - `.cursor/model-catalog.local.example.role-based-highend.json`
2. Save as `.cursor/model-catalog.local.json` with real vendor slugs.
3. Set `MODEL_RESOLVE=role_catalog` in `.cursor/scratchpad.local.md`.
4. Optional: set `MODEL_<PHASE>=<slug>` for direct overrides (step 1 wins over role lookup).
5. Run `python scripts/model_tier_validate.py --repo .` to validate.

On role lookup miss → `MODEL_ROLE_SLUG_UNKNOWN` emitted; resolver falls through to `MODEL_TIER_DEFAULT` then Cursor alias.

**`dev_difficult`**: no automatic phase routing — use `MODEL_EXECUTE=<slug>` direct override or tier `strong` + catalog tier slug.

Non-normative role recommendations: `ai_modell_auslegung_cursor_highend.md`.

### Catalog schema v2 (opt-in)

```json
{
  "schema_version": 2,
  "tiers": { "cheap": "<slug>", "balanced": "<slug>", "strong": "<slug>" },
  "roles": {
    "po": "<slug>", "sa": "<slug>", "dev": "<slug>", "dev_difficult": "<slug>",
    "qa": "<slug>", "security": "<slug>", "release": "<slug>"
  }
}
```

v1 catalogs (tiers only) unchanged. Malformed v2 → `MODEL_CATALOG_SCHEMA_V2_INVALID`.

### New reason codes

| Code | Trigger |
|------|---------|
| **`MODEL_OVERRIDE_SLUG_UNKNOWN`** | Direct slug validation failure |
| **`MODEL_ROLE_SLUG_UNKNOWN`** | Role catalog lookup miss |
| **`MODEL_CATALOG_SCHEMA_V2_INVALID`** | v2 schema validation failure |

### Non-substitution paragraph

MODEL_TIER ≠ TOKEN_PROFILE ≠ DELIVERY_MODE — unchanged from **US-0101**; model selection is orthogonal to context breadth.

### Validation commands

- `python scripts/model_tier_validate.py --repo .`
- `pytest -k us0102 tests/auto_command_contract_test.py`
- `python scripts/check_intake_template_parity.py --scope=model-tier-overrides`
- `tests/run-tests.ps1` / `tests/run-tests.sh` §26AA

Normative architecture: `docs/engineering/architecture.md` (**# US-0102**); decision: **`DEC-0087`**.

Binding decision: `decisions/DEC-0086.md`.

Context compaction policy:

- `docs/engineering/state.md` is a compact hot surface for current execution
  context and recent checkpoints.
- Historical state packs belong in `docs/engineering/state-archive/` and are
  append-only/non-destructive.
- `docs/engineering/decisions.md` is a compact index with bounded summaries and
  canonical links to full records in `decisions/DEC-xxxx.md`.
- Enforced rollover thresholds:
  - `STATE_HOT_MAX_LINES` (default `1200`)
  - `STATE_HOT_MAX_CHECKPOINTS` (default `80`)
  - `PO_TO_TL_HOT_MAX_LINES` (default `800`)
  - `PO_TO_TL_HOT_MAX_SECTIONS` (default `60`)
  - `ARCH_HOT_MAX_LINES` (default `3500`)
  - `ARCH_HOT_MAX_STORY_SECTIONS` (default `120`)
  Thresholds resolve from merged `.cursor/scratchpad.md` +
  `.cursor/scratchpad.local.md` (DEC-0054 triad contract).
  When a cap is exceeded, the mutating phase must run rollover **before**
  completion or fail closed (no successful completion with an oversize hot
  surface).

### Triad hot-surface enforcement (DEC-0054)

Canonical hot/archive surfaces:

- `docs/engineering/state.md` → `docs/engineering/state-archive/state-pack-*.md`
- `handoffs/po_to_tl.md` → `handoffs/archive/po-to-tl-pack-*.md`
- `docs/engineering/architecture.md` →
  `docs/engineering/architecture-archive/architecture-pack-*.md`

Operator commands:

```bash
python scripts/enforce-triad-hot-surface.py --check
python scripts/enforce-triad-hot-surface.py --rollover
```

- `--check` verifies all three surfaces are within policy (CI-safe).
- `--rollover` archives oldest contiguous units into the next deterministic pack
  name; reruns are idempotent when already within caps.
- Successful rollover records a verification tuple:
  `boundary`, `moved`, `retained` (counts / lines), `pack_ref`.

Rollover fail-safe reason codes:

- `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`
- `STATE_ARCHIVE_WRITE_FAILED`
- `STATE_ARCHIVE_VERIFICATION_FAILED`
- `STATE_ARCHIVE_REQUIRED`
- `ARTIFACT_HOT_SURFACE_OVERSIZE`
- `ARCH_STORY_HEADING_LEVEL_INVALID`
- `CONTEXT_BUDGET_EXCEEDED`

**Architecture file blocked on rollover?** If story sections use legacy H2 `## US-xxxx`
headings, the archiver now recognizes them for rollover after **BUG-0010**. For new work,
`/architecture` must append H1 `# US-xxxx` (or `# BUG-xxxx` for defects). To converge an
existing repo, optionally normalize `## US-xxxx` → `# US-xxxx` manually (count decrease is
allowed; adding new `## US-` story headings is blocked).

### Minimal-read defaults by phase (bounded escalation)

Read `docs/engineering/phase-context.md` first, then the **required** paths for
your phase. If unresolved, expand once to the **single** archive pack named in
the latest verification tuple for that surface. Do not load entire archive
directories by default.

| Phase | Required reads (default) | Combined line budget (guidance) |
|-------|--------------------------|----------------------------------|
| `/intake` | `phase-context.md`, target story in `docs/product/backlog.md`, `handoffs/po_to_tl.md` (tail) | ≤ 900 lines |
| `/discovery` | `phase-context.md`, `docs/product/vision.md` (story notes), `handoffs/po_to_tl.md` (tail) | ≤ 900 lines |
| `/research` | `phase-context.md`, `docs/engineering/research.md` (target entry), `docs/product/backlog.md` (target story) | ≤ 800 lines |
| `/architecture` | `phase-context.md`, `docs/engineering/architecture.md` (target story section), `docs/engineering/research.md` | ≤ 1200 lines |
| `/sprint-plan` | `phase-context.md`, `docs/engineering/architecture.md` (target story), `handoffs/tl_to_dev.md` | ≤ 1000 lines |
| `/plan-verify` | `phase-context.md`, `sprints/Sxxxx/tasks.md`, `docs/product/backlog.md` (ACs) | ≤ 900 lines |
| `/execute` | `phase-context.md`, `sprints/Sxxxx/tasks.md`, `handoffs/tl_to_dev.md` | ≤ 800 lines |
| `/qa` | `phase-context.md`, `sprints/Sxxxx/`, `tests/report.md` | ≤ 900 lines |
| `/verify-work` | `phase-context.md`, `sprints/Sxxxx/uat.json`, QA findings | ≤ 600 lines |
| `/release` | `phase-context.md`, release queue + sprint release findings | ≤ 700 lines |
| `/refresh-context` | `phase-context.md`, `docs/engineering/state.md` (tail), `docs/product/backlog.md` (status) | ≤ 900 lines |
| `/auto` (resolver) | `phase-context.md`, `handoffs/resume_brief.md`, `docs/engineering/state.md` (tail) | ≤ 700 lines |

If the default set is insufficient, escalate with an explicit note citing
`pack_ref`. Unbounded broad reads fail closed with `CONTEXT_BUDGET_EXCEEDED`.

`/ask` retrieval policy:

- Use question-scoped narrow reads first.
- Expand context in bounded steps only when unresolved.
- If unresolved after bounded expansion, answer with explicit "not found in
  current artifacts" rather than broad speculative reads.

## Model-catalog example preset delivery (US-0112 / DEC-0112)

**Default state**: 8 committed `model-catalog.local.example*.json` presets ship with the
`its-magic` framework and are delivered to operator repos via the installer manifest
(`docs/engineering/context/installer-owned-paths.manifest` [install_include_paths]) under
**framework-file semantics** (US-0018 / US-0057 / US-0075 precedence).

### Eight preset filenames (manifest rows)

1. `.cursor/model-catalog.local.example.json` — base placeholder (three tiers, opaque vendor slugs)
2. `.cursor/model-catalog.local.example.cursor-only.json` — Cursor-first alias mapping
3. `.cursor/model-catalog.local.example.level-1-easy.json` — easy complexity tier set
4. `.cursor/model-catalog.local.example.level-2-complex.json` — moderate complexity tier set
5. `.cursor/model-catalog.local.example.level-3-mega.json` — heavy complexity tier set
6. `.cursor/model-catalog.local.example.level-4-super.json` — maximal complexity tier set
7. `.cursor/model-catalog.local.example.role-based-balanced.json` — role-catalog balanced preset
8. `.cursor/model-catalog.local.example.role-based-highend.json` — role-catalog high-end preset

### Installer behavior (framework-file semantics)

- **`missing` mode** (default new install): copies the 8 example presets into the target
  `.cursor/` directory when absent; deterministic status log per file (names only; no content
  inspection); same semantics as `scratchpad.local.example.md` per US-0075.
- **`upgrade` mode**: refreshes the example presets when the packaged template version
  differs (byte-compare); skips byte-identical files; never modifies or removes the active
  operator-owned `.cursor/model-catalog.local.json` (gitignored; not in manifest).
- **Triple installer parity**: `installer.py`, `installer.ps1`, `installer.sh` all read the
  single manifest `[install_include_paths]` as source of truth; framework classification
  for `.cursor/model-catalog.local.example*.json` is identical across Python / PowerShell /
  Bash `classify_file` paths.

### Operator usage recipe

1. Inspect the 8 presets under `.cursor/` (shipped automatically by install or upgrade).
2. Choose a preset matching your intent — complexity-based (levels 1–4) or role-based
   (balanced / highend) for `MODEL_RESOLVE=role_catalog`; cursor-only alias mapping; or
   base template for custom tiers.
3. Copy the chosen preset: `cp .cursor/model-catalog.local.example.<preset>.json .cursor/model-catalog.local.json`.
4. Edit real vendor slugs into `.cursor/model-catalog.local.json` (placeholder values
   substituted; vendor-specific).
5. Set `MODEL_RESOLVE=local_catalog` (or `role_catalog` for role-based presets) in
   `.cursor/scratchpad.local.md`.
6. Validate: `python scripts/model_tier_validate.py --repo .`.
7. Parity: `python scripts/check_intake_template_parity.py --scope=model-catalog-examples`.

**Active catalog protection invariant**: `.cursor/model-catalog.local.json` remains
gitignored and outside `install_include_paths` + `clean_paths`. The installer never
auto-populates it. No installer mode copies, merges, or replaces the active catalog.
This is a DEC-0086 / DEC-0087 boundary (US-0101 catalog schema + US-0102 role precedence
remain unaltered; US-0112 only completes delivery path).

### Parity scope

```bash
python scripts/check_intake_template_parity.py --scope=model-catalog-examples
```

Validates active vs template byte-parity for `installer-owned-paths.manifest` (16 manifest
rows total across active + template paths). On mismatch → `MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_MISMATCH`.
On pass → `[MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_OK]`.

### Reason codes

| Code | Trigger |
|------|---------|
| `MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_OK` | Active vs template manifest byte-parity pass for 8 model-catalog.example paths |
| `MODEL_CATALOG_EXAMPLE_PARITY_SCOPE_MISMATCH` | Active vs template manifest byte-parity fail |

### Validation commands

- `python scripts/check_intake_template_parity.py --scope=model-catalog-examples`
- `pytest -k us0112 tests/us0112_contract_test.py`

Normative architecture: `docs/engineering/architecture.md` (**# US-0112**); decision: **`DEC-0112`** (Accepted).

Binding decision: `decisions/DEC-0112.md`. Research anchor: `docs/engineering/research.md` **R-0090**.

## Configurable multi-target publish mode (US-0054 / DEC-0036)

Post-release publish orchestration is configurable and default-safe:

- `RELEASE_PUBLISH_MODE=disabled|confirm|auto` (default `confirm`)
- `RELEASE_TARGETS_FILE=docs/engineering/release-targets.json`
- `RELEASE_TARGETS_DEFAULT=` optional comma-separated default target IDs

Target schema contract:

- Canonical target config file: `docs/engineering/release-targets.json`
- Supported target types:
  - `npm`, `choco`, `brew`, `git`, `docker`, `cloud`
  - `custom` (generic command target)
  - `ssh` (host/user/port/auth reference + remote command)
- Connectivity metadata (for operator-safe remote/local context):
  - `runtime.mode` (`local|remote`)
  - endpoint fields (`domainEnv|ipEnv|hostEnv`, `port`, `protocol`)
  - optional ingress metadata (`traefik.enabled`, `router`, `entrypoint`, `tls`)
  - optional `dockerOverSsh` object for ssh/dockerd remote execution context
- Each target entry must define deterministic fields:
  - `id` (stable unique target ID)
  - `type`
  - `enabled` (`true|false`)
  - `order` (deterministic execution ordering)
  - execution details (`command` for non-ssh, `remoteCommand` + host/user/auth refs for `ssh`)

Safety contract:

- Mandatory release gates remain unchanged and must pass before any publish
  target execution.
- `confirm` mode requires explicit operator approval before publish execution.
- Sensitive fields must be env-referenced (`*Env` keys); inline secret literals
  are not allowed.
- Invalid target config must fail fast with deterministic diagnostics and no
  partial side effects.
- Invalid remote connectivity metadata must fail fast with
  `REMOTE_CONNECTIVITY_CONFIG_INVALID`.
- Canonical operator endpoint summary is written to
  `docs/engineering/runtime-connectivity.md` with sanitized values only.

## Release operator hints contract (US-0067 / DEC-0049)

Release outputs must include deterministic operator-ready hints with mandatory
section order:

`Run -> Connect -> Verify -> Credentials -> Known Issues`

Required fields for canonical sprint notes
(`handoffs/releases/Sxxxx-release-notes.md`):

- `Run`: `start_command`, `runtime_mode`, `runtime_context_ref`
- `Connect`: `service_url`, `service_port`, `health_endpoint`
- `Verify`: deterministic `verification_steps`, `expected_health_signal`
- `Credentials`: env-reference-only source refs and expected value-source
  location guidance (never inline secrets)
- `Known Issues`: concise issue list or explicit `None`

Legacy pointer contract (`handoffs/release_notes.md`):

- keep concise latest run/connect/verify summary only
- always link to canonical sprint-scoped release notes for full details

Fail-closed reason codes:

- `RELEASE_OPERATOR_HINTS_MISSING`
- `RELEASE_OPERATOR_HINTS_AMBIGUOUS`
- `RELEASE_OPERATOR_HINTS_SECRET_EXPOSURE`

## Version-scoped release docs (US-0100 / DEC-0085)

Cumulative and per-version release documentation compose with **US-0040** sprint
notes — they do **not** replace `handoffs/releases/Sxxxx-release-notes.md`.

| Artifact | Path | Role |
|----------|------|------|
| Cumulative changelog | `CHANGELOG.md` | Keep a Changelog 1.1.0; mandatory top `## [Unreleased]` |
| Per-version GitHub body | `handoffs/releases/{semver}-release-notes.md` | **`gh -F` SOT** (semver stem without `v`) |
| Sprint workflow evidence | `handoffs/releases/Sxxxx-release-notes.md` | Unchanged (**US-0040**); derivation input only |
| Backfill manifest | `docs/engineering/context/release-version-backfill.manifest.yaml` | Tier B operator `sprint_id`→`semver` overrides |

### Operator workflow (deterministic order)

1. **`/release`** (local workflow): after step **9** finalization, step **19**
   derives work items, writes version docs when semver known, or appends
   `[Unreleased]` only when semver blank.
2. **`release-all.sh`** (npm/choco/brew + GitHub): post-`npm version`, ensure
   `handoffs/releases/${NEW_VERSION}-release-notes.md`, run
   `release_changelog_validate.py --enforce`, then `gh release create -F`.
3. **CI tag push** (when **US-0054** publish targets enabled): same `-F` path;
   confirmation gates unchanged.

### Scratchpad keys

| Key | Default | Role |
|-----|---------|------|
| `RELEASE_CHANGELOG_ENFORCE` | `1` | Blocking validator at `/release` step **19d** + `release-all.sh` |
| `RELEASE_CHANGELOG_ALLOW_GENERATE_NOTES` | `0` | Opt-in `gh --generate-notes` when version doc missing |

### Backfill tiers (one-time / idempotent)

| Tier | Source | Semver |
|------|--------|--------|
| A | Queue `release_version` non-empty | As-is |
| B | `release-version-backfill.manifest.yaml` | Operator map |
| C | Remaining released rows | Synthetic `0.0.0-wf.{NNN}` (`S0089`→`0.0.0-wf.089`) |

Run: `python scripts/release_changelog_backfill.py --repo .` (idempotent).
Ambiguous manifest collision → `RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS`.

### Troubleshooting (`RELEASE_CHANGELOG_*`)

| Code | Remediation |
|------|-------------|
| `RELEASE_CHANGELOG_VERSION_DOC_MISSING` | Run `build_version_doc` / backfill `--ensure-version` before `gh -F` |
| `RELEASE_CHANGELOG_UNRELEASED_MISSING` | Add `## [Unreleased]` header to `CHANGELOG.md` |
| `RELEASE_CHANGELOG_QUEUE_DRIFT` | Re-run `bind_queue_release_version` for target sprints |
| `RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS` | Fix manifest duplicate semver mapping |

Contract tests: `pytest -k us0100 tests/auto_command_contract_test.py`; parity:
`python scripts/check_intake_template_parity.py --scope=release-changelog`.

## Deterministic status reconciliation mode (US-0055 / DEC-0037)

Use the dedicated reconciliation command to normalize status drift across
canonical and derived artifacts:

- Command: `/status-reconcile`
- Canonical source: `docs/product/backlog.md` (story `Status`)
- Derived surfaces: `docs/product/acceptance.md`, `docs/engineering/state.md`,
  `handoffs/resume_brief.md`

Deterministic behavior:

- Detects mismatches (for example DONE + unchecked ACs, acceptance drift, resume drift).
- Applies target-scoped reconciliation only to mismatched story blocks/rows.
- Preserves canonical ownership; derived artifacts reconcile to backlog status.
- Updates `handoffs/resume_brief.md` to next OPEN story and intended phase.
- Writes auditable rows to `docs/engineering/status-normalization-report.md`.

Reason-code baseline:

- `STATUS_RECONCILE_APPLIED`
- `STATUS_RECONCILE_NOOP`
- `STATUS_RECONCILE_MISSING_INPUT`
- `STATUS_RECONCILE_CANONICAL_CONFLICT`
- `STATUS_RECONCILE_PHASE_AMBIGUOUS`
- `STATUS_RECONCILE_EVIDENCE_MISSING`

## Optional cross-repo observability mode (US-0034)

Compatibility visibility is optional and default-off in `.cursor/scratchpad.md`:

- `CROSS_REPO_OBSERVABILITY=0|1` (default `0`)
- `COMPATIBILITY_GATE_ON_CRITICAL=0|1` (default `1`)
- `COMPATIBILITY_SOURCES=` monitored source declarations

Default-off behavior:
- With `CROSS_REPO_OBSERVABILITY=0`, `/intake`, `/architecture`, `/execute`,
  and `/qa` add zero required compatibility overhead.

Enabled behavior (`CROSS_REPO_OBSERVABILITY=1`):
- Use canonical artifacts:
  - `docs/engineering/compatibility-report.md`
  - `docs/engineering/compatibility-signals.md`
  - `docs/engineering/manifests/registry.manifest.yaml`
  - `docs/engineering/manifests/repo.manifest.yaml`
- Record findings with severity, affected modules, evidence refs, and
  recommended actions.
- If unresolved critical findings exist and
  `COMPATIBILITY_GATE_ON_CRITICAL=1`, trigger decision gate before release
  progression (`COMPATIBILITY_CRITICAL_OPEN`).

## Optional component-scoped execution mode (US-0035)

Component-scoped execution is optional and default-off:

- `COMPONENT_SCOPE_MODE=0|1` (default `0`)
- `TARGET_COMPONENTS=` comma-separated scoped component IDs

Default-off behavior:
- With `COMPONENT_SCOPE_MODE=0`, workflow phases add zero required scope
  overhead.

Enabled behavior (`COMPONENT_SCOPE_MODE=1`):
- Declare scope in `docs/engineering/component-scope.md`:
  - `target_components[]`
  - `non_target_components[]`
  - `allowed_interface_touch[]`
- `/sprint-plan` tasks declare `target_component_ids` and
  `expected_impacted_interfaces`.
- `/execute` enforces scope-first behavior.
- `/qa` verifies unaffected-component checks and records evidence in
  `docs/engineering/component-scope-report.md`.
- If unapproved out-of-scope impact remains open, release must stop at decision
  gate (`COMPONENT_SCOPE_VIOLATION_UNAPPROVED`).

## Optional spec-pack documentation mode (US-0031)

Spec-pack mode is optional and default-off in `.cursor/scratchpad.md`:

- `SPEC_PACK_MODE=0|1` (default `0`)

Default-off behavior:
- With `SPEC_PACK_MODE=0`, `/intake`, `/architecture`, `/execute`, `/qa`, and
  `/release` add no required spec-pack steps (zero overhead).

Enabled behavior (`SPEC_PACK_MODE=1`):

**Canonical names and locations** (per story):
- Design Concept: `docs/engineering/spec-pack/<story_id>-design-concept.md`
- CRS (Customer/Product Requirements Summary): `docs/engineering/spec-pack/<story_id>-crs.md`
- Technical Specification: `docs/engineering/spec-pack/<story_id>-technical-specification.md`

**Traceability**: Backlog story ID (e.g. `US-0031`) maps 1:1 to the three
artifacts above. Handoffs and state should reference these paths when
spec-pack mode is enabled.

**Minimum required sections** (completeness is testable; validation blocks
only when enabled and a required section is missing or empty):

- Design Concept: `# Summary`, `# Goals`, `# Non-goals`, `# Key decisions`
- CRS: `# Purpose`, `# Scope`, `# Acceptance criteria ref`
- Technical Specification: `# Overview`, `# Components`, `# Interfaces`, `# Non-functional`

**Validation**: When `SPEC_PACK_MODE=1`, release gate checks that for the
target sprint story, all three artifacts exist and each required section
above is present and non-empty. If not, release is blocked with reason code
`SPEC_PACK_INCOMPLETE` and remediation guidance.

**Ownership (role/phase)**:
- Design Concept: Tech Lead, `/architecture` (create/update).
- CRS: PO, `/intake` (create/update for new story); Tech Lead may extend in
  architecture.
- Technical Specification: Tech Lead, `/architecture` (create); Dev, `/execute`
  (update when implementation details change).

## Optional user-guide documentation mode (US-0032)

User-guide mode is optional and default-off in `.cursor/scratchpad.md`:

- `USER_GUIDE_MODE=0|1` (default `0`)

Default-off behavior:
- With `USER_GUIDE_MODE=0`, `/intake`, `/architecture`, `/sprint-plan`, `/execute`,
  `/qa`, and `/release` add no required user-guide steps or blocking checks (zero overhead).

Enabled behavior (`USER_GUIDE_MODE=1`):

**Canonical location and naming** (per feature story):
- One guide per feature story: `docs/user-guides/US-xxxx.md` (e.g. `docs/user-guides/US-0032.md`).
- Story ID `US-xxxx` is the stable identifier; create/update the guide when the story is in scope.

**Minimum required schema** (structural validation only; completeness is testable):
- `# Purpose`
- `# Prerequisites`
- `# Usage steps`
- `# Example`
- `# Limitations`
- `# Troubleshooting`

**Traceability**: Story ID maps 1:1 to the user-guide artifact. Handoffs and release
context should reference `docs/user-guides/US-xxxx.md` for the target story when
user-guide mode is enabled.

**Validation**: When `USER_GUIDE_MODE=1`, release gate checks that for the target
sprint story, the guide file exists at the canonical path and each required section
above is present and non-empty. If not, release is blocked with reason code
`USER_GUIDE_INCOMPLETE` and remediation guidance (create or complete the guide).

**Boundary with spec-pack (US-0031)**: User guides are end-user facing how-to
documentation only. They do not duplicate Design Concept, CRS, or Technical
Specification content; user guides may reference spec-pack artifacts but must not
replicate their ownership or technical scope. See runbook/README separation guidance.

## Legacy DONE-story drift detection and guard (US-0049)

Stories that are DONE in backlog but lack aligned acceptance/traceability or
release representation are in **legacy drift**. US-0049 adds detection, bounded
repair, and an ongoing guard at release/reconciliation (DEC-0031).

**Detection rule** — A story is in legacy drift when:
- Backlog status is **DONE**, and
- At least one of:
  - Acceptance checklist item for that story is **unchecked**
  - Traceability index or `docs/engineering/state.md` **lacks an entry** for that story
  - Release artifacts (e.g. `handoffs/releases/Sxxxx-release-notes.md`, queue row)
    **lack clear representation** for that story

**Bounded repair**: Only stories matching the rule above may be mutated; no broad
rewrite of unrelated backlog/acceptance/state/release artifacts.

**Canonical audit artifact**: `docs/engineering/legacy-drift-audit.md`
- Required fields per entry: story ID, prior acceptance state, prior traceability
  state, resolved state(s), reason code, evidence reference.
- Append-only; one-time backfill and ongoing guard append entries when drift is
  detected and repaired (or when guard blocks and reports).

**Reason-code vocabulary** (with remediation):
- `BACKLOG_DONE_ACCEPTANCE_UNCHECKED` — Backlog DONE but acceptance item unchecked.
  Remediation: set acceptance checkbox from canonical release/state evidence or run one-time backfill.
- `BACKLOG_DONE_TRACEABILITY_MISSING` — Backlog DONE but traceability/state lacks entry.
  Remediation: add traceability row in `docs/engineering/state.md` from backlog/release evidence or run backfill.
- `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` — Backlog DONE but release artifacts lack representation.
  Remediation: ensure release notes or queue row exists for the story’s sprint or run backfill.

**One-time backfill mode**: Explicit trigger (e.g. dedicated check or `/memory-audit`-related path).
- Run detection once over all DONE stories; for each legacy-drift story, perform
  target-scoped repair and append an entry to `docs/engineering/legacy-drift-audit.md`.
- Idempotent when no drift: no mutations; report empty or "no drift".
- Only stories matching the detection rule are mutated.

**Ongoing guard**: At release or reconciliation boundary (or dedicated check).
- When legacy drift is detected, either **block** with explicit reason code and
  remediation, or **repair** target-scoped and append audit entry (policy documented).
- Behavior is deterministic; operators get explicit diagnostics.

## Memory drift auditing

Run `/memory-audit` at key workflow checkpoints to verify artifact consistency:

- **Pre-handoff**: before writing `handoffs/dev_to_qa.md` or any role handoff.
- **Pre-QA**: before running `/qa` or `/verify-work`.
- **Pre-release**: before running `/release`.
- **Ad-hoc**: after external code changes, long pauses, or whenever artifacts
  feel stale.

Output: `docs/engineering/memory-drift-report.md` — an advisory report with
severity-classified findings. The command is read-only and non-blocking.

Interpreting results:
- **high**: artifact contradicts repository state — fix before next handoff/release.
- **medium**: artifact is likely stale — fix before release.
- **low**: minor inconsistency — fix during `/refresh-context` or next sprint.

Template drift findings (active vs `template/`) are listed for reference only
and belong to US-0017 scope.

Follow-up commands: `/refresh-context`, `/sprint-plan`, `/verify-work`, `/intake`.

## Remote execution validation contract

Remote execution is mode-aware and default-off:

- `REMOTE_EXECUTION=0`: skip remote-config validation entirely (zero overhead).
- `REMOTE_EXECUTION=1`: validate `.cursor/remote.json` before remote activities;
  fail fast on first blocking issue.

Validation classes (remote-enabled mode):

1. Presence: config file exists at `REMOTE_CONFIG` (default `.cursor/remote.json`)
2. Syntax: JSON parses cleanly
3. Contract: required fields/types/enums
4. Semantics: `defaultTarget` points to an existing enabled target; target ids
   are unique
5. Security: no inline secret-like literals; env-var refs only for sensitive values

Required contract summary:

- Root: `version` (integer), `defaultTarget` (string), `targets` (array)
- Target: `id` (string), `type` (`docker|ssh|vm`), `enabled` (boolean),
  `host` (string), `port` (integer `1..65535`), `workspaceRoot` (string)
- Optional auth: `auth.mode` (`none|env`); if `env`, use `*Env` references

Error message format (actionable, fail-fast):

- `[REMOTE_CONFIG_ERROR] <path>: expected <rule>, got <actual>. Fix: <hint>.`

Operator troubleshooting:

- Missing config file:
  - Copy from `template/.cursor/remote.json`, or disable remote mode.
- Malformed JSON:
  - Fix syntax (commas/brackets/quotes), then retry.
- Invalid value or enum:
  - Correct field value to the documented contract.
- Security violation (inline secret-like literal):
  - Replace with env-var reference fields (`tokenEnv`, `passwordEnv`,
    `privateKeyPathEnv`, ...).

### Manual vs automation routing (US-0086)

Manual and automation modes are intentionally separate:

- Manual mode (`AUTO_REMOTE_AUTOMATION_PROFILE=off`) keeps local-first behavior.
  No automatic remote routing is allowed, and `TEST_COMMAND` is never silently
  rerouted to remote targets.
- Automation mode (`AUTO_REMOTE_AUTOMATION_PROFILE=deterministic_v1`) may route
  to Docker/SSH/local targets using deterministic precedence.
- Explicit NL intent literal is constrained to `start container <target_id>`.
  Unknown or disabled targets fail closed.

Deterministic fail-closed reason codes:

- `REMOTE_AUTOMATION_MODE_OFF`
- `REMOTE_TARGET_UNKNOWN`
- `REMOTE_TARGET_DISABLED`
- `REMOTE_TARGET_UNROUTABLE`

Security continuity (`US-0085` / `DEC-0071`) remains mandatory in all modes:

- Never read `.env` from agent automation.
- Never print secret values in command output, logs, handoffs, or state.
- Names-only evidence format is required (`secret_surface=names_only`).

### Remote-routing evidence tuple (execute/qa/release)

When automation routing is used, include this tuple in handoffs/state artifacts:

- `target_id`
- `environment_label`
- `automation_profile`
- `routing_source` (`explicit_intent|heuristic_fallback|local_default`)
- `secret_surface=names_only`

If routing is not used (mode off/local default), still record:

- `target_id=local-default`
- `environment_label=local`
- `automation_profile=off`
- `routing_source=local_default`
- `secret_surface=names_only`

### Published npm `installer.sh` / POSIX dash (US-0084)

- **Symptom**: `set: Illegal option -` on an early line when running `its-magic` or
  `sh installer.sh` on Debian/Ubuntu (**`/bin/sh`** → **dash**).
- **Common causes**: bash-only `set` options (`pipefail`, `-o errexit`, `-u` bundles)
  on the **unconditional** startup path, or **CRLF** line endings in the file that
  ships from npm.
- **`sh` vs `bash`**: the Unix CLI path uses **`sh` + `installer.sh`** (**BUG-0004** /
  **DEC-0068**). Do not assume bash for the first lines of **`installer.sh`**.
- **Remediation**:
  - Upgrade to an **its-magic** build that includes **US-0084** (LF + POSIX guards).
  - Normalize to **LF** only (e.g. `dos2unix installer.sh`, or fix checkout —
    root **`.gitattributes`** uses `*.sh text eol=lf`).
  - Reinstall from npm after verifying maintainer gates:
    `python scripts/guard_installer_publish.py` (also **`npm run guard:installer`**
    / **`prepublishOnly`**).
- **Normative**: **`docs/engineering/architecture.md`** **`# US-0084`**.

### Automated checks (US-0084)

- `python tests/installer_shell_bug0004_test.py` — CR/LF rejection, forbidden
  `set` tokens, optional **`dash -n`** when **`dash`** is on **`PATH`**.
- `python scripts/guard_installer_publish.py` — same checks for publish/CI
  (**`prepublishOnly`**).
- `python scripts/remote_config_summary.py` — with **`REMOTE_EXECUTION=1`**,
  read-only summary of **`REMOTE_CONFIG`** (default **`.cursor/remote.json`**);
  stdout is **names-only** (no secret values). **`DEC-0070`**: when
  **`REMOTE_EXECUTION=0`**, the helper exits **0** and skips validation
  (stderr skip reason).

### Optional deterministic CI routing recipe (US-0086)

Use this only when CI needs explicit remote-target hints; keep it opt-in.

1. Define explicit path filters:
   - container surfaces: `Dockerfile*`, `docker-compose*.yml`, container scripts
   - ssh/runtime infra surfaces: deployment ssh scripts, host runtime scripts
2. Route using explicit matrix labels (`local`, `docker`, `ssh`) with no
   implicit fallback logic outside documented defaults.
3. Keep manual mode unchanged: if `AUTO_REMOTE_AUTOMATION_PROFILE=off`, run
   local path and do not apply remote routing.
4. Emit names-only evidence (`target_id`, `environment_label`,
   `automation_profile`, `routing_source`, `secret_surface=names_only`) into
   CI logs/artifacts.

## Runtime QA autopilot contract (US-0065 / DEC-0047)

Generated-project validation requires runtime proof, not static checks alone.

Mandatory runtime stage order:

`startup -> readiness/connectivity -> log scan -> bounded retry -> verdict`

Deterministic runtime failure reason codes:

- `RUNTIME_STARTUP_FAILED`
- `RUNTIME_ENDPOINT_UNREACHABLE`
- `RUNTIME_LOG_CRITICAL_DETECTED`
- `RUNTIME_RETRY_BUDGET_EXHAUSTED`
- `RUNTIME_STACK_PROFILE_UNRESOLVED`

Runtime evidence schema (record in QA findings):

- `runtime_startup_command`
- `runtime_stack_profile` (`node|python|go|java|dotnet`)
- `runtime_mode` (`local|remote`)
- `runtime_health_target`
- `runtime_health_result`
- `runtime_log_summary` (severity counts and key error signals)
- `runtime_retry_count`
- `runtime_retry_ledger` (`attempt`, `delay_ms`, `outcome`)
- `runtime_final_verdict`
- `runtime_reason_code`
- `runtime_evidence_refs`

Bounded retry policy:

- retry only transient startup/connectivity failures
- enforce configured max-attempt cap (`attempt <= max`)
- fail fast on non-transient critical runtime log signals

Stack/profile resolution:

- Minimum supported runtime profiles: Node, Python, Go, Java, .NET.
- Unknown or ambiguous profile must fail closed with
  `RUNTIME_STACK_PROFILE_UNRESOLVED`.

Webapp verification path (when applicable):

- include browser-surface load validation
- capture console error summary and failed network request summary
- add these signals to `runtime_log_summary` and evidence refs

Optional debug escalation (bounded):

- use for reproducible runtime failures only
- keep instrumentation bounded and reversible
- record applied debug steps and explicit cleanup confirmation

## Generated test scaffolding + auto-run contract (US-0066 / DEC-0048)

Generated app projects require deterministic baseline test scaffolding and
automatic QA test execution evidence.

Detection/profile contract:

- Resolve one deterministic stack profile from:
  `node|python|go|java|dotnet` (minimum supported).
- If profile cannot be resolved, fail closed with
  `TEST_SCAFFOLD_STACK_UNRESOLVED`.
- If detected stack is outside supported baseline set, fail closed with
  `TEST_SCAFFOLD_UNSUPPORTED_STACK`.

Generation contract (`/execute`):

- Generate only missing baseline assets for:
  - unit tests
  - integration tests
  - acceptance tests
- Use stable scaffold paths so reruns are idempotent (no duplicate file churn).
- Record generated paths and actions in execution evidence.
- If generation fails, fail closed with `TEST_SCAFFOLD_GENERATION_FAILED`.

Runbook command wiring:

- `TEST_COMMAND` baseline is stack-aware and deterministic.
- Non-destructive precedence is mandatory:
  - preserve user-authored non-empty `TEST_COMMAND`,
  - write baseline command only when `TEST_COMMAND` is missing/unset.

QA auto-run evidence contract (`/qa`):

- Execute generated baseline tests automatically.
- Record evidence fields:
  - `generated_test_stack_profile`
  - `generated_test_command`
  - `generated_test_result`
  - `generated_test_output_ref`
  - `generated_test_paths_ref`
  - `generated_test_reason_code`

Runtime boundary with US-0065:

- Generated static test PASS is required but never sufficient for QA PASS.
- Runtime-autopilot verdict remains mandatory; non-starting apps cannot PASS QA.

## Auto continuation resume contract

`/auto` continuation uses deterministic phase resolution (DEC-0017):

1. explicit `/auto start-from=<phase>`
2. `handoffs/resume_brief.md`
3. conservative `docs/engineering/state.md` fallback
4. fail-fast

Canonical `start-from` phase IDs:
`intake`, `discovery`, `research`, `architecture`, `sprint-plan`,
`plan-verify`, `execute`, `qa`, `verify-work`, `release`, `refresh-context`.

Conflict and stale-source policy:
- Explicit valid override wins.
- If no override and `resume_brief` conflicts with `state`, fail fast.
- If `resume_brief` exists but is stale/unparseable, fail fast.
- Use state fallback only when `resume_brief` is absent.

Fail-fast error format:
- `[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`

Required error codes:
- `INVALID_START_FROM`
- `RESUME_BRIEF_MISSING`
- `RESUME_BRIEF_STALE`
- `RESUME_BRIEF_UNPARSEABLE`
- `RESUME_STATE_CONFLICT`
- `STATE_PHASE_AMBIGUOUS`
- `STATE_PHASE_UNRECOVERABLE`

Breadcrumbs required for inspectability:
- `resolution_source`, `resolved_start_phase`, `stop_reason`, `stop_phase`,
  `timestamp`.
- Record in `docs/engineering/state.md`; update `handoffs/resume_brief.md` when
  auto stops before completion.

Stop-condition preservation:
- continuation does not bypass decision gates, missing-input blockers,
  pause requests, or loop max cycle limits.

## Per-phase subagent isolation evidence (US-0048 / DEC-0029)

Per-phase fresh-context isolation is enforced with auditable, fail-closed
evidence.

### Canonical evidence store and locations

- Canonical evidence store: `docs/engineering/state.md` (append-only checkpoints).
- Cross-references are allowed in phase artifacts and handoffs:
  - `handoffs/dev_to_qa.md`, `handoffs/qa_to_dev.md`
  - `handoffs/resume_brief.md` (pause/resume provenance)
  - `sprints/Sxxxx/summary.md`, `sprints/Sxxxx/qa-findings.md`, `sprints/Sxxxx/uat.*`,
    `sprints/Sxxxx/release-findings.md`

### Required schema (one entry per phase run)

Each phase run must append an isolation evidence entry containing:

- `phase_id`: canonical phase id (`intake|discovery|research|architecture|sprint-plan|plan-verify|execute|qa|verify-work|release|refresh-context|pause|resume`)
- `role`: subagent role executing the phase (`po|curator|tech-lead|dev|qa|release|security`)
- `fresh_context_marker`: a marker unique to the fresh subagent context for this phase run
- `timestamp`: ISO UTC timestamp
- `evidence_ref`: canonical path to the primary artifact written/validated for the phase run

### Gate behavior (fail closed)

- Missing evidence blocks progression with `PHASE_CONTEXT_ISOLATION_MISSING`.
- Invalid schema/fields blocks progression with `ISOLATION_EVIDENCE_INVALID`.
- Stale evidence (reused marker across runs or older than the resumed boundary)
  blocks progression with `ISOLATION_EVIDENCE_STALE`.
- Orchestrator executing phase work without spawning a fresh subagent context is
  a hard violation: `PHASE_CONTEXT_ISOLATION_VIOLATION`.

Remediation (all cases): re-run the affected phase in a fresh subagent context
and write new isolation evidence before proceeding.

### Reason codes and remediation (US-0048)

- `PHASE_CONTEXT_ISOLATION_MISSING`: no isolation evidence entry found for a
  required phase run. Fix: rerun the phase in a fresh subagent and append the
  required evidence fields.
- `ISOLATION_EVIDENCE_INVALID`: evidence entry present but missing required
  fields or contains invalid `phase_id`/`role`. Fix: rerun the phase and write a
  corrected entry.
- `ISOLATION_EVIDENCE_STALE`: evidence is reused across runs/cycles or predates
  the latest resume boundary. Fix: rerun the phase and write a new
  `fresh_context_marker`.
- `PHASE_CONTEXT_ISOLATION_VIOLATION`: phase work was performed without a fresh
  subagent context (for example orchestrator performed phase writes). Fix: stop,
  revert unsafe artifacts if needed, rerun the phase correctly, and ensure
  orchestration-only behavior.

## Strict runtime proof contract (US-0056 / DEC-0038)

Strict runtime proof augments artifact-level isolation evidence. `/auto`,
`/verify-work`, and `/release` must validate runtime attestation tuples at phase
boundaries before continuation/finalization.

Required runtime attestation tuple fields:

- `orchestrator_run_id`
- `runtime_proof_id` (unique per phase run)
- `phase_id`
- `role`
- `proof_issued_at` (ISO UTC / RFC3339)
- `proof_ttl_seconds`
- `proof_hash`

Deterministic fail-closed reason codes:

- `RUNTIME_PROOF_MISSING`
- `RUNTIME_PROOF_INVALID`
- `RUNTIME_PROOF_REUSED`
- `RUNTIME_PROOF_STALE`
- `RUNTIME_PROOF_AMBIGUOUS_LINK`

Boundary behavior:

- Missing/invalid/reused/stale/ambiguous runtime proof blocks progression.
- Release finalization must consume strict runtime proof in addition to existing
  isolation evidence checks.
- Pause/resume provenance must reference latest valid strict-proof boundary.

## Strict `/auto` phase→role enforcement (US-0069 / DEC-0051)

`/auto` must treat phase roles as a **fail-closed admission and checkpoint
contract** (see `decisions/DEC-0051.md` and `/auto` command text).

### Canonical matrix and scratchpad alternates

- Fixed phase→role defaults are documented in `/auto` (for example `execute` →
  `dev`, `release` → `release`).
- Alternate phases resolve **one** expected role via scratchpad:
  - `AUTO_ROLE_RESEARCH`: `po` \| `tech-lead` (empty → default `tech-lead`)
  - `AUTO_ROLE_PLAN_VERIFY`: `qa` \| `tech-lead` (empty → default `qa`)
  - `AUTO_ROLE_REFRESH_CONTEXT`: `curator` \| `po` (empty → default `curator`)
- Non-empty values outside the allowed set fail closed (no unrelated-role
  substitution).

### Preflight and checkpoints

- **Preflight (before spawn)**: resolve expected role; verify the required
  subagent capability exists. Missing capability → `PHASE_ROLE_CAPABILITY_MISSING`
  with `phase_id`, expected role, observed result, remediation. Do not spawn a
  substitute role.
- **Post-completion**: isolation evidence `role` and strict-proof `role` must
  both match the same preflight-resolved role; else `PHASE_ROLE_MISMATCH`.
- **`proof_hash`**: SHA-256 over sorted-key JSON of the strict-proof tuple fields
  (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`,
  `proof_issued_at`, `proof_ttl_seconds`).

### Execute default deny and rare override

- Default: `execute` requires `dev`.
- Override allowed only when **both** hold:
  `AUTO_EXECUTE_ROLE_OVERRIDE=allowed_non_dev_execute` and
  `EXECUTE_OVERRIDE_GOVERNANCE_REF` references a parseable approved exception (for
  example `DEC-xxxx` or a documented state anchor).

### Continuation parity

- Every `/auto` run recomputes role policy and preflight; `start-from`, fresh
  `resume_brief`, and `state.md` fallback cannot bypass the gate with stale role
  intent alone.

## Configurable `/auto` phase plan (US-0070 / DEC-0052)

`/auto` schedules a **resolved ordered phase plan** from merged scratchpad
before any spawn. See `decisions/DEC-0052.md` and `/auto` command text.

### Selectors (exactly one active mode)

- `AUTO_PHASE_PLAN=full` (default when unset and no other selector is set)
- `AUTO_PHASE_EXCLUDE=<csv>` — remove listed canonical phase ids from `full`
- `AUTO_PHASE_INCLUDE=<csv>` — only listed ids, re-sorted into canonical lifecycle order
- `AUTO_PHASE_PROFILE=<name>` — expand a named profile (unknown → fail closed)
- `AUTO_PHASE_HIGH_RISK_ACK=<token>` — required when a documented high-risk profile demands acknowledgment

Conflicting selectors → `PHASE_POLICY_CONFLICT` (no plan materialization).

### Materialization and gates

- Expand → apply **non-skippable reinstatement** (`qa`, `verify-work`, `release`,
  plus evidence-chain closure per `/auto`) → intersect **`start-from` / resume
  anchor** with the plan → **empty intersection** →
  `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`.
- Record `resolved_phase_plan`, `skipped_phases` (+ reasons such as
  `policy_exclude`, `non_skippable_gate`), and **phase boundary status** entries
  in continuation breadcrumbs (`docs/engineering/state.md`).
- **Backlog-drain**, **bulk execute**, and **team scope** paths must **reload**
  scratchpad phase-selection inputs and **recompute** the plan at each bounded
  boundary (no silent revival of omitted phases).

### Failure codes (deterministic)

- `PHASE_POLICY_CONFLICT`
- `PHASE_PLAN_UNKNOWN_PHASE`
- `PHASE_PLAN_EMPTY_INCLUDE`
- `PHASE_PLAN_UNKNOWN_PROFILE`
- `PHASE_PLAN_INVALID_AUTO_PHASE_PLAN`
- `PHASE_PLAN_HIGH_RISK_ACK_REQUIRED`
- `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION`

## Optional backlog-drain auto mode (US-0044)

`/auto` can optionally continue across multiple planned stories when explicitly
enabled in scratchpad.

Controls:
- `AUTO_BACKLOG_DRAIN=0|1` (default `0`)
- `AUTO_BACKLOG_MAX_STORIES=<n>` (default `1`)
- `AUTO_BACKLOG_ON_BLOCK=stop|skip` (default `stop`)
- `AUTO_STORY_SELECTION=priority_then_backlog_order` (default)

Semantics:
- With `AUTO_BACKLOG_DRAIN=0`, keep current single-segment continuation behavior.
- With `AUTO_BACKLOG_DRAIN=1`, select next eligible OPEN story
  deterministically and run full lifecycle story-by-story until bounded limit,
  no eligible stories, or a mandatory stop condition.
- Decision gates remain mandatory and pause progression until user decision.

## Targeted bug auto drain (US-0087)

Use **`/auto`** with an explicit **OPEN** bug binding when you want defect-scoped
continuation instead of story **`AUTO_BACKLOG_DRAIN`**.

**Canonical argv** (exact literals; no aliases in v1):

- **`bug-target=BUG-####`** — single **OPEN** bug from **`docs/product/backlog.md`**
  **`## Bug issues (canonical)`** (example: **`bug-target=BUG-0007`**).
- **`bug-target=all-open`** — walk all **OPEN** bugs in ascending **numeric**
  **`BUG-####`** order (optional per-run cap: **`AUTO_BUG_MAX_ITEMS`**).

**Scratchpad** (merged; default-off — see **`.cursor/scratchpad.md`** and
**`template/.cursor/scratchpad.local.example.md`**):

- **`AUTO_BUG_QUEUE`**, **`AUTO_BUG_TARGET`**, **`AUTO_BUG_MAX_ITEMS`**, **`AUTO_BUG_ON_BLOCK`**

**Mutex**: do **not** enable **`AUTO_BACKLOG_DRAIN=1`** and **`AUTO_BUG_QUEUE=1`**
together **without** an explicit **`bug-target=`** argv on that invocation — fail
closed **`AUTO_SCHEDULER_CONFLICT`**. Supply **`bug-target=`** to select the bug
scheduler for that run (normative detail: **`docs/engineering/auto-orchestration-reference.md`**
**Optional bug-queue mode (US-0087)** and **`docs/engineering/architecture.md`**
**`# US-0087`**).

**Fail-closed codes**: **`AUTO_BUG_QUEUE_EMPTY`**, **`AUTO_BUG_TARGET_UNKNOWN`**,
**`AUTO_BUG_TARGET_NOT_OPEN`**, **`AUTO_SCHEDULER_CONFLICT`** — plus spawn-only
orchestrator rules (**`BUG-0006`**, **`US-0069`**, **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**;
see **`.cursor/commands/auto.md`**).

## Continuous `/auto` + backlog drain (US-0088)

**Goal:** a single `/auto` run (or documented equivalent outer driver) advances
through all intersected lifecycle phases until a deterministic stop, and
`AUTO_BACKLOG_DRAIN=1` can continue across multiple OPEN stories without routine
operator chatter.

### Quick start

```
/auto                                       # full lifecycle, single story
/auto start-from=execute                    # resume from execute phase
```

With backlog drain enabled (`.cursor/scratchpad.md`):

```
AUTO_BACKLOG_DRAIN=1
AUTO_BACKLOG_MAX_STORIES=5
AUTO_BACKLOG_ON_BLOCK=stop
```

### Normative reference

Multi-phase iteration lives in
**`docs/engineering/auto-orchestration-reference.md`** **`## Steps`** item 5
(cross-anchor: **"reference Step 5"**). The compact steps in
**`.cursor/commands/auto.md`** point to that block unambiguously.

### Caps and safety guards

| Control | Default | Purpose |
|---------|---------|---------|
| `AUTO_BACKLOG_MAX_STORIES` | `1` | Max stories per drain run |
| `AUTO_LOOP_MAX_CYCLES` | `5` | Max execute-QA cycles per story |
| `AUTO_PAUSE_REQUEST` | `0` | Set to `1` to request graceful stop at next safe boundary |
| `AUTO_PAUSE_POLICY` | `after_phase` | Stop boundary granularity |

### Decision gates

Decision gates are **never** suppressed — even when `AUTO_QUIET=1`. When a gate
fires, the run stops and waits for operator resolution before continuing.

### `AUTO_QUIET` (default off)

Set `AUTO_QUIET=1` in `.cursor/scratchpad.md` to suppress **routine** per-phase
success chatter. Non-suppressible notifications:

- `decision_gate`
- Errors / `missing_input`
- `pause_request`
- `loop_max`
- `blocked`
- Segment handoff / drain advance

`AUTO_QUIET` is **orthogonal** to `TOKEN_PROFILE` (**DEC-0035** / **US-0080**):
`TOKEN_PROFILE` controls context breadth and token cost, not notification policy.

Under **`full_autonomy`** IDE native chain (**US-0095**), drain advance suppresses
routine prose when **`AUTO_QUIET=1`** but **must not** emit mandatory outer-driver
wait instructions between segments.

### Native in-chat auto-chain (US-0095)

**Primary IDE recipe** for hands-off delivery when **`AUTO_FLOW_MODE=full_autonomy`**
(default-off): run **`/auto` once in Cursor** — orchestrator self-chains in-chat
across phases and drain segments via **foreground sequential** Task loop in the
**same /auto orchestrator session**.

#### Enable and run (IDE primary)

1. Set in merged scratchpad:
   - `AUTO_FLOW_MODE=full_autonomy`
   - Optional: `AUTO_BACKLOG_DRAIN=1`, caps (`AUTO_LOOP_MAX_CYCLES`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BLOCK_RETRY_MAX`)
2. Run **`/auto`** once in Cursor Agent panel (no `--invoke-cmd`).
3. Orchestrator continues in-chat until hard stop, drain budget exhausted, or
   **`NATIVE_CHAIN_UNAVAILABLE`** (optional fallback: outer driver below).

Normative detail: **`.cursor/commands/auto.md`** § **Native in-chat auto-chain (US-0095)**
and **`docs/engineering/auto-orchestration-reference.md`** § **Native in-chat auto-chain**.

#### Primary / fallback boundary

| Context | Native in-chat chain | Outer driver | Messaging |
|---------|---------------------|--------------|-----------|
| **Cursor IDE + `full_autonomy`** | **Primary** | **Optional fallback** | No mandatory outer-driver drain recipe |
| **Headless / CI** | Unavailable | **Recommended** | Runbook: headless primary |
| **`--invoke-cmd`** | N/A | **Required** bridge | Document in runbook |
| **`NATIVE_CHAIN_UNAVAILABLE`** | Stops | Suggested (**optional** tone) | Non-suppressible |

### BUG-0012 regression verify

Multi-segment operator E2E recipe — validates native-chain orchestrator compliance
(**DEC-0081**) after **US-0095** contract delivery.

1. **Scratchpad**: set **`AUTO_FLOW_MODE=full_autonomy`**, **`AUTO_BACKLOG_DRAIN=1`**,
   **`AUTO_BACKLOG_MAX_STORIES≥2`**, **`AUTO_QUIET=1`** in merged `.cursor/scratchpad.md`.
2. **Backlog**: ensure **≥2 OPEN stories** in `docs/product/backlog.md`.
3. **Invoke**: run **`/auto`** once in Cursor IDE Agent panel (no `--invoke-cmd`).
4. **Complete segment A**: let orchestration finish **story A** through **`refresh-context`**.
5. **Pass criteria**: orchestrator drain-advances to **story B** first phase **without**
   operator re-**`/auto`** and **without** forbidden terminal prose (no mandatory
   `re-run /auto`, no mandatory outer driver, no `segment exhausted` terminal when
   continuation pending).
6. **Evidence**: `docs/engineering/state.md` segment boundary shows
   **`drain_advance_action=spawned`**, **`native_chain_continuing=true`**;
   `handoffs/resume_brief.md` top pointer advances **`story_id`** to story B.

Normative detail: **`.cursor/commands/auto.md`** § **Orchestrator post-subagent continuation
mandate (BUG-0012)** and architecture **`# BUG-0012`**.

### Scratchpad example parity

Verifies `template/.cursor/scratchpad.local.example.md` stays byte-identical with canonical `.cursor/scratchpad.md`:

- **Single-source-of-truth**: canonical is `.cursor/scratchpad.md`; template example is the consumer-shipped packaged copy.
- **Sync procedure**: copy canonical `.cursor/scratchpad.md` to `template/.cursor/scratchpad.local.example.md`, preserving the example-only header (first 5 lines) and excluding project-local override section (consumer-specific `#MODEL_TIER_*`, `# Per-phase tier overrides for this project`, etc.).
- **Verification**: `pytest tests/scratchpad_example_parity_test.py -v`
- **Installer contract**: `installer.py materialize_scratchpad_example()` reads from `template/.cursor/scratchpad.local.example.md` on every install/upgrade, ensuring consumers get the latest framework defaults without overwriting their personal overrides in `.cursor/scratchpad.local.md`.

### Full-autonomy outer driver (US-0092) — fallback

Opt-in **`AUTO_FLOW_MODE=full_autonomy`** (exact literal, default-off) also enables
the shipped stdlib outer driver as **optional** / **fallback** for headless/CI or
when native in-chat chain is unavailable. Spawn-only preserved — the driver loops hook
invocations; it never performs phase-role work. **Not required** for IDE drain.

#### Enable and run (headless/CI fallback)

1. Set in merged scratchpad (`.cursor/scratchpad.md` + optional local overrides):
   - `AUTO_FLOW_MODE=full_autonomy`
   - Optional: `AUTO_BACKLOG_DRAIN=1`, `AUTO_BUG_QUEUE=1` (scheduler mutex per US-0087)
   - Caps: `AUTO_LOOP_MAX_CYCLES`, `AUTO_BACKLOG_MAX_STORIES`, `AUTO_BLOCK_RETRY_MAX` (default `3`)
   - Optional: `AUTO_OUTER_DRIVER_TIMEOUT_SECONDS` (unset = no timeout)
2. Run once: `python scripts/auto_outer_driver.py --repo .`
3. Interpret exit code (driver prints reason tokens on stderr):

| Exit | Meaning |
|------|---------|
| **0** | `completed` — segment/portfolio terminal per policy |
| **1** | Hard stop — `decision_gate`, unrecoverable `error`, isolation/strict-proof, security deny |
| **2** | Configuration — `AUTO_FLOW_MODE` not `full_autonomy` (`AUTO_FLOW_MODE_NOT_FULL_AUTONOMY`) |
| **3** | `loop_max` — `AUTO_LOOP_MAX_CYCLES` exhausted |
| **4** | `BACKLOG_MAX_STORIES_REACHED` / drain cap |
| **5** | `pause_request` / `AUTO_PAUSE_REQUEST` |
| **6** | `BLOCK_RETRY_CAP_EXHAUSTED` |
| **124** | Hook/subprocess timeout |

`--dry-run` emits planned `/auto` hook invocations and drain-advance scheduling
without side effects. `--invoke-cmd` overrides the default normative `/auto …` line.

#### Security (US-0092 / DEC-0078)

- **No** auto-read **`.env`** or secret paths.
- **No** intake evidence mutation under automation.
- **No** publish without **`RELEASE_PUBLISH_MODE=auto`** (explicit opt-in; default-off).
- Block-retry ledger **`handoffs/auto_block_retry/<orchestrator_run_id>.jsonl`** is
  names-only — no secrets, no file contents.

UAT self-verify: **`scripts/uat_probe_lib.py`** shared by **`/verify-work`** and **`/qa`**.

### Browser UAT self-test (US-0093)

Enable Cursor browser-integrated UAT probes for web acceptance steps (**DEC-0079**).

#### Scratchpad keys

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `UAT_BROWSER_PROBE_MODE` | `cursor` \| `http_fallback` \| `playwright_fallback` | `cursor` | Primary probe path |
| `UAT_BROWSER_FALLBACK_CHAIN` | `0` \| `1` | `1` | HTTP → Playwright after MCP unavailable |
| `UAT_PROCESS_HEALTH_POLL_SECONDS` | int | `60` | Readiness poll cap |
| `UAT_PROCESS_HEALTH_POLL_INTERVAL_SECONDS` | int | `2` | Poll interval |
| `DEV_SERVER_PORT` | int | unset | Port override |
| `DEV_SERVER_COMMAND` | command | unset | Startup override |

Orthogonal to **`PERMISSION_MODE`** and Cursor browser approval modes. Health URLs from
**`docs/engineering/runtime-connectivity.md`** first.

#### CI recipe

Set **`UAT_BROWSER_PROBE_MODE=http_fallback`** in CI — never false PASS without agent evidence.

#### Evidence layout

Binary artifacts under **`sprints/Sxxxx/evidence/browser/`** (gitignored OK). JSON carries path
refs only. Validate agent write-back:
`python scripts/uat_probe_lib.py --merge-result sprints/Sxxxx/evidence/browser/fragment.json`.

#### Manual override

Use **`@browser`** in Agent panel or invoke browser tools manually when MCP sequence needs operator
approval for production-like targets.

### Caveman mode (US-0089)

Optional response-side terse / imperative assistant voice. **Default off.**
When `CAVEMAN_MODE=0` (or absent), this mode adds **zero** behavioral change
and the assistant responds exactly as it did pre-US-0089. Full contract:
**DEC-0072** + `docs/engineering/architecture.md` `# US-0089` +
`.cursor/rules/caveman.mdc`.

Non-substitution with `TOKEN_PROFILE`:

`TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls reply voice. Neither substitutes for the other; setting one does not change the other. Combine freely.

#### Scratchpad keys

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `CAVEMAN_MODE` | `0` \| `1` | `0` | `0` = pre-US-0089 behavior. `1` = voice rule active. Absence = `0`. |
| `CAVEMAN_LEVEL` | `lite` \| `full` \| `ultra` or empty | empty | With `MODE=0`: inert. With `MODE=1` and empty: treat as `full`. Unknown value → `CAVEMAN_LEVEL_UNKNOWN` (fail closed; fall back to pre-US-0089 voice while continuing the turn). |
| `CAVEMAN_COMPRESS_INPUT` | `0` \| `1` | `0` | **Reserved for US-0090.** Documented no-op in US-0089. |
| `CAVEMAN_FILE_SCOPE` | string | empty | **Reserved for US-0090.** Documented no-op in US-0089. |

#### Canonical operator toggle phrases

| Phrase | Effect |
|--------|--------|
| `caveman on` | Enable Caveman voice for the session (overlay). Effective from the next assistant turn. |
| `caveman off` | Disable Caveman voice for the session (overlay). Effective from the next assistant turn. |
| `stop caveman` | Alias for `caveman off`. |
| `normal mode` | Alias for `caveman off`. |
| `caveman: lite|full|ultra` | Set level for the session (implies `caveman on`). Effective from the next assistant turn. Accepts the three literal tokens `caveman: lite`, `caveman: full`, `caveman: ultra`. |

#### Determinism semantics

- Scratchpad `CAVEMAN_MODE` / `CAVEMAN_LEVEL` are **authoritative across
  subagent spawns**; session toggle phrases are overlays for the current
  conversation only and do NOT persist across a fresh subagent context.
- Session toggle phrases apply **as an overlay for the next assistant
  turn**; they never rewrite the current turn's machine-verifiable
  artifacts (gate messages, reason codes, strict-proof tuples, isolation
  evidence fields).
- Within a session, the **last explicit toggle wins**. Ambiguous phrases
  are **not** recognized — only the literal matches in the table above.

#### Literal-region invariant (rule-enforced)

Under `CAVEMAN_MODE=1`, the 9 literal regions enumerated in
`.cursor/rules/caveman.mdc` (fenced code, paths, AC checklists, reason
codes, IDs, contract markers, strict-proof tuple fields, isolation
evidence fields, git refs) render byte-literal. The non-suppressible gate
vocabulary inherited from **US-0088** (`decision_gate`, `error`, `pause`,
`loop_max`, `blocked`, `missing input`, `[BUG_VALIDATION_OK]`,
`[INTAKE_EVIDENCE_VALIDATION_OK]`, `[SCRATCHPAD_PAIR_OK]`) also renders
byte-literal even at `CAVEMAN_LEVEL=ultra`.

#### Voice compression levels

Compact before/after examples (full contract: `.cursor/rules/caveman.mdc`):

| Scenario | Level | Before | After |
|----------|-------|--------|-------|
| Technical explain | `full` | "The spawn-only orchestrator must dispatch a fresh subagent for each phase." | "Spawn-only orchestrator dispatches fresh subagent per phase. Next: run `/execute`." |
| Destructive warning (auto-clarity break) | (pause) | "I will run `git push --force` to fix the remote." | "Destructive: `git push --force` rewrites remote history. Confirm branch and remote before proceeding." |

Normative voice-compression contract (precedence, drop rules, persistence,
9-zone deferral): **`.cursor/rules/caveman.mdc`** — `## Voice compression
(when CAVEMAN_MODE=1)`.

### Caveman input compression (US-0090)

Optional **input-side** file compression. **Default off.** Operator-initiated,
script-invoked only. Never fires autonomously. Full contract:
**DEC-0073** + `docs/engineering/architecture.md` `# US-0090` +
`scripts/caveman_compress_input.py`.

Non-substitution with `TOKEN_PROFILE` and `CAVEMAN_MODE`:

`TOKEN_PROFILE` controls context breadth. `CAVEMAN_MODE` controls reply voice. `CAVEMAN_COMPRESS_INPUT` controls input-side file compression. All three axes are orthogonal: setting one does not change the others, and none substitutes for another.

#### Activation gate (DEC-0073 §2)

All three conditions must hold before any mutation occurs:

1. `CAVEMAN_COMPRESS_INPUT=1` in `.cursor/scratchpad.md`.
2. `CAVEMAN_FILE_SCOPE` non-empty.
3. CLI invoked with `--write`.

Any failing condition short-circuits with a reason code from §7 and exit `2`.
Default / unset / partial state = no-op.

#### Sidecar originals (DEC-0073 §3)

Before mutating any file, the script writes the pre-mutation bytes to
`docs/.caveman-originals/<relative/path>/<filename>`. Atomic order: sidecar
first (temp + replace), then target (temp + replace). The tree is anchored
by `docs/.caveman-originals/.gitkeep` and excluded from VCS by the repo-root
`.gitignore` anchor for US-0090.

#### Deny-list policy (DEC-0073 §4)

Layered, read in this order (**deny always wins**):

1. Hard-coded baseline in `scripts/caveman_compress_input.py` (`DENY_BASELINE`).
2. Merged secret-like patterns from repo-root `.gitignore` (`.env*`, `*secret*`,
   `*credential*`, `*token*`, `*private*`).
3. Optional `.cursorignore` overlay when
   `CAVEMAN_COMPRESS_INGEST_CURSORIGNORE=1` in scratchpad.

Deny-list baseline is versioned via `deny_list_version` (SHA-256 of sorted
canonical JSON) and reported by `--report`.

#### Allow-list grammar (DEC-0073 §5)

Three forms in `CAVEMAN_FILE_SCOPE`:

| Form | Example | Notes |
|------|---------|-------|
| Named profile | `docs-prose-only` | Frozen v1 table; new profiles require subsequent DEC. |
| Raw CSV globs | `docs/user-guides/**/*.md,handoffs/archive/*.md` | Forward slashes only. |
| Hybrid | `profile:docs-prose-only;globs:handoffs/archive/*.md` | One profile per scope; unknown tokens fail closed. |

#### Safe-mode minifier (DEC-0073 §6)

Four-step, strictly idempotent pipeline:

1. Collapse two-or-more consecutive blank lines into a single blank line
   (outside fenced code).
2. Trim trailing whitespace on non-fence lines.
3. Normalize `CRLF` / `CR` → `LF`.
4. Preserve the source file's EOF-newline status.

Aggressive mode is **deferred**; v1 ships safe-mode only. All safe-mode
transformations keep the 9 DEC-0072 §4 literal regions byte-identical; any
drift is fail-closed with `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED`.

#### Reason-code vocabulary (DEC-0073 §7)

Nine codes in three families. No post-write codes.

| Family | Code |
|--------|------|
| Gating | `CAVEMAN_COMPRESS_MODE_DISABLED` |
| Gating | `CAVEMAN_COMPRESS_FLAG_CONFLICT` |
| Scope | `CAVEMAN_COMPRESS_SCOPE_EMPTY` |
| Scope | `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE` |
| Scope | `CAVEMAN_COMPRESS_SCOPE_VIOLATION` |
| Integrity | `CAVEMAN_COMPRESS_DENY_HIT` |
| Integrity | `CAVEMAN_COMPRESS_NOT_IDEMPOTENT` |
| Integrity | `CAVEMAN_COMPRESS_LITERAL_REGION_DAMAGED` |
| Integrity | `CAVEMAN_COMPRESS_ORIGINAL_MISSING` |

Additions require a subsequent DEC amending §7.

#### CLI contract (DEC-0073 §8)

| Flag | Semantics |
|------|-----------|
| `--dry-run` | (default) inventory + diff summary to stdout; no mutation. |
| `--write` | Perform sidecar + target mutation on eligible files (sidecar first). |
| `--verify-originals` | Walk sidecar tree; verify bidirectional presence; fail closed with `CAVEMAN_COMPRESS_ORIGINAL_MISSING` on orphan. |
| `--report` | Emit canonical JSON report on stdout (incompatible with `--write`). |

#### Scratchpad keys (US-0090 additions)

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `CAVEMAN_COMPRESS_INPUT` | `0` \| `1` | `0` | Activation gate bit (DEC-0073 §2). |
| `CAVEMAN_FILE_SCOPE` | string | empty | Profile name, CSV globs, or hybrid (§5). |
| `CAVEMAN_COMPRESS_INGEST_CURSORIGNORE` | `0` \| `1` | `0` | Optional overlay (§4). |

#### Template parity (DEC-0073 §10)

The following pairs are byte-identical between active and template copies and
installer-owned (BUG-0003 / DEC-0066): `scripts/caveman_compress_input.py`,
`docs/engineering/context/installer-owned-paths.manifest`,
`docs/engineering/runbook.md`, `docs/engineering/auto-orchestration-reference.md`.
Verify with `python scripts/check_intake_template_parity.py --scope=caveman-compress`.
Negative parity (must NOT track): `.cursor/rules/caveman.mdc` (US-0089
rule-set; US-0090 adds no new Cursor rule).

### Outer-driver equivalence (AC-1, Option B)

When a single Cursor `/auto` invocation cannot schedule multiple subagent turns,
operators may use an outer driver (script or manual re-invocation with
`start-from` / refreshed `resume_brief`). This is deterministically equivalent
when: same phase order, same isolation + strict-proof per phase, same stop
reasons, same `resume_brief` + `state.md` refresh at every boundary.

### Drain advance behavior

When `AUTO_BACKLOG_DRAIN=1` and a story reaches its terminal boundary:

1. Orchestrator reloads merged scratchpad phase-selection inputs.
2. Orchestrator recomputes the materialized phase plan for the next story.
3. Selects the next eligible OPEN story per `AUTO_STORY_SELECTION`.
4. Runs the full resolved lifecycle for that story until stop or cap.

Notify operator on segment handoff (non-routine, non-suppressible).

### Stop reasons

`completed`, `decision_gate`, `missing_input`, `pause_request`, `loop_max`,
`error`, `blocked`. See the **Deterministic stop matrix** in
**`docs/engineering/auto-orchestration-reference.md`** §
**Continuous multi-phase execution (US-0088)**.

### Troubleshooting

| Symptom | Likely cause | Fix |
|---------|-------------|-----|
| Run stops after one phase | Older `/auto` text without continuous semantics | Update to latest; verify **reference Step 5** anchor exists |
| `RESUME_BRIEF_STALE` mid-run | Brief not refreshed at phase boundary | Ensure paired `resume_brief` + `state.md` refresh per DEC-0069 |
| `AUTO_SCHEDULER_CONFLICT` | Both `AUTO_BACKLOG_DRAIN=1` and `AUTO_BUG_QUEUE=1` without `bug-target=` argv | Supply explicit `bug-target=` or disable one scheduler |
| `BACKLOG_MAX_STORIES_REACHED` | Drain cap hit | Increase `AUTO_BACKLOG_MAX_STORIES` or run another `/auto` |

### Downstream CI packaging job leak (BUG-0009 / DEC-0075)

**CI still runs its-magic packaging jobs?** Your project received a pre-fix workflow.
Run **`its-magic --target <repo> --mode upgrade`** (or **`--mode clean`** then reinstall)
to refresh `.github/workflows/ci.yml` from the corrected template. After upgrade, GitHub
Actions should show only **`checks`** and **`auto-fix`** jobs — not `npm-test`,
`brew-test`, or `choco-test`.

Scope reminder: fix applies to **new installs/upgrades**; stale repos heal on next upgrade
(**US-0018**).

## Explicit bulk sprint planning mode (US-0046)

`/sprint-plan` stays single-scope by default. Bulk planning is opt-in via
explicit argument:

- `/sprint-plan --bulk`

Deterministic controls from `.cursor/scratchpad.md`:
- `SPRINT_BULK_MAX_STORIES` (candidate OPEN stories per run)
- `SPRINT_BULK_MAX_SPRINTS` (max generated sprints per run)
- `SPRINT_BULK_SELECTION=priority_then_backlog_order`

Deterministic behavior:
- Select eligible OPEN stories by configured selection order.
- Generate one or more bounded sprint plans while preserving per-sprint sizing
  guardrails (`SPRINT_MAX_TASKS`, `SPRINT_AUTO_SPLIT`).
- Stop with explicit reason codes when bounded or blocked:
  - `SPRINT_BULK_MAX_STORIES_REACHED`
  - `SPRINT_BULK_MAX_SPRINTS_REACHED`
  - `SPRINT_BULK_NO_ELIGIBLE_STORIES`
  - `SPRINT_BULK_MISSING_ACCEPTANCE`

## Explicit bulk execute mode (US-0047)

`/auto` remains non-bulk by default. Bulk execution is explicit and can be
enabled per run (`/auto --execute-bulk`) or by scratchpad switch.

Deterministic controls:
- `AUTO_EXECUTE_BULK=0|1` (default `0`)
- `AUTO_EXECUTE_MAX_ITEMS=<n>` (default `1`)
- `AUTO_EXECUTE_ON_BLOCK=stop|skip` (default `stop`)
- `AUTO_EXECUTE_SELECTION=planned_then_priority` (default)
- `AUTO_TEAM_SCOPE_ENFORCE=0|1` (default `1`)

Execution semantics:
- Select eligible planned items deterministically.
- Preserve strict isolation:
  - fresh subagent per phase
  - fresh subagent per execute<->QA loop cycle
- Enforce bounded stop behavior:
  - `EXEC_BULK_MAX_ITEMS_REACHED`
  - `EXEC_BULK_NO_ELIGIBLE_ITEMS`
  - `EXEC_BULK_ITEM_BLOCKED_STOP`
  - `EXEC_BULK_ITEM_BLOCKED_SKIPPED`

Team mode guardrails (`TEAM_MODE=1`):
- Capture team context snapshot in breadcrumbs:
  - `TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`
- With enforcement enabled, out-of-scope tasks are never mutated and must emit:
  - `EXEC_TEAM_SCOPE_BLOCKED` (stop policy)
  - `EXEC_TEAM_SCOPE_SKIPPED` (skip policy)

## Sync policy and guarded auto-push contract (US-0038 / DEC-0018)

Sync policy controls (from `.cursor/scratchpad.md`):
- `SYNC_POLICY_MODE`: `disabled|manual|by_phase|by_milestone|custom_phase_list`
- `SYNC_CUSTOM_PHASES`: comma-separated canonical phase IDs for custom mode
- `ALLOW_AUTO_PUSH`: `0|1`
- `AUTO_PUSH_BRANCH_ALLOWLIST`: comma-separated branches/patterns

Default-safe behavior:
- Default mode is `manual` (non-auto).
- `disabled` and `manual` are near-zero-overhead modes (no auto-push attempts).
- Unset/invalid mode fails closed to `manual`.

Phase-boundary-only evaluation:
- Evaluate sync eligibility only at completed phase boundaries.
- Never evaluate during partial or in-progress work units.

Guarded auto-push eligibility (all required):
1. Boundary trigger is eligible for current mode.
2. `ALLOW_AUTO_PUSH=1`.
3. QA-first restriction passes (feature work cannot auto-push before QA pass).
4. No unresolved blocking QA findings / unresolved critical issues.
5. Branch safety passes:
   - protected/default branches denied by default,
   - allow only explicitly allowlisted branches.
6. Mandatory check chain passes.

Mandatory pre-push check chain:
1. `TEST_COMMAND` (mandatory baseline)
2. `LINT_COMMAND` (only if configured)
3. `TYPECHECK_COMMAND` (only if configured)

Rules:
- Missing `TEST_COMMAND` blocks push (`TEST_COMMAND_MISSING`).
- Failing `TEST_COMMAND` blocks push (`TEST_FAILED`).
- Timed-out `TEST_COMMAND` blocks push (`TEST_TIMEOUT`).
- Optional check failures block push when configured (`OPTIONAL_CHECK_FAILED`).
- Optional checks that are not configured must be reported as `skipped`.

Deterministic reason-code baseline:
- `SYNC_DISABLED`
- `MANUAL_MODE_NO_AUTO`
- `SYNC_TRIGGER_NOT_ELIGIBLE`
- `AUTO_PUSH_NOT_ENABLED`
- `PRE_QA_AUTOPUSH_FORBIDDEN`
- `BLOCKING_QA_FINDINGS`
- `BRANCH_NOT_ALLOWLISTED`
- `TEST_COMMAND_MISSING`
- `TEST_FAILED`
- `TEST_TIMEOUT`
- `OPTIONAL_CHECK_FAILED`
- `SYNC_PUSHED`

## Executable validate-and-push wiring (DEC-0058)

Scratchpad **`SYNC_*` / `ALLOW_AUTO_PUSH` / `AUTO_PUSH_BRANCH_ALLOWLIST`** are read from the
**merged** scratchpad only (installer merge: local → materialized baseline → example; same
precedence as installer post-install validation). **`scripts/validate-and-push.ps1`** and
**`scripts/validate-and-push.sh`** call **`python scripts/sync_push_gates.py`** for policy;
**`docs/engineering/runbook.md`** remains the sole source for **`TEST_COMMAND`** and optional
lint/typecheck commands.

**Operator rule:** changing scratchpad alone does **not** run **`git push`**. Run
**`validate-and-push`** (or CI) after an eligible boundary. For **`by_phase`**, **`by_milestone`**,
and **`custom_phase_list`**, scheduling is **operator or CI** responsibility.

**`SYNC_PHASE_BOUNDARY`:** optional environment variable (canonical phase id, case-insensitive).
When **`SYNC_POLICY_MODE=custom_phase_list`**, the variable must be set and must appear in
**`SYNC_CUSTOM_PHASES`** (comma-separated) or the script exits **`SYNC_TRIGGER_NOT_ELIGIBLE`**.

**Dry-run:** **`powershell .../validate-and-push.ps1 -DryRun`** or
**`bash scripts/validate-and-push.sh --dry-run ...`** — runs merge/policy and the runbook check
chain, then prints **`SYNC_PUSHED`** without **`git push`**.

**Branch allowlist matching (`AUTO_PUSH_BRANCH_ALLOWLIST`):** comma-separated entries; each entry
is either an exact branch name or a **`fnmatch`** pattern (for example `release/*`). An empty
allowlist denies every branch (**`BRANCH_NOT_ALLOWLISTED`**).

**QA scan (bounded):** files under **`sprints/S####/qa-findings.md`** (four digits). Blocking
rules match **`DEC-0058`** §6. **`PRE_QA_AUTOPUSH_FORBIDDEN`** applies on branches other than
**`main`** / **`master`** when **no** such **`qa-findings.md`** file exists yet (feature-line
signal; see architecture **US-0076**).

**Python:** merged policy evaluation requires **Python 3** on **`PATH`** (**`PYTHON_NOT_ON_PATH`**
if missing).

Required sync evidence fields:
- `phase_boundary`
- `policy_mode`
- `trigger_source` (`manual|auto`)
- `branch`
- `checks` (`test|lint|typecheck`: `pass|fail|skipped`)
- `qa_status_snapshot`
- `push_decision` (`pushed|blocked|not_eligible`)
- `reason_code`
- `evidence_refs`

## Release gate chain (US-0039 / DEC-0019)

Deterministic mandatory gate order; no step may be skipped or reordered:

1. **Check-in test gate** — Latest `TEST_COMMAND` evidence must be present and passing.
2. **QA completion gate** — No unresolved blocking findings in sprint QA context.
3. **UAT completion gate** — UAT artifacts populated and verified; no placeholder or unresolved-fail state.
4. **Isolation compliance gate** — Per-phase isolation evidence present and valid (US-0048 / DEC-0029).
5. **Release finalization** — Notes, queue, backlog/runbook/state updates only after gates 1–4 pass.

Default: no bypass. Override only via explicit decision gate with rationale and evidence (DEC-0019).

**Optional-command compatibility (US-0039 / AC-10)**: Blank optional runbook keys (`LINT_COMMAND`, `TYPECHECK_COMMAND`) must not cause release to fail. Mandatory gates are check-in test + QA + UAT + isolation only; optional checks run only when configured and are reported as `skipped` when not configured. Release does not require lint/typecheck evidence when those keys are blank.

**Per-gate audit verdict schema (US-0039)** — For TL/QA auditability, record per gate:

- `gate` (check-in_test | qa | uat | isolation | finalization)
- `verdict` (pass | fail | override)
- `reason_code` (e.g. RELEASE_TEST_FAILED, RELEASE_QA_BLOCKERS_OPEN, RELEASE_UAT_INCOMPLETE, RELEASE_GATE_OVERRIDE_APPROVED)
- `remediation` (short remediation steps when fail/override)
- `evidence_refs` (paths to tests/report.md, qa-findings.md, uat.json, release-findings.md, DEC-xxxx as applicable)

Record in `sprints/Sxxxx/release-findings.md` and/or `handoffs/release_queue.md` `gate_snapshot`; state checkpoint in `docs/engineering/state.md` may reference the same.

## Release queue and sprint notes contract (US-0040 / DEC-0020)

Canonical release artifacts:
- `handoffs/releases/Sxxxx-release-notes.md` (canonical per-sprint notes)
- `handoffs/release_queue.md` (canonical queue tracker)
- `handoffs/release_notes.md` (legacy-compatible latest pointer/summary)

Queue row required fields:
- `sprint_id`
- `story_refs`
- `status` (`planned|ready|unreleased|released|blocked`)
- `last_updated`
- `release_notes_ref`
- `gate_snapshot`
- `release_version` (optional before finalization)

Deterministic transition semantics:
- target sprint only may change during one `/release` run
- entering release flow sets target row to `unreleased`
- successful finalization transitions same row to `released`
- no non-target sprint row mutation

Fail-safe reason codes:
- `RELEASE_SPRINT_UNRESOLVED`
- `LEGACY_NOTES_SPRINT_UNRESOLVED`
- `QUEUE_ENTRY_MISSING`
- `NOTES_REF_MISSING`
- `STATUS_TRANSITION_INVALID`

Mismatch and unresolved-sprint policy:
- fail closed for finalization when sprint identity or queue/notes metadata is
  inconsistent
- preserve existing notes artifacts by default (non-destructive)
- do not auto-reconcile by deleting/rebuilding unrelated sprint history
- include remediation steps in queue/state and rerun `/release` after correction

## Post-QA release issue workflow (US-0042)

When `/release` finds a blocker after QA has passed, document it in a dedicated
release findings artifact (separate from QA findings):

- Canonical artifact: `sprints/Sxxxx/release-findings.md`
- Canonical handoff back to implementation: `handoffs/release_to_dev.md`

Required release-findings content:
- gate status (`PASS|BLOCKED`)
- blocking and non-blocking findings
- deterministic reason code(s)
- evidence refs
- remediation steps and rerun criteria

Boundary rule:
- QA-phase defects remain in `sprints/Sxxxx/qa-findings.md`.
- Post-QA release-gate defects must be recorded in
  `sprints/Sxxxx/release-findings.md`.

## Backlog reconciliation invariant (US-0043)

At release finalization boundary, target sprint stories must be synchronized in
`docs/product/backlog.md` using canonical release evidence precedence.

Contract:
- Scope is target sprint stories only (no global backlog mutation).
- If release evidence is PASS, set story status to `DONE` and reconcile
  acceptance checkboxes to checked state.
- If sprint is `released` but backlog story state remains contradictory
  (`OPEN`/unchecked), fail safe with reason code `BACKLOG_STATUS_DRIFT`.
- Record remediation guidance and evidence refs in release artifacts before rerun.

## Canonical status ownership and normalization guard (US-0045)

Canonical owner:
- `docs/product/backlog.md` is the authority for story status (`OPEN|DONE`).
- `docs/product/acceptance.md` and `docs/engineering/state.md` are derived views.

Deterministic reconciliation rules:
1. Read canonical story status from backlog.
2. Validate target sprint release evidence for status transitions.
3. Reconcile derived acceptance/state views from canonical backlog status.
4. Keep mutation scope target-scoped only; never broad-rewrite unrelated stories.

One-time normalization procedure:
- Run an initial normalization pass for historically drifted stories.
- Write all changed rows to `docs/engineering/status-normalization-report.md`
  including prior values, resolved values, evidence references, and timestamp.
- On future runs, append only delta entries; do not rewrite historical report rows.

Fail-safe reason codes:
- `BACKLOG_STATUS_DRIFT`: release evidence contradicts backlog/AC state.
- `CANONICAL_STATUS_CONFLICT`: canonical backlog state conflicts with derived
  status resolution at reconciliation boundary.

## Lifecycle QA matrix (US-0041)

Use this matrix to validate end-to-end installer/CLI lifecycle behavior:

| Scenario | Primary command path | Coverage location | Required evidence |
|---|---|---|---|
| Fresh install (`missing`) | `its-magic --mode missing --create` and direct installer | `tests/run-tests.ps1`, `tests/run-tests.sh` | Required files exist + `its_magic/.its-magic-version` exists |
| Overwrite + backup | `its-magic --mode overwrite --backup` and direct installer | `tests/run-tests.ps1`, `tests/run-tests.sh` | Backup snapshot contains overwritten framework file |
| Upgrade lifecycle | `its-magic --mode upgrade` and direct installer | `tests/run-tests.ps1`, `tests/run-tests.sh`, npm local tests | Framework file restored, scratchpad example refreshed, user local scratchpad preserved |
| Clean-repo safety | `its-magic --clean-repo --yes` and direct installer clean path | `tests/run-tests.ps1`, `tests/run-tests.sh`, CI lifecycle subset | Framework artifacts removed, non-framework marker preserved |
| Negative path | invalid mode/args | `tests/run-tests.ps1`, `tests/run-tests.sh` | Deterministic non-zero fail-fast behavior |
| Platform parity subset | npm/brew/choco CI jobs | `.github/workflows/ci.yml` | Lifecycle subset passes on all three runners |

## Scratchpad example upgrade contract (US-0057 / DEC-0039 / DEC-0057)

`its-magic --mode upgrade` treats `.cursor/scratchpad.local.example.md` as
framework-owned and `.cursor/scratchpad.local.md` as user-owned.

Expected deterministic outcome:
- Framework-owned example is refreshed to latest release contract **before** baseline
  materialization runs in `installer.py --scratchpad-postinstall` (**DEC-0057** ordering).
- User local scratchpad remains preserved without overwrite.
- Installer output reports manifest copy status for the example file where applicable
  (`added|updated|unchanged`) **and** `[SCRATCHPAD_LAYER]` diagnostics from post-install
  (`example_refresh`, `baseline_materialize` / `baseline_skip`, `user_local` preserved).
- CI regression: `python scripts/check-scratchpad-pair-parity.py --repo <root>` exit `0`
  when active and `template/` baseline/example pairs share the same automation `KEY=`
  set and catalog `#` headers from `# Core behavior` (**US-0075** **AC-11**).

## Scratchpad delivery Model B (US-0073 / DEC-0055)

- Install manifest ships `.cursor/scratchpad.local.example.md` (framework catalog)
  but **does not** list `.cursor/scratchpad.md` as a copied file. The installer
  **materializes** `.cursor/scratchpad.md` from the packaged template when absent
  (`missing`, `interactive`, `upgrade`) or refreshes it on `overwrite`.
- Merge precedence for automation readers: **local > materialized baseline > example**
  (same invariant as `DEC-0055`).
- Post-install validation fails closed with `[SCRATCHPAD_MERGE_ERROR]` /
  `[SCRATCHPAD_MATERIALIZE_ERROR]` when layers are missing or required keys are
  empty after merge (`US-0073` `AC-4`).
- `installer.ps1` / `installer.sh` delegate materialize+validate to
  `python installer.py --scratchpad-postinstall` (Python 3 required on PATH).
- Recovery: `python installer.py --scratchpad-postinstall --target <repo> --mode missing`
  (or re-run a full install).

## Deterministic artifact ordering and write discipline (US-0058 / DEC-0040)

Canonical policy source:
- `docs/engineering/artifact-ordering-policy.md`

Required write discipline:
- `docs/engineering/state.md`: append-bottom checkpoint writes only.
- `docs/product/backlog.md`: sorted-canonical story ordering by numeric `US-xxxx`.
- `docs/product/acceptance.md`: sorted-canonical row ordering aligned to backlog.
- Handoff surfaces use explicit policy (`prepend-top` or `append-bottom`) per
  matrix and command contract.

Fail-safe contract:
- Missing/ambiguous placement anchors fail closed with
  `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`.
- Non-monotonic `state.md` checkpoint timestamps fail closed with
  `STATE_TIMESTAMP_NON_MONOTONIC`.
- No partial mutation on fail-safe path.
- Re-run without semantic changes must be ordering-idempotent.

## Cross-phase artifact ownership guard (US-0061 / DEC-0043)

Canonical policy source:
- `docs/engineering/artifact-ownership-policy.md`

Required ownership discipline:
- Each phase may mutate only its declared owned scopes for target context.
- Cross-phase non-owned section rewrite/deletion is forbidden by default.
- `docs/engineering/architecture.md` is history-preserving: append new story
  sections or mutate target section only; unrelated story-section deletion is
  prohibited.

Fail-safe contract:
- Ownership violations fail closed with `PHASE_OWNERSHIP_VIOLATION`.
- Missing evidence on override-authorized mutation path fails closed with
  `PHASE_OVERRIDE_EVIDENCE_MISSING`.
- Architecture history deletion detection fails with
  `ARCH_HISTORY_DELETION_DETECTED`.
- No partial mutation on fail-safe path.

Execution guidance:
- Local baseline: run `sh tests/run-tests.sh` (or `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`).
- Packaging smoke: run npm local tests in `packaging/npm/`.
- CI evidence: inspect `npm-test`, `brew-test`, and `choco-test` job logs.

## Intake runtime capability and single-writer safety (US-0059 / DEC-0041)

`/intake` enforces deterministic runtime preflight and drift safety before
artifact mutation.

Capability preflight:
- Required role capability: `po` subagent.
- Default policy: fail fast when unavailable with
  `SUBAGENT_CAPABILITY_UNAVAILABLE`.
- Fallback policy is explicit only:
  - `INTAKE_SUBAGENT_FALLBACK=deny` (default): no silent fallback.
  - `INTAKE_SUBAGENT_FALLBACK=allow`: explicit operator opt-in for fallback path.

Single-writer drift safety:
- Intake run binds a deterministic writer/run identity (`writer_id`,
  `intake_run_id`) to target artifacts.
- Self-write updates for the active writer/run are valid and must not trigger
  concurrent drift blockers.
- External concurrent conflicting writes fail safe with
  `INTAKE_CONCURRENT_WRITER_DETECTED`.
- Fail-safe path performs no partial overwrite.

## Post-release operator commands (S0070 / BUG-0008 — released `2026-04-05`)

**S0070** **`released`**; **`BUG-0008`** **DONE** in canonical backlog. In-repo version **`its-magic@0.1.2-41`**. **`/release`** skipped registry publish while **`RELEASE_PUBLISH_MODE=disabled`** — operators still run the steps below when pushing to npm or validating on Debian.

- **Tests (canonical):** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` — refresh **`tests/report.md`**; release gate used **793**/0 @ **2026-04-05T20:21:40Z** with **US-0071** harness rows **PASS**.
- **Prepublish:** `npm run prepublishOnly` (runs **`guard:installer`**).
- **Publish:** `npm publish` — set **`RELEASE_PUBLISH_MODE`** to **`confirm`** or **`auto`** when ready; no inline registry secrets in docs.
- **Debian global E2E (optional follow-up):** **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`** was waived for the release cycle — when a Debian/SSH target exists (**US-0086**), run `npm install -g its-magic@0.1.2-41` (or equivalent), `cat -A` on installed `template/docs/engineering/context/installer-owned-paths.manifest` (no `^M$`), then `its-magic --target <repo> --mode missing` without `[INSTALL_MANIFEST_ERROR]`.

## Operator `.env` setup (US-0085 / DEC-0071)

### Quick start

1. Copy the committed template: `cp .env.example .env`
2. Fill in values for each variable relevant to your environment.
3. Source before remote, SSH, or release operations:
   - **Bash/Zsh**: `source .env` or `set -a; source .env; set +a`
   - **PowerShell**: `Get-Content .env | ForEach-Object { if ($_ -match '^([^#]\S+?)=(.*)$') { [Environment]::SetEnvironmentVariable($Matches[1], $Matches[2], 'Process') } }`
4. Run `python scripts/print_remote_env_hint.py` to verify parity between
   `.env.example` and the `*Env` fields in JSON configs.

### Forbidden

- **Committing `.env`**: `.env` is gitignored; never add it to version control.
- **Agents reading `.env`**: AI agents must not open, attach, read, search
  inside, or index `.env` or `.env.*` files (enforced via `.cursorignore` and
  Cursor rules). Use env var **names** in prose only.

### Allowed

- Running `ssh`, `docker`, `python scripts/remote_config_summary.py` after
  sourcing `.env` — the process inherits normal environment variables.
- Referencing env var **names** (not values) in documentation and handoffs.

## AI Decision Ledger (US-0103 / DEC-0103)

**Default-off sovereign-loop audit layer**. When `AI_DECISION_LEDGER=0` (default),
zero overhead — no files read or written. When `AI_DECISION_LEDGER=1`, every
autonomous AI deviation is recorded in an append-only JSONL ledger under
`handoffs/sovereign_decisions/<orchestrator_run_id>.jsonl`.

### Scratchpad keys

| Key | Values | Default | Behavior when off |
|-----|--------|---------|-------------------|
| `AI_DECISION_LEDGER` | `0` \| `1` | `0` | No reads / writes / schema checks. |
| `AUTO_PLAN_FIDELITY` | `strict` \| `relaxed` \| `extended` | `strict` | Active only when ledger enabled. |

Set in `.cursor/scratchpad.local.md` (gitignored) or `.cursor/scratchpad.md`.

### Enable / disable

```bash
# Enable ledger auditing
echo "AI_DECISION_LEDGER=1" >> .cursor/scratchpad.local.md

# Switch fidelity mode (relaxed allows AC drop/reorder; extended allows scope add)
echo "AUTO_PLAN_FIDELITY=relaxed" >> .cursor/scratchpad.local.md

# Disable (zero overhead)
echo "AI_DECISION_LEDGER=0" >> .cursor/scratchpad.local.md
```

### Audit ledger entries

```bash
# Validate all ledger files in handoffs/sovereign_decisions/
python scripts/ledger_validate.py --repo .

# Validate a single ledger file
python scripts/ledger_validate.py --file handoffs/sovereign_decisions/auto-20260628-01.jsonl

# Print QA findings block (JSON)
python scripts/ledger_validate.py --qa-find --orchestrator-run-id auto-20260628-01

# Validate with fail-closed enforcement
python scripts/ledger_validate.py --repo . --enforce

# Library self-test
python scripts/decision_ledger_lib.py --self-test
```

### Plan-fidelity modes

| Mode | Behavior | When to use |
|------|----------|-------------|
| `strict` | Any unapproved deviation from `resolved_phase_plan` → **`PLAN_FIDELITY_VIOLATION` hard stop**. Operator must approve override or revert. | Default. Production runs, high-risk stories. |
| `relaxed` | AI may drop/reorder existing ACs with ledger entry + QA-verifiable; new ACs/stories → `PLAN_FIDELITY_SCOPE_GATE` hard stop. | Iterative development where AC refinement is expected. |
| `extended` | AI may extend scope with new stories/features; documented non-blocking in ledger as `PLAN_FIDELITY_EXTENSION`. QA still cross-checks. | Exploratory work, prototyping, scope discovery. |

### Typical audit workflow

1. **Enable ledger** before long `/auto` run: set `AI_DECISION_LEDGER=1` in scratchpad.
2. **Run `/auto`** to completion — ledger writes accumulate in `handoffs/sovereign_decisions/<run_id>.jsonl`.
3. **Run `/qa`** — phase reads ledger, emits `ledger_findings` block in `sprints/Sxxxx/qa-findings.md` with decision counts, risk tier distribution, and fail-closed code summary.
4. **Inspect findings** — look for `violation_count > 0` (unapproved deviations) or `schema_invalid` status (corrupt ledger).
5. **Remediate or approve** — if deviations justified, set `AUTO_PLAN_FIDELITY=relaxed` or `=extended` and re-run; otherwise revert changes.

### Common failure scenarios and recovery

| Reason code | Symptom | Recovery |
|-------------|---------|----------|
| `LEDGER_FILE_MISSING` | `AI_DECISION_LEDGER=1` but no ledger file for current run | Create `handoffs/sovereign_decisions/<run_id>.jsonl` or set `AI_DECISION_LEDGER=0` |
| `LEDGER_SCHEMA_INVALID` | JSONL line fails 12-field schema validation | Open ledger, locate invalid line (validator prints line number), fix JSON syntax; if unrecoverable, truncate to last valid line |
| `LEDGER_CORRUPT` | Whole file non-UTF-8 or broken JSON | Manual repair required; consider `git restore` from prior commit or truncate to known-good prefix |
| `LEDGER_APPEND_FAILED` | Disk full, permission error, I/O error | Check disk space (`df -h`), file permissions (`ls -la handoffs/sovereign_decisions/`); retry after remediation |
| `PLAN_FIDELITY_VIOLATION` | Unapproved deviation under strict mode | Review ledger last entry; if justified, switch to `AUTO_PLAN_FIDELITY=relaxed` in scratchpad and re-run `/execute`; otherwise revert AC changes |
| `PLAN_FIDELITY_SCOPE_GATE` | New scope request under strict/relaxed mode | If scope-add intentional, switch to `AUTO_PLAN_FIDELITY=extended` and document in `sprints/Sxxxx/extension-report.md`; otherwise drop new scope |
| `LEDGER_DISABLED` | Informational — `AI_DECISION_LEDGER=0` | No action required; zero overhead when off. Opt-in via scratchpad if ledger auditing desired. |

### Parity enforcement

```bash
# Verify active ↔ template byte-parity for ledger scripts + scratchpad
python scripts/check_intake_template_parity.py --scope=sovereign-ledger
```

Pair table (`SOVEREIGN_LEDGER_PAIRS` + scratchpad):
- `scripts/decision_ledger_lib.py` ↔ `template/scripts/decision_ledger_lib.py`
- `scripts/ledger_validate.py` ↔ `template/scripts/ledger_validate.py`
- `.cursor/scratchpad.md` ↔ `template/.cursor/scratchpad.md`
- `.cursor/scratchpad.local.example.md` ↔ `template/.cursor/scratchpad.local.example.md`

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0103`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0103
- **Decision record**: `decisions/DEC-0103.md`
- **Contract tests**: `tests/us0103_contract_test.py` (8 tests)

## Goal-Based Convergence (US-0110 / DEC-0110)

**Default-off sovereign-loop terminal predicate**. When `SOVEREIGN_GOAL_MODE=phase_driven`
(default), zero overhead — no evaluation, no `goal_progress` block, no partial-delivery write.
When `goal_convergence`, `evaluate_convergence` reads composed surfaces (backlog, deferrals,
critic, smoke, ledger) and emits progress/timeout artifacts only.

### Scratchpad keys

| Key | Values | Default | Behavior when off |
|-----|--------|---------|-------------------|
| `SOVEREIGN_GOAL_MODE` | `phase_driven` \| `goal_convergence` | `phase_driven` | No evaluation side effects. |
| `SOVEREIGN_GOAL` | free-text | *(empty)* | Explicit goal wins over vision derive. |
| `SOVEREIGN_GOAL_TOP_N` | int ≥ 1 | `3` | Vision paragraph count for auto-derive. |
| `SOVEREIGN_GOAL_MAX_CHARS` | int ≥ 64 | `512` | Truncation cap for goal text. |
| `SOVEREIGN_GOAL_TIMEOUT_MAX` | int ≥ 0 | `0` | Iteration-count cap (`0` = disabled). |

### Enable / disable

```bash
# Enable goal-driven convergence
echo "SOVEREIGN_GOAL_MODE=goal_convergence" >> .cursor/scratchpad.local.md
echo "SOVEREIGN_GOAL=Ship sovereign-loop batch with zero regressions" >> .cursor/scratchpad.local.md

# Disable (zero overhead — US-0088/US-0092/US-0095/US-0044 stop matrix unchanged)
echo "SOVEREIGN_GOAL_MODE=phase_driven" >> .cursor/scratchpad.local.md
```

### Evaluate convergence

```bash
# Library self-test
python scripts/sovereign_convergence_lib.py --self-test

# Evaluate five-conjunct predicate (JSON)
python scripts/sovereign_convergence_lib.py --evaluate --repo . --orchestrator-run-id auto-20260628-04

# Dump goal_progress block
python scripts/sovereign_convergence_lib.py --dump-progress --repo . --orchestrator-run-id auto-20260628-04

# Validator self-test + schema fixtures
python scripts/sovereign_convergence_validate.py --self-test

# Validate artifacts in repo
python scripts/sovereign_convergence_validate.py --repo . --enforce
```

### Interpret `goal_progress` block

Curator **`/refresh-context`** emits a fenced JSON block under **`### goal_progress`** in
`handoffs/resume_brief.md` when `SOVEREIGN_GOAL_MODE=goal_convergence` and the sovereign loop
is active. Placement: after the latest orchestration pointer, before prior pointers.

Fields: `goal_text`, `goal_source`, `mode`, `converged`, `unmet_conditions[]`, `blocked_by[]`,
`conjuncts`, `evaluated_at`, `orchestrator_run_id`, `schema_version`.

### Partial delivery on timeout

When `SOVEREIGN_GOAL_TIMEOUT_MAX > 0` and iteration count reaches the cap without
`converged=true`, the evaluator emits **`SOVEREIGN_GOAL_TIMEOUT`** and writes
`handoffs/sovereign_partial_delivery.md` (sections: Goal, Evaluated At, Unmet Conditions,
Blocked By, Completed Stories, Open Stories, Deferrals Summary, Remediation).

### Troubleshooting reason codes

See `docs/engineering/reason_codes.md` § US-0110 for the 10-code inventory and remediation.

| Reason code | Symptom | Recovery |
|-------------|---------|----------|
| `CONVERGENCE_OPEN_STORIES_REMAIN` | OPEN stories in backlog | Complete stories or adjust goal scope |
| `CONVERGENCE_SMOKE_PROBE_FAIL` | `tests/report.md` Fail > 0 or UAT smoke step failed | Fix tests; re-run `/verify-work` |
| `SOVEREIGN_GOAL_TIMEOUT` | Iteration cap exhausted | Read partial-delivery report; increase cap or resolve blockers |
| `SOVEREIGN_GOAL_DERIVE_FAILED` | Empty/unreadable vision | Set explicit `SOVEREIGN_GOAL` |

### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=sovereign-convergence
```

Pair table (`SOVEREIGN_CONVERGENCE_PAIRS`):
- `scripts/sovereign_convergence_lib.py` ↔ `template/scripts/sovereign_convergence_lib.py`
- `scripts/sovereign_convergence_validate.py` ↔ `template/scripts/sovereign_convergence_validate.py`

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0110`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0110
- **Decision record**: `decisions/DEC-0110.md`
- **Contract tests**: `tests/us0110_contract_test.py` (8 tests)

### Cross-Model Adversarial Critic (US-0104)

**Default-off cross-model review**. When `CROSS_MODEL_REVIEW=0` (default), zero overhead — no
critic spawn, no findings writes, no anti-slop gate. When `1`, `/auto` spawns `/sovereign-critic`
after each producer phase.

#### Scratchpad keys

| Key | Values | Default | Behavior when off |
|-----|--------|---------|-------------------|
| `CROSS_MODEL_REVIEW` | `0` \| `1` | `0` | No critic spawn or findings writes. |
| `CROSS_MODEL_ANTISLOP_THRESHOLD` | int 0–10 | `6` | Aggregate below → rework loop. |
| `CROSS_MODEL_REWORK_MAX` | int ≥ 0 | `2` | Max producer re-spawns per `(run, phase)`. |

#### Enable / disable

```bash
# Enable cross-model critic
echo "CROSS_MODEL_REVIEW=1" >> .cursor/scratchpad.local.md

# Disable (zero overhead)
echo "CROSS_MODEL_REVIEW=0" >> .cursor/scratchpad.local.md
```

#### Validate findings JSONL

```bash
python scripts/sovereign_critic_lib.py --self-test
python scripts/sovereign_critic_validate.py --self-test
python scripts/sovereign_critic_validate.py --repo . --enforce
python scripts/sovereign_critic_validate.py --open-blocking --repo .
```

#### Interpret findings JSONL

Canonical path: `handoffs/sovereign_critic_findings.jsonl` (append-only, 15-field v1 schema).
Each line includes `lens` (`challenger` \| `architect` \| `subtractor`), `severity`, `confidence`
(set by reconciliation), `anti_slop_score`, `blocking`, and `degraded_mode`.

Reconciliation: ≥2 lenses share `issue_key` → `confidence=high`; single lens → `medium`.

#### Anti-slop rework remediation

When aggregate `min(lens_scores) < CROSS_MODEL_ANTISLOP_THRESHOLD` and blocking findings exist:

1. Producer phase re-spawns with fresh context (bounded by `CROSS_MODEL_REWORK_MAX`).
2. Reason **`CROSS_MODEL_ANTISLOP_FAIL`** during rework; **`CROSS_MODEL_REWORK_CAP_EXHAUSTED`**
   at cap → operator decision gate (waive or abort).

#### Degraded fallback troubleshooting

When `select_critic_model` resolves the same slug as producer (or catalog miss), framework sets
`degraded_mode=true` and runs three sequential lens spawns on the same model. Informational reason
**`CROSS_MODEL_DEGRADED_MODE`** — not a hard stop. Documented limitation per **R-0088**.

#### Isolation `model_id` v2

When `CROSS_MODEL_REVIEW=1`, producer **and** critic isolation evidence rows require additive
`model_id`. Missing → **`ISOLATION_EVIDENCE_MODEL_ID_MISSING`**.

#### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=sovereign-critic
```

Pair table (`SOVEREIGN_CRITIC_PAIRS`): lib, validator, command, scratchpad, `DEC-0104.md`.

#### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0104`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0104
- **Decision record**: `decisions/DEC-0104.md`
- **Contract tests**: `tests/us0104_contract_test.py` (8 tests + 2 compose guards)

### Sovereign Memory (US-0105)

**Default-off institutional memory**. When `SOVEREIGN_MEMORY=0` (default), zero overhead —
no JSONL writes, no injection reads, no spawn digest assembly. When `1`, bounded learnings
inject into phase spawns via `scripts/sovereign_memory_lib.py`.

#### Scratchpad keys

| Key | Values | Default | Behavior when off |
|-----|--------|---------|-------------------|
| `SOVEREIGN_MEMORY` | `0` \| `1` | `0` | No reads / writes / digest assembly. |
| `SOVEREIGN_MEMORY_TOP_N` | int ≥ 0 | `5` | Recent pool size (all four JSONL families). |
| `SOVEREIGN_MEMORY_TOP_K` | int ≥ 0 | `3` | High-impact pool (`patterns` + `mistakes`). |
| `SOVEREIGN_MEMORY_MAX_CHARS` | int ≥ 0 | `2048` | Hard cap on assembled `digest_text`. |
| `SOVEREIGN_MEMORY_JSONL_MAX_LINES` | int ≥ 1 | `500` | Active JSONL line cap before archive rollover. |

#### Enable / disable

```bash
# Enable sovereign memory
echo "SOVEREIGN_MEMORY=1" >> .cursor/scratchpad.local.md

# Disable (zero overhead)
echo "SOVEREIGN_MEMORY=0" >> .cursor/scratchpad.local.md
```

#### JSONL families vs per-run ledger

| Artifact | Path | Scope | Injected v1? |
|----------|------|-------|--------------|
| Decisions log | `docs/engineering/sovereign-memory/decisions-log.jsonl` | Cross-run distilled learnings | yes |
| Mistakes | `docs/engineering/sovereign-memory/mistakes.jsonl` | Orchestrator mistake hooks | yes (top-K) |
| Patterns | `docs/engineering/sovereign-memory/patterns.jsonl` | Phase/curator consolidation | yes (top-K) |
| Plan drift | `docs/engineering/sovereign-memory/plan-drift-register.jsonl` | Fidelity/scope hooks | yes (top-N) |
| Retrospectives | `sovereign-memory/retrospectives/<sprint_id>.md` | Curator `/refresh-context` | **no** |
| Per-run ledger (**US-0103**) | `handoffs/sovereign_decisions/<run_id>.jsonl` | Per-run audit | no (optional promotion) |

Promotion at `/refresh-context` copies ledger highlights to `decisions-log.jsonl` with
`provenance_ref=ledger:<decision_id>` when both `SOVEREIGN_MEMORY=1` and `AI_DECISION_LEDGER=1`.

#### Validate / self-test

```bash
python scripts/sovereign_memory_lib.py --self-test
python scripts/sovereign_memory_validate.py --self-test
python scripts/sovereign_memory_validate.py --repo . --enforce
```

#### Injection char-cap troubleshooting

When digest appears truncated:

1. Check `SOVEREIGN_MEMORY_MAX_CHARS` (default **2048**).
2. Reduce `SOVEREIGN_MEMORY_TOP_N` / `SOVEREIGN_MEMORY_TOP_K` if too many entries compete.
3. Informational **`SOVEREIGN_MEMORY_READ_BOUND`** when tail read truncates — digest still emitted.

#### Archive rollover remediation

When append fails with **`SOVEREIGN_MEMORY_ARCHIVE_REQUIRED`**:

1. Check permissions on `docs/engineering/sovereign-memory-archive/`.
2. Verify disk space; active file rollover moves to `<basename>-<YYYYMMDDTHHMMSSZ>.jsonl`.
3. Rollover is **not** triad compaction (**US-0072** unchanged).

#### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=sovereign-memory
```

Pair table (`SOVEREIGN_MEMORY_PAIRS`): lib, validator, scratchpad, `.gitkeep`, `DEC-0105.md`.

#### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0105`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0105
- **Decision record**: `decisions/DEC-0105.md`
- **Contract tests**: `tests/us0105_contract_test.py` (8 tests + 2 compose guards)

### Sovereign Loop Mode (US-0107)

**Default-off project orchestration**. When `AUTO_SOVEREIGN=0` (default), zero overhead — no
deferral reads/writes, no advance, no notifications. When enabled, requires
`SOVEREIGN_GOAL_MODE=goal_convergence` (fail-closed **`SOVEREIGN_LOOP_GOAL_MODE_REQUIRED`**).

#### Scratchpad keys

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `AUTO_SOVEREIGN` | `0` \| `1` | `0` | Master enable gate. |
| `AUTO_SOVEREIGN_DEFERRAL_MAX` | int ≥ 1 | `50` | Max open deferral rows. |
| `AUTO_SOVEREIGN_DRAIN_GENERATE_MAX` | int ≥ 0 | `3` | Drain-generate iterations per run. |
| `AUTO_SOVEREIGN_DEFERRAL_POLICY` | `stop` \| `skip` \| `resolve_first` | `resolve_first` | Deferral gate policy. |
| `SOVEREIGN_NOTIFY_TARGET` | `off` \| `ntfy` \| `email` \| `hook` | `off` | Notification adapter. |
| `SOVEREIGN_NOTIFY_NTFY_TOPIC` | string | *(empty)* | Local-only ntfy topic. |
| `SOVEREIGN_NOTIFY_NTFY_BASE` | URL | *(empty)* | Optional ntfy base override — local-only. |
| `SOVEREIGN_NOTIFY_HOOK_URL` | URL | *(empty)* | Webhook POST target — local-only. |
| `SOVEREIGN_NOTIFY_EMAIL_TO` | email | *(empty)* | Email v1 deferred. |

#### Enable / disable

```bash
# Enable sovereign loop (both keys required)
echo "AUTO_SOVEREIGN=1" >> .cursor/scratchpad.local.md
echo "SOVEREIGN_GOAL_MODE=goal_convergence" >> .cursor/scratchpad.local.md

# Disable (zero overhead)
echo "AUTO_SOVEREIGN=0" >> .cursor/scratchpad.local.md
```

Notification topic/URL values belong in `.cursor/scratchpad.local.md` only — never commit secrets.

#### Deferral register operator workflow

| Action | Command / API |
|--------|----------------|
| Append deferral | `append_deferral(...)` via `sovereign_loop_lib.py` |
| Resolve deferral | `resolve_deferral(repo, deferral_id, orchestrator_run_id=...)` |
| List open rows | `list_open_deferrals(repo, scratchpad=...)` (latest-state-wins) |
| Validate JSONL | `python scripts/sovereign_loop_validate.py --repo . --enforce` |

Path: `handoffs/sovereign_deferrals.jsonl` (create-on-first-write; bootstrap `.gitkeep` only).
Sidecar: `handoffs/sovereign_loop_state.json` v1 — per-run drain-generate iteration counter.

#### Drain-generate decision gate

When backlog has zero OPEN stories but convergence is not met and iterations remain under cap,
`/auto` spawns a fresh **PO** subagent (spawn-only **US-0095**) with ephemeral id
`drain-gen-{orchestrator_run_id}-{iteration}`. PO proposes up to **3** candidates per iteration.

**Mandatory per-candidate decision gate**: accept → `/intake` or controlled backlog append;
reject → discard. No auto-append without operator gate.

#### US-0109 integration (`DEPLOY_DEFERRED`)

**US-0109** (deploy smoke) is the downstream writer for `DEPLOY_DEFERRED` deferral rows when
deploy smoke cap is exhausted. Schema v1 fields: `work_item_kind=deploy`, standard deferral
register fields per **DEC-0107** §2. US-0107 owns schema, validator, and read paths only — no
deploy smoke logic in this story.

#### Validate / self-test

```bash
python scripts/sovereign_loop_lib.py --self-test
python scripts/sovereign_loop_validate.py --self-test
python scripts/sovereign_loop_validate.py --repo . --enforce
pytest -k us0107
```

#### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=sovereign-loop
```

Pair table (`SOVEREIGN_LOOP_PAIRS`): lib, validator, scratchpad, deferrals `.gitkeep`, `DEC-0107.md`.

#### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0107`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0107
- **Decision record**: `decisions/DEC-0107.md`
- **Contract tests**: `tests/us0107_contract_test.py` (8 tests + 2 compose guards)

### Sovereign Role-Behavior Manifest (US-0106)

**Default-off per-role objective + inter-role review obligations**. When `SOVEREIGN_ROLE_MANIFEST=0` (default),
zero overhead — no manifest reads, no objective injection, no review dispatch. Review spawns are
supplementary post-phase hooks — they never substitute for the US-0069 producer role.

#### Scratchpad keys

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `SOVEREIGN_ROLE_MANIFEST` | `0` \| `1` | `0` | Master enable gate. |
| `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS` | int ≥ 1 | `512` | Hard truncate for injection block. |
| `SOVEREIGN_ROLE_REVIEW_MAX_PER_PHASE` | int ≥ 0 | `2` | Per-phase review dispatch cap. |
| `SOVEREIGN_ROLE_REVIEW_REWORK_MAX` | int ≥ 0 | `1` | Bounded rework before decision gate. |

#### Enable / disable

```bash
# Enable sovereign role manifest
echo "SOVEREIGN_ROLE_MANIFEST=1" >> .cursor/scratchpad.local.md

# Disable (zero overhead)
echo "SOVEREIGN_ROLE_MANIFEST=0" >> .cursor/scratchpad.local.md
```

#### Manifest edit operator workflow

1. Open `.cursor/sovereign-role-manifest.yaml` (active) or `template/.cursor/sovereign-role-manifest.yaml.example` (template).
2. Add role: append `role_id` ∈ {`po`, `tech-lead`, `dev`, `qa`, `release`, `curator`} with `objective_function` (≤ 1024 chars at file; truncated at injection to `SOVEREIGN_ROLE_OBJECTIVE_MAX_CHARS`).
3. Add obligation: `obligation_id` (unique slug), `reviewer_role`, `target_role`, `trigger_phase` ∈ canonical phase ids, `review_focus` ∈ {`user_value_drift`, `testability`, `buildability`, `deployability`}, `artifact_refs[]`, optional `blocking` (default `false`).
4. Edit `cross_model_policy.default_order` ∈ {`role_review_first`, `critic_first`, `critic_only`, `role_review_only`} to set critic vs role-review ordering.
5. Edit `escalation_rules.rework_max` for bounded rework cap.
6. Run validator: `python scripts/sovereign_role_manifest_validate.py --repo . --enforce`.

#### Validator invocation

```bash
# Validate single manifest file
python scripts/sovereign_role_manifest_validate.py --file .cursor/sovereign-role-manifest.yaml

# Validate repo active + template pair
python scripts/sovereign_role_manifest_validate.py --repo . --enforce

# Lib self-test
python scripts/sovereign_role_manifest_validate.py --self-test
```

Success: `[SOVEREIGN_ROLE_MANIFEST_VALIDATION_OK]`.
Fail: reason codes `SOVEREIGN_ROLE_*` — `SCHEMA_INVALID`, `UNKNOWN_ROLE`, `UNKNOWN_PHASE`, `SECRET_DETECTED`, `OBJECTIVE_OVERFLOW`.

#### Review dispatch troubleshooting

| Reason code | Symptom | Remediation |
|-------------|---------|-------------|
| `SOVEREIGN_ROLE_MANIFEST_DISABLED` | `SOVEREIGN_ROLE_MANIFEST=0` — no dispatch | Set `SOVEREIGN_ROLE_MANIFEST=1` to enable |
| `ROLE_REVIEW_DISPATCH_FAILED` | JSONL append I/O error | Check file permissions on `handoffs/sovereign_role_reviews.jsonl` |
| `ROLE_REVIEW_SPAWN_FAILED` | Subagent spawn error | Retry spawn; check Task tool availability |
| `ROLE_REVIEW_BLOCKED` | Blocking review verdict `fail` | Apply escalation: rework (bounded by `SOVEREIGN_ROLE_REVIEW_REWORK_MAX`) or operator decision gate |
| `ROLE_REVIEW_DEFERRAL_FAILED` | US-0107 deferral append error | Check `handoffs/sovereign_deferrals.jsonl` permissions; fail-open logged |
| `ROLE_REVIEW_REWORK_CAP` | Rework max exhausted | Operator decision gate: waive findings or abort |

Reviews JSONL: `handoffs/sovereign_role_reviews.jsonl` (v1 schema: `schema_version`, `obligation_id`, `reviewer_role`, `target_role`, `trigger_phase`, `review_focus`, `producer_evidence_ref`, `orchestrator_run_id`, `ts`, `verdict`, `blocking`, `findings_ref`).

#### Validate / self-test

```bash
python scripts/sovereign_role_manifest_lib.py --self-test
python scripts/sovereign_role_manifest_validate.py --self-test
python scripts/sovereign_role_manifest_validate.py --repo . --enforce
pytest -k us0106
```

#### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=sovereign-role-manifest
```

Pair table (`SOVEREIGN_ROLE_MANIFEST_PAIRS`): scratchpad keys, manifest YAML, example manifest, validator, lib, reviews JSONL, template validator, template lib.

#### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0106`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0106
- **Decision record**: `decisions/DEC-0106.md`
- **Contract tests**: `tests/us0106_contract_test.py` (8 tests + 2 compose guards)

### Parallel Instance Arbitrage (US-0108)

**Default-off parallel execute-phase instance orchestration**. When `SOVEREIGN_PARALLEL_DEV=0` (default),
zero overhead — no worktrees, no parallel QA, no pick JSON, no resource guard.

#### Scratchpad keys

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `SOVEREIGN_PARALLEL_DEV` | `0` \| `1` | `0` | Master enable gate. |
| `AUTO_SOVEREIGN_PARALLEL_N` | int ≥ 1 | `3` | Instances per execute cycle. |
| `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` | int ≥ 1 | `6` | System-wide instance cap. |
| `AUTO_SOVEREIGN_MERGE_RESOLVE` | `first_pass_wins` \| `last_pass_wins` \| `winner_takes_all` \| `manual` | `first_pass_wins` | Merge policy. |
| `AUTO_SOVEREIGN_WORKTREE_KEEP` | `0` \| `1` | `0` | Retain loser worktrees for debugging. |
| `AUTO_SOVEREIGN_PARALLEL_QA` | `0` \| `1` | `0` | Enable parallel QA cross-review (v2). |
| `AUTO_SOVEREIGN_PARALLEL_QA_ARBITER` | `critic_first_pass` \| `majority_vote` | `critic_first_pass` | QA arbitration strategy. |
| `AUTO_SOVEREIGN_PARALLEL_ANTI_SLOP_THRESHOLD` | int 0-10 | `6` | Anti-slop floor. |
| `AUTO_SOVEREIGN_PARALLEL_REWORK_MAX` | int ≥ 0 | `2` | Per-instance rework cap. |
| `AUTO_SOVEREIGN_PARALLEL_MERGE_TIMEOUT_SEC` | int ≥ 10 | `60` | Merge timeout. |
| `AUTO_SOVEREIGN_PARALLEL_MODEL_<idx>` | model slug | *(empty)* | Per-instance model override (optional). |
| `AUTO_SOVEREIGN_PARALLEL_LENS_<idx>` | lens config | *(empty)* | Per-instance lens override (optional). |

#### Enable / disable

```bash
# Enable parallel dev (N=3 instances)
echo "SOVEREIGN_PARALLEL_DEV=1" >> .cursor/scratchpad.local.md
echo "AUTO_SOVEREIGN_PARALLEL_N=3" >> .cursor/scratchpad.local.md

# Disable (zero overhead)
echo "SOVEREIGN_PARALLEL_DEV=0" >> .cursor/scratchpad.local.md
```

#### Parallel dev workflow

1. **Create worktrees** (T-002/T-003): `create_worktrees(story_id, n_instances, base_branch)` → isolated
   `.git/worktrees/us0108-<story_id>-<idx>/` per instance.
2. **Simulated execute** in each worktree (T-008 step 25).
3. **Simulated QA** in each worktree (T-008 step 26).
4. **Select winner** (T-004): `select_winner(qa_results[])` → filter `qa_verdict=pass` → sort `-anti_slop_score`
   → tie-break earliest `proof_issued_at` → single winner.
5. **Read anti-slop score** (T-005): `read_anti_slop_score(lens_scores[])` via
   `sovereign_critic_lib.compute_anti_slop_aggregate` (read-only, US-0104 unchanged).
6. **Merge winner** (T-006): `merge_winner(winner_ctx, main_branch)` with bounded retry ≤2, then
   `PARALLEL_DEV_MERGE_CONFLICT` halt. Write-once `handoffs/parallel_dev_pick.json` v1.
7. **Cleanup** (T-003): winner removed; losers per `AUTO_SOVEREIGN_WORKTREE_KEEP`.

Pick JSON schema v1:
```json
{
  "schema_version": 1,
  "story_id": "US-0108",
  "winner_instance_id": "US-0108-inst0",
  "worktree_path": ".git/worktrees/us0108-US-0108-0",
  "qa_verdict": "pass",
  "anti_slop_score": 8,
  "proof_issued_at": "2026-06-29T22:00:00Z",
  "merge_policy": "first_pass_wins",
  "runner_ts_utc": "2026-06-29T22:30:00Z",
  "orchestrator_run_id": "auto-20260628-04",
  "loser_instance_ids": ["US-0108-inst1", "US-0108-inst2"]
}
```

#### Reason codes

| Code | Meaning |
|------|---------|
| `PARALLEL_DEV_DISABLED` | Feature off — backward compat path. |
| `PARALLEL_DEV_WORKTREE_CREATE_FAILED` | Worktree creation error. |
| `PARALLEL_DEV_WORKTREE_CLEANUP_FAILED` | Cleanup error (fail-open). |
| `PARALLEL_DEV_SELECTION_NO_PASS` | No QA pass verdict in any instance. |
| `PARALLEL_DEV_MERGE_CONFLICT` | Merge conflict after bounded retry. |
| `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED` | System-wide cap reached. |
| `PARALLEL_DEV_RESOURCE_LOCK_FAILED` | Lockfile error. |
| `PARALLEL_DEV_EXECUTE_FAILED` | Instance execution error. |
| `PARALLEL_DEV_ANTI_SLOP_BELOW_THRESHOLD` | Winner score below floor. |
| `PARALLEL_DEV_MERGE_TIMEOUT` | Merge operation timeout. |
| `PARALLEL_DEV_MANUAL_HALT` | Manual intervention required (`merge_resolve=manual`). |
| `PARALLEL_DEV_PICK_SCHEMA_INVALID` | Pick JSON schema violation. |

#### Resource guard

- Lockfile: `.git/us0108_parallel_dev.lock`
- `acquire_parallel_slot(slot_id, repo_root, max_total)` / `release_parallel_slot(slot_id, repo_root)`
- System cap: `AUTO_SOVEREIGN_PARALLEL_MAX_TOTAL` (default 6)
- Fail-fast `PARALLEL_DEV_RESOURCE_CAP_EXHAUSTED` when cap reached

#### Validator / self-test

```bash
# Self-test
python scripts/parallel_dev_arbiter.py --self-test

# Contract tests
python -m pytest tests/us0108_contract_test.py -v

# Parity check
python scripts/check_intake_template_parity.py --scope=sovereign-parallel-dev
```

#### Compose guards (non-negotiable)

| Compose surface | Rule |
|-----------------|------|
| US-0047 (bulk execute) | Step 22 unchanged; system cap checked **after** bulk cap. |
| US-0092 (full autonomy) | Outer driver unchanged; parallel is execute-phase internal. |
| US-0103 (ledger) | Schema unchanged; US-0108 reads ledger only. |
| US-0104 (critic) | Schema unchanged; US-0108 reads `anti_slop_score` only. |
| US-0107 (sovereign loop) | Deferral register unchanged; US-0108 appends winner/loser outcomes as consumer. |

#### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0108`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0108
- **Decision record**: `decisions/DEC-0108.md`
- **Contract tests**: `tests/us0108_contract_test.py` (8 tests)
- **Standalone runbook**: `docs/sovereign-runbook-md/US-0108.md`

---

## Self-Healing Deploy Loop (US-0109 / DEC-0109)

**Default-off** (`AUTO_SOVEREIGN_SELF_HEALING_DEPLOY=0`) — zero overhead when off. When enabled,
adds a post-deploy smoke probe + bounded retry loop on top of US-0054 publish chain.

### Scratchpad keys (schema_v1)

| Key | Values | Default | Notes |
|-----|--------|---------|-------|
| `AUTO_SOVEREIGN_SELF_HEALING_DEPLOY` | `0` \| `1` | `0` | Global gate. When `0`, zero overhead — byte-identical US-0054 publish path. |
| `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX` | int ≥ 1 | `3` | Max retry attempts after probe FAIL. |
| `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC` | int ≥ 1 | `30` | Per-stage HTTP timeout for health probe. |
| `AUTO_SOVEREIGN_DEPLOY_PROBE_KIND` | `health_endpoint` \| `acceptance_smoke` \| `both` | `both` | Which stages run during smoke probe. |
| `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH` | repo-relative path | `tests/deploy_smoke/` | Acceptance smoke tests directory (pytest runner). |
| `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` | names-only env ref | *(empty)* | Key name in `os.environ` — value is a key name, NOT a URL literal. |

Fail-closed `DEPLOY_HEALING_PROBE_TARGET_MISSING` when health endpoint unresolvable.

### Execute steps 29-31

| Step | Action |
|------|--------|
| **29 post-deploy smoke probe** | Two-stage chain `[DEPLOY_SMOKE_PROBE_OK]`. Skip when `0`. |
| **30 retry loop** | Re-enter publish PASS path on probe FAIL; cap exhaustion → step 31. |
| **31 DEPLOY_DEFERRED** | Via US-0107 `append_deferral(work_item_kind=deploy)`. Orchestrator continues. |

### Operator remediation

| Reason code | Operator action |
|-------------|-----------------|
| `DEPLOY_HEALING_DISABLED` | No action; expected default. Set `=1` to enable. |
| `DEPLOY_HEALING_SMOKE_HEALTH_FAIL` | Verify env key in scratchpad.local resolves to reachable URL. Re-run probe. |
| `DEPLOY_HEALING_SMOKE_ACCEPTANCE_FAIL` | Inspect `SOVEREIGN_DEPLOY_ACCEPTANCE_SMOKE_PATH` smoke tests. Fix failures. |
| `DEPLOY_HEALING_RETRY_ATTEMPT` | Informational per-attempt log; no action required. |
| `DEPLOY_HEALING_RETRY_CAP_EXHAUSTED` | Raise `AUTO_SOVEREIGN_DEPLOY_RETRY_MAX` if transient; otherwise resolve root cause. |
| `DEPLOY_HEALING_DEFERRED` | Resolve in `handoffs/sovereign_deferrals.jsonl`; re-run `/release` after fix. |
| `DEPLOY_HEALING_PROBE_TARGET_MISSING` | Set `AUTO_SOVEREIGN_DEPLOY_HEALTH_ENDPOINT` to valid env key; ensure env var has URL. |
| `DEPLOY_HEALING_TIMEOUT` | Raise `AUTO_SOVEREIGN_DEPLOY_SMOKE_TIMEOUT_SEC`; investigate startup latency. |

### Validate / self-test

```bash
python scripts/self_healing_deploy_validate.py --self-test
python scripts/self_healing_deploy_validate.py --repo . --enforce
```

### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=sovereign-self-healing-deploy
```

Pair table (`SOVEREIGN_SELF_HEALING_DEPLOY_PAIRS`): scratchpad, lib, validator,
contract tests, runbook, reason_codes — 6 pairs (active + template).

### Compose surfaces (read-only)

| Composed story | US-0109 boundary |
|----------------|------------------|
| US-0054 (publish) | Re-enters publish PASS only; publish targets/schema/release-notes UNCHANGED. |
| US-0100 (changelog) | No changelog writes triggered by US-0109. |
| US-0103 (ledger) | Schema UNCHANGED; optional `deploy_deferral_id` additive (v1). |
| US-0107 (sovereign loop) | Consumer of `append_deferral(...)` API only; `work_item_kind=deploy`. |
| US-0110 (convergence) | Predicate UNCHANGED; US-0110 reads open deferrals (no new logic). |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0109`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0109
- **Decision record**: `decisions/DEC-0109.md`
- **Library**: `scripts/self_healing_deploy_lib.py`
- **Validator**: `scripts/self_healing_deploy_validate.py`
- **Contract tests**: `tests/us0109_contract_test.py` + `tests/us0109_us0110_compose_test.py`

---

## Release Trigger Adapters (US-0111 / DEC-0111)

**Default source**: `RELEASE_TRIGGER_SOURCE=manual` (zero behavior change vs pre-US-0111 /release path — byte-identical).

### Adapter registry and dispatch

`scripts/release_trigger_adapters.py` provides four adapters:
- **GitHub webhook** (`github`): Parse `release.tag_name`; query GitHub API for previous tag via `GET /repos/{owner}/{repo}/releases?per_page=100` (sorted by `created_at` desc, skip current); fallback `git ls-remote --tags origin` filtered for semver.
- **npm publish** (`npm`): Read `npm_package_version` env var; query `npm view {pkg} versions --json` with `RELEASE_TRIGGER_TIMEOUT_SEC` (default 10s); offline fallback `package-lock.json` when `RELEASE_TRIGGER_FALLBACK_TO_LOCAL=1`.
- **Git tag push** (`git_tag`): Parse `GITHUB_REF=refs/tags/vX.Y.Z` or local `git describe --tags --abbrev=0`; compute previous via `git for-each-ref --sort=-version:refname refs/tags` (semver sort, not date — handles annotated vs lightweight tags).
- **Manual /release** (`manual`): `TriggerContext(source="manual", version=current, previous_version=None)` — byte-identical to pre-US-0111 /release.

Dispatch via `dispatch_to_adapter(source, env_vars)` → `TriggerContext`. Invalid source → `RELEASE_TRIGGER_SOURCE_INVALID` (fail-closed).

### Scratchpad keys

| Key | Values | Default |
|-----|--------|---------|
| `RELEASE_TRIGGER_SOURCE` | `manual` \| `github` \| `npm` \| `git_tag` \| `auto` | `manual` |
| `RELEASE_TRIGGER_TIMEOUT_SEC` | int ≥ 1 | `10` |
| `RELEASE_TRIGGER_FALLBACK_TO_LOCAL` | `0` \| `1` | `0` |

### TriggerContext dataclass

```python
@dataclass
class TriggerContext:
    version: str
    previous_version: Optional[str]
    source: str  # manual | github | npm | git_tag
    metadata: Dict[str, Any]
```

### Version comparison integration (AC-6)

`compare_versions_from_trigger(trigger)` normalizes `trigger.version` and `trigger.previous_version` via `release_changelog_lib.normalize_semver()`. Fail-closed: `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED` on invalid semver.

### Atomic promotion (AC-7, AC-8)

- **CHANGELOG.md promotion**: `promote_changelog_version(semver, sprint_ids, repo_root)` reuses `release_changelog_lib.promote_unreleased()` unchanged (US-0100 compose). Atomic write via `os.replace(temp, target)` with Windows best-effort retry (0.1s × 2). Fail-closed: `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED`.
- **Per-version notes**: `write_per_version_notes(semver, sprint_ids, repo_root)` writes `handoffs/releases/vX.Y.Z-release-notes.md` atomically. Reuses `release_changelog_lib.build_version_doc()` read-only compose. Fail-closed: `RELEASE_TRIGGER_NOTES_WRITE_FAILED`.

### Ledger event emit (AC-9)

`emit_version_derivation_event(trigger, norm_version, norm_previous, repo_root, scratchpad)`:
1. Write `handoffs/release_events/{iso-timestamp}-{semver}.json` atomically.
2. Append to US-0103 ledger via `decision_ledger_lib.append_entry(ledger_path, entry, scratchpad)` with `decision_type="version_derivation"`. Ledger schema unchanged (consumer-only append compose).
3. Fail-closed: `RELEASE_TRIGGER_EVENT_EMIT_FAILED`.

### Reason codes (9 total — DEC-0111 §7)

| Code | Trigger | Blocking? |
|------|---------|-----------|
| `RELEASE_TRIGGER_ADAPTER_FAILED` | Adapter dispatch error | **Yes** |
| `RELEASE_TRIGGER_TAG_MISSING` | Cannot resolve current tag | **Yes** |
| `RELEASE_TRIGGER_PREVIOUS_MISSING` | Cannot resolve previous tag | **Yes** |
| `RELEASE_TRIGGER_PACKAGE_JSON_MISSING` | npm adapter: package.json missing | **Yes** |
| `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED` | Atomic write failed (Windows lock, I/O) | **Yes** |
| `RELEASE_TRIGGER_NOTES_WRITE_FAILED` | Per-version notes write failed | **Yes** |
| `RELEASE_TRIGGER_EVENT_EMIT_FAILED` | Ledger/event emit failed | **Yes** |
| `RELEASE_TRIGGER_COMPARE_VERSIONS_FAILED` | Semver compare failed | **Yes** |
| `RELEASE_TRIGGER_SOURCE_INVALID` | Unknown source value | **Yes** |

### Operator troubleshooting

| Symptom | Diagnosis | Remediation |
|---------|-----------|-------------|
| `RELEASE_TRIGGER_SOURCE_INVALID` on startup | Invalid `RELEASE_TRIGGER_SOURCE` in scratchpad | Set to `manual` (default), `github`, `npm`, `git_tag`, or `auto` |
| `RELEASE_TRIGGER_TAG_MISSING` in CI | `GITHUB_REF` not set or non-semver | Ensure CI passes `GITHUB_REF=refs/tags/vX.Y.Z` or run `git tag vX.Y.Z && git push --tags` |
| `RELEASE_TRIGGER_ATOMIC_PROMOTION_FAILED` on Windows | File lock or antivirus holding CHANGELOG.md | Close IDE tabs; retry; check antivirus exclusion list |
| `RELEASE_TRIGGER_EVENT_EMIT_FAILED` with ledger enabled | Ledger file permissions or schema mismatch | Check `handoffs/sovereign_decisions/decisions.jsonl` writable; verify 12-field schema |

### Compose surfaces (read-only)

| Composed story | US-0111 boundary |
|----------------|------------------|
| US-0100 (changelog) | Reuses `promote_unreleased()` and `build_version_doc()` unchanged; no API modifications. |
| US-0054 (publish) | Dispatches before `/release` path; `release-all.sh` UNCHANGED. |
| US-0103 (ledger) | Consumer of `append_entry()` API only; `decision_type="version_derivation"` additive. |
| US-0040 (runbook) | No runbook structure changes; adds new section. |
| US-0008 (release-all.sh) | UNCHANGED; US-0111 is pre-release dispatch. |
| US-0107 (sovereign loop) | No sovereign loop changes; US-0111 emits events to ledger. |
| US-0110 (convergence) | `list_open_deferrals` UNCHANGED; no convergence predicate changes. |

### Parity enforcement

```bash
python scripts/check_intake_template_parity.py --scope=release-trigger-adapter
```

Pair table (`RELEASE_TRIGGER_ADAPTER_PAIRS`): lib + template lib + contract tests + runbook + reason_codes + scratchpad + parity itself — 7 pairs (active + template).

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0111`
- **Reason codes**: `docs/engineering/reason_codes.md` § US-0111
- **Decision record**: `decisions/DEC-0111.md`
- **Library**: `scripts/release_trigger_adapters.py`
- **Contract tests**: `tests/us0111_contract_test.py` (12 tests)

---

## Compose Guards: US-0054, US-0100, US-0110 (read-only boundaries)

Contract tests enforce US-0109 does not modify these upstream surfaces:

### US-0054 — Publish Targets

`test_us0109_us0054_compose_no_publish_semantics_change` verifies:
- No `RELEASE_PUBLISH_OK` token written by US-0109 code
- No `release_publish` function calls
- No `publish_targets` schema modifications

US-0109 reads publish status as an observer; publish logic remains in `scripts/release_publish.py`.

### US-0100 — Changelog / Unreleased Promotion

`test_us0109_us0100_compose_no_changelog_change` verifies:
- No `changelog` string literals in US-0109 code
- No `[Unreleased]` version promotion
- No `changelog_lib` or `version_changelog` imports

US-0109 does not write changelog entries or promote versions.

### US-0110 — Convergence Predicate

`test_us0109_us0110_compose_no_convergence_change` verifies:
- No `convergence` string literals in US-0109 code
- No `evaluate_convergence` function calls
- No imports from `sovereign_convergence_lib`

US-0109 does not participate in convergence evaluation.

---

## Scratchpad Example Parity (BUG-0013)

**Goal**: `template/.cursor/scratchpad.local.example.md` must stay in structural parity with the canonical `.cursor/scratchpad.md` (current source of truth), while preserving the example-only header (L1–L5) and excluding project-local flag overrides (which belong in consumer `.cursor/scratchpad.local.md`).

### Single source of truth

- Canonical scratchpad: `.cursor/scratchpad.md` (read-only for installers).
- Template example: `template/.cursor/scratchpad.local.example.md` (mirror — must stay in sync structurally; project-local value overrides must be reset to safe defaults).
- Active example: `.cursor/scratchpad.local.example.md` (body must be byte-identical to template mirror from L6 onwards).

### When to re-sync

Whenever `.cursor/scratchpad.md` gains a new `## Section` / key block, the template example must be refreshed (copy canonical, then reset project-local values):

- Copy canonical to template.
- Preserve the example-only header comment (first 5 lines).
- Reset framework/project-local keys to their safe example defaults:

| Key | Example default | Canonical (framework) value |
|---|---|---|
| `FRAMEWORK_KIT_REPO` | `0` | `1` |
| `CAVEMAN_LEVEL` | *(empty)* | `full` |
| `TOKEN_PROFILE` | `balanced` | `lean` |
| `CAVEMAN_MODE` | `0` | `1` |

### Verification command

```bash
python -m pytest tests/scratchpad_example_parity_test.py -v
```

Three regression test markers cover this contract:

- `test_bug0013_parity_check`: all canonical keys present in template (canonical keys ⊆ template example keys).
- `test_bug0013_header_preserved`: example-only header comment (L1–L5) intact.
- `test_bug0013_local_overrides_preserved`: no project-local override values leak into the template example.

### Reason codes

| Reason | Meaning |
|---|---|
| `SCRATCHPAD_EXAMPLE_OUT_OF_SYNC` | Template example is missing one or more canonical sections/keys. |
| `SCRATCHPAD_HEADER_DRIFT` | Example-only header (L1–L5) was overwritten or drifted. |
| `SCRATCHPAD_LOCAL_VALUES_LEAKED` | Project-local override values (e.g. `FRAMEWORK_KIT_REPO=1`, `CAVEMAN_LEVEL=full`) are present in the template example. |

### Normative architecture

- **Backlog**: `docs/product/backlog.md` § `BUG-0013` (scratchpad-example-stale).
- **Sprint**: `sprints/S-BUG0013/`.
- **Test**: `tests/scratchpad_example_parity_test.py`.

### Compose guards (unchanged)

US-0008, US-0040, US-0054, US-0100, US-0101, US-0102, US-0103, US-0107, US-0110 (as per sprint constraints — all UNCHANGED during BUG-0013).

---

## Project run steps

### Prerequisites

### Local run

### Tests


## Work-kind routing (US-0118 / DEC-0118)

Per-story work-kind classification + tiered delivery routing. Default-off
(`WORK_KIND_ROUTING=0` â€” zero overhead when off; byte-identical to
pre-US-0118). When enabled, the classifier derives
`(delivery_mode, phase_plan)` from the story shape using the L8
precedence chain.

### Work-kind enumeration

| work_kind | recommended_delivery_mode | recommended_phase_plan | Rule |
|-----------|---------------------------|------------------------|------|
| `doc`     | `ultra_lean`              | `[intake, execute, release]` | All touched files match `dev_environment_lib.TIER_C_SKIP_PREFIXES` or are `*.md`/`README*` under skip prefixes. |
| `mini`    | `ultra_lean` or `mega_quick` | `[spec, plan, build+verify, ship]` or `[quick]` | Single component, ACs â‰¤ 3, no companion DEC required. `mega_quick` only when US-0096 eligibility passes. |
| `code`    | `standard`                | Full canonical lifecycle (DEC-0052 chain) | Otherwise (tier A or any non-skip-prefix source path). |

Tie-break (Q1 LOCKED): when a story touches both `docs/` and `src/`
(mixed tier), **highest tier wins** (`code` > `mini` > `doc`) per
`dev_environment_lib.classify_touched_files` tier_rank A>B>C.

### L8 precedence chain

1. `start-from=<phase>` (always wins â€” intersects with the active plan).
2. Explicit `DELIVERY_MODE` (US-0096 / DEC-0082).
3. Explicit `AUTO_PHASE_*` (US-0070 / DEC-0052).
4. `WORK_KIND_ROUTING`-derived `recommended_delivery_mode` (US-0118).
5. Current default lifecycle (`standard` delivery mode).

Conflict rule: work-kind recommends `X` but explicit `DELIVERY_MODE=Y`
set and they differ â†’ `WORK_KIND_DELIVERY_MODE_CONFLICT` (fail-closed;
explicit wins per L8). Mid-story `DELIVERY_MODE` switch forbidden per
DEC-0082 Â§2 (`DELIVERY_MODE_SWITCH_MID_STORY`).

### Reason codes (R-0106 Q2 LOCKED)

| Reason code | Fail-closed? | Remediation |
|-------------|--------------|-------------|
| `WORK_KIND_ROUTING_OFF` | no (info) | Set `WORK_KIND_ROUTING=1` to enable per-story routing; current behavior unchanged. |
| `WORK_KIND_DELIVERY_MODE_CONFLICT` | yes | Explicit `DELIVERY_MODE` wins per L8; unset `DELIVERY_MODE` to allow work-kind routing OR update the backlog row; mid-story switch forbidden. |
| `WORK_KIND_CLASSIFY_FAILED` | yes | Re-run `/intake` with explicit `work_kind` override; inspect `--explain` trace; file bug if rule engine is at fault. |
| `WORK_KIND_UNKNOWN_ROUTE` | yes | Re-run classifier; if persistent, set `DELIVERY_MODE` explicitly or add `AUTO_PHASE_*` override; default to `standard` lifecycle. |
| `WORK_KIND_PLAN_COVERAGE_MISSING` | yes | Re-run classifier; if persistent, set `DELIVERY_MODE` explicitly or add `AUTO_PHASE_*` override; default to `standard` lifecycle. |
| `WORK_KIND_TIE_BREAK_APPLIED` | no (info) | Mixed-tier story resolved by highest-tier-wins. Inspect `--explain` trace to override. |

### Operator recipes

**Force full lifecycle on a `doc` story** â€” set `DELIVERY_MODE=standard`
in `.cursor/scratchpad.local.md` (or pass `delivery-mode=standard` to
`/auto`). Explicit `DELIVERY_MODE` wins per L8 #2 regardless of the
classifier recommendation.

**Inspect the classifier trace** â€” run
`python scripts/work_kind_classify_lib.py --explain --story-prose "..." --ac AC-1 AC-2 --touched docs/foo.md src/index.ts --component-scope web`.
The `rule_trace` field shows `(rule_id, matched_signal, contribution)`
tuples so operators can override with confidence (R5).

**Self-test** (AC-12) â€” `python scripts/work_kind_classify_lib.py --self-test`
exits 0 with `[WORK_KIND_CLASSIFY_SELF_TEST_OK]`;
`python scripts/work_kind_routing_lib.py --self-test` exits 0 with
`[WORK_KIND_ROUTING_SELF_TEST_OK]`.

### Intake evidence schema extension (AC-9 / R-0106 Q9)

When `WORK_KIND_ROUTING=1` and the classifier runs at `/intake` step 5
(after ACs drafted, after US-0051 decomposition evaluator, before
persistence), the intake evidence JSON (`handoffs/intake_evidence/US-xxxx-intake.json`)
gains three optional fields:

| Field | Values | When present |
|-------|-------|--------------|
| `work_kind` | `doc` \| `mini` \| `code` | When `WORK_KIND_ROUTING=1` and classifier ran at `/intake` step 5. |
| `recommended_delivery_mode` | `standard` \| `ultra_lean` \| `mega_quick` | When `WORK_KIND_ROUTING=1` and classifier ran at `/intake` step 5. |
| `work_kind_operator_decision` | `accept` \| `override` | When `WORK_KIND_ROUTING=1` and operator made an explicit decision. |

Existing intake evidence files are NOT modified â€” only the schema
contract is documented. US-0078 evidence gate still runs before any
backlog/acceptance write (L10 unchanged).

### Compose, do not amend

US-0118 is additive-only across all 6 read-only compose consumers:
US-0096 (delivery modes â€” explicit `DELIVERY_MODE` still wins per L8),
US-0070 (phase selection â€” `AUTO_PHASE_*` remains explicit override),
US-0078 (intake evidence â€” gate still runs before any write), US-0051
(decomposition â€” classifier runs after the decomposition evaluator),
US-0069 (phaseâ†’role matrix â€” classifier only selects which phases run,
not who runs them), US-0103 (AI decision ledger â€” read-only consumer
for audit trail). 23 compose guards UNCHANGED.

## Autonomy preset keys (US-0119 / DEC-0119)

**Default-off**: `AUTONOMY_PRESET=none` (default) and `AUTONOMY_STOP_POLICY=block` (default) — zero overhead when off; byte-identical to pre-US-0119 baseline.

### `AUTONOMY_PRESET` enum (R-0107 Q7 LOCKED)

| Value | Expansion | Rationale |
|-------|-----------|-----------|
| `none` (default) | `{}` — empty flag set | Full backward compatibility; zero autonomy relaxation. |
| `balanced` | 8 flags per DEC-0119 §7 (see table below) | Moderate autonomy — auto-refresh brief, work-kind auto-accept, release auto-confirm, drain auto-accept. |
| `full` | 12 flags per DEC-0119 §7 (see table below) | Maximum autonomy — adds intake-auto, cross-model-skip, goal-convergence-interval-1. |

**Merge precedence (R-0107 Q7 LOCKED)**: explicit per-flag value in scratchpad (or via preset expansion) > scratchpad default (empty for off keys) > `AUTONOMY_PRESET` expansion > consumer default.

### `AUTONOMY_STOP_POLICY` enum (DEC-0119 §3)

| Value | Dispatch behavior |
|-------|-------------------|
| `block` (default) | Strict fail-closed — any stop code halts execution. Pre-US-0119 behavior. |
| `auto_repair_then_block` | Attempt `auto_repair_kind` from stop-matrix; if repair succeeds, continue; if repair fails or cap exhausted, hard stop. |
| `auto_repair_then_skip` | Same as `auto_repair_then_block`, but on cap exhaustion skip the current phase (emit stop-mark, not hard stop). |

### 12 per-feature flags

| Flag | Preset (balanced/full) | Consumer | Pre-US-0119 surface |
|------|------------------------|----------|---------------------|
| `AUTO_REFRESH_BRIEF` | `1`/`1` | `/auto`, `/qa`, `/release` | Pre-US-0119: manual refresh only. |
| `WORK_KIND_AUTO_ACCEPT` | `1`/`1` | `/intake` step 5 | Pre-US-0119: manual accept required. |
| `RELEASE_AUTO_CONFIRM_ACCEPTANCE` | `1`/`1` | `/release` gate | Pre-US-0119: manual confirmation required. |
| `SOVEREIGN_DRAIN_AUTO_ACCEPT` | `1`/`1` | `/drain` gate | Pre-US-0119: manual accept required. |
| `CROSS_MODEL_REWORK_EXHAUSTION_POLICY` | `block`/`skip` | `/qa`, `/sovereign-critic` | Pre-US-0119: block only. |
| `CROSS_MODEL_SKIP_PHASES` | `verify-work,release`/`release` | `/sovereign-critic` | Pre-US-0119: all phases required. |
| `INTAKE_AUTONOMY_MODE` | —/`derived` | `/intake` step 5 | Pre-US-0119: manual derivation. |
| `INTAKE_MINIMAL_PACK` | —/`1` | `/intake` | Pre-US-0119: full pack only. |
| `INTAKE_ASSUME_STACK_CONTEXT` | —/`1` | `/intake` | Pre-US-0119: explicit stack context required. |
| `RUNTIME_PROOF_KIND` | `lightweight`/`lightweight` | `/auto`, `/execute`, `/qa`, `/release` | Pre-US-0119: strict SHA-256 only. |
| `GOAL_CONVERGENCE_INTERVAL` | `3`/`1` | `/qa`, `/sovereign-convergence` | Pre-US-0119: phase-by-phase evaluation. |
| `AUTONOMY_STOP_POLICY` | (stop-policy enum, not a flag) | `/auto` phase dispatch | Pre-US-0119: implicit `block`. |

### Bounded auto-repair ledger (DEC-0119 §5)

Per-run append-only ledger tracks `auto_repair` attempts:

- **Path**: `handoffs/autonomy_repair_ledger/<orchestrator_run_id>.jsonl`
- **Schema**: `{"reason_code": "<code>", "auto_repair_kind": "<kind>", "attempt": <n>, "outcome": "success|fail", "repair_evidence": "<path>"}`
- **Cap**: Per `(run, reason_code)` = 3 attempts (Q3 LOCKED).
- **Exhaustion**: Terminal stop code `AUTONOMY_REPAIR_CAP_EXHAUSTED` (run-level; distinct from story-level `BLOCK_RETRY_CAP_EXHAUSTED`).
- **Operator override**: `AUTONOMY_REPAIR_CAP_OVERRIDE=<int>` per-run scratchpad key (default: matrix-default 3).
- **Ledger audit**: `python scripts/autonomy_repair_ledger_lib.py --self-test` exits 0 with `[AUTONOMY_REPAIR_LEDGER_SELF_TEST_OK]`.

### Stop-matrix manifest

- **Path**: `docs/engineering/autonomy-stop-matrix.md` (operator-facing documentation)
- **Machine-readable**: `scripts/data/autonomy_stop_matrix.yaml`
- **Validator**: `python scripts/validate_autonomy_stop_matrix.py --self-test` exits 0 with `[MATRIX_VALID]`.
- **Structure**: 2-tier classification — `security_hard` (18+ codes, `auto_repair_kind=n/a`, `cap=0`) and `autonomy_resolvable` (9 codes, `auto_repair_kind` per DEC-0119 §4, `cap` from matrix).

### Autonomy breadcrumb (AC-9, Q10 LOCKED)

At phase boundary, after a soft-stop is actually softened, emit one-line breadcrumb in `docs/engineering/state.md`:

```markdown
autonomy_relaxed: <reason_code> -> <auto_repair_kind>
```

**One line per soft-stop** (not aggregated per phase). Breadcrumb is operator-audit trail — not a governance gate.

### Operator recipe

1. Set `AUTONOMY_PRESET=balanced` for moderate autonomy (8 flags).
2. Set `AUTONOMY_PRESET=full` for maximum autonomy (12 flags).
3. Set `AUTONOMY_STOP_POLICY=auto_repair_then_block` for repair + block on exhaustion.
4. Set `AUTONOMY_STOP_POLICY=auto_repair_then_skip` for repair + skip on exhaustion.
5. Override individual flags via explicit scratchpad entries (precedence over preset expansion).

### Troubleshooting

| Symptom | Likely cause | Remedy |
|---------|--------------|--------|
| `AUTONOMY_PRESET=none` but flags still expanded | Explicit per-flag values in scratchpad override preset=none. | Remove explicit per-flag values or set `AUTONOMY_STOP_POLICY=block`. |
| `AUTONOMY_REPAIR_CAP_EXHAUSTED` terminal stop | 3 repair attempts failed for the same reason code. | Raise `AUTONOMY_REPAIR_CAP_OVERRIDE` or investigate root cause. |
| `RUNTIME_PROOF_KIND=lightweight` rejected | Consumer does not support lightweight proofs. | Verify consumer supports lightweight kind (DEC-0038 §5); fallback to strict. |
| Parity broken `scripts/validate_autonomy_stop_matrix.py` | Active ≠ template byte-identical. | Re-sync `cp scripts/validate_autonomy_stop_matrix.py template/scripts/validate_autonomy_stop_matrix.py`. |

### Compose guards (read-only consumers — UNCHANGED by US-0119)

- US-0092 (delivery confirmation) — relaxed stop policy additive only.
- US-0095 (native auto-chain) — preset expansion additive only.
- US-0056 (strict runtime proof) — `RUNTIME_PROOF_KIND=lightweight` is opt-in lighter attestation; strict unchanged.
- US-0068 (mandatory intake packs) — evidence gate NEVER bypassed; `INTAKE_AUTONOMY_MODE=1` auto-derives answers only.
- US-0096 (delivery modes) — preset additive relaxation layer above explicit `DELIVERY_MODE`.
- BUG-0007 (truthfulness) — `INTAKE_ASSUME_STACK_CONTEXT=1` preserves `assumption_confirmation_ref` contract.

### Byte-stability surface

US-0119 adds one new sub-block in `its_magic/README.md` (§"### Autonomy preset keys (US-0119)") and is additive-only to the 6-block byte-stability surface (US-0113..US-0118). All prior blocks remain byte-identical between `active` and `template/`.

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0119`
- **Decision**: `decisions/DEC-0119.md`
- **Research**: `docs/engineering/research.md` `## R-0107`
- **Scripts**: `scripts/autonomy_preset_lib.py`, `scripts/validate_autonomy_stop_matrix.py`, `scripts/autonomy_repair_ledger_lib.py`
- **Matrix YAML**: `scripts/data/autonomy_stop_matrix.yaml`
- **Tests**: `tests/us0119_autonomy_preset_test.py` (10 markers)
- **Ledger path**: `handoffs/autonomy_repair_ledger/*.jsonl`

## Story closure (US-0120)

**Goal:** Dedicated `/closure` phase after `/release` to perform backlog status flip, acceptance tick, and state checkpoint append. Extracts these responsibilities from `/release` into a phase with exclusive ownership.

### When to run

- **Trigger:** `/closure` runs automatically after `/release` PASS verdict.
- **Phase order:** ship macro = `release` → `closure` → `refresh-context` (3 phases).
- **Orchestrator spawn:** `/auto` orchestrator spawns `/closure` subagent with `role=qe` (default) or `role=curator` (override via `AUTO_ROLE_CLOSURE`).
- **Manual trigger:** For in-flight stories at US-0120 boundary, run `/closure` directly with `story_id=<US-xxxx>`.

### How to verify

1. **Check state.md closure checkpoint:**
   ```bash
   rg "phase_id=closure" docs/engineering/state.md
   ```
   Expected: checkpoint with `phase_id=closure`, `role=qe|curator`, `story_id=<US-xxxx>`, `evidence_ref=sprints/Sxxxx/closure-verification.md`.

2. **Check runtime proof:**
   ```bash
   rg "runtime_proof_id.*US-0120" docs/engineering/state.md
   ```
   Expected: strict proof tuple with `phase_id=closure`, `role=qe|curator`, `proof_hash=<sha256>`.

3. **Check backlog status flip:**
   ```bash
   rg "^- Status: DONE$" docs/product/backlog.md
   ```
   Expected: target story block shows `Status: DONE` (was `OPEN`).

4. **Check acceptance checkbox tick:**
   ```bash
   rg "^\- \[x\] US-xxxx:" docs/product/acceptance.md
   ```
   Expected: target row shows `[x]` (was `[ ]`).

5. **Check closure-verification.md artifact:**
   ```bash
   ls sprints/Sxxxx/closure-verification.md
   ```
   Expected: file exists with `story_id`, `closure_date`, `release_evidence_refs[]`, `isolation_evidence{}`, `runtime_proof{}`.

### How to manually trigger (in-flight stories)

For stories that completed `/release` before US-0120 ship:

1. **Verify release evidence exists:**
   - `handoffs/release_queue.md` contains row with `status=released`.
   - `handoffs/releases/Sxxxx-release-notes.md` exists with PASS verdict.
   - `sprints/Sxxxx/qa-findings.md` exists.

2. **Run `/closure` with explicit story_id:**
   ```bash
   /closure story_id=US-xxxx
   ```
   Or let orchestrator detect via drain hook (3-signal: release_queue=released + backlog=OPEN + acceptance=[ ]).

3. **Verify closure artifacts:**
   - `sprints/Sxxxx/closure-verification.md` created.
   - `docs/product/backlog.md` target story `Status: DONE`.
   - `docs/product/acceptance.md` target row `[x]`.
   - `docs/engineering/state.md` closure checkpoint appended.

### Troubleshooting

| Symptom | Likely cause | Remedy |
|---------|--------------|--------|
| `CLOSURE_RELEASE_EVIDENCE_MISSING` | Release evidence incomplete (no release_queue row, no release-notes, no qa-findings). | Complete `/release` first; verify artifacts exist. |
| `CLOSURE_VERIFICATION_FAILED` | Orchestrator post-verification rg check failed (status not flipped or checkbox not ticked). | Re-run `/closure`; check for permission errors or concurrent mutations. |
| `CANONICAL_STATUS_CONFLICT` | Backlog status contradicts release evidence (e.g., release=released but backlog=OPEN). | Resolve contradiction manually; verify release_queue row `status=released` is correct. |
| `BACKLOG_STATUS_DRIFT` | Backlog not reconciled after closure (status remains OPEN). | Re-run `/closure`; check closure-verification.md for `post_closure_status=DONE`. |
| `PHASE_OWNERSHIP_VIOLATION` | `/closure` tried to mutate non-owned artifact (release notes, qa findings, execute summary). | Check cross-phase ownership guard; `/closure` owns ONLY backlog.md flip, acceptance.md tick, state.md checkpoint, closure-verification.md. |
| `PHASE_OVERRIDE_EVIDENCE_MISSING` | Override path configured (AUTO_ROLE_CLOSURE=curator) but evidence missing. | Provide override evidence or disable override (set `AUTO_ROLE_CLOSURE=` empty). |
| `CLOSURE_LEGACY_DRIFT` | Pre-US-0120 story with all 3 signals (released+OPEN+[ ]) detected by drain hook. | Run `/closure` backfill for in-flight stories; document in closure-verification.md `backward_compat_note`. |

### Compose guards (read-only consumers — UNCHANGED by US-0120)

- US-0043 (backlog reconciliation) — `/closure` executes existing contract; does not amend.
- US-0045 (canonical status source) — backlog.md remains canonical; `/closure` flips status only.
- US-0040 (release artifacts) — `/release` still owns release notes, queue, legacy pointer; `/closure` consumes only.
- US-0048 (isolation evidence) — `/closure` appends its own checkpoint; prior phases unchanged.
- US-0056 (strict runtime proof) — `/closure` appends its own proof tuple; prior phases unchanged.
- US-0096 (delivery modes) — ship macro extended to 3 phases; `standard`/`ultra_lean`/`mega_quick` semantics unchanged.

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0120` at L2125.
- **Decision**: `decisions/DEC-0120.md` (not yet written; companion DEC for US-0120).
- **Commands**: `.cursor/commands/closure.md` (active + template byte-identical).
- **Validator**: `scripts/validate_closure_verification.py` (schema validator).
- **Tests**: `tests/us0120_closure_phase_test.py` (10 markers).
- **Manifest**: `docs/engineering/context/installer-owned-paths.manifest` (closure paths in `install_include_paths` + `clean_paths`).
- **Parity checker**: `scripts/check_intake_template_parity.py --scope=us-0120` (closure-phase surfaces).

## OpenCode host mode (US-0121)

**Goal:** Ship the first vertical slice of the OpenCode adapter epic — an
empty-but-valid `template/.opencode/` pack plus an additive `--host cursor|opencode|both`
switch on the existing its-magic installer. Default install remains
**cursor-only** until explicit opt-in. Full operator runbook is US-0126; this
section is the minimal docs hook (AC-9).

### `--host` flag

```
its-magic --target <repo> --mode missing [--host cursor|opencode|both]
```

- `--host` accepts `cursor | opencode | both` (case-insensitive, whitespace-trimmed).
- Default is `cursor` when `--host` is omitted. No scratchpad key, environment
  variable, or host auto-detect may flip the default in this story.
- Unknown value → exit with `INSTALL_HOST_INVALID` (ASCII diagnostic, no GUI).
- Duplicate / conflicting `--host` argv → fail closed `INSTALL_HOST_INVALID`
  (no last-wins; closes critic finding `ik_us0121_upgrade_host_transition`).
- `--host` gates **only** `.cursor/` and `.opencode/` trees. Kernel paths
  (`docs/`, `scripts/`, `its_magic/`, `handoffs/`, `decisions/`, `sprints/`,
  `.github/workflows/`) always install regardless of `--host`.

### Install

```bash
# Cursor-only (default; .opencode/ is NOT installed)
its-magic --target . --mode missing

# OpenCode-only (.cursor/ rows skipped; kernel paths still install)
its-magic --target . --mode missing --host opencode

# Both host trees
its-magic --target . --mode missing --host both
```

### Clean (host-scoped — no silent deletion)

```bash
its-magic --clean-repo --target . --yes --host cursor      # removes [clean_paths] only
its-magic --clean-repo --target . --yes --host opencode    # removes [opencode_clean_paths] only
its-magic --clean-repo --target . --yes --host both        # removes both
```

Shrinking `--host both` → `cursor` does **not** delete `.opencode/`; it emits
`OPENCODE_ORPHANED_BY_CLEAN_CURSOR`. The operator must run
`its-magic --clean-repo --host opencode|both` to remove the orphan. Symmetric
for `--host opencode` shrinking from `both` (`CURSOR_ORPHANED_BY_CLEAN_OPENCODE`).

### Upgrade (host-scoped)

```bash
its-magic --target . --mode upgrade --host cursor
its-magic --target . --mode upgrade --host opencode
its-magic --target . --mode upgrade --host both
```

`upgrade --host cursor` after `--host both` does **not** refresh `.opencode/`;
it emits `OPENCODE_STALE_BY_UPGRADE_CURSOR`. Symmetric:
`CURSOR_STALE_BY_UPGRADE_OPENCODE` when shrinking the other way.

### Missing (host-scoped — YAGNI)

`missing` after `--host both` then `--host cursor` no-ops on `.opencode/` via
the `host_gates_cursor_row` predicate (copy-if-missing is host-scoped). No new
diagnostic needed; overwrite remains US-0008 unchanged (critic carry-in
`ik_us0121_missing_overwrite_host_gap`).

### Manifest (parallel additive sections)

`docs/engineering/context/installer-owned-paths.manifest` (active + template
byte-identical) ships two new sections; existing `[install_include_paths]`,
`[clean_paths]`, `[required_install_script_paths]` are unchanged:

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

The triple-installer (`installer.py` / `installer.ps1` / `installer.sh`) shares
a single `host_gates_cursor_row(rel, host)` predicate so the three installers
do not diverge (critic finding `ik_us0121_mixed_manifest_cursor_skip`).

### PowerShell `-InstallHost` landmine

`installer.ps1` uses `-InstallHost` (not `-Host`) internally because `-Host`
shadows the automatic `$Host` variable. `bin/its-magic.js` still exposes `--host`
to users and forwards `-InstallHost <value>` to `installer.ps1`. Document this
in QA handoffs.

### Diagnostics reference

| Code | Meaning |
|------|---------|
| `INSTALL_HOST_INVALID` | Unknown or duplicate `--host` argv (fail closed). |
| `OPENCODE_ORPHANED_BY_CLEAN_CURSOR` | `clean --host cursor` left `.opencode/` in place. |
| `OPENCODE_STALE_BY_UPGRADE_CURSOR` | `upgrade --host cursor` did not refresh `.opencode/`. |
| `CURSOR_ORPHANED_BY_CLEAN_OPENCODE` | `clean --host opencode` left `.cursor/` in place. |
| `CURSOR_STALE_BY_UPGRADE_OPENCODE` | `upgrade --host opencode` did not refresh `.cursor/`. |

### Related artifacts

- **Architecture**: `docs/engineering/architecture.md` `# US-0121`.
- **Decision**: `decisions/DEC-0120.md`.
- **Pack**: `template/.opencode/{agents/.gitkeep, commands/.gitkeep, plugins/README.md, .gitignore, README.md}`.
- **Tests**: `tests/us0121_host_mode_test.py` (14 markers).
- **Parity**: `scripts/check_intake_template_parity.py --scope=opencode-adapter`.
- **Full runbook**: US-0126 (deferred).

