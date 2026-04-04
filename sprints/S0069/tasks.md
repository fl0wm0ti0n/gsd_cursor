# Sprint S0069 Tasks

- **Story**: `US-0084`
- **Sprint**: `S0069`
- **Governance**: `architecture.md` `# US-0084`; `research.md` `R-0067`; `US-0045`

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | **Publish parity / LF**: root **`.gitattributes`** (`*.sh` **eol=lf** or equivalent); ensure **`installer.sh`** unconditional startup stays POSIX-only (**`set -e`** path); deterministic **`\r`** rejection or documented publish check so npm tarball matches repo (**AC-1**) | AC-1 |
| T-002 | done | **Guards**: extend **`tests/installer_shell_bug0004_test.py`** (forbidden tokens, **LF**); add **`dash -n installer.sh`** when **`dash`** on **PATH** (skip documented if absent); wire **CI** and/or **`package.json`** **`prepublishOnly`** per architecture layered stack (**AC-2**) | AC-2 |
| T-003 | done | **Runbook troubleshooting**: **`docs/engineering/runbook.md`** — **`set: Illegal option -`**, **CRLF**, **`sh` vs `bash`**, **`dos2unix`**, reinstall from fixed version; cross-link **`# US-0084`** installer rules (**AC-3**) | AC-3 |
| T-004 | done | **Remote profile documentation**: dev/QA-facing section(s) mapping **WSL** / **SSH** / **Docker-over-SSH** to **`docs/engineering/release-targets.json`** + **`docs/engineering/runtime-connectivity.md`**; **`REMOTE_EXECUTION`**, **`REMOTE_CONFIG`**, **`.cursor/remote.json`** (**AC-4**) | AC-4 |
| T-005 | done | **Helper**: implement **`scripts/remote_config_summary.py`** (**`--config`**, **`REMOTE_CONFIG`** default); **non-secret** stdout; **stderr** reasons; exit codes **0–5** as locked in architecture; record **REMOTE_EXECUTION=0** branch in **`decisions.md`** if chosen (**AC-5**) | AC-5 |
| T-006 | done | **Handoff / evidence cues**: update relevant **`handoffs/`** templates or runbook bullets for **`REMOTE_EXECUTION=1`** — local vs remote test locus, **environment label** in evidence, no pasted secrets (**AC-6**) | AC-6 |
| T-007 | done | **Security pass**: verify no credentials committed; helper and docs use **env var names** / **identity path strings** only — never key material or resolved secret **values**; align with existing remote policy (**AC-7**) | AC-7 |
| T-008 | done | **`template/` parity**: mirror active changes — commands, scratchpad examples, **`.cursor/remote.json`** template snippets, runbook excerpts the kit ships (**AC-8**) | AC-8 |
| T-009 | done | **E2E sanity doc**: minimal “Windows → WSL or SSH Linux → run **`its-magic` / tests**” walkthrough referencing **`S0069`** artifacts and **US-0064** targets (**AC-9**) | AC-9 |
| T-010 | done | **Harness**: register **H1–H5** in **`tests/run-tests.sh`** and **`tests/run-tests.ps1`** (installer checks, **`dash -n`** when available, helper fixtures for **0 / 3 / 4** exits per architecture) (**AC-10**) | AC-10 |

## Deterministic AC-to-task mapping

- AC-1 → T-001
- AC-2 → T-002
- AC-3 → T-003
- AC-4 → T-004
- AC-5 → T-005
- AC-6 → T-006
- AC-7 → T-007
- AC-8 → T-008
- AC-9 → T-009
- AC-10 → T-010
