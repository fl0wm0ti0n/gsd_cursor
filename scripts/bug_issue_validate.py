#!/usr/bin/env python3
"""
Validate canonical bug issues in backlog.md and optional acceptance reconciliation (US-0079 / DEC-0061).
"""

from __future__ import annotations

import argparse
import re
import sys

import bug_issue_lib as bi

OK_TAG = "[BUG_VALIDATION_OK]"


def _fail(code: str, detail: str = "") -> int:
    msg = f"{code}"
    if detail:
        msg += f": {detail}"
    print(msg, file=sys.stderr)
    return 1


def validate_backlog(text: str) -> tuple[list[str], list[bi.BugIssue]]:
    errors: list[str] = []
    if bi.BUG_SECTION_HEADER not in text:
        errors.append("BUG_VALIDATION_SECTION_MISSING")
        return errors, []
    body = bi.extract_bug_section(text)
    if body is None:
        errors.append("BUG_VALIDATION_SECTION_MISSING")
        return errors, []
    issues = bi.parse_bug_issues(body)
    if not issues:
        # Empty bug portfolio is valid (stub-only section)
        return [], []

    if not bi.issues_sorted_by_id(issues):
        errors.append("BUG_VALIDATION_ORDER_INVERSION")

    seen: set[str] = set()
    for issue in issues:
        if issue.bug_id in seen:
            errors.append(f"BUG_VALIDATION_DUPLICATE_ID:{issue.bug_id}")
        seen.add(issue.bug_id)
        if not re.fullmatch(r"BUG-\d{4}", issue.bug_id):
            errors.append(f"BUG_VALIDATION_MALFORMED_ID:{issue.bug_id}")
        if issue.status is None:
            errors.append(f"BUG_VALIDATION_STATUS_INVALID:{issue.bug_id}:missing")
        elif issue.status not in bi.ALLOWED_STATUS:
            errors.append(f"BUG_VALIDATION_STATUS_INVALID:{issue.bug_id}:{issue.status}")
        for key in bi.REQUIRED_FIELDS:
            if not bi.field_non_empty(issue.fields.get(key, "")):
                errors.append(f"BUG_VALIDATION_FIELD_EMPTY:{issue.bug_id}:{key}")
    return errors, issues


def _parse_acceptance_bug_rows(text: str) -> dict[str, bool]:
    """Map BUG-xxxx -> True if checked in ## Bug acceptance (canonical)."""
    if "## Bug acceptance (canonical)" not in text:
        return {}
    start = text.index("## Bug acceptance (canonical)")
    rest = text[start + len("## Bug acceptance (canonical)") :]
    end_m = re.search(r"\n## [^\n#]", rest)
    if end_m:
        chunk = rest[: end_m.start()]
    else:
        chunk = rest
    out: dict[str, bool] = {}
    for line in chunk.splitlines():
        m = re.match(r"^-\s*\[([ xX])\]\s*(BUG-\d{4})\b", line.strip())
        if m:
            out[m.group(2)] = m.group(1).lower() == "x"
    return out


def reconcile_acceptance(backlog_text: str, acceptance_text: str) -> list[str]:
    errors: list[str] = []
    _, issues = validate_backlog(backlog_text)
    # Re-run without early exit on section — validate_backlog already clears
    acc_map = _parse_acceptance_bug_rows(acceptance_text)
    for issue in issues:
        want_done = issue.status == "DONE"
        if issue.bug_id not in acc_map:
            errors.append(f"BUG_RECONCILE_ACCEPTANCE_MISSING_ROW:{issue.bug_id}")
            continue
        checked = acc_map[issue.bug_id]
        if want_done != checked:
            errors.append(
                f"BUG_RECONCILE_ACCEPTANCE_STATE_MISMATCH:{issue.bug_id}:backlog={issue.status}:acceptance_checked={checked}"
            )
    # Rows in acceptance without backlog entry
    backlog_ids = {i.bug_id for i in issues}
    for bid in acc_map:
        if bid not in backlog_ids:
            errors.append(f"BUG_RECONCILE_ACCEPTANCE_ORPHAN_ROW:{bid}")
    return errors


def self_test() -> int:
    good = """## Bug issues (canonical)

### BUG-0001 — Demo
- Status: OPEN
- environment: Windows 10 / framework tests
- steps_to_reproduce: 1. Run validator 2. Observe PASS
- expected: Exit zero
- actual: Exit zero
- evidence_refs: tests/bug_issue_fixtures_test.py
"""
    bad_status = good.replace("OPEN", "TRIAGED")
    bad_field = good.replace(
        "- evidence_refs: tests/bug_issue_fixtures_test.py",
        "- evidence_refs: ",
    )
    err, _ = validate_backlog(bad_status)
    if not any("BUG_VALIDATION_STATUS_INVALID" in e for e in err):
        return _fail("BUG_SELFTEST_FAILED", "expected status error")
    err2, _ = validate_backlog(bad_field)
    if not any("BUG_VALIDATION_FIELD_EMPTY" in e for e in err2):
        return _fail("BUG_SELFTEST_FAILED", "expected field error")
    err0, issues = validate_backlog(good)
    if err0:
        return _fail("BUG_SELFTEST_FAILED", str(err0))
    if len(issues) != 1:
        return _fail("BUG_SELFTEST_FAILED", "issue count")
    print(OK_TAG)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate BUG-xxxx canonical backlog section (DEC-0061).")
    ap.add_argument("--backlog", default="docs/product/backlog.md", help="Path to backlog.md")
    ap.add_argument("--acceptance", default="docs/product/acceptance.md", help="Path to acceptance.md")
    ap.add_argument("--check-acceptance", action="store_true", help="Reconcile bug rows vs backlog")
    ap.add_argument("--print-next-id", action="store_true", help="Print next BUG-#### id and exit 0")
    ap.add_argument("--self-test", action="store_true", help="Internal sanity checks")
    args = ap.parse_args()
    if args.self_test:
        return self_test()

    try:
        backlog_text = open(args.backlog, encoding="utf-8").read()
    except OSError as e:
        return _fail("BUG_VALIDATION_IO_ERROR", str(e))

    if args.print_next_id:
        print(bi.next_bug_id(backlog_text))
        return 0

    errors, _ = validate_backlog(backlog_text)
    if errors:
        for e in errors:
            print(e, file=sys.stderr)
        return 1

    if args.check_acceptance:
        try:
            acc_text = open(args.acceptance, encoding="utf-8").read()
        except OSError as e:
            return _fail("BUG_VALIDATION_IO_ERROR", str(e))
        rerr = reconcile_acceptance(backlog_text, acc_text)
        if rerr:
            for e in rerr:
                print(e, file=sys.stderr)
            return 1

    print(OK_TAG)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
