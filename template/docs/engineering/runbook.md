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

## Notes
- Leave a command blank to skip that step.
- Use explicit commands, not placeholders.
- `LINT_FIX_COMMAND` / `FORMAT_COMMAND` are used by CI auto-fix when checks fail
  (e.g. `npx eslint --fix .` or `npx prettier --write .`).
- `CI_AUTO_FIX`: set to `true` to enable the automatic fix-and-retry loop in
  GitHub Actions. When `false` (default), CI reports failures but does not
  attempt auto-fix commits.

## Project run steps (fill in per project)

### Prerequisites

- ...

### Local run

```bash
...
```

### Tests

```bash
...
```

