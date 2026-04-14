## QA -> Verify-Work Handoff -- US-0086 / S0074

> **2026-04-13T21:22:07Z** -- `/qa` complete (qa, `orchestrator_run_id=auto-20260405-01`). Story **US-0086** remains **OPEN** (US-0045). Sprint **S0074**. QA verdict: **PASS**. Ready for `/verify-work`.

### QA summary

- **Verdict**: PASS -- all 10 ACs verified; no new test failures; no blocking findings.
- **run-tests.ps1**: 788 pass, 6 fail (all pre-existing)
- **Contract tests**: 19 passed, 94 subtests
- **Remote summary tests**: 4 passed
- **Scratchpad pair parity**: SCRATCHPAD_PAIR_OK
- **Bug issue validation**: BUG_VALIDATION_OK (no regression evidence in QA scope)

### AC verification matrix

| AC | Result | Summary |
|----|--------|---------|
| AC-1 | PASS | Scratchpad automation-profile keys present in active + template surfaces |
| AC-2 | PASS | Manual vs automation mode split documented in runbook (active/template) |
| AC-3 | PASS | Deterministic routing behavior documented for mode-on/off in commands/rules |
| AC-4 | PASS | `start container <target_id>` intent and fail-closed reason codes documented |
| AC-5 | PASS | Names-only routing tuple guidance present in handoff/runbook references |
| AC-6 | PASS | Optional deterministic CI routing recipe documented |
| AC-7 | PASS | Security continuity (`.env` no-read, names-only secret posture) preserved |
| AC-8 | PASS | Routing contract regression tests pass (`auto_command_contract_test.py`) |
| AC-9 | PASS | Architecture lock consistency retained (US-0064/DEC-0070 alignment) |
| AC-10 | PASS | Active/template parity maintained across touched surfaces |

### Findings reference

- `sprints/S0074/qa-findings.md` -- full findings
- 6 pre-existing failures (installer stack-detection drift, strict-proof step-label drift, triad hot-surface oversize drift)
- 0 blocking findings

### Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-qa-qa-20260413T212207Z-S0074-US0086`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-13T21:22:07Z`
- `proof_ttl_seconds=3600`
- `proof_hash=520ee79f7f17c21d5888306add1967b4b96701cc439cf7dd521e54857ee8c3e9`

### Remote-routing evidence tuple (names-only)

- `target_id=local-default`
- `environment_label=local`
- `automation_profile=off`
- `routing_source=local_default`
- `secret_surface=names_only`

### Next

- `/verify-work` (fresh qa subagent) for S0074 / US-0086

## QA -> Verify-Work Handoff -- US-0085 / S0073

> **2026-04-13T15:00:00Z** -- `/qa` complete (qa, `orchestrator_run_id=auto-20260405-01`). Story **US-0085** remains **OPEN** (US-0045). Sprint **S0073**. QA verdict: **PASS**. Ready for `/verify-work`.

### QA summary

- **Verdict**: PASS -- all 10 ACs verified; no new test failures; no blocking findings.
- **pytest**: 56 passed, 4 skipped, 0 failed
- **run-tests.ps1**: 790 pass, 4 fail (all 4 pre-existing from prior sprints)
- **Contract tests**: 17 passed, 66 subtests
- **New tests (AC-9)**: 4/4 passed (`test_env_gitignore.py`)
- **Parity helper (AC-8)**: Parity PASS (20/20 names)
- **remote_config_summary.py (AC-10)**: exit 0 (no regression)
- **Triad hot surface**: PASS
- **User-visible metadata**: PASS
- **Scratchpad pair parity**: SCRATCHPAD_PAIR_OK
- **Bug issue validation**: BUG_VALIDATION_OK

### AC verification matrix

| AC | Result | Summary |
|----|--------|---------|
| AC-1 | PASS | `.gitignore` + `template/.gitignore` with `.env*` patterns and `!.env.example` negation |
| AC-2 | PASS | `.cursorignore` + `template/.cursorignore` with `.env*` agent exclusion |
| AC-3 | PASS | `.env.example` + `template/.env.example` with 20 names only, no values |
| AC-4 | PASS | `runbook.md` + template has `.env` setup section with forbidden/allowed guidance |
| AC-5 | PASS | `runtime-connectivity.md` + template references `.env` sourcing |
| AC-6 | PASS | `us-0084-remote-e2e.md` + template references `.env` in Path B/C |
| AC-7 | PASS | `coding-standards.mdc` + template has `.env` exclusion rule |
| AC-8 | PASS | `print_remote_env_hint.py` prints names only, parity 20/20 |
| AC-9 | PASS | `test_env_gitignore.py` 4/4 regression tests pass |
| AC-10 | PASS | `remote_config_summary.py` + tests remain PASS |

### Findings reference

- `sprints/S0073/qa-findings.md` -- full findings
- 4 pre-existing failures (documented in `sprints/S0072/qa-findings.md`)
- 0 blocking findings

### Strict runtime proof

- `orchestrator_run_id=auto-20260405-01`
- `runtime_proof_id=rp-auto-20260405-01-qa-qa-20260413T150000Z-S0073-US0085`
- `phase_id=qa`
- `role=qa`
- `proof_issued_at=2026-04-13T15:00:00Z`
- `proof_ttl_seconds=3600`
- `proof_hash=48d92b6e080de07ac3df161aa42e0ec4ddda987089d4c3a2e06f3ff5d750a196`

### Next

- `/verify-work` (fresh qa subagent) for S0073 / US-0085

### Remote-routing evidence tuple contract (US-0086 / AC-5)

For any QA cycle that uses automation remote routing, include names-only tuple
evidence in this handoff:

- `target_id`
- `environment_label`
- `automation_profile`
- `routing_source`
- `secret_surface=names_only`

When routing is not used, record local-default values rather than omitting the
tuple (`target_id=local-default`, `environment_label=local`,
`automation_profile=off`, `routing_source=local_default`).
