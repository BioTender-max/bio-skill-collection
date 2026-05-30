"""
UniD3 - Drug Discovery Knowledge Graph Query Tool
Category: Drug-centric | Type: KG | Subcategory: Drug Knowledgebase
Source: https://github.com/QSong-github/UniD3

Multi-KG from 150,000+ PubMed articles. 6 GraphML files covering
drug-disease matching, effectiveness assessment, and drug-target analysis.


6 KGs: UniD3_L1T1.graphml  UniD3_L1T3.graphml  UniD3_L2T2.graphml
UniD3_L1T2.graphml  UniD3_L2T1.graphml  UniD3_L2T3.graphml
"""

import os, glob
from pathlib import Path
import networkx as nx
from typing import Union, Optional

DATA_DIR = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_knowledgebase"
    / "UniD3"
)

# ── Internals ────────────────────────────────────────────────────────────────

def _strip(s):
    return s.strip('"') if isinstance(s, str) else s

def _norm(name):
    return _strip(name).strip().upper()

def _graphml_files(graph_names=None):
    all_f = sorted(glob.glob(os.path.join(DATA_DIR, "*.graphml")))
    if not all_f:
        raise FileNotFoundError(f"No .graphml files in {DATA_DIR}")
    if graph_names is None:
        return all_f
    avail = {os.path.splitext(os.path.basename(f))[0]: f for f in all_f}
    out = []
    for n in graph_names:
        if n not in avail:
            raise ValueError(f"'{n}' not found. Available: {list(avail)}")
        out.append(avail[n])
    return out

def _node_info(G, nid):
    a = G.nodes[nid]
    return dict(entity=_strip(nid), entity_type=_strip(a.get("entity_type","")),
                description=_strip(a.get("description","")), source_id=a.get("source_id",""))

def _edge_info(G, u, v):
    a = G.edges[u, v]
    return dict(source=_strip(u), target=_strip(v), weight=a.get("weight"),
                description=_strip(a.get("description","")),
                keywords=_strip(a.get("keywords","")), source_id=a.get("source_id",""))

# ── Public API ───────────────────────────────────────────────────────────────

def list_graphs() -> list[str]:
    """Return names of all available GraphML files (without extension)."""
    return [os.path.splitext(os.path.basename(f))[0]
            for f in sorted(glob.glob(os.path.join(DATA_DIR, "*.graphml")))]


def query_entities(entities: Union[str, list[str]],
                   graph_names: Optional[list[str]] = None) -> list[dict]:
    """Look up entities by name (case-insensitive). Returns node info per graph."""
    if isinstance(entities, str):
        entities = [entities]
    targets = {_norm(e) for e in entities}
    results = []
    for path in _graphml_files(graph_names):
        gname = os.path.splitext(os.path.basename(path))[0]
        G = nx.read_graphml(path)
        for nid in G.nodes:
            if _norm(nid) in targets:
                info = _node_info(G, nid)
                info["graph"] = gname
                results.append(info)
    return results


def get_neighbors(entity: str,
                  graph_names: Optional[list[str]] = None) -> list[dict]:
    """Return direct neighbors and edge info for an entity."""
    target = _norm(entity)
    results = []
    for path in _graphml_files(graph_names):
        gname = os.path.splitext(os.path.basename(path))[0]
        G = nx.read_graphml(path)
        mid = next((n for n in G.nodes if _norm(n) == target), None)
        if mid is None:
            continue
        for nbr in G.neighbors(mid):
            results.append(dict(graph=gname, neighbor=_node_info(G, nbr),
                                edge=_edge_info(G, mid, nbr)))
    return results


def search_by_type(entity_type: str,
                   graph_names: Optional[list[str]] = None,
                   limit: int = 50) -> list[dict]:
    """Find entities of a given type (e.g. DISEASE, DRUG, GENE)."""
    t = entity_type.strip().upper()
    results = []
    for path in _graphml_files(graph_names):
        gname = os.path.splitext(os.path.basename(path))[0]
        G = nx.read_graphml(path)
        for nid, a in G.nodes(data=True):
            if _norm(a.get("entity_type", "")) == t:
                info = _node_info(G, nid)
                info["graph"] = gname
                results.append(info)
                if len(results) >= limit:
                    return results
    return results


def search_by_keyword(keyword: str,
                      graph_names: Optional[list[str]] = None,
                      limit: int = 50) -> list[dict]:
    """Substring search over entity names and descriptions."""
    kw = keyword.strip().upper()
    results = []
    for path in _graphml_files(graph_names):
        gname = os.path.splitext(os.path.basename(path))[0]
        G = nx.read_graphml(path)
        for nid, a in G.nodes(data=True):
            if kw in _norm(nid) or kw in _strip(a.get("description","")).upper():
                info = _node_info(G, nid)
                info["graph"] = gname
                results.append(info)
                if len(results) >= limit:
                    return results
    return results


if __name__ == "__main__":
    print("Graphs:", list_graphs())
    hits = query_entities("RESPIRATORY DISEASES")
    print(f"\nquery_entities('RESPIRATORY DISEASES') → {len(hits)} hit(s)")
    for h in hits[:3]:
        print(f"  [{h['graph']}] {h['entity']} ({h['entity_type']}): {h['description']}")
    nbrs = get_neighbors("CALVES")
    print(f"\nget_neighbors('CALVES') → {len(nbrs)} neighbor(s)")
    for n in nbrs[:5]:
        print(f"  [{n['graph']}] → {n['neighbor']['entity']} ({n['neighbor']['entity_type']})")
