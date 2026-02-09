# Engineering State (compacted 2026-02-06)

## Session status
- **PAUSED** — checkpoint 2026-02-06

## Progress snapshot
- **Sprint S0001** — v1.0.0 released; all 22 tasks delivered; all phases complete (arch → plan → dev → QA → release)
- **QA:** 20 PASS / 2 FAIL / 1 WARN — 0 critical/blocking
- **Artifact:** reference app in `examples/webview-app/` (Express + SPA)

## Known issues (carry-forward)

| ID    | Severity | Summary                                                      |
|-------|----------|--------------------------------------------------------------|
| F-001 | Medium   | Silent failure on item detail fetch — needs visible feedback |
| F-002 | Medium   | Non-JSON error responses crash `apiFetch` — needs try/catch  |
| F-003 | Low      | No loading/spinner state during API calls                    |
| F-004 | Low      | Category filter values not validated on backend              |
| F-005 | Low      | Soft-delete confirmation implies restore but no restore UI   |

## Key risks
- `/shared` must build before FE/BE in CI (schema drift)
- CORS misconfiguration between SPA origin and API origin
- SQLite → PostgreSQL dialect gaps at migration time

## Git (at checkpoint)
- HEAD `8ddc68a` on `main`; 20 modified + 7 untracked; remote in sync at HEAD

## Next actions
1. Fix F-001, F-002 (medium) in S0002
2. Groom F-003–F-005 into backlog
3. Plan S0002 sprint scope
4. Commit working tree changes when ready
