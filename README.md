# Cursor-GSD-Team Kit

Drop-in template repo that implements a structured GSD workflow in Cursor:
intake -> discovery -> architecture -> sprint plan -> execute -> QA -> release,
with pause/resume, decision gates, and persistent artifacts.

## Quick start

1. Use `/gsd-intake` to capture the idea and kick off questions.
2. Continue with `/gsd-discovery`, `/gsd-architecture`, `/gsd-sprint-plan`.
3. Execute work with `/gsd-execute`, verify via `/gsd-qa`, finalize via
   `/gsd-release`.
4. Use `/gsd-pause` anytime and `/gsd-resume` to continue from artifacts.
5. Use `/gsd-refresh-context` to compact state and prevent context rot.

## Voice input (multilingual)

Voice is only an input layer. It produces text that feeds the same workflow:

- Option A: OS dictation (no setup, language support varies by OS)
- Option B: Cursor voice (if available)
- Option C: Local STT (whisper / whisper.cpp style dictation)

Recommended reliability pattern for slash commands:

- Bind a text expander or hotkey to insert `/gsd-intake ` (or any command).
- Dictate only the content after the command.

## CI/CD via runbook

Workflows in `.github/workflows/` read command keys from
`docs/engineering/runbook.md`. If a key is not set (or is a placeholder),
the workflow skips the step and exits successfully.

Supported keys:

- `TEST_COMMAND`
- `LINT_COMMAND`
- `TYPECHECK_COMMAND`
- `DEPLOY_STAGING_COMMAND`
- `DEPLOY_PROD_COMMAND`

## Installer / updater

Use one of the installers below to add this kit to an existing repo or
bootstrap an empty one:

- Windows: `gsd-installer.ps1`
- macOS/Linux: `gsd-installer.sh`
- Python fallback: `gsd-installer.py`

Modes:

- `missing` copies only files that do not exist
- `overwrite` replaces existing files
- `interactive` prompts per file

Backup option:

- Use `--backup` (or choose when prompted) to save existing files into
  `gsd-backups/<timestamp>/` before overwriting.

Examples:

- `powershell -ExecutionPolicy Bypass -File gsd-installer.ps1 --target "C:\path\to\repo" --mode missing`
- `powershell -ExecutionPolicy Bypass -File gsd-installer.ps1 --target "C:\path\to\repo" --mode overwrite --backup`
- `sh gsd-installer.sh --target "/path/to/repo" --mode missing`
- `sh gsd-installer.sh --target "/path/to/repo" --mode overwrite --backup`

## Benchmarks

Use the benchmark harness to compare kit changes over time.

- Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/run-bench.ps1`
- macOS/Linux: `sh benchmarks/run-bench.sh`

Reports are written to `benchmarks/bench-report.md`.

## Live benchmarks

Live benchmarks capture real agent runs in Cursor via hook telemetry.

- Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/live/run-live-bench.ps1`
- macOS/Linux: `sh benchmarks/live/run-live-bench.sh`

Reports are written to `benchmarks/live/live-bench-report.md`.
