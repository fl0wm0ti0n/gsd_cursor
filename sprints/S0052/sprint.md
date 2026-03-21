# Sprint S0052

- Story: `US-0073`
- Goal: implement **Model B** scratchpad delivery (example-only default install with explicit **materialized** baseline where required), canonical merged precedence (local → baseline/materialized → example), fail-closed diagnostics with layer attribution, upgrade-safe behavior per **`DEC-0039`**, installer/CLI/`template/` parity, docs + regression matrix — per **`DEC-0055`**, architecture US-0073, **`R-0050`**, and backlog AC-1..AC-10.
- Status: **verify-work-pass** (QA + UAT closed; awaiting **`/release`**)

## Scope

- Canonical delivery policy documentation and enforcement aligned to **`DEC-0055`** (no silent missing-key inference; deterministic remediation).
- Command/loaders and installers (`installer.ps1`, `installer.sh`, `installer.py`, CLI) apply the same Model B semantics and merge order.
- Upgrade path (`its-magic --mode upgrade`) preserves user local scratchpad and applies framework example refresh consistently.
- Active/`template/` parity for scratchpad-related contracts and examples.
- README + runbook operator guidance (model, migration, actions).
- Regression coverage: clean install, legacy dual-file upgrade, missing baseline recovery, local override preservation, traceability to **`US-0018`** / **`US-0057`** / automation safety defaults (**AC-10**).
