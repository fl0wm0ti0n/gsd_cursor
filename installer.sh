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
  printf "  --create          Create the target directory if it does not exist.\n"
  printf "  --host <value>    Host-surface switch: cursor | opencode | both (default: cursor).\n"
  printf "                    Normalized case-insensitive and whitespace-trimmed before validate.\n"
  printf "                    Unknown value -> exit with INSTALL_HOST_INVALID.\n"
  printf "                    Duplicate --host argv -> fail closed INSTALL_HOST_INVALID (no last-wins).\n"
  printf "                    --host gates ONLY .cursor/ and .opencode/ trees; kernel paths\n"
  printf "                    (docs/, scripts/, its_magic/, handoffs/, decisions/, sprints/,\n"
  printf "                    .github/workflows/) always install regardless of --host.\n\n"
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

# US-0121 / DEC-0120 §1: normalize-then-validate --host (Bash is case-sensitive;
# normalize lowercase). Unknown or duplicate -> fail closed INSTALL_HOST_INVALID.
host_normalize() {
  printf '%s' "$1" | tr '[:upper:]' '[:lower:]' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//'
}

host_is_valid() {
  case "$1" in
    cursor|opencode|both) return 0 ;;
    *) return 1 ;;
  esac
}

# DEC-0120 §4: shared predicate. Returns 0 (true) if row should be SKIPPED.
host_gates_cursor_row() {
  rel="$1"; host="$2"
  if [ "$host" = "opencode" ]; then
    case "$rel" in
      .cursor/*) return 0 ;;
      *) return 1 ;;
    esac
  fi
  return 1
}

host_includes_opencode() {
  [ "$1" = "opencode" ] || [ "$1" = "both" ]
}

host_includes_cursor() {
  [ "$1" = "cursor" ] || [ "$1" = "both" ]
}

build_effective_include_paths() {
  install_paths="$1"; opencode_install_paths="$2"; host="$3"
  eff=""
  for rel in $install_paths; do
    if host_gates_cursor_row "$rel" "$host"; then continue; fi
    eff="$eff $rel"
  done
  if host_includes_opencode "$host"; then
    for rel in $opencode_install_paths; do eff="$eff $rel"; done
  fi
  printf '%s' "$eff" | sed 's/^ *//'
}

build_effective_clean_paths() {
  clean_paths="$1"; opencode_clean_paths="$2"; host="$3"
  eff=""
  if host_includes_cursor "$host"; then
    for rel in $clean_paths; do eff="$eff $rel"; done
  fi
  if host_includes_opencode "$host"; then
    for rel in $opencode_clean_paths; do eff="$eff $rel"; done
  fi
  printf '%s' "$eff" | sed 's/^ *//'
}

emit_host_shrink_diagnostics() {
  target_root="$1"; host="$2"
  if [ "$host" = "cursor" ] && [ -e "$target_root/.opencode" ]; then
    printf '%s\n' "[OPENCODE_ORPHANED_BY_CLEAN_CURSOR] .opencode/ exists from a prior --host both install; --host cursor does not remove it. Run 'its-magic --clean-repo --host opencode|both' to remove it."
  fi
  if [ "$host" = "opencode" ] && [ -d "$target_root/.cursor" ]; then
    printf '%s\n' "[CURSOR_ORPHANED_BY_CLEAN_OPENCODE] .cursor/ exists from a prior --host both install; --host opencode does not remove it. Run 'its-magic --clean-repo --host cursor|both' to remove it."
  fi
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
  if ! host_includes_cursor "$HOST"; then
    printf '%s\n' "[CURSOR_HOST_HOOKS_SKIPPED] --host opencode does not materialize .cursor/ (scratchpad Model B + dev-env profile)."
    return 0
  fi
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

opencode_model_catalog_apply() {
  target_root="$1"
  if ! host_includes_opencode "$HOST"; then
    return 0
  fi
  catalog_path="$target_root/.opencode/model-catalog.local.json"
  if [ ! -f "$catalog_path" ]; then
    printf '%s\n' "[OPENCODE_MODEL_CATALOG_SKIPPED] no .opencode/model-catalog.local.json at install target (optional catalog)."
    return 0
  fi
  script_path="$SCRIPT_DIR/scripts/opencode_model_catalog_apply.py"
  if [ ! -f "$script_path" ]; then
    printf '%s\n' "[OPENCODE_MODEL_CATALOG_ERROR] scripts/opencode_model_catalog_apply.py not found next to installer.sh."
    exit 1
  fi
  if command -v python3 >/dev/null 2>&1; then
    python3 "$script_path" --target "$target_root" || exit $?
  elif command -v python >/dev/null 2>&1; then
    python "$script_path" --target "$target_root" || exit $?
  else
    printf '%s\n' "[OPENCODE_MODEL_CATALOG_ERROR] PYTHON_NOT_FOUND: Python is required for OpenCode model catalog materialization."
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
  fallback_readme="$2"
  marker="intent contract:"
  src_readme=""
  if [ -n "$fallback_readme" ] && [ -f "$fallback_readme" ]; then
    if [ ! -f "$target_root/README.md" ]; then
      src_readme="$fallback_readme"
    elif ! grep -qF "$marker" "$target_root/README.md" 2>/dev/null; then
      src_readme="$fallback_readme"
    fi
  fi
  if [ -z "$src_readme" ] && [ -f "$target_root/README.md" ]; then
    src_readme="$target_root/README.md"
  elif [ -z "$src_readme" ] && [ -n "$fallback_readme" ] && [ -f "$fallback_readme" ]; then
    src_readme="$fallback_readme"
  fi
  if [ -z "$src_readme" ]; then
    return 1
  fi
  dst="$target_root/its_magic/README.md"
  ensure_parent "$dst"
  cp -p "$src_readme" "$dst"
  return 0
}

should_bootstrap_test_command() {
  current="$1"
  candidate="$2"
  [ -n "$candidate" ] || return 1
  [ -z "$current" ] && return 0
  case "$candidate" in
    "npm run test"*|sh\ tests/run-tests*)
      case "$(printf "%s" "$current" | tr 'A-Z' 'a-z')" in
        'powershell -executionpolicy bypass -file "tests/run-tests.ps1"'|\
        'powershell -executionpolicy bypass -file tests/run-tests.ps1')
          return 0 ;;
      esac
      ;;
  esac
  return 1
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
    candidate=""
    [ "$key" = "TEST_COMMAND" ] && candidate="$TEST_CANDIDATE"
    [ "$key" = "LINT_COMMAND" ] && candidate="$LINT_CANDIDATE"
    [ "$key" = "TYPECHECK_COMMAND" ] && candidate="$TYPECHECK_CANDIDATE"
    if [ "$key" = "TEST_COMMAND" ]; then
      should_bootstrap_test_command "$current" "$candidate" || continue
    elif [ -n "$current" ]; then
      continue
    fi
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
HOST=""
HOST_SEEN=0
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
    --host)
      HOST_SEEN=$((HOST_SEEN + 1))
      if [ "$HOST_SEEN" -gt 1 ]; then
        printf '%s\n' "[INSTALL_HOST_INVALID] duplicate --host argv (no last-wins). Accepted: cursor | opencode | both (default: cursor)."
        exit 1
      fi
      RAW_HOST="$2"
      HOST=$(host_normalize "$RAW_HOST")
      if ! host_is_valid "$HOST"; then
        printf '%s\n' "[INSTALL_HOST_INVALID] unknown host value '$HOST'. Accepted: cursor | opencode | both (default: cursor)."
        exit 1
      fi
      shift 2 ;;
    --backup) BACKUP="true"; shift 1 ;;
    --create) CREATE="true"; shift 1 ;;
    --clean-repo) CLEAN_REPO="true"; shift 1 ;;
    --yes) ASSUME_YES="true"; shift 1 ;;
    --help|-h) SHOW_HELP="true"; shift 1 ;;
    --version|-v) SHOW_VERSION="true"; shift 1 ;;
    *) shift 1 ;;
  esac
done

[ -z "$HOST" ] && HOST="cursor"

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
  OPENCODE_CLEAN_PATHS=$(get_manifest_paths "opencode_clean_paths")
  EFFECTIVE_CLEAN_PATHS=$(build_effective_clean_paths "$CLEAN_PATHS" "$OPENCODE_CLEAN_PATHS" "$HOST")
  for rel in $EFFECTIVE_CLEAN_PATHS; do
    path="$TARGET_ROOT/$rel"
    if [ -e "$path" ]; then
      rm -rf "$path"
      printf "%s\n" "Removed: $rel"
    fi
  done
  printf "%s\n" "Clean completed."
  if [ "$HOST" != "both" ]; then
    emit_host_shrink_diagnostics "$TARGET_ROOT" "$HOST"
  fi
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
OPENCODE_INCLUDE_PATHS=$(get_manifest_paths "opencode_install_include_paths")
EFFECTIVE_INCLUDE_PATHS=$(build_effective_include_paths "$INCLUDE_PATHS" "$OPENCODE_INCLUDE_PATHS" "$HOST")

FILES=$(list_source_files "$SOURCE_ROOT" $EFFECTIVE_INCLUDE_PATHS)
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
  opencode_model_catalog_apply "$TARGET_ROOT"
  validate_install_completeness "$TARGET_ROOT"

  if [ "$HOST" = "cursor" ] && [ -e "$TARGET_ROOT/.opencode" ]; then
    printf '%s\n' "[OPENCODE_STALE_BY_UPGRADE_CURSOR] .opencode/ exists from a prior --host both install; --host cursor upgrade does not refresh it. Run 'its-magic --target <repo> --mode upgrade --host opencode|both' to refresh it."
  fi
  if [ "$HOST" = "opencode" ] && [ -d "$TARGET_ROOT/.cursor" ]; then
    printf '%s\n' "[CURSOR_STALE_BY_UPGRADE_OPENCODE] .cursor/ exists from a prior --host both install; --host opencode upgrade does not refresh it. Run 'its-magic --target <repo> --mode upgrade --host cursor|both' to refresh it."
  fi

  write_installed_version "$TARGET_ROOT" "$APP_VERSION"
  sync_root_readme_to_its_magic "$TARGET_ROOT" "$SCRIPT_DIR/README.md" || true
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
opencode_model_catalog_apply "$TARGET_ROOT"
validate_install_completeness "$TARGET_ROOT"

write_installed_version "$TARGET_ROOT" "$APP_VERSION"
sync_root_readme_to_its_magic "$TARGET_ROOT" "$SCRIPT_DIR/README.md" || true
bootstrap_runbook_commands "$TARGET_ROOT"
[ -n "$BOOTSTRAP_NOTES" ] && printf "%s" "$BOOTSTRAP_NOTES"
[ "$BOOTSTRAP_OK" = "true" ] || exit 1

show_banner
printf "its-magic v%s\n" "$APP_VERSION"
printf "Repository: %s\n\n" "$REPO_URL"
printf "\033[1;32m                    Installation complete!\033[0m\n\n"
exit 0

