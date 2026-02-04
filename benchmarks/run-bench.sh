#!/usr/bin/env sh
set -e

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SCENARIOS="$ROOT/benchmarks/scenarios"
TMP="$ROOT/benchmarks/.tmp"
REPORT="$ROOT/benchmarks/bench-report.md"

mkdir -p "$TMP"

pass=0
fail=0
RESULTS=""

scenario_meta() {
  file="$1"
  key="$2"
  awk -v key="$key" '
    /^\[meta\]/{inmeta=1;next}
    /^\[/{inmeta=0}
    inmeta && $0 ~ key"=" {sub(/^[^=]+=/,""); print; exit}
  ' "$file"
}

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

ensure_parent() {
  dir=$(dirname "$1")
  [ -d "$dir" ] || mkdir -p "$dir"
}

add_result() {
  name="$1"
  status="$2"
  detail="$3"
  if [ "$status" = "PASS" ]; then
    pass=$((pass + 1))
  else
    fail=$((fail + 1))
  fi
  if [ -n "$detail" ]; then
    RESULTS="$RESULTS\n- [$status] $name | $detail"
  else
    RESULTS="$RESULTS\n- [$status] $name"
  fi
}

TOTAL_START=$(date +%s)

for scn in "$SCENARIOS"/*.scn; do
  id=$(scenario_meta "$scn" "id")
  name=$(scenario_meta "$scn" "name")
  steps=$(scenario_meta "$scn" "steps")
  start=$(date +%s)

  scenario_root="$TMP/${id}-$(date -u +"%Y%m%d-%H%M%SZ")"
  mkdir -p "$scenario_root"

  if [ -f "$ROOT/gsd-installer.sh" ]; then
    sh "$ROOT/gsd-installer.sh" --target "$scenario_root" --mode missing --create >/dev/null
  fi

  missing=0
  for rel in $(scenario_require "$scn"); do
    path="$scenario_root/$rel"
    if [ ! -f "$path" ]; then
      ensure_parent "$path"
      printf "%s\n" "# Auto-generated stub" > "$path"
      missing=$((missing + 1))
    fi
  done

  section_errors=0
  sections=$(scenario_sections "$scn")
  for entry in $sections; do
    file_path=$(printf "%s" "$entry" | cut -d'|' -f1)
    headings=$(printf "%s" "$entry" | cut -d'|' -f2)
    target="$scenario_root/$file_path"
    IFS=';' 
    for h in $headings; do
      if [ -n "$h" ]; then
        grep -q "$h" "$target" || section_errors=$((section_errors + 1))
      fi
    done
    unset IFS
  done

  end=$(date +%s)
  duration=$((end - start))
  if [ "$missing" -eq 0 ] && [ "$section_errors" -eq 0 ]; then
    status="PASS"
  else
    status="FAIL"
  fi
  add_result "$id ($name)" "$status" "Steps=$steps DurationSeconds=$duration Missing=$missing SectionErrors=$section_errors"
done

TOTAL_END=$(date +%s)
TOTAL_DURATION=$((TOTAL_END - TOTAL_START))
timestamp=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

{
  echo "# GSD Kit Benchmark Report"
  echo ""
  echo "Timestamp: $timestamp"
  echo "Pass: $pass"
  echo "Fail: $fail"
  echo "TotalDurationSeconds: $TOTAL_DURATION"
  echo ""
  echo "## Results"
  printf "%b\n" "$RESULTS"
  echo ""
  echo "Notes: This benchmark simulates agent output by creating stubs for missing artifacts."
} > "$REPORT"

echo "Report written to: $REPORT"
if [ "$fail" -gt 0 ]; then
  exit 1
fi
exit 0

