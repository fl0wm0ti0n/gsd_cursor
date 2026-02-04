# Benchmarks

This harness provides automated, repeatable benchmarks for the GSD kit.

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

