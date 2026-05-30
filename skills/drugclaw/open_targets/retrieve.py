#!/usr/bin/env python3
"""
Fixed retrieval CLI for Open Targets Platform (Drug-Target Associations).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, gene names, disease names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_batch, summarize


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query_batch(entities)
        for result in results:
            print(summarize(result))
    except Exception as exc:
        print(f"[Open Targets] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
