#!/usr/bin/env sh
set -e

# BUG-0004: keep startup shell options POSIX-safe for /bin/sh execution.
# Do not use bash-only "set" flags in this unconditional startup path.

SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
SOURCE_ROOT="$SCRIPT_DIR/template"
MANIFEST_NAME="docs/engineering/context/installer-owned-paths.manifest"
REPO_URL="https://github.com/fl0wm0ti0n/its-magic"
APP_VERSION=$(sed -n 's/.*"version"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' "$SCRIPT_DIR/package.json" 2>/dev/null | head -n 1)
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
  printf "                      upgrade      Update framework files while preserving user data.\n"
  printf "                                   Use after updating its-magic to a newer version.\n"
  printf "  --backup          Before overwriting, save existing files to backups/<timestamp>/.\n"
  printf "                    Ignored when mode is 'missing' (nothing gets replaced).\n"
  printf "  --create          Create the target directory if it does not exist.\n\n"
  printf "  Note: installer bootstraps runbook TEST/LINT/TYPECHECK commands from\n"
  printf "        OS+stack detection; unresolved TEST_COMMAND fails fast with\n"
  printf "        [RUNBOOK_BOOTSTRAP_ERROR] diagnostics.\n"
  printf "  Note: scratchpad Model B: .cursor/scratchpad.md is\n"
  printf "        materialized when missing; Python 3 on PATH is required for validation.\n"
  printf "        Recovery: python installer.py --scratchpad-postinstall --target <repo> --mode missing\n\n"
  printf "Clean options:\n"
  printf "  --clean-repo      Remove all its-magic workflow artifacts from the target repo\n"
  printf "                    (owned paths from installer manifest, including .cursor,\n"
  printf "                    docs/product, docs/engineering, docs/user-guides, sprints,\n"
  printf "                    handoffs, decisions, workflow scripts, CI files, and\n"
  printf "                    installer metadata under its_magic/ (legacy .its-magic-version\n"
  printf "                    is also removed when present). Your own source code is never touched.\n"
  printf "  --target <path>   Repo to clean (default: current directory).\n"
  printf "  --yes             Skip the confirmation prompt.\n\n"
  printf "Info:\n"
  printf "  --help, -h        Show this help and exit.\n"
  printf "  --version, -v     Print the installed version and exit.\n\n"
  printf "Examples:\n"
  printf "  its-magic --target . --mode missing              Safe first-time setup\n"
  printf "  its-magic --target . --mode upgrade               Update framework, keep user data\n"
  printf "  its-magic --target . --mode overwrite --backup    Replace all files, keep backup\n"
  printf "  its-magic --clean-repo --target . --yes           Remove workflow artifacts silently\n\n"
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

get_manifest_paths() {
  section="$1"
  # BUG-0008: strip trailing CR so CRLF manifests (Windows-published npm tarballs)
  # still match [section] headers under POSIX awk on Linux.
  awk -v s="$section" '
    BEGIN { in_section=0 }
    {
      sub(/\r$/, "")
    }
    /^[[:space:]]*#/ { next }
    /^[[:space:]]*$/ { next }
    /^\[/ {
      in_section = ($0 == "[" s "]")
      next
    }
    { if (in_section) print $0 }
  ' "$OWNERSHIP_MANIFEST"
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
  printf "%s\n" "4) upgrade (update framework files, preserve user data)"
  printf "%s" "Enter 1, 2, 3, or 4: "
  read -r choice
  case "$choice" in
    1) echo "missing" ;;
    2) echo "overwrite" ;;
    4) echo "upgrade" ;;
    *) echo "interactive" ;;
  esac
}

scratchpad_postinstall() {
  target_root="$1"
  mode="$2"
  installer_py="$SCRIPT_DIR/installer.py"
  if [ ! -f "$installer_py" ]; then
    printf "%s\n" "[SCRATCHPAD_POSTINSTALL_ERROR] installer.py missing next to installer.sh."
    exit 1
  fi
  if command -v python3 >/dev/null 2>&1; then
    python3 "$installer_py" --scratchpad-postinstall --target "$target_root" --mode "$mode" || exit $?
  elif command -v python >/dev/null 2>&1; then
    python "$installer_py" --scratchpad-postinstall --target "$target_root" --mode "$mode" || exit $?
  else
    printf "%s\n" "[SCRATCHPAD_POSTINSTALL_ERROR] PYTHON_NOT_FOUND: Python 3 is required for scratchpad materialization/validation (Model B)."
    exit 1
  fi
}

validate_install_completeness() {
  target_root="$1"
  installer_py="$SCRIPT_DIR/installer.py"
  if [ ! -f "$installer_py" ]; then
    printf "%s\n" "[INSTALL_COMPLETENESS_FAILED] installer.py missing next to installer.sh."
    exit 1
  fi
  if command -v python3 >/dev/null 2>&1; then
    python3 "$installer_py" --validate-install-completeness --target "$target_root" || exit $?
  elif command -v python >/dev/null 2>&1; then
    python "$installer_py" --validate-install-completeness --target "$target_root" || exit $?
  else
    printf "%s\n" "[INSTALL_COMPLETENESS_FAILED] PYTHON_NOT_FOUND: Python is required for deterministic installer completeness validation."
    exit 1
  fi
}

classify_file() {
  rel="$1"
  case "$rel" in
    README.md) echo "mixed" ;;
    .cursor/commands/*|.cursor/rules/*|.cursor/agents/*|.cursor/skills/*) echo "framework" ;;
    .cursor/hooks/*|.cursor/hooks.json|.cursor/scratchpad.local.example.md) echo "framework" ;;
    .cursor/model-catalog.local.example*.json) echo "framework" ;;
    .github/workflows/*|scripts/validate-and-push*|scripts/sync_push_gates.py|docs/engineering/context/*|its_magic/*) echo "framework" ;;
    .its-magic-version|its_magic/.its-magic-version|its_magic/README.md) echo "framework" ;;
    docs/product/*|docs/engineering/*|docs/user-guides/*) echo "user-data" ;;
    sprints/*|handoffs/*|decisions/*) echo "user-data" ;;
    *) echo "framework" ;;
  esac
}

read_installed_version() {
  primary="$1/its_magic/.its-magic-version"
  legacy="$1/.its-magic-version"
  if [ -f "$primary" ]; then
    cat "$primary" | tr -d '\n'
    return 0
  fi
  if [ -f "$legacy" ]; then
    cat "$legacy" | tr -d '\n'
    return 0
  fi
  printf "unknown"
}

write_installed_version() {
  vf="$1/its_magic/.its-magic-version"
  ensure_parent "$vf"
  printf "%s" "$2" > "$vf"
  legacy="$1/.its-magic-version"
  [ -f "$legacy" ] && rm -f "$legacy"
  return 0
}

sync_root_readme_to_its_magic() {
  target_root="$1"
  [ -f "$target_root/README.md" ] || return 1
  dst="$target_root/its_magic/README.md"
  ensure_parent "$dst"
  cp -p "$target_root/README.md" "$dst"
  return 0
}

read_runbook_key() {
  runbook_path="$1"
  key="$2"
  [ -f "$runbook_path" ] || { printf ""; return; }
  awk -F: -v k="$key" '$1==k { sub(/^[[:space:]]*/, "", $2); print $2; exit }' "$runbook_path"
}

write_runbook_key() {
  runbook_path="$1"
  key="$2"
  value="$3"
  [ -f "$runbook_path" ] || return 1
  tmp="$runbook_path.tmp.$$"
  awk -v k="$key" -v v="$value" '
    BEGIN { changed=0 }
    index($0, k":") == 1 && changed==0 { print k": "v; changed=1; next }
    { print $0 }
    END { if (changed==0) exit 2 }
  ' "$runbook_path" > "$tmp" || { rm -f "$tmp"; return 1; }
  mv "$tmp" "$runbook_path"
  return 0
}

package_has_script() {
  target_root="$1"
  script_name="$2"
  pkg="$target_root/package.json"
  [ -f "$pkg" ] || return 1
  command -v node >/dev/null 2>&1 || return 1
  node -e "const fs=require('fs');const p=JSON.parse(fs.readFileSync(process.argv[1],'utf8'));const s=(p.scripts||{})[process.argv[2]];process.exit((typeof s==='string'&&s.trim())?0:1);" "$pkg" "$script_name" >/dev/null 2>&1
}

detect_runbook_defaults() {
  target_root="$1"
  TEST_CANDIDATE=""
  LINT_CANDIDATE=""
  TYPECHECK_CANDIDATE=""
  if [ -f "$target_root/package.json" ] && package_has_script "$target_root" "test"; then
    TEST_CANDIDATE="npm run test"
    package_has_script "$target_root" "lint" && LINT_CANDIDATE="npm run lint"
    package_has_script "$target_root" "typecheck" && TYPECHECK_CANDIDATE="npm run typecheck"
    return 0
  fi
  if [ -f "$target_root/go.mod" ]; then
    TEST_CANDIDATE="go test ./..."
    return 0
  fi
  if [ -f "$target_root/pyproject.toml" ] || [ -f "$target_root/requirements.txt" ] || [ -f "$target_root/setup.py" ]; then
    TEST_CANDIDATE="python -m pytest"
    return 0
  fi
  if [ -f "$target_root/tests/run-tests.sh" ]; then
    TEST_CANDIDATE="sh tests/run-tests.sh"
    return 0
  fi
}

validate_bootstrap_command() {
  target_root="$1"
  key="$2"
  cmd="$3"
  [ -n "$cmd" ] || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="${key}_UNDETECTED"; return 0; }
  case "$cmd" in
    "npm run "*)
      command -v npm >/dev/null 2>&1 || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="NPM_NOT_FOUND"; return 0; }
      script_name=$(printf "%s" "$cmd" | sed 's/^npm run[[:space:]]\+//')
      package_has_script "$target_root" "$script_name" || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="NPM_SCRIPT_MISSING:$script_name"; return 0; }
      BOOTSTRAP_VALID="true"; BOOTSTRAP_REASON="OK"; return 0
      ;;
    "python -m pytest")
      command -v python >/dev/null 2>&1 || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="PYTHON_NOT_FOUND"; return 0; }
      BOOTSTRAP_VALID="true"; BOOTSTRAP_REASON="OK"; return 0
      ;;
    "go test "*)
      command -v go >/dev/null 2>&1 || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="GO_NOT_FOUND"; return 0; }
      [ -f "$target_root/go.mod" ] || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="GO_MOD_MISSING"; return 0; }
      BOOTSTRAP_VALID="true"; BOOTSTRAP_REASON="OK"; return 0
      ;;
    "sh "*)
      command -v sh >/dev/null 2>&1 || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="SH_NOT_FOUND"; return 0; }
      [ -f "$target_root/tests/run-tests.sh" ] || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="RUN_TESTS_SH_MISSING"; return 0; }
      BOOTSTRAP_VALID="true"; BOOTSTRAP_REASON="OK"; return 0
      ;;
  esac
  exe=$(printf "%s" "$cmd" | awk '{print $1}')
  command -v "$exe" >/dev/null 2>&1 || { BOOTSTRAP_VALID="false"; BOOTSTRAP_REASON="EXECUTABLE_NOT_FOUND:$exe"; return 0; }
  BOOTSTRAP_VALID="true"; BOOTSTRAP_REASON="OK"
}

bootstrap_runbook_commands() {
  target_root="$1"
  runbook="$target_root/docs/engineering/runbook.md"
  [ -f "$runbook" ] || { BOOTSTRAP_OK="true"; BOOTSTRAP_NOTES=""; return 0; }
  BOOTSTRAP_NOTES=""
  APPLIED=""
  detect_runbook_defaults "$target_root"
  for key in TEST_COMMAND LINT_COMMAND TYPECHECK_COMMAND; do
    current=$(read_runbook_key "$runbook" "$key")
    [ -n "$current" ] && continue
    candidate=""
    [ "$key" = "TEST_COMMAND" ] && candidate="$TEST_CANDIDATE"
    [ "$key" = "LINT_COMMAND" ] && candidate="$LINT_CANDIDATE"
    [ "$key" = "TYPECHECK_COMMAND" ] && candidate="$TYPECHECK_CANDIDATE"
    if [ -z "$candidate" ]; then
      if [ "$key" = "TEST_COMMAND" ]; then
        BOOTSTRAP_NOTES="${BOOTSTRAP_NOTES}[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED: could not detect a valid baseline test command. Fix: define TEST_COMMAND in docs/engineering/runbook.md or add detectable stack markers (package.json scripts.test, pyproject.toml, go.mod)."$'\n'
      fi
      continue
    fi
    validate_bootstrap_command "$target_root" "$key" "$candidate"
    if [ "$BOOTSTRAP_VALID" = "true" ]; then
      if write_runbook_key "$runbook" "$key" "$candidate"; then
        if [ -z "$APPLIED" ]; then APPLIED="$key=$candidate"; else APPLIED="$APPLIED, $key=$candidate"; fi
      fi
    elif [ "$key" = "TEST_COMMAND" ]; then
      BOOTSTRAP_NOTES="${BOOTSTRAP_NOTES}[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:$BOOTSTRAP_REASON. Fix: set a valid TEST_COMMAND in docs/engineering/runbook.md."$'\n'
    fi
  done
  [ -n "$APPLIED" ] && BOOTSTRAP_NOTES="${BOOTSTRAP_NOTES}[RUNBOOK_BOOTSTRAP] Applied defaults: $APPLIED"$'\n'
  final_test=$(read_runbook_key "$runbook" "TEST_COMMAND")
  if [ -n "$final_test" ]; then BOOTSTRAP_OK="true"; else BOOTSTRAP_OK="false"; fi
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

if [ ! -d "$SOURCE_ROOT" ]; then
  printf "%s\n" "[INSTALL_SOURCE_ERROR] template directory is missing. Reinstall its-magic package."
  exit 1
fi

OWNERSHIP_MANIFEST="$SOURCE_ROOT/$MANIFEST_NAME"
if [ ! -f "$OWNERSHIP_MANIFEST" ]; then
  FALLBACK_MANIFEST="$SCRIPT_DIR/$MANIFEST_NAME"
  if [ -f "$FALLBACK_MANIFEST" ]; then
    OWNERSHIP_MANIFEST="$FALLBACK_MANIFEST"
  else
    printf "%s\n" "[INSTALL_SOURCE_ERROR] installer-owned-paths.manifest not found. Reinstall its-magic package."
    exit 1
  fi
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
  CLEAN_PATHS=$(get_manifest_paths "clean_paths")
  if [ -z "$CLEAN_PATHS" ]; then
    printf "%s\n" "[INSTALL_MANIFEST_ERROR] clean_paths section is empty in $OWNERSHIP_MANIFEST"
    exit 1
  fi
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

INCLUDE_PATHS=$(get_manifest_paths "install_include_paths")
if [ -z "$INCLUDE_PATHS" ]; then
  printf "%s\n" "[INSTALL_MANIFEST_ERROR] install_include_paths section is empty in $OWNERSHIP_MANIFEST"
  exit 1
fi

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

if [ "$MODE" = "upgrade" ]; then
  OLD_VER=$(read_installed_version "$TARGET_ROOT")
  printf "\n\033[1;36mUpgrading from v%s to v%s\033[0m\n\n" "$OLD_VER" "$APP_VERSION"

  if [ "$BACKUP" = "true" ]; then
    backup_candidates=""
    for rel in $FILES; do
      cat=$(classify_file "$rel")
      [ "$cat" = "framework" ] && [ -f "$TARGET_ROOT/$rel" ] && backup_candidates="$backup_candidates $rel"
    done
    if [ -n "$backup_candidates" ]; then
      backup_root=$(backup_files "$TARGET_ROOT" $backup_candidates)
      printf "%s\n" "Backup created at: $backup_root"
    fi
  fi

  count_added=0; list_added=""
  count_updated=0; list_updated=""
  count_unchanged=0
  count_preserved=0
  count_review=0; list_review=""
  scratchpad_example_rel=".cursor/scratchpad.local.example.md"
  scratchpad_example_status="not-seen"

  for rel in $FILES; do
    src="$SOURCE_ROOT/$rel"
    dst="$TARGET_ROOT/$rel"
    cat=$(classify_file "$rel")

    if [ ! -f "$dst" ]; then
      ensure_parent "$dst"
      cp -p "$src" "$dst"
      count_added=$((count_added + 1))
      list_added="$list_added $rel"
      [ "$rel" = "$scratchpad_example_rel" ] && scratchpad_example_status="added"
      continue
    fi

    if [ "$cat" = "framework" ]; then
      if cmp -s "$src" "$dst"; then
        count_unchanged=$((count_unchanged + 1))
        [ "$rel" = "$scratchpad_example_rel" ] && scratchpad_example_status="unchanged"
      else
        ensure_parent "$dst"
        cp -p "$src" "$dst"
        count_updated=$((count_updated + 1))
        list_updated="$list_updated $rel"
        [ "$rel" = "$scratchpad_example_rel" ] && scratchpad_example_status="updated"
      fi
      continue
    fi

    if [ "$cat" = "user-data" ]; then
      count_preserved=$((count_preserved + 1))
      continue
    fi

    if [ "$cat" = "mixed" ]; then
      count_preserved=$((count_preserved + 1))
      if ! cmp -s "$src" "$dst"; then
        count_review=$((count_review + 1))
        list_review="$list_review $rel"
      fi
      continue
    fi
  done

  scratchpad_postinstall "$TARGET_ROOT" "upgrade"
  validate_install_completeness "$TARGET_ROOT"

  write_installed_version "$TARGET_ROOT" "$APP_VERSION"
  sync_root_readme_to_its_magic "$TARGET_ROOT" || true
  bootstrap_runbook_commands "$TARGET_ROOT"
  [ -n "$BOOTSTRAP_NOTES" ] && printf "%s" "$BOOTSTRAP_NOTES"
  [ "$BOOTSTRAP_OK" = "true" ] || exit 1

  show_banner
  printf "\033[1;32mUpgrade complete: v%s -> v%s\033[0m\n\n" "$OLD_VER" "$APP_VERSION"
  if [ "$count_added" -gt 0 ]; then
    printf "  \033[1;32mAdded (new):         %s files\033[0m\n" "$count_added"
    for f in $list_added; do printf "    %s\n" "$f"; done
  fi
  if [ "$count_updated" -gt 0 ]; then
    printf "  \033[1;33mUpdated (framework): %s files\033[0m\n" "$count_updated"
    for f in $list_updated; do printf "    %s\n" "$f"; done
  fi
  printf "  Unchanged:           %s files\n" "$count_unchanged"
  printf "  Preserved (user):    %s files\n" "$count_preserved"
  [ "$scratchpad_example_status" = "not-seen" ] && scratchpad_example_status="not-in-manifest"
  printf "  Scratchpad example:  %s (.cursor/scratchpad.local.example.md)\n" "$scratchpad_example_status"
  printf "  Scratchpad layers:   post-install refreshed example-first, then baseline (see [SCRATCHPAD_LAYER] lines).\n"
  [ -f "$TARGET_ROOT/.cursor/scratchpad.local.md" ] && printf "  User local file:     preserved (.cursor/scratchpad.local.md)\n"
  if [ "$count_review" -gt 0 ]; then
    printf "\n  \033[1;35mReview recommended:  %s files\033[0m\n" "$count_review"
    for f in $list_review; do printf "    %s\n" "$f"; done
    printf "    Check .cursor/scratchpad.local.example.md for new flags.\n"
  fi
  printf "\nRepository: %s\n\n" "$REPO_URL"
  exit 0
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

scratchpad_postinstall "$TARGET_ROOT" "$MODE"
validate_install_completeness "$TARGET_ROOT"

write_installed_version "$TARGET_ROOT" "$APP_VERSION"
sync_root_readme_to_its_magic "$TARGET_ROOT" || true
bootstrap_runbook_commands "$TARGET_ROOT"
[ -n "$BOOTSTRAP_NOTES" ] && printf "%s" "$BOOTSTRAP_NOTES"
[ "$BOOTSTRAP_OK" = "true" ] || exit 1

show_banner
printf "its-magic v%s\n" "$APP_VERSION"
printf "Repository: %s\n\n" "$REPO_URL"
printf "\033[1;32m                    Installation complete!\033[0m\n\n"
exit 0

