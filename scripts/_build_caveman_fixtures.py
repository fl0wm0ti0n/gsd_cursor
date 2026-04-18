#!/usr/bin/env python3
"""One-shot generator for tests/fixtures/caveman_compress/ trees.

Run during /execute; the produced tree is the source-of-truth for the
T-005 contract subtests. Re-running is idempotent (byte-stable).
"""
from __future__ import annotations

from pathlib import Path
import sys

REPO = Path(__file__).resolve().parent.parent
ROOT = REPO / "tests" / "fixtures" / "caveman_compress"


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content.encode("utf-8"))


# ---------------- Class 01: whitespace baseline ----------------
write(ROOT / "01_whitespace_baseline" / "input.txt",
      "alpha\n\n\n\nbeta   \n\n\n\ngamma\t\t\n")
write(ROOT / "01_whitespace_baseline" / "expected.txt",
      "alpha\n\nbeta\n\ngamma\n")

# ---------------- Class 02: literal-region preservation ----------------
# 9 zones from DEC-0072 §4. Each fixture's content must pass safe-mode
# compression unchanged (byte-stable; no collapsible blank-line run; no
# trailing whitespace on non-fence lines).
write(ROOT / "02_literal_region" / "zone_01_fenced_code.md",
      "# Zone 1 — fenced code\n\n```python\nx = 1\n   return   x\n```\n")
write(ROOT / "02_literal_region" / "zone_02_paths.md",
      "# Zone 2 — paths\n\nSee `docs/engineering/runbook.md`.\n")
write(ROOT / "02_literal_region" / "zone_03_ac_checklists.md",
      "# Zone 3 — AC checklists\n\n- [ ] AC-1\n- [x] AC-2\n")
write(ROOT / "02_literal_region" / "zone_04_reason_codes.md",
      "# Zone 4 — reason codes\n\n`CAVEMAN_COMPRESS_DENY_HIT`\n")
write(ROOT / "02_literal_region" / "zone_05_ids.md",
      "# Zone 5 — IDs\n\nUS-0090, DEC-0073, BUG-0003, S0076, T-001.\n")
write(ROOT / "02_literal_region" / "zone_06_contract_markers.md",
      "# Zone 6 — contract markers\n\n`[BUG_VALIDATION_OK]`\n"
      "`[INTAKE_EVIDENCE_VALIDATION_OK]`\n`[SCRATCHPAD_PAIR_OK]`\n")
write(ROOT / "02_literal_region" / "zone_07_strict_proof_tuple.md",
      "# Zone 7 — strict-proof tuple\n\n"
      "orchestrator_run_id=auto-20260418-01\nruntime_proof_id=rp-abc\n"
      "phase_id=execute\nrole=dev\nproof_issued_at=2026-04-18T12:00:00Z\n"
      "proof_ttl_seconds=3600\n"
      "proof_hash=deadbeefcafef00d00000000000000000000000000000000000000000000beef\n")
write(ROOT / "02_literal_region" / "zone_08_isolation_evidence.md",
      "# Zone 8 — isolation evidence\n\n"
      "phase_id=execute\nrole=dev\nfresh_context_marker=true\n"
      "timestamp=2026-04-18T12:00:00Z\nevidence_ref=S0076/T-006\n")
write(ROOT / "02_literal_region" / "zone_09_git_refs.md",
      "# Zone 9 — git refs\n\nHEAD, main, origin/main, tag refs/tags/S0076.\n")

# ---------------- Class 03: deny-list refusal ----------------
# One sub-fixture per §4.1 deny entry class. The script refuses by glob
# match; fixture content is irrelevant for deny behavior, but we populate
# with minimal text so they are real files.
deny_classes = {
    "secrets_dotenv": (".env.example", "KEY=value\n"),
    "intake_evidence": (
        "intake_evidence_sample.json",
        "{\"story_ref\":\"US-0090\"}\n",
    ),
    "product_authority_backlog": ("backlog-sample.md", "# backlog\n"),
    "product_authority_acceptance": ("acceptance-sample.md", "# acceptance\n"),
    "engineering_state": ("state-sample.md", "# state\n"),
    "engineering_decisions": ("decisions-sample.md", "# decisions\n"),
    "decisions_dec": ("DEC-9999-sample.md", "# DEC-9999\n"),
    "sprint_lifecycle_planverify": (
        "plan-verify-sample.json",
        "{\"plan_verify_status\":\"PASS\"}\n",
    ),
    "sprint_lifecycle_uat": ("uat-sample.json", "{\"uat\":\"ok\"}\n"),
    "sprint_lifecycle_summary": ("summary-sample.md", "# summary\n"),
    "sprint_lifecycle_qa": ("qa-findings-sample.md", "# qa\n"),
    "sprint_lifecycle_release": ("release-findings-sample.md", "# release\n"),
    "sprint_lifecycle_tasks": ("tasks-sample.md", "# tasks\n"),
    "sprint_lifecycle_sprint": ("sprint-sample.md", "# sprint\n"),
    "publish_package": ("package-sample.json", "{}\n"),
    "publish_installer": ("installer-sample.sh", "#!/bin/sh\n"),
    "publish_workflow": ("ci-sample.yml", "name: ci\n"),
    "publish_hooks": ("hook-sample.py", "# hook\n"),
    "publish_bin": ("its-magic-sample.js", "// bin\n"),
    "publish_homebrew": ("formula-sample.rb", "# brew\n"),
    "contract_rules": ("rule-sample.mdc", "# rule\n"),
    "contract_commands": ("command-sample.md", "# command\n"),
    "contract_skills": ("SKILL-sample.md", "# skill\n"),
    "manifest_parity_manifest": ("manifest-sample.manifest", "# manifest\n"),
    "manifest_release_targets": ("release-targets-sample.json", "{}\n"),
    "manifest_token_parity": ("token-cost-parity-sample.md", "# manifest\n"),
    "binary_png": ("image-sample.png.stub", "stub\n"),
    "binary_jpg": ("image-sample.jpg.stub", "stub\n"),
    "binary_pdf": ("doc-sample.pdf.stub", "stub\n"),
    "binary_archive": ("archive-sample.zip.stub", "stub\n"),
    "binary_exec": ("bin-sample.exe.stub", "stub\n"),
    "binary_font": ("font-sample.woff.stub", "stub\n"),
    "binary_media": ("audio-sample.mp3.stub", "stub\n"),
}
for class_name, (fname, body) in deny_classes.items():
    write(ROOT / "03_deny_list" / class_name / fname, body)

# ---------------- Class 04: scope violation ----------------
write(ROOT / "04_scope_violation" / "README.md",
      "# Scope violation fixtures\n\nDrives `CAVEMAN_COMPRESS_SCOPE_UNKNOWN_PROFILE`\n"
      "by setting `CAVEMAN_FILE_SCOPE=does-not-exist`.\n")

# ---------------- Class 05: idempotency ----------------
write(ROOT / "05_idempotency" / "input.txt",
      "one\n\n\n\ntwo  \n\nthree\n")
write(ROOT / "05_idempotency" / "expected.txt",
      "one\n\ntwo\n\nthree\n")

# ---------------- Class 06: mode disabled ----------------
write(ROOT / "06_mode_disabled" / "README.md",
      "# Mode-disabled fixture\n\n"
      "Drives `CAVEMAN_COMPRESS_MODE_DISABLED` by omitting\n"
      "`CAVEMAN_COMPRESS_INPUT=1` from the scratchpad.\n")

# ---------------- Class 07: original missing ----------------
write(ROOT / "07_original_missing" / "README.md",
      "# Original-missing fixture\n\n"
      "Drives `CAVEMAN_COMPRESS_ORIGINAL_MISSING` via `--verify-originals`\n"
      "when a sidecar has no target.\n")

# ---------------- Class 08: flag conflict ----------------
write(ROOT / "08_flag_conflict" / "README.md",
      "# Flag-conflict fixture\n\n"
      "Drives `CAVEMAN_COMPRESS_FLAG_CONFLICT` via mutually-exclusive\n"
      "CLI flag pairs (--dry-run + --write; --write + --report;\n"
      "--write + --verify-originals; unknown flag token).\n")

# Manifest of fixtures for T-005 subtests to enumerate deterministically.
manifest_lines = []
for p in sorted(ROOT.rglob("*")):
    if p.is_file():
        manifest_lines.append(str(p.relative_to(ROOT)).replace("\\", "/"))
(ROOT / "MANIFEST.txt").write_bytes(("\n".join(manifest_lines) + "\n").encode("utf-8"))

print(f"Wrote {len(manifest_lines)} fixture files under {ROOT}")
