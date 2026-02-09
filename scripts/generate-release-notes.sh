#!/usr/bin/env sh
set -e

ROOT="${1:-$(cd "$(dirname "$0")/.." && pwd)}"
VERSION="${2:-v0.0.0}"
SPRINT="${3:-S0001}"

SUMMARY_PATH="$ROOT/sprints/$SPRINT/summary.md"
QA_PATH="$ROOT/sprints/$SPRINT/qa-findings.md"
RUNBOOK_PATH="$ROOT/docs/engineering/runbook.md"
OUT_PATH="$ROOT/handoffs/release_notes.md"

read_if_exists() {
  if [ -f "$1" ]; then
    cat "$1"
  fi
}

summary="$(read_if_exists "$SUMMARY_PATH")"
qa="$(read_if_exists "$QA_PATH")"
runbook="$(read_if_exists "$RUNBOOK_PATH")"

git_changes=""
if command -v git >/dev/null 2>&1; then
  if git -C "$ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    git_changes="$(git -C "$ROOT" log -n 20 --pretty=format:"- %s")"
  fi
fi

timestamp="$(date +"%Y-%m-%d")"

cat > "$OUT_PATH" <<EOF
# Release Notes — $VERSION

**Sprint:** $SPRINT
**Date:** $timestamp

---

## Summary

$summary

---

## Changes (last 20 commits)

$git_changes

---

## QA Findings (from sprint)

$qa

---

## Runbook Notes

$runbook
EOF

echo "Release notes written to: $OUT_PATH"
