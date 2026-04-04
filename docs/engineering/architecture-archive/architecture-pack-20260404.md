# Architecture archive pack (2026-04-04)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 34
- First archived heading: `# US-0039: Release Gate Tightening for Check-In Tests and QA/UAT Completion`
- Last archived heading: `# US-0039: Release Gate Tightening for Check-In Tests and QA/UAT Completion`
- Verification tuple (mandatory):
  - archived_body_lines=159
  - preamble_lines=10
  - retained_body_lines=3404

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

