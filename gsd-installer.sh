#!/usr/bin/env sh
set -e


ensure_parent() {
  dir=$(dirname "$1")
  [ -d "$dir" ] || mkdir -p "$dir"
}

list_source_files() {
  source_root="$1"
  shift
  for rel in "$@"; do
    src="$source_root/$rel"
    if [ -f "$src" ]; then
      echo "$rel"
    elif [ -d "$src" ]; then
      find "$src" -type f | sed "s|^$source_root/||"
    fi
  done | sort -u
}

backup_files() {
  target_root="$1"
  shift
  timestamp=$(date -u +"%Y%m%d-%H%M%SZ")
  backup_root="$target_root/gsd-backups/$timestamp"
  for rel in "$@"; do
    src="$target_root/$rel"
    if [ -f "$src" ]; then
      dst="$backup_root/$rel"
      ensure_parent "$dst"
      cp -p "$src" "$dst"
    fi
  done
  echo "$backup_root"
}

choose_mode() {
  printf "%s\n" "Select install mode:"
  printf "%s\n" "1) missing-only (copy only files that do not exist)"
  printf "%s\n" "2) overwrite-all (replace existing files)"
  printf "%s\n" "3) interactive (prompt per file)"
  printf "%s" "Enter 1, 2, or 3: "
  read -r choice
  case "$choice" in
    1) echo "missing" ;;
    2) echo "overwrite" ;;
    *) echo "interactive" ;;
  esac
}

prompt_yes_no() {
  label="$1"
  default="$2"
  suffix="y/N"
  [ "$default" = "true" ] && suffix="Y/n"
  printf "%s [%s]: " "$label" "$suffix"
  read -r value
  value=$(printf "%s" "$value" | tr 'A-Z' 'a-z')
  if [ -z "$value" ]; then
    [ "$default" = "true" ] && return 0 || return 1
  fi
  [ "$value" = "y" ] || [ "$value" = "yes" ]
}

TARGET=""
MODE=""
BACKUP="false"
CREATE="false"

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --backup) BACKUP="true"; shift 1 ;;
    --create) CREATE="true"; shift 1 ;;
    *) shift 1 ;;
  esac
done

SOURCE_ROOT=$(cd "$(dirname "$0")" && pwd)

if [ -z "$TARGET" ]; then
  printf "%s" "Target repository path: "
  read -r TARGET
fi

if [ ! -d "$TARGET" ]; then
  if [ "$CREATE" = "true" ] || prompt_yes_no "Target missing. Create?" "false"; then
    mkdir -p "$TARGET"
  else
    printf "%s\n" "Target directory does not exist."
    exit 1
  fi
fi
TARGET_ROOT=$(cd "$TARGET" && pwd)

if [ -z "$MODE" ]; then
  MODE=$(choose_mode)
fi

if [ "$MODE" = "overwrite" ] || [ "$MODE" = "interactive" ]; then
  if [ "$BACKUP" = "false" ]; then
    if prompt_yes_no "Backup existing files before overwrite?" "false"; then
      BACKUP="true"
    fi
  fi
fi

INCLUDE_PATHS="
.cursor/commands
.cursor/rules
.cursor/skills
.cursor/agents
.cursor/hooks
.cursor/hooks.json
.cursor/scratchpad.md
docs
sprints
handoffs
decisions
.github/workflows
README.md
gsd-installer.py
gsd-installer.ps1
gsd-installer.sh
"

FILES=$(list_source_files "$SOURCE_ROOT" $INCLUDE_PATHS)
if [ -z "$FILES" ]; then
  printf "%s\n" "No source files found to install."
  exit 1
fi

if [ "$BACKUP" = "true" ] && [ "$MODE" = "overwrite" ]; then
  overwrite_candidates=""
  for rel in $FILES; do
    [ -f "$TARGET_ROOT/$rel" ] && overwrite_candidates="$overwrite_candidates $rel"
  done
  if [ -n "$overwrite_candidates" ]; then
    backup_root=$(backup_files "$TARGET_ROOT" $overwrite_candidates)
    printf "%s\n" "Backup created at: $backup_root"
  fi
fi

for rel in $FILES; do
  src="$SOURCE_ROOT/$rel"
  dst="$TARGET_ROOT/$rel"
  if [ "$MODE" = "missing" ]; then
    [ -f "$dst" ] && continue
    ensure_parent "$dst"
    cp -p "$src" "$dst"
    continue
  fi
  if [ "$MODE" = "overwrite" ]; then
    ensure_parent "$dst"
    cp -p "$src" "$dst"
    continue
  fi
  if [ "$MODE" = "interactive" ]; then
    if [ ! -f "$dst" ]; then
      ensure_parent "$dst"
      cp -p "$src" "$dst"
      continue
    fi
    printf "%s" "File exists: $rel | [o]verwrite [s]kip [q]uit: "
    read -r answer
    answer=$(printf "%s" "$answer" | tr 'A-Z' 'a-z')
    if [ "$answer" = "q" ]; then
      printf "%s\n" "Aborted."
      exit 1
    fi
    if [ "$answer" = "o" ]; then
      if [ "$BACKUP" = "true" ]; then
        backup_root=$(backup_files "$TARGET_ROOT" "$rel")
        printf "%s\n" "Backed up: $rel -> $backup_root"
      fi
      ensure_parent "$dst"
      cp -p "$src" "$dst"
    fi
  fi
done

show_banner() {
    printf "\n"
    printf "\033[1;35m  ██╗████████╗███████╗      ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗\033[0m\n"
    printf "\033[1;35m  ██║╚══██╔══╝██╔════╝      ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝\033[0m\n"
    printf "\033[1;35m  ██║   ██║   ███████╗█████╗██╔████╔██║███████║██║  ███╗██║██║     \033[0m\n"
    printf "\033[1;36m  ██║   ██║   ╚════██║╚════╝██║╚██╔╝██║██╔══██║██║   ██║██║██║     \033[0m\n"
    printf "\033[1;36m  ██║   ██║   ███████║      ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗\033[0m\n"
    printf "\033[1;36m  ╚═╝   ╚═╝   ╚══════╝      ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝\033[0m\n"
    printf "\n"
    printf "\033[1;33m                         AI dev team\033[0m\n"
    printf "\033[1;32m                    Installation complete!\033[0m\n"
    printf "\n"
}

show_banner
exit 0

