#!/usr/bin/env python3
"""Fix the duplicate US-0114 heading in backlog.md by replacing it with US-0117."""

import sys
import re

def main():
    # Read the file
    with open('docs/product/backlog.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find all lines containing "## US-0114"
    us_0114_lines = []
    for i, line in enumerate(lines):
        if '## US-0114' in line:
            us_0114_lines.append((i, line.strip()))
    
    print(f'Found US-0114 at lines: {[line[0]+1 for line in us_0114_lines]}')
    print(f'Content: {us_0114_lines}')
    
    if len(us_0114_lines) < 2:
        print('ERROR: Expected at least 2 US-0114 headings (the correct one and the duplicate)')
        sys.exit(1)
    
    # The second US-0114 is the duplicate that should be US-0117
    duplicate_line_idx = us_0114_lines[1][0]
    print(f'Duplicate US-0114 at line {duplicate_line_idx + 1}')
    
    # Find the end of this block (next "## US-" heading or end of file)
    block_end_idx = duplicate_line_idx + 1
    for i in range(duplicate_line_idx + 1, len(lines)):
        if lines[i].strip().startswith('## US-'):
            block_end_idx = i
            break
    
    print(f'Block ends before line {block_end_idx + 1}')
    
    # New US-0117 content
    new_block = [
        '## US-0117 — Phase & role governance operator documentation in framework README\n',
        '- user_visible: true\n',
        '- Title: Add operator-facing feature guides and scratchpad reference for Phase & role governance features\n',
        '- Summary: Document US-0069-0089 and US-0092 (phase/role enforcement, phase selection policy, metadata sanitization, context slimming, scratchpad delivery, codebase map, delegation, env file, bug queue, auto quiet, caveman mode, input compression, delivery confirmation, full-autonomy mode) in the framework README with operator-ready descriptions.\n',
        '- Priority: P1\n',
        '- Status: OPEN\n',
        '- Decomposition (US-0051):\n',
        '  - **Split decision**: operator re-scope at intake broadens US-0113 from single-sovereign family → 5-story decomposition by functional family. **US-0117 = Phase & role governance family** (US-0069-0089, US-0092; ~22 features total).\n',
        '  - **Rationale**: these features share a common theme (phase orchestration + role enforcement + metadata/context governance + automation modes) and are distinct from sovereign orchestration (US-0113), release/distribution (US-0114), integration/observability (US-0115), or dev environment/auto-orchestration (US-0116).\n',
        '- related_us: US-0069, US-0070, US-0071, US-0072, US-0073, US-0074, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090, US-0092, US-0091, US-0097, US-0113, US-0114, US-0115, US-0116\n',
        '- intake_notes (2026-07-03, PO, cursor-20260703-US0117-intake): Decomposition evaluator → 5 stories by functional family. **Status: OPEN** per US-0045.\n',
        '\n',
    ]
    
    # Replace the block
    new_lines = lines[:duplicate_line_idx] + new_block + lines[block_end_idx:]
    
    # Write back
    with open('docs/product/backlog.md', 'w', encoding='utf-8') as f:
        f.writelines(new_lines)
    
    print(f'Successfully replaced duplicate US-0114 with US-0117 (lines {duplicate_line_idx+1}-{block_end_idx})')

if __name__ == '__main__':
    main()
