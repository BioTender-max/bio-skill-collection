#!/usr/bin/env python3
"""
Fixed retrieval CLI for GDSC (Genomics of Drug Sensitivity in Cancer).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, cell line names, gene targets
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_gdsc


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query_gdsc(entities)
        for res in results:
            src = res.get("source", "?")
            count = res.get("match_count", 0)
            print(f"=== GDSC [{src}]: {count} match(es) ===")
            for row in res.get("matches", [])[:10]:
                print(f"  {row}")
    except Exception as exc:
        print(f"[GDSC] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
