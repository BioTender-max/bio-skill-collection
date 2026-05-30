#!/usr/bin/env python3
"""
Fixed retrieval CLI for LiverTox (Liver Toxicity Knowledge Base).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names (e.g. acetaminophen, amoxicillin)
"""
import sys
import os
import json

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import lookup_entities


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = lookup_entities(entities)
        for entity, matches in results.items():
            print(f"=== LiverTox results for '{entity}' ({len(matches)} sections) ===")
            for m in matches:
                section = m.get("section", "?")
                snippet = m.get("snippet", "")[:200]
                print(f"  [{section}] {snippet}")
    except Exception as exc:
        print(f"[LiverTox] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
