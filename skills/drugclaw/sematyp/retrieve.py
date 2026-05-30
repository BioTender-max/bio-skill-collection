#!/usr/bin/env python3
"""
Fixed retrieval CLI for SemaTyP (Drug-Disease Association KG).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names or disease names
"""
import sys
import os
import json

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import get_predications, get_processed_drug_disease


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        for entity in entities:
            print(f"=== SemaTyP results for '{entity}' ===")
            preds = get_predications(entity, limit=10)
            if preds:
                print(f"  Predications ({len(preds)}):")
                for p in preds[:10]:
                    subj = p.get("subject", "?")
                    pred = p.get("predicate", "?")
                    obj = p.get("object", "?")
                    print(f"    {subj} --{pred}--> {obj}")
            dd = get_processed_drug_disease(entity)
            if dd:
                print(f"  Drug-Disease associations ({len(dd)}):")
                for item in dd[:10]:
                    print(f"    {item}")
            if not preds and not dd:
                print(f"  No results found.")
    except Exception as exc:
        print(f"[SemaTyP] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
