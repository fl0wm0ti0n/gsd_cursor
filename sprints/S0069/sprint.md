# Sprint S0069

- **Story**: **`US-0084`**
- **Goal**: Ship **POSIX-safe, LF-correct** published **`installer.sh`** (and template parity where applicable), **layered CI/prepublish** guards (**`dash -n`** when available), **operator runbook** troubleshooting for dash/CRLF failures, **canonical dev/QA remote Linux docs** aligned to **`US-0064`** (**`release-targets.json`**, **`runtime-connectivity.md`**), **`scripts/remote_config_summary.py`** with **non-secret** output and **locked exit codes**, **execute/qa evidence cues** for **`REMOTE_EXECUTION=1`**, **security posture** (no credential material in repo or helper stdout), **active + `template/`** parity, **minimal E2E path** (Windows → WSL/SSH → tests), and **harness rows H1–H5** per **`docs/engineering/architecture.md`** **`# US-0084`**.
- **Status**: **OPEN** — **`sprints/S0069/plan-verify.json`** **PASS** (QA **`2026-04-04T19:15:00Z`**); next **`/execute`** (**dev**).

## Scope (sprint-local AC themes)

- **AC-1** - Published **`installer.sh`** (and packaged **`template/`** mirror if introduced) matches repo **POSIX-safe** unconditional startup; **LF** for shell entrypoints via **`.gitattributes`** and/or publish/CI scan (**architecture** **`# US-0084`**).
- **AC-2** - **Regression / CI**: fail closed on non-dash-safe **`installer.sh`** (extend **`tests/installer_shell_bug0004_test.py`**, optional **`dash -n`**, **`prepublishOnly`** as architecture directs).
- **AC-3** - **`docs/engineering/runbook.md`** (and/or developer docs): **`set: Illegal option -`**, **CRLF vs LF**, **`sh` vs `bash`**, remediation (**dos2unix**, reinstall).
- **AC-4** - **Canonical remote profile doc**: **WSL**, bare **SSH**, **Docker-over-SSH** → **`release-targets.json`** / **`runtime-connectivity.md`**; **`REMOTE_EXECUTION`**, **`REMOTE_CONFIG`**, **`.cursor/remote.json`**.
- **AC-5** - **`scripts/remote_config_summary.py`**: validate **`REMOTE_CONFIG`** / template; **non-secret** summary; deterministic **exit codes** (**0–5** per architecture).
- **AC-6** - **`/execute`** / **`/qa`** handoffs or runbook: **`REMOTE_EXECUTION=1`** — where to run tests; **environment label** in evidence; **no secret leakage**.
- **AC-7** - **Security**: no credentials in repo; SSH secrets only via **agent / env** indirection; helper prints **names/path refs** only (**R-0067**).
- **AC-8** - **Active + `template/`** parity for new commands, scratchpad examples, **`.cursor/remote.json`** snippets, runbook sections touched by this sprint.
- **AC-9** - **Minimal E2E** documented path: Windows dev → **WSL** or **SSH Linux** → **`its-magic` / tests** using sprint artifacts.
- **AC-10** - **`tests/run-tests.sh`** / **`tests/run-tests.ps1`**: register **H1–H5** (installer LF/tokens, optional **`dash -n`**, helper fixtures **valid / invalid JSON / schema mismatch**).

## Governance

- `docs/engineering/architecture.md` `# US-0084`
- `docs/engineering/research.md` `R-0067`
- Related: **`US-0045`**, **`US-0064`**, **`US-0036`**, **`BUG-0004`**
