#!/usr/bin/env sh
set -e

PROMPT_FILE="$1"
SCENARIO_FILE="$2"
REPORT_PATH="${3:-benchmarks/headless/headless-report.md}"
PROTOCOL_PATH="${4:-benchmarks/headless/protocol.md}"
SUMMARY_CHARS="${5:-600}"

if [ -z "$PROMPT_FILE" ] || [ ! -f "$PROMPT_FILE" ]; then
  echo "Prompt file not found: $PROMPT_FILE"
  exit 1
fi

if ! command -v rg >/dev/null 2>&1; then
  echo "Missing dependency: ripgrep (rg)"
  echo "Install with: brew install ripgrep (macOS) or apt install ripgrep (Linux)"
  exit 1
fi

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

if [ -z "$SCENARIO_FILE" ]; then
  base="$(basename "$PROMPT_FILE" .txt)"
  candidate="$ROOT/benchmarks/scenarios/$base.scn"
  if [ -f "$candidate" ]; then
    SCENARIO_FILE="$candidate"
  fi
fi

scenario_require() {
  file="$1"
  awk '
    /^\[require\]/{inreq=1;next}
    /^\[/{inreq=0}
    inreq && NF {print}
  ' "$file"
}

scenario_sections() {
  file="$1"
  awk '
    /^\[sections\]/{insec=1;next}
    /^\[/{insec=0}
    insec && NF {print}
  ' "$file"
}

scenario_id() {
  file="$1"
  awk '
    /^\[meta\]/{inmeta=1;next}
    /^\[/{inmeta=0}
    inmeta && /^id=/ {sub(/^[^=]+=/,""); print; exit}
  ' "$file"
}

run_id="headless-$(date -u +"%Y%m%d-%H%M%SZ")"
run_root="$ROOT/benchmarks/runs/$run_id"
workspace="$run_root/workspace"
mkdir -p "$workspace"

if [ -f "$ROOT/gsd-installer.sh" ]; then
  sh "$ROOT/gsd-installer.sh" --target "$workspace" --mode missing --create >/dev/null
fi

cd "$workspace"

tmpfile="$(mktemp)"
count=0
part="$tmpfile.$count"
printf "" > "$part"
while IFS= read -r line; do
  if [ "$line" = "---" ]; then
    count=$((count + 1))
    part="$tmpfile.$count"
    printf "" > "$part"
    continue
  fi
  printf "%s\n" "$line" >> "$part"
done < "$PROMPT_FILE"

step=1
pass=0
fail=0
RESULTS=""
PROTOCOL=""
missing=0
section_errors=0
smoke_checks=""
TOTAL_START=$(date +%s)

for part in "$tmpfile".*; do
  prompt="$(cat "$part" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  if [ -z "$prompt" ]; then
    continue
  fi
  start=$(date +%s)
  echo "Running step $step"
  out_file="$tmpfile.out.$step"
  if agent -p --force --output-format text "$prompt" >"$out_file" 2>&1; then
    status="PASS"
    pass=$((pass + 1))
    exitcode=0
  else
    status="FAIL"
    fail=$((fail + 1))
    exitcode=$?
  fi
  end=$(date +%s)
  duration=$((end - start))
  RESULTS="$RESULTS\n- [$status] Step $step | DurationSeconds=$duration | ExitCode=$exitcode"
  summary=$(head -c "$SUMMARY_CHARS" "$out_file" | tr -d '\r')
  if [ "$(wc -c < "$out_file" | tr -d ' ')" -gt "$SUMMARY_CHARS" ]; then
    summary="$summary..."
  fi
  PROTOCOL="$PROTOCOL\n\n### Step $step\nStatus: $status | DurationSeconds=$duration | ExitCode=$exitcode\n\nPrompt:\n\`\`\`\n$prompt\n\`\`\`\n\nAI response (summary):\n\`\`\`\n$summary\n\`\`\`"
  step=$((step + 1))
done

TOTAL_END=$(date +%s)
TOTAL_DURATION=$((TOTAL_END - TOTAL_START))
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

if [ -n "$SCENARIO_FILE" ] && [ -f "$SCENARIO_FILE" ]; then
  for rel in $(scenario_require "$SCENARIO_FILE"); do
    [ -f "$workspace/$rel" ] || missing=$((missing + 1))
  done
  for entry in $(scenario_sections "$SCENARIO_FILE"); do
    file_path=$(printf "%s" "$entry" | cut -d'|' -f1)
    headings=$(printf "%s" "$entry" | cut -d'|' -f2)
    target="$workspace/$file_path"
    IFS=';'
    for h in $headings; do
      if [ -n "$h" ]; then
        grep -q "$h" "$target" || section_errors=$((section_errors + 1))
      fi
    done
    unset IFS
  done

  id=$(scenario_id "$SCENARIO_FILE")
  if [ "$id" = "S4" ]; then
    schema="$workspace/examples/webview-app/shared/schema.json"
    if [ -f "$schema" ]; then
      if command -v python >/dev/null 2>&1 && python - <<'PY' "$schema" >/dev/null 2>&1
import json, sys
json.load(open(sys.argv[1], "r", encoding="utf-8"))
PY
      then
        smoke_checks="$smoke_checks\n- schema.json valid: PASS"
      else
        smoke_checks="$smoke_checks\n- schema.json valid: FAIL"
      fi
    fi
    index="$workspace/examples/webview-app/frontend/index.html"
    if [ -f "$index" ]; then
      grep -q "app\.js" "$index" && smoke_checks="$smoke_checks\n- index references app.js: PASS" || smoke_checks="$smoke_checks\n- index references app.js: FAIL"
      grep -q "style\.css" "$index" && smoke_checks="$smoke_checks\n- index references style.css: PASS" || smoke_checks="$smoke_checks\n- index references style.css: FAIL"
    fi
  fi
  if [ "$id" = "S5" ]; then
    index="$workspace/examples/3d-animation/index.html"
    if [ -f "$index" ]; then
      grep -q "main\.js" "$index" && smoke_checks="$smoke_checks\n- index references main.js: PASS" || smoke_checks="$smoke_checks\n- index references main.js: FAIL"
    fi
    main="$workspace/examples/3d-animation/main.js"
    if [ -f "$main" ]; then
      grep -q "requestAnimationFrame" "$main" && smoke_checks="$smoke_checks\n- main uses requestAnimationFrame: PASS" || smoke_checks="$smoke_checks\n- main uses requestAnimationFrame: FAIL"
    fi
  fi
fi

mkdir -p "$(dirname "$REPORT_PATH")"
{
  echo "# GSD Kit Headless Benchmark Report"
  echo ""
  echo "Timestamp: $timestamp"
  echo "PromptFile: $PROMPT_FILE"
  echo "ScenarioFile: $SCENARIO_FILE"
  echo "Workspace: $workspace"
  echo "Steps: $((step - 1))"
  echo "Pass: $pass"
  echo "Fail: $fail"
  echo "TotalDurationSeconds: $TOTAL_DURATION"
  echo ""
  echo "## Validation"
  echo "MissingFiles: $missing"
  echo "SectionErrors: $section_errors"
  echo ""
  echo "## Results"
  printf "%b\n" "$RESULTS"
  if [ -n "$smoke_checks" ]; then
    echo ""
    echo "## Smoke checks"
    printf "%b\n" "$smoke_checks"
  fi
} > "$REPORT_PATH"

mkdir -p "$(dirname "$PROTOCOL_PATH")"
{
  echo "# GSD Kit Headless Protocol"
  echo ""
  echo "Timestamp: $timestamp"
  echo "PromptFile: $PROMPT_FILE"
  echo "ScenarioFile: $SCENARIO_FILE"
  echo "Workspace: $workspace"
  echo ""
  echo "## Steps"
  printf "%b\n" "$PROTOCOL"
} > "$PROTOCOL_PATH"

rm -f "$tmpfile".*
rm -f "$tmpfile".out.*
mkdir -p "$run_root/reports"
cp -f "$REPORT_PATH" "$run_root/reports/headless-report.md"
cp -f "$PROTOCOL_PATH" "$run_root/reports/protocol.md"
echo "Report written to: $REPORT_PATH"
echo "Protocol written to: $PROTOCOL_PATH"
echo "Run artifacts: $run_root"
if [ "$fail" -gt 0 ] || [ "$missing" -gt 0 ] || [ "$section_errors" -gt 0 ] || echo "$smoke_checks" | grep -q "FAIL"; then
  exit 1
fi
exit 0
