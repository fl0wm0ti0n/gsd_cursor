"""
Bug issue parsing and validation helpers (US-0079 / DEC-0061).

Canonical backlog region: ## Bug issues (canonical); each issue is ### BUG-#### — Title
"""

from __future__ import annotations

import re
from dataclasses import dataclass

BUG_SECTION_HEADER = "## Bug issues (canonical)"
BUG_BLOCK_HEADER = re.compile(r"^### (BUG-(\d{4}))\s*[—-]\s*(.*)\s*$")
STATUS_LINE = re.compile(r"^-\s*Status:\s*(OPEN|DONE)\s*$", re.IGNORECASE)
# Field keys: line starts with "- key:" (optional ** around key)
FIELD_LINE = re.compile(
    r"^-\s*\*?\*?(environment|steps_to_reproduce|expected|actual|evidence_refs)\*?\*?:\s*(.*)\s*$",
    re.IGNORECASE,
)

REQUIRED_FIELDS = (
    "environment",
    "steps_to_reproduce",
    "expected",
    "actual",
    "evidence_refs",
)

ALLOWED_STATUS = frozenset({"OPEN", "DONE"})


@dataclass
class BugIssue:
    bug_id: str
    title: str
    status: str | None
    fields: dict[str, str]
    body_lines: list[str]


def extract_bug_section(text: str) -> str | None:
    # Anchor at line start only — backlog prose may cite `## Bug issues (canonical)` inline (US-0079 notes).
    m_hdr = re.search(r"^## Bug issues \(canonical\)\s*$", text, re.MULTILINE)
    if not m_hdr:
        return None
    start = m_hdr.end()
    rest = text[start:]
    # Next top-level ## (any) ends the section
    m = re.search(r"\n## [^\n]+\n", rest)
    if m:
        return rest[: m.start()].strip()
    return rest.strip()


def parse_bug_issues(section_body: str) -> list[BugIssue]:
    """Split section into bug blocks by ### BUG-#### headers."""
    lines = section_body.splitlines()
    issues: list[BugIssue] = []
    i = 0
    while i < len(lines):
        m = BUG_BLOCK_HEADER.match(lines[i].strip())
        if not m:
            i += 1
            continue
        full_id, _num, title = m.group(1), m.group(2), m.group(3).strip()
        block_start = i
        i += 1
        while i < len(lines) and not BUG_BLOCK_HEADER.match(lines[i].strip()):
            i += 1
        block_lines = lines[block_start:i]
        issues.append(_parse_single_bug(full_id, title, block_lines))
    return issues


def _parse_single_bug(bug_id: str, title: str, block_lines: list[str]) -> BugIssue:
    status: str | None = None
    fields: dict[str, str] = {k: "" for k in REQUIRED_FIELDS}
    for raw in block_lines[1:]:
        line = raw.rstrip()
        sm = STATUS_LINE.match(line.strip())
        if sm:
            status = sm.group(1).upper()
            continue
        fm = FIELD_LINE.match(line.strip())
        if fm:
            key = fm.group(1).lower()
            val = fm.group(2).strip()
            if key in fields:
                fields[key] = val
    return BugIssue(
        bug_id=bug_id,
        title=title,
        status=status,
        fields=fields,
        body_lines=block_lines,
    )


def next_bug_id(text: str) -> str:
    """Next BUG-#### id: max existing + 1 (DEC-0061 / DEC-0034 style)."""
    section = extract_bug_section(text)
    if not section:
        return "BUG-0001"
    nums: list[int] = []
    for m in re.finditer(r"^### (BUG-(\d{4}))\s*", section, re.MULTILINE):
        nums.append(int(m.group(2)))
    if not nums:
        return "BUG-0001"
    return f"BUG-{max(nums) + 1:04d}"


def field_non_empty(value: str) -> bool:
    if not value or not value.strip():
        return False
    low = value.lower().strip()
    if low in ("(none)", "n/a", "tbd", "todo"):
        return False
    return True


def issues_sorted_by_id(issues: list[BugIssue]) -> bool:
    ids = [i.bug_id for i in issues]
    return ids == sorted(ids, key=lambda x: int(x.split("-")[1]))
