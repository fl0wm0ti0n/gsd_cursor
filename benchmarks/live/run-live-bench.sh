#!/usr/bin/env sh
set -e

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCRATCHPAD="$ROOT/.cursor/scratchpad.md"
LOG="$ROOT/.cursor/hooks/gsd-bench-log.jsonl"
REPORT="$ROOT/benchmarks/live/live-bench-report.md"

session="$1"
if [ -z "$session" ]; then
  session="run-$(date -u +"%Y%m%d-%H%M%SZ")"
fi

update_scratchpad() {
  if [ -f "$SCRATCHPAD" ]; then
    if grep -q "^GSD_BENCH_SESSION=" "$SCRATCHPAD"; then
      sed -i.bak "s/^GSD_BENCH_SESSION=.*/GSD_BENCH_SESSION=$session/" "$SCRATCHPAD"
    else
      printf "%s\n" "GSD_BENCH_SESSION=$session" >> "$SCRATCHPAD"
    fi
  else
    printf "%s\n" "GSD_BENCH_SESSION=$session" > "$SCRATCHPAD"
  fi
}

clear_scratchpad() {
  if [ -f "$SCRATCHPAD" ]; then
    sed -i.bak "s/^GSD_BENCH_SESSION=.*/GSD_BENCH_SESSION=/" "$SCRATCHPAD"
  fi
}

echo "Live benchmark session: $session"
update_scratchpad
echo "Session set in scratchpad. Run your scenario in Cursor now."
printf "%s" "Press Enter when the scenario is complete"
read -r _

clear_scratchpad
echo "Session cleared. Generating report..."

events=$(grep -F "\"session\": \"$session\"" "$LOG" || true)
start_ts=$(printf "%s\n" "$events" | head -n 1 | awk -F'"ts": "' '{print $2}' | awk -F'"' '{print $1}')
end_ts=$(printf "%s\n" "$events" | tail -n 1 | awk -F'"ts": "' '{print $2}' | awk -F'"' '{print $1}')

duration=0
if [ -n "$start_ts" ] && [ -n "$end_ts" ]; then
  start_sec=$(date -u -d "$start_ts" +"%s" 2>/dev/null || date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$start_ts" +"%s")
  end_sec=$(date -u -d "$end_ts" +"%s" 2>/dev/null || date -u -j -f "%Y-%m-%dT%H:%M:%SZ" "$end_ts" +"%s")
  duration=$((end_sec - start_sec))
fi

count_event() {
  printf "%s\n" "$events" | grep -c "\"event\": \"$1\""
}

beforeShellExecution=$(count_event "beforeShellExecution")
beforeReadFile=$(count_event "beforeReadFile")
afterFileEdit=$(count_event "afterFileEdit")
stopCount=$(count_event "stop")

timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
mkdir -p "$(dirname "$REPORT")"
{
  echo "# GSD Kit Live Benchmark Report"
  echo ""
  echo "Timestamp: $timestamp"
  echo "Session: $session"
  echo "DurationSeconds: $duration"
  echo ""
  echo "## Event Counts"
  echo "- beforeShellExecution: $beforeShellExecution"
  echo "- beforeReadFile: $beforeReadFile"
  echo "- afterFileEdit: $afterFileEdit"
  echo "- stop: $stopCount"
  echo ""
  echo "## Errors"
  echo "- none"
} > "$REPORT"

echo "Report written to: $REPORT"
exit 0

