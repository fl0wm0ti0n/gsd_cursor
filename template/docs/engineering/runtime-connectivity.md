# Runtime Connectivity

Canonical operator-facing connectivity summary for release and QA/runtime debug
contexts.

## Purpose

- Show where current targets are hosted (local vs remote).
- Provide connection instructions (domain/ip/port/protocol).
- Provide ingress/proxy metadata (for example Traefik) when configured.
- Preserve secret safety: never store secret values, only env-reference names.

## Source of truth

- `docs/engineering/release-targets.json`

## Operator summary template

For each enabled target include:

- `target_id`
- `target_type`
- `execution_mode` (`local|remote`)
- `connect_endpoint` (`protocol://domain:port` or `ip:port`)
- `ingress` (`traefik enabled/disabled`, router, entrypoint, tls)
- `docker_over_ssh` (enabled + context hints when configured)
- `release_context` (latest sprint/release note ref)
- `qa_context` (latest remote/local verification path)

## Security rules

- Do not write inline credentials/tokens/private keys.
- Only env reference names are permitted in connectivity artifacts.
- Redact auth details in handoffs and release outputs.
