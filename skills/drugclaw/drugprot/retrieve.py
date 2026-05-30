#!/usr/bin/env python3
"""
Fixed retrieval CLI for DrugProt (Drug-Protein Interaction NLP).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or protein names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_entities, format_results


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query_entities(entities)
        print(format_results(results))
    except Exception as exc:
        print(f"[DrugProt] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
