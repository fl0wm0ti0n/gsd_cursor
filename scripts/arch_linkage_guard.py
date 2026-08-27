#!/usr/bin/env python3
"""Architecture hot-surface rollover linkage guard (US-0129 / DEC-0129).

Wraps ``python scripts/enforce-triad-hot-surface.py --rollover`` with a fail-closed
pre-hook (no partial archive write) and a post-hook (active heading re-check).
Optional default-off H1 stub restore is gated by ``ARCH_LINKAGE_AUTO_REPAIR=1``.

Stdlib only. No network. No ``.env``.
"""

from __future__ import annotations

import argparse
import ast
import importlib.util
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

REASON_CODE = "ARCH_LINKAGE_ROLLOVER_BLOCKED"
REMEDIATION = (
    "set ARCH_LINKAGE_AUTO_REPAIR=1 for stub restore, or restore H1s manually, "
    "then rerun --rollover"
)
HEADING_TOKEN_RE = re.compile(r"# (?:US|BUG)-\d{4}")
STORY_ID_RE = re.compile(r"(?:US|BUG)-\d{4}")
LIVE_ARCH_MARKERS = (
    "docs/engineering/architecture.md",
    "docs\\engineering\\architecture.md",
    '"docs" / "engineering" / "architecture.md"',
    "'docs' / 'engineering' / 'architecture.md'",
    '"docs", "engineering", "architecture.md"',
    "'docs', 'engineering', 'architecture.md'",
)
ASSERT_HEADING_RE = re.compile(
    r"""(?:assertIn\(\s*|find\(\s*|startswith\(\s*)['\"](# (?:US|BUG)-\d{4})['\"]"""
    r"""|['\"](# (?:US|BUG)-\d{4})['\"]\s+in\b"""
)


def _load_eths():
    path = Path(__file__).resolve().parent / "enforce-triad-hot-surface.py"
    spec = importlib.util.spec_from_file_location("enforce_triad_hot_surface", path)
    if spec is None or spec.loader is None:
        raise ImportError("unable to load enforce-triad-hot-surface.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


_ETHS = _load_eths()
split_arch_stories = _ETHS.split_arch_stories
line_count = _ETHS.line_count
load_merged_policy = _ETHS.load_merged_policy
_int_policy = _ETHS._int_policy
STORY_HEADING_H1 = _ETHS.STORY_HEADING_H1
ARCH_REL = _ETHS.ARCH_REL
ARCH_ARCH_DIR = _ETHS.ARCH_ARCH_DIR
STATE_REL = _ETHS.STATE_REL


class BlockEvent:
    def __init__(
        self,
        story_id: str,
        missing_heading: str,
        pack_path: str,
        remediation: str = REMEDIATION,
    ) -> None:
        self.story_id = story_id
        self.missing_heading = missing_heading
        self.pack_path = pack_path
        self.remediation = remediation

    def format_line(self) -> str:
        return (
            f"{REASON_CODE} story_id={self.story_id} "
            f"missing_heading={self.missing_heading} "
            f"archive_pack_path={self.pack_path} "
            f"remediation={self.remediation}"
        )


def _tests_root(repo: Path) -> Path:
    return repo / "tests"


def _is_excluded_tmp(path: Path, tests_root: Path) -> bool:
    try:
        rel = path.relative_to(tests_root)
    except ValueError:
        return False
    return any(part.startswith(".tmp") for part in rel.parts)


def _function_reads_live_architecture(src: str) -> bool:
    if not src:
        return False
    return any(m in src for m in LIVE_ARCH_MARKERS)


def _heading_literals_from_asserts(src: str) -> Set[str]:
    found: Set[str] = set()
    for m in ASSERT_HEADING_RE.finditer(src):
        tok = m.group(1) or m.group(2)
        if tok:
            found.add(tok)
    return found


def discover_required_arch_headings(repo: Path) -> frozenset[str]:
    """Scan contract tests for live architecture.md heading asserts (DQ2).

    Include a token only when the *same function* reads live
    ``docs/engineering/architecture.md`` and asserts membership / ``find`` /
    ``startswith`` of a literal ``# US-dddd`` or ``# BUG-dddd``.
    Excludes ``tests/.tmp*``. No hand-maintained YAML/manifest.
    """
    tests_root = _tests_root(repo)
    if not tests_root.is_dir():
        return frozenset()
    tokens: Set[str] = set()
    for path in tests_root.rglob("*_test.py"):
        if _is_excluded_tmp(path, tests_root):
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except OSError:
            continue
        try:
            tree = ast.parse(text)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            src = ast.get_source_segment(text, node) or ""
            if not _function_reads_live_architecture(src):
                continue
            tokens.update(_heading_literals_from_asserts(src))
    return frozenset(tokens)


def _heading_token_from_block(block: str) -> Optional[str]:
    first = ""
    for line in block.splitlines():
        stripped = line.strip()
        if stripped:
            first = stripped
            break
    if not first:
        return None
    m = HEADING_TOKEN_RE.search(first)
    return m.group(0) if m else None


def _story_id_from_heading(heading: str) -> str:
    m = STORY_ID_RE.search(heading)
    return m.group(0) if m else heading.lstrip("# ").split()[0]


def auto_repair_enabled(policy: Dict[str, str]) -> bool:
    raw = str(policy.get("ARCH_LINKAGE_AUTO_REPAIR", "0")).strip()
    return raw == "1"


def predict_pack_path(repo: Path) -> Path:
    """Same naming as ``next_pack_path`` without mkdir or file create (no partial write)."""
    archive_dir = repo / ARCH_ARCH_DIR
    day = datetime.now(timezone.utc).strftime("%Y%m%d")
    stem = "architecture-pack"
    base = archive_dir / f"{stem}-{day}.md"
    if not base.exists():
        return base
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for c in alphabet:
        cand = archive_dir / f"{stem}-{day}-{c}.md"
        if not cand.exists():
            return cand
    for c1 in alphabet:
        for c2 in alphabet:
            cand = archive_dir / f"{stem}-{day}-{c1}{c2}.md"
            if not cand.exists():
                return cand
    return archive_dir / f"{stem}-{day}-zz.md"


def predict_architecture_moves(
    repo: Path, policy: Optional[Dict[str, str]] = None
) -> Tuple[List[str], Path, str]:
    """Simulate ``rollover_architecture`` while-pop. Does not write files.

    Imports/calls ``split_arch_stories`` and uses the same while-pop predicate.
    """
    policy = policy if policy is not None else load_merged_policy(repo)
    path = repo / ARCH_REL
    text = path.read_text(encoding="utf-8") if path.is_file() else ""
    max_lines = _int_policy(policy, "ARCH_HOT_MAX_LINES")
    max_stories = _int_policy(policy, "ARCH_HOT_MAX_STORY_SECTIONS")
    preamble, stories = split_arch_stories(text)
    predicted = predict_pack_path(repo)
    if not stories:
        return [], predicted, text
    work = list(stories)
    archived: List[str] = []
    while work and (
        line_count(preamble + "".join(work)) > max_lines or len(work) > max_stories
    ):
        archived.append(work.pop(0))
    new_body = preamble + "".join(work) if archived else text
    return archived, predicted, new_body


def _pack_rel(repo: Path, pack: Path) -> str:
    try:
        return pack.resolve().relative_to(repo.resolve()).as_posix()
    except ValueError:
        return pack.as_posix()


def _events_for_headings(
    headings: Iterable[str], repo: Path, pack: Path
) -> List[BlockEvent]:
    rel = _pack_rel(repo, pack)
    events: List[BlockEvent] = []
    for heading in sorted(set(headings)):
        events.append(
            BlockEvent(
                story_id=_story_id_from_heading(heading),
                missing_heading=heading,
                pack_path=rel,
            )
        )
    return events


def emit_blocked(events: Sequence[BlockEvent], stream=None) -> None:
    out = sys.stderr if stream is None else stream
    for ev in events:
        print(ev.format_line(), file=out)


def run_pre_guard(
    repo: Path, policy: Optional[Dict[str, str]] = None
) -> Tuple[int, List[BlockEvent]]:
    """Pre-hook: block before any archive/hot write when repair is off (AC-1/AC-2)."""
    policy = policy if policy is not None else load_merged_policy(repo)
    required = discover_required_arch_headings(repo)
    archived, predicted, _new_body = predict_architecture_moves(repo, policy)
    moved_tokens: Set[str] = set()
    for block in archived:
        tok = _heading_token_from_block(block)
        if tok:
            moved_tokens.add(tok)
    conflict = required & moved_tokens
    if not conflict:
        return 0, []
    if auto_repair_enabled(policy):
        return 0, []
    events = _events_for_headings(conflict, repo, predicted)
    emit_blocked(events)
    return 1, events


def _hot_has_heading(text: str, token: str) -> bool:
    return token in text


def _title_from_archived_heading_line(line: str) -> str:
    stripped = line.strip()
    m = re.match(r"^# (?:US|BUG)-\d{4}\s*[:\u2014\-]\s*(.+)$", stripped)
    if m:
        return m.group(1).strip()
    return stripped


def _stub_block(heading_line: str, pack_rel: str) -> str:
    token_m = HEADING_TOKEN_RE.search(heading_line)
    token = token_m.group(0) if token_m else heading_line.strip()
    title = _title_from_archived_heading_line(heading_line)
    # Keep STORY_HEADING_H1 separator (em dash).
    stub_h1 = f"{token} — {title}"
    if not STORY_HEADING_H1.match(stub_h1):
        stub_h1 = heading_line.strip()
    pointer = f"Archived body in pack_ref: {pack_rel}"
    return f"{stub_h1}\n{pointer}\n\n"


def _find_tail_insert_index(lines: Sequence[str]) -> int:
    """Insert before US-0089 / US-0090 tail (DEC-0076)."""
    us0089 = None
    us0090 = None
    for i, ln in enumerate(lines):
        stripped = ln.rstrip("\r\n")
        if stripped.startswith("# US-0089"):
            us0089 = i
            break
        if us0090 is None and stripped.startswith("# US-0090"):
            us0090 = i
    if us0089 is not None:
        return us0089
    if us0090 is not None:
        return us0090
    return len(lines)


def _heading_line_from_block(block: str) -> str:
    for line in block.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def _collect_archived_heading_map(repo: Path) -> Dict[str, Tuple[str, str]]:
    """Map heading token -> (first heading line, pack_rel) from archive packs."""
    archive_dir = repo / ARCH_ARCH_DIR
    out: Dict[str, Tuple[str, str]] = {}
    if not archive_dir.is_dir():
        return out
    packs = sorted(archive_dir.glob("architecture-pack-*.md"))
    for pack in packs:
        try:
            text = pack.read_text(encoding="utf-8")
        except OSError:
            continue
        rel = _pack_rel(repo, pack)
        _preamble, blocks = split_arch_stories(text)
        scan_blocks = blocks if blocks else [text]
        for block in scan_blocks:
            line = _heading_line_from_block(block)
            tok = _heading_token_from_block(block)
            if tok and tok not in out:
                out[tok] = (line, rel)
        # Pack header may not split; also scan raw H1 lines.
        for raw in text.splitlines():
            stripped = raw.strip()
            if STORY_HEADING_H1.match(stripped):
                tok = _heading_token_from_block(stripped + "\n")
                if tok and tok not in out:
                    out[tok] = (stripped, rel)
    return out


def inject_h1_stubs(repo: Path, missing: Sequence[str], policy: Dict[str, str]) -> List[str]:
    """Insert minimal H1 stubs before the US-0089 / US-0090 tail. Idempotent."""
    path = repo / ARCH_REL
    hot = path.read_text(encoding="utf-8") if path.is_file() else ""
    heading_map = _collect_archived_heading_map(repo)
    restored: List[str] = []
    stubs: List[str] = []
    pack_refs: List[str] = []
    for token in missing:
        if _hot_has_heading(hot, token):
            continue
        if token not in heading_map:
            continue
        heading_line, pack_rel = heading_map[token]
        stubs.append(_stub_block(heading_line, pack_rel))
        restored.append(token)
        pack_refs.append(pack_rel)
    if not stubs:
        return []
    lines = hot.splitlines(keepends=True)
    idx = _find_tail_insert_index(lines)
    insert = "".join(stubs)
    new_hot = "".join(lines[:idx]) + insert + "".join(lines[idx:])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(new_hot, encoding="utf-8", newline="\n")
    _append_repair_audit(repo, restored, pack_refs[0] if pack_refs else "")
    return restored


def _append_repair_audit(repo: Path, restored: Sequence[str], pack_ref: str) -> None:
    state_path = repo / STATE_REL
    state_path.parent.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    headings = ", ".join(restored)
    row = (
        "\n## Architecture linkage auto-repair audit (US-0129)\n\n"
        f"- timestamp: {ts}\n"
        f"- restored_headings: {headings}\n"
        f"- pack_ref: {pack_ref}\n"
    )
    prior = state_path.read_text(encoding="utf-8") if state_path.is_file() else ""
    state_path.write_text(prior + row, encoding="utf-8", newline="\n")


def run_post_guard(
    repo: Path, policy: Optional[Dict[str, str]] = None
) -> Tuple[int, List[BlockEvent]]:
    """Post-hook: verify active linkage; optional stub restore when flag=1."""
    policy = policy if policy is not None else load_merged_policy(repo)
    required = discover_required_arch_headings(repo)
    path = repo / ARCH_REL
    hot = path.read_text(encoding="utf-8") if path.is_file() else ""
    missing = sorted(tok for tok in required if not _hot_has_heading(hot, tok))
    if not missing:
        return 0, []
    predicted = predict_pack_path(repo)
    # Prefer an existing pack that was actually written.
    archive_dir = repo / ARCH_ARCH_DIR
    existing_packs = sorted(archive_dir.glob("architecture-pack-*.md")) if archive_dir.is_dir() else []
    pack_for_msg = existing_packs[-1] if existing_packs else predicted
    if auto_repair_enabled(policy):
        inject_h1_stubs(repo, missing, policy)
        hot2 = path.read_text(encoding="utf-8") if path.is_file() else ""
        still = sorted(tok for tok in required if not _hot_has_heading(hot2, tok))
        if not still:
            return 0, []
        events = _events_for_headings(still, repo, pack_for_msg)
        for ev in events:
            # Same code; repair failure is message text (no sibling family in v1).
            print(
                f"{ev.format_line()} ARCH_LINKAGE_REPAIR_FAILED",
                file=sys.stderr,
            )
        return 1, events
    events = _events_for_headings(missing, repo, pack_for_msg)
    emit_blocked(events)
    return 1, events


def main(argv: Optional[Sequence[str]] = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--repo", default=None, help="Repository root (default: parent of scripts/)")
    p.add_argument("--pre", action="store_true", help="Pre-rollover linkage guard (no writes on block)")
    p.add_argument("--post", action="store_true", help="Post-rollover linkage verify + optional stub repair")
    args = p.parse_args(argv)
    if args.repo:
        repo = Path(args.repo).resolve()
    else:
        repo = Path(__file__).resolve().parent.parent
    if args.pre == args.post:
        print(
            "STATE_ARCHIVE_VERIFICATION_FAILED expected exactly one of --pre or --post",
            file=sys.stderr,
        )
        return 2
    try:
        if args.pre:
            rc, _events = run_pre_guard(repo)
            return rc
        rc, _events = run_post_guard(repo)
        return rc
    except OSError as exc:
        print(f"{REASON_CODE} io_error detail={exc} remediation={REMEDIATION}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
