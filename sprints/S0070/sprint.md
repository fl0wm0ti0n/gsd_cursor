# Sprint S0070

- **Bug**: `BUG-0008`
- **Goal**: Close **CRLF `installer-owned-paths.manifest`** / empty **`install_include_paths`** on Linux global **npm** after in-repo mitigations: **semver bump**, **publish sanity** (**`npm pack`** / **`prepublishOnly`** / **`guard_installer_publish`**), optional **operator README** note, **26P2** regression proof, **Debian global E2E** per **`docs/engineering/architecture.md`** **`# BUG-0008`**, then **verify-work / release** traceability (**`R-0069`** delivery closure only when backlog marks **DONE** per **US-0045**).
- **Status**: **Released** — **`/release`** finalized **`2026-04-05T22:30:00Z`**; **`handoffs/release_queue.md`** **S0070** **`released`**; **`BUG-0008`** **DONE**; **`docs/product/acceptance.md`** **BUG-0008** checked; **`R-0069`** delivery-closed in **`docs/engineering/research.md`**. **Publish** skipped (**`RELEASE_PUBLISH_MODE=disabled`**). Next: **`/refresh-context`** (curator).

## Scope (sprint-local AC themes)

- **AC-1** - **`package.json`**: semver **version bump** per release policy (**US-0054**); update **`package-lock.json`** if versioned in-repo.
- **AC-2** - **Publish sanity**: **`npm pack`** (inspect tarball: **`installer-owned-paths.manifest`** paths LF / no **`\\r`**); **`npm run prepublishOnly`** (or repo-documented equivalent) **PASS**; **`python scripts/guard_installer_publish.py`** **PASS** on active + **`template/`** surfaces.
- **AC-3** - **Optional operator note**: **`README.md`** and/or **`docs/engineering/runbook.md`** — symptom (**`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`** on global Linux), fix shipped in this line, upgrade away from broken **`its-magic@0.1.2-40`** (or current bad tarball).
- **AC-4** - **QA harness 26P2**: run **`python tests/installer_manifest_crlf_bug0008_test.py`** **PASS**; confirm **`tests/run-tests.sh`** / **`tests/run-tests.ps1`** section **26P2** invokes the module (no harness drift).
- **AC-5** - **Debian global E2E** (per architecture / intake **done_definition**): **`npm install -g`** the **new** package version (or **`npm install -g`** from **`npm pack`** tarball on target); **`cat -A`** on installed **`.../template/docs/engineering/context/installer-owned-paths.manifest`** — no **`^M$`** line endings; **`its-magic --target <repo> --mode missing`** (or equivalent) **without** **`[INSTALL_MANIFEST_ERROR]`**; capture **`evidence_refs`** for **`handoffs/dev_to_qa.md`** / verify-work.
- **AC-6** - **`npm publish`**: execute per merged **`RELEASE_PUBLISH_MODE`** (**confirm** = operator confirmation gate); draft **`handoffs/releases/S0070-release-notes.md`** (**BUG-0008** bullets); align **`handoffs/release_queue.md`** when release workflow demands (**`ready`** at verify-work boundary per **US-0045**).
- **AC-7** - **Verify-work / release closure**: populate **`sprints/S0070/uat.json`** / **`sprints/S0070/uat.md`** against **AC-1..AC-7**; **`python scripts/bug_issue_validate.py --backlog docs/product/backlog.md --check-acceptance`** **PASS**; **`docs/engineering/research.md`** **`R-0069`** **delivery-closure stanza** only when **`BUG-0008`** → **DONE** (not before); **`sprints/S0070/release-findings.md`** at **`/release`**.

## Governance

- `docs/engineering/architecture.md` `# BUG-0008`
- `docs/engineering/research.md` `R-0069`
- Related: `US-0045`, `US-0054`, `US-0084`, `DEC-0068` (installer context)
