#!/usr/bin/env python3
"""
Fixed retrieval CLI for PharmGKB/ClinPGx (Pharmacogenomics).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, gene symbols (e.g. CYP2D6), or variant rsIDs
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import search, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        for entity in entities:
            result = search(entity)
            print(summarize(result, entity))
    except Exception as exc:
        print(f"[PharmGKB] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
