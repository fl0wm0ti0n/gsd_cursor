# Sprint S0054 Tasks

- Story: `US-0075`
- Sprint: `S0054`
- Governance: **`DEC-0057`** (example-first ordering + **AC-11** paired catalog parity); related **`DEC-0039`** (example refresh + user-local preservation), **`DEC-0055`** (Model B merge precedence unchanged)

| Task | Status | Description | AC |
|---|---|---|---|
| T-001 | done | Document and wire **deterministic ordering**: operator-visible catalog in **`.cursor/scratchpad.local.example.md`** / **`template/.cursor/scratchpad.local.example.md`**; materialized **`.cursor/scratchpad.md`** refresh must not introduce new documented keys **ahead of** example refresh in the same pipeline (**AC-1**) | AC-1 |
| T-002 | done | Ensure **`--mode upgrade`** and applicable fresh-install paths **always** refresh framework-owned **scratchpad.local.example** surfaces to match shipped template bytes unless a **documented exception** applies with a **reason code** (**AC-2**) | AC-2 |
| T-003 | done | When installers or CLI refresh **materialized** **`scratchpad.md`** from **`template/.cursor/scratchpad.md`**, implement the **same operation or an earlier deterministic step** that refreshes **scratchpad.local.example** from **`template/.cursor/scratchpad.local.example.md`** (no stale example + fresh baseline) (**AC-3**) | AC-3 |
| T-004 | done | Maintain **parity** across **`installer.ps1`**, **`installer.sh`**, **`installer.py`**, **`bin/its-magic.js`**, and **`docs/engineering/context/installer-owned-paths.manifest`** (+ **`template/`** mirror) for the ordering + refresh contract (**AC-4**) | AC-4 |
| T-005 | done | **Operator-visible diagnostics** that distinguish **example refresh**, **materialized baseline** actions, and **user local** preservation (**`.cursor/scratchpad.local.md`** never overwritten by framework refresh), with **DEC-0039**-aligned reason families (**AC-5**) | AC-5 |
| T-006 | done | **Regression tests**: upgrade with outdated example + current template; post-upgrade example matches template; **no** path leaves example older than template while **`scratchpad.md`** was updated (**AC-6**) | AC-6 |
| T-007 | done | Update **README** + **runbook**: copy new keys from **example** → **local**; how upgrade refreshes example; troubleshooting when drift is detected (**AC-7**) | AC-7 |
| T-008 | done | Maintain **active/template** parity for all scratchpad-related install surfaces (**AC-8**) | AC-8 |
| T-009 | done | **QA findings** for this story explicitly attest **example** and **template/example** alignment after upgrade simulation with cited evidence paths (**AC-9**) | AC-9 |
| T-010 | done | Document **deterministic remediation** if operators still see drift (re-run upgrade, manifest paths, compare to template) (**AC-10**) | AC-10 |
| T-011 | done | Implement **AC-11** **complete settings catalog parity**: same **##** section + **`KEY=`** sets on paired paths (active + template); machine-verified in **`tests/run-tests.*`**; default **full mirror**; **manifest-only** local-only exceptions (**AC-11**) | AC-11 |

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
- AC-11 → T-011
