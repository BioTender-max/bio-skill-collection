#!/usr/bin/env python3
"""
Fixed retrieval CLI for TarKG (Target Knowledge Graph).
Usage: python retrieve.py entity1 [entity2 ...]
Entities: drug names, gene/protein names, disease names
"""
import sys
import os

_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, _DIR)

from example import query_entities


def main():
    entities = sys.argv[1:]
    if not entities:
        print("Usage: retrieve.py entity1 [entity2 ...]", file=sys.stderr)
        sys.exit(1)

    try:
        results = query_entities(entities)
        for result in results:
            entity = result.get("query", "?")
            if not result.get("matched"):
                print(f"=== TarKG results for '{entity}': not found ===")
                continue
            node = result.get("node_info", {})
            out_edges = result.get("outgoing_edges", [])
            in_edges = result.get("incoming_edges", [])
            print(f"=== TarKG results for '{entity}' ===")
            print(f"  Node: {node}")
            if out_edges:
                print(f"  Outgoing ({len(out_edges)}):")
                for e in out_edges[:10]:
                    print(f"    {e.get('head_id', '?')} --{e.get('relation', '?')}--> "
                          f"{e.get('tail_name', e.get('tail_id', '?'))}")
            if in_edges:
                print(f"  Incoming ({len(in_edges)}):")
                for e in in_edges[:10]:
                    print(f"    {e.get('head_name', e.get('head_id', '?'))} "
                          f"--{e.get('relation', '?')}--> {e.get('tail_id', '?')}")
    except Exception as exc:
        print(f"[TarKG] Error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
