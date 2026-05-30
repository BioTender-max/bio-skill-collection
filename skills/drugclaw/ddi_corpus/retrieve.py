#!/usr/bin/env python3
"""
Fixed retrieval CLI for DDI Corpus 2013 (Drug-Drug Interaction NLP).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_entities


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        result = query_entities(entities)
        print(result)
    except Exception as exc:
        print(f"[DDI Corpus] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
