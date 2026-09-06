#!/usr/bin/env python3
"""BUG-0015 thin OpenCode auto bridge (IsolationEvidence + first-phase).

Durable SOT remains docs/engineering/state.md (US-0048 / DEC-0029).
First-phase order (architecture CF3 / R-0114 DQ3):
  argv --start-from → resume_brief → scratchpad → US-0087 bug-queue.
AUTO_SCHEDULER_CONFLICT mutex semantics unchanged (story-drain vs bug-queue).
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

EXIT_OK = 0
EXIT_FAIL = 1


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _parse_resume_brief(repo: Path) -> dict[str, str]:
    path = repo / "handoffs" / "resume_brief.md"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    out: dict[str, str] = {}
    for key in (
        "intended_resume_phase",
        "next_scheduled_phase",
        "orchestrator_run_id",
        "story_id",
        "bug_id",
        "sprint_id",
    ):
        m = re.search(rf"`{key}`\s*:\s*\*\*`([^`]+)`\*\*", text)
        if m:
            out[key] = m.group(1)
            continue
        m2 = re.search(rf"- `{key}`:\s*`([^`]+)`", text)
        if m2:
            out[key] = m2.group(1)
            continue
        m3 = re.search(rf"{key}=([^\s`;]+)", text)
        if m3:
            out[key] = m3.group(1)
    return out


def _merge_scratchpad(repo: Path) -> dict[str, str]:
    merged: dict[str, str] = {}
    for name in (".cursor/scratchpad.md", ".cursor/scratchpad.local.md"):
        path = repo / name
        if not path.is_file():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            m = re.match(r"^([A-Z][A-Z0-9_]*)=(.*)$", line.strip())
            if m:
                merged[m.group(1)] = m.group(2).strip()
    return merged


def _parse_state_next_phase(repo: Path) -> str | None:
    path = repo / "docs" / "engineering" / "state.md"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    matches = re.findall(r"next_scheduled_phase[=:][\s`*]*([^\s`;*`]+)", text)
    if matches:
        return matches[0].strip("`")
    return None


def select_first_phase(
    repo: Path,
    *,
    start_from: str | None,
    bug_target: str | None,
) -> dict:
    if start_from and start_from.strip():
        return {
            "ok": True,
            "phase_id": start_from.strip().lstrip("/"),
            "source": "argv",
        }

    resume = _parse_resume_brief(repo)
    for key in ("intended_resume_phase", "next_scheduled_phase"):
        val = resume.get(key, "").strip().lstrip("/")
        if val and val not in ("(none)", "auto", "n/a"):
            return {"ok": True, "phase_id": val, "source": f"resume_brief:{key}"}

    scratch = _merge_scratchpad(repo)
    # Story-drain vs bug-queue mutex (US-0087) — unchanged conflict code.
    story_drain = scratch.get("AUTO_BACKLOG_DRAIN", "0") == "1"
    bug_queue = scratch.get("AUTO_BUG_QUEUE", "0") == "1"
    if story_drain and bug_queue and not bug_target:
        return {"ok": False, "reasonCode": "AUTO_SCHEDULER_CONFLICT"}

    for key in (
        "INTENDED_RESUME_PHASE",
        "NEXT_SCHEDULED_PHASE",
        "AUTO_START_FROM",
    ):
        val = scratch.get(key, "").strip().lstrip("/")
        if val:
            return {"ok": True, "phase_id": val, "source": f"scratchpad:{key}"}

    if bug_queue or bug_target:
        # US-0087 bug-queue win: start at intake/discovery for the bug segment.
        return {
            "ok": True,
            "phase_id": "intake" if not bug_target else "research",
            "source": "us0087_bug_queue",
            "bug_target": bug_target or resume.get("bug_id", ""),
        }

    state_phase = _parse_state_next_phase(repo)
    if state_phase and state_phase not in ("(none)", "auto"):
        return {
            "ok": True,
            "phase_id": state_phase.lstrip("/"),
            "source": "state.md",
        }

    return {"ok": True, "phase_id": "execute", "source": "default"}


def append_isolation(
    repo: Path,
    *,
    parent_id: str,
    session_id: str,
    role: str,
    phase_id: str,
    timestamp: str,
    fresh_context_marker: str,
    state_path: Path | None = None,
) -> dict:
    if not parent_id or not session_id or session_id == parent_id:
        return {"ok": False, "reasonCode": "OPENCODE_SUBTASK_IGNORED"}
    path = state_path or (repo / "docs" / "engineering" / "state.md")
    path.parent.mkdir(parents=True, exist_ok=True)
    block = (
        "\n### IsolationEvidence (OpenCode plugin / BUG-0015)\n\n"
        f"- parentID=`{parent_id}`\n"
        f"- sessionID=`{session_id}`\n"
        f"- role=`{role}`\n"
        f"- phase_id=`{phase_id}`\n"
        f"- timestamp=`{timestamp or _utc_now_iso()}`\n"
        f"- fresh_context_marker=`{fresh_context_marker}`\n"
        f"- sessionID_ne_parentID=`true`\n"
    )
    if path.is_file():
        existing = path.read_text(encoding="utf-8")
        path.write_text(block + "\n" + existing, encoding="utf-8")
    else:
        path.write_text(block.lstrip() + "\n", encoding="utf-8")
    return {"ok": True}


def main() -> int:
    parser = argparse.ArgumentParser(description="BUG-0015 OpenCode auto bridge")
    parser.add_argument("--repo", default=".", help="Repository root")
    parser.add_argument(
        "--select-first-phase",
        action="store_true",
        help="Emit JSON first-phase selection",
    )
    parser.add_argument("--start-from", default=None, help="Explicit phase argv")
    parser.add_argument("--bug-target", default=None, help="Bug id when bug-queue wins")
    parser.add_argument(
        "--orchestrator-run-id",
        default=None,
        dest="orchestrator_run_id",
    )
    parser.add_argument(
        "--append-isolation",
        action="store_true",
        help="Append IsolationEvidence block to state.md",
    )
    parser.add_argument("--parent-id", default=None)
    parser.add_argument("--session-id", default=None)
    parser.add_argument("--role", default=None)
    parser.add_argument("--phase-id", default=None)
    parser.add_argument("--timestamp", default=None)
    parser.add_argument("--fresh-context-marker", default=None)
    parser.add_argument("--state-path", default=None, help="Override state.md path")
    args = parser.parse_args()
    repo = Path(args.repo).resolve()

    if args.select_first_phase:
        payload = select_first_phase(
            repo, start_from=args.start_from, bug_target=args.bug_target
        )
        sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        sys.stdout.write("\n")
        return EXIT_OK if payload.get("ok") else EXIT_FAIL

    if args.append_isolation:
        if not all(
            [
                args.parent_id,
                args.session_id,
                args.role,
                args.phase_id,
                args.fresh_context_marker,
            ]
        ):
            sys.stderr.write("append-isolation requires identity fields\n")
            return EXIT_FAIL
        state_path = Path(args.state_path) if args.state_path else None
        payload = append_isolation(
            repo,
            parent_id=args.parent_id,
            session_id=args.session_id,
            role=args.role,
            phase_id=args.phase_id,
            timestamp=args.timestamp or _utc_now_iso(),
            fresh_context_marker=args.fresh_context_marker,
            state_path=state_path,
        )
        sys.stdout.write(json.dumps(payload, sort_keys=True, separators=(",", ":")))
        sys.stdout.write("\n")
        return EXIT_OK if payload.get("ok") else EXIT_FAIL

    parser.print_help()
    return EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main())
