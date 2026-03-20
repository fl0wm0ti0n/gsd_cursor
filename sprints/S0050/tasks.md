# Sprint S0050 Tasks

- Story: `US-0071`
- Sprint: `S0050`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Encode deterministic forbidden-token policy for user-visible software surfaces (minimum matchers `US-[0-9]{4}`, `DEC-[0-9]{4}`, `R-[0-9]{4}`) with channel scope aligned to discovery refinements (CLI/UI/errors/installer-visible text) | AC-1 |
| T-002 | done | Document deterministic internal-only allowlist where planning tokens remain permitted (`docs/**`, `.cursor/**`, `sprints/**`, `handoffs/**`, `decisions/**`, template analogs, and **source comments only** — not user-facing string literals) | AC-2 |
| T-003 | done | Add `/execute` default, non-bypass guard so in-scope changes do not introduce forbidden tokens into user-visible output targets | AC-3 |
| T-004 | done | Add `/qa` automated verification for the sanitization policy; fail closed on leakage with deterministic reason codes | AC-4 |
| T-005 | done | Define findings/remediation contract: exact evidence refs (file/path context), detected token class, and safe replacement guidance | AC-5 |
| T-006 | done | Document deterministic reason-code vocabulary (minimum: `USER_VISIBLE_INTERNAL_METADATA_DETECTED`, `METADATA_SANITIZATION_POLICY_MISSING`, `METADATA_SANITIZATION_SCOPE_AMBIGUOUS`) across execute/QA/release surfaces | AC-6 |
| T-007 | done | Validate allowlist behavior: legitimate internal references in docs/comments remain allowed; guard does not false-block allowlisted surfaces | AC-7 |
| T-008 | done | Maintain active/template parity for command guidance, rules, runbook, and README for all new policy keys and failure taxonomy | AC-8 |
| T-009 | done | Add regression coverage: positive (no leak), negative (leak blocked), allowlist passes, and rerun idempotence | AC-9 |
| T-010 | done | Ensure release/readiness artifacts include auditable evidence that user-visible metadata sanitization checks executed and passed | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
- AC-8 -> T-008
- AC-9 -> T-009
- AC-10 -> T-010
