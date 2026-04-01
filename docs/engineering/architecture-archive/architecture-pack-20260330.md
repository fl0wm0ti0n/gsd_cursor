# Architecture archive pack (2026-03-30)

- Rollover trigger: `ARCH_HOT_MAX_LINES=3500, ARCH_HOT_MAX_STORY_SECTIONS=120`
- Source: `docs/engineering/architecture.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 33
- First archived heading: `# US-0036: Official Remote Config Template, Docs, and Fail-Fast Validation`
- Last archived heading: `# US-0036: Official Remote Config Template, Docs, and Fail-Fast Validation`
- Verification tuple (mandatory):
  - archived_body_lines=138
  - preamble_lines=10
  - retained_body_lines=3364

---

# US-0036: Official Remote Config Template, Docs, and Fail-Fast Validation

## Overview

US-0036 defines a canonical remote execution configuration contract and
validation behavior for optional remote workflows. The architecture is
process-level only: it specifies artifact contract, checks, error reporting,
and documentation expectations. It does not introduce a runtime transport
implementation.

Primary goals:
- Safe default-off behavior (`REMOTE_EXECUTION=0`) with zero required overhead.
- Deterministic fail-fast validation when remote mode is enabled.
- Clear, actionable error messages and security guardrails.

## Minimal architecture

### 1) Canonical contract artifact and parity

Canonical file path:
- Active repo: `.cursor/remote.json`
- Template copy: `template/.cursor/remote.json`

Parity rule:
- Both files represent the same contract shape and semantics.
- Placeholder values remain non-secret examples only.
- Any contract field changes must update active + template docs and references
  in the same change set.

### 2) Contract model (schema-level)

`remote.json` is a strict JSON object with explicit required and optional
fields. Suggested minimal shape:

```json
{
  "version": 1,
  "defaultTarget": "local-docker",
  "targets": [
    {
      "id": "local-docker",
      "type": "docker",
      "enabled": true,
      "host": "127.0.0.1",
      "port": 2375,
      "workspaceRoot": "/workspace",
      "auth": {
        "mode": "env",
        "tokenEnv": "REMOTE_DOCKER_TOKEN"
      }
    }
  ]
}
```

Validation contract:
- Required root fields: `version`, `defaultTarget`, `targets`.
- Required target fields: `id`, `type`, `enabled`, `host`, `port`,
  `workspaceRoot`.
- `type` allowed values: `docker`, `ssh`, `vm`.
- `auth.mode` allowed values: `none`, `env`.
- If `auth.mode=env`, environment variable references are required (for example
  `tokenEnv`) and inline secrets are forbidden.
- `defaultTarget` must match an existing enabled target id.

### 3) Validation model (mode-aware)

Validation trigger:
- Run remote config validation only when `REMOTE_EXECUTION=1`.
- Skip all remote config checks when `REMOTE_EXECUTION=0`.

Failure policy:
- Enabled mode (`REMOTE_EXECUTION=1`): fail fast on first blocking issue and
  stop the phase with remediation guidance.
- Disabled mode (`REMOTE_EXECUTION=0`): no blocking behavior and no extra
  required steps.

Validation classes:
1. Presence: configured path exists.
2. Syntax: valid JSON parse.
3. Contract: required fields/types/enums.
4. Semantics: cross-field checks (default target exists/enabled, unique ids).
5. Security: deny secret-like inline values in config.

### 4) Error reporting model

All validation failures must be actionable and include:
- failing location (`path`, for example `targets[0].port`)
- expected rule (`integer 1..65535`)
- actual value/type
- remediation hint

Message pattern:
`[REMOTE_CONFIG_ERROR] <path>: expected <rule>, got <actual>. Fix: <hint>.`

Examples:
- `[REMOTE_CONFIG_ERROR] .cursor/remote.json: file not found. Fix: create from template/.cursor/remote.json or set REMOTE_EXECUTION=0.`
- `[REMOTE_CONFIG_ERROR] targets[1].type: expected one of [docker, ssh, vm], got "k8s". Fix: use a supported type or extend contract in a new decision record.`
- `[REMOTE_CONFIG_ERROR] targets[0].auth.token: inline secret-like value detected. Fix: use auth.mode=env and reference tokenEnv.`

### 5) Security model

Security posture:
- Never commit tokens, passwords, private keys, or API secrets in
  `.cursor/remote.json`.
- Only commit environment-variable references (for example `tokenEnv`,
  `passwordEnv`, `privateKeyPathEnv`) or safe placeholders.
- Treat any secret-like literal in config as validation failure when remote is
  enabled.

Scope boundary:
- In scope: configuration contract and safety guidance.
- Out of scope: external secret manager integration or transport protocol work.

### 6) Docs integration model

Documentation updates required by design:
- `README.md`: user-facing remote setup, two target examples, and mode behavior
  (`REMOTE_EXECUTION` off/on).
- `docs/engineering/runbook.md`: operator-oriented validation contract,
  fail-fast expectations, and troubleshooting messages.

Doc parity expectation:
- README and runbook must describe the same contract and failure behavior with
  no contradictions.

## Sprint-plan readiness (decomposition-ready)

Implementation tasks should split cleanly into:
1. Create canonical active/template `remote.json` artifacts with safe examples.
2. Document contract schema and allowed values.
3. Implement/define validation checks and error message contract.
4. Add security guidance and secret-prohibition checks.
5. Update README and runbook with remote setup + mode-specific expectations.
6. Verify parity across active/template files and docs references.

---

