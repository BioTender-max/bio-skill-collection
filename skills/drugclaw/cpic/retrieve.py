#!/usr/bin/env python3
"""
Fixed retrieval CLI for CPIC (Clinical Pharmacogenomics Implementation Consortium).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or gene names
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
            print(f"=== CPIC results for '{entity}' ===")
            if "error" in rec:
                print(f"  Error: {rec['error']}")
                continue
            drug_info = rec.get("drug_info", [])
            guidelines = rec.get("guidelines", [])
            for d in drug_info[:3]:
                print(f"  Drug: {d.get('name', '?')} | {d.get('drugbankId', '')}")
            for g in guidelines[:5]:
                print(f"  Guideline: {g.get('name', '?')} | Genes: {g.get('genes', [])}")
    except Exception as exc:
        print(f"[CPIC] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
