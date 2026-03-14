# Runbook

## Commands

TEST_COMMAND: sh tests/run-tests.sh
LINT_COMMAND:
TYPECHECK_COMMAND:
DEPLOY_STAGING_COMMAND:
DEPLOY_PROD_COMMAND:

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

For this template/installer repository, empty optional command keys are
intentional defaults, not configuration errors:

- `LINT_COMMAND`
- `FORMAT_COMMAND`
- `TYPECHECK_COMMAND`

Teams may set these keys when needed for their own project stack.

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

- `lean`: reduce non-critical overhead defaults (for example aggressive research,
  autonomous loops, broad-context retrieval), while preserving mandatory
  quality/release gates.
- `balanced`: preserve current capability profile with moderate overhead.
- `full`: maximize context breadth and autonomy for complex/high-uncertainty work.

Manual override precedence:

- Explicit flag values remain authoritative for that flag.
- If a flag is explicitly set, it overrides profile defaults.
- Profile changes must not disable mandatory gate contracts
  (`/qa`, `/verify-work`, `/release`).

Context compaction policy:

- `docs/engineering/state.md` is a compact hot surface for current execution
  context and recent checkpoints.
- Historical state packs belong in `docs/engineering/state-archive/` and are
  append-only/non-destructive.
- `docs/engineering/decisions.md` is a compact index with bounded summaries and
  canonical links to full records in `decisions/DEC-xxxx.md`.

`/ask` retrieval policy:

- Use question-scoped narrow reads first.
- Expand context in bounded steps only when unresolved.
- If unresolved after bounded expansion, answer with explicit "not found in
  current artifacts" rather than broad speculative reads.

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
| Fresh install (`missing`) | `its-magic --mode missing --create` and direct installer | `tests/run-tests.ps1`, `tests/run-tests.sh` | Required files exist + `.its-magic-version` exists |
| Overwrite + backup | `its-magic --mode overwrite --backup` and direct installer | `tests/run-tests.ps1`, `tests/run-tests.sh` | Backup snapshot contains overwritten framework file |
| Upgrade lifecycle | `its-magic --mode upgrade` and direct installer | `tests/run-tests.ps1`, `tests/run-tests.sh`, npm local tests | Framework file restored, scratchpad example refreshed, user local scratchpad preserved |
| Clean-repo safety | `its-magic --clean-repo --yes` and direct installer clean path | `tests/run-tests.ps1`, `tests/run-tests.sh`, CI lifecycle subset | Framework artifacts removed, non-framework marker preserved |
| Negative path | invalid mode/args | `tests/run-tests.ps1`, `tests/run-tests.sh` | Deterministic non-zero fail-fast behavior |
| Platform parity subset | npm/brew/choco CI jobs | `.github/workflows/ci.yml` | Lifecycle subset passes on all three runners |

## Scratchpad example upgrade contract (US-0057 / DEC-0039)

`its-magic --mode upgrade` treats `.cursor/scratchpad.local.example.md` as
framework-owned and `.cursor/scratchpad.local.md` as user-owned.

Expected deterministic outcome:
- Framework-owned example is refreshed to latest release contract.
- User local scratchpad remains preserved without overwrite.
- Installer output reports scratchpad example refresh status
  (`added|updated|unchanged`) and preservation signal for user local file.

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
- No partial mutation on fail-safe path.
- Re-run without semantic changes must be ordering-idempotent.

Execution guidance:
- Local baseline: run `sh tests/run-tests.sh` (or `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`).
- Packaging smoke: run npm local tests in `packaging/npm/`.
- CI evidence: inspect `npm-test`, `brew-test`, and `choco-test` job logs.

## Project run steps

### Prerequisites

### Local run

### Tests
