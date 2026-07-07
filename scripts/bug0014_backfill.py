#!/usr/bin/env python3
"""BUG-0014 backfill: add feature coverage catalog rows to its_magic/README.md and docs/developer/README.md."""

from __future__ import annotations

import os
import re
import sys

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_REPO_ROOT = os.path.normpath(os.path.join(_SCRIPT_DIR, ".."))
sys.path.insert(0, _REPO_ROOT)
sys.path.insert(0, _SCRIPT_DIR)

import installer  # noqa: E402
import readme_feature_coverage_lib as rfc  # noqa: E402

CATALOG_MARKER = "<!-- readme-feature-coverage-catalog -->"

DEV_H2_ORDER = (
    "Prerequisites",
    "Workflow",
    "Quality gates",
    "Architecture notes",
    "Contracts and interfaces",
    "Engineering decisions",
)


def _operator_token(item: rfc.WorkItem) -> str:
    text = f"{item.title}\n{item.summary}\n{item.body_text}"
    m = re.search(r"(/[a-z][a-z0-9-]*)", text)
    if m:
        return m.group(1)
    for m in re.finditer(r"`?([A-Z][A-Z0-9_]+)`?", text):
        key = m.group(1)
        if len(key) > 3 and key not in ("DONE", "OPEN", "TITLE", "DEFAULT"):
            return key
    return item.item_id


def _root_blurb(item: rfc.WorkItem) -> str:
    tok = _operator_token(item)
    title = item.title.strip() or item.summary.strip()[:80]
    if tok.startswith("/"):
        return f"- `{tok}` — {title} (`{item.item_id}`)."
    if tok.isupper():
        return f"- `{tok}` scratchpad flag — {title} (`{item.item_id}`)."
    return f"- `{tok}` — {title} (`{item.item_id}`)."


def _dev_row(item: rfc.WorkItem) -> str:
    tok = _operator_token(item)
    return (
        f"- **{item.item_id}** — {item.title.strip()}; "
        f"traceability: `{tok}`, "
        f"see `docs/engineering/architecture.md`."
    )


def _strip_catalog_from_section(markdown: str, h2_wanted: str) -> str:
    """Remove existing catalog block from the specified H2 section."""
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0
    in_target_section = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            if in_target_section:
                in_target_section = False
            if rfc._h2_match(title, h2_wanted):
                in_target_section = True
                out.append(line)
                i += 1
                # skip any existing catalog block in this section
                while i < len(lines):
                    if lines[i].startswith("## ") and not lines[i].startswith("### "):
                        break
                    if lines[i].strip() == CATALOG_MARKER:
                        i += 1
                        while i < len(lines):
                            if lines[i].startswith("## ") and not lines[i].startswith("### "):
                                break
                            i += 1
                        continue
                    elif lines[i].startswith("### Feature coverage catalog"):
                        i += 1
                        while i < len(lines):
                            if lines[i].startswith("## ") and not lines[i].startswith("### "):
                                break
                            if lines[i].strip() == "" and i + 1 < len(lines) and (lines[i+1].startswith("## ") or lines[i+1].startswith("### ")):
                                break
                            if lines[i].startswith("### "):
                                break
                            i += 1
                        continue
                    else:
                        out.append(lines[i])
                        i += 1
                continue
        out.append(line)
        i += 1
    return "\n".join(out).rstrip() + "\n"


def _inject_catalog_into_h2(markdown: str, h2_wanted: str, rows: list[str]) -> str:
    """Inject catalog rows at the end of the specified H2 section."""
    if not rows:
        return markdown
    block = (
        [CATALOG_MARKER, "", "### Feature coverage catalog (US-0091)", ""]
        + sorted(set(rows))
        + [""]
    )
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)
        if line.startswith("## ") and not line.startswith("### "):
            title = line[3:].strip()
            if rfc._h2_match(title, h2_wanted):
                i += 1
                while i < len(lines) and not (
                    lines[i].startswith("## ") and not lines[i].startswith("### ")
                ):
                    out.append(lines[i])
                    i += 1
                out.extend(block)
                continue
        i += 1
    return "\n".join(out).rstrip() + "\n"


def main() -> int:
    repo = os.path.abspath(args_repo())
    backlog_path = os.path.join(repo, "docs", "product", "backlog.md")
    root_path = os.path.join(repo, "its_magic", "README.md")
    dev_path = os.path.join(repo, "docs", "developer", "README.md")

    merged, _ = installer.merge_scratchpad_layers(repo)
    manifest = rfc.load_affinity_manifest(repo)
    items = {i.item_id: i for i in rfc.parse_backlog(rfc.read_utf8(backlog_path))}

    root = rfc.read_utf8(root_path)
    dev = rfc.read_utf8(dev_path)

    root_add: dict[str, list[str]] = {}
    dev_add: dict[str, list[str]] = {}

    # Determine which items already have coverage
    root_sections = rfc.split_h2_sections(root)
    dev_sections = rfc.split_h2_sections(dev)

    for item in sorted(items.values(), key=lambda x: x.item_id):
        pred = rfc.classify_item(item, True)
        if not pred.in_scope:
            continue

        aff = rfc.resolve_affinity(item, manifest)
        root_sec = _get_section_body(root, aff.root_h2)
        dev_sec = _get_section_body(dev, aff.dev_h2)

        if not rfc.has_root_coverage(root_sec, item):
            root_add.setdefault(aff.root_h2, []).append(_root_blurb(item))

        if not rfc.has_dev_coverage(dev_sec, item):
            dev_add.setdefault(aff.dev_h2, []).append(_dev_row(item))

    # Remove existing catalogs and rebuild
    for h2 in set(root_add.keys()):
        root = _strip_catalog_from_section(root, h2)
    for h2 in set(dev_add.keys()):
        dev = _strip_catalog_from_section(dev, h2)

    # Now we also need to keep existing catalog rows that aren't being refreshed
    # Actually, let's just add to existing content without stripping
    # Re-read to avoid strip issues
    root = rfc.read_utf8(root_path)
    dev = rfc.read_utf8(dev_path)

    for h2, rows in root_add.items():
        root = _inject_catalog_into_h2(root, h2, rows)

    for h2 in DEV_H2_ORDER:
        if h2 in dev_add:
            dev = _inject_catalog_into_h2(dev, h2, dev_add[h2])

    with open(root_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(root)
    with open(dev_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dev)

    root_sections_count = len(root_add)
    dev_sections_count = len(dev_add)
    root_rows = sum(len(v) for v in root_add.values())
    dev_rows = sum(len(v) for v in dev_add.values())
    print(f"backfill: root_sections={root_sections_count} root_rows={root_rows} "
          f"dev_sections={dev_sections_count} dev_rows={dev_rows}")
    return 0


def args_repo() -> str:
    return _REPO_ROOT


def _get_section_body(markdown: str, h2_wanted: str) -> str:
    return rfc.section_body(markdown, h2_wanted)


if __name__ == "__main__":
    raise SystemExit(main())
