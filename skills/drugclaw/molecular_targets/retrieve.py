#!/usr/bin/env python3
"""
Fixed retrieval CLI for Molecular Targets (EBI Open Targets Platform).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, gene names, disease names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import search_batch, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = search_batch(entities)
        for entity, data in results.items():
            print(summarize(data, entity))
    except Exception as exc:
        print(f"[Molecular Targets] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
