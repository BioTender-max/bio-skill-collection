#!/usr/bin/env python3
"""
Fixed retrieval CLI for FDA Orange Book.
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names (e.g. aspirin, metformin)
"""
import sys
import os
import json

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import search_approved_drugs


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        for entity in entities:
            print(f"=== FDA Orange Book results for '{entity}' ===")
            result = search_approved_drugs(entity, limit=5)
            if isinstance(result, dict):
                results_list = result.get("results", [])
                total = result.get("meta", {}).get("results", {}).get("total", "?")
                print(f"  Total: {total}")
                for r in results_list[:5]:
                    appl = r.get("application_number", "?")
                    prod = r.get("products", [{}])
                    brand = prod[0].get("brand_name", "?") if prod else "?"
                    ing = r.get("sponsor_name", "?")
                    print(f"  {brand} | App#: {appl} | Sponsor: {ing}")
            else:
                print(f"  {result}")
    except Exception as exc:
        print(f"[FDA Orange Book] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
