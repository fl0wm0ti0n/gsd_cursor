# Sprint S0007

## Goal

Deliver US-0028 (Security & Compliance Review Agent) by adding an optional 7th
agent role (`security.mdc`) and `/security-review` command with design and code
review modes. When disabled (default), zero workflow overhead. When enabled,
security review runs post-architecture and post-execute with configurable
compliance profiles.

## Scope

- **In scope**: US-0028 (AC-1..AC-10).
- **Out of scope**: Automated SAST/DAST tooling, compliance certification,
  external security scanning integrations.

## Sizing Check

- `SPRINT_MAX_TASKS=12`
- `SPRINT_AUTO_SPLIT=1`
- Planned tasks: 10
- 10 < 12 — within threshold. Single sprint, no split required.

## Prerequisites

- S0006 (US-0029 Knowledge Curation) QA complete (pass).
- DEC-0012 accepted (dedicated 7th agent role for security review).
- Architecture for US-0028 finalized in `docs/engineering/architecture.md`.

## Key decisions

- DEC-0012: Security review as dedicated 7th agent role (`security.mdc`), not
  augmented behavior on existing agents. Flag-controlled (`SECURITY_REVIEW`),
  zero overhead when disabled.

## Implementation order

Execute tasks T-001 through T-010 in sequence. T-001 (security agent definition)
is the foundation — all subsequent tasks depend on the agent being defined.
T-004 (GDPR checklist) extends T-001 with concrete profile items. T-005 (workflow
integration) depends on T-001, T-002, and T-003. T-009 (template parity) must
wait until all active file changes (T-001 through T-008) are complete.

## Risks

| Risk | Mitigation |
|------|------------|
| Security agent scope creep (tries to be SAST) | Agent definition constrains to architectural and pattern-level review. Not line-by-line static analysis. |
| False sense of security from compliance profiles | Output explicitly states findings are AI-guided review, not certification. Recommends human expert for production compliance. |
| Critical findings block workflow unnecessarily | User can "accept risk" to unblock, with documented rationale. Decision gate pattern already supports this. |
| Template parity across 6 template files | Single template parity task (T-009) after all active changes complete. |
| Zero-overhead guarantee when disabled | Default SECURITY_REVIEW=0. All integration points are conditional on this flag. |

## Definition of Done

- Security agent definition exists with persona, inputs, outputs, rules, and
  compliance profile framework (AC-1).
- `/security-review` command with design and code review modes (AC-2).
- Scratchpad flags control activation; disabled by default (AC-3, AC-4).
- Design review analyzes architecture against selected profiles (AC-5).
- Code review analyzes implementation for common vulnerabilities (AC-6).
- Findings written to security-review.md with severity and remediation (AC-7).
- Workflow rules invoke security review when enabled (AC-8).
- Critical findings create decision records and block progression (AC-9).
- Template copies for all new and modified files (AC-10).
