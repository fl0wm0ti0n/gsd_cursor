# PO to TL archive pack (2026-06-13)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=650, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 2
- Retained units in hot file: 10
- First archived heading: `## Orchestrated discovery handoff — US-0099 / auto-20260614-01`
- Last archived heading: `## Orchestrated intake handoff — US-0099`
- Verification tuple (mandatory):
  - archived_body_lines=122
  - retained_body_lines=635

---

## Orchestrated discovery handoff — US-0099 / auto-20260614-01

### Target

- `story_id=US-0099`
- `orchestrator_run_id=auto-20260614-01`
- phase completed: **`discovery`** (**`po`**)
- `fresh_context_marker=po-US0099-discovery-20260614T150000Z-fresh`
- `next_scheduled_phase=research`
- `decomposition=single_story` (per **US-0051**)
- `priority=P2`
- `backlog_drain_active=true`
- `backlog_drain_stories_remaining_budget=8`

### Summary

- **`/discovery`** **PASS** — non-destructive **dev-environment profile auto-bootstrap** locked: copy **`template/.cursor/dev-environment.json.example`** → resolved path on **`missing`**, **`upgrade`**, and **npm postinstall** when target absent; **never** overwrite operator-customized profiles. Completes install-time gap left by **US-0098** / **DEC-0084** (schema + execute step **24** unchanged).
- **`remote.json`** stays manual-seed (opt-in remote, default-off); **`dev-environment.json`** auto-bootstrap because **`DEV_AUTO_LAUNCH_PROFILE`** gate expects loadable file when enabled.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Discovery locks (research inputs)

| Lock | Decision |
|------|----------|
| **Hook timing** | After **`run_scratchpad_postinstall`** on **`missing`** + **`upgrade`**; before **`bootstrap_runbook_commands`** |
| **Hook surface** | **`bootstrap_dev_environment_profile()`** in **`dev_environment_lib.py`**; **`installer.py`** + PS1/SH delegate |
| **Source** | **`template/.cursor/dev-environment.json.example`** only — never synthesize JSON |
| **Target path** | Merged scratchpad **`DEV_ENVIRONMENT_CONFIG`** when parseable repo-relative, else **`.cursor/dev-environment.json`** |
| **Skip semantics** | Target exists → skip only; no byte-compare merge |
| **Reason family** | **`DEV_ENV_BOOTSTRAP_*`** (install-time) distinct from **`DEV_ENV_PROFILE_*`** (runtime) |
| **npm postinstall** | **`bin/postinstall.js`** same contract as installer |
| **Manifest** | Local profile **not** in **`install_paths`**; example committed under **`template/`** |
| **Runbook UX** | Bootstrap automatic; manual copy demoted to **customize-after-bootstrap** |
| **Governance** | Amend **DEC-0084** (not new DEC); architecture **`# US-0099`** |
| **Tranche order** | A helper + codes → B installer → C postinstall → D runbook/tests/parity |

### Acceptance pointers (discovery emphasis)

- **AC-1**: Copy-when-missing on installer **`missing`** + **`upgrade`** with deterministic log line.
- **AC-2**: Skip-when-exists — **`DEV_ENV_BOOTSTRAP_SKIPPED_EXISTS`**; operator prose preserved.
- **AC-3**: Path resolution from merged **`DEV_ENVIRONMENT_CONFIG`**; **`DEV_ENV_BOOTSTRAP_PATH_INVALID`** fail-closed.
- **AC-4**: **`bin/postinstall.js`** npm parity; idempotent re-run.
- **AC-5**: Example names-only (**US-0085**); local file gitignored (**DEC-0084** unchanged).
- **AC-6**: Runbook customize-after-bootstrap; **`DEV_ENV_PROFILE_MISSING`** troubleshooting references bootstrap.
- **AC-7..AC-8**: **`test_us0099_*`** + parity scope; architecture + **DEC-0084** amendment.

### Top risks (carry to /research)

- **R1**: Postinstall global-install cwd — scratchpad unreadable → default path only; document edge case.
- **R2**: Accidental overwrite on upgrade — skip-if-exists must not compare bytes or merge.
- **R3**: User-visible log strings leak planning IDs — **DEC-0053** scan on installer/postinstall surfaces.

### Research asks (extend **`R-0086`**)

1. Close Q5 — helper CLI (`--bootstrap`, exit codes, log tokens).
2. Close Q6 — contract-test marker inventory + **`DEV_ENVIRONMENT_PAIRS`** delta.
3. Close Q7 — idempotency matrix (mode × exists × path override).
4. Close Q2 residual — postinstall subprocess vs inline Node invocation contract.

### Evidence refs

- `docs/product/vision.md` (**`## Discovery Notes — US-0099`**)
- `docs/product/backlog.md` (`## US-0099` — `discovery_notes` appended)
- `docs/engineering/research.md` (**`R-0086`** — discovery extension)
- `handoffs/intake_evidence/US-0099-intake-20260614.json`
- `scripts/dev_environment_lib.py`, `installer.py`, `bin/postinstall.js`
- `decisions/DEC-0084.md`
- `docs/engineering/state.md` (Discovery checkpoint — this run)
- `handoffs/resume_brief.md` (top pointer → `/research`)

### Next

- **`/research`** (fresh **tech-lead** context) for **`US-0099`** — close **`R-0086`** Q5–Q7 + postinstall contract; architecture readiness.

### Decision gate

- **None** — discovery satisfied; research readiness explicit.

---

## Orchestrated intake handoff — US-0099

### Target

- `story_id=US-0099`
- `intake_run_id=cursor-20260614-US0099-intake`
- phase completed: **`intake`** (**`po`**)
- `next_scheduled_phase=discovery`
- `decomposition=single_story` (per **US-0051**)
- `priority=P2`
- `research_anchor=R-0086` (stub — extend in **`/discovery`**)

### Summary

- **`/intake`** **PASS** — **`small-intake-pack`** from operator thread: missing **`.cursor/dev-environment.json`** after its-magic update despite **`DEV_ENVIRONMENT_CONFIG`** and **`DEV_AUTO_LAUNCH_PROFILE=deterministic_v1`**.
- **Scope**: non-destructive **copy-when-missing** of **`template/.cursor/dev-environment.json.example`** → resolved profile path on **`missing`**, **`upgrade`**, and **npm postinstall**; **never** overwrite existing operator profiles.
- **Composes**: **US-0098** / **DEC-0084** (schema unchanged), **US-0018** smart upgrade, **US-0085** names-only example.
- Status authority: **OPEN** per **US-0045**; closure at `/release`.

### Acceptance highlights (8 ACs)

| AC | Theme |
|----|-------|
| AC-1 | Copy-when-missing on installer missing + upgrade |
| AC-2 | Never overwrite existing profile |
| AC-3 | Path resolution via **`DEV_ENVIRONMENT_CONFIG`** |
| AC-4 | **`bin/postinstall.js`** npm parity |
| AC-5 | Example names-only; local file gitignored |
| AC-6 | Runbook customize-after-bootstrap |
| AC-7 | **`test_us0099_*`** + parity scope |
| AC-8 | Architecture + **`DEC-xxxx`** amends **DEC-0084** |

### Discovery asks

- Survey installer/postinstall hooks vs **`remote.json`** bootstrap patterns.
- Lock reason-code family (**`DEV_ENV_BOOTSTRAP_*`**).
- Confirm hook runs on **`npx its-magic`** consumer path.

**Next**: **`/discovery`** (fresh **PO**) for **`US-0099`**.

---

