# State archive pack (2026-04-12)

- Rollover trigger: `STATE_HOT_MAX_LINES=1200, STATE_HOT_MAX_CHECKPOINTS=80`
- Source: `docs/engineering/state.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 18
- First archived heading: `## Execute checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 — **`RELEASE_TEST_FAILED` remediation**`
- Last archived heading: `## Execute checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 — **`RELEASE_TEST_FAILED` remediation**`
- Verification tuple (mandatory):
  - archived_body_lines=22
  - preamble_lines=11
  - retained_body_lines=1187

---

## Execute checkpoint (2026-04-04) — S0070 / BUG-0008 / auto-20260404-03 — **`RELEASE_TEST_FAILED` remediation**

- **`/execute`** (**dev**) — consolidated harness green: **`tests/report.md`** **794** pass / **0** fail (timestamp **2026-04-04T20:25:29Z**); **`powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1`** **exit 0**. Remediation scope: **Homebrew** formula **url/version** ↔ **`package.json`** **`0.1.2-41`**; **scratchpad** baseline/example catalog header parity (**`# Remote execution (US-0084 / US-0064)`**); **`template/docs/engineering/auto-orchestration-reference.md`** synced (**token-cost parity**); runbook **US-0078** harness substring anchor (active+template); **`installer.sh`** **`write_installed_version`** **`return 0`** (**`set -e`** after optional legacy **`rm`**); **`tests/installer_shell_bug0004_test.py`** fixture + **`tests/run-tests.ps1`** atomic report write. **`BUG-0008`** remains **OPEN** (**US-0045**); **`docs/product/acceptance.md`** unchanged (publish/E2E still pending).

Isolation evidence (**US-0048** / **DEC-0029**):

- `phase_id=execute`
- `role=dev`
- `fresh_context_marker=dev-S0070-BUG0008-execute-tests-20260404T202529Z-fresh`
- `timestamp=2026-04-04T20:25:29Z`
- `evidence_ref=tests/report.md,tests/run-tests.ps1,tests/installer_shell_bug0004_test.py,installer.sh,packaging/homebrew/its-magic.rb,.cursor/scratchpad.local.example.md,template/.cursor/scratchpad.local.example.md,template/docs/engineering/auto-orchestration-reference.md,docs/engineering/runbook.md,template/docs/engineering/runbook.md,docs/product/backlog.md,handoffs/dev_to_qa.md`

Strict runtime proof (**US-0056** / **DEC-0038**): canonical tuple hashed as **SHA-256** of **sorted-key JSON** over (`orchestrator_run_id`, `runtime_proof_id`, `phase_id`, `role`, `proof_issued_at`, `proof_ttl_seconds`).

- `orchestrator_run_id=auto-20260404-03`
- `runtime_proof_id=rp-auto-20260404-03-execute-dev-20260404T202529Z-S0070-BUG0008-remediation`
- `phase_id=execute`
- `role=dev`
- `proof_issued_at=2026-04-04T20:25:29Z`
- `proof_ttl_seconds=3600`
- `proof_hash=9dccdb524b7ced00c8bd41075e7772eae5f85ae7937b889af3ad30f0f67e72d1`

