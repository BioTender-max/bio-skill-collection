#!/usr/bin/env python3
"""
Fixed retrieval CLI for DrugComb (Drug Combination Synergy).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or cell line names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import load_drugcomb, search_batch, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_drugcomb()
        results = search_batch(data, entities)
        for entity, hits in results.items():
            print(summarize(hits, entity))
    except Exception as exc:
        print(f"[DrugComb] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
