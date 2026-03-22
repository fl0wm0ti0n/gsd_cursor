# Sprint S0054

- Story: `US-0075`
- Goal: eliminate **example lag** and **paired-surface skew** so upgrade/install always refreshes **`.cursor/scratchpad.local.example.md`** (and template mirror) **before or bundled with** materialized **`.cursor/scratchpad.md`** refresh; enforce **AC-11** **##** + **`KEY=`** set equality on active and template baseline ↔ example pairs; operator diagnostics and CI parity per **`DEC-0057`**, architecture **`# US-0075`**, **`R-0052`**, and backlog **AC-1..AC-11**.
- Status: **released** (post-**`/release`** for **S0054** / **US-0075**; **`orchestrator_run_id=auto-20260326-01`**)

## Scope

- Deterministic **ordering** documentation and pipeline behavior — example/catalog never trails baseline refresh (**AC-1**, **AC-3**).
- **`--mode upgrade`** and applicable install paths always refresh framework-owned **scratchpad.local.example** to shipped template bytes unless a documented exception + reason code applies (**AC-2**).
- **Cross-surface parity**: **`installer.ps1`**, **`installer.sh`**, **`installer.py`**, **`bin/its-magic.js`**, **`docs/engineering/context/installer-owned-paths.manifest`** (+ **`template/`** mirror) (**AC-4**, **AC-8**).
- **Diagnostics** distinguishing example refresh, materialized baseline, and user **`.cursor/scratchpad.local.md`** preservation (**DEC-0039** alignment) (**AC-5**, **AC-10**).
- **Regression tests** for stale-example vs fresh-template / baseline paths (**AC-6**).
- **README** + **runbook** operator guidance (**AC-7**).
- **QA attestation** of example alignment after upgrade simulation (**AC-9**).
- **Machine-enforced AC-11** parity gate in **`tests/run-tests.*`** (paired paths; manifest-documented local-only exceptions only).
