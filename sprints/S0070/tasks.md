# Sprint S0070 Tasks

- **Bug**: `BUG-0008`
- **Sprint**: `S0070`
- **Governance**: `architecture.md` `# BUG-0008`; `R-0069`; `US-0045`; `US-0054`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Bump **`package.json`** version (and **`package-lock.json`** if present) per **US-0054** / team release policy so the published tarball reflects **BUG-0008** fixes | AC-1 |
| T-002 | done | Run **`npm pack`**; confirm tarball contains **`installer-owned-paths.manifest`** entries without CR bytes; run **`npm run prepublishOnly`** and **`python scripts/guard_installer_publish.py`** → **PASS** | AC-2 |
| T-003 | done | Optional: add short **operator-facing** note in **`README.md`** and/or **`docs/engineering/runbook.md`** — CRLF manifest symptom, mitigation, upgrade path from broken global version | AC-3 |
| T-004 | done | Run **`python tests/installer_manifest_crlf_bug0008_test.py`** **PASS**; verify **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** **§26P2** still wires the test (installer regression surface) | AC-4 |
| T-005 | deferred (operator) | **Debian** (or **`docker-dmz`**-equivalent) **global E2E**: **`npm install -g`** new version; **`cat -A`** on installed template manifest; **`its-magic ... --mode missing`** without **`[INSTALL_MANIFEST_ERROR]`**; record evidence refs — **not run in dev session**; exact steps in **`handoffs/dev_to_qa.md`** | AC-5 |
| T-006 | deferred (operator) | **`npm publish`** when eligible (**`RELEASE_PUBLISH_MODE`**) — **not executed** in-repo; draft **`handoffs/releases/S0070-release-notes.md`** added; **`handoffs/release_queue.md`** row **`S0070`** = **`planned`** (**`ready`** only after **`/verify-work`** per **US-0045**) | AC-6 |
| T-007 | partial | **`uat.json`** / **`uat.md`** updated with dev-verified rows; **`bug_issue_validate.py --check-acceptance`** **PASS**; **`tests/run-tests.ps1`** full harness **794/0** (**`RELEASE_TEST_FAILED`** remediated); **`release-findings.md`** still **PENDING** full verify-work/release; **`R-0069`** closure **only** when backlog **DONE** | AC-7 |

## Deterministic AC-to-task mapping

- AC-1 -> T-001
- AC-2 -> T-002
- AC-3 -> T-003
- AC-4 -> T-004
- AC-5 -> T-005
- AC-6 -> T-006
- AC-7 -> T-007
