# Release notes — Sprint S0070 / BUG-0008 (finalized)

**Released version (in-repo)**: `its-magic@0.1.2-41`  
**Release finalization**: `2026-04-05T22:30:00Z` (`orchestrator_run_id=auto-20260404-03`, strict proof `proof_hash=29228ef7c322aa74d21b8a354adf4c45bbb8d4c64c967ee9dd3d58f7e9b2bf02`)

## Summary

Fixes global Linux installs where a **CRLF** `installer-owned-paths.manifest` caused **`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`** because POSIX **`awk`** did not match **`[install_include_paths]\r`**.

## Operator-visible changes

- **`installer.sh`**: strip trailing **`\\r`** before manifest section matching (**`get_manifest_paths`**).
- **`.gitattributes`**: **`*.manifest text eol=lf`**.
- **`scripts/guard_installer_publish.py`** (+ **`template/`** parity): reject carriage returns in packaged manifest paths; **`prepublishOnly`** invokes the guard.
- **`installer.ps1`**: **`Get-ManifestSection`** trims CR for parity.
- **Regression**: **`tests/installer_manifest_crlf_bug0008_test.py`**; **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** **§26P2**.

## Upgrade

Operators on broken tarballs (e.g. **`its-magic@0.1.2-40`**) should install **≥ `0.1.2-41`** from registry after **`npm publish`**, or install from a local **`npm pack`** tarball built from this revision. See **README** “Global Linux install: empty `install_include_paths`” and **`docs/engineering/architecture.md`** **`# BUG-0008`**.

## Gate summary (US-0039)

- **Check-in test**: **PASS** — **`tests/report.md`** **793**/0 @ **2026-04-05T20:21:40Z**; **US-0071** metadata guard coverage **PASS** in harness.
- **QA**: **PASS** — **`sprints/S0070/qa-findings.md`** **PASS_WITH_DEFERRALS**; **AC-5** waived as **`DEFERRED_DEBIAN_E2E_NO_RUNTIME`** (no Debian/SSH runtime this cycle; documented in QA + UAT).
- **UAT**: **PASS** — **`sprints/S0070/uat.json`** **7**/7 **pass** (honest **UAT-5** waiver + **UAT-7** pre-release scope).
- **Isolation / strict proof**: **PASS** — per **`docs/engineering/state.md`** through **verify-work** + **release** checkpoint.
- **Publish**: **skipped** — **`RELEASE_PUBLISH_MODE=disabled`** (deterministic no-op; operator may publish later when mode allows).

## Run

- `start_command`: `powershell -ExecutionPolicy Bypass -File "tests/run-tests.ps1"` (canonical **`TEST_COMMAND`** from `docs/engineering/runbook.md`; includes **§26P2** **BUG-0008** module).
- `runtime_mode`: `local` (CLI / installer package; optional Debian global E2E when a runtime is available per **US-0086**).
- `runtime_context_ref`: `docs/engineering/runbook.md`

## Connect

- `service_url`: `n/a` (npm CLI package; no long-running HTTP service in this repo)
- `service_port`: `n/a`
- `health_endpoint`: **`its-magic --help`** / successful **`its-magic --target <repo> --mode missing`** after install (no **`[INSTALL_MANIFEST_ERROR]`** for manifest parse)

## Verify

1. `python scripts/guard_installer_publish.py` — **PASS** (no **CR** in packaged manifests).
2. `npm run prepublishOnly` — **PASS** (invokes **`guard:installer`**).
3. `python tests/installer_manifest_crlf_bug0008_test.py` — **PASS** when **`awk`** on **PATH** (else skipped per harness).
4. `python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance` — **`[BUG_VALIDATION_OK]`**.
5. Optional when Debian/SSH available: global **`npm install -g`** from **`npm pack`** or registry; **`cat -A`** on installed **`installer-owned-paths.manifest`** (no **`^M$`**); **`its-magic --target <repo> --mode missing`**.

`expected_health_signal`: No **`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`** for LF/CRLF-tolerant parse path; prepublish guard blocks **`\\r`** in shipped manifests.

## Credentials

- `credential_source_refs`: npm registry token via operator env / CI secret store only — **no** inline secrets. Use **`RELEASE_PUBLISH_MODE`** (`confirm` / `auto` / `disabled`) from merged **`.cursor/scratchpad.md`** when publishing.

## Known Issues

- **Registry**: **`npm publish`** not executed this boundary (**`RELEASE_PUBLISH_MODE=disabled`**). Operators must publish **`0.1.2-41`** when ready.
- **Debian global E2E**: **Not executed** this cycle (**`DEFERRED_DEBIAN_E2E_NO_RUNTIME`**); recommended follow-up when **US-0086** remote target exists.

## Deploy (staging / production)

- **Staging:** `DEPLOY_STAGING_COMMAND` from `docs/engineering/runbook.md` — `echo "No staging deploy target configured for this repository"`
- **Production:** `DEPLOY_PROD_COMMAND` from `docs/engineering/runbook.md` — `echo "No production deploy target configured for this repository"`
- **npm package:** **`npm publish`** only after **`npm run prepublishOnly`** **PASS**, registry auth, and **`RELEASE_PUBLISH_MODE`** not **`disabled`**.
