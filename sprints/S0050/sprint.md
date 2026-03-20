# Sprint S0050

- Story: `US-0071`
- Goal: enforce a channel-aware guard so internal planning tokens (`US-xxxx`, `DEC-xxxx`, `R-xxxx`) never appear in user-visible software outputs (CLI/UI/errors/installer-visible text), while remaining allowed on internal surfaces and in source comments only — per `DEC-0053`, architecture US-0071, and backlog AC-1..AC-10.
- Status: execute complete (handed to `/qa`)

## Scope

- Deterministic forbidden-pattern policy and explicit internal allowlist (`docs/**`, `.cursor/**`, sprint/handoff/decision trees, comments-not-strings).
- Mandatory `/execute` default guard for in-scope changes; `/qa` automated scan with fail-closed reason codes; release/readiness attestation that checks ran (not policy-only).
- Shared reason-code vocabulary (`USER_VISIBLE_INTERNAL_METADATA_DETECTED`, `METADATA_SANITIZATION_POLICY_MISSING`, `METADATA_SANITIZATION_SCOPE_AMBIGUOUS`).
- Finding schema: path/context refs, token class, safe replacement guidance.
- Active/template parity (commands, rules, runbook, README) and regression matrix (positive, negative, allowlist, idempotent reruns).
