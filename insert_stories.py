#!/usr/bin/env python3
"""Insert US-0113 through US-0117 into backlog.md after US-0112."""

def main():
    with open('docs/product/backlog.md', 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find where to insert - before the bug section marker
    insert_line = None
    for i, line in enumerate(lines):
        if '**Allocator**' in line and i > 3800:
            insert_line = i
            break
    
    if insert_line is None:
        # Fallback: find line 3894 area
        for i, line in enumerate(lines):
            if line.strip() == '' and i > 3890 and i < 3900:
                insert_line = i
                break
    
    if insert_line is None:
        print("ERROR: Could not find insertion point")
        return
    
    print(f"Inserting at line {insert_line + 1}")
    
    # New content to insert
    new_content = f"""## US-0113 — Sovereign-loop operator documentation in framework README
- Status: OPEN
- user_visible: true
- Title: Add operator documentation for sovereign-loop era features (US-0103–US-0112)
- Summary: Close the operator-documentation gap for the **sovereign-loop era features** — US-0103 (AI Decision Ledger), US-0104 (Cross-Model Adversarial Critic), US-0105 (Sovereign Memory), US-0107 (Drain-Generated Operator Guidance System), US-0108 (Sovereign Loop orchestration), US-0109 (Parallel Development Arbiter), US-0110 (Goal-Based Convergence Loops), US-0111 (Release trigger adapters), US-0112 (Model-catalog example presets). These features currently appear only as catalog one-liners in `its_magic/README.md` with no narrative explaining what they are, when to use them, which scratchpad keys control their behavior, or how operators interact with them. Ship per-feature operator guide sections in the framework README, extend **Full scratchpad reference** with sovereign-loop keys, preserve catalog anchors (US-0091), keep framework README parity (US-0097/US-0017).
- Decomposition (US-0051): Operator explicit request broadened scope → 5-story decomposition by functional family. **US-0113 = sovereign-loop family** (US-0103-0112).
- related_us: US-0103, US-0104, US-0105, US-0107, US-0108, US-0109, US-0110, US-0111, US-0112, US-0091, US-0097, US-0114, US-0115, US-0116, US-0117
- Acceptance (8 ACs — sovereign-loop operator docs):
  - [ ] AC-1: ### Sovereign-loop era (US-0103–US-0112) umbrella section under ## Commands and workflow
  - [ ] AC-2: Per-feature operator subsections for US-0103/US-0104/US-0105/US-0107/US-0108/US-0109/US-0110/US-0111/US-0112
  - [ ] AC-3: Full scratchpad reference extension
  - [ ] AC-4: Coverage preserved
  - [ ] AC-5: Framework README parity
  - [ ] AC-6: Audience + metadata hygiene
  - [ ] AC-7: Runbook cross-links
  - [ ] AC-8: Regression tests
- intake_notes (2026-07-03, PO): Decomposition → 5 stories by functional family. **Status: OPEN** per US-0045.

## US-0114 — Release & distribution operator documentation in framework README
- Status: OPEN
- user_visible: true
- Title: Add operator documentation for release & distribution family (US-0111, US-0112, US-0041, US-0062)
- Summary: Close the operator-documentation gap for the **release & distribution** functional family — US-0111 (Release trigger adapters), US-0112 (Model-catalog example presets), US-0041 (End-to-end lifecycle QA), US-0062 (`its_magic/` folder for framework metadata). Ship per-feature operator guide sections, extend scratchpad reference, preserve catalog anchors, keep framework README parity.
- Decomposition (US-0051): Operator request broadened US-0111 scope → 5-story decomposition. **US-0114 = release & distribution family**.
- related_us: US-0111, US-0112, US-0041, US-0062, US-0091, US-0097, US-0113, US-0115, US-0116, US-0117
- Acceptance (8 ACs — release & distribution operator docs):
  - [ ] AC-1: ### Release & distribution umbrella section under ## Commands and workflow
  - [ ] AC-2: Per-feature operator subsections for US-0111/US-0112/US-0041/US-0062
  - [ ] AC-3: Full scratchpad reference extension
  - [ ] AC-4: Coverage preserved
  - [ ] AC-5: Framework README parity
  - [ ] AC-6: Audience + metadata hygiene
  - [ ] AC-7: Runbook cross-links
  - [ ] AC-8: Regression tests
- intake_notes (2026-07-03, PO): Decomposition slice of US-0113. **Status: OPEN** per US-0045.

## US-0115 — Integration & observability operator documentation in framework README
- Status: OPEN
- user_visible: true
- Title: Add operator documentation for integration & observability family (US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102)
- Summary: Close the operator-documentation gap for the **integration & observability** functional family — US-0034 (Cross-repo compatibility observability), US-0084 (Codebase map freshness gate), US-0086 (Handoff hygiene validator), US-0093 (Scratchpad drift detector), US-0096 (Active context handoff), US-0101 (Model tier resolution), US-0102 (Role-based model catalog). Ship per-feature operator guide sections, extend scratchpad reference, preserve catalog anchors, keep framework README parity.
- Decomposition (US-0051): Operator request broadened US-0111 scope → 5-story decomposition. **US-0115 = integration & observability family**.
- related_us: US-0034, US-0084, US-0086, US-0093, US-0096, US-0101, US-0102, US-0091, US-0097, US-0113, US-0114, US-0116, US-0117
- Acceptance (8 ACs — integration & observability operator docs):
  - [ ] AC-1: ### Integration & observability umbrella section under ## Commands and workflow
  - [ ] AC-2: Per-feature operator subsections for US-0034/US-0084/US-0086/US-0093/US-0096/US-0101/US-0102
  - [ ] AC-3: Full scratchpad reference extension
  - [ ] AC-4: Coverage preserved
  - [ ] AC-5: Framework README parity
  - [ ] AC-6: Audience + metadata hygiene
  - [ ] AC-7: Runbook cross-links
  - [ ] AC-8: Regression tests
- intake_notes (2026-07-03, PO): Decomposition slice of US-0113. **Status: OPEN** per US-0045.

## US-0116 — Delivery & lifecycle operator documentation in framework README
- Status: OPEN
- user_visible: true
- Title: Add operator documentation for delivery & lifecycle family (US-0092, US-0095, US-0098, US-0099)
- Summary: Close the operator-documentation gap for the **delivery & lifecycle** functional family — US-0092 (Delivery confirmation gate), US-0095 (Lean memory per-story), US-0098 (Install-bootstrap pattern), US-0099 (Dev-environment copy-when-missing bootstrap). Ship per-feature operator guide sections, extend scratchpad reference, preserve catalog anchors, keep framework README parity.
- Decomposition (US-0051): Operator request broadened US-0111 scope → 5-story decomposition. **US-0116 = delivery & lifecycle family**.
- related_us: US-0092, US-0095, US-0098, US-0099, US-0091, US-0097, US-0113, US-0114, US-0115, US-0117
- Acceptance (8 ACs — delivery & lifecycle operator docs):
  - [ ] AC-1: ### Delivery & lifecycle umbrella section under ## Commands and workflow
  - [ ] AC-2: Per-feature operator subsections for US-0092/US-0095/US-0098/US-0099
  - [ ] AC-3: Full scratchpad reference extension
  - [ ] AC-4: Coverage preserved
  - [ ] AC-5: Framework README parity
  - [ ] AC-6: Audience + metadata hygiene
  - [ ] AC-7: Runbook cross-links
  - [ ] AC-8: Regression tests
- intake_notes (2026-07-03, PO): Decomposition slice of US-0113. **Status: OPEN** per US-0045.

## US-0117 — Phase & role governance operator documentation in framework README
- Status: OPEN
- user_visible: true
- Title: Add operator documentation for phase & role governance family (US-0069–US-0072, US-0075–US-0082, US-0083, US-0085, US-0087–US-0090)
- Summary: Close the operator-documentation gap for the **phase & role governance** functional family — US-0069 (Phase→role matrix), US-0070 (Phase selection policy), US-0071 (Metadata sanitization), US-0072 (Context slimming), US-0075 (Scratchpad example-first refresh), US-0076 (Codebase map), US-0077 (Delegation policy), US-0078 (Env file bootstrap), US-0079 (Bug queue routing), US-0080 (Auto quiet mode), US-0081 (Caveman mode), US-0082 (Input compression), US-0083 (Scratchpad delivery keys), US-0085 (Context fresh-context markers), US-0087 (Full-autonomy mode), US-0088 (Automation modes), US-0089 (Auto orchestration), US-0090 (Phase governance integration). Ship per-feature operator guide sections, extend scratchpad reference, preserve catalog anchors, keep framework README parity.
- Decomposition (US-0051): Operator request broadened US-0111 scope → 5-story decomposition. **US-0117 = phase & role governance family**.
- related_us: US-0069, US-0070, US-0071, US-0072, US-0075, US-0076, US-0077, US-0078, US-0079, US-0080, US-0081, US-0082, US-0083, US-0085, US-0087, US-0088, US-0089, US-0090, US-0091, US-0097, US-0113, US-0114, US-0115, US-0116
- Acceptance (8 ACs — phase & role governance operator docs):
  - [ ] AC-1: ### Phase & role governance umbrella section under ## Commands and workflow
  - [ ] AC-2: Per-feature operator subsections for US-0069/US-0070/US-0071/US-0072/US-0075/US-0076/US-0077/US-0078/US-0079/US-0080/US-0081/US-0082/US-0083/US-0085/US-0087/US-0088/US-0089/US-0090
  - [ ] AC-3: Full scratchpad reference extension
  - [ ] AC-4: Coverage preserved
  - [ ] AC-5: Framework README parity
  - [ ] AC-6: Audience + metadata hygiene
  - [ ] AC-7: Runbook cross-links
  - [ ] AC-8: Regression tests
- intake_notes (2026-07-03, PO): Decomposition slice of US-0113. **Status: OPEN** per US-0045.

"""
    
    # Insert the new content
    lines.insert(insert_line, new_content)
    
    with open('docs/product/backlog.md', 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    print(f"Successfully inserted US-0113 through US-0117 at line {insert_line + 1}")

if __name__ == '__main__':
    main()
