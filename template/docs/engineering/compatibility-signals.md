# Compatibility Signals

Structured contract-change signals for optional cross-repo observability mode.

## CS-0001

- Date: 2026-03-01
- Story: US-0034
- Producer: repo=example-producer, component=api-gateway
- Contract: contract_id=public-api, ref=contracts/public-api.yaml
- From version: 1.0.0
- To version: 1.0.1
- Change type: additive
- Impacted consumers:
  - repo=example-consumer, component=web-app, expected_range=^1.0.0
- Severity: info
- Required actions:
  - confirm consumer compatibility tests
  - keep documentation and contract references aligned
- Status: validated
