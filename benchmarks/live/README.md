# Live Benchmarks

Live benchmarks measure actual agent runs in Cursor using hook telemetry.

## How it works

1. Set a session ID in `.cursor/scratchpad.md`:
   `GSD_BENCH_SESSION=run-YYYYMMDD-HHMMSS`
2. Run the scenario in Cursor using the standard commands.
3. End the run and clear `GSD_BENCH_SESSION`.
4. Generate a report from the log file.

The log file is stored at `.cursor/hooks/gsd-bench-log.jsonl`.

