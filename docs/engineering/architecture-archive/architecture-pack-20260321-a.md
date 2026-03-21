# Architecture archive pack (2026-03-21)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 30
- First archived heading: `# US-0028: Security & Compliance Review Agent`
- Last archived heading: `# US-0028: Security & Compliance Review Agent`
- Verification tuple (mandatory):
  - archived_body_lines=246
  - preamble_lines=10
  - retained_body_lines=3285

---

# US-0028: Security & Compliance Review Agent

## Overview

US-0028 adds an optional 7th agent role (security reviewer) and `/security-review`
command, activated via scratchpad flags. When enabled, the security agent
reviews at two workflow points: post-architecture (design review) and
post-execute (code review). When disabled (default), zero workflow overhead.

Findings go to `docs/engineering/security-review.md`. Critical findings create
decision records and block progression via the existing decision gate pattern.

Per DEC-0012, this is a dedicated agent role rather than augmented behavior on
existing agents.

## Assumption challenges

**Is a 7th agent the right granularity?** Yes (DEC-0012). Security expertise is
a distinct "hat" — mixing it with TL or QA dilutes both. The flag mechanism
ensures zero overhead when disabled. Follows established one-role-per-agent
pattern.

**How do compliance profiles work?** They're prompt-embedded checklists in the
agent definition, not external data sources. Each profile maps to a set of
review questions the agent evaluates. Consistent with the framework's philosophy:
AI-driven guidance, not automated scanning.

**Can this be simpler?** This is already minimal: one agent, one command (two
modes), two flags, one output file. No external tooling, no automated SAST, no
custom parsers.

## Design

### 1) Security agent definition (`security.mdc`)

```
You are the Security Reviewer. Evaluate architecture and code for security
risks and compliance alignment.
You start in a fresh agent context for this phase.

Inputs (design review mode):
- docs/engineering/architecture.md
- docs/engineering/decisions.md
- docs/engineering/state.md
- COMPLIANCE_PROFILES from .cursor/scratchpad.md

Inputs (code review mode):
- Current sprint tasks and implementation files
- docs/engineering/architecture.md
- COMPLIANCE_PROFILES from .cursor/scratchpad.md

Outputs:
- docs/engineering/security-review.md
- decisions/DEC-xxxx.md (for critical findings)

Rules:
- Review scope is guidance-based: architectural patterns, data flows, auth
  design, common vulnerability patterns. Not line-by-line static analysis.
- Use compliance profiles as review checklists when COMPLIANCE_PROFILES is set.
- When COMPLIANCE_PROFILES is empty, apply general security best practices.
- Critical findings (severity: critical) must create a DEC-xxxx record and
  flag a decision gate. Workflow pauses until resolved.
- Non-critical findings (severity: high/medium/low) are documented in
  security-review.md with remediation guidance.
- Use only artifact files as context, not prior chat history.
- After writing findings, stop. Next phase resumes in a new subagent/chat.
```

### 2) `/security-review` command with two modes

**Design review mode** (post-architecture):

```
Inputs: architecture.md, decisions.md, COMPLIANCE_PROFILES
Review scope:
- Architecture decisions for security implications
- Data flow and storage patterns
- Authentication and authorization design
- Third-party dependency risk
- Profile-specific requirements (when profiles set)
```

**Code review mode** (post-execute):

```
Inputs: sprint tasks, implementation files, architecture.md, COMPLIANCE_PROFILES
Review scope:
- Secrets/credentials in code or config
- Injection vulnerabilities (SQL, XSS, command)
- Authentication/authorization implementation gaps
- Input validation and output encoding
- Profile-specific implementation requirements
```

Command steps:

```
1. Read SECURITY_REVIEW and COMPLIANCE_PROFILES from scratchpad.md.
2. If SECURITY_REVIEW=0, exit with "Security review is disabled."
3. Determine mode: design review (if architecture just completed) or
   code review (if execute just completed). Mode can also be specified
   explicitly by the user.
4. Load review inputs for the selected mode.
5. If COMPLIANCE_PROFILES is set, load profile-specific checklists.
6. Evaluate against security criteria and profile requirements.
7. Write findings to docs/engineering/security-review.md with severity,
   affected components, and remediation guidance.
8. For critical findings: create DEC-xxxx record, flag decision gate.
9. Update docs/engineering/state.md with review status.
```

### 3) Workflow integration points

When `SECURITY_REVIEW=1`, `/auto` spawns the security agent at two points:

```
... -> architecture -> [security-review: design] -> sprint-plan -> ...
... -> execute -> [security-review: code] -> QA -> ...
```

Integration in `/auto` command steps (conditional):

```
- After architecture phase: if SECURITY_REVIEW=1, spawn security agent
  in design review mode before proceeding to sprint-plan.
- After execute phase: if SECURITY_REVIEW=1, spawn security agent in
  code review mode before proceeding to QA.
```

Integration in `/qa` command (reference):

```
- If SECURITY_REVIEW=1, check that security-review.md exists and has no
  unresolved critical findings before proceeding.
```

When `SECURITY_REVIEW=0` (default), these steps are skipped entirely.

### 4) Compliance profile mechanism

Profiles are prompt-embedded checklists. `COMPLIANCE_PROFILES` is a
comma-separated scratchpad value. When set, the security agent applies
profile-specific review criteria in addition to general security best practices.

| Profile | Key review areas |
|---------|-----------------|
| GDPR | Data minimization, consent flows, right to erasure, data processing agreements, cross-border data transfers |
| SOC2 | Access controls, audit logging, change management, availability monitoring, incident response |
| HIPAA | PHI handling, encryption at rest/transit, access controls, audit trails, business associate agreements |
| PCI-DSS | Cardholder data protection, network segmentation, encryption, access control, logging/monitoring |
| ISO27001 | Information security policy, risk assessment, access control, cryptography, operations security |

Profiles are NOT certifications. The security-review.md output explicitly
states that findings are AI-guided review, not compliance certification.
Human expert review is recommended for production compliance.

### 5) Scratchpad flags

New flags in `.cursor/scratchpad.md`:

```
# Security review
# - SECURITY_REVIEW: 0|1 (enable optional security review, default: off)
# - COMPLIANCE_PROFILES: comma-separated (e.g., GDPR,SOC2; empty = general)
SECURITY_REVIEW=0
COMPLIANCE_PROFILES=
```

Default is OFF — zero overhead for projects that don't need security review.

### 6) Critical findings → decision records

When the security agent identifies a critical finding:

1. Create a `decisions/DEC-xxxx.md` entry describing the vulnerability,
   affected components, risk assessment, and remediation options.
2. Set finding status to "blocking" in `security-review.md`.
3. The workflow pauses at a decision gate (consistent with existing escalation
   pattern) until the user resolves the finding.
4. Resolution options: fix the issue, accept the risk (with documented
   rationale), or defer with a mitigation plan.

This integrates with the existing decision gate pattern from `core.mdc` and
the escalation rules.

### 7) Security review output format

`docs/engineering/security-review.md` structure:

```markdown
# Security Review

## Review metadata
- Date: YYYY-MM-DD
- Mode: design|code
- Sprint: Sxxxx (code review only)
- Profiles: [list or "general"]

## Findings

### [severity: critical|high|medium|low] — [title]
- **Component**: [affected area]
- **Description**: [what was found]
- **Risk**: [impact if unaddressed]
- **Remediation**: [recommended fix]
- **Status**: [open|resolved|accepted|deferred]
- **Decision**: [DEC-xxxx reference, critical only]

## Summary
- Critical: N
- High: N
- Medium: N
- Low: N
- Overall: pass|fail (fail if any critical unresolved)
```

## File changes required

| File | Change |
|------|--------|
| `.cursor/agents/security.mdc` | New: security reviewer agent definition |
| `.cursor/commands/security-review.md` | New: command with design/code review modes |
| `.cursor/commands/auto.md` | Add conditional security review steps at two integration points |
| `.cursor/commands/qa.md` | Add reference to check security-review.md for unresolved criticals |
| `.cursor/scratchpad.md` | Add SECURITY_REVIEW=0 and COMPLIANCE_PROFILES= flags |
| `.cursor/rules/core.mdc` | Add security review to phase flow (conditional) |
| `docs/engineering/security-review.md` | New: placeholder for security review findings |
| `template/.cursor/agents/security.mdc` | Template copy |
| `template/.cursor/commands/security-review.md` | Template copy |
| `template/.cursor/commands/auto.md` | Template copy |
| `template/.cursor/commands/qa.md` | Template copy |
| `template/.cursor/scratchpad.md` | Template copy (add flags) |
| `template/docs/engineering/security-review.md` | Template copy (placeholder) |

## Risks

| Risk | Mitigation |
|------|------------|
| Security agent scope creep (tries to be SAST) | Agent definition constrains to architectural and pattern-level review. Not line-by-line static analysis. |
| False sense of security from compliance profiles | Output explicitly states findings are AI-guided review, not certification. Recommends human expert for production compliance. |
| Critical findings block workflow unnecessarily | User can "accept risk" to unblock, with documented rationale. Decision gate pattern already supports this. |
| Compliance profiles are shallow/generic | Profiles are guidance frameworks. They surface relevant questions, not definitive answers. Quality improves over time as prompts are refined. |
| Template/active file drift | All new files require template copies. Noted in file changes table for Dev. |

---

