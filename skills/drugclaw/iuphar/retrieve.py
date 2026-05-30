#!/usr/bin/env python3
"""
Fixed retrieval CLI for IUPHAR/BPS Guide to Pharmacology.
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug/ligand names or target names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_entities, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query_entities(entities)
        for entity, result in results.items():
            print(summarize(result))
    except Exception as exc:
        print(f"[IUPHAR] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
