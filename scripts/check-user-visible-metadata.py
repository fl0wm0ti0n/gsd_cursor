#!/usr/bin/env python3
"""
User-visible internal metadata guard (US-0071 / DEC-0053).

Scans operator-facing software deliverables only (see runbook). Forbidden
planning-shaped tokens in user-visible string channels:

  US-[0-9]{4}, DEC-[0-9]{4}, R-[0-9]{4}

Exit 0: no violations. Exit 1: USER_VISIBLE_INTERNAL_METADATA_DETECTED.
Exit 2: METADATA_SANITIZATION_POLICY_MISSING or invocation error.
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
import tokenize
from pathlib import Path
from typing import Iterable, Iterator, List, NamedTuple, Optional, Tuple

FORBIDDEN = (
    (re.compile(r"US-[0-9]{4}"), "US"),
    (re.compile(r"DEC-[0-9]{4}"), "DEC"),
    (re.compile(r"R-[0-9]{4}"), "R"),
)


class Violation(NamedTuple):
    path: str
    line: int
    column: int
    token_class: str
    matched_text: str


def _repo_root(cli_root: Optional[str]) -> Path:
    if cli_root:
        return Path(cli_root).resolve()
    return Path(__file__).resolve().parent.parent


def _iter_scan_files(root: Path) -> Iterator[Path]:
    """Deterministic inclusive scan roots (DEC-0053 / runbook)."""
    candidates: List[Path] = []
    for rel in (
        "bin",
        "installer.py",
        "installer.ps1",
        "installer.sh",
        "packaging",
        "scripts/validate-and-push.ps1",
        "scripts/validate-and-push.sh",
    ):
        p = root / rel
        if p.is_file():
            candidates.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and f.suffix.lower() in (
                    ".js",
                    ".py",
                    ".ps1",
                    ".sh",
                    ".bash",
                ):
                    candidates.append(f)
    for path in sorted(set(candidates), key=lambda x: str(x).replace("\\", "/")):
        yield path


def _violations_python(path: Path, text: str) -> List[Violation]:
    out: List[Violation] = []
    try:
        tokens = tokenize.generate_tokens(io.StringIO(text).readline)
        for tok in tokens:
            if tok.type != tokenize.STRING:
                continue
            for rx, label in FORBIDDEN:
                m = rx.search(tok.string)
                if m:
                    line = tok.start[0]
                    col = tok.start[1] + m.start() + 1
                    out.append(
                        Violation(
                            path=str(path),
                            line=line,
                            column=col,
                            token_class=label,
                            matched_text=m.group(0),
                        )
                    )
                    break
    except tokenize.TokenError:
        out.append(
            Violation(
                path=str(path),
                line=1,
                column=1,
                token_class="PARSE",
                matched_text="(tokenize failed)",
            )
        )
    return out


def _iter_js_string_chunks(text: str) -> Iterable[Tuple[int, str]]:
    """
    Yield (start_line, chunk) for JavaScript string/template literal contents.
    Skips line and block comments; does not execute ${} inside templates.
    """
    n = len(text)
    i = 0
    line = 1

    def adv() -> None:
        nonlocal i, line
        if i < n and text[i] == "\n":
            line += 1
        i += 1

    while i < n:
        c = text[i]
        if c == "/" and i + 1 < n:
            if text[i + 1] == "/":
                i += 2
                while i < n and text[i] != "\n":
                    i += 1
                continue
            if text[i + 1] == "*":
                i += 2
                while i + 1 < n and not (text[i] == "*" and text[i + 1] == "/"):
                    adv()
                if i + 1 < n:
                    i += 2
                continue
        if c in "\"'":
            quote = c
            start_line = line
            adv()
            buf: List[str] = []
            while i < n:
                if text[i] == "\\" and i + 1 < n:
                    buf.append(text[i : i + 2])
                    i += 2
                    if buf[-1][0] == "\\" and buf[-1][1] == "n":
                        line += 1
                    continue
                if text[i] == quote:
                    adv()
                    yield start_line, "".join(buf)
                    break
                if text[i] == "\n" and quote != "'":
                    buf.append("\n")
                    adv()
                    continue
                buf.append(text[i])
                adv()
            continue
        if c == "`":
            start_line = line
            adv()
            buf = []
            depth = 1
            while i < n and depth > 0:
                if text[i] == "\\" and i + 1 < n:
                    buf.append(text[i : i + 2])
                    i += 2
                    continue
                if text[i] == "`":
                    adv()
                    depth -= 1
                    if depth == 0:
                        yield start_line, "".join(buf)
                    continue
                if text[i] == "$" and i + 1 < n and text[i + 1] == "{":
                    adv()
                    adv()
                    nested = 1
                    while i < n and nested > 0:
                        if text[i] == "{":
                            nested += 1
                        elif text[i] == "}":
                            nested -= 1
                        adv()
                    continue
                if text[i] == "\n":
                    line += 1
                buf.append(text[i])
                adv()
            continue
        adv()


def _violations_js(path: Path, text: str) -> List[Violation]:
    out: List[Violation] = []
    for start_line, chunk in _iter_js_string_chunks(text):
        for rx, label in FORBIDDEN:
            m = rx.search(chunk)
            if m:
                out.append(
                    Violation(
                        path=str(path),
                        line=start_line,
                        column=0,
                        token_class=label,
                        matched_text=m.group(0),
                    )
                )
                break
    return out


def _iter_shell_string_chunks(text: str) -> Iterable[Tuple[int, str]]:
    """POSIX-ish: double/single quoted segments; skip # comments outside quotes."""
    n = len(text)
    i = 0
    line = 1

    def adv() -> None:
        nonlocal i, line
        if i < n and text[i] == "\n":
            line += 1
        i += 1

    state = "CODE"
    while i < n:
        c = text[i]
        if state == "CODE":
            if c == "#":
                while i < n and text[i] != "\n":
                    adv()
                continue
            if c == "'":
                start_line = line
                adv()
                buf: List[str] = []
                while i < n:
                    if text[i] == "'":
                        adv()
                        yield start_line, "".join(buf)
                        break
                    if text[i] == "\n":
                        line += 1
                    buf.append(text[i])
                    adv()
                continue
            if c == '"':
                start_line = line
                adv()
                buf = []
                while i < n:
                    if text[i] == "\\" and i + 1 < n:
                        buf.append(text[i : i + 2])
                        i += 2
                        continue
                    if text[i] == '"':
                        adv()
                        yield start_line, "".join(buf)
                        break
                    if text[i] == "\n":
                        line += 1
                    buf.append(text[i])
                    adv()
                continue
            adv()
            continue


def _violations_shell(path: Path, text: str) -> List[Violation]:
    out: List[Violation] = []
    for start_line, chunk in _iter_shell_string_chunks(text):
        for rx, label in FORBIDDEN:
            m = rx.search(chunk)
            if m:
                out.append(
                    Violation(
                        path=str(path),
                        line=start_line,
                        column=0,
                        token_class=label,
                        matched_text=m.group(0),
                    )
                )
                break
    return out


def _iter_ps_string_chunks(text: str) -> Iterable[Tuple[int, str]]:
    """
    PowerShell-ish: # line comments, <# #> blocks, " and ' strings,
    @" "@ and @' '@ here-strings (no nesting).
    """
    n = len(text)
    i = 0
    line = 1

    def adv() -> None:
        nonlocal i, line
        if i < n and text[i] == "\n":
            line += 1
        i += 1

    while i < n:
        c = text[i]
        if c == "<" and i + 1 < n and text[i + 1] == "#":
            i += 2
            while i + 1 < n and not (text[i] == "#" and text[i + 1] == ">"):
                adv()
            if i + 1 < n:
                i += 2
            continue
        if c == "#":
            while i < n and text[i] != "\n":
                adv()
            continue
        if c in "\"'":
            quote = c
            start_line = line
            adv()
            buf: List[str] = []
            while i < n:
                if quote == '"' and text[i] == "`" and i + 1 < n:
                    buf.append(text[i : i + 2])
                    i += 2
                    continue
                if text[i] == quote:
                    if quote == "'" and i + 1 < n and text[i + 1] == "'":
                        buf.append("''")
                        i += 2
                        continue
                    adv()
                    yield start_line, "".join(buf)
                    break
                if text[i] == "\n" and quote == "'":
                    buf.append("\n")
                    adv()
                    continue
                buf.append(text[i])
                adv()
            continue
        if c == "@" and i + 1 < n and text[i + 1] == '"':
            start_line = line
            i += 2
            buf = []
            while i + 1 < n:
                if text[i] == '"' and text[i + 1] == '"':
                    adv()
                    adv()
                    break
                if text[i] == "\n":
                    line += 1
                buf.append(text[i])
                adv()
            else:
                break
            yield start_line, "".join(buf)
            continue
        if c == "@" and i + 1 < n and text[i + 1] == "'":
            start_line = line
            i += 2
            buf = []
            while i + 1 < n:
                if text[i] == "'" and text[i + 1] == "'":
                    adv()
                    adv()
                    break
                buf.append(text[i])
                adv()
            else:
                break
            yield start_line, "".join(buf)
            continue
        adv()


def _violations_ps1(path: Path, text: str) -> List[Violation]:
    out: List[Violation] = []
    for start_line, chunk in _iter_ps_string_chunks(text):
        for rx, label in FORBIDDEN:
            m = rx.search(chunk)
            if m:
                out.append(
                    Violation(
                        path=str(path),
                        line=start_line,
                        column=0,
                        token_class=label,
                        matched_text=m.group(0),
                    )
                )
                break
    return out


def scan_file(path: Path) -> List[Violation]:
    raw = path.read_bytes()
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        text = raw.decode("utf-8", errors="replace")

    suffix = path.suffix.lower()
    if suffix == ".py":
        return _violations_python(path, text)
    if suffix == ".js":
        return _violations_js(path, text)
    if suffix == ".ps1":
        return _violations_ps1(path, text)
    if suffix in (".sh", ".bash"):
        return _violations_shell(path, text)
    return []


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=None, help="Repository root (default: parent of scripts/)")
    ap.add_argument("--json", action="store_true", help="Emit machine-readable report on stdout")
    args = ap.parse_args()
    root = _repo_root(args.repo)
    self_path = Path(__file__).resolve()
    if not self_path.is_file():
        sys.stderr.write(
            "[METADATA_SANITIZATION_POLICY_MISSING] running check script path invalid. "
            "Fix: restore scripts/check-user-visible-metadata.py.\n"
        )
        return 2

    all_v: List[Violation] = []
    for f in _iter_scan_files(root):
        if not f.is_file():
            continue
        all_v.extend(scan_file(f))

    if args.json:
        payload = {
            "reason_code": (
                "USER_VISIBLE_INTERNAL_METADATA_DETECTED" if all_v else "OK"
            ),
            "violations": [v._asdict() for v in all_v],
        }
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif all_v:
        sys.stderr.write(
            "[USER_VISIBLE_INTERNAL_METADATA_DETECTED] Forbidden planning token in "
            "user-visible software surface. Remediation: remove tokens from operator-visible "
            "strings in scanned paths (see docs/engineering/runbook.md — US-0071); keep "
            "traceability in docs/**, .cursor/**, sprint/handoff/decision trees, or non-emitting "
            "source comments per DEC-0053.\n"
        )
        for v in all_v:
            sys.stderr.write(
                f"  evidence_ref={v.path}:{v.line}:{v.column} "
                f"token_class={v.token_class} matched={v.matched_text!r}\n"
            )

    return 1 if all_v else 0


if __name__ == "__main__":
    raise SystemExit(main())
