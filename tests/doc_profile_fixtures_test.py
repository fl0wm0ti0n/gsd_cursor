"""
Tiered regression for documentation profile (DEC-0059 / AC-8).

Invoked from tests/run-tests.ps1 and tests/run-tests.sh.
"""

from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import textwrap

ROOT = os.path.normpath(os.path.join(os.path.dirname(__file__), ".."))
VALIDATOR = os.path.join(ROOT, "scripts", "validate_doc_profile.py")
TPL = os.path.join(ROOT, "template")


def _run_validator(repo: str, no_tpl: bool) -> int:
    cmd = [sys.executable, VALIDATOR, "--repo", repo]
    if no_tpl:
        cmd.append("--no-template-parity")
    return subprocess.call(cmd, cwd=ROOT)


def _write(path: str, text: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)


def _minimal_user_readme(keys: str) -> str:
    """keys: concise|balanced|technical-deep"""
    parts = ["# Fixture\n"]
    parts.append("## Purpose\n\np\n\n## Quickstart\n\nq\n\n## Limitations\n\nl\n\n")
    if keys in ("balanced", "technical-deep"):
        parts.append("## Examples\n\ne\n\n## Related documentation\n\nr\n\n")
    if keys == "technical-deep":
        parts.append("## Troubleshooting\n\nt\n\n")
    return "".join(parts)


def _minimal_dev_readme(detail: str) -> str:
    parts = ["# Dev\n"]
    parts.append("## Prerequisites\n\np\n\n## Workflow\n\nw\n\n")
    if detail in ("balanced", "technical-deep"):
        parts.append("## Quality gates\n\nq\n\n## Architecture notes\n\na\n\n")
    if detail == "technical-deep":
        parts.append("## Contracts and interfaces\n\nc\n\n## Engineering decisions\n\nd\n\n")
    return "".join(parts)


def _seed_scratchpad(tmp: str, extra_local: str) -> None:
    d = os.path.join(tmp, ".cursor")
    os.makedirs(d, exist_ok=True)
    shutil.copy2(os.path.join(TPL, ".cursor", "scratchpad.md"), os.path.join(d, "scratchpad.md"))
    shutil.copy2(
        os.path.join(TPL, ".cursor", "scratchpad.local.example.md"),
        os.path.join(d, "scratchpad.local.example.md"),
    )
    base_local = os.path.join(d, "scratchpad.local.md")
    with open(base_local, "w", encoding="utf-8", newline="\n") as f:
        f.write(extra_local)


def main() -> int:
    if not os.path.isfile(VALIDATOR):
        print("missing validate_doc_profile.py", file=sys.stderr)
        return 1

    r = subprocess.call([sys.executable, VALIDATOR, "--self-test"], cwd=ROOT)
    if r != 0:
        return r

    # Negative: invalid audience
    with tempfile.TemporaryDirectory() as tmp:
        _seed_scratchpad(tmp, "DOC_AUDIENCE_PROFILE=not-a-profile\n")
        _write(os.path.join(tmp, "README.md"), _minimal_user_readme("concise"))
        if _run_validator(tmp, no_tpl=True) == 0:
            print("expected failure on invalid profile", file=sys.stderr)
            return 1

    # Tier A anchor: user x concise (no template parity, no developer shard)
    with tempfile.TemporaryDirectory() as tmp:
        _seed_scratchpad(tmp, "DOC_AUDIENCE_PROFILE=user\nDOC_DETAIL_LEVEL=concise\n")
        _write(os.path.join(tmp, "README.md"), _minimal_user_readme("concise"))
        if _run_validator(tmp, no_tpl=True) != 0:
            print("tier A user concise failed", file=sys.stderr)
            return 1

    # Tier A: developer x balanced
    with tempfile.TemporaryDirectory() as tmp:
        _seed_scratchpad(tmp, "DOC_AUDIENCE_PROFILE=developer\nDOC_DETAIL_LEVEL=balanced\n")
        _write(os.path.join(tmp, "README.md"), "## Contributing\n\n[c](docs/developer/README.md)\n")
        _write(os.path.join(tmp, "docs", "developer", "README.md"), _minimal_dev_readme("balanced"))
        if _run_validator(tmp, no_tpl=True) != 0:
            print("tier A developer balanced failed", file=sys.stderr)
            return 1

    # Tier A: both x technical-deep (split)
    with tempfile.TemporaryDirectory() as tmp:
        _seed_scratchpad(tmp, "DOC_AUDIENCE_PROFILE=both\nDOC_DETAIL_LEVEL=technical-deep\n")
        _write(os.path.join(tmp, "README.md"), _minimal_user_readme("technical-deep") + "## Contributing\n\nx\n")
        _write(os.path.join(tmp, "docs", "developer", "README.md"), _minimal_dev_readme("technical-deep"))
        if _run_validator(tmp, no_tpl=True) != 0:
            print("tier A both technical-deep failed", file=sys.stderr)
            return 1

    # Tier B table: remaining cells via direct lib import
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import doc_profile_lib as dpl

    assert dpl.required_user_keys("both", "concise") | dpl.required_dev_keys("both", "concise")
    assert len(dpl.required_user_keys("user", "technical-deep")) == 6

    # Tier C wiring: default merge (empty keys -> both/balanced) on synthetic tree
    with tempfile.TemporaryDirectory() as tmp:
        _seed_scratchpad(tmp, "DOC_AUDIENCE_PROFILE=\nDOC_DETAIL_LEVEL=\n")
        _write(
            os.path.join(tmp, "README.md"),
            _minimal_user_readme("balanced") + "## Contributing\n\nx\n",
        )
        _write(os.path.join(tmp, "docs", "developer", "README.md"), _minimal_dev_readme("balanced"))
        if _run_validator(tmp, no_tpl=True) != 0:
            print("tier C default merge failed", file=sys.stderr)
            return 1

    # SPEC_PACK_MODE=0 must not require extra artifacts (minimal readme without spec words)
    with tempfile.TemporaryDirectory() as tmp:
        _seed_scratchpad(
            tmp,
            textwrap.dedent(
                """\
                DOC_AUDIENCE_PROFILE=user
                DOC_DETAIL_LEVEL=concise
                SPEC_PACK_MODE=0
                USER_GUIDE_MODE=0
                """
            ),
        )
        _write(os.path.join(tmp, "README.md"), _minimal_user_readme("concise"))
        if _run_validator(tmp, no_tpl=True) != 0:
            print("optional modes off failed", file=sys.stderr)
            return 1

    # Installer bundles doc_profile_lib next to installer.py (npm global layout)
    pkg_path = os.path.join(ROOT, "package.json")
    if os.path.isfile(pkg_path):
        with open(pkg_path, "r", encoding="utf-8") as f:
            pkg = json.load(f)
        if "scripts/doc_profile_lib.py" not in pkg.get("files", []):
            print("package.json files[] must include scripts/doc_profile_lib.py", file=sys.stderr)
            return 1

    sys.path.insert(0, ROOT)
    import installer as installer_mod

    mod = installer_mod._load_doc_profile_lib()
    if not hasattr(mod, "ensure_doc_surfaces_merged"):
        print("installer _load_doc_profile_lib missing ensure_doc_surfaces_merged", file=sys.stderr)
        return 1

    with tempfile.TemporaryDirectory() as tmp:
        shutil.copy2(os.path.join(ROOT, "installer.py"), os.path.join(tmp, "installer.py"))
        os.makedirs(os.path.join(tmp, "scripts"), exist_ok=True)
        fake_inst = os.path.join(tmp, "installer.py")
        iso_spec = importlib.util.spec_from_file_location("installer_fake_pkg", fake_inst)
        if iso_spec is None or iso_spec.loader is None:
            print("could not load isolated installer spec", file=sys.stderr)
            return 1
        iso = importlib.util.module_from_spec(iso_spec)
        iso_spec.loader.exec_module(iso)
        try:
            iso._load_doc_profile_lib()
        except RuntimeError as e:
            if "DOC_PROFILE_LIB_MISSING" not in str(e):
                print(f"expected DOC_PROFILE_LIB_MISSING, got {e!r}", file=sys.stderr)
                return 1
        else:
            print("expected RuntimeError when doc_profile_lib.py absent", file=sys.stderr)
            return 1

    print("[DOC_PROFILE_FIXTURES_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
