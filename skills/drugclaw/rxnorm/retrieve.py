#!/usr/bin/env python3
"""
Fixed retrieval CLI for RxNorm (Drug Ontology & Interactions).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names (e.g. aspirin, metformin)
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query(entities)
        print(summarize(results))
    except Exception as exc:
        print(f"[RxNorm] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
