"""US-0126 OpenCode host operator runbook + consolidated reason-code table +
`--scope=opencode-adapter` parity extension — 12 contract markers.

Markers 1-12 per DEC-0126 §5 / architecture AC-4 table. All markers are
static/grep-based; no live OpenCode runtime probe (vision D10 lock — DQ4).

Layer split (DQ3 — critic NB `ik_us0126_dq3_parity_grep_false_pass` closed):
`--scope=opencode-adapter` parity CLI predicate = byte-identical pair check only;
reason-code table presence + `test_us0126_*` markers = contract-test grep, NOT
parity-CLI predicates. The parity CLI stays byte-only.

AC-10 baseline (DQ4 — critic NB `ik_us0126_research_scope_yagni_markers` closed):
`test_us0126_cursor_docs_not_deleted` uses a deterministic static check vs a
current-kit-inventory baseline (sorted file-name list checked into the repo at
execute time). NOT a frozen pre-US-0126 git snapshot (fragile). NOT a hash
manifest of the entire `.cursor/` directory (over-broad). No git history
dependency; no live OpenCode probe.

Carry-in `ik_us0126_sp_ac1_marker_prose_gap` closed: marker 1 greps the h2 PLUS
AC-1 operator phrases (stock OpenCode TUI/desktop/IDE as UI, `--host` opt-in,
`/connect` keys, kit UX = slash commands + reason codes) — defense in depth
beyond h2-only grep.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RUNBOOK = REPO_ROOT / "docs" / "engineering" / "runbook.md"
RUNBOOK_TEMPLATE = REPO_ROOT / "template" / "docs" / "engineering" / "runbook.md"
README_ROOT = REPO_ROOT / "README.md"
README_ITS_MAGIC = REPO_ROOT / "its_magic" / "README.md"
README_ITS_MAGIC_TEMPLATE = REPO_ROOT / "template" / "its_magic" / "README.md"
PARITY_SCRIPT = REPO_ROOT / "scripts" / "check_intake_template_parity.py"
MANIFEST = REPO_ROOT / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
MANIFEST_TEMPLATE = REPO_ROOT / "template" / "docs" / "engineering" / "context" / "installer-owned-paths.manifest"
TESTS_DIR = REPO_ROOT / "tests"
CURSOR_COMMANDS_DIR = REPO_ROOT / ".cursor" / "commands"
CURSOR_AGENTS_DIR = REPO_ROOT / ".cursor" / "agents"

RUNBOOK_H2 = "## OpenCode host operator runbook (US-0126)"
README_H3 = "### OpenCode host operator runbook (US-0126)"

AC1_OPERATOR_PHRASES = (
    "stock OpenCode TUI",
    "desktop",
    "IDE",
    "--host opencode",
    "--host both",
    "/connect",
    "slash commands",
    "reason codes",
)

REASON_CODES = (
    "OPENCODE_PLUGIN_SPAWN_UNSUPPORTED",
    "OPENCODE_SUBTASK_IGNORED",
    "OPENCODE_HEADLESS_UNSUPPORTED",
    "OPENCODE_DRIVER_INVOKE_FAILED",
    "INSTALL_HOST_INVALID",
    "OPENCODE_ORPHANED_BY_CLEAN_CURSOR",
    "OPENCODE_STALE_BY_UPGRADE_CURSOR",
    "CURSOR_ORPHANED_BY_CLEAN_OPENCODE",
    "CURSOR_STALE_BY_UPGRADE_OPENCODE",
    "AUTO_ORCHESTRATOR_PHASE_EXECUTION",
    "PHASE_ROLE_MISMATCH",
    "NATIVE_CHAIN_UNAVAILABLE",
    "INTAKE_PERSISTENCE_BLOCKED",
    "INTAKE_REQUIRED_TOPIC_MISSING",
    "BUG_ISSUE_VALIDATION_FAILED",
)

DOD_PHRASES = (
    "fresh `its-magic --host opencode` install",
    "distinct sessions",
    "refuse writes on non-zero exit",
)

DEFAULT_HOST_PHRASES = (
    "Default install is cursor-only",
    "--host opencode",
    "--host both",
)

OUT_OF_SCOPE_ITEMS = (
    "standalone runtime",
    "OpenCode fork",
    "VS Code contrib rewrite",
    "Caveman",
    "Cursor browser as primary UAT",
)

CURSOR_KIT_INVENTORY = (
    (
        ".cursor/commands",
        (
            "architecture.md", "ask.md", "auto.md", "closure.md", "discovery.md",
            "execute.md", "intake.md", "map-codebase.md", "memory-audit.md",
            "milestone-complete.md", "milestone-start.md", "pause.md",
            "phase-context.md", "plan-verify.md", "qa.md", "quick.md",
            "refresh-context.md", "release.md", "research.md", "resume.md",
            "security-review.md", "sovereign-critic.md", "sprint-plan.md",
            "status-reconcile.md", "verify-work.md",
        ),
    ),
    (
        ".cursor/agents",
        (
            "curator.mdc", "dev.mdc", "po.mdc", "qa.mdc", "release.mdc",
            "security.mdc", "tech-lead.mdc",
        ),
    ),
)

DEC_PATTERN = re.compile(r"\bDEC-\d{4}\b")


def _section(text, start_marker, stop_pred):
    lines = text.splitlines()
    out = []
    started = False
    for line in lines:
        if not started:
            if start_marker in line:
                started = True
            continue
        if stop_pred(line):
            break
        out.append(line)
    return "\n".join(out)


def _read(path):
    return path.read_text(encoding="utf-8")


def test_us0126_runbook_section_present():
    """Marker 1 (AC-1): grep runbook + template for h2 PLUS AC-1 operator phrases."""
    for path in (RUNBOOK, RUNBOOK_TEMPLATE):
        text = _read(path)
        assert RUNBOOK_H2 in text, f"{path}: missing h2 {RUNBOOK_H2!r}"
        section = _section(
            text, RUNBOOK_H2,
            lambda l: l.startswith("## ") and RUNBOOK_H2 not in l,
        )
        for phrase in AC1_OPERATOR_PHRASES:
            assert phrase in section, (
                f"{path}: AC-1 operator phrase {phrase!r} missing from US-0126 section"
            )


def test_us0126_reason_code_catalog_present():
    """Marker 2 (AC-2): grep runbook for each code; assert fail-closed action;
    NO OPENCODE_VALIDATOR_FAILED wrapper."""
    text = _read(RUNBOOK)
    section = _section(
        text, RUNBOOK_H2,
        lambda l: l.startswith("## ") and RUNBOOK_H2 not in l,
    )
    for code in REASON_CODES:
        assert code in section, f"reason code {code!r} missing from runbook US-0126 section"
    fail_closed_count = section.count("fail closed")
    assert fail_closed_count >= len(REASON_CODES), (
        f"expected >= {len(REASON_CODES)} 'fail closed' occurrences; got {fail_closed_count}"
    )
    assert "OPENCODE_VALIDATOR_FAILED" not in section, (
        "OPENCODE_VALIDATOR_FAILED wrapper resurrected (DEC-0125 DQ7 violation)"
    )


def test_us0126_parity_scope_opencode_adapter():
    """Marker 3 (AC-3): run parity CLI --scope=opencode-adapter; assert exit 0."""
    proc = subprocess.run(
        [sys.executable, str(PARITY_SCRIPT), "--scope", "opencode-adapter"],
        capture_output=True, text=True, cwd=str(REPO_ROOT),
    )
    assert proc.returncode == 0, (
        f"parity --scope=opencode-adapter failed rc={proc.returncode}: "
        f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
    )
    assert "[INTAKE_TEMPLATE_PARITY_OK] scope=opencode-adapter" in proc.stdout, (
        f"parity OK banner missing: {proc.stdout!r}"
    )


def test_us0126_test_marker_checklist():
    """Marker 4 (AC-4): grep tests/ for test_us0121_*..test_us0125_* markers."""
    for story in ("us0121", "us0122", "us0123", "us0124", "us0125"):
        pattern = f"def test_{story}_"
        found = False
        for py in TESTS_DIR.glob("*.py"):
            text = py.read_text(encoding="utf-8")
            if pattern in text:
                found = True
                break
        assert found, f"no {pattern!r} marker found in tests/*.py"


def test_us0126_readme_no_dec_leak():
    """Marker 5 (AC-5a): US-0071 sanitization — no DEC-xxxx in US-0126 README blurb."""
    for path in (README_ROOT, README_ITS_MAGIC, README_ITS_MAGIC_TEMPLATE):
        text = _read(path)
        section = _section(
            text, README_H3,
            lambda l: l.startswith("### ") and README_H3 not in l,
        )
        assert section.strip(), f"{path}: US-0126 README blurb empty"
        leaks = DEC_PATTERN.findall(section)
        assert not leaks, f"{path}: DEC ids leaked into US-0126 README operator prose: {leaks}"


def test_us0126_runbook_no_dec_leak():
    """Marker 6 (AC-5b): US-0071 sanitization — no DEC-xxxx in runbook US-0126
    operator prose (cross-references allowed only in Boundaries/evidence
    subsections, not in operator prose before `### Boundaries`)."""
    for path in (RUNBOOK, RUNBOOK_TEMPLATE):
        text = _read(path)
        full_section = _section(
            text, RUNBOOK_H2,
            lambda l: l.startswith("## ") and RUNBOOK_H2 not in l,
        )
        assert full_section.strip(), f"{path}: US-0126 runbook section empty"
        # Operator prose = content before the Boundaries subsection.
        boundaries_idx = full_section.find("### Boundaries")
        if boundaries_idx == -1:
            operator_prose = full_section
        else:
            operator_prose = full_section[:boundaries_idx]
        leaks = DEC_PATTERN.findall(operator_prose)
        assert not leaks, (
            f"{path}: DEC ids leaked into US-0126 runbook operator prose: {leaks}"
        )


def test_us0126_program_dod_documented():
    """Marker 7 (AC-6): grep runbook for DoD sentence key phrases (DQ5 lock)."""
    text = _read(RUNBOOK)
    section = _section(
        text, RUNBOOK_H2,
        lambda l: l.startswith("## ") and RUNBOOK_H2 not in l,
    )
    for phrase in DOD_PHRASES:
        assert phrase in section, f"DoD phrase {phrase!r} missing from runbook US-0126 section"


def test_us0126_default_host_reminder():
    """Marker 8 (AC-7): grep runbook + README for default-host phrases (DQ6 lock)."""
    paths = (RUNBOOK, RUNBOOK_TEMPLATE, README_ROOT, README_ITS_MAGIC, README_ITS_MAGIC_TEMPLATE)
    for path in paths:
        text = _read(path)
        for phrase in DEFAULT_HOST_PHRASES:
            assert phrase in text, f"{path}: default-host phrase {phrase!r} missing"


def test_us0126_out_of_scope_listed():
    """Marker 9 (AC-8): grep runbook + README for each excluded item (DQ7 lock)."""
    paths = (RUNBOOK, RUNBOOK_TEMPLATE, README_ROOT, README_ITS_MAGIC, README_ITS_MAGIC_TEMPLATE)
    for path in paths:
        text = _read(path)
        for item in OUT_OF_SCOPE_ITEMS:
            assert item in text, f"{path}: out-of-scope item {item!r} missing"


def test_us0126_template_doc_parity():
    """Marker 10 (AC-9): manifest active<->template byte-identical (DQ8 — no new
    entries) + runbook active<->template byte-identical."""
    for active, tpl in (
        (MANIFEST, MANIFEST_TEMPLATE),
        (RUNBOOK, RUNBOOK_TEMPLATE),
    ):
        assert active.is_file() and tpl.is_file(), (
            f"missing file: {active} or {tpl}"
        )
        ba = active.read_bytes()
        bt = tpl.read_bytes()
        assert ba == bt, (
            f"{active.name} active<->template not byte-identical: {len(ba)}b vs {len(bt)}b"
        )


def test_us0126_cursor_docs_not_deleted():
    """Marker 11 (AC-10): deterministic static check — .cursor/commands/ and
    .cursor/agents/ still exist with expected file names vs current kit inventory
    baseline (captured at execute time; NOT a frozen git snapshot)."""
    assert CURSOR_COMMANDS_DIR.is_dir(), ".cursor/commands/ directory missing"
    assert CURSOR_AGENTS_DIR.is_dir(), ".cursor/agents/ directory missing"
    for rel_dir, expected_names in CURSOR_KIT_INVENTORY:
        if rel_dir == ".cursor/commands":
            d = CURSOR_COMMANDS_DIR
        else:
            d = CURSOR_AGENTS_DIR
        actual = sorted(p.name for p in d.iterdir() if p.is_file())
        for name in expected_names:
            assert name in actual, f"{rel_dir}: expected file {name!r} missing; actual={actual}"


def test_us0126_prior_story_markers_present():
    """Marker 12 (AC-4 aggregate): grep tests/ for test_us0121_*..test_us0125_*
    markers (aggregate prior-story marker presence — defense in depth)."""
    for story in ("us0121", "us0122", "us0123", "us0124", "us0125"):
        pattern = f"def test_{story}_"
        count = 0
        for py in TESTS_DIR.glob("*.py"):
            text = py.read_text(encoding="utf-8")
            count += text.count(pattern)
        assert count >= 1, f"no {pattern!r} markers found in tests/*.py (count={count})"
