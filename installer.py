import argparse
import json
import os
import shutil
import sys
from datetime import datetime

REPO_URL = "https://github.com/fl0wm0ti0n/its-magic"


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
    choice = input("Enter 1, 2, or 3: ").strip()
    if choice == "1":
        return "missing"
    if choice == "2":
        return "overwrite"
    return "interactive"


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
    print("  --backup          Before overwriting, save existing files to backups/<timestamp>/.")
    print("                    Ignored when mode is 'missing' (nothing gets replaced).")
    print("  --create          Create the target directory if it does not exist.")
    print()
    print("Clean options:")
    print("  --clean-repo      Remove all its-magic workflow artifacts from the target repo")
    print("                    (.cursor, docs/product, docs/engineering, sprints, handoffs,")
    print("                    decisions). Your own source code is never touched.")
    print("  --target <path>   Repo to clean (default: current directory).")
    print("  --yes             Skip the confirmation prompt.")
    print()
    print("Info:")
    print("  --help, -h        Show this help and exit.")
    print("  --version, -v     Print the installed version and exit.")
    print()
    print("Examples:")
    print("  its-magic --target . --mode missing            Safe first-time setup")
    print("  its-magic --target . --mode overwrite --backup   Update all files, keep backup")
    print("  its-magic --clean-repo --target . --yes        Remove workflow artifacts silently")
    print()


def clean_repo(target_root):
    clean_paths = [
        ".cursor",
        os.path.join("docs", "product"),
        os.path.join("docs", "engineering"),
        "sprints",
        "handoffs",
        "decisions",
    ]
    for rel in clean_paths:
        full = os.path.join(target_root, rel)
        if os.path.exists(full):
            shutil.rmtree(full)
            print(f"Removed: {rel}")
    print("Clean completed.")


def main():
    source_root = normalize(os.path.dirname(__file__))
    version = read_version(source_root)

    parser = argparse.ArgumentParser(
        description="Install its-magic into a repo",
        add_help=False,
    )
    parser.add_argument("--target", help="Target repository path")
    parser.add_argument("--mode", choices=["missing", "overwrite", "interactive"], help="Install mode")
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
        clean_repo(target_root)
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

    include_paths = [
        ".cursor/commands",
        ".cursor/rules",
        ".cursor/skills",
        ".cursor/agents",
        ".cursor/hooks",
        ".cursor/hooks.json",
        ".cursor/scratchpad.md",
        ".cursor/scratchpad.local.example.md",
        "docs",
        "sprints",
        "handoffs",
        "decisions",
        ".github/workflows",
        "README.md",
    ]

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
            backup_root = backup_files(target_root, overwrite_candidates)
            print(f"Backup created at: {backup_root}")

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
                    backup_root = backup_files(target_root, [rel])
                    print(f"Backed up: {rel} -> {backup_root}")
                ensure_parent(dst)
                shutil.copy2(src, dst)

    show_banner(include_install_message=True)
    print(f"its-magic v{version}")
    print(f"Repository: {REPO_URL}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

