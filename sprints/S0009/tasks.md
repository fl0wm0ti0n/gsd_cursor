# Tasks — Sprint S0009

## US-0037: Mid-Process `/auto` Continuation with Deterministic Resume Point

### T-001: Define `/auto start-from=<phase>` contract and canonical phase IDs
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`
- Description: Add explicit `start-from=<phase>` input contract to `/auto` and
  define accepted canonical phase IDs for deterministic mid-process entry.
- AC covered: AC-1

### T-002: Define deterministic precedence resolver and precedence tests
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`, `sprints/S0009/uat.md`
- Description: Document strict precedence resolution contract:
  explicit argument > `handoffs/resume_brief.md` > `docs/engineering/state.md`
  fallback > fail-fast. Add UAT cases that verify precedence behavior.
- AC covered: AC-2
- Depends on: T-001

### T-003: Define conflict/staleness handling and `[AUTO_RESUME_ERROR]` codes
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`, `sprints/S0009/uat.md`
- Description: Add fail-fast policy for stale, conflicting, missing, and
  unparseable resume signals. Define `[AUTO_RESUME_ERROR]` message format and
  required error codes, and add UAT cases for conflict/staleness/error-code
  scenarios.
- AC covered: AC-3
- Depends on: T-002

### T-004: Preserve one-command continuation across remaining phases
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`
- Description: Specify that one `/auto` invocation from the resolved phase
  continues through all remaining phases in canonical order, including existing
  execute/QA loop behavior when enabled.
- AC covered: AC-4
- Depends on: T-003

### T-005: Preserve existing stop conditions and gate behavior
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/rules/core.mdc`
- Description: Explicitly retain existing stop conditions (decision gate, missing
  critical input, pause request, loop max cycles) so continuation cannot bypass
  existing controls.
- AC covered: AC-5
- Depends on: T-004

### T-006: Define continuation breadcrumbs in state and resume artifacts
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/pause.md`, `.cursor/commands/resume.md`, `docs/engineering/state.md`, `handoffs/resume_brief.md`
- Description: Add deterministic breadcrumb requirements (resolved phase, source,
  stop reason, timestamp) and where they must be recorded for inspectable
  continuation behavior.
- AC covered: AC-6
- Depends on: T-005

### T-007: Protect backward compatibility and safe defaults
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/resume.md`
- Description: Document compatibility guarantees that manual and interactive
  workflows remain unchanged unless continuation mode is explicitly used.
- AC covered: AC-7
- Depends on: T-006

### T-008: Align `/pause`, `/resume`, `/auto` guidance and user docs
- Story: US-0037
- Status: done
- Files: `.cursor/commands/auto.md`, `.cursor/commands/resume.md`, `.cursor/commands/pause.md`, `README.md`, `docs/engineering/runbook.md`
- Description: Align command guidance so resume semantics are consistent across
  all three commands. Update README/runbook to reflect user-facing continuation
  behavior and resolver expectations.
- AC covered: AC-8
- Depends on: T-007

### T-009: Complete active/template parity for continuation semantics
- Story: US-0037
- Status: done
- Files: `template/.cursor/commands/auto.md`, `template/.cursor/commands/resume.md`, `template/.cursor/commands/pause.md`, `template/README.md`, `template/docs/engineering/runbook.md`
- Description: Mirror all continuation-related command and documentation guidance
  to template copies and verify behavioral parity with active files.
- AC covered: AC-9
- Depends on: T-008

## Implementation Order and Constraints

- Execute in sequence T-001 -> T-009.
- Keep sprint atomic to US-0037 only; do not mix unrelated stories.
- Preserve existing stop conditions and gate controls in continuation mode.
- Fail fast on stale/conflicting/unparseable resume inputs; do not guess.
- Keep active/template parity as a first-class completion criterion.
