# Benchmarks

This harness provides automated, repeatable benchmarks for the its-magic.

It simulates scenario runs, validates artifact completeness, and produces a
report with timing, coverage, and errors.

## Run

- Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/run-bench.ps1`
- macOS/Linux: `sh benchmarks/run-bench.sh`

## Live benchmarks

Live benchmarks measure actual agent runs in Cursor using hook telemetry.

- Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/live/run-live-bench.ps1`
- macOS/Linux: `sh benchmarks/live/run-live-bench.sh`

## Scenarios

Scenarios live in `benchmarks/scenarios/*.scn` and use a simple format:

- `[meta]` id, name, steps
- `[require]` list of required files
- `[sections]` file path + required headings

Code scenarios can add a `[commands]` section listing the `/*` commands
that must be used. They can also require specific marker strings in code
files (for example `API_SERVER` or `RENDER_LOOP`) so the validator can check
that key pieces were implemented.

## Prompted runs

Prompt files live in `benchmarks/prompts/` and can be replayed step-by-step.

- Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/prompts/run-prompts.ps1 -PromptFile benchmarks/prompts/S4_webview_api_app.txt -Clipboard`
- macOS/Linux: `sh benchmarks/prompts/run-prompts.sh benchmarks/prompts/S4_webview_api_app.txt --clipboard`

## Fully automated (Headless CLI)

This uses Cursor CLI in non-interactive mode.

- Windows: `powershell -ExecutionPolicy Bypass -File benchmarks/headless/run-headless.ps1 -PromptFile benchmarks/prompts/S4_webview_api_app.txt -ScenarioFile benchmarks/scenarios/S4_webview_api_app.scn`
- macOS/Linux: `sh benchmarks/headless/run-headless.sh benchmarks/prompts/S4_webview_api_app.txt benchmarks/scenarios/S4_webview_api_app.scn`

Dependencies:
- Cursor CLI (`agent`)
- ripgrep (`rg`)

Outputs:
- `benchmarks/headless/headless-report.md`
- `benchmarks/headless/protocol.md` (step prompts + AI response summaries)
Per-run artifacts:
- `benchmarks/runs/headless-<timestamp>/workspace/`
- `benchmarks/runs/headless-<timestamp>/reports/`

