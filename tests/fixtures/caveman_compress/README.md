# tests/fixtures/caveman_compress/

Fixture classes for US-0090 / DEC-0073 safe-mode input-side compressor
contract tests. One directory per class; fixture class #2 has 9
sub-fixtures (one per DEC-0072 §4 zone); fixture class #3 has one
sub-fixture per DEC-0073 §4.1 deny entry-class.

| # | Directory | Class | Driven by |
|---|-----------|-------|-----------|
| 1 | `01_whitespace_baseline/` | Whitespace + LF + trailing-space canonicalization | AC-6 |
| 2 | `02_literal_region/` | Literal-region preservation, 9 zones | AC-6 |
| 3 | `03_deny_list/` | Deny-list refusal per §4.1 class | AC-6 |
| 4 | `04_scope_violation/` | Scope violation (unresolvable profile) | AC-6 |
| 5 | `05_idempotency/` | `compress(compress(f)) == compress(f)` | AC-6 |
| 6 | `06_mode_disabled/` | Mode gate disabled | AC-6 |
| 7 | `07_original_missing/` | Orphan sidecar detection | AC-6 |
| 8 | `08_flag_conflict/` | Incompatible CLI flag pairs | AC-6 |

Fixtures are deliberately small and text-only; binary classes in 03_deny_list
are represented by file-extension stubs that the script refuses by glob match
(no need for actual binary bytes).
