# Codebase Map

## Stack

| Aspect | Detail |
|--------|--------|
| Runtime | Node.js 20 (CLI wrapper only; actual logic is shell scripts) |
| Languages | JavaScript (CommonJS), PowerShell, Bash, Python 3, Ruby (Homebrew formulas), YAML (CI) |
| Build tools | None — no TypeScript, bundler, or compilation step |
| Package manager | npm (zero dependencies) |
| Test framework | Custom shell-based test runners (`tests/run-tests.ps1`, `tests/run-tests.sh`) |
| CI/CD | GitHub Actions (`ci.yml`, `deploy.yml`) |
| Distribution | npm, Chocolatey, Homebrew |
| License | MIT |

## Entry Points

| Entry | File | Purpose |
|-------|------|---------|
| CLI binary | `bin/its-magic.js` | Parses CLI args, delegates to OS-specific installer via `child_process.spawnSync` |
| Postinstall | `bin/postinstall.js` | Prints ASCII banner on `npm install` |
| Windows installer | `installer.ps1` | File-copy installer (PowerShell, 304 lines) |
| Unix installer | `installer.sh` | File-copy installer (Bash, 302 lines) |
| Fallback installer | `installer.py` | File-copy installer (Python, 294 lines) |

All three installers implement identical logic: copy `template/` files to a target repo with modes `missing` (default), `overwrite`, or `interactive`, plus optional backup and `--clean-repo`.

## Key Modules

### Core CLI

| File | Purpose |
|------|---------|
| `bin/its-magic.js` | Detects OS, parses `--target`, `--mode`, `--backup`, `--create`, `--clean-repo`, `--yes`, `--help`, `--version`; spawns the matching installer |
| `bin/postinstall.js` | npm lifecycle hook; welcome banner |
| `installer.ps1` | Full installer for Windows (file listing, modes, backup, cleanup, prompts) |
| `installer.sh` | Full installer for macOS/Linux (identical feature set) |
| `installer.py` | Fallback installer using Python stdlib only |

### Template Payload (86 files in `template/`)

The installed content for target repos:

| Directory | Contents |
|-----------|----------|
| `.cursor/commands/` | 19 slash commands (intake, discovery, research, architecture, sprint-plan, plan-verify, execute, qa, verify-work, release, pause, resume, refresh-context, auto, quick, milestone-start, milestone-complete, map-codebase, phase-context) |
| `.cursor/rules/` | 5 AI behavior rules (core, quality, coding-standards, handoffs, escalation) |
| `.cursor/agents/` | 6 subagent definitions (dev, qa, po, tech-lead, curator, release) |
| `.cursor/skills/its-magic/` | SKILL.md + 14 JSON/MD templates |
| `.cursor/hooks/` | hook.py + hooks.json + README.md |
| `docs/product/` | vision.md, backlog.md, acceptance.md |
| `docs/engineering/` | architecture.md, state.md, research.md, runbook.md, decisions.md, codebase-map.md, dependencies.json, context/phase-template.json |
| `sprints/S0001/` | sprint.md, tasks.md, progress.md, summary.md, qa-findings.md, uat.md, uat.json, plan-verify.json |
| `sprints/quick/Q0001/` | task.json, summary.md |
| `handoffs/` | 6 handoff templates (dev_to_qa, qa_to_dev, po_to_tl, tl_to_dev, release_notes, resume_brief) |
| `decisions/` | DEC-0001.md, DEC-0002.md |
| `scripts/` | validate-and-push.ps1, validate-and-push.sh |
| `.github/workflows/` | ci.yml, deploy.yml |

### Release & Distribution

| File | Purpose |
|------|---------|
| `scripts/release-all.ps1` | Unified release: version bump + npm + GitHub release + Chocolatey + Homebrew (Windows) |
| `scripts/release-all.sh` | Same for Unix |
| `scripts/generate-release-notes.ps1` | Auto-generate release notes from sprint artifacts |
| `scripts/generate-release-notes.sh` | Same for Unix |
| `packaging/chocolatey/its-magic.nuspec` | Chocolatey package manifest |
| `packaging/chocolatey/tools/chocolateyInstall.ps1` | Choco install script |
| `packaging/chocolatey/tools/chocolateyUninstall.ps1` | Choco uninstall script |
| `packaging/homebrew/its-magic.rb` | Stable Homebrew formula |
| `packaging/homebrew/its-magic-beta.rb` | Beta Homebrew formula |

### Tests & Benchmarks

| File | Purpose |
|------|---------|
| `tests/run-tests.ps1` | PowerShell test runner: validates template structure, command sections, runbook keys, installer smoke test |
| `tests/run-tests.sh` | Bash equivalent |
| `benchmarks/run-bench.ps1/.sh` | Scenario-based validation benchmarks |
| `benchmarks/live/` | Live benchmark via hook telemetry |
| `benchmarks/headless/` | Headless benchmark via Cursor CLI |
| `benchmarks/prompts/` | Prompted benchmark replay |
| `benchmarks/auto-run/` | Automated benchmark orchestration |

### CI/CD Workflows

| Workflow | Triggers | Jobs |
|----------|----------|------|
| `ci.yml` | Push to main, PRs, manual | `checks` (test/lint/typecheck from runbook), `auto-fix` (retry loop, gated by `CI_AUTO_FIX`), `npm-test` (pack + smoke), `brew-test` (macOS formula), `choco-test` (Windows package) |
| `deploy.yml` | Manual dispatch | Reads `DEPLOY_STAGING_COMMAND` or `DEPLOY_PROD_COMMAND` from runbook |

## Directory Tree

```text
its-magic/
├── bin/
│   ├── its-magic.js              CLI entry point
│   └── postinstall.js            npm postinstall banner
├── installer.ps1                 Windows installer
├── installer.sh                  Unix installer
├── installer.py                  Python fallback installer
├── template/                     86 files — payload installed into target repos
│   ├── .cursor/commands/         19 slash commands
│   ├── .cursor/rules/            5 AI behavior rules
│   ├── .cursor/agents/           6 subagent definitions
│   ├── .cursor/skills/           Skill + templates
│   ├── .cursor/hooks/            Hook scripts
│   ├── docs/                     Product + engineering docs
│   ├── sprints/                  Sprint starters
│   ├── handoffs/                 Handoff templates
│   ├── decisions/                Decision record starters
│   ├── scripts/                  validate-and-push scripts
│   └── .github/workflows/        CI/CD templates
├── scripts/                      Release & helper scripts
├── packaging/
│   ├── chocolatey/               Nuspec + install/uninstall
│   ├── homebrew/                 Stable + beta formulas
│   └── npm/                      Local test scripts
├── tests/                        Shell-based test suite
├── benchmarks/                   Scenario, live, headless, prompted benchmarks
├── milestones/                   Milestone tracking
├── .cursor/                      Active dev Cursor config (mirrors template/)
├── docs/                         Active engineering + product docs
├── sprints/                      Active sprint tracking
├── handoffs/                     Active handoff artifacts
├── decisions/                    Active decision records
├── .github/workflows/            Active CI/CD workflows
└── package.json                  npm manifest (v0.1.2-17)
```

## Conventions

- **Artifact-first memory:** All critical state persists in files, never only in chat. `docs/engineering/state.md` is the single source of truth for project status.
- **Decision gates:** High-impact changes trigger `decisions/DEC-xxxx.md` and pause execution until resolved.
- **Handoff-driven workflow:** Every role-to-role transfer uses `handoffs/*.md`.
- **Pause/resume as first-class:** `handoffs/resume_brief.md` captures next actions; the curator agent keeps context compact.
- **Runbook-driven tooling:** `docs/engineering/runbook.md` defines all test/lint/typecheck/deploy commands — scripts, CI, and agents all read from it.
- **Configuration layering:** Shared defaults in `scratchpad.md` (committed), personal overrides in `scratchpad.local.md` (gitignored); hook merges both (local wins).
- **Triple installer parity:** PowerShell, Bash, and Python installers implement identical logic.
- **Self-dogfooding:** The repo uses its own its-magic workflow (active `.cursor/`, `docs/`, `sprints/`, `handoffs/`, `decisions/` alongside the `template/` copies).
- **Zero dependencies:** No npm dependencies; Node.js is only a delivery mechanism for the CLI wrapper.
- **Multiplatform distribution:** npm (global/npx), Chocolatey (Windows), Homebrew (macOS/Linux) — unified release scripts handle all three.
- **3-layer quality chain:** (1) Cursor AI loop (in-editor), (2) validate-and-push (local pre-push), (3) CI auto-fix (GitHub Actions).

## Agent Roles

| Agent | Role | Key Outputs |
|-------|------|-------------|
| PO | Clarify requirements, persist stories | `docs/product/*`, `handoffs/po_to_tl.md` |
| Tech Lead | Architecture, risks, sprint plan | `docs/engineering/architecture.md`, `decisions.md`, `sprints/S0001/*`, `handoffs/tl_to_dev.md` |
| Dev | Implement tasks, maintain artifacts | Code, `sprints/S0001/summary.md`, `handoffs/dev_to_qa.md` |
| QA | Validate acceptance, report findings | `sprints/S0001/qa-findings.md`, `handoffs/qa_to_dev.md` |
| Release | Prepare release notes, runbook | `handoffs/release_notes.md`, `runbook.md` |
| Curator | Compact context, refresh artifacts | `state.md`, `decisions.md`, `resume_brief.md` |

## Hooks

| Event | Behavior |
|-------|----------|
| `beforeShellExecution` | Blocks dangerous commands (`rm -rf /`, `del /f /s`, `format`, `mkfs`, `diskpart`, `shutdown`, piped curl-to-shell) |
| `beforeReadFile` | Warns on secret-like files (`.env`, `id_rsa`, `.pem`, `.key`, `.p12`, `credentials.json`) |
| `afterFileEdit` | Tracks code changes vs. context refresh; persists to `hook-state.json` |
| `stop` | Reminds to refresh context when `MAGIC_CONTEXT_STRICT=1` and code changed but context not updated |
