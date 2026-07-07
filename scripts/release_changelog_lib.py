"""
Release changelog derivation, coalesce, promote, fingerprint idempotency (US-0100 / DEC-0085).

Derivation precedence (L4):
  1. Sprint note ``## What's new`` bullets + inline US-xxxx / BUG-xxxx refs
  2. Backlog ``## US-xxxx`` / ``### BUG-xxxx`` title + summary (one-liner)
  3. Queue row ``story_refs`` (fallback when sprint note sparse)

Category map: US→Added, BUG→Fixed, user_visible:false→Changed.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, List, Optional, Sequence, Tuple

# AUTONOMY_PRESET consumer wiring (US-0119 / DEC-0119):
# RELEASE_AUTO_CONFIRM_ACCEPTANCE and RELEASE_PUBLISH_AUTO_CONFIRM are autonomy
# flags controlled by AUTONOMY_PRESET. When AUTONOMY_PRESET != none,
# expand_autonomy_preset merges per-feature defaults. Default AUTONOMY_PRESET=none
# produces empty dict (byte-identical pre-US-0119 behaviour).
AUTONOMY_PRESET_DEFAULT = "none"
RELEASE_AUTO_CONFIRM_ACCEPTANCE = "RELEASE_AUTO_CONFIRM_ACCEPTANCE"
RELEASE_PUBLISH_AUTO_CONFIRM = "RELEASE_PUBLISH_AUTO_CONFIRM"

# Derivation precedence (documented L4 order — do not reorder without DEC revision)
DERIVATION_PRECEDENCE: Tuple[str, ...] = (
    "sprint_notes_whats_new",
    "backlog_title_summary",
    "queue_story_refs",
)

US_ID = re.compile(r"\bUS-\d{4}\b")
BUG_ID = re.compile(r"\bBUG-\d{4}\b")
SEMVER_SECTION = re.compile(r"^##\s+\[(.+?)\]\s*(?:-\s*(\d{4}-\d{2}-\d{2}))?\s*$", re.MULTILINE)
USER_VISIBLE = re.compile(r"^-\s*user_visible:\s*(true|false)\s*$", re.IGNORECASE | re.MULTILINE)
SEMVER_VALID = re.compile(
    r"^[0-9]+\.[0-9]+\.[0-9]+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$"
)

# Fail-closed reason codes (RELEASE_CHANGELOG_* family)
RELEASE_CHANGELOG_VERSION_MISSING = "RELEASE_CHANGELOG_VERSION_MISSING"
RELEASE_CHANGELOG_DUPLICATE_VERSION = "RELEASE_CHANGELOG_DUPLICATE_VERSION"
RELEASE_CHANGELOG_WORK_ITEM_GAP = "RELEASE_CHANGELOG_WORK_ITEM_GAP"
RELEASE_CHANGELOG_ORDER_INVALID = "RELEASE_CHANGELOG_ORDER_INVALID"
RELEASE_CHANGELOG_UNRELEASED_MISSING = "RELEASE_CHANGELOG_UNRELEASED_MISSING"
RELEASE_CHANGELOG_QUEUE_DRIFT = "RELEASE_CHANGELOG_QUEUE_DRIFT"
RELEASE_CHANGELOG_VERSION_DOC_MISSING = "RELEASE_CHANGELOG_VERSION_DOC_MISSING"
RELEASE_CHANGELOG_SPRINT_ORPHAN = "RELEASE_CHANGELOG_SPRINT_ORPHAN"
RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS = "RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS"
RELEASE_CHANGELOG_IDEMPOTENCY_VIOLATION = "RELEASE_CHANGELOG_IDEMPOTENCY_VIOLATION"
RELEASE_CHANGELOG_IDEMPOTENCY_OK = "RELEASE_CHANGELOG_IDEMPOTENCY_OK"

FAIL_CODES = (
    RELEASE_CHANGELOG_VERSION_MISSING,
    RELEASE_CHANGELOG_DUPLICATE_VERSION,
    RELEASE_CHANGELOG_WORK_ITEM_GAP,
    RELEASE_CHANGELOG_ORDER_INVALID,
    RELEASE_CHANGELOG_UNRELEASED_MISSING,
    RELEASE_CHANGELOG_QUEUE_DRIFT,
    RELEASE_CHANGELOG_VERSION_DOC_MISSING,
    RELEASE_CHANGELOG_SPRINT_ORPHAN,
    RELEASE_CHANGELOG_BACKFILL_AMBIGUOUS,
    RELEASE_CHANGELOG_IDEMPOTENCY_VIOLATION,
)


class ReleaseChangelogError(Exception):
    def __init__(self, code: str, message: str = "") -> None:
        self.code = code
        super().__init__(message or code)


@dataclass
class WorkItem:
    item_id: str
    title: str
    summary: str
    category: str  # Added | Fixed | Changed
    source: str = ""


@dataclass
class QueueRow:
    sprint_id: str
    story_refs: str
    status: str
    last_updated: str
    release_notes_ref: str
    release_version: str
    raw_line: str


def read_utf8(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def write_utf8(path: str, content: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)


def normalize_semver(raw: str) -> str:
    """Strip leading v; semver-parse; raise VERSION_MISSING on empty/invalid."""
    if raw is None:
        raise ReleaseChangelogError(RELEASE_CHANGELOG_VERSION_MISSING, "version is None")
    s = raw.strip()
    if s.lower().startswith("v"):
        s = s[1:]
    if not s:
        raise ReleaseChangelogError(RELEASE_CHANGELOG_VERSION_MISSING, "empty version")
    if not SEMVER_VALID.match(s):
        raise ReleaseChangelogError(
            RELEASE_CHANGELOG_VERSION_MISSING, f"invalid semver: {raw!r}"
        )
    return s


def version_fingerprint(semver: str, work_item_ids: Sequence[str]) -> str:
    """Idempotency key: semver + sorted work_item_ids."""
    norm = normalize_semver(semver)
    ids = sorted(set(work_item_ids))
    return f"{norm}|{','.join(ids)}"


def _one_liner(text: str, max_len: int = 160) -> str:
    line = " ".join(text.split())
    if len(line) > max_len:
        return line[: max_len - 3] + "..."
    return line


def parse_queue_rows(repo_root: str) -> List[QueueRow]:
    path = os.path.join(repo_root, "handoffs", "release_queue.md")
    if not os.path.isfile(path):
        return []
    rows: List[QueueRow] = []
    for line in read_utf8(path).splitlines():
        if not line.startswith("| S"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 9:
            continue
        rows.append(
            QueueRow(
                sprint_id=parts[1],
                story_refs=parts[2],
                status=parts[3],
                last_updated=parts[4],
                release_notes_ref=parts[5],
                release_version=parts[7] if len(parts) > 7 else "",
                raw_line=line,
            )
        )
    return rows


def _queue_row_map(repo_root: str) -> Dict[str, QueueRow]:
    return {r.sprint_id: r for r in parse_queue_rows(repo_root)}


def _parse_backlog_items(repo_root: str) -> Dict[str, WorkItem]:
    backlog_path = os.path.join(repo_root, "docs", "product", "backlog.md")
    if not os.path.isfile(backlog_path):
        return {}
    text = read_utf8(backlog_path)
    items: Dict[str, WorkItem] = {}
    for m in re.finditer(r"^##\s+(US-\d{4})\s*[—\-]\s*(.+)$", text, re.MULTILINE):
        item_id, title = m.group(1), m.group(2).strip()
        block = text[m.end() : text.find("\n## ", m.end())]
        uv = USER_VISIBLE.search(block)
        user_vis = uv.group(1).lower() == "true" if uv else True
        sm = re.search(r"^-\s*Summary:\s*(.+)$", block, re.MULTILINE)
        summary = _one_liner(sm.group(1)) if sm else title
        if not user_vis:
            cat = "Changed"
        else:
            cat = "Added"
        items[item_id] = WorkItem(item_id, title, summary, cat, "backlog_title_summary")
    for m in re.finditer(r"^###\s+(BUG-\d{4})\s*[—\-]\s*(.+)$", text, re.MULTILINE):
        item_id, title = m.group(1), m.group(2).strip()
        block = text[m.end() : text.find("\n### ", m.end())]
        block = block.split("\n## ")[0]
        sm = re.search(r"^-\s*Summary:\s*(.+)$", block, re.MULTILINE)
        summary = _one_liner(sm.group(1)) if sm else title
        items[item_id] = WorkItem(item_id, title, summary, "Fixed", "backlog_title_summary")
    return items


def _extract_whats_new(repo_root: str, sprint_id: str) -> List[str]:
    notes_path = os.path.join(
        repo_root, "handoffs", "releases", f"{sprint_id}-release-notes.md"
    )
    if not os.path.isfile(notes_path):
        return []
    text = read_utf8(notes_path)
    m = re.search(r"^##\s+What's new\s*$", text, re.MULTILINE | re.IGNORECASE)
    if not m:
        return []
    rest = text[m.end() :]
    end = re.search(r"^##\s+", rest, re.MULTILINE)
    section = rest[: end.start()] if end else rest
    bullets: List[str] = []
    for line in section.splitlines():
        s = line.strip()
        if s.startswith("- "):
            bullets.append(s[2:].strip())
    return bullets


def _category_for_id(item_id: str, backlog: Dict[str, WorkItem]) -> str:
    if item_id in backlog:
        return backlog[item_id].category
    if item_id.startswith("BUG-"):
        return "Fixed"
    return "Added"


def derive_work_items(sprint_ids: Sequence[str], repo_root: str) -> List[WorkItem]:
    """L4 precedence: sprint notes → backlog → queue story_refs."""
    backlog = _parse_backlog_items(repo_root)
    qmap = _queue_row_map(repo_root)
    seen: Dict[str, WorkItem] = {}

    for sprint_id in sprint_ids:
        # 1. Sprint notes What's new
        for bullet in _extract_whats_new(repo_root, sprint_id):
            for pat in (US_ID, BUG_ID):
                for item_id in pat.findall(bullet):
                    if item_id in seen:
                        continue
                    title = backlog[item_id].title if item_id in backlog else item_id
                    summary = _one_liner(bullet) if bullet else title
                    seen[item_id] = WorkItem(
                        item_id,
                        title,
                        summary,
                        _category_for_id(item_id, backlog),
                        "sprint_notes_whats_new",
                    )

        # 2. Backlog for refs mentioned in sprint notes full text
        notes_path = os.path.join(
            repo_root, "handoffs", "releases", f"{sprint_id}-release-notes.md"
        )
        if os.path.isfile(notes_path):
            note_text = read_utf8(notes_path)
            for item_id in US_ID.findall(note_text) + BUG_ID.findall(note_text):
                if item_id in seen:
                    continue
                if item_id in backlog:
                    wi = backlog[item_id]
                    seen[item_id] = WorkItem(
                        wi.item_id, wi.title, wi.summary, wi.category, wi.source
                    )

        # 3. Queue story_refs fallback
        row = qmap.get(sprint_id)
        if row:
            for token in re.split(r"[,;\s]+", row.story_refs):
                token = token.strip()
                if not token or token in seen:
                    continue
                if token in backlog:
                    wi = backlog[token]
                    seen[token] = WorkItem(
                        wi.item_id, wi.title, wi.summary, wi.category, "queue_story_refs"
                    )
                elif US_ID.fullmatch(token) or BUG_ID.fullmatch(token):
                    seen[token] = WorkItem(
                        token,
                        token,
                        token,
                        _category_for_id(token, backlog),
                        "queue_story_refs",
                    )

    def sort_key(w: WorkItem) -> Tuple[int, int]:
        if w.item_id.startswith("US-"):
            return (0, int(w.item_id.split("-")[1]))
        return (1, int(w.item_id.split("-")[1]))

    return sorted(seen.values(), key=sort_key)


def coalesce_sprints_by_semver(
    rows: Optional[Sequence[QueueRow]], repo_root: str
) -> Dict[str, List[str]]:
    """Group released queue rows by normalized semver (non-empty release_version)."""
    if rows is None:
        rows = parse_queue_rows(repo_root)
    groups: Dict[str, List[str]] = {}
    for row in rows:
        if row.status != "released":
            continue
        if not row.release_version.strip():
            continue
        try:
            key = normalize_semver(row.release_version)
        except ReleaseChangelogError:
            continue
        groups.setdefault(key, []).append(row.sprint_id)
    for key in groups:
        groups[key] = sorted(set(groups[key]))
    return groups


def version_doc_path(repo_root: str, semver: str) -> str:
    norm = normalize_semver(semver)
    return os.path.join(repo_root, "handoffs", "releases", f"{norm}-release-notes.md")


def _format_version_doc(
    semver: str,
    work_items: Sequence[WorkItem],
    sprint_ids: Sequence[str],
    fingerprint: str,
) -> str:
    lines = [
        f"# Release notes — {normalize_semver(semver)}",
        "",
        f"<!-- release_changelog_fingerprint: {fingerprint} -->",
        "",
        "> Per-version GitHub `-F` SOT (**US-0100**). Sprint-scoped evidence remains in "
        "`handoffs/releases/Sxxxx-release-notes.md` — do not overwrite unrelated version files.",
        "",
        "## Work items",
        "",
    ]
    for wi in work_items:
        lines.append(f"- **{wi.item_id}** — {wi.summary}")
    lines.extend(["", "## Sprint evidence", ""])
    for sid in sorted(set(sprint_ids)):
        lines.append(f"- [`{sid}`](handoffs/releases/{sid}-release-notes.md)")
    lines.append("")
    return "\n".join(lines)


def build_version_doc(semver: str, sprint_ids: Sequence[str], repo_root: str) -> str:
    """Write per-version doc; return path. Idempotent on matching fingerprint."""
    norm = normalize_semver(semver)
    work_items = derive_work_items(sprint_ids, repo_root)
    fp = version_fingerprint(norm, [w.item_id for w in work_items])
    path = version_doc_path(repo_root, norm)

    if os.path.isfile(path):
        existing = read_utf8(path)
        m = re.search(r"<!-- release_changelog_fingerprint:\s*(.+?)\s*-->", existing)
        if m and m.group(1).strip() == fp:
            print(RELEASE_CHANGELOG_IDEMPOTENCY_OK, file=__import__("sys").stderr)
            return path
        if m and m.group(1).strip() != fp:
            raise ReleaseChangelogError(
                RELEASE_CHANGELOG_DUPLICATE_VERSION,
                f"fingerprint mismatch for {norm}",
            )

    content = _format_version_doc(norm, work_items, sprint_ids, fp)
    write_utf8(path, content)
    return path


def changelog_path(repo_root: str) -> str:
    return os.path.join(repo_root, "CHANGELOG.md")


def ensure_changelog_stub(repo_root: str) -> None:
    path = changelog_path(repo_root)
    if os.path.isfile(path):
        return
    stub = (
        "# Changelog\n\n"
        "All notable changes to this project will be documented in this file.\n\n"
        "The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),\n"
        "and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).\n\n"
        "<!-- semver-sections-newest-first -->\n\n"
        "## [Unreleased]\n\n"
    )
    write_utf8(path, stub)


def extract_changelog_section(semver: str, repo_root: str) -> Optional[str]:
    """Read cumulative section text for semver (body only, no heading)."""
    path = changelog_path(repo_root)
    if not os.path.isfile(path):
        return None
    norm = normalize_semver(semver)
    text = read_utf8(path)
    pattern = re.compile(
        rf"^##\s+\[{re.escape(norm)}\]\s*(?:-\s*\d{{4}}-\d{{2}}-\d{{2}})?\s*$",
        re.MULTILINE,
    )
    m = pattern.search(text)
    if not m:
        return None
    rest = text[m.end() :]
    nxt = re.search(r"^##\s+\[", rest, re.MULTILINE)
    body = rest[: nxt.start()] if nxt else rest
    return body.strip()


def _split_changelog_sections(text: str) -> Tuple[str, str, List[Tuple[str, str, str]]]:
    """Return (header, unreleased_body, [(semver, date, body), ...])."""
    m = re.search(r"^##\s+\[Unreleased\]\s*$", text, re.MULTILINE)
    if not m:
        raise ReleaseChangelogError(RELEASE_CHANGELOG_UNRELEASED_MISSING)
    header = text[: m.start()]
    rest = text[m.end() :]
    sections: List[Tuple[str, str, str]] = []
    pos = 0
    for sm in SEMVER_SECTION.finditer(rest):
        if sm.start() > pos:
            # content before first semver section is unreleased body
            pass
        semver_raw = sm.group(1)
        if semver_raw.lower() == "unreleased":
            continue
        date = sm.group(2) or ""
        start = sm.end()
        nxt = SEMVER_SECTION.search(rest, start)
        body = rest[start : nxt.start() if nxt else len(rest)]
        sections.append((semver_raw, date, body.strip()))
    unreleased_end = SEMVER_SECTION.search(rest)
    unreleased_body = rest[: unreleased_end.start()].strip() if unreleased_end else rest.strip()
    return header, unreleased_body, sections


def _format_work_items_changelog(work_items: Sequence[WorkItem]) -> str:
    by_cat: Dict[str, List[WorkItem]] = {"Added": [], "Fixed": [], "Changed": []}
    for wi in work_items:
        by_cat.setdefault(wi.category, []).append(wi)
    parts: List[str] = []
    for cat in ("Added", "Fixed", "Changed"):
        items = by_cat.get(cat) or []
        if not items:
            continue
        parts.append(f"### {cat}")
        parts.append("")
        for wi in items:
            parts.append(f"- **{wi.item_id}** — {wi.summary}")
        parts.append("")
    return "\n".join(parts).strip()


def append_unreleased(work_items: Sequence[WorkItem], repo_root: str) -> None:
    """Append categorized bullets under top [Unreleased] only."""
    ensure_changelog_stub(repo_root)
    path = changelog_path(repo_root)
    text = read_utf8(path)
    header, unreleased_body, sections = _split_changelog_sections(text)
    new_block = _format_work_items_changelog(work_items)
    if new_block:
        if unreleased_body:
            unreleased_body = unreleased_body + "\n\n" + new_block
        else:
            unreleased_body = new_block
    out = header + "## [Unreleased]\n\n"
    if unreleased_body:
        out += unreleased_body + "\n\n"
    for semver, date, body in sections:
        out += f"## [{semver}]"
        if date:
            out += f" - {date}"
        out += "\n\n" + body + "\n\n"
    write_utf8(path, out.rstrip() + "\n")


def promote_unreleased(
    semver: str,
    sprint_ids: Sequence[str],
    repo_root: str,
    release_date: Optional[str] = None,
) -> None:
    """Move [Unreleased] items into ## [semver] - date; recreate empty [Unreleased]."""
    ensure_changelog_stub(repo_root)
    path = changelog_path(repo_root)
    text = read_utf8(path)
    header, unreleased_body, sections = _split_changelog_sections(text)
    norm = normalize_semver(semver)
    work_items = derive_work_items(sprint_ids, repo_root)
    promoted = _format_work_items_changelog(work_items)
    if unreleased_body:
        promoted = (unreleased_body + "\n\n" + promoted).strip() if promoted else unreleased_body
    date = release_date or datetime.now(timezone.utc).strftime("%Y-%m-%d")
    # Remove existing section for same semver
    sections = [(s, d, b) for s, d, b in sections if normalize_semver(s) != norm]
    sections.insert(0, (norm, date, promoted))
    out = header + "## [Unreleased]\n\n\n"
    for s, d, b in sections:
        out += f"## [{s}]"
        if d:
            out += f" - {d}"
        out += "\n\n" + b + "\n\n"
    write_utf8(path, out.rstrip() + "\n")


def bind_queue_release_version(
    sprint_ids: Sequence[str], semver: str, repo_root: str
) -> None:
    """Mutate only specified sprint rows in handoffs/release_queue.md."""
    path = os.path.join(repo_root, "handoffs", "release_queue.md")
    if not os.path.isfile(path):
        raise ReleaseChangelogError(
            RELEASE_CHANGELOG_QUEUE_DRIFT, "release_queue.md missing"
        )
    norm = normalize_semver(semver)
    targets = set(sprint_ids)
    lines = read_utf8(path).splitlines()
    out: List[str] = []
    for line in lines:
        if not line.startswith("| S"):
            out.append(line)
            continue
        cols = [p.strip() for p in line.split("|")[1:-1]]
        if len(cols) < 7:
            out.append(line)
            continue
        if cols[0] in targets:
            cols[6] = norm
            out.append("| " + " | ".join(cols) + " |")
        else:
            out.append(line)
    write_utf8(path, "\n".join(out) + "\n")


def ensure_version_doc_for_release(semver: str, repo_root: str) -> str:
    """Coalesce released rows for semver (or all unbound since tag) and build doc."""
    norm = normalize_semver(semver)
    rows = parse_queue_rows(repo_root)
    sprint_ids: List[str] = []
    for row in rows:
        if row.status != "released":
            continue
        rv = row.release_version.strip()
        if rv and normalize_semver(rv) == norm:
            sprint_ids.append(row.sprint_id)
        elif not rv:
            sprint_ids.append(row.sprint_id)
    if not sprint_ids:
        sprint_ids = [r.sprint_id for r in rows if r.status == "released"][-1:]
    return build_version_doc(norm, sprint_ids, repo_root)


def runtime_proof_hash(payload: Dict[str, object]) -> str:
    canonical = json.dumps(payload, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
