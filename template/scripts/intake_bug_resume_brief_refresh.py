#!/usr/bin/env python3
"""
Atomic refresh of handoffs/resume_brief.md after successful /intake bug persistence (DEC-0069 / BUG-0005).

Idempotent: same inputs yield the same latest-pointer section. Uses temp file + os.replace for atomicity.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
import tempfile
from pathlib import Path

import bug_issue_lib as bi
import bug_issue_validate as biv


def bug_status(backlog_text: str, bug_id: str) -> str | None:
    section = bi.extract_bug_section(backlog_text)
    if not section:
        return None
    for issue in bi.parse_bug_issues(section):
        if issue.bug_id == bug_id:
            return issue.status
    return None


def upsert_latest_orchestration_pointer(full_text: str, latest_block: str) -> str:
    """Replace ## Latest orchestration pointer section or insert after # Resume Brief."""
    latest_block = latest_block.rstrip("\n") + "\n"
    lines = full_text.splitlines(keepends=True)
    if not lines:
        return "# Resume Brief\n\n" + latest_block

    out: list[str] = []
    i = 0
    replaced = False
    while i < len(lines):
        line = lines[i]
        if line.startswith("## Latest orchestration pointer"):
            out.append(latest_block)
            i += 1
            while i < len(lines) and not lines[i].startswith("## "):
                i += 1
            replaced = True
            continue
        out.append(line)
        i += 1

    if replaced:
        return "".join(out)

    text = "".join(lines)
    stripped = text.lstrip("\n")
    if stripped.startswith("# Resume Brief"):
        return text.rstrip("\n") + "\n\n" + latest_block
    return "# Resume Brief\n\n" + latest_block + text.lstrip("\n")


def build_latest_pointer_markdown(
    *,
    bug_id: str,
    intake_boundary_utc: str,
    orchestrator_run_id: str | None,
    intake_evidence_ref: str | None,
    sprint_id: str | None,
) -> str:
    orch = orchestrator_run_id if orchestrator_run_id else "(unknown)"
    ev = intake_evidence_ref if intake_evidence_ref else "(none)"
    spr = sprint_id if sprint_id else "(none)"
    return f"""## Latest orchestration pointer — post-bug-intake (DEC-0069)

- **Boundary**: successful **`/intake bug`** persistence (**`US-0045`**) — **`intake_boundary_utc={intake_boundary_utc}`**
- **`bug_id`**: **`{bug_id}`** — must remain **`OPEN`** in **`docs/product/backlog.md`** (authority); this refresh is rejected if backlog shows **DONE**
- **Intake evidence ref**: `{ev}`
- **`orchestrator_run_id`**: `{orch}` (boundary metadata when known; optional at intake)
- **Contract**: default **`/auto`** continuation targets **`discovery`** for this OPEN bug (not a stale pre-intake **`intake`** resume target)

## Current status

- **Active bug**: **`{bug_id}`** — **OPEN** per **`docs/product/backlog.md`** at refresh time

## Intended resume phase

`discovery`

## Resume target

- bug_id={bug_id}
- story_id=(none)
- sprint_id={spr}
- boundary=post-bug-intake (**DEC-0069**)

## Latest auto breadcrumb seed

- requested_start_from=(none)
- resolved_start_phase=discovery
- resolution_source=resume_brief
- resolution_status=resolved
- stop_reason=intake_complete
- stop_phase=intake
- next_scheduled_phase=discovery
- bug_id={bug_id}
- story_id=(none)
- sprint_id={spr}
- orchestrator_run_id={orch}
- intake_boundary_utc={intake_boundary_utc}
"""


def extract_brief_bug_id(brief_text: str) -> str | None:
    for line in brief_text.splitlines():
        s = line.strip()
        m = re.match(r"^-\s*bug_id=(BUG-\d{4})\s*$", s)
        if m:
            return m.group(1)
    return None


def validate_brief_open_bug_alignment(brief_text: str, backlog_text: str) -> list[str]:
    """Writer-side guard: brief bug_id must match an OPEN row in backlog (US-0045)."""
    errors: list[str] = []
    bid = extract_brief_bug_id(brief_text)
    if not bid:
        errors.append("INTAKE_RESUME_BRIEF_PARSE_BUG_ID_MISSING")
        return errors

    st = bug_status(backlog_text, bid)
    if st is None:
        errors.append(f"INTAKE_RESUME_BRIEF_BACKLOG_BUG_UNKNOWN:{bid}")
        return errors
    if st != "OPEN":
        errors.append(f"INTAKE_RESUME_BRIEF_BACKLOG_CONTRADICTION:{bid}:status={st}")
    if "`discovery`" not in brief_text and "resolved_start_phase=discovery" not in brief_text:
        errors.append("INTAKE_RESUME_BRIEF_DISCOVERY_PHASE_MISSING")
    return errors


def atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(
        dir=path.parent,
        prefix=".resume_brief_tmp_",
        suffix=".md",
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
        os.replace(tmp, path)
    except Exception:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def _fail(code: str, detail: str = "") -> int:
    msg = code
    if detail:
        msg += f": {detail}"
    print(msg, file=sys.stderr)
    return 1


def self_test() -> int:
    block = build_latest_pointer_markdown(
        bug_id="BUG-0999",
        intake_boundary_utc="2026-04-03T12:00:00Z",
        orchestrator_run_id="auto-test",
        intake_evidence_ref="handoffs/intake_evidence/x.json",
        sprint_id="S0001",
    )
    old = "# Resume Brief\n\n## Latest orchestration pointer — old\n\n- x\n\n## Checkpoint\n\nkeep\n"
    new = upsert_latest_orchestration_pointer(old, block)
    if "keep" not in new:
        return _fail("SELFTEST_FAILED", "lost tail section")
    if "BUG-0999" not in new or "resolved_start_phase=discovery" not in new:
        return _fail("SELFTEST_FAILED", "missing expected content")
    if "## Latest orchestration pointer — old" in new:
        return _fail("SELFTEST_FAILED", "old latest not replaced")
    good_backlog = """## Bug issues (canonical)

### BUG-0999 — T
- Status: OPEN
- environment: e
- steps_to_reproduce: s
- expected: x
- actual: y
- evidence_refs: z
"""
    errs = validate_brief_open_bug_alignment(new, good_backlog)
    if errs:
        return _fail("SELFTEST_FAILED", str(errs))
    bad_backlog = good_backlog.replace("OPEN", "DONE")
    errs2 = validate_brief_open_bug_alignment(new, bad_backlog)
    if not any("CONTRADICTION" in e for e in errs2):
        return _fail("SELFTEST_FAILED", "expected contradiction on DONE")
    print("[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--bug-id", default="", help="Persisted BUG-#### id (required unless --self-test)")
    ap.add_argument("--backlog", default="docs/product/backlog.md")
    ap.add_argument("--resume-brief", default="handoffs/resume_brief.md")
    ap.add_argument(
        "--intake-boundary-utc",
        default="",
        help="RFC3339 UTC timestamp for intake completion boundary (required unless --validate-file)",
    )
    ap.add_argument("--orchestrator-run-id", default="", help="Optional orchestrator run id")
    ap.add_argument("--intake-evidence", default="", help="Optional intake evidence path or ref")
    ap.add_argument("--sprint-id", default="", help="Optional sprint id")
    ap.add_argument("--dry-run", action="store_true", help="Print body only; do not write")
    ap.add_argument("--validate-file", action="store_true", help="Validate existing brief vs backlog; no write")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    if not args.bug_id:
        return _fail("INTAKE_RESUME_BRIEF_INVALID_BUG_ID", "missing --bug-id")
    if not re.fullmatch(r"BUG-\d{4}", args.bug_id):
        return _fail("INTAKE_RESUME_BRIEF_INVALID_BUG_ID", args.bug_id)

    try:
        backlog_text = Path(args.backlog).read_text(encoding="utf-8")
    except OSError as e:
        return _fail("INTAKE_RESUME_BRIEF_IO_ERROR", str(e))

    berr, _ = biv.validate_backlog(backlog_text)
    if berr:
        for e in berr:
            print(e, file=sys.stderr)
        return _fail("INTAKE_RESUME_BRIEF_BACKLOG_INVALID", berr[0])

    resume_path = Path(args.resume_brief)
    if args.validate_file:
        if not resume_path.is_file():
            return _fail("INTAKE_RESUME_BRIEF_MISSING", str(resume_path))
        brief_text = resume_path.read_text(encoding="utf-8")
        bid_file = extract_brief_bug_id(brief_text)
        if bid_file != args.bug_id:
            return _fail(
                "INTAKE_RESUME_BRIEF_BUG_ID_MISMATCH",
                f"cli={args.bug_id} brief={bid_file}",
            )
        verr = validate_brief_open_bug_alignment(brief_text, backlog_text)
        if verr:
            for e in verr:
                print(e, file=sys.stderr)
            return 1
        print("[INTAKE_RESUME_BRIEF_VALIDATE_OK]")
        return 0

    if not args.intake_boundary_utc.strip():
        return _fail("INTAKE_RESUME_BRIEF_BOUNDARY_UTC_REQUIRED", "supply --intake-boundary-utc")

    st = bug_status(backlog_text, args.bug_id)
    if st is None:
        return _fail("INTAKE_RESUME_BRIEF_BUG_NOT_FOUND", args.bug_id)
    if st != "OPEN":
        return _fail(
            "INTAKE_RESUME_BRIEF_BACKLOG_CONTRADICTION",
            f"{args.bug_id} must be OPEN for discovery default; got {st}",
        )

    block = build_latest_pointer_markdown(
        bug_id=args.bug_id,
        intake_boundary_utc=args.intake_boundary_utc,
        orchestrator_run_id=args.orchestrator_run_id or None,
        intake_evidence_ref=args.intake_evidence or None,
        sprint_id=args.sprint_id or None,
    )

    prior = resume_path.read_text(encoding="utf-8") if resume_path.is_file() else ""
    merged = upsert_latest_orchestration_pointer(prior, block)
    verr = validate_brief_open_bug_alignment(merged, backlog_text)
    if verr:
        for e in verr:
            print(e, file=sys.stderr)
        return 1

    if args.dry_run:
        print(merged)
        return 0

    try:
        atomic_write(resume_path, merged)
    except OSError as e:
        return _fail("INTAKE_RESUME_BRIEF_WRITE_FAILED", str(e))

    print("[INTAKE_BUG_RESUME_BRIEF_REFRESH_OK]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
