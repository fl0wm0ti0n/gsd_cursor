# UAT — Sprint S0007

## Target

- **US-0028**: Security & Compliance Review Agent
  - AC-1: New agent definition security.mdc with inputs, outputs, persona, artifact responsibilities
  - AC-2: New /security-review command with design review and code review steps
  - AC-3: Scratchpad flags SECURITY_REVIEW (on/off) and COMPLIANCE_PROFILES (comma-separated) control activation
  - AC-4: When SECURITY_REVIEW is disabled (default), zero workflow overhead
  - AC-5: Design review analyzes architecture decisions, data flows, auth patterns against selected profiles
  - AC-6: Code review analyzes implementation for secrets, injection, auth/authz gaps, profile-specific requirements
  - AC-7: Findings to docs/engineering/security-review.md with severity, affected components, remediation
  - AC-8: Workflow rules invoke security review at correct points when enabled
  - AC-9: Critical findings create decision records and block progression until resolved
  - AC-10: Template copies include security agent, command, and placeholder security-review.md

## Steps

1. **AC-1**: Confirm `.cursor/agents/security.mdc` exists and includes persona, mode inputs, outputs, and artifact ownership.
   - Result: **PASS**
2. **AC-2**: Confirm `.cursor/commands/security-review.md` defines both design-review and code-review workflows.
   - Result: **PASS**
3. **AC-3**: Confirm `SECURITY_REVIEW` and `COMPLIANCE_PROFILES` flags are present and documented as activation controls.
   - Result: **PASS**
4. **AC-4**: Confirm disabled default behavior (`SECURITY_REVIEW=0`) skips security workflow insertion points.
   - Result: **PASS**
5. **AC-5**: Confirm design review scope covers architecture/data-flow/auth checks against selected compliance profiles.
   - Result: **PASS**
6. **AC-6**: Confirm code review scope covers secrets, injection, auth/authz, and profile-specific implementation checks.
   - Result: **PASS**
7. **AC-7**: Confirm findings are captured in `docs/engineering/security-review.md` with severity, component, and remediation.
   - Result: **PASS**
8. **AC-8**: Confirm workflow integration triggers security review at post-architecture and post-execute checkpoints when enabled.
   - Result: **PASS**
9. **AC-9**: Confirm critical findings escalation creates `decisions/DEC-xxxx.md` and blocks progression until resolution.
   - Result: **PASS**
10. **AC-10**: Confirm template parity includes security agent/command and placeholder security review artifact updates.
    - Result: **PASS**

## Results

- Story: **US-0028**
- UAT Steps Executed: **10**
- Passed: **10**
- Failed: **0**
- Overall UAT Result: **PASS**

## AC Traceability Summary

- AC-1..AC-10 each have at least one direct UAT step and all are **PASS**.
- Evidence basis: `sprints/S0007/qa-findings.md` (overall QA PASS, AC re-validation 10/10), `sprints/S0007/summary.md` (implemented task coverage and green test report).
