#!/usr/bin/env python3
"""
Fixed retrieval CLI for ChEMBL (Drug Bioactivity and Target Database).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, ChEMBL IDs (CHEMBL###), or gene names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import (
    query_molecules, query_targets,
    summarize_molecule, summarize_target,
)


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        print("=== ChEMBL Molecule Results ===")
        mol_results = query_molecules(entities, limit=3)
        for entity, mols in mol_results.items():
            print(f"  [{entity}]")
            for mol in mols:
                if "error" not in mol:
                    print(f"    {summarize_molecule(mol)}")
                else:
                    print(f"    Error: {mol['error']}")

        print("=== ChEMBL Target Results ===")
        tgt_results = query_targets(entities, limit=3)
        for entity, tgts in tgt_results.items():
            print(f"  [{entity}]")
            for tgt in tgts:
                if "error" not in tgt:
                    print(f"    {summarize_target(tgt)}")
                else:
                    print(f"    Error: {tgt['error']}")
    except Exception as exc:
        print(f"[ChEMBL] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
