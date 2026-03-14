# Dev -> QA Handoff — Sprint S0034 (US-0055)

## Status

S0034 implementation is complete for **US-0055** (Deterministic Status
Reconciliation Command) and ready for `/qa`.

## Scope completed

1. **Command contract (T-001, T-002 / AC-1, AC-2)**: added new deterministic
   `/status-reconcile` command with mismatch detection matrix and bounded repair
   workflow.
2. **Canonical precedence + normalization (T-003..T-005 / AC-3..AC-5)**:
   command defines backlog authority, derived-surface reconciliation semantics,
   and target-scoped mutation boundaries.
3. **Continuation readiness (T-006 / AC-6)**: command defines deterministic
   resume update behavior to next OPEN story and intended phase.
4. **Evidence + diagnostics (T-007, T-008 / AC-7, AC-8)**: normalization report
   and state-checkpoint evidence contract plus deterministic reason-code set.
5. **Regression + parity (T-009, T-010 / AC-9, AC-10)**: test runners extended
   with US-0055 assertions and active/template docs/command parity updated.

## QA verification checklist (S0034)

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and
   confirm PASS including US-0055 assertion block.
2. Confirm active/template parity:
   - `.cursor/commands/status-reconcile.md`, `template/.cursor/commands/status-reconcile.md`
   - `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
   - `README.md`, `template/README.md`
3. Confirm sprint artifacts:
   - `sprints/S0034/tasks.md` all done
   - `sprints/S0034/progress.md` implementation complete
   - `sprints/S0034/summary.md` present and consistent

## Artifacts updated (S0034)

- `.cursor/commands/status-reconcile.md`, `template/.cursor/commands/status-reconcile.md`
- `docs/engineering/architecture.md`, `docs/engineering/research.md`
- `decisions/DEC-0037.md`, `docs/engineering/decisions.md`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0034/tasks.md`, `sprints/S0034/progress.md`, `sprints/S0034/summary.md`

---

# Dev -> QA Handoff — Sprint S0033 (US-0054)

## Status

S0033 implementation is complete for **US-0054** (Configurable Multi-Target
Release Publish with Confirmation Gate) and ready for `/qa`.

## Scope completed

1. **Publish control surface (T-001, T-004 / AC-1, AC-4)**: added deterministic
   release publish controls in scratchpad (`RELEASE_PUBLISH_MODE`,
   `RELEASE_TARGETS_FILE`, `RELEASE_TARGETS_DEFAULT`) with default `confirm`.
2. **Target taxonomy + generic support (T-002 / AC-2)**: documented built-in
   target taxonomy (`npm|choco|brew|git|docker|cloud`) and generic `custom`
   target contract.
3. **SSH support (T-003 / AC-3)**: added first-class `ssh` target contract in
   canonical target schema file with env-referenced host/user/auth fields.
4. **Deterministic run safety (T-005, T-006 / AC-5, AC-6)**: release contract
   now includes deterministic ordering, selection, and fail-fast invalid-config
   reason codes.
5. **Secret handling + parity (T-007, T-008 / AC-7, AC-8)**: env-reference-only
   secret policy documented and mirrored across active/template artifacts.
6. **Regression and invariants (T-009, T-010 / AC-9, AC-10)**: test runners now
   assert US-0054 contracts while preserving mandatory release gate semantics.

## QA verification checklist (S0033)

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and
   confirm PASS including US-0054 assertions.
2. Confirm active/template parity:
   - `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
   - `.cursor/commands/release.md`, `template/.cursor/commands/release.md`
   - `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
   - `README.md`, `template/README.md`
   - `docs/engineering/release-targets.json`, `template/docs/engineering/release-targets.json`
3. Confirm sprint artifacts:
   - `sprints/S0033/tasks.md` all done
   - `sprints/S0033/progress.md` implementation complete
   - `sprints/S0033/summary.md` present and consistent

## Artifacts updated (S0033)

- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
- `.cursor/commands/release.md`, `template/.cursor/commands/release.md`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `docs/engineering/release-targets.json`, `template/docs/engineering/release-targets.json`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0033/tasks.md`, `sprints/S0033/progress.md`, `sprints/S0033/summary.md`

---

# Dev -> QA Handoff — Sprint S0032 (US-0053)

## Status

S0032 implementation is complete for **US-0053** (Context Compaction and Tiered
Token-Cost Optimization Mode) and ready for `/qa`.

## Scope completed

1. **Tiered profile contract (T-001..T-003 / AC-1..AC-3)**: introduced
   `TOKEN_PROFILE=lean|balanced|full` with deterministic semantics and
   manual-override precedence in active/template scratchpad and docs.
2. **State compaction policy (T-004 / AC-4)**: defined active hot-surface policy
   in `docs/engineering/state.md` and added archive contract in
   `docs/engineering/state-archive/README.md` (active + template).
3. **Decisions compaction (T-005 / AC-5)**: compacted
   `docs/engineering/decisions.md` into bounded summaries with canonical
   `decisions/DEC-xxxx.md` linkouts; aligned template baseline.
4. **`/ask` narrow-read policy (T-006 / AC-6)**: updated active/template
   `.cursor/commands/ask.md` to targeted-first, bounded expansion retrieval with
   explicit unresolved behavior.
5. **Parity + regression coverage (T-007..T-009 / AC-7, AC-8)**: aligned
   active/template command/runbook/README/scratchpad/state contracts and added
   US-0053 assertions in both test runners.
6. **Operator guidance and invariants (T-010 / AC-9, AC-10)**: updated runbook
   and README with profile tradeoffs/escalation guidance while preserving
   mandatory release-gate semantics and ID/history invariants.

## QA verification checklist (S0032)

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and
   confirm PASS including US-0053 assertion block:
   - `TOKEN_PROFILE` contract in active/template scratchpads
   - `/ask` narrow-read contract (active + template)
   - runbook/README US-0053 guidance parity
   - state archive README presence (active + template)
   - compact decisions-index assertions
2. Confirm active/template parity for token-profile + compaction contracts:
   - `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
   - `.cursor/commands/ask.md`, `template/.cursor/commands/ask.md`
   - `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
   - `README.md`, `template/README.md`
   - `docs/engineering/state.md`, `template/docs/engineering/state.md`
3. Confirm sprint artifacts:
   - `sprints/S0032/tasks.md` all done
   - `sprints/S0032/progress.md` implementation complete
   - `sprints/S0032/summary.md` present and consistent

## Artifacts updated (S0032)

- `.cursor/commands/ask.md`, `template/.cursor/commands/ask.md`
- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `docs/engineering/state.md`, `template/docs/engineering/state.md`
- `docs/engineering/state-archive/README.md`, `template/docs/engineering/state-archive/README.md`
- `docs/engineering/decisions.md`, `template/docs/engineering/decisions.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0032/tasks.md`, `sprints/S0032/progress.md`, `sprints/S0032/summary.md`
- `docs/engineering/state.md`, `handoffs/dev_to_qa.md`

---

# Dev -> QA Handoff — Sprint S0031 (US-0052)

## Status

S0031 implementation is complete for **US-0052** (Optional Fresh-Project ID
Namespace Bootstrap) and ready for `/qa`.

## Scope completed

1. **Bootstrap control contract (T-001 / AC-1, AC-6)**: added explicit
   `ID_NAMESPACE_BOOTSTRAP` scratchpad switch (active + template), default-off.
2. **Freshness eligibility and bootstrap behavior (T-002, T-003 / AC-2, AC-4)**:
   intake/research/architecture contracts now define deterministic freshness
   checks and first-ID bootstrap semantics (`US-0001`, `DEC-0001`, `R-0001`)
   only when eligible.
3. **Compatibility-safe continuation (T-004, T-006 / AC-3, AC-5)**: contracts
   require highest-existing-ID continuation for non-fresh repos, collision-safe
   generation, and no historical renumbering.
4. **Deterministic diagnostics (T-005 / AC-4, AC-6)**: ineligible bootstrap
   requests now require `ID_BOOTSTRAP_NOT_FRESH` diagnostic with remediation
   guidance.
5. **Operator guidance (T-007 / AC-6)**: runbook/README (active + template)
   include bootstrap behavior, eligibility criteria, and constraints.
6. **Regression + parity (T-008..T-010 / AC-7, AC-8)**: both test runners now
   assert US-0052 contracts across active/template command, agent, runbook, and
   README surfaces.

## QA verification checklist (S0031)

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and
   confirm PASS including US-0052 assertion block:
   - `ID_NAMESPACE_BOOTSTRAP` scratchpad keys (active + template)
   - bootstrap policy in intake/research/architecture commands
   - bootstrap policy in PO and Tech Lead agents
   - runbook/README US-0052 guidance parity
2. Confirm active/template parity for updated command contracts:
   - `.cursor/commands/intake.md` and `template/.cursor/commands/intake.md`
   - `.cursor/commands/research.md` and `template/.cursor/commands/research.md`
   - `.cursor/commands/architecture.md` and `template/.cursor/commands/architecture.md`
3. Confirm active/template parity for updated agent guidance:
   - `.cursor/agents/po.mdc` and `template/.cursor/agents/po.mdc`
   - `.cursor/agents/tech-lead.mdc` and `template/.cursor/agents/tech-lead.mdc`
4. Confirm runbook and README US-0052 guidance parity:
   - `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
   - `README.md`, `template/README.md`
5. Confirm baseline report snapshot:
   - `tests/report.md` timestamp `2026-03-12T19:43:28Z`, `Pass: 440`, `Fail: 0`.

## Artifacts updated (S0031)

- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
- `.cursor/commands/intake.md`, `template/.cursor/commands/intake.md`
- `.cursor/commands/research.md`, `template/.cursor/commands/research.md`
- `.cursor/commands/architecture.md`, `template/.cursor/commands/architecture.md`
- `.cursor/agents/po.mdc`, `template/.cursor/agents/po.mdc`
- `.cursor/agents/tech-lead.mdc`, `template/.cursor/agents/tech-lead.mdc`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0031/tasks.md`, `sprints/S0031/progress.md`, `sprints/S0031/summary.md`
- `docs/engineering/state.md`, `handoffs/dev_to_qa.md`

---

# Dev -> QA Handoff — Sprint S0030 (US-0051)

## Status

S0030 implementation is complete for **US-0051** (Intelligent Intake
Decomposition and Risk-Aware PO Questioning) and ready for `/qa`.

## Scope completed

1. **Decomposition heuristics and trigger contract (T-001, T-005 / AC-1, AC-5)**:
   active/template `/intake` now include deterministic breadth/risk evaluation,
   bounded split trigger behavior, and explicit single-story default for narrow
   intake.
2. **Vertical-slice decomposition quality (T-002 / AC-1, AC-2)**: intake split
   guidance enforces independently valuable/testable stories and avoids
   technical-layer-only decomposition by default.
3. **Split rationale persistence (T-003 / AC-3, AC-9)**: intake contract now
   requires explicit rationale, split axis, and story boundary evidence in
   product and handoff artifacts.
4. **Explicit user split decision authority (T-004 / AC-4)**: guidance now
   requires accept/merge/adjust confirmation before final persistence.
5. **Risk-aware adaptive questioning (T-006, T-007 / AC-6, AC-7)**: PO behavior
   now expands follow-ups for broad/high-risk intake and keeps rounds bounded.
6. **Low-touch compatibility preserved (T-008 / AC-8)**:
   `INTAKE_GUIDED_MODE=0` remains minimal-overhead with mandatory duplicate
   safety and no forced decomposition.
7. **Artifact traceability contract (T-009 / AC-9)**: decomposition/questioning
   evidence requirement added for `backlog.md`, `acceptance.md`, and
   `handoffs/po_to_tl.md`.
8. **Parity + regression (T-010, T-011 / AC-10)**: updated active/template
   intake + PO guidance, runbook/README docs, and both test runners with new
   US-0051 assertions.

## QA verification checklist (S0030)

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and
   confirm PASS including US-0051 assertion block:
   - deterministic decomposition evaluator
   - accept/merge/adjust control
   - bounded questioning contract
   - no-forced-decomposition low-touch behavior
   - runbook/README US-0051 documentation parity
2. Confirm active/template intake command parity in:
   - `.cursor/commands/intake.md`
   - `template/.cursor/commands/intake.md`
3. Confirm active/template PO agent parity in:
   - `.cursor/agents/po.mdc`
   - `template/.cursor/agents/po.mdc`
4. Confirm runbook and README US-0051 guidance parity:
   - `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
   - `README.md`, `template/README.md`
5. Confirm baseline report snapshot:
   - `tests/report.md` timestamp `2026-03-12T17:48:56Z`, `Pass: 422`, `Fail: 0`.

## Artifacts updated (S0030)

- `.cursor/commands/intake.md`, `template/.cursor/commands/intake.md`
- `.cursor/agents/po.mdc`, `template/.cursor/agents/po.mdc`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `README.md`, `template/README.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0030/tasks.md`, `sprints/S0030/progress.md`, `sprints/S0030/summary.md`
- `docs/engineering/state.md`, `handoffs/dev_to_qa.md`

---

# Dev -> QA Handoff — Sprint S0029 (US-0050)

## Status

S0029 implementation is complete for **US-0050** (Clean Install Hygiene and Complete Clean-Repo Coverage) and ready for `/qa`.

## Scope completed

1. **Ownership manifest contract (T-001 / AC-2)**: Added canonical manifest `docs/engineering/context/installer-owned-paths.manifest` and template parity copy.
2. **Installer refactor to shared contract (T-002..T-004 / AC-1, AC-2)**: `installer.ps1`, `installer.sh`, and `installer.py` all consume manifest sections for install and clean path scope.
3. **Expanded clean-repo safety coverage (T-005 / AC-3)**: clean removes manifest-owned workflow artifacts (including docs/user-guides, validate scripts, workflow files, `.its-magic-version`) while preserving non-framework markers.
4. **Template starter neutrality (T-006 / AC-4)**: removed seeded operational rows from template engineering starter artifacts (`status-normalization-report`, `compatibility-*`, `component-scope-*`).
5. **Hardcoded reference neutralization (T-007 / AC-5)**: removed fixed `DEC-0011` wording from template research entry format header.
6. **Fresh-install baseline regression (T-008 / AC-6)**: tests verify missing install yields neutral starter artifacts and no hardcoded `DEC-0011` in starter research.
7. **Lifecycle clean/install regression (T-009 / AC-8)**: tests validate clean-repo completeness for owned paths and non-framework preservation in both installer and CLI paths.
8. **Upgrade/parity verification (T-010 / AC-7, AC-9)**: upgrade lifecycle assertions remain passing; active/template clean semantics and ownership manifest parity validated.
9. **QA blocker remediation (execute loop)**: synced stable Homebrew formula (`packaging/homebrew/its-magic.rb`) to package version `0.1.2-20` (URL + version + SHA256), resolving baseline version-sync test failures.

## QA verification checklist (S0029)

1. Run `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` and review new S0029 checks in `tests/report.md`.
2. Confirm installers load shared manifest: `installer.ps1`, `installer.sh`, `installer.py` reference `installer-owned-paths.manifest`.
3. Confirm clean-repo manifest scope includes docs/user-guides, scripts/validate-and-push.*, `.github/workflows/ci.yml`, `.github/workflows/deploy.yml`, `.its-magic-version`.
4. Confirm template starter neutrality in:
   - `template/docs/engineering/status-normalization-report.md`
   - `template/docs/engineering/compatibility-report.md`
   - `template/docs/engineering/compatibility-signals.md`
   - `template/docs/engineering/component-scope.md`
   - `template/docs/engineering/component-scope-report.md`
   - `template/docs/engineering/research.md` (no `DEC-0011` string)
5. Confirm README/help text alignment for clean-repo semantics:
   - `README.md`, `template/README.md`, `bin/its-magic.js`, and installer help output.
6. Confirm Homebrew stable formula version-sync checks pass:
   - `Homebrew stable formula URL uses npm version tag`
   - `Homebrew stable formula version matches npm version`
7. Verify current baseline report is green:
   - `tests/report.md` timestamp `2026-03-11T22:03:11Z`, `Pass: 404`, `Fail: 0`.

## Artifacts updated (S0029)

- `docs/engineering/context/installer-owned-paths.manifest`
- `template/docs/engineering/context/installer-owned-paths.manifest`
- `installer.ps1`, `installer.sh`, `installer.py`, `bin/its-magic.js`
- `packaging/homebrew/its-magic.rb`
- `README.md`, `template/README.md`
- Template engineering starter artifacts listed in scope item #4
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0029/tasks.md`, `sprints/S0029/progress.md`, `sprints/S0029/summary.md`
- `docs/engineering/state.md`, `handoffs/dev_to_qa.md`

---

# Dev -> QA Handoff — Sprint S0028 (US-0049)

## Status

S0028 implementation is complete for **US-0049** (Legacy DONE-Story Acceptance/Traceability Backfill Guard) and ready for `/qa`.

## Scope completed

1. **Detection rule (T-001/AC-1)**: Documented in runbook: legacy drift = backlog DONE and (acceptance unchecked OR traceability/state lacks entry OR release artifacts lack representation).
2. **Bounded repair (T-002/AC-2)**: Only stories matching the rule are mutated; no broad rewrite (runbook + release guard).
3. **Audit report (T-003/AC-3)**: Canonical path `docs/engineering/legacy-drift-audit.md` with required fields (story_id, prior_acceptance_state, prior_traceability_state, resolved_state, reason_code, evidence_ref, timestamp); created in repo and template.
4. **Reason codes (T-004/AC-4)**: `BACKLOG_DONE_ACCEPTANCE_UNCHECKED`, `BACKLOG_DONE_TRACEABILITY_MISSING`, `BACKLOG_DONE_RELEASE_ARTIFACT_MISSING` with remediation in runbook and release fail-safe list (active + template).
5. **One-time backfill (T-005/AC-5)**: Documented in runbook: explicit trigger, idempotent when no drift, emit audit.
6. **Ongoing guard (T-006/AC-6)**: Release step 3e — legacy drift guard at release/reconciliation; block or target-scoped repair with audit append; deterministic (active + template).
7. **Template parity (T-007/AC-7)**: template runbook, release.md, legacy-drift-audit.md aligned with active.
8. **Regression (T-008/AC-8)**: 14 US-0049 assertions in `tests/run-tests.ps1` (canonical path, runbook section, reason codes, idempotent no-drift, release guard).

## QA verification checklist (S0028)

1. Run: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`; confirm PASS including all "Legacy DONE-story drift" / US-0049 assertions (block #27).
2. Confirm `docs/engineering/legacy-drift-audit.md` exists (active) with schema and required fields.
3. Confirm runbook section "Legacy DONE-story drift detection and guard (US-0049)" with detection rule, reason codes, one-time backfill, ongoing guard (active + template).
4. Confirm release command step 3e "Legacy drift guard (US-0049 / DEC-0031)" and the three reason codes in fail-safe list (active + template).
5. Spot-check template parity: `template/docs/engineering/runbook.md`, `template/.cursor/commands/release.md`, `template/docs/engineering/legacy-drift-audit.md`.

## Artifacts updated (S0028)

- `docs/engineering/runbook.md`, `docs/engineering/legacy-drift-audit.md`
- `.cursor/commands/release.md`
- `template/docs/engineering/runbook.md`, `template/.cursor/commands/release.md`, `template/docs/engineering/legacy-drift-audit.md`
- `tests/run-tests.ps1`
- `sprints/S0028/tasks.md`, `progress.md`, `summary.md`, `uat.md`, `uat.json`
- `docs/engineering/state.md`, `handoffs/dev_to_qa.md`

---

# Dev -> QA Handoff — Sprint S0027 (US-0032)

## Status

S0027 implementation is complete for **US-0032** (Optional Feature User Guide Generation) and ready for `/qa`.

## Scope completed

1. **USER_GUIDE_MODE** flag (default 0) in active and template scratchpad.
2. When **USER_GUIDE_MODE=0**: intake, architecture, sprint-plan, execute, qa, release add no required user-guide steps or blocking checks (zero overhead); documented in all six commands (active + template).
3. Canonical path **docs/user-guides/US-xxxx.md** per feature story; runbook section and **docs/user-guides/README.md** (active + template).
4. Minimum guide schema: Purpose, Prerequisites, Usage steps, Example, Limitations, Troubleshooting in runbook and docs/user-guides/README.md.
5. Release gate step 3d: when USER_GUIDE_MODE=1, validate target-story user guide; block with **USER_GUIDE_INCOMPLETE** when missing or required sections absent (release.md active + template).
6. Story ID → user guide traceability in handoffs.mdc and runbook; referenced in handoff/release context.
7. Boundaries with US-0031: user guides end-user only; no duplicate spec-pack content; separation in runbook and docs/user-guides/README.md.
8. Template parity: commands, runbook, README, docs/user-guides/README.md, handoffs.mdc; regression tests in tests/run-tests.ps1 and tests/run-tests.sh (USER_GUIDE_MODE, USER_GUIDE_INCOMPLETE, runbook/README/user-guides README).

## QA verification checklist (S0027)

1. Run: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (or `sh tests/run-tests.sh`); confirm PASS including "Optional user-guide documentation checks (US-0032)".
2. Confirm scratchpad (active + template) contains USER_GUIDE_MODE=0 and intake/release document zero-overhead when disabled.
3. Confirm runbook has "Optional user-guide documentation mode (US-0032)" with canonical path, schema, validation, and boundary with spec-pack.
4. Confirm docs/user-guides/README.md exists (active + template) with path, schema, and US-0031 boundary.
5. Confirm release command (active + template) has step 3d and reason code USER_GUIDE_INCOMPLETE.
6. Spot-check template parity for commands, runbook, README, handoffs.mdc.

## Artifacts updated (S0027)

- `.cursor/scratchpad.md`, `template/.cursor/scratchpad.md`
- `.cursor/commands/intake.md`, `architecture.md`, `sprint-plan.md`, `execute.md`, `qa.md`, `release.md` (+ template)
- `.cursor/rules/handoffs.mdc` (+ template)
- `docs/engineering/runbook.md`, `docs/user-guides/README.md`, `README.md` (+ template)
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0027/tasks.md`, `progress.md`, `summary.md`, `uat.json`, `uat.md`

---

# Dev -> QA Handoff — Sprint S0025 (US-0048)

## Status

S0025 implementation is complete for `US-0048` (Per-phase subagent isolation) and ready for `/qa`.

## Scope completed

1. Enforced `/auto` orchestrator-only behavior with fail-closed isolation enforcement and reason codes (active + template).
2. Defined isolation evidence schema + canonical locations in runbook + README (active + template).
3. Added mandatory isolation evidence write requirements to phase commands and agents.
4. Tightened execute↔QA loop semantics: fresh context per cycle; marker reuse treated as stale evidence.
5. Added isolation compliance gates:
   - `/verify-work` gate blocks handoff to `/release` on isolation violations.
   - `/release` gate chain includes isolation after UAT and before finalization.
6. Added pause/resume provenance fields and `/resume` validation requirements.
7. Added US-0048 regression assertions in both test runners for active/template parity and contract presence.

## QA verification checklist

1. Run suite:
   - `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"`
2. Confirm `tests/report.md` includes PASS for US-0048 checks:
   - `/auto` includes "Per-phase isolation enforcement (US-0048 / DEC-0029)" and isolation reason codes
   - runbook includes "Per-phase subagent isolation evidence (US-0048 / DEC-0029)" and reason codes
   - `/verify-work` includes "Isolation compliance gate (US-0048 / DEC-0029)"
   - `/release` includes isolation gate and reason codes; gate chain order includes isolation after UAT
   - `/pause` includes `isolation_provenance_ref`; `/resume` validates isolation provenance
   - README documents per-phase isolation evidence (active + template)
   - dev agent documents isolation evidence (active + template)
3. Spot-check template parity by reading corresponding `template/` command/runbook/readme copies.

## Artifacts updated for QA

- `.cursor/commands/auto.md`, `execute.md`, `qa.md`, `verify-work.md`, `release.md`, `pause.md`, `resume.md` (+ `template/` copies)
- `.cursor/agents/dev.mdc`, `qa.mdc`, `release.mdc`, `curator.mdc` (+ `template/` copies)
- `docs/engineering/runbook.md`, `README.md` (+ `template/` copies)
- `handoffs/resume_brief.md`, `template/handoffs/resume_brief.md`
- `tests/run-tests.ps1`, `tests/run-tests.sh`
- `sprints/S0025/tasks.md`, `sprints/S0025/progress.md`, `sprints/S0025/summary.md`

---

# Dev -> QA Handoff — Sprint S0011 (US-0039)

## Status

S0011 implementation is complete for **US-0039** (Release Gate Tightening) and ready for `/qa`.

## Scope completed

1. **Gate chain and ordering**: Mandatory order check-in test → QA → UAT → release finalization in `.cursor/commands/release.md` and `docs/engineering/runbook.md`.
2. **Check-in test evidence**: Validity contract (present/fresh/passing) and reason codes `RELEASE_TEST_EVIDENCE_MISSING`, `RELEASE_TEST_STALE`, `RELEASE_TEST_FAILED` in release.md and state.md.
3. **QA completion gate**: No unresolved blocking findings before release; release.md, qa.md, handoffs/qa_to_dev.md.
4. **UAT completion gate**: Placeholder/incomplete/unresolved-fail block with `RELEASE_UAT_INCOMPLETE` / `RELEASE_UAT_FAILED`; S0011 uat.md/uat.json.
5. **Per-gate audit schema**: Verdict, reason_code, remediation, evidence_refs in release_notes.md, state.md, runbook.
6. **No-bypass default**: release.md and `.cursor/rules/core.mdc`.
7. **Override evidence contract**: release.md, DEC-0019, release_notes.md (decision ref, rationale, approver, risk acceptance).
8. **Regression matrix**: S0011 uat.md, uat.json, plan-verify.json (positive/negative/stale/no-bypass/override).
9. **Optional-command compatibility**: Blank LINT/TYPECHECK do not fail release; runbook, release.md, README.
10. **Template parity**: template release, qa, execute, runbook, README aligned for gate semantics.
11. **Traceability**: state.md execute checkpoint; tl_to_dev execution guardrails; regression tests in tests/run-tests.ps1 and tests/run-tests.sh.

## Required next step

- Run **`/qa`** for S0011 and verify US-0039 AC-1..AC-10 contract coverage (gate order, test/QA/UAT evidence, no-bypass, override, optional keys, regression, parity).

---

# Dev -> QA Handoff — Sprint S0026 (US-0031)

## Status

S0026 implementation is complete for `US-0031` and ready for `/qa`.

## Scope completed

1. Added `SPEC_PACK_MODE=0|1` (default 0) in active/template scratchpad.
2. Documented zero-overhead when disabled in intake/architecture/release/execute/qa.
3. Defined canonical spec-pack paths and minimum required sections in runbook;
   added `docs/engineering/spec-pack/README.md` in active and template.
4. Release gate 3c: when enabled, validate spec-pack completeness; block with
   `SPEC_PACK_INCOMPLETE` when required sections missing.
5. Traceability (story ID → three artifacts) and ownership (role/phase) in runbook.
6. Active/template parity for commands, runbook, README; US-0031 regression
   checks in `tests/run-tests.ps1` and `tests/run-tests.sh`.

## Required next step

- Run `/qa` for S0026 and verify AC-1..AC-8 contract coverage.

---

# Dev -> QA Handoff — Sprint S0024 (US-0035)

## Status

S0024 implementation is complete for `US-0035` and ready for `/qa`.

## Scope completed

1. Added optional component scope controls (`COMPONENT_SCOPE_MODE`,
   `TARGET_COMPONENTS`) in active/template scratchpad.
2. Added scope declaration/report artifacts for enabled mode.
3. Added scoped contracts in intake/architecture/sprint-plan/execute/qa/release.
4. Added release decision-gate reason code for unapproved out-of-scope impact.
5. Added US-0035 regression checks in both test runners.

## Required next step

- Run `/qa` for S0024 and verify AC-1..AC-8 contract coverage.

---

# Dev -> QA Handoff — Sprint S0023 (US-0034)

## Status

S0023 implementation is complete for `US-0034` and ready for `/qa`.

## Scope completed

1. Added optional compatibility observability mode controls and source list.
2. Added compatibility contracts in intake/architecture/execute/qa/release docs.
3. Added canonical compatibility report/signals/manifests artifacts.
4. Added release critical compatibility reason code contract.
5. Added regression checks in both test runners.

## Required next step

- Run `/qa` for S0023 and verify AC-1..AC-8 contract coverage.

---

# Dev -> QA Handoff — Sprint S0022 (US-0033)

## Status

S0022 implementation is complete for `US-0033` and ready for `/qa`.

## Scope completed

1. Added single intake switch `INTAKE_GUIDED_MODE` in scratchpad (active/template).
2. Added guided and low-touch mode behavior contracts in `/intake`.
3. Added mode-aware expectations in `po.mdc`.
4. Updated runbook/README guidance for operators.
5. Added US-0033 regression checks in both test runners.

## Required next step

- Run `/qa` for S0022 and verify AC-1..AC-9 contract coverage.

---

# Dev -> QA Handoff — Sprint S0021 (US-0045)

## Status

S0021 implementation is complete for `US-0045` and ready for `/qa`.

## Scope completed

1. Added canonical status ownership contract and deterministic reconciliation
   precedence.
2. Added one-time normalization baseline report artifact with auditable rows.
3. Added `CANONICAL_STATUS_CONFLICT` fail-safe reason code contract.
4. Added non-canonical readiness guards to `/auto` and `/execute`.
5. Added `/sprint-plan` planning-source clarification and regression checks.

## Required next step

- Run `/qa` for S0021 and verify AC-1..AC-10 contract coverage.

---

# Dev -> QA Handoff — Sprint S0020 (US-0047)

## Status

S0020 implementation is complete for `US-0047` and ready for `/qa`.

## Scope completed

1. Added explicit `/auto --execute-bulk` activation contract and default-safe fallback.
2. Added deterministic selection, bounded controls, and reason-code outputs.
3. Added team-scoped no-write guardrails for out-of-scope task handling.
4. Preserved fresh-context isolation and execute↔QA bounded loop semantics.
5. Added active/template parity updates and regression checks.

## Required next step

- Run `/qa` for S0020 and verify AC-1..AC-10 contract coverage.

---

# Dev -> QA Handoff — Sprint S0019 (US-0046)

## Status

S0019 implementation is complete for `US-0046` and ready for `/qa`.

## Scope completed

1. Added explicit `/sprint-plan --bulk` trigger and default-safe fallback behavior.
2. Added deterministic selection and bounded bulk stop reason contracts.
3. Added scratchpad bulk controls and runbook/README documentation.
4. Preserved sizing and fail-safe stop semantics.
5. Added active/template parity updates and regression checks.

## Required next step

- Run `/qa` for S0019 and verify AC-1..AC-10 contract coverage.

---

# Dev -> QA Handoff — Sprint S0014 (US-0042)

## Status

S0014 implementation is complete for `US-0042` and ready for `/qa`.

## Scope completed

1. Release findings workflow contract added to `/release`.
2. Deterministic blocked-release handoff added (`handoffs/release_to_dev.md`).
3. Post-QA release issue boundary documented in runbook/README.
4. Template parity updates completed for command/rules/docs/handoffs.
5. Regression checks added in `tests/run-tests.ps1` and `tests/run-tests.sh`.

## Required next step

- Run `/qa` for S0014 and verify AC-1..AC-8 contract coverage.

---

# Dev -> QA Handoff — Sprint S0013 (US-0041)

## Status

S0013 implementation is complete for `US-0041` and ready for `/qa`.

## Scope completed

1. Lifecycle clean-repo safety checks added for installer and CLI paths in both
   PowerShell and shell runners.
2. CLI lifecycle checks added (`missing`, `overwrite --backup`, `upgrade`,
   `clean-repo`) in both PowerShell and shell runners.
3. Invalid-mode negative-path fail-fast checks added in both runners.
4. npm local package tests expanded with lifecycle subset (`upgrade` and
   clean-repo safety marker checks).
5. CI lifecycle subset expanded for npm/brew/choco jobs with bounded checks for
   upgrade and clean-repo safety.
6. Lifecycle QA matrix documented in runbook + README and mirrored to template
   copies for parity.
7. Sprint artifacts and traceability updated for `S0013`.

## QA verification checklist

1. Re-run PowerShell suite:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
2. Confirm added lifecycle checks PASS in `tests/report.md`:
   - clean-repo safety (installer)
   - CLI lifecycle (`missing`, backup, upgrade, clean)
   - invalid mode fail-fast
3. Re-run shell suite where `sh` is available:
   - `sh tests/run-tests.sh`
4. Validate npm local package lifecycle subset:
   - `powershell -ExecutionPolicy Bypass -File packaging/npm/test-npm-local.ps1`
   - or `sh packaging/npm/test-npm-local.sh`
5. Validate CI lifecycle subset in `.github/workflows/ci.yml`:
   - `npm-test`, `brew-test`, `choco-test` now include upgrade + clean-repo checks.
6. Verify lifecycle QA matrix docs:
   - `docs/engineering/runbook.md`
   - `README.md`
   - template parity in `template/docs/engineering/runbook.md` and `template/README.md`.

## Artifacts updated for QA

- `tests/run-tests.ps1`
- `tests/run-tests.sh`
- `packaging/npm/test-npm-local.ps1`
- `packaging/npm/test-npm-local.sh`
- `.github/workflows/ci.yml`
- `docs/engineering/runbook.md`
- `README.md`
- `template/docs/engineering/runbook.md`
- `template/README.md`
- `sprints/S0013/tasks.md`
- `sprints/S0013/progress.md`
- `sprints/S0013/summary.md`
- `sprints/S0013/uat.md`
- `sprints/S0013/uat.json`
- `sprints/S0013/plan-verify.json`
- `docs/engineering/state.md`
- `handoffs/tl_to_dev.md`
- `handoffs/po_to_tl.md`
- `handoffs/resume_brief.md`

---

# Dev -> QA Handoff — Sprint S0012 (US-0040)

## Status

S0012 implementation is complete for `US-0040` and ready for `/qa`.

## Scope completed

1. Canonical sprint-scoped release notes contract delivered:
   - `handoffs/releases/Sxxxx-release-notes.md`
   - target-sprint-only write semantics (no cross-sprint overwrite)
2. Canonical release queue tracker delivered:
   - `handoffs/release_queue.md`
   - required fields and deterministic status model
3. Deterministic transition semantics documented:
   - `ready -> unreleased -> released`
   - only target sprint queue row may mutate per `/release` run
4. Fail-safe unresolved sprint policy implemented with deterministic reason codes:
   - `RELEASE_SPRINT_UNRESOLVED`
   - `LEGACY_NOTES_SPRINT_UNRESOLVED`
   - `QUEUE_ENTRY_MISSING`
   - `NOTES_REF_MISSING`
   - `STATUS_TRANSITION_INVALID`
5. Legacy migration/backfill contract documented as non-destructive and idempotent.
6. Legacy `handoffs/release_notes.md` behavior updated to backward-compatible
   latest-pointer/summary with unreleased queue visibility.
7. Ownership/touchpoints aligned across `/release`, `core.mdc`, and
   `handoffs.mdc` guidance.
8. Active/template parity completed for all US-0040 touched command/rule/doc and
   handoff artifacts.
9. Regression matrix and automated checks delivered:
   - `sprints/S0012/uat.md`, `sprints/S0012/uat.json`,
     `sprints/S0012/plan-verify.json`
   - `tests/run-tests.ps1`, `tests/run-tests.sh`

## QA verification checklist

1. Re-run tests:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
2. Confirm test evidence:
   - `tests/report.md` shows `Pass: 142`, `Fail: 0`
   - timestamp `2026-02-25T23:11:21Z`
3. Verify canonical release artifacts exist in active and template:
   - `handoffs/release_queue.md`
   - `handoffs/releases/Sxxxx-release-notes.md`
4. Verify release command enforces:
   - target-sprint-only mutation
   - unresolved sprint fail-safe
   - queue/notes mismatch reason-code handling
   - non-destructive migration/backfill contract
5. Verify backward compatibility:
   - `handoffs/release_notes.md` operates as latest-pointer/summary
   - unreleased queue visibility guidance present
6. Verify runbook and README include US-0040 queue/history model semantics.
7. Verify active/template parity for all touched release command/rule/doc
   artifacts.
8. Confirm process-level scope only:
   - no deployment runtime rewrite claims.

## Artifacts updated for QA

- `.cursor/commands/release.md`
- `.cursor/rules/core.mdc`
- `.cursor/rules/handoffs.mdc`
- `docs/engineering/runbook.md`
- `README.md`
- `handoffs/release_notes.md`
- `handoffs/release_queue.md`
- `handoffs/releases/Sxxxx-release-notes.md`
- `sprints/S0012/tasks.md`
- `sprints/S0012/progress.md`
- `sprints/S0012/summary.md`
- `sprints/S0012/uat.md`
- `sprints/S0012/uat.json`
- `sprints/S0012/plan-verify.json`
- `docs/engineering/state.md`
- `tests/run-tests.ps1`
- `tests/run-tests.sh`
- Template parity copies under `template/` for touched command/rule/doc/handoff
  artifacts.

---

# Dev -> QA Handoff — Sprint S0010 (US-0038)

## Status

S0010 implementation is complete for `US-0038` and ready for `/qa`.

## Scope completed

1. Canonical sync policy modes and defaults are documented and aligned:
   - `disabled|manual|by_phase|by_milestone|custom_phase_list`
   - default-safe posture: `SYNC_POLICY_MODE=manual`, `ALLOW_AUTO_PUSH=0`
2. Sync eligibility is explicitly phase-boundary-only (no intra-phase evaluation).
3. Mandatory pre-push gate semantics are implemented in both validate scripts:
   - `TEST_COMMAND` is required
   - missing/failing/timed-out test blocks push deterministically
4. Optional checks (`LINT_COMMAND`, `TYPECHECK_COMMAND`) are evaluated only when
   configured and reported as `pass|fail|skipped`.
5. QA-first guardrails are documented:
   - feature auto-push forbidden before QA completion
   - blocker-aware no-push on unresolved blocking QA findings/critical issues
6. Branch safety deny-by-default + allowlist model is documented:
   - protected/default branch denied unless explicitly allowlisted
7. Deterministic sync reason codes/evidence schema is added across command/runbook/state guidance.
8. Active/template parity is completed for all touched command/docs/config files.
9. Regression matrix for positive and negative paths is added in S0010 UAT artifacts.

## QA verification checklist

1. Re-run tests:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
2. Confirm US-0038 contract checks are present in `tests/report.md`:
   - sync policy flags in active and template scratchpad
   - guarded eligibility contract in active and template `/auto`
   - sync reason code references in active and template runbook
   - validate scripts require `TEST_COMMAND`
   - validate scripts include optional `TYPECHECK_COMMAND` handling
3. Verify pre-push gate semantics from scripts:
   - missing `TEST_COMMAND` fails with reason code
   - failing/timed-out tests block push
4. Verify optional-check semantics:
   - `LINT_COMMAND` / `TYPECHECK_COMMAND` skipped when unset
   - configured failures block eligibility
5. Verify QA-first and blocker-aware restrictions are present in `/qa` and `/release`.
6. Verify branch safety deny-by-default + allowlist contract is present in docs.
7. Verify deterministic sync evidence fields and reason codes are consistently documented.
8. Verify no runtime orchestrator claims were introduced (process guidance only).

## Artifacts updated for QA

- `.cursor/commands/auto.md`
- `.cursor/commands/execute.md`
- `.cursor/commands/qa.md`
- `.cursor/commands/release.md`
- `.cursor/scratchpad.md`
- `docs/engineering/runbook.md`
- `README.md`
- `scripts/validate-and-push.ps1`
- `scripts/validate-and-push.sh`
- `tests/run-tests.ps1`
- `tests/run-tests.sh`
- `sprints/S0010/tasks.md`
- `sprints/S0010/progress.md`
- `sprints/S0010/summary.md`
- `sprints/S0010/uat.md`
- `sprints/S0010/uat.json`
- `sprints/S0010/plan-verify.json`
- `docs/engineering/state.md`
- template parity copies under `template/` for touched command/docs/config files.

---

# Dev -> QA Handoff — Sprint S0009 (US-0037)

## Status

S0009 implementation is complete for `US-0037` and ready for `/qa`.

## Scope completed

1. Deterministic `/auto start-from=<phase>` contract delivered with canonical
   phase IDs.
2. Resolver precedence documented and aligned:
   - explicit argument
   - `handoffs/resume_brief.md`
   - conservative `docs/engineering/state.md` fallback
   - fail-fast on ambiguity/conflict/unrecoverable
3. Conflict/staleness/unparseable policy added with mandatory
   `[AUTO_RESUME_ERROR]` format and required error codes.
4. Existing stop conditions explicitly preserved in continuation mode:
   decision gate, missing critical input, pause request, loop max cycles.
5. Breadcrumb contract added for inspectability:
   start source, resolved phase, resolution status, stop reason, stop phase,
   timestamp in state/resume artifacts.
6. `/pause`, `/resume`, `/auto`, README, and runbook continuation semantics are
   aligned.
7. Active/template parity completed for all changed continuation-related
   command/rule/doc files.
8. Contract-level tests updated in:
   - `tests/run-tests.ps1`
   - `tests/run-tests.sh`

## QA verification checklist

1. Re-run tests:
   - `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`
   - Latest dev execution evidence: `tests/report.md` timestamp
     `2026-02-25T13:26:07Z` (`Pass=103`, `Fail=0`)
2. Confirm report contains US-0037 contract checks:
   - canonical `start-from` phase list present
   - precedence order (`argument > resume_brief > state > fail-fast`)
   - stale/unparseable/conflict fail-fast policy
   - `[AUTO_RESUME_ERROR]` format + required code list
   - breadcrumb fields in continuation guidance
3. Confirm `/pause`, `/resume`, and `/auto` guidance is semantically aligned.
4. Confirm stop-condition preservation is explicit and unchanged.
5. Confirm process-level scope only:
   - no runtime orchestrator rewrite or product runtime feature claims.
6. Confirm active/template parity for all US-0037 touched files.

## Artifacts updated for QA

- `sprints/S0009/tasks.md`
- `sprints/S0009/progress.md`
- `sprints/S0009/summary.md`
- `sprints/S0009/uat.md`
- `sprints/S0009/uat.json`
- `docs/engineering/state.md`
