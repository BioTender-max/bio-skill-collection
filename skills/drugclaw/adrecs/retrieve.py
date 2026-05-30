#!/usr/bin/env python3
"""
Fixed retrieval CLI for ADReCS (Adverse Drug Reaction Classification System).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, BADD IDs, DrugBank IDs, ATC codes, ADR terms, etc.
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import (
    load_drug_adr, load_drug_info, load_adr_ontology,
    search_batch, summarize,
)


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        da = load_drug_adr()
        di = load_drug_info()
        ao = load_adr_ontology()
        results = search_batch(entities, drug_adr_df=da, drug_info_df=di, adr_ont_df=ao)
        for entity, hits in results.items():
            print(summarize(hits, entity))
    except Exception as exc:
        print(f"[ADReCS] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
