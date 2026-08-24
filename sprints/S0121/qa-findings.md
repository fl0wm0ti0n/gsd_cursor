# QA Findings — US-0121 / S0121

> ## Loop-3 verdict — PASS (0 blocking findings; harness Fail:0 independently re-run)
>
> - sprint_id: S0121
> - story_id: US-0121
> - phase_id: qa (auto-implementation loop, cycle 3 — execute loop-3+4 harness remediation + original US-0121 host-mode work)
> - role: qa (fresh per BUG-0006)
> - orchestrator_run_id: auto-20260824-01
> - delivery_mode: ultra_lean
> - macro_phase: build+verify
> - fresh_context_marker: qa-US0121-qa-loop3-20260824T104600Z-fresh (new; not reused from loop-2)
> - timestamp: 2026-08-24T10:46:00Z (UTC)
> - model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
> - verdict: **PASS** (0 blocking findings; loop-1 NB-1..NB-4 carried forward; NB-1 CLOSED for this env)
> - blocking_findings: 0
> - non_blocking_findings: 4 (carried forward; NB-1 CLOSED for this env; no new AC breaks)
> - tests_run: live (canonical harness + US-0121 pytest + BUG-0011 linkage + metadata guard + triad)
> - next_scheduled_phase: /verify-work (0 blocking findings; verify-work re-enabled)
> - stop_condition: STOP after qa loop-3; do not spawn /verify-work or /execute. Orchestrator reroutes.
>
> ### Independent verification evidence (loop-3 — no rubber-stamp)
>
> | Check | Method | Result |
> |---|---|---|
> | `tests/report.md` header `Fail: 0` | Independent re-run `powershell -ExecutionPolicy Bypass -File tests/run-tests.ps1` (exit 0; fresh report @ 2026-08-24T10:45:36Z) | **Pass:845 / Fail: 0** (literal zero) |
> | Zero `- [FAIL]` lines | Grep `\[FAIL\]` against post-rerun report.md | **0 matches** |
> | US-0121 host-mode pytest | `python -m pytest tests/us0121_host_mode_test.py -v` (python 3.12.10 on PATH) | **14/14 passed** (3.37s) |
> | BUG-0011 architecture linkage | `python -m pytest tests/auto_command_contract_test.py::AutoCommandContractTest::test_bug0011_architecture_linkage -q` | **1 passed, 9 subtests passed** |
> | Metadata guard (US-0071) | `python scripts/check-user-visible-metadata.py --repo .` | **exit 0** |
> | Triad hot-surface | `python scripts/enforce-triad-hot-surface.py --check` | **exit 0** |
> | Host gating preserved | Grep `CURSOR_HOST_HOOKS_SKIPPED` in installer.py | **L555 present** |
> | Architecture US-0089 forward-link | Grep `BUG-0011` in architecture.md | **L989 + L2253 + L2660** |
> | Architecture US-0091/US-0093 sections | Grep `^# US-009` | **L1035 (US-0091) + L1050 (US-0093)** — loop-3 triad rollover intact |
> | Installer README mirror | Grep `sync_root_readme_to_its_magic` / `intent contract:` | **L603 marker + L626 fn + L1158/L1240 call sites** — no regression |
> | run-tests PATH | Read `tests/run-tests.ps1` L8-33 | **`Ensure-NodeOnPath` present**; `@(...).Count` header writes literal `Fail: 0` |
>
> ### UAT probe notes (loop-3 — honest, no silent green)
>
> - **Python on PATH**: `python --version` → `Python 3.12.10` (live pytest executed; loop-1/loop-2 NB-1 CLOSED for this env).
> - **Node on PATH (bare shell)**: `node --version` → `term not recognized` in fresh QA shell. **However**, canonical harness re-ran green (exit 0, Fail:0) because `Ensure-NodeOnPath` prepends winget/standard Node dirs inside the harness process. Node-dependent CLI lifecycle tests pass within the harness context.
> - **npm**: same as node — not on bare shell PATH; harness-internal only.
> - **UAT probe class**: contract/CLI (not a web app). No browser UAT required (UAT_PROBE_NOT_APPLICABLE). Full UAT rewrite belongs to `/verify-work` per orchestrator brief.
> - **No silent PASS**: pytest 14/14 executed live (not static fallback). Harness re-run produced fresh `tests/report.md` timestamp (2026-08-24T10:45:36Z), not the dev-attested 10:37:29Z copy.
>
> ### Loop-3+4 harness remediation regression check
>
> - **Installer README mirror** (loop-3): `sync_root_readme_to_its_magic` prefers kit-root `README.md` when target stub lacks `intent contract:` marker. No `US-xxxx` literals in installers (metadata guard exit 0). No regression.
> - **run-tests PATH** (loop-4): `Ensure-NodeOnPath` at L8-31; invoked at L33. `@((...)).Count` writes literal `Fail: 0`. Independent re-run confirms `Fail: 0` literal at L5. No regression.
> - **Architecture forward-links** (loop-4): US-0089 deferred-anchor at L989 forward-links `BUG-0011` / `DEC-0077`. `test_bug0011_architecture_linkage` passes. US-0091 (L1035) + US-0093 (L1050) placed mid-file by loop-3 triad rollover — preserves `# US-0089` bottom-append invariant. No regression.
>
> ### AC re-evaluation (loop-3 — live + static)
>
> | AC | Marker(s) | Loop-3 Status |
> |----|-----------|----------------|
> | AC-1 (template/.opencode tree) | 11, 12 | **PASS** (live markers 11+12) |
> | AC-2 (--host flag) | 1-7, 14 | **PASS** (live markers 1-7; static 14) |
> | AC-3 (install/upgrade/clean host-scoped) | 2-4, 8, 9, 14 | **PASS** (live markers 2-4, 8, 9) |
> | AC-4 (cursor coexistence byte-identity) | 2-4 | **PASS** (live markers 2-4) |
> | AC-5 (manifest + triple-installer) | 10, 11, 14 | **PASS** (live markers 10, 11, 14) |
> | AC-6 (parity scope) | 13 | **PASS** (live marker 13; NB-2 carried) |
> | AC-7 (contract tests 14 markers) | 1-14 | **PASS** (14/14 live) |
> | AC-8 (compose 5/5 UNCHANGED) | manual | **PASS** (loop-3+4 touched harness + arch forward-link + installer README mirror only; compose surface unchanged) |
> | AC-9 (docs hook minimal) | 14 + runbook h2 | **PASS** |
> | AC-10 (no secrets in template) | 12 | **PASS** (live marker 12; B-1 closed loop-2) |
>
> ### Compose guards (5/5 UNCHANGED — read-only, loop-3)
>
> | Compose target | Verification | Result |
> |---|---|---|
> | US-0008 (CLI installer) | loop-3+4 touched installer README mirror (metadata-safe) + run-tests PATH + arch forward-link; `--host` + missing/overwrite/clean/upgrade UNCHANGED | read-only |
> | DEC-0045 (its_magic/ ownership) | unchanged | read-only |
> | US-0102 (volatile-ID rule) | template ships no slugs; *.local.json{,c} gitignore mirrors kit | read-only |
> | US-0001 (phase names) | placeholders only; no command body clone | read-only |
> | US-0018 (packaging delivery) | installer delivery path unchanged; Homebrew 0.1.3-4 (loop-3) | read-only |
>
> ### Scope discipline (loop-3 — do-not-expand)
>
> - NB-2 (AC-6 parity scope grep-only) — **not** addressed (deferred).
> - NB-3 (triple-installer behavioral parity grep-only) — **not** addressed (deferred).
> - NB-4 (symmetric CURSOR_* shrink diagnostics grep-only) — **not** addressed (deferred; would require 15th marker).
> - No 15th test added (14-marker budget locked per `ik_us0121_ac9_help_test_yagni`).
> - No backlog/acceptance mutation (US-0045).
> - US-0121 not flipped to DONE; acceptance boxes not ticked (closure owns that at `/release`).
>
> ## Non-blocking findings (loop-3 — carried forward from loop-1/loop-2; no new AC breaks)
>
> ### NB-1: tests_not_run=python_not_on_path — CLOSED for this environment (loop-3)
>
> - severity: non-blocking (environmental) — **CLOSED in loop-3** (python 3.12.10 on PATH; live pytest 14/14)
> - ac_mapping: AC-7
> - status: resolved (loop-3) — carried forward as historical note
> - evidence: `python --version` → `Python 3.12.10`; `python -m pytest tests/us0121_host_mode_test.py -v` → 14 passed in 3.37s.
> - impact: none for loop-3 (live coverage achieved). NB-1 remains a note for any future env without python on PATH.
>
> ### NB-2: AC-6 parity scope is grep-only and excludes pack files (marker 13)
>
> - severity: non-blocking (carried forward; not addressed in loop-3 per scope discipline)
> - ac_mapping: AC-6
> - marker: 13 — **PASSED live** in loop-3 (grep-only assertion holds)
> - issue_key: ik_us0121_ac6_parity_scope_pack_gap
> - impact: pack-file drift under template/.opencode/ enforced only by static markers 11+12, not by parity CLI subprocess invocation.
> - remediation: defer to a future slice (US-0122..US-0126). Not blocking.
>
> ### NB-3: triple-installer behavioral parity is grep-only (marker 14)
>
> - severity: non-blocking (carried forward; not addressed in loop-3)
> - ac_mapping: AC-5
> - marker: 14 — **PASSED live** in loop-3 (static grep assertion holds)
> - issue_key: ik_us0121_py_only_behavioral_triple_grep
> - impact: PS/sh behavioral parity YAGNI-deferred to manual QA runbook (US-0126).
> - remediation: defer. Not blocking.
>
> ### NB-4: symmetric CURSOR_* shrink diagnostics grep-only (markers 8-9)
>
> - severity: non-blocking (carried forward; not addressed in loop-3)
> - ac_mapping: AC-3, AC-7
> - markers: 8, 9 — **PASSED live** in loop-3 (opencode-shrink behavioral); symmetric CURSOR_* shrink-to-opencode path remains grep-only in marker 14.
> - impact: shrink-to-opencode behavioral path untested at runtime.
> - remediation: defer (would break 14-marker budget). Not blocking.
>
> ## Decision gate (loop-3)
>
> - decision_gate=false (0 blocking findings)
> - next_scheduled_phase=/verify-work (0 blocking findings; verify-work re-enabled per ultra_lean merge)
> - stop_condition=STOP after qa loop-3; do not spawn /verify-work or /execute from this QA subagent. Hand off via artifacts only.
>
> ## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2) — loop-3
>
> - phase_id=qa
> - role=qa
> - fresh_context_marker=qa-US0121-qa-loop3-20260824T104600Z-fresh
> - timestamp=2026-08-24T10:46:00Z
> - model_id=glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
> - evidence_ref=sprints/S0121/qa-findings.md (loop-3 section) + handoffs/qa_to_verify.md (loop-3) + handoffs/dev_to_qa.md (loop-4 delta) + sprints/S0121/summary.md (loop-4 section) + tests/report.md@2026-08-24T10:45:36Z + tests/us0121_host_mode_test.py (14/14 live) + docs/engineering/state.md (qa loop-3 checkpoint)
> - next_scheduled_phase=/verify-work
> - stop_condition=STOP after qa loop-3; do not spawn next phase. Orchestrator reroutes to /verify-work in a fresh subagent.
> - Prior qa-phase strict proof consumed (loop-2): `rp-auto-20260823-01-qa-qa-loop2-20260823T115500Z-US-0121` (proof_hash=601792CC0D9CFFE7B87A2F46BC0C13FDA330F1E0B1946E99CE93B61A256091DF). Not reused.
> - Prior dev loop-4 strict proof consumed: `rp-auto-20260824-01-execute-dev-loop4-20260824T103729Z-US-0121` (proof_hash=d7cf0bc4013542331a876979027fd24fd72d0de13f6bbd28f8821d0a5f91c743). Not reused.
> - Prior sovereign-critic loop-4 strict proof consumed: `tl-US0121-sovereign-critic-execute-loop4-20260824T104028Z-fresh` (anti_slop_aggregate=8; 0 blocking findings; producer PASS upheld).
>
> ## Strict runtime proof (US-0056 / DEC-0038) — loop-3
>
> - runtime_proof_id=rp-auto-20260824-01-qa-qa-loop3-20260824T104600Z-US-0121
> - orchestrator_run_id=auto-20260824-01
> - phase_id=qa, role=qa, story_id=US-0121, sprint_id=S0121
> - delivery_mode=ultra_lean, macro_phase=build+verify
> - model_id=glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
> - proof_issued_at=2026-08-24T10:46:00Z
> - proof_ttl_seconds=3600
> - proof_hash=9BF670357BA9AD30AB20EEDEFFECC6A2F3E1700EE1539E6F3F7E600FB7A0DF58 (SHA-256, UTF-8 bytes via PowerShell)
> - Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","model_id":"glm-5.2-high","orchestrator_run_id":"auto-20260824-01","phase_id":"qa","proof_issued_at":"2026-08-24T10:46:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260824-01-qa-qa-loop3-20260824T104600Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}`
> - proof_ttl=2026-08-24T11:46:00Z (1-hour TTL)
>
> ## Stop condition (loop-3)
>
> STOP after qa loop-3. Do not spawn /verify-work or /execute from this QA subagent (BUG-0006). Hand off via artifacts only: sprints/S0121/qa-findings.md (this file) + handoffs/qa_to_verify.md (loop-3) + docs/engineering/state.md isolation append + handoffs/resume_brief.md prepend. The orchestrator (AUTO_IMPLEMENTATION_LOOP=1) reroutes to /verify-work in a fresh subagent.

---

> ## Loop-2 verdict — PASS (B-1 CLOSED; 0 blocking findings)
>
> - sprint_id: S0121
> - story_id: US-0121
> - phase_id: qa (merges plan-verify + execute QA + verify-work + UAT per ultra_lean / US-0096 / DEC-0082)
> - role: qa (fresh per BUG-0006)
> - orchestrator_run_id: auto-20260823-01
> - delivery_mode: ultra_lean
> - macro_phase: build+verify
> - fresh_context_marker: qa-US0121-qa-loop2-20260823T115500Z-fresh
> - timestamp: 2026-08-23T11:55:00Z (UTC)
> - model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
> - verdict: **PASS** (B-1 closed; 0 blocking findings)
> - blocking_findings: 0
> - non_blocking_findings: 4 (carried forward from loop-1; no new AC breaks)
> - tests_run: 0 (python_not_on_path — static review fallback per qa.md §2; NB-1, non-blocking)
> - next_scheduled_phase: /verify-work (B-1 closed; verify-work re-enabled)
>
> ### B-1 closure verification (loop-2)
>
> - **B-1 status**: CLOSED
> - **issue_key**: ik_us0121_marker12_apikey_prose_false_positive (loop-1 blocking; loop-2 closed)
> - **remediation applied**: Option C (both)
>   1. `tests/us0121_host_mode_test.py` L248: regex tightened from `r"apiKey|api_key|sk-|MODEL="` (substring search) to `r"\bapiKey\s*[:=]|api_key\s*[:=]|sk-[A-Za-z0-9]{8,}|MODEL\s*="` (assignment-like only; word-boundary on `apiKey`; 8+ alnum chars after `sk-`; whitespace around `[:=]`).
>   2. `template/.opencode/README.md` L45-46: rephrased from "a consumer repo may add one with provider/apiKey and must not commit it" to "a consumer repo may add one with provider credentials; do not commit it". The literal `apiKey` token is no longer present in the pack.
>
> ### Static-review evidence (loop-2)
>
> - `rg "apiKey|api_key|sk-|MODEL=" template/.opencode` -> **0 hits** (was 1 hit at `template/.opencode/README.md:45` before loop-2). Confirmed via Grep tool.
> - Tightened regex (L248) verified against synthetic positives (7/7 match: `apiKey: "..."`, `apiKey = "..."`, `api_key: "..."`, `api_key = "..."`, `sk-AbCdEfGh12345`, `MODEL=gpt-4`, `MODEL = gpt-4`) and synthetic prose negatives (6/6 no-match). README.md full-text match against tightened regex -> False (expected). Defense-in-depth confirmed.
> - `tests/us0121_host_mode_test.py` <-> `template/tests/us0121_host_mode_test.py` SHA-256 byte-identical: `F3A6075783B87851C6529B0AC8C788449E43E815AE2EEA0511157A55AD6AF83B` (both copies; matches dev loop-2 attestation).
> - `template/.opencode/README.md` SHA-256 = `F50558292496E124D08D1B1D643B1F8EAB3938B8A3F11F5D8A6D77AA7F1DBAD5` (post-rephrase).
> - Manifest byte-identity (active <-> template) preserved: `4AC96FF8A3B9EA2B025A93D787526B0E6343B662BA78BB0C8A72B186697082B5` (both copies; unchanged in loop-2).
> - Parity script byte-identity (active <-> template) preserved: `E479211A556543C91972D1E9417A4F31058791A0DA03A9EDE26A67507458B647` (both copies; unchanged in loop-2).
> - `tests_not_run=python_not_on_path` (NB-1 persists; `py`/`python`/`python3`/`node` all absent on this Windows host — confirmed via PATH probe: `py`->EXC, `python`->9009, `python3`->9009, `node`->EXC). Live pytest not run at QA time. Per qa.md §2: static review fallback used; B-1 closed at static layer.
>
> ### AC re-evaluation (loop-2)
>
> | AC | Marker(s) | Type | Loop-2 Status |
> |----|-----------|------|---------------|
> | AC-1 (template/.opencode tree) | 11, 12 (static) | static grep + pack layout | **PASS** (layout + no-secrets gate) |
> | AC-2 (--host flag) | 1-7 (behavioral) + 14 (static) | behavioral + static | PASS (static); behavioral not run (NB-1) |
> | AC-3 (install/upgrade/clean host-scoped) | 2-4, 8, 9 (behavioral) + 14 (static) | behavioral + static | PASS (static); behavioral not run (NB-1) |
> | AC-4 (cursor coexistence byte-identity) | 2-4 (behavioral) | behavioral | not run (NB-1) |
> | AC-5 (manifest + triple-installer) | 10, 11, 14 (static) | static + manifest byte-identity | **PASS** |
> | AC-6 (parity scope) | 13 (static) | static grep | PASS (grep-only; NB-2 non-blocking) |
> | AC-7 (contract tests 14 markers) | 1-14 | behavioral + static | **PASS** (B-1 closed; marker 12 regex assignment-like; static review confirms no false-positive) |
> | AC-8 (compose 5/5 UNCHANGED) | manual | static review | PASS (additive only; loop-2 touched only README + test pair) |
> | AC-9 (docs hook minimal) | 14 (static --host in JS help) + runbook h2 | static grep | PASS |
> | AC-10 (no secrets in template) | 12 (static) | static grep | **PASS** (rg 0 hits; tightened regex no longer matches prose; defense-in-depth) |
>
> ### Compose guards (5/5 UNCHANGED — verified read-only, loop-2)
>
> | Compose target | Verification | Result |
> |---|---|---|
> | US-0008 (CLI installer) | loop-2 touched only README + test pair; installer source unchanged | read-only |
> | DEC-0045 (its_magic/ ownership) | its_magic/ ownership unchanged | read-only |
> | US-0102 (volatile-ID rule) | template ships no vendor slugs; *.local.json{,c} gitignore mirrors kit convention | read-only |
> | US-0001 (phase names) | placeholders only; no command body clone | read-only |
> | US-0018 (packaging delivery) | installer delivery path unchanged in loop-2 | read-only |
>
> ### UAT probe classification (US-0092 / DEC-0078) — loop-2
>
> - story kind: CLI installer + template pack (not a web app).
> - probe class: **contract/CLI** (per orchestrator brief).
> - HTTP origin: none.
> - UAT_PROBE_NOT_APPLICABLE — no browser UAT required. Automatable probe = CLI pytest (tests/us0121_host_mode_test.py) + parity CLI (scripts/check_intake_template_parity.py --scope=opencode-adapter). Both deferred to a python-on-PATH environment (NB-1).
> - Not UAT_PROBE_UNRESOLVED — the probe maps cleanly to CLI contract tests; only the runtime is unavailable.
>
> ### Scope discipline (loop-2 — do-not-expand per orchestrator brief)
>
> - NB-2 (AC-6 parity scope grep-only) — **not** addressed.
> - NB-3 (triple-installer behavioral parity grep-only) — **not** addressed.
> - NB-4 (symmetric CURSOR_* shrink diagnostics grep-only) — **not** addressed.
> - Installers (`installer.py` / `installer.ps1` / `installer.sh` / `bin/its-magic.js`), manifest, and `scripts/check_intake_template_parity.py` — **unchanged** in loop-2.
> - No 15th test added (14-marker budget locked per `ik_us0121_ac9_help_test_yagni`).
>
> ## Non-blocking findings (loop-2 — carried forward from loop-1; no new AC breaks)
>
> ### NB-1: tests_not_run=python_not_on_path (environmental)
>
> - severity: non-blocking (environmental)
> - ac_mapping: AC-7 (live pytest not run)
> - status: skipped (loop-2)
> - evidence: `py`/`python`/`python3`/`node` all return exit 9009 / "Python was not found" / "term not recognized" on this Windows host. Confirmed via PATH probe in QA loop-2.
> - impact: 14/14 markers not exercised live. Static review covers markers 11-14 (grep) and the static portions of markers 1-10 (installer source structure). Behavioral assertions (markers 1-10 invoke installer.py in tempfile.TemporaryDirectory()) are not run.
> - mitigation: orchestrator should rerun /qa (or /verify-work) in an environment with python 3 on PATH before /release. Until then, QA verdict relies on static review + the B-1 closure proof.
>
> ### NB-2: AC-6 parity scope is grep-only and excludes pack files (marker 13)
>
> - severity: non-blocking
> - ac_mapping: AC-6
> - marker: 13 (test_us0121_parity_scope_opencode_adapter_registered)
> - issue_key: ik_us0121_ac6_parity_scope_pack_gap (execute-critic row 17)
> - evidence: tests/us0121_host_mode_test.py L264-278 only greps PARITY_SCRIPT source for "opencode-adapter" / OPENCODE_ADAPTER_PAIRS / SCOPES[all] membership. It never subprocess-invokes python scripts/check_intake_template_parity.py --scope=opencode-adapter. OPENCODE_ADAPTER_PAIRS pairs manifest/script/test mirrors only — explicitly excludes template/.opencode/** per Q9 YAGNI comment.
> - impact: pack-file drift under template/.opencode/ is enforced only by static marker 11 (manifest grep) and marker 12 (no-secrets grep), not by the parity CLI named in AC-6.
> - remediation: defer to a future slice (US-0122..US-0126) when an active .opencode/ mirror exists; or add a subprocess invocation in marker 13 once python is on PATH. Not blocking because the manifest byte-identity gate (marker 11) + no-secrets gate (marker 12) cover the pack surface this slice owns.
>
> ### NB-3: triple-installer behavioral parity is grep-only (marker 14)
>
> - severity: non-blocking
> - ac_mapping: AC-5
> - marker: 14 (test_us0121_triple_installer_host_parity)
> - issue_key: ik_us0121_py_only_behavioral_triple_grep (execute-critic row 18)
> - evidence: markers 1-10 subprocess-invoke installer.py only. Marker 14 is static grep asserting host_gates_cursor_row / Host-GatesCursorRow / --host / -InstallHost / 5 diagnostic strings exist in installer.ps1, installer.sh, installer.py, bin/its-magic.js. No test exercises PS -InstallHost duplicate argv enforcement, sh --host forwarding, or JS -InstallHost bridge at runtime.
> - impact: PS/sh behavioral parity is YAGNI-deferred to manual QA. Marker 14 names "triple-installer parity" but enforces source presence only.
> - remediation: defer to manual QA runbook (US-0126) or add PS/sh subprocess markers once python+pwsh+bash are all on PATH. Not blocking because the source-level contract is locked and the predicate is shared.
>
> ### NB-4: symmetric CURSOR_* shrink diagnostics grep-only (markers 8-9)
>
> - severity: non-blocking
> - ac_mapping: AC-3, AC-7
> - markers: 8, 9 (behavioral, opencode-shrink only) + 14 (static grep for all 5 diagnostics)
> - evidence: markers 8-9 cover OPENCODE_ORPHANED_BY_CLEAN_CURSOR / OPENCODE_STALE_BY_UPGRADE_CURSOR only (shrink both -> cursor). The symmetric CURSOR_ORPHANED_BY_CLEAN_OPENCODE / CURSOR_STALE_BY_UPGRADE_OPENCODE (shrink both -> opencode) are grep-only in marker 14 (L300-309). installer.py L170-174 and L1084-1088 emit them; installer.ps1 L142 and L773 emit them; installer.sh L183 and L670 emit them.
> - impact: shrink-to-opencode behavioral path is untested at runtime.
> - remediation: defer to a future slice or add markers 15-16 (would break the locked 14-marker budget per ik_us0121_ac9_help_test_yagni / ik_us0121_plan_verify_phantom_coverage). Not blocking because the source contract is present and symmetric.
>
> ## Decision gate (loop-2)
>
> - decision_gate=false (B-1 closed; no new blocking findings)
> - next_scheduled_phase=/verify-work (B-1 closed; verify-work re-enabled per ultra_lean merge)
> - stop_condition=STOP after qa loop-2; do not spawn /verify-work from this QA subagent. Hand off via artifacts only.
>
> ## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2) — loop-2
>
> - phase_id=qa
> - role=qa
> - fresh_context_marker=qa-US0121-qa-loop2-20260823T115500Z-fresh
> - timestamp=2026-08-23T11:55:00Z
> - model_id=glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
> - evidence_ref=sprints/S0121/qa-findings.md (this file, loop-2 section) + handoffs/qa_to_verify.md + handoffs/dev_to_qa.md (loop-2 delta) + sprints/S0121/summary.md (loop-2 section) + tests/us0121_host_mode_test.py (L248) + template/.opencode/README.md (L45-46) + docs/engineering/state.md (qa loop-2 checkpoint)
> - next_scheduled_phase=/verify-work
> - stop_condition=STOP after qa loop-2; do not spawn next phase. Orchestrator reroutes to /verify-work in a fresh subagent.
> - Prior qa-phase strict proof consumed (loop-1): `rp-auto-20260823-01-qa-qa-20260823T114000Z-US-0121` (proof_hash=457664171B3FF0771957E71785576B14B39C66F3F988066A82904BFB177BAB78). Not reused.
> - Prior dev loop-2 strict proof consumed: `rp-auto-20260823-01-execute-dev-loop2-20260823T115000Z-US-0121` (proof_hash=469A1DB5E910AA81571B343820426B0FC5E3384CDEDF103D9C1C88B3FB8F2CB8). Not reused.
> - Prior sovereign-critic loop-2 strict proof consumed: `tl-US0121-sovereign-critic-execute-loop2-20260823T115200Z-fresh` (anti_slop_aggregate=8; 0 blocking findings).
>
> ## Strict runtime proof (US-0056 / DEC-0038) — loop-2
>
> - runtime_proof_id=rp-auto-20260823-01-qa-qa-loop2-20260823T115500Z-US-0121
> - orchestrator_run_id=auto-20260823-01
> - phase_id=qa, role=qa, story_id=US-0121, sprint_id=S0121
> - delivery_mode=ultra_lean, macro_phase=build+verify
> - proof_issued_at=2026-08-23T11:55:00Z
> - proof_ttl_seconds=3600
> - proof_hash=601792CC0D9CFFE7B87A2F46BC0C13FDA330F1E0B1946E99CE93B61A256091DF (SHA-256, UTF-8 bytes via PowerShell — python not on PATH)
> - Canonical payload (sorted-key JSON per DEC-0038): `{"delivery_mode":"ultra_lean","macro_phase":"build+verify","orchestrator_run_id":"auto-20260823-01","phase_id":"qa","proof_issued_at":"2026-08-23T11:55:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260823-01-qa-qa-loop2-20260823T115500Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}`
> - proof_ttl=2026-08-23T12:55:00Z (1-hour TTL)
>
> ## Stop condition (loop-2)
>
> STOP after qa loop-2. Do not spawn /verify-work or /execute from this QA subagent (BUG-0006). Hand off via artifacts only: sprints/S0121/qa-findings.md (this file) + handoffs/qa_to_verify.md + docs/engineering/state.md isolation append + handoffs/resume_brief.md prepend. The orchestrator (AUTO_IMPLEMENTATION_LOOP=1) reroutes to /verify-work in a fresh subagent.

---

## Loop-1 history (preserved below — FAIL, B-1 opened; closed by loop-2 above)

- sprint_id: S0121
- story_id: US-0121
- phase_id: qa (merges plan-verify + execute QA + verify-work + UAT per ultra_lean / US-0096 / DEC-0082)
- role: qa (fresh per BUG-0006)
- orchestrator_run_id: auto-20260823-01
- delivery_mode: ultra_lean
- macro_phase: build+verify
- fresh_context_marker: qa-US0121-qa-20260823T114000Z-fresh
- timestamp: 2026-08-23T11:40:00Z (UTC)
- model_id: glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- verdict: **FAIL** (1 blocking finding)
- blocking_findings: 1
- non_blocking_findings: 4
- tests_run: 0 (python_not_on_path — static review fallback per qa.md §2)
- next_scheduled_phase: /execute (auto-implementation loop; blocking finding open)

## Test plan (AC-1..AC-10 → 14 markers + manual/static checks)

| AC | Marker(s) | Type | Status |
|----|-----------|------|--------|
| AC-1 (template/.opencode tree) | 11, 12 (static) | static grep + pack layout | PASS (layout) / **FAIL** (marker 12) |
| AC-2 (--host flag) | 1-7 (behavioral) + 14 (static) | behavioral + static | PASS (static); behavioral not run |
| AC-3 (install/upgrade/clean host-scoped) | 2-4, 8, 9 (behavioral) + 14 (static) | behavioral + static | PASS (static); behavioral not run |
| AC-4 (cursor coexistence byte-identity) | 2-4 (behavioral) | behavioral | not run (python absent) |
| AC-5 (manifest + triple-installer) | 10, 11, 14 (static) | static + manifest byte-identity | PASS |
| AC-6 (parity scope) | 13 (static) | static grep | PASS (grep-only; see NB-2) |
| AC-7 (contract tests 14 markers) | 1-14 | behavioral + static | **FAIL** (marker 12 false-positive) |
| AC-8 (compose 5/5 UNCHANGED) | manual | static review | PASS (additive only) |
| AC-9 (docs hook minimal) | 14 (static --host in JS help) + runbook h2 | static grep | PASS |
| AC-10 (no secrets in template) | 12 (static) | static grep | **FAIL** (README prose false-positive) |

## Test execution

### Attempted

- py -3 -m pytest tests/us0121_host_mode_test.py -v
- python -m pytest tests/us0121_host_mode_test.py -v
- python3 -m pytest tests/us0121_host_mode_test.py -v

### Result

- tests_not_run=python_not_on_path — py, python, python3, node all absent from PATH on this Windows host (PowerShell-only environment; same as execute phase per handoffs/dev_to_qa.md L92 and sprints/S0121/summary.md L82).
- Per .cursor/commands/qa.md §2: fell back to **static review** (no disk scan; no hang). Static review can still FAIL when code/docs contradict ACs — and it did (see B-1).

### Static review evidence

- Manifest byte-identity (active ↔ template) verified via Get-FileHash -Algorithm SHA256:
  - docs/engineering/context/installer-owned-paths.manifest = 4AC96FF8A3B9EA2B025A93D787526B0E6343B662BA78BB0C8A72B186697082B5
  - template/docs/engineering/context/installer-owned-paths.manifest = 4AC96FF8A3B9EA2B025A93D787526B0E6343B662BA78BB0C8A72B186697082B5 ✅
  - scripts/check_intake_template_parity.py = E479211A556543C91972D1E9417A4F31058791A0DA03A9EDE26A67507458B647 (both copies) ✅
  - tests/us0121_host_mode_test.py = ABCE6E344C09F6BE6AFDA245655CAC2EDB59734E754AFFE9CCF389402800CFB9 (both copies) ✅
- Manifest contains [opencode_install_include_paths] + [opencode_clean_paths] with the 5 pack rows + .opencode clean row.
- installer.py L16-176: HOST_VALUES, HOST_DEFAULT=cursor, _HostAction (duplicate fail-closed L25-29, unknown fail-closed L32-36), host_gates_cursor_row L40-50, host_includes_opencode/host_includes_cursor L53-58, build_effective_include_paths L135-144, build_effective_clean_paths L147-154, emit_host_shrink_diagnostics L157-175 (orphan), L964-970 (unknown fail-closed), L1078-1089 (stale upgrade diagnostics). --help L808-814 documents --host.
- installer.ps1 L5 $InstallHost, L21-37 normalize + duplicate fail-closed, L96 Host-GatesCursorRow, L115 predicate apply, L139-142 orphan diagnostics, L560-567 --help doc, L770-773 stale upgrade diagnostics. **No -Host parameter** (uses -InstallHost to avoid the $Host automatic-variable landmine — confirmed).
- installer.sh L50-56 --help doc, L119-120 normalize, L133 host_gates_cursor_row, L156 predicate apply, L180-183 orphan diagnostics, L457-466 --host argparse + duplicate fail-closed + unknown fail-closed, L528/576 opencode section reads, L667-670 stale upgrade diagnostics.
- bin/its-magic.js L65-81 --host parser (normalize lowercase+trim, duplicate fail-closed, unknown fail-closed), L98-101 --help, L135-144 --help documents --host value + cursor-default + diagnostics, L189-194 INSTALL_HOST_INVALID emit, L211 -InstallHost forward to PS, L228 --host forward to sh.
- template/.opencode/ layout: agents/.gitkeep (0 bytes), commands/.gitkeep (0 bytes), plugins/README.md, .gitignore (7 lines, Q10 four pattern groups), README.md (76 lines). No repo-root opencode.json. No active kit .opencode/ mirror.
- scripts/check_intake_template_parity.py L484-497 OPENCODE_ADAPTER_PAIRS (3 pairs: manifest, parity script, test file), L521 opencode-adapter in SCOPES, L543 added to SCOPES[all] union.
- docs/engineering/runbook.md L3870 ## OpenCode host mode (US-0121) h2 + --host flag + cursor-default + install/clean/upgrade + orphan/stale diagnostics + PS -InstallHost landmine note (L3964).

## Blocking findings

### B-1: marker 12 false-positive — README prose contains `apiKey` (AC-10 / AC-7)

- severity: blocking
- ac_mapping: AC-10, AC-7
- marker: 12 (test_us0121_no_secrets_in_pack)
- status: FAIL
- issue_key: ik_us0121_marker12_apikey_prose_false_positive (execute-critic row 16, escalated by QA to blocking)
- evidence:
  - tests/us0121_host_mode_test.py L243: pattern = re.compile(r"apiKey|api_key|sk-|MODEL=") — substring search, **no word-boundary**, **no README exclusion**.
  - tests/us0121_host_mode_test.py L245-253: os.walk(TEMPLATE_OPENCODE) reads every file including README.md; pattern.search(text) returns match on first apiKey substring.
  - template/.opencode/README.md L45: "ships no opencode.json (a consumer repo may add one with provider/apiKey" — the literal substring apiKey is present in prose documenting a forbidden pattern.
  - Confirmed via rg "apiKey|api_key|sk-|MODEL=" template/.opencode/ → 1 hit at template\.opencode\README.md:45.
- impact: pytest tests/us0121_host_mode_test.py -v will fail marker 12 on first live run (any environment with python on PATH). AC-10 contract test obligation is unmet. The execute phase declared PASS with tests_not_run=python_not_on_path, so this false-positive was not caught at execute time.
- root cause: The regex is too permissive (substring match without word-boundary or assignment-context) AND the README documents the forbidden pattern using the literal token. Either side can be fixed; both are valid product/test bugs.
- reproduction:
  1. Install python 3 on PATH.
  2. python -m pytest tests/us0121_host_mode_test.py::test_us0121_no_secrets_in_pack -v
  3. Observe failure: AssertionError: secret-like patterns found in template/.opencode/: ['template/.opencode/README.md'].
- remediation options (dev picks one; QA does not implement):
  - Option A (test fix — preferred, smallest surface): tighten the regex to match assignments, not prose. Use re.compile(r"\bapiKey\s*[:=]|api_key\s*[:=]|sk-[A-Za-z0-9]{8,}|MODEL\s*=") or exclude README.md from the walk. This documents the forbidden pattern in README without false-positive.
  - Option B (product fix): rephrase template/.opencode/README.md L45 to avoid the literal apiKey token (e.g., "a consumer repo may add one with provider credentials and must not commit it"). Keeps the naive regex.
  - Option C (both): combine A + B for defense-in-depth.
- compose_guard_impact: none (README is template-only; not a US-0008 / DEC-0045 / US-0102 / US-0001 / US-0018 surface).
- decision_gate: required — auto-implementation loop reroutes to /execute (per AUTO_IMPLEMENTATION_LOOP=1). QA does not spawn /execute.

## Non-blocking findings

### NB-1: tests_not_run=python_not_on_path (environmental)

- severity: non-blocking (environmental)
- ac_mapping: AC-7 (live pytest not run)
- status: skipped
- evidence: py/python/python3/node all return exit 9009 / "Python was not found" on this Windows host. Same as execute phase.
- impact: 14/14 markers not exercised live. Static review covers markers 11-14 (grep) and the static portions of markers 1-10 (installer source structure). Behavioral assertions (markers 1-10 invoke installer.py in tempfile.TemporaryDirectory()) are not run.
- mitigation: orchestrator should rerun /qa in an environment with python 3 on PATH before /release. Until then, QA verdict relies on static review + the B-1 false-positive proof.

### NB-2: AC-6 parity scope is grep-only and excludes pack files (marker 13)

- severity: non-blocking
- ac_mapping: AC-6
- marker: 13 (test_us0121_parity_scope_opencode_adapter_registered)
- issue_key: ik_us0121_ac6_parity_scope_pack_gap (execute-critic row 17)
- evidence: tests/us0121_host_mode_test.py L259-273 only greps PARITY_SCRIPT source for "opencode-adapter" / OPENCODE_ADAPTER_PAIRS / SCOPES[all] membership. It never subprocess-invokes python scripts/check_intake_template_parity.py --scope=opencode-adapter. OPENCODE_ADAPTER_PAIRS (L484-497) pairs manifest/script/test mirrors only — explicitly excludes template/.opencode/** per Q9 YAGNI comment.
- impact: pack-file drift under template/.opencode/ is enforced only by static marker 11 (manifest grep) and marker 12 (no-secrets grep), not by the parity CLI named in AC-6.
- remediation: defer to a future slice (US-0122..US-0126) when an active .opencode/ mirror exists; or add a subprocess invocation in marker 13 once python is on PATH. Not blocking because the manifest byte-identity gate (marker 11) + no-secrets gate (marker 12) cover the pack surface this slice owns.

### NB-3: triple-installer behavioral parity is grep-only (marker 14)

- severity: non-blocking
- ac_mapping: AC-5
- marker: 14 (test_us0121_triple_installer_host_parity)
- issue_key: ik_us0121_py_only_behavioral_triple_grep (execute-critic row 18)
- evidence: markers 1-10 subprocess-invoke installer.py only. Marker 14 is static grep asserting host_gates_cursor_row / Host-GatesCursorRow / --host / -InstallHost / 5 diagnostic strings exist in installer.ps1, installer.sh, installer.py, bin/its-magic.js. No test exercises PS -InstallHost duplicate argv enforcement (L30-38 $args rescan), sh --host forwarding, or JS -InstallHost bridge at runtime.
- impact: PS/sh behavioral parity is YAGNI-deferred to manual QA. Marker 14 names "triple-installer parity" but enforces source presence only.
- remediation: defer to manual QA runbook (US-0126) or add PS/sh subprocess markers once python+pwsh+bash are all on PATH. Not blocking because the source-level contract is locked and the predicate is shared.

### NB-4: symmetric CURSOR_* shrink diagnostics grep-only (markers 8-9)

- severity: non-blocking
- ac_mapping: AC-3, AC-7
- markers: 8, 9 (behavioral, opencode-shrink only) + 14 (static grep for all 5 diagnostics)
- evidence: markers 8-9 cover OPENCODE_ORPHANED_BY_CLEAN_CURSOR / OPENCODE_STALE_BY_UPGRADE_CURSOR only (shrink both → cursor). The symmetric CURSOR_ORPHANED_BY_CLEAN_OPENCODE / CURSOR_STALE_BY_UPGRADE_OPENCODE (shrink both → opencode) are grep-only in marker 14 (L300-304). installer.py L170-174 and L1084-1088 emit them; installer.ps1 L142 and L773 emit them; installer.sh L183 and L670 emit them.
- impact: shrink-to-opencode behavioral path is untested at runtime.
- remediation: defer to a future slice or add markers 15-16 (would break the locked 14-marker budget per ik_us0121_ac9_help_test_yagni / ik_us0121_plan_verify_phantom_coverage). Not blocking because the source contract is present and symmetric.

## Compose guards (5/5 UNCHANGED — verified read-only)

| Compose target | Verification | Result |
|---|---|---|
| US-0008 (CLI installer) | additive --host only; missing/overwrite/clean/upgrade semantics UNCHANGED | read-only |
| DEC-0045 (its_magic/ ownership) | its_magic/ ownership unchanged | read-only |
| US-0102 (volatile-ID rule) | template ships no vendor slugs; *.local.json{,c} gitignore mirrors kit convention | read-only |
| US-0001 (phase names) | placeholders only; no command body clone | read-only |
| US-0018 (packaging delivery) | installer delivery path unchanged except additive --host forward | read-only |

## UAT probe classification (US-0092 / DEC-0078)

- story kind: CLI installer + template pack (not a web app).
- probe class: **contract/CLI** (per orchestrator brief).
- HTTP origin: none.
- UAT_PROBE_NOT_APPLICABLE — no browser UAT required. Automatable probe = CLI pytest (tests/us0121_host_mode_test.py) + parity CLI (scripts/check_intake_template_parity.py --scope=opencode-adapter). Both deferred to a python-on-PATH environment (see NB-1).
- Not UAT_PROBE_UNRESOLVED — the probe maps cleanly to CLI contract tests; only the runtime is unavailable.

## Decision gate

- decision_gate=true (blocking finding B-1 open)
- next_scheduled_phase=/execute (auto-implementation loop; AUTO_IMPLEMENTATION_LOOP=1)
- stop_condition=STOP after qa; do not spawn /execute or /verify-work. Hand off via artifacts only.

## Isolation evidence (US-0048 / DEC-0029 / US-0104 v2)

- phase_id=qa
- role=qa
- fresh_context_marker=qa-US0121-qa-20260823T114000Z-fresh
- timestamp=2026-08-23T11:40:00Z
- model_id=glm-5.2-high (CROSS_MODEL_REVIEW=1 — required)
- evidence_ref=sprints/S0121/qa-findings.md + handoffs/qa_to_dev.md
- next_scheduled_phase=/execute (blocking finding open)
- stop_condition=STOP after qa; do not spawn next phase.

## Strict runtime proof (US-0056 / DEC-0038)

- runtime_proof_id=rp-auto-20260823-01-qa-qa-20260823T114000Z-US-0121
- orchestrator_run_id=auto-20260823-01
- phase_id=qa, role=qa, story_id=US-0121, sprint_id=S0121
- delivery_mode=ultra_lean, macro_phase=build+verify
- proof_issued_at=2026-08-23T11:40:00Z
- proof_ttl_seconds=3600
- proof_hash=457664171B3FF0771957E71785576B14B39C66F3F988066A82904BFB177BAB78 (SHA-256, UTF-8 bytes via PowerShell — python not on PATH)
- Canonical payload (sorted-key JSON per DEC-0038): {"delivery_mode":"ultra_lean","macro_phase":"build+verify","orchestrator_run_id":"auto-20260823-01","phase_id":"qa","proof_issued_at":"2026-08-23T11:40:00Z","proof_ttl_seconds":3600,"role":"qa","runtime_proof_id":"rp-auto-20260823-01-qa-qa-20260823T114000Z-US-0121","sprint_id":"S0121","story_id":"US-0121"}
- proof_ttl=2026-08-23T12:40:00Z (1-hour TTL)

## Stop condition

STOP after qa. Do not spawn /execute or /verify-work from this QA subagent (BUG-0006). Hand off via artifacts only: sprints/S0121/qa-findings.md + handoffs/qa_to_dev.md + docs/engineering/state.md isolation append + handoffs/resume_brief.md prepend. The orchestrator (AUTO_IMPLEMENTATION_LOOP=1) reroutes to /execute in a fresh dev subagent to close B-1.
