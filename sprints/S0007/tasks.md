# Tasks — Sprint S0007

## US-0028: Security & Compliance Review Agent

### T-001: Create security agent definition (security.mdc)
- Story: US-0028
- Status: done
- Files: `.cursor/agents/security.mdc` (NEW)
- Description: Create the security reviewer agent definition per DEC-0012 and
  architecture section 1. Include persona ("You are the Security Reviewer"),
  inputs for both modes (design review: architecture.md, decisions.md, state.md,
  COMPLIANCE_PROFILES; code review: sprint tasks, implementation files,
  architecture.md, COMPLIANCE_PROFILES), outputs (security-review.md,
  decisions/DEC-xxxx.md for criticals), rules (guidance-based review, compliance
  profiles as checklists, critical findings create DEC-xxxx and trigger decision
  gates, non-critical findings documented with remediation, fresh context per
  phase, stop after writing findings). Include high-level review areas for all
  5 compliance profiles (GDPR, SOC2, HIPAA, PCI-DSS, ISO27001).
- AC covered: AC-1, AC-9
- Notes: Foundation task. All subsequent tasks depend on this agent existing.

### T-002: Create /security-review command with design and code review modes
- Story: US-0028
- Status: done
- Files: `.cursor/commands/security-review.md` (NEW)
- Description: Create the `/security-review` command per architecture section 2.
  Subagent: security. Execution model: run in fresh security subagent context.
  Inputs: scratchpad flags, architecture.md, decisions.md, sprint tasks.
  Outputs: security-review.md, DEC-xxxx (for criticals), state.md.
  Design review scope: architecture decisions, data flow/storage, auth design,
  third-party dependency risk, profile-specific requirements.
  Code review scope: secrets/credentials, injection vulnerabilities, auth/authz
  implementation, input validation, profile-specific implementation.
  Command steps: (1) read SECURITY_REVIEW and COMPLIANCE_PROFILES from
  scratchpad, (2) if SECURITY_REVIEW=0 exit with "disabled" message, (3)
  determine mode (design or code, can be specified explicitly), (4) load review
  inputs for selected mode, (5) if COMPLIANCE_PROFILES set load profile
  checklists, (6) evaluate against criteria, (7) write findings to
  security-review.md, (8) for critical findings create DEC-xxxx and flag
  decision gate, (9) update state.md.
- AC covered: AC-2, AC-5, AC-6
- Depends on: T-001

### T-003: Add SECURITY_REVIEW and COMPLIANCE_PROFILES scratchpad flags
- Story: US-0028
- Status: done
- Files: `.cursor/scratchpad.md`, `.cursor/scratchpad.local.example.md`
- Description: Add security review flags to both scratchpad files. Add a
  "Security review" comment section with: `SECURITY_REVIEW=0` (default OFF for
  zero overhead) and `COMPLIANCE_PROFILES=` (empty = general best practices
  only). Document that COMPLIANCE_PROFILES accepts comma-separated values
  (GDPR, SOC2, HIPAA, PCI-DSS, ISO27001). When SECURITY_REVIEW=0, all
  security review integration points are skipped entirely.
- AC covered: AC-3, AC-4

### T-004: Add concrete GDPR compliance profile checklist
- Story: US-0028
- Status: done
- Files: `.cursor/agents/security.mdc` (modify from T-001)
- Description: Expand the GDPR profile section in security.mdc with concrete,
  actionable checklist items for both design review and code review modes.
  Design review items: (1) data minimization — only necessary personal data
  collected, (2) consent flows — explicit opt-in with withdraw mechanism, (3)
  right to erasure — deletion path exists for all stored personal data, (4)
  data processing agreements — third-party processors identified with DPA
  requirements, (5) cross-border data transfers — transfer mechanisms identified
  (adequacy, SCCs, BCRs), (6) privacy by design — data protection considered
  in architecture, not bolted on.
  Code review items: (1) no personal data in logs, (2) consent checks before
  data processing, (3) data retention limits enforced, (4) encryption at rest
  and in transit for personal data, (5) access controls on personal data
  endpoints, (6) audit trail for data access/modification.
  Other profiles (SOC2, HIPAA, PCI-DSS, ISO27001) retain high-level review
  areas from T-001. GDPR is the reference implementation for detailed profiles.
- AC covered: AC-5
- Depends on: T-001

### T-005: Integrate security review into /auto and /qa workflow commands
- Story: US-0028
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/qa.md`
- Description: Add conditional security review integration per architecture
  section 3.
  In `/auto`: add two conditional steps — (a) after architecture phase, if
  `SECURITY_REVIEW=1`, spawn security agent in design review mode before
  proceeding to sprint-plan; (b) after execute phase, if `SECURITY_REVIEW=1`,
  spawn security agent in code review mode before proceeding to QA. When
  `SECURITY_REVIEW=0`, these steps are skipped entirely.
  In `/qa`: add a pre-check — if `SECURITY_REVIEW=1`, verify that
  `docs/engineering/security-review.md` exists and has no unresolved critical
  findings before proceeding with QA.
- AC covered: AC-8
- Depends on: T-001, T-002, T-003

### T-006: Create security-review.md report placeholder
- Story: US-0028
- Status: done
- Files: `docs/engineering/security-review.md` (NEW)
- Description: Create the security review report placeholder per architecture
  section 7. Structure: (1) header "Security Review", (2) "Review metadata"
  section with date, mode, sprint, profiles fields, (3) "Findings" section with
  finding format (severity, component, description, risk, remediation, status,
  decision reference), (4) "Summary" section with severity counts and overall
  pass/fail. Include a note that findings are AI-guided review, not compliance
  certification — human expert review is recommended for production compliance.
  File is a template/placeholder — populated by the security agent when
  `/security-review` runs.
- AC covered: AC-7

### T-007: Add critical findings → decision record escalation integration
- Story: US-0028
- Status: done
- Files: `.cursor/commands/security-review.md` (expand step 8)
- Description: Ensure the critical findings escalation flow is fully detailed
  in the `/security-review` command (step 8). Verify that escalation.mdc already
  covers security-originated decision gates (it does — "security" is listed as
  a trigger). Ensure step 8 explicitly describes: (1) create
  `decisions/DEC-xxxx.md` with vulnerability description, affected components,
  risk assessment, and remediation options, (2) set finding status to "blocking"
  in security-review.md, (3) workflow pauses at decision gate until user
  resolves, (4) resolution options: fix the issue, accept the risk with
  documented rationale, or defer with a mitigation plan. Verify DEC-xxxx
  template format is compatible with security finding records.
- AC covered: AC-9
- Depends on: T-002
- Notes: escalation.mdc already lists "security" as a decision gate trigger.
  This task ensures the security command's critical findings flow is complete
  and integrates with the existing decision gate pattern.

### T-008: Update core.mdc with conditional security review phase
- Story: US-0028
- Status: done
- Files: `.cursor/rules/core.mdc`
- Description: Add security review to the phase flow description in core.mdc as
  a conditional step. The phase flow becomes: intake -> discovery -> research ->
  architecture -> [security-review: design, if SECURITY_REVIEW=1] -> sprint plan
  -> plan verify -> execute -> [security-review: code, if SECURITY_REVIEW=1] ->
  QA -> verify work -> release -> refresh context. Add a note that when
  `SECURITY_REVIEW=0` (default), the security review steps are skipped and the
  flow is unchanged from the current behavior.
- AC covered: AC-8
- Depends on: T-001

### T-009: Template parity for all US-0028 changes
- Story: US-0028
- Status: done
- Files:
  - `template/.cursor/agents/security.mdc` (NEW — copy from T-001 + T-004)
  - `template/.cursor/commands/security-review.md` (NEW — copy from T-002 + T-007)
  - `template/.cursor/commands/auto.md` (copy from T-005)
  - `template/.cursor/commands/qa.md` (copy from T-005)
  - `template/.cursor/scratchpad.md` (copy from T-003)
  - `template/docs/engineering/security-review.md` (NEW — copy from T-006)
- Description: Copy all US-0028 active file changes to their template
  counterparts. Ensure every new file and every modification made in T-001
  through T-008 is reflected in the corresponding template/ file. Template
  security-review.md (report) is the same placeholder as the active copy.
  Template scratchpad.md gets the same SECURITY_REVIEW=0 and
  COMPLIANCE_PROFILES= flags. core.mdc template copy must also include the
  conditional phase flow update from T-008.
- AC covered: AC-10
- Depends on: T-001 through T-008
- Notes: Execute after all active file tasks are complete to ensure copies
  are accurate. 6 template files total (3 new + 3 modified).

### T-010: Update docs/engineering/state.md and verify cross-references
- Story: US-0028
- Status: done
- Files: `docs/engineering/state.md`, `docs/engineering/decisions.md`
- Description: Update engineering state with S0007 sprint progress and
  session status. Verify that DEC-0012 is listed in decisions.md. Confirm
  cross-references: security.mdc references DEC-0012, /security-review command
  references scratchpad flags, /auto and /qa reference security-review.md,
  core.mdc references the conditional phase flow. Ensure the traceability
  index row for US-0028 → S0007 is present (added during sprint planning).
- AC covered: (cross-cutting verification)
- Depends on: T-001 through T-009

## Implementation order and constraints

- Execute tasks in sequence: T-001 → T-010.
- T-001 is the foundation — creates the security agent that all other tasks
  reference. Include the full agent definition with critical findings behavior.
- T-004 extends T-001 by adding detailed GDPR checklist items to security.mdc.
- T-005 (workflow integration) requires T-001, T-002, and T-003 to be complete
  (agent exists, command exists, flags exist).
- T-007 refines T-002's step 8 with detailed escalation flow.
- T-009 (template parity) must execute after T-001 through T-008 to capture
  all active file changes.
- T-010 (docs/verification) is the final cleanup task.
- SECURITY_REVIEW default is 0 (OFF). All integration points must be conditional.
- Compliance profiles are prompt-embedded checklists, not external data files.
- Reference DEC-0012 for the security agent integration model decision.
