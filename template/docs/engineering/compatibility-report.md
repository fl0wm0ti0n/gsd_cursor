# Compatibility Report

- Mode: optional (`CROSS_REPO_OBSERVABILITY`)
- Scope: workflow-level compatibility visibility and risk reporting
- Status: advisory unless critical-gate policy is enabled

## Findings

| Finding ID | Story | Producer | Consumer | Severity | Evidence | Recommended action | Gate recommendation |
|---|---|---|---|---|---|---|---|
| CR-0001 | US-0034 | repo=example-producer/module=api-gateway | repo=example-consumer/module=web-app | info | `docs/engineering/compatibility-signals.md` | keep contract versions aligned; rerun compatibility checks on contract changes | none |

## Summary

- Critical: 0
- High: 0
- Medium: 0
- Low: 0
- Info: 1
- Overall: PASS
