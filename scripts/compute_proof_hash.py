#!/usr/bin/env python3
import hashlib
import json
import sys

payload = {
    "orchestrator_run_id": "auto-20260628-04",
    "phase_id": "discovery",
    "proof_issued_at": "2026-06-28T18:04:00Z",
    "proof_ttl_seconds": 3600,
    "role": "po",
    "runtime_proof_id": "rp-auto-20260628-04-discovery-po-20260628T180400Z-US0106"
}

canonical_json = json.dumps(payload, sort_keys=True)
proof_hash = hashlib.sha256(canonical_json.encode()).hexdigest()

print(f"Canonical JSON: {canonical_json}")
print(f"Proof hash: {proof_hash}")
