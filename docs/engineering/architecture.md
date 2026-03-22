# Architecture

## Overview

US-0018 adds a fourth installer mode (`--mode upgrade`) that safely updates its-magic framework files in a target repo while preserving user data files. The design introduces three new concepts: file classification, version tracking, and an upgrade flow algorithm.

The existing installer architecture (Node.js CLI wrapper → OS-specific installer script → file copy loop) remains unchanged. Upgrade mode is an additional branch in the existing mode switch, using the same file listing and copy infrastructure.

---

# US-0034: Multi-Repo and Contract Compatibility Observability

## Overview

US-0034 adds optional compatibility observability across repositories and
components using manifest artifacts and contract-change signals. The goal is
deterministic impact visibility for planning, QA, and release decisions, not
runtime dependency orchestration.

This architecture follows the user clarification:
- Keep a global view for inventory and cross-repo links.
- Keep per-repo and per-component manifests close to each codebase.
- Surface API changes directly to dependent repos/components so agents can
  derive required work.

## Minimal manifest model

### A1) Global registry manifest (inventory + links)

Canonical artifact:
- `docs/engineering/manifests/registry.manifest.yaml`

Purpose:
- Source-of-truth inventory of known repos/components.
- Cross-repo contract dependency links.
- Ownership and lifecycle visibility.

Minimum required fields:
- `schema_version`
- `generated_at`
- `repos[]`: `{ repo_id, repo_url_or_path, owner, status, manifest_ref }`
- `contracts[]`: `{ contract_id, producer_repo, producer_component, contract_ref, version }`
- `compatibility_links[]`: `{ contract_id, consumer_repo, consumer_component, expected_version_range, criticality }`

### A2) Per-repo manifest

Canonical artifact (inside each repo):
- `docs/engineering/manifests/repo.manifest.yaml`

Purpose:
- Local declaration of exposed and consumed contracts.
- Repo-level owner/version/status metadata.

Minimum required fields:
- `schema_version`
- `repo_id`
- `owner`
- `version`
- `components[]` (references to component manifests)
- `exports[]` (contracts this repo publishes)
- `imports[]` (contracts this repo consumes)

### A3) Per-component manifest

Canonical artifact:
- `docs/engineering/manifests/components/<component_id>.manifest.yaml`

Purpose:
- Unit of scoped change analysis and protection checks.

Minimum required fields:
- `component_id`
- `repo_id`
- `owner`
- `status` (`active|deprecated|experimental|retired`)
- `exposed_contracts[]` (`contract_id`, `api_spec_ref`, `version`)
- `consumed_contracts[]` (`contract_id`, `expected_version_range`)
- `protected_interfaces[]` (interfaces expected to remain stable for non-target work)

### A4) Compatibility map and contract links

Compatibility is represented as producer->consumer edges in
`registry.manifest.yaml.compatibility_links[]`, with each edge tied to a
specific `contract_id` and expected consumer version range.

This creates a deterministic impact graph:
- Contract changes from producer side identify all consumer edges.
- Each edge yields a candidate impact task in sprint planning.

### A5) Change signal model (contract diff + impact)

Canonical artifact:
- `docs/engineering/compatibility-signals.md`

Each signal entry records one observed contract change:
- `signal_id` (`CS-xxxx`)
- `date`
- `story_id`
- `producer_repo` / `producer_component`
- `contract_id`
- `from_version` / `to_version`
- `change_type` (`additive|behavioral|breaking|docs-only`)
- `impacted_consumers[]`
- `severity` (`info|low|medium|high|critical`)
- `required_actions[]` (for impacted repos/components)
- `status` (`open|planned|validated|accepted-risk|resolved`)

Severity baseline:
- `breaking` with impacted consumers -> `high` (or `critical` for
  production-critical links).
- `behavioral` -> `medium`.
- `docs-only` drift -> `low`.

## Workflow integration

### B1) Phase responsibilities

| Phase | Manifest/compatibility responsibilities |
|------|------------------------------------------|
| `/intake` | If enabled, declare target repos/modules and contract artifacts in story scope. |
| `/architecture` | Define/confirm registry and local manifest updates; create compatibility approach and risk policy. |
| `/sprint-plan` | Convert compatibility links + open change signals into explicit tasks per impacted consumer. |
| `/execute` | Update local manifests when contracts/components change; append contract-change signals. |
| `/qa` | Validate impacted consumer coverage and verify signal statuses/evidence. |
| `/verify-work` | Confirm traceability from story -> signals -> tasks -> QA evidence. |
| `/release` | Apply compatibility gate only when enabled and unresolved high/critical findings exist. |
| `/refresh-context` | Curator compacts stale signals, verifies manifest consistency, and updates state summary. |

### B2) Impact derivation model for agents

When a contract change is detected, agents derive work deterministically:
1. Find `contract_id` in `registry.manifest.yaml`.
2. Enumerate `compatibility_links` for consumers.
3. For each consumer edge, create/verify tasks:
   - contract alignment update,
   - consumer regression/smoke verification,
   - docs alignment if public API docs changed.
4. Record findings in `compatibility-report.md` and link to story/sprint tasks.

### B3) Findings and gating policy

Canonical compatibility findings artifact:
- `docs/engineering/compatibility-report.md`

Minimum finding fields:
- `finding_id`
- `story_id`
- `contract_id`
- `producer` + `consumer`
- `severity`
- `evidence`
- `recommended_action`
- `gate_recommendation` (`none|decision-gate`)

Gate behavior:
- Default: non-blocking advisory output.
- If `CROSS_REPO_OBSERVABILITY=1` and unresolved `critical` findings exist,
  trigger decision gate before release progression.

### B4) Default-off / zero-overhead behavior

Control flags in `.cursor/scratchpad.md`:
- `CROSS_REPO_OBSERVABILITY=0` (default)
- `COMPATIBILITY_GATE_ON_CRITICAL=1` (effective only when observability is on)

When `CROSS_REPO_OBSERVABILITY=0`:
- No required manifest processing.
- No required compatibility report updates.
- No additional blocking gates.

## Artifacts and status taxonomy

Canonical files:
- `docs/engineering/manifests/registry.manifest.yaml`
- `docs/engineering/manifests/repo.manifest.yaml`
- `docs/engineering/manifests/components/<component_id>.manifest.yaml`
- `docs/engineering/compatibility-signals.md`
- `docs/engineering/compatibility-report.md`

Status taxonomy:
- Manifest entity status: `active|deprecated|experimental|retired`
- Signal status: `open|planned|validated|accepted-risk|resolved`
- Finding severity: `info|low|medium|high|critical`

---

# US-0035: Component-Scoped Execution Mode with Protection Guards

## Overview

US-0035 introduces an optional scoped-execution mode for multi-component repos.
The mode constrains planning and implementation to declared target components
while requiring explicit protection checks for non-target components.

## Component scope model

### C1) Scope declaration contract

Canonical declaration artifact:
- `docs/engineering/component-scope.md`

Minimum required fields per scoped story:
- `story_id`
- `scope_mode` (`off|on`)
- `target_components[]`
- `non_target_components[]`
- `allowed_interface_touch[]` (explicitly permitted cross-component interfaces)
- `out_of_scope_constraints[]`
- `approval_policy` (who can approve scope expansion)

Scratchpad controls:
- `COMPONENT_SCOPE_MODE=0` (default off)
- `TARGET_COMPONENTS=` (comma-separated defaults for current cycle; optional)

### C2) Non-target protection model

When scope mode is enabled:
- `/sprint-plan` requires each task to include:
  - `target_component_ids`
  - `expected_impacted_interfaces`
- `/execute` enforces scope-first behavior:
  - no intentional edits outside targets unless escalation is approved
- `/qa` requires unaffected-component checks for `non_target_components`:
  - smoke/regression confirmation
  - compatibility signal review for unintended interface impact

Evidence destination:
- `docs/engineering/component-scope-report.md`

### C3) Decision-gate trigger conditions

Trigger decision gate when all conditions are true:
1. `COMPONENT_SCOPE_MODE=1`
2. Out-of-scope component impact is detected
3. Impact is not listed in `allowed_interface_touch[]`
4. No prior approval record exists in decisions/handoff artifacts

Gate outcomes:
- approve scope expansion (update scope artifact + tasks),
- split into separate story/sprint,
- rollback/defer cross-component change.

## Workflow integration (scoped mode)

| Phase | Scoped-mode behavior |
|------|-----------------------|
| `/intake` | Declare in-scope vs out-of-scope components. |
| `/architecture` | Define expected interface touch and protection strategy. |
| `/sprint-plan` | Require component-tagged tasks and impact assumptions. |
| `/execute` | Enforce target-only execution unless approved escalation. |
| `/qa` | Verify target outcomes plus non-target protection checks. |
| `/verify-work` | Confirm scope evidence coverage before pass recommendation. |
| `/release` | If unapproved out-of-scope impact remains, hold via decision gate. |

Default-off behavior:
- If `COMPONENT_SCOPE_MODE=0`, no extra required declarations/checks/gates.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Scope metadata becomes stale | Require `/sprint-plan` refresh of scope file each sprint. |
| False-positive out-of-scope alarms | Allow explicit `allowed_interface_touch[]` declarations. |
| Teams bypass non-target checks | QA checklist requires component-scope report evidence when mode is on. |

---

# US-0036: Official Remote Config Template, Docs, and Fail-Fast Validation

## Overview

US-0036 defines a canonical remote execution configuration contract and
validation behavior for optional remote workflows. The architecture is
process-level only: it specifies artifact contract, checks, error reporting,
and documentation expectations. It does not introduce a runtime transport
implementation.

Primary goals:
- Safe default-off behavior (`REMOTE_EXECUTION=0`) with zero required overhead.
- Deterministic fail-fast validation when remote mode is enabled.
- Clear, actionable error messages and security guardrails.

## Minimal architecture

### 1) Canonical contract artifact and parity

Canonical file path:
- Active repo: `.cursor/remote.json`
- Template copy: `template/.cursor/remote.json`

Parity rule:
- Both files represent the same contract shape and semantics.
- Placeholder values remain non-secret examples only.
- Any contract field changes must update active + template docs and references
  in the same change set.

### 2) Contract model (schema-level)

`remote.json` is a strict JSON object with explicit required and optional
fields. Suggested minimal shape:

```json
{
  "version": 1,
  "defaultTarget": "local-docker",
  "targets": [
    {
      "id": "local-docker",
      "type": "docker",
      "enabled": true,
      "host": "127.0.0.1",
      "port": 2375,
      "workspaceRoot": "/workspace",
      "auth": {
        "mode": "env",
        "tokenEnv": "REMOTE_DOCKER_TOKEN"
      }
    }
  ]
}
```

Validation contract:
- Required root fields: `version`, `defaultTarget`, `targets`.
- Required target fields: `id`, `type`, `enabled`, `host`, `port`,
  `workspaceRoot`.
- `type` allowed values: `docker`, `ssh`, `vm`.
- `auth.mode` allowed values: `none`, `env`.
- If `auth.mode=env`, environment variable references are required (for example
  `tokenEnv`) and inline secrets are forbidden.
- `defaultTarget` must match an existing enabled target id.

### 3) Validation model (mode-aware)

Validation trigger:
- Run remote config validation only when `REMOTE_EXECUTION=1`.
- Skip all remote config checks when `REMOTE_EXECUTION=0`.

Failure policy:
- Enabled mode (`REMOTE_EXECUTION=1`): fail fast on first blocking issue and
  stop the phase with remediation guidance.
- Disabled mode (`REMOTE_EXECUTION=0`): no blocking behavior and no extra
  required steps.

Validation classes:
1. Presence: configured path exists.
2. Syntax: valid JSON parse.
3. Contract: required fields/types/enums.
4. Semantics: cross-field checks (default target exists/enabled, unique ids).
5. Security: deny secret-like inline values in config.

### 4) Error reporting model

All validation failures must be actionable and include:
- failing location (`path`, for example `targets[0].port`)
- expected rule (`integer 1..65535`)
- actual value/type
- remediation hint

Message pattern:
`[REMOTE_CONFIG_ERROR] <path>: expected <rule>, got <actual>. Fix: <hint>.`

Examples:
- `[REMOTE_CONFIG_ERROR] .cursor/remote.json: file not found. Fix: create from template/.cursor/remote.json or set REMOTE_EXECUTION=0.`
- `[REMOTE_CONFIG_ERROR] targets[1].type: expected one of [docker, ssh, vm], got "k8s". Fix: use a supported type or extend contract in a new decision record.`
- `[REMOTE_CONFIG_ERROR] targets[0].auth.token: inline secret-like value detected. Fix: use auth.mode=env and reference tokenEnv.`

### 5) Security model

Security posture:
- Never commit tokens, passwords, private keys, or API secrets in
  `.cursor/remote.json`.
- Only commit environment-variable references (for example `tokenEnv`,
  `passwordEnv`, `privateKeyPathEnv`) or safe placeholders.
- Treat any secret-like literal in config as validation failure when remote is
  enabled.

Scope boundary:
- In scope: configuration contract and safety guidance.
- Out of scope: external secret manager integration or transport protocol work.

### 6) Docs integration model

Documentation updates required by design:
- `README.md`: user-facing remote setup, two target examples, and mode behavior
  (`REMOTE_EXECUTION` off/on).
- `docs/engineering/runbook.md`: operator-oriented validation contract,
  fail-fast expectations, and troubleshooting messages.

Doc parity expectation:
- README and runbook must describe the same contract and failure behavior with
  no contradictions.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split cleanly into:
1. Create canonical active/template `remote.json` artifacts with safe examples.
2. Document contract schema and allowed values.
3. Implement/define validation checks and error message contract.
4. Add security guidance and secret-prohibition checks.
5. Update README and runbook with remote setup + mode-specific expectations.
6. Verify parity across active/template files and docs references.

---

# US-0037: Mid-Process `/auto` Continuation with Deterministic Resume Point

## Overview

US-0037 adds deterministic continuation semantics for `/auto` so teams can
restart from mid-process with one command and continue remaining phases without
manual phase triggers. The design is workflow-level orchestration only. It does
not change phase deliverables, decision gates, or runtime product behavior.

## Assumption challenge and alternatives

### Option A: Keep implicit behavior only

Pros:
- No command contract changes.
- Lowest immediate implementation effort.

Cons:
- Resume behavior stays inference-heavy and non-deterministic.
- Ambiguous source resolution can silently choose the wrong phase.
- Does not satisfy ACs for explicit `start-from`, fail-fast conflicts, and
  inspectable breadcrumbs.

### Option B: Resume-only continuation (no `/auto start-from`)

Pros:
- Simpler than full unification.
- Reuses `resume_brief.md` as primary source.

Cons:
- No explicit operator override for urgent/manual recovery cases.
- Still weak when resume brief is stale/missing and state fallback is needed.
- Splits semantics across `/resume` and `/auto` instead of one deterministic
  control model.

### Option C: Unified deterministic model (chosen)

Pros:
- Explicit `/auto start-from=<phase>` override for intentional control.
- Deterministic source precedence when no override.
- Fail-fast on ambiguity/staleness/conflict rather than guessing.
- One-command continuation through remaining phases with existing stop rules.

Cons:
- Slightly more command/rule documentation work.
- Requires explicit conflict/error contract and breadcrumb schema.

## Minimal architecture

### 1) Canonical phase IDs and validation

Accepted canonical IDs for `start-from`:
- `intake`
- `discovery`
- `research`
- `architecture`
- `sprint-plan`
- `plan-verify`
- `execute`
- `qa`
- `verify-work`
- `release`
- `refresh-context`

Validation policy:
- Unknown/non-canonical phase -> fail fast.
- Alias forms are not accepted in v1 (`sprint_plan`, `verifywork`, etc.) to
  keep behavior deterministic.

### 2) Deterministic resume-source precedence

When `/auto` is invoked, resolve start phase in strict order:

1. **Explicit override**: command argument `start-from=<phase>`.
2. **Resume brief source**: `handoffs/resume_brief.md` intended resume phase.
3. **State fallback source**: infer next phase from `docs/engineering/state.md`.
4. **Fail-fast**: if unresolved, ambiguous, conflicting, or stale.

Deterministic rule:
- Once a higher-priority source resolves validly, lower sources are ignored for
  phase selection (but can still be used for consistency checks and warnings).

### 3) Conflict and staleness policy

Resolver outcomes:
- `resolved`: exactly one valid phase source selected by precedence.
- `conflict`: sources disagree and no explicit override exists.
- `stale`: source exists but points to an invalid/outdated context.
- `missing`: required data not present.
- `ambiguous`: multiple possible phases inferred from same source.

Policy:
- If explicit `start-from` is valid, proceed and record that it overrides other
  sources.
- If no explicit override and `resume_brief` conflicts with `state` inference:
  fail fast with actionable remediation.
- If `resume_brief` exists but is stale/unparseable, do not silently skip to
  state; fail fast and request cleanup or explicit override.
- Use `state` fallback only when `resume_brief` is genuinely absent.
- If state inference is ambiguous/unrecoverable, fail fast.

### 4) Error messaging contract (fail-fast)

All resolver failures must return a structured message contract:

`[AUTO_RESUME_ERROR] <code>: <summary>. Source=<source>. Fix: <action>.`

Required codes:
- `INVALID_START_FROM`
- `RESUME_BRIEF_MISSING`
- `RESUME_BRIEF_STALE`
- `RESUME_BRIEF_UNPARSEABLE`
- `RESUME_STATE_CONFLICT`
- `STATE_PHASE_AMBIGUOUS`
- `STATE_PHASE_UNRECOVERABLE`

Examples:
- `[AUTO_RESUME_ERROR] INVALID_START_FROM: "planverify" is not a canonical phase. Source=argument. Fix: use one of [intake..refresh-context].`
- `[AUTO_RESUME_ERROR] RESUME_STATE_CONFLICT: resume_brief=qa, state_inferred=verify-work. Source=resolver. Fix: run /resume to reconcile artifacts or rerun /auto start-from=<phase>.`

### 5) State fallback inference contract

`docs/engineering/state.md` fallback is intentionally conservative:
- Infer from latest explicit boundary/checkpoint statements that indicate
  "ready for <phase>" or "paused at <phase>".
- If multiple candidate phases are present in latest state slice, mark
  ambiguous and fail.
- If no trustworthy boundary phrase exists, mark unrecoverable and fail.

This keeps inference deterministic and avoids hidden heuristics.

### 6) One-command continuation flow (remaining phases only)

After phase resolution, `/auto` executes remaining phases in canonical order,
starting at resolved phase, preserving existing behavior:
- Fresh subagent per phase.
- Existing execute/QA loop behavior when `AUTO_IMPLEMENTATION_LOOP=1`.
- Existing optional security review steps when `SECURITY_REVIEW=1`.
- Existing stop conditions remain unchanged:
  - decision gate
  - missing critical input
  - pause request (`AUTO_PAUSE_REQUEST=1` at safe boundary)
  - loop max cycles reached

No gate bypass is allowed in continuation mode.

### 7) Observability and breadcrumb contract

Continuation must write deterministic breadcrumbs to artifacts so behavior is
auditable.

Minimum breadcrumb fields:
- `invocation_mode` (`auto`)
- `requested_start_from` (value or `none`)
- `resolved_start_phase`
- `resolution_source` (`argument|resume_brief|state_fallback`)
- `resolution_status` (`resolved|fail-fast`)
- `stop_reason` (`completed|decision_gate|missing_input|pause_request|loop_max`)
- `stop_phase`
- `timestamp`

Artifact update targets:
- `docs/engineering/state.md`: append a concise continuation checkpoint summary.
- `handoffs/resume_brief.md` (when stopped before completion): update intended
  resume phase plus stop reason and last completed phase.

### 8) Backward compatibility and safe defaults

- Existing manual workflows remain unchanged.
- `/resume` continues to work for context loading and status reporting.
- `/auto` gains explicit deterministic continuation behavior only when invoked.
- If no explicit `start-from` is provided, legacy users still get automatic
  continuation — now with deterministic source policy and fail-fast safety.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split into:
1. Define parser/validator for `start-from` canonical phase IDs.
2. Implement precedence resolver with strict conflict/staleness outcomes.
3. Implement fail-fast error message contract and user remediation text.
4. Implement conservative `state.md` inference helper with ambiguity handling.
5. Wire continuation flow to existing stop conditions (no behavior bypass).
6. Add breadcrumb writing contract to `state.md` and `resume_brief.md`.
7. Align `/auto`, `/resume`, `/pause` command guidance and template parity.

---

# US-0038: Phase-Triggered Sync Policy with Guarded Auto-Push

## Overview

US-0038 defines workflow-level sync policy semantics at phase boundaries. The
goal is deterministic and safe synchronization behavior with zero-overhead
defaults when automation is disabled. This architecture does not implement a
runtime git orchestrator; it defines policy contracts, gates, and artifacts.

## Assumption challenge and alternatives

### Option A: Always auto-push after every phase

Pros:
- Simple to explain.
- Frequent backups to remote.

Cons:
- Violates QA-first safety for feature work.
- High risk of pushing unstable/incomplete changes.
- Conflicts with teams that intentionally stay manual.

### Option B: Manual sync only

Pros:
- Maximum user control and least automation risk.
- Already compatible with existing workflow habits.

Cons:
- No deterministic cadence policy when teams want guarded automation.
- Misses requested phase/milestone trigger model.

### Option C: Policy-driven guarded auto-sync (chosen)

Pros:
- Supports disabled/manual/by-phase/by-milestone/custom modes.
- Enforces mandatory pre-push checks and QA-first restrictions.
- Preserves manual behavior and keeps default non-disruptive.

Cons:
- More policy/evidence fields to maintain in artifacts.

## Minimal architecture

### 1) Sync policy control model

Canonical policy object (stored in workflow artifacts/command context):
- `mode`: `disabled|manual|by_phase|by_milestone|custom_phase_list`
- `custom_phases[]`: canonical phase IDs (used only in `custom_phase_list`)
- `allow_auto_push`: `0|1` (default `0`)
- `auto_push_branch_allowlist[]`: explicit branch names/patterns allowed for
  auto-push
- `optional_checks_enabled`: inferred from runbook command presence

Mode semantics:
- `disabled`: no policy evaluation and no sync attempts.
- `manual`: only user-invoked sync; no auto-triggered sync.
- `by_phase`: evaluate eligibility on every phase-completion boundary.
- `by_milestone`: evaluate only at milestone completion boundary.
- `custom_phase_list`: evaluate only when completed phase matches configured
  list.

Default-safe posture:
- Default mode is non-auto (`manual` or `disabled`).
- If unset/invalid, fail closed to `manual`.

### 2) Guarded auto-push eligibility model

Policy evaluation runs only at phase completion boundaries. A sync attempt is
eligible only when all conditions are true:
1. Boundary trigger matches configured mode.
2. `allow_auto_push=1`.
3. QA-first guard passes for feature work:
   - before QA pass, auto-push is forbidden;
   - manual user-invoked sync is still allowed.
4. No unresolved blocking QA findings / critical unresolved issues.
5. Branch safety guard passes (see below).
6. Mandatory pre-push check chain passes.

If any condition fails, result is deterministic `no_push` with reason code.

### 3) Branch safety constraints

Auto-push branch policy:
- Deny auto-push to protected/default branches by default.
- Allow auto-push only on explicitly allowlisted branches.
- If branch is unknown/unclassified, fail closed (no auto-push).
- Manual push behavior remains unchanged and user-controlled.

### 4) Mandatory pre-push check chain

Pre-push chain order (deterministic):
1. `TEST_COMMAND` (mandatory baseline).
2. `LINT_COMMAND` (if configured and non-empty).
3. `TYPECHECK_COMMAND` (if configured and non-empty).

Rules:
- Missing/blank `TEST_COMMAND` blocks push.
- Test failure/timeout blocks push.
- Optional checks are skipped only when not configured.
- Optional check failures block push when configured.
- Result details must show which checks ran, skipped, passed, or failed.

This aligns with existing `validate-and-push` scripts where tests are already
required before push.

### 5) Observability and evidence artifacts

Canonical sync evidence destination:
- `docs/engineering/state.md` (session status + latest gate verdict)
- `handoffs/dev_to_qa.md` or phase handoff context as needed

Recommended structured entry fields per sync attempt:
- `sync_id` (`SYNC-xxxx`)
- `timestamp`
- `phase_boundary`
- `policy_mode`
- `trigger_source` (`manual|auto`)
- `branch`
- `checks` (`test`, `lint`, `typecheck` with `pass|fail|skipped`)
- `qa_status_snapshot`
- `push_decision` (`pushed|blocked|not_eligible`)
- `reason_code`
- `evidence_refs` (paths to runbook/sprint findings/test reports)

Reason code examples:
- `SYNC_DISABLED`
- `MANUAL_MODE_NO_AUTO`
- `PRE_QA_AUTOPUSH_FORBIDDEN`
- `BLOCKING_QA_FINDINGS`
- `BRANCH_NOT_ALLOWLISTED`
- `TEST_COMMAND_MISSING`
- `TEST_FAILED`
- `OPTIONAL_CHECK_FAILED`
- `SYNC_PUSHED`

### 6) Compatibility constraints

- Keep existing stop conditions and decision gate behavior unchanged.
- Preserve manual mode semantics; no forced push path is introduced.
- Keep optional runbook checks optional; only `TEST_COMMAND` is mandatory.
- Maintain active/template behavioral parity for command/rule/doc updates.

## Sprint-plan readiness (decomposition-ready)

Implementation should split into:
1. Define sync policy schema + defaults in workflow docs/command guidance.
2. Add phase-boundary eligibility evaluation contract and reason codes.
3. Define branch safety deny/allowlist policy for auto-push.
4. Align pre-push check contract with runbook commands and script semantics.
5. Add deterministic sync evidence format to state/handoff artifacts.
6. Add QA scenarios for pre-QA auto-push denial, check failures, and
   disabled/manual zero-overhead behavior.
7. Enforce active + `template/` parity for all touched behavior docs.

---

# US-0039: Release Gate Tightening for Check-In Tests and QA/UAT Completion

## Overview

US-0039 tightens `/release` readiness with deterministic mandatory gates and
explicit evidence requirements. The objective is to block release when check-in
tests, QA completion, or UAT completeness are missing/stale/failing. Evidence
flow is read-from-canonical-artifacts only; no inferred pass from absence of
evidence (per R-0020).

## Assumption challenge and alternatives

### Option A: Keep UAT-only gate in release

Pros:
- Minimal documentation changes.

Cons:
- Missing hard checks for check-in test status and QA completion.
- Permits inconsistent release readiness evidence.

### Option B: Single combined "quality gate"

Pros:
- Shorter release step text.

Cons:
- Non-deterministic ordering and weak auditability.
- Harder to diagnose exactly which prerequisite failed.

### Option C: Deterministic ordered gates with explicit evidence (chosen)

Pros:
- Clear pass/fail sequencing and remediation.
- Strong audit trail in release artifacts/state.
- No default bypass path.

Cons:
- Adds explicit gate reporting requirements.

## Minimal architecture

### 1) Release gates and evidence flow

- **Evidence flow**: Gates read from canonical evidence artifacts only. Pass is
  asserted only when evidence exists and indicates pass; missing or stale
  evidence never implies pass.
- **Canonical evidence sources**:
  - Check-in test: `tests/report.md` (or runbook-defined test output location).
  - QA completion: `sprints/Sxxxx/qa-findings.md` (no unresolved blocking
    findings in current sprint context).
  - UAT completion: `sprints/Sxxxx/uat.json`, `sprints/Sxxxx/uat.md` (no
    placeholder, incomplete, or unresolved-fail state).

### 2) Deterministic gate order

Release gate sequence is fixed and documented; ordering is enforced so audit
trails are unambiguous:

1. **Check-in test gate** — `TEST_COMMAND` baseline evidence.
2. **QA completion gate** — no unresolved blocking findings.
3. **UAT completion gate** — verified/populated UAT artifacts.
4. **Release notes + runbook update steps** — only after gates 1–3 pass.

No later gate is evaluated as pass if an earlier mandatory gate fails.

### 3) Stale and missing evidence behavior

- **Missing evidence**: Block release with deterministic reason code and
  remediation (e.g. run `TEST_COMMAND`, re-run QA, complete verify-work). Do not
  infer pass.
- **Stale evidence**: Block release when evidence is absent or does not satisfy
  validity criteria (e.g. evidence exists and passed; optional timestamp/re-run
  policy per runbook). Prefer simple rule: "evidence exists and passed" plus
  optional timestamp check rather than complex TTL.
- **Reason codes** (aligned with R-0020 and existing release vocabulary):
  - `RELEASE_SPRINT_UNRESOLVED` — sprint context not resolvable for release.
  - `RELEASE_TEST_FAILED` — check-in test run failed.
  - `RELEASE_TEST_STALE` — test evidence missing or stale; re-run required.
  - `RELEASE_QA_EVIDENCE_MISSING` — QA evidence absent for sprint context.
  - `RELEASE_QA_BLOCKERS_OPEN` — unresolved blocking findings in QA artifact.
  - `RELEASE_UAT_INCOMPLETE` — UAT placeholder or incomplete.
  - `RELEASE_UAT_FAILED` — UAT has unresolved fail state.
  - `RELEASE_GATE_OVERRIDE_APPROVED` — override with DEC reference (exception path only).

Each code must have documented remediation (what to fix, which artifact/command, next step).

### 4) No-bypass default and decision-gate override path

- **Default**: No release path may bypass test/QA/UAT gates. Default
  configuration has no bypass (per vision Discovery Notes — US-0039).
- **Override** (exception-only): Allowed only via explicit decision gate: user
  approval, documented rationale (e.g. `DEC-xxxx`), and audit trail. Release
  output must record override with `RELEASE_GATE_OVERRIDE_APPROVED` and DEC
  reference. See DEC-0019.

### 5) Auditable gate evidence

- Each gate writes pass/fail and evidence pointers to handoff/state artifacts so
  QA and TL can verify decisions; no silent or inferred state.
- Canonical destinations: release handoff, `sprints/Sxxxx/release-findings.md`,
  `docs/engineering/state.md` (as applicable).
- Per-gate verdict fields: gate name, status, reason_code, evidence_refs,
  remediation; for overrides, decision_ref (DEC-xxxx) required.

### 6) Compatibility constraints

- Keep existing workflow stop conditions and escalation semantics.
- Preserve teams with blank optional lint/typecheck commands from false
  failures (release still requires test + QA + UAT evidence only).
- Maintain active/template parity for gate semantics (see Template parity scope below).

## Template parity scope

Active and `template/` release/qa/execute guidance must stay behaviorally
aligned so installed repos get the same release-safety contract. Drift between
active and template causes inconsistent gate semantics for new installs.

**Canonical files for gate-semantics parity:**

- `.cursor/commands/release.md`
- `.cursor/commands/qa.md`
- `.cursor/commands/execute.md`
- Runbook sections covering release gates, reason codes, and evidence locations
- Release-findings and reason-code documentation (e.g. runbook, release command text)

**Mitigation:** (1) List these files in release checklist or parity
verification steps; (2) Include template-parity verification in release
checklist or regression tests; (3) Document gate order and reason codes in both
active and template copies.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Stale-evidence threshold too strict or ambiguous | Prefer "evidence exists and passed" plus optional timestamp check; avoid complex TTL. Document in runbook. |
| Template parity drift | Canonical file list above; parity check in release checklist or regression; gate order and reason codes documented in both active and template. |
| Over-strict validation blocks runs if evidence writes are incomplete | Deterministic reason codes and remediation guidance (which command/artifact to fix); fail closed only when gate evidence is required and missing/invalid. |
| Operator friction on override path | Override remains exception-only; explicit decision gate + DEC reference keeps audit trail and discourages casual bypass. |

## Decision linkage

- Research: R-0020, R-0005
- Decision: DEC-0019

## Sprint-plan readiness (decomposition-ready)

Implementation should split into:
1. Update `/release` gate contract with strict ordered gates.
2. Define freshness/validity criteria for "latest check-in test" evidence (simple rule preferred).
3. Add QA evidence contract checks for unresolved blockers.
4. Preserve and tighten UAT verified-state gate wording.
5. Add structured gate verdict logging to release notes/state/release-findings artifacts.
6. Define explicit decision-gate override template and constraints (DEC ref required).
7. Add QA regression matrix with positive/negative and stale-evidence cases.
8. Template parity: align and verify release/qa/execute and runbook sections per canonical file list.

---

# US-0040: Per-Sprint Release Notes and Release Queue Tracker

## Overview

US-0040 replaces single mutable release notes with sprint-scoped artifacts and a
canonical queue that tracks each sprint's release lifecycle state. The goal is
to prevent overwrite, preserve history, and make unreleased work visible before
release finalization.

Scope remains workflow/process-level only. No deployment runtime changes.

## Assumption challenge and alternatives

### Option A: Keep single mutable `handoffs/release_notes.md`

Pros:
- No new artifacts or migration.

Cons:
- Fails history preservation and non-overwrite requirements.
- Cannot represent multiple unreleased sprint states deterministically.

### Option B: Keep single file with appended history sections

Pros:
- Preserves one-file discoverability.
- Better history than overwrite model.

Cons:
- Queue state remains implicit and harder to validate.
- High risk of inconsistent section formatting and parsing ambiguity.
- Backfill and partial-release state tracking remain brittle.

### Option C: Per-sprint immutable notes + canonical queue index (chosen)

Pros:
- Deterministic per-sprint history with no cross-sprint overwrite.
- Explicit queue model (`planned -> ready -> unreleased -> released`) per sprint.
- Clear migration and failure-safe semantics.

Cons:
- Adds one queue artifact and compatibility pointer rules.

## Minimal architecture

### 1) Canonical artifacts

Release notes:
- `handoffs/releases/Sxxxx-release-notes.md` (primary, sprint-scoped)

Queue index:
- `handoffs/release_queue.md` (canonical release state tracker)

Backward-compatibility pointer file:
- `handoffs/release_notes.md` remains and is updated as "latest release pointer"
  + compatibility summary (no destructive rewrite of historical sprint notes).

### 2) Queue schema and states

Each queue row records at minimum:
- `sprint_id` (for example `S0010`)
- `story_refs` (one or more `US-xxxx`)
- `status` (`planned|ready|unreleased|released|blocked`)
- `last_updated` (ISO timestamp)
- `release_notes_ref` (`handoffs/releases/Sxxxx-release-notes.md`)
- `gate_snapshot` (test/qa/uat summary or reason code)
- `release_version` (optional until final release)

State semantics:
- `planned`: sprint exists but release flow not yet entered.
- `ready`: verify-work complete and release can be attempted.
- `unreleased`: release flow entered; notes created/updated; finalization not done.
- `released`: release finalization succeeded for that sprint.
- `blocked`: deterministic failure (for example unresolved sprint identity or gate
  failure) with remediation guidance.

### 3) Deterministic transition contract

Only the target sprint row may transition during one `/release` run:

1. Resolve sprint ID from current context.
2. If unresolved:
   - do not write any sprint notes file,
   - do not mutate another sprint's queue row,
   - add/update `blocked` queue entry keyed as `UNKNOWN` with reason code
     (`RELEASE_SPRINT_UNRESOLVED`) and remediation.
3. If resolved:
   - ensure queue row exists (create if missing),
   - set row to `unreleased`,
   - write/update only `handoffs/releases/Sxxxx-release-notes.md`,
   - keep other sprint rows untouched.
4. On successful gate completion + finalization:
   - transition same row `unreleased -> released`,
   - update `release_version`/timestamp,
   - refresh compatibility pointer in `handoffs/release_notes.md`.
5. On failure after notes write:
   - keep row in `unreleased` or `blocked` with reason code,
   - never delete or overwrite other sprint note files.

### 4) Backward compatibility contract

`handoffs/release_notes.md` remains supported and becomes:
- latest release summary for the most recently finalized sprint,
- pointer list to recent per-sprint files,
- explicit note that canonical history lives under `handoffs/releases/`.

Existing workflows reading `handoffs/release_notes.md` continue to work for
"latest release" use cases, while full history is preserved per sprint.

### 5) Migration/backfill contract

One-time migration policy for legacy `handoffs/release_notes.md`:

1. Attempt to resolve sprint identity from legacy file content and state context.
2. If resolvable:
   - create `handoffs/releases/Sxxxx-release-notes.md` using legacy content,
   - preserve original legacy file content (append compatibility pointer section).
3. If not resolvable:
   - keep legacy file unchanged,
   - add queue note in `handoffs/release_queue.md` with `blocked` status and
     reason `LEGACY_NOTES_SPRINT_UNRESOLVED`,
   - include manual migration guidance.

Migration is non-destructive and repeat-safe (idempotent by sprint file existence
check).

### 6) Failure-safe behavior for metadata inconsistency

When queue and notes metadata disagree (missing file, wrong status, missing row):
- fail closed for release finalization (no forced `released` transition),
- preserve existing note artifacts as-is,
- write deterministic reason code in queue row:
  - `QUEUE_ENTRY_MISSING`
  - `NOTES_REF_MISSING`
  - `STATUS_TRANSITION_INVALID`
  - `RELEASE_SPRINT_UNRESOLVED`
- provide remediation steps (rebuild row, restore ref, rerun `/release`).

No automatic destructive reconciliation is allowed.

### 7) Ownership and phase touchpoints

- `/verify-work`: marks sprint release-candidate readiness (`ready`) in state
  context.
- `/release`: owns transitions `ready -> unreleased -> released` and note file
  generation/update for target sprint only.
- `/refresh-context`: curates queue readability, keeps stale blocked entries
  visible, and preserves historical integrity.

### 8) Template parity requirements

Implementation must keep active and `template/` guidance aligned for:
- `.cursor/commands/release.md` (new queue + per-sprint notes semantics)
- related rules/handoff guidance where release artifact paths are referenced
- placeholder artifacts for `handoffs/release_queue.md` and
  `handoffs/releases/` conventions.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split into:
1. Add canonical artifact contracts and queue schema docs.
2. Add resolver + fail-safe transition semantics in release guidance.
3. Add migration/backfill steps for legacy `handoffs/release_notes.md`.
4. Add backward-compatible pointer behavior in legacy release notes file.
5. Add QA matrix for unresolved sprint, overwrite prevention, queue-note mismatch,
   migration success/failure, and active/template parity.

---

# US-0046: Explicit `/sprint-plan --bulk` Mode

## Overview

US-0046 adds an explicit bulk planning mode for `/sprint-plan` so multiple OPEN
stories can be planned in one bounded run. The architecture keeps current
single-scope behavior as default and adds deterministic selection/grouping rules
only when bulk mode is explicitly enabled.

## Assumption challenge and alternatives

### Option A: Keep current `/sprint-plan` behavior only

Pros:
- No command contract changes.
- Lowest implementation complexity.

Cons:
- Does not satisfy the requirement for explicit multi-story planning throughput.
- Forces repetitive manual planning runs for large backlogs.

### Option B: Implicitly auto-bulk whenever many OPEN stories exist

Pros:
- Minimal user input.
- High throughput potential.

Cons:
- Ambiguous operator intent.
- High risk of surprising large planning mutations.
- Harder to audit and bound safely.

### Option C: Explicit bulk planning trigger with bounded deterministic policy (chosen)

Pros:
- Clear operator intent and safer defaults.
- Deterministic selection/grouping output.
- Predictable bounded behavior with explicit stop reasons.

Cons:
- Adds policy controls and additional regression surface.

## Minimal architecture

### 1) Explicit mode trigger and defaults

- Add an explicit trigger for bulk planning in `/sprint-plan` (flag/argument).
- Default behavior without trigger remains current non-bulk planning.
- Invalid or ambiguous bulk arguments fail safe with actionable guidance.

### 2) Deterministic story selection policy

Selection order:
1. Story priority (highest first)
2. Backlog order (stable tie-breaker)

Policy requirements:
- Stable ordering for reproducibility.
- No hidden randomness.
- Story selection evidence logged in planning breadcrumbs.

### 3) Bounded planning controls

Required controls:
- max stories per bulk run
- max generated sprints per run

Stop outcomes must be deterministic and recorded:
- reached max stories
- reached max generated sprints
- no eligible OPEN stories
- blocked by missing/ambiguous acceptance

### 4) Grouping and splitting contract

Bulk planning uses deterministic grouping:
- prefer single-story sprints by default,
- allow multi-story grouping only when estimated task count remains within
  `SPRINT_MAX_TASKS`,
- if estimated size exceeds threshold and `SPRINT_AUTO_SPLIT=1`, split and
  continue within run bounds.

No grouping rule may bypass sizing safety controls.

### 5) Artifact completeness and traceability

For each generated sprint, planning output must be complete:
- `sprint.md`
- `tasks.md`
- `progress.md`
- UAT placeholders
- `plan-verify` readiness contract

Traceability updates in `state.md` must remain deterministic and non-duplicative.

### 6) Risk model

| Risk | Mitigation |
|------|------------|
| Bulk run plans too much at once | bounded max stories/sprints controls + explicit stop reasons |
| Story starvation in repeated bulk runs | deterministic priority ordering with stable backlog tie-break and periodic fairness review |
| Incomplete generated artifacts | enforce per-sprint completeness checklist before moving to next item |
| Confusing behavior change for current users | explicit mode trigger; default non-bulk behavior unchanged |

## Decision linkage

- Research basis: `R-0010`, `R-0011`, `R-0013`
- Decision: `DEC-0023`

---

# US-0047: Explicit Bulk Execute Orchestration Mode

## Overview

US-0047 introduces explicit bulk execution orchestration that processes planned
sprints/stories continuously while preserving strict fresh-context isolation,
execute↔QA loop controls, and deterministic stop/skip behavior. In team mode,
execution must be scoped to member-owned tasks only.

## Assumption challenge and alternatives

### Option A: Rely only on existing `/auto` flag combinations

Pros:
- Reuses current functionality.
- No new command-level contract.

Cons:
- Operator intent remains implicit and easier to misconfigure.
- Team-member task scoping is not explicit in execution contract.
- Harder to communicate/verify bounded behavior per run.

### Option B: Global bulk execute without team-scope enforcement

Pros:
- Maximum throughput in single-user scenarios.

Cons:
- Unsafe for concurrent team members.
- High duplicate-work and task-collision risk.

### Option C: Explicit bulk execute mode with team-scoped guardrails (chosen)

Pros:
- Clear activation semantics and safer defaults.
- Enforces member/task scope in team mode.
- Keeps bounded and auditable behavior.

Cons:
- Requires additional scope-check logic and reason-code coverage.

## Minimal architecture

### 1) Explicit mode trigger and defaults

- Define explicit bulk execute mode (new command or explicit mode argument).
- Without explicit trigger, keep current non-bulk execution behavior.
- Invalid/ambiguous trigger input fails safe with remediation.

### 2) Work-item selection and breadcrumbs

Selection policy must be deterministic and logged:
- selected sprint/story id
- selection policy source
- team-context snapshot (when enabled):
  `TEAM_MODE`, `TEAM_MEMBER`, `ACTIVE_TASK_IDS`

### 3) Isolation and loop contract

- Fresh subagent context is mandatory per phase for each item.
- Fresh subagent context is mandatory for each execute↔QA loop cycle.
- Loop bounds (`AUTO_IMPLEMENTATION_LOOP`, max cycles) apply per item.

### 4) Team-scope enforcement model

When `TEAM_MODE=1`:
- only tasks in `ACTIVE_TASK_IDS` for the current `TEAM_MEMBER` are executable,
- pre-mutation scope validation is mandatory before task execution writes,
- out-of-scope tasks must be handled deterministically:
  - `skip` with reason code, or
  - `block` with reason code based on configured policy,
- no writes are allowed for out-of-scope tasks.

### 5) Bounded controls and stop policy

Required bounded controls:
- max items per run
- block handling policy (`stop` or `skip`)

Deterministic stop/skip outcomes:
- max items reached
- blocked item stop
- blocked item skipped
- no eligible scoped items
- decision gate pause

### 6) Resume semantics

Interrupted bulk runs require deterministic checkpoint fields:
- last completed item
- next candidate item
- stop reason
- stop phase
- team-context snapshot (if team mode)

Resume must continue safely from recorded checkpoint state.

### 7) Risk model

| Risk | Mitigation |
|------|------------|
| Duplicate or conflicting team execution | member-scope filter + no-write rule for out-of-scope tasks |
| Long unattended runs hide failures | bounded controls + deterministic reason-code breadcrumbs |
| Context bleed between items | fresh subagent per phase and per execute↔QA cycle |
| Ambiguous resume after interruption | explicit checkpoint schema with next-item and stop metadata |

## Decision linkage

- Research basis: `R-0010`, `R-0012`, `R-0013`
- Decision: `DEC-0024`

---

# US-0048: Enforced Per-Phase Subagent Isolation with Audit Gate

## Overview

US-0048 makes per-phase subagent isolation a hard-enforced workflow contract with
auditable evidence and fail-closed gates. Policy text already mandates isolation
(DEC-0007, US-0023); this story adds mandatory evidence writing, deterministic
reason codes, and blocking behavior at progression and release when evidence is
missing or violated.

Scope: workflow contract enforcement, evidence schema, gates, reason codes,
regression coverage. Out of scope: runtime product feature changes, external
orchestration platform migration.

## Assumption challenge and alternatives

### Option A: Advisory-only (logging deviation, no gates)

- **Pros**: Low effort; no blocking.
- **Cons**: Does not close recurrence risk; user reported breach was execution
  in one context instead of fresh subagent per phase. Rejected as insufficient.

### Option B: Hard enforcement + auditable evidence + fail-closed gates (chosen)

- **Pros**: Closes compliance gap; deterministic detection and blocking;
  operator gets explicit diagnostics (reason code, phase, evidence ref,
  remediation). Aligns with PO recommendation and vision discovery notes.
- **Cons**: Higher effort; evidence write discipline required; possible friction
  if evidence writes are inconsistent. Mitigated by clear schema, remediation
  guidance, and bounded migration for legacy artifacts.

## Minimal architecture

### 1) Components and data flow for isolation evidence

- **Orchestrator** (`/auto`): Must not execute phase work in-process; must
  spawn/trigger fresh subagent context per phase and per execute↔QA cycle.
  Reads handoffs and state; writes phase-boundary breadcrumbs and delegates
  phase execution to a new context.
- **Phase executors** (each phase command run in its role): On phase start/completion,
  write **isolation evidence** to canonical locations (see below). Evidence is
  the only cross-phase proof of fresh-context execution.
- **Gate evaluators** (`/verify-work`, `/release`): Before allowing progression
  or release finalization, read canonical isolation evidence for the current
  sprint/phase span; if required evidence is missing or invalid, block with
  deterministic reason code and remediation.
- **Canonical evidence store**: Single authoritative place where isolation
  evidence is written and read for gates. Recommended: a dedicated section in
  `docs/engineering/state.md` and/or phase-scoped footers in handoffs, plus
  optional append-only `docs/engineering/isolation-evidence.log` or equivalent
  for machine-checkable audit. Schema below.

Data flow:

1. Phase N starts in a **new** subagent context → executor writes isolation
   evidence (phase_id, role, fresh_context_marker, timestamp, evidence_ref).
2. Phase N completes → handoff written; evidence may be appended/updated for
   phase N completion.
3. Before phase N+1 or before verify-work/release, gate evaluator reads
   evidence for completed phases in scope; if any required row is missing or
   invalid → fail closed, emit reason code and remediation.
4. Pause/resume: resume checkpoint carries isolation provenance (last phase
   with valid evidence, evidence_ref) so continuation does not silently reuse
   context.

### 2) Isolation evidence schema (minimal)

Required fields (per phase boundary):

- `phase_id`: canonical phase identifier (e.g. intake, discovery, architecture,
  sprint-plan, execute, qa, verify-work, release, refresh-context).
- `role`: agent role that executed the phase (po, tech-lead, dev, qa, release,
  curator).
- `fresh_context_marker`: value attesting new context (e.g. session id or
  explicit "fresh" token; format defined in runbook).
- `timestamp`: ISO 8601.
- `evidence_ref`: pointer to this evidence record (e.g. state.md section id or
  log line id).

Optional for resume provenance:

- `session_id`, `parent_phase` (for chained continuation).

Canonical locations:

- Primary: `docs/engineering/state.md` — dedicated "Isolation evidence" section
  with one block per phase transition (sprint/phase scoped).
- Alternative/append: handoff footers or `docs/engineering/isolation-evidence.log`
  (append-only) for gate scripts to parse. Runbook documents where gates read
  from.

### 3) Reason-code taxonomy (isolation violations)

Deterministic codes for gate output and remediation:

| Code | Meaning | Remediation |
|------|---------|-------------|
| `PHASE_CONTEXT_ISOLATION_MISSING` | Required isolation evidence for one or more phases is absent | Run the missing phase(s) in a fresh subagent context and ensure evidence is written; re-run gate. |
| `PHASE_CONTEXT_ISOLATION_VIOLATION` | Evidence indicates reused context (e.g. same session across phases) or invalid role/phase mapping | Re-run affected phase(s) in a fresh context; correct role/phase mapping in commands. |
| `ISOLATION_EVIDENCE_STALE` | Evidence timestamp or scope does not match current sprint/phase span | Re-run phase(s) or refresh evidence; ensure state/handoffs are current. |
| `ISOLATION_EVIDENCE_INVALID` | Schema violation (missing required field, malformed) | Fix evidence schema in artifact or in writer (command/agent); re-run phase. |

Remediation guidance must be explicit in gate output (reason code, phase id,
evidence ref, suggested next action).

### 4) Verify-work and release gate placement and precedence

- **Verify-work**: Before marking verify-work as PASS, run an **isolation-compliance
  gate**: for the current sprint, all phases that should have been executed
  (from sprint start through execute and QA) must have valid isolation evidence.
  If not, verify-work outcome is BLOCKED; output includes reason code and
  remediation. Order: other verify-work checks (e.g. UAT) may run first or in
  parallel; isolation gate must pass before verify-work is considered complete.
- **Release**: Before release finalization, run the same **isolation-compliance
  gate** for the sprint being released. If isolation evidence is missing or
  invalid, release is blocked; release command output includes reason code,
  phase(s) affected, evidence ref, remediation. Gate order: check-in test →
  QA → UAT → **isolation compliance** → release notes/queue update. Isolation
  gate does not replace other gates; it is an additional mandatory gate.

Precedence: Isolation gate is mandatory and fail-closed. No bypass in default
configuration; any override requires explicit decision gate and documented
rationale (same pattern as US-0039 release overrides).

### 5) Pause/resume provenance behavior

- On **pause**: Persist current phase, last completed phase, and evidence_ref
  (or equivalent) for the last phase with valid isolation evidence in
  `handoffs/resume_brief.md` and/or `docs/engineering/state.md`.
- On **resume**: Resolver uses resume checkpoint; continuation must not assume
  the same context is still valid. Next phase must run in a **new** subagent
  context and write new isolation evidence. Breadcrumbs must record
  `resolved_start_phase`, `isolation_evidence_ref_at_resume`, and
  `continuation_fresh_context_required=true` so that gate evaluators can require
  evidence for the resumed phase and subsequent phases.
- Isolation evidence must **survive** pause/resume: evidence written before
  pause remains valid for gate checks after resume; no ambiguity that "resumed"
  implies reuse of pre-pause context for new work.

### 6) Active/template parity requirements

- Command contracts (`/auto`, `/execute`, `/qa`, `/verify-work`, `/release`)
  that define isolation semantics, evidence-writing steps, and gate behavior
  must be updated in both active repo and `template/` so that new installs
  get the same enforcement.
- Runbook and README must document: isolation evidence schema, canonical
  locations, reason-code list, and remediation guidance. Parity required for
  active and template copies.
- Regression coverage (positive: valid evidence allows progression; negative:
  missing evidence, reused context, invalid role/phase) must be reflected in
  test/QA guidance in both active and template where applicable.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-strict validation blocks runs when evidence writes are incomplete | Clear schema and runbook steps; remediation guidance; optional bounded migration or legacy handling for repos without prior evidence. |
| Backward compatibility: existing artifacts lack new evidence fields | Gates apply to "required evidence for phases in scope"; legacy runs can define grace period or one-time migration that backfills or waives for pre-US-0048 sprints (documented). |
| Operator friction on first failure | Deterministic reason codes and explicit remediation (phase, evidence ref, next action) so operators can fix without guesswork. |
| Resume ambiguity | Provenance in resume checkpoint (evidence ref at resume, continuation requires fresh context) and documentation that resumed phase writes new evidence. |

## Decision linkage

- Research basis: `R-0018`, `R-0019`
- Decision: `DEC-0029`

# US-0050: Clean Install Hygiene and Complete Clean-Repo Coverage

## Context and scope

US-0050 addresses installer trust and determinism gaps observed in real installs:
partial cleanup with `--clean-repo`, seeded historical starter data in template
artifacts, and starter references that look like cross-repo memory carryover.
Scope includes installer cleanup contract, template artifact neutrality, and
install/clean regression coverage. Out of scope: runtime product behavior and
non-workflow repository content.

## Assumption challenge and alternatives

### Option A: Keep per-installer hardcoded cleanup path lists

- **Pros**: Lowest immediate implementation effort.
- **Cons**: Path drift risk across PS1/SH/PY; recurring partial cleanup defects.
  Rejected.

### Option B: Ownership manifest as single source of truth (chosen)

- **Pros**: Deterministic cleanup coverage, simpler parity verification, safer
  scope control (installer-owned only), easier regression testing.
- **Cons**: Requires introducing and maintaining one canonical ownership
  artifact and readers in each installer.

## Minimal architecture

### 1) Ownership contract

- Introduce a canonical installer-managed ownership manifest (for example
  `template/docs/engineering/context/installer-owned-paths.json`) that defines:
  - directory ownership entries
  - file ownership entries
  - optional exclusions/safety guards
- All installer entry points (`installer.ps1`, `installer.sh`, `installer.py`)
  consume this same manifest for:
  - install include scope
  - clean-repo deletion scope

### 2) Clean-repo execution model

- `--clean-repo` resolves managed paths from ownership manifest.
- Delete only installer-owned paths that exist in target repo.
- Never traverse or delete paths outside manifest ownership boundaries.
- Emit deterministic cleanup summary (removed paths + skipped missing paths).

### 3) Template neutrality rules

- Starter artifacts in `template/docs/engineering/*` must be neutral placeholders:
  no seeded operational history rows from this repository.
- Cross-references to concrete runtime IDs are allowed only when matching baseline
  records are intentionally shipped and documented; otherwise use neutral wording.

### 4) Regression coverage

- Add install/clean lifecycle assertions:
  - fresh install => no preloaded story/decision/research operational history rows
  - clean-repo => full removal of installer-owned artifacts
  - reinstall after clean => same clean baseline
  - parity across installer entry points
- Maintain US-0018 upgrade contract compatibility.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-cleaning deletes non-framework project files | Ownership manifest must be explicit allowlist only; no broad wildcard deletes. |
| Under-cleaning leaves artifacts behind | Regression tests assert full ownership set removal per installer path. |
| Template hygiene regresses over time | Add template neutrality checks in lifecycle test suite and release checklist. |

## Decision linkage

- Research basis: `R-0024`, `R-0025`
- Decision: `DEC-0032`

# US-0051: Intelligent Intake Decomposition and Risk-Aware PO Questioning

## Context and scope

US-0051 improves intake quality by splitting broad requests into multiple
independently valuable stories and by increasing PO follow-up depth when request
breadth/risk is high (not ambiguity-only). Out of scope: downstream execute/release
contracts and runtime feature implementation.

## Assumption challenge and alternatives

### Option A: Keep single-story default with larger AC lists

- **Pros**: Simpler logic; minimal behavior change.
- **Cons**: Oversized stories, weaker sprintability, lower traceability of split
  intent. Rejected.

### Option B: Deterministic decomposition heuristics + explicit user confirmation (chosen)

- **Pros**: Better backlog quality, bounded behavior, user authority retained,
  clearer sprint planning input.
- **Cons**: More intake logic and documentation; requires robust heuristics to
  avoid over-splitting.

## Minimal architecture

### 1) Decomposition evaluator

- Add intake-time evaluator that scores request breadth using heuristics:
  - feature count / workflow-step count
  - cross-cutting impact surface
  - acceptance set size
  - risk and unknown dependencies
- If score exceeds threshold, propose multi-story decomposition.

### 2) Split strategy

- Prefer vertical slices/workflow-step slices with independent value.
- Avoid technical-layer-only split output (frontend-only/backend-only stories).
- Persist split rationale in backlog and PO->TL handoff.

### 3) Adaptive questioning policy

- Keep `INTAKE_GUIDED_MODE=1` behavior but add risk-aware escalation:
  - ambiguity-based questions (existing)
  - risk/breadth-based questions (new)
- Keep question loop bounded (max rounds or stop when acceptance confidence is sufficient).
- Preserve explicit user choice to accept/merge/adjust proposed splits.

### 4) Low-touch compatibility

- `INTAKE_GUIDED_MODE=0` keeps low-touch path and mandatory duplicate check.
- No forced decomposition in low-touch mode unless user requests decomposition.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-splitting into too many tiny stories | Threshold + bounded split count + explicit user confirmation before persist. |
| Under-splitting broad requests | Include breadth and risk heuristics; emit rationale when staying single-story. |
| Endless follow-up loop | Bounded question rounds and deterministic stop conditions. |

## Decision linkage

- Research basis: `R-0024`, `R-0025`
- Decision: `DEC-0033`

# US-0052: Optional Fresh-Project ID Namespace Bootstrap

## Context and scope

US-0052 adds an optional bootstrap path for fresh repos so first IDs can start
at `US-0001` / `DEC-0001` / `R-0001`, while preserving current highest-existing-ID
continuation for non-fresh repositories. Out of scope: retroactive renumbering
or migration of existing histories.

## Assumption challenge and alternatives

### Option A: Always continue from highest discovered ID

- **Pros**: Simpler and backward compatible.
- **Cons**: Cannot satisfy fresh-project expectation in repos that want explicit
  namespace bootstrap semantics. Rejected as sole mode.

### Option B: Optional bootstrap mode with deterministic freshness checks (chosen)

- **Pros**: Supports fresh-project UX while maintaining compatibility in existing
  repos; no historical rewrites.
- **Cons**: Requires robust eligibility detection and collision safeguards.

## Minimal architecture

### 1) Bootstrap control

- Add explicit bootstrap control (flag or scratchpad/command argument), default off.
- Bootstrap applies only during eligible first-run/new-project initialization.

### 2) Freshness detection

- Determine eligibility from absence of existing `US-`, `DEC-`, and `R-` IDs in
  canonical artifacts.
- Emit deterministic diagnostics when bootstrap requested but repo is not fresh.

### 3) ID generation contract

- If bootstrap eligible and enabled: start at `0001`.
- Otherwise: continue from highest existing ID (current behavior).
- Never rewrite historical IDs.

### 4) Test coverage

- Add regression cases for:
  - fresh + bootstrap enabled
  - fresh + bootstrap disabled
  - non-fresh + bootstrap requested
  - mixed/partial artifact edge cases

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| ID collision in partially initialized repos | Multi-artifact freshness check and fail-fast diagnostics. |
| Operator confusion about bootstrap behavior | Clear README/runbook/help contract with examples and constraints. |
| Hidden behavior changes in existing repos | Default-off bootstrap and strict compatibility with highest-ID continuation. |

## Decision linkage

- Research basis: `R-0024`, `R-0025`
- Decision: `DEC-0034`

---

# US-0053: Context Compaction and Tiered Token-Cost Optimization Mode

## Overview

US-0053 introduces a deterministic token-efficiency control surface that reduces
recurring context volume while preserving workflow safety guarantees. The design
adds a tiered policy profile (`lean|balanced|full`), compact active-context
contracts for high-traffic artifacts, and a narrow-read retrieval strategy for
`/ask`.

## Challenge and alternatives

### Alternatives considered

1. **Manual per-flag tuning only** (no profile):
   flexible but error-prone; high operator overhead and inconsistent behavior.
2. **Single global token-saver on/off switch**:
   too coarse; insufficient control for teams needing intermediate depth.
3. **Tiered profile with documented override precedence** (selected):
   balances operator simplicity with deterministic, testable behavior.

### Simpler-path check

The selected architecture keeps existing features and safety gates, changing only
default intensity and retrieval scope. It avoids new runtime services or external
state stores and reuses existing artifact-first contracts.

## Minimal architecture

### 1) Token profile policy layer

- Add `TOKEN_PROFILE=lean|balanced|full` in scratchpad (default `balanced`).
- Define deterministic profile mapping to existing switches (automation looping,
  early research, intake depth, and optional overhead modes).
- Document explicit precedence:
  - mandatory gate invariants cannot be disabled by profile,
  - explicit manual flag overrides (when present) take precedence over profile
    defaults for documented keys.

### 2) Compact active-context contract

- Keep `docs/engineering/state.md` as canonical active evidence store but define
  a bounded **active context pack** section for routine reads.
- Archive older checkpoint blocks into versioned archive packs under a dedicated
  state-archive path; keep canonical references in active state.
- Compaction is append-safe and non-destructive: no historical deletion, only
  bounded active window + archive pointers.

### 3) Decisions index compaction

- Keep `docs/engineering/decisions.md` as compact current index:
  - current context pack,
  - bounded decision summary list,
  - canonical pointers to full `decisions/DEC-xxxx.md`.
- Prevent uncontrolled growth by moving long historical narrative detail to DEC
  records only.

### 4) `/ask` narrow-read retrieval strategy

- Update `/ask` policy to question-scoped retrieval:
  1. targeted section reads first (latest relevant checkpoints/story blocks),
  2. bounded expansion only when unresolved,
  3. explicit "not found in artifacts" response when evidence is absent.
- Preserve strict read-only behavior and zero artifact mutation contract.

### 5) Guardrail invariants

- Mandatory workflow gates remain unchanged:
  - `/qa` completion requirements,
  - `/verify-work` UAT completeness,
  - `/release` deterministic gate chain and isolation checks.
- Token savings are achieved via retrieval scope and default overhead intensity,
  not by removing safeguards.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Profile ambiguity causes inconsistent behavior | Publish deterministic profile mapping + precedence contract and regression tests. |
| Over-compaction hides needed evidence | Keep archive links canonical and require escalation path from active to archive reads. |
| Lean mode under-questions complex work | Document escalation guidance (`lean` -> `balanced`/`full`) and preserve manual override path. |
| Safety regression under token optimization | Lock mandatory gate invariants in tests and runbook contracts. |

## Decision linkage

- Research basis: `R-0027`, `R-0028`
- Decision: `DEC-0035`

---

# US-0054: Configurable Multi-Target Release Publish with Confirmation Gate

## Overview

US-0054 adds an optional post-release publish orchestration contract so each
repository can configure its own publish destinations (for example npm, choco,
brew, git, docker, cloud, custom servers) while enforcing a default confirmation
boundary before publish execution.

## Architecture goals

- Keep `/release` gate chain semantics unchanged and mandatory.
- Add publish-target behavior as a configuration-driven post-release layer.
- Support built-in target types and generic custom/SSH targets without hardcoded
  provider coupling.
- Fail fast on invalid target definitions with deterministic diagnostics.
- Preserve active/template parity and secret-safety contracts.

## Minimal architecture

1. **Target contract surface**
   - Canonical configurable target file under engineering docs (example schema).
   - Each target entry includes stable `id`, `type`, `enabled`, `order`,
     execution command/template, and optional environment/credential references.

2. **Execution mode control**
   - Scratchpad-controlled publish mode:
     - `disabled` (no publish step),
     - `confirm` (default; operator approval required),
     - `auto` (explicit opt-in).
   - Optional default target selection list, overridable per run.

3. **Target taxonomy**
   - Built-in `type` guidance for common destinations: `npm`, `choco`, `brew`,
     `git`, `docker`, `cloud`.
   - Generic `custom` target for arbitrary command workflows.
   - First-class `ssh` target with host/user/port/auth-reference/remote command.

4. **Safety and validation boundary**
   - Deterministic pre-execution validation for required fields and type
     constraints.
   - Env-reference-only sensitive values (`*Env` style) for tokens/passwords/keys.
   - Invalid or incomplete config blocks publish execution with explicit reason
     codes and no partial target side effects.

5. **Deterministic run semantics**
   - Explicit target selection (single/multi-target) per publish run.
   - Deterministic order by configured `order` then stable ID tie-break.
   - Disabled targets are skipped with explicit audit entries.

## Guardrail invariants

- Mandatory release quality gates remain unchanged:
  check-in tests -> QA -> UAT -> isolation -> release finalization.
- Publish target execution is additional post-release behavior and cannot bypass
  release evidence requirements.
- Existing story/decision/research ID semantics remain unchanged.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Ambiguous target config creates non-deterministic runs | strict schema and deterministic ordering rules |
| Missing confirmation triggers unintended publish | default `confirm` mode, explicit operator approval gate |
| Secret leakage in repo config | env-reference-only sensitive fields and fail-fast validation |
| Provider lock-in | built-in target guidance plus generic `custom` and `ssh` types |

## Decision linkage

- Research basis: `R-0029`, `R-0030`
- Decision: `DEC-0036`
- Boundaries: add configurable publish target layer only; do not alter mandatory
  `/release` gate chain contract.

---

# US-0055: Deterministic Status Reconciliation Command

## Overview

US-0055 adds a dedicated reconciliation command to normalize status drift across
canonical and derived workflow artifacts so continuation (`/auto`) can safely
resume from the correct next OPEN story and phase.

## Architecture goals

- Preserve canonical status ownership (`docs/product/backlog.md`).
- Reconcile derived artifacts deterministically (`acceptance`, `state`, `resume`).
- Keep mutation scope bounded to mismatched stories and linked derived entries.
- Emit auditable normalization evidence and deterministic reason codes.
- Preserve release-gate safety invariants and non-destructive history behavior.

## Minimal architecture

1. **New reconciliation command contract**
   - Add command (for example `/status-reconcile`) with deterministic detection,
     repair, and fail-closed blocked/conflict behavior.
   - Distinguish from `/memory-audit`:
     - `/memory-audit` remains read-only detection,
     - `/status-reconcile` performs bounded reconciliation writes.

2. **Canonical precedence model**
   - Authoritative source: backlog story `Status` (`OPEN|DONE`).
   - Derived surfaces:
     - `docs/product/acceptance.md` check rows,
     - backlog AC checkboxes for DONE stories,
     - `handoffs/resume_brief.md` next story + intended phase,
     - state reconciliation checkpoint.
   - If canonical status conflicts with release evidence, fail closed with reason
     code and remediation (no silent correction).

3. **Deterministic mutation boundaries**
   - Update only stories detected as mismatched.
   - Do not rewrite unrelated story blocks, sprint history, or narrative content.
   - Normalize DONE stories with unchecked ACs and acceptance drift in target scope.

4. **Auditability contract**
   - Write normalization evidence rows to canonical report artifact
     (`docs/engineering/status-normalization-report.md`):
     story ID, prior values, resolved values, evidence refs, timestamp.
   - Append reconciliation checkpoint in `docs/engineering/state.md`.

5. **Continuation readiness contract**
   - Recompute next OPEN story by canonical backlog priority/order.
   - Update `handoffs/resume_brief.md` deterministically:
     next actions, intended resume phase, latest breadcrumb metadata.

## Guardrail invariants

- Mandatory `/qa` -> `/verify-work` -> `/release` gate semantics remain unchanged.
- Reconciliation must not bypass release evidence requirements.
- No destructive rewrite of unrelated historical artifacts.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Over-broad repair mutates unrelated history | strict target-scoped mutation rules |
| Ambiguous conflict handling yields inconsistent outcomes | deterministic precedence + fail-safe reason codes |
| Hidden drift after repair | mandatory normalization report rows + state checkpoint evidence |

## Decision linkage

- Research basis: `R-0031`
- Decision: `DEC-0037`
- Boundaries: add reconciliation command and evidence contract only; do not
  change feature/runtime behavior beyond workflow status normalization.

---

# US-0056: Strict Runtime Proof for Per-Phase Subagent Isolation

## Overview

US-0056 strengthens the existing isolation contract by requiring runtime
attestation at each phase boundary. Artifact markers remain required, but `/auto`
must fail closed unless each completed phase provides valid, unique, fresh, and
linkable runtime proof.

## Architecture goals

- Add strict runtime attestation without weakening current isolation evidence.
- Enforce deterministic boundary validation and fail-closed continuation.
- Preserve pause/resume traceability with strict-proof provenance.
- Keep active/template parity and bounded compatibility handling for legacy runs.

## Minimal architecture

1. **Runtime attestation envelope**
   - Required fields per completed phase run:
     - `orchestrator_run_id`
     - `runtime_proof_id`
     - `phase_id`
     - `role`
     - `proof_issued_at` (UTC/RFC3339)
     - `proof_ttl_seconds`
     - `proof_hash` (deterministic hash over canonical tuple fields)
   - Evidence must be linked to canonical checkpoint in `docs/engineering/state.md`.

2. **Boundary validator in `/auto`**
   - After each phase, `/auto` validates attestation tuple and linkage before
     advancing.
   - Fail-closed reasons are deterministic:
     - `RUNTIME_PROOF_MISSING`
     - `RUNTIME_PROOF_INVALID`
     - `RUNTIME_PROOF_REUSED`
     - `RUNTIME_PROOF_STALE`
     - `RUNTIME_PROOF_AMBIGUOUS_LINK`

3. **Strict-proof provenance for pause/resume**
   - `handoffs/resume_brief.md` stores strict-proof provenance reference for last
     valid boundary.
   - Resume resolution fails closed when provenance is stale/unparseable or
     strict-proof chain cannot be validated.

4. **Gate integration**
   - Isolation/release verification consumes strict attestation in addition to
     existing artifact evidence fields from US-0048/DEC-0029.
   - No gate bypass: missing strict-proof evidence blocks continuation/release.

5. **Legacy compatibility contract**
   - No historical rewrite.
   - Legacy runs without strict attestation produce remediation guidance and
     deterministic blocked outcomes.

## Guardrail invariants

- `/auto` remains orchestration-only; phase work is still isolated by role.
- Strict runtime proof augments, not replaces, existing evidence requirements.
- Fail-closed behavior is mandatory on missing/invalid/reused/stale proof.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| False blocks due to tight freshness windows | bounded TTL defaults + clear remediation guidance |
| Proof-ID collision/reuse ambiguity | deterministic uniqueness constraints + reuse checks |
| Partial rollout causes parity drift | active/template contract parity + regression coverage |

## Decision linkage

- Research basis: `R-0034`
- Decision: `DEC-0038` accepted for strict attestation tuple + validator contract
- Boundaries: workflow orchestration proof contract only; no product runtime behavior changes.

---

# US-0057: Upgrade-Safe Scratchpad Example Refresh and Parity

## Overview

US-0057 tightens installer upgrade behavior so the framework-owned scratchpad
example is always refreshed while user-owned local overrides remain preserved.
The solution extends existing upgrade ownership semantics (US-0018/US-0050)
with explicit scratchpad-surface rules and deterministic operator diagnostics.

## Ownership model

- Framework-owned: `.cursor/scratchpad.local.example.md`
- User-owned: `.cursor/scratchpad.local.md`
- Mixed/shared defaults remain unchanged (`.cursor/scratchpad.md`).

## Upgrade behavior contract

In `--mode upgrade`, installers must:
1. Refresh framework-owned scratchpad example to latest release content.
2. Preserve user-owned local scratchpad with no overwrite path.
3. Emit deterministic diagnostics:
   - scratchpad example status (`added|updated|unchanged`)
   - user local file preservation signal when present.

## Parity and validation

- The same behavior is required in all installer implementations:
  - `installer.ps1`
  - `installer.sh`
  - `installer.py`
- Regression coverage validates:
  - framework refresh for example file,
  - preservation of user local overrides,
  - no regression in existing install/upgrade/clean guarantees.

## Decision linkage

- Research basis: `R-0032`
- Decision: `DEC-0039`

---

# US-0058: Deterministic Artifact Ordering and Write Discipline

## Overview

US-0058 standardizes write ordering across mutable workflow artifacts. The goal
is deterministic, idempotent artifact mutations so command reruns do not
oscillate insertion direction or reorder unrelated entries.

## Architecture goals

- Define one canonical ordering matrix for mutable artifact surfaces.
- Keep `state.md` checkpoint writes append-bottom only.
- Keep backlog/acceptance story ordering sorted-canonical and aligned.
- Enforce fail-safe behavior when insertion anchors are missing or ambiguous.
- Preserve canonical ownership guarantees from US-0045/US-0055.

## Minimal architecture

1. **Ordering matrix artifact**
   - New canonical policy file:
     `docs/engineering/artifact-ordering-policy.md`
   - Defines per-artifact policy: `append-bottom`, `prepend-top`,
     `sorted-canonical`.

2. **Command contract integration**
   - Commands that mutate ordering-sensitive artifacts must reference the matrix:
     `/auto`, `/intake`, `/release`, `/refresh-context`, `/status-reconcile`.
   - Command behavior must remain target-scoped; no broad rewrites.

3. **Fail-safe anchor handling**
   - Missing/ambiguous placement anchors trigger deterministic fail-closed code:
     `ARTIFACT_ORDERING_ANCHOR_AMBIGUOUS`.
   - No partial writes on fail-safe path.

4. **Idempotence requirement**
   - Re-running commands with no semantic changes must keep identical order.
   - No top/bottom insertion flips across repeated runs.

## Decision linkage

- Research basis: `R-0033`
- Decision: `DEC-0040`

---

# US-0059: Deterministic Intake Runtime Capability Guard and Single-Writer Drift Safety

## Overview

US-0059 hardens `/intake` runtime behavior so missing role-capability and
concurrent-writer scenarios are handled deterministically and fail safe.

## Architecture goals

- Fail fast when required role-specific intake subagent capability is missing.
- Prevent silent fallback in default policy.
- Distinguish self-write updates from external concurrent artifact drift.
- Preserve deterministic ordering and canonical ownership guarantees.
- Keep active/template contracts and regression checks aligned.

## Minimal architecture

1. **Capability preflight contract**
   - `/intake` performs capability preflight for role-specific `po` subagent
     before artifact mutation.
   - Missing capability fails fast with deterministic reason code
     `SUBAGENT_CAPABILITY_UNAVAILABLE`.
   - Default policy denies fallback (`INTAKE_SUBAGENT_FALLBACK=deny`);
     fallback requires explicit opt-in (`allow`).

2. **Single-writer intake scope**
   - Each intake run binds deterministic writer identity metadata:
     - `writer_id`
     - `intake_run_id`
   - Mutation scope is constrained to target intake artifacts:
     `vision`, `backlog`, `acceptance`, and `po_to_tl`.

3. **Self-write-aware drift detection**
   - Drift checks must accept self-generated writes for the same
     `(writer_id, intake_run_id)` as valid continuation.
   - Conflicting external concurrent mutation fails safe with reason code
     `INTAKE_CONCURRENT_WRITER_DETECTED` and no partial overwrite.

4. **Ordering/ownership compatibility**
   - Existing canonical ownership (`backlog` authority) remains unchanged.
   - Sorted-canonical intake placement and monotonic timestamp constraints remain
     mandatory and non-bypass.

5. **Verification and parity**
   - Add regression coverage for:
     - capability-missing fail-fast path,
     - self-write non-false-positive path,
     - external concurrent writer fail-safe path.
   - Keep active/template command/runbook/README parity.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Strict preflight blocks valid fallback workflows | explicit opt-in fallback policy via `INTAKE_SUBAGENT_FALLBACK=allow` |
| Incomplete writer identity causes residual false positives | deterministic run-scoped writer IDs and target-scoped mutation checks |
| Broad drift handling accidentally suppresses real conflicts | fail-safe only for same writer/run identity; external conflicting writes remain blocking |

## Decision linkage

- Research basis: `R-0035`
- Decision: `DEC-0041`
- Boundaries: workflow runtime guard behavior only; no product runtime feature changes.

---

# US-0060: Deterministic State Hot-Surface Rollover and Archive Enforcement

## Overview

US-0060 enforces bounded growth for `docs/engineering/state.md` by introducing
deterministic rollover triggers and non-destructive archival into
`docs/engineering/state-archive/`.

## Architecture goals

- Keep `state.md` as a compact hot surface for recent checkpoints.
- Enforce deterministic rollover thresholds instead of policy-only guidance.
- Preserve full historical evidence via append-only archive packs.
- Keep rollover idempotent and fail-safe on ambiguous boundaries or write errors.
- Preserve ordering, canonical ownership, and retrieval contracts.

## Minimal architecture

1. **Rollover trigger contract**
   - Configure via scratchpad:
     - `STATE_HOT_MAX_LINES` (default `1200`)
     - `STATE_HOT_MAX_CHECKPOINTS` (default `80`)
   - `/refresh-context` evaluates both thresholds and triggers rollover when
     either is exceeded.

2. **Deterministic archive mechanics**
   - Move oldest low-frequency checkpoints from hot surface into deterministic
     archive packs (`state-pack-YYYY-QN.md` or `state-pack-YYYYMMDD.md`).
   - Preserve chronology and evidence references.
   - Keep bounded recent checkpoints in hot surface.

3. **Fail-safe behavior**
   - If archive boundary cannot be safely determined:
     `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`.
   - If archive write cannot be completed:
     `STATE_ARCHIVE_WRITE_FAILED`.
   - Both fail-safe paths forbid partial mutation.

4. **Retrieval compatibility**
   - `/ask` and `/refresh-context` continue latest-first hot-surface reads.
   - Bounded expansion to archives only when unresolved.

5. **Parity and verification**
   - Active/template parity across scratchpad flags, command contracts,
     runbook/README, and policy artifacts.
   - Regression coverage for threshold-crossing rollover, idempotent reruns,
     and fail-safe error paths.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Thresholds too low reduce near-term debugging context | conservative defaults with explicit scratchpad overrides |
| Non-deterministic archive boundaries cause churn | deterministic boundary selection and stable pack naming |
| Partial archive writes corrupt traceability | fail-safe no-partial-write on archive boundary/write errors |

## Decision linkage

- Research basis: `R-0036`
- Decision: `DEC-0042`
- Boundaries: workflow artifact compaction enforcement only; no product runtime behavior changes.

---

# US-0061: Cross-Phase Artifact Ownership Guard and Deterministic Archive Control

## Overview

US-0061 hardens non-destructive artifact mutation behavior across phases and
adds stricter archive execution controls. The goal is to prevent cross-phase
history loss (especially in `docs/engineering/architecture.md`) while making
state archival deterministic and verifiable.

## Architecture goals

- Define explicit phase/artifact ownership boundaries.
- Fail closed on non-owned section deletion/rewrite attempts.
- Allow only explicit, auditable override-authorized mutation paths.
- Preserve architecture history across all normal phase runs.
- Strengthen state archive execution with deterministic verification evidence.

## Minimal architecture

1. **Ownership matrix contract**
   - Canonical policy artifact:
     `docs/engineering/artifact-ownership-policy.md`.
   - Matrix defines:
     - artifact scope ownership,
     - allowed phases,
     - override-authorized phases.

2. **Cross-phase guardrail enforcement**
   - Every mutable command phase must enforce ownership policy before write.
   - Non-authorized section rewrite/deletion fails safe with
     `PHASE_OWNERSHIP_VIOLATION`.
   - Override-authorized mutation requires explicit evidence fields; missing
     evidence fails with `PHASE_OVERRIDE_EVIDENCE_MISSING`.

3. **Architecture history protection**
   - `docs/engineering/architecture.md` is history-preserving:
     - append new `US-xxxx` section for new stories,
     - update target section only when needed,
     - unrelated story-section deletion is forbidden.
   - Detection fail-safe: `ARCH_HISTORY_DELETION_DETECTED`.

4. **Deterministic archive control hardening**
   - `/refresh-context` archive behavior remains threshold-driven
     (`STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS`).
   - Add deterministic archive verification evidence (boundary + moved/retained
     markers).
   - Verification mismatch fails with `STATE_ARCHIVE_VERIFICATION_FAILED`.

5. **Parity and verification**
   - Active/template parity required for commands, rules, policy docs, runbook,
     README, and regression assertions.
   - Regression coverage includes:
     - prohibited cross-phase deletion path,
     - explicit override evidence requirement path,
     - archive verification fail-safe path.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Ownership matrix too strict blocks legitimate target updates | target-scope rules are explicit per artifact; no broad denial defaults |
| Override path becomes implicit bypass | override-authorized list is explicit and evidence-gated |
| Archive verification adds overhead | verification output remains deterministic and bounded |

## Decision linkage

- Research basis: `R-0037`
- Decision: `DEC-0043`
- Boundaries: workflow artifact mutation/archival safety only; no product runtime feature changes.

---

# US-0064: Remote Runtime Connectivity Contract for QA/Release/Publish

## Overview

US-0064 extends release target configuration with runtime connectivity metadata
and defines phase-level consumption rules for remote/local contexts. It enables
release and QA workflows to provide deterministic operator connection guidance
without weakening gates or exposing secrets.

## Architecture goals

- Extend target schema for runtime connectivity and ingress metadata.
- Support Docker-over-SSH runtime/deploy patterns as first-class contract data.
- Keep remote behavior config-driven and deterministic for release/QA/execute.
- Provide canonical operator connectivity documentation.
- Preserve existing quality/release gates and secret safety constraints.

## Minimal architecture

1. **Connectivity schema extension**
   - Add deterministic metadata to `docs/engineering/release-targets.json`:
     - `runtime.mode` (`local|remote`)
     - endpoint fields (`domainEnv|ipEnv|hostEnv`, `port`, `protocol`)
     - optional ingress (`traefik.enabled`, `router`, `entrypoint`, `tls`)
     - optional `dockerOverSsh` contract for SSH targets.

2. **Validation and fail-safe behavior**
   - Enforce type-specific connectivity validation in release/remote-aware phase
     contracts.
   - Missing/invalid required connectivity fields fail with
     `REMOTE_CONNECTIVITY_CONFIG_INVALID`.
   - Connectivity document write failures fail with
     `RUNTIME_CONNECTIVITY_DOC_WRITE_FAILED`.

3. **Phase consumption contract**
   - `/release` consumes enriched connectivity metadata and emits operator-safe
     endpoint guidance.
   - `/qa` supports optional remote runtime verification/debug context when
     target runtime is remote.
   - `/execute` records remote/local execution context for handoff/state
     evidence when remote target context is active.

4. **Canonical operator documentation**
   - Add `docs/engineering/runtime-connectivity.md` as canonical sanitized
     runtime endpoint summary and connection guide.
   - Keep secrets out of artifacts (env-reference names only).

5. **Parity and verification**
   - Active/template parity for schema, commands, runbook/README, and docs.
   - Regression checks cover schema fields, phase contracts, and connectivity doc
     presence.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Schema complexity increases onboarding effort | provide minimal deterministic default fields and documented examples |
| Secret leakage in operator outputs | enforce env-reference-only policy and explicit redaction contract |
| Remote/local ambiguity in phase behavior | require explicit `runtime.mode` and deterministic skip/no-op semantics |

## Decision linkage

- Research basis: `R-0040`
- Decision: `DEC-0044`
- Boundaries: workflow release/QA/execute connectivity context only; no product runtime behavior changes.

---

# US-0062: Installer-Owned `its_magic/` Folder for Framework Metadata

## Overview

US-0062 introduces a deterministic installer-owned metadata boundary so
framework metadata is kept separate from project artifacts. Canonical installer
metadata now lives under `its_magic/`, while project-owned surfaces remain in
their existing product/engineering locations.

## Architecture goals

- Define a stable metadata home for installer/runtime framework markers.
- Preserve non-destructive behavior for existing repositories.
- Keep install/upgrade/clean behavior manifest-driven and auditable.
- Maintain active/template parity across installer implementations.

## Minimal architecture

1. **Canonical metadata home**
   - Installer-managed metadata surfaces are placed under `its_magic/`.
   - Canonical installed version marker path becomes
     `its_magic/.its-magic-version`.
   - Framework metadata README surface is emitted as `its_magic/README.md`.

2. **Manifest and ownership classification**
   - `installer-owned-paths.manifest` install/clean sections include `its_magic`.
   - Installer classifiers treat `its_magic/*` as framework-owned scope.
   - Project content locations remain outside `its_magic/` and are not relocated.

3. **Upgrade migration compatibility**
   - Upgrade/read logic accepts legacy root `.its-magic-version` for backward
     compatibility.
   - Write path always targets `its_magic/.its-magic-version`.
   - Legacy root marker is removed after successful canonical write.

4. **Clean-repo safety**
   - Clean operation removes framework-owned `its_magic/` contents and legacy
     root marker if present.
   - Non-owned project content remains untouched.

5. **Verification and parity**
   - Regression tests cover fresh install, upgrade migration, and clean behavior.
   - Active/template installer scripts and manifests remain contract-equivalent.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Legacy repositories rely on root version marker | read fallback supports legacy marker; write migrates to canonical location |
| Metadata boundary drift across platforms | align PowerShell/shell/Python installers plus shared manifest contract |
| Clean behavior removes too broadly | clean remains restricted to manifest-owned paths only |

## Decision linkage

- Research basis: `R-0038`
- Decision: `DEC-0045`
- Boundaries: installer metadata placement/migration only; no product runtime feature behavior changes.

---

# US-0063: OS-Aware Runbook Command Auto-Bootstrap with Verified Quality Gates

## Overview

US-0063 adds deterministic installer-time bootstrap for runbook command keys to
avoid first-run blockers while preserving strict quality gate behavior.

## Architecture goals

- Auto-populate real baseline command defaults from OS + stack signals.
- Preserve user-provided explicit runbook commands.
- Keep mandatory gate policy intact (`TEST_COMMAND` required).
- Emit deterministic diagnostics for unresolved/invalid baseline generation.

## Minimal architecture

1. **Bootstrap contract + precedence**
   - Apply `user override > detected defaults > fail-fast diagnostics`.
   - Never overwrite non-empty user command values in runbook.

2. **Detection + mapping**
   - Detect stack from canonical markers:
     - `package.json` scripts (`test`, optional `lint`, optional `typecheck`)
     - `go.mod`
     - Python markers (`pyproject.toml`, `requirements.txt`, `setup.py`)
     - platform test scripts where appropriate.
   - Map to deterministic defaults:
     - Node: `npm run test` (+ optional `npm run lint`, `npm run typecheck`)
     - Go: `go test ./...`
     - Python: `python -m pytest`

3. **Validation and fail-fast**
   - Probe candidate commands for baseline validity prior to write.
   - If baseline remains unresolved or invalid, emit deterministic diagnostics:
     - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED`
     - `[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:<reason>`
   - Installer exits non-zero on unresolved mandatory baseline.

4. **Parity and compatibility**
   - Implement equivalent behavior in PowerShell/shell/Python installers.
   - Keep active/template docs and tests aligned.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Incorrect default inferred for custom stack | user override always wins and is never overwritten |
| Optional command over-detection causes false confidence | only populate optional commands when confidently detectable |
| Regression across installer variants | enforce cross-installer parity and lifecycle regression tests |

## Decision linkage

- Research basis: `R-0039`
- Decision: `DEC-0046`
- Boundaries: installer/bootstrap and workflow gate readiness only; no runtime product behavior change.

---

# US-0065: Runtime QA Autopilot for Generated Projects

## Overview

US-0065 makes runtime verification mandatory for generated projects so QA cannot
pass on static checks alone. The architecture adds a minimal deterministic
runtime-validation contract across execute/qa, with bounded retries and
structured evidence.

## Architecture goals

- Require startup, readiness/connectivity, and runtime-log validation before
  PASS.
- Keep retry behavior bounded and auditable.
- Preserve remote-runtime support using existing connectivity contract surfaces.
- Keep scope strict to runtime verification/evidence only (no test scaffold or
  release hint schema expansion in this story).

## Minimal architecture

1. **Runtime verification pipeline (mandatory)**
   - Canonical stage order:
     `startup -> readiness/connectivity -> log scan -> bounded retry loop -> verdict`.
   - PASS requires all mandatory stages to succeed (or be deterministically
     skipped by explicit policy).
   - Evidence contract must include:
     - startup command/profile,
     - runtime mode (`local|remote`) and endpoint/health result,
     - retry ledger (attempt, delay, outcome),
     - log severity summary,
     - final verdict + reason code.

2. **Reason-code taxonomy (deterministic)**
   - Runtime failure boundaries use explicit families:
     - `RUNTIME_STARTUP_FAILED`
     - `RUNTIME_ENDPOINT_UNREACHABLE`
     - `RUNTIME_LOG_CRITICAL_DETECTED`
     - `RUNTIME_RETRY_BUDGET_EXHAUSTED`
     - `RUNTIME_STACK_PROFILE_UNRESOLVED`
   - Each reason code includes concise remediation guidance and evidence refs.

3. **Bounded retry policy**
   - Retries apply only to transient startup/connectivity failures.
   - Retry ceiling and delay/backoff are configured and capped.
   - Non-transient signals (for example critical runtime log severity) fail
     closed without broad retry loops.

4. **Stack-aware runtime profile selection**
   - Minimum supported stack profiles: Node, Python, Go, Java, .NET.
   - Unknown/ambiguous stack falls back deterministically to explicit fail-safe
     (`RUNTIME_STACK_PROFILE_UNRESOLVED`) rather than silent PASS.

5. **Webapp verification path (when applicable)**
   - For HTTP/UI runtime contexts, include browser-surface runtime checks and
     console/network error inspection evidence.
   - Keep this as runtime-truth verification, not release-hint or scaffold work.

## Alternatives challenged and tradeoffs

1. **Strict mandatory runtime pipeline vs optional best-effort checks**
   - Alternative: optional runtime checks with warning-only outcome.
   - Tradeoff: lower friction but preserves false-PASS risk.
   - Decision: choose strict mandatory pipeline because acceptance requires
     deterministic runtime proof.
   - Risk: slower QA runs on large projects.
   - Mitigation: bounded retries and explicit timeout caps.

2. **Unified retry policy vs stack-specific retry heuristics**
   - Alternative: per-stack retry semantics.
   - Tradeoff: potentially better tuning but higher complexity/drift.
   - Decision: start with unified bounded policy plus deterministic caps.
   - Risk: defaults may be suboptimal for some stacks.
   - Mitigation: keep policy configurable and evidence-first for tuning.

3. **Fail-fast unknown stack vs permissive generic runtime attempt**
   - Alternative: generic fallback command attempts.
   - Tradeoff: broader coverage but unpredictable behavior/noise.
   - Decision: fail-fast unresolved stack profile for deterministic outcomes.
   - Risk: legitimate projects may require manual profile mapping initially.
   - Mitigation: explicit remediation output and future profile extension path.

## Decision gates

- **Gate A (must pass):** reason-code set and evidence schema approved as
  canonical contract for execute/qa.
- **Gate B (must pass):** bounded retry defaults validated as strict enough to
  prevent retry storms while avoiding common transient false negatives.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Timeout defaults produce false negatives on slower runtimes | require configurable timeout ceilings with deterministic evidence output |
| Retry policy masks persistent defects | limit retries to transient classes and fail fast on critical log severity |
| Stack detection ambiguity causes inconsistent behavior | enforce explicit unresolved-stack fail-safe reason code and remediation |
| Browser checks increase runtime overhead for web stacks | run browser path conditionally only for detected HTTP/UI contexts |

## Decision linkage

- Research basis: `R-0042` (and `R-0041` for baseline workflow pattern alignment)
- Decision: `DEC-0047`
- Boundaries: runtime verification contract/evidence only for generated projects; no test scaffolding (`US-0066`) and no release-hint schema expansion (`US-0067`).

---

# Architecture Addendum (US-0066): Generated Test Scaffolding and Auto-Run Contract

Date: 2026-03-16
Story: `US-0066`
Research anchor: `R-0043` (plus `R-0041` baseline context)

## Problem statement

Generated app repositories can pass process gates without guaranteed baseline
tests when projects start with no test assets. `US-0066` closes this gap by
enforcing deterministic, non-destructive baseline test scaffolding and
automatic QA execution evidence.

## Scope and boundaries (strict)

- In scope:
  - workflow-level baseline test scaffold generation for Node/Python/Go/Java/.NET,
  - deterministic `TEST_COMMAND` baseline wiring for resolved stacks,
  - mandatory `/qa` baseline test auto-run evidence,
  - idempotent rerun and non-destructive preservation behavior.
- Out of scope:
  - advanced framework-specific test architecture generation,
  - runtime startup/connectivity verdict replacement (remains `US-0065`),
  - release operator hint schema expansion (`US-0067`) and intake packs (`US-0068`).

## Architecture decision summary

1. **Deterministic stack-profile baseline generation**
   - Detect supported stack/project profile (Node/Python/Go/Java/.NET).
   - Generate only missing baseline unit/integration/acceptance scaffold assets.
   - Write generated path inventory to execution evidence.

2. **Runbook command baseline wiring**
   - Resolve one minimal runnable baseline `TEST_COMMAND` per supported stack.
   - Apply non-destructive precedence:
     - keep existing user-authored runnable command,
     - fill only missing/unset baseline command.

3. **Mandatory QA auto-run evidence**
   - `/qa` must execute resolved baseline tests automatically.
   - Evidence requires command, pass/fail verdict, and output reference.

4. **Fail-closed unsupported/unresolved handling**
   - Deterministic diagnostics are required when profile resolution or generation
     fails:
     - `TEST_SCAFFOLD_STACK_UNRESOLVED`
     - `TEST_SCAFFOLD_UNSUPPORTED_STACK`
     - `TEST_SCAFFOLD_GENERATION_FAILED`

5. **Idempotent rerun contract**
   - Stable scaffold paths/conventions; no duplicate baseline files on rerun.
   - No oscillating command rewrites between repeated `/execute` runs.

6. **Runtime-autopilot integration boundary**
   - Static baseline test PASS is necessary but not sufficient.
   - Runtime startup/connectivity/log verdict remains governed by `US-0065`.

## Alternatives challenged and tradeoffs

1. **Mandatory scaffolding vs optional best-effort**
   - Alternative: warning-only scaffold attempt.
   - Tradeoff: lower friction, weaker guarantees.
   - Decision: mandatory fail-closed contract to satisfy AC-2/4/5/10.
   - Risk: stricter failures in partially configured repos.
   - Mitigation: deterministic remediation diagnostics and explicit evidence refs.

2. **Per-stack deterministic templates vs one generic template**
   - Alternative: single generic scaffold shape.
   - Tradeoff: simpler implementation, weaker runnable correctness.
   - Decision: per-stack minimal deterministic profiles to stay runnable by default.
   - Risk: profile matrix maintenance overhead.
   - Mitigation: keep first iteration limited to five minimum stacks.

3. **Built-in profile matrix vs plugin architecture (v1)**
   - Alternative: extensible plugin model immediately.
   - Tradeoff: future flexibility, higher complexity/risk now.
   - Decision: built-in deterministic matrix in v1 (simplest viable approach).
   - Risk: slower onboarding for niche stacks.
   - Mitigation: explicit unsupported-stack fail-safe and future extension path.

## Decision gates

- **Gate A (must pass):** non-destructive precedence behavior is canonical and
  testable (existing user tests/commands preserved).
- **Gate B (must pass):** unsupported/unresolved stack handling is deterministic
  and fail-closed with actionable remediation.
- **Gate C (must pass):** QA auto-run evidence schema is complete and auditable.

## Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Wrong stack chosen in polyglot repos | deterministic stack-selection precedence + unresolved fail-safe |
| Baseline generation clobbers user-authored assets | explicit non-destructive precedence and scoped writes to missing assets only |
| Repeated runs create duplicate/oscillating artifacts | stable path conventions + rerun idempotence checks in regression suite |
| Static tests pass while runtime still broken | preserve strict `US-0065` runtime-autopilot gate as independent mandatory verdict |

## Decision linkage

- Research basis: `R-0043` (with `R-0041` supporting baseline patterns).
- Decision: `DEC-0048`.
- Boundary note: `US-0066` covers generated test scaffolding + QA auto-run
  evidence only; release operator hint schema remains `US-0067`.

## US-0067 Architecture: Release operator Run/Connect/Verify hints contract

### Scope and constraints

- Story: `US-0067`
- Scope: release-operator guidance contract only for `Run/Connect/Verify` hints.
- In-scope:
  - deterministic release artifact schema and ordering,
  - required field validation and fail-closed behavior,
  - concise legacy pointer parity for latest release summary.
- Out-of-scope:
  - runtime autopilot logic and evidence contract (`US-0065`),
  - generated test scaffold logic (`US-0066`),
  - deployment engine orchestration or platform-specific operators.

### Architecture decisions

1. **Canonical operator section with fixed order**
   - Canonical sprint release notes must include:
     `Run -> Connect -> Verify -> Credentials (env-ref only) -> Known Issues`.
   - Fixed order is mandatory for idempotent reruns and operator readability.

2. **Required-field contract for release finalization**
   - Release completion must validate required fields before final PASS.
   - Missing or ambiguous required fields fail closed with deterministic reason
     codes and remediation guidance in release findings.

3. **Runtime context explicitness**
   - `runtime_mode` must be explicit as `local|remote`.
   - When `docs/engineering/runtime-connectivity.md` exists, endpoint/connectivity
     claims in release artifacts must align with that contract.

4. **Credentials safety boundary**
   - Credentials guidance is env-reference-only.
   - Inline secret values in release/operator artifacts are prohibited.

5. **Legacy pointer surface parity**
   - `handoffs/release_notes.md` remains concise and points to canonical sprint
     release notes while preserving a deterministic latest run/connect summary.

### Deterministic validation and reason-code baseline

- Required validation boundaries for finalization:
  - missing required operator fields,
  - ambiguous run/connect values,
  - missing explicit runtime mode,
  - credentials section violating env-ref-only policy.
- Deterministic fail-closed reason-code baseline:
  - `RELEASE_OPERATOR_HINTS_MISSING_REQUIRED_FIELD`
  - `RELEASE_OPERATOR_HINTS_AMBIGUOUS_FIELD`
  - `RELEASE_OPERATOR_HINTS_RUNTIME_CONTEXT_MISSING`
  - `RELEASE_OPERATOR_HINTS_CREDENTIALS_POLICY_VIOLATION`

### Alternatives challenged and tradeoffs

1. **Flexible free-form notes without fixed schema**
   - Alternative: allow arbitrary operator narrative.
   - Tradeoff: lower authoring friction, weaker reproducibility and readability.
   - Decision: fixed schema to keep output deterministic and auditable.

2. **Warning-only validation for missing fields**
   - Alternative: permit completion with warnings.
   - Tradeoff: fewer blocked releases, but poor operator actionability.
   - Decision: fail-closed finalization on missing/ambiguous required fields.

3. **Embedding credentials directly in notes**
   - Alternative: include inline secrets for convenience.
   - Tradeoff: short-term ease, unacceptable security exposure.
   - Decision: env-ref-only credentials contract.

### Decision gates

- **Gate A (must pass):** canonical release notes include fixed-order operator
  sections with all required fields.
- **Gate B (must pass):** release finalization blocks with deterministic reason
  code when required fields are missing or ambiguous.
- **Gate C (must pass):** credentials guidance is env-ref-only and no inline
  secrets appear in release surfaces.

### Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Operator notes drift into non-deterministic formatting | enforce fixed-order section schema and parity checks |
| Release passes without actionable run/connect details | fail-closed required-field validation with reason-code remediation |
| Runtime context mismatch across docs/surfaces | explicit `local|remote` field and alignment check against runtime-connectivity contract |
| Secret leakage into release notes | env-ref-only credentials rule plus validation guardrails |

### Decision linkage

- Research basis: `R-0044` (with `R-0041` supporting baseline patterns).
- Decision: `DEC-0049`.
- Boundary note: `US-0067` covers release operator hints only; runtime execution
  truth and generated test scaffolding remain governed by `US-0065`/`US-0066`.

## US-0068 Architecture: Mandatory intake question packs for first and small intakes

### Scope and constraints

- Story: `US-0068`
- Scope: intake questionnaire and persistence-gate policy only.
- In-scope:
  - deterministic two-pack intake schema (`first-intake-pack`, `small-intake-pack`),
  - required topic coverage validation before persistence,
  - bounded assumptions confirmation path as explicit compatibility mechanism,
  - low-touch mode compatibility without safety-topic bypass,
  - deterministic intake evidence fields for downstream trust.
- Out-of-scope:
  - runtime QA autopilot contract (`US-0065`),
  - generated test scaffolding contract (`US-0066`),
  - release operator `Run/Connect/Verify` hints contract (`US-0067`).

### Architecture decisions

1. **Two deterministic intake packs with explicit coverage taxonomy**
   - `first-intake-pack` captures comprehensive foundation topics for new/first
     requests.
   - `small-intake-pack` captures compact but mandatory topics for narrow follow-up
     work.
   - Both packs use stable topic IDs with required/optional classification.

2. **Fail-closed persistence gate**
   - Story persistence to backlog/acceptance is blocked when required topic
     coverage is incomplete.
   - Persistence may proceed only when:
     - required coverage is complete, or
     - bounded assumptions are explicitly confirmed by the user and recorded.

3. **Low-touch compatibility with safety floor**
   - Low-touch interaction remains available for speed.
   - Critical safety coverage cannot be skipped by low-touch path when required
     fields are missing.

4. **Deterministic intake evidence contract**
   - Intake outputs must persist structured evidence fields:
     - `asked_topics`
     - `missing_topics`
     - `assumptions_confirmed`
   - Coverage state becomes auditable and machine-verifiable for downstream phases.

5. **Bounded rounds and deterministic diagnostics**
   - Guided/adaptive follow-ups remain allowed but bounded.
   - Missing required coverage emits deterministic fail-closed diagnostics with
     remediation guidance.

### Deterministic validation and reason-code baseline

- Required validation boundaries:
  - unresolved required topic coverage for selected pack,
  - missing explicit user confirmation when assumptions are used,
  - attempted persistence while required coverage remains incomplete.
- Deterministic fail-closed reason-code baseline:
  - `INTAKE_REQUIRED_TOPIC_MISSING`
  - `INTAKE_REQUIRED_PACK_INCOMPLETE`
  - `INTAKE_ASSUMPTION_CONFIRMATION_REQUIRED`
  - `INTAKE_PERSISTENCE_BLOCKED`

### Alternatives challenged and tradeoffs

1. **Adaptive-only intake without fixed minimum packs**
   - Alternative: continue fully dynamic prompting.
   - Tradeoff: lower upfront friction, weaker deterministic quality floor.
   - Decision: enforce two fixed minimum packs.

2. **Single comprehensive pack for every intake**
   - Alternative: always ask full questionnaire.
   - Tradeoff: stronger completeness, higher friction for small requests.
   - Decision: use two-pack model to balance quality and flow.

3. **Warning-only persistence when coverage is incomplete**
   - Alternative: persist with warnings.
   - Tradeoff: fewer blocks, degraded downstream reliability.
   - Decision: fail closed until coverage or confirmed assumptions exist.

### Decision gates

- **Gate A (must pass):** deterministic pack schemas include required topic IDs
  matching `US-0068` acceptance coverage.
- **Gate B (must pass):** persistence blocks deterministically on incomplete
  required coverage.
- **Gate C (must pass):** low-touch path preserves critical safety coverage and
  records structured evidence fields.

### Risks and mitigations

| Risk | Mitigation |
|------|------------|
| Question packs become too broad and increase friction | maintain two-pack model with compact small-intake scope and bounded follow-ups |
| Weak topic taxonomy allows false coverage completion | require deterministic topic IDs with required/optional classification |
| Low-touch path bypasses critical safety topics | enforce fail-closed safety floor before persistence |
| Drift between active/template intake policy surfaces | keep deterministic reason-code and schema parity checks in intake command/rules updates |

### Decision linkage

- Research basis: `R-0045` (with `R-0041` supporting baseline intake patterns).
- Decision: `DEC-0050`.
- Boundary note: `US-0068` governs intake coverage enforcement only; runtime/test/release
  contracts remain `US-0065`/`US-0066`/`US-0067`.

---

## US-0069 Architecture: Strict phase role enforcement for `/auto`

### Scope and constraints

- Story: `US-0069`
- Scope: `/auto` orchestration — canonical phase→role mapping, preflight
  capability resolution, boundary evidence validation, diagnostics, and
  alignment with strict runtime proof (`DEC-0038`).
- In-scope:
  - deterministic matrix for all canonical `/auto` phase IDs,
  - scratchpad policy keys for allowed alternates (`research`, `plan-verify`,
    `refresh-context`),
  - preflight gate before phase spawn (no silent unrelated-role fallback),
  - checkpoint rejection when isolation `role` conflicts with expected contract,
  - strict-proof `role` / `proof_hash` consistency with resolved canonical role,
  - default deny for `execute` outside `dev` except documented override path,
  - resume / `start-from` parity with preflight re-evaluation.
- Out-of-scope:
  - configurable phase include/exclude profiles (`US-0070`),
  - product/runtime semantics of generated application code.

### Architecture model

1. **Single-valued expected role per boundary**  
   For each transition, `/auto` computes one expected `role` from the canonical
   matrix plus alternate policy (see `DEC-0051`). That value drives:
   - which subagent capability must be available preflight,
   - what isolation evidence must record,
   - what strict-proof tuple must attest.

2. **Preflight admission**  
   Treat role resolution like fail-closed admission: if the required capability
   cannot be satisfied, emit `PHASE_ROLE_CAPABILITY_MISSING` with
   `phase_id`, expected role, observed result, and remediation — do not spawn
   phase work under a substitute role.

3. **Post-completion validation**  
   When a phase completes, validate isolation evidence `role` against the same
   expected role computed preflight. Mismatch → `PHASE_ROLE_MISMATCH` and no
   forward progress.

4. **Strict-proof linkage**  
   The `DEC-0038` tuple’s `role` must match isolation `role` (both equal to the
   resolved canonical role). `proof_hash` remains SHA-256 over sorted-key JSON of
   the tuple fields (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`,
   `role`, `proof_issued_at`, `proof_ttl_seconds`).

5. **Execute default deny**  
   `execute` expects `dev`. Non-`dev` requires `AUTO_EXECUTE_ROLE_OVERRIDE` plus
   `execute_override_governance_ref` per `DEC-0051` (rare, audited).

6. **Continuation parity**  
   Every `/auto` invocation (including resume) recomputes policy and
   capability; stale `resume_brief` cannot bypass the gate.

### Operator and documentation surfaces

- `/auto` command text, related agent/command docs, runbook, README, and
  scratchpad examples must document the matrix, policy keys, reason codes, and
  override contract for active + template parity (implementation tranche).

### Regression and QA implications (planning hook)

- Pass path: capability available, correct role, aligned isolation + proof.
- Fail path: missing capability → `PHASE_ROLE_CAPABILITY_MISSING`.
- Evidence path: wrong `role` in checkpoint → `PHASE_ROLE_MISMATCH`.
- No silent fallback: assert orchestrator stops rather than substituting roles.
- Reason-code vocabulary stable and documented (AC-9).

### Decision linkage

- Research basis: `R-0048`
- Decision: `DEC-0051`
- Boundary note: phase-selection configuration remains `US-0070`; this story does
  not define skip/include profiles.

---

## US-0070 Architecture: Configurable `/auto` phase selection policy

### Scope and constraints

- Story: `US-0070`
- Scope: scratchpad-driven **resolved phase plan** for `/auto` (subset of the
  canonical lifecycle in order), interaction with `start-from`, continuation
  modes (resume, backlog-drain, bulk execute, team scope), and operator-visible
  diagnostics — **without** silent safety bypass or role substitution.
- In-scope:
  - single active policy mode (`AUTO_PHASE_PLAN`, `AUTO_PHASE_EXCLUDE`,
    `AUTO_PHASE_INCLUDE`, `AUTO_PHASE_PROFILE`) with fail-closed conflict
    handling,
  - deterministic expansion → non-skippable reinstatement (default profile) →
    `start-from` intersection,
  - breadcrumb contract for selected/skipped phases and reason codes,
  - explicit compatibility with `DEC-0051` / `US-0069` (roles apply only to
    planned phases; no alternate-role fallback when a phase is omitted).
- Out-of-scope:
  - concrete `/auto` implementation and automated tests (execute/QA tranche),
  - changing per-phase internal work semantics inside a retained phase.

### Architecture model

1. **Plan as first-class input to orchestration**  
   Before any phase spawn, materialize an ordered list of canonical `phase_id`
   values. Treat this list as the only schedule `/auto` may execute for that run
   (subject to stop conditions, loops, and security-review inserts per existing
   command contract).

2. **Policy modes (exactly one)**  
   Follow `DEC-0052`: default `full`; otherwise `exclude`, `include`, or
   `profile` with deterministic validation and `PHASE_POLICY_CONFLICT` (or
   equivalent) when multiple selectors compete.

3. **Non-skippable reinstatement (default)**  
   After computing the candidate list, reinsert members of the **default
   non-skippable set** that were removed:
   - minimum **safety gates**: `qa`, `verify-work`, `release`,
   - plus any phase required so that every **later planned phase** still has a
     valid chain of isolation + strict-proof evidence for the same story/run
     under `DEC-0029` / `DEC-0038` (do not assert downstream gates passed
     without their checkpoints).  
   Record each reinstatement in breadcrumbs with reason `non_skippable_gate` (or
   more specific documented codes).

4. **`start-from` intersection**  
   When `start-from=<phase>` is present, drop planned phases strictly before the
   anchor, then require a non-empty remainder; else fail closed with resolved
   plan vs requested anchor (backlog discovery contract).

5. **Continuation parity**  
   Reload merged scratchpad policy on every `/auto` entry (including resume);
   recompute the plan; never revive omitted phases without explicit breadcrumb
   explanation.

6. **Role and capability gates (`US-0069`)**  
   For each phase in the resolved plan, run the same preflight role resolution
   and capability admission as today (`DEC-0051`). Skipping a phase does **not**
   change the expected role of any other phase.

### Operator surfaces

- Scratchpad keys, mode precedence, non-skippable defaults, profile/ack
  requirements, and reason codes must appear in `/auto` command text,
  scratchpad examples, runbook, and README with active/template parity
  (`US-0070` AC-8).

### Regression and QA implications (planning hook)

- Default path: full plan unchanged vs pre-`US-0070` behavior.
- Selective path: exclude `research` and/or `sprint-plan` still reinstate safety
  gates and preserves evidence chain.
- Fail paths: unknown phase id, empty include, policy conflict, bad profile,
  `start-from` empty intersection — each deterministic code, no partial spawn.
- Resume path: policy bytes stable across interruption; plan reproducible.

### Decision linkage

- Research basis: `R-0049`
- Decision: `DEC-0052`
- Boundary note: role enforcement remains `DEC-0051` / `US-0069`; this story adds
  **which phases are scheduled**, not **who may run** them.

---

# US-0071: User-Visible Internal Metadata Sanitization Guard

## Overview

`US-0071` introduces a **channel-aware** policy: internal planning identifiers
are required for traceability in docs and comments, but must never appear in
**user-visible software outputs** (CLI/UI/errors/installer-visible text). The
architecture is a small, auditable control plane: **forbidden patterns** in
disallowed channels, **explicit allowlist** for internal surfaces, and **mandatory
execute → QA → release** evidence with shared reason codes.

## Policy model

### 1. Forbidden baseline (disallowed channels only)

Apply deterministic planning-shaped matchers in user-visible targets:

- `US-[0-9]{4}`
- `DEC-[0-9]{4}`
- `R-[0-9]{4}`

Matching should prefer planning-shaped tokens to limit accidental hits on
unrelated strings (`R-0046`).

### 2. Allowlisted internal surfaces

Permitted without guard failure:

- `docs/**`
- `.cursor/**`
- `sprints/**`, `handoffs/**`, `decisions/**` (and analogous template trees)
- **Source comments only** — not string literals that ship to users

### 3. Enforcement chain

| Boundary | Responsibility |
|----------|------------------|
| `/execute` | Default, non-bypass guard so in-scope changes do not introduce forbidden tokens into user-visible outputs. |
| `/qa` | Automated scan; fail closed with path evidence, token class, remediation; idempotent reruns. |
| `/release` / readiness | Attest checks **executed and passed** (AC-10), not policy-only. |

### 4. Reason codes (minimum vocabulary)

Use consistently across phases (`DEC-0053`):

- `USER_VISIBLE_INTERNAL_METADATA_DETECTED`
- `METADATA_SANITIZATION_POLICY_MISSING`
- `METADATA_SANITIZATION_SCOPE_AMBIGUOUS`

### 5. Parity and tests

- Active vs `template/` parity on commands, rules, runbook, README (AC-8).
- Regression: positive, negative, allowlist, rerun idempotence (AC-9).

## Decision linkage

- Research basis: `R-0046`
- Decision: `DEC-0053`

---

# US-0072: Deterministic Context Slimming and Archive Enforcement (Triad)

## Overview

`US-0072` makes **hot-surface compaction** and **bounded phase reads** a
first-class workflow contract for three canonical artifacts:
`docs/engineering/state.md`, `handoffs/po_to_tl.md`, and
`docs/engineering/architecture.md`. The design extends `DEC-0042` state rollover
with **parallel scratchpad thresholds**, **deterministic archive packs**,
**same-boundary enforcement**, and **verification tuples** so growth cannot pass
silently.

## Triad surfaces and caps

Thresholds are read from **merged scratchpad** (active + local) with defaults
documented in `DEC-0054`:

- **State** — `STATE_HOT_MAX_LINES`, `STATE_HOT_MAX_CHECKPOINTS` (existing).
- **PO→TL handoff** — `PO_TO_TL_HOT_MAX_LINES`, `PO_TO_TL_HOT_MAX_SECTIONS`.
- **Architecture** — `ARCH_HOT_MAX_LINES`, `ARCH_HOT_MAX_STORY_SECTIONS`.

## Archive layout

- `docs/engineering/state-archive/state-pack-*.md`
- `handoffs/archive/po-to-tl-pack-*.md`
- `docs/engineering/architecture-archive/architecture-pack-*.md`

Packs are append-only historical stores; hot files retain the newest material
per deterministic slice rules.

## Phase ownership gates

| Artifact | Typical mutator | Pre-completion gate |
|----------|-----------------|---------------------|
| `state.md` | Curator `/refresh-context` | Rollover or fail-closed when over cap. |
| `po_to_tl.md` | PO `/intake`, `/discovery`, handoff append paths | Rollover or fail-closed when over cap. |
| `architecture.md` | Tech-lead `/architecture` | Rollover or fail-closed when over cap; never delete unrelated `US-xxxx` sections (`DEC-0043`). |

Any phase that mutates a triad file inherits the gate for that run.

## Verification and idempotence

Successful rollover emits `boundary`, `moved`, `retained`, `pack_ref` in phase
evidence (for example `state.md` checkpoint body or sibling runbook table).
Reruns are idempotent: satisfied caps → no duplicate packs.

## Minimal-read model

Phase commands document **required files first**, numeric read budgets, and
**escalation only** to a named `pack_ref` when unresolved—aligned with
`DEC-0035` narrow-read retrieval. Optional compact pointer files or hot-header
blocks implement `AC-6` without duplicating full checkpoints.

## Reason codes

Minimum shared vocabulary (`DEC-0054`): `STATE_ARCHIVE_REQUIRED`,
`STATE_ARCHIVE_VERIFICATION_FAILED`, `ARTIFACT_HOT_SURFACE_OVERSIZE`,
`CONTEXT_BUDGET_EXCEEDED`, plus `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS` and
`STATE_ARCHIVE_WRITE_FAILED` where applicable.

## Decision linkage

- Research basis: `R-0047`
- Decision: `DEC-0054`

---

# US-0073: Scratchpad delivery simplification (example-only install policy)

## Overview

`US-0073` selects **Model B** from `R-0050`: installers ship **framework-owned**
`.cursor/scratchpad.local.example.md` as the primary default catalog; an
**effective baseline** is established only through **explicit materialization**
(or legacy committed `.cursor/scratchpad.md` on upgrade). The goal is simpler
delivery without weakening deterministic automation, upgrade parity, or
ownership rules already fixed in `DEC-0039`.

## Merge and safety model

### 1) Canonical precedence (merged key/value resolution)

Apply **after** loading each participating file:

1. `.cursor/scratchpad.local.md` (user-owned, never installer-overwritten).
2. `.cursor/scratchpad.md` **or** materialized baseline bytes (stable /
   auditable equivalent to historical committed baseline).
3. `.cursor/scratchpad.local.example.md` (framework-owned defaults; refreshed on
   upgrade per `DEC-0039`).

### 2) Fail-closed missing keys

If a **required** automation key is absent or invalid after merge, stop with
diagnostics that name which layers were consulted and how to remediate — **no**
silent inference (`AC-2`, `AC-4`).

### 3) Upgrade / legacy

- Preserve user local; refresh example only (`DEC-0039`).
- Repos with existing committed `scratchpad.md` keep deterministic behavior;
  migration paths that remove or replace baseline must be **explicitly**
  documented and test-covered.

### 4) Parity

Same policy across `installer.ps1`, `installer.sh`, `installer.py`, CLI, and
`template/` (`AC-6`, `AC-8`).

### 5) Regression focus

Fresh install, upgrade from legacy dual-file layout, missing baseline /
materialization, and local-only override; each maps to deterministic outcomes
(`AC-9`, `AC-10`).

## Decision linkage

- Research basis: `R-0050`
- Decision: `DEC-0055`

---

# US-0074: Baseline version-sync and TEST_COMMAND bootstrap

## Overview

`US-0074` closes persistent baseline failures in `tests/run-tests.ps1` /
`tests/run-tests.sh`: Homebrew stable formula alignment with npm, and installer
/ CLI bootstrap of `TEST_COMMAND` in materialized `docs/engineering/runbook.md`.
The design pins **one canonical version source** and **one bootstrap outcome
contract** so execute/QA can restore a fully green baseline without scope creep.

## Version sync model

### Canonical source

- **`package.json` `version`** is authoritative for semantic version and for the
  GitHub tag segment `v{version}` used in the Homebrew `url`.

### Homebrew stable formula rules

- Committed `packaging/homebrew/its-magic.rb` must satisfy, on every release that
  bumps npm:
  - `url` contains `.../refs/tags/v{package.json.version}.tar.gz`
  - Ruby `version "{package.json.version}"`
  - `sha256` matches the tarball for that tag
- Release scripts are the default enforcement path so formula and npm cannot
  diverge casually.

## TEST_COMMAND bootstrap model

### Surfaces and precedence

- Installers and CLI entrypoints materialize runbook commands per **`DEC-0046`**
  (user override wins; then stack detection; fail-fast diagnostics when
  unresolved).
- Baseline asserts require the **resolved** `TEST_COMMAND` after bootstrap to be
  **only** `npm run test` **or** `sh tests/run-tests.sh` for the detectable-stack
  scenarios under test (see **`R-0051`** post-discovery notes for detector/path
  pitfalls).

### Parity

- **`DEC-0056`** requires identical logical outcomes across
  `installer.ps1`, `installer.sh`, `installer.py`, and `bin/its-magic.js`
  delegation, with active + `template/` parity.

### PowerShell runner

- Emitting `tests/run-tests.ps1` as the bootstrap `TEST_COMMAND` is **out of
  scope** for the current baseline contract; widening requires an explicit future
  decision and test updates (`R-0051`).

## Verification

- Story acceptance re-runs consolidated tests and QA evidence so all four
  formerly failing checks pass without assert weakening (`US-0074` `AC-6`,
  `AC-7`, `AC-9`).
- Regression guidance lives in **`DEC-0056`** and this section for future drift.

## Decision linkage

- Research basis: **`R-0051`**
- Decision: **`DEC-0056`**

---

# US-0075: Upgrade scratchpad example–first refresh and paired catalog parity

## Overview

`US-0075` closes **example drift** and **paired-surface skew**: upgrade/install must refresh
**`.cursor/scratchpad.local.example.md`** from the shipped template **before or together with**
any step that advances materialized **`.cursor/scratchpad.md`**, so operators always see a
current **copy-from** catalog. **`AC-11`** adds **deterministic parity** between each
**baseline ↔ example** pair (active repo and `template/`) on **`##` sections** and **`KEY=`**
lines, with values allowed to differ only for documented conservative defaults.

## Ordering model

1. **Template catalog authority** — Framework vocabulary ships in
   **`template/.cursor/scratchpad.local.example.md`** (and is mirrored to active example on
   upgrade/install per pipeline design).
2. **No stale example + fresh baseline** — Any refresh of materialized **`scratchpad.md`**
   from **`template/.cursor/scratchpad.md`** is preceded by or bundled with example refresh
   from **`template/.cursor/scratchpad.local.example.md`** (**`DEC-0057`** §1).
3. **Parity surfaces** — Same ordering and diagnostics across installers, CLI, manifest, and
   `template/` (**`DEC-0057`**, **`US-0075`** **`AC-4`**, **`AC-8`**).

## Merge and ownership (unchanged)

- Precedence and layers remain **`DEC-0055`** (local → materialized baseline → example).
- User **`.cursor/scratchpad.local.md`** is never overwritten by framework refresh (**`DEC-0039`**).

## AC-11 parity gate

- Compare **paired** paths only: active **`.cursor/scratchpad.md`** ↔
  **`.cursor/scratchpad.local.example.md`** and **`template/.cursor/scratchpad.md`** ↔
  **`template/.cursor/scratchpad.local.example.md`**.
- Require **set equality** of **`##` section headers** and **`KEY=`** keys; manifest-documented
  local-only exceptions are the only allowed asymmetry (**`R-0052`** design).
- Enforce in **`tests/run-tests.*`** (or equivalent CI hook), not review-only.

## Diagnostics

- Distinguish **example** vs **materialized baseline** vs **user local** actions with
  deterministic reason families (**`DEC-0039`** alignment, **`US-0075`** **`AC-5`**).

## Verification

- Regression tests for outdated example + current template, post-upgrade example bytes, and
  absence of “baseline moved / example older than template” paths (**`US-0075`** **`AC-6`**,
  **`AC-9`**).

## Decision linkage

- Research basis: **`R-0052`**
- Decision: **`DEC-0057`**
