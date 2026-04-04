# QA findings — S0069 / US-0084

**Orchestrator run id:** `auto-20260404-02`  
**Verdict:** **PASS**

## Test plan

1. **Installer POSIX / LF / forbidden tokens (AC-2, architecture `# US-0084`)** — `python tests/installer_shell_bug0004_test.py`
2. **Remote config summary helper + exit codes (AC-5, AC-10 H3–H5)** — `python tests/remote_config_summary_test.py`
3. **Prepublish guard stack** — `python scripts/guard_installer_publish.py`
4. **Template / intake script parity** — `python scripts/check_intake_template_parity.py --repo .`
5. **Triad hot surface (DEC-0054)** — `python scripts/enforce-triad-hot-surface.py --check`
6. **Spot (dev handoff, installer adjacent)** — `python tests/installer_completeness_bug0003_test.py`

## Command outcomes

| Command | Outcome | Notes |
|--------|---------|--------|
| `python tests/installer_shell_bug0004_test.py` | **PASS** | 5 tests, 3 skipped on this host (documented); LF + token checks exercised |
| `python tests/remote_config_summary_test.py` | **PASS** | 4 tests — fixtures for exits **0** / **3** / **4** per AC-10 |
| `python scripts/guard_installer_publish.py` | **PASS** | `dash` not on PATH; skip documented; Python CRLF + token path enforced |
| `python scripts/check_intake_template_parity.py --repo .` | **PASS** | `[INTAKE_TEMPLATE_PARITY_OK]` |
| `python scripts/enforce-triad-hot-surface.py --check` | **PASS** | After QA **`state.md`** append: first check **FAIL** (`ARTIFACT_HOT_SURFACE_OVERSIZE`); **`--rollover`** (`units=1`); final **`--check`** **PASS** |
| `python tests/installer_completeness_bug0003_test.py` | **PASS** | 3 tests — unrelated regression guard |

## Architecture / tasks / backlog

- **`docs/engineering/architecture.md`** **`# US-0084`**: `.gitattributes` + LF policy, layered guards (`prepublishOnly` + Python + optional `dash -n`), runbook + remote map + helper contract + H1–H5 — **consistent with implemented artifacts** (spot-checked vs **`handoffs/dev_to_qa.md`**).
- **`sprints/S0069/tasks.md`**: **T-001..T-010** all **done** — matches sprint scope.
- **`docs/product/backlog.md`**: acceptance checkboxes for **US-0084** remain **unchecked** until **`/verify-work`** / canonical closure (**US-0045**); story **OPEN**.

## Coverage vs AC-1..AC-10 (summary)

| AC | Coverage note |
|----|----------------|
| **AC-1** | `.gitattributes` + byte-level rejection in tests; **`installer.sh`** POSIX startup preserved per BUG-0004 lineage |
| **AC-2** | Extended **`installer_shell_bug0004_test.py`** + **`guard_installer_publish.py`** + optional **`dash -n`** when available |
| **AC-3** | Spot-check: runbook **`REMOTE_EXECUTION`** / installer troubleshooting present (execute scope; not re-audited line-by-line in this run) |
| **AC-4** | **`runtime-connectivity.md`** / release-targets alignment documented in sprint summary + dev handoff |
| **AC-5** | **`remote_config_summary.py`** + **DEC-0070** (`REMOTE_EXECUTION=0` → exit **0**, skip stderr) |
| **AC-6** | Command/scratchpad cues per handoff list |
| **AC-7** | Helper + fixtures use env names / path refs only (reviewed via test expectations + architecture) |
| **AC-8** | Intake template parity gate **PASS** |
| **AC-9** | **`docs/engineering/us-0084-remote-e2e.md`** delivered in execute scope |
| **AC-10** | **`tests/run-tests.sh`** / **`.ps1`** rows **H1–H5** registered; Python tests validate H1 + H3–H5 directly |

## Findings

- **None blocking.** Optional note: **`dash`** absent on Windows runner — **H2** / guard skip path is **documented** and matches **R-0067** / architecture.

## Next phase

**`/verify-work`** (fresh **qa** context).
