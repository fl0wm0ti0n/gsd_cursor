#!/usr/bin/env sh
set -e

PROMPT_FILE="$1"
CLIPBOARD="$2"

if [ -z "$PROMPT_FILE" ] || [ ! -f "$PROMPT_FILE" ]; then
  echo "Prompt file not found: $PROMPT_FILE"
  exit 1
fi

copy_clipboard() {
  if command -v pbcopy >/dev/null 2>&1; then
    pbcopy
    return 0
  fi
  if command -v xclip >/dev/null 2>&1; then
    xclip -selection clipboard
    return 0
  fi
  return 1
}

step=1
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
for part in "$tmpfile".*; do
  prompt="$(cat "$part" | sed 's/^[[:space:]]*//;s/[[:space:]]*$//')"
  if [ -z "$prompt" ]; then
    continue
  fi
  echo ""
  echo "Step $step:"
  echo "$prompt"
  if [ "$CLIPBOARD" = "--clipboard" ]; then
    if printf "%s" "$prompt" | copy_clipboard; then
      echo "Copied to clipboard."
    else
      echo "Clipboard not available; copy manually."
    fi
  fi
  printf "%s" "Press Enter after sending this prompt in Cursor"
  read -r _
  step=$((step + 1))
done
rm -f "$tmpfile".*

exit 0
