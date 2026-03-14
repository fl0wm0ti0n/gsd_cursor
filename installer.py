import argparse
import filecmp
import json
import os
import shutil
import sys
from datetime import datetime

REPO_URL = "https://github.com/fl0wm0ti0n/its-magic"
MANIFEST_RELATIVE_PATH = os.path.join("docs", "engineering", "context", "installer-owned-paths.manifest")


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
        if not install_paths or not clean_paths:
            raise RuntimeError(f"[INSTALL_MANIFEST_ERROR] {path} is missing required sections or entries.")
        return install_paths, clean_paths
    raise RuntimeError("[INSTALL_SOURCE_ERROR] installer-owned-paths.manifest not found. Reinstall its-magic package.")


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
    "scripts/validate-and-push", "docs/engineering/context/",
)
FRAMEWORK_EXACT = {
    ".cursor/hooks.json", ".cursor/scratchpad.local.example.md",
    ".its-magic-version",
}
USER_DATA_PREFIXES = (
    "docs/product/", "docs/engineering/", "docs/user-guides/",
    "sprints/", "handoffs/", "decisions/",
)
MIXED_FILES = {".cursor/scratchpad.md", "README.md"}


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
    vf = os.path.join(target_root, ".its-magic-version")
    if os.path.isfile(vf):
        with open(vf, "r", encoding="utf-8") as f:
            return f.read().strip()
    return "unknown"


def write_installed_version(target_root, ver):
    vf = os.path.join(target_root, ".its-magic-version")
    with open(vf, "w", encoding="utf-8") as f:
        f.write(ver)


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
    print()
    print("Clean options:")
    print("  --clean-repo      Remove all its-magic workflow artifacts from the target repo")
    print("                    (owned paths from installer manifest, including .cursor,")
    print("                    docs/product, docs/engineering, docs/user-guides, sprints,")
    print("                    handoffs, decisions, workflow scripts, CI files, and")
    print("                    .its-magic-version). Your own source code is never touched.")
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
    args = parser.parse_args()

    if len(sys.argv) == 1 or args.help:
        show_help(version)
        return 0

    if args.version:
        print(f"its-magic v{version}")
        return 0

    if not os.path.isdir(source_root):
        print("[INSTALL_SOURCE_ERROR] template directory is missing. Reinstall its-magic package.")
        return 1
    try:
        include_paths, clean_paths = load_ownership_manifest(source_root, script_dir)
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

        write_installed_version(target_root, version)

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

    write_installed_version(target_root, version)

    show_banner(include_install_message=True)
    print(f"its-magic v{version}")
    print(f"Repository: {REPO_URL}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

