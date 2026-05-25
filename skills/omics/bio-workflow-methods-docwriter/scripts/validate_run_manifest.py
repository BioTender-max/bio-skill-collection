#!/usr/bin/env python3
"""Validate a run manifest (YAML or JSON) against schemas/run-manifest.schema.json.

Usage:
  python scripts/validate_run_manifest.py run_manifest.yaml
"""

import json
import sys
from pathlib import Path

import jsonschema
import yaml


def load_obj(path: Path):
    text = path.read_text()
    if path.suffix.lower() in {'.yml', '.yaml'}:
        return yaml.safe_load(text)
    return json.loads(text)


def main():
    if len(sys.argv) != 2:
        print("ERROR: Provide a manifest path (YAML or JSON).", file=sys.stderr)
        sys.exit(2)

    manifest_path = Path(sys.argv[1]).resolve()
    if not manifest_path.exists():
        print(f"ERROR: Not found: {manifest_path}", file=sys.stderr)
        sys.exit(2)

    schema_path = Path(__file__).resolve().parents[1] / 'schemas' / 'run-manifest.schema.json'
    schema = json.loads(schema_path.read_text())

    manifest = load_obj(manifest_path)

    try:
        jsonschema.validate(instance=manifest, schema=schema)
    except jsonschema.ValidationError as e:
        print("VALIDATION FAILED:\n")
        print(e.message)
        if e.path:
            print(f"\nAt: {'/'.join([str(p) for p in e.path])}")
        sys.exit(1)

    print("OK: manifest validates against run-manifest.schema.json")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
