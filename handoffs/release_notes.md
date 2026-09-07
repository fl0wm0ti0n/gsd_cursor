# Release Notes (Legacy Compatibility Pointer)

This file remains backward-compatible for workflows that read
`handoffs/release_notes.md` as the latest release summary.

Canonical sprint history now lives under:
- `handoffs/releases/Sxxxx-release-notes.md`

Canonical queue state now lives under:
- `handoffs/release_queue.md`

---

---

## Release finalized note (S0133)

- Sprint: `S0133`
- Story: `US-0131` (Cross-host Its-Magic runtime configuration and parity — host-neutral `.its-magic/config*`; Cursor adapter; OpenCode-only without `.cursor/`; 10 contract markers)
- Release: **finalized** (`2026-09-07T21:15:18Z`, `orchestrator_run_id=auto-20260907-us0131`, `fresh_context_marker=release-US0131-release-20260907T211518Z-fresh`, `runtime_proof_id=rp-auto-20260907-us0131-release-release-20260907T211518Z-US-0131`, `model_id=composer-2.5`)
- Queue: **`handoffs/release_queue.md`** row **`S0133`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS** — all mandatory release gates (1, 2, 3, 4, 4b) green with **Fail:0**.
- **Run / verify:** `python -m pytest tests/us0131_contract_test.py -v` → 10 passed; `python scripts/check_intake_template_parity.py --scope=us-0131` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS (`coverage_missing=[]`); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; harness `tests/report.md` @ `2026-09-07T21:15:18Z` **Pass:853 / Fail:0**. See **`handoffs/releases/S0133-release-notes.md`** **## Run** / **## Verify**.
- **Operator summary**: start=`python -m pytest tests/us0131_contract_test.py -v`; endpoint=`n/a` (cross-host config kit); verify pointer=`handoffs/releases/S0133-release-notes.md` ## Verify.
- **Gate snapshot**: check_in_tests=PASS (harness Fail:0 + us0131 10/10); qa=PASS (0 blockers; B-1 CLOSED); verify_work=PASS (8/8 ACs; 9/9 UAT; 10/10 live); uat=PASS (9/9); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed @21:15:18Z before TTL 21:46:21Z); finalization=PASS (queue → `released`).
- ACs satisfied: **8/8** (10/10 contract markers live; 0 open blocking findings)
- Compose guards: DEC-0131 Accepted; US-0132 OOS; US-0131 OPEN; acceptance unchecked L159
- **Backlog status**: US-0131 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0131 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=10026570510E2C006AE4A86CFC2F0A70BE0CF170E30E43C13BEC342EC3E72D7A`, `proof_ttl=2026-09-07T22:15:18Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0132)

- Sprint: `S0132`
- Story: `BUG-0016` (OpenCode Layer-1 agent permission matrix vs kit duties — bash ask; PO paths; S* globs; release duty paths; 7 contract markers)
- Release: **finalized** (`2026-09-06T19:35:00Z`, `orchestrator_run_id=auto-20260906-bug0016`, `fresh_context_marker=release-BUG0016-release-20260906T193500Z-fresh`, `runtime_proof_id=rp-auto-20260906-bug0016-release-release-20260906T193500Z-BUG-0016`, `model_id=composer-2.5`)
- Queue: **`handoffs/release_queue.md`** row **`S0132`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS** — all mandatory release gates (1, 2, 3, 4, 4b) green with **Fail:0**.
- **Run / verify:** `python -m pytest tests/bug0016_contract_test.py -v` → 7 passed; `python -m pytest tests/us0122_contract_test.py -q` → 8 passed; `python scripts/check_intake_template_parity.py --scope=bug-0016` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS (`coverage_missing=[]`); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; harness `tests/report.md` @ `2026-09-06T20:46:57Z` **Pass:851 / Fail:0**. See **`handoffs/releases/S0132-release-notes.md`** **## Run** / **## Verify**.
- **Operator summary**: start=`python -m pytest tests/bug0016_contract_test.py -v`; endpoint=`n/a` (permission matrix kit); verify pointer=`handoffs/releases/S0132-release-notes.md` ## Verify.
- **Gate snapshot**: check_in_tests=PASS (harness Fail:0 + bug0016 7/7); qa=PASS (0 blockers); verify_work=PASS (8/8 ACs; 9/9 UAT; 7/7 live); uat=PASS (9/9); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed @19:35:00Z before TTL 20:25:00Z); finalization=PASS (queue → `released`).
- ACs satisfied: **8/8** (7/7 contract markers live; 0 open blocking findings)
- Compose guards: DEC-0122 §2 sole SOT; DEC-0124/0125 UNCHANGED; BUG-0016 OPEN L4914; acceptance unchecked L181
- **Backlog status**: BUG-0016 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: BUG-0016 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=FB658AA87D763F7282EEE5279116C551AF40C5F03A4D8DEF491E09EF2538135F`, `proof_ttl=2026-09-06T20:35:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0131)

- Sprint: `S0131`
- Story: `BUG-0015` (OpenCode `/auto` plugin dispatch attach — `command.transform` / `editor.add` → `runAutoLifecycle` + 7 contract-test markers)
- Release: **finalized** (`2026-09-06T15:30:00Z` attempt 2, `orchestrator_run_id=auto-20260906-bug0015`, `fresh_context_marker=release-BUG0015-release-rerun-20260906T153000Z-fresh`, `runtime_proof_id=rp-auto-20260906-bug0015-release-release-20260906T153000Z-BUG-0015`, `model_id=composer-2.5`)
- Queue: **`handoffs/release_queue.md`** row **`S0131`** = **`released`** (idempotent; workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (2nd attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green with **Fail:0**.
- **Run / verify:** `python -m pytest tests/bug0015_contract_test.py -v` → 7 passed in 0.69s; `python -m pytest tests/us0124_contract_test.py -q` → 12 passed; `python scripts/check_intake_template_parity.py --scope=bug-0015` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS (`coverage_missing=[]`); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; harness `tests/report.md` @ `2026-09-06T15:28:42Z` **Pass:849 / Fail:0**. See **`handoffs/releases/S0131-release-notes.md`** **## Run** / **## Verify**.
- **Operator summary**: start=`python -m pytest tests/bug0015_contract_test.py -v`; endpoint=`n/a` (plugin kit); verify pointer=`handoffs/releases/S0131-release-notes.md` ## Verify.
- **Gate snapshot**: check_in_tests=PASS (harness Fail:0 + bug0015 7/7); qa=PASS (0 blockers); verify_work=PASS (8/8 ACs; 9/9 UAT; 7/7 live); uat=PASS (9/9); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed @15:30:00Z before TTL 16:05:00Z); critic `ik_bug0015_release_gate1_fail_nonzero`=resolved; finalization=PASS (queue → `released`).
- ACs satisfied: **8/8** (7/7 contract markers live; 0 open blocking findings)
- Compose guards: DEC-0124/0125 UNCHANGED (backlog OPEN L4899; acceptance unchecked L180)
- **Backlog status**: BUG-0015 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: BUG-0015 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=1467A9436D9012A5974AC13C269E28EDFA1D1E9821BA3C94422E1DAB4D8FAD00`, `proof_ttl=2026-09-06T16:30:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0129)

- Sprint: `S0129`
- Story: `US-0129` (Architecture hot-surface rollover linkage guard — `arch_linkage_guard.py` pre/post `--rollover`, `ARCH_LINKAGE_ROLLOVER_BLOCKED`, optional `ARCH_LINKAGE_AUTO_REPAIR`, `/refresh-context` wiring, 8 contract-test markers, harness **26AB**)
- Release: **finalized** (`2026-08-27T08:42:00Z`, `orchestrator_run_id=auto-20260827-01`, `fresh_context_marker=rel-US0129-release-20260827T084200Z-fresh`, `runtime_proof_id=rp-auto-20260827-01-release-release-20260827T084200Z-US-0129`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0129`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0129_contract_test.py -v` → 8 passed in 0.58s; `python scripts/check_intake_template_parity.py --scope=arch-linkage` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS (`coverage_missing=[]`); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; `tests/report.md` Pass:847 / Fail:0 @ 2026-08-27T08:41:43Z (harness **re-run** this release spawn). See **`handoffs/releases/S0129-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 08:41:43Z; harness re-run post-execute incl. 26AB); qa=PASS (0 blockers); verify_work=PASS (6/6 ACs; 7/7 UAT; 8/8 live); uat=PASS (7/7); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 09:26:26Z); finalization=PASS (queue → `released`).
- ACs satisfied: **6/6** (8/8 contract markers live; 0 blocking findings)
- Compose guards: **8/8 UNCHANGED** (backlog OPEN L4482; acceptance unchecked L157; arch anchor L1527)
- **Backlog status**: US-0129 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0129 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=3E9968156A9C5EEF3338ADE30856B30A8166FCCFA085A5BD667CA49AEE6D5399`, `proof_ttl=2026-08-27T09:42:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0130)

- Sprint: `S0130`
- Story: `US-0130` (Operator-pinned sovereign-critic model — catalog `roles.critic` + scratchpad `MODEL_SOVEREIGN-CRITIC` + `select_critic_model` overlay + 10 contract-test markers)
- Release: **finalized** (`2026-08-26T22:42:00Z`, `orchestrator_run_id=auto-20260826-01`, `fresh_context_marker=rel-US0130-release-20260826T224200Z-fresh`, `runtime_proof_id=rp-auto-20260826-01-release-release-20260826T224200Z-US-0130`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0130`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0130_contract_test.py -v` → 10 passed in 0.06s; `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/check_intake_template_parity.py --scope=model-tier-overrides` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS (`coverage_missing=[]`; US-0130 OPEN excluded); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; `tests/report.md` Pass:845 / Fail:0 @ 2026-08-26T22:41:33Z (harness **re-run** this release spawn). See **`handoffs/releases/S0130-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 22:41:33Z; harness re-run post-execute); qa=PASS (0 blockers); verify_work=PASS (9/9 ACs; 10/10 UAT; 10/10 live); uat=PASS (10/10); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 23:31:36Z); finalization=PASS (queue → `released`).
- ACs satisfied: **9/9** (10/10 contract markers live; 0 blocking findings)
- Compose guards: **9/9 UNCHANGED** (backlog OPEN L4516; acceptance unchecked L158; arch anchor L1815)
- **Backlog status**: US-0130 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0130 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=8CD2E1B2A5D252EE4778E18A5F274C7DF6359042AC8E414D5B24540BB598C8FE`, `proof_ttl=2026-08-26T23:42:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0128)

- Sprint: `S0128`
- Story: `US-0128` (Convergence smoke surrogate for contract-test and waived-probe UAT slices — `_eval_smoke_green` surrogate, canonical `convergence_smoke` uat step, `CONVERGENCE_SMOKE_SURROGATE_MISSING`, `/qa`+`/verify-work` contracts, 11 contract-test markers)
- Release: **finalized** (`2026-08-26T20:58:00Z`, `orchestrator_run_id=auto-20260826-01`, `fresh_context_marker=rel-US0128-release-20260826T205800Z-fresh`, `runtime_proof_id=rp-auto-20260826-01-release-release-20260826T205800Z-US-0128`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0128`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0128_contract_test.py -v` → 11 passed in 1.42s; `python scripts/check_intake_template_parity.py --scope=sovereign-convergence` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS (`coverage_missing=[]`; US-0128 OPEN excluded); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; `tests/report.md` Pass:845 / Fail:0 @ 2026-08-26T20:57:42Z (harness **re-run** this release spawn). See **`handoffs/releases/S0128-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 20:57:42Z; harness re-run post-execute); qa=PASS (0 blockers); verify_work=PASS (6/6 ACs; 7/7 UAT; 11/11 live); uat=PASS (7/7); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 21:48:49Z); finalization=PASS (queue → `released`).
- ACs satisfied: **6/6** (11/11 contract markers live; 0 blocking findings)
- Compose guards: **8/8 UNCHANGED** (backlog OPEN L4445; acceptance unchecked L156; arch anchor L1671)
- **Backlog status**: US-0128 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0128 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=042AFE016454CE61643A0EEAA53AA44A9B2187EB2C19D8C944A77FBC6A335DFD`, `proof_ttl=2026-08-26T21:58:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0127)

- Sprint: `S0127`
- Story: `US-0127` (Convergence critic conjunct — blocking-only open findings + non-blocking auto-resolve at sovereign-critic PASS + hygiene CLI — 13 contract-test markers)
- Release: **finalized** (`2026-08-26T19:13:30Z`, `orchestrator_run_id=auto-20260826-01`, `fresh_context_marker=rel-US0127-release-20260826T191330Z-fresh`, `runtime_proof_id=rp-auto-20260826-01-release-release-20260826T191330Z-US-0127`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0127`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0127_contract_test.py -v` → 13 passed in 0.63s; `python scripts/check_intake_template_parity.py --scope=sovereign-critic` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → PASS after US-0126 dev README remediation; `python scripts/check-user-visible-metadata.py --repo .` → exit 0; `tests/report.md` Pass:845 / Fail:0 @ 2026-08-26T19:13:17Z (harness **re-run** this release spawn). See **`handoffs/releases/S0127-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 19:13:17Z; harness re-run); qa=PASS (0 blockers); verify_work=PASS (6/6 ACs; 13/13 live); uat=PASS (6/6); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 20:02:16Z); finalization=PASS (queue → `released`).
- ACs satisfied: **6/6** (13/13 contract markers live; 0 blocking findings)
- Compose guards: **8/8 UNCHANGED** (backlog OPEN L4407; acceptance unchecked L155; arch anchor L1852)
- **Backlog status**: US-0127 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0127 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=A8C7F6BE6B9E8B17D591AF58D108157DCD2BC040AD351DBBA235D77B480C0EB5`, `proof_ttl=2026-08-26T20:13:30Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0126)

- Sprint: `S0126`
- Story: `US-0126` (OpenCode host operator runbook + consolidated cross-host reason-code catalog + `--scope=opencode-adapter` parity — 12 contract-test markers, runbook h2 + README blurb, parity CLI scope extension)
- Release: **finalized** (`2026-08-25T17:30:00Z`, `orchestrator_run_id=auto-20260825-01`, `fresh_context_marker=rel-US0126-release-20260825T173000Z-fresh`, `runtime_proof_id=rp-auto-20260825-01-release-release-20260825T173000Z-US-0126`, `model_id=glm-5.2-high`)
- Queue: **`handoffs/release_queue.md`** row **`S0126`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0126_contract_test.py -v` → 12 passed in 0.14s; `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/validate_readme_feature_coverage.py --repo . --report` → `status=PASS coverage_missing=[]` (US-0126 absent — OPEN, excluded by validator); `python scripts/check-user-visible-metadata.py --repo .` → exit 0; `tests/report.md` Pass:845 / Fail:0 literal @ 2026-08-25T17:13:14Z (harness **not** re-run this release spawn). See **`handoffs/releases/S0126-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 17:13:14Z accepted; metadata guard exit 0); qa=PASS (loop-2; 0 blockers; B-1 CLOSED in execute loop-2); verify_work=PASS (loop-2; 10/10 ACs; 12/12 live); uat=PASS (12/12); isolation=PASS (execute loop-2+qa loop-2+verify-work loop-2+sovereign-critic; model_id=glm-5.2-high set); strict_runtime_proof=PASS (verify-work proof consumed before TTL 18:24:35Z; hash recomputed match); finalization=PASS (queue → `released`).
- ACs satisfied: **10/10** (12/12 contract markers live; 0 blocking findings)
- Compose guards: **8/8 UNCHANGED** (backlog OPEN L4368; acceptance unchecked L154; arch anchor L1747; DEC-0126 Accepted; cursor commands unchanged; cursor agents unchanged; template/.opencode unchanged; installer-owned-paths.manifest unchanged; OPENCODE_VALIDATOR_FAILED wrapper NOT resurrected; mirrors byte-identical)
- **Backlog status**: US-0126 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0126 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=7070BE1A0FE9386E67DE72AB2ED35FFE307A1355B49151785BDC728A5BFF6EB3`, `proof_ttl=2026-08-25T18:30:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0125)

- Sprint: `S0125`
- Story: `US-0125` (OpenCode thin dispatch-only commands + validator bridge — 15 command files ≤20 lines, Python CLI SOT, 11 contract-test markers)
- Release: **finalized** (`2026-08-24T21:33:00Z`, `orchestrator_run_id=auto-20260824-02`, `fresh_context_marker=rel-US0125-release-20260824T213300Z-fresh`, `runtime_proof_id=rp-auto-20260824-02-release-release-20260824T213300Z-US-0125`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0125`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0125_contract_test.py -v` → 11 passed in 0.45s; `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`; `tests/report.md` Pass:845 / Fail:0 literal @ 2026-08-24T21:04:51Z (harness **not** re-run this release spawn). See **`handoffs/releases/S0125-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 21:04:51Z accepted; metadata guard L712–L717); qa=PASS (loop-2; 0 blockers; B-1+B-2 closed); verify_work=PASS (11/11; 11/11 live); uat=PASS (11/11); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 23:35:00Z); finalization=PASS (queue → `released`).
- ACs satisfied: **10/10** (11/11 contract markers live; 0 blocking findings)
- Compose guards: **7/7 UNCHANGED** (backlog OPEN; acceptance unchecked; arch anchor; DEC-0125 Accepted; cursor commands unchanged; mirrors byte-identical)
- **Backlog status**: US-0125 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0125 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=CB1BB92BB263BEA244C382A4A7B3662BB45A00EBD4B41ECC4E8ADB5F26A5E2CC`, `proof_ttl=2026-08-24T22:33:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0124)

- Sprint: `S0124`
- Story: `US-0124` (OpenCode orchestrator plugin spawn-only `/auto` — US-0069 phase→role spawn, isolation evidence, US-0092 stop matrix + headless invoke, 12 contract-test markers)
- Release: **finalized** (`2026-08-24T19:35:00Z`, `orchestrator_run_id=auto-20260824-02`, `fresh_context_marker=rel-US0124-release-20260824T193500Z-fresh`, `runtime_proof_id=rp-auto-20260824-02-release-release-20260824T193500Z-US-0124`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0124`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0124_contract_test.py -v` → 12 passed in 1.14s; `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`; `tests/report.md` Pass:845 / Fail:0 literal @ 2026-08-24T19:17:58Z (harness **not** re-run this release spawn). See **`handoffs/releases/S0124-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 19:17:58Z accepted; metadata guard L712–L717); qa=PASS (loop-2; 0 blockers; B-1 closed); verify_work=PASS (loop-2; 11/11; 12/12 live); uat=PASS (11/11); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 20:30:00Z); finalization=PASS (queue → `released`).
- ACs satisfied: **11/11** (12/12 contract markers live; 0 blocking findings)
- Compose guards: **9/9 UNCHANGED** (backlog OPEN; acceptance unchecked; arch anchor; DEC-0124 Accepted; no auto.md clone; mirrors byte-identical)
- **Backlog status**: US-0124 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0124 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** + **`RELEASE_PUBLISH_AUTO_CONFIRM=0`** — `publish_snapshot=skipped_pending_operator_confirm`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=21738212CD0C94494ECB8951B233CFD0FFE663852BDF643E0598AE83E8043777`, `proof_ttl=2026-08-24T20:35:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0123)

- Sprint: `S0123`
- Story: `US-0123` (Per-role OpenCode model slug routing — example catalog + materializer + fail-closed validator + 8 contract-test markers)
- Release: **finalized** (`2026-08-24T15:32:00Z`, `orchestrator_run_id=auto-20260824-01`, `fresh_context_marker=rel-US0123-release-20260824T153200Z-fresh`, `runtime_proof_id=rp-auto-20260824-01-release-release-20260824T153200Z-US-0123`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0123`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (1st attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green.
- **Run / verify:** `python -m pytest tests/us0123_contract_test.py -v` → 8 passed in 0.20s; `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`; `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` → `[MODEL_TIER_VALIDATION_OK]`; `tests/report.md` Pass:845 / Fail:0 literal @ 2026-08-24T15:12:17Z (harness **not** re-run this release spawn). See **`handoffs/releases/S0123-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 15:12:17Z accepted; metadata guard L712–L717); qa=PASS (loop-2; 0 blockers); verify_work=PASS (loop-2; 10/10; 8/8 live); uat=PASS (10/10); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 16:24:00Z); finalization=PASS (queue → `released`).
- ACs satisfied: **10/10** (8/8 contract markers live; 0 blocking findings; 1 non-blocking carry-forward)
- Compose guards: **6/6 UNCHANGED** (backlog OPEN; acceptance unchecked; arch anchor; DEC-0123 Accepted; no `model:`; mirrors byte-identical)
- **Backlog status**: US-0123 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0123 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — `publish_snapshot=skipped_disabled`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=EED2303A06C30EB5DAC490D738B95F1B1D7E281A0CF20F1DCC6C8B8E7ECD81F6`, `proof_ttl=2026-08-24T16:32:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release finalized note (S0122)

- Sprint: `S0122`
- Story: `US-0122` (OpenCode role agents and Layer-1 permission table — eight markdown agents in `template/.opencode/agents/` + locked DEC-0122 §2 matrix + 8 contract-test markers)
- Release: **finalized** (`2026-08-24T13:22:00Z`, `orchestrator_run_id=auto-20260824-01`, `fresh_context_marker=rel-US0122-release-20260824T132200Z-fresh`, `runtime_proof_id=rp-auto-20260824-01-release-release-20260824T132200Z-US-0122`, `model_id=composer-2.5-fast`)
- Queue: **`handoffs/release_queue.md`** row **`S0122`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (2nd attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green. Prior BLOCKED attempt (2026-08-24T12:45:00Z `RELEASE_TEST_FAILED`) CLOSED by execute loop-2 remediations + qa/verify-work loop-2.
- **Run / verify:** `python -m pytest tests/us0122_contract_test.py -v` → 8 passed in 0.03s; `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`; `tests/report.md` Pass:845 / Fail:0 literal @ 2026-08-24T13:02:49Z (harness **not** re-run this release spawn). See **`handoffs/releases/S0122-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Fail:0 @ 13:02:49Z accepted; metadata guard L712–L717); qa=PASS (loop-2; 0 blockers); verify_work=PASS (loop-2; 10/10; 8/8 live); uat=PASS (10/10); isolation=PASS; strict_runtime_proof=PASS (verify-work proof consumed before TTL 14:16:00Z); finalization=PASS (queue → `released`).
- ACs satisfied: **10/10** (8/8 contract markers live; 0 blocking findings; 3 non-blocking carry-forwards)
- Compose guards: **5/5 UNCHANGED** (US-0003, US-0023/BUG-0006, US-0121, US-0102/DEC-0087, US-0002/US-0004)
- **Backlog status**: US-0122 remains **OPEN** — closure deferred to `/closure`
- **Acceptance**: US-0122 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — `publish_snapshot=skipped_disabled`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Strict runtime proof (release)**: `proof_hash=82FDC8D25981588F7AF370ECE715A8D84187DEAC7057FE2E9FD2717EE834741A`, `proof_ttl=2026-08-24T14:22:00Z`
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro phase 2 per DEC-0082)

## Release blocked note (S0122 — historical, 1st attempt; superseded by PASS above)

- Sprint: `S0122`
- Story: `US-0122`
- Release: **BLOCKED (1st attempt)** (`2026-08-24T12:45:00Z`, `fresh_context_marker=rel-US0122-release-20260824T124500Z-fresh`, `runtime_proof_id=rp-auto-20260824-01-release-release-20260824T124500Z-US-0122`) — **superseded by `released` on 2026-08-24T13:22:00Z (2nd attempt) above**
- **Reason code**: `RELEASE_TEST_FAILED` (harness Fail:15 @ 12:44:49Z pre-remediation)
- **Remediation (completed)**: execute loop-2 mirrored runbook, fixed architecture ordering, triad rollover → `tests/report.md` Fail:0 @ 13:02:49Z; qa loop-2 + verify-work loop-2 PASS

## Release finalized note (S0121)

- Sprint: `S0121`
- Story: `US-0121` (OpenCode host-mode adapter — additive `--host cursor|opencode|both` + empty-but-valid `template/.opencode/` pack + parity scope + 14 contract-test markers)
- Release: **finalized** (`2026-08-24T10:58:00Z`, `orchestrator_run_id=auto-20260824-01`, `fresh_context_marker=rel-US0121-release-20260824T105800Z-fresh`, `runtime_proof_id=rp-auto-20260824-01-release-release-20260824T105800Z-US-0121`, `model_id=glm-5.2-high`)
- Queue: **`handoffs/release_queue.md`** row **`S0121`** = **`released`** (workflow-only; no version bump; backlog reconciliation deferred to `/closure`)
- **Verdict**: **PASS (3rd attempt)** — all mandatory release gates (1, 2, 3, 4, 4b) green. Prior BLOCKED attempts (2026-08-23T12:48:00Z + 2026-08-23T16:35:00Z) CLOSED by execute loop-3+4 harness remediation + fresh verify-work (2026-08-24T10:52:00Z).
- **Run / verify:** `python -m pytest tests/us0121_host_mode_test.py -v` → 14 passed in 3.43s (Python 3.12.10 on PATH; pytest 9.1.1); `python scripts/check_intake_template_parity.py --scope=opencode-adapter` → `[INTAKE_TEMPLATE_PARITY_OK]`; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → exit 0; `tests/report.md` Pass:845 / Fail:0 literal; zero `[FAIL]` rows. See **`handoffs/releases/S0121-release-notes.md`** **## Run** / **## Verify**.
- **Gate snapshot**: check_in_tests=PASS (Pass:845/Fail:0 literal @ 2026-08-24T10:45:36Z; US-0071 metadata guard coverage present); qa=PASS (loop-3; 0 blockers; B-1 CLOSED; NB-1 CLOSED for env); verify_work=PASS (10/10 ACs live; 14/14 contract-test markers PASSED live); uat=PASS (10/10 ACs; probe `UAT_PROBE_PASS`); isolation=PASS (execute loop-3+loop-4, qa loop-3, verify-work, sovereign-critic; all `model_id` set); strict_runtime_proof=PASS (verify-work + qa loop-3 + execute loop-4 proofs all fresh within 1-hour TTL; no reuse); finalization=PASS (queue row S0121 → `released`).
- ACs satisfied: **10/10** (live pytest 14/14; B-1 CLOSED; 0 blocking findings; 4 non-blocking NB-1..NB-4 carried, NB-1 CLOSED for env)
- Compose guards: **5/5 UNCHANGED** (US-0008, DEC-0045, US-0102, US-0001, US-0018 — additive only; release does not mutate installer surfaces)
- **Backlog status**: US-0121 remains **OPEN** — closure deferred to `/closure` per US-0120 design (release does not flip backlog Status or tick ACs)
- **Acceptance**: US-0121 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — `publish_snapshot=skipped_disabled` (`RELEASE_PUBLISH_AUTO_CONFIRM=0`)
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Isolation**: PASS (execute loop-3+loop-4, qa loop-3, verify-work, sovereign-critic in `docs/engineering/state.md`; release checkpoint appended with `model_id=glm-5.2-high`)
- **Strict runtime proof (release)**: `proof_hash=284BA5148FC227A2DA47A0D10DA126F78E8330423C814D66571BA3264335ABBB`, `proof_ttl=2026-08-24T11:58:00Z` (attests fresh release subagent context AND release PASS — all gates 1–4b green)
- **Next**: **`/closure`** (fresh **qe** subagent, ship macro — second canonical phase per DEC-0082) for backlog OPEN→DONE + acceptance tick + `sprints/S0121/closure-verification.md` + closure checkpoint in `docs/engineering/state.md`. After closure PASS → `/refresh-context` (fresh curator subagent).

## Release blocked note (S0121 — historical, 2nd attempt; superseded by PASS above)

- Sprint: `S0121`
- Story: `US-0121` (OpenCode host-mode adapter — additive `--host cursor|opencode|both` + empty-but-valid `template/.opencode/` pack + parity scope + 14 contract-test markers)
- Release: **BLOCKED (2nd attempt)** (`2026-08-23T16:35:00Z`, `orchestrator_run_id=auto-20260823-01`, `fresh_context_marker=rel-US0121-release-20260823T163500Z-fresh`, `runtime_proof_id=rp-auto-20260823-01-release-release-20260823T163500Z-US-0121`, `model_id=glm-5.2-high`)
- Queue: **`handoffs/release_queue.md`** row **`S0121`** was **`blocked`** (NOT `released` — fail-closed) — **superseded by `released` on 2026-08-24T10:58:00Z (3rd attempt) above**
- **Reason codes**: `RELEASE_TEST_FAILED` (fresh `tests/report.md` @ 2026-08-23T16:27:27Z records `Pass:779 / Fail:50`; Fail ≠ 0) + `RUNTIME_PROOF_STALE` (prior verify-work proof TTL `2026-08-23T13:00:00Z` is in the past relative to now `2026-08-23T16:35:00Z`; prior release proof attested BLOCKED and is also stale → not reused)
- **Prior attempt closure**: The 12:48:00Z `RELEASE_TEST_STALE` + `RELEASE_TEST_EVIDENCE_MISSING` are now CLOSED by operator remediation (python 3.12.10 user-scope on PATH; `python -m pytest tests/us0121_host_mode_test.py -v` → 14 passed per orchestrator resume note 2026-08-23T16:32:00Z; `tests/report.md` refreshed 2026-08-23T16:27:27Z). However the canonical harness still recorded `Fail:50`, so gate 1 failed with a new reason code `RELEASE_TEST_FAILED`.
- **Remediation (completed)**: reran `/verify-work` (qa) in a fresh subagent to mint a fresh gate-4b proof (2026-08-24T10:52:00Z); resolved the 50 failing canonical harness rows via execute loop-3+4 so `tests/report.md` reaches `Fail:0` (Pass:845 @ 2026-08-24T10:45:36Z); reran `/release` in a fresh subagent (3rd attempt → PASS above).

## Release finalized note (S0120)

- Sprint: `S0120`
- Story: `US-0120` (Dedicated `/closure` phase with exclusive Story Closure responsibility)
- Release: **finalized** (`2026-07-08T19:45:00Z`, `orchestrator_run_id=auto-20260708-01`, `fresh_context_marker=release-US0120-release-20260708T194500Z-fresh`, `runtime_proof_id=rp-auto-20260708-01-release-release-20260708T194500Z-US-0120`)
- Queue: **`handoffs/release_queue.md`** row **`S0120`** = **`released`** (governance-only; backlog reconciliation deferred to `/closure`)
- **Run / verify:** `python -m pytest tests/us0120_closure_phase_test.py -v` → 10 passed in 0.08s; `python scripts/validate_closure_verification.py --self-test` → `[VALIDATE_CLOSURE_VERIFICATION_SELF_TEST_OK]` exit 0; `python scripts/check_intake_template_parity.py --repo . --scope=us-0120` → `[INTAKE_TEMPLATE_PARITY_OK]` exit 0. See **`handoffs/releases/S0120-release-notes.md`**.
- ACs satisfied: **12/12** (closure command, DEC-0052/DEC-0082, auto orchestration, release.md step removal, closure-verification schema, isolation/runtime proof contracts, 10 contract tests, drain hook, documentation, compose guards)
- Compose guards: **6/6 UNCHANGED** (US-0043, US-0045, US-0040, US-0048, US-0056, US-0096)
- **Backlog status**: US-0120 remains **OPEN** — closure deferred to `/closure` per US-0120 design
- **Acceptance**: US-0120 row remains **unchecked** — tick at `/closure`
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — `publish_snapshot=skipped_disabled`
- Sync: **`SYNC_POLICY_MODE=disabled`** → `push_decision=not_eligible`, `reason_code=SYNC_DISABLED`
- **Next**: **`/closure`** (fresh **qe** context, ship macro — second canonical phase per DEC-0082)

## Release finalized note (S0118)

- Sprint: `S0118`
- Story: `US-0118` (Work-kind classification + tiered delivery routing per story)
- Release: **finalized** (`2026-07-05T00:20:00Z`, `orchestrator_run_id=auto-20260704-01`, `fresh_context_marker=release-US0118-release-20260705T002000Z-fresh`, `runtime_proof_id=rp-auto-20260704-01-release-release-20260705T002000Z-US-0118`)
- Queue: **`handoffs/release_queue.md`** row **`S0118`** = **`released`** (out-of-band; documentation+code story, default-off feature, no version bump)
- **Run / verify:** `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed in 0.10s; `python -m pytest tests/us0118_contract_test.py -v` → 13 passed in 0.10s (17 total); `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 (`coverage_missing=[]`); `python scripts/validate_doc_profile.py --repo .` → `[DOC_PROFILE_VALIDATE_OK]`; `python scripts/check-user-visible-metadata.py --repo .` → exit 0 (silent PASS); `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`; `python scripts/check_intake_template_parity.py --scope work-kind-routing --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=work-kind-routing`; `python scripts/work_kind_classify_lib.py --self-test` → `[WORK_KIND_CLASSIFY_SELF_TEST_OK]` exit 0; `python scripts/work_kind_routing_lib.py --self-test` → `[WORK_KIND_ROUTING_SELF_TEST_OK]` exit 0; `python -c "...PARITY_OK..."` → `PARITY_OK 203287 203287` (byte-identical). See **`handoffs/releases/S0118-release-notes.md`** **## Validator outputs**.
- ACs satisfied: **12/12** (AC-1 classifier lib, AC-2 doc/mini/code rules + Q1 tie-break, AC-3 `WORK_KIND_ROUTING=0` default-off + zero-overhead-when-off, AC-4 backlog row fields, AC-5 `/intake` step 4b hook + operator accept/override, AC-6 `/auto` step 0a hook + L8 precedence, AC-7 6 `WORK_KIND_*` reason codes + remediation, AC-8 compose-do-not-amend 6/6 read-only consumers + 23/23 compose guards UNCHANGED + `dev_environment_lib.py` IMPORT only (Q9 LOCKED), AC-9 13 `test_us0118_*` markers + `--scope=work-kind-routing` parity, AC-10 `## US-0118` h1 anchor at architecture.md L1713 (T-anch NO-OP / verification), AC-11 runbook h2 + `/auto` + `/intake` prose, AC-12 `--self-test` exits 0 + installer manifest triple-installer parity)
- Compose guards: **23/23 UNCHANGED** (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062 — additive-only; US-0118 itself does NOT become a NEW compose guard — it's a routing primitive)
- Files shipped: `scripts/work_kind_classify_lib.py` (NEW) + `template/scripts/work_kind_classify_lib.py` (NEW), `scripts/work_kind_routing_lib.py` (NEW) + `template/scripts/work_kind_routing_lib.py` (NEW), `tests/us0118_contract_test.py` (NEW) + `template/tests/us0118_contract_test.py` (NEW), `its_magic/README.md` (umbrella + operator subsection + scratchpad ref extension; pure addition +2333 / 0 deletions), `template/its_magic/README.md` (byte-sync per AC-5/AC-9), `docs/engineering/runbook.md` + `template/docs/engineering/runbook.md` (`## Work-kind routing (US-0118 / DEC-0118)` h2 L3579), `.cursor/commands/auto.md` + `template/.cursor/commands/auto.md` (step 0a hook L292–L300), `.cursor/commands/intake.md` + `template/.cursor/commands/intake.md` (step 4b hook L246+), `.cursor/scratchpad.md` + `template/.cursor/scratchpad.local.example.md` + `.cursor/scratchpad.local.example.md` (`WORK_KIND_ROUTING=0` + `WORK_KIND_TIE_BREAK=highest_tier_wins` keys L188–L199), `docs/engineering/context/installer-owned-paths.manifest` + `template/docs/engineering/context/installer-owned-paths.manifest` (both new scripts listed in `[install_include_paths]` + `[clean_paths]` + `[required_install_script_paths]`), `scripts/check_intake_template_parity.py` + `template/scripts/check_intake_template_parity.py` (`WORK_KIND_ROUTING_PAIRS` (8 byte-identical pairs) + `--scope=work-kind-routing` flag)
- US-0113/US-0114/US-0115/US-0116/US-0117 byte-stability preserved (**6th-story cumulative surface — first 6-cumulative-surface story**; US-0118 adds net-new-keys-only + cross-link-pointers + reason-code-only entries to its own 6th sub-block; never edits US-0113's L2421, US-0114's L2545, US-0115's L2617, US-0116's L2765, or US-0117's L2856 blocks; pure addition 2333 insertions / 0 deletions confirmed via `git diff --stat HEAD -- its_magic/README.md`; `PARITY_OK 203287 203287` authoritative end-to-end proof; pattern now scales from quint to sextet)
- `## US-0118` section resolved in `/architecture` phase (T-anch NO-OP / verification per R-0105 Q-2 LOCKED — no execute-phase write to architecture.md; anchor confirmed at L1713)
- `dev_environment_lib.py` NOT modified (Q9 LOCKED import contract — `TIER_C_SKIP_PREFIXES` + `classify_touched_files` imported, not reimplemented; contract test `test_us0118_classify_touched_files_reuse` enforces the boundary; PASS)
- Backward compatibility: `WORK_KIND_ROUTING=0` default-off + early-return + `/intake` step 5 skip; contract test `test_us0118_default_off_zero_overhead` asserts byte-identical-to-pre-US-0118 behavior — PASS
- No packaging version bump (documentation+code story released out-of-band; default-off feature — no installer-visible behavior change; S0117 precedent — S0113..S0117 all shipped without bump); no `its_magic/.its-magic-version` change (remains `0.1.3-3`); no chocolatey `.nupkg`/`.nuspec` changes; no homebrew `.rb` formula changes
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- Release trigger: **`RELEASE_TRIGGER_SOURCE=manual`** (no adapter subprocess)
- Drain-advance note: 1 story shipped this cycle; backlog drain active. **US-0108 status-drift** flagged as non-blocking finding for operator awareness (US-0108 shipped via `sprints/S0108/release-verdict.json` but its `docs/product/backlog.md` row was never flipped OPEN→DONE — US-0045 status authority drift; reconcile separately)
- **Next**: **`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase per ultra_lean) for segment closeout; backlog drain continues with drain-advance to next OPEN story or drain-complete terminal

## Release finalized note (S0117)

- Sprint: `S0117`
- Story: `US-0117` (Phase & role governance operator documentation in framework README)
- Release: **finalized** (`2026-07-04T20:12:10Z`, `orchestrator_run_id=auto-20260704-01`, `fresh_context_marker=release-US0117-release-20260704T201210Z-fresh`, `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T201210Z-US-0117`)
- Queue: **`handoffs/release_queue.md`** row **`S0117`** = **`released`** (out-of-band; documentation-only, no version bump)
- **Drain-complete note**: **5/5 stories shipped** (US-0113, US-0114, US-0115, US-0116, US-0117). All 5 documentation families complete. Drain queue now EMPTY (0 stories remaining).
- **Run / verify:** `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed in 0.10s; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 (`coverage_missing=[]`); `python scripts/validate_doc_profile.py --repo .` → `[DOC_PROFILE_VALIDATE_OK]`; `python scripts/check-user-visible-metadata.py --repo .` → exit 0 (silent PASS); `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`; `python -c "...PARITY_OK..."` → `PARITY_OK 191091 191091` (AC-5 byte-identical). See **`handoffs/releases/S0117-release-notes.md`** **## Validator outputs**.
- ACs satisfied: **8/8** (AC-1 umbrella `### Phase & role governance` at L1864, AC-2 18 subsections US-0069→US-0090, AC-3 scratchpad ref extension 46 net-new keys + 9 reason-code-only + 7 prose-only + cross-link pointers at L2856, AC-4 coverage preserved, AC-5 framework README parity, AC-6 metadata hygiene, AC-7 18 runbook cross-links, AC-8 regression tests)
- Compose guards: **23/23 UNCHANGED** (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062 — documentation-only)
- Files shipped: `its_magic/README.md` (umbrella + 18 subsections + scratchpad ref extension; pure addition +2188 / 0 deletions), `template/its_magic/README.md` (byte-sync per AC-5)
- US-0113/US-0114/US-0115/US-0116 byte-stability preserved (5th-story cumulative surface — first 5-cumulative-surface story; net-new keys + cross-link pointers + reason-code-only + prose-only entries only; no edits to US-0113's L2421, US-0114's L2545, US-0115's L2617, or US-0116's L2765 blocks)
- 36 DC anchors + `## US-0117` section resolved in `/architecture` phase (final deferred-candidate resolution point — T-anch in S0117 = NO-OP / verification)
- 2 labeling corrections applied (US-0082 = "Codebase map" NOT "Input compression"; US-0090 = "Caveman input compression" NOT "Phase governance integration")
- 1 US-id collision resolved (US-0089 = "Auto orchestration" NOT "Caveman mode" per `/architecture` lock)
- No packaging version bump (documentation-only); no `its_magic/.its-magic-version` change; no chocolatey/homebrew changes
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- Release trigger: **`RELEASE_TRIGGER_SOURCE=manual`** (no adapter subprocess)
- **Next**: **`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout; backlog drain queue **EMPTY** (0 stories remaining — final story in 5-story drain shipped)

## Release finalized note (S0116)

- Sprint: `S0116`
- Story: `US-0116` (Delivery & lifecycle operator documentation in framework README)
- Release: **finalized** (`2026-07-04T17:51:00Z`, `orchestrator_run_id=auto-20260704-01`, `fresh_context_marker=release-US0116-release-20260704T175100Z-fresh`, `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T175100Z-US-0116`)
- Queue: **`handoffs/release_queue.md`** row **`S0116`** = **`released`** (out-of-band; documentation-only, no version bump)
- **Run / verify:** `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed in 0.09s; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 (`coverage_missing=[]`); `python scripts/validate_doc_profile.py --repo .` → `[DOC_PROFILE_VALIDATE_OK]`; `python scripts/check-user-visible-metadata.py --repo .` → exit 0 (silent PASS); `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`; `python -c "...PARITY_OK..."` → `PARITY_OK 145485 145485` (AC-5 byte-identical). See **`handoffs/releases/S0116-release-notes.md`** **## Validator outputs**.
- ACs satisfied: **8/8** (AC-1 umbrella `### Delivery & lifecycle` at L1665, AC-2 4 subsections US-0092→US-0095→US-0098→US-0099, AC-3 scratchpad ref extension 2 net-new keys + 5 reason-code-only entries + grouped cross-link pointers + cross-link to US-0114 L1806 + cross-link to US-0115 L1878 at L2225, AC-4 coverage preserved, AC-5 framework README parity, AC-6 metadata hygiene, AC-7 4 runbook cross-links, AC-8 regression tests)
- Compose guards: **23/23 UNCHANGED** (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062 — documentation-only)
- Files shipped: `its_magic/README.md` (umbrella + 4 subsections + scratchpad ref extension; pure addition +1370 / 0 deletions), `template/its_magic/README.md` (byte-sync per AC-5)
- US-0113/US-0114/US-0115 byte-stability preserved (4th-story cumulative surface — first 4-cumulative-surface story; cross-link pointers + reason-code-only entries + 2 net-new US-0098 key rows only; no edits to US-0113's L1682, US-0114's L1806, or US-0115's L1878 blocks)
- DC-4 deferred to US-0117 (4 missing `# US-0092`/`# US-0095`/`# US-0098`/`# US-0099` h1 anchors in `architecture.md`; US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) + DC-4 (4) = 18 total)
- No packaging version bump (documentation-only); no `its_magic/.its-magic-version` change; no chocolatey/homebrew changes
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- Release trigger: **`RELEASE_TRIGGER_SOURCE=manual`** (no adapter subprocess)
- **Next**: **`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout; backlog drain continues with US-0117 (1 story remaining — inherits 18 architecture.md triad hygiene anchors)

## Release finalized note (S0115)

- Sprint: `S0115`
- Story: `US-0115` (Integration & observability operator documentation in framework README)
- Release: **finalized** (`2026-07-04T08:47:00Z`, `orchestrator_run_id=auto-20260704-01`, `fresh_context_marker=release-US0115-release-20260704T084700Z-fresh`, `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T084700Z-US-0115`)
- Queue: **`handoffs/release_queue.md`** row **`S0115`** = **`released`** (out-of-band; documentation-only, no version bump)
- **Run / verify:** `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed in 0.06s; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 (`coverage_missing=[]`); `python scripts/validate_doc_profile.py --repo .` → `[DOC_PROFILE_VALIDATE_OK]`; `python scripts/check-user-visible-metadata.py --repo .` → exit 0 (silent PASS); `python scripts/check_intake_template_parity.py --repo .` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`; `python -c "...PARITY_OK..."` → `PARITY_OK 128660 128660` (AC-5 byte-identical). See **`handoffs/releases/S0115-release-notes.md`** **## Validator outputs**.
- ACs satisfied: **8/8** (AC-1 umbrella `### Integration & observability` at L1410, AC-2 7 subsections US-0034→US-0084→US-0086→US-0093→US-0096→US-0101→US-0102, AC-3 scratchpad ref extension net-new keys + cross-link pointers + reason-code-only entries at L1878, AC-4 coverage preserved, AC-5 framework README parity, AC-6 metadata hygiene, AC-7 7 runbook cross-links, AC-8 regression tests)
- Compose guards: **23/23 UNCHANGED** (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0034, US-0084, US-0086, US-0093, US-0096, US-0041, US-0062 — documentation-only)
- Files shipped: `its_magic/README.md` (umbrella + 7 subsections + scratchpad ref extension), `template/its_magic/README.md` (byte-sync per AC-5)
- US-0113/US-0114 byte-stability preserved (3rd-story cumulative surface; cross-link pointers only; no edits to US-0113's L1682 or US-0114's L1806 blocks)
- DC-3 deferred to US-0117 (7 missing `# US-xxxx` h1 anchors in `architecture.md`; US-0117 inherits DC-1 (5) + DC-2 (2) + DC-3 (7) = 14 total)
- No packaging version bump (documentation-only); no `its_magic/.its-magic-version` change; no chocolatey/homebrew changes
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- Release trigger: **`RELEASE_TRIGGER_SOURCE=manual`** (no adapter subprocess)
- **Next**: **`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout; backlog drain continues with US-0116, US-0117 (2 stories remaining)

## Release finalized note (S0114)

- Sprint: `S0114`
- Story: `US-0114` (Release & distribution operator documentation in framework README)
- Release: **finalized** (`2026-07-04T07:12:00Z`, `orchestrator_run_id=auto-20260704-01`, `fresh_context_marker=release-S0114-US0114-20260704T071200Z-fresh`, `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T071200Z-US-0114`)
- Queue: **`handoffs/release_queue.md`** row **`S0114`** = **`released`**
- **Run / verify:** `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` exit 0 (no new gaps); `python scripts/validate_doc_profile.py` → `[DOC_PROFILE_VALIDATE_OK]`; `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`; `cmd /c fc /b its_magic\README.md template\its_magic\README.md` → no differences (AC-5 byte-identical). See **`handoffs/releases/S0114-release-notes.md`** **## Run** / **## Verify**.
- ACs satisfied: **8/8** (AC-1 umbrella, AC-2 4 subsections US-0041→US-0062→US-0111→US-0112, AC-3 scratchpad ref extension net-new keys + cross-link pointers, AC-4 coverage preserved, AC-5 framework README parity, AC-6 metadata hygiene, AC-7 runbook cross-links, AC-8 regression tests)
- Compose guards: **18/18 UNCHANGED** (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112, US-0041, US-0062 — documentation-only)
- Files shipped: `its_magic/README.md` (umbrella + 4 subsections + scratchpad ref extension), `template/its_magic/README.md` (byte-sync per AC-5)
- US-0113 byte-stability preserved (cross-link pointers only; no edits to US-0113's umbrella or sovereign-loop keys block)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- Release trigger: **`RELEASE_TRIGGER_SOURCE=manual`** (no adapter subprocess)
- **Next**: **`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout; backlog drain continues with US-0115, US-0116, US-0117 (3 stories remaining)

## Release finalized note (S0113)

- Sprint: `S0113`
- Story: `US-0113` (Sovereign-loop operator documentation in framework README)
- Release: **finalized** (`2026-07-04T03:00:00Z`, `orchestrator_run_id=auto-20260704-01`, `fresh_context_marker=release-S0113-US0113-20260704T030000Z-fresh`, `runtime_proof_id=rp-auto-20260704-01-release-release-20260704T030000Z-US-0113`)
- Queue: **`handoffs/release_queue.md`** row **`S0113`** = **`released`**
- **Run / verify:** `python -m pytest tests/scratchpad_example_parity_test.py -v` → 4 passed; `python scripts/validate_doc_profile.py` → `[DOC_PROFILE_VALIDATE_OK]`; `python scripts/check_intake_template_parity.py` → `[INTAKE_TEMPLATE_PARITY_OK] scope=intake`; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → exit 1 only on pre-existing US-0117 gap (out-of-scope DC-1; no NEW gaps — AC-4 preservation satisfied); `fc /b its_magic\README.md template\its_magic\README.md` → no differences (AC-5 byte-identical). See **`handoffs/releases/S0113-release-notes.md`** **## Run** / **## Verify**.
- ACs satisfied: **8/8** (AC-1 umbrella, AC-2 9 subsections, AC-3 scratchpad ref extension, AC-4 coverage preserved, AC-5 framework README parity, AC-6 metadata hygiene, AC-7 runbook cross-links, AC-8 regression tests)
- Compose guards: **16/16 UNCHANGED** (US-0091, US-0097, US-0017, US-0040, US-0100..US-0112 — documentation-only)
- Files shipped: `its_magic/README.md` (umbrella + 9 subsections + scratchpad ref extension), `template/its_magic/README.md` (byte-sync per AC-5)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- Release trigger: **`RELEASE_TRIGGER_SOURCE=manual`** (no adapter subprocess)
- **Next**: **`/refresh-context`** (fresh **curator** context, ship macro — second canonical phase) for segment closeout; backlog drain continues with US-0114..US-0117 (4 stories remaining)

## Release finalized note (S-BUG0014)

- Sprint: `S-BUG0014`
- Bug: `BUG-0014` (Sovereign-loop era features missing from README feature coverage catalog and legacy release_notes.md)
- Release: **finalized** (`2026-07-03T20:10:00Z`, `orchestrator_run_id=auto-20260703-01`, `fresh_context_marker=release-SBUG0014-BUG0014-20260703T201000Z-fresh`)
- Queue: **`handoffs/release_queue.md`** row **`S-BUG0014`** = **`released`**
- **Run / verify:** `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]` (117/117); `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` → `[BUG_VALIDATION_OK]`; see **`handoffs/releases/S-BUG0014-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty**

## Release finalized note (S0112)

- Sprint: `S0112`
- Story: `US-0112` (Ship model-catalog example presets on install/upgrade — DEC-0112)
- Release: **finalized** (`2026-06-30T23:40:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0112-US0112-20260630T234000Z-fresh`)
- Queue: **`handoffs/release_queue.md`** row **`S0112`** = **`released`**
- **Run / verify:** `pytest tests/us0112_contract_test.py -v` -> 12 passed; see **`handoffs/releases/S0112-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** -- deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** -> **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0** OPEN stories remaining

## Release finalized note (S0111)

- Sprint: `S0111`
- Story: `US-0111` (Release Trigger-Driven Version Changelog Derivation — DEC-0111)
- Release: **finalized** (`2026-06-30T19:45:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0111-US0111-auto-20260628-04-20260630T194500Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0111`** = **`released`**
- **Run / verify:** `pytest tests/us0111_contract_test.py -v` -> 12 passed; `python scripts/release_trigger_adapters.py --self-test` -> `[RELEASE_TRIGGER_SELF_TEST_OK]`; see **`handoffs/releases/S0111-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** -- deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** -> **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **1** OPEN story remaining (US-0112)

## Release finalized note (S0109)

## Release finalized note (S0109)

- Sprint: `S0109`
- Story: `US-0109` (Self-Healing Deploy Loop -- DEC-0109)
- Release: **finalized** (`2026-06-30T03:00:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0109-US0109-auto-20260628-04-20260630T030000Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0109`** = **`released`**
- **Run / verify:** `pytest tests/us0109_contract_test.py -v` -> 11 passed; `python scripts/self_healing_deploy_validate.py --self-test` -> `[SELF_HEALING_DEPLOY_VALIDATION_OK]`; see **`handoffs/releases/S0109-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** -- deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** -> **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **2** OPEN stories remaining (US-0111, US-0112)

## Release finalized note (S0108)

- Sprint: `S0108`
- Story: `US-0108` (Parallel Instance Arbitrage for dev phase — DEC-0108)
- Release: **finalized** (`2026-06-29T23:00:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0108-US0108-auto-20260628-04-20260629T230000Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0108`** = **`released`**
- **Run / verify:** `pytest tests/us0108_contract_test.py -v` → 9 passed; see **`sprints/S0108/release-notes.md`** **## Summary**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout

## Release finalized note (S0106)

- Sprint: `S0106`
- Story: `US-0106` (Sovereign Role-Behavior Manifest — DEC-0106)
- Release: **finalized** (`2026-06-29T01:35:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0106-US0106-auto-20260628-04-20260629T013500Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0106`** = **`released`**
- **Run / verify:** `pytest tests/us0106_contract_test.py -v` → 8 passed; `python scripts/sovereign_role_manifest_validate.py --self-test` → `[SOVEREIGN_ROLE_MANIFEST_SELF_TEST_OK]`; see **`handoffs/releases/S0106-release-notes.md`** **## Summary**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio OPEN stories remain

## Release finalized note (S0105)

- Sprint: `S0105`
- Story: `US-0105` (Sovereign Memory — DEC-0105)
- Release: **finalized** (`2026-06-29T00:13:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0105-US0105-auto-20260628-04-20260629T001300Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0105`** = **`released`**
- **Run / verify:** `pytest tests/us0105_contract_test.py -v` → 10 passed; see **`handoffs/releases/S0105-release-notes.md`** **## Summary**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio OPEN stories remain

## Release finalized note (S0104)

- Sprint: `S0104`
- Story: `US-0104` (Cross-Model Adversarial Critic — DEC-0104)
- Release: **finalized** (`2026-06-29T00:03:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0104-US0104-auto-20260628-04-20260629T000300Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0104`** = **`released`**
- **Run / verify:** `pytest tests/us0104_contract_test.py -v` → 10 passed; `python scripts/sovereign_critic_validate.py --self-test` → `[SOVEREIGN_CRITIC_SELF_TEST_OK]`; see **`handoffs/releases/S0104-release-notes.md`** **## Summary**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio OPEN stories remain

## Release finalized note (S0103)

- Sprint: `S0103`
- Story: `US-0103` (AI Decision Ledger + Plan Fidelity policy — DEC-0103)
- Release: **finalized** (`2026-06-28T15:00:00+02:00`, `orchestrator_run_id=auto-20260628-03`, `fresh_context_marker=release-S0103-US0103-auto-20260628-03-20260628T150000Z`)
- Queue: **`handoffs/release_queue.md`** row **`S0103`** = **`released`**
- **Run / verify:** `pytest tests/us0103_contract_test.py -v` → 8 passed; `python scripts/ledger_validate.py --self-test` → `[LEDGER_SELF_TEST_OK]`; see **`handoffs/releases/S0103-release-notes.md`** **## Summary**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio OPEN stories remain

## Release finalized note (S0107)

- Sprint: `S0107`
- Story: `US-0107` (Sovereign Loop Mode / AUTO_SOVEREIGN — DEC-0107)
- Release: **finalized** (`2026-06-29T00:23:00Z`, `orchestrator_run_id=auto-20260628-04`, `fresh_context_marker=release-S0107-20260629T002300Z-fresh`)
- Queue: **`handoffs/release_queue.md`** row **`S0107`** = **`released`**
- **Run / verify:** `pytest tests/us0109_contract_test.py -v` → 10 passed; `python scripts/sovereign_loop_lib.py --self-test` → `[SOVEREIGN_LOOP_SELF_TEST_OK]`; see **`handoffs/releases/S0107-release-notes.md`** **## Run** / **## Verify**
- Changelog: step **19** appended **US-0107** under **`CHANGELOG.md`** **`[Unreleased]`** (workflow-only; no semver)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **5** OPEN stories remaining (US-0106, US-0108, US-0109, US-0111, US-0112)

## Release finalized note (S0092)

- Sprint: `S0092`
- Story: `US-0102` (direct per-phase model slug override + role-based catalog presets — DEC-0087 / composes DEC-0086)
- Release: **finalized** (`2026-06-26T00:00:00Z`, `orchestrator_run_id=auto-20260615-02`, strict proof `proof_hash=18d3bed52733e0325eac9068b5aa61f07a97153791217d1e23e4e62663e0b858`)
- Queue: **`handoffs/release_queue.md`** row **`S0092`** = **`released`**
- **Run / verify:** `pytest -k us0102 tests/auto_command_contract_test.py -v` → 8 passed; `python scripts/model_tier_validate.py --repo .` → `[MODEL_TIER_VALIDATION_OK]`; see **`handoffs/releases/S0092-release-notes.md`** **## Run** / **## Verify**
- Changelog: step **19** appended **US-0102** under **`CHANGELOG.md`** **`[Unreleased]`** (workflow-only; no semver)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **4** remaining

## Release finalized note (S0090)

- Sprint: `S0090`
- Story: `US-0100` (version-scoped release changelog + GitHub `-F` attachment — DEC-0085 / R-0087)
- Release: **finalized** (`2026-06-15T08:00:00Z`, `orchestrator_run_id=auto-20260615-01`, strict proof `proof_hash=92e55de82e4089435f4a6b3229e3233bbc2a4c4fd4aca5675313b8d7638d1d85`)
- Queue: **`handoffs/release_queue.md`** row **`S0090`** = **`released`**
- **Run / verify:** `pytest -k us0100 tests/auto_command_contract_test.py -v` → 10 passed; `python scripts/release_changelog_validate.py --repo .` → exit 0 warn (enforce notes legacy semver rows pending backfill); see **`handoffs/releases/S0090-release-notes.md`** **## Run** / **## Verify**
- Changelog: step **19** appended **US-0100** under **`CHANGELOG.md`** **`[Unreleased]`** (workflow-only; no semver)
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **6** remaining

## Release finalized note (S0089)

- Sprint: `S0089`
- Story: `US-0099` (auto-bootstrap dev-environment profile on install/upgrade — DEC-0084 amended § bootstrap posture / R-0086)
- Release: **finalized** (`2026-06-14T23:30:00Z`, `orchestrator_run_id=auto-20260614-01`, strict proof `proof_hash=907a95ae387d71891aa3d7c86a9c39a164451f3a75966567d61344a3fba22cda`)
- Queue: **`handoffs/release_queue.md`** row **`S0089`** = **`released`**
- **Run / verify:** `pytest -k us0099 tests/auto_command_contract_test.py -v` → 7 passed; `python scripts/dev_environment_lib.py --self-test` → `[DEV_ENVIRONMENT_SELF_TEST_OK]`; see **`handoffs/releases/S0089-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **7** remaining

## Release finalized note (S0088)

- Sprint: `S0088`
- Story: `US-0098` (dev environment auto-launch profile — DEC-0084 / R-0085)
- Release: **finalized** (`2026-06-14T12:30:00Z`, `orchestrator_run_id=auto-20260613-01`, strict proof `proof_hash=be1986208496cb2ac1947b34f1b4cea458851f39c88146eb04ba85c8fd009dd5`)
- Queue: **`handoffs/release_queue.md`** row **`S0088`** = **`released`**
- **Run / verify:** `pytest -k us0098 tests/auto_command_contract_test.py -v` → 8 passed; `python scripts/dev_environment_lib.py --self-test` → `[DEV_ENVIRONMENT_SELF_TEST_OK]`; see **`handoffs/releases/S0088-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **8** remaining

## Release finalized note (S0087)

- Sprint: `S0087`
- Story: `US-0097` (project-owned root README bootstrap — DEC-0083 / R-0084)
- Release: **finalized** (`2026-06-14T04:30:00Z`, `orchestrator_run_id=auto-20260613-01`, strict proof `proof_hash=008ad6a2f2d8c6dd7b1ee5c32145936445e9a33627ed3ed90dc545cc5d468530`)
- Queue: **`handoffs/release_queue.md`** row **`S0087`** = **`released`**
- **Run / verify:** `pytest -k us0097 tests/auto_command_contract_test.py -v` → 8 passed; `python scripts/validate_project_readme_coverage.py --self-test` → `[PROJECT_README_COVERAGE_SELF_TEST_OK]`; see **`handoffs/releases/S0087-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — deterministic no-op (`publish_snapshot=skipped_disabled`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio next OPEN **US-0098**; backlog drain budget **9** remaining

## Release finalized note (S0086)

- Sprint: `S0086`
- Story: `US-0096` (delivery modes: ultra-lean + mega-quick — DEC-0082 / R-0082)
- Release: **finalized** (`2026-06-13T16:00:00Z`, `orchestrator_run_id=auto-20260612-01`, strict proof `proof_hash=20f59d2ac3731ab4dfdf67925e5b630bf208dc4c20c84892702b537619dc30b1`)
- Queue: **`handoffs/release_queue.md`** row **`S0086`** = **`released`**
- **Run / verify:** `pytest -k "us0096 or us0095 or bug0012" tests/auto_command_contract_test.py -v` → 20 passed; `python scripts/check_intake_template_parity.py --scope=us-0096` → `[INTAKE_TEMPLATE_PARITY_OK]`; see **`handoffs/releases/S0086-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **8** remaining

## Release finalized note (S0085)

- Sprint: `S0085`
- Bug: `BUG-0012` (native-chain drain-advance enforcement — DEC-0081 / R-0083)
- Release: **finalized** (`2026-06-13T01:30:00Z`, `orchestrator_run_id=auto-20260612-01`, strict proof `proof_hash=44b55cf523c1c6721f1b9e359e683a9216379d5b314f401b0a722f667f51afe2`)
- Queue: **`handoffs/release_queue.md`** row **`S0085`** = **`released`**
- **Run / verify:** `pytest -k "bug0012 or us0095" tests/auto_command_contract_test.py -v` → 12 passed; `python scripts/check_intake_template_parity.py --scope=bug-0012` → `[INTAKE_TEMPLATE_PARITY_OK]`; see **`handoffs/releases/S0085-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`SYNC_POLICY_MODE=disabled`** → **`push_decision=not_eligible`**, **`reason_code=SYNC_DISABLED`**
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty**; portfolio next OPEN **US-0096**

## Release finalized note (S0084)

- Sprint: `S0084`
- Story: `US-0095` (Native in-Cursor `/auto` auto-chaining — DEC-0080 / R-0081)
- Release: **finalized** (`2026-06-07T23:30:00Z`, `orchestrator_run_id=auto-20260607-02`, strict proof `proof_hash=423dead28ffb878335ae77568a29c357fffc185859bf3d2fb98dd23f4fe3202d`)
- Queue: **`handoffs/release_queue.md`** row **`S0084`** = **`released`**
- **Run / verify:** `pytest -k us0095 tests/auto_command_contract_test.py -v` → 7 passed; `python scripts/check_intake_template_parity.py --scope=us-0095` → `[INTAKE_TEMPLATE_PARITY_OK]`; see **`handoffs/releases/S0084-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **9** remaining

## Release finalized note (S0083)

- Sprint: `S0083`
- Story: `US-0094` (README visionary intro + tiered feature hierarchy — R-0080)
- Release: **finalized** (`2026-06-07T16:30:00Z`, `orchestrator_run_id=auto-20260607-01`, strict proof `proof_hash=1a245b9025a2d1acf19f5993e4ac7febfb8abc5c1bd75ad88a18e296c7c4dd00`)
- Queue: **`handoffs/release_queue.md`** row **`S0083`** = **`released`**
- **Run / verify:** `python scripts/validate_readme_feature_coverage.py --repo . --enforce` → `[README_FEATURE_COVERAGE_VALIDATE_OK]`; `coverage_missing=[]`, `coverage_total=104`; see **`handoffs/releases/S0083-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories

## Release finalized note (S0082)

- Sprint: `S0082`
- Story: `US-0093` (Cursor browser-integrated UAT self-test — DEC-0079)
- Release: **finalized** (`2026-06-07T01:30:00Z`, `orchestrator_run_id=auto-20260606-04`, strict proof `proof_hash=57e939f5220447bd9a4697146f6a78fb5fbe6d92005eeafcd354e34c8d7c8ab0`)
- Queue: **`handoffs/release_queue.md`** row **`S0082`** = **`released`**
- **Run / verify:** `pytest -k us0093` → 6 passed; `python scripts/uat_probe_lib.py --self-test` → `[UAT_PROBE_LIB_SELF_TEST_OK]`; see **`handoffs/releases/S0082-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **1** remaining

## Release finalized note (S0081)

- Sprint: `S0081`
- Story: `US-0092` (Full-autonomy `/auto` mode + outer driver + self-verification — DEC-0078)
- Release: **finalized** (`2026-06-06T22:30:00Z`, `orchestrator_run_id=auto-20260606-03`, strict proof `proof_hash=c090713e2791b75a697db7e09c9a874a257e3d79b742436837b6d84d2d1d0c78`)
- Queue: **`handoffs/release_queue.md`** row **`S0081`** = **`released`**
- **Run / verify:** `pytest -k us0092` → 9 passed; `python scripts/auto_outer_driver.py --self-test` → `[AUTO_OUTER_DRIVER_SELF_TEST_OK]`; `python scripts/uat_probe_lib.py --self-test` → `[UAT_PROBE_LIB_SELF_TEST_OK]`; see **`handoffs/releases/S0081-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; portfolio **0 OPEN** stories; backlog drain budget **2** remaining

## Release finalized note (S0080)

- Sprint: `S0080`
- Bug: `BUG-0011` (Caveman voice compression rules — DEC-0077)
- Release: **finalized** (`2026-06-06T17:00:00Z`, `orchestrator_run_id=auto-20260606-02`, strict proof `proof_hash=06b929b4b97c50dfb4012154443764c17e2958c409d4df9d0b16dda5b39825fc`)
- Queue: **`handoffs/release_queue.md`** row **`S0080`** = **`released`**
- **Run / verify:** `pytest -k caveman_voice` → 9 passed; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`** (808/14); see **`handoffs/releases/S0080-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout; bug queue **empty**

## Release finalized note (S0079)

- Sprint: `S0079`
- Bug: `BUG-0010` (triad archiver dual-level heading fix — DEC-0076)
- Release: **finalized** (`2026-06-06T16:36:00Z`, `orchestrator_run_id=auto-20260606-02`, strict proof `proof_hash=185901a6d7b195ae6ab54f9221953ba4311a955d70d62b76c69ca1c351ac4b14`)
- Queue: **`handoffs/release_queue.md`** row **`S0079`** = **`released`**
- **Run / verify:** `python scripts/enforce-triad-hot-surface.py --self-test` → exit 0; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0079-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** for **`BUG-0011`** (bug queue remaining = 1)

## Release finalized note (S0078)

- Sprint: `S0078`
- Bug: `BUG-0009` (downstream CI packaging job leak — DEC-0075)
- Release: **finalized** (`2026-06-06T16:15:00Z`, `orchestrator_run_id=auto-20260606-02`, strict proof `proof_hash=ca36057ca8aff89ceee48d2474bf84c5533f777c9f9cd194a1c18ef8425484bc`)
- Queue: **`handoffs/release_queue.md`** row **`S0078`** = **`released`**
- **Run / verify:** `python scripts/check_downstream_ci_guard.py --repo . --report` → `ok=true`; `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0078-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (14 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** for **`BUG-0010`** (bug queue remaining = 2)

## Release finalized note (S0077)

- Sprint: `S0077`
- Story: `US-0091` (README feature coverage backfill + blocking drift gate — DEC-0074)
- Release: **finalized** (`2026-06-06T13:43:20Z`, `orchestrator_run_id=auto-20260606-01`, strict proof `proof_hash=cbfc031254b549dfef27f12c4a6d5acb51b528835180b60252e54b44d238bd47`)
- Queue: **`handoffs/release_queue.md`** row **`S0077`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; `python scripts/validate_readme_feature_coverage.py --repo . --enforce` -> **`[README_FEATURE_COVERAGE_VALIDATE_OK]`**; see **`handoffs/releases/S0077-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (9 pre-existing disjoint harness failures)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (backlog drain budget remaining = 3; OPEN bugs `BUG-0009..BUG-0011` on bug queue)

## Release finalized note (S0076)

- Sprint: `S0076`
- Story: `US-0090` (Caveman input compression — operator-gated, sidecar-first, default-off CLI + installer surface; DEC-0073)
- Release: **finalized** (`2026-04-19T00:05:00Z`, `orchestrator_run_id=auto-20260418-01`, strict proof `proof_hash=0126c54efd3cc8158d9d0a687a66e9bce8f4eeefb89522993bb5ce805bb87e40`)
- Queue: **`handoffs/release_queue.md`** row **`S0076`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; see **`handoffs/releases/S0076-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (9 pre-existing disjoint failures block push gate even though release-gate classification tolerates them)
- Carried-forward non-blocking observations: (1) `PARTIAL_VERBATIM` on DEC-0073 §1 publication (architecture verbatim; reference + runbook paraphrase; DEC-0072 §6 row 6 pinned test preserved byte-unchanged); (2) UAT-3 `--dry-run` vs `--write` narration variance (AC-4 fail-closed intent satisfied via `--write` evidence).
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain; budget remaining = 4)

## Release finalized note (S0075)

- Sprint: `S0075`
- Story: `US-0089` (Cursor Caveman mode — scratchpad-configurable terse responses)
- Release: **finalized** (`2026-04-18T19:00:00Z`, `orchestrator_run_id=auto-20260418-01`, strict proof `proof_hash=2f7351477332235595f379aae04d3830a0efc33f9a9cef887822999bcc9839b3`)
- Queue: **`handoffs/release_queue.md`** row **`S0075`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; see **`handoffs/releases/S0075-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation (`publish_snapshot=skipped_pending_operator_confirm`)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=1`**, **branch=main**, **`push_decision=blocked`**, **`reason_code=TEST_FAILED`** (11 pre-existing disjoint failures block push gate even though release-gate classification tolerates them)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0074)

- Sprint: `S0074`
- Story: `US-0086` (automation-driven remote execution selection)
- Release: **finalized** (`2026-04-13T22:30:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=3bc64c2345bb8861075d957ae665280da80f41d0ce21ba4caa6e55e865b96153`)
- Queue: **`handoffs/release_queue.md`** row **`S0074`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` -> **`tests/report.md`**; see **`handoffs/releases/S0074-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** - **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** -> **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0073)

- Sprint: `S0073`
- Story: `US-0085` (Gitignored `.env` for remote and release connectivity — no AI read)
- Release: **finalized** (`2026-04-13T17:00:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=201375708766b544b12a336534d09e5a8c69369bf18e10c8ea8ac76717dcfb75`)
- Queue: **`handoffs/release_queue.md`** row **`S0073`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0073-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0072)

- Sprint: `S0072`
- Story: `US-0088` (`/auto` continuous multi-phase loop + quiet backlog drain)
- Release: **finalized** (`2026-04-13T01:15:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=a1c18a2b7e8a8f83687ca47ad29c0764b0a5867e4098e8e1c1a20314ffe68bbd`)
- Queue: **`handoffs/release_queue.md`** row **`S0072`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0072-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (next OPEN story per backlog drain)

## Release finalized note (S0071)

- Sprint: `S0071`
- Story: `US-0087` (**`/auto`** explicit bug targeting / bug-queue mode)
- Release: **finalized** (`2026-04-12T19:05:00Z`, `orchestrator_run_id=auto-20260405-01`, strict proof `proof_hash=b453b8901b083fb927dc73cfea54655f4e4ea1a703c4f1ea3e5cb420e6c4b215`)
- Queue: **`handoffs/release_queue.md`** row **`S0071`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0071-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=confirm`** — **no** automated publish without explicit operator confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context) for segment closeout, then **`/auto`** / portfolio (**US-0088** intake already in **`resume_brief`**)

## Release finalized note (S0070)

- Sprint: `S0070`
- Bug: `BUG-0008` (CRLF **`installer-owned-paths.manifest`** / **`R-0069`**)
- Release: **finalized** (`2026-04-05T22:30:00Z`, `orchestrator_run_id=auto-20260404-03`, strict proof `proof_hash=29228ef7c322aa74d21b8a354adf4c45bbb8d4c64c967ee9dd3d58f7e9b2bf02`)
- Queue: **`handoffs/release_queue.md`** row **`S0070`** = **`released`**
- **Run / verify:** `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` → **`tests/report.md`**; see **`handoffs/releases/S0070-release-notes.md`** **## Run** / **## Verify**
- Publish: **`RELEASE_PUBLISH_MODE=disabled`** — **no** **`npm publish`** this boundary (deterministic no-op)
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (unless scratchpad overrides)
- **Next**: **`/refresh-context`** (fresh **curator** context)

## Release finalized note (S0069)

- Sprint: `S0069`
- Story: `US-0084` (POSIX npm installer + Linux remote test targets; **US-0064** alignment; **DEC-0070** remote-config helper skip policy)
- Release: **finalized** (`2026-04-05T00:10:00Z`, `orchestrator_run_id=auto-20260404-02`, strict proof `proof_hash=418cbee2c8f7508880e1cbcae744d67877c08e68c91432b3de38f0e1773b07fc`)
- Queue: **`handoffs/release_queue.md`** row **`S0069`** = **`released`**
- Publish posture: **`RELEASE_PUBLISH_MODE=confirm`** — no auto-publish without confirmation
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (no auto-push this boundary)
- **Next**: **`/refresh-context`** (fresh **curator** context)

## Release finalized note (S0068) (historical)

- Sprint: `S0068`
- Bug: `BUG-0007` (**R-0066** / **`INTAKE_ANSWER_REF_NOT_TOPIC_DISTINCT`**)
- Release: **finalized** (`2026-04-05T00:10:00Z`, `orchestrator_run_id=auto-20260404-01`, strict proof `proof_hash=6c824be4c8dfb3ecb25de8e8ca90910789436a2c916489fb15a935baf3c64202`)
- Queue: **`handoffs/release_queue.md`** row **`S0068`** = **`released`**
- Sync (**DEC-0018**): **`ALLOW_AUTO_PUSH=0`** → **`push_decision=not_eligible`**, **`reason_code=MANUAL_MODE_NO_AUTO`** (no auto-push this boundary)
- Portfolio: **`docs/product/backlog.md`** — canonical **bug** rows **BUG-0001..BUG-0007** all **DONE**; **next OPEN bug:** **(none)**
- **Next**: **`/refresh-context`** (fresh **curator** context) — **superseded** by **S0069** pointer above

## Release readiness note (S0068) (historical)

- Pre-release verify-work **PASS** (`2026-04-04T23:45:00Z`); superseded by **Release finalized note (S0068)** above.

## Release readiness note (S0067)

- Sprint: `S0067`
- Bug: `BUG-0006` (**spawn-only `/auto`**, **`AUTO_ORCHESTRATOR_PHASE_EXECUTION`**, **R-0065**)
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0067-release-notes.md` (`2026-04-04T09:00:00Z`, `orchestrator_run_id=auto-20260403-03`); **`/refresh-context`** **complete** — successor track **`S0068`** / **`BUG-0007`** **released** (`2026-04-05`).

## Release readiness note (S0066)

- Sprint: `S0066`
- Bug: `BUG-0005` (**DEC-0069**)
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0066-release-notes.md`; **`/refresh-context`** **complete** (`auto-20260403-02`, **`2026-04-03T23:55:00Z`**) — superseded by **`S0067`** closure track; portfolio now advances via **`BUG-0007`** after **`S0067`** **`/refresh-context`**.

## Release readiness note (S0065)

- Sprint: `S0065`
- Bug: `BUG-0004`
- Release: **finalized** - queue row **`released`**; canonical notes `handoffs/releases/S0065-release-notes.md`; next **`/refresh-context`** completed.

## Release readiness note (S0064)

- Sprint: `S0064`
- Story: `US-0083`
- Release: **finalized** - queue row **`released`**; canonical notes `handoffs/releases/S0064-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0063)

- Sprint: `S0063`
- Bug: `BUG-0003`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0063-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0062)

- Sprint: `S0062`
- Story: `US-0082`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0062-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0061)

- Sprint: `S0061`
- Story: `US-0081`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0061-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0060)

- Sprint: `S0060`
- Bug: `BUG-0001`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0060-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0059)

- Sprint: `S0059`
- Story: `US-0080`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0059-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0058)

- Sprint: `S0058`
- Story: `US-0079`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0058-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Unreleased queue visibility

Check `handoffs/release_queue.md` for all pending entries where `status=unreleased`
or `status=blocked` before finalization.

- **No `unreleased` or `blocked` entries** for S0121 as of `2026-08-24T10:58:00Z` — S0121 transitioned to `released` (3rd release attempt PASS). See `## Release finalized note (S0121)` above.

## Release readiness note (S0057)

- Sprint: `S0057`
- Story: `US-0078`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0057-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0056)

- Sprint: `S0056`
- Story: `US-0077`
- Release: **finalized** — queue row **`released`**; canonical notes `handoffs/releases/S0056-release-notes.md`; next **`/refresh-context`** (see `docs/engineering/state.md`).

## Release readiness note (S0055)

- Sprint: `S0055`
- Story: `US-0076`
- Verify-work: PASS
- UAT status: PASS (`10/10`, `0` failed)
- QA findings: PASS with no in-scope blockers (`sprints/S0055/qa-findings.md`)
- Release readiness: Finalized as `released` in `handoffs/release_queue.md`
  with canonical sprint-scoped notes.

## Latest operator summary (Run/Connect/Verify)

- **Start command:** Latest sprint **`S0129`** (RELEASED — finalized 1st attempt, `2026-08-27T08:42:00Z`): kit/scripts story — guarded triad rollover via `python scripts/arch_linkage_guard.py --pre --repo .` then `enforce-triad-hot-surface.py --rollover`; see `## Run` in `handoffs/releases/S0129-release-notes.md`.
- **Endpoint + port:** N/A (kit/scripts story — no service endpoint) — see `## Connect` in `handoffs/releases/S0129-release-notes.md`.
- **Verification steps + health signal:** See `## Verify` in `handoffs/releases/S0129-release-notes.md` (health = 8/8 contract markers + arch-linkage parity + harness Fail:0).
- **Credentials source refs (sanitized):** See `## Credentials` in `handoffs/releases/S0129-release-notes.md` (n/a — `ARCH_LINKAGE_AUTO_REPAIR` in operator scratchpad only).
- **Known issues:** See `## Known Issues` in `handoffs/releases/S0129-release-notes.md` (no blocking issues; NB-1 superseded by harness re-run).

## Historical references

- `S0075`: `handoffs/releases/S0075-release-notes.md`
- `S0074`: `handoffs/releases/S0074-release-notes.md`
- `S0073`: `handoffs/releases/S0073-release-notes.md`
- `S0072`: `handoffs/releases/S0072-release-notes.md`
- `S0071`: `handoffs/releases/S0071-release-notes.md`
- `S0070`: `handoffs/releases/S0070-release-notes.md`
- `S0069`: `handoffs/releases/S0069-release-notes.md`
- `S0068`: `handoffs/releases/S0068-release-notes.md`
- `S0067`: `handoffs/releases/S0067-release-notes.md`
- `S0066`: `handoffs/releases/S0066-release-notes.md`
- `S0065`: `handoffs/releases/S0065-release-notes.md`
- `S0064`: `handoffs/releases/S0064-release-notes.md`
- `S0063`: `handoffs/releases/S0063-release-notes.md`
- `S0062`: `handoffs/releases/S0062-release-notes.md`
- `S0061`: `handoffs/releases/S0061-release-notes.md`
- `S0060`: `handoffs/releases/S0060-release-notes.md`
- `S0059`: `handoffs/releases/S0059-release-notes.md`
- `S0058`: `handoffs/releases/S0058-release-notes.md`
- `S0057`: `handoffs/releases/S0057-release-notes.md`
- `S0056`: `handoffs/releases/S0056-release-notes.md`
- `S0055`: `handoffs/releases/S0055-release-notes.md`
- `S0054`: `handoffs/releases/S0054-release-notes.md`
- `S0053`: `handoffs/releases/S0053-release-notes.md`
- `S0052`: `handoffs/releases/S0052-release-notes.md`
- `S0051`: `handoffs/releases/S0051-release-notes.md`
- `S0050`: `handoffs/releases/S0050-release-notes.md`
- `S0049`: `handoffs/releases/S0049-release-notes.md`
- `S0048`: `handoffs/releases/S0048-release-notes.md`
- `S0047`: `handoffs/releases/S0047-release-notes.md`
- `S0046`: `handoffs/releases/S0046-release-notes.md`
- `S0045`: `handoffs/releases/S0045-release-notes.md`
- `S0044`: `handoffs/releases/S0044-release-notes.md`
- `S0043`: `handoffs/releases/S0043-release-notes.md`
- `S0042`: `handoffs/releases/S0042-release-notes.md`
- `S0041`: `handoffs/releases/S0041-release-notes.md`
- `S0040`: `handoffs/releases/S0040-release-notes.md`
- `S0039`: `handoffs/releases/S0039-release-notes.md`
- `S0038`: `handoffs/releases/S0038-release-notes.md`
- `S0037`: `handoffs/releases/S0037-release-notes.md`
- `S0036`: `handoffs/releases/S0036-release-notes.md`
- `S0035`: `handoffs/releases/S0035-release-notes.md`
- `S0034`: `handoffs/releases/S0034-release-notes.md`
- `S0033`: `handoffs/releases/S0033-release-notes.md`
- `S0032`: `handoffs/releases/S0032-release-notes.md`
- `S0031`: `handoffs/releases/S0031-release-notes.md`
- `S0030`: `handoffs/releases/S0030-release-notes.md`
- `S0029`: `handoffs/releases/S0029-release-notes.md`
- `S0011`: `handoffs/releases/S0011-release-notes.md`
- `S0025`: `handoffs/releases/S0025-release-notes.md`
- `S0026`: `handoffs/releases/S0026-release-notes.md`
- `S0027`: `handoffs/releases/S0027-release-notes.md`
- `S0028`: `handoffs/releases/S0028-release-notes.md`
- `S0024`: `handoffs/releases/S0024-release-notes.md`
- `S0023`: `handoffs/releases/S0023-release-notes.md`
- `S0022`: `handoffs/releases/S0022-release-notes.md`
- `S0021`: `handoffs/releases/S0021-release-notes.md`
- `S0020`: `handoffs/releases/S0020-release-notes.md`
- `S0019`: `handoffs/releases/S0019-release-notes.md`
- `S0018`: `handoffs/releases/S0018-release-notes.md`
- `S0017`: `handoffs/releases/S0017-release-notes.md`
- `S0016`: `handoffs/releases/S0016-release-notes.md`
- `S0015`: `handoffs/releases/S0015-release-notes.md`
- `S0013`: `handoffs/releases/S0013-release-notes.md`
- `S0012`: `handoffs/releases/S0012-release-notes.md`
- `S0010`: `handoffs/releases/S0010-release-notes.md`

---

## Per-gate audit verdict (US-0039)

When `/release` runs, each gate (check-in test, QA, UAT, finalization) is recorded with:
- **verdict**: pass | fail | override
- **reason_code**: e.g. RELEASE_TEST_FAILED, RELEASE_QA_BLOCKERS_OPEN, RELEASE_UAT_INCOMPLETE, RELEASE_GATE_OVERRIDE_APPROVED
- **remediation**: short steps when not pass
- **evidence_refs**: paths to tests/report.md, qa-findings.md, uat.json, release-findings.md, DEC-xxxx

Canonical per-run gate snapshot lives in `sprints/Sxxxx/release-findings.md` and queue row `gate_snapshot`; TL/QA audit from those artifacts and `docs/engineering/state.md` checkpoints.

**Override path (US-0039)**: When a gate is overridden, record decision record ref (DEC-xxxx), rationale, approver, and risk acceptance in release-findings and gate_snapshot; use reason code `RELEASE_GATE_OVERRIDE_APPROVED`.

## Compatibility behavior contract

- Keep this file as a pointer/summary; do not treat it as canonical historical
  storage.
- `/release` must update sprint-scoped notes first, then refresh this pointer.
- Never delete or destructively rewrite historical sprint-scoped note files
  through this legacy path.
