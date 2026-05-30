#!/usr/bin/env python3
"""
Fixed retrieval CLI for KEGG Drug (Drug-Drug Interactions & Targets).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or KEGG Drug IDs (e.g. D00109)
"""
import sys
import os
import json

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query(entities)
        for rec in results:
            entity = rec.get("entity", "?")
            print(f"=== KEGG Drug results for '{entity}' ===")
            if "error" in rec:
                print(f"  Error: {rec['error']}")
                continue
            entries = rec.get("entries", [])
            for e in entries[:5]:
                name = e.get("name", "?")
                targets = e.get("targets", [])
                interactions = e.get("interactions", [])
                print(f"  Drug: {name}")
                if targets:
                    print(f"  Targets: {', '.join(str(t) for t in targets[:5])}")
                if interactions:
                    print(f"  Interactions: {', '.join(str(i) for i in interactions[:5])}")
    except Exception as exc:
        print(f"[KEGG Drug] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
