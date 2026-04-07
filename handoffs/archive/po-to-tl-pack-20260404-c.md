# PO to TL archive pack (2026-04-04)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 46
- First archived heading: `## PO → TL bug intake — **BUG-0008** (2026-04-04)`
- Last archived heading: `## PO → TL bug intake — **BUG-0008** (2026-04-04)`
- Verification tuple (mandatory):
  - archived_body_lines=8
  - retained_body_lines=800

---

## PO → TL bug intake — **BUG-0008** (2026-04-04)

- **Defect**: CRLF **`installer-owned-paths.manifest`** in npm global install → POSIX **`awk`** never matches **`[install_include_paths]`** → **`[INSTALL_MANIFEST_ERROR] install_include_paths section is empty`** on Linux (**repro**: **`its-magic@0.1.2-40`**, **`cat -A`** shows **`^M$`**).
- **In-repo fix (pending QA/release)**: **`installer.sh`** strip **`\\r`** before section parse; **`.gitattributes`** **`*.manifest text eol=lf`**; **`guard_installer_publish.py`** (+ **`template/scripts/`** parity) rejects CR in manifests; **`tests/installer_manifest_crlf_bug0008_test.py`** harness **26P2**; **`installer.ps1`** **`TrimEnd('`r')`** in **`Get-ManifestSection`**.
- **Evidence**: **`handoffs/intake_evidence/BUG-0008-intake-20260404.json`**; **`docs/engineering/research.md`** **`R-0069`**. Next: **`/discovery`** or **`/sprint-plan`** for **BUG-0008** (portfolio **OPEN**).

---

