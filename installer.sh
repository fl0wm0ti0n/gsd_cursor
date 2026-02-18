#!/usr/bin/env sh
set -e

SOURCE_ROOT=$(cd "$(dirname "$0")" && pwd)
REPO_URL="https://github.com/fl0wm0ti0n/its-magic"
APP_VERSION=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$SOURCE_ROOT/package.json" | head -n 1)
[ -z "$APP_VERSION" ] && APP_VERSION="unknown"

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
  printf "\n"
}

show_help() {
  show_banner
  printf "its-magic v%s\n" "$APP_VERSION"
  printf "Repository: %s\n\n" "$REPO_URL"
  printf "Install AI dev team workflow files into any Cursor repository.\n\n"
  printf "Usage:\n"
  printf "  its-magic --target <path> [--mode <mode>] [--backup] [--create]\n"
  printf "  its-magic --clean-repo [--target <path>] [--yes]\n"
  printf "  its-magic --help | --version\n\n"
  printf "Install options:\n"
  printf "  --target <path>   Path to the repository where workflow files are installed.\n"
  printf "                    If omitted you will be prompted interactively.\n"
  printf "  --mode <mode>     How to handle files that already exist in the target:\n"
  printf "                      missing      Only copy files that do not exist yet (default).\n"
  printf "                                   Safe for repos that already have some workflow files.\n"
  printf "                      overwrite    Replace every file, even if it already exists.\n"
  printf "                                   Combine with --backup to keep a snapshot first.\n"
  printf "                      interactive  Ask per file whether to overwrite or skip.\n"
  printf "  --backup          Before overwriting, save existing files to backups/<timestamp>/.\n"
  printf "                    Ignored when mode is 'missing' (nothing gets replaced).\n"
  printf "  --create          Create the target directory if it does not exist.\n\n"
  printf "Clean options:\n"
  printf "  --clean-repo      Remove all its-magic workflow artifacts from the target repo\n"
  printf "                    (.cursor, docs/product, docs/engineering, sprints, handoffs,\n"
  printf "                    decisions). Your own source code is never touched.\n"
  printf "  --target <path>   Repo to clean (default: current directory).\n"
  printf "  --yes             Skip the confirmation prompt.\n\n"
  printf "Info:\n"
  printf "  --help, -h        Show this help and exit.\n"
  printf "  --version, -v     Print the installed version and exit.\n\n"
  printf "Examples:\n"
  printf "  its-magic --target . --mode missing            Safe first-time setup\n"
  printf "  its-magic --target . --mode overwrite --backup   Update all files, keep backup\n"
  printf "  its-magic --clean-repo --target . --yes        Remove workflow artifacts silently\n\n"
}

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
  backup_root="$target_root/backups/$timestamp"
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
CLEAN_REPO="false"
ASSUME_YES="false"
SHOW_HELP="false"
SHOW_VERSION="false"

if [ $# -eq 0 ]; then
  SHOW_HELP="true"
fi

while [ $# -gt 0 ]; do
  case "$1" in
    --target) TARGET="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --backup) BACKUP="true"; shift 1 ;;
    --create) CREATE="true"; shift 1 ;;
    --clean-repo) CLEAN_REPO="true"; shift 1 ;;
    --yes) ASSUME_YES="true"; shift 1 ;;
    --help|-h) SHOW_HELP="true"; shift 1 ;;
    --version|-v) SHOW_VERSION="true"; shift 1 ;;
    *) shift 1 ;;
  esac
done

if [ "$SHOW_VERSION" = "true" ]; then
  printf "its-magic v%s\n" "$APP_VERSION"
  exit 0
fi

if [ "$SHOW_HELP" = "true" ]; then
  show_help
  exit 0
fi

if [ "$CLEAN_REPO" = "true" ]; then
  if [ -z "$TARGET" ]; then
    TARGET="."
  fi
  if [ ! -d "$TARGET" ]; then
    printf "%s\n" "Target directory does not exist."
    exit 1
  fi
  TARGET_ROOT=$(cd "$TARGET" && pwd)
  if [ "$ASSUME_YES" != "true" ]; then
    if ! prompt_yes_no "Clean its-magic workflow artifacts in $TARGET_ROOT?" "false"; then
      printf "%s\n" "Aborted."
      exit 1
    fi
  fi
  CLEAN_PATHS="
.cursor
docs/product
docs/engineering
sprints
handoffs
decisions
"
  for rel in $CLEAN_PATHS; do
    path="$TARGET_ROOT/$rel"
    if [ -e "$path" ]; then
      rm -rf "$path"
      printf "%s\n" "Removed: $rel"
    fi
  done
  printf "%s\n" "Clean completed."
  exit 0
fi

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
.cursor/scratchpad.local.example.md
docs
sprints
handoffs
decisions
.github/workflows
README.md
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

show_banner
printf "its-magic v%s\n" "$APP_VERSION"
printf "Repository: %s\n\n" "$REPO_URL"
printf "\033[1;32m                    Installation complete!\033[0m\n\n"
exit 0

