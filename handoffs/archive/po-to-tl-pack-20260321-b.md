# PO to TL archive pack (2026-03-21)

- Rollover trigger: `PO_TO_TL_HOT_MAX_LINES=800, PO_TO_TL_HOT_MAX_SECTIONS=60`
- Source: `handoffs/po_to_tl.md`
- Archived units (oldest first, contiguous prefix): 1
- Retained units in hot file: 23
- First archived heading: `## Discovery Addendum — US-0074 (Baseline Regression Cleanup: Homebrew + TEST_COMMAND)`
- Last archived heading: `## Discovery Addendum — US-0074 (Baseline Regression Cleanup: Homebrew + TEST_COMMAND)`
- Verification tuple (mandatory):
  - archived_body_lines=45
  - retained_body_lines=768

---

## Discovery Addendum — US-0074 (Baseline Regression Cleanup: Homebrew + TEST_COMMAND)

### Discovery outcome (PO)

- **Problem statement**: In-scope sprint QA (e.g. **S0051** / **US-0072**) passed while
  the consolidated baseline runner still reported **four** failing rows, explicitly
  classified as known debt under **`US-0074`** in `sprints/S0051/qa-findings.md`.
- **Locked scope** (no creep):
  1. `Homebrew stable formula URL uses npm version tag`
  2. `Homebrew stable formula version matches npm version`
  3. `Installer bootstraps TEST_COMMAND for detectable stack`
  4. `CLI missing install bootstraps TEST_COMMAND for detectable stack`
- **Product intent**: Operators should see a **fully green** `tests/run-tests.*`
  baseline for these checks after this story; they should not remain perpetual
  “out of scope” footnotes in unrelated QA reports.
- **Canonical version line**: Treat **`package.json` / npm** as the authoritative
  semver for the Homebrew stable formula’s tag and `version` field; research must
  confirm how release scripts bump npm vs formula and close any ordering/drift gap
  the tests encode.
- **`TEST_COMMAND` bootstrap**: Research and architecture must align installer
  (`installer.ps1`, `installer.sh`, `installer.py`) and CLI (`bin/its-magic.js`)
  missing-install behavior with **`DEC-0046`** / **`US-0063`** — deterministic
  detection, user-override precedence, and no false-green tests.

### TL guidance — `/research` next

- Start from **`R-0051`** and extend with per-check root-cause notes, owning file
  paths, and any publish-pipeline touchpoints (npm, GitHub tag, formula update).
- Produce a minimal **fix ordering** recommendation (e.g. version sync before
  bootstrap assertions if tests are order-sensitive).
- Explicit **active + `template/`** parity requirements in the research notes so
  `/architecture` and `/execute` do not split behavior.
- **Out of scope**: triad hot-surface / **DEC-0054**, scratchpad Model B /
  **DEC-0055**, and new feature work beyond the four baseline asserts.

### Artifacts to read first

- `sprints/S0051/qa-findings.md` (classification block)
- `tests/report.md` (latest failing row evidence)
- `packaging/homebrew/its-magic.rb`, `package.json`
- `docs/engineering/runbook.md`, `template/docs/engineering/runbook.md`
- `installer.ps1`, `installer.sh`, `installer.py`, `bin/its-magic.js`

---

