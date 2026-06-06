#!/usr/bin/env python3
"""One-time backfill helper for US-0091 (execute phase only)."""

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

SLASH_CMD = re.compile(r"(/[a-z][a-z0-9-]*)")
SCRATCHPAD_KEY = re.compile(r"`?([A-Z][A-Z0-9_]+)`?")
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
    m = SLASH_CMD.search(text)
    if m:
        return m.group(1)
    for m in SCRATCHPAD_KEY.finditer(text):
        key = m.group(1)
        if len(key) > 3 and key not in ("DONE", "OPEN", "TITLE"):
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
        f"- **{item.item_id}** — {item.title.strip()}; traceability: `{tok}`, "
        f"see `docs/engineering/architecture.md`."
    )


def _strip_old_catalog(markdown: str) -> str:
    lines = markdown.splitlines()
    out: list[str] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == CATALOG_MARKER:
            i += 1
            while i < len(lines):
                if lines[i].startswith("## ") and not lines[i].startswith("### "):
                    break
                i += 1
            continue
        out.append(lines[i])
        i += 1
    return "\n".join(out).rstrip() + "\n"


def _inject_catalog(markdown: str, h2_wanted: str, rows: list[str]) -> str:
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


def _set_user_visible(backlog: str, item_id: str, value: bool) -> str:
    if re.search(rf"^## {re.escape(item_id)}\s", backlog, re.MULTILINE):
        hdr = rf"(^## {re.escape(item_id)}[^\n]*\n)"
    else:
        hdr = rf"(^### {re.escape(item_id)}[^\n]*\n)"
    m = re.search(hdr, backlog, re.MULTILINE)
    if not m:
        return backlog
    start = m.end()
    chunk = backlog[start:]
    nxt = re.search(r"\n(?:## |### BUG-)", chunk)
    end = start + (nxt.start() if nxt else len(chunk))
    block = backlog[m.start() : end]
    if re.search(r"^-\s*user_visible:", block, re.MULTILINE):
        return backlog
    line = f"- user_visible: {'true' if value else 'false'}\n"
    return backlog[: m.end()] + line + backlog[m.end() :]


def main() -> int:
    repo = _REPO_ROOT
    backlog_path = os.path.join(repo, "docs", "product", "backlog.md")
    merged, _ = installer.merge_scratchpad_layers(repo)
    manifest = rfc.load_affinity_manifest(repo)
    items = {i.item_id: i for i in rfc.parse_backlog(rfc.read_utf8(backlog_path))}
    root_path = os.path.join(repo, "README.md")
    dev_path = os.path.join(repo, "docs", "developer", "README.md")
    root = _strip_old_catalog(rfc.read_utf8(root_path))
    dev = _strip_old_catalog(rfc.read_utf8(dev_path))
    backlog = rfc.read_utf8(backlog_path)

    root_add: dict[str, list[str]] = {}
    dev_add: dict[str, list[str]] = {}
    for item in sorted(items.values(), key=lambda x: x.item_id):
        pred = rfc.classify_item(item, False)
        if pred.input_invalid:
            backlog = _set_user_visible(backlog, item.item_id, False)
            continue
        if not pred.in_scope:
            if item.status == "DONE":
                backlog = _set_user_visible(backlog, item.item_id, False)
            continue
        backlog = _set_user_visible(backlog, item.item_id, True)
        aff = rfc.resolve_affinity(item, manifest)
        root_add.setdefault(aff.root_h2, []).append(_root_blurb(item))
        dev_add.setdefault(aff.dev_h2, []).append(_dev_row(item))

    for h2, lines in root_add.items():
        root = _inject_catalog(root, h2, lines)

    for h2 in DEV_H2_ORDER:
        if h2 in dev_add:
            dev = _inject_catalog(dev, h2, dev_add[h2])

    with open(root_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(root)
    with open(dev_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(dev)
    with open(backlog_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(backlog)
    tpl = os.path.join(repo, "template", "README.md")
    with open(tpl, "w", encoding="utf-8", newline="\n") as f:
        f.write(root)
    print(f"backfill: root_sections={len(root_add)} dev_sections={len(dev_add)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
