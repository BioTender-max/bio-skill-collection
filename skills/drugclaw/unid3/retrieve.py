#!/usr/bin/env python3
"""
Fixed retrieval CLI for UniD3 (Drug Discovery Knowledge Graph).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, disease names, gene names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_entities, get_neighbors


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        for entity in entities:
            print(f"=== UniD3 results for '{entity}' ===")
            nodes = query_entities(entity)
            if nodes:
                print(f"  Found in {len(nodes)} graph(s):")
                for n in nodes[:5]:
                    print(f"  [{n.get('graph', '?')}] {n.get('entity', '?')} "
                          f"({n.get('entity_type', '?')}) | {n.get('description', '')[:100]}")
            neighbors = get_neighbors(entity)
            if neighbors:
                print(f"  Neighbors ({len(neighbors)}):")
                for nb in neighbors[:10]:
                    g = nb.get("graph", "?")
                    tgt = nb.get("neighbor", {})
                    edge = nb.get("edge", {})
                    desc = edge.get("description", "")[:80]
                    print(f"  [{g}] --> {tgt.get('entity', '?')} ({tgt.get('entity_type', '?')}) | {desc}")
            if not nodes and not neighbors:
                print("  No results found.")
    except Exception as exc:
        print(f"[UniD3] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
