# PO to TL archive pack (2026-03-21)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 148
- Retained units in hot file: 23
- First archived heading: `## Discovery Addendum — US-0072 (Deterministic Context Slimming + Archive Enforcement)`
- Last archived heading: `## Discovery Addendum — US-0032 (Optional Feature User Guide Generation)`
- Verification tuple (mandatory):
  - archived_body_lines=1978
  - retained_body_lines=768

---

## Discovery Addendum — US-0072 (Deterministic Context Slimming + Archive Enforcement)

### Discovery context

- Intake and `R-0047` already establish that archive behavior must be an
  **execution gate**, not documentation-only, and that hot vs archive split
  reduces irrelevant-context load.
- Operational observation remains: hot files can exceed thresholds while archive
  evidence does not materialize, increasing hallucination risk and breaking
  auditable compaction expectations.

### Discovery outcomes

- **Default scope triad**: `docs/engineering/state.md`,
  `handoffs/po_to_tl.md`, `docs/engineering/architecture.md` are the primary
  hot/archive enforcement targets (AC-1). Expansion to additional `handoffs/*`
  surfaces requires explicit research/architecture justification.
- **Policy binding**: Thresholds and caps resolve from **merged scratchpad**
  (active + `.cursor/scratchpad.local.md`) so enforcement matches operator
  configuration.
- **Fail-closed rollover**: On threshold breach, the mutating phase performs
  rollover in the **same** boundary or stops with a deterministic reason code;
  no silent oversized hot surfaces (AC-2, AC-4).
- **Evidence + idempotence**: Archive success emits `boundary`, `moved`,
  `retained`, `pack_ref` per AC-3; pack naming must support idempotent reruns.
- **Context minimization**: Per-phase **required reads** and **bounded**
  escalation paths (AC-5); compact pointers/summaries in hot headers or sibling
  artifacts satisfy AC-6 intent.
- **Regression**: Coverage must include threshold success, empty/missing archive
  when rollover should have run, idempotent rerun, and budget violations (AC-10).
- **Scope wall**: Explicit non-overlap with `US-0071`, `US-0073`, `US-0074`; no
  evidence deletion; no QA/release gate weakening.

### Recommendation

- Proceed to **`/research`** for **`US-0072`** only — extend **`R-0047`** with
  concrete threshold keys, phase×role read matrices, boundary ownership
  (which phase mutates which artifact), and test hooks aligned to AC-1..AC-10.

---

## PO -> TL Handoff — US-0074 (Baseline Regression Cleanup)

### Intake context

- User requests clearing remaining baseline failing checks that repeatedly appear
  as out-of-scope findings in QA.
- Target failures explicitly named by user and recent QA evidence:
  - `Homebrew stable formula URL uses npm version tag`
  - `Homebrew stable formula version matches npm version`
  - `Installer bootstraps TEST_COMMAND for detectable stack`
  - `CLI missing install bootstraps TEST_COMMAND for detectable stack`

### Duplicate/overlap evaluation

- Related stories:
  - `US-0063` (OS-aware `TEST_COMMAND` bootstrap),
  - `US-0018`/`US-0057` (upgrade + scratchpad ownership/parity),
  - `US-0073` (scratchpad delivery policy).
- Assessment: not duplicate.
  - Existing stories define intended behavior; this story is a focused baseline
    regression closure and compatibility restoration pass for known failing checks.

### Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** recommended.
- Reason:
  - Four failing checks form one tightly coupled baseline health objective and
    should be validated in one integrated QA/release pass.

### Intake pack evidence (US-0068)

- selected_pack=`small-intake-pack`
- asked_topics:
  - `outcome_success_criteria`
  - `impacted_components`
  - `constraints_compatibility_risks`
  - `required_tests_acceptance_checks`
  - `done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### Scope for TL

- In scope:
  - deterministic fixes for the four named failing checks,
  - cross-installer parity + CLI path verification,
  - updated tests/docs/evidence to prevent recurrence.
- Out of scope:
  - unrelated feature additions outside these baseline failures.

### Research reference

- `R-0051`: baseline failure closure patterns for Homebrew/npm sync and
  installer bootstrap reliability.

### Recommendation

- Continue current queue order first: **`US-0072`**, then **`US-0073`**.
- Proceed to **`/discovery`** for **`US-0074`** once those are complete (or
  reprioritize explicitly if user wants immediate baseline cleanup next).

---

## PO -> TL Handoff — US-0073 (Scratchpad Delivery Simplification)

### Intake context

- User requests simplification of scratchpad delivery in installed repos:
  current model ships both `.cursor/scratchpad.md` and
  `.cursor/scratchpad.local.example.md`; user prefers example-only baseline.
- This request directly affects installer/upgrade behavior and automation flag
  resolution for `/auto` and phase commands.

### Duplicate/overlap evaluation

- Related stories:
  - `US-0018` (upgrade mode),
  - `US-0057` (scratchpad example refresh + ownership/parity),
  - `US-0069`/`US-0070` (runtime behavior depends on scratchpad flags).
- Assessment: not duplicate.
  - Existing stories harden current two-file behavior but do not decide/implement
    an example-only installer delivery model with deterministic fallback safety.

### Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** recommended.
- Reason:
  - installer delivery policy, runtime flag resolution safety, and migration
    compatibility are tightly coupled and should be validated together.

### Intake pack evidence (US-0068)

- selected_pack=`small-intake-pack`
- asked_topics:
  - `outcome_success_criteria`
  - `impacted_components`
  - `constraints_compatibility_risks`
  - `required_tests_acceptance_checks`
  - `done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### Scope for TL

- In scope:
  - choose canonical scratchpad delivery model (two-file vs example-only),
  - deterministic fallback semantics when baseline config file is absent,
  - upgrade migration behavior from current installs,
  - parity across installer entry points + CLI,
  - docs/tests for safety and operator clarity.
- Out of scope:
  - removing automation flags/gates from the framework,
  - weakening fail-closed behavior for missing required runtime config.

### Research reference

- `R-0050`: config-template/override patterns and separation principles relevant
  to scratchpad delivery choices.

### Recommendation

- Proceed to **`/discovery`** for `US-0073`.
- Discovery focus:
  - compatibility impact matrix against existing installed repos,
  - deterministic load precedence/fallbacks for `/auto` flag resolution,
  - migration and rollback strategy for upgrade mode.

---

## PO -> TL Handoff — US-0072 (Deterministic Context Slimming + Archive Enforcement)

### Intake context

- User reports persistent operational gap: `docs/engineering/state.md` keeps
  growing while `docs/engineering/state-archive/` remains effectively empty.
- User also reports `handoffs` and `docs/engineering/architecture.md` growth is
  creating noisy context that increases subagent misunderstanding/hallucination
  risk.
- User requests deterministic process changes so subagents read only
  context-necessary files while preserving required traceability.

### Duplicate/overlap evaluation

- Related stories:
  - `US-0053` (context compaction + `/ask` narrow reads),
  - `US-0060` (state rollover + archive enforcement),
  - `US-0061` (ownership guard + deterministic archive control).
- Assessment: not duplicate.
  - Existing contracts define policy, but current observed behavior indicates an
    enforcement/integration gap (archive not materializing, hot files still
    oversized).
  - This story focuses on fail-closed execution enforcement and bounded
    per-phase read contracts across multiple large artifacts.

### Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** recommended.
- Reason:
  - archive enforcement and context-budget control are tightly coupled in one
    operational objective (smaller, safer context surfaces with no evidence loss).

### Intake pack evidence (US-0068)

- selected_pack=`small-intake-pack`
- asked_topics:
  - `outcome_success_criteria`
  - `impacted_components`
  - `constraints_compatibility_risks`
  - `required_tests_acceptance_checks`
  - `done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### Scope for TL

- In scope:
  - deterministic hot/archive thresholds + enforcement for state/handoff/architecture,
  - fail-closed boundary checks when rollover is required but missing,
  - archive verification evidence schema and idempotent pack behavior,
  - strict per-phase minimal-read policy and compact phase-context pointers,
  - regression coverage for empty-archive and oversize-hot-surface failures.
- Out of scope:
  - deleting historical evidence,
  - weakening lifecycle quality/safety gates.

### Research reference

- `R-0047`: archive/rotation and bounded-context retrieval patterns for
  deterministic compaction with low hallucination risk.

### Recommendation

- **`/discovery` complete for `US-0072`** (see **Discovery Addendum — US-0072**
  at top of this file).
- Proceed to **`/research`** for **`US-0072`**, extending **`R-0047`** with
  implementation-ready threshold binding, phase-boundary ownership, bounded-read
  matrices, and verification/idempotence notes tied to AC-1..AC-10.

---

## PO -> TL Handoff — US-0071 (User-Visible Internal Metadata Sanitization Guard)

### Intake context

- User reports repeated cases where planning identifiers (for example `US-xxxx`)
  appear in user-visible software outputs (UI strings or other end-user-visible
  surfaces).
- User policy requirement is explicit:
  - allowed: internal docs + code comments,
  - forbidden: user-visible product surfaces.
- User expects deterministic automation guardrails, not manual discipline only.

### Duplicate/overlap evaluation

- Related stories:
  - `US-0069` (role enforcement in `/auto`),
  - `US-0068` (intake question-pack enforcement),
  - `US-0067` (release operator output schema).
- Assessment: not duplicate.
  - Existing stories improve orchestration quality and release clarity but do not
    define a dedicated cross-phase policy for blocking internal planning IDs in
    user-visible software.

### Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** recommended.
- Reason:
  - one policy boundary (internal metadata visibility) with cohesive
    execute/qa/release evidence integration.
- Alternatives considered:
  - split into "policy definition" + "qa gate" (rejected: tightly coupled and
    harder to validate independently for this scope size).

### Intake pack evidence (US-0071)

- selected_pack=`small-intake-pack`
- asked_topics:
  - `outcome_success_criteria`
  - `impacted_components`
  - `constraints_compatibility_risks`
  - `required_tests_acceptance_checks`
  - `done_definition`
- missing_topics=`(none)`
- assumptions_confirmed=`(none)`

### Scope for TL

- In scope:
  - deterministic forbidden-token policy for user-visible surfaces,
  - explicit allowlist for internal-only surfaces (docs/comments),
  - execute/qa fail-closed checks with deterministic reason codes and evidence,
  - release/readiness evidence references for sanitization verification,
  - active/template parity across command/rule/doc guidance.
- Out of scope:
  - broad content-style governance unrelated to internal planning metadata,
  - modifying business feature scope outside this visibility-policy contract.

### Research reference

- `R-0046`: user-visible internal metadata leakage prevention patterns, with
  security/error-handling references and policy implications.

### Recommendation

- **`/discovery` complete for `US-0071`** (see **Discovery Addendum — US-0071**).
- Proceed to **`/research`** for **`US-0071`**, extending `R-0046` findings into
  concrete scan targets, allowlist boundaries, and test matrix notes for
  execute/QA automation.

---

## Discovery Addendum — US-0071 (User-Visible Internal Metadata Sanitization Guard)

### Discovery context

- Discovery confirms a recurring quality gap: planning identifiers (`US-xxxx`,
  `DEC-xxxx`, `R-xxxx`) can appear in operator- or user-visible software outputs
  despite being acceptable in internal markdown and comments.
- Existing orchestration stories improve roles, phase plans, and release hints but
  do not define a cross-phase **output sanitization** contract for those tokens.

### Discovery outcomes

- Define **user-visible surfaces** as software-facing channels (CLI stdout/stderr,
  UI copy, user-facing errors, installer-visible messages) while **excluding**
  repository documentation trees, `.cursor` policy text, sprint/handoff/decision
  artifacts, and source comments from mandatory redaction.
- Keep **minimum forbidden patterns** aligned with backlog AC-1; allow research to
  propose extensions without shrinking the baseline taxonomy.
- Require **execute default guard** and **QA automated verification** with
  fail-closed diagnostics: file/path context, token class, safe replacement
  guidance, and documented reason codes (`USER_VISIBLE_INTERNAL_METADATA_DETECTED`,
  `METADATA_SANITIZATION_POLICY_MISSING`, etc.).
- Plan **regression shape**: positive clean output, negative leak detection,
  allowlist (docs/comments) non-regression, idempotent reruns — matching AC-9.
- **Scope wall**: no `US-0069` role-matrix changes, no `US-0070` phase-selection
  policy edits, no generic marketing copy standards.

### Recommendation

- Proceed to **`/research`** for **`US-0071`** only (deepen `R-0046` into
  implementation-ready guard + verification design).

---

## PO -> TL Handoff — US-0069 and US-0070 (/auto role enforcement + phase selection policy)

### Intake context

- User confirmed an external generated-repo run where `/auto` moved from intake
  into implementation behavior under tech-lead context instead of intended
  phase-role routing.
- User requested deterministic prevention of this behavior via strict phase role
  capability enforcement and fail-closed diagnostics.
- User also requested a scratchpad-controlled way to fine-tune which phases
  `/auto` runs (for example skipping `research` or `sprint-plan`) without
  disabling automation entirely.

### Duplicate/overlap evaluation

- Related stories:
  - `US-0048` (per-phase isolation evidence),
  - `US-0056` (strict runtime proof),
  - `US-0059` (intake role capability guard),
  - `US-0047` (bulk execute orchestration controls).
- Assessment: not duplicate.
  - `US-0069` introduces strict phase-role capability enforcement and role
    mismatch rejection across `/auto` lifecycle boundaries.
  - `US-0070` introduces operator-configurable phase selection policy for
    `/auto`, which existing mode toggles do not provide.

### Decomposition decision (US-0051 contract)

- Evaluator result: **two-story split** recommended and user-approved.
- `US-0069` scope: safety contract (role enforcement, fail-fast, evidence role
  validation).
- `US-0070` scope: operability contract (phase include/exclude policy with
  deterministic precedence and diagnostics).

### Scope for TL

- In scope:
  - deterministic phase->role mapping and capability preflight in `/auto`,
  - fail-closed reason codes for role-capability missing and role mismatch,
  - checkpoint role validation against expected phase-role contract,
  - scratchpad-driven phase selection policy with clear precedence and guardrails,
  - resume/start-from interaction contract for selected/skipped phases.
- Out of scope:
  - bypassing mandatory safety checks without explicit policy contract,
  - changing application-level implementation logic in generated repositories.

### Recommendation

- **`/discovery` complete for `US-0069`** (see **Discovery Addendum — US-0069**).
- **`/discovery` complete for `US-0070`** (see **Discovery Addendum — US-0070**).
- Proceed to **`/research`** for **`US-0070`** next (phase-selection policy contract).
- Discovery focus for `US-0069` (completed):
  - deterministic phase-role matrix and allowed override semantics,
  - reason-code taxonomy and fail-closed behavior for capability/mismatch paths,
  - evidence validation hooks at phase boundaries.
- Discovery focus for `US-0070`:
  - scratchpad schema for phase selection (`include`/`exclude`/profiles),
  - non-skippable safety boundary policy,
  - deterministic interaction with `start-from`, resume, backlog-drain, and
    bulk/team modes.

---

## Discovery Addendum — US-0069 (Strict Phase Role Enforcement in `/auto`)

### Discovery context

- Discovery confirms the reported failure mode: phases that should run under
  `dev`/`qa`/`release`/`curator` contexts can collapse into a single role
  (commonly `tech-lead`) when orchestration does not enforce capability routing.
- Existing isolation and strict-proof contracts record `role`, but without a
  hard phase→role gate, incorrect roles can still produce forward progress.

### Discovery outcomes

- Recommend **mandatory preflight** before each `/auto` phase transition: resolve
  required role from the canonical matrix (backlog AC-1), apply documented
  policy for allowed alternates, then fail closed with deterministic reason
  codes (`PHASE_ROLE_CAPABILITY_MISSING`, `PHASE_ROLE_MISMATCH`) when
  unavailable or mismatched.
- Recommend **checkpoint rejection** when completed-phase isolation evidence
  `role` does not match the expected contract for that `phase_id` (including
  policy-resolved alternate), satisfying AC-3.
- Recommend **default deny** for `execute` outside `dev` unless an explicit
  override contract is documented (AC-5).
- Recommend **strict-proof tuple alignment**: `role` in the runtime attestation
  matches the resolved canonical role and links to the same checkpoint as
  US-0048 isolation fields (AC-10 traceability).
- Explicit **non-scope** reminder: operator phase skip/include profiles are
  `US-0070` only; this story must not subsume phase-selection configuration.

### Recommendation

- Proceed to **`/research`** for **`US-0069` only** (role enforcement contract).
- Phase-selection configuration is **`US-0070`** (see **Discovery Addendum — US-0070**).

---

## Discovery Addendum — US-0070 (Configurable Auto Phase Selection Policy)

### Discovery context

- Operators want `/auto` to support **scratchpad-driven phase inclusion/exclusion**
  (for example skip `research` or `sprint-plan`) while keeping deterministic
  automation, fail-fast diagnostics, and visible breadcrumbs.
- `US-0069` now governs **which role** must run a phase; `US-0070` governs
  **whether a phase is scheduled at all** in a given `/auto` invocation — the
  two contracts must compose without role substitution or silent gate bypass.

### Discovery outcomes

- Recommend a **single active phase-policy mode** per run with explicit
  precedence (default full lifecycle; optional `AUTO_PHASE_EXCLUDE`,
  `AUTO_PHASE_INCLUDE`, or `AUTO_PHASE_PROFILE`) and deterministic fail-closed
  errors for unknown ids, empty plans, or conflicting policy keys.
- Recommend computing an **`effective_phase_plan`** (ordered canonical subset)
  after resume/`start-from` resolution and **before** the first phase spawn;
  record it in continuation breadcrumbs (`docs/engineering/state.md` and
  operator-visible status fields).
- Recommend a **non-skippable phase** baseline tied to mandatory evidence and
  quality gates (for example `qa`, `verify-work`, `release`), with only
  **explicit, named, documented profiles** allowing narrower plans — never silent
  omission from empty scratchpad values.
- Recommend deterministic **`start-from` ∩ effective plan** semantics with
  empty-intersection fail-fast and diagnostics that echo both inputs.
- Recommend parity rules for **`AUTO_BACKLOG_DRAIN`**, **`AUTO_EXECUTE_BULK`**,
  **`TEAM_MODE`**, and **`AUTO_PAUSE_*`**: carry forward the same phase policy
  metadata across segment boundaries so skipped phases stay skipped until the
  operator changes policy.
- Recommend reason-code extensions (to be finalized in research) such as
  `PHASE_POLICY_CONFLICT`, `PHASE_PLAN_EMPTY`, `PHASE_ID_UNKNOWN`,
  `START_FROM_PHASE_PLAN_EMPTY_INTERSECTION` for invalid operator config.

### Recommendation

- Proceed to **`/research`** for **`US-0070` only**, producing a precedence matrix,
  default non-skippable set, named profile sketch, and compatibility notes with
  `US-0069` role enforcement and existing `/auto` resume precedence.

---

## Discovery Addendum — US-0068 (Mandatory Intake Question Packs)

### Discovery context

- Discovery confirms a deterministic intake-quality gap: adaptive questioning
  exists, but minimum required topic coverage is not enforced before persistence.
- User intent requires mandatory questionnaire coverage in both first-intake and
  small-intake paths, with explicit blocked behavior when critical answers are
  missing.

### Discovery outcomes

- Recommend two canonical packs with deterministic topic IDs and coverage rules:
  - `first-intake-pack` (comprehensive): users/problem, runtime environment,
    stack/framework/runtime, architecture preferences, UI/UX expectations,
    security/compliance, NFR priorities, scope/timeline.
  - `small-intake-pack` (compact): desired outcome, impacted components,
    constraints/compatibility risk, required tests/acceptance checks, done
    definition.
- Recommend fail-closed persistence gating:
  - no backlog/acceptance persistence until required coverage is satisfied, or
    bounded assumptions are explicitly confirmed and recorded.
- Recommend deterministic diagnostics and evidence fields in intake outputs:
  `asked_topics`, `missing_topics`, `assumptions_confirmed`, and reason-coded
  block metadata for missing required answers.
- Scope boundary reminder: keep this story limited to intake questionnaire and
  persistence-gate policy; runtime QA/test scaffolding/release operator hints
  remain in `US-0065`/`US-0066`/`US-0067`.

### Recommendation

- Proceed to **`/research`** for `US-0068` only, focusing on pack schema,
  low-touch compatibility boundaries, fail-closed reason-code taxonomy, and
  canonical evidence-write locations.

---

## Discovery Addendum — US-0067 (Release Operator Hints Contract)

### Discovery context

- Discovery confirms an operator-readiness gap: release artifacts can pass gates
  while still lacking practical run/connect/verify instructions needed for fast
  real-world startup validation.
- Existing release notes are summary-focused; deterministic operator guidance
  fields are not currently enforced as mandatory contract output.

### Discovery outcomes

- Recommend a required section schema for sprint release notes with fixed order:
  `Run` -> `Connect` -> `Verify` -> `Credentials (env-ref only)` -> `Known Issues`.
- Recommend strict required-field validation and fail-closed release finalization
  when any run/connect/verify field is missing or ambiguous.
- Recommend explicit runtime context reporting (`local|remote`) aligned with
  runtime-connectivity documentation when available.
- Recommend concise pointer parity in `handoffs/release_notes.md` so latest
  operator run/connect summary links to canonical sprint release notes.
- Scope boundary reminder: keep this story limited to release operator hint
  contract; runtime autopilot and generated test scaffolding remain in
  `US-0065` and `US-0066`.

### Recommendation

- Proceed to **`/research`** for `US-0067` only, focusing on existing release
  artifact patterns, deterministic schema validation points, reason-code
  taxonomy for missing/ambiguous fields, and active/template parity surfaces.

---

## Discovery Addendum — US-0066 (Generated Test Scaffolding + Auto-Run)

### Discovery context

- Discovery confirms a generated-project reliability gap: baseline quality gates
  can run without guaranteeing baseline runnable tests exist for new app repos.
- Existing runbook/test command contracts are necessary but insufficient when
  repos start without scaffolded unit/integration/acceptance tests.

### Discovery outcomes

- Recommend deterministic stack/profile-driven baseline test scaffold generation
  for Node/Python/Go/Java/.NET minimum, with fail-safe behavior for unresolved
  or unsupported stack contexts.
- Recommend non-destructive generation precedence: scaffold only missing
  baseline assets and preserve user-authored tests/commands with explicit merge
  and precedence rules.
- Recommend deterministic runbook wiring so generated baseline tests are
  executable via `TEST_COMMAND` and automatically executed during `/qa`.
- Recommend idempotent rerun guarantees with auditable evidence (generated
  paths, skip reasons, preserved existing assets, and pass/fail test output
  references).
- Scope boundary reminder: keep runtime startup/connectivity/log autopilot in
  `US-0065`; keep release operator `Run/Connect/Verify` schema in `US-0067`.

### Recommendation

- Proceed to **`/research`** for `US-0066` only, focusing on scaffold template
  coverage by stack, deterministic merge precedence, fail-safe diagnostics, and
  idempotent rerun evidence schema.

---

# PO -> TL Handoff — US-0065..US-0068 (Runtime QA/Dev Autopilot + Test Scaffolding + Release Runbook Hints + Intake Question Packs)

## Intake context

User validated a real external generated-repo gap (not this framework repo's
self-tests):
- runtime app was not reliably started/validated,
- logs/errors were not inspected deeply enough,
- bounded self-debug retries were not enforced,
- generated baseline tests were not guaranteed,
- release output lacked concrete run/connect hints,
- intake still missed essential clarifying questions in some runs.

User explicitly requested a 4-story decomposition:
- Story A -> Runtime QA Autopilot (`US-0065`)
- Story B -> Generated Test Scaffolding + Auto-run (`US-0066`)
- Story C -> Release Operator Hints Contract (`US-0067`)
- Story D -> Mandatory Intake Question Packs (`US-0068`)

## Duplicate/overlap evaluation

- Related stories:
  - `US-0041` (installer/CLI lifecycle QA for this framework repo),
  - `US-0064` (remote connectivity metadata and remote-aware phase behavior),
  - `US-0051` / `US-0033` (intake decomposition and guided intake behavior).
- Assessment: not a duplicate.
  - Current contracts do not hard-enforce generated-project runtime startup +
    connectivity/log/debug loop as mandatory QA pass criteria.
  - Existing guided intake is adaptive but lacks fixed mandatory first/small
    questionnaire coverage gates.

## Decomposition decision (US-0051 contract)

- Evaluator result: **multi-story split** recommended and user-approved.
- Option considered:
  - single large story (rejected: mixes runtime QA, test generation, release UX,
    and intake policy into one difficult validation scope).
- Selected option:
  - four focused stories with clear acceptance boundaries and independent
    regression paths.
- User authority evidence:
  - user explicitly accepted split A-D in intake request.

## Scope for TL

- In scope:
  - language/project-aware runtime boot/health/log/debug QA contract,
  - generated-test scaffolding + automatic QA execution evidence contract,
  - mandatory release `Run/Connect/Verify` operator hints schema,
  - mandatory first/small intake question packs with persistence gating.
- Out of scope:
  - replacing per-project app architecture decisions,
  - embedding inline secrets in release/operator artifacts,
  - bypassing existing release/decision safety gates.

## Research reference

- `R-0041`: runtime verification/autopilot patterns, browser/debug-assisted web
  validation, and structured intake questionnaire coverage model.

## Recommendation

- Proceed to **`/discovery`** for `US-0065` first, then continue in order:
  `US-0066` -> `US-0067` -> `US-0068`.
- Discovery focus:
  - deterministic reason codes and bounded retry policy,
  - stack-profile command resolution + fallback behavior,
  - release operator hint schema and fail-safe validation,
  - intake questionnaire gating and low-touch compatibility.

## Discovery Addendum — US-0065 (Runtime QA Autopilot)

### Discovery context

- Discovery confirms a hard runtime-verification gap for generated projects:
  current workflow evidence can pass without proving the target app/service
  actually started, became reachable, or produced a clean runtime signal.
- Existing lifecycle and release gates remain necessary but are insufficient for
  generated-project runtime truth without a mandatory startup/connectivity/log
  contract.

### Discovery outcomes

- Recommend a deterministic runtime QA autopilot envelope with mandatory stages:
  startup attempt -> health/connectivity probe -> log/error scan -> bounded
  debug retry loop -> final PASS/FAIL verdict.
- Recommend explicit reason-code families for each failure boundary
  (startup-failed, endpoint-unreachable, log-critical-detected,
  retry-budget-exhausted, stack-profile-unresolved) with remediation guidance.
- Recommend stack-profile command resolution (Node/Python/Go/Java/.NET minimum)
  with deterministic fallback and non-silent fail-safe behavior when no runnable
  runtime profile can be selected.
- Recommend webapp-aware verification path inclusion (browser-level smoke and
  console/network error checks) when app context indicates HTTP/UI runtime.
- Recommend QA evidence schema hardening for reproducibility: startup command,
  runtime mode (`local|remote`), target endpoint/health result, log summary,
  retry attempt ledger, and final verdict.
- Scope boundary reminder: keep `US-0065` limited to runtime verification and
  QA evidence contract; route generated test scaffolding and release operator
  hints to `US-0066`/`US-0067`.

### Recommendation

- Proceed to **`/research`** for `US-0065` only, focusing on runtime
  attestation patterns, bounded retry policy defaults, stack-detection fallback
  matrix, and deterministic reason-code taxonomy.

### Discovery remediation note (strict-proof rerun)

- Discovery rerun was executed for `US-0065` remediation scope only.
- Functional discovery conclusions are unchanged; scope remains runtime
  verification contract/evidence only.
- Next phase recommendation remains **`/research`** for `US-0065`.

---

# PO -> TL Handoff — US-0064 (Remote Connectivity Contract for QA/Release/Publish)

## Intake context

User requests extending release target configuration to include runtime
connectivity and remote execution details, including:
- domain/IP/port metadata,
- Traefik/ingress possibilities,
- Docker via SSH execution targets.

User also requests that remote-aware phases consume this contract and provide
operator-facing connection guidance (where hosted/how to connect), persisted in
documentation.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0054` (configurable multi-target publish + SSH/custom targets),
  - `US-0034` (optional cross-repo observability),
  - `US-0039` (release gates).
- Assessment: not a duplicate.
  - Existing story `US-0054` provides publish target taxonomy and confirmation.
  - This story adds richer runtime/connectivity schema + remote phase
    consumption + operator connectivity documentation contract.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - target schema extension, release/qa phase consumption, remote execution
    context handling, and canonical connectivity documentation are tightly
    coupled.
- User authority evidence: user explicitly requested intake.

## Scope for TL

- In scope:
  - schema extension for connectivity metadata and Docker-over-SSH targets,
  - deterministic validation and fail-fast diagnostics,
  - remote-aware release/qa (and relevant execution) behavior contract,
  - canonical operator connectivity documentation artifact + updates.
- Out of scope:
  - secret-inline storage in repo files,
  - weakening existing mandatory release/quality gates.

## Risks

- Overly broad schema can add complexity/noise for local-only repos.
- Inconsistent remote-context detection can cause wrong phase behavior.
- Poor redaction policy can leak sensitive connection/auth information.

## Research reference

- `R-0040`: remote connectivity schema and phase-consumption patterns for
  operator-safe QA/release workflows.

## Recommendation

- Proceed to **`/discovery`** for `US-0064`, focusing on:
  - minimal deterministic schema shape for connectivity metadata,
  - remote/local phase selection and skip semantics,
  - operator-facing connectivity output + canonical document lifecycle.

---

# PO -> TL Handoff — US-0063 (OS-Aware Runbook Bootstrap + Verified Gates)

## Intake context

User requests automatic runbook command bootstrap for new repositories so first
sprint runs do not block on missing command configuration.

User explicitly requires:
- no quality-gate weakening,
- no placeholder-only bypass behavior,
- OS-aware defaults (Windows vs Unix),
- real command suitability for the detected project stack.

Observed mismatch example:
- Windows operator context with runbook baseline `TEST_COMMAND: sh tests/run-tests.sh`.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0015` (intentional optional empty command keys),
  - `US-0038`/`US-0039` (mandatory test gate contracts),
  - `US-0050`/`US-0018` (installer hygiene and upgrade behavior).
- Assessment: not a duplicate.
  - Existing work defines command semantics and installer behavior.
  - This story adds deterministic OS/stack-aware bootstrap and command
    verification during onboarding.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - bootstrap precedence, OS/stack detection, command verification, and gate
    compatibility are tightly coupled,
  - safer to validate as one onboarding contract.
- User authority evidence: user explicitly requested intake.

## Scope for TL

- In scope:
  - deterministic bootstrap precedence and non-destructive overwrite policy,
  - OS/shell-aware command generation defaults,
  - stack signal detection for baseline/optional checks,
  - fail-fast diagnostics for invalid/unresolvable generated commands,
  - parity/tests/docs updates.
- Out of scope:
  - weakening mandatory quality/release gates,
  - forcing one stack-specific command policy on all repositories.

## Risks

- Over-aggressive auto-detection may generate wrong commands for uncommon setups.
- Under-specified fallback behavior can recreate onboarding blockers.
- Incomplete parity can cause platform drift between installer implementations.

## Research reference

- `R-0039`: OS-aware runbook bootstrap patterns with mandatory-gate safety.

## Recommendation

- Proceed to **`/discovery`** for `US-0063`, focusing on:
  - deterministic precedence and override policy,
  - OS/shell detection contract and supported signal set,
  - command validation criteria + diagnostics.

---

# PO -> TL Handoff — US-0062 (Installer-Owned `its_magic/` Metadata Boundary)

## Intake context

User requests that installer-owned, non-project artifacts be placed under a
dedicated `its_magic/` folder rather than mixed into root/project artifact
space.

User explicitly highlights:
- framework README surface and version marker as `its_magic/` candidates,
- clear separation from project-owned artifacts (`src`, project docs, and other
  implementation/runtime content).

## Duplicate/overlap evaluation

- Related stories:
  - `US-0050` (clean install hygiene / clean-repo coverage),
  - `US-0018` (upgrade mode),
  - `US-0057` (scratchpad example upgrade parity).
- Assessment: not a duplicate.
  - Existing work improves hygiene and upgrade safety.
  - This story adds explicit folder-level installer ownership boundary and
    deterministic migration/cleanup semantics for framework metadata.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - installer placement, ownership manifest updates, upgrade migration, and
    clean behavior are tightly coupled,
  - safer to design/verify as one cohesive ownership-boundary package.
- User authority evidence: user explicitly requested intake.

## Scope for TL

- In scope:
  - canonical `its_magic/` ownership boundary for framework metadata,
  - deterministic placement/migration rules for install and upgrade modes,
  - clean-repo behavior aligned with updated ownership manifest,
  - parity updates across installer scripts/templates/docs/tests.
- Out of scope:
  - relocating project business artifacts into framework-owned folder,
  - changing product runtime feature behavior.

## Risks

- Over-broad ownership classification could accidentally move or delete
  project-owned files.
- Incomplete migration logic could leave mixed layouts across existing repos.
- Insufficient docs could confuse users about framework-vs-project ownership.

## Research reference

- `R-0038`: installer ownership boundary patterns for framework metadata
  placement and non-destructive migration.

## Recommendation

- Proceed to **`/discovery`** for `US-0062`, focusing on:
  - deterministic ownership matrix for `its_magic/`,
  - migration-safe upgrade path from legacy top-level layout,
  - clean-repo and regression coverage to prevent project-file impact.

---

# PO -> TL Discovery Addendum — US-0061 (Ownership Guard + Archive Control)

## Discovery context

- Discovery confirms policy gap: ordering rules do not fully prevent phase-level
  deletion/rewrite of non-owned sections.
- User-reported architecture history loss indicates need for explicit
  cross-phase ownership enforcement.
- State compaction requires deterministic verification outputs to ensure archive
  execution is real and auditable.

## Discovery outcomes

- Recommend canonical phase/artifact ownership matrix with explicit allowed
  phases and target scopes.
- Recommend fail-safe reason codes for prohibited cross-phase mutation and
  missing override evidence.
- Recommend explicit architecture history-preservation rule with
  non-target-section deletion detection.
- Recommend archive verification fail-safe path
  (`STATE_ARCHIVE_VERIFICATION_FAILED`) in refresh-context controls.

## Recommendation

- Proceed to **`/architecture`** for `US-0061`, focusing on ownership matrix
  schema, override evidence contract, and archive verification semantics.

---

# PO -> TL Handoff — US-0061 (Cross-Phase Ownership Guard + Archive Control)

## Intake context

User reports history loss in `docs/engineering/architecture.md` in a new-repo
run and requests stronger non-destructive guarantees across relevant phases and
artifacts.

User explicitly requests this intake to include:
- phase ownership guardrails (no cross-phase deletions),
- explicit override-authorized phase model for exceptional mutation,
- stricter deterministic archive execution controls so `state.md` remains
  bounded.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0058` (deterministic artifact ordering),
  - `US-0060` (state rollover enforcement),
  - `US-0045` / `US-0055` (canonical ownership + reconciliation).
- Assessment: not a duplicate.
  - Existing work defines ordering, status ownership, and rollover thresholds.
  - This new story adds cross-phase section ownership enforcement, explicit
    override-authority semantics, and executable archive verification controls.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - ownership matrix, override authority rules, command-level guardrails, and
    archive execution controls are tightly coupled,
  - safest to validate as one deterministic policy package.
- User authority evidence: user explicitly requested intake.

## Scope for TL

- In scope:
  - deterministic phase/artifact ownership matrix and guard checks,
  - fail-safe reason-code path for prohibited cross-phase deletion/rewrite,
  - explicit override-authorized mutation path with auditable evidence,
  - architecture history-preservation guard semantics,
  - deterministic archive execution + verification outputs and idempotence.
- Out of scope:
  - deleting historical evidence for size reduction,
  - changing product runtime behavior.

## Risks

- Ownership rules that are too broad may block valid target-scoped updates.
- Weak override boundaries can reintroduce destructive rewrites.
- Archive controls without deterministic verification can still drift under
  reruns or partial-write failures.

## Research reference

- `R-0037`: cross-phase ownership guard patterns and deterministic archive
  execution controls.

## Recommendation

- Proceed to **`/discovery`** for `US-0061`, focusing on:
  - ownership matrix shape (artifact + section granularity),
  - override authority contract and evidence schema,
  - archive boundary algorithm + verification ledger outputs.

---

# PO -> TL Discovery Addendum — US-0060 (State Rollover Enforcement)

## Discovery context

- Discovery confirms compaction enforcement gap: `state.md` hot surface grows
  beyond practical bounds because rollover triggers are not mandatory.
- Existing archive policy exists, but deterministic trigger and fail-safe
  mechanics require explicit contract hardening.

## Discovery outcomes

- Recommend deterministic threshold contract in scratchpad:
  `STATE_HOT_MAX_LINES` and `STATE_HOT_MAX_CHECKPOINTS`.
- Recommend enforced rollover in `/refresh-context` with deterministic archive
  partitioning/naming and bounded hot-surface retention.
- Recommend explicit fail-safe diagnostics:
  - `STATE_ARCHIVE_BOUNDARY_AMBIGUOUS`
  - `STATE_ARCHIVE_WRITE_FAILED`
- Recommend active/template parity plus regression coverage for threshold,
  idempotence, and fail-safe paths.

## Recommendation

- Proceed to **`/architecture`** for `US-0060`, focusing on threshold defaults,
  archive boundary algorithm, and fail-safe mutation guarantees.

---

# PO -> TL Handoff — US-0060 (State Hot-Surface Rollover Enforcement)

## Intake context

User reports unbounded growth of `docs/engineering/state.md` in a fresh repo
(~1800 lines after two sprints) and requests deterministic minimization behavior
that is actually enforced, not policy-only.

User explicitly approved taking this as intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0053` (context compaction and token profile),
  - `US-0058` (deterministic artifact ordering).
- Assessment: not a duplicate.
  - `US-0053` introduced hot-surface/archive policy.
  - `US-0060` focuses on deterministic rollover enforcement thresholds and
    fail-safe archive mechanics when growth exceeds bounds.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - threshold trigger, archive pack mechanics, idempotence, and retrieval
    compatibility are tightly coupled,
  - best validated as one bounded compaction-enforcement package.
- User authority evidence: user explicitly requested intake.

## Scope for TL

- In scope:
  - deterministic rollover trigger contract (`max_lines` and/or
    `max_checkpoints`) for `state.md`,
  - non-destructive archival into canonical `state-pack-*` files,
  - idempotent rollover behavior and fail-safe archive error handling,
  - command integration (`/refresh-context`, retrieval behavior) and parity/tests/docs.
- Out of scope:
  - deleting historical evidence,
  - changing delivery workflow phase semantics.

## Risks

- Over-aggressive rollover may hide near-term troubleshooting context if bounds
  are too low.
- Non-idempotent archive routines can create duplicate packs or reorder history.
- Partial writes during rollover failure can corrupt traceability.

## Research reference

- `R-0036`: deterministic event/state compaction and retention-trigger patterns.

## Recommendation

- Proceed to **`/discovery`** for `US-0060`, focusing on:
  - explicit threshold defaults and override contract,
  - deterministic archive partitioning/naming and write ordering,
  - fail-safe error matrix for archive and anchor edge cases.

---

# PO -> TL Discovery Addendum — US-0059 (Intake Capability Guard + Drift Safety)

## Discovery context

- Discovery confirms intake reliability gap at runtime boundary:
  - missing role-specific `po` capability handling,
  - self-write vs external-writer drift discrimination.
- Contract must preserve existing ordering and canonical ownership guarantees.

## Discovery outcomes

- Recommend capability preflight before mutation with deterministic fail-fast
  reason code `SUBAGENT_CAPABILITY_UNAVAILABLE`.
- Recommend explicit fallback policy switch only
  (`INTAKE_SUBAGENT_FALLBACK=deny|allow`) with default deny.
- Recommend deterministic writer/run identity model for intake mutations
  (`writer_id`, `intake_run_id`) and self-write allow semantics.
- Recommend fail-safe conflict handling with deterministic reason code
  `INTAKE_CONCURRENT_WRITER_DETECTED` and no partial overwrite.

## Recommendation

- Proceed to **`/architecture`** for `US-0059` with focus on command contract,
  reason-code matrix, and parity/test coverage.

---

# PO -> TL Handoff — US-0059 (Intake Runtime Capability Guard + Drift Safety)

## Intake context

User reports a first-intake run in a fresh repo where the runtime claimed:
- `po` subagent cannot run in current environment (capability mismatch),
- intake proceeded directly,
- then blocked because `docs/product/backlog.md` "changed mid-run" from empty to
  populated.

User explicitly requested this be formalized as a bug intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0048` (fresh per-phase subagent isolation evidence),
  - `US-0056` (strict runtime proof for phase isolation),
  - `US-0058` (deterministic artifact ordering).
- Assessment: not a duplicate.
  - Existing stories define isolation/order contracts.
  - This new story targets intake-time capability negotiation and self-write vs
    external-writer drift discrimination.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - capability preflight, writer identity/run scoping, and deterministic drift
    diagnostics are tightly coupled,
  - safest to implement and validate as one bounded intake runtime contract.
- User authority evidence: user explicitly requested bug intake.

## Scope for TL

- In scope:
  - intake preflight for required `po` subagent capability,
  - deterministic fail-fast reason code + remediation output for capability
    mismatch,
  - deterministic single-writer guard semantics and self-write-aware drift
    detection,
  - fail-safe behavior on true concurrent writer detection,
  - active/template parity, tests, and operator docs.
- Out of scope:
  - removing existing release/isolation fail-closed gates,
  - changing non-intake workflow feature behavior.

## Risks

- Overly strict capability checks could block valid fallback usage if policy is
  not explicit.
- Weak writer identity semantics can still produce false-positive drift blocks.
- Broad file rewrites during guard implementation could violate ordering
  idempotence.

## Research reference

- `R-0035`: capability mismatch handling and single-writer drift guard patterns.

## Recommendation

- Proceed to **`/discovery`** for `US-0059`, focusing on:
  - capability contract shape and policy defaults,
  - run-id/writer-identity model for intake writes,
  - deterministic reason-code matrix for fail-fast vs fail-safe paths.

---

# PO -> TL Discovery Addendum — US-0056 (Strict Runtime Proof)

## Discovery context

- Discovery confirms a contract gap between artifact-level isolation evidence
  and strict runtime-attested phase execution guarantees.
- `/auto` must validate runtime proof at every phase boundary before proceeding;
  otherwise fail closed.

## Discovery outcomes

- Recommend introducing a strict runtime attestation envelope per phase run with
  unique proof identity and bounded freshness checks.
- Recommend deterministic reason-code taxonomy for strict-proof failure classes
  (missing, invalid shape, reused proof, stale proof, ambiguous linkage).
- Recommend integrating strict-proof checks into:
  - phase-boundary continuation in `/auto`,
  - pause/resume provenance,
  - isolation/release gate consumption.

## Recommendation

- Proceed to **`/research`** for `US-0056` to gather attestation patterns and
  define bounded compatibility behavior for legacy runs.

---

# PO -> TL Handoff — US-0058 (Deterministic Artifact Ordering)

## Intake context

User requests deterministic artifact update ordering because current behavior can
mix top and bottom insertions. Reported affected surfaces include
`docs/engineering/state.md`, `docs/product/backlog.md`, and
`docs/product/acceptance.md`.

User explicitly approved taking this as intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0045` (canonical status source + drift guard)
  - `US-0055` (status reconciliation command)
- Assessment: not a duplicate.
  - Prior stories focus on status precedence/reconciliation.
  - `US-0058` is specifically about deterministic insertion/sorting discipline
    across artifact mutation commands.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - one core objective (deterministic ordering contract),
  - tightly coupled concerns (ordering matrix, mutation anchors, idempotence,
    parity, tests),
  - better validated as one cross-command policy package.
- User authority evidence: user explicitly requested this intake.

## Scope for TL

- In scope:
  - per-file ordering matrix (`append-bottom`, `prepend-top`, `sorted-canonical`),
  - command contract updates for deterministic insertion points and fail-safe
    behavior,
  - idempotent re-run guarantees (no oscillating order),
  - active/template parity and regression coverage.
- Out of scope:
  - changing runtime product feature behavior.

## Risks

- First normalization could cause large diffs if migration is not bounded.
- Ambiguous anchors may trigger non-deterministic writes if not fail-safe.
- Divergent command behavior could persist without parity enforcement.

## Research reference

- `R-0033`: ordering policy patterns + artifact-specific guidance.

## Recommendation

- Proceed to **`/discovery`** for `US-0058`, focusing on:
  - file-by-file ordering matrix and deterministic anchors,
  - one-time bounded normalization strategy,
  - command ownership map and regression scope.

---

# PO -> TL Handoff — US-0057 (Upgrade-Safe Scratchpad Example Refresh)

## Intake context

User reports that upgrading via `its-magic --mode upgrade` can leave
`.cursor/scratchpad.local.example.md` with fewer or missing options, while some
options already exist in the user's scratchpad surfaces. User requests reliable
upgrade behavior and parity.

User explicitly approved taking this as intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0018` (smart upgrade mode)
  - `US-0050` (clean install hygiene and install/clean ownership)
- Assessment: not a duplicate.
  - Existing stories establish broad upgrade/ownership behavior.
  - `US-0057` is focused on a specific scratchpad example/user drift path and
    deterministic installer parity + diagnostics.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - one objective (upgrade-safe scratchpad example refresh),
  - tightly coupled scope across ownership policy, installer parity, diagnostics,
    and regression checks,
  - can be validated in one integrated installer/test pass.
- User authority evidence: user explicitly requested this intake.

## Scope for TL

- In scope:
  - deterministic scratchpad example ownership/update policy on upgrade,
  - user scratchpad preservation behavior,
  - installer parity across PS1/sh/py,
  - explicit upgrade diagnostics for example refresh/preservation outcomes,
  - active/template parity and regression coverage.
- Out of scope:
  - unrelated runtime workflow feature changes.

## Risks

- Refresh logic might overwrite user-owned scratchpad values.
- Under-refresh may keep stale example contract and hide new options.
- Installer parity gaps can cause OS-specific drift behavior.

## Research reference

- `R-0032`: upgrade-safe example/local config patterns + installer references.

## Recommendation

- Proceed to **`/discovery`** for US-0057 with focus on:
  - ownership matrix and deterministic precedence,
  - upgrade diagnostics for example vs user surfaces,
  - parity contract across all installers and tests.

---

# PO -> TL Handoff — US-0056 (Strict Runtime Proof for Per-Phase Isolation)

## Intake context

User wants strict runtime proof that `/auto` phase execution actually uses fresh
subagent executions per phase, beyond artifact-only isolation evidence rows.
User observed a single visible chat flow and requested fail-closed proof
enforcement.

User explicitly approved taking this as intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0048` / `DEC-0029` (per-phase isolation evidence contract)
  - `US-0055` (status reconciliation command)
- Assessment: not a duplicate.
  - `US-0048` defines required evidence fields and fail-closed behavior, but
    lacks strict runtime attestation guarantees.
  - `US-0056` introduces explicit runtime-proof schema and enforcement so phase
    isolation cannot be satisfied by artifact markers alone.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - one shared objective (strict runtime isolation proof),
  - tightly coupled scope across attestation schema, `/auto` gate enforcement,
    resume/pause provenance, and operator diagnostics,
  - should be validated in one integrated parity/regression pass.
- User authority evidence: user explicitly requested strict proof via intake.

## Scope for TL

- In scope:
  - strict runtime attestation schema per phase run,
  - deterministic `/auto` fail-closed checks for missing/reused/stale proof,
  - integration with isolation/release gates and resume provenance,
  - deterministic reason-code taxonomy and remediation guidance,
  - active/template parity and regression coverage.
- Out of scope:
  - product runtime feature behavior changes,
  - external orchestration platform migration.

## Risks

- False confidence if proof fields are present but not uniquely bound to phase execution.
- Overly strict gating could block continuation without actionable remediation.
- Legacy runs without strict attestation may need bounded compatibility handling.

## Recommendation

- Proceed to **`/discovery`** for `US-0056`, focusing on:
  - runtime proof schema and uniqueness constraints,
  - strict fail-safe reason-code contract,
  - pause/resume provenance compatibility,
  - auditable operator-visible diagnostics.

---

# PO -> TL Handoff — US-0055 (Deterministic Status Reconciliation Command)

## Intake context

User reported status drift after refresh/auto boundaries where some historical
stories remain marked DONE in backlog while related acceptance/checklist surfaces
still show unchecked entries. User requested a dedicated command to check and
clean this "chaos" so next `/auto` continuation resumes from the correct OPEN
story baseline.

User explicitly approved taking this as intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0024` (`/memory-audit`, read-only drift detection)
  - `US-0045` (canonical status ownership)
  - `US-0049` (legacy DONE-story drift guard at release boundary)
- Assessment: not a duplicate.
  - `US-0055` adds an explicit deterministic **repair/reconciliation command**
    across backlog/acceptance/state/resume surfaces and continuation readiness.
  - Existing contracts detect/guard in parts, but there is no dedicated operator
    command that performs bounded reconciliation and resume setup.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - one shared operational objective (deterministic status normalization and
    continuation readiness),
  - tightly coupled scope across detection rules, repair semantics, audit
    evidence, and resume baseline update,
  - can be validated in one integrated parity/regression pass.
- User authority evidence: user explicitly requested this intake.

## Scope for TL

- In scope:
  - new reconciliation command contract (for example `/status-reconcile`),
  - deterministic status mismatch detection across backlog/acceptance/state/resume,
  - bounded target-scoped repair behavior with audit traceability,
  - reason-code and remediation contract for blocked/conflict states,
  - deterministic resume metadata update for next OPEN story/phase,
  - active/template parity and regression coverage.
- Out of scope:
  - changing product feature semantics,
  - bypassing mandatory QA/UAT/release gates,
  - destructive rewrite of unrelated historical artifacts.

## Risks

- Over-broad mutation could rewrite unrelated historical entries.
- Ambiguous source precedence can create non-deterministic reconciliation.
- Poorly bounded repair may hide true release-evidence conflicts.

## Recommendation

- Proceed to **`/discovery`** for `US-0055`, focusing on:
  - canonical precedence and deterministic mutation boundaries,
  - blocked/conflict reason-code set and remediation UX,
  - audit artifact schema for before/after normalization evidence,
  - resume phase resolution rules after reconciliation.

## Discovery addendum — US-0055

- Discovery completed for US-0055 and validated:
  - canonical backlog status must remain authoritative,
  - reconciliation mutation must stay target-scoped and auditable,
  - deterministic resume update is required for safe `/auto` continuation.
- Updated recommendation: Proceed to **`/research`** for US-0055.

---

# PO -> TL Handoff — US-0054 (Configurable Multi-Target Release Publish)

## Intake context

User requested intake for configurable publish targets after workflow release
finalization, including support for:

1. heterogeneous destinations per project (registry/git/docker/cloud/custom),
2. generic/custom server targets,
3. SSH-based execution targets,
4. half-automatic safety where the agent asks for confirmation before publish.

User explicitly approved taking this as intake.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0038` (sync policy and guarded auto-push)
  - `US-0039` (release gate chain and no-bypass release semantics)
  - `US-0036` (remote config validation contract)
- Assessment: not a duplicate.
  - `US-0054` focuses on **post-release publish target configuration and
    operator-confirmed execution** across heterogeneous destinations.
  - Existing stories cover release safety and sync behavior, but not a generic
    configurable publish-target model including SSH/custom server paths.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - one shared operational objective (configurable multi-target publish with
    confirmation safety),
  - tightly coupled scope across target schema, confirmation flow, and
    execution/fail-fast behavior,
  - can be validated in one integrated parity and regression pass.
- User authority evidence: user explicitly asked to take this as intake and
  requested generic/custom + SSH support.

## Scope for TL

- In scope:
  - configurable publish-target schema and validation,
  - target-type support for built-in + generic custom command targets,
  - SSH target support via config,
  - operator confirmation gate before publish execution,
  - deterministic selection/order/skip and fail-fast diagnostics,
  - active/template parity and regression coverage.
- Out of scope:
  - replacing provider-specific CLIs,
  - hardcoding one deployment platform,
  - storing inline secrets in committed artifacts.

## Risks

- Under-specified target schema may produce non-deterministic execution.
- Missing confirmation boundaries may allow accidental publish actions.
- Secret handling can regress if env-reference-only constraints are not explicit.

## Research reference

- `R-0029`: configurable multi-target publish patterns, confirmation gates, and
  SSH-based deployment references.

## Recommendation

- Proceed to **`/research`** for US-0054 with these targets:
  - canonical target schema and fail-fast validation rules,
  - target taxonomy (built-in + `custom` + `ssh`) and deterministic execution order,
  - confirmation gate semantics (default-on) and operator override boundaries,
  - env-reference-only credential handling contract for publish targets,
  - deterministic reason-code set for invalid config/blocked execution,
  - active/template parity and regression matrix.

## Discovery addendum — US-0054

- Discovery references reviewed:
  - GitHub deployment environments/protection rules,
  - GitHub environment management guidance,
  - SSH deployment patterns for CI/CD.
- Discovery conclusion:
  - publish targets must be configuration-driven per repository,
  - SSH/custom server targets should be first-class target types,
  - default confirmation gate is required for half-automatic safety,
  - deterministic validation/reason-code contract is required before architecture.

---

# PO -> TL Handoff — US-0053 (Context Compaction + Tiered Token-Cost Optimization)

## Intake context

User concern: current workflow likely consumes too many tokens due to repeated
reads/writes of large memory artifacts. User requested:

1. a tiered token-saver mode (lean/balanced/full style) with minimal feature
   loss,
2. context compaction strategy for large artifacts (especially
   `docs/engineering/state.md`),
3. compact `docs/engineering/decisions.md`,
4. narrow-read `/ask` policy focused on question-scoped retrieval.

User explicitly asked to treat this as intake and accepted the tiered-profile
direction.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0024` (memory drift audit, read-only advisory)
  - `US-0033` (guided intake behavior switch)
  - `US-0045` (canonical status ownership/reconciliation)
- Assessment: not a duplicate.
  - `US-0053` focuses on token-efficiency policy controls and compact active
    context retrieval behavior while preserving existing quality gates.

## Decomposition decision (US-0051 contract)

- Evaluator result: **single-story** (no split) recommended.
- Rationale:
  - one shared operational objective (token-cost reduction with safety
    invariants),
  - tightly coupled scope across profile defaults, context compaction, and ask
    retrieval policy,
  - can be validated through one integrated policy + parity regression pass.
- User authority evidence: user approved this intake direction and asked to
  proceed as intake.

## Scope for TL

- In scope:
  - tiered token profile contract and mapping to scratchpad behavior switches,
  - active-vs-archive compaction policy for `state.md`,
  - compact index policy for `decisions.md`,
  - `/ask` narrow-read retrieval rules,
  - active/template parity and regression coverage.
- Out of scope:
  - removing mandatory QA/UAT/release gates,
  - destructive deletion of historical evidence,
  - changing canonical status ownership semantics.

## Risks

- Over-aggressive compaction could hide required evidence if archive links or
  retrieval rules are ambiguous.
- Profile mapping may create operator confusion if override precedence is not
  explicit and deterministic.
- Token-saver defaults must not silently degrade release safety behavior.

## Research reference

- `R-0026`: Token-cost optimization patterns for artifact-first AI workflows.

## Recommendation

- Proceed to **`/research`** for US-0053 with these targets:
  - exact profile mapping table (`lean|balanced|full`) and deterministic
    override precedence,
  - compact/hot vs archive structure contract for `state.md` including archival
    trigger and retrieval policy,
  - compact index boundary for `decisions.md` and canonical linking pattern to
    `decisions/DEC-xxxx.md`,
  - `/ask` retrieval-order contract (targeted read -> bounded expansion -> fail
    with explicit "not found in artifacts"),
  - regression/parity matrix for active + `template/` surfaces and guardrail
    invariants (mandatory release chain unchanged).

## Discovery addendum — US-0053

- Discovery references reviewed:
  - OpenAI prompt caching docs (`platform.openai.com/docs/guides/prompt-caching`)
  - Anthropic prompt caching docs (`platform.claude.com/docs/en/build-with-claude/prompt-caching`)
  - Progressive context loading pattern reference
    (`williamzujkowski.github.io/.../from-150k-to-2k-tokens...`)
- Discovery conclusion:
  - major savings should come from retrieval scope control and compact active
    memory surfaces rather than reducing mandatory quality gates,
  - tiered profile UX is preferred over many independent toggles for daily use,
  - profile/override behavior must be deterministic and testable.

---

# PO -> TL Handoff — US-0049 (Legacy DONE-Story Acceptance/Traceability Backfill Guard)

## Discovery context (fresh PO run)

Discovery run for **US-0049** in fresh PO context. Story remains **OPEN**. Scope confirmed: deterministic detection and bounded repair for legacy DONE-story vs acceptance/traceability drift, with one-time backfill mode, ongoing guard, audit report, and reason-code vocabulary.

## Intake context

User hint: legacy DONE-story acceptance/traceability backfill guard. Context: US-0017 and US-0030 were DONE in backlog but unchecked in acceptance and not clearly represented in traceability/release artifacts.

## Duplicate/overlap evaluation

- **US-0045** (canonical status + one-time normalization): establishes contract and normalization concept; does not define the dedicated guard procedure, audit report schema, or reason-code vocabulary for legacy-DONE drift.
- **US-0043** (backlog reconciliation at release): forward-looking release-boundary reconciliation; does not cover one-time backfill for already-drifted legacy stories or ongoing guard with explicit audit report.
- **US-0024** (memory drift audit): read-only artifact-vs-code audit; different scope from backlog-vs-acceptance/traceability drift.
- **Assessment**: Not a duplicate. US-0049 focuses on the operational guard/backfill mechanism, audit report format, and reason codes for the specific "backlog DONE vs acceptance/traceability disagree" case; complements US-0045 and US-0043.

## Scope (TL)

- **In scope**: Detection rule for legacy drift (backlog DONE and acceptance unchecked or traceability/release missing). Bounded target-scoped repair only. Audit report with story ID, prior/resolved state, reason code, evidence ref. Reason-code vocabulary (e.g. `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING`). Optional one-time backfill mode + ongoing guard at reconciliation/release (or dedicated check). Template parity and regression coverage for backfill/guard behavior.
- **Out of scope**: Changing canonical status ownership (US-0045). Broad reconciliation semantics beyond target-scoped legacy repair. Runtime product feature behavior.

## Discovery addendum — US-0049

- **Detection rule**: Legacy drift = backlog status DONE and (acceptance checklist item for that story unchecked OR traceability index/state lacks entry OR release artifacts lack clear representation for that story).
- **Audit report**: Canonical artifact (e.g. `docs/engineering/legacy-drift-audit.md`) with required fields: story ID, prior acceptance state, prior traceability state, resolved state(s), reason code, evidence reference.
- **Operator UX**: Guard block or repair must emit explicit reason codes and remediation so operators can fix or escalate by decision; no silent block.
- **Research anchor**: R-0023; align with US-0045 and US-0043 boundaries without duplicating their scope.

## Risks

- Backfill run on large backlogs may touch many entries; keep repair target-scoped and report-only for audit so impact is inspectable.
- Guard at release boundary could block release if legacy drift is detected; reason codes and remediation guidance must be explicit so operators can fix or override by decision.

## Recommendation

- Implement detection and audit report first; then one-time backfill mode; then ongoing guard integration at release/reconciliation boundaries. Regression tests should cover no-drift, single-drift repair, and guard block/repair with reason code.

## Research reference

- **R-0023**: Legacy DONE-story acceptance/traceability backfill guard and audit reporting (intake-time research).

## Next phase

- **Proceed to `/research`** for US-0049 to refine detection rule, audit artifact location/schema, reason-code contract, and guard integration points. Then `/architecture` and `/sprint-plan` for implementation tasks.

---

# Discovery Addendum — US-0039 (Release Gate Tightening)

## Discovery focus and references

- Discovery objective: sharpen US-0039 scope for research and implementation with mandatory gates, deterministic ordering, auditable evidence, no bypass without decision gate, and template parity.
- References: `docs/product/vision.md` (Discovery Notes — US-0039), `docs/product/backlog.md` (US-0039 + discovery notes).
- User focus: release gate tightening — mandatory check-in test + QA + UAT completeness gates, deterministic ordering, auditable gate evidence, no bypass without decision gate, template parity.

## Discovery conclusions for TL

- **Mandatory gates**: `/release` must enforce (1) check-in test pass (TEST_COMMAND baseline), (2) QA completion evidence (no unresolved blocking findings in sprint context), (3) UAT completeness (no placeholder, incomplete, or unresolved-fail state). All three are required in default configuration.
- **Deterministic order**: gates must run in fixed order (test → QA → UAT → release-note/runbook) and be documented so audit trails are unambiguous.
- **Auditable evidence**: each gate writes pass/fail and evidence pointers to handoff/state artifacts; no silent or inferred state so QA/TL can audit decisions.
- **No bypass by default**: no release path may skip these gates in default configuration; any override requires explicit decision gate + documented rationale (e.g. DEC-xxxx).
- **Template parity**: active and `template/` release/qa/execute guidance must stay behaviorally aligned for gate semantics.

## Research handoff targets

1. Define canonical evidence sources and artifact locations for each gate (where test result, QA evidence, UAT evidence are read/written).
2. Define exact gate evaluation order and integration points in `/release` flow (and any verify-work/release boundary steps).
3. Define reason-code taxonomy for gate failures (e.g. CHECK_IN_TEST_FAILED, QA_BLOCKING_UNRESOLVED, UAT_INCOMPLETE) and remediation guidance contract.
4. Define regression matrix: positive (all gates pass), negative (each gate fail path, stale evidence, bypass attempt without decision gate).
5. Define template-parity verification: which files and behaviors must match between active and `template/` for release gate semantics.

## Next phase

- **Proceed to `/research`** for US-0039 with emphasis on evidence contract, gate order, reason-code design, and template-parity scope. No architecture or implementation in this step; research informs TL architecture and sprint planning.

---

# PO -> TL Handoff — US-0048 (Phase-Isolation Enforcement Gap Closure)

## Intake Context

User reported a process-compliance breach: `/auto` flow was executed in one
agent context instead of fresh subagent contexts per phase. User requested this
gap to be closed, not just documented.

## Duplicate/overlap evaluation

- Related stories:
  - `US-0023` (fresh context model baseline)
  - `US-0037` (deterministic `/auto` continuation)
  - `US-0047` (bulk-mode isolation granularity)
- Assessment: this is not a duplicate. Existing stories define behavior but do
  not hard-enforce/process-gate single-run context drift in all paths.

## Options considered (guided intake)

1. **Soft control**: add deviation logging only (low effort, lower safety).
2. **Strict control**: add hard enforcement + auditable evidence + fail-closed
   gates (higher effort, closes recurrence risk).

## Recommendation

- Recommend **Option 2 (strict control)**.
- User intent is explicit: prevent recurrence and enforce workflow rules.

## Accepted story

- `US-0048` — Enforced Per-Phase Subagent Isolation with Audit Gate
- Priority: P1
- Status: OPEN
- Research reference: `R-0018`

## TL scope boundaries

- In scope:
  - hard enforcement in orchestration contracts
  - isolation evidence schema and checkpoints
  - deterministic reason codes and remediation guidance
  - verify/release gate integration and regression coverage
  - active/template parity
- Out of scope:
  - runtime product feature changes
  - external orchestration platform migration

## Risks

- Over-strict validation may block runs if evidence writes are incomplete.
- Backward compatibility risk if historical artifacts are missing new evidence
  fields.

## Mitigations

- Add deterministic remediation paths and bounded migration guidance for legacy
  artifacts.
- Keep enforcement default-safe but fail closed only when target-phase evidence
  is required and missing/invalid.

## Discovery Addendum — US-0048

### Discovery focus and references

- Discovery objective: sharpen US-0048 scope for architecture/research with
  operator UX expectations and enforcement boundaries.
- References: `docs/product/vision.md` (Discovery Notes — US-0048),
  `docs/product/backlog.md` (US-0048), `docs/engineering/research.md` (R-0018).
- User-reported gap: auto run executed in one agent context instead of fresh
  subagent per phase; enforcement must close this recurrence risk.

### Discovery conclusions for TL

- Isolation must be **enforceable**, not advisory: policy text exists; execution
  can still reuse context without deterministic detection/gate.
- Evidence schema expectations (from R-0018): phase id, role, fresh-context
  marker, timestamp, evidence ref; machine-checkable and auditable.
- Operator UX: fail-closed with **explicit diagnostics** (reason code, phase,
  evidence ref, remediation) — no silent block or vague error.
- Gate placement: workflow progression and release boundaries (including
  `/verify-work`, `/release`) must block on missing/invalid isolation evidence.
- Resume/pause: isolation provenance must survive checkpoint boundaries so
  continuation remains trustworthy.

### Research handoff targets

1. Define canonical isolation evidence schema and artifact locations (where
   evidence is written and read for gates).
2. Define gate placement and evaluation order (when isolation is checked in
   `/auto`, phase transitions, `/verify-work`, `/release`).
3. Define reason-code taxonomy (e.g. `PHASE_CONTEXT_ISOLATION_MISSING`,
   `PHASE_CONTEXT_ISOLATION_VIOLATION`) and remediation guidance contract.
4. Define regression matrix: positive (valid evidence allows progression),
   negative (missing evidence, reused context, invalid role/phase mapping).
5. Define backward compatibility / migration for artifacts lacking new evidence
   fields (bounded migration or explicit legacy handling).

### Next phase

- **Proceed to `/research`** for US-0048 with emphasis on evidence schema,
  gate placement, reason-code design, and regression coverage. No architecture
  or implementation in this step; research informs TL architecture and
  sprint planning.

---

# PO -> TL Handoff — Intake: Release Doc Delta Gate + Optional Spec Pack

## Intake Context

User request in fresh `/intake` context:

1. Release gate must include README/runbook delta check when commands/flags changed.
2. Also create Design Concept, CRS, and Technical Specification if enabled.

This is treated as process/workflow enhancement (not feature implementation).

## Overlap and Duplicate Evaluation

- No direct duplicate found in current backlog.
- Related but non-duplicate stories:
  - `US-0015`: runbook command documentation intent (narrower and already handled).
  - `US-0024`: memory drift auditing (advisory/read-only, not release blocking).
  - `US-0028` and `US-0029`: optional flag-driven behavior pattern (useful precedent).
- Decision: add two new stories instead of modifying existing ones to keep scope explicit and testable.

## Stories Accepted

### US-0030 — Release Gate for Command/Flag Documentation Delta
- Intent: prevent release drift where behavior changes are not reflected in docs.
- Scope: release/process guardrail requiring README + runbook parity for changed commands/flags.
- Priority: P1
- Status: OPEN
- Backlog artifact: `docs/product/backlog.md` (8 ACs)

### US-0031 — Optional Documentation Pack (Design Concept, CRS, Technical Spec)
- Intent: support teams that require formal docs without imposing overhead on everyone.
- Scope: optional generation/validation path controlled by config/flag.
- Priority: P2
- Status: OPEN
- Backlog artifact: `docs/product/backlog.md` (8 ACs)

## Split/Merge Rationale

- Split was chosen because the stories have different triggers and risks:
  - `US-0030` is always in release-critical path and should be strict/blocking.
  - `US-0031` is optional and policy-driven, with zero-overhead expectation when disabled.
- Merging would blur blocking behavior and make acceptance testing ambiguous.

## Boundaries for TL

- In scope:
  - Workflow rules/commands/readiness checks.
  - Artifact conventions, role ownership, and pass/fail criteria.
  - Template parity where process guidance exists in both active and `template/`.
- Out of scope:
  - New runtime product features.
  - Domain-specific content authoring beyond minimum structure for Design Concept/CRS/Technical Spec.

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Delta check over-blocks unrelated releases | Throughput drops | Require explicit changed command/flag evidence before gate applies |
| Delta check under-detects actual behavior changes | Doc drift persists | Define canonical detection scope and required evidence output in gate report |
| README vs runbook ownership unclear | Ping-pong and delays | Assign ownership by phase/role and enforce in handoff checklist |
| Optional spec-pack defaults to noisy workflow | Team friction | Keep default disabled and require explicit enable flag |
| Spec-pack artifacts become shallow placeholders | False confidence | Enforce minimum required sections and completeness checks |
| Active/template drift for new guidance | Inconsistent installs | Include template parity AC and verify in release checklist |

## TL Planning Recommendations

1. Implement `US-0030` first (higher release risk reduction, tighter scope).
2. Implement `US-0031` second (optional path, broader cross-phase ownership).
3. Define one canonical flag for spec-pack enablement early in architecture.
4. Define deterministic evidence format for doc-delta gate output so QA can assert pass/fail reliably.

## Expected Deliverables in Next Phases

- Architecture defines:
  - command/flag delta detection boundaries,
  - blocking conditions and override policy (if any),
  - spec-pack artifact names/locations and required sections.
- Sprint plan maps both stories to tasks with explicit template parity checks.
- QA verifies gating behavior with positive/negative cases for both enabled and disabled modes.

---

## Intake Addendum — Optional User-Friendly Feature Instructions

### New intake

User asks for "an option for generating a user-friendly instruction/doc of every feature."

### Overlap and duplicate evaluation

- Closest overlap: `US-0031` (optional spec-pack with Design Concept, CRS, Technical Spec).
- Assessment: related but not duplicate.
  - `US-0031` targets internal/engineering specification artifacts.
  - New request targets user-facing, feature-level usage instructions.
- Decision: create a new story to avoid mixing audiences, ownership, and acceptance checks.

### Accepted story

#### US-0032 — Optional Feature User Guide Generation
- Priority: P2
- Status: OPEN
- Why separate from `US-0031`:
  - Keeps technical spec completeness checks separate from user-guide quality checks.
  - Prevents one optional mode from becoming ambiguous and overly broad.
  - Preserves clear role boundaries (technical authorship vs end-user documentation tone).

### TL guidance and boundaries

- In scope:
  - Optional, flag-controlled per-feature user guide artifacts.
  - Deterministic required sections and validation when enabled.
  - Story-to-guide traceability and release/handoff references.
  - Active/template parity for docs/commands/rules touching this mode.
- Out of scope:
  - Replacing or merging with `US-0031` technical spec-pack artifacts.
  - Mandatory overhead in default mode.
  - Full product manual generation beyond per-feature guidance.

## Discovery Addendum — US-0032 (Optional Feature User Guide Generation)

### Discovery focus and references

- Discovery objective: refine US-0032 into an architecture-ready, optional user-guide mode that fits the existing docs-as-code workflow.
- References:
  - `docs/product/backlog.md` (US-0032 ACs and discovery notes).
  - `docs/product/vision.md` (Discovery Notes — US-0032).
  - `docs/engineering/research.md` (R-0021).
  - `US-0031` spec-pack story and its ACs.

### Discovery conclusions for TL

- Audience split is critical: US-0032 should produce end-user-facing how-to guides (task-focused, friendly tone), while US-0031 remains technical/engineering documentation; content and ownership must not be mixed.
- User-guide mode must be controlled by a single flag (default: disabled) and impose **zero required steps or blocking checks** when disabled; no hidden gates in intake/architecture/sprint/execute/qa/release.
- When enabled, each accepted feature story should have **one canonical guide artifact** (story/feature-ID based naming) with a deterministic schema: purpose, prerequisites, step-by-step usage, example, limitations, troubleshooting.
- Guides must be integrated into the docs-as-code flow: stored in-repo, updated in the same change as the feature, and validated via simple structural checks (required sections present) instead of subjective scoring.
- Traceability expectations: backlog/acceptance/release handoffs should be able to reference the corresponding guide when mode is on, without making those artifacts the canonical source of guide content.

### Research handoff targets (R-0021 anchor)

Per **R-0021**, TL should:

1. Define the canonical location and naming pattern for per-feature guides (e.g. `docs/user-guides/US-xxxx.md` or equivalent) and how it links back to stories and sprints.
2. Refine the minimal, testable schema for user guides (required sections and any metadata/frontmatter needed for automation).
3. Evaluate interaction boundaries with spec-pack mode (US-0031) to avoid duplicated content responsibilities while keeping both optional.
4. Propose validation and gating behavior when the user-guide flag is enabled (which phases check for guide completeness, and how failures are reported).
5. Identify risks around drift between feature behavior and guides and recommend lightweight mitigation patterns (definition-of-done hooks, regression checks, or release-time reminders).

### Next phase

- **Proceed to `/research` for US-0032**, using `R-0021` as the primary research anchor and this discovery addendum as scope clarification. No implementation or sprint planning yet; `/research` should finalize patterns and constraints for TL architecture.

