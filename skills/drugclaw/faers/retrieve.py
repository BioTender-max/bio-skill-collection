#!/usr/bin/env python3
"""
Fixed retrieval CLI for FAERS (FDA Adverse Event Reporting System).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names (e.g. aspirin, ibuprofen)
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import count_reactions_batch, summarize_reactions


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        batch = count_reactions_batch(entities, top_n=10)
        for drug, rxns in batch.items():
            print(summarize_reactions(rxns, drug))
    except Exception as exc:
        print(f"[FAERS] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
