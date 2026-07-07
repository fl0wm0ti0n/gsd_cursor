#!/usr/bin/env python3
"""Validator: US-0120 closure-verification.md schema

Required fields (Q6 LOCKED, .md format):
- story_id (US-XXXX pattern)
- closure_date (ISO-8601 UTC)
- closure_role (qe|curator)
- pre_closure_status (OPEN)
- post_closure_status (DONE)
- release_evidence_refs[] (array of paths)
- isolation_evidence{} (object)
- runtime_proof{} (object)

Optional fields:
- normalization_notes
- backward_compat_note

Exit 0 / 1.
"""

import argparse
import json
import re
import sys
from pathlib import Path

STORY_ID_RE = re.compile(r'^US-\d{4}$')
ISO_DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$')

REQUIRED_FIELDS = [
    'story_id',
    'closure_date',
    'closure_role',
    'pre_closure_status',
    'post_closure_status',
    'release_evidence_refs',
    'isolation_evidence',
    'runtime_proof',
]

OPTIONAL_FIELDS = [
    'normalization_notes',
    'backward_compat_note',
]


def parse_md_frontmatter(text: str) -> dict:
    """Parse YAML-like frontmatter from .md file."""
    if not text.startswith('---'):
        return {}
    
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}
    
    frontmatter = {}
    for line in parts[1].strip().splitlines():
        line = line.strip()
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            
            # Try to parse as JSON for arrays and objects
            if value.startswith('[') or value.startswith('{'):
                try:
                    value = json.loads(value)
                except json.JSONDecodeError:
                    pass
            
            # Strip quotes
            if isinstance(value, str) and len(value) >= 2 and value[0] == value[-1] and value[0] in ('"', "'"):
                value = value[1:-1]
            
            frontmatter[key] = value
    
    return frontmatter


def validate_story_id(value: str) -> bool:
    return bool(STORY_ID_RE.match(value))


def validate_closure_date(value: str) -> bool:
    return bool(ISO_DATE_RE.match(value))


def validate_closure_role(value: str) -> bool:
    return value in ('qe', 'curator')


def validate_pre_status(value: str) -> bool:
    return value == 'OPEN'


def validate_post_status(value: str) -> bool:
    return value == 'DONE'


def validate_release_evidence_refs(value) -> bool:
    if isinstance(value, list):
        return all(isinstance(ref, str) and ref.strip() for ref in value)
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return isinstance(parsed, list) and all(isinstance(r, str) for r in parsed)
        except:
            return False
    return False


def validate_isolation_evidence(value) -> bool:
    if isinstance(value, dict):
        required_keys = {'phase_id', 'role', 'fresh_context_marker', 'timestamp', 'evidence_ref'}
        return required_keys.issubset(value.keys())
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return isinstance(parsed, dict)
        except:
            return False
    return False


def validate_runtime_proof(value) -> bool:
    if isinstance(value, dict):
        required_keys = {'runtime_proof_id', 'proof_hash', 'proof_ttl'}
        return required_keys.issubset(value.keys())
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
            return isinstance(parsed, dict)
        except:
            return False
    return False


VALIDATORS = {
    'story_id': validate_story_id,
    'closure_date': validate_closure_date,
    'closure_role': validate_closure_role,
    'pre_closure_status': validate_pre_status,
    'post_closure_status': validate_post_status,
    'release_evidence_refs': validate_release_evidence_refs,
    'isolation_evidence': validate_isolation_evidence,
    'runtime_proof': validate_runtime_proof,
}


def validate(file_path: str, silent: bool = False) -> tuple[bool, list[str]]:
    """Validate closure-verification.md file. Returns (pass, errors)."""
    path = Path(file_path)
    
    if not path.exists():
        return False, [f"File not found: {file_path}"]
    
    try:
        text = path.read_text(encoding='utf-8')
    except Exception as e:
        return False, [f"Failed to read file: {e}"]
    
    frontmatter = parse_md_frontmatter(text)
    
    errors = []
    
    # Check required fields exist
    for field in REQUIRED_FIELDS:
        if field not in frontmatter:
            errors.append(f"Missing required field: {field}")
            continue
        
        value = frontmatter[field]
        
        # Check optional fields don't need validation
        if field in OPTIONAL_FIELDS:
            continue
        
        validator = VALIDATORS.get(field)
        if validator and not validator(value):
            errors.append(f"Invalid value for {field}: {value}")
    
    # Check for optional unrecognized fields? No, schema allows extras for extensibility
    
    if not silent:
        if errors:
            print(f"[VALIDATE_CLOSURE_VERIFICATION_FAIL] {file_path}", file=sys.stderr)
            for err in errors:
                print(f"  - {err}", file=sys.stderr)
        else:
            print(f"[VALIDATE_CLOSURE_VERIFICATION_OK] {file_path}")
    
    return len(errors) == 0, errors


def main():
    parser = argparse.ArgumentParser(description='Validate closure-verification.md (US-0120)')
    parser.add_argument('file', nargs='?', help='Path to closure-verification.md')
    parser.add_argument('--self-test', action='store_true', help='Self-test validator schema enforcement')
    parser.add_argument('--silent', action='store_true', help='Silent mode (exit code only)')
    
    args = parser.parse_args()
    
    if args.self_test:
        # Self-test: validate schema enforcement
        test_cases = [
            # Valid case
            ('valid', {
                'story_id': 'US-0120',
                'closure_date': '2026-07-07T22:00:00Z',
                'closure_role': 'qe',
                'pre_closure_status': 'OPEN',
                'post_closure_status': 'DONE',
                'release_evidence_refs': ['handoffs/releases/S0120-release-notes.md'],
                'isolation_evidence': {
                    'phase_id': 'closure',
                    'role': 'qe',
                    'fresh_context_marker': 'qe-US0120-closure-20260707T220000Z-fresh',
                    'timestamp': '2026-07-07T22:00:00Z',
                    'evidence_ref': 'sprints/S0120/closure-verification.md'
                },
                'runtime_proof': {
                    'runtime_proof_id': 'rp-auto-20260707-execute-qe-20260707T220000Z-US-0120',
                    'proof_hash': 'a' * 64,
                    'proof_ttl': '2026-07-07T23:00:00Z'
                }
            }, True),
            
            # Invalid story_id
            ('invalid_story_id', {
                'story_id': 'US-abc',
                'closure_date': '2026-07-07T22:00:00Z',
                'closure_role': 'qe',
                'pre_closure_status': 'OPEN',
                'post_closure_status': 'DONE',
                'release_evidence_refs': ['path'],
                'isolation_evidence': {'phase_id': 'x'},
                'runtime_proof': {'runtime_proof_id': 'x'}
            }, False),
            
            # Invalid role
            ('invalid_role', {
                'story_id': 'US-0120',
                'closure_date': '2026-07-07T22:00:00Z',
                'closure_role': 'dev',
                'pre_closure_status': 'OPEN',
                'post_closure_status': 'DONE',
                'release_evidence_refs': ['path'],
                'isolation_evidence': {'phase_id': 'x'},
                'runtime_proof': {'runtime_proof_id': 'x'}
            }, False),
            
            # Missing required field
            ('missing_field', {
                'story_id': 'US-0120',
                'closure_date': '2026-07-07T22:00:00Z'
            }, False),
        ]
        
        all_pass = True
        for name, mock_data, expected_pass in test_cases:
            # Test validation logic directly
            result = True
            errors_list = []
            
            # Check story_id
            if 'story_id' in mock_data:
                if not validate_story_id(mock_data['story_id']):
                    result = False
            
            # Check closure_role
            if 'closure_role' in mock_data:
                if not validate_closure_role(mock_data['closure_role']):
                    result = False
            
            # Check missing required fields
            for field in REQUIRED_FIELDS:
                if field not in mock_data:
                    errors_list.append(f"Missing required field: {field}")
            
            if errors_list:
                result = False
            
            if result != expected_pass:
                print(f"SELF_TEST_FAIL {name}: expected={expected_pass} got={result}", file=sys.stderr)
                all_pass = False
            else:
                print(f"SELF_TEST_OK {name}")
        
        if all_pass:
            print("[VALIDATE_CLOSURE_VERIFICATION_SELF_TEST_OK]")
            return 0
        else:
            print("[VALIDATE_CLOSURE_VERIFICATION_SELF_TEST_FAIL]", file=sys.stderr)
            return 1
    
    if not args.file:
        parser.error("file argument required (or use --self-test)")
    
    passed, errors = validate(args.file, silent=args.silent)
    return 0 if passed else 1


if __name__ == '__main__':
    sys.exit(main())
