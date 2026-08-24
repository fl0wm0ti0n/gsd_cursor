# QA Findings - US-0123 / S0123 (loop-2 after harness-refresh)

- **phase_id**: qa
- **role**: qa (fresh per BUG-0006; loop-2 after harness-refresh execute)
- **story_id**: US-0123
- **sprint_id**: S0123
- **orchestrator_run_id**: auto-20260824-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **fresh_context_marker**: qa-US0123-qa-20260824T151700Z-fresh-loop2
- **timestamp (UTC)**: 2026-08-24T15:17:00Z
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 - required on isolation)
- **producer_model_id**: composer-2.5 (dev / execute harness-refresh)
- **producer_runtime_proof_id**: rp-auto-20260824-01-execute-harness-refresh-dev-20260824T151230Z-US-0123
- **producer_proof_hash**: 029BE6F670D2B17AD7B86D297EE68B09392A649B540FE2FEE2A2BA7E68B54979
- **producer_proof_ttl**: 2026-08-24T16:12:30Z (consumed before expiry - OK)
- **verdict**: **PASS** (8/8 contract tests independent re-run; opencode-adapter parity; opencode-catalog validator; compose 6/6 UNCHANGED; byte-identical mirrors; ACs 10/10 covered; tests/report.md @ 2026-08-24T15:12:17Z Pass:845 Fail:0 literal; zero [FAIL]; no fake browser PASS)
- **story_status**: OPEN (not marked DONE - US-0045; closure owns the flip)
- **blocking_findings**: 0
- **non_blocking_findings**: 1 (carry-forward `ik_us0123_installer_hook_not_contract_tested` - installer `--host` hook not pytest-marked; T-003 hook covered by installer parity + manual spot-check, not a contract marker gap)
- **acceptance_row_unchecked**: true (`docs/product/acceptance.md` L151 - `- [ ] US-0123`; read-only)
- **next_scheduled_phase**: /verify-work (fresh qa subagent per BUG-0006)
- **stop_condition**: STOP after /qa loop-2. Hand off via artifacts only to /verify-work.

## Independent checks (loop-2)

| # | Check | Command | Result |
|---|-------|---------|--------|
| 1 | Contract tests (8 markers) | `python -m pytest tests/us0123_contract_test.py -v` | **8/8 PASS** (0.21s, exit 0) |
| 2 | OpenCode adapter parity | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | **PASS** (`[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`) |
| 3 | OpenCode catalog validator | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | **PASS** (`[MODEL_TIER_VALIDATION_OK]`) |
| 4 | Template agents omit `model:` | `rg "^model:" template/.opencode/agents` | **0 matches** |
| 5 | tests/report.md timestamp >= 2026-08-24T15:12:17Z | read L3 | **PASS** - `Timestamp: 2026-08-24T15:12:17Z` (equals harness-refresh threshold) |
| 6 | tests/report.md literal `Fail: 0` | read L5 | **PASS** - `Fail: 0` |
| 7 | tests/report.md zero `[FAIL]` rows | `rg "\[FAIL\]" tests/report.md` | **0 matches** |
| 8 | tests/report.md `Pass: 845` | read L4 | **PASS** - `Pass: 845` |
| 9 | Runbook byte-identical active+template | SHA-256 compare `docs/engineering/runbook.md` vs `template/...` | **PASS** - `66ee024a...` equal |
| 10 | Manifest byte-identical active+template | SHA-256 compare `docs/engineering/context/installer-owned-paths.manifest` vs `template/...` | **PASS** - `f7c1c09c...` equal |
| 11 | Compose guards 6/6 UNCHANGED | read backlog L4248, acceptance L151, architecture L1382, DEC-0123 L3, template agents, mirrors | **PASS** - backlog `Status: OPEN`; acceptance `- [ ]`; arch `US-0123` anchor present; DEC-0123 `Accepted`; template agents no `model:`; mirrors byte-identical |
| 12 | No fake browser PASS | `sprints/S0123/uat.json` `browser_probe_used=false` | **PASS** - pack/contract story; no browser_smoke classified |

## Contract test markers (independent re-run, loop-2)

`python -m pytest tests/us0123_contract_test.py -v` -> **8 passed in 0.21s** (exit 0)

| # | Marker | AC | Result |
|---|--------|----|--------|
| 1 | `test_us0123_template_agents_omit_model` | AC-1, AC-3 | PASS |
| 2 | `test_us0123_no_vendor_slugs_in_template` | AC-3 | PASS |
| 3 | `test_us0123_example_catalog_placeholders_only` | AC-2, AC-3 | PASS |
| 4 | `test_us0123_example_catalog_per_role_divergence` | AC-7, AC-9 | PASS |
| 5 | `test_us0123_fail_closed_unknown_slug` | AC-4 | PASS |
| 6 | `test_us0123_materializer_no_op_when_catalog_absent` | AC-1, AC-4 | PASS |
| 7 | `test_us0123_auth_store_never_in_template_or_git` | AC-5 | PASS |
| 8 | `test_us0123_compose_cursor_unchanged` | AC-6, AC-8 | PASS |

## AC coverage (10/10)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1 Resolution chain | COVERED | marker 1 + 6 (materializer no-op when absent; template omits model) |
| AC-2 Multi-provider examples | COVERED | marker 3 - 6 providers (deepseek, moonshot, zai, anthropic, openai, dashscope) >= 4 required |
| AC-3 No vendor IDs in template | COVERED | markers 1, 2, 3 + grep `^model:` 0 matches |
| AC-4 Unknown slug fail-closed | COVERED | markers 5, 6 - `OPENCODE_MODEL_SLUG_UNKNOWN` + no-op when catalog absent |
| AC-5 Auth store | COVERED | marker 7 - auth.json/api_key/sk- never in template or git |
| AC-6 Compose US-0101/US-0102 | COVERED | marker 8 - Cursor alias runtime unchanged; OpenCode additive; TOKEN_PROFILE orthogonal |
| AC-7 Per-role assignment | COVERED | marker 4 - >= 2 roles configurable to different providers |
| AC-8 Contract tests | COVERED | 8/8 PASS; markers cover placeholder-only, fail-closed, schema, non-substitution |
| AC-9 Chinese APIs as capability | COVERED | marker 4 - deepseek/moonshot/zai/dashscope present; kit-operated proxy out of scope |
| AC-10 Tool-calling quality | COVERED | runbook h2 `## OpenCode model slug routing (US-0123)` present + byte-identical mirror |

## Full-harness claim (loop-2) - MADE

`tests/report.md` header: `Timestamp: 2026-08-24T15:12:17Z` / `Pass: 845` / `Fail: 0`. The report timestamp **equals** the harness-refresh execute timestamp (`2026-08-24T15:12:17Z` per `sprints/S0123/progress.md`), satisfying the `>= 2026-08-24T15:12:17Z` threshold. `rg "\[FAIL\]" tests/report.md` -> 0 matches. `rg "\[PASS\]" tests/report.md` -> 845 matches. **Full-harness `Fail: 0` claim is made for US-0123 loop-2** (unlike loop-1 where the report was stale at 13:02:49Z). US-0123 contract evidence rests on: 8/8 independent pytest re-run + parity + validator + byte-identity probes + fresh harness report.

## Compose guards (6/6 UNCHANGED)

| # | Guard | Evidence |
|---|-------|----------|
| 1 | `docs/product/backlog.md` US-0123 | L4248 `Status: OPEN` (not mutated) |
| 2 | `docs/product/acceptance.md` US-0123 | L151 `- [ ] US-0123` (unchecked; not mutated) |
| 3 | `docs/engineering/architecture.md` US-0123 | L1382 `## US-0123 - Per-role OpenCode model slug routing (multi-provider)` (anchor present; not mutated) |
| 4 | `decisions/DEC-0123.md` | L3 `Status: Accepted` (not mutated) |
| 5 | `template/.opencode/agents/*.md` | grep `^model:` -> 0 matches (no `model:` keys in template) |
| 6 | Byte-identical mirrors | runbook + manifest SHA-256 equal active+template |

## UAT probes (DEC-0009 / US-0092 / DEC-0078)

`UAT_BROWSER_PROBE_MODE=cursor` (default). Pack/contract story with no web UI surface. No `browser_smoke` step classified. ACs mapped to pytest markers + static checks as stack-profile probes with evidence (command + output). No `.env` read. No intake evidence mutation. No `UAT_PROBE_FORBIDDEN`. **No fake browser PASS** - `browser_probe_used=false` recorded in `sprints/S0123/uat.json`.

| Probe ID | Kind | Command | Passed | Reason |
|----------|------|---------|--------|--------|
| `us0123-contract-gate` | pytest | `python -m pytest tests/us0123_contract_test.py -v` | true | 8/8 PASS exit 0 |
| `opencode-adapter-parity` | static | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | true | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `opencode-catalog-validator` | static | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | true | `[MODEL_TIER_VALIDATION_OK]` |
| `harness-report-fresh` | static | read `tests/report.md` L3-L5 + `rg [FAIL]` | true | Timestamp 2026-08-24T15:12:17Z >= threshold; Fail:0; zero [FAIL]; Pass:845 |
| `compose-guards-6-unchanged` | static | read backlog/acceptance/architecture/DEC-0123/template agents/mirrors | true | backlog OPEN L4248; acceptance unchecked L151; arch anchor L1382; DEC-0123 Accepted; 0 `^model:`; mirrors byte-identical |
| `byte-identical-mirrors` | static | SHA-256 compare runbook + manifest | true | 2/2 equal |

## Non-blocking findings (carry-forward)

- `ik_us0123_installer_hook_not_contract_tested` (carry-forward): installer `--host opencode|both` hook (`installer.py` L580-586, `installer.ps1` `-InstallHost`, `installer.sh`) is not pytest-marked. Coverage rests on installer parity + manual spot-check. Non-blocking - T-003 hook is integration-level, not a contract-test gap. Recommend future story (e.g. US-0126 runbook parity) add an installer hook contract marker if operator-facing guarantee is desired.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`
- `role=qa`
- `story_id=US-0123`
- `sprint_id=S0123`
- `fresh_context_marker=qa-US0123-qa-20260824T151700Z-fresh-loop2`
- `timestamp=2026-08-24T15:17:00Z` (UTC)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 - required on isolation; **NEW** fresh_context_marker per US-0048 - marker reuse = stale isolation evidence)
- `evidence_ref=sprints/S0123/qa-findings.md, handoffs/qa_to_verify.md, sprints/S0123/uat.json, sprints/S0123/uat.md, docs/engineering/state.md (qa loop-2 checkpoint append-bottom)`
- QA subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward; no subagent spawned from this QA subagent.

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-qa-qa-20260824T151700Z-US-0123-loop2`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"qa","proof_issued_at":"2026-08-24T15:17:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-qa-qa-20260824T151700Z-US-0123-loop2","sprint_id":"S0123","story_id":"US-0123"}`
- `proof_hash=9CC32FD6A0EE8C0EDE3696E060BDBD8A8F19E914BFFBE51719E1A7B79704F107`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T16:17:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

## Stop condition

STOP after /qa loop-2. Hand off via artifacts only to `/verify-work` in fresh qa subagent per BUG-0006. Do not spawn `/verify-work` from this qa subagent. Do not mark US-0123 DONE.

---


# QA Findings â€” US-0123 / S0123

- **phase_id**: qa
- **role**: qa (fresh per BUG-0006)
- **story_id**: US-0123
- **sprint_id**: S0123
- **orchestrator_run_id**: auto-20260824-01
- **delivery_mode**: ultra_lean
- **macro_phase**: build+verify
- **fresh_context_marker**: qa-US0123-qa-20260824T145500Z-fresh
- **timestamp (UTC)**: 2026-08-24T14:55:00Z
- **model_id**: glm-5.2-high (CROSS_MODEL_REVIEW=1 â€” required on isolation)
- **producer_model_id**: composer-2.5 (execute dev)
- **producer_runtime_proof_id**: rp-auto-20260824-01-execute-dev-20260824T144800Z-US-0123
- **producer_proof_hash**: 3579702AE6A0305460FE137BB73B612C12DA88B57F6D8A32D109E7895F07BEB5
- **producer_proof_ttl**: 2026-08-24T15:48:00Z (consumed before expiry â€” OK)
- **verdict**: **PASS** (8/8 contract tests independent re-run; opencode-adapter parity; opencode-catalog validator; compose 6/6 UNCHANGED; byte-identical mirrors; ACs 10/10 covered; UAT probes static-contract mapped; no fake browser PASS)
- **story_status**: OPEN (not marked DONE â€” US-0045; closure owns the flip)
- **blocking_findings**: 0
- **non_blocking_findings**: 1 (carry-forward `ik_us0123_installer_hook_not_contract_tested` â€” installer `--host` hook not pytest-marked; T-003 hook covered by installer parity + manual spot-check, not a contract marker gap)
- **acceptance_row_unchecked**: true (`docs/product/acceptance.md` L151 â€” `- [ ] US-0123`; read-only)
- **next_scheduled_phase**: /verify-work (fresh qa subagent per BUG-0006)
- **stop_condition**: STOP after /qa. Hand off via artifacts only to /verify-work.

## Test plan (runbook-derived)

| # | Check | Command | Result |
|---|-------|---------|--------|
| 1 | Contract tests (8 markers) | `python -m pytest tests/us0123_contract_test.py -v` | **8/8 PASS** (0.20s) |
| 2 | OpenCode adapter parity | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | **PASS** (`[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter`) |
| 3 | OpenCode catalog validator | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | **PASS** (`[MODEL_TIER_VALIDATION_OK]`) |
| 4 | Template agents omit `model:` | `rg "^model:" template/.opencode/agents` | **0 matches** |
| 5 | Example catalog placeholders only | read `template/.opencode/model-catalog.local.example.json` | **PASS** â€” 6 providers, 8 roles, all `<your-*-slug>` placeholders; no live vendor slugs |
| 6 | Runbook h2 present + byte-identical | `rg "OpenCode model slug routing \(US-0123\)" docs/engineering/runbook.md template/docs/engineering/runbook.md` + SHA-256 compare | **PASS** â€” both at L3991; SHA-256 `66ee024a...` equal; len 196778 equal |
| 7 | Manifest byte-identical activeâ†”template | SHA-256 compare `docs/engineering/context/installer-owned-paths.manifest` vs `template/...` | **PASS** â€” `f7c1c09c...` equal |
| 8 | Paired script/test mirrors byte-identical | SHA-256 compare 3 pairs (contract test, parity script, validator) | **PASS** â€” 3/3 equal |
| 9 | Compose guards 6/6 UNCHANGED | read backlog L4248, acceptance L151, architecture L1703, DEC-0123 L4, template agents, mirrors | **PASS** â€” backlog `Status: OPEN`; acceptance `- [ ]`; architecture `# US-0123` anchor present; DEC-0123 `Accepted`; template agents no `model:`; mirrors byte-identical |
| 10 | Installer hook present | `rg InstallHost installer.ps1`, `rg opencode_model_catalog_apply installer.py` | **PASS** â€” `-InstallHost` param present; `opencode_model_catalog_apply.py` referenced L580â€“586 |

## Contract test markers (independent re-run)

`python -m pytest tests/us0123_contract_test.py -v` â†’ **8 passed in 0.20s** (exit 0)

| # | Marker | AC | Result |
|---|--------|----|--------|
| 1 | `test_us0123_template_agents_omit_model` | AC-1, AC-3 | PASS |
| 2 | `test_us0123_no_vendor_slugs_in_template` | AC-3 | PASS |
| 3 | `test_us0123_example_catalog_placeholders_only` | AC-2, AC-3 | PASS |
| 4 | `test_us0123_example_catalog_per_role_divergence` | AC-7, AC-9 | PASS |
| 5 | `test_us0123_fail_closed_unknown_slug` | AC-4 | PASS |
| 6 | `test_us0123_materializer_no_op_when_catalog_absent` | AC-1, AC-4 | PASS |
| 7 | `test_us0123_auth_store_never_in_template_or_git` | AC-5 | PASS |
| 8 | `test_us0123_compose_cursor_unchanged` | AC-6, AC-8 | PASS |

## AC coverage (10/10)

| AC | Status | Evidence |
|----|--------|----------|
| AC-1 Resolution chain | COVERED | marker 1 + 6 (materializer no-op when absent; template omits model) |
| AC-2 Multi-provider examples | COVERED | marker 3 â€” 6 providers (deepseek, moonshot, zai, anthropic, openai, dashscope) â‰¥4 required |
| AC-3 No vendor IDs in template | COVERED | markers 1, 2, 3 + grep `^model:` 0 matches |
| AC-4 Unknown slug fail-closed | COVERED | markers 5, 6 â€” `OPENCODE_MODEL_SLUG_UNKNOWN` + no-op when catalog absent |
| AC-5 Auth store | COVERED | marker 7 â€” auth.json/api_key/sk- never in template or git |
| AC-6 Compose US-0101/US-0102 | COVERED | marker 8 â€” Cursor alias runtime unchanged; OpenCode additive; TOKEN_PROFILE orthogonal |
| AC-7 Per-role assignment | COVERED | marker 4 â€” â‰¥2 roles configurable to different providers (poâ†’anthropic, devâ†’deepseek, qaâ†’moonshot, tech-leadâ†’zai, releaseâ†’openai) |
| AC-8 Contract tests | COVERED | 8/8 PASS; markers cover placeholder-only, fail-closed, schema, non-substitution |
| AC-9 Chinese APIs as capability | COVERED | marker 4 â€” deepseek/moonshot/zai/dashscope present; kit-operated proxy out of scope |
| AC-10 Tool-calling quality | COVERED | runbook h2 one-liner `## OpenCode model slug routing (US-0123)` present + byte-identical mirror |

## UAT probes (DEC-0009 / US-0092 / DEC-0078)

`UAT_BROWSER_PROBE_MODE=cursor` (default). This is a pack/contract story with no web UI surface. No `browser_smoke` step classified. ACs are mapped to pytest markers + static checks as stack-profile probes with evidence (command + output). No `.env` read. No intake evidence mutation. No `UAT_PROBE_FORBIDDEN`. **No fake browser PASS** â€” `browser_probe_used=false` recorded in `sprints/S0123/uat.json`.

| Probe ID | Kind | Command | Passed | Reason |
|----------|------|---------|--------|--------|
| `us0123-contract-gate` | pytest | `python -m pytest tests/us0123_contract_test.py -v` | true | 8/8 PASS exit 0 |
| `opencode-adapter-parity` | static | `python scripts/check_intake_template_parity.py --repo . --scope=opencode-adapter` | true | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `opencode-catalog-validator` | static | `python scripts/model_tier_validate.py --scope opencode-catalog --repo .` | true | `[MODEL_TIER_VALIDATION_OK]` |
| `runbook-h2-us0123` | static | grep `OpenCode model slug routing (US-0123)` + SHA-256 compare | true | h2 present L3991 both sides; SHA-256 equal |
| `compose-guards-6-unchanged` | static | read backlog/acceptance/architecture/DEC-0123/template agents/mirrors | true | backlog OPEN L4248; acceptance unchecked L151; arch anchor L1703; DEC-0123 Accepted; 0 `^model:`; mirrors byte-identical |
| `byte-identical-mirrors` | static | SHA-256 compare runbook + manifest + 3 paired scripts | true | 5/5 equal |

## Full-harness claim â€” NOT made

`tests/report.md` header: `Timestamp: 2026-08-24T13:02:49Z` / `Pass: 845` / `Fail: 0`. The report timestamp **predates** the US-0123 execute timestamp (`2026-08-24T14:48:00Z`) by ~1h46m. Per QA PASS-claim rule, no full-harness `Fail: 0` claim is made for US-0123. The stale report is noted without claiming green. US-0123 contract evidence rests on the 8/8 independent pytest re-run + parity + validator + byte-identity probes above. `rg "\[FAIL\]" tests/report.md` â†’ 0 matches (no failing rows in the stale report, but staleness disqualifies it as US-0123 evidence).

## Compose guards (6/6 UNCHANGED)

| # | Guard | Evidence |
|---|-------|----------|
| 1 | `docs/product/backlog.md` US-0123 | L4248 `Status: OPEN` (not mutated) |
| 2 | `docs/product/acceptance.md` US-0123 | L151 `- [ ] US-0123` (unchecked; not mutated) |
| 3 | `docs/engineering/architecture.md` US-0123 | L1703 `# US-0123 â€” Per-role OpenCode model slug routing (multi-provider)` (anchor present; not mutated) |
| 4 | `decisions/DEC-0123.md` | L4 `Status: Accepted` (not mutated) |
| 5 | `template/.opencode/agents/*.md` | grep `^model:` â†’ 0 matches (no `model:` keys in template) |
| 6 | Byte-identical mirrors | runbook + manifest + 3 paired scripts all SHA-256 equal activeâ†”template |

## Non-blocking findings (carry-forward)

- `ik_us0123_installer_hook_not_contract_tested` (carry-forward from sovereign-critic-execute): installer `--host opencode|both` hook (`installer.py` L580â€“586, `installer.ps1` `-InstallHost`, `installer.sh`) is not pytest-marked. Coverage rests on installer parity + manual spot-check. Non-blocking â€” T-003 hook is integration-level, not a contract-test gap. Recommend future story (e.g. US-0126 runbook parity) add an installer hook contract marker if operator-facing guarantee is desired.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- `phase_id=qa`
- `role=qa`
- `story_id=US-0123`
- `sprint_id=S0123`
- `fresh_context_marker=qa-US0123-qa-20260824T145500Z-fresh`
- `timestamp=2026-08-24T14:55:00Z` (UTC)
- `model_id=glm-5.2-high` (CROSS_MODEL_REVIEW=1 â€” required on isolation; **NEW** fresh_context_marker per US-0048 â€” marker reuse = stale isolation evidence)
- `evidence_ref=sprints/S0123/qa-findings.md, handoffs/qa_to_verify.md, sprints/S0123/uat.json, sprints/S0123/uat.md, docs/engineering/state.md (qa checkpoint append-bottom)`
- QA subagent spawned fresh per BUG-0006 / US-0048 isolation; no prior chat history carried forward; no subagent spawned from this QA subagent.

## Strict runtime proof tuple (US-0056 / DEC-0038)

- `runtime_proof_id=rp-auto-20260824-01-qa-qa-20260824T145500Z-US-0123`
- Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"qa","proof_issued_at":"2026-08-24T14:55:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-qa-qa-20260824T145500Z-US-0123","sprint_id":"S0123","story_id":"US-0123"}`
- `proof_hash=6D35A32F5E471232B0750442E370047E536442C87F36692A67D811F87C08CDAD`
- `proof_ttl_seconds=3600`
- `proof_ttl=2026-08-24T15:55:00Z` (1-hour TTL per DEC-0038, UTC = issued_at + 3600s)

## Stop condition

STOP after /qa. Hand off via artifacts only to `/verify-work` in fresh qa subagent per BUG-0006. Do not spawn `/verify-work` from this qa subagent. Do not mark US-0123 DONE.
