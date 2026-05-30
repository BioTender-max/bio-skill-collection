#!/usr/bin/env python3
"""
Fixed retrieval CLI for TTD (Therapeutic Target Database).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, target names, or disease names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_json


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        result = query_json(entities)
        print(result)
    except Exception as exc:
        print(f"[TTD] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
