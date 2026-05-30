#!/usr/bin/env python3
"""
Fixed retrieval CLI for DrugMechDB (Drug Mechanism of Action).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, disease names, DrugBank IDs, MESH IDs
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import load, build_index, search_batch, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        db = load()
        index = build_index(db)
        results = search_batch(db, entities, index=index)
        for entity, paths in results.items():
            print(summarize(paths, entity))
    except Exception as exc:
        print(f"[DrugMechDB] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
