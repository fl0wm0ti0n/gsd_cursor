import argparse
import filecmp
import importlib.util
import json
import os
import re
import shlex
import shutil
import sys
from datetime import datetime

REPO_URL = "https://github.com/fl0wm0ti0n/its-magic"
MANIFEST_RELATIVE_PATH = os.path.join("docs", "engineering", "context", "installer-owned-paths.manifest")
MANIFEST_REQUIRED_SCRIPTS_SECTION = "required_install_script_paths"


def normalize(path):
    return os.path.normpath(os.path.abspath(path))


def read_version(source_root):
    package_path = os.path.join(source_root, "package.json")
    try:
        with open(package_path, "r", encoding="utf-8") as f:
            return json.load(f).get("version", "unknown")
    except Exception:
        return "unknown"


def list_source_files(source_root, include_paths):
    files = []
    for rel in include_paths:
        src = os.path.join(source_root, rel)
        if os.path.isfile(src):
            files.append(rel)
        elif os.path.isdir(src):
            for root, _, filenames in os.walk(src):
                for name in filenames:
                    full = os.path.join(root, name)
                    rel_path = os.path.relpath(full, source_root)
                    files.append(rel_path)
    return sorted(set(files))


def read_manifest_paths(manifest_path, section_name):
    items = []
    in_section = False
    with open(manifest_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                in_section = line == f"[{section_name}]"
                continue
            if in_section:
                items.append(line)
    return items


def load_ownership_manifest(source_root, script_dir):
    candidates = [
        os.path.join(source_root, MANIFEST_RELATIVE_PATH),
        os.path.join(script_dir, MANIFEST_RELATIVE_PATH),
    ]
    for path in candidates:
        if not os.path.isfile(path):
            continue
        install_paths = read_manifest_paths(path, "install_include_paths")
        clean_paths = read_manifest_paths(path, "clean_paths")
        required_script_paths = read_manifest_paths(path, MANIFEST_REQUIRED_SCRIPTS_SECTION)
        if not install_paths or not clean_paths:
            raise RuntimeError(f"[INSTALL_MANIFEST_ERROR] {path} is missing required sections or entries.")
        if not required_script_paths:
            raise RuntimeError(
                f"[INSTALL_MANIFEST_ERROR] {path} is missing [{MANIFEST_REQUIRED_SCRIPTS_SECTION}] entries."
            )
        return install_paths, clean_paths, required_script_paths, path
    raise RuntimeError("[INSTALL_SOURCE_ERROR] installer-owned-paths.manifest not found. Reinstall its-magic package.")


def validate_install_completeness(target_root, source_root, required_script_paths, manifest_path):
    missing_paths = []
    for rel in sorted(set(required_script_paths)):
        src = os.path.join(source_root, rel)
        dst = os.path.join(target_root, rel)
        if not os.path.isfile(src) or not os.path.isfile(dst):
            missing_paths.append(rel.replace("\\", "/"))
    if not missing_paths:
        return True
    print(
        "[INSTALL_COMPLETENESS_FAILED] Required installer scripts are missing after "
        "copy/classification invariant check."
    )
    for rel in missing_paths:
        print(f"[INSTALL_REQUIRED_SCRIPT_MISSING:{rel}]")
    print(
        "Fix: update manifest parity and required-script inventory at "
        f"{MANIFEST_RELATIVE_PATH} (section [{MANIFEST_REQUIRED_SCRIPTS_SECTION}]), "
        "ensure each listed script exists in template/scripts and clean-path ownership, "
        "then rerun installer missing/upgrade."
    )
    print(f"Manifest source: {manifest_path}")
    return False


def ensure_parent(path):
    parent = os.path.dirname(path)
    if parent and not os.path.isdir(parent):
        os.makedirs(parent, exist_ok=True)


def backup_files(target_root, rel_paths):
    timestamp = datetime.utcnow().strftime("%Y%m%d-%H%M%SZ")
    backup_root = os.path.join(target_root, "backups", timestamp)
    for rel in rel_paths:
        src = os.path.join(target_root, rel)
        if os.path.isfile(src):
            dst = os.path.join(backup_root, rel)
            ensure_parent(dst)
            shutil.copy2(src, dst)
    return backup_root


def choose_mode():
    print("Select install mode:")
    print("1) missing-only (copy only files that do not exist)")
    print("2) overwrite-all (replace existing files)")
    print("3) interactive (prompt per file)")
    print("4) upgrade (update framework files, preserve user data)")
    choice = input("Enter 1, 2, 3, or 4: ").strip()
    if choice == "1":
        return "missing"
    if choice == "2":
        return "overwrite"
    if choice == "4":
        return "upgrade"
    return "interactive"


FRAMEWORK_PREFIXES = (
    ".cursor/commands/", ".cursor/rules/", ".cursor/agents/",
    ".cursor/skills/", ".cursor/hooks/", ".github/workflows/",
    "scripts/validate-and-push", "docs/engineering/context/", "its_magic/",
)
FRAMEWORK_EXACT = {
    ".cursor/hooks.json", ".cursor/scratchpad.local.example.md",
    ".its-magic-version", "its_magic/.its-magic-version", "its_magic/README.md",
}
USER_DATA_PREFIXES = (
    "docs/product/", "docs/engineering/", "docs/user-guides/",
    "sprints/", "handoffs/", "decisions/",
)
MIXED_FILES = {"README.md"}

# Model B (DEC-0055 / US-0073): baseline bytes live in template only; installs materialize `.cursor/scratchpad.md`.
SCRATCHPAD_BASELINE_REL = os.path.join(".cursor", "scratchpad.md")
SCRATCHPAD_EXAMPLE_REL = os.path.join(".cursor", "scratchpad.local.example.md")
SCRATCHPAD_LOCAL_REL = os.path.join(".cursor", "scratchpad.local.md")

# After merge (local > baseline > example), these must be non-empty (fail closed).
REQUIRED_SCRATCHPAD_KEYS = (
    "MAGIC_CONTEXT_STRICT",
    "AUTO_FLOW_MODE",
    "PHASE_MODE",
    "PERMISSION_MODE",
    "AUTO_LOOP_MAX_CYCLES",
    "SYNC_POLICY_MODE",
    "DONE",
    "TEAM_MODE",
)


def parse_scratchpad_file(path):
    """Parse KEY=value lines; empty values are retained (explicit override to empty)."""
    if not os.path.isfile(path):
        return {}
    out = {}
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#") or line.startswith("- "):
                continue
            if "=" not in line:
                continue
            key, _, val = line.partition("=")
            key = key.strip()
            if not key:
                continue
            out[key] = val.strip()
    return out


def merge_scratchpad_layers(target_root):
    """
    Model B merge precedence: local > materialized baseline > example (later wins only when key absent).
    """
    ex_path = os.path.join(target_root, SCRATCHPAD_EXAMPLE_REL)
    base_path = os.path.join(target_root, SCRATCHPAD_BASELINE_REL)
    loc_path = os.path.join(target_root, SCRATCHPAD_LOCAL_REL)
    example = parse_scratchpad_file(ex_path)
    baseline = parse_scratchpad_file(base_path)
    local = parse_scratchpad_file(loc_path)
    merged = {}
    all_keys = set(example) | set(baseline) | set(local)
    for key in all_keys:
        if key in local:
            merged[key] = local[key]
        elif key in baseline:
            merged[key] = baseline[key]
        elif key in example:
            merged[key] = example[key]
    paths = {"example": ex_path, "baseline": base_path, "local": loc_path}
    return merged, paths


def validate_merged_scratchpad(target_root):
    """Return (ok, list of diagnostic lines)."""
    merged, paths = merge_scratchpad_layers(target_root)
    diagnostics = []
    if not os.path.isfile(paths["example"]):
        diagnostics.append(
            "[SCRATCHPAD_MERGE_ERROR] EXAMPLE_LAYER_MISSING: "
            f".cursor/scratchpad.local.example.md not found under {target_root}. "
            "Fix: re-run its-magic install/upgrade."
        )
    if not os.path.isfile(paths["baseline"]):
        diagnostics.append(
            "[SCRATCHPAD_MERGE_ERROR] MATERIALIZED_BASELINE_MISSING: "
            f".cursor/scratchpad.md not found under {target_root}. "
            "Fix: run `python installer.py --scratchpad-postinstall --target <repo> --mode missing` "
            "or re-run its-magic install (Model B materialization; see docs)."
        )
    missing = []
    for key in REQUIRED_SCRATCHPAD_KEYS:
        val = merged.get(key)
        if val is None or str(val).strip() == "":
            missing.append(key)
    if missing:
        diagnostics.append(
            "[SCRATCHPAD_MERGE_ERROR] REQUIRED_KEY_MISSING_AFTER_MERGE: "
            f"keys={','.join(missing)}. Layers consulted: local, baseline|materialized, example "
            f"({paths['local']}, {paths['baseline']}, {paths['example']}). "
            "Fix: set non-empty values in .cursor/scratchpad.local.md or restore materialized baseline from template."
        )
    ok = not diagnostics
    return ok, diagnostics


def materialize_scratchpad_example(target_root, source_root, print_ok=True):
    """
    Always refresh framework-owned scratchpad.local.example from template first
    (example-first ordering before baseline; never touches scratchpad.local.md).
    """
    src = os.path.join(source_root, SCRATCHPAD_EXAMPLE_REL)
    dst = os.path.join(target_root, SCRATCHPAD_EXAMPLE_REL)
    if not os.path.isfile(src):
        print(
            "[SCRATCHPAD_EXAMPLE_ERROR] TEMPLATE_EXAMPLE_MISSING: "
            f"expected template file at {src}. Reinstall its-magic package."
        )
        return False
    ensure_parent(dst)
    shutil.copy2(src, dst)
    if print_ok:
        print(
            "[SCRATCHPAD_LAYER] example_refresh: copied template "
            f"{SCRATCHPAD_EXAMPLE_REL} -> target (ordering: example before baseline)."
        )
    return True


def materialize_scratchpad_baseline(target_root, source_root, mode, print_ok=True):
    """
    Write stable baseline bytes from template when Model B requires it.
    Never touches .cursor/scratchpad.local.md.
    """
    src = os.path.join(source_root, SCRATCHPAD_BASELINE_REL)
    dst = os.path.join(target_root, SCRATCHPAD_BASELINE_REL)
    if not os.path.isfile(src):
        print(
            "[SCRATCHPAD_MATERIALIZE_ERROR] TEMPLATE_BASELINE_MISSING: "
            f"expected template file at {src}. Reinstall its-magic package."
        )
        return False
    wrote = False
    if mode == "overwrite":
        ensure_parent(dst)
        shutil.copy2(src, dst)
        wrote = True
    elif mode == "upgrade":
        if not os.path.isfile(dst):
            ensure_parent(dst)
            shutil.copy2(src, dst)
            wrote = True
    else:
        # missing, interactive
        if not os.path.isfile(dst):
            ensure_parent(dst)
            shutil.copy2(src, dst)
            wrote = True
    if wrote and print_ok:
        print(
            "[SCRATCHPAD_LAYER] baseline_materialize: wrote materialized "
            f"{SCRATCHPAD_BASELINE_REL} from template (Model B)."
        )
    elif print_ok and os.path.isfile(dst):
        print(
            "[SCRATCHPAD_LAYER] baseline_skip: materialized baseline already present "
            f"({SCRATCHPAD_BASELINE_REL}); not overwritten in this mode."
        )
    return True


def _load_doc_profile_lib():
    """
    Load doc_profile_lib from scripts/ adjacent to this installer (repo checkout or npm package root).
    Path is derived from __file__ only (no cwd / PYTHONPATH dependency).
    """
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "scripts", "doc_profile_lib.py")
    if not os.path.isfile(path):
        raise RuntimeError(
            "[DOC_PROFILE_LIB_MISSING] Expected documentation profile library at "
            f"{path} (same directory as installer.py). "
            "Global installs require this file in the published its-magic package; "
            f"reinstall or upgrade its-magic ({REPO_URL})."
        )
    spec = importlib.util.spec_from_file_location("doc_profile_lib", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(
            "[DOC_PROFILE_LIB_LOAD_ERROR] Could not create import spec for "
            f"{path}. Reinstall its-magic ({REPO_URL})."
        )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["doc_profile_lib"] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        sys.modules.pop("doc_profile_lib", None)
        raise RuntimeError(
            "[DOC_PROFILE_LIB_LOAD_ERROR] doc_profile_lib failed to load "
            f"({e!r}). Reinstall its-magic ({REPO_URL})."
        ) from e
    return mod


def _load_dev_environment_lib():
    """Load dev_environment_lib from scripts/ adjacent to this installer."""
    here = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(here, "scripts", "dev_environment_lib.py")
    if not os.path.isfile(path):
        raise RuntimeError(
            "[DEV_ENVIRONMENT_LIB_MISSING] Expected dev environment library at "
            f"{path} (same directory as installer.py). "
            f"Reinstall or upgrade its-magic ({REPO_URL})."
        )
    spec = importlib.util.spec_from_file_location("dev_environment_lib", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(
            "[DEV_ENVIRONMENT_LIB_LOAD_ERROR] Could not create import spec for "
            f"{path}. Reinstall its-magic ({REPO_URL})."
        )
    mod = importlib.util.module_from_spec(spec)
    sys.modules["dev_environment_lib"] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception as e:
        sys.modules.pop("dev_environment_lib", None)
        raise RuntimeError(
            "[DEV_ENVIRONMENT_LIB_LOAD_ERROR] dev_environment_lib failed to load "
            f"({e!r}). Reinstall its-magic ({REPO_URL})."
        ) from e
    return mod


def bootstrap_dev_environment_profile_installer_hook(target_root, source_root):
    """
    Non-destructive dev-environment profile bootstrap.
    Fail-closed only on PATH_INVALID / SOURCE_MISSING.
    """
    try:
        lib = _load_dev_environment_lib()
    except RuntimeError as exc:
        print(str(exc))
        return False
    merged, _paths = merge_scratchpad_layers(target_root)
    reason, _channel = lib.bootstrap_dev_environment_profile(
        target_root, source_root, merged
    )
    if reason in (
        lib.DEV_ENV_BOOTSTRAP_PATH_INVALID,
        lib.DEV_ENV_BOOTSTRAP_SOURCE_MISSING,
    ):
        return False
    return True


def _doc_profile_sync(target_root, merged, print_ok=True):
    """Append missing normative README/developer doc sections from merged profile (non-destructive)."""
    doc_profile_lib = _load_doc_profile_lib()
    notes = doc_profile_lib.ensure_doc_surfaces_merged(merged, target_root, print_ok=print_ok)
    bad = [ln for ln in notes if ln.startswith("[DOC_PROFILE_INVALID]")]
    return (not bad), notes


def run_scratchpad_postinstall(target_root, source_root, mode, print_ok=True):
    if not materialize_scratchpad_example(target_root, source_root, print_ok=print_ok):
        return False
    if not materialize_scratchpad_baseline(target_root, source_root, mode, print_ok=print_ok):
        return False
    ok, diagnostics = validate_merged_scratchpad(target_root)
    for line in diagnostics:
        print(line)
    if ok:
        merged, _paths = merge_scratchpad_layers(target_root)
        try:
            dp_ok, dp_notes = _doc_profile_sync(target_root, merged, print_ok=print_ok)
        except RuntimeError as e:
            print(str(e))
            ok = False
        else:
            for line in dp_notes:
                print(line)
            if not dp_ok:
                ok = False
    if ok and print_ok:
        loc = os.path.join(target_root, SCRATCHPAD_LOCAL_REL)
        if os.path.isfile(loc):
            print(
                "[SCRATCHPAD_LAYER] user_local: preserved "
                f"{SCRATCHPAD_LOCAL_REL} (merge precedence unchanged)."
            )
        print(
            "[SCRATCHPAD_POSTINSTALL_OK] Model B: example refreshed, baseline handled, "
            "merged scratchpad validation passed."
        )
    return ok


def classify_file(rel_path):
    normalized = rel_path.replace(os.sep, "/")
    if normalized in MIXED_FILES:
        return "mixed"
    for p in FRAMEWORK_PREFIXES:
        if normalized.startswith(p):
            return "framework"
    if normalized in FRAMEWORK_EXACT:
        return "framework"
    for p in USER_DATA_PREFIXES:
        if normalized.startswith(p):
            return "user-data"
    return "framework"


def read_installed_version(target_root):
    primary = os.path.join(target_root, "its_magic", ".its-magic-version")
    if os.path.isfile(primary):
        with open(primary, "r", encoding="utf-8") as f:
            return f.read().strip()
    legacy = os.path.join(target_root, ".its-magic-version")
    if os.path.isfile(legacy):
        with open(legacy, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "unknown"


def write_installed_version(target_root, ver):
    vf = os.path.join(target_root, "its_magic", ".its-magic-version")
    ensure_parent(vf)
    with open(vf, "w", encoding="utf-8") as f:
        f.write(ver)
    legacy = os.path.join(target_root, ".its-magic-version")
    if os.path.isfile(legacy):
        os.remove(legacy)


def sync_root_readme_to_its_magic(target_root):
    root_readme = os.path.join(target_root, "README.md")
    if not os.path.isfile(root_readme):
        return False
    its_magic_readme = os.path.join(target_root, "its_magic", "README.md")
    ensure_parent(its_magic_readme)
    shutil.copy2(root_readme, its_magic_readme)
    return True


def read_runbook_key(runbook_path, key):
    if not os.path.isfile(runbook_path):
        return ""
    needle = f"{key}:"
    with open(runbook_path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith(needle):
                return line[len(needle):].strip()
    return ""


def write_runbook_key(runbook_path, key, value):
    with open(runbook_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
    needle = f"{key}:"
    changed = False
    for idx, raw in enumerate(lines):
        line = raw.rstrip("\n")
        if line.startswith(needle):
            lines[idx] = f"{needle} {value}\n"
            changed = True
            break
    if changed:
        with open(runbook_path, "w", encoding="utf-8") as f:
            f.writelines(lines)
    return changed


def package_has_script(target_root, script_name):
    pkg_path = os.path.join(target_root, "package.json")
    if not os.path.isfile(pkg_path):
        return False
    try:
        with open(pkg_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)
        scripts = pkg.get("scripts", {})
        val = scripts.get(script_name)
        return isinstance(val, str) and val.strip() != ""
    except Exception:
        return False


def detect_runbook_defaults(target_root):
    tests_sh = os.path.join(target_root, "tests", "run-tests.sh")
    has_pkg = os.path.isfile(os.path.join(target_root, "package.json"))
    has_py = any(
        os.path.isfile(os.path.join(target_root, p))
        for p in ("pyproject.toml", "requirements.txt", "setup.py")
    )
    has_go = os.path.isfile(os.path.join(target_root, "go.mod"))

    result = {"TEST_COMMAND": "", "LINT_COMMAND": "", "TYPECHECK_COMMAND": ""}

    if has_pkg and package_has_script(target_root, "test"):
        result["TEST_COMMAND"] = "npm run test"
        if package_has_script(target_root, "lint"):
            result["LINT_COMMAND"] = "npm run lint"
        if package_has_script(target_root, "typecheck"):
            result["TYPECHECK_COMMAND"] = "npm run typecheck"
    elif has_go:
        result["TEST_COMMAND"] = "go test ./..."
    elif has_py:
        result["TEST_COMMAND"] = "python -m pytest"
    elif os.path.isfile(tests_sh):
        result["TEST_COMMAND"] = "sh tests/run-tests.sh"

    return result


def validate_bootstrap_command(target_root, key, command):
    if not command:
        return False, f"{key}_UNDETECTED"
    if command.startswith("npm run "):
        if not shutil.which("npm"):
            return False, "NPM_NOT_FOUND"
        script_name = command[len("npm run "):].strip()
        if not package_has_script(target_root, script_name):
            return False, f"NPM_SCRIPT_MISSING:{script_name}"
        return True, "OK"
    if command.startswith("python -m "):
        if not shutil.which("python"):
            return False, "PYTHON_NOT_FOUND"
        if command == "python -m pytest":
            has_py = any(
                os.path.isfile(os.path.join(target_root, p))
                for p in ("pyproject.toml", "requirements.txt", "setup.py")
            )
            if not has_py:
                return False, "PYTHON_STACK_MARKERS_MISSING"
        return True, "OK"
    if command.startswith("go test "):
        if not shutil.which("go"):
            return False, "GO_NOT_FOUND"
        if not os.path.isfile(os.path.join(target_root, "go.mod")):
            return False, "GO_MOD_MISSING"
        return True, "OK"
    if command.startswith("powershell "):
        if not os.path.isfile(os.path.join(target_root, "tests", "run-tests.ps1")):
            return False, "RUN_TESTS_PS1_MISSING"
        return True, "OK"
    if command.startswith("sh "):
        if not shutil.which("sh"):
            return False, "SH_NOT_FOUND"
        if not os.path.isfile(os.path.join(target_root, "tests", "run-tests.sh")):
            return False, "RUN_TESTS_SH_MISSING"
        return True, "OK"
    try:
        parts = shlex.split(command)
    except ValueError:
        return False, "COMMAND_PARSE_FAILED"
    if not parts:
        return False, "COMMAND_EMPTY"
    if not shutil.which(parts[0]):
        return False, f"EXECUTABLE_NOT_FOUND:{parts[0]}"
    return True, "OK"


def bootstrap_runbook_commands(target_root):
    runbook_path = os.path.join(target_root, "docs", "engineering", "runbook.md")
    if not os.path.isfile(runbook_path):
        return True, []

    defaults = detect_runbook_defaults(target_root)
    diagnostics = []
    changed = []

    for key in ("TEST_COMMAND", "LINT_COMMAND", "TYPECHECK_COMMAND"):
        current = read_runbook_key(runbook_path, key)
        if current:
            continue
        candidate = defaults.get(key, "")
        if not candidate:
            if key == "TEST_COMMAND":
                diagnostics.append(
                    "[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_UNRESOLVED: could not detect a valid baseline test command. "
                    "Fix: define TEST_COMMAND in docs/engineering/runbook.md or add detectable stack markers (package.json scripts.test, pyproject.toml, go.mod)."
                )
            continue
        valid, reason = validate_bootstrap_command(target_root, key, candidate)
        if valid:
            if write_runbook_key(runbook_path, key, candidate):
                changed.append(f"{key}={candidate}")
        elif key == "TEST_COMMAND":
            diagnostics.append(
                f"[RUNBOOK_BOOTSTRAP_ERROR] TEST_COMMAND_INVALID:{reason}. "
                "Fix: set a valid TEST_COMMAND in docs/engineering/runbook.md."
            )

    if changed:
        diagnostics.append("[RUNBOOK_BOOTSTRAP] Applied defaults: " + ", ".join(changed))

    has_test = read_runbook_key(runbook_path, "TEST_COMMAND") != ""
    if not has_test:
        return False, diagnostics
    return True, diagnostics


def prompt_yes_no(label, default=False):
    suffix = "Y/n" if default else "y/N"
    value = input(f"{label} [{suffix}]: ").strip().lower()
    if not value:
        return default
    return value in ("y", "yes")


def show_banner(include_install_message=False):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    m = "\033[1;35m"
    c = "\033[1;36m"
    y = "\033[1;33m"
    g = "\033[1;32m"
    r = "\033[0m"
    print()
    print(f"{m}  ██╗████████╗███████╗      ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗{r}")
    print(f"{m}  ██║╚══██╔══╝██╔════╝      ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝{r}")
    print(f"{m}  ██║   ██║   ███████╗█████╗██╔████╔██║███████║██║  ███╗██║██║     {r}")
    print(f"{c}  ██║   ██║   ╚════██║╚════╝██║╚██╔╝██║██╔══██║██║   ██║██║██║     {r}")
    print(f"{c}  ██║   ██║   ███████║      ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗{r}")
    print(f"{c}  ╚═╝   ╚═╝   ╚══════╝      ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝{r}")
    print()
    print(f"{y}                         AI dev team{r}")
    if include_install_message:
        print(f"{g}                    Installation complete!{r}")
    print()


def show_help(version):
    show_banner(include_install_message=False)
    print(f"its-magic v{version}")
    print(f"Repository: {REPO_URL}")
    print()
    print("Install AI dev team workflow files into any Cursor repository.")
    print()
    print("Usage:")
    print("  its-magic --target <path> [--mode <mode>] [--backup] [--create]")
    print("  its-magic --clean-repo [--target <path>] [--yes]")
    print("  its-magic --help | --version")
    print()
    print("Install options:")
    print("  --target <path>   Path to the repository where workflow files are installed.")
    print("                    If omitted you will be prompted interactively.")
    print("  --mode <mode>     How to handle files that already exist in the target:")
    print("                      missing      Only copy files that do not exist yet (default).")
    print("                                   Safe for repos that already have some workflow files.")
    print("                      overwrite    Replace every file, even if it already exists.")
    print("                                   Combine with --backup to keep a snapshot first.")
    print("                      interactive  Ask per file whether to overwrite or skip.")
    print("                      upgrade      Update framework files while preserving user data.")
    print("                                   Use after updating its-magic to a newer version.")
    print("  --backup          Before overwriting, save existing files to backups/<timestamp>/.")
    print("                    Ignored when mode is 'missing' (nothing gets replaced).")
    print("  --create          Create the target directory if it does not exist.")
    print("  Note: installer bootstraps runbook TEST/LINT/TYPECHECK commands")
    print("        from OS+stack detection; unresolved TEST_COMMAND fails fast with")
    print("        [RUNBOOK_BOOTSTRAP_ERROR] diagnostics.")
    print("  Note: scratchpad Model B: `.cursor/scratchpad.md` is")
    print("        materialized from the packaged template when missing; merged validation")
    print("        requires Python 3 on PATH for installer.ps1 / installer.sh. Recovery:")
    print("        python installer.py --scratchpad-postinstall --target <repo> --mode missing")
    print()
    print("Clean options:")
    print("  --clean-repo      Remove all its-magic workflow artifacts from the target repo")
    print("                    (owned paths from installer manifest, including .cursor,")
    print("                    docs/product, docs/engineering, docs/user-guides, sprints,")
    print("                    handoffs, decisions, workflow scripts, CI files, and")
    print("                    installer metadata under its_magic/ (legacy .its-magic-version")
    print("                    is also removed when present). Your own source code is never touched.")
    print("  --target <path>   Repo to clean (default: current directory).")
    print("  --yes             Skip the confirmation prompt.")
    print()
    print("Info:")
    print("  --help, -h        Show this help and exit.")
    print("  --version, -v     Print the installed version and exit.")
    print()
    print("Examples:")
    print("  its-magic --target . --mode missing              Safe first-time setup")
    print("  its-magic --target . --mode upgrade               Update framework, keep user data")
    print("  its-magic --target . --mode overwrite --backup    Replace all files, keep backup")
    print("  its-magic --clean-repo --target . --yes           Remove workflow artifacts silently")
    print()


def clean_repo(target_root, clean_paths):
    for rel in clean_paths:
        full = os.path.join(target_root, rel)
        if os.path.exists(full):
            if os.path.isdir(full):
                shutil.rmtree(full)
            else:
                os.remove(full)
            print(f"Removed: {rel}")
    print("Clean completed.")


def main():
    script_dir = normalize(os.path.dirname(__file__))
    template_dir = os.path.join(script_dir, "template")
    source_root = template_dir
    version = read_version(script_dir)

    parser = argparse.ArgumentParser(
        description="Install its-magic into a repo",
        add_help=False,
    )
    parser.add_argument("--target", help="Target repository path")
    parser.add_argument("--mode", choices=["missing", "overwrite", "interactive", "upgrade"], help="Install mode")
    parser.add_argument("--backup", action="store_true", help="Backup files before overwriting")
    parser.add_argument("--create", action="store_true", help="Create target directory if missing")
    parser.add_argument("--clean-repo", action="store_true", help="Remove installed workflow artifacts")
    parser.add_argument("--yes", action="store_true", help="Skip clean confirmation prompt")
    parser.add_argument("--help", "-h", action="store_true", help="Show help")
    parser.add_argument("--version", "-v", action="store_true", help="Show version")
    parser.add_argument(
        "--scratchpad-postinstall",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    parser.add_argument("--source-root", help=argparse.SUPPRESS)
    parser.add_argument(
        "--validate-install-completeness",
        action="store_true",
        help=argparse.SUPPRESS,
    )
    args = parser.parse_args()

    if len(sys.argv) == 1 or args.help:
        show_help(version)
        return 0

    if args.version:
        print(f"its-magic v{version}")
        return 0

    if args.source_root:
        source_root = normalize(args.source_root)

    if args.scratchpad_postinstall:
        target_root = normalize(args.target) if args.target else normalize(".")
        mode = args.mode or "missing"
        if mode not in ("missing", "overwrite", "interactive", "upgrade"):
            print(
                "[SCRATCHPAD_POSTINSTALL_ERROR] INVALID_MODE: use --mode "
                "missing|overwrite|interactive|upgrade with --scratchpad-postinstall."
            )
            return 1
        if not os.path.isdir(source_root):
            print("[INSTALL_SOURCE_ERROR] template directory is missing. Reinstall its-magic package.")
            return 1
        if not os.path.isdir(target_root):
            print(f"[SCRATCHPAD_POSTINSTALL_ERROR] TARGET_MISSING: {target_root}")
            return 1
        ok = run_scratchpad_postinstall(target_root, source_root, mode, print_ok=True)
        return 0 if ok else 1

    if args.validate_install_completeness:
        target_root = normalize(args.target) if args.target else normalize(".")
        if not os.path.isdir(target_root):
            print(f"[INSTALL_COMPLETENESS_FAILED] target directory missing: {target_root}")
            return 1
        if not os.path.isdir(source_root):
            print("[INSTALL_SOURCE_ERROR] template directory is missing. Reinstall its-magic package.")
            return 1
        try:
            _install_paths, _clean_paths, required_script_paths, manifest_path = load_ownership_manifest(
                source_root, script_dir
            )
        except RuntimeError as exc:
            print(str(exc))
            return 1
        ok = validate_install_completeness(target_root, source_root, required_script_paths, manifest_path)
        return 0 if ok else 1

    if not os.path.isdir(source_root):
        print("[INSTALL_SOURCE_ERROR] template directory is missing. Reinstall its-magic package.")
        return 1
    try:
        include_paths, clean_paths, required_script_paths, manifest_path = load_ownership_manifest(
            source_root, script_dir
        )
    except RuntimeError as exc:
        print(str(exc))
        return 1

    target_root = normalize(args.target) if args.target else None

    if args.clean_repo:
        if not target_root:
            target_root = normalize(".")
        if not os.path.isdir(target_root):
            print("Target directory does not exist.")
            return 1
        if not args.yes and not prompt_yes_no(f"Clean its-magic workflow artifacts in {target_root}?", default=False):
            print("Aborted.")
            return 1
        clean_repo(target_root, clean_paths)
        return 0

    if not target_root:
        target_root = normalize(input("Target repository path: ").strip())

    if not os.path.isdir(target_root):
        if args.create or prompt_yes_no("Target missing. Create?", default=False):
            os.makedirs(target_root, exist_ok=True)
        else:
            print("Target directory does not exist.")
            return 1

    mode = args.mode or choose_mode()
    backup_enabled = args.backup
    if mode in ("overwrite", "interactive") and not args.backup:
        backup_enabled = prompt_yes_no("Backup existing files before overwrite?", False)

    files = list_source_files(source_root, include_paths)
    if not files:
        print("No source files found to install.")
        return 1

    overwrite_candidates = []
    if backup_enabled and mode == "overwrite":
        for rel in files:
            if os.path.isfile(os.path.join(target_root, rel)):
                overwrite_candidates.append(rel)
        if overwrite_candidates:
            broot = backup_files(target_root, overwrite_candidates)
            print(f"Backup created at: {broot}")

    if mode == "upgrade":
        old_ver = read_installed_version(target_root)
        print(f"\n\033[1;36mUpgrading from v{old_ver} to v{version}\033[0m\n")

        if backup_enabled:
            bc = [r for r in files if classify_file(r) == "framework" and os.path.isfile(os.path.join(target_root, r))]
            if bc:
                broot = backup_files(target_root, bc)
                print(f"Backup created at: {broot}")

        added, updated, review = [], [], []
        unchanged = preserved = 0
        scratchpad_example_rel = ".cursor/scratchpad.local.example.md"
        scratchpad_example_status = "not-seen"

        for rel in files:
            src = os.path.join(source_root, rel)
            dst = os.path.join(target_root, rel)
            exists = os.path.isfile(dst)
            cat = classify_file(rel)

            if not exists:
                ensure_parent(dst)
                shutil.copy2(src, dst)
                added.append(rel)
                if rel == scratchpad_example_rel:
                    scratchpad_example_status = "added"
                continue

            if cat == "framework":
                if filecmp.cmp(src, dst, shallow=False):
                    unchanged += 1
                    if rel == scratchpad_example_rel:
                        scratchpad_example_status = "unchanged"
                else:
                    ensure_parent(dst)
                    shutil.copy2(src, dst)
                    updated.append(rel)
                    if rel == scratchpad_example_rel:
                        scratchpad_example_status = "updated"
                continue

            if cat == "user-data":
                preserved += 1
                continue

            if cat == "mixed":
                preserved += 1
                if not filecmp.cmp(src, dst, shallow=False):
                    review.append(rel)
                continue

        if not run_scratchpad_postinstall(target_root, source_root, "upgrade", print_ok=True):
            return 1
        if not bootstrap_dev_environment_profile_installer_hook(target_root, source_root):
            return 1
        if not validate_install_completeness(target_root, source_root, required_script_paths, manifest_path):
            return 1

        write_installed_version(target_root, version)
        sync_root_readme_to_its_magic(target_root)
        runbook_ok, runbook_notes = bootstrap_runbook_commands(target_root)
        for note in runbook_notes:
            print(note)
        if not runbook_ok:
            return 1

        show_banner()
        g = "\033[1;32m"
        y = "\033[1;33m"
        p = "\033[1;35m"
        d = "\033[0;90m"
        r = "\033[0m"
        print(f"{g}Upgrade complete: v{old_ver} -> v{version}{r}\n")
        if added:
            print(f"  {g}Added (new):         {len(added)} files{r}")
            for f in added:
                print(f"    {f}")
        if updated:
            print(f"  {y}Updated (framework): {len(updated)} files{r}")
            for f in updated:
                print(f"    {f}")
        print(f"  Unchanged:           {unchanged} files")
        print(f"  Preserved (user):    {preserved} files")
        if scratchpad_example_status == "not-seen":
            scratchpad_example_status = "not-in-manifest"
        print(f"  Scratchpad example:  {scratchpad_example_status} (.cursor/scratchpad.local.example.md)")
        print(
            "  Scratchpad layers:   post-install refreshed example-first, then baseline "
            "(see [SCRATCHPAD_LAYER] lines)."
        )
        if os.path.isfile(os.path.join(target_root, ".cursor", "scratchpad.local.md")):
            print("  User local file:     preserved (.cursor/scratchpad.local.md)")
        if review:
            print(f"\n  {p}Review recommended:  {len(review)} files{r}")
            for f in review:
                print(f"    {f}")
            print(f"    {d}Check .cursor/scratchpad.local.example.md for new flags.{r}")
        print(f"\nRepository: {REPO_URL}\n")
        return 0

    for rel in files:
        src = os.path.join(source_root, rel)
        dst = os.path.join(target_root, rel)
        exists = os.path.isfile(dst)

        if mode == "missing":
            if exists:
                continue
            ensure_parent(dst)
            shutil.copy2(src, dst)
            continue

        if mode == "overwrite":
            ensure_parent(dst)
            shutil.copy2(src, dst)
            continue

        if mode == "interactive":
            if not exists:
                ensure_parent(dst)
                shutil.copy2(src, dst)
                continue
            answer = input(f"File exists: {rel} | [o]verwrite [s]kip [q]uit: ").strip().lower()
            if answer == "q":
                print("Aborted.")
                return 1
            if answer == "o":
                if backup_enabled:
                    broot = backup_files(target_root, [rel])
                    print(f"Backed up: {rel} -> {broot}")
                ensure_parent(dst)
                shutil.copy2(src, dst)

    if not run_scratchpad_postinstall(target_root, source_root, mode, print_ok=True):
        return 1
    if not bootstrap_dev_environment_profile_installer_hook(target_root, source_root):
        return 1
    if not validate_install_completeness(target_root, source_root, required_script_paths, manifest_path):
        return 1

    write_installed_version(target_root, version)
    sync_root_readme_to_its_magic(target_root)
    runbook_ok, runbook_notes = bootstrap_runbook_commands(target_root)
    for note in runbook_notes:
        print(note)
    if not runbook_ok:
        return 1

    show_banner(include_install_message=True)
    print(f"its-magic v{version}")
    print(f"Repository: {REPO_URL}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

