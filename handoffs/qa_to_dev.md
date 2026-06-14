## QA → Dev Handoff — **S0089** / **US-0099** — post-**`/qa`** → **`/execute`**

> **2026-06-14T20:00:00Z** — `/qa` complete (fresh **qa** subagent, `orchestrator_run_id=auto-20260614-01`, `fresh_context_marker=qa-S0089-US0099-qa-20260614T200000Z-fresh`). Story **US-0099** remains **OPEN** (US-0045). Sprint **S0089**. QA verdict: **FAIL** (one blocking metadata finding). Return to **`/execute`** for remediation.

### QA summary

- **Overall verdict**: **FAIL** — AC-1..AC-8 functional coverage **PASS**; **blocking** metadata guard failure blocks verify-work.
- **Contract tests**: `pytest -k us0099` → **7 passed** (10 subtests); all seven `test_us0099_*` subtests green.
- **Validators**: `dev_environment_lib.py --self-test` → `[DEV_ENVIRONMENT_SELF_TEST_OK]`; parity `--scope=dev-environment` → `[INTAKE_TEMPLATE_PARITY_OK]`.
- **Metadata guard**: `python scripts/check-user-visible-metadata.py` → **FAIL** exit 1.

### Blocking finding (must fix)

| ID | Reason code | Location | Fix |
|----|-------------|----------|-----|
| B-001 | `USER_VISIBLE_INTERNAL_METADATA_DETECTED` | `installer.py:378:65` — docstring contains `US-0099` | Remove planning id from docstring string literal; use neutral prose (e.g. "Non-destructive dev-environment profile bootstrap."). Re-run metadata checker → exit 0. |

### AC verification matrix (functional — all PASS)

| AC | Verdict | Task | Evidence pointer |
|----|---------|------|------------------|
| AC-1 Copy-when-missing | PASS | T-001, T-002, T-005 | `test_us0099_copy_when_missing`, `test_us0099_installer_hook_literals` |
| AC-2 Never overwrite | PASS | T-002, T-006 | `test_us0099_skip_when_exists`, `test_us0099_upgrade_idempotent` |
| AC-3 Path resolution | PASS | T-001, T-006 | `test_us0099_path_override` |
| AC-4 npm postinstall | PASS | T-003 | `test_us0099_postinstall_parity` |
| AC-5 Example source | PASS | T-001 | architecture § Contrast table; no install_paths row |
| AC-6 Runbook UX | PASS | T-004 | runbook § install-time bootstrap |
| AC-7 Contract + parity | PASS | T-005..T-009 | seven `test_us0099_*`; harness §26X |
| AC-8 Architecture | PASS | *(architecture phase)* | DEC-0084 amended; `# US-0099` |

### Artifacts authored this phase

- **`sprints/S0089/qa-findings.md`** — full per-AC verdicts, blocking finding, isolation + runtime proof.
- **`sprints/S0089/uat.json`** / **`uat.md`** — QA-populated UAT steps (8/8 AC PASS at functional level).
- **`docs/engineering/state.md`** — QA checkpoint appended.
- **`handoffs/qa_to_dev.md`** — this handoff.
- **`handoffs/qa_to_verify_work.md`** — blocked pending B-001 remediation.

### Runtime proof (US-0056 / DEC-0038)

- `orchestrator_run_id=auto-20260614-01`
- `runtime_proof_id=rp-auto-20260614-01-qa-qa-20260614T200000Z-S0089-US0099`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-06-14T20:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=36456d96213ec820015c833325652387715ef99244433a1f83cf7438d400d2c2`
- `fresh_context_marker=qa-S0089-US0099-qa-20260614T200000Z-fresh`

### Dev remediation focus

1. Fix `installer.py:378` docstring — remove `US-0099` from scanned string channel.
2. Re-run post-edit gates: `pytest -k us0099`, `dev_environment_lib.py --self-test`, `check_intake_template_parity.py --scope=dev-environment`, **`check-user-visible-metadata.py`** (must exit 0).
3. Hand back to **`/qa`** (fresh **qa**) after fix.

### Next

- **`/execute`** (fresh **dev**) for **`S0089`** / **`US-0099`** — metadata remediation only.
