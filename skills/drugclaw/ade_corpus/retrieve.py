#!/usr/bin/env python3
"""
Fixed retrieval CLI for ADE Corpus V2 (Adverse Drug Events).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or adverse event terms
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import ADECorpus


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        corpus = ADECorpus()
        result = corpus.query(entities)
        print(result)
    except Exception as exc:
        print(f"[ADE Corpus] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
