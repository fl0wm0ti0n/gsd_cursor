import argparse
import os
import shutil
import sys
from datetime import datetime


def normalize(path):
    return os.path.normpath(os.path.abspath(path))


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
    backup_root = os.path.join(target_root, "gsd-backups", timestamp)
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


def main():
    parser = argparse.ArgumentParser(description="Install GSD toolkit into a repo")
    parser.add_argument("--target", help="Target repository path")
    parser.add_argument(
        "--mode",
        choices=["missing", "overwrite", "interactive"],
        help="Install mode",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Backup files before overwriting",
    )
    parser.add_argument(
        "--create",
        action="store_true",
        help="Create target directory if missing",
    )
    args = parser.parse_args()

    source_root = normalize(os.path.dirname(__file__))
    target_root = normalize(args.target) if args.target else None

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
        "docs",
        "sprints",
        "handoffs",
        "decisions",
        ".github/workflows",
        "README.md",
        "gsd-installer.py",
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
            else:
                continue

    show_banner()
    return 0


def show_banner():
    M = "\033[1;35m"
    C = "\033[1;36m"
    Y = "\033[1;33m"
    G = "\033[1;32m"
    R = "\033[0m"
    print()
    print(f"{M}  ██╗████████╗███████╗      ███╗   ███╗ █████╗  ██████╗ ██╗ ██████╗{R}")
    print(f"{M}  ██║╚══██╔══╝██╔════╝      ████╗ ████║██╔══██╗██╔════╝ ██║██╔════╝{R}")
    print(f"{M}  ██║   ██║   ███████╗█████╗██╔████╔██║███████║██║  ███╗██║██║     {R}")
    print(f"{C}  ██║   ██║   ╚════██║╚════╝██║╚██╔╝██║██╔══██║██║   ██║██║██║     {R}")
    print(f"{C}  ██║   ██║   ███████║      ██║ ╚═╝ ██║██║  ██║╚██████╔╝██║╚██████╗{R}")
    print(f"{C}  ╚═╝   ╚═╝   ╚══════╝      ╚═╝     ╚═╝╚═╝  ╚═╝ ╚═════╝ ╚═╝ ╚═════╝{R}")
    print()
    print(f"{Y}                         AI dev team{R}")
    print(f"{G}                    Installation complete!{R}")
    print()


if __name__ == "__main__":
    raise SystemExit(main())

