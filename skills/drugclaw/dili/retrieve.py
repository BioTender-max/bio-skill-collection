#!/usr/bin/env python3
"""
Fixed retrieval CLI for DILI (Drug-Induced Liver Injury datasets).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names (e.g. acetaminophen, isoniazid)
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_dili


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query_dili(entities)
        for res in results:
            if "error" in res:
                print(f"[DILI] {res['error']}")
                continue
            src = res.get("source", "?")
            count = res.get("match_count", 0)
            print(f"=== DILI [{src}]: {count} match(es) ===")
            for row in res.get("matches", [])[:10]:
                print(f"  {row}")
    except Exception as exc:
        print(f"[DILI] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
