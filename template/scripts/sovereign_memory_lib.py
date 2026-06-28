#!/usr/bin/env python3
"""
Sovereign Memory helper library (US-0105 / DEC-0105).

Project-level institutional memory: bounded JSONL artifacts under
docs/engineering/sovereign-memory/ with phase-spawn injection digest.

Reason codes (DEC-0105 §9):
  SOVEREIGN_MEMORY_DISABLED, SOVEREIGN_MEMORY_SCHEMA_INVALID,
  SOVEREIGN_MEMORY_APPEND_FAILED, SOVEREIGN_MEMORY_DECISION_DUPLICATE,
  SOVEREIGN_MEMORY_SECRET_DETECTED, SOVEREIGN_MEMORY_ARCHIVE_REQUIRED,
  SOVEREIGN_MEMORY_READ_BOUND, SOVEREIGN_MEMORY_PROMOTION_SKIPPED

Default-off: SOVEREIGN_MEMORY=0 → zero overhead (no reads, no writes, no digest).
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple

SCHEMA_VERSION = 1
MEMORY_DIR_REL = "docs/engineering/sovereign-memory"
ARCHIVE_DIR_REL = "docs/engineering/sovereign-memory-archive"
RETROSPECTIVES_SUBDIR = "retrospectives"

SOVEREIGN_MEMORY_KEY = "SOVEREIGN_MEMORY"
SOVEREIGN_MEMORY_TOP_N_KEY = "SOVEREIGN_MEMORY_TOP_N"
SOVEREIGN_MEMORY_TOP_K_KEY = "SOVEREIGN_MEMORY_TOP_K"
SOVEREIGN_MEMORY_MAX_CHARS_KEY = "SOVEREIGN_MEMORY_MAX_CHARS"
SOVEREIGN_MEMORY_JSONL_MAX_LINES_KEY = "SOVEREIGN_MEMORY_JSONL_MAX_LINES"

SOVEREIGN_MEMORY_VALUES = frozenset({"0", "1"})
SOVEREIGN_MEMORY_DEFAULT = "0"
SOVEREIGN_MEMORY_TOP_N_DEFAULT = 5
SOVEREIGN_MEMORY_TOP_K_DEFAULT = 3
SOVEREIGN_MEMORY_MAX_CHARS_DEFAULT = 2048
SOVEREIGN_MEMORY_JSONL_MAX_LINES_DEFAULT = 500
SOVEREIGN_MEMORY_READ_TAIL_DEFAULT = 500

TEXT_MAX_CHARS = 2000
RATIONALE_MAX_CHARS = 2000
TAGS_MAX = 10
TAG_MAX_CHARS = 40
DECISION_KEY_HEX_LEN = 16

JSONL_FAMILIES = frozenset({"decisions", "mistakes", "patterns", "plan-drift"})
JSONL_FILENAMES = {
    "decisions": "decisions-log.jsonl",
    "mistakes": "mistakes.jsonl",
    "patterns": "patterns.jsonl",
    "plan-drift": "plan-drift-register.jsonl",
}

STATUS_VALUES = frozenset({"active", "superseded", "archived"})
MISTAKE_TAG_VALUES = frozenset({
    "fix_failed",
    "revert_applied",
    "plan_fidelity_violation",
    "test_regression",
    "scope_creep",
})
MISTAKE_HOOK_TABLE = {
    "fix_failed": "FIX_FAILED",
    "revert_applied": "REVERT_APPLIED",
    "plan_fidelity_violation": "PLAN_FIDELITY_VIOLATION",
    "test_regression": "TEST_REGRESSION",
    "scope_creep": "PLAN_FIDELITY_SCOPE_GATE",
}
DRIFT_TYPE_VALUES = frozenset({
    "ac_drop",
    "ac_reorder",
    "scope_add",
    "plan_change",
    "acceptance_drift",
})

BASE_REQUIRED_FIELDS = frozenset({
    "schema_version",
    "ts",
    "entry_id",
    "impact_score",
    "text",
    "tags",
    "status",
})

DECISIONS_REQUIRED = BASE_REQUIRED_FIELDS | frozenset({
    "decision_key",
    "decision_text",
    "rationale",
})
MISTAKES_REQUIRED = BASE_REQUIRED_FIELDS | frozenset({
    "mistake_tag",
    "failure_reason_code",
})
PATTERNS_REQUIRED = BASE_REQUIRED_FIELDS | frozenset({
    "pattern_id",
    "applies_to",
})
PLAN_DRIFT_REQUIRED = BASE_REQUIRED_FIELDS | frozenset({
    "drift_type",
    "from_artifact",
    "to_artifact",
})

FAMILY_REQUIRED = {
    "decisions": DECISIONS_REQUIRED,
    "mistakes": MISTAKES_REQUIRED,
    "patterns": PATTERNS_REQUIRED,
    "plan-drift": PLAN_DRIFT_REQUIRED,
}

SECRET_PATTERNS = (
    re.compile(r"(?i)(api[_-]?key|secret|password|token|bearer)\s*[:=]\s*\S+"),
    re.compile(r"(?i)-----BEGIN (RSA |EC )?PRIVATE KEY-----"),
    re.compile(r"sk-[a-zA-Z0-9]{20,}"),
    re.compile(r"ghp_[a-zA-Z0-9]{20,}"),
)


class ReasonCode(str, Enum):
    SOVEREIGN_MEMORY_DISABLED = "SOVEREIGN_MEMORY_DISABLED"
    SOVEREIGN_MEMORY_SCHEMA_INVALID = "SOVEREIGN_MEMORY_SCHEMA_INVALID"
    SOVEREIGN_MEMORY_APPEND_FAILED = "SOVEREIGN_MEMORY_APPEND_FAILED"
    SOVEREIGN_MEMORY_DECISION_DUPLICATE = "SOVEREIGN_MEMORY_DECISION_DUPLICATE"
    SOVEREIGN_MEMORY_SECRET_DETECTED = "SOVEREIGN_MEMORY_SECRET_DETECTED"
    SOVEREIGN_MEMORY_ARCHIVE_REQUIRED = "SOVEREIGN_MEMORY_ARCHIVE_REQUIRED"
    SOVEREIGN_MEMORY_READ_BOUND = "SOVEREIGN_MEMORY_READ_BOUND"
    SOVEREIGN_MEMORY_PROMOTION_SKIPPED = "SOVEREIGN_MEMORY_PROMOTION_SKIPPED"


@dataclass
class InjectionDigest:
    digest_text: str
    entry_ids: List[str] = field(default_factory=list)
    char_count: int = 0


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.000Z")


def _archive_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _fsync_file(path: Path) -> None:
    try:
        fd = os.open(str(path), os.O_RDONLY)
        try:
            os.fsync(fd)
        except OSError:
            pass
        finally:
            os.close(fd)
    except OSError:
        pass


def parse_scratchpad_int(
    scratchpad: Optional[Dict[str, str]],
    key: str,
    default: int,
    *,
    minimum: int = 0,
    maximum: Optional[int] = None,
) -> int:
    pad = scratchpad or {}
    raw = pad.get(key, str(default))
    try:
        value = int(str(raw).strip())
    except (TypeError, ValueError):
        value = default
    if maximum is not None:
        value = min(maximum, value)
    return max(minimum, value)


def is_sovereign_memory_enabled(scratchpad: Optional[Dict[str, str]]) -> bool:
    if not scratchpad:
        return False
    return scratchpad.get(SOVEREIGN_MEMORY_KEY, SOVEREIGN_MEMORY_DEFAULT).strip() == "1"


def resolve_memory_dir(repo_root: Optional[Path] = None) -> Path:
    root = Path(repo_root or ".").resolve()
    return root / MEMORY_DIR_REL


def resolve_archive_dir(repo_root: Optional[Path] = None) -> Path:
    root = Path(repo_root or ".").resolve()
    return root / ARCHIVE_DIR_REL


def resolve_jsonl_path(family: str, repo_root: Optional[Path] = None) -> Path:
    if family not in JSONL_FAMILIES:
        raise ValueError(f"unknown family: {family}")
    return resolve_memory_dir(repo_root) / JSONL_FILENAMES[family]


def resolve_retrospectives_dir(repo_root: Optional[Path] = None) -> Path:
    return resolve_memory_dir(repo_root) / RETROSPECTIVES_SUBDIR


def normalize_decision_text(text: str) -> str:
    return " ".join(str(text).strip().lower().split())


def compute_decision_key(decision_text: str) -> str:
    normalized = normalize_decision_text(decision_text)
    digest = hashlib.sha256(normalized.encode("utf-8")).hexdigest()
    return digest[:DECISION_KEY_HEX_LEN]


def scan_secrets(text: str) -> Optional[ReasonCode]:
    for pattern in SECRET_PATTERNS:
        if pattern.search(text or ""):
            return ReasonCode.SOVEREIGN_MEMORY_SECRET_DETECTED
    return None


def schema_check(entry: dict, family: str) -> Tuple[bool, Optional[str]]:
    if family not in JSONL_FAMILIES:
        return False, f"unknown family: {family}"
    if not isinstance(entry, dict):
        return False, "entry must be a dict"

    required = FAMILY_REQUIRED[family]
    missing = required - set(entry.keys())
    if missing:
        return False, f"missing fields: {sorted(missing)}"

    if entry.get("schema_version") != SCHEMA_VERSION:
        return False, "schema_version must be 1"

    if entry.get("status") not in STATUS_VALUES:
        return False, f"status must be one of {sorted(STATUS_VALUES)}"

    impact = entry.get("impact_score")
    if not isinstance(impact, int) or impact < 0 or impact > 100:
        return False, "impact_score must be int 0..100"

    tags = entry.get("tags")
    if not isinstance(tags, list) or len(tags) > TAGS_MAX:
        return False, f"tags must be list with at most {TAGS_MAX} items"
    for tag in tags:
        if not isinstance(tag, str) or len(tag) > TAG_MAX_CHARS:
            return False, f"each tag must be string max {TAG_MAX_CHARS} chars"

    text = entry.get("text", "")
    if not isinstance(text, str) or not text.strip() or len(text) > TEXT_MAX_CHARS:
        return False, f"text must be non-empty string max {TEXT_MAX_CHARS} chars"

    secret = scan_secrets(text)
    if secret:
        return False, ReasonCode.SOVEREIGN_MEMORY_SECRET_DETECTED.value

    if family == "decisions":
        rationale = entry.get("rationale", "")
        if not isinstance(rationale, str) or not rationale.strip() or len(rationale) > RATIONALE_MAX_CHARS:
            return False, f"rationale must be non-empty max {RATIONALE_MAX_CHARS} chars"
        if scan_secrets(rationale):
            return False, ReasonCode.SOVEREIGN_MEMORY_SECRET_DETECTED.value
        dt = entry.get("decision_text", "")
        if scan_secrets(str(dt)):
            return False, ReasonCode.SOVEREIGN_MEMORY_SECRET_DETECTED.value
        expected_key = compute_decision_key(str(dt))
        if entry.get("decision_key") != expected_key:
            return False, "decision_key mismatch"

    if family == "mistakes":
        if entry.get("mistake_tag") not in MISTAKE_TAG_VALUES:
            return False, f"mistake_tag must be one of {sorted(MISTAKE_TAG_VALUES)}"

    if family == "patterns":
        applies = entry.get("applies_to")
        if not isinstance(applies, list):
            return False, "applies_to must be a list"

    if family == "plan-drift":
        if entry.get("drift_type") not in DRIFT_TYPE_VALUES:
            return False, f"drift_type must be one of {sorted(DRIFT_TYPE_VALUES)}"

    return True, None


def _count_nonempty_lines(path: Path) -> int:
    if not path.is_file():
        return 0
    count = 0
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                count += 1
    return count


def _load_existing_decision_keys(repo_root: Optional[Path] = None) -> Set[str]:
    path = resolve_jsonl_path("decisions", repo_root)
    if not path.is_file():
        return set()
    keys: Set[str] = set()
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            key = obj.get("decision_key")
            if isinstance(key, str):
                keys.add(key)
    return keys


def _ensure_memory_dir(repo_root: Optional[Path] = None) -> Tuple[bool, Optional[ReasonCode]]:
    try:
        resolve_memory_dir(repo_root).mkdir(parents=True, exist_ok=True)
        return True, None
    except OSError:
        return False, ReasonCode.SOVEREIGN_MEMORY_APPEND_FAILED


def _append_jsonl_line(
    family: str,
    entry: dict,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    ok_dir, rc_dir = _ensure_memory_dir(repo_root)
    if not ok_dir:
        return False, rc_dir

    ok_archive, rc_archive = maybe_archive_jsonl(family, repo_root, scratchpad)
    if not ok_archive:
        return False, rc_archive

    path = resolve_jsonl_path(family, repo_root)
    try:
        line = json.dumps(entry, separators=(",", ":"), ensure_ascii=False) + "\n"
        with path.open("a", encoding="utf-8") as handle:
            handle.write(line)
            handle.flush()
        _fsync_file(path)
        return True, None
    except OSError:
        return False, ReasonCode.SOVEREIGN_MEMORY_APPEND_FAILED


def read_entries(
    family: str,
    repo_root: Optional[Path] = None,
    *,
    tail_n: Optional[int] = None,
    active_only: bool = True,
) -> Tuple[List[dict], Optional[ReasonCode]]:
    path = resolve_jsonl_path(family, repo_root)
    if not path.exists():
        return [], None

    bound = tail_n if tail_n is not None else SOVEREIGN_MEMORY_READ_TAIL_DEFAULT
    lines: List[str] = []
    truncated = False
    with path.open("r", encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                lines.append(line)
                if len(lines) > bound:
                    truncated = True
                    lines = lines[-bound:]

    entries: List[dict] = []
    for line in lines:
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            return [], ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID
        ok, _ = schema_check(obj, family)
        if not ok:
            return [], ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID
        if active_only and obj.get("status") != "active":
            continue
        entries.append(obj)

    if truncated:
        return entries, ReasonCode.SOVEREIGN_MEMORY_READ_BOUND
    return entries, None


def _sort_recent(entries: Sequence[dict]) -> List[dict]:
    by_id = sorted(entries, key=lambda item: str(item.get("entry_id", "")))
    by_ts = sorted(by_id, key=lambda item: str(item.get("ts", "")), reverse=True)
    return by_ts


def _sort_high_impact(entries: Sequence[dict]) -> List[dict]:
    by_id = sorted(entries, key=lambda item: str(item.get("entry_id", "")))
    by_ts = sorted(by_id, key=lambda item: str(item.get("ts", "")), reverse=True)
    return sorted(by_ts, key=lambda item: -int(item.get("impact_score", 0)))


def _format_digest_line(family: str, entry: dict) -> str:
    label = JSONL_FILENAMES.get(family, family).replace(".jsonl", "")
    text = str(entry.get("text", "")).strip()
    if len(text) > 160:
        text = text[:157] + "..."
    return f"- [{label}] {entry.get('entry_id')}: {text}"


def build_injection_digest(
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> InjectionDigest:
    if not is_sovereign_memory_enabled(scratchpad):
        return InjectionDigest(digest_text="", entry_ids=[], char_count=0)

    top_n = parse_scratchpad_int(scratchpad, SOVEREIGN_MEMORY_TOP_N_KEY, SOVEREIGN_MEMORY_TOP_N_DEFAULT, minimum=0)
    top_k = parse_scratchpad_int(scratchpad, SOVEREIGN_MEMORY_TOP_K_KEY, SOVEREIGN_MEMORY_TOP_K_DEFAULT, minimum=0)
    max_chars = parse_scratchpad_int(
        scratchpad,
        SOVEREIGN_MEMORY_MAX_CHARS_KEY,
        SOVEREIGN_MEMORY_MAX_CHARS_DEFAULT,
        minimum=0,
    )

    all_recent: List[Tuple[str, dict]] = []
    high_impact_pool: List[Tuple[str, dict]] = []

    for family in JSONL_FAMILIES:
        entries, _ = read_entries(family, repo_root, active_only=True)
        for entry in entries:
            all_recent.append((family, entry))
            if family in ("patterns", "mistakes"):
                high_impact_pool.append((family, entry))

    if not all_recent:
        placeholder = "(no sovereign memory entries)"
        return InjectionDigest(
            digest_text=placeholder,
            entry_ids=[],
            char_count=len(placeholder),
        )

    recent_sorted = _sort_recent([entry for _, entry in all_recent])
    recent_ids: List[str] = []
    recent_lines: List[str] = []
    for entry in recent_sorted:
        entry_id = str(entry.get("entry_id"))
        if entry_id in recent_ids:
            continue
        recent_ids.append(entry_id)
        family = next(f for f, e in all_recent if e.get("entry_id") == entry_id)
        recent_lines.append(_format_digest_line(family, entry))
        if len(recent_ids) >= top_n:
            break

    high_sorted = _sort_high_impact([entry for _, entry in high_impact_pool])
    high_lines: List[str] = []
    high_ids: List[str] = []
    selected = set(recent_ids)
    for entry in high_sorted:
        entry_id = str(entry.get("entry_id"))
        if entry_id in selected:
            continue
        selected.add(entry_id)
        high_ids.append(entry_id)
        family = next(f for f, e in high_impact_pool if e.get("entry_id") == entry_id)
        high_lines.append(_format_digest_line(family, entry))
        if len(high_ids) >= top_k:
            break

    sections: List[str] = []
    if recent_lines:
        sections.append("## Recent learnings\n" + "\n".join(recent_lines))
    if high_lines:
        sections.append("## High-impact patterns\n" + "\n".join(high_lines))

    digest_text = "\n\n".join(sections) if sections else "(no sovereign memory entries)"
    if max_chars > 0 and len(digest_text) > max_chars:
        digest_text = digest_text[: max_chars - 3].rstrip() + "..."

    ordered_ids = recent_ids + [item for item in high_ids if item not in recent_ids]
    return InjectionDigest(
        digest_text=digest_text,
        entry_ids=ordered_ids,
        char_count=len(digest_text),
    )


def build_injection_digest_block(
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Optional[str]:
    """Spawn assembler helper: fenced sovereign_memory_digest block or None when disabled."""
    if not is_sovereign_memory_enabled(scratchpad):
        return None
    digest = build_injection_digest(repo_root, scratchpad)
    return (
        "### sovereign_memory_digest\n\n"
        "```\n"
        f"{digest.digest_text}\n"
        "```\n"
    )


def dedupe_decision(
    decision_text: str,
    existing_keys: Iterable[str],
) -> Tuple[str, bool]:
    key = compute_decision_key(decision_text)
    return key, key in set(existing_keys)


def maybe_archive_jsonl(
    family: str,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return True, None

    path = resolve_jsonl_path(family, repo_root)
    if not path.is_file():
        return True, None

    max_lines = parse_scratchpad_int(
        scratchpad,
        SOVEREIGN_MEMORY_JSONL_MAX_LINES_KEY,
        SOVEREIGN_MEMORY_JSONL_MAX_LINES_DEFAULT,
        minimum=1,
    )
    if _count_nonempty_lines(path) < max_lines:
        return True, None

    archive_dir = resolve_archive_dir(repo_root)
    basename = path.stem
    archive_path = archive_dir / f"{basename}-{_archive_timestamp()}.jsonl"
    try:
        archive_dir.mkdir(parents=True, exist_ok=True)
        if archive_path.exists():
            return True, None
        path.replace(archive_path)
        path.write_text("", encoding="utf-8")
        _fsync_file(path)
        return True, None
    except OSError:
        return False, ReasonCode.SOVEREIGN_MEMORY_ARCHIVE_REQUIRED


def append_decision(
    entry: dict,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return False, ReasonCode.SOVEREIGN_MEMORY_DISABLED
    ok, _ = schema_check(entry, "decisions")
    if not ok:
        return False, ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID

    existing = _load_existing_decision_keys(repo_root)
    _, is_dup = dedupe_decision(str(entry.get("decision_text", "")), existing)
    if is_dup:
        return False, ReasonCode.SOVEREIGN_MEMORY_DECISION_DUPLICATE

    return _append_jsonl_line("decisions", entry, repo_root, scratchpad)


def append_mistake(
    entry: dict,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return False, ReasonCode.SOVEREIGN_MEMORY_DISABLED
    ok, _ = schema_check(entry, "mistakes")
    if not ok:
        return False, ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID
    return _append_jsonl_line("mistakes", entry, repo_root, scratchpad)


def append_pattern(
    entry: dict,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return False, ReasonCode.SOVEREIGN_MEMORY_DISABLED
    ok, _ = schema_check(entry, "patterns")
    if not ok:
        return False, ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID
    return _append_jsonl_line("patterns", entry, repo_root, scratchpad)


def append_drift(
    entry: dict,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return False, ReasonCode.SOVEREIGN_MEMORY_DISABLED
    ok, _ = schema_check(entry, "plan-drift")
    if not ok:
        return False, ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID
    return _append_jsonl_line("plan-drift", entry, repo_root, scratchpad)


def build_mistake_entry(
    *,
    mistake_tag: str,
    failure_reason_code: str,
    text: str,
    impact_score: int = 50,
    source_orchestrator_run_id: Optional[str] = None,
    source_story_id: Optional[str] = None,
    phase_id: Optional[str] = None,
    provenance_ref: Optional[str] = None,
    tags: Optional[List[str]] = None,
) -> dict:
    return {
        "schema_version": SCHEMA_VERSION,
        "ts": _utc_now_iso(),
        "entry_id": str(uuid.uuid4()),
        "source_orchestrator_run_id": source_orchestrator_run_id,
        "source_story_id": source_story_id,
        "phase_id": phase_id,
        "impact_score": impact_score,
        "text": text[:TEXT_MAX_CHARS],
        "tags": tags or ["mistake"],
        "status": "active",
        "provenance_ref": provenance_ref,
        "mistake_tag": mistake_tag,
        "failure_reason_code": failure_reason_code,
    }


def record_mistake_hook(
    mistake_tag: str,
    *,
    text: str,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
    source_orchestrator_run_id: Optional[str] = None,
    source_story_id: Optional[str] = None,
    phase_id: Optional[str] = None,
    provenance_ref: Optional[str] = None,
) -> Tuple[bool, Optional[ReasonCode]]:
    """Orchestrator-detectable mistake hook — no-op when SOVEREIGN_MEMORY=0."""
    if mistake_tag not in MISTAKE_TAG_VALUES:
        return False, ReasonCode.SOVEREIGN_MEMORY_SCHEMA_INVALID
    failure_reason_code = MISTAKE_HOOK_TABLE.get(mistake_tag, mistake_tag.upper())
    entry = build_mistake_entry(
        mistake_tag=mistake_tag,
        failure_reason_code=failure_reason_code,
        text=text,
        source_orchestrator_run_id=source_orchestrator_run_id,
        source_story_id=source_story_id,
        phase_id=phase_id,
        provenance_ref=provenance_ref,
    )
    return append_mistake(entry, repo_root, scratchpad)


def promote_from_ledger(
    orchestrator_run_id: str,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
    *,
    decision_types: Optional[Sequence[str]] = None,
) -> Tuple[List[str], Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return [], ReasonCode.SOVEREIGN_MEMORY_DISABLED

    pad = scratchpad or {}
    if pad.get("AI_DECISION_LEDGER", "0").strip() != "1":
        return [], ReasonCode.SOVEREIGN_MEMORY_PROMOTION_SKIPPED

    try:
        from decision_ledger_lib import (  # noqa: WPS433
            ReasonCode as LedgerReasonCode,
            read_entries as read_ledger_entries,
            resolve_ledger_path,
        )
    except ImportError:
        return [], ReasonCode.SOVEREIGN_MEMORY_PROMOTION_SKIPPED

    ledger_path = resolve_ledger_path(orchestrator_run_id, repo_root)
    entries, rc, _ = read_ledger_entries(ledger_path)
    if rc == LedgerReasonCode.LEDGER_FILE_MISSING or not entries:
        return [], ReasonCode.SOVEREIGN_MEMORY_PROMOTION_SKIPPED

    types_filter = set(decision_types) if decision_types else None
    promoted: List[str] = []
    existing_keys = _load_existing_decision_keys(repo_root)

    for ledger_entry in entries:
        dt = str(ledger_entry.get("decision_type", ""))
        if types_filter is not None and dt not in types_filter:
            continue
        decision_text = str(ledger_entry.get("rationale", "")).strip()
        if not decision_text:
            decision_text = (
                f"{ledger_entry.get('from_artifact', '(none)')} -> "
                f"{ledger_entry.get('to_artifact', '(none)')}"
            )
        key, is_dup = dedupe_decision(decision_text, existing_keys)
        if is_dup:
            continue

        entry_id = str(uuid.uuid4())
        memory_entry = {
            "schema_version": SCHEMA_VERSION,
            "ts": _utc_now_iso(),
            "entry_id": entry_id,
            "source_orchestrator_run_id": orchestrator_run_id,
            "source_story_id": None,
            "phase_id": ledger_entry.get("phase_id"),
            "impact_score": 60,
            "text": decision_text[:TEXT_MAX_CHARS],
            "tags": ["promoted", "ledger"],
            "status": "active",
            "provenance_ref": f"ledger:{ledger_entry.get('decision_id')}",
            "decision_key": key,
            "decision_text": decision_text[:TEXT_MAX_CHARS],
            "rationale": f"Promoted from per-run ledger decision_type={dt}.",
        }
        ok, reason = append_decision(memory_entry, repo_root, scratchpad)
        if ok:
            promoted.append(entry_id)
            existing_keys.add(key)

    if not promoted:
        return [], ReasonCode.SOVEREIGN_MEMORY_PROMOTION_SKIPPED
    return promoted, None


def write_retrospective(
    sprint_id: str,
    body: str,
    repo_root: Optional[Path] = None,
    scratchpad: Optional[Dict[str, str]] = None,
) -> Tuple[Optional[Path], Optional[ReasonCode]]:
    if not is_sovereign_memory_enabled(scratchpad):
        return None, ReasonCode.SOVEREIGN_MEMORY_DISABLED

    ok_dir, rc_dir = _ensure_memory_dir(repo_root)
    if not ok_dir:
        return None, rc_dir

    retro_dir = resolve_retrospectives_dir(repo_root)
    try:
        retro_dir.mkdir(parents=True, exist_ok=True)
        path = retro_dir / f"{sprint_id}.md"
        path.write_text(body, encoding="utf-8")
        _fsync_file(path)
        return path, None
    except OSError:
        return None, ReasonCode.SOVEREIGN_MEMORY_APPEND_FAILED


def build_sample_decision() -> dict:
    decision_text = "Prefer create-on-first-write for sovereign-memory JSONL files"
    return {
        "schema_version": SCHEMA_VERSION,
        "ts": _utc_now_iso(),
        "entry_id": str(uuid.uuid4()),
        "source_orchestrator_run_id": "auto-research-stub",
        "source_story_id": "US-0105",
        "phase_id": "research",
        "impact_score": 70,
        "text": decision_text,
        "tags": ["schema", "bootstrap"],
        "status": "active",
        "provenance_ref": "R-0093",
        "decision_key": compute_decision_key(decision_text),
        "decision_text": decision_text,
        "rationale": "Avoids empty tracked JSONL clutter; directory .gitkeep suffices until first write.",
    }


def build_sample_mistake() -> dict:
    return build_mistake_entry(
        mistake_tag="fix_failed",
        failure_reason_code="FIX_FAILED",
        text="Auto-loop exhausted fix attempts without green QA.",
        source_story_id="US-0105",
        phase_id="execute",
    )


def self_test() -> bool:
    errors: List[str] = []

    if is_sovereign_memory_enabled({SOVEREIGN_MEMORY_KEY: "0"}):
        errors.append("SOVEREIGN_MEMORY=0 must disable")
    if not is_sovereign_memory_enabled({SOVEREIGN_MEMORY_KEY: "1"}):
        errors.append("SOVEREIGN_MEMORY=1 must enable")

    sample = build_sample_decision()
    ok, err = schema_check(sample, "decisions")
    if not ok:
        errors.append(f"decisions schema_check failed: {err}")

    key_a = compute_decision_key("Prefer create-on-first-write")
    key_b = compute_decision_key("prefer   create-on-first-write")
    if key_a != key_b:
        errors.append("decision_key normalization mismatch")

    _, is_dup = dedupe_decision("Prefer create-on-first-write", {key_a})
    if not is_dup:
        errors.append("dedupe_decision should detect duplicate key")

    disabled = build_injection_digest(scratchpad={SOVEREIGN_MEMORY_KEY: "0"})
    if disabled.digest_text or disabled.entry_ids:
        errors.append("disabled gate must return empty digest")

    if build_injection_digest_block(scratchpad={SOVEREIGN_MEMORY_KEY: "0"}) is not None:
        errors.append("digest block must be None when disabled")

    enabled = build_injection_digest(scratchpad={
        SOVEREIGN_MEMORY_KEY: "1",
        SOVEREIGN_MEMORY_MAX_CHARS_KEY: "128",
    })
    if enabled.char_count > 128:
        errors.append("digest must respect SOVEREIGN_MEMORY_MAX_CHARS")

    secret_sample = build_sample_decision()
    secret_sample["text"] = "api_key=supersecretvalue"
    bad, bad_err = schema_check(secret_sample, "decisions")
    if bad or bad_err != ReasonCode.SOVEREIGN_MEMORY_SECRET_DETECTED.value:
        errors.append("secret scanner must reject api_key patterns")

    if len(FAMILY_REQUIRED) != 4:
        errors.append("expected four JSONL families")

    if len(MISTAKE_HOOK_TABLE) != len(MISTAKE_TAG_VALUES):
        errors.append("mistake hook table must cover all tags")

    if errors:
        for item in errors:
            print(f"  {item}", file=sys.stderr)
        print("[SELF_TEST_FAILED]", file=sys.stderr)
        return False

    print("[SOVEREIGN_MEMORY_SELF_TEST_OK]")
    return True


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Sovereign memory library (US-0105 / DEC-0105)")
    parser.add_argument("--self-test", action="store_true", help="Run self-test")
    args = parser.parse_args()
    if args.self_test:
        sys.exit(0 if self_test() else 1)
    parser.print_help()
    sys.exit(2)
