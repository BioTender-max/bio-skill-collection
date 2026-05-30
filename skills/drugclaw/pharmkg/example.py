"""
PharmKG - Pharmacology Knowledge Graph Benchmark
Category: Drug-centric | Type: KG | Subcategory: Drug Knowledgebase
Link: https://github.com/MindRank-Biotech/PharmKG
Paper: https://academic.oup.com/bib/article/22/4/bbaa344/6042240

PharmKG is a multi-relational, attributed biomedical knowledge graph benchmark
integrating gene-disease, chemical-gene, chemical-disease, and chemical-chemical
relationships.  ~188 k entities, 39 relation types, >1 M triples.

Access method: Local CSV (raw_PharmKG-180k.csv).
"""

import csv
import json
import sys
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Optional, Tuple

# PharmKG CSV contains entity-embedding columns with very long values.
csv.field_size_limit(sys.maxsize)

DATA_PATH = str(
    Path(__file__).resolve().parents[3]
    / "resources_metadata"
    / "drug_knowledgebase"
    / "PharmKG"
    / "raw_PharmKG-180k.csv"
)

# Triple stored as lightweight (entity1, relation, entity2) tuple.
Triple = Tuple[str, str, str]


# ── load ────────────────────────────────────────────────────────────────────

def load_pharmkg(path: str = DATA_PATH) -> List[Triple]:
    """Load PharmKG CSV into a list of (entity1, relation, entity2) tuples.

    Only the three name/relation columns are kept; embedding columns are
    skipped to save memory on this >1 M-row file.
    """
    triples: List[Triple] = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            triples.append((
                row["Entity1_name"].strip(),
                row["relationship_type"].strip(),
                row["Entity2_name"].strip(),
            ))
    return triples


def _build_index(triples: List[Triple]) -> Dict[str, List[int]]:
    """Build a case-insensitive entity→row-index list for fast lookup."""
    idx: Dict[str, List[int]] = defaultdict(list)
    for i, (e1, _rel, e2) in enumerate(triples):
        idx[e1.lower()].append(i)
        idx[e2.lower()].append(i)
    return idx


# ── search ──────────────────────────────────────────────────────────────────

def _triple_to_dict(t: Triple) -> dict:
    return {"entity1": t[0], "relation": t[1], "entity2": t[2]}


def search(
    triples: List[Triple],
    entity: str,
    index: Optional[Dict[str, List[int]]] = None,
) -> List[dict]:
    """Return all triples where *entity* appears as head or tail.

    If an index is supplied (from ``_build_index``), uses O(1) lookup.
    Otherwise falls back to a linear scan with case-insensitive substring
    matching.  Results are returned as list[dict] for readability.
    """
    q = entity.strip().lower()
    if not q:
        return []

    # Exact match via index
    if index is not None:
        row_ids = index.get(q, [])
        if row_ids:
            seen = set(row_ids)
            return [_triple_to_dict(triples[i]) for i in seen]

    # Fallback: substring scan
    results = []
    for t in triples:
        if q in t[0].lower() or q in t[2].lower():
            results.append(_triple_to_dict(t))
    return results


def search_batch(
    triples: List[Triple],
    entities: List[str],
    index: Optional[Dict[str, List[int]]] = None,
) -> Dict[str, List[dict]]:
    """Search multiple entities. Returns {entity: [triples]}."""
    return {e: search(triples, e, index=index) for e in entities}


# ── output helpers ──────────────────────────────────────────────────────────

def summarize(hits: list, entity: str) -> str:
    """Compact, LLM-readable summary of triples for *entity*.

    Format per line:
        (Entity1) --[relation]--> (Entity2)
    Grouped by relation type, capped at 200 lines.
    """
    if not hits:
        return f"{entity}: no triples found."

    by_rel: Dict[str, list] = defaultdict(list)
    for t in hits:
        by_rel[t["relation"]].append(t)

    lines = [f"{entity}: {len(hits)} triple(s), {len(by_rel)} relation type(s)"]
    cap = 200
    n = 0
    for rel, ts in sorted(by_rel.items(), key=lambda kv: -len(kv[1])):
        lines.append(f"  [{rel}] ({len(ts)})")
        for t in ts[:20]:
            lines.append(f"    ({t['entity1']}) --[{rel}]--> ({t['entity2']})")
            n += 1
            if n >= cap:
                lines.append(f"  ... truncated at {cap} lines")
                return "\n".join(lines)
        if len(ts) > 20:
            lines.append(f"    ... +{len(ts) - 20} more")
    return "\n".join(lines)


def to_json(hits: list) -> str:
    """Return triples as a JSON string."""
    return json.dumps(hits, ensure_ascii=False, indent=2)


# ── main examples ───────────────────────────────────────────────────────────

if __name__ == "__main__":
    data = load_pharmkg()
    idx = _build_index(data)
    print(f"Loaded {len(data)} triples, index has {len(idx)} unique entities.\n")

    # Single entity search
    for q in ["aspirin", "metformin", "BRCA1", "Alzheimer Disease"]:
        hits = search(data, q, index=idx)
        print(summarize(hits, q))
        print()

    # Batch search
    batch = search_batch(data, ["ibuprofen", "TP53"], index=idx)
    for ent, hits in batch.items():
        print(summarize(hits, ent))
        print()

    # JSON output (first 3 triples of aspirin)
    aspirin_hits = search(data, "aspirin", index=idx)
    print("JSON (first 3):")
    print(to_json(aspirin_hits[:3]))
