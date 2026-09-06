# Verify-Work Findings — S0132 / BUG-0016

**Phase**: verify-work  
**Role**: qa (fresh subagent)  
**Bug**: BUG-0016 (OpenCode Layer-1 role permissions vs kit duties)  
**Sprint**: S0132  
**Orchestrator run**: auto-20260906-bug0016  
**Verify-work timestamp**: 2026-09-06T19:25:00Z  
**Fresh context marker**: qa-BUG0016-verify-work-20260906T192500Z-fresh  
**Verdict**: VERIFY_WORK_PASS  

## Independent verify-work verification

Fresh QA subagent per US-0048 / BUG-0006. Context limited to artifacts/handoffs (narrow-read). Independent re-run of contract + compose + parity gates. UAT populated from AC-1..AC-8. No browser fake PASS. No DONE flip.

## Test battery (live)

| Gate | Command | Result |
|------|---------|--------|
| BUG-0016 contract | `python -m pytest tests/bug0016_contract_test.py -v` | **7 passed** in 0.03s |
| US-0122 compose | `python -m pytest tests/us0122_contract_test.py -q` | **8 passed** in 0.04s |
| Parity | `python scripts/check_intake_template_parity.py --scope=bug-0016` | `[INTAKE_TEMPLATE_PARITY_OK]` |
| Triad | `python scripts/enforce-triad-hot-surface.py --check` | exit 0 |
| Metadata | `python scripts/check-user-visible-metadata.py --repo . --json` | OK / 0 violations |

## AC verification (architecture `# BUG-0016`)

| AC | Description | Result |
|----|-------------|--------|
| AC-1 | po/tl/curator `bash: ask` | **PASS** (UAT-1; marker 1) |
| AC-2 | PO intake_evidence + resume_brief + state; `**` deny last | **PASS** (UAT-2; marker 2) |
| AC-3 | `sprints/S*/…` not `Sxxxx` | **PASS** (UAT-3; marker 3) |
| AC-4 | Release duty paths complete | **PASS** (UAT-4; marker 4) |
| AC-5 | Success test (c) preserved | **PASS** (UAT-5; marker 5) |
| AC-6 | security/auto unchanged | **PASS** (UAT-6; marker 6) |
| AC-7 | Active ↔ template parity | **PASS** (UAT-7; marker 7) |
| AC-8 | DEC-0122 §2 sole SOT | **PASS** (UAT-8; us0122 8/8) |

## UAT summary

- **Total**: 9 (UAT-1..UAT-8 + `convergence_smoke`)
- **Passed**: 9
- **Failed**: 0
- **uat_lifecycle**: populated (DEC-0009)
- **Probe class**: `contract_tests_primary`
- **Waived live probes**: 6 × `UAT_PROBE_FORBIDDEN` (no fake browser PASS)
- **convergence_smoke**: pass (`contract_test_failed=0`)

## Isolation compliance gate

| Phase | Marker | Result |
|-------|--------|--------|
| execute | `dev-BUG0016-execute-20260906T190500Z-fresh` | PASS |
| qa | `qa-BUG0016-qa-20260906T191500Z-fresh` | PASS |
| verify-work | `qa-BUG0016-verify-work-20260906T192500Z-fresh` | PASS (this phase) |

## Runtime proofs

| Phase | runtime_proof_id | proof_hash |
|-------|------------------|------------|
| execute | `rp-auto-20260906-bug0016-execute-dev-20260906T190500Z-BUG-0016` | `519A7617F1ADBEAFD95A940AF28B130F8EB309350F3F787C0AC02152FBEC76BF` |
| qa (consumed) | `rp-auto-20260906-bug0016-qa-qa-20260906T191500Z-BUG-0016` | `2258AE43B09997167501DD437B38DBA1A01356D1D09991707C1098EBC8D5523D` (MATCH; consumed 19:25 before ttl 20:15) |
| verify-work (issued) | `rp-auto-20260906-bug0016-verify-work-qa-20260906T192500Z-BUG-0016` | `C9DE18A187C251AEC3081E43EA65645CBA3B7C8341D0F10639567CF3224B5B41` |

## Status (US-0045)

- backlog Status: **OPEN** (not DONE)
- acceptance L181: **unchecked**
- BUG-0015: DONE preserved (not reopened)
- intake JSON: not mutated

## Blocking findings

None.

## Next

`/release` (fresh release subagent). STOP — do not spawn `/release` from this subagent.
