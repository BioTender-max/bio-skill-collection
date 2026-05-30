#!/usr/bin/env python3
"""
Fixed retrieval CLI for DrugRepoBank (Drug Repurposing Bank).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or DrugBank IDs
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
        tables = load_all()
        results = search_batch(tables, entities)
        for entity, result in results.items():
            print(summarize(result))
    except Exception as exc:
        print(f"[DrugRepoBank] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
