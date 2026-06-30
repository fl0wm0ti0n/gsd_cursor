#!/usr/bin/env python3
import pathlib

p = pathlib.Path(r'handoffs\release_notes.md').resolve()
text = p.read_text('utf-8')
lines = text.split('\n')

# Find all '## Latest operator summary' section lines and replace them with S0109 refs
in_operator_section = False
new_lines = []
skip_until_next_h2 = False

i = 0
while i < len(lines):
    line = lines[i]
    if line.startswith('## Latest operator summary'):
        in_operator_section = True
        # Replace all 4 bullet items in this section
        new_lines.append(line)
        new_lines.append('')
        new_lines.append('- **Start command:** Last finalized sprint **`S0109`**: `pytest tests/us0109_contract_test.py -v` -- refer to `## Run` in')
        new_lines.append('  `handoffs/releases/S0109-release-notes.md`.')
        new_lines.append('- **Endpoint + port:** N/A (release documentation layer) -- refer to `## Connect` in')
        new_lines.append('  `handoffs/releases/S0109-release-notes.md`.')
        new_lines.append('- **Verification steps + health signal:** Refer to `## Verify` in')
        new_lines.append('  `handoffs/releases/S0109-release-notes.md`.')
        new_lines.append('- **Credentials source refs (sanitized):** Refer to `## Credentials` in')
        new_lines.append('  `handoffs/releases/S0109-release-notes.md` (env-ref only).')
        new_lines.append('- **Known issues:** Refer to `## Known Issues` in')
        new_lines.append('  `handoffs/releases/S0109-release-notes.md`.')
        new_lines.append('')
        # Skip original content until next ## heading
        i += 1
        while i < len(lines) and not lines[i].startswith('## '):
            i += 1
        continue
    else:
        new_lines.append(line)
    i += 1

result = '\n'.join(new_lines)

# Also fix any remaining broken references like S0107 when they should be S0109 in the "Last finalized sprint" line
result = result.replace('Last finalized sprint **`S0107`**: `pytest tests/us0109_contract_test.py -v`', 
                       'Last finalized sprint **`S0109`**: `pytest tests/us0109_contract_test.py -v`')
result = result.replace('Last finalized sprint **`S0107`**: `pytest -k us0107 tests/us0107_contract_test.py -v`',
                       'Last finalized sprint **`S0109`**: `pytest tests/us0109_contract_test.py -v`')

p.write_text(result, 'utf-8')
print(f"OK - file now {len(result.split(chr(10)))} lines")
