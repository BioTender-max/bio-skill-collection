#!/usr/bin/env python3
"""
Fixed retrieval CLI for DILIrank (Drug-Induced Liver Injury Ranking).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names (e.g. acetaminophen, isoniazid)
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import load_all, search_batch, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        data = load_all()
        results = search_batch(data, entities)
        for entity, result in results.items():
            print(summarize(result, entity))
    except Exception as exc:
        print(f"[DILIrank] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
